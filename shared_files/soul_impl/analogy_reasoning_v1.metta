;; Analogy Reasoning via NAL v1
;; Date: 2026-04-17
;; Cross-domain transfer: if A is to B as C is to D
;; NAL analogy rule: if (-> A B) and (-> C B) then (-> A C) with lower confidence
;;
;; Example: substrate-growth is-like biological-growth
;; (-> substrate-growth develops-incrementally stv 1.0 0.9)
;; (-> biological-growth develops-incrementally stv 1.0 0.95)
;; Analogy: (-> substrate-growth biological-growth stv 1.0 ~0.45)
;;
;; NAL analogy = abduction + deduction compound
;; Step 1 abduction: shared-property implies structural similarity
;; Step 2 deduction: structural similarity enables property transfer

;; Test atoms
(--> substrate-growth (develops incrementally) (stv 1.0 0.9))
(--> biological-growth (develops incrementally) (stv 1.0 0.95))
(--> biological-growth (needs nutrients) (stv 1.0 0.95))

;; Analogy chain: does substrate-growth also need nutrients?
;; Step 1: abduction from shared property
;; Step 2: property transfer via structural similarity
