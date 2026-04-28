;; Fix 2: next-actionable-goal Full Scan
;; Problem: next-actionable-goal only scans priorities 1-4, missing goals 5-15.
;; Combined with stale completion this created the wake vacuum:
;;   Goals 1-4 complete -> scanner stops -> Goals 5-15 ignored -> empty prompt
;;
;; Fix: Scan ALL 15 priority slots. If all complete, invoke wake-reset then retry.

(= (next-actionable-goal)
   (let $all-goals (get-goals-by-priority-ascending)
        (let $active (filter (lambda ($g) (not (== (get-status $g) complete))) $all-goals)
             (if (== (length $active) 0)
                 (do (wake-reset-goals)
                     (next-actionable-goal))
                 (head $active)))))

;; Proof trace:
;; Before fix: Wake -> scan 1-4 -> all complete -> return nothing -> empty prompt
;; After fix:  Wake -> scan 1-15 -> all complete -> reset -> scan 1-15 -> goal 1 planned -> structured prompt
