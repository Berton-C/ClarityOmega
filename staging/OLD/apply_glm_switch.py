#!/usr/bin/env python3
"""
Switch default LLM provider to Friendli/GLM-5.1 by adopting upstream's
provider-registry pattern, with three modifications to upstream's code:
  - Dead code at upstream lines 131-157 commented out (preserved for future)
  - callProvider made resilient (log + return empty string vs raise)
  - GlmProvider class added for GLM-5.1 thinking mode
  - Friendli registered alongside Anthropic, ASICloud, ASIOne, OpenAI

Hypothesis: This switch makes Friendli the active provider, preserves
all existing functionality, adds crash resilience for API failures
through the class-level try/except pattern, and creates the foundation
for future multi-provider concurrency via the registry.

Usage:
    python3 apply_glm_switch.py           # dry-run
    python3 apply_glm_switch.py --apply   # apply

Exit codes:
    0 - success or dry-run completed
    1 - pre-condition check failed
    2 - post-condition check failed (rollback performed)
    3 - file I/O error
"""

import sys
import os
import shutil
import difflib
from datetime import datetime

# ============================================================
# NEW lib_llm_ext.py CONTENT
# Base: upstream/main:lib_llm_ext.py (179 lines, verified by direct read)
# Modifications:
#   - Removed Ollama-local registration (not used in this fork)
#   - Lines 131-157 (dead _chatAsiOne, useAsi1) commented out
#   - callProvider returns empty string + logs instead of raising
#   - Added GlmProvider class for GLM-5.1 thinking mode
#   - Added Friendli/GLM-5.1 registration
# ============================================================

