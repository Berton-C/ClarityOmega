;; lib_attention_steering.metta - Effort allocation via soul-aligned Gibbs tilting v2
;; Formalizes resonance-reward loop in MeTTa
;; Pure = definitions only, no imports, no side effects

;; Types
(: EffortWeight Type)
(: SoulAlign Type)
(: steering-report Type)
(: mk-effort (-> Atom Number EffortWeight))
(: mk-align (-> Atom Number SoulAlign))
(: mk-steering (-> Atom EffortWeight Number steering-report))

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
(= (effort-normalize-2 $w1 $w2)
   (let* (($sum (+ $w1 $w2))
          ($n1 (/ $w1 $sum))
          ($n2 (/ $w2 $sum)))
     ($n1 $n2)))

;; priority-rank: combine soul-alignment and urgency into single priority score
(= (priority-rank $alignment $urgency $urgency-weight)
   (* $alignment (+ 1.0 (* $urgency-weight $urgency))))

;; === New v2 functions ===

;; effort-budget: allocate fixed budget across two goals proportionally
(: effort-budget (-> Number Number Number (Number Number)))
(= (effort-budget $w1 $w2 $total-budget)
   (let $sum (+ $w1 $w2)
     ((* $total-budget (/ $w1 $sum))
      (* $total-budget (/ $w2 $sum)))))

;; attention-decay: effort decays over time without reinforcement
(: attention-decay (-> Number Number Number Number))
(= (attention-decay $effort $decay-rate $elapsed)
   (* $effort (- 1.0 (* $decay-rate $elapsed))))

;; soul-effort-gate: only pass effort if soul-alignment exceeds threshold
(: soul-effort-gate (-> Number Number Number Number))
(= (soul-effort-gate $effort $soul-align $min-align)
   (if (>= $soul-align $min-align) $effort 0.0))

;; steering-classify: qualitative effort level
(: steering-classify (-> Number Atom))
(= (steering-classify $effort)
   (if (> $effort 0.7) high-effort
     (if (> $effort 0.4) moderate-effort
       (if (> $effort 0.15) low-effort
         deprioritized))))

;; Full steering report: alignment check, effort gate, classification
(: steering-full (-> Atom Number Number Number Number steering-report))
(= (steering-full $goal $goal-val $soul-val $min-align $min-effort)
   (let* (($align (soul-alignment $goal-val $soul-val))
          ($gated (soul-effort-gate $align $align $min-align))
          ($effort (attention-gate $gated $min-effort))
          ($class (steering-classify $effort)))
     (mk-steering $class (mk-effort $goal $effort) $align)))
