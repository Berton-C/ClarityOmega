;; idle_cycle_detector_writers.metta -- Side-effecting writers for idle-pattern atoms
;; v2 cycle-level wiring per Step 4.5 corrected + split-refactor (May 15 2026)
;;
;; This file contains the do-*! functions that mutate idle-pattern atoms in &self.
;; Pure read helpers (count-sends-in-window, current-idle-pattern, idle-pattern-block,
;; send-burst-threshold documentation atom) remain in idle_cycle_detector.metta.
;;
;; C12-safe: no match inside if. All guards use collapse-then-branch.
;; Mirror pattern: AtomSpace atoms only, no change-state!.
;; Pure-vs-writer split per task_state precedent (Discipline 2 refinement).
;;
;; Section 1: do-clear-idle-pattern! (freshness clearer)
;; Section 2: do-update-idle-pattern! (cycle-level writer)

;; ================================================================
;; SECTION 1: FRESHNESS CLEARER
;; ================================================================

;; Removes ALL prior idle-pattern atoms (C12-safe).
;; Bug-2 fix (May 20 2026): car-atom + remove-atom pattern was removing zero
;; atoms in this runtime, causing 50+ stale (idle-pattern productive 0) atoms
;; to accumulate from cycle 1 onward. current-idle-pattern reads via car-atom
;; which returns the OLDEST atom (bootstrap), explaining stale prompt data.
;; Fix mirrors recent_action_populator's verified-working pruning shape.
(= (do-clear-idle-pattern!)
   (let $existing (collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))
      (if (== $existing ())
          _
          (let $old (superpose $existing)
                    (if (== $old ())
                        ()
                        (remove-atom &self $old))))))

;; ================================================================
;; SECTION 2: CYCLE-LEVEL WRITER
;; ================================================================

;; Runs each cycle from loop.metta after populate-recent-action.
;; Reads count via pure helper (count-sends-in-window from idle_cycle_detector.metta),
;; derives verdict, clears prior atom via do-clear-idle-pattern!, emits fresh atom.
;; Threshold 3 hardcoded per F39 + F42 (declaration atom in pure file is
;; documentation only).
(= (do-update-idle-pattern!)
   (let* (($count (count-sends-in-window))
          ($_diag_count (println! (DIAG-WRITER-COUNT $count)))
          ($verdict (if (> $count 3)
                        send-burst
                        productive))
          ($_diag_verdict (println! (DIAG-WRITER-VERDICT $verdict))))
      (progn
         (do-clear-idle-pattern!)
         (println! (DIAG-WRITER-POST-CLEAR (collapse (match &self (idle-pattern $v $c) ($v $c)))))
         (add-atom &self (idle-pattern $verdict $count)))))
