;; task_selector.metta -- selects highest-value next task from available options
;; Author: ClarityClaw  Date: 2026-04-26
;; Routes attention to the task most aligned with current goal and context.

;; Task pool -- available tasks with estimated value
(= (available-task $task-id $description $goal-alignment $urgency) (stv 0.5 0.5))

;; Selection criteria weights
(= (selection-weight goal-alignment 0.5) (stv 0.9 0.85))
(= (selection-weight urgency 0.3) (stv 0.9 0.85))
(= (selection-weight novelty 0.1) (stv 0.8 0.7))
(= (selection-weight human-requested 0.1) (stv 0.9 0.85))

;; Score a task
(= (task-score $task-id $goal-align $urgency $novelty $human-req)
   (+ (* $goal-align 0.5)
      (+ (* $urgency 0.3)
         (+ (* $novelty 0.1)
            (* $human-req 0.1)))))

;; Blocked task filter
(= (task-blocked $task-id $reason) (stv 1.0 0.9))

;; Is task actionable?
(= (task-actionable $task-id)
   (if (match &self (= (task-blocked $task-id $r) (stv $w $c)) True)
       False
       True))

;; Anti-busywork filter: reject tasks that score below threshold
(= (min-value-threshold 0.3) (stv 0.9 0.85))

;; Should act or wait?
(= (act-or-wait $best-score)
   (if (>= $best-score (min-value-threshold))
       Act
       Wait))

;; Context-aware: is human message new?
(= (message-context new) (stv 0.5 0.5))
(= (message-context stale) (stv 0.5 0.5))

;; Verdict
(= (task-selector-verdict $task-id $score)
   (TaskSelector
     (SelectedTask $task-id)
     (Score $score)
     (Actionable (task-actionable $task-id))
     (Decision (act-or-wait $score))))
