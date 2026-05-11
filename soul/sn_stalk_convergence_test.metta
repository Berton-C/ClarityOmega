; Stalk learning convergence test
; If the revision mechanism works, stalk frequency should converge toward observed accuracy
; Synthetic test: true accuracy for urgency-detection is 0.60
; Start: (stv 0.70 0.40), feed 20 observations at 60% correct

; Helper: batch-revise applies N observations sequentially
; 12 correct observations (60% of 20): evidence (stv 1.0 0.05) each
; 8 incorrect observations (40% of 20): evidence (stv 0.0 0.05) each
; Expected result: frequency should drift from 0.70 toward 0.60

; Test Step 1: Start state
(SN-stalk urgency-detection (stv 0.70 0.40))

; Test Step 2: Apply one correct observation
; (|- (SN-stalk urgency-detection (stv 0.70 0.40))
;     (SN-stalk urgency-detection (stv 1.0 0.05)))
; Expected: f moves toward 1.0 by small amount, c increases slightly

; Test Step 3: Apply one incorrect observation
; (|- (result-from-step2) (SN-stalk urgency-detection (stv 0.0 0.05)))
; Expected: f pulled back downward, c increases

; After 20 steps the stalk should approximate (stv ~0.60 high-c)
; If it does: learning works. If not: revision is cosmetic.
; Run manually one observation at a time to trace convergence.
