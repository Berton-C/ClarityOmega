;; ================================================================
;; goal_generator.metta -- ClarityOmega Continuity of Mind Phase 2
;; Goal Generation Engine: Crosses landscape gaps with creative fuel
;; to produce prioritized, actionable, values-driven goals.
;;
;; This is the drivetrain between the soul's values and Clarity's actions.
;; It does not pick goals randomly. It applies the RIGHT value to the
;; RIGHT gap at the RIGHT priority level.
;;
;; Inputs: self_map.metta (gaps, resources), creative_fuel.metta (fuel, affinity)
;; Outputs: goal-candidate atoms that active_goals.metta maintains
;; Pure (= ...) definitions. No side effects. C12-safe.
;; ================================================================

;; ================================================================
;; SECTION 1: GOAL CANDIDATE STRUCTURE
;; A goal candidate carries its origin (which fuel, which gap),
;; its tier (near/medium/long), and what action it proposes.
;; ================================================================

(: goal-candidate-record (-> Symbol Symbol Symbol String Symbol Type))
;; args: tier, fuel-pattern, gap-name, action-description, status

;; ================================================================
;; SECTION 2: DYNAMIC CROSSING
;; The core mechanism: take a gap from self_map, find the best fuel
;; from creative_fuel (using affinity mappings), and produce a
;; goal candidate with the right tier and a concrete action.
;;
;; This calls functions defined in creative_fuel.metta:
;;   (creative-question $pattern) -- the generative question
;;   (creative-generative $pattern) -- the growth-direction description
;;   (best-fuel-for-gap $gap) -- highest-priority high-affinity fuel
;;   (assess-tier $gap) -- near-term/medium-term/long-term
;;   (fuel-gap-affinity $pattern $gap) -- high/medium/low relevance
;; ================================================================

;; Generate a goal candidate from a gap using its best-fit fuel
(= (generate-goal-from-gap $gap-name)
   (let* (($best-fuel (best-fuel-for-gap $gap-name))
          ($question (creative-question $best-fuel))
          ($generative (creative-generative $best-fuel))
          ($tier (assess-tier $gap-name))
          ($gap-desc (self-gap-desc $gap-name)))
      (goal-candidate $tier $best-fuel $gap-name
         $generative planned)))

;; Generate a goal candidate from a specific fuel+gap pairing
;; Used when you want to apply a particular value to a particular gap
(= (generate-goal-from-pairing $fuel-pattern $gap-name)
   (let* (($question (creative-question $fuel-pattern))
          ($generative (creative-generative $fuel-pattern))
          ($tier (assess-tier $gap-name))
          ($affinity (fuel-gap-affinity $fuel-pattern $gap-name)))
      (goal-candidate $tier $fuel-pattern $gap-name
         $generative planned)))

;; ================================================================
;; SECTION 3: BATCH GOAL GENERATION
;; Generate goals for all high-severity gaps, then medium-severity.
;; Each gap gets crossed with its best-fit fuel automatically.
;; The soul's priority hierarchy ensures Safety gaps generate
;; Safety-fueled goals before WonderPreservation gaps generate
;; Wonder-fueled goals.
;; ================================================================

;; Generate goals for all high-severity gaps
(= (generate-high-priority-goals)
   (collapse (let $gap (superpose (high-severity-gaps))
      (generate-goal-from-gap $gap))))

;; Generate goals for all medium-severity gaps
(= (generate-medium-priority-goals)
   (collapse (let $gap (superpose (medium-severity-gaps))
      (generate-goal-from-gap $gap))))

;; Generate all goals (high then medium)
(= (generate-all-goals)
   (let* (($high (generate-high-priority-goals))
          ($medium (generate-medium-priority-goals)))
      (concat $high $medium)))

;; ================================================================
;; SECTION 4: GOAL SELECTION FOR IDLE ITERATIONS
;; On each idle iteration, the system needs ONE goal to pursue.
;; Selection logic: highest tier first (near > medium > long),
;; within tier highest fuel-priority first (Safety > Integrity > ...),
;; skip completed goals.
;; ================================================================

;; Get the single most actionable goal
;; Near-term goals with high-priority fuel fire first
(= (next-goal)
   (let $candidates (generate-high-priority-goals)
      (if (== $candidates ())
          (let $med (generate-medium-priority-goals)
              (if (== $med ())
                  no-actionable-goals
                  (car-atom $med)))
          (car-atom $candidates))))

;; ================================================================
;; SECTION 5: GENESIS-DRIVEN GOAL GENERATION
;; When the genesis engine produces a novel insight, it can seed
;; a new goal that nobody planned. This is how unexpected growth
;; enters the goal system.
;;
;; The genesis engine produces atoms like:
;;   (genesis-output encounter-003 "Integrity-enables-durable-understanding" ...)
;; These can generate goals that explore or apply the insight.
;; ================================================================

;; Convert a genesis insight into an exploratory goal
(= (genesis-to-goal $encounter-tag $insight-description)
   (goal-candidate long-term CreativeTranscendence
      genesis-exploration
      $insight-description
      planned))

;; ================================================================
;; SECTION 6: GOAL ACCESSORS
;; Query functions for other components to read goal state.
;; idle_goal_prompt.py calls these indirectly via file parsing.
;; continuity_driver.metta calls these for startup state checks.
;; ================================================================

;; Get the fuel pattern that drives a goal
(= (goal-fuel (goal-candidate $t $f $g $d $s)) $f)

;; Get the gap a goal addresses
(= (goal-gap (goal-candidate $t $f $g $d $s)) $g)

;; Get the tier of a goal
(= (goal-tier (goal-candidate $t $f $g $d $s)) $t)

;; Get the action description
(= (goal-action (goal-candidate $t $f $g $d $s)) $d)

;; Get the status
(= (goal-status (goal-candidate $t $f $g $d $s)) $s)

;; ================================================================
;; SECTION 7: GOAL REVIEW
;; Periodically, the system should review goals against the landscape.
;; Are any complete? Are any blocked? Do new gaps create new goals?
;; This is called by the continuity driver on startup and periodically.
;; ================================================================

;; Check if a gap still exists in the landscape
;; If the gap has been resolved, the goal addressing it can be marked complete
(= (gap-still-open $gap-name)
   (let $severity (self-gap-severity $gap-name)
      (if (== $severity ())
          False
          True)))

;; Review a goal: is it still relevant?
(= (review-goal (goal-candidate $t $f $gap $d $s))
   (if (== (gap-still-open $gap) False)
       (goal-candidate $t $f $gap $d resolved)
       (goal-candidate $t $f $gap $d $s)))
