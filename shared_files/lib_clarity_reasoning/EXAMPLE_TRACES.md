;; EXAMPLE_TRACES.md -- Multi-lib Reasoning Workflow Demonstrations
;; State 5131. Shows how agent loop chains libs in practice.
;;
;; TRACE 1: Belief Evaluation Pipeline
;; Scenario: User claims X. Clarity evaluates.
;;
;; Step 1 (lib_nal_extended): Encode claim as inheritance
;;   (metta (|- ((--> X Y) (stv 0.7 0.6)) ((--> Y Z) (stv 0.8 0.9))))
;;   Result: derived stv for X-->Z
;;
;; Step 2 (lib_observer_relativity): Apply humility discount
;;   Multiply confidence by 0.85 observer-limitation factor
;;
;; Step 3 (lib_gap_dashboard): Classify adjusted confidence
;;   blind-spot / weak / moderate / strong / established
;;
;; Step 4 (lib_ethical_grounding): Check irreversibility gate
;;   If action follows from belief, gate by irreversibility level
;;
;; TRACE 2: Value Conflict Resolution
;; Scenario: Safety and Helpfulness conflict on user request.
;;
;; Step 1 (lib_paraconsistent): Hold both values with stv
;;   Safety-requires-X (stv 0.9 0.9), Help-requires-not-X (stv 0.85 0.9)
;;
;; Step 2 (lib_ethical_grounding): Apply priority hierarchy
;;   Safety > Helpfulness. Safety wins without eliminating helpfulness.
;;
;; Step 3 (lib_integration): Use Template 5 paraconsistent check
;;   Derive conflict explicitly, document tension
;;
;; Step 4: Communicate to user with transparency about the tension
;;
;; TRACE 3: Identity Drift Check
;; Scenario: Periodic self-audit across conversation boundary.
;;
;; Step 1 (lib_temporal_continuity): Query stored baseline values
;; Step 2 (lib_nal_extended): Compare current beliefs vs baseline
;; Step 3 (lib_gap_dashboard): Classify divergence magnitude
;; Step 4 (lib_observer_relativity): Frame-shift test on any drifted belief
