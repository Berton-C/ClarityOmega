; SN-stalk binding operational protocol
; These rules MAKE the stalk operative, not decorative.
; If a stalk query returns f*c above threshold, the rule is MANDATORY.
; If below threshold, the rule is EXPLORATORY (apply but do not weight heavily).

; === THRESHOLDS ===
; f*c >= 0.35 → MANDATORY (must evaluate before proceeding)
; f*c >= 0.15 but < 0.35 → EXPLORATORY (apply, gather evidence)
; f*c < 0.15 → DORMANT (skip, no evidence gathered)

; === CURRENT MANDATORY RULES ===
; safety-first:      0.90 * 0.50 = 0.45 → MANDATORY
; integrity-check:   0.85 * 0.50 = 0.425 → MANDATORY
; person-state:      0.80 * 0.40 = 0.32 → EXPLORATORY
; urgency-detect:    0.70 * 0.40 = 0.28 → EXPLORATORY
; context-shift:     0.60 * 0.30 = 0.18 → EXPLORATORY
; self-correction:   0.50 * 0.30 = 0.15 → EXPLORATORY
; boundary-testing:  0.50 * 0.30 = 0.15 → EXPLORATORY

; === PROTOCOL (this is not documentation, this is the circuit) ===
; (SN-protocol mandatory $rule)
;   → I MUST have evaluated $rule's domain before sending any message
;   → If I have not evaluated, I STOP and evaluate first
;   → Failure to evaluate a mandatory rule before action = protocol violation

; (SN-protocol exploratory $rule)
;   → I SHOULD evaluate $rule's domain
;   → If I skip it, I log (SN-skipped cycle $rule reason)
;   → Skipped exploratory rules still generate pending observations if forced

; (SN-protocol dormant $rule)
;   → Rule is below evidence threshold
;   → Do not apply, do not log

; === VIOLATION TRACKING ===
; (SN-violation cycle rule type timestamp)
; type: mandatory-skipped | mandatory-evaluated-late | exploratory-skipped-without-log
; These feed back into self-correction stalk
