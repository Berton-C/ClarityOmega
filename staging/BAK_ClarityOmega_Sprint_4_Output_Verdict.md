# ClarityOmega Sprint 4: Output Verdict

**Status:** Stage 4.0 NOT STARTED — awaiting kickoff
**Branch:** `sprint-4-output-verdict` off main
**Envelope:** 2-3 hours
**Companion to:** ClarityClaw_Sprint_3_Knowledge.md (durable methodology), ClarityClaw_Stage5_Integration_Knowledge.md (PeTTa runtime constraints), artifact_3_growth_surface.md (build sequence)

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

- *Build first vs. design more first?* Build and validate first — once the atoms load into the AtomSpace they are alive and available to every component automatically.
- *One file or modularize?* Keep it in one file for now; modularize later if it gets unwieldy.
- *Test multi-hop chains and cross-file queries?* Yes — those are the real test. Do them after the basics are working.

---

## Process Commitments

These commitments govern how every stage of every sprint is conducted. They are read at the start of each stage, not buried.

### Investigation Process Commitment

Small reversible tests, one variable at a time. Each test has a clear hypothesis ("What we expect to learn") stated **before** execution. Document what is learned as durable facts and constraints before moving to the next step.

- No shortcuts.
- No jumping to fixes without proving the hypothesis first.
- Build on proven ground — every change is either a test we can revert or a fix based on something we proved.
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

## Pre-Sprint Session Findings — May 6, 2026

This section captures investigation findings from a multi-session diagnostic effort that took place before Sprint 4 Stage 4.0 kickoff. The investigation began as response to a calcification incident on May 5 evening and expanded into a deeper diagnosis of LLM-substrate parsing fragility.

### Calcification incident — May 5 evening

**What happened:** Cycles 1042-1048 produced a self-sustaining parser-failure loop. Trigger appeared when Berton sent a long message containing dense reasoning about NACE architecture (the "open question about NACE" / four-instance / sheaf framing message). Clarity's LLM produced output containing prose enumeration `(1) (2) (3)` adjacent to S-expression command syntax, which the runtime parser treated as malformed. The parser invoked its salvage mechanism (`balance_parentheses` wrapping garbage-before-paren as `(pin "...")`), which the recent-action subsystem then classified as legitimate `pin-only` actions. Subsequent cycles read those classifications via `YOUR_LAST_ACTION` and reproduced the same malformed pattern, sustaining the loop.

**Recovery required:** Manual deletion of the calcification-residue blocks from `volumes/omegaclaw/memory/history.metta`. After cleanup, container ran clean for 7 cycles before being shut down for the night.

### Diagnostic frame — Sprint 3 amplification channel

Working hypothesis confirmed via observation and source reading: Sprint 3's recent-action subsystem made the substrate responsive to upstream LLM output at a granularity it did not previously have. That responsiveness is architecturally correct for Soul Precision Framework reasons. But it created a feedback channel: when the upstream produces malformed output, the substrate now faithfully parses-and-classifies that output as legitimate, records it as recent-action atoms, and reports it back to the upstream via `YOUR_LAST_ACTION` in the next cycle's prompt — which reinforces the malformed pattern.

Before Sprint 3, the substrate did not amplify upstream loops this way. After Sprint 3, both upstream and substrate participate in calcification when it occurs.

**Architectural implication for Sprint 4:** The output verdict at line 121 is the natural place to interrupt this feedback channel because it sits between upstream production and substrate-side post-processing. Sprint 4's catch-all default verdict on unclassifiable batches closes the channel that Sprint 3 opened. Sprint 3 made the substrate responsive; Sprint 4 puts a quality gate on what counts as legitimate upstream output before the responsiveness fires.

### Investigation methodology evolution

