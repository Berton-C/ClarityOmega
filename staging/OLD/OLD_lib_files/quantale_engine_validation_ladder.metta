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
