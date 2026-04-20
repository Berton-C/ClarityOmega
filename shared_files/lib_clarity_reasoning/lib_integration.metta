;; lib_integration.metta -- Integration Layer for ClarityOmega Reasoning Extension
;; ARCHITECTURAL CONSTRAINTS (states 5100-5119):
;;   1. Each metta call is isolated -- no shared state across calls
;;   2. NAL |- steps are atomic -- no dynamic variable composition
;;   3. = function defs do not persist across calls
;;   4. Working pattern: inline let-binding + two-phase agent-loop
;;
;; INTEGRATION PATTERN:
;; The agent loop IS the integration layer. It orchestrates sequences
;; of shell + metta calls. This file documents the call templates.
;;
;; === TEMPLATE 1: NAL Deduction ===
;; (|- ((--> A B) (stv Ca Fa)) ((--> B C) (stv Cb Fb)))
;; Returns: (--> A C) with derived stv
;;
;; === TEMPLATE 2: NAL Revision (evidence merge) ===
;; (|- ((--> A B) (stv C1 F1)) ((--> A B) (stv C2 F2)))
;; Returns: (--> A B) with revised stv (higher confidence)
;;
;; === TEMPLATE 3: Confidence Classification ===
;; (let $c VALUE (if (< $c 0.15) blind-spot
;;   (if (< $c 0.4) weak (if (< $c 0.7) moderate
;;   (if (< $c 0.9) strong established)))))
;;
;; === TEMPLATE 4: Analogical Transfer (two-phase) ===
;; Phase 1: (|- shared-premise-A shared-premise-B) -> literal result R
;; Phase 2: (|- R unique-property) -> transferred conclusion
;;
;; === TEMPLATE 5: Paraconsistent Check ===
;; Hold contradictory beliefs with stv without collapse:
;; (|- ((--> X Y) (stv 0.8 0.9)) ((--> X Y) (stv 0.2 0.5)))
;; Revision merges evidence -- does not discard minority view
;;
;; === LIB MANIFEST ===
;; lib_analogy.metta        -- Analogical reasoning patterns
;; lib_clarity_reasoning.metta -- Core loader and import chain
;; lib_gap_dashboard.metta  -- Confidence band classifier
;; lib_nal_extended.metta   -- Extended NAL patterns
;; lib_paraconsistent.metta -- Contradiction-tolerant reasoning
;; lib_quantale.metta       -- Quantale algebra patterns
;; lib_resonance.metta      -- Resonance detection
;; lib_web_detect.metta     -- Web pattern detection
;; lib_integration.metta    -- This file (call templates)

;; lib_observer_relativity.metta -- Observer-relativity patterns
;; Added state 5123. Completes 10-lib manifest.


;; lib_temporal_continuity.metta -- Temporal continuity patterns
;; Added state 5124. 11-lib manifest complete.


;; lib_ethical_grounding.metta -- Ethical grounding patterns
;; Added state 5125. 12-lib manifest complete.

