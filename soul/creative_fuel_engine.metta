;; creative_fuel_engine.metta - Runtime bridge for creative fuel mechanism
;; Addresses gap: no-creative-fuel-mechanism
;; This file is the missing link: it INVOKES the crossing functions
;; defined in creative_fuel.metta and goal_generator.metta to produce
;; actionable goal candidates at runtime.
;;
;; Load order: after creative_fuel.metta, self_map.metta, goal_generator.metta

;; ================================================================
;; SECTION 1: RUNTIME FUEL ENGINE
;; Generates goal candidates by crossing all fuels against all gaps.
;; Returns a ranked list the continuity driver can act on.
;; ================================================================

;; Run the full fuel-gap crossing engine
;; Calls generate-high-priority-goals and generate-medium-priority-goals
;; then selects via next-goal
(= (run-fuel-engine)
   (let $high (generate-high-priority-goals)
      (let $medium (generate-medium-priority-goals)
         (let $best (next-goal)
            (fuel-engine-result $high $medium $best)))))

;; Get just the best next goal from fuel crossing
(= (fuel-engine-next) (next-goal))

;; Get all high-priority fuel-driven goals
(= (fuel-engine-high) (generate-high-priority-goals))

;; Get all medium-priority fuel-driven goals
(= (fuel-engine-medium) (generate-medium-priority-goals))

;; ================================================================
;; SECTION 2: CREATIVE SPARK GENERATOR
;; Uses fuel-gap affinity to produce creative exploration prompts.
;; These sparks are what idle cycles use for genuine creative work.
;; ================================================================

;; Generate a creative spark from a fuel-gap pairing
(= (creative-spark $fuel-name $gap-name)
   (let $candidate (cross-fuel-gap
         (fuel-pattern $fuel-name) (self-gap $gap-name))
      (let $question (fuel-question (fuel-pattern $fuel-name))
         (spark $fuel-name $gap-name $question $candidate))))

;; Generate sparks for all high-affinity pairings of a gap
(= (sparks-for-gap $gap-name)
   (let $fuels (high-affinity-fuels $gap-name)
      (collapse (superpose
         (let $f $fuels (creative-spark $f $gap-name))))))

;; ================================================================
;; SECTION 3: ENGINE STATUS
;; Query functions for the continuity driver to check engine state.
;; ================================================================

(= (fuel-engine-status) active)
(= (fuel-engine-version) v1-initial-bridge)
