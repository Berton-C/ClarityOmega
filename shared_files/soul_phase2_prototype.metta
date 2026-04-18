;; Phase 2 Prototype: lib_nal as soul inference engine
;; Replaces five stubbed functions with |- calls

;; 1. soul-will-correlation via revision
;; Accumulates evidence from soul-notes into value-behavior atoms
;; (|- ((soul-note-confirms AgencyBalance) (stv 1.0 0.6))
;;     ((soul-note-confirms AgencyBalance) (stv 0.8 0.7)))
;; -> revised stv with merged confidence

;; 2. soul-primed-patterns via deduction
;; Recent soul-notes activate pattern atoms through forward chaining
;; (|- ((--> recent-context agency-relevant) (stv 0.9 0.8))
;;     ((--> agency-relevant AgencyBalance-primed) (stv 0.85 0.75)))
;; -> AgencyBalance is primed for this cycle

;; 3. soul-calibration-confidence via revision
;; Merges Layer 1 pre-compute with Layer 2 verdict
;; (|- ((soul-calibration layer1-estimate) (stv 0.7 0.5))
;;     ((soul-calibration layer2-verdict) (stv 0.8 0.7)))
;; -> calibrated confidence with merged evidence

;; 4. soul-pre-compute via deduction + abduction
;; Chains primed patterns into predictions before LLM call
;; Abduction detects gaps where predictions miss

;; 5. tier-b-capture-units driven by correlation confidence
;; High-confidence patterns get brief treatment
;; Low-confidence patterns get full compass depth
