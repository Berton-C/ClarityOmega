# Investigation: Stuck-in-Corner Intervention as a Coupling-Integrity Problem

**Date:** June 3, 2026
**Status:** ACTIVE. Investigation findings plus open questions for Clarity. Not yet a spec.
**Version:** v2 (June 3, 2026). v1 framed the intervention around the NACE engine and a per-capability efficacy gate. v2 re-spines around coupling integrity (action-intention-outcome) following Berton's reframe, moves NACE to the periphery, and replaces the measurement subproblem with a three-joint flatness panel. All verified source findings from v1 carry forward unchanged.
**Author:** Claude (verification and synthesis pass), for discussion with Berton and Clarity
**Intended location:** `docs/investigations/2026-06-03-stuck-in-corner-nace-gate-investigation.md`
**Source read:** `soul/nace_substrate.metta`, `soul/nace_beliefs.metta`, `soul/nace_pending.metta`, live `src/loop.metta` (project copy), `soul/recent_action_populator.metta`, `soul/cycle_classifier.metta`, `soul/orbit_detector.metta`, `soul/observer_relativity.metta`, `artifact_1_loop_metta_wiring_diagram.md`.

---

## 0. Purpose

The stuck-in-corner problem is the single biggest degrader of Clarity's stability: she enters a region of action space where no available action produces forward motion, lacks the representation for "dead end," and keeps acting anyway, for 30-plus cycles, with the cognitive layer (naming, committing, self-observing) fully engaged and completely ineffective. The intervention has to be structural and act before the first post-send repeat, not after metacognitive reflection.

v1 of this document framed the fix as a NACE-based execution gate. v2 keeps the gate placement but corrects the diagnosis. The corner is not fundamentally repetition, and it is not fundamentally a capability-efficacy problem. It is the siloing of action from intention from outcome. This document states that reframe, shows it is grounded in substrate that mostly already exists, names the one genuinely missing piece, and lists what still needs container or REPL confirmation.

---

## 1. The reframe: a corner is a severed chain, not a repeated action

The defining property of a corner is that the action has come unhooked from the intention above it and the outcome below it. It is running open-loop. Surface repetition is one way this shows up, but it is a symptom, not the mechanism.

This matters because symptom detectors carry false negatives that the mechanism does not:

