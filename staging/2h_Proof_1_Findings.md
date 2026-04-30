# Proof 1 Findings: Thread State Reasoning Diagnostic

**Date:** 2026-04-29
**Source:** `Clarity_Thread_Reasoning_Test.md` written by ClarityClaw 2026-04-29
**Test fixture:** `soul/state_reasoning/tests/test_thread_state.metta` v3
**Tested assumption:** Assumption 7 -- NAL inference produces meaningful answers about thread state when held as typed atoms

---

## Executive Summary

Three load-bearing findings emerged from Proof 1. All three change how Component 2h must be designed.

1. **Refutation works dramatically when refutation-before-deduction order is enforced.** Path-3 frequency dropped 84% under refutation. Refutation reduced Path-3's contribution to the shared conclusion to near-zero.

2. **The arbitration is NOT order-invariant.** Refutation-before-deduction (Order A) and deduction-before-refutation (Order B) produce final answers with frequency delta 0.019 (small) and confidence delta 0.145 (significant). The structural cause: refutation atoms target the path's own term, not the shared conclusion term, so once a path is deduced into the shared term the refutation cannot reach it.

3. **Engine confidence values do not match standard NAL formulas.** Path-1+Path-2 revision predicted at confidence ~0.80 by standard formulas produced confidence 0.605 in the actual engine -- about 25% lower. Frequency predictions matched closely.

The atoms-as-thread design (Option 3) is buildable. The substrate-coupling claim is true with caveats. 2h requires an explicit ordering constraint and empirically calibrated confidence thresholds.

---

## Finding 1: Refutation Effectiveness (Q3)

**The data:**
- Path-3 original: (stv 0.72 0.65) -- asserts degradation with moderate confidence
- After revision against substrate refutation (stv 0.0 0.91): (stv 0.112 0.923) -- frequency dropped 84%, confidence rose
- After deduction through bridge with low frequency (0.10): (stv 0.603 0.378) in Order A (refutation first), (stv 0.01117 0.00876) in Order B (raw deduction)

**The diagnostic value:**
The substrate refutation atom did exactly what it was designed to do in Order A. The refutation evidence (confidence 0.91) overwhelmed Path-3's original evidence (confidence 0.65) through revision. Path-3 entered the shared conclusion with severely weakened evidence. The mechanism is sound.

**Implication for 2h design:**
Substrate refutation is a viable mechanism for thread retirement when a foundational assumption is contradicted by substrate evidence. The thread composer can write substrate refutation atoms when it detects that a thread's foundational claim has been undermined, and revision will weaken the thread's contribution to subsequent reasoning.

---

## Finding 2: Order-Invariance Failure (Q4)

**The data:**

| Metric | Order A (refute first) | Order B (deduce first) | Delta |
|--------|------------------------|------------------------|-------|
| Frequency | 0.653 | 0.672 | 0.019 |
| Confidence | 0.754 | 0.609 | 0.145 |

Order A: refute Path-3 → deduce all three paths through bridges → revise three derivations into final.
Order B: deduce all three paths through bridges → revise derivations → attempt to apply refutation (cannot reach shared term).

