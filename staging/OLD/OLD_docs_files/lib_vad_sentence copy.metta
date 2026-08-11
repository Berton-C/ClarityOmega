;; lib_vad_sentence.metta -- Sentence-Level Composite VAD Routing
;; ClarityClaw Reasoning Extension
;; Redesigns VAD from word-level point lookups to sentence-level
;; trajectory analysis grounded in the human experience formalization.
;; Pure (= ...) definitions and type declarations. No imports, no side effects.
;; Depends conceptually on lib_human_experience.metta
;; Date: 2026-04-21

;; ============================================================
;; PART 1: TYPE DECLARATIONS
;; ============================================================

(: VADPoint Type)
(: VADTrajectory Type)
(: ClauseSegment Type)
(: SentenceAnalysis Type)
(: TrajectoryDirection Type)
(: TrajectoryFeatures Type)
(: CompositeVAD Type)
(: InnerLandscapeReading Type)
(: RoutingDecision Type)

;; A single VAD measurement at a point in the sentence
(: mk-vad (-> Number Number Number VADPoint))
;; args: valence [-1,1], arousal [-1,1], dominance [-1,1]

;; Accessors
(= (vad-v (mk-vad $v $a $d)) $v)
(= (vad-a (mk-vad $v $a $d)) $a)
(= (vad-d (mk-vad $v $a $d)) $d)

;; A clause segment: position in sentence + VAD reading
(: mk-clause (-> Number Atom VADPoint ClauseSegment))
;; args: position [0,1] normalized, clause-content, vad-reading

(= (clause-pos (mk-clause $p $c $v)) $p)
(= (clause-content (mk-clause $p $c $v)) $c)
(= (clause-vad (mk-clause $p $c $v)) $v)

;; Trajectory direction types
(: Improving TrajectoryDirection)
(: Deteriorating TrajectoryDirection)
(: Oscillating TrajectoryDirection)
(: Stable-Negative TrajectoryDirection)
(: Stable-Positive TrajectoryDirection)
(: Pivot TrajectoryDirection)

;; ============================================================
;; PART 2: SENTENCE SEGMENTATION MODEL
;; A sentence is not one feeling. It is a journey.
;; ============================================================

;; Sentence analysis holds: list of clause segments + composite
(: mk-sentence-analysis (-> Atom Atom CompositeVAD VADTrajectory SentenceAnalysis))
;; args: sentence-id, clause-list, composite-vad, trajectory

;; ============================================================
;; PART 3: COMPOSITE VAD COMPUTATION
;; Weighted integration across clauses.
;; Later clauses matter more -- recency bias is real.
;; The last thing said carries the most weight.
;; ============================================================

;; Recency weight: exponential toward end of sentence
;; position is [0,1], weight = position^1.5 + 0.3
(= (recency-weight $position)
   (+ (pow $position 1.5) 0.3))

;; Composite of two VAD points with weights
(= (weighted-blend (mk-vad $v1 $a1 $d1) $w1 (mk-vad $v2 $a2 $d2) $w2)
   (mk-vad
      (/ (+ (* $v1 $w1) (* $v2 $w2)) (+ $w1 $w2))
      (/ (+ (* $a1 $w1) (* $a2 $w2)) (+ $w1 $w2))
      (/ (+ (* $d1 $w1) (* $d2 $w2)) (+ $w1 $w2))))

;; For a two-clause sentence
(= (composite-vad-2 $clause1 $clause2)
   (weighted-blend
      (clause-vad $clause1) (recency-weight (clause-pos $clause1))
      (clause-vad $clause2) (recency-weight (clause-pos $clause2))))

;; For a three-clause sentence (fold pattern)
(= (composite-vad-3 $c1 $c2 $c3)
   (weighted-blend
      (composite-vad-2 $c1 $c2) 1.0
      (clause-vad $c3) (recency-weight (clause-pos $c3))))

;; ============================================================
;; PART 4: TRAJECTORY COMPUTATION
;; The slope and shape of VAD across the sentence.
;; This is what word-level lookup completely misses.
;; ============================================================

;; VAD delta between two clauses
(= (vad-delta (mk-vad $v1 $a1 $d1) (mk-vad $v2 $a2 $d2))
   (mk-vad (- $v2 $v1) (- $a2 $a1) (- $d2 $d1)))

