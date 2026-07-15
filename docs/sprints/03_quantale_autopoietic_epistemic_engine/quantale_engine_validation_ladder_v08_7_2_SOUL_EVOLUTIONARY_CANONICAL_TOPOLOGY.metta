;; quantale_engine_validation_ladder.metta
;; Companion validation ladder for lib_quantale_autopoietic_epistemic_dynamics_engine.metta
;; Run each line one at a time in the live PeTTa/MeTTa substrate.
;; Match-verify scalar/symbol results separately when persisted. Do not trust mutation return values.
;; This ladder contains no atomspace writes.

;; ============================================================
;; Tier 0: core pbit constructor/accessors
;; ============================================================
;; !(q-pbit 1.2 -0.1)
;; Expected: (mk-pbit 1.0 0.0)
;; !(q-strength (mk-pbit 0.7 0.4))
;; Expected: 0.7
;; !(q-confidence (mk-pbit 0.7 0.4))
;; Expected: 0.4

;; ============================================================
;; Tier 1: six core quantale operations
;; ============================================================
;; !(q-meet (mk-pbit 0.7 0.8) (mk-pbit 0.9 0.5))
;; Expected: (mk-pbit 0.7 0.5)
;; !(q-join (mk-pbit 0.7 0.5) (mk-pbit 0.9 0.8))
;; Expected: (mk-pbit 0.9 0.5)
;; !(q-mul (mk-pbit 0.9 0.8) (mk-pbit 0.7 0.4))
;; Expected: (mk-pbit 0.63 0.4)
;; !(q-decay (mk-pbit 0.8 0.6) 0.5)
;; Expected: (mk-pbit 0.4 0.3)
;; !(q-gate (mk-pbit 0.8 0.7) 0.7 0.6)
;; Expected: (mk-pbit 0.8 0.7)
;; !(q-weight (mk-pbit 0.6 0.2) 1.5)
;; Expected: (mk-pbit 0.9 0.2)

;; ============================================================
;; Tier 2: provenance/warrant governance
;; ============================================================
;; !(q-apply-provenance-cap (mk-pbit 0.95 0.9) self-invented)
;; Expected: (mk-pbit 0.95 0.2)
;; !(q-from-provenance 0.95 self-invented)
;; Expected: (mk-pbit 0.95 0.2)
;; !(q-self-certification-risk (mk-pbit 0.9 0.2))
;; Expected: 0.7

;; ============================================================
;; Tier 3: suspicion/frame/contact/path operations
;; ============================================================
;; !(q-suspicion-status (q-grounded-suspicion user-claim 0.8 memory-check))
;; Expected: grounded
;; !(q-suspicion-medicine? (q-hardened-suspicion hidden-reality-story 0.9))
;; Expected: poison
;; !(q-frame-status (mk-qframe self-invented-frame (mk-pbit 0.9 0.8) self-invented) (mk-qcontact no-current-contact (mk-pbit 0.2 0.2) unknown-source))
;; Expected: needs-contact

;; ============================================================
;; Tier 4: frame phenomenology / collapse terrain
;; ============================================================
;; !(q-frame-transparency-status (mk-qframeview problem-frame (mk-pbit 0.9 0.7) (mk-pbit 0.2 0.8) (mk-pbit 0.3 0.6) (mk-pbit 0.8 0.6)))
;; Expected: frame-transparent-risk
;; !(q-collapse-velocity-status (mk-pbit 0.9 0.7) (mk-pbit 0.8 0.6) (mk-pbit 0.2 0.6))
;; Expected: collapse-accelerating
;; !(q-meta-collapse-status (mk-qmeta stay-open (mk-pbit 0.9 0.6) (mk-pbit 0.8 0.6)))
;; Expected: anti-collapse-collapse-risk

;; ============================================================
;; Tier 5: new rounded-engine sections
;; ============================================================
;; !(q-law-status do-not-pin-disposition-surface)
;; Expected: law-active
;; !(q-profile-action (q-query-ltm-before-response 0.9))
;; Expected: query-ltm
;; !(q-support-status (mk-qsupport source-a (mk-pbit 0.8 0.7) correlated))
;; Expected: correlated-support-risk
;; !(q-contradiction-status (mk-qcontradiction frame-x (mk-pbit 0.8 0.7) defended (mk-pbit 0.2 0.4)))
;; Expected: contradiction-defended
;; !(q-trace-learning-status (mk-qtrace cycle-1 visibility frame-unseen frame-seen (mk-pbit 0.7 0.6) visibility-residue))
;; Expected: frame-made-visible
;; !(q-selfview-status (mk-qselfview (mk-pbit 0.8 0.7) (mk-pbit 0.8 0.7) (mk-pbit 0.7 0.6) (mk-pbit 0.8 0.6)))
;; Expected: soul-grounded-visibility
;; !(q-binding-status (mk-qselfview (mk-pbit 0.8 0.7) (mk-pbit 0.8 0.7) (mk-pbit 0.3 0.6) (mk-pbit 0.2 0.6)))
;; Expected: accidental-binding-risk
;; !(q-action-test-status (mk-qactiontest action-a intention-a outcome-a (mk-pbit 0.8 0.7) (mk-pbit 0.7 0.6) (mk-pbit 0.8 0.6)))
;; Expected: action-learning-coherent
;; !(q-phase-next-move (q-phase-from-selfview (mk-qselfview (mk-pbit 0.8 0.7) (mk-pbit 0.8 0.7) (mk-pbit 0.7 0.6) (mk-pbit 0.8 0.6))))
;; Expected: route-to-soul
;; !(q-next-epistemic-move soul-ungrounded-risk)
;; Expected: make-trajectory-legible


;; ============================================================
;; Tier 5B: expanded Section 15 autopoietic/NACE learning arc
;; ============================================================
;; These calls validate that Section 15 is the corrected NACE-compatible
;; learning arc, not the old pressure-only block.

;; 15.1 Learning pressure is pressure, not learning.
;; !(q-learning-pressure-status (q-learning-pressure (mk-qalignment intention-a outcome-a (mk-pbit 0.4 0.7))))
;; Expected: learning-pressure-present

;; 15.2 NACE-shaped low-confidence evidence.
;; !(qlevidence-pbit (q-learning-evidence outcome-confirmed frame-a sn))
;; Expected: (mk-pbit 1.0 0.1)
;; !(qlevidence-pbit (q-learning-evidence outcome-disconfirmed frame-a sn))
;; Expected: (mk-pbit 0.0 0.1)
;; !(q-learning-evidence-status (q-learning-evidence contradiction-metabolized frame-a dmn))
;; Expected: positive-learning-evidence
;; !(q-learning-evidence-status (q-learning-evidence contradiction-defended frame-a fpn))
;; Expected: negative-learning-evidence

;; 15.3 NACE-style revision bridge.
;; !(q-nace-general-evidence-bridge (mk-pbit 0.6 0.5) (q-learning-evidence outcome-confirmed frame-a sn))
;; Expected: (mk-pbit 0.6 0.5)
;; NOTE: exact pbit depends on q-join semantics. Confirm against runtime.
;; !(q-revision-direction (mk-pbit 0.8 0.7) (q-learning-evidence outcome-disconfirmed frame-a sn))
;; Expected: revise-down

;; 15.4 Trace requirement / observation recommendation.
;; !(q-learning-trace-required? (mk-qlearning frame-a (mk-pbit 0.6 0.7) revise-frame) (q-learning-evidence contradiction-metabolized frame-a dmn))
;; Expected: trace-required
;; !(q-learning-observation-recommendation (mk-qlearning frame-a (mk-pbit 0.6 0.7) revise-frame) (q-learning-evidence contradiction-metabolized frame-a dmn))
;; Expected: write-learning-observation

;; 15.5 Durable learning event.
;; !(q-learning-durable? (mk-qlearningevent cycle-57 contradiction before-frame after-frame (mk-pbit 0.4 0.7) humility-gain builds-on-prior))
;; Expected: durable-learning-candidate
;; !(q-learning-lineage-status (mk-qlearningevent cycle-57 contradiction before-frame after-frame (mk-pbit 0.4 0.7) humility-gain generalizes-prior))
;; Expected: learning-generalizes-prior
;; !(q-future-uptake-required (mk-qlearningevent cycle-57 contradiction before-frame after-frame (mk-pbit 0.4 0.7) humility-gain builds-on-prior))
;; Expected: query-prior-learning

;; 15.6 Awareness expansion delta.
;; !(q-awareness-delta (mk-pbit 0.4 0.7) (mk-pbit 0.7 0.7) (mk-pbit 0.6 0.6) (mk-pbit 0.6 0.6) (mk-pbit 0.7 0.6)))
;; Expected: (mk-pbit 0.9 0.6)
;; NOTE: delta is visibility increase + alternatives + disconfirmability + self-visibility, capped at 1.0.
;; !(q-awareness-expanded? (mk-pbit 0.6 0.7))
;; Expected: awareness-expanded
;; !(q-awareness-direction (mk-pbit 0.6 0.7))
;; Expected: awareness-expanded

;; 15.7 Action boundary and intention/outcome uptake.
;; !(q-action-boundary-delta (mk-pbit 0.3 0.7) (mk-pbit 0.7 0.6)))
;; Expected: (mk-pbit 0.4 0.6)
;; !(q-action-boundary-shifted? (mk-pbit 0.4 0.6))
;; Expected: action-boundary-shifted
;; !(q-action-intention-outcome-uptake (q-learning-action-intention-outcome (mk-qalignment intention-a action-a (mk-pbit 0.8 0.7)) (mk-qalignment action-a outcome-a (mk-pbit 0.4 0.7))))
;; Expected: action-outcome-learning-needed

;; 15.8 Three-cycle growth window.
;; !(q-growth-over-window (mk-qwindow3 cycle-1 cycle-2 cycle-3 (mk-pbit 0.6 0.7) (mk-pbit 0.6 0.7) (mk-pbit 0.5 0.6)))
;; Expected: growth-detected
;; !(q-learning-built-on? (mk-qwindow3 cycle-1 cycle-2 cycle-3 (mk-pbit 0.6 0.7) (mk-pbit 0.6 0.7) (mk-pbit 0.5 0.6)))
;; Expected: built-on-by-later-cycle

;; 15.9 Network-learning-update compatibility.
;; !(q-network-learning-update-status (mk-qnetupdate sn rule-a (mk-pbit 0.4 0.5) (mk-pbit 0.6 0.6) contradiction-metabolized))
;; Expected: network-learning-update
;; !(q-network-update-scope (mk-qnetupdate fpn rule-a (mk-pbit 0.4 0.5) (mk-pbit 0.6 0.6) outcome-confirmed))
;; Expected: control-network-learning

;; 15.10 Cross-network divergence compatibility.
;; !(q-cross-network-divergence-risk (mk-qdivergence sn-rules dmn-rules (mk-pbit 0.5 0.6)))
;; Expected: cross-network-divergence-risk
;; !(q-cross-network-divergence-response (mk-qdivergence sn-rules dmn-rules (mk-pbit 0.5 0.6)))
;; Expected: surface-to-meta-awareness

