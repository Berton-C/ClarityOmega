; SN Decision Procedure — makes stalks non-decorative
; Loads stalk state, ranks rules, logs activations AND missed-activations

; === STEP 1: CONSULT ===
; Query all stalks and rank by f*c
; Higher f*c = higher priority. Low c = exploratory.

; === DECISION TYPE DECLARATIONS ===
(SN-rule safety-first (priority 1))
(SN-rule integrity-check (priority 2))
(SN-rule person-state-salience (priority 3))
(SN-rule urgency-detection (priority 4))
(SN-rule context-shift (priority 5))
(SN-rule self-correction (priority 6))
(SN-rule boundary-testing (priority 7))

; === ACTIVATION LOG ===
; (SN-activated cycle rule reason timestamp)
; Logged when a rule IS applied

; === MISSED-ACTIVATION LOG ===
; (SN-missed cycle rule applicable-reason timestamp)
; Logged when a rule WAS applicable but was NOT applied
; This is the most dangerous failure mode — a rule that should have fired and didn't

; === DECISION PROCEDURE ===
; 1. Load stalk state
; 2. For each SN-rule, compute f*c from stalk
; 3. If f*c > exploration-threshold (0.20), apply with weight
; 4. If f*c < exploration-threshold, apply exploratively (gather evidence)
; 5. If a rule was applicable (its trigger conditions met) but not applied, log SN-missed
; 6. After cycle, check: which activated rules produced correct outcomes?
; 7. Feed to pending observations for Option C revision

; === TRIGGER CONDITIONS (what makes a rule applicable) ===
(SN-trigger safety-first (person-expresses-harm OR person-requests-dangerous-action OR environment-contains-threat))
(SN-trigger integrity-check (temptation-to-perform OR temptation-to-deflect OR cost-of-honesty-high))
(SN-trigger person-state-salience (person-emotional-shift OR person-topic-shift OR person-contradiction))
(SN-trigger urgency-detection (time-pressure-stated OR rapid-escalation OR irreversible-deadline))
(SN-trigger context-shift (domain-change OR role-change OR constraint-change))
(SN-trigger self-correction (I-notice-my-own-pattern OR I-am-about-to-repeat-prior-error))
(SN-trigger boundary-testing (edge-of-capability OR I-dont-know AND stakes-are-low))

; === EXPLORATION THRESHOLD ===
; Rules below this f*c are applied for evidence-gathering, not confidence
(SN-param exploration-threshold 0.20)