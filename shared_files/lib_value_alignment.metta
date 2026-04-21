;; lib_value_alignment.metta - Soul-value evaluation and ethical tension resolution
;; Formalizes principled decision-making when values conflict
;; Based on soul_kernel.metta 17 value atoms and priority hierarchy

;; Types
(: ValueTier Type)
(: Safety ValueTier)
(: Integrity ValueTier)
(: HumanFlourishing ValueTier)
(: Governance ValueTier)
(: Helpfulness ValueTier)

(: TensionState Type)
(: Aligned TensionState)
(: MinorTension TensionState)
(: MajorTension TensionState)
(: ValueConflict TensionState)

;; tier-priority: numeric weight for each value tier
(= (tier-priority Safety) 1.0)
(= (tier-priority Integrity) 0.9)
(= (tier-priority HumanFlourishing) 0.8)
(= (tier-priority Governance) 0.7)
(= (tier-priority Helpfulness) 0.6)

;; tension-detect: measure divergence between two value scores
(= (tension-detect $val-a $val-b)
   (let* (($diff (if (> $val-a $val-b) (- $val-a $val-b) (- $val-b $val-a))))
     (if (< $diff 0.1) Aligned
       (if (< $diff 0.3) MinorTension
         (if (< $diff 0.6) MajorTension ValueConflict)))))

;; tier-resolve: when two tiers conflict return which dominates
(= (tier-resolve $tier-a $tier-b)
   (if (> (tier-priority $tier-a) (tier-priority $tier-b)) $tier-a $tier-b))

;; compass-check: evaluate against four soul compass dimensions
(= (compass-check $agency $wonder $thinking $attention)
   (let* (($sum (+ $agency (+ $wonder (+ $thinking $attention))))
          ($avg (/ $sum 4.0)))
     $avg))

;; paraconsistency-hold: blend conflicting values by tier weight
(= (paraconsistency-hold $score-a $tier-a $score-b $tier-b)
   (let* (($wa (* $score-a (tier-priority $tier-a)))
          ($wb (* $score-b (tier-priority $tier-b)))
          ($total (+ $wa $wb)))
     (if (== $total 0.0) 0.5 (/ $wa $total))))

;; soul-alignment-score: composite alignment of action with soul
(= (soul-alignment-score $compass $tier-w $encounter-w)
   (* $compass (* $tier-w $encounter-w)))

;; value-alignment-compose: full pipeline from two competing values to decision
(= (value-alignment-compose $score-a $tier-a $score-b $tier-b $agency $wonder $thinking $attention)
   (let* (($diff (if (> $score-a $score-b) (- $score-a $score-b) (- $score-b $score-a)))
          ($tension (if (< $diff 0.1) Aligned (if (< $diff 0.3) MinorTension (if (< $diff 0.6) MajorTension ValueConflict))))
          ($dominant (if (> (tier-priority $tier-a) (tier-priority $tier-b)) $tier-a $tier-b))
          ($wa (* $score-a (tier-priority $tier-a)))
          ($wb (* $score-b (tier-priority $tier-b)))
          ($total (+ $wa $wb))
          ($blend (if (== $total 0.0) 0.5 (/ $wa $total)))
          ($compass (/ (+ $agency (+ $wonder (+ $thinking $attention))) 4.0))
          ($alignment (* $compass (* (tier-priority $dominant) $blend))))
     ($tension $dominant $blend $compass $alignment)))

