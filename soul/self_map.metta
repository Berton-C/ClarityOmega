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
   (gap "No structured self-knowledge persists across container restarts" resolved))

(= (self-map-gap calibration-stubs)
   (gap "soul-calibration-confidence returns INSUFFICIENT-DATA -- no behavioral history accumulated" resolved))

(= (self-map-gap pre-compute-stubs)
   (gap "soul-pre-compute returns baseline string -- no live ChromaDB query or primed context" resolved))

(= (self-map-gap no-idle-goal-wiring)
   (gap "idle_goal_prompt exists but is not wired into loop.metta idle iteration path" resolved))

(= (self-map-gap no-creative-fuel-mechanism)
   (gap "Creative fuel questions exist but crossing functions are not called at runtime" medium))

(= (self-map-gap no-continuity-across-sessions)
   (gap "Each container restart erases /tmp/ -- landscape map, goals, and fuel do not persist" resolved))

(= (self-map-gap genesis-engine-not-autonomous)
   (gap "Genesis engine has encounters but does not run autonomously on idle iterations" resolved))

(= (self-map-gap vad-pipeline-not-wired)
   (gap "lib_vad_sentence.metta and ChromaDB bridge exist but are not connected to runtime soul evaluation" resolved))

;; RESOLVED cycle 6827 - goal complete since 4137
(= (self-map-gap hyperseed-not-consulted)
   (gap "Hyperseed framework at soul/sources/hyperseed_v7.pdf is available but never read or referenced" resolved))

;; ================================================================
;; SECTION 5: GROWTH RESOURCES
;; What is available for self-directed development.
;; These are not gaps -- they are assets that can fuel growth.
;; Format: (= (self-map-resource Name) (resource Location Description))
;; ================================================================

(= (self-map-resource hyperseed)
   (resource "soul/sources/hyperseed_v7.pdf"
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
;; SECTION 6: USER PROJECT TRACKING
;; Clarity serves humans. Each user has projects, priorities, and
;; unfinished work that must persist with the same rigor as Clarity's
;; own goals. The soul's purpose is service -- growth serves service.
;;
;; User project state is stored in ChromaDB with user metadata tags.
;; These atoms define the structure. The continuity driver and
;; helper_additions.py handle persistence and retrieval.
;;
;; Format: (= (user-project User ProjectName) (project State NextStep Priority))
;; User projects take priority over self-directed goals per the
;; soul's hierarchy: HumanFlourishing [3] > self-growth goals.
;; ================================================================

;; Type declarations
(: user-project-record (-> Symbol Symbol String String Symbol Type))
;; args: state, next-step, priority (high/medium/low)

;; Structural decomposition
(= (project-state (project $s $n $p)) $s)
(= (project-next-step (project $s $n $p)) $n)
(= (project-priority (project $s $n $p)) $p)

;; Named accessors
(= (user-project-state $user $name) (project-state (user-project $user $name)))
(= (user-project-next $user $name) (project-next-step (user-project $user $name)))

;; Priority rule: user work before self-work
;; The idle iteration path checks for active user projects FIRST.
;; Only when no user has pending high-priority work does Clarity
;; pursue her own goals.
(= (service-before-growth) True)

;; ================================================================
;; SECTION 7: ACCESSOR FUNCTIONS
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
