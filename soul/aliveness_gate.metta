;; Aliveness Gate v7 - Reads queryable state atoms, with fallback
;; If no latch-state atom exists, defaults to SILENT (safe)

(= (aliveness-gate $msgnew $idle)
  (if (not (== $idle ""))
    ENGAGE
    (aliveness-gate-latch $msgnew)))

(= (aliveness-gate-latch True) ENGAGE)

(= (aliveness-gate-latch False)
  (latch-dispatch (match &self (latch-state $s) $s)))

(= (latch-dispatch IDLE) SILENT)
(= (latch-dispatch ENGAGED) ENGAGE)
(= (latch-dispatch COMPLETING) ENGAGE)
(= (latch-dispatch $other) SILENT)
