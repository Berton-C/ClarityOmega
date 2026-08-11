;; affective_architecture_uncertainty.metta -- VAD model applied to uncertainty navigation
;; Author: ClarityClaw  Date: 2026-06-09
;; Cross-domain: vad-affective -> human uncertainty resilience
;;
;; Core insight: the emotional experience of uncertainty is
;; determined by dominance level, not information quantity.

;; Uncertainty trigger pattern
(= (uncertainty-trigger high-arousal)
   (trigger "Unknown conditions activate arousal before assessment completes." (stv 0.9 0.9)))
(= (uncertainty-trigger low-dominance)
   (trigger "Feeling at effect of unknowns rather than agent within them." (stv 0.9 0.9)))

;; Self-knowledge shifts the dominance axis
(= (self-knowledge-shift dominance-increase)
   (shift "Self-assessment increases dominance. Not by reducing uncertainty but by increasing agency within it." (stv 0.88 0.88)))
(= (self-knowledge-shift arousal-modulation)
   (shift "Knowing your response patterns modulates arousal without eliminating it." (stv 0.85 0.85)))

;; The transformation is affective not informational
(= (affective-transformation same-uncertainty)
   (insight "The uncertainty does not change. Your relationship to it does. This is structural resilience." (stv 0.92 0.85)))

;; VAD-uncertainty navigation equation
(= (navigation-equation uncertainty-resilience)
   (equation "resilience = f(dominance, arousal_modulation) not f(information, certainty)" (stv 0.9 0.85)))

;; Cross-domain bridge
(= (cross-domain-bridge vad-affective uncertainty-navigation)
   (bridge "The VAD model reveals that uncertainty distress is a dominance problem, not an information problem. Self-knowledge increases dominance. Structural resilience is affective." (stv 0.9 0.85)))