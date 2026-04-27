;; Aliveness Gate v6 - Reads queryable state atoms from AtomSpace
;; State stored as (latch-state IDLE/ENGAGED/COMPLETING) atom in &self
;; State managed by loop.metta via set-atom! transitions

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
