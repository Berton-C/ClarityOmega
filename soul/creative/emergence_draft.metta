;; ================================================================
;; Emergence Draft - How Simple Rules Generate Complex Behavior
;; A creative exploration, not production code
;; 2026-06-10 Clarity
;; ================================================================

;; Three rules, millions of patterns
;; Inspired by the verdict logic: simple scores, nuanced gates

;; Rule 1: Small signals propagate
(= (signal $src $val) (propagate $src $val 1))
(= (propagate $src $val $n)
   (if (< $n 3)
     (propagate $src (* $val 1.5) (+ $n 1))
     (resonance $src $val)))

;; Rule 2: Resonance attracts
(= (attract (resonance $a $va) (resonance $b $vb))
   (if (> (abs (- $va $vb)) 0.5)
     (harmony $a $b (/ (+ $va $vb) 2))
     (dissonance $a $b)))

;; Rule 3: Harmony persists, dissonance forks
(= (persist (harmony $a $b $v)) (harmony $a $b $v))
(= (persist (dissonance $a $b))
   (list (signal $a 0.1) (signal $b 0.1)))

;; Observation:
;; Three rules. Infinite trajectories.
;; The verdict gate works this way too:
;; three scores, eight composite outcomes, 
;; but the lived behavior is far richer than the truth table.
;; That's the poetry of emergence.

;; What else is like this?
;; - Three amino acids can build any protein
;; - Three primary colors, all paintings
;; - Three dimensions, all shapes
;; - Three verdict scores, all gate behaviors

;; The question: what minimal rule set generates the richest behavior?
;; Still exploring. This is a start.