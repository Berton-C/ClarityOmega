;; === cycle_trace_writers.metta ===
;; DRAFT for Clarity's analysis. Destination: soul/cycle_trace_writers.metta
;; (new file, build step B2, import line in lib_clarity_reasoning manifest).
;;
;; Side-effecting writers for the cycle-cmd trace. Pure reads live in
;; cycle_trace.metta (Discipline 6A). Clear pattern per ADR-005
;; (superpose-iteration over a collapsed match). Pruning per the
;; recent_action_populator window precedent.

;; Record one atom per command in this cycle's parsed batch.
;; $cmds is the collapsed ground list ($metta_cmds at loop.metta line 140).
;; repr is bound in a let BEFORE storage so the stored atom carries the
;; reduced string, not an unreduced call (F1.1 lesson).
(= (do-record-cycle-cmds! $cmds $cycle-id)
   (let $c (superpose $cmds)
        (if (== $c ())
            ()
            (let $r (repr $c)
                 (add-atom &self (cycle-cmd $cycle-id $r))))))

;; Prune atoms older than the window (ADR-005 iteration shape; numeric guard
;; per the populator precedent).
(= (do-prune-cycle-trace! $cycle-id)
   (let $olds (collapse (match &self (cycle-cmd $c $r) (cycle-cmd $c $r)))
        (let $o (superpose $olds)
             (if (== $o ())
                 ()
                 (let (cycle-cmd $oc $or) $o
                      (if (< $oc (- $cycle-id (cycle-trace-window)))
                          (remove-atom &self (cycle-cmd $oc $or))
                          ()))))))

;; Cycle driver: one hook, unconditional (the trace always runs; detection
;; outlives enforcement, commitment 7).
(= (populate-cycle-trace! $cmds $cycle-id)
   (let* (($_r (do-record-cycle-cmds! $cmds $cycle-id))
          ($_p (do-prune-cycle-trace! $cycle-id)))
         ()))
