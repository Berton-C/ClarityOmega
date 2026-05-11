; SN-stalk observation hook (Option C — delayed evidence)
;
; When I apply a salience rule in cycle N, I log a pending observation.
; When subsequent human response provides evidence, I convert to revision.
;
; PENDING FORMAT:
; (SN-pending cycle-id rule-name predictedSalient timestamp)
;
; EVIDENCE FORMAT (when it arrives):
; (SN-evidence cycle-id rule-name correct? timestamp)
;
; REVISION:
; correct  -> (|- (SN-stalk $rule (stv $current_f $current_c)) (SN-stalk $rule (stv 1.0 0.1)))
; wrong   -> (|- (SN-stalk $rule (stv $current_f $current_c)) (SN-stalk $rule (stv 0.0 0.1)))
;
; After revision, write updated state to sn_stalk_state.metta
; Remove resolved pending from state file