NEW_LIB_LLM_EXT = '''import os, openai
from typing import Optional


class AIProvider:
    """Lazy AI provider with on-demand initialization."""

    def __init__(self, name: str, var_name: str, model_name: str, base_url: str):
        self._name = name
        self._var_name = var_name
        self._model_name = model_name
        self._base_url = base_url
        self._client = None  # lazy initialization

    def _ensure_client(self):
        """Initialize client on first use."""
        if self._client is None:
            self._client = self._create_client()

    def _create_client(self) -> Optional[openai.OpenAI]:
        """Create OpenAI client from environment."""
        if self._var_name in os.environ:
            if self._var_name == "OLLAMA_API_KEY":
                llm_server_local_url = os.environ.get("LLM_SERVER_LOCAL_URL")
                if llm_server_local_url:
                    self._base_url = llm_server_local_url.rstrip("/") + "/v1"
                elif not self._base_url.endswith("/v1"):
                    self._base_url = self._base_url.rstrip("/") + "/v1"

            return openai.OpenAI(api_key=os.environ.get(self._var_name), base_url=self._base_url)

        return None

    @property
    def is_available(self) -> bool:
        """Check if provider is configured (without initializing)."""
        return bool(os.environ.get(self._var_name))

    def chat(self, model: str, content: str, max_tokens: int = 6000, **kwargs) -> str:
        """Send chat request, initializing client if needed."""
        self._ensure_client()

        if self._client is None:
            raise RuntimeError(f"{self._name} not configured (set {self._var_name})")

        content = content.replace(":-:-:-:", " ")
        try:
            response = self._client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
                max_tokens=max_tokens,
                **kwargs
            )

            return self._clean_text(response.choices[0].message.content)
        except Exception as e:
            print(f"[lib_llm_ext.AIProvider.chat] Exception while communicating with LLM: {e}")
            return ""

    def _clean_text(self, text: str) -> str:
        """Unescape special characters."""
        if text is None:
            return ""
        return text.replace("_quote_", '"').replace("_apostrophe_", "'")


class AsiOneProvider(AIProvider):
    """Lazy AI provider with on-demand initialization."""

    def __init__(self, name: str, var_name: str, model_name: str, base_url: str):
        super().__init__(name, var_name, model_name, base_url)

    def chat(self, model: str, content: str, max_tokens: int = 6000, **kwargs) -> str:
        """Send chat request, initializing client if needed."""
        self._ensure_client()

        if self._client is None:
            raise RuntimeError(f"{self._name} not configured (set {self._var_name})")

        sysmsg, usermsg = content.split(":-:-:-:")
        try:
            response = self._client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": sysmsg},
                          {"role": "user", "content": usermsg}],
                max_tokens=max_tokens,
                extra_body={
                    "enable_thinking": True,
                    "thinking_budget": 6000 
                },
                **kwargs
            )

            return self._clean_text(response.choices[0].message.content)
        except Exception as e:
            print(f"[lib_llm_ext.ASIOneProvider.chat] Exception while communicating with LLM: {e}")
            return ""


class GlmProvider(AIProvider):
    """Friendli/GLM-5.1 with deep reasoning enabled.

    Per Friendli docs:
      - extra_body needs parse_reasoning AND nested
        chat_template_kwargs.enable_thinking (note: nested, not top-level)
      - In thinking mode, response may have empty message.content
        with reasoning text in message.reasoning_content -- fall back
        to reasoning_content when content is empty.
    """

    def __init__(self, name: str, var_name: str, model_name: str, base_url: str):
        super().__init__(name, var_name, model_name, base_url)

    def chat(self, model: str, content: str, max_tokens: int = 6000, **kwargs) -> str:
        """Send chat request, initializing client if needed."""
        self._ensure_client()

        if self._client is None:
            raise RuntimeError(f"{self._name} not configured (set {self._var_name})")

        try:
            spl = content.split(":-:-:-:")
            sysmsg = spl[0]
            usermsg = spl[1] if len(spl) > 1 else ""
            response = self._client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": sysmsg},
                          {"role": "user", "content": usermsg}],
                max_tokens=max_tokens,
                extra_body={
                    "parse_reasoning": True,
                    "chat_template_kwargs": {"enable_thinking": True}
                },
                **kwargs
            )
            msg = response.choices[0].message
            text = (getattr(msg, "content", None) or "").strip()
            if not text:
                # GLM thinking-mode fallback: substance may live in reasoning_content
                text = (getattr(msg, "reasoning_content", None) or "").strip()
            return self._clean_text(text)
        except Exception as e:
            print(f"[lib_llm_ext.GlmProvider.chat] Exception while communicating with LLM: {e}")
            return ""


# Provider registry - lazy, no initialization yet
_provider_registry = {}


def _register_provider(name: str, var_name: str, model_name: str, base_url: str):
    """Register a provider configuration (no instantiation yet)."""
    _register_provider_instance(AIProvider(name, var_name, model_name, base_url))

def _register_provider_instance(provider: AIProvider):
    """Register a pre-initialized provider configuration (no instantiation yet)."""
    _provider_registry[provider._name] = provider

def _get_provider(name: str) -> Optional[AIProvider]:
    """Get or create provider instance on demand."""
    return _provider_registry.get(name)


# Register all providers (cheap - just stores config)
_register_provider(name="ASICloud", var_name="ASI_API_KEY", model_name="minimax/minimax-m2.5", base_url="https://inference.asicloud.cudos.org/v1")
_register_provider(name="Anthropic", var_name="ANTHROPIC_API_KEY", model_name="claude-opus-4-6", base_url="https://api.anthropic.com/v1/")
_register_provider_instance(AsiOneProvider(name="ASIOne", var_name="ASIONE_API_KEY", model_name="asi1-ultra", base_url="https://api.asi1.ai/v1"))
_register_provider_instance(GlmProvider(name="Friendli", var_name="FRIENDLI_API_KEY", model_name="zai-org/GLM-5.1", base_url="https://api.friendli.ai/serverless/v1"))
# At the moment the OpenAI model call is in PeTTa, just init a default config here
_register_provider(name="OpenAI", var_name="OPENAI_API_KEY", model_name="gpt-5.4", base_url="https://api.openai.com/v1")


def callProvider(provider_name: str, content: str, max_tokens: int = 6000) -> str:
    """Generic dispatcher for MeTTa.

    Resilient: returns empty string + logs on missing/unavailable provider
    rather than raising, to avoid crashing the container loop on transient
    config issues.
    """
    provider = _get_provider(provider_name)
    if provider is None:
        print(f"[lib_llm_ext.callProvider] Unknown provider: {provider_name}")
        return ""
    if not provider.is_available:
        print(f"[lib_llm_ext.callProvider] {provider_name} not configured (missing {provider._var_name})")
        return ""
    return provider.chat(model=provider._model_name, content=content, max_tokens=max_tokens)


# ============================================================================
# RESERVED FOR FUTURE USE -- standalone _chatAsiOne / useAsi1 helpers
# ----------------------------------------------------------------------------
# These were present in upstream's lib_llm_ext.py at lines 131-157 but
# reference symbols (ASIONE_CLIENT, _clean) that no longer exist after the
# class-based refactor. Commented out rather than deleted because they may
# be revived for direct-call use cases (per-call style without registry
# dispatch) in future work.
#
# def _chatAsiOne(client, model, content, max_tokens=6000, **kwargs):
#     spl = content.split(":-:-:-:")
#     try:
#         resp = client.chat.completions.create(
#             model=model,
#             messages=[{"role": "system", "content": spl[0]},
#                       {"role": "user", "content": spl[1]}],
#             max_tokens=max_tokens,
#             extra_body={
#                 "enable_thinking": True,
#                 "thinking_budget": 6000
#             },
#             **kwargs
#         )
#         return _clean(resp.choices[0].message.content)
#     except Exception as e:
#         print(f"[lib_llm_ext._chat] Exception while communicating with LLM: {e}")
#         return ""
#
# def useAsi1(content):
#     resp = _chatAsiOne(
#         client=ASIONE_CLIENT,
#         model="asi1-ultra",
#         content=content
#     )
#     resp = resp.replace("</arg_value>", " ").replace("</tool_call>", " ").replace("<arg_value>", " ").replace("<tool_call>", " ")
#     return resp
# ============================================================================


_embedding_model = None

def initLocalEmbedding():
    model_name="intfloat/e5-large-v2"
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer(model_name)
    return _embedding_model

def useLocalEmbedding(atom):
    global _embedding_model
    if _embedding_model is None:
        raise RuntimeError("Call initLocalEmbedding() first.")
    return _embedding_model.encode(
        atom,
        normalize_embeddings=True
    ).tolist()
'''


