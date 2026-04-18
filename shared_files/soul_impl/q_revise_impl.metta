;; q-revise implementation - NAL revision rule
;; Merges two independent evidence streams
;; Formula: s_new = (s1*c1 + s2*c2)/(c1+c2), c_new = (c1+c2)/(c1+c2+1)
(= (q-revise (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (/ (+ (* $s1 $c1) (* $s2 $c2)) (+ $c1 $c2))
            (/ (+ $c1 $c2) (+ (+ $c1 $c2) 1))))