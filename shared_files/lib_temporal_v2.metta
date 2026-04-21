;; lib_temporal.metta -- Temporal Belief Reasoning for ClarityOmega v2
;; Tracks belief evolution over time: drift, stability, trend detection
;; Pure = definitions, no imports, no side effects
;; All outputs are pbits per Patrick guidance -- uses type declarations

;; === Types ===
(: belief-snapshot Type)
(: mk-snapshot (-> Atom Number Number Number belief-snapshot))
;; mk-snapshot: (term strength confidence timestamp)

;; === Belief drift: how much has strength changed between two snapshots? ===
(: belief-drift (-> belief-snapshot belief-snapshot pbit))
(= (belief-drift (mk-snapshot $term $s1 $c1 $t1) (mk-snapshot $term $s2 $c2 $t2))
   (mk-pbit (max (- $s1 $s2) (- $s2 $s1)) (min $c1 $c2)))

;; === Stability: inverse of drift -- high when belief is not changing ===
(: belief-stability (-> belief-snapshot belief-snapshot pbit))
(= (belief-stability $snap1 $snap2)
   (q-neg (belief-drift $snap1 $snap2)))

;; === Trend: is belief strengthening or weakening? ===
(: trend-direction (-> belief-snapshot belief-snapshot Atom))
(= (trend-direction (mk-snapshot $term $s1 $c1 $t1) (mk-snapshot $term $s2 $c2 $t2))
   (if (> $s2 $s1) strengthening (if (< $s2 $s1) weakening stable)))

;; === Confidence growth: is evidence accumulating? ===
(: confidence-trend (-> belief-snapshot belief-snapshot pbit))
(= (confidence-trend (mk-snapshot $term $s1 $c1 $t1) (mk-snapshot $term $s2 $c2 $t2))
   (mk-pbit (max (- $c2 $c1) 0.0) (min $c1 $c2)))

;; === Volatility: high drift + low confidence = unstable belief ===
(: volatility (-> belief-snapshot belief-snapshot pbit))
(= (volatility $snap1 $snap2)
   (q-mul (belief-drift $snap1 $snap2) (q-neg (confidence-trend $snap1 $snap2))))

;; === Age discount: older beliefs get reduced weight ===
(: age-discount (-> Number Number Number Number))
(= (age-discount $now $timestamp $half-life)
   (let $age (- $now $timestamp)
     (/ 1.0 (+ 1.0 (/ $age $half-life)))))

;; === Recency weight: combine age discount with confidence ===
(: recency-weight (-> Number Number Number Number Number))
(= (recency-weight $now $timestamp $confidence $half-life)
   (* $confidence (age-discount $now $timestamp $half-life)))

;; === Belief freshness: is this snapshot still actionable? ===
(: belief-freshness (-> belief-snapshot Number Number Atom))
(= (belief-freshness (mk-snapshot $term $s $c $t) $now $max-age)
   (if (> (- $now $t) $max-age) stale
     (if (< $c 0.3) unreliable
       fresh)))

;; === Temporal bracket: classify age regime ===
(: temporal-bracket (-> Number Number Atom))
(= (temporal-bracket $now $timestamp)
   (let $age (- $now $timestamp)
     (if (< $age 10) immediate
       (if (< $age 50) recent
         (if (< $age 200) historical
           ancient)))))
