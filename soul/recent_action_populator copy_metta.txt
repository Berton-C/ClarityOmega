;; soul/recent_action_populator.metta
;; Asserts a (recent-action $cycle-id $action-type $description) atom
;; into &self each iteration, and prunes atoms older than 10 cycles back.
;;
;; Architecture (per Clarity's review, May 3, 2026):
;;   - cycle_classifier.metta: pure classification functions (input -> tag)
;;   - recent_action_populator.metta: side-effecting populator (assert + prune)
;;   - orbit_detector.metta: pattern-matching reader (matches recent-action atoms)
;;
;; Reader and writer have separate change-reasons. Pruning policy and assertion
;; lifecycle live here. Read patterns live in orbit_detector. Pure classification
;; logic lives in cycle_classifier.
;;
;; Window: 10 cycles. The most history-dependent orbit pattern is
;; idle-status-resend, which compares consecutive cycles. 10 gives ample headroom.
;;
;; Pruning uses Clarity's safe two-pass pattern: collapse the atoms-to-remove
;; first (snapshot), then remove from the snapshot. This avoids
;; concurrent-modification concerns from running remove-atom inside an
;; iterating match.

;; Window size for recent-action atom retention (in cycles)
(= (recent-action-window) 10)

;; Diagnostic flag: when True, prints POPULATOR-DIAG each iteration showing
;; cycle-id, msgnew, sexpr-len, the classified action-type, and the description.
;; Useful when debugging populator inputs or classifier outputs. Flip to False
;; for normal operation; flip to True when investigating a populator/classifier
;; concern. Future re-enables (Sprint 3.3+ orbit detection, pruning verification)
;; will get the same shape automatically.
(= (populator-diagnostic-active) True)

;; Main entry point: classify, describe, assert, prune.
;; Called from loop.metta after $results execution.
;; Args:
;;   $sexpr    -- parsed command list, shape ((cmd-name "arg-string") ...)
;;   $msgnew   -- Boolean, True if a new human message arrived this cycle
;;   $cycle-id -- monotonic iteration index ($k from loop.metta)
(= (populate-recent-action $sexpr $msgnew $cycle-id)
   (let* (($action-type  (classify-cycle-action-type $sexpr $msgnew))
          ($description  (classify-cycle-description $sexpr))
          ($rendered     (repr $description))
          ($_diag (if (populator-diagnostic-active)
                      (println! (POPULATOR-DIAG cycle-id $cycle-id msgnew $msgnew sexpr-len (size-atom $sexpr) action-type $action-type description $description))
                      ()))
          ($_assert      (add-atom &self (recent-action $cycle-id $action-type $rendered)))
          ($prune-before (- $cycle-id (recent-action-window)))
          ($to-remove    (collapse (match &self (recent-action $old-id $t $d)
                                          (if (< $old-id $prune-before)
                                              (recent-action $old-id $t $d)
                                              ()))))
          ($_prune       (let $old (superpose $to-remove)
                                   (if (== $old ())
                                       ()
                                       (remove-atom &self $old)))))
         ()))
