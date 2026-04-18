;; Self-Weaving Web Detection v2 - Deterministic closure

(= (closure-strength-v2 soul-value)
   (q-join (regenerates q-revise soul-value) (regenerates value-tension soul-value)))

(= (closure-strength-v2 value-alignment)
   (regenerates soul-value value-alignment))

(= (closure-strength-v2 value-tension)
   (q-join (regenerates soul-value value-tension) (regenerates q-neg value-tension)))

(= (closure-strength-v2 soul-coherence)
   (regenerates q-meet soul-coherence))

(= (web-vitality-v2)
   (q-meet (closure-strength-v2 soul-value)
   (q-meet (closure-strength-v2 value-alignment)
   (q-meet (closure-strength-v2 value-tension)
           (closure-strength-v2 soul-coherence)))))