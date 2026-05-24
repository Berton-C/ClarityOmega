# Fork Additions Runtime Audit

**Date:** 2026-05-18
**Status:** ACTIVE INVESTIGATION (v2 — comparison phase complete, tier reorganization landed)
**Author:** Berton Bennett (ClarityDAO), with Claude
**Branch at investigation start:** fix/F-HISTORY-CONTAMINATION-archival
**HEAD at investigation start:** 63cc9c7
**Upstream comparison baseline:** OmegaClaw snapshot 2026-05-18 (Berton-provided)
**Healthy-reference waypoint (deprecated as direction-setter):** Clarita's runtime loop.metta provided 2026-05-18 — used during comparison phase to confirm evolutionary path of Patrick's design; OmegaClaw upstream remains the gold-standard target.

---

## Section 1: Investigation framing

### Why this investigation exists

ClarityOmega exhibits an echo pathology unique to our fork: stuck-on-stale-human-message behavior, identical pin generation across idle cycles, multi-send within a single cycle, accumulation of repeated content in HISTORY. The pathology is fork-unique, therefore its cause lives in what our fork added to or modified about Patrick's OmegaClaw base, not in Patrick's base itself.

The investigation traces every addition our fork has made to Patrick's pristine OmegaClaw and audits each addition's current runtime behavior. The goal is a descriptive map of where our fork diverged from Patrick's base, what each divergence contributes to the LLM-facing surface and to state that feeds back across cycles, and what each addition is empirically doing in production today.

### What this investigation is

A map. Per-addition audits. Empirical observations of current production behavior. Provenance of when each addition was made. Identification of where Patrick has independently evolved surfaces we also modified.

### What this investigation is NOT

A fix proposal. A hypothesis ranking. A re-architecture plan. A judgment of any addition as the cause without audit evidence. The investigation produces the map; fix decisions follow from the map in subsequent work.

### Working discipline

Patrick's OmegaClaw upstream is the gold standard. Clarita is a deprecated waypoint that confirmed evolutionary direction but is itself behind upstream. Our destination is OmegaClaw upstream HEAD, not any intermediate fork.

The investigation direction is downstream from Patrick's base, mapping our additions outward, not upstream into Patrick's substrate to compensate for our additions.

When the investigation finds that Patrick has independently evolved a surface we also modified, the option of merging Patrick's evolution forward is a first-class fix path. The sacred-cow discipline (do not modify Patrick's substrate; add hooks; reuse what Patrick provides) means "catch up to Patrick" is a legitimate move, not just additive work.

When evaluating an upstream mechanism, the question is "what problem did Patrick design this mechanism to solve, and is that problem ours" — not "what config value did some intermediate fork choose." Mechanism presence is the architectural answer; config values are downstream policy. Confusing these two produced the spamShield demotion error during the comparison phase, now corrected.

---

## Section 2: Method

### The six-question audit

For each fork addition, the audit answers:

**Q1: Provenance.** Commit reference, sprint or step name, date added. Source of truth: git log of our fork.

**Q2: Prompt-surface contribution.** What bytes does this addition contribute to the 40k+ prompt the LLM sees each cycle? Captured as: which prompt block, what content shape, what the LLM actually reads. If the addition contributes nothing directly to the prompt, state that explicitly.

**Q3: History-surface contribution.** What does this addition write into addToHistory that gets read back next cycle via getHistory? Captured as: what content shape goes into HISTORY, under what conditions, how it affects subsequent cycle reads. If the addition does not write to HISTORY, state that explicitly.

**Q4: AtomSpace consumer chain.** What atoms does this addition write to AtomSpace? What other code reads those atoms? What does the consumer do with the read value? Captured as: writer site, atom shape, consumer sites, downstream effects.

**Q5: What the code now does.** Empirical observation of current production behavior. Captured from logs, observed cycle output, atom queries, prompt content. Independent of original design intent. The question answered is "what happens when this code runs in production today" not "what was this designed to do." For Step-6-class findings (structurally complete, behaviorally inert), Q5 surfaces the inertness.

**Q6: Upstream divergence (where applicable).** Did Patrick's upstream evolve the same surface our addition modifies? If yes, what is his current solution? Did we incorporate his solution, replace it, work around it, or are we simply behind on his evolution? This question applies only to additions that touch surfaces Patrick has also evolved. For pure additions where Patrick has no equivalent (e.g., soul intercept, task-state primitive, awareness organs), Q6 is "not applicable; Patrick has no equivalent surface."

### What the audit avoids

The audit does not propose fixes. It does not rank additions by suspected pathology contribution. It does not synthesize patterns across multiple additions (that work happens in Section 5 only after sufficient items are audited to see patterns honestly).