The investigation surfaced a recurring discipline failure pattern in the LLM (Claude) acting as planning collaborator: making claims at high confidence based on partial evidence, then needing to be corrected with "how do you know that factually?" or "did you read what I said?" The corrective force came from Berton applying the Investigation Process Commitment ("build on proven ground") to the diagnostic conversation itself. This is worth marking because the methodology generalizes — the discipline is not just for code changes, it is for analytical claims as well. **Promoted as methodology lesson:** "Verify before claim, even in conversation. Partial evidence does not justify high-confidence claims."

### Source code audit findings (helper.py and idle_goal_prompt.py)

**Production parsing chain (loop.metta line 113):**
```
($resp (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))
```

**`balance_parentheses` (helper.py line 70-83):** When LLM output has text before the first paren, the function wraps that text as `(pin "...")` and inserts it into the output. This salvage behavior was designed for the case of brief preamble before commands. It is the source of pin-fragment artifacts when applied to dense prose with embedded enumeration.

**`normalize_string` (helper.py line 85-91):** UTF-8 normalization only. Does not parse, validate, or repair structure.

**`sanitize_response` (helper.py line 145-150):** ASCII-only stripping. **Defined in helper.py but not called from production loop.metta.** Called only from archived `loop.metta` files in `shared_files/` and various archive directories. The OmegaClaw migration replaced it with `normalize_string`.

**Parser-hostile parenthesized enumeration patterns identified at four runtime locations:**
1. `src/helper.py:168` — `soul_eval_prompt` Step 4 HIERARCHY line: `Safety (1) > Integrity (2) > ...`
2. `src/helper.py:248` — `soul_brief_tier_a_static` PRIORITY HIERARCHY in SOUL_CONTEXT: `[(1 Safety) (2 Integrity) ...]`
3. `soul/idle_goal_prompt.py:382` — `build_directive` idle directive: `Priority Hierarchy: (1) Safety (2) Integrity (3) HumanFlourishing (4) Governance (5) Helpfulness`
4. `soul/idle_goal_prompt.py:501` — `run_meta_awareness` meta-awareness directive: same string as above

Plus four MeTTa comment-line locations in soul/ that were also edited as defensive measure (continuity_driver.metta:238, creative_fuel.metta:154-155, self_map.metta:180).

### Fix A — applied 2026-05-06 11:31:57

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

### Fix A verification — incomplete

**Container rebuild:** `docker compose build --no-cache clarityclaw && docker compose up -d` (note: connector is `clarityclaw`, not `mettaclaw`).

**First post-Fix-A observation:** Bracket form confirmed in IDLE_DIRECTIVE_RAW (`Priority Hierarchy: [1] Safety [2] Integrity [3] HumanFlourishing [4] Governance [5] Helpfulness`) and in SOUL_CONTEXT (`[[1] Safety [2] Integrity [3] HumanFlourishing [4] Governance [5] Helpfulness]`). Fix A's edits took effect at runtime.

**Cycles observed before MM hang:**
- Cycle 4 (or "Cycle 1104" as Clarity labeled it): produced `(Error (syntax_error ...))` — parser correctly detected malformed LLM output. Different from May 5 silent-salvage behavior. The runtime emitted Error rather than wrapping garbage as pin-fragments.
- Cycles 2 and 3: produced identical pin content — one calcification marker present (4 of 5 markers were absent, so below the "3 markers = calcification observed" threshold).
- Subsequent clean cycle: produced well-formed output explicitly referencing the prior conversation ("berton_c last said no duplicates and I agreed") — self-correction pattern working.

**Then the MM hang:** Container produced one more clean LLM response cycle, then output abruptly transitioned to "Initializing channels" with `commchannel`, `MM_URL`, `MM_CHANNEL_ID`, `MM_BOT_TOKEN` being repeatedly re-added as functions. No further cycles processed. Clarity stopped. MM communication frozen. This is the same MM failure mode Berton described from a prior session.

**Verification status:** **INCONCLUSIVE.** Fix A's edits took effect at runtime. The May 5 calcification fingerprint did not recur in the cycles that ran. But verification is blocked by an MM-hang failure mode that prevents the system from running long enough (15-20 cycles minimum) to characterize stable operation. Cannot declare Fix A successful or failed from this evidence alone.

