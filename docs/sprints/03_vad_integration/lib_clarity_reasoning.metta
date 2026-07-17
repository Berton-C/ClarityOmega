;; lib_clarity_reasoning.metta -- ClarityOmega Reasoning Extension Architecture Loader
;; Master integration file -- imports all production reasoning libraries
;; Updated 2026-04-20: 7 libs production-ready, Patrick type guidance applied

;; === Core NAL Extensions ===
;; Wraps Patrick |- operator with higher-order reasoning patterns
!(import! &self lib_nal_extended)

;; === Quantale Algebra (pbit) ===
;; Type-safe probabilistic bit algebra: q-mul, q-join, q-meet, q-neg
;; Uses (: pbit Type) declarations per Patrick -- PeTTa strict typing is asset
!(import! &self lib_quantale)

;; === Web Coherence Detection ===
;; Convergence, divergence, causal chains, tension detection in belief webs
;; Returns pbits for integration with quantale algebra
!(import! &self lib_web_detect)

;; === Soul-Compass Resonance Evaluation ===
;; Agency, wonder, safety, integrity scoring with composite resonance
;; All outputs are pbits -- any low value constrains composite via q-meet
!(import! &self lib_resonance)

;; === Temporal Belief Reasoning ===
;; Tracks belief evolution: drift, stability, trend, volatility
;; Uses typed belief-snapshot constructor, all outputs are pbits
!(import! &self lib_temporal)

;; === Paraconsistent Reasoning ===
;; Tension classification, contradiction holding, soul-goal tension analysis
;; Enables reasoning under contradiction without collapse
!(import! &self lib_paraconsistent)

;; === Metacognitive Monitoring ===
;; Reasoning quality monitor: circular detection, confidence decay,
;; overconfidence flags, narrowing detection, composite health scoring
;; This lib watches the other 6 -- the architecture reasons about itself
!(import! &self lib_metacognitive)

;; === Analogy Reasoning ===
;; Two-step compound: abduction plus deduction for structural transfer
!(import! &self lib_analogy)


;; === Induction Reasoning ===
;; Shared-subject generalization with evidence accumulation via revision
!(import! &self lib_induction)


;; === Epistemic Gap Detection ===
;; Low confidence regions become learning goals via autocatalytic loop
!(import! &self lib_epistemic_gap)


;; === Counterfactual Reasoning ===
;; Causal analysis via negation and substitution comparison
!(import! &self lib_counterfactual)


;; === Goal Decomposition ===
;; Means-ends analysis with dependency-ordered subgoals
!(import! &self lib_goal_decomposition)


;; === VAD Perception & Routing ===
!(import! &self lib_vad)

