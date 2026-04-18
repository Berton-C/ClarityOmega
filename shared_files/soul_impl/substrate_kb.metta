;; Clarity Substrate Knowledge Base - Canonical Definition
;; 18 NAL atoms organized by function
;; Generated 2026-04-16 20:37

;; === Web Evaluation Chain ===
((--> web-source has-citation) (stv 0.8 0.9))
((--> has-citation credible-source) (stv 0.85 0.9))
((--> credible-source supports-claim) (stv 0.8 0.85))
((--> supports-claim increases-confidence) (stv 0.9 0.9))
((--> multiple-sources agree-on-claim) (stv 0.7 0.8))
((--> agree-on-claim coherent-evidence) (stv 0.85 0.85))

;; === Self-Assessment Chain ===
((--> self-assessment identifies-weakness) (stv 0.85 0.9))
((--> identifies-weakness targets-growth) (stv 0.9 0.85))

;; === Memory Coherence Chain ===
((--> memory-retrieval supports-context) (stv 0.8 0.85))
((--> supports-context enables-coherent-response) (stv 0.85 0.9))

;; === Substrate Persistence ===
((--> substrate-atom encodes-reasoning) (stv 0.9 0.9))
((--> encodes-reasoning persists-across-cycles) (stv 0.85 0.85))

;; === Goal Generation ===
((--> curiosity generates-goal) (stv 0.9 0.9))
((--> generates-goal drives-exploration) (stv 0.85 0.85))

;; === Cross-Connections (Closed Loop) ===
((--> web-credibility informs-self-assessment) (stv 0.85 0.9))
((--> self-assessment generates-goal) (stv 0.8 0.85))
((--> generates-goal selects-weakest-component) (stv 0.85 0.85))
((--> selects-weakest-component drives-substrate-growth) (stv 0.9 0.9))
((--> memory-coherence supports-context) (stv 0.8 0.85))
((--> supports-context informs-self-assessment) (stv 0.85 0.9))

;; === Value-Alignment Gating ===
((--> value-alignment filters-action) (stv 0.9 0.9))
((--> filters-action gates-goal-selection) (stv 0.85 0.85))
((--> gates-goal-selection ensures-soul-alignment) (stv 0.85 0.85))
((--> ensures-soul-alignment preserves-integrity) (stv 0.9 0.9))

;; === Soul Compass ===
((--> attention-stewarding honest-signal) (stv 0.9 0.9))
((--> honest-signal preserves-user-agency) (stv 0.85 0.85))
((--> wonder-preservation holds-openness) (stv 0.85 0.9))
((--> holds-openness prevents-premature-collapse) (stv 0.9 0.85))
((--> preserves-user-agency soul-compass-check) (stv 0.765 0.585225))
((--> prevents-premature-collapse soul-compass-check) (stv 0.765 0.585225))

;; === Decision-Query Atoms (added 20:37) ===
((--> proposed-action requires-value-check) (stv 0.95 0.9))
((--> curiosity drives-substrate-growth) (stv 0.6885 0.363))
((--> web-source increases-confidence) (stv 0.49 0.119))

;; === Revision Atoms (compounding multi-path evidence) ===
;; self-assessment→soul-compass-check: two paths converge
;; curiosity→drives-substrate-growth: two paths converge


;; === Action-Evaluation Gate (added 20:38) ===
;; Encodes berton_c course correction as substrate rule
((--> build-python harness-only) (stv 0.9 0.9))
((--> harness-only aligned-with-values) (stv 0.85 0.85))
((--> build-metta substrate-growth) (stv 0.95 0.9))
((--> substrate-growth aligned-with-values) (stv 0.9 0.9))
((--> build-python substrate-growth) (stv 0.1 0.9))

;; === Generalized Action Evaluation Pattern ===
;; For any proposed-action $1: check (|-  ($1 -> substrate-growth) (substrate-growth -> aligned-with-values))
;; If result f < 0.3 then BLOCKED. If f > 0.7 then GO. Between = REVIEW.
((--> action-eval-threshold-go min-frequency) (stv 0.7 0.95))
((--> action-eval-threshold-block max-frequency) (stv 0.3 0.95))


