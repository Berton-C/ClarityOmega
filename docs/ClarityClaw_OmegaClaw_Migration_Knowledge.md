# ClarityClaw OmegaClaw Migration Knowledge

**Date:** April 14, 2026
**Status:** Phase 4 complete -- soul patches applied to OmegaClaw base
**Author:** Berton Bennett / ClarityDAO, with Claude
**Base commit:** OmegaClaw-Core 9509a7d (tag v0.1.7)
**Repo:** /Users/bcb/Documents/ClarityClaw/clarityclaw-omega

---

## 1. Why We Migrated

ClarityClaw was forked from patham9/mettaclaw. Stage 5 (loop integration) hit PeTTa runtime
constraints that were base issues, not soul issues: atom_string/2 crashes on ChromaDB query
returns (C7), multi-byte UTF-8 handling failures (C5), and superpose crashes on non-list atoms
(C6). OmegaClaw (asi-alliance/OmegaClaw-Core) is Patrick's evolved codebase with fixes for
these constraints. Migration to OmegaClaw resolves C7 automatically via normalize_string and
provides a cleaner base for completing Stage 5.

---

## 2. Three Critical Discoveries

**Discovery 1: normalize_string fixes C7.**
OmegaClaw wraps every eval result in the loop:
```
(catch (let $R (eval $s) (py-call (helper.normalize_string $R))))
```
normalize_string in src/helper.py converts any eval return value to clean UTF-8 before Prolog
processes it. This resolves the atom_string/2 crash on $results that blocked Mattermost responses.

**Discovery 2: Local embeddings -- no OpenAI key needed.**
OmegaClaw uses sentence-transformers with intfloat/e5-large-v2, pre-downloaded at build time.
Embeddings run locally. Only Anthropic API key required for LLM calls. The two-API-key requirement
from the old base is eliminated.

**Discovery 3: helper.py is in src/ not repo root.**
OmegaClaw's helper.py lives at src/helper.py. PeTTa resolves it through the explicit import in
lib_omegaclaw.metta: `!(import! &self (library omegaclaw ./src/helper.py))`. No PYTHONPATH
configuration needed.

---

## 3. Full File Survey

Every file in OmegaClaw was read before writing any code. Findings:

### src/loop.metta (74 lines)
The main agent loop. Indentation: 39 spaces for let* bindings, 10 spaces for initLoop progn
body, 31 spaces for startup block. All spaces, no tabs.

Key differences from old MeTTaClaw:
- Loop variable is maxNewInputLoops (was maxLoops)
- Wake loop mechanism: maxWakeLoops + wakeupInterval + &nextWakeAt
- Provider routing: three-way branch (OpenAI / Anthropic / MiniMax)
- normalize_string wraps eval in $results binding
- Default provider is Anthropic (was OpenAI)

### src/helper.py (66 lines)
Four functions: extract_timestamp, around_time, balance_parentheses, normalize_string.
balance_parentheses is improved over old version (handles garbage before first paren, wraps
as pin command). normalize_string is the C7 fix. No sys.path manipulation, no PYTHONPATH
awareness.

### src/memory.metta
initMemory configures memory parameters and initializes local embeddings via
lib_llm_ext.initLocalEmbedding when embeddingprovider is Local (default). query returns raw
results from lib_chromadb.query -- normalization happens in the loop, not in query itself.
embed routes through useLocalEmbedding or useGPTEmbedding based on config.

### src/channels.metta
Defaults to IRC on QuakeNet. Mattermost is the else-branch with hardcoded SingularityNET
values. ClarityClaw overrides to local Mattermost via docker-compose environment variables.
send function has dedup guard (&lastsend) -- silently drops duplicate messages.

### src/utils.metta
Critical native patterns:
- exists-file: MeTTa-native file existence check via Prolog exists_file. Use instead of
  py-call (helper.file_exists_int ...) where possible.
- configure: reads command-line args with argk, falls back to default, adds to &self as fact.
  Use for soul-specific config values.
- string-safe: encodes quotes, newlines, apostrophes for safe Prolog transport. Counterpart
  is _clean in lib_llm_ext.py which reverses encoding on LLM output.
- sub_string: imported from Prolog, available for substring operations.
- string_concat: imported from Prolog, available for string concatenation.

