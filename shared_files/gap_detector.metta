;; Epistemic Gap Detector - MeTTa Native Patterns
;; Threshold check as type-level constraint

;; Define confidence threshold for gap detection
(= (confidence-threshold) 0.3)

;; Extract confidence from an STV
(= (get-confidence (stv $f $c)) $c)

;; Extract frequency from an STV
(= (get-frequency (stv $f $c)) $f)

;; A link is weak if its confidence is below threshold
;; This pattern matches any inheritance with low confidence
(= (is-weak-link (--> $a $b) (stv $f $c))
   (if (< $c (confidence-threshold)) True False))

;; Gap signal generation from weak link detection
(= (gap-signal (--> $a $b) (stv $f $c))
   (if (is-weak-link (--> $a $b) (stv $f $c))
       (learning-target $a $b (- (confidence-threshold) $c))
       none))

;; Chain strength is product of confidences along path
(= (chain-strength (stv $f1 $c1) (stv $f2 $c2))
   (stv (* $f1 $f2) (* $c1 $c2)))