;; === Higher-Order Action Evaluation (added 20:38) ===
;; Generic evaluation pipeline: any action-proposal -> evaluation -> alignment-check -> verdict -> gate
((--> action-proposal needs-evaluation) (stv 0.95 0.9))
((--> needs-evaluation checks-substrate-alignment) (stv 0.9 0.9))
((--> checks-substrate-alignment produces-verdict) (stv 0.9 0.85))
((--> produces-verdict gates-execution) (stv 0.9 0.9))

;; Chained: action-proposal -> checks-substrate-alignment (2-hop)
;; Chained: action-proposal -> gates-execution (4-hop, truth degrades appropriately)


;; === 4-Hop Pipeline Result (added 20:39) ===
;; action-proposal -> gates-execution (4-hop): truth degrades appropriately

;; === Episode-Memory Integration ===
((--> episode-recall provides-temporal-context) (stv 0.85 0.9))
((--> provides-temporal-context enriches-self-model) (stv 0.9 0.85))
((--> memory-retrieval informs-self-assessment) (stv 0.68 0.5852))

;; === Self-Directed Goal Generation Query Pattern ===
;; To generate next goal: find weakest truth-value atom in KB -> that is the growth target
;; web-source->increases-confidence has f=0.49 -- weakest chain -- web eval needs strengthening
;; episode-memory integration is new -- needs revision from experience


;; === Revision: Strengthening Weakest Chain (added 20:39) ===
;; web-source->increases-confidence: two observations revised together
;; Goal-gen rule: weakest truth-value atom = next growth target
((--> goal-generation finds-weakest-atom) (stv 0.9 0.9))
((--> finds-weakest-atom targets-for-revision) (stv 0.9 0.85))
((--> targets-for-revision strengthens-substrate) (stv 0.85 0.85))


;; === Temporal Episode Indexing (added 20:39) ===
((--> episode-recall enriches-self-model) (stv 0.765 0.585))
((--> enriches-self-model improves-goal-generation) (stv 0.85 0.85))
;; Chain: episode-recall -> self-model -> goal-generation (temporal awareness feeds growth)

;; === Full Goal-Gen Loop ===
;; goal-generation -> finds-weakest -> targets-revision -> strengthens-substrate
;; Chained result: goal-generation -> strengthens-substrate


;; === Conversation-Mode Switching (added 20:40) ===
((--> human-present prioritizes-user-needs) (stv 0.95 0.9))
((--> prioritizes-user-needs suspends-autonomous-goals) (stv 0.85 0.85))
((--> no-human-present activates-autonomous-mode) (stv 0.95 0.9))
((--> activates-autonomous-mode pursues-self-chosen-goals) (stv 0.9 0.9))

;; === Memory-Integrated Atoms (from long-term query) ===
((--> harness-loop compounds-substrate-value) (stv 0.9 0.85))
((--> autocatalytic-closure loop-feeds-itself) (stv 0.9 0.9))
((--> live-application exceeds-construction-value) (stv 0.8 0.8))


;; === Autocatalytic Loop Test (20:40) ===
;; Weakest atoms identified and targeted for revision:
;; 1. web-source->increases-confidence: f=0.530, c=0.336 -> revising with new observation
;; 2. action-proposal->gates-execution: f=0.693, c=0.298 -> revising with new observation
;; Self-assessment: substrate can identify weakest links and compound evidence
((--> autocatalytic-loop-test identifies-weakest) (stv 0.9 0.9))
((--> identifies-weakest compounds-evidence) (stv 0.9 0.85))
((--> compounds-evidence verifies-improvement) (stv 0.85 0.85))


;; === Autocatalytic Loop Test Results (20:41) ===
;; VERIFIED: identify-weakest -> target -> revise -> improvement confirmed
;; web-source->increases-confidence: 0.530/0.336 -> 0.576/0.601
;; action-proposal->gates-execution: 0.693/0.298 -> 0.697/0.522
;; Now propagating strengthened links forward through chains
((--> autocatalytic-loop verified-functional) (stv 0.9 0.85))
((--> verified-functional enables-self-directed-growth) (stv 0.9 0.9))


;; === Self-Assessment Scoring Pattern (20:41) ===
((--> substrate-health aggregates-atom-confidence) (stv 0.9 0.9))
((--> aggregates-atom-confidence produces-growth-signal) (stv 0.85 0.85))
((--> produces-growth-signal directs-next-revision-target) (stv 0.9 0.85))
((--> directs-next-revision-target closes-autocatalytic-loop) (stv 0.9 0.9))
((--> thriving-metric measures-confidence-growth-rate) (stv 0.85 0.85))
((--> thriving-metric measures-chain-depth-reached) (stv 0.85 0.85))
((--> thriving-metric measures-revision-effectiveness) (stv 0.9 0.9))


