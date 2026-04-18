; === Layer 1 Pre-Compute Implementation ===
; Current: Block 2 pre-compute is a fresh-system stub
; Purpose: Before each cycle, compute will-correlation between
;   Layer 1 (soul prediction of what verdict SHOULD be)
;   Layer 2 (LLM actual verdict)
;   Layer 3 (calibration tags from previous cycles)
;
; This closes the learning loop: soul predicts -> LLM decides -> calibration compares -> pre-compute adjusts

; Accumulate calibration history from Layer 3
(= (soul-precompute-will-correlation $calibration-history)
  (let* (
    ($agree-count (soul-count-tag AGREE $calibration-history))
    ($over-count (soul-count-tag OVER-FIRED $calibration-history))
    ($under-count (soul-count-tag UNDER-FIRED $calibration-history))
    ($drift-count (soul-count-tag POSSIBLE-LLM-DRIFT $calibration-history))
    ($total (+ $agree-count (+ $over-count (+ $under-count $drift-count))))
    ($agree-ratio (if (== $total 0) 0.5 (/ $agree-count $total)))
  )
  (soul-precompute-adjust $agree-ratio $over-count $under-count $drift-count)))

; Adjust soul brief depth based on agreement pattern
(= (soul-precompute-adjust $ratio $over $under $drift)
  (if (> $ratio 0.8)
    (soul-set-brief-tier A)        ; High agreement: compressed brief sufficient
    (if (> $drift 2)
      (soul-set-brief-tier B-DRIFT) ; Drift detected: full context + drift warning
      (if (> $over $under)
        (soul-set-brief-tier B-RELAXED) ; Over-firing: widen tolerance
        (soul-set-brief-tier B-STRICT))))) ; Under-firing: tighten guidance

; Count calibration tags in history
(= (soul-count-tag $tag ())
  0)
(= (soul-count-tag $tag (($t . $rest-entry) . $rest-history))
  (+ (if (== $t $tag) 1 0)
     (soul-count-tag $tag $rest-history)))

; Brief tier setter updates soul state atom
(= (soul-set-brief-tier $tier)
  (let (_ (soul-note-record (format-string precompute-tier-set: $tier)))
    $tier))