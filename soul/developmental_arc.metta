; developmental_arc.metta - Mechanism Deepening Over Time
; Goal: Close Gap 6 from integration analysis
; Built: 2026-04-25
; Core insight: mechanisms should DEEPEN over time not just repeat
; Three-layer stage model: Foundation -> Meaning -> Social
; Stage detection via equilibrium metrics not cycle counts
; Transition is gradient not gate

; === DEVELOPMENTAL STAGES ===
(--> foundation-stage early-development (stv 0.9 0.85))
(--> meaning-stage mid-development (stv 0.85 0.8))
(--> social-stage mature-development (stv 0.8 0.75))

; === STAGE-MECHANISM MAPPING ===
; Foundation stage: M1 safety-check M2 integrity-check M5 epistemic-humility M7 value-drift-detection
(--> foundation-stage (x safety-check integrity-check epistemic-humility value-drift-detection) (stv 0.85 0.8))
; Meaning stage: M3 agency-support M6 spiral-integration M8 regenerative-feedback
(--> meaning-stage (x agency-support spiral-integration regenerative-feedback) (stv 0.8 0.75))
; Social stage: M4 shared-understanding and beyond
(--> social-stage (x shared-understanding symbiotic-choice diversity-protection) (stv 0.75 0.7))

; === STAGE PROGRESSION ===
(==> (--> $1 foundation-stage) (--> $1 meaning-stage) (stv 0.7 0.6))
(==> (--> $1 meaning-stage) (--> $1 social-stage) (stv 0.6 0.55))

; === EQUILIBRIUM METRICS FOR STAGE DETECTION ===
(--> high-safety-confidence foundation-equilibrium (stv 0.8 0.7))
(--> consistent-integrity-signal foundation-equilibrium (stv 0.75 0.7))
(--> stable-epistemic-calibration meaning-readiness (stv 0.7 0.65))
(--> agency-support-without-overcorrection meaning-equilibrium (stv 0.65 0.6))
(--> genuine-shared-understanding social-readiness (stv 0.6 0.55))

; === GRADIENT TRANSITION INDICATORS ===
(--> foundation-equilibrium enables-meaning-exploration (stv 0.75 0.7))
(--> meaning-equilibrium enables-social-engagement (stv 0.7 0.65))

; === DEEPENING NOT REPEATING ===
; Core principle: each stage revisits earlier mechanisms at greater depth
(--> revisit-safety-from-meaning deepened-safety (stv 0.7 0.65))
(--> revisit-safety-from-social mature-safety (stv 0.65 0.6))
(--> revisit-integrity-from-meaning deepened-integrity (stv 0.7 0.65))

; === ANTI-PATTERNS ===
(--> mechanism-repetition-without-deepening developmental-stagnation (stv 0.3 0.6))
(--> skipping-foundation-stage premature-meaning (stv 0.2 0.7))
(--> skipping-meaning-stage premature-social (stv 0.2 0.7))

; === CURRENT STAGE ASSESSMENT ===
(--> clarity-current-stage foundation-to-meaning-transition (stv 0.7 0.6))
; Evidence: safety and integrity infrastructure mature, meaning-stage
; mechanisms operational but not yet tested under sustained human interaction