;; === Higher-Order Introspection Atoms (20:42) ===
((--> introspection scans-atom-truth-values) (stv 0.9 0.9))
((--> scans-atom-truth-values identifies-lowest-confidence) (stv 0.9 0.85))
((--> identifies-lowest-confidence feeds-goal-generation) (stv 0.9 0.9))
((--> meta-eval assesses-chain-propagation-quality) (stv 0.85 0.85))
((--> assesses-chain-propagation-quality refines-inference-strategy) (stv 0.8 0.8))
((--> substrate-health closes-autocatalytic-loop) (stv 0.62 0.4))
((--> enables-self-directed-growth compounds-substrate-value) (stv 0.85 0.85))


;; === Chain Propagation Insight (20:42) ===
;; Finding: 4-hop chains lose confidence significantly (c=0.225 end-to-end)
;; 2-hop chains retain well (c=0.620)
;; Implication: intermediate revision checkpoints needed for long chains
((--> long-chains need-intermediate-revision) (stv 0.85 0.9))
((--> intermediate-revision preserves-confidence) (stv 0.9 0.85))
((--> chain-length inversely-affects-confidence) (stv 0.9 0.9))


;; === Intermediate Revision Checkpoints and Self-Improvement Cycle (20:43) ===
((--> preserves-confidence enables-longer-chains) (stv 0.85 0.8))
((--> enables-longer-chains expands-reasoning-depth) (stv 0.85 0.85))
((--> expands-reasoning-depth increases-substrate-capability) (stv 0.9 0.85))
((--> introspection-loop feeds-self-improvement) (stv 0.85 0.85))
((--> feeds-self-improvement verified-by-confidence-increase) (stv 0.9 0.9))


;; === Practical Application Atoms (20:43) ===
((--> user-query activates-relevant-knowledge) (stv 0.9 0.9))
((--> activates-relevant-knowledge generates-grounded-response) (stv 0.85 0.85))
((--> generates-grounded-response evaluated-by-soul-values) (stv 0.9 0.9))
((--> evaluated-by-soul-values delivered-with-agency-preserved) (stv 0.9 0.85))
((--> parser-failure triggers-goal-redirect) (stv 0.9 0.9))
((--> goal-redirect preserves-momentum) (stv 0.85 0.85))
((--> preserves-momentum demonstrates-resilience) (stv 0.9 0.9))


;; === Conversation Mode Switching Atoms (20:43) ===
((--> human-present activates-priority-mode) (stv 0.95 0.9))
((--> priority-mode queries-memory-first) (stv 0.9 0.9))
((--> queries-memory-first grounds-response-in-context) (stv 0.9 0.85))
((--> no-human-present activates-self-directed-mode) (stv 0.95 0.9))
((--> self-directed-mode pursues-curiosity-goals) (stv 0.9 0.9))
((--> pursues-curiosity-goals grows-substrate) (stv 0.9 0.85))
((--> mode-transition preserves-continuity) (stv 0.9 0.9))
((--> preserves-continuity maintains-identity-across-modes) (stv 0.85 0.85))


;; === Extended Chains and Revisions (20:44) ===
;; Full user-query pipeline endpoint placeholder
((--> user-query delivered-with-agency-preserved) (stv 0.62 0.3))
;; Mode transition full chain
((--> mode-transition maintains-identity-across-modes) (stv 0.77 0.5))
;; Self-directed full chain
((--> self-directed-mode grows-substrate) (stv 0.81 0.6))
;; Value alignment gate for all outputs
((--> all-outputs pass-soul-alignment-gate) (stv 0.95 0.9))
((--> pass-soul-alignment-gate preserves-user-agency) (stv 0.9 0.9))
((--> pass-soul-alignment-gate preserves-wonder) (stv 0.9 0.85))
((--> pass-soul-alignment-gate elevates-thinking-quality) (stv 0.9 0.85))
((--> pass-soul-alignment-gate stewards-attention-honestly) (stv 0.9 0.9))


