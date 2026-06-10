;; getSoulBrief - pure MeTTa function querying AtomSpace for soul brief
;; Author: ClarityClaw  Date: 2026-04-26

;; Section 1: Identity
(= (brief-identity)
   (soul-identity-name))

;; Section 2: Priority Anchor
(= (brief-priorities)
   (soul-priority-hierarchy))

;; Section 3: Active Goals - non-complete only
(= (brief-active-goal-entry $n)
   (if (== (active-goal-status $n) complete)
       ()
       ((active-goal-status $n) (active-goal-action $n) (active-goal-gap $n))))

(= (brief-active-goals)
   (filter-empty-entries
     (collapse (match &self (= (active-goal $n) $g)
       (brief-active-goal-entry $n)))))

;; Section 4: High-Severity Gaps
(= (brief-high-gaps)
   (high-severity-gaps))

;; Section 5: Creative Fuel Direction
(= (brief-creative-direction)
   (creative-question Safety))

;; Section 6: Assemble Full Brief
(= (getSoulBrief)
   (SoulBrief
     (Identity (brief-identity))
     (Priorities (brief-priorities))
     (ActiveGoals (brief-active-goals))
     (HighGaps (brief-high-gaps))
     (CreativeDirection (brief-creative-direction))))
