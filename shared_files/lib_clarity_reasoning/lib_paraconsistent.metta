;; lib_paraconsistent.metta -- ClarityClaw paraconsistent reasoning
;; Handles contradictory evidence without explosion
;; Pure MeTTa, builds on lib_nal |- operator

;; --- Dual-evidence tension ---
;; Given positive and negative evidence for same claim,
;; revise them and check if result is indeterminate
(= (dual-revise $pos $neg)
   (|- $pos $neg))

;; --- Indeterminacy check ---
;; A revised belief near f=0.5 with high confidence is paraconsistent tension
(= (indeterminate? (stv $f $c))
   (if (and (> $c 0.5) (and (> $f 0.35) (< $f 0.65)))
     True False))

;; --- Value conflict surface ---
;; Two values pulling in opposite directions on same decision
;; Returns conflict-signal when both are confident but opposed
(= (value-conflict ($v1 (stv $f1 $c1)) ($v2 (stv $f2 $c2)))
   (if (and (> $c1 0.5) (> $c2 0.5))
     (if (> (abs (- $f1 $f2)) 0.4)
       (conflict $v1 $v2 (abs (- $f1 $f2)))
       (aligned $v1 $v2))
     (insufficient-evidence)))

;; --- Suspension operator ---
;; When tension is real, suspend judgment rather than collapse
;; Returns both perspectives held simultaneously
(= (suspend $claim $evidence-for $evidence-against)
   (let $revised (|- $evidence-for $evidence-against)
     (let ($term (stv $f $c)) $revised
       (if (indeterminate? (stv $f $c))
         (suspended $claim $f $c)
         (resolved $claim $f $c)))))

;; --- Tension-aware choice ---
;; Given two options with paraconsistent evidence, pick the one
;; with higher expectation while flagging if tension exists
(= (tension-choice $opt1 $stv1 $opt2 $stv2)
   (let $e1 (expectation $stv1)
     (let $e2 (expectation $stv2)
       (if (> (abs (- $e1 $e2)) 0.1)
         (if (> $e1 $e2)
           (prefer $opt1 $e1 (no-tension))
           (prefer $opt2 $e2 (no-tension)))
         (deadlock $opt1 $opt2 $e1)))))
