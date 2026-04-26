;; Aliveness Gate - the nexus mechanism
;; Runs AFTER AtomSpace queries, BEFORE LLM call
;; Returns SILENT, REASON, or ENGAGE
;; Two inputs: $msgnew (is message new?) and $idle (supervisor directive)

;; New human message: always ENGAGE
(= (aliveness-gate True $idle) ENGAGE)

;; No new message but supervisor has work: ENGAGE
(= (aliveness-gate False $idle)
  (if (not (== $idle ""))
    ENGAGE
    (if (goal-just-completed)
      REASON
      (if (orbit-detected)
        SILENT
        (if (actionable-task-found)
          REASON
          SILENT)))))

(= (goal-just-completed)
  (match &self (= (goal-completion-status) completed) True))
(= (goal-just-completed) False)

(= (orbit-detected)
  (match &self (= (orbit-status) orbiting) True))
(= (orbit-detected) False)

(= (actionable-task-found)
  (match &self (= (pending-task) ready) True))
(= (actionable-task-found) False)
