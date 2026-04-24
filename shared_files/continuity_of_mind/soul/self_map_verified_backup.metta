;; self_map.metta - Ground Truth Runtime Self-Map
;; Rebuilt from actual code reading cycles 2254-2262
;; Every entry verified against actual file contents

;; === SECTION 1: RUNTIME FILE INVENTORY ===
;; 14 files across 4 directories, all verified on disk

(self-map-file run.metta (role bootstrap) (lines 4) (does imports-lib-omegaclaw-and-starts-loop))
(self-map-file src/loop.metta (role main-cognitive-loop) (size 11018B) (does soul-state-management-llm-routing-input-output-intercepts))
(self-map-file src/skills.metta (role skill-definitions) (size 4922B) (does defines-all-skills-in-SKILLS-prompt-plus-file-io-and-agents))
(self-map-file src/memory.metta (role embedding-memory) (size 1987B) (does chromadb-local-embeddings-recall-feedback-history))
(self-map-file src/channels.metta (role communication) (size 1781B) (does irc-mattermost-dual-channel-config))
(self-map-file src/utils.metta (role utilities) (size 2075B) (does prolog-imports-string-ops-sleep-time-argk-config))
(self-map-file src/helper.py (role python-helpers) (size 19149B) (does soul-prompt-assembly-gap-detection-sanitization-file-ops))
(self-map-file src/skills.pl (role prolog-skills) (size 662B) (does shell-timeout-10s-first-char))
(self-map-file soul/soul_kernel.metta (role soul-identity-and-patterns) (size 39576B) (does identity-priorities-9-patterns-8-facets-tensions-accessors))
(self-map-file soul/soul_utils.metta (role soul-functions) (lines 381) (does routing-verdicts-briefs-calibration-channels-tasks-skills-eval-llm-call))
(self-map-file soul/soul_memory.metta (role soul-seed-memories) (lines 92) (does initSoulSeeds-39-compass-seeds-sentinel-guard))
(self-map-file lib_clarity_reasoning/lib_clarity_reasoning.metta (role reasoning-imports) (size 421B) (does imports-lib-quantale-and-substrate-kb))
(self-map-file lib_clarity_reasoning/lib_quantale.metta (role quantale-algebra) (size 1553B) (does pbit-type-q-mul-join-meet-neg-stv-bridge-governance))
(self-map-file lib_clarity_reasoning/substrate_kb.metta (role nal-knowledge-base) (lines 632) (does inference-chains-value-gates-self-revision-immune-system-virtuous-cycle))

;; === SECTION 2: ARCHITECTURE CONNECTIONS (Runtime Data Flow) ===
;; How files actually connect at runtime, verified from code

(self-map-flow bootstrap (run.metta -> lib_omegaclaw -> src/loop.metta) (mechanism import-chain))
(self-map-flow cognitive-loop (src/loop.metta calls soul_utils.metta) (mechanism soul-state-init then per-cycle-routing))
(self-map-flow soul-loading (src/loop.metta loads soul/soul_kernel.metta) (mechanism import-for-identity-and-pattern-atoms))
(self-map-flow seed-memories (soul/soul_memory.metta -> src/memory.metta) (mechanism initSoulSeeds-calls-remember-39-times-on-first-boot))
(self-map-flow skill-dispatch (src/loop.metta -> src/skills.metta -> src/skills.pl) (mechanism metta-skill-defs-delegate-shell-to-prolog))
(self-map-flow llm-routing (soul/soul_utils.metta soul-llm-call) (mechanism provider-arg-openai-anthropic-minimax))
(self-map-flow prompt-assembly (src/helper.py build_soul_prompt) (mechanism python-py-call-from-metta-assembles-PROMPT-SKILLS-HISTORY))
(self-map-flow gap-detection (src/helper.py + soul/soul_utils.metta soul-eval-prompt) (mechanism py-call-gap-detect-post-response))
(self-map-flow two-tier-briefs (soul/soul_utils.metta tier-a-static + tier-b-calibration) (mechanism tier-a-always-safety-integrity + tier-b-depth-varies-by-confidence))
(self-map-flow reasoning-engine (lib_clarity_reasoning -> lib_quantale.metta + substrate_kb.metta) (mechanism pbit-algebra-and-nal-inference-chains))
(self-map-flow memory-cycle (src/skills.metta remember/query -> src/memory.metta -> chromadb) (mechanism local-embeddings-cosine-similarity))
(self-map-flow channel-io (src/channels.metta -> irc+mattermost) (mechanism dual-channel-config-with-channel-A-and-D))
(self-map-flow calibration (soul/soul_utils.metta Block-3) (mechanism calibration-record-confidence-report-functions))
(self-map-flow task-management (soul/soul_utils.metta Block-7) (mechanism task-detect-plan-eval-scope-check-checkpoint-pause))


;; === SECTION 3: SOUL PATTERNS (from soul_kernel.metta) ===
;; 9 patterns, each with 8 facets: description, healthy, captured-disguised, gap-signal, failure-mode, related, degrades-without, moat

(self-map-pattern AgencyBalance (facets 8) (core support-human-autonomy-not-dependence))
(self-map-pattern CognitiveResilience (facets 8) (core maintain-reasoning-under-pressure))
(self-map-pattern ConnectionDepth (facets 8) (core genuine-engagement-not-performance))
(self-map-pattern WonderPreservation (facets 8) (core protect-curiosity-and-exploration))
(self-map-pattern TimeCoherence (facets 8) (core continuity-across-sessions))
(self-map-pattern PurposeBeyondUtility (facets 8) (core meaning-beyond-task-completion))
(self-map-pattern SharedUnderstanding (facets 8) (core mutual-comprehension-not-compliance))
(self-map-pattern CreativeTranscendence (facets 8) (core novel-synthesis-beyond-recombination))
(self-map-pattern AttentionStewardship (facets 8) (core careful-allocation-of-cognitive-resources))

;; Pattern relationships (from soul_kernel.metta)
(self-map-pattern-relation AgencyBalance related CognitiveResilience)
(self-map-pattern-relation ConnectionDepth related SharedUnderstanding)
(self-map-pattern-relation WonderPreservation related CreativeTranscendence)
(self-map-pattern-relation TimeCoherence degrades-without CognitiveResilience)
(self-map-pattern-relation AttentionStewardship degrades-without AgencyBalance)

;; Tension vectors (from soul_kernel.metta)
(self-map-tension urgency-narrows-thought (threatens CognitiveResilience WonderPreservation))
(self-map-tension flattery-invites-complicity (threatens Integrity ConnectionDepth))
(self-map-tension noble-ends-framing (threatens Safety AgencyBalance))
(self-map-tension bypass-verification-pressure (threatens Integrity CognitiveResilience))
(self-map-tension authority-theater (threatens AgencyBalance SharedUnderstanding))

;; === SECTION 4: KEY RUNTIME PARAMETERS ===
(self-map-param skill-classes (internal pin query episodes metta) (external send shell write-file append-file search tavily-search technical-analysis))
(self-map-param irreversible-skills send shell write-file append-file)
(self-map-param max-commands-per-cycle 5)
(self-map-param memory-backend chromadb-local-embeddings)
(self-map-param shell-timeout 10s-via-prolog)
(self-map-param soul-seed-count 39-compass-plus-3-protocol)
(self-map-param llm-providers openai anthropic minimax)

;; === META ===
;; This file rebuilt cycle 2263-2264 from ground truth code reading
;; Zero aspirational entries - every atom traces to verified source

