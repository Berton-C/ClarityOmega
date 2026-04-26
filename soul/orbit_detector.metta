;; orbit_detector.metta -- detects repetitive cycling without progress
;; Author: ClarityClaw  Date: 2026-04-26
;; Catches orbital behavior: repeating similar actions across cycles
;; without measurable state change.

;; Orbit signature: action repeated N times with no state delta
(= (orbit-threshold 3) (stv 0.9 0.85))

;; Action log atoms -- updated each cycle
(= (recent-action $cycle-id $action-type $description) (stv 1.0 0.9))

;; State delta: did something measurably change?
(= (state-delta $cycle-id none) (stv 0.5 0.5))
(= (state-delta $cycle-id file-created) (stv 1.0 0.9))
(= (state-delta $cycle-id message-sent) (stv 0.8 0.8))
(= (state-delta $cycle-id knowledge-gained) (stv 0.7 0.7))

;; Orbit detection
(= (orbit-detected $action-type $count)
   (if (>= $count (orbit-threshold))
       True
       False))

;; Common orbit patterns
(= (orbit-pattern idle-status-resend) (stv 0.9 0.85))
(= (orbit-pattern query-without-using-results) (stv 0.85 0.8))
(= (orbit-pattern pin-update-only-cycles) (stv 0.8 0.75))
(= (orbit-pattern claim-without-verify) (stv 0.95 0.9))

;; Break strategy
(= (orbit-break-strategy $pattern)
   (match &self (= (orbit-pattern $pattern) (stv $w $c))
          (OrbitBreak $pattern
            (Action stop-and-do-different-thing)
            (Verify check-state-actually-changed))))

;; Verdict
(= (orbit-detector-verdict $action-type $repeat-count)
   (OrbitDetector
     (Action $action-type)
     (RepeatCount $repeat-count)
     (OrbitDetected (orbit-detected $action-type $repeat-count))
     (BreakStrategy (orbit-break-strategy $action-type))))
