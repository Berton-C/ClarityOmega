;; lib_nal_extended.metta -- ClarityClaw NAL extensions
;; Builds on lib_nal.metta foundation
;; Pure MeTTa, no Python

;; --- Expectation calculation ---
;; Expectation = confidence * freq - 0.5 + 0.5
(= (expectation (stv $f $c)) (+ (* $c (- $f 0.5)) 0.5))

;; --- Two-step deduction chain ---
;; Given A->B and B->C, derives A->C via |-
(= (chain2 $ab $bc)
   (|- $ab $bc))

;; --- Three-step deduction chain ---
;; Given A->B, B->C, C->D derives A->D
(= (chain3 $ab $bc $cd)
   (let $ac (|- $ab $bc)
     (|- $ac $cd)))

;; --- Revision accumulator ---
;; Revises two same-term evidence into compound
(= (revise-pair $e1 $e2) (|- $e1 $e2))

;; --- Tension detector ---
;; Two statements about same term with opposing frequency
;; Returns tension magnitude as frequency gap
(= (tension? ((--> $s $p) (stv $f1 $c1)) ((--> $s $p) (stv $f2 $c2)))
   (let $gap (abs (- $f1 $f2))
     (if (> $gap 0.4) (tension $s $p $gap) (no-tension))))
