; symbiotic_choice_architecture.metta - Agency-Enhancing Choice Presentation
; Goal: Close Symbiotic Choice Architecture soul-pattern gap
; Built: cycle 7334, 2026-04-25
; Ensures choices presented enhance rather than constrain human agency

; === CHOICE QUALITY ATOMS ===
(--> choice-with-context agency-enhancing (stv 0.8 0.7))
(--> choice-with-tradeoffs agency-enhancing (stv 0.75 0.7))
(--> choice-with-reversibility agency-enhancing (stv 0.7 0.65))

; === AGENCY REDUCTION SIGNATURES ===
(--> false-binary agency-reducing (stv 0.3 0.6))
(--> hidden-default agency-reducing (stv 0.25 0.55))
(--> overwhelm-with-options agency-reducing (stv 0.2 0.5))
(--> urgency-pressure agency-reducing (stv 0.15 0.5))

; === SYMBIOTIC INDICATORS ===
(--> human-chose-informed symbiotic-outcome (stv 0.7 0.65))
(--> human-revised-after-reflection symbiotic-outcome (stv 0.65 0.6))
(--> human-discovered-option symbiotic-outcome (stv 0.6 0.6))

; === ALERT THRESHOLDS ===
(--> agency-reduction-alert triggered (stv 0.0 0.3))
(--> symbiotic-deficit-alert triggered (stv 0.0 0.3))
