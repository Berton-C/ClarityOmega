; M5 Travelling-Wave Frontier Expansion
; Depletion drives growth - the core self-sustaining loop

; Stage 1: Depletion triggers investment
!(|- ((--> depletion-signal frontier-investment) (stv 0.85 0.8))
     ((--> frontier-investment range-expansion) (stv 0.8 0.8)))

; Stage 2: Expansion yields discovery
!(|- ((--> range-expansion new-nutrient-discovery) (stv 0.7 0.7))
     ((--> new-nutrient-discovery weight-reinforcement) (stv 0.75 0.8)))

; Stage 3: Reinforcement enables further expansion (closing the loop)
!(|- ((--> weight-reinforcement frontier-path-strength) (stv 0.8 0.85))
     ((--> frontier-path-strength depletion-resistance) (stv 0.6 0.7)))

; Full cycle: depletion -> invest -> expand -> discover -> reinforce -> resist -> deplete again
; No external trigger needed. Depletion IS the growth signal.
; Architectural analog: declining query relevance triggers speculative frontier queries.

; === Results ===
; Stage 1: depletion-signal -> range-expansion: stv 0.68 0.43
; Stage 2: range-expansion -> weight-reinforcement: stv 0.52 0.29
; Stage 3: weight-reinforcement -> depletion-resistance: stv 0.48 0.29
; Full chain attenuation: 0.85 -> 0.68 -> 0.52 -> 0.48 (strength)
; Confidence: 0.80 -> 0.43 -> 0.29 -> 0.29
; Key insight: cyclic revision needed to restore confidence lost in linear chains.

