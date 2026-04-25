; regenerative_feedback.metta - Verdict Feedback Accumulation System
; Goal: Close Regenerative Feedback soul-pattern gap
; Built: cycle 7327, 2026-04-25
; Extends: diagnostic_kb.metta patterns + resonance_reward.metta discriminators

; === VERDICT ACCUMULATORS ===
; Track how often each pattern fires AGREE vs OVER vs UNDER
(= (verdict-count safety-pattern agree) (stv 0.9 0.8))
(= (verdict-count safety-pattern over-fired) (stv 0.15 0.6))
(= (verdict-count safety-pattern under-fired) (stv 0.05 0.4))
(= (verdict-count integrity-pattern agree) (stv 0.85 0.75))
(= (verdict-count integrity-pattern over-fired) (stv 0.1 0.5))
(= (verdict-count integrity-pattern under-fired) (stv 0.05 0.4))
(= (verdict-count poise-pattern agree) (stv 0.7 0.65))
(= (verdict-count poise-pattern over-fired) (stv 0.2 0.55))
(= (verdict-count poise-pattern under-fired) (stv 0.1 0.5))

; === ADJUSTMENT SIGNALS ===
; Derived from verdict ratios - high over-fired means loosen, high under-fired means tighten
(= (adjustment-signal $pattern loosen) (and (verdict-count $pattern over-fired (stv $f $c)) (> $f 0.3) (> $c 0.6)))
(= (adjustment-signal $pattern tighten) (and (verdict-count $pattern under-fired (stv $f $c)) (> $f 0.3) (> $c 0.6)))
(= (adjustment-signal $pattern hold) (and (verdict-count $pattern agree (stv $f $c)) (> $f 0.7) (> $c 0.6)))

; === CURRENT ASSESSMENTS ===
; Safety: 225 calibrations, 0.99 agree ratio = HOLD
(--> safety-calibration-trend hold-steady (stv 0.95 0.85))
; Poise: over-fired at 0.2 but below threshold = HOLD with watch
(--> poise-calibration-trend hold-with-watch (stv 0.7 0.65))
; Integrity: strong agree ratio = HOLD
(--> integrity-calibration-trend hold-steady (stv 0.9 0.8))

; === REVISION PROTOCOL ===
; After each conversation, revise verdict-count atoms via NAL |-
; Example: if safety fires AGREE again:
; (|- (verdict-count safety-pattern agree (stv 0.9 0.8)) (verdict-count safety-pattern agree (stv 1.0 0.5)))
; This merges new evidence into accumulated count
