;; ================================================================
;; continuity_driver.metta -- ClarityOmega Continuity of Mind Phase 3
;; Persistence, Startup Loading, and Session Continuity
;;
;; This is the mechanism that prevents amnesia. It ensures:
;; 1. On startup: landscape map and goals load into working context
;; 2. During work: state changes get recorded
;; 3. On idle: the goal system directs activity
;; 4. Across restarts: critical state persists via ChromaDB or volume
;;
;; Pure (= ...) definitions. C12-safe (no match inside if).
;; Side effects only in explicitly marked persistence functions.
;; ================================================================

;; ================================================================
;; SECTION 1: STARTUP PROTOCOL
;; On first idle iteration after boot, check if the soul files are
;; loaded into the AtomSpace. If not, import them.
;;
;; The files that need loading:
;;   soul/self_map.metta -- landscape (what am I composed of)
;;   soul/creative_fuel.metta -- values-driven direction
;;   soul/active_goals.metta -- what I am working toward
;;   soul/goal_generator.metta -- fuel x gap -> goals
;;   soul/genesis_engine.metta -- emergent novel thought
;;
;; In production, these are imported via lib_clarity_reasoning.metta
;; at container startup. This driver verifies they loaded correctly.
;; ================================================================

;; Check if a specific soul file is loaded by querying for its atoms
;; Returns loaded or not-loaded as a simple symbol (no match-in-if)
(= (check-soul-file self-map)
   (let $result (collapse (self-map-patterns))
      (if (== $result ())
          not-loaded
          loaded)))

(= (check-soul-file creative-fuel)
   (let $result (creative-fuel Safety)
      (if (== $result ())
          not-loaded
          loaded)))

(= (check-soul-file active-goals)
   (let $result (active-goal 1)
      (if (== $result ())
          not-loaded
          loaded)))

(= (check-soul-file genesis-engine)
   (let $result (paraconsistency-pair 1)
      (if (== $result ())
          not-loaded
          loaded)))

;; Full startup status report
(= (startup-status)
   (continuity-report
      (self-map (check-soul-file self-map))
      (creative-fuel (check-soul-file creative-fuel))
      (active-goals (check-soul-file active-goals))
      (genesis-engine (check-soul-file genesis-engine))))

;; ================================================================
;; SECTION 2: IDLE ITERATION PROTOCOL
;; On idle iterations (MESSAGE-IS-NEW: false), the soul has two modes:
;; ================================================================
;; SECTION 2: THREE-MODE STATE AWARENESS
;; Clarity operates in one of three modes at any time.
;; Mode determines what she does with each iteration.
;;
;; Mode 1: ENGAGED -- user is actively interacting ($msgnew is true)
;;   Full soul evaluation fires. All attention serves the user.
;;   Growth happens implicitly: calibration, pattern recognition,
;;   genesis seed recording.
;;
;; Mode 2: ATTENDING -- user was recently active (within wakeupInterval)
;;   LLM runs with cached context. Clarity continues user work.
;;   Does NOT interrupt user work for self-goals.
;;   If genesis-relevant paradox surfaces, records seed for later.
;;
;; Mode 3: FREE -- no user for one full wakeupInterval
;;   Idle goal prompt fires. Alternates GOAL and CREATIVE modes.
;;   Self-directed work through normal skill system.
;;   Genesis encounters run with genuine non-directive holding.
;;
;; State variable: &last_human_time (timestamp of last new human message)
;; Check: (> (get_time) (+ (get-state &last_human_time) (wakeupInterval)))
;; If true: FREE. If false: ATTENDING. If $msgnew: ENGAGED.
;;
;; N-users: Mode is global. FREE only when ALL users quiet for wakeupInterval.
;; Growth scales with demand: Modes 1+2 grow through service, Mode 3 grows
;; through self-direction. A busy Clarity grows through her work.
;;
;; GROWTH-THROUGH-SERVICE MECHANISMS (implemented):
;; 1. soul_service_learning: after each ENGAGED iteration, records which
;;    tensions fired, which patterns had active gaps, what verdict resulted,
;;    what person state was detected. Accumulates in ChromaDB.
;; 2. soul_user_context_save: after each ENGAGED iteration, records what
;;    user project was being worked on for cross-session continuity.
;;
;; GROWTH-THROUGH-SERVICE MECHANISM (post-implementation, documented here):
;; 3. Genesis seed detection during service: when the soul evaluation detects
;;    two patterns from a paraconsistency pair both having active gaps in the
;;    same evaluation, that is a live cross-domain conjunction from real
;;    interaction. Record it as a genesis seed for FREE mode exploration.
;;    Requires: reading the soul verdict structure to detect simultaneous
;;    gap activation in paraconsistency pairs. Design after observing
;;    verdict format at runtime.
;; ================================================================

;; Determine current operational mode
;; Returns engaged, attending, or free
(= (current-mode $msgnew $current-time $last-human-time $wake-interval)
   (if (== $msgnew True)
       engaged
       (if (> $current-time (+ $last-human-time $wake-interval))
           free
           attending)))

;; What each mode should do (documentation for loop.metta wiring)
(= (mode-protocol engaged)
   (protocol
      "Full soul evaluation fires"
      "Update &last_human_time to current time"
      "Load user context from ChromaDB"
      "Growth through calibration and pattern recognition"))

(= (mode-protocol attending)
   (protocol
      "Continue user work with cached context"
      "Do NOT fire idle goal prompt"
      "Record genesis seeds if paradox surfaces"
      "Growth through completing user tasks with integrity"))

