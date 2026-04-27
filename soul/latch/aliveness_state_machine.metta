;; LATCH Aliveness State Machine v2
;; Rewritten to use change-state!/get-state (proven primitives from loop.metta)
;; State variable &latch_state initialized in loop.metta
;; Valid states: IDLE, ENGAGED, COMPLETING

;; State query
(= (current-latch-state)
   (get-state &latch_state))

;; Transition functions
(= (transition-to-engaged)
   (change-state! &latch_state ENGAGED))

(= (transition-to-completing)
   (change-state! &latch_state COMPLETING))

(= (transition-to-idle)
   (change-state! &latch_state IDLE))

;; Guard: only transition if current state matches expected
(= (guarded-transition $from $to)
   (if (== (current-latch-state) $from)
       (change-state! &latch_state $to)
       (current-latch-state)))

;; Semantic transitions with guards
(= (engage-from-idle)
   (guarded-transition IDLE ENGAGED))

(= (complete-from-engaged)
   (guarded-transition ENGAGED COMPLETING))

(= (idle-from-completing)
   (guarded-transition COMPLETING IDLE))
