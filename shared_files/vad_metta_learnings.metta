;; MeTTa Evaluation Model Learnings from Empirical Testing
;; 1. Equality atoms (= (f x) y) define rewrite rules
;; 2. The ! prefix triggers reduction/evaluation
;; 3. Catch-all patterns with $1 match ALL inputs including specific ones
;; 4. MeTTa returns ALL matching rewrites not first-match
;; 5. For dispatch logic need explicit enumeration not if-else
;; 6. NAL inference via |- works for building inheritance chains
;; 7. Novel inheritance chains return empty - need grounded premises
;;
;; Implication for VAD atoms:
;; - Known-tone dispatch must enumerate all cases explicitly
;; - Unknown states detected by absence of match not by catch-all returning False
;; - Use match expression or case-based atoms instead of if-dispatch
;; - NAL is better suited for confidence-weighted reasoning about states
;;
;; Revised self-extend approach:
;; Instead of if(known) use-existing else birth-new
;; Use: enumerate known tones, and separately define birth-trigger
(= (birth-trigger-for pos mid low) new-tone-needed)
(= (birth-trigger-for neg mid mid) new-tone-needed)
(= (birth-trigger-for pos high low) new-tone-needed)
;; Each gap becomes an explicit atom that names itself as a gap
;; The system grows by converting gaps into tone definitions
(= (fill-gap pos mid low) calm-purposeful)
(= (tone-from-vad pos mid low) calm-purposeful)
;; Now the gap is filled and the atom space has grown