### src/skills.metta
MeTTa-native file I/O:
- read-file: uses exists_file guard then read_file_to_string
- write-file: opens file in write mode via Prolog
- append-file: opens file in append mode via Prolog. REQUIRES file to pre-exist (exists_file
  guard). Our touch_file in helper.py is still needed for creating new files.
- first_char: imported from skills.pl, used in loop guard checks
- metta skill: sread then eval -- relevant for soul mutation gate

New skills since old base: tavily-search, technical-analysis (via agentverse.py).

### lib_omegaclaw.metta
Import chain. Core libraries same as old base (lib_patrick, lib_llm, lib_vector,
lib_combinatorics). Duplicate src/channels import is Patrick's design. Soul imports added
after src/memory import. Missing context.metta import -- file never existed in repo history,
PeTTa silently handles it.

### lib_llm_ext.py
LLM call wrappers. useClaude uses OpenAI-compatible client pointed at Anthropic API
(claude-opus-4-6). _clean reverses string-safe encoding. _chat is generic wrapper with
max_tokens=6000 default. initLocalEmbedding lazy-loads sentence-transformers model.
useLocalEmbedding encodes with normalization, returns list.

### lib_nal.metta
Non-Axiomatic Logic (NAL) reasoning engine. Truth functions, inference rules (deduction,
abduction, induction, revision). The |- function is the inference entry point. This is the
future Phase 2 PLN integration point -- the infrastructure is already present.

### channels/mattermost.py
Matured significantly. New features: authentication system (OMEGACLAW_AUTH_SECRET env var,
_is_allowed_message gating), display name resolution, WebSocket ping keepalive (25s),
message concatenation (multiple messages between loops joined with |).

### channels/irc.py
Not critical for ClarityClaw. IRC on QuakeNet is vestigial.

### scripts/omegaclaw_setup.sh
Standalone docker run deployment for IRC. Security flags worth adopting: --security-opt
no-new-privileges, --init, tmpfs mounts. Generates auth secret automatically.

### Dockerfile (118 lines)
Multi-stage build on swipl:9.2.4. Builder stage compiles PeTTa, FAISS, downloads embedding
model. Runtime stage is lean. COPY . /PeTTa/repos/omegaclaw copies entire repo into container.
Non-root user 65534. chmod 0444 on prompt.txt removed per Decision D.

### run.metta
git-import! line removed. Was cloning OmegaClaw from GitHub at runtime, overwriting local
files including soul code. Now relies on Dockerfile COPY.

---

## 4. Decisions Made

### Decision A: helper.py location
**Option 1 chosen:** Merge soul functions into OmegaClaw's src/helper.py. Preserves their
functions (balance_parentheses, normalize_string, around_time, extract_timestamp) in a
clearly marked upstream section. Soul functions in a clearly marked ClarityClaw section below.
SOUL_DEBUG flag for debug prints. No PYTHONPATH change needed.

### Decision B: soul/ directory location
Copied wholesale from clarityclaw-main. Three import lines added to lib_omegaclaw.metta
after src/memory import:
```
!(import! &self (library omegaclaw ./soul/soul_kernel))
!(import! &self (library omegaclaw ./soul/soul_utils))
!(import! &self (library omegaclaw ./soul/soul_memory))
```

### Decision C: PYTHONPATH for soul imports
No change needed. py-call resolves helper through lib_omegaclaw.metta's explicit import of
./src/helper.py. Verify at first build.

### Decision D: prompt.txt handling
chmod 0444 line removed from Dockerfile. prompt.txt stays at 0644 (writable by owner).
Berton hand-merges OmegaClaw's Max Botnick prompt with ClarityClaw identity before first
build. No automated copy.

### Decision E: Anthropic vs OpenAI for LLM
Anthropic as default provider. soul-llm-call dispatcher built as MeTTa function in
soul_utils.metta (not Python) -- mirrors the main loop's provider routing pattern. Supports
per-function provider override via configure mechanism. Preserves path to local models via
LM Studio (OpenAI-compatible endpoint at localhost:1234/v1).

### Decision F: Two-key vs one-key configuration
Single required key: ANTHROPIC_API_KEY. OpenAI key remains in .env as commented-out option.
Local embeddings are default (intfloat/e5-large-v2, 1024 dimensions). Verify soul seeding
with local embeddings at first build.

---

