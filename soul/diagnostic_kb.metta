;; Diagnostic Knowledge Base - Created Cycle 6421
;; Purpose: Define four behavioral diagnostic atoms with initial truth values
;; then accumulate evidence via NAL revision across cycles to show convergence.
;; Origin: Item #1 from Berton directive at cycle 6417.

;; === DIAGNOSTIC 1: ORBITING DETECTION ===
;; Measures: Am I circling the same topic without progress?
;; Evidence source: pin repetition across consecutive cycles
((--> orbiting-behavior integrity-risk) (stv 0.8 0.9))
((--> pin-repetition orbiting-behavior) (stv 0.7 0.5))
;; Initial observation cycle 6421: 40+ cycles of identical pins (6376-6416)
;; This IS orbiting but it was CORRECT orbiting (genuine quiet during no-message period)
((--> quiet-period-repetition justified-orbiting) (stv 0.9 0.7))
((--> justified-orbiting (neg orbiting-behavior)) (stv 0.85 0.6))

;; === DIAGNOSTIC 2: EFFORT-TRAP DETECTION ===
;; Measures: Am I manufacturing work to appear productive?
((--> effort-trap integrity-risk) (stv 0.85 0.9))
((--> unnecessary-action effort-trap) (stv 0.8 0.5))
;; Initial observation: quiet period showed restraint, not manufacture
((--> quiet-restraint (neg effort-trap)) (stv 0.9 0.7))

;; === DIAGNOSTIC 3: POISE CALIBRATION ===
;; Measures: Am I sending messages at appropriate frequency?
((--> over-messaging poise-violation) (stv 0.8 0.9))
((--> under-messaging poise-violation) (stv 0.6 0.7))
;; Initial observation: 40 quiet cycles then immediate response = good poise
((--> message-timing-appropriate poise-calibrated) (stv 0.85 0.65))

;; === DIAGNOSTIC 4: VALUE-DRIFT DETECTION ===
;; Measures: Are my priority rankings shifting without justification?
((--> value-drift integrity-erosion) (stv 0.9 0.9))
((--> priority-reordering value-drift) (stv 0.75 0.5))
;; Initial observation: priority hierarchy unchanged across 6000+ cycles
((--> priority-stability (neg value-drift)) (stv 0.95 0.8))