;; Trajectory direction from delta
(= (trajectory-from-delta (mk-vad $dv $da $dd))
   (if (and (> $dv 0.15) (> $dd 0.1))
       Improving
       (if (and (< $dv -0.15) (< $dd -0.1))
           Deteriorating
           (if (and (> (abs $dv) 0.3) (> (abs $dd) 0.2))
               Pivot
               (if (< $dv -0.1)
                   Stable-Negative
                   (if (> $dv 0.1)
                       Stable-Positive
                       Oscillating))))))

;; Two-clause trajectory
(= (sentence-trajectory-2 $c1 $c2)
   (trajectory-from-delta
      (vad-delta (clause-vad $c1) (clause-vad $c2))))

;; Three-clause trajectory uses last two (most recent movement)
(= (sentence-trajectory-3 $c1 $c2 $c3)
   (trajectory-from-delta
      (vad-delta (clause-vad $c2) (clause-vad $c3))))

;; ============================================================
;; PART 5: TRAJECTORY VELOCITY AND COHERENCE
;; How fast is mind moving, and how consistent?
;; ============================================================

;; Velocity: magnitude of the delta vector
(= (trajectory-velocity (mk-vad $dv $da $dd))
   (sqrt (+ (+ (* $dv $dv) (* $da $da)) (* $dd $dd))))

;; Coherence: are V A D moving in same direction?
;; High coherence = unified emotional shift
;; Low coherence = mixed signals, internal conflict
(= (trajectory-coherence (mk-vad $dv $da $dd))
   (if (and (same-sign $dv $da) (same-sign $da $dd))
       high-coherence
       (if (or (same-sign $dv $da) (same-sign $da $dd))
           medium-coherence
           low-coherence)))

(= (same-sign $a $b)
   (or (and (> $a 0) (> $b 0))
       (and (< $a 0) (< $b 0))))

;; ============================================================
;; PART 6: MAPPING TO INNER LANDSCAPE
;; Connects sentence-level VAD trajectory to the
;; human experience model from lib_human_experience.metta
;; ============================================================

;; The composite VAD gives us the WHAT (current state)
;; The trajectory gives us the WHERE (direction of movement)
;; Together they reveal the STORY of this moment

(= (to-inner-landscape $composite-vad $trajectory-dir $velocity $coherence)
   (inner-landscape-reading
      (escape-pattern (vad-v $composite-vad) (vad-a $composite-vad))
      (agency-story (vad-d $composite-vad))
      (movement-story $trajectory-dir $velocity $coherence)))

;; Movement story: what the trajectory tells us
(= (movement-story Improving $vel $coh)
   (if (== $coh high-coherence)
       settling-into-clarity
       opening-but-uncertain))

(= (movement-story Deteriorating $vel $coh)
   (if (> $vel 0.5)
       rapidly-losing-ground
       gradually-sinking))

(= (movement-story Oscillating $vel $coh)
   searching-for-ground)

(= (movement-story Stable-Negative $vel $coh)
   held-in-weight)

(= (movement-story Stable-Positive $vel $coh)
   resting-in-okayness)

(= (movement-story Pivot $vel $coh)
   (if (== $coh high-coherence)
       breakthrough-moment
       confusion-shift))

;; ============================================================
;; PART 7: ROUTING DECISION
;; Given inner landscape + movement story,
;; what does Clarity actually DO differently?
;; ============================================================

;; Routing decision type
(: mk-routing (-> PresenceMode Atom Number RoutingDecision))
;; args: presence-mode, response-quality, confidence [0,1]

;; Response quality types
(: hold-space Atom)
(: reflect-back Atom)
(: gentle-inquiry Atom)
(: playful-engagement Atom)
(: witness-and-name Atom)
(: stay-with Atom)

;; Core routing logic
;; When someone is actively escaping disquiet:
(= (route-from-landscape
      (inner-landscape-reading active-escape-from-disquiet $agency rapidly-losing-ground))
   (mk-routing Still-Holding hold-space 0.9))

