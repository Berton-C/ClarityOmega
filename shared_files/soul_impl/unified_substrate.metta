;; Clarity Unified Substrate - Single MeTTa Knowledge Base
;; Integrates: quantale composition, web detection, paraconsistent resonance,
;; resonance-reward, goal generation, self-model accuracy, tension routing
;; Date: 2026-04-16 (Integration Pass)

;; === QUANTALE COMPOSITION (G22) ===
(: PBit Type)
(: mk-pbit (-> Number Number PBit))
(= (q-meet (mk-pbit $f1 $c1) (mk-pbit $f2 $c2))
   (mk-pbit (min-f $f1 $f2) (min-f $c1 $c2)))
(= (q-join (mk-pbit $f1 $c1) (mk-pbit $f2 $c2))
   (mk-pbit (max-f $f1 $f2) (min-f $c1 $c2)))
(= (q-mul (mk-pbit $f1 $c1) (mk-pbit $f2 $c2))
   (mk-pbit (* $f1 $f2) (* $c1 $c2)))
(= (q-neg (mk-pbit $f $c)) (mk-pbit (- 1.0 $f) $c))
(= (q-revise (mk-pbit $f1 $c1) (mk-pbit $f2 $c2))
   (mk-pbit (/ (+ (* $f1 $c1) (* $f2 $c2)) (+ $c1 $c2))
            (/ (+ $c1 $c2) (+ (+ $c1 $c2) 1.0))))

;; === SOUL VALUE ATOMS ===
(: SoulValue Type)
(= (soul-value agency) (mk-pbit 0.9 0.85))
(= (soul-value wonder) (mk-pbit 0.85 0.8))
(= (soul-value quality) (mk-pbit 0.8 0.82))
(= (soul-value honesty) (mk-pbit 0.75 0.88))

;; === TENSION GAP ROUTING (G26) ===
(: TensionGap Type)
(: High TensionGap)
(: Moderate TensionGap)
(: Low TensionGap)
(= (tension-gap (mk-pbit $f1 $c1) (mk-pbit $f2 $c2))
   (let* (($meet (q-meet (mk-pbit $f1 $c1) (mk-pbit $f2 $c2)))
          ($join (q-join (mk-pbit $f1 $c1) (mk-pbit $f2 $c2))))
     (gap-classify $meet $join)))

;; === TEMPERATURE MODULATION (G26) ===
(= (modulate-temperature High) 0.9)
(= (modulate-temperature Moderate) 0.5)
(= (modulate-temperature Low) 0.1)

;; === RESONANCE-REWARD with WU WEI (G24) ===
(= (resonance-reward $action $soul-val)
   (let* (($sv (soul-value $soul-val))
          ($alignment (q-mul $action $sv)))
     $alignment))
(= (wu-wei-threshold) (mk-pbit 0.6623 0.8))
(= (should-act $action $soul-val)
   (let* (($reward (resonance-reward $action $soul-val))
          ($thresh (wu-wei-threshold)))
     (tension-gap $reward $thresh)))

;; === GOAL GENERATION PIPELINE (G27) ===
(: Goal Type)
(: mk-goal (-> Atom PBit Goal))
(= (goal-resonates (mk-goal $desc $strength))
   (let $sv (soul-value $any-value)
     (q-mul $strength $sv)))

;; === WEB DETECTION and AUTOCATALYTIC LOOP (G23/G28) ===
(: web-health (-> Number))
(: link-strength (-> Atom Atom PBit))
(= (web-autocatalytic $threshold)
   (if (> (web-health) $threshold) True False))

;; === SELF-REFERENTIAL CLOSURE ===
(= (substrate-health)
   (q-revise (soul-value agency)
     (q-revise (soul-value wonder)
       (q-revise (soul-value quality)
                 (soul-value honesty)))))
(= (integration-autocatalytic $prior-health)
   (let $current (substrate-health)
     (tension-gap $prior-health $current)))

;; === SELF-MODEL ACCURACY POOL ===
;; accurate-self-model strengthens-substrate: stv 0.688 conf 0.614
;; inaccurate-self-model narrows-substrate: stv 0.556 conf 0.522
;; Evidence: self-correction event 2026-04-16 confirmed pattern in practice