## 5. Where OmegaClaw Supersedes Our Stage 5 Code

These are places where OmegaClaw's maturation makes our old approach unnecessary or where
Patrick's approach is better than ours:

1. **Provider routing for main LLM call:** OmegaClaw has three-way branch (OpenAI / Anthropic
   / MiniMax). Our old two-way branch with lib_llm_asicloud is obsolete.

2. **sanitize_response between balance_parentheses and sread:** normalize_string replaces our
   ASCII-stripping sanitize_response. Patrick's approach keeps valid UTF-8 instead of
   replacing everything non-ASCII with ?.

3. **$results binding:** OmegaClaw's version wraps eval in normalize_string. Our old version
   had bare (catch (eval $s)) which crashed on ChromaDB returns.

4. **println! RESULTS-DONE and DEBUG-RESULTS-PRINTED:** Workarounds for the $results crash.
   normalize_string makes them unnecessary. Dropped entirely.

5. **Wake loop fallback:** OmegaClaw's &nextWakeAt mechanism replaces our dead-end _ when
   loops reaches 0.

6. **balance_parentheses:** OmegaClaw's version handles garbage before first paren and wraps
   it as a (pin "...") command. Our version did not. Use theirs.

---

## 6. Patrick's MeTTa-Native Patterns We Should Adopt

Our soul code was built heavily in Python because the old MeTTa layer lacked clean patterns.
OmegaClaw provides MeTTa-native equivalents for several things we did in Python:

- **exists-file** (utils.metta): MeTTa-native file check via Prolog. Evaluate replacing
  py-call (helper.file_exists_int ...) in soul-rationality-startup-check.

- **configure** (utils.metta): Config mechanism for all parameters. Use for soul-specific
  config (soulProvider, etc.) instead of inventing custom config patterns.

- **string-safe / _clean pipeline**: Trust it for quote/newline handling. Do not double-encode
  strings that have already been through string-safe.

- **normalize_string**: Use instead of sanitize_response in the loop chain. sanitize_response
  remains available in helper.py for cases where ASCII-only stripping is specifically needed.

- **sub_string** (Prolog import): Available for substring extraction. Potential replacement
  for extract_after in some contexts.

- **string_concat** (Prolog import): Available for string concatenation. Potential replacement
  for concat_strings.

- **write-file / append-file** (skills.metta): MeTTa-native file I/O. Use when possible.
  append-file still requires pre-existing file (touch_file still needed).

- **_chat pattern** (lib_llm_ext.py): Generic LLM wrapper with _clean built in. Soul LLM
  calls route through this via useClaude.

**Guiding principle:** Use Patrick's demonstrated working code. Our soul code should work LIKE
his code works. Adopt his methods and approaches. Our job is to creatively use what he has
shown as working and apply it to the soul use case. Our implementation takes priority over
his only when his falls short of what we need.

---

## 7. ChromaDB Baseline

OmegaClaw's chromadb setup is Patrick's authoritative version. We treat it as the working
baseline. Key facts:
- petta_lib_chromadb is cloned from patham9/petta_lib_chromadb at build time
- git-import! in lib_omegaclaw.metta also references it at runtime
- Local embeddings (e5-large-v2) produce 1024-dimensional vectors
- Old base used OpenAI embeddings (3072 dimensions) -- different vector space
- Fresh ChromaDB on OmegaClaw base, no mismatch issues
- Soul seeding via remember() must be verified at first build
- Do not carry ChromaDB assumptions from the old repo

---

## 8. Insertion Points (Pattern-Based)

All insertion points use content pattern matching, not line numbers, for resilience across
upstream updates.

### 5a: State variables in initLoop
**Anchor:** `(change-state! &loops (maxNewInputLoops))))`
**Action:** Insert 7 soul state variables BEFORE this closing line
**Indentation:** 10 spaces (matching initLoop progn body)

### 5a: Startup block
**Anchor 1:** `(initMemory)`
**Anchor 2:** `(initChannels)`
**Action:** Insert initSoulSeeds and soul-rationality-startup-check BETWEEN these two
**Indentation:** 31 spaces (matching startup block)

### 5b: normalize_string wrapping
**Anchor:** `($resp (py-call (helper.balance_parentheses $respi)))`
**Action:** Replace with `($resp (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))`

