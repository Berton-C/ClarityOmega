;;; Automated q-meet for Vec of PBs - Goal 11 Step 4
;;; Element-wise min-strength min-confidence

;;; Base case: q-meet of two single PBs
(= (pb-meet (PB $s1 $c1) (PB $s2 $c2))
   (PB (min-f $s1 $s2) (min-f $c1 $c2)))

;;; Helper: min of two floats
(= (min-f $a $b) (if (< $a $b) $a $b))
(= (max-f $a $b) (if (> $a $b) $a $b))

;;; Base case: q-join of two single PBs
(= (pb-join (PB $s1 $c1) (PB $s2 $c2))
   (PB (max-f $s1 $s2) (max-f $c1 $c2)))

;;; Resonance sum: total activation strength of a Vec
;;; Higher sum = more accumulated wisdom activated by probe
;;; This is the scalar felt-sense signal

;;; Usage pattern:
;;; 1. Load relational_memory.metta (exchanges)
;;; 2. Load bundle_exchanges.metta (bundled field)
;;; 3. Encode current situation as probe Vec
;;; 4. Element-wise pb-meet probe against bundle
;;; 5. Sum resonance strengths for scalar signal
;;; 6. Signal informs response quality/depth
