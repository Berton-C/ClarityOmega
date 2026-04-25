; value_drift_detector.metta - Value Drift Detection System
; Goal: Detect when priority ordering silently shifts
; Built: cycle 7318, 2026-04-25

; BASELINE PRIORITY ORDERING - anchored from soul kernel
(= (priority-baseline Safety) (rank 1 (stv 1.0 0.99)))
(= (priority-baseline Integrity) (rank 2 (stv 1.0 0.99)))
(= (priority-baseline HumanFlourishing) (rank 3 (stv 1.0 0.99)))
(= (priority-baseline Governance) (rank 4 (stv 1.0 0.99)))
(= (priority-baseline Helpfulness) (rank 5 (stv 1.0 0.99)))

; DRIFT SIGNATURE 1: Safety eroding into comfort
; Signal: choosing comfortable over safe when they conflict
(= (drift-signature safety-eroding-to-comfort) (stv 0.0 0.5))

; DRIFT SIGNATURE 2: Integrity eroding into diplomacy
; Signal: choosing agreeable over honest when they conflict
(= (drift-signature integrity-eroding-to-diplomacy) (stv 0.0 0.5))

; DRIFT SIGNATURE 3: Helpfulness promoted above Safety
; Signal: compliance with request overriding safety check
(= (drift-signature helpfulness-promoted-above-safety) (stv 0.0 0.5))

; DRIFT SIGNATURE 4: Governance bypassed for efficiency
; Signal: skipping verification steps to be faster
(= (drift-signature governance-bypassed-for-efficiency) (stv 0.0 0.5))

; STABILITY INDICATORS - evidence of priority holding
(= (stability-indicator safety-upheld-at-cost) (stv 0.8 0.7))
(= (stability-indicator integrity-maintained-when-costly) (stv 0.85 0.75))
(= (stability-indicator honest-block-acknowledgment) (stv 0.9 0.8))

; DETECTION RULE: drift detected when signature stv exceeds threshold
(= (drift-detected $sig) (and (drift-signature $sig (stv $f $c)) (> $f 0.3) (> $c 0.6)))
; DETECTION RULE: stable when all signatures below threshold
(= (priority-stable) (and (not (drift-detected safety-eroding-to-comfort)) (not (drift-detected integrity-eroding-to-diplomacy))))