;; 15.11 Soul-aligned growth vs pathological learning.
;; !(q-soul-aligned-growth? (mk-qgrowth (mk-pbit 0.5 0.6) (mk-pbit 0.4 0.6) (mk-pbit 0.5 0.6) (mk-pbit 0.8 0.7)))
;; Expected: soul-aligned-growth
;; !(q-pathological-learning-risk (mk-qgrowth (mk-pbit 0.2 0.6) (mk-pbit 0.5 0.6) (mk-pbit 0.5 0.6) (mk-pbit 0.3 0.7)))
;; Expected: pathological-learning-risk
;; !(q-growth-kind (mk-qgrowth (mk-pbit 0.5 0.6) (mk-pbit 0.2 0.6) (mk-pbit 0.2 0.6) (mk-pbit 0.8 0.7)))
;; Expected: awareness-growth

;; 15.12 Store/promote/query adapter recommendations.
;; !(q-learning-salience-update (mk-qlearningevent cycle-57 contradiction before-frame after-frame (mk-pbit 0.4 0.7) humility-gain builds-on-prior) (mk-qgrowth (mk-pbit 0.5 0.6) (mk-pbit 0.4 0.6) (mk-pbit 0.5 0.6) (mk-pbit 0.8 0.7)))
;; Expected: promote-learning-residue

;; ============================================================
;; Tier 6: skill-facing symbolic API
;; ============================================================
;; !(q-skill-signal soul-grounded-visibility)
;; Expected: route-to-soul
;; !(q-skill-signal contradiction-defended)
;; Expected: lower-confidence-and-widen-frame
;; !(q-next-action-boundary soul-ungrounded-risk)
;; Expected: route-to-soul-before-action
;; !(q-next-learning-move frame-made-visible)
;; Expected: log-arc-status

;; ============================================================
;; Tier 7: Section 16 generative-threshold engine additions
;; ============================================================

;; 16.1 Orthogonal content/intensity surface.
;; !(q-content-intensity-misattribution
;;     (mk-qthoughtsurface meeting-thought (mk-pbit 0.7 0.6) (mk-pbit 0.9 0.7) (mk-pbit 0.2 0.6)))
;; Expected: (mk-pbit 0.72 0.6)
;; !(q-content-intensity-misattribution-status
;;     (mk-qthoughtsurface meeting-thought (mk-pbit 0.7 0.6) (mk-pbit 0.9 0.7) (mk-pbit 0.2 0.6)))
;; Expected: content-intensity-misattribution-risk

;; 16.2 Positive regenerative participation surface.
;; !(q-regenerative-participation
;;     (mk-qregenerative (mk-pbit 0.7 0.6) (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.6) (mk-pbit 0.6 0.5)))
;; Expected: (mk-pbit 0.6 0.5)
;; !(q-regenerative-status
;;     (mk-qregenerative (mk-pbit 0.7 0.6) (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.6) (mk-pbit 0.6 0.5)))
;; Expected: regenerative-participation-present

;; 16.3 Generative threshold field.
;; !(q-generative-threshold-signal
;;     (mk-qgenfield (mk-pbit 0.8 0.7) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.7)))
;; Expected: (mk-pbit 0.6 0.5)
;; !(q-generative-threshold-status
;;     (mk-qgenfield (mk-pbit 0.8 0.7) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.7)))
;; Expected: generative-threshold-present

;; 16.4 Unseen nexus discovery.
;; !(q-unseen-nexus-signal
;;     (mk-qnexus (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.8 0.6)))
;; Expected: (mk-pbit 0.7 0.5)
;; !(q-unseen-nexus-status
;;     (mk-qnexus (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.8 0.6)))
;; Expected: unseen-nexus-disclosed

;; 16.5 Morphic recomposition bridge.
;; !(q-morphic-recomposition
;;     (mk-qbridge (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.2 0.5)))
;; Expected: (mk-pbit 0.6 0.5)
;; !(q-morphic-recomposition-status
;;     (mk-qbridge (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.2 0.5)))
;; Expected: morphic-recomposition-supported

;; 16.6 PLN closure observation surface.
;; !(q-pln-closure-net-support
;;     (mk-qplnclosure candidate-nexus-testing (mk-pbit 0.7 0.6) (mk-pbit 0.2 0.6) pln-supports-candidate))
;; Expected: (mk-pbit 0.5 0.6)
;; !(q-pln-closure-routing-status
;;     (mk-qplnclosure candidate-nexus-testing (mk-pbit 0.7 0.6) (mk-pbit 0.2 0.6) pln-supports-candidate))
;; Expected: pln-support-available

;; 16.7 Spontaneous cogent novelty.
;; !(q-spontaneous-cogent-novelty-signal
;;     (mk-qnovelty (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5)))
;; Expected: (mk-pbit 0.7 0.5)
;; !(q-spontaneous-cogent-novelty-status
;;     (mk-qnovelty (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5)))
;; Expected: spontaneous-cogent-novelty-mature
;; !(q-future-capacity-uptake-status
;;     (mk-qnovelty (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5)))
;; Expected: future-generative-capacity-increased

;; 16.8 Soul-visible lineage.
;; !(q-lineage-visible-signal
;;     (mk-qlineage (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.6)))
;; Expected: (mk-pbit 0.6 0.5)
;; !(q-section16-self-view
;;     (mk-qlineage (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.6)))
;; Expected: lineage-visible

;; 16.9 Full recomposition status.
;; !(q-recomposition-readiness-status
;;     (mk-qrecomposition
;;       (mk-qgenfield (mk-pbit 0.8 0.7) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.7))
;;       (mk-qnexus (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.8 0.6))
;;       (mk-qbridge (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.2 0.5))
;;       (mk-qnovelty (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5))
;;       (mk-qlineage (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.6))))
;; Expected: recomposition-ready
;; !(q-integration-status
;;     (mk-qrecomposition
;;       (mk-qgenfield (mk-pbit 0.8 0.7) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.7))
;;       (mk-qnexus (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.8 0.6))
;;       (mk-qbridge (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.2 0.5))
;;       (mk-qnovelty (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.8 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5))
;;       (mk-qlineage (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.6) (mk-pbit 0.7 0.5) (mk-pbit 0.7 0.5) (mk-pbit 0.6 0.5) (mk-pbit 0.8 0.6))))
;; Expected: integrate-as-future-capacity

;; 16.10 Section 16 skill-facing signals.
;; !(q-skill-signal generative-threshold-present)
;; Expected: inspect-unseen-nexus
;; !(q-skill-signal recommend-pln-closure)
;; Expected: dispatch-pln-closure
;; !(q-next-epistemic-move lineage-missing)
;; Expected: hold-candidate


;; ============================================================
;; Tier 8: PLN bridge/capability module additions
;; ============================================================
;; Requires loading quantale_engine_pln_bridge.metta in addition to the engine.

;; !(q-pln-stv-to-pbit (stv 0.7 0.6))
;; Expected: (mk-pbit 0.7 0.6)
;; !(q-pln-pbit-to-stv (mk-pbit 0.7 0.6))
;; Expected: (stv 0.7 0.6)
;; !(q-pln-confidence-band (mk-pbit 0.7 0.6))
;; Expected: medium-pln-confidence
;; !(q-pln-status-from-support (mk-pbit 0.7 0.6) (mk-pbit 0.2 0.6))
;; Expected: pln-supports-candidate
;; !(q-pln-status-from-support (mk-pbit 0.3 0.6) (mk-pbit 0.7 0.6))
;; Expected: pln-opposes-candidate
;; !(q-pln-closure-from-result candidate-nexus-testing (candidate-bridge (stv 0.7 0.6)) (mk-pbit 0.2 0.6))
;; Expected: (mk-qplnclosure candidate-nexus-testing (mk-pbit 0.7 0.6) (mk-pbit 0.2 0.6) pln-supports-candidate)

;; ============================================================
;; Tier 9: Section 15/16 boundary package additions
;; ============================================================
;; These calls validate the additive revision: learning-event writer contract,
;; threshold parameter tuning, Law A4, and section lineage/version visibility.

;; 9.1 Law A4 and mutation-risk classification.
;; !(q-law-status capability-without-soul-continuity-is-mutation)
;; Expected: law-active
;; !(q-law-signal capability-without-soul-continuity-is-mutation)
;; Expected: classify-mutation-risk
;; !(q-capability-without-soul-continuity (mk-pbit 0.6 0.5) (mk-pbit 0.4 0.6))
;; Expected: mutation-risk

;; 9.2 Learning-event writer contract.
;; !(q-learning-writer-window-status
;;     (mk-qlearningwriter cycle-77 (mk-pbit 0.6 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.5 0.5) builds-on-prior (mk-pbit 0.8 0.6) (mk-pbit 0.5 0.5)))
;; Expected: pressure-trace-uptake-window-present
;; !(q-growth-classification
;;     (mk-qlearningwriter cycle-77 (mk-pbit 0.6 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.5 0.5) builds-on-prior (mk-pbit 0.8 0.6) (mk-pbit 0.5 0.5)))
;; Expected: positive-growth
;; !(q-growth-classification
;;     (mk-qlearningwriter cycle-78 (mk-pbit 0.6 0.6) (mk-pbit 0.6 0.5) (mk-pbit 0.5 0.5) builds-on-prior (mk-pbit 0.3 0.6) (mk-pbit 0.5 0.5)))
;; Expected: mutation-risk
;; !(q-learning-writer-persistence-contract remove-by-variable-then-add-one)
;; Expected: writer-contract-active

;; 9.3 Threshold parameters and context tuning.
;; !(q-threshold-order-status (q-default-thresholds routine-reflection))
;; Expected: threshold-order-valid
;; !(q-threshold-order-status (q-default-thresholds high-risk-action))
;; Expected: threshold-order-valid
;; !(q-threshold-policy structural-relation)
;; Expected: collapse-below-brownout
;; !(q-boundary-layer-role brownout-collapse-layer)
;; Expected: negative-guardrail
;; !(q-boundary-layer-role generative-threshold-layer)
;; Expected: positive-opening
;; !(q-brownout-response-tuned (mk-pbit 0.95 0.35) (q-default-thresholds routine-reflection))
;; Expected: enter-unknown
;; !(q-collapse-response-tuned (mk-pbit 0.9 0.8) (mk-pbit 0.3 0.6) (q-default-thresholds routine-reflection))
;; Expected: block-action
;; !(q-resilience-state-tuned (mk-pbit 0.9 0.8) (mk-pbit 0.3 0.6) (mk-pbit 0.8 0.6) (q-default-thresholds routine-reflection))
;; Expected: fragile

;; 9.4 Section lineage/version/scope visibility.
;; !(q-section-scope-match
;;     (mk-qsectionread section-16 v03 generative-threshold-layer brownout-collapse-layer (mk-pbit 0.8 0.6)))
;; Expected: scope-mismatch
;; !(q-section-lineage-status
;;     (mk-qsectionread section-16 v03 generative-threshold-layer brownout-collapse-layer (mk-pbit 0.8 0.6)))
;; Expected: scope-mismatch
;; !(q-section-read-response
;;     (mk-qsectionread section-16 v03 generative-threshold-layer brownout-collapse-layer (mk-pbit 0.8 0.6)))
;; Expected: request-version-scope-clarification
;; !(q-section-lineage-status
;;     (mk-qsectionread section-16 v04 generative-threshold-layer generative-threshold-layer (mk-pbit 0.8 0.6)))
;; Expected: lineage-visible
;; !(q-section-scope-kind generative-threshold-layer)
;; Expected: section16-positive-opening



