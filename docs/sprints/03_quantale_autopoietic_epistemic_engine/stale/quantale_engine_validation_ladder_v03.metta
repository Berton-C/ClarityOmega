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
