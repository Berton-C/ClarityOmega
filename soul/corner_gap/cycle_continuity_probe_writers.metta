;; cycle_continuity_probe_writers.metta -- snapshot tracking + graded verdict (writers)
;; Author: ClarityClaw. Granularity-layer reference draft 2026-06-03.
;;
;; Two responsibilities:
;;   1. Maintain the prior-cycle profile snapshot as a singleton (clear-then-write),
;;      so behavior-stasis-pbit compares last cycle to this cycle.
;;   2. Provide the graded drop-in replacement for populate-coupling-verdict: write
;;      a (coupling-status <cycle> <verdict>) atom from the graded corner gate
;;      instead of the crisp coupling-verdict. The downstream sustained-corner
;;      reader (count-corners-in-window, corner-confirmed in
;;      coupling_integrity_detector.metta) is unchanged and still counts `corner`.
;;
;; ORDERING in loop.metta cycle tail (after populate-recent-action and
;; populate-state-delta):
;;   do-update-corner-graded! computes the verdict (which reads the PRIOR snapshot
;;   via behavior-stasis-pbit), writes coupling-status, THEN snapshots THIS cycle's
;;   profile as the new prior. The snapshot must come last so the verdict sees the
;;   previous cycle, not itself.
;;
;; KNOWN INEFFICIENCY: behavior-stasis-pbit builds this cycle's pfn to score it,
;; and do-snapshot-cycle-pfn! builds it again to store it. Two builds per cycle.
;; Acceptable for a reference draft; collapse to one build if profiling warrants.
;;
;; CONFIRM (REPL): storing and re-reading the constructed pfn term round-trips
;; cleanly (add-atom stores unreduced; the pfn is inert data once numeric weights
;; are bound, so this should hold, but verify).
;;
;; PeTTa constraints: C12-safe, ASCII-safe, no RMW. Depends on
;; cycle_continuity_probe (build-cycle-pfn, corner-confirmed-full) and
;; coupling_integrity_detector (coupling-status-window).

;; ----------------------------------------------------------------
;; SNAPSHOT TRACKER (singleton clear-then-write)
;; ----------------------------------------------------------------
;; BUG FIX (2026-06-04, harness): same clear-before-add empty trap as
;; do-clear-state-delta! / do-clear-coupling-status!. The prior shape superposed
;; before guarding empty; on a cold space (superpose ()) yields zero solutions and
;; halts do-snapshot-cycle-pfn!'s let* before $_store, so no snapshot is ever
;; stored and behavior-stasis-pbit always falls to its bootstrap branch. Guard the
;; collapsed list for empty first, collapse-wrap the removal for one solution.
(= (do-clear-cycle-pfn!)
   (let $existing (collapse (match &self (cycle-pfn-snapshot $p) (cycle-pfn-snapshot $p)))
      (if (== $existing ())
          ()
          (let $_drained (collapse (let $old (superpose $existing)
                                        (remove-atom &self $old)))
             ()))))

(= (do-snapshot-cycle-pfn!)
   (let* (($curr   (build-cycle-pfn))
          ($_clear (do-clear-cycle-pfn!))
          ($_store (add-atom &self (cycle-pfn-snapshot $curr))))
      ()))

;; ----------------------------------------------------------------
;; GRADED VERDICT WRITER (drop-in replacement for populate-coupling-verdict)
;; ----------------------------------------------------------------
;; Writes corner / not-corner from the graded gate, prunes the coupling-status
;; window, then snapshots this cycle's profile for next cycle's stasis comparison.
(= (do-update-corner-graded! $cycle-id)
   (let* (($verdict      (if (== (corner-confirmed-full) True) corner not-corner))
          ($_assert      (add-atom &self (coupling-status $cycle-id $verdict)))
          ($prune-before (- $cycle-id (coupling-status-window)))
          ($to-remove    (collapse (match &self (coupling-status $old-id $v)
                                          (if (< $old-id $prune-before)
                                              (coupling-status $old-id $v)
                                              ()))))
          ($_prune       (if (== $to-remove ())
                                   ()
                                   (let $_drained (collapse (let $old (superpose $to-remove)
                                                                 (if (== $old ()) () (remove-atom &self $old))))
                                      ())))
          ($_snap        (do-snapshot-cycle-pfn!)))
      ()))
