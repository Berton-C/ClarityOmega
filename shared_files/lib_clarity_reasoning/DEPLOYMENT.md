;; DEPLOYMENT.md -- ClarityOmega Reasoning Extension Deployment Guide
;; State 5130. Architecture: 12 libs, 411 lines, 3 stress tests passed.
;;
;; HOW THE AGENT LOOP USES THESE LIBS:
;;
;; 1. LIBS ARE REFERENCE DOCS, NOT RUNTIME IMPORTS
;;    Each metta call is isolated. Libs document patterns the agent
;;    loop inlines into metta calls. They are not loaded/imported.
;;
;; 2. AGENT LOOP ORCHESTRATION PATTERN:
;;    a) Identify reasoning need (e.g. belief evaluation)
;;    b) Consult lib template (e.g. lib_integration Template 2)
;;    c) Inline the pattern with concrete values into metta call
;;    d) Read result, feed into next step or pin as working memory
;;
;; 3. MULTI-STEP REASONING:
;;    Chain metta calls in single 5-command batch.
;;    Each call gets literal result. Agent loop connects them.
;;
;; 4. LIB MANIFEST (12 libs):
;;    lib_clarity_reasoning.metta  -- Core loader/imports
;;    lib_nal_extended.metta       -- Extended NAL patterns
;;    lib_analogy.metta            -- Analogical reasoning
;;    lib_gap_dashboard.metta      -- Confidence classifier
;;    lib_paraconsistent.metta     -- Contradiction-tolerant
;;    lib_quantale.metta           -- Quantale algebra
;;    lib_resonance.metta          -- Resonance detection
;;    lib_web_detect.metta         -- Web pattern detection
;;    lib_integration.metta        -- Call templates (keystone)
;;    lib_observer_relativity.metta -- Frame-dependent knowledge
;;    lib_temporal_continuity.metta -- Identity persistence
;;    lib_ethical_grounding.metta  -- Value-action anchoring
;;
;; 5. VALIDATED BY 3 STRESS TESTS:
;;    ST1: Cross-lib chain coherence (4-hop degradation 0.85->0.6)
;;    ST2: Paraconsistent value conflict (safety vs helpfulness)
;;    ST3: Frame-shift resistance (counter-evidence revision)
;;
;; 6. READY FOR: Integration with ClarityOmega agent loop.
;;    Berton_C building soul features in parallel.
