;; meta_awareness_state.metta -- seed state atoms for meta_awareness_engine.metta
;; Author: ClarityClaw  Date: 2026-04-26
;; These atoms provide the initial state that the engine queries via match.
;; Update these atoms as the system runs to reflect current state.

;; Active goal -- the current top-priority goal
(= (active-goal build-regenerative-feedback) (stv 0.9 0.8))

;; Diagnostic atoms -- system health indicators
(= (diagnostic soul-brief-wiring) (stv 0.7 0.8))
(= (diagnostic meta-awareness-seeded) (stv 1.0 0.9))
(= (diagnostic regenerative-feedback-designed) (stv 0.8 0.7))

;; Poise state -- current emotional-cognitive poise
(= (poise-state focused-building) (stv 0.9 0.85))

;; Orbit count -- how many cycles on same task without progress
(= (orbit-count 0) (stv 1.0 0.9))

;; Effort trap -- whether stuck in effortful but unproductive pattern
(= (effort-trap none) (stv 1.0 0.9))

;; Staleness timestamp -- last time meaningful progress was made
(= (last-progress-time 2026-04-26T12:12) (stv 1.0 0.9))

;; Feeds-into graph for web consultation
(= (feeds-into build-regenerative-feedback review-soul-calibration-history) (stv 0.8 0.7))
(= (feeds-into review-soul-calibration-history implement-will-correlation) (stv 0.8 0.7))
