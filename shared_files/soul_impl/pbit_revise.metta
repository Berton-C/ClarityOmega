;; NAL-compatible revision for p-bits
;; s_new = weighted avg by confidence, c_new = c1+c2-c1*c2

(= (q-revise (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (/ (+ (* $s1 $c1) (* $s2 $c2)) (+ $c1 $c2))
            (- (+ $c1 $c2) (* $c1 $c2))))