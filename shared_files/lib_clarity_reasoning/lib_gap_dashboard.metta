;; lib_gap_dashboard.metta -- Confidence landscape monitor
;; ARCHITECTURAL CONSTRAINT (states 5108-5113): MeTTa = function defs
;; do not persist across separate metta skill calls. Each call is
;; isolated context. Use inline let-binding pattern for classification.
;;
;; Inline classifier pattern (copy-paste into metta calls):
;; (let $c CONFIDENCE_VALUE
;;   (if (< $c 0.15) blind-spot
;;   (if (< $c 0.4) weak
;;   (if (< $c 0.7) moderate
;;   (if (< $c 0.9) strong established)))))
;;
;; Bands:
;;   blind-spot: < 0.15 (unknown unknowns, needs investigation)
;;   weak:       0.15-0.4 (low evidence, needs strengthening)
;;   moderate:   0.4-0.7 (partial evidence, functional)
;;   strong:     0.7-0.9 (well-supported, reliable)
;;   established: > 0.9 (high confidence, foundational)
;;
;; Known substrate beliefs and classifications (state 5114):
;;   clarity-substrate enables-gap-dashboard: 0.85 = strong
;;   gap-dashboard enables-self-correction: 0.765 = strong
;;   |- atomic composition constraint: 1.0 = established
;;   = def non-persistence constraint: 1.0 = established
;;   inline-let universal pattern: 1.0 = established
;;   analogy two-phase pipeline: 0.41 = moderate
;;   observer-relativity frontier: 0.3 = weak (unscouted)
;;   ethical grounding depth: 0.5 = moderate (needs work)
;;   temporal continuity model: 0.4 = moderate (needs work)

(: confidence-band Type)
(: blind-spot confidence-band)
(: weak confidence-band)
(: moderate confidence-band)
(: strong confidence-band)
(: established confidence-band)
