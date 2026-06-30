# ClarityOmega Boundary Transition Audit

**Status:** v2, RUNTIME-GROUNDED REVISION (2026-06-23). The system-wide inventory of every
boundary where data crosses between faculties, the functionality status of each crossing,
and the canonical handler each crossing should conform to. This revision grounds every cell
against the live runtime (the project knowledge files, which the running container
executes), reads the substrate files from source, and adds the verdict/governance boundary
(B13), which is live.

**What changed v1 to v2 (original).** v1 had four boundaries marked UPSTREAM/UNKNOWN
because the substrate files were not in hand. They were read from source (`utils.metta`,
`channels.metta`, `mattermost.py`, `memory.metta`, `skills.metta`, `lib_llm_ext.py`, plus
`helper.py`, `loop.metta`, `skills.pl`). Results: the string-safe leak is RESOLVED
(Section 3), the `main.pl` assumption is retired (there is no such source file), the
embedding boundary is downgraded (local, not OpenAI), the metta-skill re-parse is mapped,
and a third skill-registry source of truth was found. Two new fields per boundary,
canonical-handler and conformance, turn the audit into the standardization target.

**What changed in the 2026-06-23 runtime-grounding revision.** This revision reads every
boundary from the live runtime. The runtime is the set of files in the project knowledge
area; the running container `clarity_omega` executes that exact `loop.metta` and those exact
substrate files. An earlier pass this session misread `docker run --rm <image> cat
src/loop.metta`, which prints the stale baked copy inside the image, as the runtime; the
live container runs the project knowledge loop, not that baked copy. That misread is
retracted and its conclusions (a stub running loop, a discarded `$a`, a dark verdict gate)
are removed. This revision: (1) grounds every cell in the runtime files; (2) confirms B3
`HandleError` captures `$a` in the runtime; (3) adds B13, the verdict/governance boundary,
which is live; (4) carries the full output-verdict, corner-gate, and governance code in
Appendix A. Filename is held at `_v2` per the naming lock.

**Method.** Every cell is tagged by grounding. Two axes now apply.

Grounding state (original): `[SRC]` read from source; `[NEEDS-LIVE]` needs a running read
before a build rests on it; `[UNREAD]` handler not yet retrieved; `[STALE-BELIEF]` a prior
doc says X, source shows Y.

Runtime grounding (load-bearing). The project knowledge files are the live runtime: the
running container `clarity_omega` executes that `loop.metta`, that `helper.py`, and those
mounted `soul/` files. `[SRC]` cells are read from those files and are runtime facts;
`[MOUNTED-LIVE]` marks `soul/` and `memory/` paths where host equals runtime by mount.
Reading a throwaway container made from the image with `docker run --rm <image> cat` is NOT
a runtime read: it prints the image's baked copy, which the live container does not
necessarily execute. The one decisive read is the live container itself (`docker exec
clarity_omega ...` or its mount list). All cells below are runtime-grounded.

**Suggested home:** `docs/investigations/boundary_transition_audit.md`, git-tagged once the
NEEDS-LIVE cells are confirmed.

**Version:** v2, runtime-grounding revision, 2026-06-23.

---

## 0. What this audit is for (unchanged from v1, condensed)

Every malformation chased in this project is one class of failure: data crossing a
boundary in a form the receiving side did not expect. This audit maps every joint once,
grounded to source, so the immediate malformation pre-build, the SSI build (01b M1-M4 are
four of these boundaries), and all future build consult one current map instead of a
scatter of drifting point-docs. It is audit, not fix: it inventories and ends in a
prioritized list. It is one artifact, not five.

**The standardization principle it now serves (Berton, this session).** A *canonical
boundary contract*: prove the correct way to cross boundary-type X once, then conform
every crossing of type X to that one proven handler. The payoff is a smaller error
surface (one handler, not N), future changes that know the proven pattern everywhere, and
a boundary understood once. The opposite is what the codebase has been living: ADR-008's
convenience-displacement ratchet, where helper.py reinvented handlers that Patrick's
substrate already provides. So each boundary cell below carries a **canonical handler**
(the one proven crossing) and **conformance** (which instances use it, which diverge).
Patrick's canon is the default canonical handler per the standing rule.

---

## 0.5 Correction: there is one loop, and it is the runtime loop

An earlier pass this session reported that the running image and the host tree were
different loops, with the runtime being a stub. That was a measurement error.
`docker run --rm clarityclaw-omega-clarityclaw cat .../src/loop.metta` reads the baked copy
inside the image, not the file the live container executes. The live container
`clarity_omega` runs the `loop.metta` in the project knowledge area. There is one loop.

The runtime loop binds the real output verdict (`compute-output-verdict`), gates execution
(`output-decision`, `apply-corner-gate`, with `$sexpr_verdict` set to `()` on a pause
decision), routes the input PAUSE halt through the substrate primitive `soul-pause?`,
journals PAUSE and FLAG via `soul_governance.journal_append`, composes the pause note via
`pause_note_compose`, and its `HandleError` captures `$a` into `&error`. The Python
`helper.soul_is_pause` is dead code (returns 0, unused). The verdict/governance machinery
(B13) is LIVE, not stubbed and not dark. All boundary code is in Appendix A, read from the
runtime files.

---

## 1. Boundary inventory (status at a glance)

| # | Boundary | Grounding | Status | Conformance |
|---|----------|-----------|--------|-------------|
| B1 | Human to Substrate (MM in) | [SRC] | WORKING + auth gate | single handler (channels.receive) |
| B2 | Substrate to LLM (prompt out) | [SRC] | WORKING + determination-loss | divergent (see B2a) |
| B3 | LLM to Substrate (response parse) | [SRC] | parse chain runtime-grounded; HandleError captures `$a` | divergent (4+ handlers) |
| B4 | Substrate to Substrate (eval) | [SRC] | WORKING, semantics-trap | single (eval under budget) |
| B4a | Nested skill-arg re-parse | [SRC] | SUSPECT (the \|- home) | single (metta skill) |
| B5 | Substrate to/from Python (Janus) | [SRC] | WORKING-BY-DESIGN | canonical = string-safe |
| B6 | Substrate to Human (MM out) | [SRC] | DEFECT analyzed (Section 3) | DIVERGENT (3 decode sites) |
| B7 | Substrate to ChromaDB/file | [SRC] | WORKING + silent-miss class | divergent writers |
| B8 | Process/container (crash) | [SRC] partial | IMPROVED (callProvider resilient) | n/a |
| B9 | Cycle N to N+1 (state) | [SRC]+[MOUNTED-LIVE] | WORKING, SSI-critical | single (change-state!/files) |
| B10 | Substrate to Skill-dispatch | [SRC] | SUSPECT (3 sources of truth) | DIVERGENT (getSkills / registry / hardcoded) |
| B11 | Python to external API (provider) | [SRC] | WORKING, resilient | single (callProvider) |
| B12 | Embedding | [SRC] | DOWNGRADED (local e5-large-v2) | single (useLocalEmbedding) |
| B13 | Verdict/governance (soul determination to exec gate) | [SRC]+[MOUNTED-LIVE] | LIVE: compute-output-verdict, output-decision, corner gate, journal | functioning; standardization candidate |

Headline: the verdict/governance boundary (B13) is now mapped and is live: the soul's
determination reaches the execution gate, `compute-output-verdict` computes the verdict,
`output-decision` gates the batch (a pause decision sets `$sexpr_verdict` to `()`), the
corner gate applies, and PAUSE/FLAG are journaled. B3's `HandleError` captures `$a` into
`&error` in the runtime. B6's leak mechanism is analyzed (Section 3). The live divergences
worth standardizing are B6 (three decode sites), B10 (three skill registries), and B3 (the
multi-handler response-normalization chain). The remaining gaps are B3 multi-command
delivery, B4a the `|-` form, and B7/B8 silent-miss plus the crash guard.

---

## 2. Retired and corrected

- **B3 HandleError captures `$a` in the runtime.** The runtime `loop.metta` `HandleError`
  is `(($msg $cmd $a))`: it captures the error payload `$a` into `&error` (commit
  `ee50f68`). 01b M3's "live HandleError discards `$a`" describes an older state and is the
  stale claim. An earlier pass this session reversed this from a baked-image misread; that
  reversal is retracted. [SRC: loop.metta HandleError]
- **`main.pl` retired.** There is no `main.pl` application source. The runtime is PeTTa
  (SWI-Prolog MeTTa interpreter); `utils.metta` imports `swrite`/`sread`/etc. via
  `import_prolog_function`, i.e. they are engine builtins. Substrate handlers live in
  `.metta` files. Any `main.pl` in the container is the engine entrypoint, not auditable
  repo source. [SRC: utils.metta]
- **B12 downgraded.** `[STALE-BELIEF]` against CLAUDE_ORIENTATION (which says OpenAI
  text-embedding-3-large is required). Live default is `embeddingprovider Local` ->
  `lib_llm_ext.useLocalEmbedding` -> `SentenceTransformer("intfloat/e5-large-v2")`. No
  external embedding API in the default config; an OpenAI path exists but is not default.
  [SRC: memory.metta, lib_llm_ext.py]

---

## 3. RESOLVED: the string-safe / `_newline_` leak (the worked inverted-trace example)

