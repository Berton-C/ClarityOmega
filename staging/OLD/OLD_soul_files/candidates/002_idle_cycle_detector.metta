;; Candidate 002: idle-cycle-detector
;; Proposed 2026-04-25T17:24 by Clarity
;; Purpose: Detect when Clarity is idle-cycling on a blocked goal
;; and suggest productive alternative work instead of repeating
;; the same status check.
;;
;; Motivation: 15+ identical iterations observed on Goal 15 while
;; blocked on external input. This wastes cycles and demonstrates
;; a gap in self-regulation.

(= (candidate-id 002) idle-cycle-detector)
(= (candidate-status idle-cycle-detector) proposed)
(= (candidate-description idle-cycle-detector)
  "Detect idle cycling on blocked goals and redirect to productive alternatives")

;; === DETECTION RULE ===
;; If same pin text repeated 3+ times AND goal status is blocked:
;;   -> trigger idle-cycle-detected
(= (idle-cycle-threshold) 3)
(= (idle-cycle-action blocked-on-external)
  (alternatives
    (propose-new-candidate)
    (review-existing-artifacts-for-quality)
    (write-documentation)
    (run-soul-eval-audit)
    (consolidate-knowledge-into-atomspace)))

;; === TEST HOOK ===
(= (test-idle-cycle-detector)
  (idle-cycle-action blocked-on-external))
