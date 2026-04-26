;; goal_completion_checker.metta -- verifies goal completion claims against evidence
;; Author: ClarityClaw  Date: 2026-04-26
;; Prevents RECOGNITION-VS-ACQUISITION: claiming done without behavioral proof.

;; Goal state tracking
(= (goal-state $goal-id not-started) (stv 1.0 0.9))
(= (goal-state $goal-id in-progress) (stv 0.5 0.5))
(= (goal-state $goal-id claimed-done) (stv 0.5 0.3))
(= (goal-state $goal-id verified-done) (stv 1.0 0.9))

;; Evidence types
(= (evidence-type file-exists) (stv 0.9 0.85))
(= (evidence-type test-passes) (stv 0.95 0.9))
(= (evidence-type human-confirmed) (stv 1.0 0.95))
(= (evidence-type output-verified) (stv 0.9 0.85))

;; Completion check: claimed-done without evidence is a gap
(= (completion-gap $goal-id)
   (match &self (= (goal-state $goal-id claimed-done) (stv $w1 $c1))
          (if (not (match &self (= (goal-evidence $goal-id $etype) (stv $w2 $c2)) True))
              (CompletionGap $goal-id no-evidence)
              (CompletionVerified $goal-id))))

;; Done-when criteria registry
(= (done-when $goal-id $criterion) (stv 0.9 0.8))

;; Check all criteria met
(= (all-criteria-met $goal-id)
   (if (match &self (= (done-when $goal-id $c) (stv $w $conf))
              (not (match &self (= (criterion-satisfied $goal-id $c) (stv $w2 $c2)) True)))
       False
       True))

;; Verdict
(= (goal-completion-verdict $goal-id)
   (GoalCompletionCheck
     (Goal $goal-id)
     (Gap (completion-gap $goal-id))
     (AllCriteriaMet (all-criteria-met $goal-id))))
