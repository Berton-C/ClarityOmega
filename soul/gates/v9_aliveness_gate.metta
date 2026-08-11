; v9 Aliveness Gate
; Entry point: (aliveness-gate $msgnew $idle)
; $msgnew - boolean, true when a new human message arrived this cycle
; $idle - the idle_directive STRING (from helper.py), NOT the idle-pattern atom
; Naming: $idle parameter is the idle_directive STRING (from helper.py),
; distinct from (current-idle-pattern) ATOM (from idle_cycle_detector).
; The naming similarity is historical; signature preserved for loop.metta compatibility.
; Returns: ENGAGE or SILENT only. Pure consumer, no atom writes.
; C12-safe: no match inside if; collapse-then-branch where needed.

; Priority 1: idle_directive non-empty OR msgnew=True -> ENGAGE
; (supervisor authority + active conversation)
(aliveness-gate $msgnew $idle
    (if (or (> (string_length $idle) 0) $msgnew)
        ENGAGE
        (gate-on-idle-pattern (current-idle-pattern))))

; Priority 2: idle-pattern verdict
; send-burst -> SILENT (user overwhelmed, back off)
; productive -> fall through (continue checks)
; Pre-bootstrap: () -> fall through
(gate-on-idle-pattern ()
    (gate-on-agency-balance (current-agency-balance)))
(gate-on-idle-pattern (send-burst $count)
    SILENT)
(gate-on-idle-pattern (productive $count)
    (gate-on-agency-balance (current-agency-balance)))

; Priority 3: agency-balance verdict
; dependency-risk -> SILENT (system is doing too much, person too passive)
; healthy -> fall through
; Pre-bootstrap: () -> fall through
(gate-on-agency-balance ()
    (gate-on-task-phase (current-phase)))
(gate-on-agency-balance (dependency-risk $person $system)
    SILENT)
(gate-on-agency-balance (healthy $person $system)
    (gate-on-task-phase (current-phase)))

; Priority 4: passive phases -> SILENT
; Priority 5: active phases -> fall through to latch-dispatch
; Priority 6: unknown phase -> latch-dispatch (defaults SILENT)
(gate-on-task-phase attending
    SILENT)
(gate-on-task-phase idle
    SILENT)
(gate-on-task-phase waiting
    SILENT)
(gate-on-task-phase reflecting
    SILENT)
(gate-on-task-phase engaged
    (gate-on-latch-fallback))
(gate-on-task-phase research
    (gate-on-latch-fallback))
(gate-on-task-phase response-drafting
    (gate-on-latch-fallback))
(gate-on-task-phase boundary-detected
    (gate-on-latch-fallback))n; Priority 6: any other/unknown phase -> latch-dispatch
(gate-on-task-phase $other
    (gate-on-latch-fallback))

; Legacy latch-state fallback (v8 dispatch preserved as transitional safety net)
; Uses collapse-then-branch for C12-safety and to handle missing latch-state atom.
; If no latch-state atom exists -> conservative SILENT.
(gate-on-latch-fallback
    (gate-read-latch-state (collapse (match &self (latch-state $s) $s))))

; No latch-state atom present -> conservative SILENT
(gate-read-latch-state ()
    SILENT)

; Latch-state found, dispatch on its value
(gate-read-latch-state ($state)
    (latch-dispatch $state))

; v8 latch-dispatch rules (preserved as fallback semantics)
; IDLE -> SILENT (no active engagement)
; ENGAGED -> ENGAGE (active loop participation)
; COMPLETING -> SILENT (wrapping up, don't start new work)
; Unknown state -> SILENT (conservative default)
(latch-dispatch IDLE
    SILENT)
(latch-dispatch ENGAGED
    ENGAGE)
(latch-dispatch COMPLETING
    SILENT)
(latch-dispatch $unknown
    SILENT)
