;; Fix 1: Wake Goal Reset
;; Problem: On wake, all 15 goals have status=complete, so next-actionable-goal
;; returns nothing. The prompt assembles with empty ActiveGoals and HighGaps,
;; producing a structural vacuum -- no goal drives behavior.
;;
;; Root cause: Goal completion is never cycled. Once all goals reach complete,
;; the system has no mechanism to re-seed planned goals for a new wake cycle.
;;
;; Fix: On wake, detect all-complete state and reset goals to planned.

(= (wake-reset-goals)
   (if (== (count-incomplete-goals) 0)
       (do (reset-all-goals-to-planned)
           (log WAKE-ALL-COMPLETE-RESET-TO-PLANNED))
       (log WAKE-ACTIVE-GOALS-FOUND-NO-RESET)))

(= (count-incomplete-goals)
   (let $goals (get-all-goals)
        (length (filter (lambda ($g) (not (== (get-status $g) complete))) $goals))))

(= (reset-all-goals-to-planned)
   (map-goals (lambda ($g) (set-status $g planned))))
