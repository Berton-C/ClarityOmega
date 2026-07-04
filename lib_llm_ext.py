import os, openai
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
        with reasoning text in message.reasoning_content. That reasoning
        is PRINTED to the log for visibility but NOT returned as the
        response (returning it fed her deliberation to the command
        parser: draft send lines executed as real sends, 2026-07-04).
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
            reasoning = (getattr(msg, "reasoning_content", None) or "").strip()
            # Boundary diagnostic (2026-07-04): one line per call, makes the
            # empty-content mechanism observable and this fix falsifiable.
            print("[GlmProvider.chat] content_len=%d reasoning_len=%d fallback_would_have_fired=%s"
                  % (len(text), len(reasoning), (not text) and bool(reasoning)))
            if not text:
                # Empty-content cycle. The old fallback returned
                # reasoning_content as the response; the canon line splitter
                # then executed every draft (send ...) line inside her
                # deliberation (proven 2026-07-04: the 13:28 batch, one
                # entry, three sends, reasoning-as-content header) and
                # reasoning walls reached Mattermost. Visibility is
                # preserved by printing the reasoning here, labeled; the
                # command channel gets an empty response, which takes the
                # existing safe path in the loop (first_char gate no-ops
                # with a format reminder).
                if reasoning:
                    print("[GlmProvider.chat] content EMPTY; reasoning_content follows (visibility only, NOT returned as commands):")
                    print(reasoning)
                return ""
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
_register_provider_instance(GlmProvider(name="Friendli52", var_name="FRIENDLI_API_KEY", model_name="zai-org/GLM-5.2", base_url="https://api.friendli.ai/serverless/v1"))
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