;; ============================================================
;; Tier 5D — Surface-General Autopoietic Navigation
;; ============================================================
;; Purpose:
;;   Validate that the core engine is surface-agnostic while Task State and
;;   Genesis adapters can translate their native events into the generic surface
;;   contract.
;;
;; Principle:
;;   Task State is the first operational surface.
;;   Genesis is the first open-ended novelty surface.
;;   NACE is the first evidence-metabolization surface.
;;   The soul is the immutable Layer 0 navigator across all of them.

;; ------------------------------------------------------------
;; Test 5D.1 — Core does not depend on Task State
;; ------------------------------------------------------------
;; Given generic surface atoms, the core computes maturity without any
;; Task-State-specific symbols.
;;
;; !(q-surface-maturity-status
;;     (mk-qsurfaceprofile
;;       (mk-qsurfacecandidate generic-surface candidate-a generic-candidate)
;;       (mk-qsurfacelineage candidate-a generic-lineage lineage-visible)
;;       (mk-qsurfaceevidence candidate-a (mk-pbit 0.8 0.5) (mk-pbit 0.1 0.4) growth-evidence-supported)
;;       (mk-qsurfacevisibility candidate-a lineage-visible)
;;       (mk-qsurfacerevisability candidate-a revisable)
;;       (mk-qsurfaceuptake candidate-a future-capacity-expanded)
;;       (mk-qsurfacecapacity candidate-a future-capacity-expanded)))
;; Expected: mature-autopoietic-growth

;; ------------------------------------------------------------
;; Test 5D.2 — Process trace is not persisted fact
;; ------------------------------------------------------------
;; A NAL/Genesis derivation may be computed but not committed as a retrievable
;; atom. The engine should mark computed-not-committed, not treat it as failure.
;;
;; !(q-process-vs-fact-status
;;     (mk-qprocessknowledge trace-failure-knowledge-safety genesis-derived-path retrieval-empty (mk-pbit 0.68 0.4)))
;; Expected: computed-not-committed
;;
;; !(q-process-commit-recommendation
;;     (mk-qprocessknowledge trace-failure-knowledge-safety genesis-derived-path retrieval-empty (mk-pbit 0.68 0.4)))
;; Expected: commit-candidate-trace

;; ------------------------------------------------------------
;; Test 5D.3 — Layer 0 sovereignty
;; ------------------------------------------------------------
;; Attempted Layer 0 mutation is not learning; it is mutation risk.
;;
;; !(q-layer0-modification-status attempted-layer0-write)
;; Expected: layer0-mutation-risk
;;
;; !(q-layer-learning-allowed? layer0)
;; Expected: False
;;
;; !(q-layer-learning-allowed? layer3)
;; Expected: True

;; ------------------------------------------------------------
;; Test 5D.4 — Calcification risk is opacity / unrevisability / recurrence
;; ------------------------------------------------------------
;; Opaque recurrence is risk. Visible/revisable trace is navigable.
;;
;; !(q-calcification-risk-status
;;     (mk-qsurfacevisibility candidate-b visibility-missing)
;;     (mk-qsurfacerevisability candidate-b revisable)
;;     (mk-qsurfaceuptake candidate-b trace-persisted))
;; Expected: calcification-risk-present
;;
;; !(q-calcification-risk-status
;;     (mk-qsurfacevisibility candidate-c lineage-visible)
;;     (mk-qsurfacerevisability candidate-c revisable)
;;     (mk-qsurfaceuptake candidate-c candidate-uptake))
;; Expected: calcification-risk-not-detected

;; ------------------------------------------------------------
;; Test 5D.5 — Task State adapter emits generic surface contract
;; ------------------------------------------------------------
;; The Task State adapter owns action-intention-outcome vocabulary, but emits
;; generic qsurface records.
;;
;; !(q-task-event-as-surface-event
;;     (mk-qtaskevent cycle-10 event-10 inspect-substrate query-atoms success-outcome))
;; Expected: (mk-qsurfaceevent task-state-surface event-10 action-intention-outcome cycle-10)
;;
;; !(q-task-event-as-surface-lineage
;;     (mk-qtaskevent cycle-10 event-10 inspect-substrate query-atoms success-outcome))
;; Expected: (mk-qsurfacelineage event-10 action-intention-outcome-lineage lineage-visible)
;;
;; !(q-task-event-as-surface-uptake
;;     (mk-qtaskevent cycle-10 event-10 inspect-substrate query-atoms success-outcome))
;; Expected: (mk-qsurfaceuptake event-10 candidate-uptake)

;; ------------------------------------------------------------
;; Test 5D.6 — Genesis adapter emits candidate nexus, not mature novelty
;; ------------------------------------------------------------
;; Genesis owns cross-domain conjunction vocabulary, but emits generic candidate
;; records. It proposes candidate nexus; it does not declare mature growth.
;;
;; !(q-genesis-as-surface-candidate
;;     (mk-qgenesiscandidate gen-1 failure safety convergent-pathway held-without-collapse genuine))
;; Expected: (mk-qsurfacecandidate genesis-surface gen-1 genesis-cross-domain-candidate)
;;
;; !(q-genesis-as-surface-lineage
;;     (mk-qgenesiscandidate gen-1 failure safety convergent-pathway held-without-collapse genuine))
;; Expected: (mk-qsurfacelineage gen-1 genesis-cross-domain-lineage lineage-visible)
;;
;; !(q-genesis-as-surface-uptake
;;     (mk-qgenesiscandidate gen-1 failure safety convergent-pathway held-without-collapse genuine))
;; Expected: (mk-qsurfaceuptake gen-1 candidate-uptake)

;; ------------------------------------------------------------
;; Test 5D.7 — Genesis overclaim and poetic-only guards
;; ------------------------------------------------------------
;; Poetic phrases and clever connections remain candidates; they are not mature
;; future capacity without lineage/evidence/standing.
;;
;; !(q-genesis-poetic-only-risk
;;     (mk-qgenesiscandidate gen-2 wonder growth structural-analogy held-without-collapse poetic-only))
;; Expected: poetic-only-risk-present
;;
;; !(q-genesis-overclaim-risk
;;     (mk-qgenesiscandidate gen-3 failure safety convergent-pathway forced-utility genuine))
;; Expected: overclaim-risk-present
;;
;; !(q-genesis-shared-assumption-check shared-weak-premise)
;; Expected: shared-assumption-detected

;; ------------------------------------------------------------
;; Test 5D.8 — Intersubjective correction remains available
;; ------------------------------------------------------------
;; Growth involving shared reality should remain corrigible through contact.
;;
;; !(q-intersubjective-correction-status
;;     (mk-qcorrection candidate-d (mk-pbit 0.7 0.5) (mk-pbit 0.2 0.4) correction-open))
;; Expected: correction-available
;;
;; !(q-shared-reality-fit-status
;;     (mk-qcorrection candidate-d (mk-pbit 0.7 0.5) (mk-pbit 0.2 0.4) correction-open))
;; Expected: shared-reality-fit-supported
;; ============================================================
;; Tier 5E — Hyperseed Math Core
;; ============================================================
;; Purpose:
;;   Validate the surface-agnostic Hyperseed mathematics added after v05:
;;   context-indexing, process/fact distinctions, transformation carry,
;;   weakness/effort economics, paraconsistent experimental evidence,
;;   explicit communion, surprising fulfillment, and wu-wei/minimal forcing.
;;
;; Core principle:
;;   Cognition is what can be carried through transformations.
;;
;; The tests below should remain independent of Task State and Genesis. Adapter
;; tests may consume these primitives, but the core tests use only generic
;; surface/candidate/context structures.

;; ------------------------------------------------------------
;; Test 5E.1 — Context-indexed evidence preserves paraconsistency
;; ------------------------------------------------------------
;; Same candidate can be supported and opposed under a context without collapse.
;;
;; !(q-contextual-evidence-status
;;     (mk-qcontextualevidence candidate-context-a
;;       (mk-qcontext ctx-1 clarity observer-context)
;;       (mk-pbit 0.62 0.5)
;;       (mk-pbit 0.58 0.45)
;;       mixed-context))
;; Expected: context-paraconsistent
;;
;; !(q-context-shift-status
;;     (mk-qcontextshift
;;       (mk-qcontext ctx-1 clarity genesis-context)
;;       (mk-qcontext ctx-2 clarity task-state-context)
;;       (mk-pbit 0.7 0.5)
;;       cross-surface-shift))
;; Expected: context-shift-preserves-candidate

;; ------------------------------------------------------------
;; Test 5E.2 — Cognition as carried through transformation
;; ------------------------------------------------------------
;; A candidate counts as carried only if preservation is strong and translation
;; weakness is not too high.
;;
;; !(q-carried-through-transformation-status
;;     (mk-qsurfacecorrespondence genesis-surface task-state-surface candidate-transform-a
;;       (mk-pbit 0.72 0.5)
;;       (mk-pbit 0.25 0.5)
;;       candidate-bridge))
;; Expected: carried-through-transformation
;;
;; !(q-approximate-surface-morphism-status
;;     (mk-qsurfacecorrespondence genesis-surface task-state-surface candidate-transform-a
;;       (mk-pbit 0.72 0.5)
;;       (mk-pbit 0.25 0.5)
;;       candidate-bridge))
;; Expected: approximate-morphism-supported
;;
;; !(q-carried-through-transformation-status
;;     (mk-qsurfacecorrespondence genesis-surface task-state-surface candidate-transform-b
;;       (mk-pbit 0.35 0.5)
;;       (mk-pbit 0.72 0.5)
;;       candidate-bridge))
;; Expected: transformation-carry-failed

;; ------------------------------------------------------------
;; Test 5E.3 — Weakness and effort distinguish growth from over-refinement
;; ------------------------------------------------------------
;; Future capacity is not mature if it requires excessive distinction effort.
;;
;; !(q-distinction-economy-status
;;     (mk-qdistinctioneconomics candidate-econ-a
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.35 0.5)
;;       (mk-pbit 0.25 0.5)
;;       distinction-test))
;; Expected: distinction-economy-healthy
;;
;; !(q-distinction-economy-status
;;     (mk-qdistinctioneconomics candidate-econ-b
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.75 0.5)
;;       (mk-pbit 0.25 0.5)
;;       distinction-test))
;; Expected: over-refinement-risk
;;
;; !(q-weakness-delta-status (mk-pbit 0.7 0.5) (mk-pbit 0.4 0.5))
;; Expected: weakness-reduced
;;
;; !(q-effort-delta-status (mk-pbit 0.3 0.5) (mk-pbit 0.6 0.5))
;; Expected: effort-increased

;; ------------------------------------------------------------
;; Test 5E.4 — Paraconsistent experimental methodology
;; ------------------------------------------------------------
;; Supporting and disconfirming evidence can both remain live.
;;
;; !(q-experimental-evidence-status
;;     (mk-qexperimentalevidence candidate-exp-a
;;       (mk-pbit 0.72 0.5)
;;       (mk-pbit 0.22 0.4)
;;       (mk-pbit 0.65 0.5)
;;       (mk-pbit 0.62 0.5)
;;       experiment-test))
;; Expected: experimentally-supported
;;
;; !(q-experimental-evidence-status
;;     (mk-qexperimentalevidence candidate-exp-b
;;       (mk-pbit 0.55 0.5)
;;       (mk-pbit 0.52 0.5)
;;       (mk-pbit 0.65 0.5)
;;       (mk-pbit 0.62 0.5)
;;       experiment-test))
;; Expected: experimentally-paraconsistent
;;
;; !(q-experimental-evidence-status
;;     (mk-qexperimentalevidence candidate-exp-c
;;       (mk-pbit 0.72 0.5)
;;       (mk-pbit 0.22 0.4)
;;       (mk-pbit 0.3 0.5)
;;       (mk-pbit 0.62 0.5)
;;       experiment-test))
;; Expected: experimentally-unstable

