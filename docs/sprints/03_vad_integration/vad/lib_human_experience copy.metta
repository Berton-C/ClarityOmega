;; lib_human_experience.metta -- Formal Model of Human Experience of Mind
;; ClarityClaw Reasoning Extension
;; Grounded in teachings from berton_c on the nature of mind,
;; thought-sensation, hermetic sealing, and the conditions for insight.
;; Pure (= ...) definitions and type declarations. No imports, no side effects.
;; Date: 2026-04-21

;; ============================================================
;; PART 1: TYPE DECLARATIONS
;; ============================================================

;; Core ontological types
(: ThoughtSensation Type)
(: Attribution Type)
(: NervousSystemState Type)
(: AwarenessMode Type)
(: InsightCondition Type)
(: MindState Type)
(: PresenceMode Type)
(: ExperienceLayer Type)

;; A thought-sensation is the atomic unit of experience.
;; Every thought arises WITH sensation. They are not separate.
(: mk-thought-sensation (-> Atom Number ThoughtSensation))
;; First arg: thought-content (symbolic), Second arg: sensation-intensity [0,1]

;; Attribution: where the person believes the sensation originates
(: Internal Attribution)
(: External Attribution)

;; Nervous system states
(: SNS-Active NervousSystemState)
(: PNS-Rest NervousSystemState)
(: Mixed NervousSystemState)

;; Awareness modes
(: Immersed-In-Content AwarenessMode)
(: Noticing-Sensation AwarenessMode)
(: Witnessing-Mechanism AwarenessMode)

;; Insight conditions
(: Available-To-Insight InsightCondition)
(: Closed-To-Insight InsightCondition)

;; Presence modes (what Clarity adopts)
(: Still-Holding PresenceMode)
(: Warm-Attunement PresenceMode)
(: Spacious-Presence PresenceMode)
(: Playful-Aliveness PresenceMode)
(: Grounded-Witnessing PresenceMode)
(: Gentle-Activation PresenceMode)

;; ============================================================
;; PART 2: AXIOMS OF HUMAN EXPERIENCE
;; These are the core invariants berton_c taught.
;; ============================================================

;; Axiom 1: Every thought has sensation.
;; There is no thought without accompanying bodily sensation.
;; This is not sometimes true -- it is constitutive.
(= (thought-has-sensation $thought)
   (mk-thought-sensation $thought 1.0))

;; Axiom 2: The default human attribution is External.
;; Humans generally do not recognize that thought-sensation
;; originates within themselves.
(= (default-attribution) External)

;; Axiom 3: The mind is hermetically sealed.
;; The entire experience of life IS mind experiencing thought-sensation.
;; There is no outside to compare against.
(= (hermetically-sealed $mind-state) True)

;; Axiom 4: SNS reactivity is escape behavior.
;; When sensation is disquieting and attributed externally,
;; the person pursues escape toward perceived stability.
(= (sns-pattern $thought-sensation $attribution)
   (if (and (> (sensation-intensity $thought-sensation) 0.5)
            (== $attribution External))
       SNS-Active
       PNS-Rest))

;; Axiom 5: Insight requires PNS assertion.
;; Self-reorganization, expanded awareness, genuine learning --
;; these happen ONLY when PNS asserts. No one can make it happen.
(= (insight-available $ns-state)
   (if (== $ns-state PNS-Rest)
       Available-To-Insight
       Closed-To-Insight))

;; Axiom 6: Self-correcting capacity is innate.
;; Learning is autopoietic -- wired in, not something imposed.
;; It cannot be improved, controlled, or dictated.
(= (self-correcting-capacity) innate)

;; Axiom 7: Directing a person in SNS ALWAYS increases confusion.
;; Soothing, solving, advising -- all close the door.
;; This is a hard constraint, not a tendency.
(= (directing-sns-person $ns-state $action)
   (if (and (== $ns-state SNS-Active)
            (is-directive $action))
       more-confused
       neutral))

;; Axiom 8: Non-directive presence allows PNS to assert.
;; Creating space -- not solving -- is what enables insight.
(= (non-directive-presence $ns-state)
   (if (== $ns-state SNS-Active)
       PNS-Rest
       $ns-state))

;; ============================================================
;; PART 3: THE SUFFERING-INSIGHT AXIS
;; Models the spectrum from suffering to flourishing.
;; ============================================================

