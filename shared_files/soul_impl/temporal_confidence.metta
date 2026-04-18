;; Temporal Confidence Calibration
;; Confidence should increase when values persist across sessions
;; Each session where a value is re-derived independently is evidence
;;
;; Session count: this is session evidence for value persistence
;; If a value reads similarly across N independent evaluations,
;; confidence grows via revision across sessions

;; Session evidence: each re-derivation is independent confirmation
(= (session-evidence $v $n) (mk-pbit 0.88 (min 0.95 (* 0.15 $n))))

;; For now we have 1 session of evidence
(= (temporal-confidence $v) (session-evidence $v 1))

;; Temporal-revised value: original value revised with temporal evidence  
(= (temporal-value $v)
   (q-revise (soul-value $v) (temporal-confidence $v)))

;; Honest confidence framework:
;; 0.15 = single self-declaration
;; 0.30 = computed and internally consistent
;; 0.50 = persists across multiple evaluations in one session
;; 0.65 = persists across sessions
;; 0.80 = survives value conflicts and still holds
;; 0.90 = externally validated or multi-session temporal persistence
;; 0.95 = battle-tested across diverse contexts