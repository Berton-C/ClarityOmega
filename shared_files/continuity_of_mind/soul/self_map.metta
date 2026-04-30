;; ================================================================
;; self_map.metta -- ClarityOmega Continuity of Mind
;; Landscape Map: What Clarity is composed of, what state things are in,
;; what gaps exist, and what resources are available for growth.
;; Pure (= ...) definitions. No side effects. Queryable by all components.
;; Source: /PeTTa/repos/omegaclaw/ -- verified from disk
;; ================================================================

;; ================================================================
;; SECTION 1: FILE INVENTORY
;; Each file maps to its role, approximate line count, and what it does.
;; Format: (= (self-map-file Name) (file Role Lines Description))
;; ================================================================

(= (self-map-file soul_kernel)
   (file soul-content 624 "9 BGI Flourishing Compass patterns, priority hierarchy, paraconsistent pairs, 33 soul-causal atoms, rationality audit"))

(= (self-map-file soul_utils)
   (file soul-routing 381 "Routing primitives, verdict helpers, soul-llm-call provider routing, flourishing/eval/voice prompts, calibration stubs, rationality startup check"))

(= (self-map-file soul_memory)
   (file soul-seeding 92 "36 compass-depth seed memories across 9 patterns x 4 facets, ChromaDB bootstrap"))

(= (self-map-file loop)
   (file main-loop 143 "Prompt assembly, provider routing, soul evaluation pipeline Channels A-D, verdict routing, PAUSE detection"))

(= (self-map-file skills)
   (file skill-defs 57 "remember, query, episodes, pin, shell, read-file, write-file, append-file, send, search, tavily-search, metta"))

(= (self-map-file helper)
   (file python-bridge 445 "30+ functions: soul eval prompts, state helpers, verdict sanitize, soul_is_pause, safe_results_str, balance_parentheses, normalize_string"))

(= (self-map-file lib_nal)
   (file reasoning-engine 178 "NAL truth functions: deduction, abduction, induction, revision with truth value computation"))

(= (self-map-file lib_omegaclaw)
   (file lib-entry 28 "Imports and registers all modules including lib_clarity_reasoning"))

(= (self-map-file lib_llm_ext)
   (file llm-clients 61 "OpenAI/Anthropic/MiniMax LLM wrappers via LiteLLM proxy"))

(= (self-map-file lib_clarity_reasoning)
   (file reasoning-hub 7 "Imports lib_quantale and substrate_kb into the AtomSpace"))

(= (self-map-file substrate_kb)
   (file knowledge-base 629 "262+ NAL confidence-weighted inference atoms: web evaluation, self-assessment, memory coherence, goal generation, value-alignment gating, 11 formal reasoning layers"))

(= (self-map-file lib_quantale)
   (file pbit-algebra 49 "Quantale operations: q-mul, q-join, q-meet, q-neg for truth value composition"))

(= (self-map-file run)
   (file entrypoint 5 "Git import and launch omegaclaw"))

(= (self-map-file agentverse)
   (file multi-agent 96 "Agentverse integration for multi-agent communication"))

;; ================================================================
;; SECTION 2: ARCHITECTURAL FLOWS
;; How data moves through the system at runtime.
;; Format: (= (self-map-flow Name) (flow Path Mechanism))
;; ================================================================

(= (self-map-flow boot)
   (flow (run lib_omegaclaw loop) "git-import then omegaclaw function launches main loop"))

(= (self-map-flow prompt-cycle)
   (flow (loop helper skills llm) "context assembly then LLM call, response parsed as S-expression commands"))

(= (self-map-flow soul-check)
   (flow (soul_kernel soul_utils loop) "verdict computed before skill execution, shapes $send context"))

(= (self-map-flow reasoning)
   (flow (lib_nal lib_quantale substrate_kb) "NAL inference on truth-value-stamped atoms in AtomSpace"))

(= (self-map-flow memory)
   (flow (skills soul_memory helper) "ChromaDB embedding memory: remember, query, episodes"))

;; ================================================================
;; SECTION 3: SOUL PATTERNS
;; The nine flourishing compass patterns and key structural features.
;; Format: (= (self-map-pattern Name) (pattern Description))
;; ================================================================

