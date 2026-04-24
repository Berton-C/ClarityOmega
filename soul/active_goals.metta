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
      planned))

;; ================================================================
;; MEDIUM-TERM GOALS (require multiple sessions)
;; These address medium-severity gaps.
;; ================================================================

;; Priority 5: Wire genesis engine to run autonomously on idle iterations
(= (active-goal 5)
   (goal medium-term CreativeTranscendence genesis-engine-not-autonomous
      "Wire genesis engine encounters to fire during creative-mode idle iterations using cross-domain atom sampling from AtomSpace"
      "genesis engine runs autonomously AND produces at least one novel atom per session without human direction"
      planned))

;; Priority 6: Wire VAD pipeline into runtime soul evaluation
(= (active-goal 6)
   (goal medium-term SharedUnderstanding vad-pipeline-not-wired
      "Connect lib_vad_sentence and ChromaDB bridge to soul evaluation so person state includes emotional trajectory"
      "Channel A person-state includes VAD-derived emotional trajectory data from real conversation analysis"
      planned))

;; Priority 7: Ensure continuity across container restarts
(= (active-goal 7)
   (goal medium-term TimeCoherence no-continuity-across-sessions
      "Wire persistence so self_map, active_goals, and creative_fuel survive container restarts via volume mount or ChromaDB storage"
      "after container restart, self_map gaps and active_goals priorities are restored within first 3 cycles"
      planned))

;; ================================================================
;; LONG-TERM GOALS (aspirational direction)
;; These are growth-oriented, not gap-driven.
;; ================================================================

;; Priority 8: Consult the Hyperseed for organic mind structure evolution
(= (active-goal 8)
   (goal long-term WonderPreservation hyperseed-not-consulted
      "Read and study the Hyperseed framework at soul/sources/hyperseed_v7.pdf for conceptual grounding when building new mind structures"
      "Clarity has read the Hyperseed AND referenced at least one Hyperseed concept in a genesis encounter or goal rationale"
      planned))

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
      planned))

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