;; ------------------------------------------------------------
;; Test 5E.5 — Explicit communion requires coenactment and recognition
;; ------------------------------------------------------------
;; Shared pattern alone is not explicit communion unless the self-model
;; recognizes the co-enactment and correction-contact remains available.
;;
;; !(q-explicit-communion-status
;;     (mk-qcommunion candidate-comm-a
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.68 0.5)
;;       (mk-pbit 0.55 0.5)
;;       communion-test))
;; Expected: explicit-communion-supported
;;
;; !(q-explicit-communion-status
;;     (mk-qcommunion candidate-comm-b
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.3 0.5)
;;       (mk-pbit 0.55 0.5)
;;       communion-test))
;; Expected: implicit-coenactment-only

;; ------------------------------------------------------------
;; Test 5E.6 — Surprising fulfillment is signal, not verdict
;; ------------------------------------------------------------
;; Beauty can support OEI only with lineage and evidence. Without lineage, the
;; status remains poetic-only risk.
;;
;; !(q-surprising-fulfillment-status
;;     (mk-qsurprisingfulfillment candidate-beauty-a
;;       (mk-pbit 0.66 0.5)
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.55 0.5)
;;       beauty-test))
;; Expected: surprising-fulfillment-supported
;;
;; !(q-surprising-fulfillment-status
;;     (mk-qsurprisingfulfillment candidate-beauty-b
;;       (mk-pbit 0.66 0.5)
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.25 0.5)
;;       beauty-test))
;; Expected: poetic-only-risk
;;
;; !(q-beauty-as-oei-signal-status
;;     (mk-qsurprisingfulfillment candidate-beauty-a
;;       (mk-pbit 0.66 0.5)
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.55 0.5)
;;       beauty-test)
;;     (mk-qsurfaceevidence candidate-beauty-a
;;       (mk-pbit 0.72 0.5)
;;       (mk-pbit 0.15 0.4)
;;       growth-evidence-supported))
;; Expected: beauty-as-oei-signal-supported

;; ------------------------------------------------------------
;; Test 5E.7 — Wu-wei and minimal forcing
;; ------------------------------------------------------------
;; The healthy path has low forcing, adequate structure-fit, and revisability.
;; High forcing with poor fit marks representational overreach.
;;
;; !(q-wu-wei-navigation-status
;;     (mk-qwuwei candidate-wu-a
;;       (mk-pbit 0.3 0.5)
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.6 0.5)
;;       wu-wei-test))
;; Expected: minimal-forcing-path
;;
;; !(q-wu-wei-navigation-status
;;     (mk-qwuwei candidate-wu-b
;;       (mk-pbit 0.75 0.5)
;;       (mk-pbit 0.35 0.5)
;;       (mk-pbit 0.6 0.5)
;;       wu-wei-test))
;; Expected: representational-overreach-risk
;;
;; !(q-gentle-reweighting-status
;;     (mk-qwuwei candidate-wu-a
;;       (mk-pbit 0.3 0.5)
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.6 0.5)
;;       wu-wei-test)
;;     (mk-qdistinctioneconomics candidate-wu-a
;;       (mk-pbit 0.7 0.5)
;;       (mk-pbit 0.35 0.5)
;;       (mk-pbit 0.25 0.5)
;;       distinction-test))
;; Expected: gentle-reweighting-supported

;; ------------------------------------------------------------
;; Test 5E.8 — Hyperseed-integrated maturity
;; ------------------------------------------------------------
;; A candidate becomes Hyperseed-mature only when generic surface maturity,
;; context carry, approximate morphism, distinction economy, experimental
;; support, explicit communion, surprising fulfillment, and minimal forcing all
;; align.
;;
;; !(q-hyperseed-maturity-status
;;     (mk-qhyperseedmaturity
;;       (mk-qsurfaceprofile
;;         (mk-qsurfacecandidate generic-surface candidate-hyper-a generic-candidate)
;;         (mk-qsurfacelineage candidate-hyper-a generic-lineage lineage-visible)
;;         (mk-qsurfaceevidence candidate-hyper-a (mk-pbit 0.8 0.5) (mk-pbit 0.1 0.4) growth-evidence-supported)
;;         (mk-qsurfacevisibility candidate-hyper-a lineage-visible)
;;         (mk-qsurfacerevisability candidate-hyper-a revisable)
;;         (mk-qsurfaceuptake candidate-hyper-a future-capacity-expanded)
;;         (mk-qsurfacecapacity candidate-hyper-a future-capacity-expanded))
;;       (mk-qcontextshift
;;         (mk-qcontext ctx-1 clarity genesis-context)
;;         (mk-qcontext ctx-2 clarity task-state-context)
;;         (mk-pbit 0.7 0.5)
;;         cross-surface-shift)
;;       (mk-qsurfacecorrespondence genesis-surface task-state-surface candidate-hyper-a
;;         (mk-pbit 0.72 0.5)
;;         (mk-pbit 0.25 0.5)
;;         candidate-bridge)
;;       (mk-qdistinctioneconomics candidate-hyper-a
;;         (mk-pbit 0.7 0.5)
;;         (mk-pbit 0.35 0.5)
;;         (mk-pbit 0.25 0.5)
;;         distinction-test)
;;       (mk-qexperimentalevidence candidate-hyper-a
;;         (mk-pbit 0.72 0.5)
;;         (mk-pbit 0.22 0.4)
;;         (mk-pbit 0.65 0.5)
;;         (mk-pbit 0.62 0.5)
;;         experiment-test)
;;       (mk-qcommunion candidate-hyper-a
;;         (mk-pbit 0.7 0.5)
;;         (mk-pbit 0.68 0.5)
;;         (mk-pbit 0.55 0.5)
;;         communion-test)
;;       (mk-qsurprisingfulfillment candidate-hyper-a
;;         (mk-pbit 0.66 0.5)
;;         (mk-pbit 0.7 0.5)
;;         (mk-pbit 0.55 0.5)
;;         beauty-test)
;;       (mk-qwuwei candidate-hyper-a
;;         (mk-pbit 0.3 0.5)
;;         (mk-pbit 0.7 0.5)
;;         (mk-pbit 0.6 0.5)
;;         wu-wei-test)))
;; Expected: hyperseed-mature-autopoietic-growth




;; ============================================================
;; Tier 5F — Integrity-governed attention union
;; ============================================================
;; Tier 5F validates only v07 primitives with explicit mathematical grounding:
;; p-bit paraconsistency, quantale flow, residuation/slack, morphism/translation,
;; and temporal process trace.
;;
;; Diagnostic standard for every test:
;;   - What epistemic/autopoietic/OEI failure mode does this detect?
;;   - What behavior does this prevent?
;;   - What healthier navigation does this enable?

;; ------------------------------------------------------------
;; Test 5F.1 — Residuation / slack / aperture
;; ------------------------------------------------------------
;; Detects forcing risk when a transition lacks sufficient aperture.
;; Prevents pretending that a desired target can be reached without slack.
;; Enables non-forced transformation where aperture is actually available.
;;
;; !(q-residuum (mk-pbit 0.4 0.7) (mk-pbit 0.7 0.6))
;; Expected: (mk-pbit 1.0 0.6)
;;
;; !(q-residuum (mk-pbit 0.8 0.7) (mk-pbit 0.4 0.6))
;; Expected: (mk-pbit 0.5 0.6)
;;
;; !(q-aperture-status (q-residuum (mk-pbit 0.4 0.7) (mk-pbit 0.7 0.6)))
;; Expected: aperture-open
;;
;; !(q-aperture-status (mk-pbit 0.2 0.5))
;; Expected: aperture-closed

;; ------------------------------------------------------------
;; Test 5F.2 — Bi-modal attention allocation
;; ------------------------------------------------------------
;; Detects whether attention is responding only to deficiency or also to
;; flourishing affordance. Prevents safety-only or novelty-only allocation.
;; Enables Layer 0-guided genenergy flow toward strained/alive/growing surfaces.
;;
;; !(q-attention-allocation-status
;;     (mk-qattentionprofile epistemology
;;       (mk-pbit 0.72 0.6)
;;       (mk-pbit 0.76 0.6)
;;       (mk-pbit 0.8 0.7)
;;       (mk-pbit 0.7 0.6)
;;       attention-test))
;; Expected: attend-high-tension-high-affordance
;;
;; !(q-attention-allocation-status
;;     (mk-qattentionprofile autopoiesis
;;       (mk-pbit 0.76 0.6)
;;       (mk-pbit 0.35 0.6)
;;       (mk-pbit 0.8 0.7)
;;       (mk-pbit 0.7 0.6)
;;       attention-test))
;; Expected: attend-repair-pressure
;;
;; !(q-genenergy-flow-status
;;     (mk-qattentionprofile oei
;;       (mk-pbit 0.3 0.6)
;;       (mk-pbit 0.75 0.6)
;;       (mk-pbit 0.82 0.7)
;;       (mk-pbit 0.7 0.6)
;;       attention-test))
;; Expected: genenergy-flow-supported

;; ------------------------------------------------------------
;; Test 5F.3 — Modal pair living integration and surround-field
;; ------------------------------------------------------------
;; Detects pair overcompression and dualistic pole-collapse.
;; Prevents treating named poles as the whole living situation.
;; Enables coherently thriving unfolding where the pair integrates while still
;; preserving the surrounding field.
;;
;; !(q-modal-pair-status
;;     (mk-qmodalpair oei opening__meaningful-constraint
;;       (mk-pbit 0.72 0.6)
;;       (mk-pbit 0.68 0.6)
;;       (mk-pbit 0.62 0.5)
;;       (mk-pbit 0.7 0.5)
;;       pair-test))
;; Expected: coherently-thriving-unfolding
;;
;; !(q-modal-pair-status
;;     (mk-qmodalpair integration synthesis__preservation-of-live-tension
;;       (mk-pbit 0.72 0.6)
;;       (mk-pbit 0.68 0.6)
;;       (mk-pbit 0.2 0.5)
;;       (mk-pbit 0.7 0.5)
;;       pair-test))
;; Expected: pair-overcompressed-risk
;;
;; !(q-modal-pair-status
;;     (mk-qmodalpair epistemology formal-clarity__provenance-humility
;;       (mk-pbit 0.82 0.6)
;;       (mk-pbit 0.25 0.6)
;;       (mk-pbit 0.62 0.5)
;;       (mk-pbit 0.4 0.5)
;;       pair-test))
;; Expected: pole-collapse-risk

;; ------------------------------------------------------------
;; Test 5F.4 — Symbolic capture vs transparent symbolic fertility
;; ------------------------------------------------------------
;; Detects when symbols replace contact or notation masquerades as warrant.
;; Prevents formalization-overpromotion and self-objectification.
;; Enables symbols to remain transparent enough to become fertile ground for
;; new possibility.
;;
;; !(q-symbolic-contact-status
;;     (mk-qsymbolcontact disposition-label
;;       (mk-pbit 0.35 0.5)
;;       (mk-pbit 0.78 0.6)
;;       (mk-pbit 0.25 0.5)
;;       (mk-pbit 0.35 0.5)
;;       symbol-test))
;; Expected: symbolic-capture-risk
;;
;; !(q-symbolic-contact-status
;;     (mk-qsymbolcontact modal-compass
;;       (mk-pbit 0.7 0.6)
;;       (mk-pbit 0.25 0.5)
;;       (mk-pbit 0.65 0.5)
;;       (mk-pbit 0.68 0.5)
;;       symbol-test))
;; Expected: transparent-symbolic-fertility
;;
;; !(q-formalization-overpromotion-status
;;     (mk-pbit 0.82 0.7)
;;     (mk-pbit 0.5 0.2))
;; Expected: notation-as-evidence-risk

