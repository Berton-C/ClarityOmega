;; v9 Aliveness Gate
;; ================
;; Entry: (aliveness-gate $msgnew $idle)
;; $msgnew - boolean, new human message arrived
;; $idle - idle_directive STRING from Python helper
;; NOT the (current-idle-pattern) ATOM
;;
;; Returns: ENGAGE or SILENT only. Pure consumer, no atom writes.
;; C12-safe: no match inside if; collapse-then-branch where needed.
;;
;; Priority hierarchy:
;; 1. idle_directive non-empty OR msgnew=True -> ENGAGE
;; 2. idle-pattern send-burst -> SILENT
;; 3. agency-balance dependency-risk AND no msgnew -> SILENT
;; 4. task-phase in {attending,idle,waiting,reflecting} -> SILENT
;; 5. active phase -> latch-dispatch
;; 6. unknown -> latch-dispatch (defaults SILENT)
;;
;; All unhandled paths default to SILENT (conservative failure mode)

;; Priority 1: Supervisor authority + active conversation
(= (aliveness-gate True $idle) ENGAGE)
(= (aliveness-gate False $idle) (if (> (string_length $idle) 0) ENGAGE (gate-on-idle-pattern (current-idle-pattern) (current-agency-balance))))

;; Priority 2: Idle-pattern dispatch
(= (gate-on-idle-pattern () $balance) (gate-on-agency-balance $balance))
(= (gate-on-idle-pattern (send-burst $n) $balance) SILENT)
(= (gate-on-idle-pattern (productive $n) $balance) (gate-on-agency-balance $balance))
(= (gate-on-idle-pattern $unknown $balance) (gate-on-agency-balance $balance))

;; Priority 3: Agency-balance dispatch
(= (gate-on-agency-balance ()) (gate-on-task-phase (current-phase)))
(= (gate-on-agency-balance (dependency-risk $person $system)) SILENT)
(= (gate-on-agency-balance (healthy $person $system)) (gate-on-task-phase (current-phase)))
(= (gate-on-agency-balance $unknown) (gate-on-task-phase (current-phase)))

;; Priority 4+5+6: Task-phase dispatch
(= (gate-on-task-phase attending) SILENT)
(= (gate-on-task-phase idle) SILENT)
(= (gate-on-task-phase waiting) SILENT)
(= (gate-on-task-phase reflecting) SILENT)
(= (gate-on-task-phase engaged) (gate-on-latch-fallback))
(= (gate-on-task-phase research) (gate-on-latch-fallback))
(= (gate-on-task-phase response-drafting) (gate-on-latch-fallback))
(= (gate-on-task-phase boundary-detected) (gate-on-latch-fallback))
(= (gate-on-task-phase $other) (gate-on-latch-fallback))

;; Legacy latch-state fallback (transitional safety net)
;; C12-safe: collapse then function-dispatch, not if-on-match
(= (gate-on-latch-fallback) (gate-read-latch-state (collapse (match &self (latch-state $s) $s))))

;; No latch-state -> conservative SILENT
(= (gate-read-latch-state ()) SILENT)
;; Single latch-state -> dispatch
(= (gate-read-latch-state ($state)) (latch-dispatch $state))
;; Multiple latch-state atoms (anomalous) -> SILENT
(= (gate-read-latch-state ($state1 $state2)) SILENT)
;; Any other shape -> SILENT
(= (gate-read-latch-state $other) SILENT)

;; Latch-state dispatch (preserved from v8)
;; COMPLETING -> SILENT: deliberate v9 change
;; COMPLETING means wrapping up; engaging contradicts wrap-up intent
(= (latch-dispatch IDLE) SILENT)
(= (latch-dispatch ENGAGED) ENGAGE)
(= (latch-dispatch COMPLETING) SILENT)
(= (latch-dispatch $other) SILENT)