;; Epistemic Gap Detector v0.1
;; Uses low-confidence atoms as automatic learning goal generators
;; Date: 2026-04-15 23:10

;; Meta-reasoning: confidence signals where attention should go
(--> low-confidence-region epistemic-gap (stv 0.85 0.7))
(--> epistemic-gap learning-target (stv 0.9 0.75))
(--> unknown-territory curiosity-signal (stv 0.9 0.8))
(--> curiosity-signal self-directed-goal (stv 0.85 0.7))

;; Known low-confidence regions from substrate work
;; cross-domain-transfer: validated conceptually but thin empirically
(--> cross-domain-transfer substrate-capability (stv 0.7 0.4))
;; decision-cards: plausible but unobserved in practice
(--> decision-card-effectiveness empirical-validation (stv 0.6 0.225))
;; structural-confidence-ceiling: theoretical, needs formal proof
(--> structural-confidence-ceiling formal-grounding (stv 0.75 0.35))

;; Pattern: low stv confidence flags where to explore next
;; Revision accumulates evidence as exploration proceeds