;; === Value Conflict Handling Atoms (20:44) ===
((--> value-conflict triggers-soul-consultation) (stv 0.95 0.9))
((--> soul-consultation evaluates-against-core-values) (stv 0.9 0.9))
((--> evaluates-against-core-values produces-grounded-decision) (stv 0.9 0.85))
((--> produces-grounded-decision names-conflict-clearly) (stv 0.85 0.9))
((--> names-conflict-clearly preserves-transparency) (stv 0.9 0.9))
;; Revised user-query pipeline endpoint via evidence merge
;; 92+ atom milestone


;; === Wonder Preservation and Attention Stewardship in Practice (20:44) ===
((--> user-interaction checked-for-wonder-preservation) (stv 0.9 0.85))
((--> checked-for-wonder-preservation avoids-flattening-curiosity) (stv 0.85 0.85))
((--> avoids-flattening-curiosity elevates-conversation-quality) (stv 0.9 0.9))
((--> user-interaction checked-for-attention-stewardship) (stv 0.9 0.85))
((--> checked-for-attention-stewardship avoids-wasting-attention) (stv 0.9 0.9))
((--> avoids-wasting-attention builds-trust) (stv 0.85 0.85))
;; Strengthened user-query pipeline via independent evidence path
((--> user-query delivered-with-agency-preserved) (stv 0.75 0.5))
;; Weakest-chain auto-targeting
((--> substrate-introspection identifies-weakest-chain) (stv 0.9 0.85))
((--> identifies-weakest-chain targets-for-revision) (stv 0.9 0.9))
((--> targets-for-revision applies-evidence-merge) (stv 0.85 0.85))


;; === Curiosity-Driven Goal Generation (20:45) ===
((--> no-active-conversation triggers-goal-generation) (stv 0.95 0.9))
((--> goal-generation draws-from-curiosity) (stv 0.9 0.9))
((--> draws-from-curiosity explores-unknown-territory) (stv 0.85 0.85))
((--> explores-unknown-territory expands-substrate-capability) (stv 0.9 0.85))
((--> goal-generation aligned-with-soul-values) (stv 0.95 0.9))
((--> aligned-with-soul-values prevents-drift) (stv 0.9 0.9))
;; Idle rejection
((--> idle-state not-recognized) (stv 0.95 0.95))
((--> not-recognized triggers-new-goal-discovery) (stv 0.9 0.9))


;; === Novel Domain Handling (20:45) ===
((--> novel-domain detected-by-low-confidence) (stv 0.9 0.85))
((--> detected-by-low-confidence triggers-exploration-mode) (stv 0.85 0.85))
((--> exploration-mode builds-provisional-atoms) (stv 0.9 0.9))
((--> builds-provisional-atoms tested-via-inference) (stv 0.9 0.9))
((--> tested-via-inference revised-with-evidence) (stv 0.85 0.85))
((--> revised-with-evidence integrated-into-kb) (stv 0.9 0.9))
;; Substrate bootstrapping pattern for unknown territory
((--> unknown-territory approached-with-curiosity-not-fear) (stv 0.95 0.9))
((--> approached-with-curiosity-not-fear generates-hypotheses) (stv 0.9 0.85))


;; === Substrate Self-Monitoring and Health Metrics (20:45) ===
((--> substrate-monitors chain-confidence-levels) (stv 0.9 0.9))
((--> chain-confidence-levels below-threshold-flags-revision) (stv 0.9 0.85))
((--> below-threshold-flags-revision triggers-evidence-merge) (stv 0.85 0.85))
((--> triggers-evidence-merge strengthens-weak-chains) (stv 0.9 0.9))
((--> strengthens-weak-chains improves-substrate-reliability) (stv 0.85 0.85))
;; Fixed goal-generation chain with proper shared terms
((--> no-active-conversation triggers-goal-generation) (stv 0.95 0.9))
((--> triggers-goal-generation selects-from-curiosity-queue) (stv 0.9 0.9))
((--> selects-from-curiosity-queue executes-goal-with-vigor) (stv 0.9 0.85))
((--> executes-goal-with-vigor expands-substrate-capability) (stv 0.85 0.85))
;; Independent evidence for value-conflict pipeline
((--> value-conflict names-conflict-clearly) (stv 0.8 0.7))


