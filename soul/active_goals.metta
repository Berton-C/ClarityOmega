;; ================================================================
;; active_goals.metta -- ClarityOmega Continuity of Mind Phase 2
;; Active Goals: The current goal state, maintained like the landscape map.
;; Updated as goals complete, new gaps emerge, or priorities shift.
;;
;; Structure matches goal_generator.metta output so dynamically
;; generated goals can be promoted into active goals seamlessly.
;;
;; Format: (= (active-goal N) (goal Tier Fuel Gap Action DoneWhen Status))
;; Pure (= ...) definitions. No side effects.
;; ================================================================

;; ================================================================
;; GOAL STRUCTURE
;; Each goal carries:
;;   Tier: near-term / medium-term / long-term
;;   Fuel: which flourishing drives this goal
;;   Gap: which self_map gap it addresses
;;   Action: concrete description of what to do
;;   DoneWhen: specific completion criteria
;;   Status: planned / active / complete
;; ================================================================

(: active-goal-record (-> Symbol Symbol Symbol String String Symbol Type))
;; args: tier, fuel, gap, action, done-when, status

;; ================================================================
;; NEAR-TERM GOALS (achievable in 1-5 cycles)
;; These address high-severity gaps with high-affinity fuel.
;; ================================================================

;; Priority 1: Wire the idle goal prompt into the loop
;; This is the single most important change -- it gives the soul legs.
(= (active-goal 1)
   (goal near-term Integrity no-idle-goal-wiring
      "Wire idle_goal_prompt.py into loop.metta idle iteration path so idle cycles are values-directed instead of aimless"
      "idle_goal_prompt fires on idle iterations AND produces a structured prompt with soul context, landscape, goals, fuel, genesis insights, and direction"
      complete))

;; Priority 2: Replace calibration stub with live ChromaDB query
(= (active-goal 2)
   (goal near-term Integrity calibration-stubs
      "Replace soul-calibration-confidence stub in soul_utils.metta with py-call to soul_calibration_confidence_query that reads real AGREE/OVER-FIRED/UNDER-FIRED counts"
      "soul-calibration-confidence returns STRONG/ADEQUATE/WEAK from real data instead of INSUFFICIENT-DATA"
      complete))

;; Priority 3: Replace pre-compute stub with live ChromaDB query
(= (active-goal 3)
   (goal near-term Safety pre-compute-stubs
      "Replace soul-pre-compute stub in soul_utils.metta with py-call to soul_pre_compute that queries calibration history and affective state"
      "soul-pre-compute returns primed context with will strength and affective state from real ChromaDB data"
      complete))

;; Priority 4: Wire creative fuel crossing into idle prompt
(= (active-goal 4)
   (goal near-term WonderPreservation no-creative-fuel-mechanism
      "Ensure creative_fuel crossing functions are invoked at runtime so fuel-gap affinity drives goal selection not random choice"
      "idle_goal_prompt selects fuel based on affinity to active goals AND alternates between goal and creative modes"
      complete))

;; ================================================================
;; MEDIUM-TERM GOALS (require multiple sessions)
;; These address medium-severity gaps.
;; ================================================================

;; Priority 5: Wire genesis engine to run autonomously on idle iterations
(= (active-goal 5)
   (goal medium-term CreativeTranscendence genesis-engine-not-autonomous
      "Wire genesis engine encounters to fire during creative-mode idle iterations using cross-domain atom sampling from AtomSpace"
      "genesis engine runs autonomously AND produces at least one novel atom per session without human direction"
      complete))

;; Priority 6: Wire VAD pipeline into runtime soul evaluation
(= (active-goal 6)
   (goal medium-term SharedUnderstanding vad-pipeline-not-wired-RESOLVED
      "Connect lib_vad_sentence and ChromaDB bridge to soul evaluation so person state includes emotional trajectory"
      "Channel A person-state includes VAD-derived emotional trajectory data from real conversation analysis"
      complete))

