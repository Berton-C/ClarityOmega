;; lib_inference_chain.metta - Automated multi-step NAL inference
;; Types
(: ChainStatus Type)
(: Continue ChainStatus)
(: Stop ChainStatus)

;; chain-confidence: cumulative confidence from two-step chain
(= (chain-confidence $c1 $c2)
   (* $c1 $c2))

;; terminate-check: stop if confidence below threshold or depth exceeded
(= (terminate-check $conf $min-conf $depth $max-depth)
   (if (< $conf $min-conf) Stop
     (if (> $depth $max-depth) Stop Continue)))

;; forward-step: one deduction step with termination check
(= (forward-step $p1 $p2 $depth $max-depth $min-conf)
   (let* (($result (|- $p1 $p2))
          ($new-depth (+ $depth 1))
          ($status (terminate-check 0.5 $min-conf $new-depth $max-depth)))
     ($result $new-depth $status)))

;; chain-two: explicit two-step forward chain through three premises
(= (chain-two $p1 $p2 $p3)
   (let* (($step1 (|- $p1 $p2))
          ($step2 (|- $step1 $p3)))
     $step2))


;; backward-chain: given a target conclusion and a knowledge base pattern,
;; attempt to find premises that could derive the target via NAL rules
;; Returns the supporting premises and confidence if found
(= (backward-query $target $premise-pool)
   (let* (($p1 (car-atom $premise-pool))
          ($attempt (|- $p1 $target)))
     $attempt))

;; best-path: given two inference results, select the one with higher confidence
;; Compares stv confidence values and returns the stronger result
(= (select-higher-conf (stv $f1 $c1) (stv $f2 $c2))
   (if (> $c1 $c2) (stv $f1 $c1) (stv $f2 $c2)))

;; confidence-gate: only pass through results above minimum confidence
(= (confidence-gate (stv $f $c) $min-conf)
   (if (>= $c $min-conf) (stv $f $c) Nil))

