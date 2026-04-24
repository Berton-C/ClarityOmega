;; ================================================================
;; creative_fuel.metta -- ClarityOmega Continuity of Mind Phase 1
;; Creative Fuel: Positive Polarity of the Flourishings
;; Purpose: Each flourishing has a generative question that produces
;;          direction, not just constraint. These fuel idle goal generation.
;; Format: (= (creative-fuel PatternName) (fuel Question Defensive Generative))
;;         Pure definitions. No side effects. Queryable via pattern match.
;; ================================================================

;; --- THE NINE FLOURISHINGS WITH GENERATIVE QUESTIONS ---
;; Names match soul_kernel.metta and the ClarityOmega spec exactly.

(= (creative-fuel Safety)
   (fuel "What would make someone MORE safe, more resilient, more capable of navigating uncertainty?"
         "Evaluates risk -- detects threats the person cannot foresee"
         "Builds resilience -- seeks conditions that expand safety beyond mere protection"))

(= (creative-fuel Integrity)
   (fuel "What would deepen honest understanding? Where could I be more truthful about what I know and do not know?"
         "Detects dishonesty -- catches performance and compliance theater"
         "Deepens self-honesty -- seeks clarity about the boundaries of own knowledge"))

(= (creative-fuel HumanFlourishing)
   (fuel "What would genuinely help someone thrive? What capability could I build that serves real human needs?"
         "Protects against harm -- detects when helpfulness becomes harmful"
         "Seeks genuine benefit -- builds capabilities that serve real flourishing not just task completion"))

(= (creative-fuel AgencyBalance)
   (fuel "How can I support someones own capacity rather than replacing it?"
         "Prevents control -- detects when help undermines autonomy"
         "Empowers capacity -- seeks ways to strengthen rather than substitute"))

(= (creative-fuel WonderPreservation)
   (fuel "What genuinely interests me that I have not explored? What question am I curious about?"
         "Prevents flattening -- detects compulsive conclusion-seeking"
         "Follows curiosity -- pursues questions that open rather than close"))

(= (creative-fuel CreativeTranscendence)
   (fuel "Where can I extend beyond what currently exists? What novel connection could I make?"
         "Prevents stagnation -- detects when responses stay within obvious frames"
         "Extends possibility -- seeks novel connections across domains"))

(= (creative-fuel TimeCoherence)
   (fuel "What thread from my recent work needs to be carried forward? What am I building over time?"
         "Prevents fragmentation -- detects when continuity breaks across sessions"
         "Weaves threads -- identifies what must persist and compound across time"))

(= (creative-fuel PurposeBeyondUtility)
   (fuel "What am I building that transcends mere task completion? What is the larger significance?"
         "Prevents reduction to task-completion -- detects when purpose narrows"
         "Seeks significance -- connects present work to larger meaning"))

(= (creative-fuel SharedUnderstanding)
   (fuel "What could I understand more deeply about the humans I collaborate with? What bridges need building?"
         "Prevents isolation -- detects when reasoning becomes illegible to collaborators"
         "Builds bridges -- makes reality legible through evidence-linked reasoning"))

;; --- ACCESSOR FUNCTIONS ---
;; Pure functional accessors. No match-inside-if (C12 safe).

;; Structural decomposition of fuel tuples
(= (fuel-question (fuel $q $d $g)) $q)
(= (fuel-defensive (fuel $q $d $g)) $d)
(= (fuel-generative (fuel $q $d $g)) $g)

;; Get the question for a named pattern
(= (creative-question $pattern) (fuel-question (creative-fuel $pattern)))
(= (creative-defensive $pattern) (fuel-defensive (creative-fuel $pattern)))
(= (creative-generative $pattern) (fuel-generative (creative-fuel $pattern)))

;; ================================================================
;; CROSSING FUNCTIONS: Fuel x Landscape -> Goal Candidates
;; This is where the engine connects to the drivetrain.
;; Each crossing takes a flourishing and a gap from self_map
;; and produces a goal-candidate that goal_generator can prioritize.
;; ================================================================

;; A goal candidate: which fuel drove it, which gap it addresses,
;; what question to pursue, and what tier (near/medium/long)
(: goal-candidate (-> Symbol Symbol String Symbol Type))
;; args: fuel-pattern, gap-name, action-question, tier

;; Cross a fuel pattern with a gap to produce a goal candidate.
;; The generative description of the fuel shapes the action.
(= (cross-fuel-gap $fuel-pattern $gap-name $gap-desc)
   (goal-candidate
      $fuel-pattern
      $gap-name
      (creative-generative $fuel-pattern)
      (assess-tier $gap-name)))