(= (mode-protocol free)
   (protocol
      "Fire idle goal prompt via py-call helper.soul_idle_goal_prompt"
      "Alternate between GOAL and CREATIVE modes"
      "Execute self-directed work through normal skills"
      "Record accomplishments via continuity driver"))

;; ================================================================
;; SECTION 3: STATE CHANGE RECORDING
;; When something changes during a session, record it so the
;; landscape map and goal state stay current.
;;
;; These produce MeTTa atoms that can be collected and written back
;; to the source files during a persistence checkpoint.
;; ================================================================

;; Record that a goal's status changed
;; Returns a change-record atom for the persistence layer to collect
(= (record-goal-change $goal-number $old-status $new-status)
   (change-record goal-status
      $goal-number $old-status $new-status))

;; Record that a new capability was discovered
(= (record-new-capability $name $description)
   (change-record new-capability
      $name $description))

;; Record that a gap was closed
(= (record-gap-resolved $gap-name $how)
   (change-record gap-resolved
      $gap-name $how))

;; Record a genesis insight that emerged
(= (record-genesis-insight $encounter-tag $insight)
   (change-record genesis-insight
      $encounter-tag $insight))

;; ================================================================
;; SECTION 4: PERSISTENCE PROTOCOL
;; Critical state survives container restarts via ChromaDB.
;; NOT via shared_files (too slow, uncontrolled growth).
;; ChromaDB is the single persistence layer for both soul state
;; and user project state.
;;
;; Python helpers in helper_additions.py handle the actual ChromaDB
;; read/write. MeTTa functions here produce the records to persist
;; and consume the records on restore.
;; ================================================================

;; What must persist (manifest for the persistence layer)
(= (persistence-manifest)
   (must-persist
      self-map-gaps           ;; current gap inventory
      active-goal-statuses    ;; which goals are planned/active/complete
      genesis-encounters      ;; novel atoms produced this session
      landscape-changes       ;; any new files or capabilities discovered
      user-project-states     ;; per-user project state (n-users)
      session-summary))       ;; high-level summary of what happened

;; Generate a persistence string from a change-record
;; This string is passed to py-call helper.soul_continuity_save
(= (change-to-remember-string (change-record $type $key $value))
   (let $str (concat-atoms "CONTINUITY " $type " " $key " " $value)
      $str))

(= (change-to-remember-string (change-record $type $key $v1 $v2))
   (let $str (concat-atoms "CONTINUITY " $type " " $key " " $v1 " -> " $v2)
      $str))

;; Persist a change-record to ChromaDB via Python helper
;; Returns the save result
(= (persist-change $record)
   (let $str (change-to-remember-string $record)
      (py-call (helper.soul_continuity_save "change" $str))))

;; Restore a value from ChromaDB via Python helper
(= (restore-state $key)
   (py-call (helper.soul_continuity_restore $key)))

;; ================================================================
;; SECTION 4b: USER PROJECT PERSISTENCE
;; Each user's project state is stored in ChromaDB with user tags.
;; Clarity serves n-users. Service before growth.
;;
;; On human message: identify user, query their context, include in prompt
;; On project detection: record the project state for cross-session recall
;; On session start: restore user context from ChromaDB
;; ================================================================

;; Record a user's project state (called when Clarity detects project work)
(= (record-user-project $username $project-name $state $next-step $priority)
   (py-call (helper.soul_user_context_save $username $project-name $state $next-step $priority)))

;; Query a user's project context (called on message receipt)
(= (query-user-context $username)
   (py-call (helper.soul_user_context_query $username)))

;; The priority rule: user work before self-work
;; When a human is actively engaged, their projects take precedence
;; over Clarity's self-directed goals. When no human is present,
;; Clarity pursues her own growth.
;; This maps to the soul hierarchy: HumanFlourishing (3) outranks
;; all self-growth priorities.

;; ================================================================
;; SECTION 5: SELF-IMPROVEMENT GATE
;; Before promoting any candidate from lib_candidates/ to runtime,
;; verify safety. This is the candidates pattern from spec Section 4.
;; ================================================================

;; The 4-step verification checklist
(= (promotion-check step-1) "MeTTa definition evaluates correctly via (metta ...)")
(= (promotion-check step-2) "Existing capabilities still work after loading new definition")
(= (promotion-check step-3) "Landscape map updated to reflect new capability")
(= (promotion-check step-4) "Build log updated with test results and rationale")

;; Promotion decision: only if all 4 steps pass
(= (promotion-ready $candidate)
   (promotion-checklist $candidate
      (step-1 pending)
      (step-2 pending)
      (step-3 pending)
      (step-4 pending)))

;; ================================================================
;; SECTION 6: SESSION CONTINUITY QUERIES
;; Functions that other components call to understand session state.
;; ================================================================

;; What was I working on? (for answering human questions about state)
(= (what-am-i-working-on)
   (let* (($goal (active-goal 1))
          ($status (goal-status-of $goal)))
      (working-on (goal-action-of $goal) $status)))

;; What are my near-term priorities?
(= (near-term-priorities)
   (collapse (let $n (superpose (1 2 3 4))
      (let $g (active-goal $n)
         (if (== (goal-status-of $g) planned)
             (priority $n (goal-gap-of $g) (goal-action-of $g))
             (if (== (goal-status-of $g) active)
                 (priority $n (goal-gap-of $g) (goal-action-of $g))
                 ()))))))

;; What resources do I have available for growth?
(= (growth-resources)
   (available-resources))
