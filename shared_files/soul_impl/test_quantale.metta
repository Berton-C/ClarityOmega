;; Test: can MeTTa compute with quantale ops?
(= (qm (P $f1 $c1) (P $f2 $c2)) (P (* $f1 $f2) (* $c1 $c2)))

;; Query
!(qm (P 0.9 0.85) (P 0.8 0.82))