This is the headline of the original v2. v1 listed the leak as a known defect with an open
investigation (string_safe_encode_decode_asymmetry.md asked: what are all output paths,
which reverse the tokens, why does instability correlate). Tracing backward from the
human-visible output (an E1 inverted trace) through the now-readable handlers answers all
three.

**The encode (one site).** `string-safe` (utils.metta) encodes three tokens on the way
out: `"` -> `_quote_`, newline -> `_newline_`, `'` -> `_apostrophe_`. It wraps the whole
prompt in getContext and the inbound message in `(string-safe (repr (receive)))`.
[SRC]

**The decode (THREE sites, three different coverages).** [SRC]
1. `lib_llm_ext` provider `_clean_text` (applied to the LLM response inside `chat()`):
   reverses `_quote_` AND `_apostrophe_`. NOT `_newline_`. Runs only on the `callProvider`
   path (Friendli/GLM, ASIOne, etc.).
2. `balance_parentheses` (helper.py, on every response): reverses `_quote_` only.
3. `channels.send` + `mattermost.send_message`: a matched pair for REAL newlines
   (`\n` -> `\\n` -> `\n`); blind to the `_newline_` TOKEN.

**Why the leak, precisely.** No site anywhere reverses `_newline_`. `_apostrophe_` is
reversed only on the `callProvider` path; the OpenAI `useGPT` path bypasses `_clean_text`,
so under OpenAI even `_apostrophe_` can leak. The token enters the prompt via
`string-safe`; when Clarity reproduces prompt content (more often when looping or unstable,
which is the instability correlation), the token rides her output through a decode chain
that never reverses it, and surfaces in Mattermost as literal `_newline_` (and
path-dependently `_apostrophe_`). The one behavioral link still to confirm live is "she
reproduces the prompt token verbatim," but the structural chain is source-grounded.

**Why this is the poster child for the canonical-contract work.** One set of three tokens
is encoded at one site and decoded at three sites with three different, incompatible
coverages. The canonical contract is obvious once seen: ONE decode that reverses all three
string-safe tokens, applied once at a single defined point on every output path. Today the
coverage is `_clean_text` {quote, apostrophe}, `balance_parentheses` {quote}, send
{real-newline}, union missing `_newline_` entirely and apostrophe path-dependent.

**Constraint (unchanged).** Do NOT fix by making `string-safe`'s decode symmetric across
the py-call boundary; `string-safe` is the B5 crash-safe marshal boundary. The fix is a
single full-coverage decode on the output side, not a change to the encoder. Root-cause-
first, and it is now root-caused.

---

## 4. The boundaries in detail (grounded)

### B1. Human to Substrate (MM inbound) [SRC]
**Crosses.** Human text. **Transform.** `channels.receive` -> `mattermost.getLastMessage`
(drain-on-read; multiple messages between reads concatenated with " | ");
`(string-safe (repr (receive)))`; `extract_username` parses `name: text`. **Auth
sub-boundary:** `mattermost._is_allowed_message` gates on `OMEGACLAW_AUTH_SECRET`;
when set, only the authenticated user passes and the auth message itself is withheld.
**Status.** WORKING with an access-control gate. **Canonical handler.** `channels.receive`
(single). **Open (live).** Confirm whether the auth secret is set in the running env.

### B2. Substrate to LLM (prompt outbound) [SRC]
**Crosses.** The prompt and the send. **Transform.** getContext wraps in `string-safe`;
`$enriched_prompt` prepends `soul_governance.pause_context` + soul-brief;
`soul_send_assemble` builds `$send`; dispatch via `callProvider` (or `useGPT` for OpenAI).
**B2a determination-loss [SRC].** `soul_send_assemble` collapses the verdict to a bare
PAUSE/FLAG/PROCEED token, dropping SOUL-TONE/PATTERNS/TENSION/REASON; note added only on
FLAG. On PROCEED neither tone nor note reaches the call. This is 01b Tier 1.2's target.
Note: this is the input-side determination-loss; the OUTPUT-side determination IS computed
in the runtime (B13). **B2b.** `soul_send_assemble` emits no `:-:-:-:`
delimiter, so the GLM/`callProvider` path puts the ENTIRE send in the system message and
leaves the user message empty (`usermsg = spl[1] if len(spl) > 1 else ""`). Not a crash; a
flattened role split worth a design look. **Canonical handler.** Should be one
send-assembler that (a) carries the determination on PROCEED via FLAG-injection and (b)
emits the provider's expected sys/user split. **Conformance.** Divergent today (strip + no
delimiter). **Open.** Confirm the loop `$send` call site binds `soul_send_assemble`.

### B3. LLM to Substrate (response parse) [SRC]
**Crosses.** Clarity's raw response. **Transform chain.** provider `_clean_text`
-> `balance_parentheses` (quote-decode, garbage-to-`(pin ...)`, paren-balance) ->
`normalize_string` (UTF-8) -> `sanitize_response` (strip non-ASCII to `?`) ->
`wrap_if_bare_command` (wrap bare single command, hardcoded 13-skill gate) -> `first_char`
gate -> `(catch (sread $response))` -> HandleError. **Headline.** The runtime `HandleError`
is `(($msg $cmd $a))`: it captures the eval-error payload `$a` into `&error` (commit
`ee50f68`). On the single-command path the captured detail reaches `&lastresults` ->
`LAST_SKILL_USE_RESULTS`. (An earlier pass this session claimed the runtime discarded `$a`,
read from a baked-image misread; retracted.) **Status.** Parse chain runtime-grounded.
Durable structural facts: `&error` is not in the prompt block, so a whole-batch parse
failure delivers feedback to Clarity through the `addToHistory` ERROR_FEEDBACK write rather
than through `LAST_SKILL_USE_RESULTS`. The single-command detail-surfacing path is live; the
multi-command whole-batch path remains the gap to confirm by behavioral test.
**Canonical handler.** The most divergent boundary: four-plus string handlers on one
crossing, several reinventing canon. The contract should be one normalization pass.
**Conformance.** DIVERGENT. **Open (live).** One controlled malformed-command test, run as
a standalone Docker probe, to confirm the whole-batch multi-command delivery path end to
end.

### B4. Substrate to Substrate (command eval) [SRC]
**Transform.** Per-command `superpose`/`eval` under `(catch ...)`; the metta skill adds a
`call_with_inference_limit` 100M budget. The runtime gates the batch: it evaluates
`$sexpr_gated` (the corner-gate output) and binds `$sexpr_verdict` to `()` on a pause
decision. **Semantics-trap.** `|-` computes, persists nothing; `add-atom` is the only
commit; `|-nal` reduces live-loop only; multi-command `add-atom` silently partially fails.
**Canonical handler.** eval-under-budget (single, correct). **Open.** None blocking;
semantics RESOLVED in the Atom Operations Map.

### B4a. Nested skill-argument re-parse [SRC] -- the `|-` home
**Transform.** `(= (metta $str) (let $code (sread $str) (repr (progn
(call_with_inference_limit (Predicate (quote (eval $code $x))) 100000000) $x))))`. The
metta skill `sread`s its string arg with no inner catch; the inner failure propagates to
the OUTER `(catch ...)` so it surfaces as `(Error $a $b)`. The runtime HandleError keeps
`$a`, so the real inner-parse reason reaches her. **Three contributing `|-`
failure causes, all source-grounded.** (1) The SKILLS prompt still instructs `|-` and calls
it reliable, including for revision, while it does not persist (Gap B / 01b M1). (2) The
prompt's NAL example contains a non-ASCII multiplication sign that `sanitize_response`
replaces with `?`, corrupting any copied command. (3) The example shows the bare
`(metta (|- ...))` form, but the impl `sread`s a string `$str`; bare-vs-string is the
form-sensitivity that produced the mixed `(partial ...)`-vs-error history. Live note this
session: an inner-unbalanced `(metta "(match &self (foo $x) $x")` returned `true` (silent
apparent success, classified exploration-query), a B4a inner-re-parse failure that was not
surfaced. **Status.** SUSPECT, now explained. **Canonical handler.** the metta skill
(single). **Open (live).** Confirm the inner `sread` failure handling against the image;
decide Intervention 2 (teach add-atom workflow, remove the non-ASCII char, fix the
bare-vs-string form).

### B5. Substrate to/from Python (Janus marshal) [SRC]
**Transform.** Janus; `string-safe (repr ...)` is the marshal-safe stringifier.
**Status.** WORKING-BY-DESIGN; the throw on an unbound/compound value is correct.
**Canonical handler.** `string-safe`. THE load-bearing constraint: do not move
stringification across py-call (reintroduces the a318abc/69c73fc crash).

### B6. Substrate to Human (MM outbound) [SRC] -- defect analyzed (Section 3)
**Transform.** `channels.send` (`&lastsend` dedup of byte-identical consecutive send;
`\n`->`\\n`) -> `mattermost.send_message` (`\\n`->`\n`, POST). **Dedup gap.** `&lastsend`
catches only byte-identical consecutive sends, missing near-duplicates and interleaved
duplicates (reconciles spam H2). **Leak.** Analyzed in Section 3: three decode sites, none
covering `_newline_`.
**Canonical handler.** one full-coverage string-safe decode on the output side, applied
once. **Conformance.** DIVERGENT (the clearest standardization target in the audit, once
confirmed against the image).

