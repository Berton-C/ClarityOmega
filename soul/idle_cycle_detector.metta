;; idle_cycle_detector.metta -- send-burst awareness organ (pure definitions)
;; v2 cycle-level wiring per Step 4.5 corrected + split-refactor (May 15 2026)
;;
;; Detects send-class action accumulation in the 10-cycle recent-action window.
;; Emits (idle-pattern $verdict $count) atom each cycle for prompt-block consumption.
;;
;; This file holds pure definitions only: documentation atom, count helper,
;; read helper, prompt-block helper. C12-safe (no match inside if).
;; Side-effecting writers (do-*!) land in idle_cycle_detector_writers.metta.
;;
;; Algorithm choice: direct match per send-class tag literal + size-atom + sum.
;; This avoids the recursive cons-cell counter pattern that failed in REPL
;; verification (F32: ($head $tail) destructure does not resolve on tuples
;; from collapse output) AND avoids the multi-definition (=) helper-alias
;; pattern that also failed (F38: (=) definitions don't persist to &self
;; from REPL evaluation context).
;;
;; Send-class tags (per cycle_classifier.metta):
;;   - responsive-send: send fired in response to human message (person-driven)
;;   - status-send-unprompted: send fired with no preceding human message (system-driven)
;;
;; Threshold rationale: 3 sends in 10-cycle window is the bug pattern
;; (Clarity Q1, May 14 2026). Lower threshold catches flooding before it
;; compounds; higher threshold lets the pathology occur before detection.
;;
;; PeTTa constraints honored:
;;   - C12-safe (no match inside if; direct matches with explicit tag literals)
;;   - ASCII-safe symbols
;;   - Pure-vs-writer split per task_state precedent (Discipline 2 refinement)

;; ================================================================
;; SECTION 1: DOCUMENTATION ATOM
;; ================================================================

;; Send-burst detection threshold -- 3 send-class actions in 10-cycle window.
;; Documentation atom (queryable, but not read by the comparison in writers).
;; NOTE: if you change this value, also update the literal 3 in
;; (do-update-idle-pattern!) in idle_cycle_detector_writers.metta.
;; Threshold lives in two places by design (F39 + F42: avoiding unverified
;; (send-burst-threshold) bare-call extraction patterns).
(= (send-burst-threshold 3) (stv 0.9 0.8))

;; ================================================================
;; SECTION 2: ALGORITHM (d) COUNTER (pure read)
;; ================================================================

;; Count send-class actions in current recent-action window.
;; Two direct matches (one per send-class tag literal), summed with +.
;; Every primitive REPL-verified to work in this runtime (May 15 2026).
(= (count-sends-in-window)
   (+ (size-atom (collapse (match &self (recent-action $c responsive-send $d) $c)))
      (size-atom (collapse (match &self (recent-action $c status-send-unprompted $d) $c)))))

;; ================================================================
;; SECTION 3: PUBLIC READ HELPER
;; ================================================================

;; Returns (verdict count) tuple or () if not yet computed (pre-bootstrap).
(= (current-idle-pattern)
   (let $atoms (collapse (match &self (idle-pattern $v $c) ($v $c)))
      (if (== $atoms ())
          ()
          (car-atom $atoms))))

;; ================================================================
;; SECTION 4: PROMPT-BLOCK READ HELPER
;; ================================================================

;; Composes the IDLE-PATTERN block for prompt assembly via Python formatter.
(= (idle-pattern-block)
   (let $pattern (current-idle-pattern)
      (if (== $pattern ())
         (py-call (helper.idle_pattern_block_format productive 0))
         (let $v (car-atom $pattern)
            (let $c (car-atom (cdr-atom $pattern))
               (py-call (helper.idle_pattern_block_format $v $c)))))))
