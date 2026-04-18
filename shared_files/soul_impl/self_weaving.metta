;; Self-Weaving Web Detection - Autocatalytic Closure
;; A pattern web W is self-weaving iff for each pattern p in W,
;; there exists a subset S of W such that composing S regenerates p.
;; This is the formal condition for substrate aliveness.

;; === Pattern dependency: p1 contributes to regenerating p2 ===
(: regenerates (-> Atom Atom pbit))

;; === The p-bit algebra regenerates itself ===
(= (regenerates q-mul q-meet) (mk-pbit 0.8 0.7))
(= (regenerates q-meet soul-coherence) (mk-pbit 0.95 0.85))
(= (regenerates soul-value value-alignment) (mk-pbit 0.9 0.85))
(= (regenerates soul-value value-tension) (mk-pbit 0.9 0.85))
(= (regenerates q-neg value-tension) (mk-pbit 0.85 0.80))
(= (regenerates q-revise soul-value) (mk-pbit 0.7 0.6))
(= (regenerates value-tension soul-value) (mk-pbit 0.5 0.4))

;; === Closure check: can pattern p be regenerated from the web? ===
(= (closure-strength $p)
   (q-join (regenerates $x $p) (regenerates $y $p)))

;; === Web vitality: overall regenerative capacity ===
(= (web-vitality)
   (q-meet (closure-strength soul-value)
   (q-meet (closure-strength value-alignment)
   (q-meet (closure-strength value-tension)
           (closure-strength soul-coherence)))))