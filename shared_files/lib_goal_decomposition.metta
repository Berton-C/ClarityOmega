;; lib_goal_decomposition.metta — Break complex goals into trackable subgoals
;; Types
(: GoalTree Type)
(: Dependency Type)
(: DecompResult Type)
(: CompletionSignal Type)
(: GoalStatus Type)
(: mk-goal-tree (-> Symbol Symbol Expression Atom GoalTree))
(: mk-dependency (-> Symbol Symbol Number Dependency))
(: mk-decomp (-> Symbol Expression Symbol DecompResult))
(: mk-completion (-> Symbol Number Symbol CompletionSignal))
;; Goal status values
(: Blocked GoalStatus)
(: Ready GoalStatus)
(: Partial GoalStatus)
(: Complete GoalStatus)
;; check-dependencies: compare child confidence against blocking threshold
;; If child-conf < threshold then Blocked, if child-conf >= 0.8 then Complete, else Partial
;; propagate-up: revise parent stv using child completion confidence as new evidence
;; find-frontier: from a list of goals return those with status Ready

;; check-dependencies: given dependency confidence and threshold, classify goal status
;; Usage: (check-dependencies dep-confidence threshold) -> GoalStatus
;; Validated 2026-04-21: 0.3/0.5->Blocked, 0.85/0.5->Complete, 0.6/0.5->Partial
(= (check-dependencies $dep-conf $threshold)
   (if (< $dep-conf $threshold) Blocked
     (if (> $dep-conf 0.8) Complete Partial)))

;; propagate-up: revise parent confidence using child completion as new evidence
;; Takes parent-stv and child-completion-confidence, returns revised stv
(= (propagate-up (stv $f1 $c1) $child-conf)
   (let* (($c2 (* 0.9 $child-conf))
          ($f2 $child-conf)
          ($new-f (/ (+ (* $f1 $c1) (* $f2 $c2)) (+ $c1 $c2)))
          ($new-c (+ $c1 $c2)))
     (stv $new-f (min 0.99 $new-c))))

;; find-ready: filter goals by checking if dependency confidence meets threshold
;; Returns Ready or Blocked for a single goal check
(= (goal-readiness $dep-conf $threshold)
   (if (>= $dep-conf $threshold) Ready Blocked))


;; find-frontier-single: check if a goal is ready based on dependency confidence
(= (find-frontier-single $gid $dep-conf $threshold)
   (if (>= $dep-conf $threshold) ($gid Ready) Nil))

;; recompose-min: bottleneck combiner for child confidences
(= (recompose-min $c1 $c2)
   (if (< $c1 $c2) $c1 $c2))

;; assess-parent-2: propagate two child completions up to parent stv
(= (assess-parent-2 (stv $pf $pc) $child1 $child2)
   (let* (($min-child (if (< $child1 $child2) $child1 $child2))
          ($c2 (* 0.9 $min-child))
          ($f2 $min-child)
          ($new-f (/ (+ (* $pf $pc) (* $f2 $c2)) (+ $pc $c2)))
          ($new-c (+ $pc $c2)))
     (stv $new-f (min 0.99 $new-c))))

