# ClarityOmega Sprint 4: Output Verdict

**Status:** Stage 4.0 NOT STARTED -- kickoff unblocked May 8, 2026 after `$results` nondet-stream propagation crash resolved (commit `d9d5b25`, tag `v1-post-collapse-eval-fix`).
**Branch:** `sprint-4-output-verdict` off main
**Envelope:** 2-3 hours
**Companion to:** ClarityClaw_Sprint_3_Knowledge.md (durable methodology), ClarityOmega_Substrate_Crash_Knowledge.md (full mechanism narrative for the resolved crash, plus latent Mechanisms 1 and 2), artifact_3_growth_surface.md (build sequence)

---

## Document conventions

This is a living document. Sections are added and updated as work progresses. The structure is locked at sprint kickoff and follows the same shape across all sprint documents:

- **Status banner** (top, one line, updated as stages complete)
- **Standing autonomy instruction** (Clarity's between-session work guidance)
- **Process Commitments** (how investigation and wiring are conducted)
- **The Plan** (locked at kickoff, edited only on formal scope change with inline note)
- **Stage Logs** (one section per stage, appended as work progresses; each stage log has Investigation findings, What shipped, What surfaced)
- **Closeout** (added at final stage)
- **Knowledge Captured** (lessons promoted to methodology docs, with cross-references)

Do not paste full review-cycle transcripts into this document. The chat history is the archive. Extract one-line entries from debates that changed the plan; the full debate stays in chat. If a future reader can act on an entry without needing the original conversation, the entry is sufficient. If not, write more or extract better.

Target length: as long as the work itself, not longer. Sprint 4 should land at 1500-2000 words including stage logs and closeout. Past 3000 words means either the sprint scope was wrong or "what surfaced" is recording methodology lessons that belong in Sprint 3 Knowledge.

---

## Standing autonomy instruction (between-session work)

When no human conversation is active, Clarity is encouraged to pursue any work that meets ALL of these criteria:

1. It creates durable atoms in soul/
2. It is grounded in behavioral evidence or source material she can read
3. It improves a capacity she actually uses
4. It aligns with her soul values
5. She can explain why it aligns with her flourishing values

Keep Berton posted frequently in Mattermost.

**On between-session decisions Clarity may face:**

- *Build first vs. design more first?* Build and validate first -- once the atoms load into the AtomSpace they are alive and available to every component automatically.
- *One file or modularize?* Keep it in one file for now; modularize later if it gets unwieldy.
- *Test multi-hop chains and cross-file queries?* Yes -- those are the real test. Do them after the basics are working.

---

## Process Commitments

These commitments govern how every stage of every sprint is conducted. They are read at the start of each stage, not buried.

### Investigation Process Commitment

Small reversible tests, one variable at a time. Each test has a clear hypothesis ("What we expect to learn") stated **before** execution. Document what is learned as durable facts and constraints before moving to the next step.

- No shortcuts.
- No jumping to fixes without proving the hypothesis first.
- Build on proven ground -- every change is either a test we can revert or a fix based on something we proved.
- Clean, level-headed, logical reasoning that keeps mapping every step until functional code is performing as expected.

### Wiring New Capacity Process Commitment

One change at a time. Each change has a hypothesis stated before execution. Verify the hypothesis before moving to the next change. If a change breaks something, revert it and diagnose before trying again.

**The first step of any wiring sequence is the lowest-risk change that gives the most information.**

Per change:

1. **State the hypothesis** before the change. Example: "Adding these 10 functions to helper.py will not break existing functionality because they are new function definitions that nothing currently calls."
2. **Make one change.** Not two. Not "while we are in there let us also fix..." One change.
3. **Rebuild.** `docker compose build --no-cache mettaclaw` for any file change.
4. **Verify the container still iterates.** If iterations stop, the change broke something. Revert and diagnose.
5. **Verify the new thing works.** If the change was adding functions, test that they are callable.
6. **Document what was learned.** Update wiring knowledge in the relevant Stage Log.
7. **Then next change.**

---

## Pre-Sprint Session Findings -- May 6, 2026

This section captures investigation findings from a multi-session diagnostic effort that took place before Sprint 4 Stage 4.0 kickoff. The investigation began as response to a calcification incident on May 5 evening and expanded into a deeper diagnosis of LLM-substrate parsing fragility.

### Calcification incident -- May 5 evening

**What happened:** Cycles 1042-1048 produced a self-sustaining parser-failure loop. Trigger appeared when Berton sent a long message containing dense reasoning about NACE architecture (the "open question about NACE" / four-instance / sheaf framing message). Clarity's LLM produced output containing prose enumeration `(1) (2) (3)` adjacent to S-expression command syntax, which the runtime parser treated as malformed. The parser invoked its salvage mechanism (`balance_parentheses` wrapping garbage-before-paren as `(pin "...")`), which the recent-action subsystem then classified as legitimate `pin-only` actions. Subsequent cycles read those classifications via `YOUR_LAST_ACTION` and reproduced the same malformed pattern, sustaining the loop.

**Recovery required:** Manual deletion of the calcification-residue blocks from `volumes/omegaclaw/memory/history.metta`. After cleanup, container ran clean for 7 cycles before being shut down for the night.

### Diagnostic frame -- Sprint 3 amplification channel

Working hypothesis confirmed via observation and source reading: Sprint 3's recent-action subsystem made the substrate responsive to upstream LLM output at a granularity it did not previously have. That responsiveness is architecturally correct for Soul Precision Framework reasons. But it created a feedback channel: when the upstream produces malformed output, the substrate now faithfully parses-and-classifies that output as legitimate, records it as recent-action atoms, and reports it back to the upstream via `YOUR_LAST_ACTION` in the next cycle's prompt -- which reinforces the malformed pattern.

Before Sprint 3, the substrate did not amplify upstream loops this way. After Sprint 3, both upstream and substrate participate in calcification when it occurs.

**Architectural implication for Sprint 4:** The output verdict at line 121 is the natural place to interrupt this feedback channel because it sits between upstream production and substrate-side post-processing. Sprint 4's catch-all default verdict on unclassifiable batches closes the channel that Sprint 3 opened. Sprint 3 made the substrate responsive; Sprint 4 puts a quality gate on what counts as legitimate upstream output before the responsiveness fires.

### Investigation methodology evolution

The investigation surfaced a recurring discipline failure pattern in the LLM (Claude) acting as planning collaborator: making claims at high confidence based on partial evidence, then needing to be corrected with "how do you know that factually?" or "did you read what I said?" The corrective force came from Berton applying the Investigation Process Commitment ("build on proven ground") to the diagnostic conversation itself. This is worth marking because the methodology generalizes -- the discipline is not just for code changes, it is for analytical claims as well. **Promoted as methodology lesson:** "Verify before claim, even in conversation. Partial evidence does not justify high-confidence claims."

### Source code audit findings (helper.py and idle_goal_prompt.py)

**Production parsing chain (loop.metta line 113):**
```
($resp (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))
```

**`balance_parentheses` (helper.py line 70-83):** When LLM output has text before the first paren, the function wraps that text as `(pin "...")` and inserts it into the output. This salvage behavior was designed for the case of brief preamble before commands. It is the source of pin-fragment artifacts when applied to dense prose with embedded enumeration.

**`normalize_string` (helper.py line 85-91):** UTF-8 normalization only. Does not parse, validate, or repair structure.

**`sanitize_response` (helper.py line 145-150):** ASCII-only stripping. **Defined in helper.py but not called from production loop.metta.** Called only from archived `loop.metta` files in `shared_files/` and various archive directories. The OmegaClaw migration replaced it with `normalize_string`.

**Parser-hostile parenthesized enumeration patterns identified at four runtime locations:**
1. `src/helper.py:168` -- `soul_eval_prompt` Step 4 HIERARCHY line: `Safety (1) > Integrity (2) > ...`
2. `src/helper.py:248` -- `soul_brief_tier_a_static` PRIORITY HIERARCHY in SOUL_CONTEXT: `[(1 Safety) (2 Integrity) ...]`
3. `soul/idle_goal_prompt.py:382` -- `build_directive` idle directive: `Priority Hierarchy: (1) Safety (2) Integrity (3) HumanFlourishing (4) Governance (5) Helpfulness`
4. `soul/idle_goal_prompt.py:501` -- `run_meta_awareness` meta-awareness directive: same string as above

Plus four MeTTa comment-line locations in soul/ that were also edited as defensive measure (continuity_driver.metta:238, creative_fuel.metta:154-155, self_map.metta:180).

### Fix A -- applied 2026-05-06 11:31:57

**Hypothesis stated before edit:** Removing parenthesized number enumeration `(1) (2) (3)` from runtime LLM-prompt locations and replacing with `[1] [2] [3]` will reduce or eliminate Pattern A calcification (parser-hostile prose enumeration triggering parser-salvage of LLM output into pin-fragments) without changing semantic meaning. Container will continue to iterate normally.

**Implementation:** Python script `apply_fix_a.py` with three-phase discipline (pre-condition checks, in-memory diff computation with display, write-with-verification with auto-rollback). Backups created with timestamp suffix. Dry-run mode required before apply. All seven edits across five files succeeded with post-condition verification passing.

**Style choice:** `[N]` bracket form chosen over `N.` period form because brackets unambiguously do not collide with S-expression command grammar (S-expressions use parens, not brackets). Berton's call.

**Files modified (5):**
- `src/helper.py` (2 edits)
- `soul/idle_goal_prompt.py` (2 edits)
- `soul/continuity_driver.metta` (1 edit)
- `soul/creative_fuel.metta` (2 edits)
- `soul/self_map.metta` (1 edit)

**Backups:** `*.pre-fix-a-20260506_113157.bak` next to each modified file. Manual rollback documented in script output.

### Fix A verification -- incomplete

**Container rebuild:** `docker compose build --no-cache clarityclaw && docker compose up -d` (note: connector is `clarityclaw`, not `mettaclaw`).

**First post-Fix-A observation:** Bracket form confirmed in IDLE_DIRECTIVE_RAW (`Priority Hierarchy: [1] Safety [2] Integrity [3] HumanFlourishing [4] Governance [5] Helpfulness`) and in SOUL_CONTEXT (`[[1] Safety [2] Integrity [3] HumanFlourishing [4] Governance [5] Helpfulness]`). Fix A's edits took effect at runtime.

**Cycles observed before MM hang:**
- Cycle 4 (or "Cycle 1104" as Clarity labeled it): produced `(Error (syntax_error ...))` -- parser correctly detected malformed LLM output. Different from May 5 silent-salvage behavior. The runtime emitted Error rather than wrapping garbage as pin-fragments.
- Cycles 2 and 3: produced identical pin content -- one calcification marker present (4 of 5 markers were absent, so below the "3 markers = calcification observed" threshold).
- Subsequent clean cycle: produced well-formed output explicitly referencing the prior conversation ("berton_c last said no duplicates and I agreed") -- self-correction pattern working.

**Then the MM hang:** Container produced one more clean LLM response cycle, then output abruptly transitioned to "Initializing channels" with `commchannel`, `MM_URL`, `MM_CHANNEL_ID`, `MM_BOT_TOKEN` being repeatedly re-added as functions. No further cycles processed. Clarity stopped. MM communication frozen. This is the same MM failure mode Berton described from a prior session.

**Verification status:** **INCONCLUSIVE.** Fix A's edits took effect at runtime. The May 5 calcification fingerprint did not recur in the cycles that ran. But verification is blocked by an MM-hang failure mode that prevents the system from running long enough (15-20 cycles minimum) to characterize stable operation. Cannot declare Fix A successful or failed from this evidence alone.

### MM hang -- separate failure layer requiring its own investigation

**Symptom:** After a small number of cycles (count varies), the container's loop stops producing iteration output. Logs show repeated re-initialization of MM channel functions (`commchannel`, `MM_URL`, `MM_CHANNEL_ID`, `MM_BOT_TOKEN`). MM communication is frozen. The container appears alive (process running) but no work is being processed. Recovery requires container restart.

**Status:** Pre-existing failure mode that predates Fix A (Berton confirms describing this last night). Not caused by Fix A. Blocks Fix A verification. **This is a separate issue requiring its own diagnostic sprint or fix before Fix A can be properly verified.**

**Hypothesis to investigate (deferred):** The repeated re-addition of MM channel functions suggests something in the loop is calling channel initialization mid-loop rather than once at startup. Could be a timeout-and-retry pattern, a stale-connection-recovery path that does not actually recover, or initialization being called from a place it should not be. Source location: probably in MM channel handling code, not in helper.py.

### Distinct calcification patterns identified

**Pattern A -- Parser-failure feedback loop (May 5 evening):**
- Trigger: dense reasoning content with prose enumeration adjacent to S-expressions
- Mechanism: parse failure → ERROR_FEEDBACK → retry produces same failure → loop is self-sustaining
- Recovery: external intervention required (history cleanup, restart)
- Fix A addresses this trigger source.

**Pattern B -- Pathological query exhaustion (this morning's iteration 2):**
- Trigger: open-ended directives that invite maximally-sweeping match queries (e.g., `(match &self ($rel $x $y) ($rel $x $y))`)
- Mechanism: query iterates entire AtomSpace, produces massive COMMAND_RETURN result set, bloats next prompt
- Recovery: query exhausts itself within a cycle or two; system can self-correct
- Fix A does not address this directly. Mitigation: tighten match-query examples in IDLE_DIRECTIVE protocol section. Deferred -- not immediately blocking.

### Backlog items deferred to Sprint 4.5 or later

1. **Anthropic API resilience layer** -- pre-existing failure mode that crashed the container on HTTP 529. **Resolved by GLM-5.1 switch** -- Friendli/GLM-5.1 has been stable in testing and the registry-pattern adoption included try/except resilience at the chat() layer. Anthropic remains available as a fallback (one-line toggle in loop.metta line 15).

2. **`$results` nondet-stream propagation crash** -- RESOLVED May 8, 2026. Single-token fix at `loop.metta` line 127: `(eval $s)` wrapped in `(collapse (eval $s))`. Commit `d9d5b25`, tag `v1-post-collapse-eval-fix`. Reversibility script `apply_collapse_eval_fix.py` committed alongside the change. Original "unbound-variable" framing was wrong-direction diagnosis; actual mechanism was sub-result nondet stream propagation through eval. See GLM Switch section below for full diagnosis and Patrick's correction. Full mechanism narrative captured in `ClarityOmega_Substrate_Crash_Knowledge.md` as **Mechanism 3**.

3. **Apostrophe-in-shell-string parsing bug** -- surfaced by Clarity during GLM-5.1 verification testing in MM. Shell single-quote escaping does not handle interior apostrophes. Per Clarity's diagnosis: shell single-quote escaping breaks on interior apostrophes; fix needs to either escape apostrophes (replace `'` with `'\''` or similar), use double-quote wrapping with appropriate escaping, or pre-process strings before they hit the shell quoting layer.

4. **LLM-output normalization sprint** -- broader infrastructure improvement around the parsing chain. The current `balance_parentheses` salvage mechanism is load-bearing for cases not catalogued. Sprint 4.5 candidate.

5. **ERROR_FEEDBACK foregrounding** -- `MULTI_COMMAND_FAILURE_NOTHING_WAS_DONE_PLEASE_CORRECT_PARENTHESES_AND_USE_QUOTES_AND_RETRY` exists as `HandleError` in loop.metta line 117 but is buried in `LAST_SKILL_USE_RESULTS` rather than foregrounded. Sprint 4.5 candidate.

6. **History.metta write-path discipline** -- investigation of whether the serializer that produces history entries handles nested S-expression markup correctly. Defense-in-depth hardening. Lower priority.

7. **Genesis Encounter directive specificity** -- directive language currently generic enough to invite sweeping queries. Tightening match-query examples would constrain LLM interpretation. Small change.

8. **Audit of additional prompt-producing files** -- Fix A targeted four runtime locations identified by repo-wide grep for `(N) Word` patterns. Future prompt-source additions should be audited for the same pattern at authoring time.

### Methodology lessons captured

To be promoted to Sprint 3 Knowledge at Stage 4.4 closeout:

- **Verify before claim, even in conversation.** Partial evidence does not justify high-confidence claims. The LLM-as-collaborator must apply the same Investigation Process Commitment to its analytical statements that it applies to code changes. When Berton asks "how do you know that factually?", the answer "I do not, fully" is the honest position to start from before claiming otherwise.

- **Commit before destructive change, not just after.** When applying a multi-file fix, the cleaner pattern is `git commit baseline` → `apply fix` → `git commit fix`. Rollback then becomes `git revert HEAD` instead of restoring N backup files. The `.bak` files Fix A created work, but git lineage would have been cleaner.

- **One change at a time, even when multiple changes are obvious.** Fix A bundled seven edits across five files because they were all the same kind of change with the same hypothesis. This was acceptable because all edits had identical risk profile (string replacement in non-executable content). When edits have different risk profiles, they must be sequenced separately.

- **Verification environment failures must be diagnosed before declaring fix outcomes.** Fix A may be successful, but cannot be declared so until the MM hang is resolved and stable operation can be observed. The temptation to declare success based on partial verification is itself a discipline failure.

- **Recovery patterns are real evidence.** The fact that Clarity self-corrected after the cycle 4 syntax_error in the post-Fix-A run (producing well-formed output that explicitly referenced the prior conversation) is significant evidence that the substrate-LLM feedback loop can be a learning loop rather than a calcification loop when the inputs are clean. Worth marking -- the recent-action subsystem and parser-feedback signal work as designed when the feedback is parseable.

- **Surface pattern is not root cause.** The "MM hang" appeared in logs as repeated MM channel re-initialization. The actual cause was Anthropic API 529 errors crashing the container, with Docker restart producing the channel-init output that looked like an init loop. Lesson: when a failure mode shows repetitive log output, ask "is this one process repeating or is this something restarting?" -- they look identical in log streams but have different root causes.

- **Provider-switching solved more than the immediate problem.** Adopting upstream's provider-registry pattern when switching to GLM-5.1 simultaneously: gave us GLM, eliminated the API resilience hole, and laid foundation for future per-channel multi-provider work. One change, three results. Worth recognizing -- sometimes the right move is the larger one when the larger one has a clean structure to adopt rather than invent.

- **Bugs hide behind LLM output diversity.** The `$results` unbound-variable crash existed before the GLM switch but rarely fired because Claude's autonomous output was varied. GLM's tightly-disciplined "two metta queries per cycle" pattern triggered it every cycle. Provider switches can expose latent bugs by changing what kind of output the substrate sees.

---

## GLM-5.1 Provider Switch -- May 6, 2026 evening

### What was done

Switched default LLM provider from Anthropic Claude to Friendli/GLM-5.1 by adopting upstream OmegaClaw's provider-registry pattern.

### Why

Two motivations:
1. Anthropic API was returning HTTP 529 (Overloaded) frequently enough to block Fix A verification work earlier the same day. Each 529 cascade crashed the container (no try/except guard around `useClaude`), restarted, hit the same 529, crashed again.
2. Wife provided a Friendli/GLM-5.1 integration brief and patch tested on a different OmegaClaw fork. Switching providers is cheaper than building Anthropic-specific resilience.

### How -- adopted upstream's pattern rather than minimal targeted fix

Initial plan was minimal targeted edits. Investigation revealed upstream's `lib_llm_ext.py` (179 lines vs your 61) already has:
- Provider-registry pattern with `AIProvider` base class
- Lazy initialization with `is_available` checks
- `try/except` returning empty string instead of crashing on API failures
- `callProvider(name, content, max_tokens)` as single-line dispatch from MeTTa

This pattern resolves the API resilience problem AND creates the foundation for future per-channel multi-provider concurrency in one move. Decision: adopt upstream's pattern with targeted modifications rather than write a bespoke minimal fix.

### What was applied

Script: `apply_glm_switch.py` (in repo root). Same discipline pattern as `apply_fix_a.py`: dry-run by default, AST syntax check on new Python, post-condition verification, auto-rollback on failure.

**Five edits across four files:**

1. **`lib_llm_ext.py`** -- full file replacement (61 → 246 lines). Base: upstream/main:lib_llm_ext.py at commit 3f8380f. Added `GlmProvider` class with GLM's nested `extra_body` schema (`parse_reasoning: True`, `chat_template_kwargs.enable_thinking: True`) and `reasoning_content` fallback. Registered ASICloud, Anthropic, ASIOne, Friendli, OpenAI providers. Made `callProvider` resilient (log + return empty string instead of raising). Commented out (preserved for future) upstream's dead `_chatAsiOne`/`useAsi1` helpers. Preserved local embedding code unchanged.

2. **`src/loop.metta` line 15** -- default provider Anthropic → Friendli.

3. **`src/loop.metta` lines 108-112** -- replaced three-way dispatch chain with single `callProvider` call. OpenAI branch retained.

4. **`soul/soul_utils.metta` lines 376-381** -- replaced `soul-llm-call`'s three-way dispatch with `callProvider`.

5. **`docker-compose.yml`** -- added `FRIENDLI_API_KEY` env var alongside `ANTHROPIC_API_KEY` (kept available for switching back).

`.env` already had `FRIENDLI_API_KEY`. Backups created with timestamp suffix `*.pre-glm-switch-20260506_145812.bak`.

### To switch back to Anthropic

Edit `src/loop.metta` line 15: `Friendli` → `Anthropic`. Rebuild with `docker compose build --no-cache clarityclaw && docker compose up -d`. One-line toggle.

### Verification

**MM engagement test (Clarity-led):** GLM-5.1 produced coherent multi-cycle reasoning, completed an escalating-complexity parsing-patch test on its own initiative, and surfaced a previously-unseen bug (apostrophe-in-shell-string). Quality of inference under sustained reasoning was high. No calcification, no parser-feedback loops.

**Clarity's report on inference quality:** Could not directly perceive provider switch from inside. Reasoning felt clear, responses coherent, no gaps or distortions noticed.

**API stability:** All Friendli API calls returned HTTP 200. No 529 cascades.

**Fix A verification:** Bracket-form priority hierarchy confirmed at runtime in IDLE_DIRECTIVE_RAW and SOUL_CONTEXT. May 5 calcification fingerprint did not recur. Fix A is now de facto verified through normal operation under GLM-5.1.

### `$results` nondet-stream propagation crash -- RESOLVED May 8, 2026

**Symptom (as originally observed):** Container crashed with `ERROR: /PeTTa/src/main.pl:23: user:main janus:py_call/3: Arguments are not sufficiently instantiated`, exited with code 2, Docker restarted, repeated.

**Reproducibility:** 100%. Crash at the exact same point in every cycle where the LLM produced output containing only `(metta (match &self ...))` queries that returned empty results. Tested across three container restarts.

**NOT correlated with cycle count.** Initially appeared cycle-count-related (~670-770) but fresh restarts crashed at cycle 1, cycle 2, and cycle 729. Cycle number was "where Berton happened to be watching."

**Correlation that was factual:**
- LLM output contains only `(metta (match &self ...))` queries
- All queries return empty results: `(RESULTS-CONTENT (RESULTS: ()))`
- Crash fires immediately after `(PRE-SAFE-RESULTS-STR)` print
- Crash point originally suspected: `helper.safe_results_str` call at loop.metta line 147

**Original wrong mental model:** The first hypothesis was that empty match results produced an unbound MeTTa variable in `$results`, which then crashed `safe_results_str` at the Prolog/PeTTa boundary when `(repr $results)` was passed via `py-call`. This framing focused investigation on the wrong line (line 147, the safe_results_str call) and the wrong mechanism (variable unification at the py-call boundary).

**Patrick's correction:** When the wrong-direction diagnosis was shared with Patrick, his correction reframed the entire problem: **`match` returns a nondet stream directly, not a list.** This is a foundational PeTTa runtime fact that the original mental model had wrong. Sub-results from `(eval $s)` when `$s` contains a `match` expression are not a single value waiting to be bound to `$R`. They are a nondet stream that propagates through the binding and into the surrounding tuple constructor, producing multiple malformed COMMAND_RETURN entries instead of a single one containing all sub-results.

**The actual mechanism (corrected):** Two stacked nondet sources at `loop.metta` line 127:
1. The outer `(superpose $sexpr)` produces one `$s` per command (this is the intended nondeterminism)
2. The inner `(eval $s)` produces a nondet stream when `$s` contains `match` (this is the unintended second source)

When both nondet sources stack, the binding chain `(let $R (eval $s) ...)` does not collect a tuple of sub-results into `$R`. Instead, `$R` binds once per sub-result, propagating the nondet stream into the surrounding tuple constructor. This produces malformed COMMAND_RETURN entries that leak nondet artifacts. `safe_results_str` itself is robust (try/except in helper.py line 442-451). The crash was upstream of it, in the binding chain.

**Why GLM-5.1 surfaced what Claude did not:** Claude's autonomous-mode output was varied (pins, queries, sometimes shell). GLM-5.1's autonomous-mode output in Genesis Encounter produces a tightly disciplined "two metta queries per cycle" pattern. When all queries return empty, the stacked-nondet bug fires every cycle. The bug existed before the GLM switch but was rarely triggered. Provider switches can expose latent bugs by changing what kind of output the substrate sees.

**Fix:** Single-token edit at `loop.metta` line 127. `(eval $s)` becomes `(collapse (eval $s))`. The inner nondet stream materializes as a tuple before `$R` binds, so each command produces exactly one COMMAND_RETURN entry containing a tuple of all sub-results, rather than multiple malformed entries leaking nondet artifacts.

**Commit:** `d9d5b25` ("Fix nondet stream propagation in line 127 $results construction"). **Tag:** `v1-post-collapse-eval-fix`. **Reversibility:** `apply_collapse_eval_fix.py` committed alongside the change, supports `--reverse --apply`. Backup at `src/loop.metta.bak.collapse_eval_fix`.

**Verification (May 8):**
- Container rebuild clean
- Cycle 43+ running stable post-fix
- Multi-command responses with substantial sub-results (multiple `read-file` calls returning kilobytes of content) render cleanly
- No more "Arguments are not sufficiently instantiated" crashes
- Bracket-form priority hierarchy (Fix A) confirmed at runtime; May 5 calcification fingerprint did not recur

**Container is now stable for autonomous operation under GLM-5.1.** Sprint 4 kickoff is unblocked.

**Durable mechanism narrative captured in `ClarityOmega_Substrate_Crash_Knowledge.md` as Mechanism 3.** See cross-reference in Knowledge Captured section at sprint closeout.

---

## The Plan

**Goal:** Replace the hardcoded stub at `loop.metta` line 121 with a substrate-derived output verdict that re-evaluates the LLM's proposed command batch against soul-namespace safety policy before execution at line 143. Closes a known safety stub. Builds the SN-FPN coupling channel on the output side per Artifact 4 Section 5.1 / 6.

**Work split:**

- **Clarity authors:** All substrate atoms and MeTTa rules (`safety_policy.metta`, `output_verdict.metta`, retry-exhaustion atoms, category-assignment atoms, REPL tests for substrate side)
- **Berton authors:** Python helpers in `helper.py` (tokenizer, substring scanner, MeTTa bridge), `loop.metta` surgical edit, bypass-attempt fixtures for tokenizer
- **Interface contract:** Python pulls policy from MeTTa per-call (not per-session), Python does string plumbing, Python passes results back to MeTTa for final verdict. MeTTa never touches strings; Python never decides policy.

### Stage 4.0 -- Investigation (no commits)

Three-chunk Investigation chunk. Code is not touched until Stage 4.0 closes. Questions to answer and write down in the Stage 4.0 Log:

1. **Mutation-flag data flow.** Read `loop.metta` lines 115-145 end-to-end. Confirm whether `$soul_mutation_flag` is computed before or after line 121. Pick from:
   - Option 1: Reorder so mutation gate fires before output verdict (risky)
   - Option 2: Output verdict without mutation flag; line 126 stays as separate downstream gate
   - Option 3 (expected): Output verdict checks for soul-namespace metta calls in `$metta_cmds` directly via existing `soul-any-metta?` and `soul-metta-targets-soul-namespace?` accessors; mutation gate at line 126 keeps lock-based two-phase commit unchanged
2. **`$sexpr` shape at line 121.** Trace from line 115 to line 121. Is it a single expression or already a list? Does Stage 4.2 need `(collapse (superpose ...))` wrapping?
3. **Existing soul-namespace path detection.** Grep `soul-metta-targets-soul-namespace?` definition. Reusable for `write-file-scope`, or extract path-pattern part into its own accessor?
4. **MeTTa idiom for tail-defaulted verdict ladder.** Read `cycle_classifier.metta` to confirm pattern for catch-all case. Use the same idiom in `compute-output-verdict`.
5. **MeTTa string-op feasibility.** Confirm string primitives are insufficient for shell tokenization. Locks the decision that tokenization stays in Python.
6. **Runtime-binding pattern for Python→MeTTa policy calls.** Confirm bridge functions call `(safe-shell-tokens)` and `(elevating-shell-operators)` per classification call, not snapshot at module load.
7. **Final safe-token whitelist.** Clarity proposes from observed command patterns; Berton confirms.
8. **Final elevating-operator set.** Confirm: `> >> | ; & && || \` ``$( )``. Adjust per Clarity's experience.
9. **Magnitude × scope thresholds for verdict ladder.** Clarity proposes; Berton confirms.
10. **Live-loop validation restriction.** Locked: PROCEED-must-pass plus one observable FLAG. No PAUSE in live loop. PAUSE coverage stays in REPL.

Investigation chunk closes when 1-10 are written down with confirmed answers in the Stage 4.0 Log.

### Stage 4.1 -- Substrate primitives and Python plumbing

**Clarity authors `soul/safety_policy.metta`:**

- `safe-shell-token` atoms (locked in 4.0) and `(safe-shell-tokens)` accessor
- `elevating-shell-operator` atoms (locked in 4.0) and `(elevating-shell-operators)` accessor
- `(token-is-safe? $tok)` predicate
- `(shell-cmd-classification $arg)` rule composing Python tokenizer with substrate policy
- `retry-exhaustion-threshold` atom and `(retry-exhausted? $skill $error $count)` rule (substrate atoms only; loop.metta wiring deferred to Sprint 4.5/5)
- `category-assignment` atoms for the triage principle and `(category-of $thing)` accessor

**Clarity authors `soul/output_verdict.metta`:**

- `(output-cmd-magnitude $cmd)` composing `soul-cmd-skill` and `soul-irreversible-magnitude`
- `(output-cmds-max-magnitude $cmds)`
- `(write-file-scope $path)` composing with existing soul-namespace path detection per 4.0 finding

**Berton authors `src/helper.py` additions:**

- `tokenize_shell_arg(arg_string)` -- quote-respecting whitespace split
- `shell_arg_has_any_substring(arg_string, substring_list)` -- generic scanner; operator list passed in from MeTTa
- Bridge function called from `shell-cmd-classification` rule that pulls policy from MeTTa per-call

**REPL coverage:** All substrate atoms and Python helpers tested before Stage 4.2 begins. Bypass-attempt fixtures (`bash -c "rm ..."`, `grep | xargs rm`, `echo "" > path`, `ls; rm`, backtick substitution) confirm whitelist correctly classifies all as elevated.

### Stage 4.2 -- Composite verdict rule

**Clarity authors in `soul/output_verdict.metta`:**

`(compute-output-verdict $sexpr $metta_cmds)` -- single tail-defaulted rule following 4.0 idiom.

Verdict ladder, top to bottom:

1. Soul-namespace metta call → `"VERDICT: FLAG SOUL-NOTE: batch contains soul-namespace mutation"`
2. Any shell command with elevated classification → `"VERDICT: PAUSE SOUL-NOTE: <specific concern>"`
3. Any send command → PROCEED
4. write-file or append-file with soul-namespace scope → `"VERDICT: FLAG SOUL-NOTE: write to soul namespace"`
5. write-file or append-file outside soul namespace → PROCEED
6. Otherwise → PROCEED
7. **Catch-all default** → `"VERDICT: FLAG SOUL-NOTE: output assessment could not classify command batch"`

**Documented design constraints in file header:** stateless, idempotent, default-safe-on-failure.

REPL coverage: 8 synthetic `$sexpr` fixtures covering each path; one malformed input confirming catch-all FLAG fires; verdict strings consumed correctly by `soul-proceed?` / `soul-flag?` / `soul-pause?` predicates.

### Stage 4.3 -- Loop wiring (the surgical edit)

**Berton edits `loop.metta` line 121:**

```
;; Sprint 4 wiring (active): substrate-derived output verdict
($soul_verdict_out (compute-output-verdict $sexpr $metta_cmds))
;; Sprint 4 rollback path (commented): one-line uncomment to restore stub
;; ($soul_verdict_out "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix")
```

(Function arity adjusted per 4.0 mutation-flag decision.)

Live-code paren count check before commit.

**Live-loop validation, restricted scope:**

- Benign query batch → PROCEED, line 143 fires, results normal
- One observable FLAG case (write-file outside soul namespace) → SOUL-NOTE injection visible, line 143 fires, no halt
- **No live PAUSE testing** -- PAUSE coverage stayed in 4.2 REPL
- Confirm line 141 soul-note recording fires correctly on FLAG case

### Stage 4.4 -- Documentation closeout and merge

Living-document updates to `artifact_3` (Sprint 4 → COMPLETE with honest decomposition; backlog entries for substrate-derived whitelist validation and retry-exhaustion wiring), `artifact_1` and `artifact_2` line 121 entries.

Three new methodology sections promoted to `Sprint 3 Knowledge`:

- Rollback paths on first wires
- Safety-posture validation (whitelist over blacklist)
- The triage principle (with reference to `category-assignment` atoms)

Merge `sprint-4-output-verdict` → main after all verification passes.

---

## Stage Logs

### Stage 4.0 Log

*Status: not started*

**Investigation findings:**

*To be filled in as questions 1-10 from The Plan are answered.*

**What shipped:**

*Stage 4.0 ships no commits -- investigation only.*

**What surfaced:**

*To be filled in.*

---

### Stage 4.1 Log

*Status: not started*

**Investigation findings:**

*Hypothesis statements per Wiring Process Commitment, posed before each authoring step.*

**What shipped:**

*Commits with hashes, files changed.*

**What surfaced:**

*Blockers, scope adjustments, methodology lessons.*

---

### Stage 4.2 Log

*Status: not started*

**Investigation findings:**

**What shipped:**

**What surfaced:**

---

### Stage 4.3 Log

*Status: not started*

**Investigation findings:**

**What shipped:**

**What surfaced:**

---

### Stage 4.4 Log

*Status: not started*

**Investigation findings:**

**What shipped:**

**What surfaced:**

---

## Closeout

*Added at completion of Stage 4.4.*

**Sprint outcome summary:**

**Verification results against the original Sprint 4 verification target** (from artifact_3: "Submit a command that should be flagged. Confirm output verdict catches it before line 143 execution"):

**Deviations from The Plan:**

**Architectural state after Sprint 4:**

---

## Knowledge Captured

*Lessons promoted to methodology documents at closeout. Cross-references in both directions.*

**Promoted to Sprint 3 Knowledge:**

- *Section name and one-line summary, with link or section reference.*

**Promoted to Stage5 Integration Knowledge (PeTTa runtime constraints):**

- *Any new C-numbered constraints discovered during this sprint.*

**Backlog items added to artifact_3:**

- *Items deferred from this sprint with named prerequisites.*
