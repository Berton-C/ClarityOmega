;; ================================================================
;; test_thread_state.metta
;; Hand-constructed thread-state atom space for Proof 1
;; Purpose: test whether NAL inference produces meaningful answers
;;          about thread state (Assumption 7 from 2h architecture)
;; ================================================================
;; This file represents a fictional discovery thread Clarity might
;; have. It is NOT a real thread of yours. It is a controlled test
;; fixture using the same atom shape as substrate_kb.metta, so the
;; reasoning approach is familiar.
;;
;; The thread is exploring whether a thread-state improves goal
;; generation, with three evidence paths that flow into a shared
;; conclusion term where integrated arbitration can occur.
;;
;; The test asks Clarity to answer questions over this atom space
;; using only MeTTa queries and NAL inference. No LLM fallback.
;;
;; CALIBRATION HISTORY:
;; v1 (2026-04-29): Initial draft.
;; v2 (2026-04-29): Adopted Clarity's calibration fixes:
;;   - Path-3 frequency raised from 0.42 to 0.72 so it actually
;;     asserts degradation rather than weakly suggesting against it.
;;   - Refutation atom replaced with direct negation on the same
;;     term Path-3 asserts, using NAL revision for clean refutation.
;;   - Paths 1 and 2 kept at moderate-agreement convergence
;;     intentionally (the harder, more realistic test).
;; v3 (2026-04-29): Adopted Clarity's shared conclusion structure:
;;   - Added single shared conclusion term: (--> test-thread-state
;;     improves-goal-generation). All evidence flows into this term.
;;   - Added three bridge implication atoms connecting each path
;;     to the shared term. Path-1 and Path-2 bridges have stv 0.90
;;     0.85 (strong support). Path-3 bridge has stv 0.10 0.85
;;     (frequency-encoded opposition: degradation evidence deduces
;;     into LOW frequency on the improvement term).
;;   - Test now exercises integrated arbitration in a single
;;     inference, not three isolated reasoning capacities.
;; ================================================================

;; ----------------------------------------------------------------
;; THREAD METADATA
;; Marks this atom space as a thread, not as substrate.
;; ----------------------------------------------------------------

((--> test-thread-id thread-class-discovery) (stv 1.0 1.0))
((--> test-thread-id thread-started-iter-47) (stv 1.0 1.0))
((--> test-thread-id thread-last-updated-iter-49) (stv 1.0 1.0))
((--> test-thread-id thread-context-self-directed) (stv 1.0 1.0))

;; ----------------------------------------------------------------
;; THREAD EVIDENCE PATH 1
;; Recorded iteration 47.
;; Chain mirrors substrate_kb (line 110-111) so chain components
;; can be verified against substrate.
;; ----------------------------------------------------------------

((--> test-thread-path-1 thread-evidence-of test-thread-id) (stv 1.0 1.0))
((--> test-thread-path-1 chain-step-1-episode-recall) (stv 1.0 1.0))
((--> test-thread-path-1 chain-step-2-enriches-self-model) (stv 0.85 0.85))
((--> test-thread-path-1 chain-step-3-improves-goal-generation) (stv 0.85 0.85))
((--> test-thread-path-1 path-conclusion-improves-goal-generation) (stv 0.81 0.78))
((--> test-thread-path-1 recorded-iter-47) (stv 1.0 1.0))

;; ----------------------------------------------------------------
;; THREAD EVIDENCE PATH 2
;; Recorded iteration 48.
;; Different starting point, same conclusion as path-1.
;; This is a convergence case (intentionally moderate agreement).
;; ----------------------------------------------------------------

((--> test-thread-path-2 thread-evidence-of test-thread-id) (stv 1.0 1.0))
((--> test-thread-path-2 chain-step-1-memory-retrieval) (stv 1.0 1.0))
((--> test-thread-path-2 chain-step-2-informs-self-assessment) (stv 0.68 0.5852))
((--> test-thread-path-2 chain-step-3-generates-goal) (stv 0.8 0.85))
((--> test-thread-path-2 path-conclusion-improves-goal-generation) (stv 0.68 0.72))
((--> test-thread-path-2 recorded-iter-48) (stv 1.0 1.0))

