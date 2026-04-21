;; lib_attention_steering.metta - Effort allocation via soul-aligned Gibbs tilting
;; Formalizes resonance-reward loop in MeTTa

;; Types
(: EffortWeight Type)
(: SoulAlign Type)
(: mk-effort (-> Atom Number EffortWeight))
(: mk-align (-> Atom Number SoulAlign))

;; soul-alignment: cosine-like alignment score between goal values and soul values
;; Simplified as product of two normalized scores
(= (soul-alignment $goal-val $soul-val)
   (* $goal-val $soul-val))

;; gibbs-weight: Boltzmann weighting for effort sharpening
;; weight = exp(alignment / temperature) approximated as alignment^(1/temp)
;; For temp=0.5 this squares the alignment, sharpening toward high-align goals
(= (gibbs-sharpen $alignment $inv-temp)
   (let* (($base $alignment)
          ($result (* $base (+ 1.0 (* $inv-temp $base)))))
     $result))

;; effort-compare: select higher-effort goal for priority
(= (effort-compare (mk-effort $g1 $w1) (mk-effort $g2 $w2))
   (if (> $w1 $w2) (mk-effort $g1 $w1) (mk-effort $g2 $w2)))

;; resonance-boost: amplify effort by autocatalytic loop strength
(= (resonance-boost $base-effort $loop-strength)
   (* $base-effort (+ 1.0 $loop-strength)))

;; attention-gate: only allocate effort above minimum threshold
(= (attention-gate $effort $min-effort)
   (if (>= $effort $min-effort) $effort 0.0))

;; effort-normalize: scale effort weights to sum to 1.0 given two weights
;; For two-item normalization: w1/(w1+w2)
(= (effort-normalize-2 $w1 $w2)
   (let* (($sum (+ $w1 $w2))
          ($n1 (/ $w1 $sum))
          ($n2 (/ $w2 $sum)))
     ($n1 $n2)))

;; priority-rank: combine soul-alignment and urgency into single priority score
;; priority = alignment * (1 + urgency-boost)
(= (priority-rank $alignment $urgency $urgency-weight)
   (* $alignment (+ 1.0 (* $urgency-weight $urgency))))