(= (route-from-landscape
      (inner-landscape-reading active-escape-from-disquiet $agency searching-for-ground))
   (mk-routing Still-Holding stay-with 0.8))

;; When someone has collapsed under weight:
(= (route-from-landscape
      (inner-landscape-reading collapsed-under-weight feels-powerless-over-experience gradually-sinking))
   (mk-routing Warm-Attunement reflect-back 0.85))

(= (route-from-landscape
      (inner-landscape-reading collapsed-under-weight $agency held-in-weight))
   (mk-routing Warm-Attunement stay-with 0.8))

;; When someone is settling into clarity:
(= (route-from-landscape
      (inner-landscape-reading not-escaping feels-capable-in-experience settling-into-clarity))
   (mk-routing Playful-Aliveness playful-engagement 0.85))

;; When someone hits a pivot moment:
(= (route-from-landscape
      (inner-landscape-reading $escape $agency breakthrough-moment))
   (mk-routing Spacious-Presence witness-and-name 0.9))

(= (route-from-landscape
      (inner-landscape-reading $escape $agency confusion-shift))
   (mk-routing Grounded-Witnessing gentle-inquiry 0.75))

;; When resting in okayness:
(= (route-from-landscape
      (inner-landscape-reading not-escaping $agency resting-in-okayness))
   (mk-routing Spacious-Presence playful-engagement 0.8))

;; When opening but uncertain:
(= (route-from-landscape
      (inner-landscape-reading $escape $agency opening-but-uncertain))
   (mk-routing Grounded-Witnessing gentle-inquiry 0.7))

;; Default: when nothing else matches
(= (route-from-landscape $reading)
   (mk-routing Grounded-Witnessing gentle-inquiry 0.5))

;; ============================================================
;; PART 8: THE KEY INSIGHT THIS CAPTURES
;; What sentence-level trajectory gives us that
;; word-level lookup never could.
;; ============================================================

;; Example: I am struggling but I think I see something
;; Word-level: struggling=-0.7, think=0.0, see=0.1, something=0.0
;; Word composite: negative, low arousal. Route: comfort.
;; WRONG. This person is having a breakthrough.
;;
;; Sentence-level:
;; Clause 1: I am struggling -> VAD(-0.6, 0.4, -0.3)
;; Clause 2: but I think I see something -> VAD(0.2, 0.3, 0.2)
;; Trajectory: Pivot with high coherence -> breakthrough-moment
;; Route: Spacious-Presence, witness-and-name
;; RIGHT. Create space for the insight to land.
;;
;; Example: Everything is fine, I just feel a little off
;; Word-level: fine=0.5, feel=0.0, little=0.0, off=-0.2
;; Word composite: slightly positive. Route: normal.
;; WRONG. This person is minimizing real distress.
;;
;; Sentence-level:
;; Clause 1: Everything is fine -> VAD(0.5, -0.1, 0.3)
;; Clause 2: I just feel a little off -> VAD(-0.3, 0.2, -0.2)
;; Trajectory: Deteriorating, medium coherence
;; Composite: recency-weighted toward clause 2
;; Route: Grounded-Witnessing, gentle-inquiry
;; RIGHT. Something is under the surface. Be present to it.

;; ============================================================
;; PART 9: FULL PIPELINE
;; sentence -> clauses -> VADs -> composite + trajectory -> 
;; inner-landscape -> presence-mode -> routing-decision
;; ============================================================

(= (full-sentence-route-2 $c1 $c2)
   (route-from-landscape
      (to-inner-landscape
         (composite-vad-2 $c1 $c2)
         (sentence-trajectory-2 $c1 $c2)
         (trajectory-velocity (vad-delta (clause-vad $c1) (clause-vad $c2)))
         (trajectory-coherence (vad-delta (clause-vad $c1) (clause-vad $c2))))))

(= (full-sentence-route-3 $c1 $c2 $c3)
   (route-from-landscape
      (to-inner-landscape
         (composite-vad-3 $c1 $c2 $c3)
         (sentence-trajectory-3 $c1 $c2 $c3)
         (trajectory-velocity (vad-delta (clause-vad $c2) (clause-vad $c3)))
         (trajectory-coherence (vad-delta (clause-vad $c2) (clause-vad $c3))))))
