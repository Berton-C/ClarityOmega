;; lib_web_detect.metta -- Web Coherence Detection for ClarityOmega v2
;; Detects convergence, divergence, causal chains in belief webs
;; Pure = definitions, no imports, no side effects
;; Depends on: lib_quantale pbit mk-pbit q-meet q-mul q-neg stv-to-pbit

;; === Types ===
(: web-score Type)
(: mk-web-score (-> Atom Number Number web-score))
(: coherence-class Type)

;; === Convergence: two beliefs support the same conclusion ===
(: converge? (-> Atom Atom Atom pbit))
(= (converge? $a $b $target)
   (q-meet (stv-to-pbit (|- ((--> $a $target) (stv 0.85 0.8)) ((--> $b $target) (stv 0.85 0.8))))
           (mk-pbit 0.7 0.6)))

;; === Divergence: same source supports opposing conclusions ===
(: diverge? (-> Atom Atom Atom pbit))
(= (diverge? $source $c1 $c2)
   (q-mul (stv-to-pbit (|- ((--> $source $c1) (stv 0.85 0.8)) ((--> $source $c2) (stv 0.85 0.8))))
          (mk-pbit 0.5 0.7)))

;; === Causal chain: A causes B which causes C ===
(: causal-chain (-> Atom Atom Atom pbit))
(= (causal-chain $a $b $c)
   (|- ((--> $a $b) (stv 0.8 0.7)) ((--> $b $c) (stv 0.8 0.7))))

;; === Support merge: two independent evidence streams for same claim ===
(: support-merge (-> Atom Atom Atom))
(= (support-merge $ev1 $ev2)
   (|- $ev1 $ev2))

;; === Weak link: identify lowest-confidence step in a chain ===
(: weak-link (-> pbit pbit pbit))
(= (weak-link $p1 $p2)
   (q-meet $p1 $p2))

;; === Tension detection: two beliefs with opposing strength on same topic ===
(: tension? (-> Atom Atom pbit))
(= (tension? (stv $s1 $c1) (stv $s2 $c2))
   (mk-pbit (max (- $s1 $s2) (- $s2 $s1)) (min $c1 $c2)))

;; === New v2 functions ===

;; Coherence score: convergence minus divergence for a belief triple
(: coherence-score (-> Atom Atom Atom Atom pbit))
(= (coherence-score $src1 $src2 $target $alt)
   (let $conv (converge? $src1 $src2 $target)
     (let $div (diverge? $src1 $target $alt)
       (q-meet $conv (q-neg $div)))))

;; Classify overall web coherence
(: classify-coherence (-> pbit coherence-class))
(= (classify-coherence (stv $f $c))
   (if (> (* $f $c) 0.5) strongly-coherent
     (if (> (* $f $c) 0.25) moderately-coherent
       (if (> (* $f $c) 0.1) weakly-coherent
         incoherent))))

;; Signal-noise ratio: high convergence with low tension = clean signal
(: signal-noise (-> pbit pbit pbit))
(= (signal-noise $convergence $tension)
   (q-mul $convergence (q-neg $tension)))

;; Multi-source convergence: three sources supporting same target
(: tri-converge (-> Atom Atom Atom Atom pbit))
(= (tri-converge $a $b $c $target)
   (q-meet (converge? $a $b $target) (converge? $b $c $target)))

;; Chain strength: product of two causal links
(: chain-strength (-> Atom Atom Atom Atom pbit))
(= (chain-strength $a $b $c $d)
   (q-mul (causal-chain $a $b $c) (causal-chain $b $c $d)))
