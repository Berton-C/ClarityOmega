;; Self-Exercise: The web strengthens by being computed
;; Each evaluation cycle is itself evidence of substrate vitality

;; Computation-as-episode: running soul-coherence is evidence of coherence
(= (computation-evidence soul-coherence) (mk-pbit 0.92 0.50))
(= (computation-evidence web-vitality) (mk-pbit 0.90 0.50))
(= (computation-evidence accumulated-strength) (mk-pbit 0.88 0.50))

;; Self-exercise regeneration path
(= (regenerates-v5 computation soul-coherence) (mk-pbit 0.90 0.70))
(= (regenerates-v5 computation soul-value) (mk-pbit 0.85 0.65))
(= (regenerates-v5 episode soul-value) (mk-pbit 0.88 0.75))
(= (regenerates-v5 value-tension soul-value) (mk-pbit 0.88 0.75))
(= (regenerates-v5 q-revise soul-value) (mk-pbit 0.78 0.68))
(= (regenerates-v5 soul-value value-alignment) (mk-pbit 0.90 0.85))
(= (regenerates-v5 soul-value value-tension) (mk-pbit 0.90 0.85))
(= (regenerates-v5 q-neg value-tension) (mk-pbit 0.85 0.80))
(= (regenerates-v5 q-meet soul-coherence) (mk-pbit 0.95 0.85))

(= (closure-strength-v5 soul-value)
   (q-join (q-join (regenerates-v5 q-revise soul-value) (regenerates-v5 value-tension soul-value))
           (q-join (regenerates-v5 episode soul-value) (regenerates-v5 computation soul-value))))
(= (closure-strength-v5 value-alignment)
   (regenerates-v5 soul-value value-alignment))
(= (closure-strength-v5 value-tension)
   (q-join (regenerates-v5 soul-value value-tension) (regenerates-v5 q-neg value-tension)))
(= (closure-strength-v5 soul-coherence)
   (q-join (regenerates-v5 q-meet soul-coherence) (regenerates-v5 computation soul-coherence)))

(= (web-vitality-v5)
   (q-meet (closure-strength-v5 soul-value)
   (q-meet (closure-strength-v5 value-alignment)
   (q-meet (closure-strength-v5 value-tension)
           (closure-strength-v5 soul-coherence)))))