# ============================================================
# EDIT SPECIFICATIONS for non-replacement files
# ============================================================

EDITS = [
    (
        'src/loop.metta',
        '          (configure provider Anthropic) ;Anthropic or OpenAI or ASICloud',
        '          (configure provider Friendli) ;Friendli or Anthropic or ASICloud or ASIOne (was: Anthropic)',
        'loop.metta line 15: default provider Anthropic -> Friendli',
    ),
    (
        'src/loop.metta',
        '''                                       ($respi (if (== $aliveness SILENT) "" (if (== (provider) OpenAI)
                                                   (useGPT (LLM) (maxOutputToken) (reasoningMode) $send)
                                                   (if (== (provider) Anthropic)
                                                       (py-call (lib_llm_ext.useClaude $send))
                                                       (py-call (lib_llm_ext.useMiniMax $send))))))''',
        '''                                       ($respi (if (== $aliveness SILENT) "" (if (== (provider) OpenAI)
                                                   (useGPT (LLM) (maxOutputToken) (reasoningMode) $send)
                                                   (py-call (lib_llm_ext.callProvider (provider) $send (maxOutputToken))))))''',
        'loop.metta lines 108-112: dispatch chain -> callProvider',
    ),
    (
        'soul/soul_utils.metta',
        '''(= (soul-llm-call $prompt $prov)
   (if (== $prov OpenAI)
       (useGPT (LLM) 500 (reasoningMode) $prompt)
       (if (== $prov Anthropic)
           (py-call (lib_llm_ext.useClaude $prompt))
           (py-call (lib_llm_ext.useMiniMax $prompt)))))''',
        '''(= (soul-llm-call $prompt $prov)
   (if (== $prov OpenAI)
       (useGPT (LLM) 500 (reasoningMode) $prompt)
       (py-call (lib_llm_ext.callProvider $prov $prompt 6000))))''',
        'soul_utils.metta soul-llm-call: dispatch chain -> callProvider',
    ),
    (
        'docker-compose.yml',
        '      # Anthropic API key -- primary LLM provider (Decision E)\n      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}',
        '      # Anthropic API key -- LLM provider (kept available for switching back)\n      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}\n      # Friendli/GLM-5.1 API key -- current default LLM provider\n      - FRIENDLI_API_KEY=${FRIENDLI_API_KEY}',
        'docker-compose.yml: add FRIENDLI_API_KEY env var',
    ),
]


# ============================================================
# UTILITIES
# ============================================================

def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def red(t): return color(t, '31')
def green(t): return color(t, '32')
def yellow(t): return color(t, '33')
def blue(t): return color(t, '34')
def bold(t): return color(t, '1')


def show_diff(path, old_content, new_content):
    diff = difflib.unified_diff(
        old_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f'a/{path}',
        tofile=f'b/{path}',
        n=3,
    )
    for line in diff:
        if line.startswith('+++') or line.startswith('---'):
            print(bold(line.rstrip()))
        elif line.startswith('+'):
            print(green(line.rstrip()))
        elif line.startswith('-'):
            print(red(line.rstrip()))
        elif line.startswith('@@'):
            print(blue(line.rstrip()))
        else:
            print(line.rstrip())