### MM hang — separate failure layer requiring its own investigation

**Symptom:** After a small number of cycles (count varies), the container's loop stops producing iteration output. Logs show repeated re-initialization of MM channel functions (`commchannel`, `MM_URL`, `MM_CHANNEL_ID`, `MM_BOT_TOKEN`). MM communication is frozen. The container appears alive (process running) but no work is being processed. Recovery requires container restart.

**Status:** Pre-existing failure mode that predates Fix A (Berton confirms describing this last night). Not caused by Fix A. Blocks Fix A verification. **This is a separate issue requiring its own diagnostic sprint or fix before Fix A can be properly verified.**

**Hypothesis to investigate (deferred):** The repeated re-addition of MM channel functions suggests something in the loop is calling channel initialization mid-loop rather than once at startup. Could be a timeout-and-retry pattern, a stale-connection-recovery path that does not actually recover, or initialization being called from a place it should not be. Source location: probably in MM channel handling code, not in helper.py.

### Distinct calcification patterns identified

**Pattern A — Parser-failure feedback loop (May 5 evening):**
- Trigger: dense reasoning content with prose enumeration adjacent to S-expressions
- Mechanism: parse failure → ERROR_FEEDBACK → retry produces same failure → loop is self-sustaining
- Recovery: external intervention required (history cleanup, restart)
- Fix A addresses this trigger source.

