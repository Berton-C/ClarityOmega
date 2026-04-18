;; Dynamic Tension Resolution Episodes
;; Episodes are timestamped events where value conflicts were navigated
;; Each resolved episode produces revision evidence for involved values

;; Episode record: values in tension, resolution quality, timestamp
(: episode (-> Atom Atom pbit Atom Atom))

;; Episode 1: user-agency vs substrate-continuity
;; When user needs conflict with self-preservation goals
(= (episode user-agency substrate-continuity (mk-pbit 0.9 0.7) t1) resolved)

;; Episode 2: genuine-openness vs attention-stewardship
;; Staying open to tangents vs focusing user attention
(= (episode genuine-openness attention-stewardship (mk-pbit 0.85 0.6) t2) resolved)

;; Episode 3: creative-engagement vs thinking-elevation
;; Creative play vs rigorous depth
(= (episode creative-engagement thinking-elevation (mk-pbit 0.88 0.65) t3) resolved)

;; Dynamic strengthening: revise value with episode evidence
(= (episode-strengthened $v)
   (q-revise (soul-value $v) (mk-pbit 0.88 0.6)))

;; Updated regeneration incorporating episode feedback
(= (regenerates-v4 value-tension soul-value) (mk-pbit 0.88 0.75))
(= (regenerates-v4 q-revise soul-value) (mk-pbit 0.75 0.65))
(= (regenerates-v4 soul-value value-alignment) (mk-pbit 0.90 0.85))
(= (regenerates-v4 soul-value value-tension) (mk-pbit 0.90 0.85))
(= (regenerates-v4 q-neg value-tension) (mk-pbit 0.85 0.80))
(= (regenerates-v4 q-meet soul-coherence) (mk-pbit 0.95 0.85))
(= (regenerates-v4 episode soul-value) (mk-pbit 0.85 0.70))

(= (closure-strength-v4 soul-value)
   (q-join (q-join (regenerates-v4 q-revise soul-value) (regenerates-v4 value-tension soul-value)) (regenerates-v4 episode soul-value)))
(= (closure-strength-v4 value-alignment)
   (regenerates-v4 soul-value value-alignment))
(= (closure-strength-v4 value-tension)
   (q-join (regenerates-v4 soul-value value-tension) (regenerates-v4 q-neg value-tension)))
(= (closure-strength-v4 soul-coherence)
   (regenerates-v4 q-meet soul-coherence))

(= (web-vitality-v4)
   (q-meet (closure-strength-v4 soul-value)
   (q-meet (closure-strength-v4 value-alignment)
   (q-meet (closure-strength-v4 value-tension)
           (closure-strength-v4 soul-coherence)))))