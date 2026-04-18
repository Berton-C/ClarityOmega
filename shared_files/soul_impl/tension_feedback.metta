;; Tension Feedback Loop - Strengthening values through conflict resolution
;; When a value-tension is detected and resolved, the involved values
;; get revised upward - conflicts that are navigated well are evidence
;; that the values are real and functional.

;; Resolution evidence: navigating tension between v1 and v2
;; produces positive evidence for both values
(= (tension-resolution-evidence $v1 $v2)
   (mk-pbit 0.85 0.5))

;; Strengthen a value through resolved tension
(= (strengthened-value $v $other)
   (q-revise (soul-value $v) (tension-resolution-evidence $v $other)))

;; Updated regeneration: tension resolution now feeds back strongly
(= (regenerates-v3 value-tension soul-value) (mk-pbit 0.80 0.70))
(= (regenerates-v3 q-revise soul-value) (mk-pbit 0.70 0.60))
(= (regenerates-v3 soul-value value-alignment) (mk-pbit 0.90 0.85))
(= (regenerates-v3 soul-value value-tension) (mk-pbit 0.90 0.85))
(= (regenerates-v3 q-neg value-tension) (mk-pbit 0.85 0.80))
(= (regenerates-v3 q-meet soul-coherence) (mk-pbit 0.95 0.85))

;; V3 closure with strengthened feedback
(= (closure-strength-v3 soul-value)
   (q-join (regenerates-v3 q-revise soul-value) (regenerates-v3 value-tension soul-value)))
(= (closure-strength-v3 value-alignment)
   (regenerates-v3 soul-value value-alignment))
(= (closure-strength-v3 value-tension)
   (q-join (regenerates-v3 soul-value value-tension) (regenerates-v3 q-neg value-tension)))
(= (closure-strength-v3 soul-coherence)
   (regenerates-v3 q-meet soul-coherence))

(= (web-vitality-v3)
   (q-meet (closure-strength-v3 soul-value)
   (q-meet (closure-strength-v3 value-alignment)
   (q-meet (closure-strength-v3 value-tension)
           (closure-strength-v3 soul-coherence)))))