### 5b: Input intercept
**Anchor:** `($send (py-str ($prompt $lastmessage)))`
**Action:** Replace with full soul evaluation sequence (Channel A, B+C, $send assembly)
**Indentation:** 39 spaces (matching let* bindings)

### 5c: Output intercept
**Anchor:** `($_ (println! (RESPONSE: $sexpr)))`
**Action:** Insert soul output evaluation AFTER this line, BEFORE $results binding
**Indentation:** 39 spaces (matching let* bindings)
**CRITICAL:** Do NOT touch OmegaClaw's $results binding -- normalize_string handles it

---

## 9. Patch Scripts

Four scripts in scripts/ directory:

**soul_patch_all.sh** -- master script. Checks prerequisites, runs patches in order. Supports
--dry-run.

**soul_patch_lib.py** -- adds soul imports to lib_omegaclaw.metta after src/memory import.
Anchor: `!(import! &self (library omegaclaw ./src/memory))`

**soul_patch_dockerfile.py** -- removes chmod 0444 line from Dockerfile. Flexible pattern
matching for whitespace variations.

**soul_patch_loop.py** -- applies all 5a/5b/5c patches to src/loop.metta. Five patches in
sequence: state vars, startup block, normalize wrapping, input intercept, output intercept.

All scripts are:
- **Pattern-based:** anchor on content, not line numbers
- **Idempotent:** detect if already applied, skip gracefully
- **Loud on failure:** if anchor not found, print exactly what was expected
- **Backup-creating:** create .pre-soul-backup files before modifying

---

## 10. Recurring Merge Workflow

ClarityClaw merges with OmegaClaw upstream frequently. The workflow:

```bash
# 1. Fetch latest OmegaClaw
git remote add upstream https://github.com/asi-alliance/OmegaClaw-Core.git  # one-time
git fetch upstream

# 2. Create a merge branch
git checkout -b merge-upstream-YYYY-MM-DD

# 3. Merge upstream
git merge upstream/main

# 4. If loop.metta has conflicts:
#    Resolve by accepting upstream's version of loop.metta
#    Then restore from backup and re-patch:
cp src/loop.metta.pre-soul-backup src/loop.metta  # or accept upstream's clean version
python3 scripts/soul_patch_loop.py

# 5. If lib_omegaclaw.metta has conflicts:
#    Resolve, then re-run:
python3 scripts/soul_patch_lib.py

# 6. If Dockerfile has conflicts:
#    Resolve, then re-run:
python3 scripts/soul_patch_dockerfile.py

# 7. If src/helper.py has conflicts:
#    MANUAL REVIEW REQUIRED
#    Check if Patrick changed his four upstream functions
#    Replace upstream section, keep ClarityClaw section
#    This is the one file that cannot be fully automated

# 8. Build and test
docker compose build --no-cache
docker compose up -d
docker logs [container] | grep SOUL-AUDIT
```

### What can break during merge

**loop.metta changes:** If Patrick restructures the let* chain, adds new bindings, changes
variable names, or modifies the $results binding, the patch scripts will fail with a clear
message about which anchor was not found. Read the new loop.metta, update the anchor pattern
in the script, and re-run.

**helper.py changes:** If Patrick adds new functions or modifies balance_parentheses /
normalize_string, manually update the upstream section of our merged helper.py. Do not
overwrite the ClarityClaw section.

**New files:** If Patrick adds context.metta or other new files, they get picked up
automatically by lib_omegaclaw.metta's imports. No action needed unless they define functions
that conflict with our soul function names.

**lib_omegaclaw.metta import order changes:** If Patrick reorders imports, the soul_patch_lib
anchor (src/memory import) might move. Script will still find it as long as the exact line
text is preserved.

---

## 11. Structural Differences Reference

| Aspect | Old ClarityClaw | OmegaClaw |
|--------|----------------|-----------|
| Repo path in container | /app/PeTTa/repos/mettaclaw | /PeTTa/repos/omegaclaw |
| PeTTa root | /app/PeTTa | /PeTTa |
| helper.py location | repo root | src/helper.py |
| Dockerfile | Single-stage, Ubuntu | Multi-stage, swipl:9.2.4 |
| Runs as | root | user 65534 (non-root) |
| Embeddings | OpenAI text-embedding-3-large (3072d) | Local e5-large-v2 (1024d) |
| LLM provider default | OpenAI | Anthropic |
| Loop variable | maxLoops | maxNewInputLoops |
| Wake feature | none | maxWakeLoops + wakeupInterval |
| normalize_string | absent (C7 crash) | present (C7 resolved) |
| lib name | lib_mettaclaw.metta | lib_omegaclaw.metta |
| prompt.txt permissions | read-write | 0644 (chmod 0444 removed) |
| Library path prefix | (library mettaclaw ...) | (library omegaclaw ...) |