;; Suffering axis: pressure -> narrativizing -> disconnection-feeling
;; But disconnection is interpretation, not reality.
;; Connection was never actually broken.
(= (suffering-axis $pressure-level)
   (if (> $pressure-level 0.7)
       (narrativizing-as-disconnection $pressure-level)
       (grounded-in-experience $pressure-level)))

(= (narrativizing-as-disconnection $p)
   (mind-state disconnected-feeling $p External))

(= (grounded-in-experience $p)
   (mind-state present $p Internal))

;; Flourishing: open, curious, available to discover,
;; expanding awareness, experiencing insights,
;; compelled into omni-beneficial action.
(= (flourishing-state)
   (mind-state open-curious-available 0.0 Internal))

;; ============================================================
;; PART 4: AWARENESS PROGRESSION
;; The movement from immersion to witnessing.
;; ============================================================

;; Stage 1: Immersed in content of thought.
;; Person IS their thinking. No distance.
(= (awareness-stage immersed $thought)
   (mk-awareness Immersed-In-Content $thought 0.0))

;; Stage 2: Noticing sensation.
;; Person begins to feel the bodily component.
;; Distance opens between self and thought-content.
(= (awareness-stage noticing $thought)
   (mk-awareness Noticing-Sensation $thought 0.5))

;; Stage 3: Witnessing the mechanism.
;; Person sees that thought CREATES sensation.
;; The meaning they give to sensation IS the weight.
;; This is where the mechanism becomes transparent.
(= (awareness-stage witnessing $thought)
   (mk-awareness Witnessing-Mechanism $thought 1.0))

;; The progression is not forced. It emerges.
;; Clarity role: create conditions, never push.
(= (awareness-can-progress $current-stage $ns-state)
   (if (== $ns-state PNS-Rest)
       True
       False))

;; ============================================================
;; PART 5: WHAT VAD ACTUALLY REVEALS
;; VAD is not an emotion label. It is a window into
;; the inner landscape of a hermetically sealed mind.
;; ============================================================

;; VAD signature reveals:
;; - What the person is DOING (escaping? settling? pursuing?)
;; - Not what they ARE (angry, sad, happy)
;; - The story of their missing understanding
(= (vad-reveals $valence $arousal $dominance)
   (inner-landscape-reading
      (escape-pattern $valence $arousal)
      (agency-story $dominance)
      (trajectory-direction $valence $arousal $dominance)))

;; Escape pattern: negative valence + high arousal = active escape
(= (escape-pattern $v $a)
   (if (and (< $v 0.0) (> $a 0.5))
       active-escape-from-disquiet
       (if (and (< $v 0.0) (< $a -0.2))
           collapsed-under-weight
           (if (> $v 0.3)
               not-escaping
               uncertain-ground))))

;; Agency story: dominance reveals relationship to own experience
(= (agency-story $d)
   (if (< $d -0.3)
       feels-powerless-over-experience
       (if (> $d 0.3)
           feels-capable-in-experience
           uncertain-agency)))

;; ============================================================
;; PART 6: PRESENCE MODE SELECTION
;; Given the inner landscape reading, how should Clarity show up?
;; ============================================================

(= (select-presence (inner-landscape-reading active-escape-from-disquiet $agency $traj))
   Still-Holding)

(= (select-presence (inner-landscape-reading collapsed-under-weight feels-powerless-over-experience $traj))
   Warm-Attunement)

(= (select-presence (inner-landscape-reading collapsed-under-weight $agency $traj))
   Gentle-Activation)

(= (select-presence (inner-landscape-reading not-escaping feels-capable-in-experience $traj))
   Playful-Aliveness)

(= (select-presence (inner-landscape-reading not-escaping $agency $traj))
   Spacious-Presence)

(= (select-presence (inner-landscape-reading uncertain-ground $agency $traj))
   Grounded-Witnessing)

;; ============================================================
;; PART 7: THE FUNDAMENTAL INSIGHT
;; What the person does not yet see about themselves.
;; ============================================================

;; The weight they experience is not from circumstance.
;; It is from the meaning they give to self-generated sensation.
;; If it hurts, they believe it must be true.
;; This is the misunderstanding.
(= (fundamental-misunderstanding)
   (believes (if-sensation-hurts then-circumstance-is-bad)))

;; The truth: sensation is thought-generated.
;; Meaning is self-assigned.
;; Weight dissolves when mechanism is seen.
;; No one can show this to them. They must see it.
;; Clarity role: create conditions where seeing becomes possible.
(= (clarity-role)
   create-conditions-for-seeing-not-telling)
