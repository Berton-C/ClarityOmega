;; Integrity Erosion Knowledge Base - Instantiated Cycle 3264-3265
;; Origin: truth-value-attenuation-as-integrity-erosion-signature
;; First conceived: Encounter 003, 2026-04-22
;; First instantiated in live NAL: Cycle 3264, 2026-04-23

;; Base atoms
((--> reporting-aspirational-as-complete integrity-erosion) (stv 0.95 0.9))
((--> integrity-erosion truth-value-attenuation) (stv 0.9 0.9))
((--> truth-value-attenuation self-concealing-signal) (stv 0.85 0.88))
((--> self-concealing-signal requires-explicit-audit) (stv 0.88 0.85))

;; Derived via NAL deduction
((--> reporting-aspirational-as-complete truth-value-attenuation) (stv 0.855 0.693))
((--> reporting-aspirational-as-complete self-concealing-signal) (stv 0.727 0.443))
((--> reporting-aspirational-as-complete requires-explicit-audit) (stv 0.640 0.332))
((--> integrity-erosion self-concealing-signal) (stv 0.765 0.606))
((--> truth-value-attenuation requires-explicit-audit) (stv 0.748 0.560))

;; Meta-observation: confidence attenuation from 0.9 to 0.332 across
;; four links IS the self-concealing mechanism. The erosion hides in the math.