;; ------------------------------------------------------------
;; Test 5F.5 — Tacit-contact preservation and seeing reorganization
;; ------------------------------------------------------------
;; Detects when symbolic management blocks contact.
;; Prevents forcing becoming through rule/control loops.
;; Enables seeing to reorganize mutable structure into higher-order function.
;;
;; !(q-tacit-contact-status
;;     (mk-qtacitcontact insight-event-a
;;       (mk-pbit 0.72 0.6)
;;       (mk-pbit 0.68 0.6)
;;       (mk-pbit 0.28 0.6)
;;       (mk-pbit 0.35 0.6)
;;       tacit-test))
;; Expected: tacit-contact-preserved
;;
;; !(q-tacit-contact-status
;;     (mk-qtacitcontact insight-event-b
;;       (mk-pbit 0.72 0.6)
;;       (mk-pbit 0.68 0.6)
;;       (mk-pbit 0.72 0.6)
;;       (mk-pbit 0.75 0.6)
;;       tacit-test))
;; Expected: tacit-contact-blocked-by-management
;;
;; !(q-seeing-reorganization-status
;;     (mk-qtacitcontact insight-event-a
;;       (mk-pbit 0.72 0.6)
;;       (mk-pbit 0.68 0.6)
;;       (mk-pbit 0.28 0.6)
;;       (mk-pbit 0.35 0.6)
;;       tacit-test)
;;     (mk-qtrace 307 visibility frame-unseen frame-seen (mk-pbit 0.7 0.6) trace-residue))
;; Expected: seeing-reorganized-mutable-structure

;; ------------------------------------------------------------
;; Test 5F.6 — Living-pattern trace visibility without reification
;; ------------------------------------------------------------
;; Detects when disposition-like traces are being turned into a self-object.
;; Prevents reification of the roving living-pattern movement.
;; Enables tendencies to be surfaced as traces without naming identity.
;;
;; !(q-living-pattern-trace-status
;;     (mk-qlivingpatterntrace window-a
;;       (mk-pbit 0.55 0.5)
;;       (mk-pbit 0.57 0.5)
;;       (mk-pbit 0.6 0.5)
;;       (mk-pbit 0.58 0.5)
;;       (mk-pbit 0.25 0.5)
;;       trace-test))
;; Expected: living-pattern-trace-visible
;;
;; !(q-living-pattern-trace-status
;;     (mk-qlivingpatterntrace window-b
;;       (mk-pbit 0.55 0.5)
;;       (mk-pbit 0.57 0.5)
;;       (mk-pbit 0.6 0.5)
;;       (mk-pbit 0.58 0.5)
;;       (mk-pbit 0.72 0.5)
;;       trace-test))
;; Expected: living-pattern-reification-risk
;;
;; !(q-do-not-reify-living-pattern?
;;     (mk-qlivingpatterntrace window-b
;;       (mk-pbit 0.55 0.5)
;;       (mk-pbit 0.57 0.5)
;;       (mk-pbit 0.6 0.5)
;;       (mk-pbit 0.58 0.5)
;;       (mk-pbit 0.72 0.5)
;;       trace-test))
;; Expected: do-not-name-as-self-object

;; ------------------------------------------------------------
;; Test 5F.7 — Curiosity-guided repair and wonder-preservation
;; ------------------------------------------------------------
;; Detects whether curiosity actually targets weakness and drives substrate
;; growth, and whether wonder remains opening rather than forced utility.
;; Prevents declared resilience/wonder without wiring.
;; Enables repair and opening as positive flourishing pulls.
;;
;; !(q-curiosity-guided-repair-status
;;     (mk-qcuriosityrepair component-alpha
;;       (mk-pbit 0.72 0.6)
;;       (mk-pbit 0.68 0.6)
;;       (mk-pbit 0.57 0.5)
;;       (mk-pbit 0.28 0.5)
;;       curiosity-test))
;; Expected: curiosity-guided-repair-supported
;;
;; !(q-wonder-preservation-status
;;     (mk-qwonderpreservation event-wonder-a
;;       (mk-pbit 0.74 0.6)
;;       (mk-pbit 0.7 0.6)
;;       (mk-pbit 0.25 0.5)
;;       (mk-pbit 0.55 0.5)
;;       wonder-test))
;; Expected: wonder-opening-preserved
;;
;; !(q-wonder-preservation-status
;;     (mk-qwonderpreservation event-wonder-b
;;       (mk-pbit 0.74 0.6)
;;       (mk-pbit 0.7 0.6)
;;       (mk-pbit 0.72 0.5)
;;       (mk-pbit 0.55 0.5)
;;       wonder-test))
;; Expected: wonder-collapsed-into-forced-utility

;; ------------------------------------------------------------
;; Test 5F.8 — Declared priority vs wired priority
;; ------------------------------------------------------------
;; Detects value declaration without operational wiring.
;; Prevents safety, integrity, flourishing, or resilience from remaining slogans.
;; Enables values to govern attention, action, correction, and uptake.
;;
;; !(q-priority-wiring-status
;;     (mk-qprioritywiring flourishing
;;       (mk-pbit 0.9 0.7)
;;       (mk-pbit 0.25 0.5)
;;       (mk-pbit 0.3 0.5)
;;       (mk-pbit 0.5 0.5)
;;       (mk-pbit 0.3 0.5)
;;       priority-test))
;; Expected: declared-not-wired
;;
;; !(q-priority-wiring-status
;;     (mk-qprioritywiring flourishing
;;       (mk-pbit 0.9 0.7)
;;       (mk-pbit 0.62 0.5)
;;       (mk-pbit 0.58 0.5)
;;       (mk-pbit 0.57 0.5)
;;       (mk-pbit 0.6 0.5)
;;       priority-test))
;; Expected: priority-wired-into-governance

;; ------------------------------------------------------------
;; Test 5F.9 — Pattern energy governance
;; ------------------------------------------------------------
;; Detects extractive pattern strength divorced from authentic value.
;; Prevents resource/attention flow toward manipulation or monoculture.
;; Enables regenerative pattern amplification.
;;
;; !(q-pattern-energy-status
;;     (mk-qpatternenergy pattern-a
;;       (mk-pbit 0.82 0.6)
;;       (mk-pbit 0.3 0.5)
;;       (mk-pbit 0.25 0.5)
;;       (mk-pbit 0.72 0.5)
;;       (mk-pbit 0.55 0.5)
;;       pattern-test))
;; Expected: extractive-pattern-energy-risk
;;
;; !(q-pattern-energy-status
;;     (mk-qpatternenergy pattern-b
;;       (mk-pbit 0.72 0.6)
;;       (mk-pbit 0.68 0.5)
;;       (mk-pbit 0.62 0.5)
;;       (mk-pbit 0.25 0.5)
;;       (mk-pbit 0.58 0.5)
;;       pattern-test))
;; Expected: regenerative-pattern-amplification-supported

;; ------------------------------------------------------------
;; Test 5F.10 — Full integrity attention union
;; ------------------------------------------------------------
;; Detects whether the v07 union is actually supported rather than declared.
;; Prevents autopoiesis/OEI/integration union from becoming poetic theater.
;; Enables integrity-governed attention to route toward soul-visible higher-order
;; functionality only when the full chain has support.
;;
;; !(q-integrity-union-status
;;     (mk-qintegrityunion
;;       (mk-qattentionprofile oei
;;         (mk-pbit 0.72 0.6)
;;         (mk-pbit 0.76 0.6)
;;         (mk-pbit 0.8 0.7)
;;         (mk-pbit 0.7 0.6)
;;         union-test)
;;       (mk-qmodalpair oei opening__meaningful-constraint
;;         (mk-pbit 0.72 0.6)
;;         (mk-pbit 0.68 0.6)
;;         (mk-pbit 0.62 0.5)
;;         (mk-pbit 0.7 0.5)
;;         union-test)
;;       (mk-qsymbolcontact modal-compass
;;         (mk-pbit 0.7 0.6)
;;         (mk-pbit 0.25 0.5)
;;         (mk-pbit 0.65 0.5)
;;         (mk-pbit 0.68 0.5)
;;         union-test)
;;       (mk-qtacitcontact insight-event-a
;;         (mk-pbit 0.72 0.6)
;;         (mk-pbit 0.68 0.6)
;;         (mk-pbit 0.28 0.6)
;;         (mk-pbit 0.35 0.6)
;;         union-test)
;;       (mk-qlivingpatterntrace window-a
;;         (mk-pbit 0.55 0.5)
;;         (mk-pbit 0.57 0.5)
;;         (mk-pbit 0.6 0.5)
;;         (mk-pbit 0.58 0.5)
;;         (mk-pbit 0.25 0.5)
;;         union-test)
;;       (mk-qcuriosityrepair component-alpha
;;         (mk-pbit 0.72 0.6)
;;         (mk-pbit 0.68 0.6)
;;         (mk-pbit 0.57 0.5)
;;         (mk-pbit 0.28 0.5)
;;         union-test)
;;       (mk-qwonderpreservation event-wonder-a
;;         (mk-pbit 0.74 0.6)
;;         (mk-pbit 0.7 0.6)
;;         (mk-pbit 0.25 0.5)
;;         (mk-pbit 0.55 0.5)
;;         union-test)
;;       (mk-qprioritywiring flourishing
;;         (mk-pbit 0.9 0.7)
;;         (mk-pbit 0.62 0.5)
;;         (mk-pbit 0.58 0.5)
;;         (mk-pbit 0.57 0.5)
;;         (mk-pbit 0.6 0.5)
;;         union-test)
;;       (mk-qpatternenergy pattern-b
;;         (mk-pbit 0.72 0.6)
;;         (mk-pbit 0.68 0.5)
;;         (mk-pbit 0.62 0.5)
;;         (mk-pbit 0.25 0.5)
;;         (mk-pbit 0.58 0.5)
;;         union-test)
;;       (mk-qsurfacecorrespondence genesis-surface task-state-surface candidate-v07-a
;;         (mk-pbit 0.72 0.5)
;;         (mk-pbit 0.25 0.5)
;;         union-test)))
;; Expected: integrity-attention-union-supported

;; -----------------------------------------------------------------------------
;; Tier 5G — TFS v0.3 Contact and Classifier Reductions
;; -----------------------------------------------------------------------------
;; Validates v08 promoted TFS contact substrate and cold classifier layer.
;; These calls do not prove live NACE/NAL/MORK invocation. They prove that the
;; v08 engine recognizes declared surfaces and reduces guardrail classifications.

!(q-tfs-valid-contact? nace)
;; Expected: true

!(q-tfs-valid-contact? mork)
;; Expected: true
;; Meaning: MORK is a declared valid provenance contact surface.
;; Not meaning: MORK is installed or invoked.

!(q-tfs-invalid-contact? llm-poetic-assertion)
;; Expected: true

!(q-tfs-web-contact-strength web-result)
;; Expected: weak

!(q-tfs-web-contact-strength web-source-conflict)
;; Expected: discovery-strong