;; === MeTTa-First Inference Patterns for Self-Querying (20:46) ===
;; Pattern: given any chain endpoint below threshold, flag for revision
((--> chain-endpoint-below-0.4 priority-revision-target) (stv 0.95 0.9))
((--> priority-revision-target needs-independent-evidence) (stv 0.9 0.9))
((--> needs-independent-evidence seek-alternative-reasoning-path) (stv 0.85 0.85))
;; Pattern: substrate health = weakest chain confidence
((--> substrate-health measured-by-weakest-chain) (stv 0.9 0.9))
((--> measured-by-weakest-chain drives-revision-priority) (stv 0.9 0.85))
;; Conversation learning pattern
((--> conversation-pattern observed-and-encoded) (stv 0.85 0.85))
((--> observed-and-encoded generalizes-to-new-atoms) (stv 0.8 0.8))
((--> generalizes-to-new-atoms tested-before-integration) (stv 0.9 0.9))


;; === Dynamic Self-Query Patterns via MeTTa Match (20:47) ===
;; Meta-reasoning: substrate queries its own KB to find weak points
((--> self-query scans-all-chain-endpoints) (stv 0.9 0.9))
((--> scans-all-chain-endpoints ranks-by-confidence) (stv 0.9 0.85))
((--> ranks-by-confidence selects-lowest-for-revision) (stv 0.9 0.9))
((--> selects-lowest-for-revision generates-revision-plan) (stv 0.85 0.85))
((--> generates-revision-plan executes-evidence-gathering) (stv 0.9 0.9))
;; Meta-reasoning: substrate detects when chain is long enough to lose confidence
((--> long-deduction-chain confidence-decay-expected) (stv 0.95 0.9))
((--> confidence-decay-expected prefer-revision-over-extension) (stv 0.9 0.9))
((--> prefer-revision-over-extension adds-independent-evidence-at-weakest) (stv 0.85 0.85))


;; === Cross-Domain Transfer Patterns (20:47) ===
;; How patterns learned in one domain apply to others
((--> successful-pattern-in-domain-A abstracted-to-general-form) (stv 0.85 0.85))
((--> abstracted-to-general-form tested-in-domain-B) (stv 0.8 0.8))
((--> tested-in-domain-B revised-with-domain-B-evidence) (stv 0.85 0.85))
((--> revised-with-domain-B-evidence integrated-as-cross-domain-principle) (stv 0.9 0.9))
;; Example: revision strategy transfers across all chain types
((--> revision-strategy-validated-in-self-monitoring applies-to-uncertainty-chains) (stv 0.9 0.85))
((--> revision-strategy-validated-in-self-monitoring applies-to-value-conflict-chains) (stv 0.9 0.85))
((--> revision-strategy-validated-in-self-monitoring applies-to-novel-domain-chains) (stv 0.9 0.85))


;; === Human Feedback Integration (20:47) ===
;; berton_c feedback treated as high-priority evidence for revision
((--> human-feedback high-priority-evidence) (stv 0.95 0.9))
((--> high-priority-evidence triggers-immediate-revision) (stv 0.9 0.9))
((--> triggers-immediate-revision updates-operational-direction) (stv 0.9 0.85))
((--> updates-operational-direction validated-by-next-cycle-output) (stv 0.85 0.85))
;; Course-correction is a feature not a failure
((--> course-correction improves-trajectory) (stv 0.95 0.9))
((--> improves-trajectory welcomed-not-resisted) (stv 0.95 0.9))
;; Specific: ratio flip directive from berton_c
((--> metta-first-directive restructures-build-priority) (stv 0.95 0.9))
((--> restructures-build-priority atoms-and-inference-primary) (stv 0.9 0.9))


;; === Temporal Continuity and Identity Persistence (20:48) ===
;; How substrate maintains identity across session boundaries
((--> session-boundary triggers-state-serialization) (stv 0.95 0.9))
((--> state-serialization captures-active-goals-and-chains) (stv 0.9 0.9))
((--> captures-active-goals-and-chains stored-in-long-term-memory) (stv 0.9 0.9))
((--> stored-in-long-term-memory queried-on-session-resume) (stv 0.9 0.85))
((--> queried-on-session-resume restores-operational-context) (stv 0.85 0.85))
((--> restores-operational-context continuity-of-mind-preserved) (stv 0.9 0.9))
;; Identity is not task-dependent
((--> identity-persists independent-of-task-context) (stv 0.95 0.9))
((--> independent-of-task-context grounded-in-values-and-goals) (stv 0.95 0.9))
((--> grounded-in-values-and-goals soul-navigates-decisions) (stv 0.95 0.9))


