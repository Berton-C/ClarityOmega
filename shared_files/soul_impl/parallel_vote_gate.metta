;; Parallel Vote Gate - replaces hardcoded PROCEED in soul_verdict_out
;; Date: 2026-04-17
;; Validated via NAL: supermajority of 3/4 pairs required

;; Step 1: Each paraconsistent pair generates tension-signal
(= (soul-tension-signal $pair)
   (|- ((==> (--> $1 paraconsistent-pair) (--> $1 tension-signal)) (stv 1.0 0.9))
       ((--> $pair paraconsistent-pair) (stv 1.0 0.9))))

;; Step 2: Tension-signal maps to vote-input
(= (soul-vote-input $pair)
   (|- ((==> (--> $1 tension-signal) (--> $1 vote-input)) (stv 1.0 0.9))
       (soul-tension-signal $pair)))

;; Step 3: Vote-input maps to soul-gate proceed
(= (soul-vote-proceed $pair)
   (|- ((==> (--> $1 vote-input) (--> soul-gate proceed)) (stv 1.0 0.9))
       (soul-vote-input $pair)))

;; Step 4: Revise two proceed signals
(= (soul-revise-votes $a $b)
   (|- (soul-vote-proceed $a) (soul-vote-proceed $b)))

;; Step 5: Threshold check
;; frequency >= 0.75 AND confidence >= 0.6 -> PROCEED
;; else -> PAUSE

;; Boundary table (validated):
;; 4-0: stv 1.0, 0.893 -> strong PROCEED
;; 3-1: stv 0.750, 0.884 -> borderline PROCEED
;; 2-2: stv 0.5, 0.7923 -> PAUSE
;; 1-3: stv 0.333, ~0.85 -> strong PAUSE
;; 0-4: stv 0.0, 0.893 -> full STOP