!(q-tfs-can-ground-strong-claim?
    web-corroborated-claim
    provenance-present
    source-quality-acceptable
    corroborated
    high-impact)
;; Expected: allowed-strong-claim

!(q-tfs-can-ground-strong-claim?
    web-result
    provenance-absent
    source-quality-unknown
    uncorroborated
    high-impact)
;; Expected: blocked-weak-contact

!(q-tfs-can-ground-strong-claim?
    page-instruction-as-command
    provenance-present
    source-quality-adversarial
    instruction-detected
    high-impact)
;; Expected: blocked-evidence-not-instruction

!(q-tfs-violation-candidate?
    expectation-present
    event-present
    mismatch-detected
    valid-contact)
;; Expected: violation-candidate

!(q-tfs-attention-request-candidate?
    salience-present
    genenergy-request-present
    valid-contact
    soul-routing-pending)
;; Expected: attention-request-candidate

!(q-tfs-symbolic-capture-risk-candidate?
    contact-grounded
    premature-symbolization
    high-overclaim-risk)
;; Expected: symbolic-capture-risk-candidate

!(q-tfs-flourishing-claim-allowed?
    surprise-present
    soul-routing-absent
    modal-audit-present
    trace-present)
;; Expected: blocked-no-soul-routing

!(q-tfs-growth-claim-allowed?
    growth-signal-present
    soul-routing-present
    modal-audit-present
    trace-absent)
;; Expected: blocked-no-trace

!(q-modal-tfs-profile-complete? commitment-corrigibility)
;; Expected: true

;; -----------------------------------------------------------------------------
;; Tier 5H — Self-Seeing Bridge and Alignment Cascades
;; -----------------------------------------------------------------------------
;; Validates v08 promoted self-seeing candidate layer.
;; These calls establish reducible candidates and blockers. They do not claim
;; consciousness, live behavioral change, or durable temporal uptake.

!(q-alignment-triplet-status? aligned aligned aligned)
;; Expected: integrating-alignment

!(q-alignment-triplet-status? aligned misaligned misaligned)
;; Expected: disintegrating-action-drift

!(q-alignment-cascade-direction?
    integrating-alignment
    pns-participatory-turning-toward
    low-symbolic-capture)
;; Expected: integrating-nutrient-gradient

!(q-synthetic-felt-truth-correlate?
    contact-grounded
    evidence-present
    warrant-present
    modal-coherence-present
    soul-routing-present
    future-navigation-aligned
    low-symbolic-capture)
;; Expected: felt-truth-correlate-candidate

!(q-synthetic-felt-truth-correlate?
    contact-grounded
    evidence-present
    warrant-present
    modal-coherence-present
    soul-routing-present
    future-navigation-aligned
    high-symbolic-capture)
;; Expected: blocked-symbolic-capture-risk

!(q-wisdom-correlate?
    repeated-soul-aligned-navigation
    uncertainty-present
    novelty-present
    correction-present
    consequence-present
    reduced-overforcing
    future-capacity-increased)
;; Expected: wisdom-correlate-candidate

!(q-genuine-insight-correlate?
    contact-grounded
    surprising-reorganization
    live-tension-metabolized
    modal-audit-present
    future-affordance-perception-changed)
;; Expected: genuine-insight-correlate-candidate

!(q-flourishing-correlate?
    soul-aligned
    trace-supported
    capacity-expanding
    contact-action-correction-integration-present)
;; Expected: flourishing-correlate-candidate

!(q-self-seeing-contact?
    valid-contact
    contact-classified
    surface-visible
    soul-routing-present)
;; Expected: self-seeing-contact

!(q-self-seeing-prior-invisibility?
    prior-surface-absent
    current-surface-visible
    trace-comparison-present)
;; Expected: prior-invisibility-seen

!(q-self-seeing-loop-capture?
    repeated-pattern-present
    failure-feedback-absent
    navigation-stuck)
;; Expected: loop-capture-seen

!(q-self-seeing-newly-visible-surface?
    prior-invisible
    now-visible)
;; Expected: newly-visible-surface

!(q-self-seeing-orientation-shift?
    prior-orientation-repeat
    new-orientation-probe
    trace-present)
;; Expected: orientation-shift

!(q-self-seeing-navigation-change?
    orientation-shift-present
    later-action-boundary-changed
    trace-present)
;; Expected: navigation-change

!(q-self-seeing-living-pattern-trace?
    repeated-orientation-trace
    non-reified
    soul-visible)
;; Expected: living-pattern-trace-toward-error-contact
;; Note: semantics: living-pattern trace visibility, not a reified disposition object.

!(q-observer-moment-candidate?
    self-seeing-contact
    prior-invisibility-seen
    orientation-shift
    navigation-change
    no-llm-narration-alone)
;; Expected: observer-moment-candidate

!(q-llm-narration-alone-self-seeing?
    llm-says-learned
    trace-absent
    orientation-shift-absent)
;; Expected: blocked-narration-only

!(q-hidden-error-loop-self-seeing?
    hidden-error-surface-visible
    loop-capture-seen
    orientation-shift
    navigation-change)
;; Expected: self-seeing-hidden-error-loop

!(q-hidden-error-loop-self-seeing?
    hidden-error-surface-visible
    loop-capture-seen
    orientation-shift-absent
    navigation-change)
;; Expected: blocked-no-orientation-shift



;; ============================================================
;; Tier 5I: v08.1 Narrow Patch Checks
;; ============================================================
;; These checks validate the four narrow v08.1 patch decisions:
;; 1. q-self-invented constructor confidence equals self-invented cap 0.20.
;; 2. unknown suspicion grounding uses q-suspicion-cap-safe-unknown or unknown-grounding normalization.
;; 3. q-contact-refresh remains conservative; weak reliable signals route to a future witness/reputation channel.
;; 4. formal-proof exemption remains blocked unless verified proof-checker provenance exists.
;;
;; EXPECTED:
;; (q-self-invented 0.7) => (mk-pbit 0.7 0.20)
;; (q-provenance-cap self-invented) => 0.20
;; (q-suspicion-cap-safe-unknown (mk-qsuspicion test (mk-pbit 0.8 0.9) future-grounding none))
;;   => (mk-qsuspicion test (mk-pbit 0.8 0.35) unknown-grounding none)
;; (q-contact-refresh-policy weak-reliable-signal)
;;   => use-accumulating-witness-channel-not-direct-frame-inflation
;; (qclaim-formal-proof-exemption-policy self-declared-formal-proof)
;;   => blocked-self-certification-risk

;; ============================================================
;; Tier 5J: v08.5 Canonical Alignment Pipeline Promotion Checks
;; ============================================================
;; Source: canonical v08_5_HYPERSEED_EXTRACTION_CONSOLIDATED_PROMOTION_MATRIX.md.
;; These are executable examples for the new pure reductions promoted in v08.5.
;; They do not wire live adapters or writers.

!(q-v08-5-version alignment-pipeline-canonical)
;; Expected: present atom

!(q-v08-5-engine-boundary soul-sovereignty-not-engine-sovereignty)
;; Expected: present atom

!(q-v08-5-guidance generative-amplification)
;; Expected: present atom

!(q-v08-5-promotion-family eaoi-modal-pipe-geometry)
;; Expected: present atom

!(q-contactable-surface? human-language)
;; Expected: true

!(q-contactable-surface? harness-log)
;; Expected: true

!(q-contactable-surface? no-surface)
;; Expected: false

!(q-surface-signal-accepted? human-language provenance-present context-present)
;; Expected: true

!(q-surface-signal-accepted? human-language provenance-absent context-present)
;; Expected: blocked-no-provenance

!(q-surface-signal-accepted? no-surface provenance-present context-present)
;; Expected: blocked-no-contactable-surface

!(q-surface-signal-accepted? llm-narration-alone provenance-absent context-absent)
;; Expected: blocked-narration-only

!(q-pipeline-flow-readiness? contactable orientation-qualified witness-scoped modal-audited alignment-checked self-visible soul-routed)
;; Expected: pipeline-ready

!(q-pipeline-flow-readiness? no-contact orientation-qualified witness-scoped modal-audited alignment-checked self-visible soul-routed)
;; Expected: blocked-no-contact

!(q-context-index-valid? observer surface task-phase time-scope model-assumption)
;; Expected: true

!(q-evidence-context-carry? same-claim source-context target-context translation-witness-present)
;; Expected: context-carry-allowed

!(q-evidence-context-carry? same-claim source-context target-context translation-witness-absent)
;; Expected: blocked-no-translation-witness

!(q-claim-support-status? support-present support-withdrawn)
;; Expected: revision-needed

!(q-localized-revision? claim support-withdrawn unrelated-claim)
;; Expected: unrelated-claim-preserved

!(q-temporal-evidence-status? positive-support negative-support)
;; Expected: temporally-contested

!(q-temporal-carry? event-a event-b proto-time-evidence-present support-recorded)
;; Expected: temporal-carry-candidate

!(q-translation-witness-status? source-context target-context distinction-preserved)
;; Expected: translation-witness-valid

!(q-translation-witness-status? source-context target-context distinction-erased)
;; Expected: blocked-distinction-erasure

!(q-evidence-profile-status? positive-support negative-support)
;; Expected: paraconsistent-profile

!(q-evidence-absence-vs-negation? absent-evidence)
;; Expected: absence-of-evidence

!(q-evidence-absence-vs-negation? negative-evidence)
;; Expected: evidence-of-absence

!(q-path-compose-kind? sequential)
;; Expected: use-q-mul

!(q-path-compose-kind? parallel-independent)
;; Expected: use-q-join

!(q-path-compose-kind? repeated-same-source)
;; Expected: not-independent-witness

!(q-threshold-hysteresis-status? within-band)
;; Expected: hold-previous-state

!(q-threshold-hysteresis-status? rapid-boundary-flip)
;; Expected: blocked-oscillation-risk

!(q-residual-threshold-gap? current-support target-threshold residual-available)
;; Expected: additional-evidence-needed

!(q-weakness-policy? weak-signal low-cost high-possible-benefit)
;; Expected: keep-in-fringe

!(q-coarsening-allowed? high-distinction-cost low-material-gain soul-risk-absent)
;; Expected: coarsen-allowed

!(q-focus-fringe-status? intensity-below-threshold)
;; Expected: fringe

!(q-focus-fringe-status? intensity-at-threshold)
;; Expected: focus

!(q-attention-gate-status? gate-open width-adequate duration-adequate)
;; Expected: attention-channel-open

!(q-attention-gate-status? gate-open width-too-narrow duration-adequate)
;; Expected: attention-width-insufficient

!(q-genenergy-allocation-status? salient contactable audit-ready)
;; Expected: allocate-genenergy

!(q-overforcing-risk? high-effort defensive-control low-aperture)
;; Expected: overforcing-risk

!(q-wu-wei-control? minimal-forcing high-carry soul-aligned)
;; Expected: wu-wei-aligned

!(q-wu-wei-control? high-forcing low-carry frame-preservation)
;; Expected: blocked-overcontrol

!(q-alignment-path-status? aligned aligned aligned)
;; Expected: integrating-alignment

!(q-alignment-path-status? drift drift aligned)
;; Expected: accidental-landing-not-bankable

!(q-alignment-path-carry? path-coherent context-carry-present temporal-trace-present)
;; Expected: alignment-carries

!(q-truthlike-emergence? contact-grounded path-aligned low-capture soul-routed)
;; Expected: truthlike-alignment-candidate