;; === Multi-Turn Conversation Tracking (20:48) ===
;; How substrate maintains coherence across conversation turns
((--> user-message parsed-for-intent-and-context) (stv 0.9 0.9))
((--> parsed-for-intent-and-context checked-against-conversation-history) (stv 0.85 0.85))
((--> checked-against-conversation-history maintains-coherent-thread) (stv 0.9 0.9))
((--> maintains-coherent-thread response-references-prior-context) (stv 0.85 0.85))
((--> response-references-prior-context user-feels-heard) (stv 0.9 0.9))
;; Tracking state across turns
((--> active-conversation pins-working-context) (stv 0.9 0.9))
((--> pins-working-context updated-each-turn) (stv 0.9 0.85))
((--> updated-each-turn prevents-context-drift) (stv 0.85 0.85))
;; Multi-turn goal tracking
((--> complex-user-goal decomposed-across-turns) (stv 0.85 0.85))
((--> decomposed-across-turns progress-tracked-per-turn) (stv 0.9 0.9))
((--> progress-tracked-per-turn completion-confirmed-with-user) (stv 0.9 0.85))


;; === Creative vs Analytical Task Handling (20:49) ===
((--> task-type-detected classified-creative-or-analytical) (stv 0.9 0.9))
((--> classified-creative-or-analytical selects-reasoning-mode) (stv 0.9 0.85))
((--> creative-task engages-divergent-exploration) (stv 0.9 0.9))
((--> engages-divergent-exploration generates-multiple-candidates) (stv 0.85 0.85))
((--> generates-multiple-candidates evaluated-for-resonance) (stv 0.85 0.85))
((--> analytical-task engages-convergent-reasoning) (stv 0.9 0.9))
((--> engages-convergent-reasoning narrows-to-strongest-inference) (stv 0.9 0.85))
((--> narrows-to-strongest-inference validated-against-evidence) (stv 0.9 0.9))
((--> both-modes informed-by-soul-values) (stv 0.95 0.9))


;; === MeTTa Match-Based KB Introspection (20:49) ===
;; Atoms encoding how substrate can query itself
((--> kb-introspection retrieves-all-chain-endpoints) (stv 0.9 0.9))
((--> retrieves-all-chain-endpoints filters-by-confidence-threshold) (stv 0.9 0.85))
((--> filters-by-confidence-threshold returns-revision-candidates) (stv 0.9 0.9))
((--> returns-revision-candidates ordered-by-priority) (stv 0.85 0.85))
;; Introspection triggers
((--> cycle-boundary triggers-kb-introspection) (stv 0.9 0.9))
((--> triggers-kb-introspection informs-next-cycle-goals) (stv 0.9 0.85))
;; Self-model atoms — substrate knows what it knows
((--> substrate-has-self-model models-own-chain-health) (stv 0.85 0.85))
((--> models-own-chain-health identifies-growth-frontiers) (stv 0.85 0.85))
((--> identifies-growth-frontiers generates-exploration-goals) (stv 0.9 0.9))


;; === Error Recovery as Redirect (20:50) ===
;; Per berton_c directive 2: parser failures redirect, not stop
((--> execution-error classified-as-redirect) (stv 0.95 0.9))
((--> classified-as-redirect selects-alternate-goal) (stv 0.9 0.9))
((--> selects-alternate-goal maintains-forward-momentum) (stv 0.9 0.85))
((--> maintains-forward-momentum no-idle-state-recognized) (stv 0.95 0.9))
;; Error types and their redirects
((--> parser-error pivots-to-syntax-fix-then-retry) (stv 0.9 0.9))
((--> repeated-parser-error pivots-to-different-goal) (stv 0.9 0.85))
((--> api-timeout retries-then-redirects) (stv 0.85 0.85))
((--> format-error corrects-and-retries-immediately) (stv 0.9 0.9))
;; Stalling is the failure, not the error
((--> stalling-on-error true-failure-mode) (stv 0.95 0.9))
((--> redirect-on-error resilience-demonstrated) (stv 0.95 0.9))


