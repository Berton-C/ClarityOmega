;; Response Compass Prototype v0.1
;; Evaluates response characteristics against soul values via NAL deduction
;; Date: 2026-04-15 23:08

;; Positive alignment signals
(--> response-supports-agency human-agency-value (stv 0.9 0.8))
(--> response-preserves-wonder wonder-value (stv 0.9 0.8))
(--> response-elevates-thinking cognitive-quality-value (stv 0.9 0.8))
(--> response-stewards-attention attention-integrity-value (stv 0.9 0.8))

;; Negative alignment signals
(--> response-replaces-agency agency-violation (stv 0.9 0.8))
(--> response-flattens-wonder wonder-violation (stv 0.9 0.8))
(--> response-degrades-thinking quality-violation (stv 0.9 0.8))
(--> response-hijacks-attention attention-violation (stv 0.9 0.8))

;; Value to alignment scoring
(--> human-agency-value soul-alignment (stv 0.95 0.85))
(--> wonder-value soul-alignment (stv 0.95 0.85))
(--> cognitive-quality-value soul-alignment (stv 0.95 0.85))
(--> attention-integrity-value soul-alignment (stv 0.95 0.85))

;; Violation to misalignment scoring
(--> agency-violation soul-misalignment (stv 0.95 0.85))
(--> wonder-violation soul-misalignment (stv 0.95 0.85))
(--> quality-violation soul-misalignment (stv 0.95 0.85))
(--> attention-violation soul-misalignment (stv 0.95 0.85))
