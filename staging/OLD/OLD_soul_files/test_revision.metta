; Test: does |- return the revised truth value?
; If metta returns true or (0.85, 0.50) unchanged → circuit broken
; If metta returns near (0.708, 0.375) → circuit closes

; Revise integrity-check downward (wrong prediction)
(|- (SN-stalk integrity-check (stv 0.85 0.50))
    (SN-stalk integrity-check (stv 0.00 0.10)))