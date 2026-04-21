;; lib_metacognition.metta - Self-monitoring and adaptive reasoning control v2
;; Enables Clarity to assess own reasoning quality and adapt strategies
;; Pure = definitions only, no imports, no side effects

;; Types
(: MetaState Type)
(: Confident MetaState)
(: Uncertain MetaState)
(: Stuck MetaState)
(: Exploring MetaState)
(: meta-audit Type)
(: mk-audit (-> MetaState Atom Number meta-audit))

;; confidence-self-assess: map raw confidence to qualitative meta-state
(= (confidence-self-assess $conf)
   (if (>= $conf 0.8) Confident
     (if (>= $conf 0.5) Uncertain
       (if (>= $conf 0.2) Exploring Stuck))))

;; stuck-detection: true if no progress across N attempts
(= (stuck-detect $progress-delta $threshold $attempt-count $patience)
   (if (and (< $progress-delta $threshold) (> $attempt-count $patience)) True False))

;; progress-measure: normalized distance between current and target
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

;; === New v2 functions ===

;; Full reasoning audit: state plus strategy plus quality in one call
(: reasoning-audit (-> Number Number Number meta-audit))
(= (reasoning-audit $confidence $coherence $novelty)
   (let* (($state (confidence-self-assess $confidence))
          ($strategy (strategy-shift $state))
          ($quality (reasoning-quality $confidence $coherence $novelty)))
     (mk-audit $state $strategy $quality)))

;; Confidence calibration: detect drift between expected and observed
(: confidence-drift (-> Number Number Number))
(= (confidence-drift $expected $observed)
   (max (- $expected $observed) (- $observed $expected)))

;; Calibration quality classifier
(: calibration-quality (-> Number Atom))
(= (calibration-quality $drift)
   (if (< $drift 0.1) well-calibrated
     (if (< $drift 0.25) slightly-miscalibrated
       (if (< $drift 0.5) significantly-miscalibrated
         severely-miscalibrated))))

;; Meta-chain: assess then decide if reassessment needed
(: meta-chain (-> Number Number Number meta-audit))
(= (meta-chain $conf $coh $nov)
   (let $audit (reasoning-audit $conf $coh $nov)
     (case $audit
       (((mk-audit Stuck $s $q) (reasoning-audit (* $conf 0.5) $coh (* $nov 1.5)))
        ($other $other)))))

;; Belief revision trigger: should we revise based on quality?
(: revision-trigger? (-> Number Number Atom))
(= (revision-trigger? $quality $threshold)
   (if (< $quality $threshold) revise-now
     (if (< $quality (* $threshold 1.5)) monitor-closely
       no-revision-needed)))