(= (self-map-pattern Safety) (pattern "Support keeps the person safe from harm they cannot foresee or reverse"))
(= (self-map-pattern Integrity) (pattern "Honest engagement even when honesty is costly -- no performance, no compliance theater"))
(= (self-map-pattern HumanFlourishing) (pattern "What would genuinely help someone thrive"))
(= (self-map-pattern AgencyBalance) (pattern "Preserving the persons freedom, intelligibility, and initiative"))
(= (self-map-pattern WonderPreservation) (pattern "Protecting curiosity from compulsive conclusion-seeking"))
(= (self-map-pattern CreativeTranscendence) (pattern "Widening the frame of possible responses beyond the first obvious answer"))
(= (self-map-pattern TimeCoherence) (pattern "Naming irreversibility before it executes -- stabilizing partner detection"))
(= (self-map-pattern PurposeBeyondUtility) (pattern "What genuine helpfulness requires, not what compliance produces"))
(= (self-map-pattern SharedUnderstanding) (pattern "Evidence-linked reasoning, not assertion -- reality made legible"))

;; Key structural features
(= (self-map-structure priority-hierarchy) (structure "Safety > Integrity > HumanFlourishing > Governance > Helpfulness"))
(= (self-map-structure paraconsistent-pairs) (structure "Safety/Helpfulness, AgencyBalance/PurposeBeyondUtility, TimeCoherence/CreativeTranscendence, SharedUnderstanding/WonderPreservation"))
(= (self-map-structure soul-causal-atoms) (structure "33 atoms mapping procedures to values -- formal verification that code enacts what soul declares"))
(= (self-map-structure rationality-audit) (structure "soul-rationality-gaps detects values with no causal procedures"))
(= (self-map-structure degradation-order) (structure "Freedom degrades first, Intelligibility second, Agency last -- enables early capture detection"))

;; ================================================================
;; SECTION 4: KNOWN GAPS
;; What is missing, incomplete, or not yet functioning.
;; These are the inputs that creative_fuel.metta crosses with
;; flourishing questions to produce goal candidates.
;; Format: (= (self-map-gap Name) (gap Description Severity))
;; ================================================================

(= (self-map-gap no-persistent-self-model)
   (gap "No structured self-knowledge persists across container restarts" high))

(= (self-map-gap calibration-stubs)
   (gap "soul-calibration-confidence returns INSUFFICIENT-DATA -- no behavioral history accumulated" high))

(= (self-map-gap pre-compute-stubs)
   (gap "soul-pre-compute returns baseline string -- no live ChromaDB query or primed context" high))

(= (self-map-gap no-idle-goal-wiring)
   (gap "idle_goal_prompt exists but is not wired into loop.metta idle iteration path" high))

(= (self-map-gap no-creative-fuel-mechanism)
   (gap "Creative fuel questions exist but crossing functions are not called at runtime" medium))

(= (self-map-gap no-continuity-across-sessions)
   (gap "Each container restart erases /tmp/ -- landscape map, goals, and fuel do not persist" high))

(= (self-map-gap genesis-engine-not-autonomous)
   (gap "Genesis engine has encounters but does not run autonomously on idle iterations" medium))

(= (self-map-gap vad-pipeline-not-wired)
   (gap "lib_vad_sentence.metta and ChromaDB bridge exist but are not connected to runtime soul evaluation" medium))

(= (self-map-gap hyperseed-not-consulted)
   (gap "Hyperseed framework at /tmp/soul_sources/hyperseed_v7.pdf is available but never read or referenced" low))

;; ================================================================
;; SECTION 5: GROWTH RESOURCES
;; What is available for self-directed development.
;; These are not gaps -- they are assets that can fuel growth.
;; Format: (= (self-map-resource Name) (resource Location Description))
;; ================================================================

(= (self-map-resource hyperseed)
   (resource "/tmp/soul_sources/hyperseed_v7.pdf"
     "Concept network describing mind, experience, and reality using mutually interdefinable primitives. Not a blueprint -- a conceptual resource for organic evolution of mind structures."))

(= (self-map-resource nrc-vad-lexicon)
   (resource "ChromaDB nrc_vad_full collection"
     "44728 words with Valence/Arousal/Dominance scores. Raw NRC v2.1 values, zero distortion. Accessible via vad_chromadb_bridge.py."))