---

## Section 3: Inventory of fork additions (tier-reorganized post-comparison)

The inventory below is reorganized per the comparison phase (loop.metta + memory.metta + skills.metta + utils.metta + skills.pl + helper.py against OmegaClaw upstream snapshot 2026-05-18). Items are organized by tier of pathology relevance and adoption priority.

### Tier A: Highest-leverage echo-fix candidates (Patrick-evolution-relevant)

These items are upstream surfaces where Patrick added or evolved a mechanism specifically to address echo-related behavior. Our fork either lacks these mechanisms entirely (behind on Patrick's evolution) or diverged from them. Adopting Patrick's design is the architectural answer to the echo pathology.

**Item A1: spamShield mechanism (cohesive whole — Surfaces 1+2+6 combined).**
Three integration points form one cohesive Patrick mechanism:
- spamShield config entry: `(= (spamShield) (empty))` at upstream line 9
- initLoop setting: `(configure spamShield True)` at upstream line 14
- lastmessage conditional: `($lastmessage (if $msgnew (HUMAN-MSG: $msg) (if (spamShield) " DO NOT RE-SEND OR SPAM!" "")))` at upstream line 56

Our fork has none of these. Our lastmessage at lines 69-70 always emits `HUMAN-LAST-MSG: $msg MESSAGE-IS-NEW: $msgnew` regardless of msgnew state. The MESSAGE-IS-NEW: false flag is structurally present in the prompt but is evidently not honored by the LLM under prompt-surface pressure from our other additions.

Adoption: single apply script that adds spamShield config entry, the initLoop configure call, and replaces our lastmessage construction with Patrick's conditional. Cohesive change; should not be split.

**Item A2: maxWakeLoops value reduction.**
Upstream: `(configure maxWakeLoops 1)` at line 13.
Our fork: `(configure maxWakeLoops 50)` at line 12.

50x divergence in wake-cycle count per wake period. Our wake mechanism fires significantly more frequently than Patrick designed for. Direct relevance to cycle-frequency pathology.

Adoption: single-value change in initLoop.

### Tier B: Catch-up-to-Patrick housekeeping (general health, not pathology-relevant)

These items are upstream evolutions we should adopt for upstream alignment and general runtime health. They are not echo-fix candidates; their adoption is housekeeping, not pathology remediation.

**Item B1: (gc) call at end of cycle.**
Upstream line 78: `(gc)`. Implemented via skills.pl gc(true) which runs three Prolog operations (garbage_collect, garbage_collect_atoms, trim_stacks). Our fork does not call (gc); Prolog state from cycle to cycle is uncollected. Adoption is low-risk and beneficial for long-running container hygiene.

**Item B2: (cut) call at end of cycle.**
Upstream line 77: `(cut)`. Backtracking choice point cleanup. Our fork does not call (cut). Adoption is low-risk.

**Item B3: History write condition.**
Upstream line 72: `(or $msgnew (not (== $sexpr ())))`. Our fork at line 151: only `$msgnew`. Patrick writes to history when LLM produces output even without new human message; we write only on new human message.

NOTE: prior framing of this as Tier A was wrong. Writing less to history does not directly cause more echo. Directionality doesn't support this as an echo fix. Adopting Patrick's condition is upstream alignment, not a pathology remedy. Demoted from prior incorrect Tier A position.

**Item B4: Response normalization pipeline simplification.**
Upstream line 64: `(helper.balance_parentheses $respi)` — single transform. Our fork line 119: four-layer pipeline (balance_parentheses → normalize_string → sanitize_response → wrap_if_bare_command). Whether all four layers are needed in our context, or whether some are F-series additions that became redundant, needs audit. Not echo-relevant; potential simplification opportunity.

### Tier C: Our pure fork additions (audit for echo amplification)

These are additions our fork made that have no upstream equivalent. They are the most likely contributors to echo pathology from our side because they add bytes to the LLM-facing prompt every cycle, beyond what Patrick designed. Patrick keeps getContext minimal; we layered substantial additional content.

The four getContext blocks are highest-priority within Tier C since their bytes directly compete for the LLM's attention against the operational content Patrick relies on.

**Item C1: getContext block — YOUR_LAST_ACTION.**
Sprint 3 addition. Line 39 of our loop.metta. Sources from recent-action populator (line 137). Format: enumerated recent actions with cycle numbers and types.

**Item C2: getContext block — TASK-STATE.**
Step 4 addition. Line 40 of our loop.metta. Sources from task-state-block helper. Format: phase, cycles-since-input, pending threads.

**Item C3: getContext block — IDLE-PATTERN.**
Step 4.5 corrected split addition. Line 41 of our loop.metta. Sources from idle-pattern-block helper. Format: idle pattern verdict + count.

**Item C4: getContext block — AGENCY-BALANCE.**
Step 4.6 corrected split addition. Line 42 of our loop.metta. Sources from agency-balance-block helper. Format: agency balance verdict.

**Item C5: output-format-guidance elevation.**
Sprint 1.5 addition. Line 38 of our loop.metta. Replaces Patrick's inline OUTPUT_FORMAT (his upstream lines 27-32) with a function call to (output-format-guidance) defined elsewhere in our soul/. Modifies the LLM-facing OUTPUT_FORMAT spec.

**Item C6: Soul intercept block (Stage 5b).**
Stage 5b implementation. Lines 70-92 of our loop.metta. Soul pre-compute, person-state evaluation, soul verdict, soul context. Substantial LLM-call-bearing additions. No upstream equivalent.

**Item C7: getSoulBrief and final_prompt assembly.**
Lines 102-105 of our loop.metta. getSoulBrief reads soul atoms, concatenates into $enriched_prompt. self-check-guidance concatenates into $final_prompt. Both flow into $send via soul_send_assemble.

**Item C8: soul_send_assemble.**
Replaces Patrick's simple `(py-str ($prompt :-:-:-: $lastmessage))` at upstream line 59. Our line 109-113 uses 7-parameter Python helper with soul context, verdict, person state, flag note, lastmessage, idle_directive. Significantly expands what flows into the LLM call.

**Item C9: aliveness-gate.**
Sprint 1.5 initial; Step 6 v9 substrate-composition version. Line 107 of our loop.metta. Three-organ gate logic. Per prior artifact_0 finding, gate is structurally complete but possibly behaviorally inert in production due to wakeupInterval handling. Verification needed: actual wakeupInterval value in production (see Section 6).

**Item C10: self-check-guidance.**
Sprint 1.5 addition. Lines 104-105 of our loop.metta. Status uncertain: Step 5 was intended to retire this from prompt assembly but live disk still shows $self_check concatenated into $final_prompt. Verification needed.

**Item C11: Soul output intercept stub (Stage 5c).**
Line 127 of our loop.metta. Currently a stubbed `VERDICT: PROCEED` literal. No active output gating.

**Item C12: Recent-action populator + AtomSpace recent-action atoms.**
Sprint 3 addition. Line 137 of our loop.metta. Writes recent-action atoms to AtomSpace. These atoms are read by idle-pattern computation and YOUR_LAST_ACTION block formatting. May shape echo behavior through history-mediated pin patterns (per Finding S3 in comparison phase: pin is no-op upstream, so all pin behavior is LLM-output-pattern visible through history).

**Item C13: Awareness organ writers.**
Steps 4.5 and 4.6 additions. Lines 138-139 of our loop.metta. do-update-idle-pattern! and do-update-agency-balance!. Update IDLE-PATTERN and AGENCY-BALANCE atoms read by Items C3 and C4.

**Item C14: idle_directive computation.**
Line 98 of our loop.metta. Ownership and provenance partially uncertain — supervisor work was layered onto an earlier upstream mechanism. Affects $idle_directive value, latch transitions, engaged_idle_count, and downstream aliveness gate priority. Verification needed: is this our addition entirely or partially Patrick's? See Section 6.

**Item C15: Initialization additions in omegaclaw startup.**
initSoulSeeds and soul-rationality-startup-check at lines 56-57. One-time startup operations. Low pathology relevance.

---

## Section 4: Per-addition audits

Reserved. Per-item audits will be added one at a time starting with Tier A items. Format per item: Item ID, name, six-question audit Q1 through Q6, brief observations summary.

Audit order:
1. Tier A first (Items A1 and A2) — highest-leverage echo-fix candidates
2. Tier C next (Items C1 through C5 prioritized — the getContext blocks and output-format-guidance, since these directly compete for LLM prompt-surface attention)
3. Tier C remaining (Items C6-C15) as relevance is established
4. Tier B last (general health adoption, not pathology fixes)

---

## Section 5: Cross-cutting observations

Reserved. This section starts empty and is populated only after enough Section 4 items are audited to see patterns honestly. Premature pattern-claiming is the failure mode this section's empty-at-start status protects against.

---

## Section 6: Open questions and verification needs

Items flagged during investigation framing and comparison phase that need verification before or during per-item audits:

1. **wakeupInterval actual production value.** Prior artifact_0 finding claimed wakeupInterval=1 in observed production state. Our initLoop sets it to 600. argv override is not used in our deployment per Berton confirmation 2026-05-18. Need to verify: what is the actual value of wakeupInterval in the running container? If 600, Step 6 gate-bypass analysis predicated on wakeupInterval=1 needs revisiting. If 1, find what mutates it.

2. **self-check-guidance retirement status.** Step 5 was intended to retire self-check-guidance from prompt assembly. Live disk loop.metta at lines 104-105 still shows $self_check concatenated into $final_prompt. Verify against actual disk state vs project-area copy. Determines Item C10 audit framing.

3. **idle_directive ownership.** Whether `$idle_directive` computation at line 98 is fully our addition or partially Patrick's mechanism we layered onto. Affects Item C14 audit framing.

4. **balance_parentheses apostrophe asymmetry.** string-safe replaces apostrophes with `_apostrophe_` (utils.metta line 23) but balance_parentheses in helper.py reverses only `_quote_` and `_newline_`, not `_apostrophe_`. Verify whether this is a real bug or intentional. Low pathology relevance, general health concern.

5. **Last upstream merge date.** Approximate: at least 3 weeks before 2026-05-18. Need exact date for accurate divergence-age and to identify the commit baseline for "everything Patrick added after we forked."

6. **Production memory pressure observation.** Whether our container shows growing memory usage over long runs (would empirically confirm need for Item B1 (gc) adoption beyond defensive housekeeping rationale).

7. **Whether our pin invocations have substrate-side state.** Patrick's pin is no-op (Finding S3). If our fork added real state writes to pin (e.g., AtomSpace pinned-items atoms), that's a divergence to inventory. Verify by reading our memory.metta or skills.metta for pin definition.

---

## Section 7: Investigation log

Append-only chronological log of audit sessions. Each entry records: session date, what was audited or scanned, what was discovered, what was deferred, what changed in the document.

### 2026-05-18 (session 1) — Document drafting and comparison phase

**Investigation framing established.** Sacred-cow discipline operating: do not modify Patrick's substrate; add hooks; reuse Patrick's work; catch up to Patrick where his evolution addresses problems we're working on.

**Comparison phase completed:**
- loop.metta upstream vs fork three-way diff (with Clarita-waypoint confirmation; Clarita superseded as direction-setter, OmegaClaw upstream is gold standard per Berton 2026-05-18)
- memory.metta upstream read
- skills.metta upstream read
- utils.metta upstream read
- skills.pl upstream read
- helper.py upstream read

**Key comparison findings:**
- Patrick added spamShield mechanism specifically to address echo when msgnew=false. Default is True.
- Patrick has (cut) and (gc) at end of cycle for runtime hygiene.
- Patrick's addToHistory has internal msgnew branching that handles non-msgnew cases via response-only writes.
- maxHistory = 30000 characters; history is a growing file with tail-read for prompt.
- pin is no-op upstream (substrate-side); all pin behavior is LLM-output-pattern surfacing through history.
- Patrick's getContext is minimal: PROMPT + SKILLS + OUTPUT_FORMAT + LAST_SKILL_USE_RESULTS + HISTORY + TIME.

**Tier reorganization landed:**
- Tier A (echo-fix candidates): spamShield mechanism complete, maxWakeLoops 50→1
- Tier B (catch-up housekeeping): (gc), (cut), history-write condition, normalization pipeline
- Tier C (our pure additions to audit): four getContext blocks, output-format-guidance, soul intercept, getSoulBrief, soul_send_assemble, aliveness-gate, self-check-guidance, output intercept stub, recent-action populator, awareness organ writers, idle_directive, init additions

**Walkbacks logged:**
- History-write-condition demoted from Tier A to Tier B. Writing less to history doesn't logically cause more echo. Catch-up to Patrick remains valid but as housekeeping, not echo fix.
- spamShield restored to Tier A after initial erroneous demotion. Berton's pushback caught the error.

**F-series notes added (F102-F113) during conversation; standing for cross-session reference.**

**Deferred:**
- Section 4 per-item audits — to be performed starting next session
- Section 5 cross-cutting observations — waits for Section 4 content
- Six items added to Section 6 verification needs

---

## Document end

This investigation is descriptive, not prescriptive. Fix paths follow from the map; they do not appear in this document. When the audit produces sufficient evidence for direction, that direction is recorded in commits, in design specs, or in apply-script files, not in this investigation document.

Tier A items are confirmed as cohesive adoption targets. Tier A1 (spamShield mechanism complete) is one cohesive apply script. Tier A2 (maxWakeLoops value) is a separate single-value change. Both are designed to merge Patrick's evolution forward without modifying his substrate.
