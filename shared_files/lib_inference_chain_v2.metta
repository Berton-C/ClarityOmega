;; lib_inference_chain.metta -- Multi-step inference chaining v2
;; Forward and backward chaining with confidence propagation
;; Pure = definitions only, no imports, no side effects

;; Types
(: chain-result Type)
(: mk-chain-result (-> Atom pbit chain-result))
(: chain-quality Type)

;; === Chain confidence: product of step confidences ===
(: chain-confidence (-> pbit pbit pbit))
(= (chain-confidence $step1 $step2)
   (q-mul $step1 $step2))

;; === Termination check: stop chaining below floor ===
(: terminate-check (-> pbit Number Atom))
(= (terminate-check (stv $f $c) $floor)
   (if (< (* $f $c) $floor) terminate continue))

;; === Forward step: derive conclusion from premise + rule ===
(: forward-step (-> Atom Atom pbit))
(= (forward-step $premise $rule)
   (stv-to-pbit (|- $rule $premise)))

;; === Two-step forward chain ===
(: chain-two (-> Atom Atom Atom pbit))
(= (chain-two $premise $rule1 $rule2)
   (let $mid (forward-step $premise $rule1)
     (chain-confidence $mid (forward-step $mid $rule2))))

;; === Backward query: given target, find supporting premise ===
(: backward-query (-> Atom Atom pbit))
(= (backward-query $target $rule)
   (stv-to-pbit (|- $rule ((--> $target query) (stv 1.0 0.5)))))

;; === Select higher confidence between two chains ===
(: select-higher-conf (-> pbit pbit pbit))
(= (select-higher-conf (stv $f1 $c1) (stv $f2 $c2))
   (if (> (* $f1 $c1) (* $f2 $c2)) (stv $f1 $c1) (stv $f2 $c2)))

;; === Confidence gate: only pass if above threshold ===
(: confidence-gate (-> pbit Number pbit))
(= (confidence-gate (stv $f $c) $threshold)
   (if (>= (* $f $c) $threshold) (stv $f $c) (stv 0.0 0.0)))

;; === New v2 functions ===

;; Chain strength: numeric magnitude of chained inference
(: chain-strength (-> pbit Number))
(= (chain-strength (stv $f $c)) (* $f $c))

;; Quality classifier for inference chains
(: classify-chain (-> pbit chain-quality))
(= (classify-chain $p)
   (let $s (chain-strength $p)
     (if (> $s 0.5) strong-chain
       (if (> $s 0.25) moderate-chain
         (if (> $s 0.1) weak-chain
           broken-chain)))))

;; Three-step forward chain with termination checking
(: chain-three (-> Atom Atom Atom Atom Number pbit))
(= (chain-three $premise $r1 $r2 $r3 $floor)
   (let $step1 (forward-step $premise $r1)
     (if (== (terminate-check $step1 $floor) terminate) $step1
       (let $step2 (chain-confidence $step1 (forward-step $step1 $r2))
         (if (== (terminate-check $step2 $floor) terminate) $step2
           (chain-confidence $step2 (forward-step $step2 $r3)))))))

;; Two-step backward chain
(: backward-chain-two (-> Atom Atom Atom pbit))
(= (backward-chain-two $target $rule1 $rule2)
   (let $mid (backward-query $target $rule2)
     (chain-confidence $mid (backward-query $mid $rule1))))

;; Chain report: result plus quality classification
(: chain-report (-> pbit chain-result))
(= (chain-report $p)
   (mk-chain-result (classify-chain $p) $p))

;; Parallel chains: run two chains, pick stronger
(: best-chain (-> pbit pbit chain-result))
(= (best-chain $chain1 $chain2)
   (chain-report (select-higher-conf $chain1 $chain2)))
