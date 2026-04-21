;; lib_epistemic_gap.metta — Epistemic gap detection v2
;; Low confidence regions become learning goals
;; Autocatalytic loop: inference reveals gaps, gaps drive exploration
;; Pure = definitions only, no imports, no side effects

;; Types
(: epistemic-gap Type)
(: mk-gap (-> Atom Atom pbit epistemic-gap))
(: learning-goal Type)
(: mk-learning-goal (-> Atom Atom pbit learning-goal))
(: gap-severity Type)

;; Step 1: Detect gap — low confidence signals epistemic boundary
(: detect-gap (-> Atom Atom pbit epistemic-gap))
(= (detect-gap $domain $claim $evidence)
   (case $evidence
     (((stv $f $c) (if (< $c 0.5)
       (mk-gap $domain $claim $evidence)
       (mk-gap $domain $claim (stv 0.0 0.0)))))))

;; Step 2: Gap to learning goal
(: gap-to-goal (-> epistemic-gap learning-goal))
(= (gap-to-goal (mk-gap $domain $claim $ev))
   (mk-learning-goal $domain $claim $ev))

;; Step 3: Priority ranking — lower confidence means higher priority
(: gap-priority (-> pbit Number))
(= (gap-priority (stv $f $c)) (- 1.0 $c))

;; Step 4: Severity classification
(: classify-severity (-> pbit gap-severity))
(= (classify-severity (stv $f $c))
   (if (< $c 0.1) blind-spot
     (if (< $c 0.2) critical-gap
       (if (< $c 0.35) weak-zone
         (if (< $c 0.5) soft-gap
           no-gap)))))

;; Step 5: Expectation-based gap detection
;; Gap exists when expectation is near 0.5 (maximum uncertainty)
(: expectation-gap (-> Number Number Number))
(= (expectation-gap $f $c)
   (let $exp (+ 0.5 (* $c (- $f 0.5)))
     (- 1.0 (* 2.0 (if (> $exp 0.5) (- $exp 0.5) (- 0.5 $exp))))))

;; Step 6: Gap merge — combine two gaps on same claim via evidence union
(: merge-gaps (-> epistemic-gap epistemic-gap epistemic-gap))
(= (merge-gaps (mk-gap $d $claim (stv $f1 $c1)) (mk-gap $d $claim (stv $f2 $c2)))
   (mk-gap $d $claim (stv (/ (+ $f1 $f2) 2.0) (max $c1 $c2))))

;; Pipeline: detect and convert to learning goal in one step
(: epistemic-scan (-> Atom Atom pbit learning-goal))
(= (epistemic-scan $domain $claim $evidence)
   (gap-to-goal (detect-gap $domain $claim $evidence)))

;; Extended pipeline: scan with severity tag
(: epistemic-scan-tagged (-> Atom Atom pbit (learning-goal gap-severity)))
(= (epistemic-scan-tagged $domain $claim $evidence)
   (case $evidence
     (((stv $f $c) ((epistemic-scan $domain $claim $evidence)
                    (classify-severity $evidence))))))
