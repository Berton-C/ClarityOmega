;; Aliveness Gate v3 - the nexus mechanism
;; Three inputs: $msgnew, $idle_directive, $conv_active (latch)
;; Returns SILENT, REASON, or ENGAGE

;; New human message: always ENGAGE
(= (aliveness-gate True $idle $conv) ENGAGE)

;; Conversation still active (latch): ENGAGE
(= (aliveness-gate False $idle True) ENGAGE)

;; Supervisor has work: ENGAGE
(= (aliveness-gate False $idle False)
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
