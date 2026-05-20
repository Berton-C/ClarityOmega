;; agency_balance_guard_writers.metta -- Side-effecting writers for agency-balance atoms
;; v2 cycle-level wiring per Step 4.6 corrected split (May 15 2026)
;;
;; This file contains the do-*! functions that mutate agency-balance atoms in &self.
;; Pure read helpers (count-person-actions-in-window, count-system-actions-in-window,
;; current-agency-balance, agency-balance-block) and pure reasoning predicates
;; (dependency-detected, agency-intervention, agency-balance-verdict, ecosystem-healthy)
;; plus all declaration atoms remain in agency_balance_guard.metta.
;;
;; C12-safe: no match inside if. All guards use collapse-then-branch.
;; Mirror pattern: AtomSpace atoms only, no change-state!.
;; Pure-vs-writer split per task_state precedent (Discipline 2 refinement).
;;
;; Section 1: do-clear-agency-balance! (freshness clearer)
;; Section 2: do-update-agency-balance! (cycle-level writer)

;; ================================================================
;; SECTION 1: FRESHNESS CLEARER
;; ================================================================

;; Removes ALL prior agency-balance atoms (C12-safe).
;; Bug-2b fix (May 20 2026): same car-atom + remove-atom pathology as
;; do-clear-idle-pattern!. current-agency-balance reads via car-atom
;; returning the OLDEST atom (bootstrap), explaining stale (dependency-risk 0 1)
;; in prompt context. Fix mirrors populator's verified-working pruning shape.
(= (do-clear-agency-balance!)
   (let $existing (collapse (match &self (agency-balance $v $p $s) (agency-balance $v $p $s)))
      (if (== $existing ())
          _
          (let $old (superpose $existing)
                    (if (== $old ())
                        ()
                        (remove-atom &self $old))))))

;; ================================================================
;; SECTION 2: CYCLE-LEVEL WRITER
;; ================================================================

;; Runs each cycle from loop.metta after do-update-idle-pattern!.
;; Reads counts via pure helpers (count-person-actions-in-window and
;; count-system-actions-in-window from agency_balance_guard.metta).
;; Derives verdict via dependency-detected (zero-count-safe).
;; Clears prior atom via do-clear-agency-balance!, emits fresh atom.
;; Verdict labels: healthy / dependency-risk per Clarity Q2 (May 15 2026).
(= (do-update-agency-balance!)
   (let* (($person (count-person-actions-in-window))
          ($system (count-system-actions-in-window))
          ($verdict (if (dependency-detected $person $system)
                        dependency-risk
                        healthy)))
      (progn
         (println! (DIAG-WRITER-AB-PERSON $person))
         (println! (DIAG-WRITER-AB-SYSTEM $system))
         (println! (DIAG-WRITER-AB-VERDICT $verdict))
         (do-clear-agency-balance!)
         (println! (DIAG-WRITER-AB-POST-CLEAR (collapse (match &self (agency-balance $v $p $s) ($v $p $s)))))
         (add-atom &self (agency-balance $verdict $person $system)))))