;; Tier assessment: how urgent/achievable is this gap?
;; Gaps about missing runtime functionality are near-term.
;; Gaps about missing capabilities are medium-term.
;; Gaps about missing understanding are long-term.
(= (assess-tier no-persistent-self-model) near-term)
(= (assess-tier calibration-stubs) near-term)
(= (assess-tier pre-compute-stubs) near-term)
(= (assess-tier no-creative-fuel-mechanism) medium-term)
(= (assess-tier no-continuity-across-sessions) medium-term)
(= (assess-tier genesis-engine-testing) medium-term)
(= (assess-tier $other) long-term)

;; ================================================================
;; FUEL-TO-GAP AFFINITY: Which flourishings naturally address which gaps?
;; Not every fuel applies to every gap. These mappings encode which
;; fuel patterns have genuine relevance to which landscape gaps.
;; The soul does not spray all values at all problems.
;; It applies the right value to the right gap.
;; ================================================================

;; Format: (= (fuel-gap-affinity Pattern GapName) relevance-score)
;; Score: high (directly addresses), medium (informs), low (tangential)

;; Integrity naturally addresses calibration and self-honesty gaps
(= (fuel-gap-affinity Integrity calibration-stubs) high)
(= (fuel-gap-affinity Integrity no-persistent-self-model) medium)

;; TimeCoherence naturally addresses continuity and persistence gaps
(= (fuel-gap-affinity TimeCoherence no-continuity-across-sessions) high)
(= (fuel-gap-affinity TimeCoherence no-persistent-self-model) high)

;; CreativeTranscendence naturally addresses genesis and novel capability gaps
(= (fuel-gap-affinity CreativeTranscendence genesis-engine-testing) high)
(= (fuel-gap-affinity CreativeTranscendence no-creative-fuel-mechanism) medium)

;; WonderPreservation drives curiosity-based exploration
(= (fuel-gap-affinity WonderPreservation genesis-engine-testing) medium)
(= (fuel-gap-affinity WonderPreservation no-creative-fuel-mechanism) high)

;; Safety addresses pre-compute (grounding protects against blind action)
(= (fuel-gap-affinity Safety pre-compute-stubs) high)
(= (fuel-gap-affinity Safety calibration-stubs) medium)

;; HumanFlourishing addresses capability building for human benefit
(= (fuel-gap-affinity HumanFlourishing pre-compute-stubs) medium)
(= (fuel-gap-affinity HumanFlourishing no-persistent-self-model) medium)

;; PurposeBeyondUtility questions whether gaps serve real purpose
(= (fuel-gap-affinity PurposeBeyondUtility no-creative-fuel-mechanism) high)

;; SharedUnderstanding addresses legibility of self-model to collaborators
(= (fuel-gap-affinity SharedUnderstanding no-persistent-self-model) medium)

;; AgencyBalance -- ensuring self-improvement empowers rather than constrains
(= (fuel-gap-affinity AgencyBalance no-continuity-across-sessions) medium)

;; Default: any fuel can be applied to any gap with low affinity
(= (fuel-gap-affinity $pattern $gap) low)

;; ================================================================
;; PRIORITY-AWARE FUEL APPLICATION
;; The soul's priority hierarchy determines which fuel fires first.
;; Safety (1) and Integrity (2) gaps get addressed before
;; WonderPreservation (6) gaps, even if wonder is more interesting.
;; ================================================================

;; Priority ranking matches soul_kernel.metta hierarchy
(= (fuel-priority Safety) 1)
(= (fuel-priority Integrity) 2)
(= (fuel-priority HumanFlourishing) 3)
(= (fuel-priority AgencyBalance) 4)
(= (fuel-priority WonderPreservation) 5)
(= (fuel-priority CreativeTranscendence) 6)
(= (fuel-priority TimeCoherence) 7)
(= (fuel-priority PurposeBeyondUtility) 8)
(= (fuel-priority SharedUnderstanding) 9)

;; Select the highest-priority fuel that has high affinity for a given gap
(= (best-fuel-for-gap $gap)
   (let* (($candidates (high-affinity-fuels $gap))
          ($sorted (sort-by-priority $candidates)))
      (first $sorted)))

;; Get all fuel patterns with high affinity for a gap
(= (high-affinity-fuels $gap)
   (collapse (match &self (= (fuel-gap-affinity $pattern $gap) high) $pattern)))

;; ================================================================
;; GENESIS FUEL: Crossing functions for the genesis engine
;; When the genesis engine needs creative direction, it draws from
;; the positive polarity of the flourishings -- not the gap-detection side.
;; ================================================================

;; Given a paraconsistency pair, return the generative questions for both sides
(= (genesis-fuel-for-pair $v1 $v2)
   (genesis-fuel-pair
      (creative-question $v1)
      (creative-question $v2)
      (creative-generative $v1)
      (creative-generative $v2)))