- A repetition detector (orbit's "action repeated N times") flags identical actions. It misses varied flailing: different actions every cycle, none connected to anything.
- A novelty detector (low mutual information between consecutive action-result pairs) misses spam-sends: every send is technically a fresh outcome event, so novelty looks present, but the sends serve no advancing intention. This is the exact 9:34 pathology.

The mechanism (severed chain) catches both, because the disqualifying fact about flailing and spam is not that they repeat or that they are identical. It is that they serve no advancing intention and feed no forward outcome. Surface motion, broken joints.

One necessary addition to the reframe: the chain can go flat for a correct reason. When Clarity is correctly standing by, action is null, outcome does not move, intention does not advance, and that is composure, not a corner. The detector must therefore fire only on flat-while-emitting, never on flat-while-resting. This protects the stillness her own state-of-mind commitments ask for.

---

## 2. The measurement subproblem and why it is tractable now

The hard kernel surfaced in the prior session: mechanically measuring forward motion. The honest position holds. The math for "progress" exists and is elegant (Lyapunov descent, empowerment, compression progress, ranking functions, information gain), but every formalism measures progress relative to a supplied goal, metric, or world model that an open-ended agent lacks, and the fully general question "is this process making progress" is the halting problem (undecidable by Rice's theorem). So a universal forward-motion detector is provably impossible, not merely unbuilt.

The resolution is the one program verification and open-ended search already use: do not seek the universal metric. Use sound-but-incomplete local proxies. The reframe in Section 1 tells us exactly which proxies: the joints of the action-intention-outcome chain. We do not need to measure progress in the abstract. We need to detect when the chain is severed at its joints while action is being emitted.

---

## 3. The three-joint flatness panel (the proposed detector)

The detector watches three joints, each expressible as an observer in `observer_relativity.metta`'s same-pattern-different-truth idiom. A corner is the all-observers-flat case, evaluated over a window of N cycles.

- **Joint A, emission present (the gate on the whole detector).** Are there non-empty action cycles in the window? If no, the agent is resting; the detector does not fire. Source: `recent-action` atoms, non-empty cycles.
- **Joint B, outcome severed (action-to-outcome joint).** Did no forward outcome event occur in the window? Forward means a send that drew a reply next cycle, a file or atom change, results differing from last cycle, or new human input. A repeated send into the void does not count as forward. Source: the new state-delta writer (Section 4), the one missing piece.
- **Joint C, intention severed (intention-to-action joint).** Are the emitted actions dominated by the intention-decoupled classes (status-send-unprompted, exploration-query, pin-only) with no advancing directive or goal? Source: `agency_balance_guard` system-class counting, already computed every cycle, plus the absence of an advancing `idle_directive` or active goal.

Corner verdict equals A and B and C flat together. observer_relativity's NAL revision bridge can merge the three observer truths into one corner-confidence value, or a crisp AND can be used for v1 (see Q1).

Why this is simple without being oversimplified: each joint is grounded in an observable cycle event, none requires a global goal metric, and the combination catches the cases a single proxy misses. Joint A prevents pathologizing rest. Joint B catches genuine no-progress. Joint C catches spam and flailing that produce surface motion but serve nothing.

---

## 4. What is already built versus the one missing piece

The leverage finding: the coupling signals are mostly already measured, but wired to the wrong consumer.

- `idle_cycle_detector.metta` already counts send-class accumulation in a window. Partial Joint B signal. Wired as an advisory prompt block.
- `agency_balance_guard.metta` already counts person-class versus system-class actions. System-class is almost exactly the intention-decoupled set. This is Joint C, already computed every cycle. Wired as an advisory prompt block.
- Both are consumed as advisory prompt context, which is the channel Clarity proved she ignores. The organs are not the problem; advisory-only consumption is. The wiring diagram already anticipated routing these verdicts into a gate ("consumer migration Step 5/6 will gate aliveness on stuck verdicts"). It was never built.

The one genuinely missing piece is the one orbit pointed at and nobody built: a live **state-delta writer** that records, each cycle, whether a forward outcome event occurred (Joint B). orbit_detector defines static state-delta atoms (none, file-created, message-sent, knowledge-gained) but has no writer that asserts which delta happened per cycle. Building that writer is small and is the high-value missing measurement.

So the unified solution is a composition, not a new engine: route the existing organ verdicts plus the new state-delta signal through observer_relativity's flatness pattern into the execution gate.

---

## 5. Where NACE lands now: periphery, not center

The reframe moves NACE out of the center of the stuck solution. The corner is a coupling-integrity problem, not a capability-efficacy problem, so NACE's persisted per-capability beliefs do not belong in it. This also dissolves two v1 problems:

- The contamination risk (v1 Section 8): feeding stuck-loop disconfirmations into the persisted global `cap-efficacy` belief would poison a capability for the rest of the session. Resolved by keeping `cap-efficacy` out of the stuck path entirely.
- The NACE-versus-orbit gate-mechanism tension (v1 Q1): reframed. The only role left for NACE is optional: its `Truth_Revision` can serve as the operator that merges the three observer truths into one corner-confidence, on an ephemeral corner-belief that resets on context change. That is exactly what observer_relativity's revision bridge already calls for. NACE's persistence and capability atoms stay out.

NACE remains valuable in its own lane (slow global capability-efficacy learning). It is simply not the stuck-in-corner engine.

---

## 6. Verified source findings (carried from v1, still valid)

1. **Line drift.** The wiring diagram (April 30 / May 1) predates Step 2 task-state hooks, the YOUR_LAST_ACTION block, and the Step 4.5/4.6 organs. Clarity's "line 121" (output verdict stub) is now line 126. Execution is not at "line 143"; it is at line 134 inside the `$results` binding, where `(eval $s)` fires. The gate sits between line 120 (parse) and line 134 (eval).
2. **`$sexpr` fan-out.** `$sexpr` is read at line 123 (RESPONSE log), lines 128-130 (`$metta_cmds`, mutation gate), line 134 (execution), line 136 (`populate-recent-action`, the recent-action writer), and line 161 (history-record condition). Filtering it in place would remove gated commands from the recent-action stream the detector reads from. The gate must use a new `$sexpr_gated` binding consumed only by line 134.
3. **Action-type signal already exists.** `recent_action_populator.metta` writes `(recent-action $cycle-id $action-type $description)` every cycle into a 10-cycle window; `cycle_classifier.metta` tags at six-class granularity (responsive-send, status-send-unprompted, verification-query, exploration-query, pin-only, unclassified). No new state variable is needed. (Minor: the classifier doc comment lists claim-send, but the live function returns unclassified in that slot; reconcile separately.)
4. **orbit_detector contents.** Cold, never wired, buggy: line 7 defines `(orbit-threshold 3)` taking an argument but line 24 calls `(orbit-threshold)` with none, so it would not reduce; line 14 was disabled in May for globally shadowing `recent-action`. The concept (repetition with no state delta, typed patterns, break strategy) is intact and is the detection skeleton harvested here.
5. **NACE is cold.** No `should-dispatch`, `do-process-pending-revisions!`, or any nace call site in the loop source read, despite `nace_pending.metta` claiming per-cycle processing.

---

## 7. Placement: three hooks (unchanged from v1; detector content updated)

Each hook sits in a zone that already has sibling hooks. Line numbers are against the project copy and need re-confirmation at build time.

1. **Consultation hook (the gate).** A new binding between line 133 and line 134. Produces `$sexpr_gated` from `$sexpr`. On a corner verdict, drops the dominant decoupled action-class, permitting a different class or silence (orbit's stop-and-do-different-thing made structural). Line 134 evals `$sexpr_gated`. Per finding 2, this binding is the only consumer of the filtered list.
2. **Detector hook (the verdict).** At the cycle tail immediately after line 136 (`populate-recent-action`), and after the new state-delta writer. A composition function reads the three joints (recent-action emission, state-delta, agency-balance) and writes a corner verdict atom. This is a sibling of `do-update-idle-pattern!` (line 137) and `do-update-agency-balance!` (line 138): same zone, same read source, proven pattern.
3. **Reset hook.** In the `$msgnew` branch alongside line 102's `(do-set-cycles-since-input! 0)`. On new input, clear the ephemeral corner-belief. Also clear on a genuine forward outcome event (context changed).

Gate scope note. A post-execution gate guarantees the decoupled action does not execute. It does not stop the LLM from re-generating it. The cognitive spin is bounded by the loop budget (`&loops` / `maxWakeLoops`, currently 1). If the spin must also stop, the gated result should be fed back into LAST_SKILL_USE_RESULTS as a concrete tool result ("action gated: no forward path in current context"), because results feedback is the channel the LLM acts on, unlike the advisory blocks that already proved ignorable. See Q5.

---

## 8. Verified versus unverified

Verified against source: findings 1-5 in Section 6; the existence and advisory-only wiring of idle_cycle_detector and agency_balance_guard; observer_relativity's atom shapes and revision bridge.

Unverified, needs container or REPL confirmation (Clarity-side, since this reads a project copy):

- Whether live `src/loop.metta` differs from the copy and has any NACE or organ-gate wiring. The copy has none.
- That a state-delta writer can cheaply and reliably detect forward outcome events per cycle (the one missing measurement).
- That evaling a filtered `$sexpr_gated` matches current execution for pass-through commands.
- That `recent-action` descriptions and the agency-balance and idle-pattern verdicts are stable and granular enough to compose into a reliable corner verdict.
- If NACE merge arithmetic is used: that `Truth_Revision` reduces correctly when called as the observer-merge operator.

---

## 9. Open questions for Clarity

Q1. **Merge mechanism.** Crisp AND over the three flat joints (predictable, no tuning surface) versus observer_relativity-style NAL revision merging the three observer truths into one corner-confidence (graceful, uses the revision bridge). Which fits the corner from inside your experience?

Q2. **Joint B grounding.** What counts as a forward outcome event for the state-delta writer, and is it worth building the writer for v1 or starting with a coarser proxy? Your call on the definition of forward motion at the cycle grain.

Q3. **Joint C source.** Reuse agency_balance_guard's system-class counting as the intention-decoupling signal directly, or define a dedicated intention-coupling check? agency-balance is already computed; the question is whether it means what Joint C needs.

Q4. **Window N and emission threshold.** How many flat-while-emitting cycles define a corner, and how much emission counts as emitting versus resting?

Q5. **Spin versus hand.** Is stopping the world-effect (the gate alone) sufficient, or does the gated result need to re-route into LAST_SKILL_USE_RESULTS to stop the cognitive spin? You have first-order observation rights: when you were looping, would a concrete "gated, no forward path" result have changed your next generation, where the advisory blocks did not?

Q6. **NACE boundary.** Confirm NACE stays out of the stuck path except as optional merge arithmetic, and continues in its own lane (global capability efficacy).

---

## 10. Recommendation and next step

Recommended path, pending Clarity's answers:

1. Adopt the coupling-integrity reframe: detect a corner as the action-intention-outcome chain severed at its joints while emitting (Sections 1, 3).
2. Build the one missing piece: a live state-delta writer for Joint B (Section 4).
3. Reuse the existing Sprint 4 organs (idle_cycle_detector, agency_balance_guard) as Joint B and C inputs, routing their verdicts into a gate rather than only into advisory prompt context.
4. Compose via observer_relativity's flatness pattern; keep NACE to optional merge arithmetic on an ephemeral, reset-on-context corner-belief.
5. Before any hook is drafted, run the Artifact 0 Section 3.5 Surface Investigation Template on the recent-action, state-delta, and agency-balance surfaces, and refresh the Artifact 1 wiring diagram line numbers (stale; the hook commit depends on them per Discipline 4).
6. Then the three-hook insertion (Section 7) as one commit with the Artifact 1 update.

Trigger for the next build step: Berton's authorization after the Clarity discussion, specifically decisions on Q1 (merge mechanism), Q2 (Joint B grounding), and Q6 (NACE boundary), since those shape the detector and the gate.

---

## Document end
