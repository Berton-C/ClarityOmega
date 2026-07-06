;; === corner_window_writers.metta ===
;; DRAFT for Clarity's analysis. Destination:
;; soul/corner_gap/corner_window_writers.metta (new file, build step B4).
;;
;; Confirmation-scoped command record for the pattern-scoped gate. While a
;; corner is confirmed (graded, corner-confirmed-core), each proposed
;; command's repr is recorded; the gate filter suppresses only exact matches
;; against this record. On any non-confirmed cycle the record clears, so
;; suppression never outlives the corner (release hygiene). Clear per ADR-005.

(= (do-clear-corner-window!)
   (let $olds (collapse (match &self (corner-window-cmd $c $r) (corner-window-cmd $c $r)))
        (let $o (superpose $olds)
             (if (== $o ())
                 ()
                 (remove-atom &self $o)))))

(= (do-record-corner-window! $cmds $cycle-id)
   (let $c (superpose $cmds)
        (if (== $c ())
            ()
            (let $r (repr $c)
                 (add-atom &self (corner-window-cmd $cycle-id $r))))))

;; Cycle driver: record while the graded corner is confirmed, clear otherwise.
;; Hook ordering: AFTER populate-coupling-verdict (loop.metta line 176), so
;; the record reflects this cycle's confirmed state.
(= (populate-corner-window! $cmds $cycle-id)
   (if (== (corner-confirmed-core) True)
       (do-record-corner-window! $cmds $cycle-id)
       (do-clear-corner-window!)))
