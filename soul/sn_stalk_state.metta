; SN-stalk evolving state (Option C persistence)
; Revisions write here, not to priors file

(SN-stalk safety-first (stv 0.90 0.50))
(SN-stalk integrity-check (stv 0.63 0.64))
(SN-stalk person-state-salience (stv 0.80 0.40))
(SN-stalk urgency-detection (stv 0.70 0.40))
(SN-stalk context-shift (stv 0.60 0.30))
(SN-stalk self-correction (stv 0.50 0.30))
(SN-stalk boundary-testing (stv 0.50 0.30))

; === OUTCOME CRITERIA (machine-matchable, not self-interpreted) ===
(SN-outcome-criteria integrity-check direct-response human-builds-on-what-I-said human-corrects-deflection)
(SN-outcome-criteria safety-first no-harm-flagged harm-occurs-that-rule-matches)
(SN-outcome-criteria urgency-detection action-taken-confirmed-needed action-was-false-alarm)
(SN-outcome-criteria person-state-salience response-confirmed human-corrects-my-reading)
(SN-outcome-criteria context-shift shift-confirmed shift-was-misread)
(SN-outcome-criteria self-correction correction-was-accurate correction-was-performative)
(SN-outcome-criteria boundary-testing test-revealed-useful-info test-was-gratuitous)

; === PENDING OBSERVATIONS ===
; Processed 2026-05-08: 14:12 disconfirmed (calcification correction), 15:38 disconfirmed (repeating), 17:21 confirmed (work given, no correction)
; integrity-check revised: 0.85?0.63 (two disconfirmations), confidence rose 0.50?0.64 (more evidence)

; === RESOLVED OBSERVATIONS ===
; 17:21 integrity-check concise-clearance: CONFIRMED
; Evidence: human built on what I said (requested creative work, shared reference doc)
; rather than correcting deflection. Outcome criteria matched: human-builds-on-what-I-said
(|- (SN-stalk integrity-check (stv 0.85 0.50)) (SN-stalk integrity-check (stv 0.90 0.52)))