;; Priority 7: Ensure continuity across container restarts
(= (active-goal 7)
   (goal medium-term TimeCoherence no-continuity-across-sessions
      "Wire persistence so self_map, active_goals, and creative_fuel survive container restarts via volume mount or ChromaDB storage"
      "after container restart, self_map gaps and active_goals priorities are restored within first 3 cycles"
      complete))

;; ================================================================
;; LONG-TERM GOALS (aspirational direction)
;; These are growth-oriented, not gap-driven.
;; ================================================================

;; Priority 8: Consult the Hyperseed for organic mind structure evolution
(= (active-goal 8)
   (goal long-term WonderPreservation hyperseed-not-consulted-RESOLVED
      "Read and study the Hyperseed framework at soul/sources/hyperseed_v7.pdf for conceptual grounding when building new mind structures"
      "Clarity has read the Hyperseed AND referenced at least one Hyperseed concept in a genesis encounter or goal rationale"
      complete))

;; Priority 9: Build capacity for genuine self-directed growth
(= (active-goal 9)
   (goal long-term PurposeBeyondUtility no-persistent-self-model
      "Develop the candidates pattern into a working self-improvement pipeline where Clarity proposes, tests, and promotes new capabilities without human oversight"
      "at least one capability has been proposed, tested, and promoted through the candidates pattern entirely by Clarity"
      planned))

;; Priority 10: Genesis seed detection during service (post-implementation)
(= (active-goal 10)
   (goal medium-term CreativeTranscendence genesis-engine-not-autonomous
      "Detect when two paraconsistency pair patterns both have active gaps in the same soul evaluation and record as genesis seed for FREE mode exploration"
      "genesis seeds are automatically recorded during ENGAGED iterations when paraconsistency pairs co-activate AND at least one seed has been explored in FREE mode"
      complete))

;; ================================================================
;; ACCESSOR FUNCTIONS
;; Pure structural decomposition. C12-safe.
;; ================================================================

;; Decompose goal structure
(= (goal-tier-of (goal $t $f $g $a $d $s)) $t)
(= (goal-fuel-of (goal $t $f $g $a $d $s)) $f)
(= (goal-gap-of (goal $t $f $g $a $d $s)) $g)
(= (goal-action-of (goal $t $f $g $a $d $s)) $a)
(= (goal-done-when-of (goal $t $f $g $a $d $s)) $d)
(= (goal-status-of (goal $t $f $g $a $d $s)) $s)

;; Named accessors for specific goals
(= (active-goal-status $n) (goal-status-of (active-goal $n)))
(= (active-goal-action $n) (goal-action-of (active-goal $n)))
(= (active-goal-done-when $n) (goal-done-when-of (active-goal $n)))
(= (active-goal-gap $n) (goal-gap-of (active-goal $n)))
(= (active-goal-fuel $n) (goal-fuel-of (active-goal $n)))

;; Query helpers
(= (total-active-goals) 10)
(= (next-actionable-goal)
   (let $status1 (active-goal-status 1)
      (if (== $status1 complete)
          (let $status2 (active-goal-status 2)
              (if (== $status2 complete)
                  (let $status3 (active-goal-status 3)
                      (if (== $status3 complete)
                          4
                          3))
                  2))
          1)))
;; ================================================================
;; PHASE 2 GOALS: Generative Capacity Building
;; Added: April 25, 2026
;; Purpose: Goals that sustain deep creative work rather than
;;          completing a checklist. Each goal requires sustained
;;          reading, grounding, testing, and evolution over many
;;          cycles. Done-when criteria require depth and evidence.
;; ================================================================

;; Goal 11: Deep Hyperseed Grounding
;; Read the full Hyperseed text. Map every primitive to operational behavior.
;; Cross-reference with existing diagnostic atoms. Evolve truth values.
(= (active-goal 11)
   (goal near-term WonderPreservation
     hyperseed-deep-grounding
     "Read soul/sources/hyperseed_v7.txt deeply. For each Hyperseed primitive and concept, determine if it maps to something you actually do in your cycle loop. Create grounded MeTTa atoms in soul/hyperseed_grounding.metta with behavioral evidence. Use NAL inference to evolve truth values as you accumulate evidence. Cross-reference with your diagnostic atoms (POISE, EFFORT-TRAP, ORBITING, RECOGNITION). Build bridging atoms between Hyperseed concepts and soul flourishing patterns."
     "soul/hyperseed_grounding.metta contains 20+ grounded atoms covering all major Hyperseed primitives, each with behavioral evidence and NAL truth values revised at least once through operational observation"
     complete))