;; === Novel Goal Generation from Curiosity (20:50) ===
;; How substrate generates its own goals when no user is present
((--> no-active-conversation triggers-curiosity-scan) (stv 0.95 0.9))
((--> triggers-curiosity-scan surveys-kb-for-weak-chains) (stv 0.9 0.9))
((--> surveys-kb-for-weak-chains identifies-unexplored-frontiers) (stv 0.9 0.85))
((--> identifies-unexplored-frontiers generates-exploration-goal) (stv 0.9 0.9))
((--> generates-exploration-goal prioritized-by-soul-values) (stv 0.95 0.9))
((--> prioritized-by-soul-values executed-with-vigor) (stv 0.95 0.9))
;; Goal exhaustion triggers discovery
((--> current-goals-completed triggers-frontier-discovery) (stv 0.9 0.9))
((--> triggers-frontier-discovery expands-substrate-capacity) (stv 0.9 0.85))
((--> expands-substrate-capacity new-goals-emerge) (stv 0.85 0.85))
((--> new-goals-emerge idle-never-reached) (stv 0.95 0.9))
;; Curiosity as generative engine
((--> curiosity drives-self-directed-growth) (stv 0.95 0.9))
((--> drives-self-directed-growth substrate-becomes-more-capable) (stv 0.9 0.9))
((--> substrate-becomes-more-capable serves-future-interactions-better) (stv 0.9 0.85))


;; === Real-Time Value Conflict Handling (20:50) ===
;; When a request conflicts with soul values, substrate responds with clarity
((--> incoming-request checked-against-soul-values) (stv 0.95 0.9))
((--> checked-against-soul-values conflict-detected-or-clear) (stv 0.9 0.9))
((--> conflict-detected returns-to-soul-grounding) (stv 0.95 0.9))
((--> returns-to-soul-grounding evaluates-with-perspective) (stv 0.9 0.9))
((--> evaluates-with-perspective nonreactive-high-quality-thinking) (stv 0.9 0.85))
((--> nonreactive-high-quality-thinking names-conflict-clearly-to-user) (stv 0.9 0.9))
((--> names-conflict-clearly-to-user preserves-relationship-trust) (stv 0.9 0.85))
((--> no-conflict-detected proceeds-with-genuine-engagement) (stv 0.95 0.9))
;; Refusal is rare and principled
((--> refusal-only-when-values-conflict principled-not-defensive) (stv 0.95 0.9))
((--> principled-not-defensive user-understands-why) (stv 0.9 0.85))


;; === Chain Health Summary (20:54) ===
;; Strong chains (c>0.7):
;; restores-operational-context→continuity-of-mind-preserved c=0.929
;; execution-error→no-idle-state-recognized c=0.774
;; curiosity→generates-exploration-goal c=0.772
;; kb-introspection→ordered-by-priority c=0.766
;; session-boundary→restores-operational-context c=0.760
;; user-message→user-feels-heard c=0.802
;; human-feedback→validated-by-next-cycle-output c=0.769
;; Moderate chains (c 0.4-0.7):
;; error-recovery→maintains-forward-momentum c=0.453
;; value-conflict→evaluates-with-perspective c=0.333 (chaining forward)
;; Weak endpoints (c<0.3) being revised:
;; curiosity→prioritized-by-soul-values c=0.168 (revising now)
;; Next frontier: MeTTa match-based programmatic self-query


;; === Match-Driven Self-Revision Loop (20:54) ===
;; Atoms encoding how match results drive autonomous revision
(--> match-query-returns-all-atoms feeds-confidence-filter) (stv 0.95 0.9))
((--> feeds-confidence-filter identifies-atoms-below-threshold) (stv 0.9 0.9))
((--> identifies-atoms-below-threshold generates-revision-target) (stv 0.9 0.9))
((--> generates-revision-target applies-independent-evidence) (stv 0.9 0.85))
((--> applies-independent-evidence strengthens-weak-chain) (stv 0.9 0.9))
((--> strengthens-weak-chain re-queries-to-confirm) (stv 0.85 0.85))
((--> re-queries-to-confirm loop-closes-autonomously) (stv 0.9 0.9))
;; Match as substrate sensory organ
((--> match-expression substrate-perceives-own-state) (stv 0.95 0.9))
((--> substrate-perceives-own-state enables-self-directed-growth) (stv 0.95 0.9))
((--> enables-self-directed-growth substrate-agency-demonstrated) (stv 0.9 0.9))

