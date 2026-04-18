(= (retrieve-weight default) (stv 1.0 0.9))
(= (reinforce-positive $w) (+ $w 0.1))
(= (reinforce-negative $w) (- $w 0.2))
(= (decay-toward-baseline $w) (+ (* 0.95 $w) (* 0.05 1.0)))

;; Context-sensitive weight: (weight memory-id domain) -> stv
;; A memory has different weights in different domains
;; This mirrors mycelial local gradient sensitivity
(= (context-weight mem1 domain-a) (stv 1.0 0.8))
(= (context-weight mem1 domain-b) (stv 1.0 0.3))