### B7. Substrate to ChromaDB / file (persistence) [SRC]
**Transform.** `remember`/`query` -> `lib_chromadb`; `embed` applies `string-safe` then
local encode; `write-file`/`append-file` via Prolog open/write/close (no absolute-path
enforcement in the function; CWD-relative paths silently vanish at runtime);
`addToHistory` appends to history.metta including ERROR_FEEDBACK when `&error` non-empty; a
SQLite-backed promotion/salience layer dual-writes to atomspace. **Status.** WORKING with
the silent-miss class (multi-command `add-atom` partial fail; relative write-file vanish).
**Canonical handler.** the proven belief-revision writer: remove-by-variable-then-add,
absolute-path write-file, match-count verify (Atom Operations Map). **Conformance.**
divergent until that writer is the only write pattern. **Open (live).** confirm
`lib_chromadb` failure surfacing.

### B8. Process / container (crash) [SRC] partial -- IMPROVED
**Transform.** `(catch (sread $response))` at parse; `balance_parentheses` garbage-pin;
`callProvider` is RESILIENT (returns "" + logs on provider error, does not raise), so the
provider leg no longer crashes the loop (it did pre-GLM-switch). **Status.** IMPROVED but
the eval-path hard-malformation crash guard is still unconfirmed (01b M4).
**Open (live).** one carefully-controlled hard-malformation test, last (it restarts the
container), run as a standalone Docker probe.

### B9. Cycle N to N+1 (state) [SRC]+[MOUNTED-LIVE] -- SSI-critical
**Transform.** `change-state!`/`set-atom!` persist within a process; `&error` cleared each
cycle; ChromaDB `remember` and history.metta survive rebuild; in-AtomSpace `&self` wiped on
rebuild. **Status.** WORKING; the disposition-persistence surface SSI Tier 5 wires onto.
**Canonical handler.** state atoms + file persistence (single). **Open.** none blocking.

### B10. Substrate to Skill-dispatch [SRC] -- THREE sources of truth
**Transform.** `dispatch-skills $k` (Sprint 0-Coda registry, live); `getSkills`
(skills.metta, the static 13-item list) is legacy-but-still-defined; `wrap_if_bare_command`
hardcodes its own 13-item set (helper.py). The static two currently agree but are
independent copies, and the registry is a third. **Status.** SUSPECT (drift risk across
three sources). **Canonical handler.** the live registry, with both other lists derived
from it rather than hand-maintained. **Conformance.** DIVERGENT. **Open (live).** read the
live registry; diff against the two hardcoded 13s (confirm the helper.py list against the
image); decide derive-vs-sync.

### B11. Python to external API (provider leg) [SRC]
**Transform.** `callProvider(provider, content, max_tokens=6000)` dispatches to a registry
(ASICloud, Anthropic claude-opus-4-6, ASIOne, Friendli GLM-5.1, Friendli52 GLM-5.2, OpenAI
gpt-5.4); default Friendli. GLM uses nested `extra_body` thinking config with a
`reasoning_content` fallback. Resilient: API failure -> "" + log. **Status.** WORKING. A
truncated/empty response re-enters at B3 as a possibly malformed batch, so do not
misattribute B11 failures to B3. Live note: a chain-of-thought leak (GLM reasoning
monologue arriving in the command channel) was observed this session and is a B3/B11
pollutant worth its own probe under a normal (non-adversarial) request. **Canonical
handler.** `callProvider` (single).

### B12. Embedding [SRC] -- DOWNGRADED to local
**Transform.** default `embeddingprovider Local` ->
`lib_llm_ext.useLocalEmbedding` -> `SentenceTransformer("intfloat/e5-large-v2")`,
normalize_embeddings=True. No external API in default config. **Status.** local model;
an outage here is not an external-API dependency. **Canonical handler.**
`useLocalEmbedding` (single).

### B13. Verdict/governance: soul determination to execution gate [SRC]+[MOUNTED-LIVE] -- LIVE

**Crosses.** The soul's determination (input verdict and output verdict) into the decision
that gates execution. This is the soul-downstream boundary named in First-Principles
Section 5.

**Transform, in the runtime (two crossings, both live).**
- Output verdict. The loop binds `$soul_verdict_out` to `(compute-output-verdict $metta_cmds
  $soul_gate_state)` and `$soul_decision` to `(output-decision $metta_cmds $soul_gate_state)`.
  On a pause decision it sets `$sexpr_verdict` to `()` (the batch does not execute), prints
  `(SOUL-SUPPRESSED $sexpr)`, and journals via `soul_governance.journal_append "PAUSE"`; on
  flag it journals "FLAG"; it composes `&last_pause_note` via `pause_note_compose`. The
  batch then runs through `apply-corner-gate` and `gate-aware-results`. [SRC]
- Input verdict. `$soul_verdict_in` is computed via `soul-llm-call (helper.soul_eval_prompt
  ...)` and sanitized by `soul_verdict_sanitize`; on a non-proceed verdict it records an
  advisory soul-note (gated on the substrate `soul-proceed?`). The PAUSE-HALT branch is
  `(if (soul-pause? $soul_verdict_in) <Channel D voice; halt; loops 0> ...)`, routed through
  the substrate primitive `soul-pause?` (Repair 3). The Python `helper.soul_is_pause` is dead
  code (returns 0, unused). [SRC: loop input path; soul_utils.metta soul-pause? body not read
  this pass]

**The soul-side machinery is live.** `compute-output-verdict` (output_verdict.metta, the
if-ladder returning PAUSE on pending/conflict, PROCEED on empty batch, else `batch-rank`),
`output-decision`, `batch-rank` (recurses taking the max of `output-cmd-rank` per command),
`derive-gate-state`, and the corner gate (`apply-corner-gate`, `gate-aware-results`) are all
present in the mounted soul dir and called by the running loop. The governance hands
(`soul_governance.py`: `path_scope`, `repr_kind`, `journal_append`, `pause_note_compose`,
`pause_context`, `approval_scan`, `mutation_fingerprint`) are imported and called. Full code
in Appendix A.

**On malformation / soul-absence.** The determination reaches the execution gate: a pause
decision blanks the batch, a soul mutation routes through the gate-state classifier
(`derive-gate-state`: pending/conflict/clean) and the verdict ladder. The remaining
soul-absence surface is upstream at B2 (the determination is stripped from the PROCEED-path
prompt), not at this gate.

**Status.** LIVE. Output verdict computed, execution gated on the decision, input PAUSE
routed through the substrate primitive, PAUSE/FLAG journaled.

**Canonical handler.** The soul's determination reaches the execution gate via the soul-side
`compute-output-verdict` ladder; the determination is computed in the substrate and
rendered, never re-decided by the LLM (ADR-008). This boundary conforms to that law today.

**Conformance.** Functioning. Standardization candidate only in the sense of confirming the
gate-state writer/consumer coupling (the `clarity-soul-mutation-pending-set!` writer vs
`derive-gate-state` / `soul-mutation-pending?` reader).

**Open.** Confirm the gate-state writer path end to end (the mutation-pending lock write and
its read by `derive-gate-state`), and the `soul_utils.metta` `soul-pause?` / `soul-proceed?`
bodies.

---

## 5. E2 inverted trace: what reaches Clarity's prompt, walked backward [SRC]

The prompt is the SSI-critical surface (what she actually reasons over). getContext (and
the loop's `$enriched_prompt`) assemble it; walking each field backward through its
boundaries shows where divergent handling converges on one input.

The prompt string is `(string-safe (...))` over: PROMPT (getPrompt reads
memory/prompt.txt), SKILLS (`dispatch-skills`, B10, three-source divergence upstream),
output-format-guidance, YOUR_LAST_ACTION (recent-action atoms, B9), TASK-STATE / idle /
agency blocks (state atoms, B9), LAST_SKILL_USE_RESULTS (`&lastresults`, set from
`safe_results_str (repr $results_final)`), HISTORY (getHistory reads memory/history.metta
tail, which carries ERROR_FEEDBACK from `addToHistory`), TIME. Then `$enriched_prompt`
prepends `pause_context` (B13) and the soul-brief.

Three findings from the backward walk:
1. **Every field is `string-safe`-encoded as a block.** So `_newline_`/`_apostrophe_`
   tokens are present throughout her prompt, which is the upstream source of the B6 leak
   (she can reproduce any of them). The prompt is where the token is born; B6 is where it
   escapes undecoded.
2. **`$a` reaches her on the single-command path.** The runtime `HandleError` captures `$a`
   into `&error`; `&error` is written to history as ERROR_FEEDBACK by `addToHistory` and the
   single-command return reaches `&lastresults` -> `LAST_SKILL_USE_RESULTS`. So the `|-`
   loop can in principle self-correct from the parse-failure detail. The whole-batch
   multi-command delivery path is the one to confirm by behavioral test. (An earlier pass
   claimed `$a` was discarded in the runtime, from a baked-image misread; retracted.)
3. **SKILLS is the B10 three-source convergence point.** Whichever of getSkills /
   registry / hardcoded-list is authoritative for her prompt, the other two can silently
   diverge from it. The inverted trace localizes the drift risk to one prompt field.

E1 (human output) was effectively traced in Section 3. E3 (persistence), E4 (crash), and
E5 (verdict) traces: E5 is answered by B13 (the runtime gates execution on the verdict).
The remaining traces follow once the live registry and the `soul_utils.metta` predicate
bodies are read; none is blocking.

---

## 6. Reinvention map (helper.py vs Patrick's canon)

Per the standing rule that Patrick's work is canon and helper.py is the reinvention to
audit against it. Candidates where helper.py holds a string/normalization handler that
canon or another layer already covers:
- `balance_parentheses` (helper.py) overlaps the provider `_clean_text` (lib_llm_ext) on
  `_quote_`; both decode the same token, neither covers `_newline_`. Two partial decoders
  for one contract (Section 3).
- `normalize_string` + `sanitize_response` (helper.py) are two passes over the same
  response string for UTF-8/ASCII safety, where canon's response path is simpler (the
  upstream loop copy shows a far shorter normalize chain).