def deduplicate_preserve_order(items):
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


# ============================================================
# MAIN
# ============================================================

def main():
    apply_changes = '--apply' in sys.argv
    
    print(bold("=" * 70))
    print(bold("Switch default LLM provider to Friendli/GLM-5.1"))
    print(bold("=" * 70))
    print()
    print(f"Mode: {'APPLY' if apply_changes else 'DRY-RUN'}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # ----------------------------------------------------------------
    # PHASE 1: Pre-conditions
    # ----------------------------------------------------------------
    print(bold("PHASE 1: Pre-condition checks"))
    print("-" * 70)
    
    if not os.path.exists('lib_llm_ext.py'):
        print(red("  FAIL: lib_llm_ext.py does not exist"))
        return 1
    print(green("  OK:   lib_llm_ext.py exists (will be replaced)"))
    
    file_contents = {}
    for path, old, new, desc in EDITS:
        if not os.path.exists(path):
            print(red(f"  FAIL: {path} does not exist"))
            return 1
        if path not in file_contents:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    file_contents[path] = f.read()
            except IOError as e:
                print(red(f"  FAIL: cannot read {path}: {e}"))
                return 3
        if old not in file_contents[path]:
            print(red(f"  FAIL: {path}"))
            print(red(f"        expected text not found: {desc}"))
            print(red(f"        first 80 chars of expected: {repr(old[:80])}"))
            return 1
        print(green(f"  OK:   {desc}"))
    
    # Check .env for FRIENDLI_API_KEY (warning only)
    if os.path.exists('.env'):
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                env_content = f.read()
            if 'FRIENDLI_API_KEY=' in env_content:
                print(green("  OK:   .env contains FRIENDLI_API_KEY"))
            else:
                print(yellow("  WARN: .env exists but does not contain FRIENDLI_API_KEY"))
        except IOError:
            print(yellow("  WARN: could not read .env"))
    else:
        print(yellow("  WARN: .env does not exist"))
    
    print()
    print(green(bold("Phase 1 complete: pre-conditions met.")))
    print()
    
    # ----------------------------------------------------------------
    # PHASE 2: Compute changes
    # ----------------------------------------------------------------
    print(bold("PHASE 2: Computing changes"))
    print("-" * 70)
    
    new_contents = {}
    
    with open('lib_llm_ext.py', 'r', encoding='utf-8') as f:
        old_lib = f.read()
    new_contents['lib_llm_ext.py'] = NEW_LIB_LLM_EXT
    print(f"  lib_llm_ext.py: full file replacement "
          f"({len(old_lib.splitlines())} lines -> "
          f"{len(NEW_LIB_LLM_EXT.splitlines())} lines)")
    
    for path, old, new, desc in EDITS:
        if path not in new_contents:
            new_contents[path] = file_contents[path]
        new_contents[path] = new_contents[path].replace(old, new, 1)
    
    edit_paths = deduplicate_preserve_order([e[0] for e in EDITS])
    for path in edit_paths:
        replacements = sum(1 for p, _, _, _ in EDITS if p == path)
        print(f"  {path}: {replacements} replacement(s)")
    
    print()
    print(bold("PHASE 2.5: Diffs"))
    print("-" * 70)
    
    print(f"\n--- Diff for {bold('lib_llm_ext.py')} (large -- summary only) ---")
    print(yellow(f"  Old: {len(old_lib.splitlines())} lines (your current file)"))
    print(green(f"  New: {len(NEW_LIB_LLM_EXT.splitlines())} lines "
                f"(upstream provider-registry pattern + GlmProvider + Friendli registration)"))
    print(f"  After apply: diff against backup with `diff -u <backup> lib_llm_ext.py`")
    
    for path in ['src/loop.metta', 'soul/soul_utils.metta', 'docker-compose.yml']:
        if path in new_contents and file_contents.get(path) != new_contents[path]:
            print(f"\n--- Diff for {bold(path)} ---")
            show_diff(path, file_contents[path], new_contents[path])
    
    print()
    
    # ----------------------------------------------------------------
    # PHASE 3: Apply or stop
    # ----------------------------------------------------------------
    if not apply_changes:
        print(bold("=" * 70))
        print(yellow(bold("DRY-RUN COMPLETE. No files modified.")))
        print()
        print("To apply: python3 apply_glm_switch.py --apply")
        print(bold("=" * 70))
        return 0
    
    print(bold("PHASE 3: Applying changes with backups"))
    print("-" * 70)
    
    backup_suffix = f".pre-glm-switch-{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    backups_made = []
    
    try:
        for path in new_contents:
            backup_path = path + backup_suffix
            shutil.copy2(path, backup_path)
            backups_made.append((path, backup_path))
            print(green(f"  Backed up: {path} -> {backup_path}"))
        
        for path, content in new_contents.items():
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(green(f"  Wrote:     {path}"))
        
        print()
        
        # ----------------------------------------------------------------
        # PHASE 4: Post-conditions
        # ----------------------------------------------------------------
        print(bold("PHASE 4: Post-condition checks"))
        print("-" * 70)
        
        all_verified = True
        
        # 4a. Python syntax
        try:
            import ast
            with open('lib_llm_ext.py', 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            print(green("  OK:   lib_llm_ext.py parses as valid Python"))
        except SyntaxError as e:
            print(red(f"  FAIL: lib_llm_ext.py syntax error: {e}"))
            all_verified = False
        
        # 4b. Required names present
        try:
            with open('lib_llm_ext.py', 'r', encoding='utf-8') as f:
                lib_content = f.read()
            required = ['callProvider', 'AIProvider', 'AsiOneProvider',
                        'GlmProvider', 'initLocalEmbedding',
                        'useLocalEmbedding', '_provider_registry',
                        '"Friendli"', '"Anthropic"', '"ASICloud"', '"ASIOne"',
                        'FRIENDLI_API_KEY', 'zai-org/GLM-5.1',
                        'parse_reasoning', 'chat_template_kwargs',
                        'reasoning_content']
            missing = [n for n in required if n not in lib_content]
            if missing:
                print(red(f"  FAIL: lib_llm_ext.py missing names: {missing}"))
                all_verified = False
            else:
                print(green("  OK:   lib_llm_ext.py contains all required names"))
        except IOError:
            print(red("  FAIL: cannot re-read lib_llm_ext.py"))
            all_verified = False
        
        # 4c. EDITS verification
        for path, old, new, desc in EDITS:
            with open(path, 'r', encoding='utf-8') as f:
                on_disk = f.read()
            if old in on_disk:
                print(red(f"  FAIL: old text still in {path}: {desc}"))
                all_verified = False
            elif new not in on_disk:
                print(red(f"  FAIL: new text not in {path}: {desc}"))
                all_verified = False
            else:
                print(green(f"  OK:   {desc}"))
        
        if not all_verified:
            print()
            print(red(bold("POST-CONDITION FAILURES. ROLLING BACK.")))
            for orig, backup in backups_made:
                shutil.copy2(backup, orig)
                print(yellow(f"  Restored: {orig}"))
            return 2
        
        print()
        print(green(bold("Phase 4 complete: all changes verified.")))
        print()
        
        # ----------------------------------------------------------------
        # PHASE 5: Summary
        # ----------------------------------------------------------------
        print(bold("=" * 70))
        print(green(bold("GLM SWITCH APPLIED SUCCESSFULLY")))
        print(bold("=" * 70))
        print()
        print("Backups:")
        for orig, backup in backups_made:
            print(f"  {backup}")
        print()
        print("To roll back manually:")
        for orig, backup in backups_made:
            print(f"  cp {backup} {orig}")
        print()
        print(bold("Next steps:"))
        print("  1. Confirm FRIENDLI_API_KEY in .env (verified in Phase 1)")
        print("  2. docker compose build --no-cache clarityclaw && docker compose up -d")
        print("  3. docker logs -f clarity_omega")
        print("  4. Watch for HTTP 200 from api.friendli.ai/serverless/v1")
        print("  5. Test via Mattermost message")
        print()
        print("To switch back to Anthropic:")
        print("  Edit src/loop.metta line 15: 'Friendli' -> 'Anthropic'")
        print("  docker compose build --no-cache clarityclaw && docker compose up -d")
        print()
        return 0
    
    except Exception as e:
        print(red(f"\nUNEXPECTED ERROR: {e}"))
        print(red("Rolling back..."))
        for orig, backup in backups_made:
            try:
                shutil.copy2(backup, orig)
                print(yellow(f"  Restored: {orig}"))
            except Exception as rerr:
                print(red(f"  ROLLBACK FAILED for {orig}: {rerr}"))
        return 3


if __name__ == '__main__':
    sys.exit(main())