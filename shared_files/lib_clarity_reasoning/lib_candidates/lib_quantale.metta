;; lib_quantale.metta -- Quantale composition for truth value algebra
;; Pure (= ...) definitions. No imports, no side effects.
;; Defines composition operators on (frequency confidence) pairs.

;; Quantale meet: min-based composition (cautious merge)
(= (q-meet ($f1 $c1) ($f2 $c2))
   (let* (($f (min $f1 $f2))
          ($c (min $c1 $c2)))
     ($f $c)))

;; Quantale join: max-based composition (optimistic merge)
(= (q-join ($f1 $c1) ($f2 $c2))
   (let* (($f (max $f1 $f2))
          ($c (min $c1 $c2)))
     ($f $c)))

;; Quantale tensor: multiplicative composition (chained evidence)
(= (q-tensor ($f1 $c1) ($f2 $c2))
   (let* (($f (* $f1 $f2))
          ($c (* $c1 $c2)))
     ($f $c)))

;; Quantale residual: implication strength (if A then how much B)
(= (q-residual ($f1 $c1) ($f2 $c2))
   (let* (($f (if (< $f1 0.001) 1.0 (min 1.0 (/ $f2 $f1))))
          ($c (* $c1 $c2)))
     ($f $c)))

;; Confidence-weighted blend: weighted average by confidence
(= (q-blend ($f1 $c1) ($f2 $c2))
   (let* (($total (+ $c1 $c2))
          ($f (if (< $total 0.001) 0.5 (/ (+ (* $f1 $c1) (* $f2 $c2)) $total)))
          ($c (max $c1 $c2)))
     ($f $c)))
