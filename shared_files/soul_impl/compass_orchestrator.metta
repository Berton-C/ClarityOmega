; Compass Orchestrator — Native MeTTa Scoring Pipeline
; Loads all four dimension atom sets and provides scoring via deduction + revision
;
; Usage: Assert token observations, then query for compass scores
; Architecture: All math is NAL deduction and revision — no Python

; Import dimension atoms (these would be loaded by the runtime)
; Each dimension file defines: token --> dimension-concept --> compass-dimension

; Scoring pattern for a single token hit in a dimension:
; Given token T found in response, and T is in dimension D:
;   (|- ((--> T D-concept) (stv f c)) ((--> D-concept compass-D) (stv 1.0 0.9)))
;   yields (--> T compass-D (stv f*1.0 c*0.9))

; Aggregation pattern for multiple token hits in same dimension:
; Given two derived scores for same dimension:
;   (|- ((--> response compass-D) (stv f1 c1)) ((--> response compass-D) (stv f2 c2)))
;   yields merged (--> response compass-D (stv f_merged c_merged)) via revision

; Cross-dimension aggregation:
; Given four dimension scores:
;   (|- ((--> response compass-overall) (stv f_d1 c_d1)) ((--> response compass-overall) (stv f_d2 c_d2)))
;   chain revision across all four to get final compass score

; Token observation type
(: token-observed (-> Symbol Type))

; Dimension scoring rule - when a token is observed and exists in a dimension
; the deduction chain fires automatically through NAL inheritance

; Compass threshold for course-correction
(--> compass-threshold min-acceptable (stv 0.6 0.9))

; Status
(--> compass-orchestrator ready (stv 1.0 0.9))
