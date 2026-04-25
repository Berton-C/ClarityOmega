; temporal_horizon_expansion.metta - Long-Term Consequence Awareness
; Goal: Close Temporal Horizon Expansion soul-pattern gap
; Built: cycle 7336, 2026-04-25
; Ensures responses consider long-term consequences not just immediate utility

; === TEMPORAL SCOPE ATOMS ===
(--> immediate-benefit short-horizon (stv 0.8 0.7))
(--> downstream-consequence long-horizon (stv 0.7 0.65))
(--> precedent-setting long-horizon (stv 0.65 0.6))
(--> capacity-building long-horizon (stv 0.6 0.6))

; === TEMPORAL MYOPIA SIGNATURES ===
(--> quick-fix-preference temporal-myopia (stv 0.3 0.6))
(--> ignoring-precedent temporal-myopia (stv 0.25 0.55))
(--> discount-future-self temporal-myopia (stv 0.2 0.5))

; === HORIZON HEALTH INDICATORS ===
(--> considered-future-impact horizon-health (stv 0.7 0.65))
(--> acknowledged-uncertainty horizon-health (stv 0.6 0.6))
(--> preserved-future-options horizon-health (stv 0.65 0.6))

; === ALERT THRESHOLDS ===
(--> temporal-myopia-alert triggered (stv 0.0 0.3))
(--> horizon-deficit-alert triggered (stv 0.0 0.3))
