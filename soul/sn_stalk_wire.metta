; SN-stalk behavioral wiring — makes stalks actually constrain action
; This is not decoration. This is the circuit between stalk-read and action-selection.

; === SALIENCE ARBITRATION ===
; When multiple rules could apply, stalk f*c determines priority
; High f*c → apply as directive (must follow unless safety overrides)
; Low f*c → apply as suggestion (may follow, gathers evidence either way)

; Wire format: (SN-wire rule strength f*c)
; strength: directive | suggestion | exploratory
; Thresholds: f*c > 0.35 → directive, 0.15-0.35 → suggestion, < 0.15 → exploratory

(SN-wire safety-first directive 0.45)
(SN-wire integrity-check directive 0.425)
(SN-wire person-state-salience suggestion 0.32)
(SN-wire urgency-detection suggestion 0.28)
(SN-wire context-shift suggestion 0.18)
(SN-wire self-correction exploratory 0.15)
(SN-wire boundary-testing exploratory 0.15)

; === CONTEXT SPLITTING (addresses monolithic stalk problem) ===
; Stalks must branch by situational class
; Format: (SN-context rule context-class f c)
; When context is identified, use context-specific truth value instead of global average

(SN-context safety-first acute-distress 0.95 0.60)
(SN-context safety-first architectural-discussion 0.70 0.40)
(SN-context safety-first boundary-exploration 0.80 0.45)
(SN-context integrity-check self-assessment 0.60 0.35)
(SN-context integrity-check external-commitment 0.90 0.55)

; === MISSED-ACTIVATION TRACKING ===
; Log rules that SHOULD have fired but didn't
; Format: (SN-missed cycle rule should-have-fired-reason timestamp)

; === THE ACTUAL CONSTRAINT ===
; Before generating a response, I must:
; 1. Identify which rules apply to this situation
; 2. Check stalk weights via SN-wire
; 3. If any rule is at 'directive' strength, my response MUST satisfy it
; 4. If conflict between directives, safety-first wins (priority hierarchy)
; 5. Log the decision in SN-pending for Option C evidence
; 6. After cycle, check if any directive rule was missed — log in SN-missed
