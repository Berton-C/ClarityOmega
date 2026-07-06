;; state_delta_writer_writers.metta -- forward-outcome detection (writers)
;; Author: ClarityClaw. 2026-06-03. Status: drafted, not yet verified in the container.
;;
;; Singleton clear-then-write, so latest-state-delta-verdict reads the live cycle.
;; NOTE for the reader: the clearer uses superpose iteration to remove every
;; matching atom. A car-atom-only remove removes zero atoms once a stack has
;; accumulated (the ADR-005 trap); do not "simplify" to it.
;;
;; PeTTa constraints: C12-safe, ASCII-safe, mirror pattern (AtomSpace only,
;; no change-state!). Pure read helpers live in state_delta_writer.metta.
;;
;; CONFIRM (REPL): the no-op token in the clearer (_ here) versus () behaves as a
;; true no-op in this runtime. do-clear-idle-pattern! uses _; recent_action
;; populator's prune uses (). Verify before relying on it.
;;
;; BUG FIX (2026-06-04, harness): the prior shape did (superpose $existing) FIRST
;; and guarded (== $old ()) after. On an empty AtomSpace (superpose ()) yields ZERO
;; solutions, which halts the enclosing populate let* at the clear binding before
;; the add binding runs, so add-atom never fires and the writer is inert every cold
;; cycle. Fix: guard (== $existing ()) on the collapsed LIST before superpose (the
;; verified do-clear-idle-pattern! shape), and collapse-wrap the removal so the
;; clearer returns exactly one solution and cannot multiply the following add.

;; ----------------------------------------------------------------
;; FRESHNESS CLEARER (removes ALL prior state-delta atoms)
;; ----------------------------------------------------------------
(= (do-clear-state-delta!)
   (let $existing (collapse (match &self (state-delta $c $v) (state-delta $c $v)))
      (if (== $existing ())
          ()
          (let $_drained (collapse (let $old (superpose $existing)
                                        (remove-atom &self $old)))
             ()))))

;; ----------------------------------------------------------------
;; CYCLE-LEVEL WRITER (clear, then emit one fresh atom)
;; ----------------------------------------------------------------
;; Runs each cycle from loop.metta AFTER populate-recent-action and BEFORE
;; populate-coupling-verdict (the coupling detector reads this cycle's verdict via
;; latest-state-delta-verdict). Ordering is load-bearing.
(= (populate-state-delta $msgnew $results-nonempty $results-novel $cycle-id)
   (let* (($verdict (classify-state-delta $msgnew $results-nonempty $results-novel))
          ($_clear  (do-clear-state-delta!))
          ($_assert (add-atom &self (state-delta $cycle-id $verdict))))
      ()))