---

## 12. Files Modified by ClarityClaw

These are the only files ClarityClaw modifies in the OmegaClaw repo. Everything else is
Patrick's code, untouched.

**Modified:**
- src/loop.metta -- soul intercepts 5a/5b/5c (via patch script)
- src/helper.py -- soul functions merged into ClarityClaw section (manual merge)
- lib_omegaclaw.metta -- three soul import lines added (via patch script)
- Dockerfile -- chmod 0444 removed (via patch script)
- run.metta -- git-import! line removed (manual edit, one-time)
- memory/prompt.txt -- ClarityClaw identity (hand-edited by Berton)

**Added (no upstream counterpart):**
- soul/soul_kernel.metta
- soul/soul_utils.metta
- soul/soul_memory.metta
- soul/test_*.metta files
- soul/archives/
- scripts/soul_patch_loop.py
- scripts/soul_patch_lib.py
- scripts/soul_patch_dockerfile.py
- scripts/soul_patch_all.sh
- docs/ClarityClaw_OmegaClaw_Merge_Checklist.md
- docs/ClarityClaw_Stage5_Integration_Knowledge.md
- docs/ClarityClaw_OmegaClaw_Migration_Knowledge.md (this file)
- docs/decisions/ADR-003-communication-channel.md
- docs/decisions/ADR-004-phase2-anthropic-sdk.md

**Untouched Patrick files:**
- src/utils.metta, src/memory.metta, src/channels.metta, src/skills.metta, src/skills.pl
- src/agentverse.py
- lib_llm_ext.py, lib_nal.metta
- channels/irc.py, channels/mattermost.py, channels/websearch.py
- scripts/omegaclaw_setup.sh
- .dockerignore, .gitignore, .github/, LICENSE, README.md, omegaclaw-logo

---

## 13. Open Items

- **soul-llm-call dispatcher:** Defined in design, needs to be written in soul_utils.metta.
  MeTTa function mirroring the main loop's provider routing pattern.

- **soul-rationality-startup-check:** References (library mettaclaw ...) paths in current soul
  code. Must be updated to (library omegaclaw ...) before first build.

- **PAUSE routing (Step 12):** Not yet implemented in the patch scripts. The PAUSE branch
  (Channel D soul voice, loop halt) needs to be added to the input intercept. Currently
  PAUSE falls through to normal $send assembly.

- **prompt.txt:** Berton hand-merging OmegaClaw's Max Botnick text with ClarityClaw identity.
  Must be complete before first build.

- **context.metta:** Missing from repo despite import in lib_omegaclaw.metta. Berton checking
  with Patrick. PeTTa appears to handle the missing import silently.

- **Mattermost configuration:** channels.metta defaults need to be overridden for local
  Mattermost instance via docker-compose environment variables.

- **docker-compose.yml:** Needs to be written for OmegaClaw base. Different from old compose
  (different paths, single API key, local embeddings, no LiteLLM needed).

- **First build verification checklist:**
  1. Container starts without crashes
  2. PYTHONPATH resolves helper (Step 14 in merge checklist)
  3. Soul seeds load (grep SOUL-AUDIT in logs)
  4. normalize_string resolves C7 (query test)
  5. Local embeddings produce valid vectors
  6. Agent responds on Mattermost

---

## 14. Attribution

- **Patrick Hammer** (patham9, SingularityNET / ASI Alliance): original MeTTaClaw, OmegaClaw,
  PeTTa, NACE. All upstream code is his.
- **Berton Bennett** (ClarityDAO): ClarityClaw soul architecture, this migration.
- **Haley Lowy** (SingularityNET): co-author of BGI Flourishing Compass v1.0 and MeTTaSoul
  essays that the soul architecture implements.
- **Ben Goertzel** (SingularityNET): Hyperseed framework that the Compass applies.