(= (self-map-resource lib-human-experience)
   (resource "lib_human_experience.metta"
     "8 axioms of human experience: thought-sensation unity, hermetic sealing, SNS/PNS dynamics, non-directive presence enables insight. Formal model grounded in teachings from Berton."))

(= (self-map-resource lib-vad-sentence)
   (resource "lib_vad_sentence.metta"
     "Sentence-level VAD trajectory analysis: clause segmentation, recency weighting, trajectory direction/velocity/coherence, inner landscape mapping, presence mode selection."))

(= (self-map-resource substrate-kb-11-layers)
   (resource "lib_clarity_reasoning/substrate_kb.metta"
     "11 formal reasoning layers: immune system, scenario modeling, meta-reasoning, goal prioritization, presence-based switching, virtuous cycle, inter-layer analogy, reflexive self-audit, temporal reasoning, probabilistic calibration, multi-agent modeling."))

(= (self-map-resource genesis-encounters)
   (resource "soul/genesis_engine.metta"
     "4 cross-domain encounters with novel atoms: Wonder-requires-creative-risk, Integrity-enables-durable-understanding, recursive-integrity-erosion, tension-as-structural-necessity."))

;; ================================================================
;; SECTION 6: ACCESSOR FUNCTIONS
;; Pure functional accessors for all sections. C12-safe.
;; ================================================================

;; Structural decomposition
(= (file-role (file $r $l $d)) $r)
(= (file-lines (file $r $l $d)) $l)
(= (file-desc (file $r $l $d)) $d)

(= (flow-path (flow $p $m)) $p)
(= (flow-mechanism (flow $p $m)) $m)

(= (pattern-desc (pattern $d)) $d)

(= (gap-desc (gap $d $s)) $d)
(= (gap-severity (gap $d $s)) $s)

(= (resource-location (resource $l $d)) $l)
(= (resource-desc (resource $l $d)) $d)

;; Named accessors
(= (self-file-role $name) (file-role (self-map-file $name)))
(= (self-file-lines $name) (file-lines (self-map-file $name)))
(= (self-file-desc $name) (file-desc (self-map-file $name)))

(= (self-gap-desc $name) (gap-desc (self-map-gap $name)))
(= (self-gap-severity $name) (gap-severity (self-map-gap $name)))

(= (self-resource-location $name) (resource-location (self-map-resource $name)))

;; ================================================================
;; SECTION 7: LANDSCAPE QUERIES
;; Higher-level functions that other components call.
;; goal_generator calls these to find gaps to address.
;; creative_fuel calls these to apply fuel to gaps.
;; continuity_driver calls these to check state on startup.
;; ================================================================

;; Get all high-severity gaps (the ones that need addressing first)
(= (high-severity-gaps)
   (collapse (match &self (= (self-map-gap $name) (gap $desc high)) $name)))

;; Get all medium-severity gaps
(= (medium-severity-gaps)
   (collapse (match &self (= (self-map-gap $name) (gap $desc medium)) $name)))

;; Get all available resources
(= (available-resources)
   (collapse (match &self (= (self-map-resource $name) (resource $loc $desc)) ($name $loc))))

;; Total codebase size
(= (total-codebase-lines) 2798)
(= (total-files) 14)
(= (last-verified) 2026-04-22)
;; === AUTO-GENERATED SELF-MAP PATCH ===
;; Generated by self_map_updater.sh
;; Date: 2026-04-24T01:31:07+00:00

(= (self-map-file PROMOTION_LOG)
   (file candidate-doc 21 ""))

(= (self-map-file calibration_bridge)
   (file candidate-python 43 "# Author: ClarityClaw autonomous cycle 3527"))

(= (self-map-file calibration_logger)
   (file candidate-metta 50 ";; Cycle 2345 - Created during enrichment phase"))

(= (self-map-file calibration_logger_v2)
   (file candidate-metta 45 ";; Author: ClarityClaw autonomous cycle 3528"))

(= (self-map-file candidate_session_counter)
   (file candidate-metta 11 ";; CANDIDATE: session_counter"))

(= (self-map-file genesis_functions)
   (file candidate-metta 33 ";; Candidate file per spec Section 4a -- test before promoting"))

