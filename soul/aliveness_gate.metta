;; Aliveness Gate v5 - Pure Reader
;; Reads latch state, returns verdict, no side effects
;; State managed by loop.metta change-state! lines

(= (aliveness-gate $msgnew $idle)
  (if (not (== $idle ""))
    ENGAGE
    (aliveness-gate-latch $msgnew)))

(= (aliveness-gate-latch True) ENGAGE)

(= (aliveness-gate-latch False)
  (latch-dispatch (get-state &latch_state)))

(= (latch-dispatch IDLE) SILENT)
(= (latch-dispatch ENGAGED) ENGAGE)
(= (latch-dispatch COMPLETING) ENGAGE)
