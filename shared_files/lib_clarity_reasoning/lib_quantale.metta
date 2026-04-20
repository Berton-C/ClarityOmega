;; lib_quantale.metta -- ClarityClaw quantale p-bit algebra
;; Sub-symbolic confidence flow operations
;; Pure MeTTa, no Python

;; --- Quantale meet: minimum confidence floor ---
(= (q-meet (stv $f1 $c1) (stv $f2 $c2))
   (stv (min $f1 $f2) (min $c1 $c2)))

;; --- Quantale join: maximum confidence ceiling ---
(= (q-join (stv $f1 $c1) (stv $f2 $c2))
   (stv (max $f1 $f2) (max $c1 $c2)))

;; --- Quantale multiply: tensor product ---
;; Combines two independent evidence streams
(= (q-mul (stv $f1 $c1) (stv $f2 $c2))
   (stv (* $f1 $f2) (* $c1 $c2)))

;; --- Confidence decay: temporal erosion ---
;; Reduces confidence by decay factor over time
(= (q-decay (stv $f $c) $rate)
   (stv $f (* $c $rate)))

;; --- Threshold gate: only pass if expectation above bar ---
(= (q-gate (stv $f $c) $threshold)
   (let $exp (+ (* $c (- $f 0.5)) 0.5)
     (if (> $exp $threshold)
       (stv $f $c)
       (stv $f 0.0))))

;; --- Evidence weight: positive evidence count analog ---
(= (q-weight (stv $f $c))
   (let $w (/ $c (- 1.0 $c))
     (* $f $w)))
