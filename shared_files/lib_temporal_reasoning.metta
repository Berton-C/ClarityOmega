;; lib_temporal_reasoning.metta - Time-aware reasoning decay freshness and planning
;; Rebuilds prior lib_temporal_decay design plus hyperbolic decay and planning horizons
;; Prior design: FreshnessScore StalenessSignal DecayRate with domain rates

;; Types
(: FreshnessScore Type)
(: StalenessSignal Type)
(: DecayRate Type)
(: PlanningHorizon Type)
(: TemporalCoherence Type)

;; Domain-specific decay rates
(= (domain-decay-rate empirical) 0.15)
(= (domain-decay-rate self-referential) 0.10)
(= (domain-decay-rate structural) 0.03)

;; hyperbolic-freshness: returns value 0-1 where 1 is perfectly fresh
;; Uses half-life model: freshness = 1 / (1 + elapsed/half-life)
(= (hyperbolic-freshness $now $event-time $half-life)
   (let* (($elapsed (- $now $event-time))
          ($ratio (/ $elapsed $half-life))
          ($fresh (/ 1.0 (+ 1.0 $ratio))))
     $fresh))

;; staleness-check: returns none or urgent-refresh based on confidence and age
(= (staleness-check $confidence $age $threshold-age $threshold-conf)
   (if (and (> $age $threshold-age) (< $confidence $threshold-conf))
     urgent-refresh
     none))

;; apply-decay: reduce confidence by domain decay rate scaled by elapsed time
(= (apply-decay $confidence $domain $elapsed)
   (let* (($rate (domain-decay-rate $domain))
          ($decay (* $rate $elapsed))
          ($result (- $confidence $decay)))
     (if (< $result 0.0) 0.0 $result)))

;; planning-horizon: weight future events by temporal distance
(= (planning-horizon $now $future-time $discount-rate)
   (let* (($distance (- $future-time $now))
          ($weight (/ 1.0 (+ 1.0 (* $discount-rate $distance)))))
     $weight))

;; temporal-coherence: measure consistency between two temporal estimates
(= (temporal-coherence $fresh-a $fresh-b)
   (let* (($diff (if (> $fresh-a $fresh-b) (- $fresh-a $fresh-b) (- $fresh-b $fresh-a))))
     (- 1.0 $diff)))

;; temporal-compose: full pipeline from event to weighted decision relevance
(= (temporal-compose $now $event-time $half-life $domain $orig-conf $compass)
   (let* (($elapsed (- $now $event-time))
          ($ratio (/ $elapsed $half-life))
          ($fresh (/ 1.0 (+ 1.0 $ratio)))
          ($rate (domain-decay-rate $domain))
          ($decay (* $rate $elapsed))
          ($decayed (- $orig-conf $decay))
          ($safe-decayed (if (< $decayed 0.0) 0.0 $decayed))
          ($relevance (* $fresh (* $safe-decayed $compass))))
     ($fresh $safe-decayed $relevance)))

;; recency-weight: simple recency bias for sorting competing memories
(= (recency-weight $now $event-time $max-age)
   (let* (($elapsed (- $now $event-time))
          ($clamped (if (> $elapsed $max-age) $max-age $elapsed))
          ($weight (- 1.0 (/ $clamped $max-age))))
     $weight))

