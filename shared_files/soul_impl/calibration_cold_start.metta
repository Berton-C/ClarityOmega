;; Calibration Cold Start Graceful Degradation
;; Addresses failure mode: layer1_precompute reads history that doesn't exist yet
;; Solution: tiered fallback based on available calibration count

;; Count available calibration entries
(= (cal-count-tier $count)
   (if (< $count 3) conservative
   (if (< $count 10) moderate
   confident)))

;; Conservative: full brief always, no tier compression
(= (cold-start-brief conservative $soul-context)
   (soul-tier-a-full $soul-context))

;; Moderate: use tier-b with default weights, no learned adjustments
(= (cold-start-brief moderate $soul-context)
   (soul-tier-b-capture-units $soul-context))

;; Confident: normal layer1 precompute with learned weights
(= (cold-start-brief confident $soul-context)
   (layer1-precompute $soul-context))

;; Entry point replaces direct layer1-precompute call
(= (calibration-aware-brief $soul-context $cal-history)
   (cold-start-brief (cal-count-tier (length $cal-history)) $soul-context))
