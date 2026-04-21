;; lib_metacognition.metta - Self-monitoring and adaptive reasoning control
;; Enables Clarity to assess own reasoning quality and adapt strategies

;; Types
(: MetaState Type)
(: Confident MetaState)
(: Uncertain MetaState)
(: Stuck MetaState)
(: Exploring MetaState)

;; confidence-self-assess: map raw confidence to qualitative meta-state
(= (confidence-self-assess $conf)
   (if (>= $conf 0.8) Confident
     (if (>= $conf 0.5) Uncertain
       (if (>= $conf 0.2) Exploring Stuck))))

;; stuck-detection: true if no progress across N attempts
;; progress-delta below threshold over attempt-count above patience
(= (stuck-detect $progress-delta $threshold $attempt-count $patience)
   (if (and (< $progress-delta $threshold) (> $attempt-count $patience)) True False))

;; progress-measure: normalized distance between current and target
;; Returns value in 0-1 range where 1 means target reached
(= (progress-measure $current $target)
   (if (== $target 0.0) 0.0
     (let* (($ratio (/ $current $target))
            ($clamped (if (> $ratio 1.0) 1.0 $ratio)))
       $clamped)))

;; strategy-shift: recommend action based on meta-state
(= (strategy-shift Confident) DeepenCurrentPath)
(= (strategy-shift Uncertain) GatherMoreEvidence)
(= (strategy-shift Exploring) BroadenSearch)
(= (strategy-shift Stuck) BacktrackAndReframe)

;; reasoning-quality: composite score from confidence and coherence
(= (reasoning-quality $confidence $coherence $novelty)
   (let* (($base (* 0.5 $confidence))
          ($coh-contrib (* 0.3 $coherence))
          ($nov-contrib (* 0.2 $novelty)))
     (+ $base (+ $coh-contrib $nov-contrib))))