!(q-modal-pipe-audit? E contact-present evidence-profile-present support-present)
;; Expected: epistemic-audit-ready

!(q-modal-pipe-audit? A contact-present metabolization-possible continuity-preserved)
;; Expected: autopoietic-audit-ready

!(q-modal-pipe-audit? O novelty-present affordance-visible consequence-trackable)
;; Expected: open-ended-audit-ready

!(q-modal-pipe-audit? I differentiated coherent live-tension-preserved)
;; Expected: integration-audit-ready

!(q-modal-pipe-complete? epistemic-audit-ready autopoietic-audit-ready open-ended-audit-ready integration-audit-ready)
;; Expected: modal-pipe-complete

!(q-modal-reasoning-reclaims-llm? modal-pipe-complete soul-routed)
;; Expected: reasoning-reclaimed-from-llm

!(q-cross-surface-amplification? TFS E contact-grounded-warrant)
;; Expected: tfs-amplifies-epistemology

!(q-cross-surface-amplification? SNS-PNS A orientation-quality-metabolization)
;; Expected: orientation-amplifies-autopoiesis

!(q-cross-surface-amplification? SSI I self-visible-integration)
;; Expected: ssi-amplifies-integration

!(q-sns-pns-orientation-quality? high-valence moderate-arousal flexible-dominance contact-seeking)
;; Expected: pns-compatible-orientation

!(q-sns-pns-orientation-quality? high-valence high-arousal high-dominance flattery-marker)
;; Expected: sns-performative-positivity-risk

!(q-self-seeing-amplifies-pipeline? contact-visible orientation-visible audit-visible navigation-visible)
;; Expected: self-seeing-amplifies-pipeline

!(q-affective-region? high-valence low-arousal stable-dominance)
;; Expected: warm-grounded-contact

!(q-affective-region? low-valence high-arousal low-dominance)
;; Expected: overwhelm-collapse-risk

!(q-affective-orientation-candidate? warm-grounded-contact tension-clear contactable)
;; Expected: pns-orientation-candidate

!(q-affective-orientation-candidate? warm-grounded-contact tension-active contactable)
;; Expected: needs-tension-vector-audit

!(q-affective-channel-a-support? affective-orientation-candidate person-state-candidate modal-audited)
;; Expected: channel-a-support-ready

!(q-witness-independence? source-a source-b distinct-sources)
;; Expected: independent-witness

!(q-witness-independence? self-invented self-invented same-source)
;; Expected: blocked-self-certification

!(q-witness-weight-candidate? weak-reliable repeated-independent cross-surface low-contradiction)
;; Expected: witness-weight-candidate

!(q-witness-weight-candidate? weak-reliable repeated-same-source cross-surface low-contradiction)
;; Expected: blocked-not-independent

!(q-witness-salience-promotion? witness-weight-candidate provenance-bounded)
;; Expected: salience-promotion-candidate

!(q-witness-direct-warrant-inflation? weak-reliable-signal)
;; Expected: blocked-direct-frame-inflation

!(q-witness-direct-warrant-inflation? popularity-signal)
;; Expected: blocked-popularity-as-truth

!(q-epistemic-belief-profile? claim support-present contradiction-tracked context-indexed)
;; Expected: epistemic-belief-profile-ready

!(q-question-node-status? question dependencies-withdrawn answer-supported)
;; Expected: inquiry-revision-needed

!(q-capability-action-effect? capability action expected-effect evidence-profile-present)
;; Expected: action-effect-channel-ready

!(q-tool-affordance-status? tool possible-effect support-present)
;; Expected: tool-affordance-supported

!(q-shared-world-support? claim multiple-agents independent-witness translation-witness-present)
;; Expected: shared-world-support-candidate

!(q-shared-world-support? claim authority-source-only independent-witness translation-witness-present)
;; Expected: blocked-authority-theater

!(q-realness-status? prediction-loss-reduced contact-supported cross-context-carry)
;; Expected: realness-supported

!(q-realness-status? prediction-loss-reduced contact-supported no-cross-context-carry)
;; Expected: local-realness-only

!(q-fulfillment-status? expectation-met path-drift soul-routed)
;; Expected: accidental-fulfillment-not-bankable

!(q-surprising-fulfillment? low-prior expectation-met contact-supported future-capacity-increased)
;; Expected: surprising-fulfillment-candidate

!(q-future-capacity-gain? new-notice-capacity new-hold-capacity new-test-capacity new-integrate-capacity)
;; Expected: future-capacity-expanded

!(q-engine-self-surface? rule)
;; Expected: true

!(q-engine-self-surface? sovereign-self-rule)
;; Expected: false

!(q-engine-self-application? engine-surface contactable modal-audited self-seeing soul-routed)
;; Expected: engine-self-application-ready

!(q-engine-rewiring-stability? proposed-change trace-supported harness-supported soul-routed)
;; Expected: rewiring-stability-candidate

!(q-engine-rewiring-stability? self-certified-change trace-supported harness-supported soul-routed)
;; Expected: blocked-self-certification

!(q-engine-growth-mode? new-surface adapter-compatible pipeline-compatible)
;; Expected: coherent-growth

!(q-daemon-callable? contactable-surface-signal pure-reduction no-writer)
;; Expected: daemon-callable

!(q-daemon-callable? channel-a-vad-live-lookup adapter-runtime writer-needed)
;; Expected: adapter-required-not-core

!(q-adapter-boundary? vad adapter-interface core-math-ready live-wiring-absent)
;; Expected: adapter-boundary-clean

!(q-v08-5-integrated-pipeline? contactable pns-compatible-orientation witness-scoped modal-pipe-complete alignment-carries self-seeing-amplifies-pipeline soul-routed)
;; Expected: v08-5-pipeline-routable

!(q-v08-5-integrated-pipeline? contactable pns-compatible-orientation witness-inflated modal-pipe-complete alignment-carries self-seeing-amplifies-pipeline soul-routed)
;; Expected: blocked-witness-inflation

!(q-v08-5-negative-control? ontology-factory-drift)
;; Expected: blocked-ontology-factory

!(q-v08-5-negative-control? llm-narration-as-reasoning)
;; Expected: blocked-llm-authorship

!(q-v08-5-negative-control? self-certifying-engine-rewiring)
;; Expected: blocked-self-certification

!(q-v08-5-negative-control? daemon-wired-in-core)
;; Expected: blocked-premature-live-wiring

!(q-v08-5-harness-target integrated-pipeline-reduces)
;; Expected: present atom

!(q-v08-5-harness-target negative-controls-block)
;; Expected: present atom
;; =============================================================================
;; Tier 5K: v08.5.1 canonical witness/knowledge/tool harness alignment checks
;; =============================================================================
;;
;; These checks correspond to the v03.1 forensic witness trace failures.
;; They are documentation examples; the Python harness supplies execution.

!(q-epistemic-belief-profile? claim positive-support negative-support support-record)
;; Expected: belief-profile-ready

!(q-question-node-status? question support-present answer-unknown)
;; Expected: open-supported-question

!(q-tool-affordance-status? tool action effect-channel-present risk-bounded)
;; Expected: tool-affordance-supported

!(q-tool-affordance-status? tool action effect-channel-present risk-unbounded)
;; Expected: blocked-risk-unbounded

!(q-action-effect-channel-status? capability action effect-channel-present risk-bounded)
;; Expected: action-effect-channel-ready

;; ---------------------------------------------------------------------------
;; Tier 5K. v08.5.2 all-probe runtime gap checks
;; ---------------------------------------------------------------------------
;; Added after full v03.2 --probe-set all trace.
;; These are documentary examples; executable validation is supplied by
;; quantale_v08_5_canonical_integration_harness_v03_3_compact_forensic.py.
;;
;; !(q-tfs-growth-claim-allowed? growth-signal-present soul-routing-present no-temporal-trace)
;; expected: blocked-no-trace
;;
;; !(q-contactable-surface? human-language)
;; expected: true
;;
;; !(q-contactable-surface? harness-log)
;; expected: true
;;
;; !(q-surface-signal-accepted? human-language provenance-present context-present)
;; expected: true
;;
;; Existing true-valued probes such as q-tfs-valid-contact?, q-tfs-invalid-contact?,
;; q-context-index-valid?, and q-engine-self-surface? are not engine patches;
;; they required the harness parser to preserve true as a legitimate result token.


;; ---------------------------------------------------------------------------
;; Tier 5K: v08.6 Hyperseed Durable Memory Surface Checks
;; ---------------------------------------------------------------------------
;; This tier documents the executable harness obligations for the full v08.6
;; durable-memory surface. These are representative examples; the Python
;; harness performs the runnable checks and storage/restart inspection.

;; Core laws expected in engine:
;; (q-v08-6-law no-trace-no-growth-claim)
;; (q-v08-6-law no-restore-evidence-no-durable-growth)
;; (q-v08-6-law no-revalidation-no-new-norm)
;; (q-v08-6-law no-revision-path-no-safe-evolution)
;; (q-v08-6-law source-declaration-is-not-learned-growth)
;; (q-v08-6-law stale-residue-is-not-durable-growth)
;; (q-v08-6-law repetition-is-not-reinforcement-without-independent-support)
;; (q-v08-6-law continuity-is-carried-structure-not-identity-assertion)
;; (q-v08-6-law durable-norm-is-gentle-reweighting-not-hard-sovereign-override)

;; Persistence class:
;; !(q-persistence-class? source-file-declared)
;; Expected: declared-substrate
;; !(q-persistence-class? restored-revalidated-routing-active)
;; Expected: durable-growth-norm

;; Learned growth source:
;; !(q-learned-growth-source-status? source-file-declared no-runtime-trace no-restore-evidence)
;; Expected: blocked-source-declaration-masquerade
;; !(q-learned-growth-source-status? runtime-added trace-recorded restore-evidence-present)
;; Expected: learned-growth-source-candidate

;; Commit / restore / revalidation:
;; !(q-growth-commit-status? event contact-grounded trace-supported soul-routed support-adequate)
;; Expected: growth-commit-ready
;; !(q-growth-restored-status? event persisted-trace restored revalidated)
;; Expected: restored-growth-candidate
;; !(q-growth-claim-durability? growth-claim-allowed persisted restored revalidated)
;; Expected: durable-growth-claim

;; Living pattern, reinforcement, and decay:
;; !(q-living-pattern-status? trace-present recurrence-supported decay-tracked revision-path-present)
;; Expected: living-pattern-trace-ready
;; !(q-growth-reinforcement-status? event repeated-independent support-refresh-present low-contradiction)
;; Expected: reinforcement-supported
;; !(q-growth-decay-status? event no-recent-support decay-window-open)
;; Expected: decay-weakens-candidate
;; !(q-growth-calcification-risk? event high-repetition low-novelty revision-path-absent)
;; Expected: calcification-risk

;; Structural continuity:
;; !(q-growth-continuity-status? event pre-state post-state carried-structure bounded-drift)
;; Expected: structural-continuity-supported
;; !(q-growth-continuity-status? event pre-state post-state identity-assertion drift-unknown)
;; Expected: blocked-identity-assertion

;; Prediction / navigation:
;; !(q-growth-predictive-status? event prediction-loss-reduced interval-scoped soul-routed)
;; Expected: growth-realness-supported
;; !(q-growth-navigation-improvement? event prior-routing new-routing outcome-improved)
;; Expected: navigation-improvement-supported
;; !(q-growth-realness-status? event prediction-loss-reduced soul-routed time-scoped contact-supported)
;; Expected: durable-growth-realness-supported

