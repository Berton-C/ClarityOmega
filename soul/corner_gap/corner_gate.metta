;; ============================================================
;; soul/corner_gap/corner_gate.metta -- CORNER-GATE V3 SHIM
;; Installed by apply_corner_gate_v3_monolith.py. The v2 enforcement body
;; (pattern-scoped holding, filter-corner-cmds, held-marker emission)
;; is RETIRED (design doc 5.1; reasons: enforcement-retired-by-
;; design, defect-D-A, defect-D-B). Names and arities preserved.
;; v3 does not imperatively hold, block, or release. It feeds conditions;
;; the engine computes blockers, candidates, and navigation states.
;; ============================================================

;; Pass-through: nothing is ever held.
(= (apply-corner-gate-v2 $sexpr $msgnew) $sexpr)

;; The legibility seam: appends the coupling line to the RESULTS payload.
;; S1: novelty classification upstream compares raw $results; this touches
;; only the results_final path that feeds &lastresults.
(= (gate-aware-results (RESULTS: $inner))
   (let* (($line (coupling-legibility-line))
          ($el (COUPLING-STATE-LINE $line))
          ($inner2 (cons-atom $el $inner)))
     (RESULTS: $inner2)))