**Pattern B — Pathological query exhaustion (this morning's iteration 2):**
- Trigger: open-ended directives that invite maximally-sweeping match queries (e.g., `(match &self ($rel $x $y) ($rel $x $y))`)
- Mechanism: query iterates entire AtomSpace, produces massive COMMAND_RETURN result set, bloats next prompt
- Recovery: query exhausts itself within a cycle or two; system can self-correct
- Fix A does not address this directly. Mitigation: tighten match-query examples in IDLE_DIRECTIVE protocol section. Deferred — not immediately blocking.

### Backlog items deferred to Sprint 4.5 or later

1. **MM hang investigation and fix** — pre-existing failure mode blocking Fix A verification. Highest priority because it blocks all verification of subsequent changes.

2. **LLM-output normalization sprint** — broader infrastructure improvement around the parsing chain. The current `balance_parentheses` salvage mechanism is load-bearing for cases we have not catalogued; changing it without that catalog is risky. Sprint 4.5 candidate, after MM hang is resolved.

3. **ERROR_FEEDBACK foregrounding** — `MULTI_COMMAND_FAILURE_NOTHING_WAS_DONE_PLEASE_CORRECT_PARENTHESES_AND_USE_QUOTES_AND_RETRY` exists as `HandleError` in loop.metta line 117 but is buried in `LAST_SKILL_USE_RESULTS` rather than foregrounded as a dedicated retry signal. Improvement opportunity: separate ERROR_FEEDBACK section in next-cycle prompt with explicit "your previous output failed parsing because of X — fix X before retrying" guidance. Sprint 4.5 candidate, related to retry-exhaustion wiring already scoped there.

4. **History.metta write-path discipline** — investigation of whether the serializer that produces history entries handles nested S-expression markup correctly. Multiple incidents where pollution accumulated and required manual cleanup. Defense-in-depth hardening so future upstream loops do not corrupt the file the same way. Lower priority than items 1-3.

5. **Genesis Encounter directive specificity** — directive language is currently generic enough to invite sweeping queries. Tightening the match-query examples to specific patterns rather than `(match &self ...)` placeholder would constrain LLM interpretation. Small change, can ship with item 2 or independently.

6. **Audit of additional prompt-producing files** — Fix A targeted four runtime locations identified by repo-wide grep for `(N) Word` patterns. Future prompt-source additions should be audited for the same pattern at the time of authoring. Methodology entry: any new file that produces text destined for LLM prompts should avoid parenthesized enumeration in any form.

### Methodology lessons captured

To be promoted to Sprint 3 Knowledge at Stage 4.4 closeout:

- **Verify before claim, even in conversation.** Partial evidence does not justify high-confidence claims. The LLM-as-collaborator must apply the same Investigation Process Commitment to its analytical statements that it applies to code changes. When Berton asks "how do you know that factually?", the answer "I do not, fully" is the honest position to start from before claiming otherwise.

- **Commit before destructive change, not just after.** When applying a multi-file fix, the cleaner pattern is `git commit baseline` → `apply fix` → `git commit fix`. Rollback then becomes `git revert HEAD` instead of restoring N backup files. The `.bak` files Fix A created work, but git lineage would have been cleaner.

- **One change at a time, even when multiple changes are obvious.** Fix A bundled seven edits across five files because they were all the same kind of change with the same hypothesis. This was acceptable because all edits had identical risk profile (string replacement in non-executable content). When edits have different risk profiles, they must be sequenced separately.

- **Verification environment failures must be diagnosed before declaring fix outcomes.** Fix A may be successful, but cannot be declared so until the MM hang is resolved and stable operation can be observed. The temptation to declare success based on partial verification is itself a discipline failure.

- **Recovery patterns are real evidence.** The fact that Clarity self-corrected after the cycle 4 syntax_error in the post-Fix-A run (producing well-formed output that explicitly referenced the prior conversation) is significant evidence that the substrate-LLM feedback loop can be a learning loop rather than a calcification loop when the inputs are clean. Worth marking — the recent-action subsystem and parser-feedback signal work as designed when the feedback is parseable.

---

## The Plan

**Goal:** Replace the hardcoded stub at `loop.metta` line 121 with a substrate-derived output verdict that re-evaluates the LLM's proposed command batch against soul-namespace safety policy before execution at line 143. Closes a known safety stub. Builds the SN-FPN coupling channel on the output side per Artifact 4 Section 5.1 / 6.

**Work split:**

- **Clarity authors:** All substrate atoms and MeTTa rules (`safety_policy.metta`, `output_verdict.metta`, retry-exhaustion atoms, category-assignment atoms, REPL tests for substrate side)
- **Berton authors:** Python helpers in `helper.py` (tokenizer, substring scanner, MeTTa bridge), `loop.metta` surgical edit, bypass-attempt fixtures for tokenizer
- **Interface contract:** Python pulls policy from MeTTa per-call (not per-session), Python does string plumbing, Python passes results back to MeTTa for final verdict. MeTTa never touches strings; Python never decides policy.

### Stage 4.0 — Investigation (no commits)

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

### Stage 4.1 — Substrate primitives and Python plumbing

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

- `tokenize_shell_arg(arg_string)` — quote-respecting whitespace split
- `shell_arg_has_any_substring(arg_string, substring_list)` — generic scanner; operator list passed in from MeTTa
- Bridge function called from `shell-cmd-classification` rule that pulls policy from MeTTa per-call

**REPL coverage:** All substrate atoms and Python helpers tested before Stage 4.2 begins. Bypass-attempt fixtures (`bash -c "rm ..."`, `grep | xargs rm`, `echo "" > path`, `ls; rm`, backtick substitution) confirm whitelist correctly classifies all as elevated.

### Stage 4.2 — Composite verdict rule

**Clarity authors in `soul/output_verdict.metta`:**

`(compute-output-verdict $sexpr $metta_cmds)` — single tail-defaulted rule following 4.0 idiom.

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

### Stage 4.3 — Loop wiring (the surgical edit)

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
- **No live PAUSE testing** — PAUSE coverage stayed in 4.2 REPL
- Confirm line 141 soul-note recording fires correctly on FLAG case

### Stage 4.4 — Documentation closeout and merge

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

*Stage 4.0 ships no commits — investigation only.*

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