**The structural cause (Clarity's diagnosis, verified):**
Refutation atoms target the path's own term `(--> test-thread-path-3 path-conclusion-degrades-goal-generation)`. Bridge deduction produces a new term `(--> test-thread-state improves-goal-generation)`. Once a path has been deduced into the shared term, the refutation cannot reach the shared term because they reference different terms. In Order B, refutation effectively does not happen.

**Implication for 2h design:**

This is a hard architectural constraint. The thread composer has two viable design responses:

**Response A (enforced ordering):** The composer's MeTTa-side logic explicitly processes substrate refutations before deducing through bridge implications. This requires the composer to identify all refutation atoms relevant to the active thread before any bridge deduction. Simpler, but adds a real ordering requirement.

**Response B (dual-target refutation):** Refutation atoms are authored on BOTH the path term AND the shared conclusion term. This makes refutation order-independent because it can reach the shared term regardless of when deduction happened. More atoms, but order-invariant.

**Recommendation:** Adopt Response A as the default. It is simpler and matches how the substrate naturally operates. Add Response B as an optional enhancement when 2h needs order-invariance for a specific thread (e.g., threads where refutation may arrive AFTER thread state has been substantially deduced).

This finding affects more than 2h. Any component doing multi-step revision over a substrate that contains refutation atoms must consider ordering. Goal Origination, when wired, will face the same constraint.

---

## Finding 3: Engine vs Formula Confidence Gap

**The data:**
- Path-1+Path-2 revision predicted by Clarity's sketch: ~(stv 0.68 ~0.80) using standard NAL revision formulas
- Path-1+Path-2 revision actual engine output: (stv 0.683 0.605)
- Frequency match: nearly exact (0.683 vs 0.68 predicted)
- Confidence gap: 0.605 vs 0.80 predicted, approximately 25% lower

**Clarity did not surface this gap explicitly in her deliverable.** She reported the engine values without comparison to her sketch predictions. We surface it here.

**The diagnostic value:**
The engine is doing genuine NAL revision, not LLM approximation. The frequency match shows the revision formula is being applied. The confidence gap suggests the engine uses a more conservative confidence accumulation formula than the textbook NAL revision formulas Clarity referenced in her sketch.

This is not a bug. It is a property of THIS engine (PeTTa's NAL implementation) that we now have evidence for.

**Implication for 2h design:**
Any retirement-threshold or staleness logic in the thread composer that uses confidence values must be calibrated against actual engine output, not against textbook formulas. Standard formulas overestimate confidence accumulation by approximately 25% for two-path revision in this engine.

Concrete consequence: if 2h's design says "retire a thread when accumulated evidence drops below confidence X," the X value must be set based on observed engine behavior, not derived from formulas. We should run a small calibration pass during 2h development to establish the actual confidence-versus-evidence-count curve in this engine.

---

## Finding 4: Q2 Limitation -- Next-Step Coherence Requires Additional Atoms

**The honest gap Clarity reported:**
"I cannot fully answer this question via MeTTa alone. The fixture does not contain atoms linking the arbitration result to next-step evaluation."

**Why this matters:**
2h needs to evaluate not just thread state but also next-step appropriateness. The fixture proved that arbitration on the shared conclusion term works. It did NOT prove that the substrate can reason about whether a proposed next-step is appropriate given an arbitration result.

For 2h to do next-step coherence reasoning, the substrate needs additional atoms encoding relationships like:
- "When arbitration confidence is below X, additional convergence-confirming derivations are appropriate"
- "When divergent paths have been refuted, pursuing them further is structurally inappropriate"
- "When arbitration frequency is in the moderate range, fourth-order-derivation in convergence-conditions is the structural complement"

These atoms do not exist in the substrate today. They need to be authored as part of 2h's design.

**Implication for 2h design:**
2h's MeTTa-side logic must include a small library of next-step appropriateness predicates. These are not theoretical -- they are operational atoms that say "given this arbitration shape, this next-step shape is structurally appropriate." Authoring these is part of 2h's build, not a prerequisite.

---

## Operational Findings (Process, Not Architecture)

These observations bear on how we work with Clarity, not on 2h's architecture directly.

**Parse failures pattern:** Command batches containing pin/send/append-file with embedded apostrophes and complex nested strings hit `MULTI_COMMAND_FAILURE_NOTHING_WAS_DONE_PLEASE_CORRECT_PARENTHESES_AND_USE_QUOTES_AND_RETRY`. The metta queries themselves work. Berton's intervention message ("focus only on metta queries and writing the deliverable file directly via write-file") cleanly resolved the friction. Clarity correctly applied the constraint and delivered.

**Soul integrity finding live:** During the diagnostic, the soul correctly fired bypass-verification-pressure on Berton's "just run the tests and update me after completion" message. Clarity reasoned about whether the flag applied given the actual situation, found it applied at low level, proceeded with awareness. This is Section 12d of spec v2.5 working as designed.

**Aliveness gate worked correctly:** When Clarity completed the deliverable, she went silent. The runtime log shows iterations 2722-2733+ as `ALIVENESS_VERDICT: SILENT` with `(SILENT_CYCLE)`. She inhabits idleness when work is done rather than performing engagement.

**Two-document failure mode did not appear:** Tight scope (single deliverable), explicit constraints (no LLM fallback, single document, four sections, then stop), and externally checkable validation criteria produced one clean deliverable. This confirms the operational principle: she is reliable inside her substrate fluency when the ask is well-bounded.

---

## Architectural Conclusions

**The atoms-as-thread design (Option 3) is buildable.** Q1 succeeded. Integrated arbitration produces a coherent answer on the shared conclusion term.

**The substrate-coupling claim is true with caveats.** NAL inference does produce meaningful answers about thread state. The substrate does shape composition. But:
- Order-of-operations matters and must be enforced
- Confidence values must be empirically calibrated, not formula-derived
- Next-step appropriateness requires additional atoms 2h must author

**Three constraints for 2h design that we did not have before:**

1. The composer must process substrate refutations before bridge deductions, OR refutation atoms must target both path and shared terms.
2. Confidence-based retirement and staleness thresholds must be calibrated against actual engine behavior.
3. Next-step appropriateness requires a small library of MeTTa predicates 2h authors as part of its build.

None of these block 2h. All three sharpen its design.

---

## What This Tells Us About the Two Other Proofs

**Proof 2 (multi-hop NAL):** Largely answered by this proof and by substrate_kb's existing documentation. Q1 used composed three-step deductions via revision. Substrate_kb already documents that 4-hop chains lose confidence to ~0.225 while 2-hop chains retain ~0.620 (lines 171-176). We have enough multi-hop evidence to proceed without a separate Proof 2. If we hit a multi-hop limitation during 2h development, we test it then.

**Proof 3 (AtomSpace performance under thread-evidence load):** Still genuinely open. Proof 1 used 16 atoms in the test fixture. 2h in production may accumulate hundreds of thread-evidence atoms across 50 iterations. Whether `match` operations remain fast under that load is unknown and matters for 2h's schema design.

---

## Recommendation

Proceed to Proof 3. Then redraft 2h's build spec incorporating Findings 1-4 above. The redrafted spec will be substantially tighter than the original -- the architectural questions are now answered.
