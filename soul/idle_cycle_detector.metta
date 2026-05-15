;; idle_cycle_detector.metta -- send-burst awareness organ
;; v2 cycle-level wiring per Step 4.5 corrected (algorithm-d, May 15 2026)
;;
;; Detects send-class action accumulation in the 10-cycle recent-action window.
;; Emits (idle-pattern $verdict $count) atom each cycle for prompt-block consumption.
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
;;   - Mirror pattern (no change-state!; freshness via remove-atom + add-atom)
;;   - do-*! naming for side-effecting writers

;; Send-burst detection threshold -- 3 send-class actions in 10-cycle window.
;; Documentation atom (queryable, but not read by the comparison below).
;; NOTE: if you change this value, also update the literal 3 in
;; (do-update-idle-pattern!) below. Threshold lives in two places by design
;; (F39: avoiding unverified (send-burst-threshold) extraction patterns).
(= (send-burst-threshold 3) (stv 0.9 0.8))

;; ===== ALGORITHM (d): pre-filtered match + size-atom counter =====

;; Count send-class actions in current recent-action window.
;; Two direct matches (one per send-class tag literal), summed with +.
;; Every primitive REPL-verified to work in this runtime (May 15 2026).
(= (count-sends-in-window)
   (+ (size-atom (collapse (match &self (recent-action $c responsive-send $d) $c)))
      (size-atom (collapse (match &self (recent-action $c status-send-unprompted $d) $c)))))

;; ===== PUBLIC READ HELPER =====

;; Returns (verdict count) tuple or () if not yet computed (pre-bootstrap).
(= (current-idle-pattern)
   (let $atoms (collapse (match &self (idle-pattern $v $c) ($v $c)))
      (if (== $atoms ())
          ()
          (car-atom $atoms))))

;; ===== FRESHNESS CLEARER =====

;; Removes prior idle-pattern atom (C12-safe).
(= (do-clear-idle-pattern!)
   (let $existing (collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))

;; ===== CYCLE-LEVEL WRITER =====

;; Runs each cycle from loop.metta after populate-recent-action.
;; Computes send-count via algorithm (d), derives verdict, emits fresh atom.
;; Threshold 3 hardcoded per F39 (declaration atom above is documentation only).
(= (do-update-idle-pattern!)
   (let* (($count (count-sends-in-window))
          ($verdict (if (> $count 3)
                        send-burst
                        productive)))
      (progn
         (do-clear-idle-pattern!)
         (add-atom &self (idle-pattern $verdict $count)))))

;; ===== PROMPT BLOCK HELPER =====

;; Composes the IDLE-PATTERN block for prompt assembly via Python formatter.
(= (idle-pattern-block)
   (let $pattern (current-idle-pattern)
      (if (== $pattern ())
         (py-call (helper.idle_pattern_block_format productive 0))
         (let $v (car-atom $pattern)
            (let $c (car-atom (cdr-atom $pattern))
               (py-call (helper.idle_pattern_block_format $v $c)))))))