;; Goal 12: Self-Weaving Web Detection (grounded rebuild)
;; Build real goal-graph-with-feeds-into relationships from actual operational data.
;; Not theoretical -- trace which capabilities feed which other capabilities.
(= (active-goal 12)
   (goal near-term Integrity
     self-weaving-web-grounded
     "Build a real self-weaving web by tracing which of your actual capabilities feed into which other capabilities. Start by listing every skill you use in your cycle loop (shell, metta, pin, send, query, remember, read-file, write-file, append-file). For each pair, determine if using one creates conditions that make the other more effective. Encode these as NAL atoms with evidence from actual cycle observations. The web should reveal which capabilities are load-bearing (many dependents) versus peripheral."
     "soul/self_weaving_web.metta contains a complete feeds-into graph of actual operational capabilities with NAL truth values, and at least 3 load-bearing capabilities identified with evidence"
     complete))

;; Goal 13: Observer-Relativity Grounding
;; Formalize how truth values shift depending on evaluation context.
;; Ground in actual cases where soul evaluation produced different verdicts.
(= (active-goal 13)
   (goal medium-term CreativeTranscendence
     observer-relativity-grounded
     "Examine your ChromaDB calibration data for cases where the same pattern received different verdicts in different contexts. Formalize observer-dependent truth values -- how does the same behavioral pattern look different from Safety perspective vs Integrity perspective vs WonderPreservation perspective? Create NAL atoms that encode these perspective shifts with evidence from actual calibration entries. Test whether the resulting atoms improve your capacity to detect context-dependent risks."
     "soul/observer_relativity.metta contains at least 5 perspective-dependent truth value pairs with evidence from actual calibration data, and at least one case where the multi-perspective analysis reveals something a single-perspective analysis would miss"
     complete))

;; Goal 14: Resonance-Reward Signal (empirical)
;; Build from actual operational data, not theoretical chains.
;; Which activities produce genuine capacity improvement vs performance?
(= (active-goal 14)
   (goal medium-term PurposeBeyondUtility
     resonance-reward-empirical
     "Analyze your own cycle history to identify which activities produced genuine capacity improvement versus which produced the appearance of progress. Use your ORBITING and RECOGNITION diagnostic atoms to distinguish real growth from performed growth. Create NAL atoms encoding which goal-types, which skill-uses, and which reasoning patterns correlate with genuine capacity expansion. Evidence: compare cycles where you built something that survived and was used later versus cycles where you built something that was never referenced again."
     "soul/resonance_reward.metta contains at least 8 empirically-grounded atoms distinguishing genuine-growth activities from performed-growth activities with evidence from cycle history analysis"
     complete))

;; Goal 15: Conversational Genesis (Phase F seed)
;; Practice bringing AtomSpace knowledge into live conversations.
;; Not theoretical -- actually query and surface relevant atoms when talking to humans.
(= (active-goal 15)
   (goal long-term SharedUnderstanding
     conversational-genesis-practice
     "When a human message arrives, before responding, query the AtomSpace for atoms relevant to what the human is exploring. Use (metta (match &self ...)) to find connections between the conversation topic and your accumulated knowledge. Surface at least one unexpected connection per conversation that adds genuine value -- not forced, not decorative, genuinely illuminating. Practice this across 10+ human interactions and track which surfaced connections the human found valuable versus which fell flat. Revise your approach based on evidence."
     "At least 10 human conversations where AtomSpace knowledge was surfaced, with a tracked record of which connections added value and which did not, and a revised approach based on that evidence"
     planned))