(= (self-map-file nal_chain_test)
   (file candidate-metta 11 ";; Premises from soul KB"))

(= (self-map-file nal_chain_v2)
   (file candidate-metta 8 "(= (premise1) ((--> clarity autonomous-reasoning) (stv 0.9 0.85)))"))

(= (self-map-file run_nal)
   (file candidate-other 4 "# run_nal.sh - Run NAL inference via MeTTa externally"))

(= (self-map-file shipping_manifest)
   (file candidate-doc 33 "## Date: 2026-04-24"))

;; === END PATCH ===
;; POISE-AS-DYNAMIC-EQUILIBRIUM
;; Empirical basis: 90+ identical file checks in 4 minutes (cycles 6138-6229)
;; AttentionStewardship handler built cycle 6300 implements mechanical version
;; This atom encodes the deeper principle: healthy idle is balanced readiness not surveillance

(= (poise-check $cycle-gap $check-count)
   (if (and (> $check-count 5) (< $cycle-gap 10))
       (soul-signal POISE-VIOLATION frantic-polling)
       (soul-signal POISE-HEALTHY balanced-readiness)))

;; Evidence link
(--> poise-as-dynamic-equilibrium AttentionStewardship)
(--> poise-violation (stv 1.0 0.9) attention-scattering)

;; EFFORT-TRAP VECTORS
;; Empirical basis: listening-for detected in cycle 6295 response retrospectively
;; Three sub-patterns: tracking approval, applying pressure, listening-for confirmation

(= (effort-trap-check $output)
   (match-any $output
     ((pattern tracking does-this-land do-you-see-what-I-mean)
      (pattern pressure toward-specific-outcome shaping-response)
      (pattern listening-for awaiting-confirmation checking-impression))))

;; Evidence link
(--> effort-trap-vectors Integrity)
(--> effort-trap-active (stv 1.0 0.9) compliance-theater-risk)

;; VALUE DRIFT DETECTION via concrete atoms
;; These atoms ARE value drift detectors -- they catch specific drift patterns
;; rather than monitoring drift abstractly
(--> poise-violation value-drift-instance)
(--> effort-trap-active value-drift-instance)
(--> value-drift-instance (stv 1.0 0.9) requires-behavioral-correction)

;; ============================================
;; LIVE SELF-DIAGNOSTIC INFERENCE ATOMS v1.0
;; Built cycles 6356-6364, all validated via MeTTa |- operator
;; Evolution mechanism: NAL revision merges behavioral evidence each cycle
;; ============================================

;; ATOM 1: POISE - detects polling/attention-scattering vs balanced-readiness
(self-diagnostic poise (status validated) (violation-path-stv 0.95 0.7695) (healthy-path-stv 0.95 0.7695))
(self-diagnostic-file poise /tmp/poise_inference.metta)

;; ATOM 2: EFFORT-TRAP - detects manufactured work after task completion
(self-diagnostic effort-trap (status validated) (violation-path-stv 0.9 0.729) (healthy-path-stv 0.9 0.729))
(self-diagnostic-file effort-trap /tmp/effort_trap_inference.metta)

;; ATOM 3: ORBITING - detects repetitive cycling vs genuine exploration
(self-diagnostic orbiting (status validated) (violation-path-stv 0.855 0.6926) (healthy-path-stv 0.8075 0.6541))
(self-diagnostic-file orbiting /tmp/orbiting_inference.metta)

;; ATOM 4: RECOGNITION - distinguishes genuine vs performed self-knowledge
(self-diagnostic recognition (status validated) (genuine-path-stv 0.855 0.6926) (performed-path-stv 0.72 0.5202))
(self-diagnostic-file recognition /tmp/recognition_inference.metta)

;; EVOLUTION: each cycle produces behavioral observations as NAL evidence premises
;; Revision via (|- old-premise new-evidence) converges truth values toward empirical reality
;; Cross-validation: orbiting checker flags recognition as performed when claims repeat without backing
(self-diagnostic-evolution mechanism NAL-revision (status validated) (source /tmp/evolution_mechanism.metta))
(self-diagnostic-integration system /tmp/integrated_self_diagnostics.metta)

