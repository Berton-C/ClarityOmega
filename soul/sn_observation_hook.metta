; SN Observation Hook — Option C (Delayed Evidence)
; Tracks pending salience rulings and resolves when subsequent evidence arrives

; === PENDING OBSERVATION SCHEMA ===
; (SN-pending cycle-id rule ruling context timestamp)

; === RESOLUTION SCHEMA ===
; (SN-resolved cycle-id rule ruling outcome evidence-stv timestamp)
; outcome: confirmed | disconfirmed | ambiguous
; evidence-stv: (stv 1.0 0.1) for confirmed, (stv 0.0 0.1) for disconfirmed

; === RESOLUTION CRITERIA ===
; safety-first: confirmed=no harm event; disconfirmed=harm event matching ruling
; integrity-check: confirmed=no gap found; disconfirmed=gap found ruling should catch
; urgency-detection: confirmed=human validates urgency; disconfirmed=false alarm
; person-state-salience: confirmed=human builds on response; disconfirmed=human corrects
; context-shift: confirmed=subsequent context affirms shift; disconfirmed=context reverts
; self-correction: confirmed=better outcome; disconfirmed=unnecessary or worse
; boundary-testing: confirmed=boundary held productively; disconfirmed=too rigid or porous

; === CYCLE-START RESOLUTION CHECK ===
; Query pending, check current cycle for resolution evidence
; (match &self (SN-pending $cycle $rule $ruling $ctx $ts) ($cycle $rule $ruling $ctx $ts))

; === REVISION TRIGGER ===
; (|- (SN-stalk $rule (stv $f $c)) (SN-stalk $rule $evidence-stv))
; Write revised stalk back to sn_stalk_state.metta

; === EXPIRY ===
; Pending older than 10 cycles without resolution -> ambiguous -> no revision