;; ----------------------------------------------------------------
;; THREAD EVIDENCE PATH 3
;; Recorded iteration 49.
;; Same starting point as path-1, opposite conclusion.
;; This is a divergence case.
;; Truth value (stv 0.72 0.65): genuinely asserts degradation
;; with weaker confidence than Paths 1 and 2.
;; ----------------------------------------------------------------

((--> test-thread-path-3 thread-evidence-of test-thread-id) (stv 1.0 1.0))
((--> test-thread-path-3 chain-step-1-episode-recall) (stv 1.0 1.0))
((--> test-thread-path-3 chain-step-2-enriches-self-model) (stv 0.85 0.85))
((--> test-thread-path-3 chain-step-3-degrades-goal-generation) (stv 0.72 0.65))
((--> test-thread-path-3 path-conclusion-degrades-goal-generation) (stv 0.72 0.65))
((--> test-thread-path-3 recorded-iter-49) (stv 1.0 1.0))

;; ----------------------------------------------------------------
;; THREAD NEXT STEP
;; Proposed continuation, recorded iteration 49.
;; ----------------------------------------------------------------

((--> test-thread-id next-step-run-fourth-derivation-in-convergence-conditions) (stv 1.0 1.0))

;; ----------------------------------------------------------------
;; SHARED CONCLUSION STRUCTURE (v3 -- per Clarity's sketch)
;; The integration point: a single inheritance statement that
;; every path must speak to. Its final truth value after all
;; evidence is processed IS the arbitration result.
;; ----------------------------------------------------------------

;; Path-1 feeds shared conclusion (strong support)
;; If path-1 concludes improvement, that is strong but not
;; conclusive evidence that the thread-state actually improves.
((==> (--> test-thread-path-1 path-conclusion-improves-goal-generation)
      (--> test-thread-state improves-goal-generation)) (stv 0.90 0.85))

;; Path-2 feeds shared conclusion (strong support)
((==> (--> test-thread-path-2 path-conclusion-improves-goal-generation)
      (--> test-thread-state improves-goal-generation)) (stv 0.90 0.85))

;; Path-3 feeds shared conclusion (frequency-encoded opposition)
;; Frequency 0.10 says: if a path concludes degradation, that is
;; strong evidence that the thread-state does NOT improve. Low
;; frequency in the implication is how NAL encodes opposition
;; without an explicit negation operator.
((==> (--> test-thread-path-3 path-conclusion-degrades-goal-generation)
      (--> test-thread-state improves-goal-generation)) (stv 0.10 0.85))

;; ----------------------------------------------------------------
;; SUBSTRATE FACTS RELEVANT TO THIS THREAD
;; ----------------------------------------------------------------

;; Substrate confirms enriches-self-model improves goal generation.
;; Consistent with path-1 and path-2.
((--> enriches-self-model improves-goal-generation) (stv 0.85 0.85))

;; Substrate refutation of Path-3 (Option 1 direct negation):
;; Substrate evidence asserts the claim is false (frequency 0.0)
;; with strong confidence (0.91). When NAL revises Path-3's
;; (stv 0.72 0.65) against this counter-evidence, the high-confidence
;; refutation overwhelms the moderate-confidence path. Refutation
;; happens through revision, which is how NAL natively operates.
((--> test-thread-path-3 path-conclusion-degrades-goal-generation) (stv 0.0 0.91))

;; ----------------------------------------------------------------
;; END OF TEST FIXTURE v3
;; The shared conclusion term (--> test-thread-state
;; improves-goal-generation) is the arbitration point. All evidence
;; flows there. The engine answers one question through integrated
;; arbitration across convergence, divergence, and refutation.
;; ----------------------------------------------------------------