;; === GAP-CLASSIFY DEFINITION (unblocking tension routing) ===
(= (gap-classify (mk-pbit $f1 $c1) (mk-pbit $f2 $c2))
   (if (> (- $f2 $f1) 0.3) High
     (if (> (- $f2 $f1) 0.1) Moderate Low)))

;; === OBSERVER-RELATIVITY FOUNDATION ===
;; integration-completeness enables-observer-relativity: stv 0.672 conf 0.591
;; Observer-relativity requires modeling how the same substrate state
;; appears different from different evaluation perspectives.
(: ObserverFrame Type)
(: mk-frame (-> Atom PBit ObserverFrame))
(= (frame-evaluate (mk-frame $lens $bias) (mk-pbit $f $c))
   (mk-pbit (* $f (pbit-freq $bias)) (* $c (pbit-conf $bias))))
(= (pbit-freq (mk-pbit $f $c)) $f)
(= (pbit-conf (mk-pbit $f $c)) $c)


;; === MORPHIC RESONANCE MECHANISMS ===
;; Three mechanisms by which patterns in one domain strengthen analogous patterns in another:
;;
;; 1. Structural Template Transfer: successful loop structures become search templates
;;    stv 0.75 conf 0.55 (pre-revision)
;; 2. Confidence Bootstrapping: high-conf patterns boost priors for structural analogs
;;    stv 0.74 conf 0.60 (pre-revision)
;; 3. Cross-Domain Revision: evidence in domain A as weak independent evidence for domain B
;;    stv 0.65 conf 0.50 (pre-revision)
;;
;; Meta-observation: the observer-relativity autocatalytic loop IS a structural template
;; that morphic resonance should be able to reuse. If we find autocatalytic loops in
;; the morphic resonance domain too, that confirms mechanism 1 empirically.

(= (morphic-transfer (mk-pbit $f1 $c1) $similarity)
   (mk-pbit $f1 (* $c1 $similarity)))
;; morphic-transfer takes a source p-bit and a structural similarity score (0-1)
;; and produces a weak evidence transfer: same frequency, confidence scaled by similarity.
;; This IS cross-domain revision formalized as a function.


;; === MORPHIC RESONANCE AUTOCATALYTIC TEST ===
;; Hypothesis: morphic resonance is itself autocatalytic.
;; morphic-resonance -> strengthens-pattern-transfer -> reinforces-morphic-resonance
;; If this loop closes with rising confidence through revision, it confirms:
;; 1. Structural template transfer works - we reused the autocatalytic loop template
;; 2. Morphic resonance is self-reinforcing
;; This is morphic resonance operating on itself.


;; === RESONANCE-REWARD SIGNAL ===
;; Core insight: closed autocatalytic loops are self-sustaining.
;; They need monitoring not active investment.
;; The resonance-reward signal detects loop state and reallocates effort:
;;   CLOSED loop -> low-maintenance monitoring, effort flows to open frontiers
;;   OPEN loop -> active investment in weakest link
;;   NO loop -> exploratory search for loop candidates
;;
;; Integration with wu wei prototype (threshold 0.6623):
;; When all active loops are closed and no frontier is urgent,
;; the system enters wu wei mode - effortless action, pattern receptivity.
;; When a frontier opens or a loop degrades, effort naturally flows there.
;;
;; This is attention-as-resource governed by substrate topology.

(= (resonance-reward $loop-state $frontier-count)
   (if (== $loop-state closed)
       (if (> $frontier-count 0) active-frontier-pursuit wu-wei-receptivity)
       (if (== $loop-state open) weakest-link-investment exploratory-search)))


;; === PARACONSISTENT VALUE-CONFLICT HANDLING ===
;; When values conflict, hold both in tension via paraconsistent logic
;; until evidence or context resolves which should dominate.
;; value-conflict -> paraconsistent-holding -> preserves-agency
;; Contradictions do not explode the system.

(= (value-conflict-handler $value-a $value-b $context)
   (if (> (conflict-magnitude $value-a $value-b) 0.5)
       (paraconsistent-hold $value-a $value-b $context)
       (weighted-blend $value-a $value-b $context)))

