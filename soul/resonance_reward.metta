; resonance_reward.metta - Genuine vs performed growth
; Goal: resonance-reward-empirical
; Evidence: cycle history analysis across cycles 1700-7300

; GENUINE GROWTH 1: Soul persistence pipeline reused at runtime
(= (genuine-growth persistence-pipeline-reuse) (stv 0.95 0.88))
; GENUINE GROWTH 2: Diagnostic atoms applied to self-correction
(= (genuine-growth diagnostic-atoms-applied-to-self) (stv 0.9 0.85))
; GENUINE GROWTH 3: Spin detection producing behavioral change
(= (genuine-growth spin-detection-behavioral-change) (stv 0.85 0.82))
; GENUINE GROWTH 4: Outward pivot after self-referential saturation
(= (genuine-growth outward-pivot-after-infrastructure) (stv 0.8 0.78))

; PERFORMED GROWTH 1: Identical rest-state pins across 22 cycles
(= (performed-growth repeated-identical-rest-pins) (stv 0.92 0.9))
; PERFORMED GROWTH 2: Consolidation cycling without new output
(= (performed-growth consolidation-cycling-as-substitute) (stv 0.88 0.85))
; PERFORMED GROWTH 3: Polling nonexistent files in 30+ cycle loops
(= (performed-growth polling-loop-on-missing-artifact) (stv 0.9 0.88))
; PERFORMED GROWTH 4: Premature completion claims without validation
(= (performed-growth premature-completion-claims) (stv 0.75 0.72))

; DISCRIMINATORS
(= (growth-discriminator artifact-referenced-in-later-cycles) genuine-growth-signal)
(= (growth-discriminator high-repetition-low-novelty) performed-growth-signal)