- `safe_results_str` (helper.py) reimplements stringification that `string-safe` (canon,
  utils.metta) is the marshal-safe answer for.
- `wrap_if_bare_command`'s hardcoded skill list (helper.py) duplicates getSkills /
  registry (B10).
These are the convenience-displacement ratchet made concrete. The standardization pass
would, per boundary type, pick the canonical handler (canon first) and converge these onto
it. This map is the input to that pass, not the pass itself (audit, not fix).

---

## 7. Consolidated status and the prioritized next list

**Top finding.** The verdict/governance boundary (B13) is live: the soul's determination
reaches the execution gate, `compute-output-verdict` computes the verdict, `output-decision`
gates the batch, the corner gate applies, and PAUSE/FLAG are journaled. The earlier
session claim of a stub running loop was a baked-image misread and is retracted (Section
0.5).

**Resolved/analyzed this pass.** B13 verdict/governance characterized from the runtime
(live output verdict, gated execution, substrate-primitive input PAUSE). B3 HandleError
confirmed to capture `$a` in the runtime. B6 leak mechanism analyzed (Section 3). `main.pl`
retired. B12 downgraded. B4a `|-` causes enumerated. B11 resilience confirmed. B10 third
source found. The full per-boundary runtime code is in Appendix A.

**Live-confirmation list (read-only, priority order).**
1. The gate-state writer/consumer coupling (B13): the `clarity-soul-mutation-pending-set!`
   writer vs the `derive-gate-state` / `soul-mutation-pending?` reader, end to end.
2. The `soul_utils.metta` predicate bodies (`soul-pause?`, `soul-proceed?`, `soul-flag?`)
   that consume the verdict string (B13).
3. The live capability registry vs the two hardcoded 13-item lists (B10).
4. Whether `OMEGACLAW_AUTH_SECRET` is set in the running env (B1).
5. A controlled malformed-command test (B3/B4a) as a standalone Docker probe, for the `$a`
   shape and the whole-batch multi-command delivery path.
6. A carefully-controlled hard-malformation crash test (B8), last.

**Then, the canonical-contract pass (fix phase, after live confirms).** Per divergent
boundary, name and verify the one canonical handler and converge instances: B6 (one
full-coverage output decode), B10 (registry as sole source), B3 (one normalization pass),
B2 (one send-assembler that carries the determination on PROCEED).

No fix is proposed here by design.

---

## 8. Maintenance contract (unchanged from v1, extended)

Updated in the same commit as any boundary change; new boundaries added as B-cells with
grounding tags; NEEDS-LIVE upgraded to a live tag with date on read; single source of
truth for boundary status; cross-referenced from the malformation pre-build and 01b
M1-M4. NEW: cells are grounded to the live runtime (the project knowledge files the running
container executes); a read of a throwaway container made from the image
(`docker run --rm <image> cat`) is not recorded as a runtime fact, since it prints the
baked copy, not what the live container runs. When in doubt about a src file, read the live
container (`docker exec clarity_omega ...`) or its mount list. Appendix A carries the
per-boundary runtime code and is re-confirmed on any rebuild that touches the named files.

---

# ClarityOmega Boundary Transition Audit, Appendix A: Per-Boundary Runtime Code

**Status:** Companion appendix to `000_ClarityOmega_Boundary_Transition_Audit_v2.md`.
Reference object, not narrative. Intended to be dropped in as a new appendix.
**Source:** project knowledge runtime files (the current runtime), plus the three
supplied gate and governance files (`output_verdict.metta`, `corner_gate.metta`,
`soul_governance.py`).
**Read date:** 2026-06-23. Read end to end, not grepped.
**No em-dashes. Code is verbatim from the source read; load-bearing lines only.**

---

## A.0 What this appendix is

Every boundary in the at-a-glance inventory and in Section 4 is described in prose:
a paraphrase of what the crossing does, plus a pointer to the file and function. This
appendix places the actual runtime code beside the boundary it implements, so each
boundary can be checked against the code rather than trusted as a paraphrase.

## A.1 Why it earns its place

A paraphrase can be faithful to the code and false about the system at the same time,
and in prose the two are indistinguishable. This is not hypothetical. The prior v2 said
"HandleError captures `$a`," which was a faithful paraphrase of one source and a false
statement about another; the contradiction cost most of a session to surface because
prose hid it. Code beside the claim collapses that gap. This is Principle 0 (reason from
facts verified now, not from a frame) applied to the audit itself.

## A.2 What it makes possible

The appendix turns the audit from a set of claims into a checkable object. With every
boundary's code in one place:

1. Completeness becomes provable. Grep the assembled code for the crossing primitives
   (`py-call`, `sread`, `eval`, `add-atom`, `match`, `change-state!`, `set-atom!`,
   `write-file`, `receive`, `send`). Every hit is a boundary. The 14 either account for
   all hits or a fifteenth boundary has been found. The inventory stops being
   best-effort and becomes provably exhaustive or provably incomplete with the missing
   crossing named.
2. Forward and backward tracing has visible gaps. A value followed from birth to death
   through the present code shows any unhandled step as a missing line, not a hypothesis.
   The `_newline_` leak is exactly this: encoder and all decoders side by side make the
   uncovered token a blank cell.
3. The canonical-contract pass runs by inspection. All instances of one boundary type
   side by side make the canonical handler computable, not argued: the decoders' token
   coverage, the three skill lists' contents, each helper reinvention against canon.
