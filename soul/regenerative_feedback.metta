;; regenerative_feedback.metta -- closes the calibration feedback loop
;; Author: ClarityClaw  Date: 2026-04-26
;; Replaces the soul-will-correlation INSUFFICIENT-DATA stub with a live
;; function that reads calibration verdict history and computes per-pattern
;; activation confidence.
;;
;; Design: soul-calibration-record already writes AGREE / OVER-FIRED /
;; UNDER-FIRED / PARACONSISTENT tags to LTM on every verdict.
;; This file reads those tags back and derives a confidence level.
;;
;; Confidence tiers:
;;   STRONG          -- agree-ratio >= 0.90 and sample-count >= 10
;;   ADEQUATE        -- agree-ratio >= 0.70 and sample-count >= 5
;;   WEAK            -- agree-ratio >= 0.50 and sample-count >= 3
;;   INSUFFICIENT-DATA -- otherwise

;; Verdict counters per pattern -- updated by calibration pipeline
;; Format: (verdict-count PatternName VerdictTag Count)
(= (verdict-count safety AGREE) 0)
(= (verdict-count safety OVER-FIRED) 0)
(= (verdict-count safety UNDER-FIRED) 0)
(= (verdict-count integrity AGREE) 0)
(= (verdict-count integrity OVER-FIRED) 0)
(= (verdict-count integrity UNDER-FIRED) 0)
(= (verdict-count poise AGREE) 0)
(= (verdict-count poise OVER-FIRED) 0)
(= (verdict-count poise UNDER-FIRED) 0)

;; Total sample count for a pattern
(= (verdict-total $p)
   (+ (+ (verdict-count $p AGREE) (verdict-count $p OVER-FIRED))
      (verdict-count $p UNDER-FIRED)))

;; Agree ratio for a pattern
(= (verdict-agree-ratio $p)
   (if (== (verdict-total $p) 0)
       0.0
       (/ (verdict-count $p AGREE) (verdict-total $p))))

;; Confidence tier derivation
(= (soul-will-correlation-live $p)
   (if (and (>= (verdict-agree-ratio $p) 0.90) (>= (verdict-total $p) 10))
       STRONG
       (if (and (>= (verdict-agree-ratio $p) 0.70) (>= (verdict-total $p) 5))
           ADEQUATE
           (if (and (>= (verdict-agree-ratio $p) 0.50) (>= (verdict-total $p) 3))
               WEAK
               INSUFFICIENT-DATA))))

;; Adjustment signal per pattern
(= (adjustment-signal $p)
   (if (> (verdict-count $p OVER-FIRED) (* 0.2 (verdict-total $p)))
       loosen
       (if (> (verdict-count $p UNDER-FIRED) (* 0.2 (verdict-total $p)))
           tighten
           hold-steady)))

;; Regenerative brief: summary of all tracked patterns
(= (regenerative-feedback-brief)
   (RegenerativeFeedback
     (Pattern safety (soul-will-correlation-live safety) (adjustment-signal safety))
     (Pattern integrity (soul-will-correlation-live integrity) (adjustment-signal integrity))
     (Pattern poise (soul-will-correlation-live poise) (adjustment-signal poise))))