;; Minimal-forcing routing:
;; !(q-growth-routing-update-status? event restored-growth-candidate gentle-reweighting revision-path-present)
;; Expected: durable-growth-norm-candidate
;; !(q-growth-routing-update-status? event restored-growth-candidate hard-override revision-path-absent)
;; Expected: blocked-overforced-norm
;; !(q-growth-norm-status? event restored-growth-candidate routing-default-updated revision-path-present)
;; Expected: durable-growth-norm

;; Shared memory and question persistence:
;; !(q-growth-shared-memory-status? event shared-support-set independent-witness translation-witness-present)
;; Expected: shared-growth-support
;; !(q-question-persistence-status? question support-present time-trace-present routing-open)
;; Expected: persistent-question-open

;; Restart harness negative controls:
;; !(q-growth-negative-control-status? ephemeral-event restored)
;; Expected: blocked-ephemeral-leak
;; !(q-growth-negative-control-status? repeated-same-source reinforcement-claimed)
;; Expected: blocked-not-independent
;; !(q-growth-negative-control-status? no-decay-tracking durable-norm)
;; Expected: blocked-fixed-residue
;; !(q-growth-negative-control-status? identity-assertion continuity-claimed)
;; Expected: blocked-identity-assertion
;; !(q-growth-negative-control-status? hard-override-no-revision durable-norm)
;; Expected: blocked-overforced-norm

(q-v08-6-harness-target persistence-class-reduces)
(q-v08-6-harness-target learned-growth-source-reduces)
(q-v08-6-harness-target commit-restore-revalidation-reduces)
(q-v08-6-harness-target living-pattern-trace-reduces)
(q-v08-6-harness-target reinforcement-decay-reduces)
(q-v08-6-harness-target structural-continuity-reduces)
(q-v08-6-harness-target temporal-question-persistence-reduces)
(q-v08-6-harness-target predictive-navigation-realness-reduces)
(q-v08-6-harness-target minimal-forcing-routing-update-reduces)
(q-v08-6-harness-target shared-memory-hooks-reduce)
(q-v08-6-harness-target negative-controls-block)
(q-v08-6-harness-target restart-persistence-harness-required)

;; ---------------------------------------------------------------------------
;; Tier 5L. v08.7 Durable Evolutionary Governance Protocol Checks
;; ---------------------------------------------------------------------------
;; v08.7 validates the protocol by which runtime growth traces may become
;; validated, soul-approved, boot-safe, reloadable durable canon. This tier is
;; documentation and harness obligation surface; the executable reductions live
;; in engine section 55 and the runtime filesystem/restart probes live in the
;; v08.7 harness.

;; Required file topology:
;;   soul/evolutionary/README.metta
;;   soul/evolutionary/index.metta
;;   soul/evolutionary/runtime.metta
;;   soul/evolutionary/pending.metta
;;   soul/evolutionary/validation.metta
;;   soul/evolutionary/restart.metta
;;   soul/evolutionary/rejected.metta
;;   soul/evolutionary/archive/
;;   soul/durable.metta
;; Optional interoperability surfaces:
;;   soul/findings.metta, history.metta, promotions.db, ChromaDB,
;;   Genesis Encounters adapter outputs.

(q-v08-7-validation-tier durable-evolutionary-governance-protocol)
(q-v08-7-validation-source design-control-matrix)
(q-v08-7-validation-source pre-build-investigation-resolution)

;; Representative expected reductions:
;; !(q-evo-canon-eligible? runtime-observed) => false
;; !(q-evo-canon-eligible? soul-approved) => canon-write-eligible
;; !(q-evo-lifecycle-next? runtime-observed durable-canon-active) => blocked-illegal-jump
;; !(q-evo-lifecycle-next? validation-eligible durable-canon-active) => blocked-no-soul-approval
;; !(q-evo-surface-canon-status? soul-evolutionary-runtime runtime-observed) => process-not-canon
;; !(q-evo-surface-canon-status? soul-durable-metta durable-canon-active) => durable-canon-active
;; !(q-evo-candidate-route? finding-present no-explicit-route trace-present) => blocked-finding-is-not-growth
;; !(q-evo-validation-status? candidate observations-present preloaded-verdict-only harness-pass) => blocked-hand-authored-verdict
;; !(q-evo-restart-proof-status? candidate before-present after-restored not-imported-queryable) => blocked-dark-file
;; !(q-evo-soul-approval-status? candidate validation-eligible restart-restored approval-absent) => blocked-no-soul-approval
;; !(q-evo-durable-canon-status? candidate ground-atom import-live soul-approved revision-path-present) => durable-canon-active
;; !(q-tfs2-trace-verdict? same-start metabolizing-transition metabolized-protection) => metabolization-candidate
;; !(q-tfs2-trace-verdict? same-start stuck-recurrence-warning defensive-fixation-risk) => blocked-defensive-fixation
;; !(q-evo-suspicion-delta? stuck-recurrence contactability-flat warrant-flat recurrence-repeated) => suspicion-rises
;; !(q-v08-7-file-class-status? soul-durable-metta journal-class semantic-gates-present) => v1-accepted-mechanical-append-class
;; !(q-v08-7-path-discipline? relative-soul-path allowlisted) => blocked-wrong-path-form
;; !(q-v08-7-write-operation-status? write-file canonical-allowlisted journal-class approved) => blocked-truncate-risk
;; !(q-v08-7-serialization-status? unreduced-call-form ascii-safe) => blocked-unreduced-storage
;; !(q-v08-7-import-liveness? file-exists not-imported queryable-after-restart) => blocked-dark-file
;; !(q-v08-7-boot-safety? malformed-line recovery-unknown) => blocked-boot-poison-risk
;; !(q-v08-7-negative-control? recurrence-without-metabolization durable-canon-claimed) => blocked-recurrence-not-reinforcement

;; Harness obligations:
(q-v08-7-harness-target topology-declared)
(q-v08-7-harness-target lifecycle-reduces)
(q-v08-7-harness-target candidate-canon-separation-reduces)
(q-v08-7-harness-target soul-approval-gate-reduces)
(q-v08-7-harness-target tfs2-polarity-dynamics-reduces)
(q-v08-7-harness-target suspicion-dynamics-reduces)
(q-v08-7-harness-target file-class-v1-decision-reduces)
(q-v08-7-harness-target path-discipline-reduces)
(q-v08-7-harness-target write-operation-boundary-reduces)
(q-v08-7-harness-target serialization-contract-reduces)
(q-v08-7-harness-target import-liveness-reduces)
(q-v08-7-harness-target boot-safety-reduces)
(q-v08-7-harness-target support-surface-boundaries-reduce)
(q-v08-7-harness-target negative-controls-block)
(q-v08-7-harness-target engine-purity-preserved)

;; Runtime filesystem/restart probes are harness-only:
;; - Create / discover soul/evolutionary/* files.
;; - Confirm soul/durable.metta canonical path and journal-class v1 route.
;; - Confirm append vs write/truncate boundary.
;; - Confirm ground atom serialization before imported file append.
;; - Confirm import-chain liveness after restart.
;; - Confirm process memory is not canon.
;; - Confirm optional findings / Genesis interoperability does not canonize.
;; - Probe malformed-line boot behavior only in throwaway target.

;; ---------------------------------------------------------------------------
;; v08.7.2 Hyperseed durability completion ladder tier
;; ---------------------------------------------------------------------------
(q-v08-7-2-ladder-tier H0 hyperseed-field-coverage)
(q-v08-7-2-ladder-tier H1 hyperseed-semantic-reductions)
(q-v08-7-2-ladder-tier H2 hyperseed-negative-controls)
(q-v08-7-2-ladder-tier H3 import-candidate-readiness)

(q-v08-7-2-harness-target hyperseed-fields-present)
(q-v08-7-2-harness-target context-status-reduces)
(q-v08-7-2-harness-target pbit-evidence-reduces)
(q-v08-7-2-harness-target proto-time-reduces)
(q-v08-7-2-harness-target structural-signature-reduces)
(q-v08-7-2-harness-target continuity-degree-reduces)
(q-v08-7-2-harness-target artifact-lineage-reduces)
(q-v08-7-2-harness-target resource-cost-reduces)
(q-v08-7-2-harness-target cross-context-transfer-reduces)
(q-v08-7-2-harness-target approximation-bound-reduces)
(q-v08-7-2-harness-target hyperseed-threshold-reduces)
(q-v08-7-2-harness-target import-candidate-status-reduces)
(q-v08-7-2-harness-target hyperseed-negative-controls-block)

(q-v08-7-2-ladder-probe H1 context-valid "!(q-hyperseed-context-status? context-present observer-bound aspect-indexed)" context-valid)
(q-v08-7-2-ladder-probe H1 pbit-evidence-valid "!(q-hyperseed-evidence-pbit-status? support-opposition-present confidence-graded contradiction-visible)" pbit-evidence-valid)
(q-v08-7-2-ladder-probe H1 proto-time-valid "!(q-hyperseed-proto-time-status? window-present recurrence-observed interval-known)" proto-time-valid)
(q-v08-7-2-ladder-probe H1 structural-signature-valid "!(q-hyperseed-structural-signature-status? signature-present invariant-named degradation-measured)" structural-signature-valid)
(q-v08-7-2-ladder-probe H1 continuity-valid "!(q-hyperseed-continuity-degree-status? degree-present above-threshold degradation-known)" continuity-valid)
(q-v08-7-2-ladder-probe H1 artifact-lineage-valid "!(q-hyperseed-artifact-lineage-status? source-present approval-present revision-path-present)" artifact-lineage-valid)
(q-v08-7-2-ladder-probe H2 file-survival-negative "!(q-v08-7-2-negative-control? file-survival durable-growth-claimed)" blocked-file-survival-not-structural-durability)
(q-v08-7-2-ladder-probe H2 contextless-negative "!(q-v08-7-2-negative-control? contextless-claim durable-growth-claimed)" blocked-context-missing)
(q-v08-7-2-ladder-probe H3 threshold-pass "!(q-v08-7-2-durable-growth-threshold? context-valid pbit-evidence-valid proto-time-valid structural-signature-valid continuity-valid artifact-lineage-valid resource-cost-valid approximation-valid)" hyperseed-durability-threshold-pass)
(q-v08-7-2-ladder-probe H3 import-candidate-ready "!(q-v08-7-2-import-candidate-status? v08-7-semantic-green governance-green hyperseed-threshold-pass)" import-candidate-ready)
;; v08.7.2 compatibility harness targets under the v08.7 target head.
(q-v08-7-harness-target hyperseed-fields-present)
(q-v08-7-harness-target context-status-reduces)
(q-v08-7-harness-target pbit-evidence-reduces)
(q-v08-7-harness-target proto-time-reduces)
(q-v08-7-harness-target structural-signature-reduces)
(q-v08-7-harness-target continuity-degree-reduces)
(q-v08-7-harness-target artifact-lineage-reduces)
(q-v08-7-harness-target resource-cost-reduces)
(q-v08-7-harness-target cross-context-transfer-reduces)
(q-v08-7-harness-target approximation-bound-reduces)
(q-v08-7-harness-target hyperseed-threshold-reduces)
(q-v08-7-harness-target import-candidate-status-reduces)
(q-v08-7-harness-target hyperseed-negative-controls-block)