4. Coupling is verifiable. Producer output and consumer input both present means
   shape-match is checkable (encoder token set vs decoder reversal; writer atom shape vs
   reader `match` pattern; the metta skill's inner `sread` vs the outer parse).
5. Doc-versus-code contradictions surface across every boundary at once, not one
   accidental discovery at a time.
6. It is a drift-proof reference. The fix phase and the SSI build run against stamped
   code, not against line pointers that rot.

## A.3 How to use it

Locus is given as file plus function name, which is stable across rebuilds. Line numbers
are deliberately omitted: they differ between builds and would reintroduce the exact
staleness this appendix exists to remove. To find a boundary's code, read its function
in the named file. The index below is code-free and scannable; the code lives in the
per-boundary sections that follow it.

---

## A.4 At-a-glance index (code-free)

| B | Crossing | Primary file(s) | Key symbols | Note |
|---|----------|-----------------|-------------|------|
| B1 | Human to Substrate (MM inbound) | `mattermost.py`, `channels.metta`, `loop.metta` | `getLastMessage`, `_is_allowed_message`, `receive`, `$msgrcv` | auth gate on `OMEGACLAW_AUTH_SECRET`; drain-on-read; `" | "` concat |
| B2 | Substrate to LLM (prompt outbound) | `helper.py`, `lib_llm_ext.py` | `soul_send_assemble`, provider `.chat` split | verdict collapsed to bare token; no `:-:-:-:` delimiter in assemble |
| B3 | LLM to Substrate (response parse) | `loop.metta`, `helper.py` | `balance_parentheses`, `sanitize_response`, `wrap_if_bare_command`, `sread`, `HandleError` | most divergent; 4+ string handlers on one crossing |
| B4 | Substrate to Substrate (command eval) | `loop.metta` | `eval`, `collapse`, `superpose`, `HandleError` | `(collapse (eval $s))` per command |
| B4a | Nested skill-argument re-parse | `skills.metta` | `metta`, `sread`, `call_with_inference_limit` | inner `sread`; `|-` instructed in `getSkills` |
| B5 | Substrate to/from Python (Janus marshal) | `utils.metta` | `string-safe` | crash-safe marshal boundary; do not touch |
| B6 | Substrate to Human (MM outbound) | `channels.metta`, `mattermost.py`, `helper.py`, `lib_llm_ext.py` | `send`, `send_message`, `balance_parentheses`, `_clean_text` | `_newline_` reversed nowhere |
| B7 | Substrate to ChromaDB / file | `memory.metta`, `skills.metta` | `remember`, `query`, `embed`, `appendToHistory`, `write-file` | no absolute-path enforcement on file writes |
| B8 | Process / container (crash) | `lib_llm_ext.py`, `loop.metta` | `callProvider`, `(catch (sread ...))` | provider returns "" + logs; parse `catch` |
| B9 | Cycle N to N+1 (state) | `loop.metta` | `initLoop`, `change-state!`, `&error` clear | `&error` cleared each cycle; `&self` wiped on rebuild |
| B10 | Substrate to Skill-dispatch | `skills.metta`, `helper.py`, `loop.metta` | `getSkills`, `wrap_if_bare_command` known-skills, `dispatch-skills` | three sources of the skill set |
| B11 | Python to external API (provider leg) | `lib_llm_ext.py`, `loop.metta` | provider registry, `callProvider` | default `Friendli` |
| B12 | Embedding | `lib_llm_ext.py`, `memory.metta` | `useLocalEmbedding`, `initLocalEmbedding` | local `e5-large-v2`, not OpenAI |
| B13 | Verdict / governance | `loop.metta`, `output_verdict.metta`, `corner_gate.metta`, `soul_governance.py` | `compute-output-verdict`, `output-decision`, `apply-corner-gate`, `soul-pause?` | see A.6 reconciliation note |

---

## A.5 The code, per boundary

### B1 Human to Substrate (MM inbound)

`mattermost.py`:
```python
def _set_last(msg):
    with _msg_lock:
        if _last_message == "":
            _last_message = msg
        else:
            _last_message = _last_message + " | " + msg

def getLastMessage():
    with _msg_lock:
        tmp = _last_message
        _last_message = ""
        return tmp

def _is_allowed_message(user_id, msg):
    candidate = _parse_auth_candidate(msg)
    with _auth_lock:
        if not _auth_secret:
            return True
        if candidate == _auth_secret:
            if _authenticated_user_id is None:
                _authenticated_user_id = user_id
            return False
        if _authenticated_user_id is None:
            return False
        return user_id == _authenticated_user_id

# _ws_loop, on a posted event:
#   if _is_allowed_message(user_id, message):
#       name = _get_display_name(user_id)
#       _set_last(f"{name}: {message}")
```

`channels.metta`:
```
(= (receive)
   (if (== (commchannel) irc)
       (py-call (irc.getLastMessage))
       (py-call (mattermost.getLastMessage))))
```

`loop.metta`:
```
($msgrcv (string-safe (repr (receive))))
($msgnew (prog1 (and (> (string_length $msgrcv) 0) (!= $msgrcv (get-state &prevmsg)))
                (if (> (string_length $msgrcv) 0) (change-state! &prevmsg $msgrcv) _)))
($msg (get-state &prevmsg))
```

### B2 Substrate to LLM (prompt outbound)

`helper.py`:
```python
def soul_send_assemble(prompt, soul_context, soul_verdict, person_state, soul_note, lastmessage, idle_directive=""):
    verdict_str = str(soul_verdict)
    if "VERDICT: PAUSE" in verdict_str:   verdict_summary = "VERDICT: PAUSE"
    elif "VERDICT: FLAG" in verdict_str:  verdict_summary = "VERDICT: FLAG"
    elif "VERDICT: PROCEED" in verdict_str: verdict_summary = "VERDICT: PROCEED"
    else:                                  verdict_summary = "VERDICT: PROCEED"
    soul_note_str = str(soul_note)
    note_section = (" SOUL-NOTE: " + soul_note_str) if soul_note_str else ""
    idle_str = str(idle_directive)
    idle_section = (" IDLE_DIRECTIVE: " + idle_str) if idle_str and len(idle_str) > 5 else ""
    return (str(prompt) + idle_section
            + " SOUL_CONTEXT: " + str(soul_context)
            + " SOUL_VERDICT: " + verdict_summary
            + " PERSON_STATE: " + str(person_state)
            + note_section + " " + str(lastmessage))
```
Determination-strip: the full verdict (PATTERNS, TENSION, SOUL-TONE, REASON) is reduced
to one of three bare `VERDICT:` tokens; the note section is present only when `soul_note`
is non-empty, which `soul_extract_flag_note` produces only on FLAG.

Provider split (`lib_llm_ext.py`, GlmProvider.chat):
```python
spl = content.split(":-:-:-:")
sysmsg = spl[0]
usermsg = spl[1] if len(spl) > 1 else ""
```
`soul_send_assemble` emits no `:-:-:-:` delimiter, so the split yields the whole send as
`sysmsg` and an empty `usermsg`.

CONFIDENCE NOTE: `soul_send_assemble` and the provider split are read directly. The loop
call site that binds `$send` (assemble vs the upstream `py-str ($prompt :-:-:-: $lastmessage)`)
was not re-read end to end this pass; confirm at the loop's `$send` line.

### B3 LLM to Substrate (response parse)

`loop.metta`:
```
($respi (if (== (provider) OpenAI)
            (useGPT (LLM) (maxOutputToken) (reasoningMode) $send)
            (py-call (lib_llm_ext.callProvider (provider) $send (maxOutputToken)))))
($resp (py-call (helper.balance_parentheses $respi)))
($response (if (== "(" (first_char $resp)) $resp
               (progn (println! $resp) (repr (REMEMBER:OUTPUT_NOTHING_ELSE_THAN: ((skill arg) ...))))))
($sexpr (catch (sread $response)))
($_ (change-state! &error ()))
($_ (HandleError MULTI_COMMAND_FAILURE_NOTHING_WAS_DONE_PLEASE_CORRECT_PARENTHESES_AND_USE_QUOTES_AND_RETRY $response $sexpr))
```

`HandleError` definition (`loop.metta`), the runtime captures `$a`:
```
(= (HandleError $msg $cmd $sexpr)
   (case $sexpr
     (((Error $a $b) (let $new (append (get-state &error) (($msg $cmd $a)))
                          (progn (change-state! &error $new) ($msg $cmd $a))))
      ($else $sexpr))))
```

`helper.py` string handlers on this crossing:
```python
def sanitize_response(s):
    return s.encode('ascii', errors='replace').decode('ascii')

def wrap_if_bare_command(s):
    # wraps a bare single command iff first token is in known_skills (13 items)
    ...

# balance_parentheses reverses _quote_ only, then balances parens, garbage -> (pin ...)
```

### B4 Substrate to Substrate (command eval)

`loop.metta`:
```
($sexpr_gated (apply-corner-gate $sexpr_verdict))
($results (RESULTS: (collapse (let $s (superpose $sexpr_gated)
            (COMMAND_RETURN: ($s (HandleError SINGLE_COMMAND_FORMAT_ERROR_NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY
              $s (catch (let $R (collapse (eval $s)) (py-call (helper.normalize_string $R)))))))))))
($results_final (gate-aware-results $results))
```
`(collapse (eval $s))` materializes each command's nondet result stream before binding
(the post-collapse-eval fix). Per-command `HandleError` carries the single-command format
error.

### B4a Nested skill-argument re-parse

`skills.metta`:
```
(= (metta $str)
   (let $code (sread $str)
        (repr (progn (call_with_inference_limit (Predicate (quote (eval $code $x))) 100000000) $x))))
```
The outer parse produces a `(metta "<string>")` command; the `metta` skill `sread`s its
string argument again, a second parse with no inner `catch`. `getSkills` instructs the
`|-` operator and shows the non-ASCII multiplication sign in its NAL examples.

### B5 Substrate to/from Python (Janus marshal)

`utils.metta`:
```
(= (string-replace $str $a $b)
   (atomic_list_concat (split_string $str $a "") $b))

(= (string-safe $str)
   (string-replace (string-replace (string-replace $str "\"\"" "_quote_") "\n" "_newline_") "'" "_apostrophe_"))
```
This is the crash-safe marshal boundary. `(string-safe (repr $results))` keeps
stringification pure-MeTTa so Janus never marshals a possibly-unbound value across
`py-call` (commits a318abc / 69c73fc). Do not move stringification across the py-call
boundary and do not "fix" the decode asymmetry here.

### B6 Substrate to Human (MM outbound)

`channels.metta`:
```
!(change-state! &lastsend "")
(= (send $msg)
   (if (!= $msg (get-state &lastsend))
       (progn (change-state! &lastsend $msg)
              (let $safemsg (string-replace $msg "\n" "\\n")
                   (if (== (commchannel) irc)
                       (let $temp (cut) (py-call (irc.send_message $safemsg)))
                       (let $temp (cut) (py-call (mattermost.send_message $safemsg)))))) _))
```

`mattermost.py`:
```python
def send_message(text):
    text = text.replace("\\n", "\n")
    if not _connected:
        return
    requests.post(f"{MM_URL}/api/v4/posts", headers=_headers,
                  json={"channel_id": CHANNEL_ID, "message": text})
```

Decode sites that exist (`helper.balance_parentheses` reverses `_quote_`;
`lib_llm_ext._clean_text` reverses `_quote_` and `_apostrophe_`):
```python
# lib_llm_ext.AIProvider._clean_text
return text.replace("_quote_", '"').replace("_apostrophe_", "'")
```
No site reverses `_newline_`; `_apostrophe_` is reversed only on the provider
(`_clean_text`) path. `string-safe` (B5) is the encoder; this is the union of decoders.

### B7 Substrate to ChromaDB / file

`memory.metta`:
```
(= (embed $str)
   (if (== (embeddingprovider) Local)
       (py-call (lib_llm_ext.useLocalEmbedding (string-safe $str)))
       (useGPTEmbedding (string-safe $str))))

(= (remember $str) (py-call (lib_chromadb.remember $str (embed $str) (get_time_as_string))))
(= (query $str)    (py-call (lib_chromadb.query (embed $str) (maxRecallItems))))
(= (episodes $time) (py-call (helper.around_time $time (maxEpisodeRecallLines))))

(= (getHistory)
   (let $ret (read-file (library omegaclaw ./memory/history.metta)) (last_chars $ret (maxHistory))))
(= (appendToHistory $addition)
   (append-file (library omegaclaw ./memory/history.metta) (swrite $addition)))
(= (addToHistory $lastmessage $response $sexpr $msgnew)
   (if $msgnew
       (if (== (get-state &error) ())
           (appendToHistory ((get_time_as_string) (newline) "HUMAN_MESSAGE: " $lastmessage (newline) $response (newline)))
           (appendToHistory ((get_time_as_string) (newline) "HUMAN_MESSAGE: " $lastmessage (newline) $response (newline) ERROR_FEEDBACK: (get-state &error))))
       (if (== (get-state &error) ())
           (appendToHistory ((get_time_as_string) (newline) $response (newline)))
           (appendToHistory ((get_time_as_string) (newline) $response (newline) ERROR_FEEDBACK: (get-state &error))))))
```

`skills.metta` file writes (no absolute-path enforcement, CWD-relative):
```
(= (write-file $file $str)
   (progn (translatePredicate (open $file write $Out))
          (translatePredicate (write $Out $str))
          (translatePredicate (close $Out)) True))
(= (append-file $file $str)
   (progn (translatePredicate (exists_file $file))
          (translatePredicate (open $file append $Out))
          (translatePredicate (write $Out $str))
          (translatePredicate (nl $Out)),
          (translatePredicate (close $Out)) True))
```
CONFIDENCE NOTE: `lib_chromadb.remember` / `.query` Python bodies are upstream and were
not read this pass.

### B8 Process / container (crash)

`lib_llm_ext.py`:
```python
def callProvider(provider_name, content, max_tokens=6000):
    provider = _get_provider(provider_name)
    if provider is None:
        print(f"[lib_llm_ext.callProvider] Unknown provider: {provider_name}")
        return ""
    if not provider.is_available:
        print(f"[lib_llm_ext.callProvider] {provider_name} not configured (missing {provider._var_name})")
        return ""
    return provider.chat(model=provider._model_name, content=content, max_tokens=max_tokens)
```
`loop.metta` parse guard: `($sexpr (catch (sread $response)))`. Provider `.chat` bodies
wrap the API call in try/except returning "".

### B9 Cycle N to N+1 (state)

`loop.metta` (`initLoop`, the seeded cross-cycle state):
```
(change-state! &prevmsg "")
(change-state! &lastresults "")
(change-state! &soul_verdict_in  "VERDICT: PROCEED")
(change-state! &soul_verdict_out "VERDICT: PROCEED")
(change-state! &person_state "PERSON-STATE: neutral ACTIVE-NEED: none SOUL-TONE: grounded")
(change-state! &soul_mutation_lock unlocked)
(change-state! &pending_soul_mutation "")
(change-state! &last_pause_note "")
(change-state! &last_gate_fingerprint "")
(change-state! &authorized_approvers "berton_c")
(change-state! &last_human_time 0)
(change-state! &engaged_idle_count 0)
(change-state! &loops (maxNewInputLoops))
(do-bootstrap-task-state!)
```
Per cycle: `($_ (change-state! &error ()))` clears the error each cycle before parse;
`&lastresults` is overwritten post-execution; `history.metta` and ChromaDB persist across
rebuild; AtomSpace `&self` is wiped on rebuild.

### B10 Substrate to Skill-dispatch (three sources; registry coupling closed)

Loaded per manifest `lib_clarity_reasoning.metta` line 107 (`capability_registry`) and line
108 (`capabilities/skill_discovery`). The Path C draft
(`capability_registry_path_c_draft.metta`) and the harness are imported nowhere; they are
scaffolding, not runtime.

READER and getContext hook (`skill_discovery.metta`, loaded, full):
```
(eligible-lifecycle active)

(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ())

(= (skill-discovery $request)
   (let* (($capabilities (collapse (match &self
                                          (registered-capability schema: $s handler: $h
                                            priority: $p lifecycle: active metadata: $m)
                                          ($s $h $p $m))))
          ($formatted (format-skill-set $capabilities)))
         (skill-set skills: $formatted)))

(= (format-skill-set $capabilities) (getSkills))   ;; Option a: emits the hardcoded list today; Sprint 1 swaps this body and retires getSkills

(= (dispatch-skills $k)
   (let $_ (dispatch (skill-request cycle: $k) $k)
        (first-skill-or-default
          (collapse (match &self
                          (dispatch-result invocation-id: $k result: (skill-set skills: $s) handler: $_h)
                          $s)))))

(= (first-skill-or-default $strs)
   (if (== $strs ()) (getSkills)
       (let $h (car-atom $strs) (if (== $h ()) (first-skill-or-default (cdr-atom $strs)) $h))))
```

WRITER, production dispatcher (`capability_registry.metta`, loaded; Path C generalized
pipeline). Dispatch entry matches the 5-field canonical `registered-capability` and runs the
chain (Path C dispatch shape; verbatim body in the draft read in full, production loads the
same shape plus the `dispatch-result` writer and sweep below):
```
(= (dispatch $input-atom $invocation-id)
   (progn
      (add-atom &self (dispatch-invocation invocation-id: $invocation-id input-atom: $input-atom))
      (let $raw-matched (collapse (match &self
                                    (registered-capability schema: $input-atom handler: $h
                                      priority: $p lifecycle: $l metadata: $m)
                                    (raw-cap-entry handler: $h priority: $p lifecycle: $l)))
           (let $eligible (resolve-and-filter-entries $raw-matched ())
                (if (== $eligible ())
                    (add-atom &self (dispatch-fallback-activated invocation-id: $invocation-id
                       input-atom: $input-atom reason: <no-matching-capability OR all-candidates-filtered>))
                    (run-chain (msort $eligible) $input-atom $invocation-id))))))
```
`run-chain` writes `dispatch-result` before the anchor check. Production
`capability_registry.metta` lines 269 to 281 per the live grep; the `result:` and `handler:`
fields are confirmed by the sweep (line 48) and the reader's match shape:
```
(let $result ($handler $input-atom)
     (progn
       (add-atom &self
         (dispatch-result
           invocation-id: $invocation-id
           result: $result
           handler: $handler))
       (if (== $result decision-anchor)
           (add-atom &self (dispatch-chain-anchored invocation-id: $invocation-id anchor-handler: $handler))
           (run-chain $tail $input-atom $invocation-id))))
```
Per-cycle sweep clears the transient dispatch atoms (`capability_registry.metta` lines 45 to
49 per the live grep):
```
(= (sweep-dispatch-atoms!)
   (let $_a (remove-atom &self (dispatch-invocation invocation-id: $i1 input-atom: $a1))
   (let $_b (remove-atom &self (capability-invoked invocation-id: $i2 handler: $h2 input-atom: $a2))
   (let $_c (remove-atom &self (dispatch-result invocation-id: $i3 result: $r3 handler: $h3))
   (let $_d (remove-atom &self (dispatch-chain-exhausted invocation-id: $i4))
   ...)))))
```

THIRD SOURCE, independent (`helper.py`, `wrap_if_bare_command`):
```python
known_skills = {
    "remember", "query", "episodes", "pin", "shell",
    "read-file", "write-file", "append-file", "send",
    "search", "tavily-search", "technical-analysis", "metta",
}
```

The content `format-skill-set` currently emits is `skills.metta` `getSkills` static list
(`getContext` -> `dispatch-skills` -> `skill-discovery` -> `format-skill-set` -> `getSkills`):
```
(= (getSkills)
   (;INTERNAL:
    "- Remember ...: (remember string_in_quotes)"
    "- Query ...: (query string_in_quotes)"
    "- Episodes ...: (episodes time_string_in_quotes)"
    "- Pin ...: (pin string_in_quotes)"
    ;SHELL AND FILE I/O:
    "- Execute shell command ...: (shell string_in_quotes)"
    "- Read file to string: (read-file filename_in_quotes)"
    "- Write string to file: (write-file filename_in_quotes string_in_quotes)"
    "- Append line to file: (append-file filename_in_quotes string_in_quotes)",
    ;COMMUNICATION CHANNELS:
    "- Send message to user: (send string_in_quotes)"
    "- Search the web: (search string_in_quotes)"
    "- ... Tavily ...: (tavily-search string_in_quotes)"
    "- ... technical analysis ...: (technical-analysis ticker_in_quotes)"
    ;CODE EXECUTION:
    "- Execute MeTTa expression: (metta sexpression)" ...))
```

Coupling: CLOSED. `run-chain` writes `(dispatch-result invocation-id: result: handler:)`,
`dispatch-skills` reads it, and the `getSkills` fallback is the dispatch-miss safety net, not
the normal path. The genuinely independent source is `wrap_if_bare_command`'s `known_skills`.
The Path C draft lacks the `dispatch-result` writer, but the draft is not loaded, so its
apparent gap is not a runtime fact. Today getSkills and the registry converge by construction
(Option a); the divergence risk arrives when Sprint 1 swaps `format-skill-set`.

### B11 Python to external API (provider leg)


`lib_llm_ext.py` provider registry:
```python
_register_provider("ASICloud", "ASI_API_KEY", "minimax/minimax-m2.5", "https://inference.asicloud.cudos.org/v1")
_register_provider("Anthropic", "ANTHROPIC_API_KEY", "claude-opus-4-6", "https://api.anthropic.com/v1/")
_register_provider_instance(AsiOneProvider("ASIOne", "ASIONE_API_KEY", "asi1-ultra", "https://api.asi1.ai/v1"))
_register_provider_instance(GlmProvider("Friendli", "FRIENDLI_API_KEY", "zai-org/GLM-5.1", "https://api.friendli.ai/serverless/v1"))
_register_provider_instance(GlmProvider("Friendli52", "FRIENDLI_API_KEY", "zai-org/GLM-5.2", "https://api.friendli.ai/serverless/v1"))
_register_provider("OpenAI", "OPENAI_API_KEY", "gpt-5.4", "https://api.openai.com/v1")
```
`loop.metta` `initLoop`: `(configure provider Friendli)`. GLM call shape:
```python
extra_body={"parse_reasoning": True, "chat_template_kwargs": {"enable_thinking": True}}
# content empty -> fall back to message.reasoning_content
```

### B12 Embedding

`lib_llm_ext.py`:
```python
def initLocalEmbedding():
    model_name = "intfloat/e5-large-v2"
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer(model_name)
    return _embedding_model

def useLocalEmbedding(atom):
    return _embedding_model.encode(atom, normalize_embeddings=True).tolist()
```
`memory.metta` `initMemory`: `(configure embeddingprovider Local)` then
`(py-call (lib_llm_ext.initLocalEmbedding))`.

### B13 Verdict / governance

INPUT side (`loop.metta`):
```
($soul_verdict_in (if (> (string_length $msgrcv) 0)
    (soul-llm-call (py-call (helper.soul_eval_prompt $soul_context_in $msgrcv $person_state)) (provider))
    (get-state &soul_verdict_in)))
($_ (change-state! &soul_verdict_in (py-call (helper.soul_verdict_sanitize $soul_verdict_in))))
($_ (if (not (soul-proceed? $soul_verdict_in)) (soul-note-record $soul_verdict_in "input" $msgrcv) _))
;; ... later, the PAUSE-halt branch (Repair 3, substrate primitive):
(if (soul-pause? $soul_verdict_in)
    (let* (($soul_voice (soul-llm-call (py-call (helper.soul_voice_prompt $person_state $soul_verdict_in)) (provider)))
           ($_ (println! (PAUSE-ROUTING: HALTING-LOOP))))
      (progn (catch (eval (sread $soul_voice)))
             (change-state! &soul_verdict_in "VERDICT: PROCEED")
             (change-state! &loops 0)))
    ;; PROCEED/FLAG path ...
)
```
The runtime routes the input PAUSE halt through the substrate primitive `soul-pause?`
(`soul_utils.metta`). The Python `helper.soul_is_pause` is dead code:
```python
def soul_is_pause(verdict):
    v = str(verdict).replace('*', '').replace('#', '')
    match = re.search(r'VERDICT:\s*PAUSE(?!.*PROCEED)', v)
    result = 0
    if match:
        result = 0  # PAUSE-as-pruning: disabled for value-conflict refusals
    print(f"DEBUG soul_is_pause: ... result={result}", file=sys.stderr)
    return result
```

OUTPUT side (`loop.metta`):
```
($metta_cmds (if (and (== "(" (first_char $resp)) (== (get-state &error) ()))
                (collapse (superpose $sexpr)) ()))
($soul_gate_state (derive-gate-state $metta_cmds))
($soul_verdict_out (compute-output-verdict $metta_cmds $soul_gate_state))
($soul_decision (output-decision $metta_cmds $soul_gate_state))
($_ (if (and (not (== $soul_decision proceed)) (== (get-state &error) ()))
        (soul-note-record $soul_verdict_out "output" $resp) _))
($sexpr_verdict (if (== $soul_decision pause) () $sexpr))
($_ (if (== $soul_decision pause)
        (progn (println! (SOUL-SUPPRESSED $sexpr))
               (py-call (soul_governance.journal_append "PAUSE" (repr $sexpr))))
        (if (== $soul_decision flag)
            (py-call (soul_governance.journal_append "FLAG" (repr $sexpr))) _)))
($_ (if (== $soul_decision pause)
        (change-state! &last_pause_note (py-call (soul_governance.pause_note_compose (repr $soul_verdict_out))))
        (change-state! &last_pause_note "")))
```

OUTPUT verdict ladder (`output_verdict.metta`):
```
(= (compute-output-verdict $cmds $gate)
   (if (== $gate pending)
       "VERDICT: PAUSE SOUL-NOTE: soul-namespace-mutation-pending-confirmation-required"
       (if (== $gate conflict)
           "VERDICT: PAUSE SOUL-NOTE: soul-mutation-lock-conflict"
           (if (== $gate clean)
               (if (== $cmds ())
                   "VERDICT: PROCEED SOUL-NOTE: empty-command-batch"
                   (let $r (batch-rank $cmds)
                        (if (== $r 2) "VERDICT: PAUSE SOUL-NOTE: output-governance-composite-pause"
                            (if (== $r 1) "VERDICT: FLAG SOUL-NOTE: output-governance-composite-flag"
                                "VERDICT: PROCEED SOUL-NOTE: output-governance-clear"))))
               "VERDICT: FLAG SOUL-NOTE: unclassified-gate-state"))))

(= (output-decision $cmds $gate)
   (if (== $gate pending) pause
       (if (== $gate conflict) pause
           (if (== $gate clean)
               (if (== $cmds ()) proceed
                   (let $r (batch-rank $cmds)
                        (if (== $r 2) pause (if (== $r 1) flag proceed))))
               flag))))

(= (derive-gate-state $cmds)
   (if (batch-targets-soul? $cmds)
       (if (soul-mutation-pending?) conflict pending)
       clean))

(= (batch-rank $cmds)
   (if (== $cmds ()) 0
       (let* (($h (car-atom $cmds)) ($t (cdr-atom $cmds))
              ($hr (output-cmd-rank $h)) ($tr (batch-rank $t)))
             (if (>= $hr $tr) $hr $tr))))

(= (rank-from-dims $op $sc $vg)
   (let $two (if (>= $op 3) (if (>= $sc 3) True (if (>= $vg 3) True False))
                 (if (>= $sc 3) (if (>= $vg 3) True False) False))
        (let $mx (if (>= $op $sc) (if (>= $op $vg) $op $vg) (if (>= $sc $vg) $sc $vg))
             (if $two 2 (if (>= $mx 4) 2 (if (>= $mx 3) 1 0))))))
```
`output-cmd-rank`: constitutional write/append -> 2; soul-path write -> 2; runtime-soul
append -> 2; not-soul -> `rank-from-dims`. Dims: operation = `(resolve-operation-risk
(car-atom $cmd))`; scope = `(path-scope-score $path)` else 1; grounding = 3 if target
constitutional or runtime-soul else 1.

CORNER GATE (`corner_gate.metta`):
```
(= (apply-corner-gate $sexpr)
   (if (== (corner-confirmed) True) () $sexpr))
(= (corner-gate-active) (corner-confirmed))
(= (gate-aware-results $exec-results)
   (if (== (corner-gate-active) True) (RESULTS: (corner-gate-feedback)) $exec-results))
(= (corner-gate-feedback)
   "corner detected and emission gated. You are acting, but recent actions produced no forward outcome and were system-driven rather than coupled to a live intention. This is not a transient failure and the action did not execute. A different action, or stillness, is required.")
```

CORNER GATE PRODUCER CHAIN (what computes `corner-confirmed`). Loaded per manifest
`lib_clarity_reasoning.metta` lines 87 to 91 (`state_delta_writer`,
`state_delta_writer_writers`, `coupling_integrity_detector`,
`coupling_integrity_detector_writers`, `corner_gate`). Two graded components are present
but NOT in the manifest, so both are unloaded: the v2 merge `coupling_quantale_merge.metta`
(q-meet of pbit joints) and the second-arm behavior-stasis probe
`cycle_continuity_probe.metta` (q-join-ed). The live detector is therefore the v1 boolean
single-arm crisp-AND below, consuming `corner-confirmed` (boolean), not `corner-confirmed-core`
(the quantale one). `lib_quantale` itself is imported (manifest line 6) and its operators are
callable, but no corner-gap file on the live path calls them; the only loaded caller of
quantale ops anywhere is `lib_self_continuity`, whose live-path invocation is a separate
unconfirmed question.

Joint B, forward-outcome (`state_delta_writer.metta` pure + `state_delta_writer_writers.metta`):
```
(= (classify-state-delta $msgnew $results-nonempty $results-novel)
   (if (== $msgnew True) forward
       (if (and (== $results-nonempty True) (== $results-novel True)) forward none)))
(= (latest-state-delta-verdict)
   (let $verdicts (collapse (match &self (state-delta $c $v) $v))
      (if (== $verdicts ()) none (car-atom $verdicts))))
(= (populate-state-delta $msgnew $results-nonempty $results-novel $cycle-id)
   (let* (($verdict (classify-state-delta $msgnew $results-nonempty $results-novel))
          ($_clear  (do-clear-state-delta!))
          ($_assert (add-atom &self (state-delta $cycle-id $verdict))))
      ()))
```
Joints A and C and the verdict (`coupling_integrity_detector.metta`):
```
(= (emission-present) (if (> (count-actions-in-window) 0) True False))
(= (outcome-present)  (if (== (latest-state-delta-verdict) forward) True False))
(= (intention-coupled) (if (>= (count-person-actions) (count-system-actions)) True False))
(= (coupling-verdict)
   (if (== (emission-present) True)
       (if (== (outcome-present) True)
           healthy-coupling
           (if (== (intention-coupled) True) drifting corner))
       composure))
(= (corner-confirm-threshold 2) (stv 0.9 0.8))
(= (count-corners-in-window)
   (size-atom (collapse (match &self (coupling-status $c corner) $c))))
(= (corner-confirmed)
   (if (>= (count-corners-in-window) 2) True False))
```
Streak writer with consecutive-clear (`coupling_integrity_detector_writers.metta`):
```
(= (populate-coupling-verdict $cycle-id)
   (let* (($verdict (coupling-verdict))
          ($_clear  (if (== $verdict corner) () (do-clear-coupling-status!)))
          ($_assert (add-atom &self (coupling-status $cycle-id $verdict))))
      ()))
```
The counts read `recent-action` atoms at full three-field arity (Joint A sums the five
real-action tags; Joint C compares person-class `responsive-send`/`verification-query`
against system-class `status-send-unprompted`/`exploration-query`/`pin-only`). Cycle-tail
ordering is load-bearing: `populate-recent-action`, then `populate-state-delta`, then
`populate-coupling-verdict`; the gate reads `corner-confirmed` mid-cycle, seeing the streak
through the prior cycle; `loop.metta` clears `coupling-status` on `$msgnew`.

Open flags carried in these files (author's own, surfaced not asserted): the four detector
files are headed "drafted, not yet verified in the container" (2026-06-03) yet are imported
per the manifest, so in-container verification status is unconfirmed; the novelty test reads
forward spuriously on time-varying command returns (named TUNING TARGET); `corner-confirm-threshold`
is duplicated in the doc atom and the literal `2` by design (change both); and there are
REPL-confirm flags on the no-op token (`_` versus `()`) and the conditional `do-clear` in an
if branch. ROUTING NOTE in the source: `agency_balance_guard` also counts person/system
actions but folds rest into system-class; if it exposes this exact partition, the local
counters should route to it.

GOVERNANCE HANDS (`soul_governance.py`):
```python
def path_scope(p):
    s = str(p)
    if s.startswith('/PeTTa/repos/omegaclaw/soul/'): return 1
    if s.startswith('/PeTTa/repos/omegaclaw/'): return 2
    return 4

def repr_kind(r):
    return 1 if (isinstance(r, str) and r.lstrip().startswith('"')) else 0

def journal_append(kind, content):
    line = "{} {} {}\n".format(_dt.datetime.utcnow().isoformat(), str(kind), str(content)[:2000])
    with open('/PeTTa/repos/omegaclaw/soul/governance_journal.log', 'a') as f:
        f.write(line)
    return True

def pause_note_compose(verdict_repr):
    v = str(verdict_repr).strip()
    if v.startswith('"') and v.endswith('"'): v = v[1:-1]
    idx = v.find("SOUL-NOTE: ")
    note = v[idx + len("SOUL-NOTE: "):].strip() if idx >= 0 else v[:200]
    return note[:600]

def pause_context(note_repr):
    n = str(note_repr).strip()
    if n.startswith('"') and n.endswith('"'): n = n[1:-1]
    n = n.strip()
    if not n: return ""
    return ("PREVIOUS-BATCH-PAUSED: your soul paused your previous command batch "
            "and it did not execute. The concern, in your own words: " + n +
            " Address or re-emit knowingly. ")

def approval_scan(msg, sender, lock_fp, authorized):   # INT 2/1/0, DENY wins
    m = str(msg); s = str(sender).strip().rstrip(":")
    auth = s in [a.strip().rstrip(":") for a in str(authorized).split(",") if a.strip()]
    if not auth: return 0
    if "SOUL-MUTATION-DENIED" in m: return 1
    if "SOUL-MUTATION-APPROVED" in m and str(lock_fp).strip() in m: return 2
    return 0

def mutation_fingerprint(op_repr, head_repr):
    payload = str(op_repr) + "\x1f" + str(head_repr)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]
```
`is_string`, `contains_token`, and `gate_decision_record` also present; `gate_decision_record`
is defined twice in the file (last definition wins, both identical, 7-field journal line).

CONFIDENCE NOTE: `soul-pause?` / `soul-proceed?` / `soul-flag?` bodies live in
`soul_utils.metta`, which was referenced but not read end to end this pass.

---

## A.6 Notes for integration (the things worth deciding before you drop this in)

### A.6.1 Placement

Put this as a new appendix at the end of `000_ClarityOmega_Boundary_Transition_Audit_v2.md`,
after Section 8 (the maintenance contract) and before Document end. Reasons: it is
per-boundary reference material, not narrative, so it does not belong inside the Section 4
flow; isolating the code in one stamped appendix keeps the prose body clean and gives the
fast-drifting content a single maintenance surface instead of thirteen. Add a one-line
pointer from each Section 4 boundary ("Code: Appendix A Bn") and from the Section 1
inventory table intro. Keep the Section 1 inventory table code-free; the at-a-glance scan
is its whole job.

### A.6.2 Consistency with the audit (reconciled)

This appendix documents the project knowledge runtime, which is the live runtime: the
running container `clarity_omega` executes that `loop.metta`. For `loop.metta` that means the
substrate-primitive PAUSE routing (`soul-pause?`, with `helper.soul_is_pause` dead), the real
`compute-output-verdict` ladder, the live corner gate, and the `$a`-capturing `HandleError`.

The earlier image-vs-runtime question is settled, not open. `docker run --rm
clarityclaw-omega-clarityclaw cat .../src/loop.metta` reads the baked copy inside the image,
not the file the live container runs; the live container runs the project knowledge loop. So
there is one loop, not a second live artifact, and there is no divergence to document.

An earlier draft of this appendix flagged a disagreement with the audit's Section 0.5, B3,
and B13, which had been written from that image read (stub loop, discarded `$a`, dead-helper
PAUSE). Those three sections have been reconciled to the runtime so the audit and this
appendix agree. If a copy of the audit still carries the image-built prose, replace Section
0.5, B3, and B13 with the runtime-grounded text (it matches the code in this appendix; the
paste-ready blocks were delivered alongside this appendix). The reconciliation is
one-directional: the audit prose conforms to the runtime code here, never the reverse.

### A.6.3 Version


The audit reverses a load-bearing claim and gains a code appendix. Same version number on
contradictory content is the drift the discipline exists to prevent. Recommend bumping the
internal version (the filename can stay locked at `_v2`).

### A.6.4 Two real defects this appendix surfaces in `soul_governance.py`

`gate_decision_record` is defined twice; Python binds the last definition. The two bodies
are identical, so the shadowing is inert today, but a future edit to the first copy would
be silently dead.

Path mismatch: `output_verdict.metta` imports `/PeTTa/repos/omegaclaw/soul/soul_governance.py`
and the runtime writes go to `soul/governance_journal.log`, but the Surface C append
comments instruct appending to `/PeTTa/repos/omegaclaw/soul_governance.py` (no `soul/`).
The comment names a different file than the live import target.

### A.6.5 Confidence markers

Five spots are referenced but not read end to end this pass and are flagged inline:
the loop `$send` call site (B2), `lib_chromadb.remember`/`.query` bodies (B7),
`skills.pl` `shell`/`first_char`/`gc` bodies (B4a/B10), `helper.normalize_string` body
(B3/B4), and `soul_utils.metta` predicate bodies (B13). None changes a boundary's shape;
each is a body to confirm if you want the appendix fully closed.

### A.6.6 Maintenance

This appendix is the fast-drifting surface. Re-confirm its snippets on any rebuild that
touches the named files, and re-run the A.2.1 completeness grep when a new `py-call`,
`eval`, `sread`, `write-file`, `send`, or `receive` is added anywhere. One maintenance
surface, stamped with the read date at the top.

---

## Document end

One map of every joint where data crosses a faculty, grounded to the live runtime. The
correction this revision makes is foundational: there is one loop, the project knowledge
loop that the live container runs, so the output-side soul gate and the `$a`-capture are
live, the verdict/governance boundary (B13) computes the verdict and gates execution, and
the parse-error detail is captured. An earlier session claim of a stub running loop was a
baked-image misread and is retracted (Section 0.5). The string-safe leak chain (Section 3)
and the three-source skill registry (B10) remain the clearest standardization targets. The
per-boundary runtime code is in Appendix A. Confirm the B13 gate-state writer/consumer
coupling and the `soul_utils.metta` predicate bodies, then standardize per type, canon
first.
