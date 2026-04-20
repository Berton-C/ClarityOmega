;; lib_nal_extended.metta -- Extended NAL reasoning functions
;; Pure (= ...) definitions. No imports, no side effects.
;; Extends Patrick's lib_nal without touching it.

;; Abduction: (A-->B, A-->C) => (B-->C) with f=1.0, c=f_a*c_a*c_b/(f_a*c_a*c_b + k)
(= (abduction ($f1 $c1) ($f2 $c2))
   (let* (($k 1.0)
          ($num (* (* $f1 $c1) $c2))
          ($den (+ $num $k))
          ($f 1.0)
          ($c (/ $num $den)))
     ($f $c)))

;; Induction: (A-->B, C-->B) => (A-->C) with f=f_b, c=f_b*c_a*c_b/(f_b*c_a*c_b + k)
(= (induction ($f1 $c1) ($f2 $c2))
   (let* (($k 1.0)
          ($num (* (* $f2 $c1) $c2))
          ($den (+ $num $k))
          ($f $f2)
          ($c (/ $num $den)))
     ($f $c)))

;; Exemplification: (A-->B, B-->C) => (C-->A) with f=1.0, c=f_a*f_b*c_a*c_b/(f_a*f_b*c_a*c_b + k)
(= (exemplification ($f1 $c1) ($f2 $c2))
   (let* (($k 1.0)
          ($num (* (* (* $f1 $f2) $c1) $c2))
          ($den (+ $num $k))
          ($f 1.0)
          ($c (/ $num $den)))
     ($f $c)))

;; Comparison: (A-->B, A-->C) => (B<->C) with f=f_a*f_b, c=...
(= (comparison ($f1 $c1) ($f2 $c2))
   (let* (($k 1.0)
          ($f (* $f1 $f2))
          ($num (* (* $f1 $c1) $c2))
          ($den (+ $num $k))
          ($c (/ $num $den)))
     ($f $c)))
