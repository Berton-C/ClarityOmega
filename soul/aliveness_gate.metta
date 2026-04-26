;; Aliveness Gate - the nexus mechanism
;; Runs AFTER AtomSpace queries, BEFORE LLM call
;; Returns SILENT, REASON, or ENGAGE

(= (aliveness-gate True    ) ENGAGE)

(= (aliveness-gate False    )
  (if (goal-just-completed )
    REASON
    (if (orbit-detected  )
      SILENT
      (if (actionable-task-found  )
        REASON
        SILENT))))

(= (goal-just-completed )
  (match &self (= (goal-completion-status ) completed) True))
(= (goal-just-completed ) False)

(= (orbit-detected  )
  (match &self (= (orbit-status) orbiting) True))
(= (orbit-detected  ) False)

(= (actionable-task-found  )
  (match &self (= (pending-task ) ready) True))
(= (actionable-task-found  ) False)
