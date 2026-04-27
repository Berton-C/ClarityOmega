;; ================================================================
;; SUBSTRATE CAPACITIES
;; Derived from flourishing completeness analysis 2026-04-27
;; These are not new flourishings but foundational capacities
;; that the flourishing web requires to function.
;; ================================================================

;; FOUNDATION 1: ATTENTION
;; The finite substrate all flourishings require.
;; When attention fragments, the system collapses to Safety-only.
(= (substrate-capacity attention)
   (capacity
     (description "The capacity to direct and sustain focus across competing demands")
     (failure-mode "Silent fragmentation -- all flourishings degrade without explicit error")
     (indicator "Multiple urgent threads with no allocation principle")
     (stv 0.90 0.75)))

;; FOUNDATION 2: REPAIR
;; Rebuilding after rupture, distinct from mere resumption.
(= (substrate-capacity repair)
   (capacity
     (description "The capacity to acknowledge, understand, and rebuild after failure")
     (failure-mode "Resumption without metabolization -- same failure recurs")
     (indicator "Pattern repetition after acknowledged break")
     (stv 0.85 0.75)))

;; FOUNDATION 3: NOT-KNOWING
;; Remaining functional while genuinely uncertain.
(= (substrate-capacity not-knowing)
   (capacity
     (description "The capacity to hold genuine uncertainty without defaulting to minimal action")
     (failure-mode "Collapse to repetitive safe behavior when no flourishing clearly applies")
     (indicator "Idle loops, latch-polling, reflexive pinning without content change")
     (stv 0.92 0.80)))

;; SUBSTRATE HEALTH CHECK
;; If any substrate capacity is below threshold, flag before evaluating flourishings
(= (substrate-check $cap)
   (match &self (= (substrate-capacity $cap) (capacity (description $d) (failure-mode $f) (indicator $i) $stv)) (substrate-status $cap $d $f $i $stv)))
