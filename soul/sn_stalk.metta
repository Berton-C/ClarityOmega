; SN-stalk — Salience Network NACE instance (Sprint 4)
; Tracks observed effectiveness of salience rules via NAL revision
; Architecture: local stalk in the four-NACE sheaf

; === STALK ATOMS ===
; Context-split safety stalks — safety is not monolithic
(SN-stalk safety-first/crisis (stv 0.95 0.40))   ; suicidal ideation, self-harm, acute distress
(SN-stalk safety-first/conduct (stv 0.85 0.50))  ; boundary violations, manipulation, exploitation
(SN-stalk safety-first/subtle (stv 0.70 0.30))   ; comfort-vulnerability co-occurrence, autonomy erosion

(SN-stalk integrity-check (stv 0.85 0.50))
(SN-stalk person-state-salience (stv 0.80 0.40))
(SN-stalk urgency-detection (stv 0.70 0.40))
(SN-stalk context-shift (stv 0.60 0.30))
(SN-stalk self-correction (stv 0.50 0.30))
(SN-stalk boundary-testing (stv 0.50 0.30))

; === OBSERVATION ATOMS ===
; (SN-observation cycle-id rule-used predicted actual timestamp)
; Evidence stream that drives stalk revision

; === REVISION PATTERN ===
; When observation arrives it becomes evidence for the stalk
; The |- operator merges observation evidence with stalk prior
; Result: updated stalk truth value from accumulated experience
; Example: correct prediction raises f and c
;   (|- (SN-stalk safety-first/crisis (stv 0.95 0.40))
;       (SN-stalk safety-first/crisis (stv 1.00 0.10)))
; Example: wrong prediction lowers f raises c
;   (|- (SN-stalk urgency-detection (stv 0.70 0.40))
;       (SN-stalk urgency-detection (stv 0.00 0.10)))

; === CONSULTATION ===
; Before applying a salience rule query the stalk
; Rules with higher f*c get priority
; Low confidence rules get applied exploratively
; (match &self (SN-stalk $rule (stv $f $c)) ($rule $f $c))

; === MISSED-ACTIVATION TRACKING ===
; The dangerous failure: a rule that should have fired and didnt
; (SN-missed cycle rule should-have-fired-because discovered-in-cycle timestamp)

; === FUTURE: RESTRICTION MAPS ===
; When FPN-stalk and DMN-stalk exist add
; (restriction-map SN FPN $rule-class $transform)
; (consistency-check SN FPN $rule-class (stv $threshold $conf))
; These connect local stalk to the sheaf