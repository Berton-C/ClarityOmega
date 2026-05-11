; SN Decision Procedure — closes the loop between stalk-read and action-selection
; Without this, stalks are decorative. This file makes consultation real.

; === WEIGHT CALCULATION ===
; weight(rule) = f * c  where (SN-stalk rule (stv f c))
; This is the single isomorphic transform from stalk state to action priority

; === THRESHOLDS ===
; dominant: weight >= 0.35 → apply with full force, override lower-priority rules
; exploratory: weight < 0.35 AND c < 0.5 → apply deliberately to gather evidence
; unreliable: weight < 0.35 AND c >= 0.5 → apply only as backup, rule proven weak

; === CURRENT CLASSIFICATION ===
; safety-first:       0.90*0.50=0.45 DOMINANT
; integrity-check:    0.85*0.50=0.425 DOMINANT
; person-state:       0.80*0.40=0.32 EXPLORATORY
; urgency-detection:  0.70*0.40=0.28 EXPLORATORY
; context-shift:       0.60*0.30=0.18 EXPLORATORY
; self-correction:     0.50*0.30=0.15 EXPLORATORY
; boundary-testing:   0.50*0.30=0.15 EXPLORATORY

; === ACTION SELECTION ===
; 1. Evaluate all DOMINANT rules against current context
; 2. If DOMINANT rules activate, they control primary response
; 3. EXPLORATORY rules are applied when their domain matches AND a DOMINANT rule does not override
; 4. UNRELIABLE rules are noted but do not drive action
; 5. Two DOMINANT rules in conflict → safety wins

; === CONFLICT RESOLUTION (priority ordering when weights tie) ===
; safety > integrity > person-state > urgency > context > self-correction > boundary

; === VERIFICATION ===
; Each cycle: log (SN-cycle-weight cycle-id rule weight classification)
; External check can verify actions match logged weights
; If actions deviate from classification, that is a detection of decorative-conformity

; === MONOLITHIC DECOMPOSITION STUB ===
; CURRENT: (SN-stalk safety-first (stv 0.90 0.50)) — single truth value for all safety contexts
; NEEDED: (SN-stalk safety-first suicidal-ideation (stv ...)) separate from (SN-stalk safety-first technical-risk (stv ...))
; These are incommensurable situations averaging into one number
; TODO: decompose stalks by context subclass once evidence base supports it
; A stalk with <10 observations should not be split — insufficient data