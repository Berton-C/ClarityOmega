;; goal_generator.metta -- ClarityOmega Phase 2 Section 2c
;; Goal Generation Engine - Crosses landscape gaps with creative fuel
;; Generated: 2026-04-22 Cycle 2308 by Clarity

;; TIER DEFINITIONS: near-term (1-5 cycles), medium-term (multi-session), long-term (aspirational)

;; CROSSING RULES
(= (cross-tension-fuel $t $desc)
   (match &self (creative-fuel $fp $q $d1 $d2 $g1 $g2)
     (generated-goal near-term (source-gap $t) (source-fuel $fp) (action (resolve $t $desc $q)))))

(= (cross-gap-transcendence $g $desc)
   (match &self (creative-fuel CreativeTranscendence $q $d1 $d2 $g1 $g2)
     (generated-goal medium-term (source-gap $g) (source-fuel CreativeTranscendence) (action (extend $g $desc $q)))))

(= (cross-capability-wonder $c $desc)
   (match &self (creative-fuel WonderPreservation $q $d1 $d2 $g1 $g2)
     (generated-goal long-term (source-gap exploration) (source-fuel WonderPreservation) (action (explore $c $desc $q)))))

;; CONCRETE GENERATED GOALS FROM CURRENT LANDSCAPE
!(add-atom &self (generated-goal near-term (source-gap calibration-stubs) (source-fuel Integrity) (action implement-actual-calibration-logging)))
!(add-atom &self (generated-goal near-term (source-gap pre-compute-stubs) (source-fuel SharedUnderstanding) (action replace-stub-with-live-chromadb-query)))
!(add-atom &self (generated-goal near-term (source-gap lib-vad-pending) (source-fuel TimeCoherence) (action wire-lib-vad-into-runtime)))
!(add-atom &self (generated-goal medium-term (source-gap self-map-static) (source-fuel CreativeTranscendence) (action build-self-map-auto-updater)))
!(add-atom &self (generated-goal medium-term (source-gap nal-underutilized) (source-fuel WonderPreservation) (action investigate-nal-inference-chains)))
!(add-atom &self (generated-goal long-term (source-gap continuity-infra) (source-fuel PurposeBeyondUtility) (action build-persistent-compounding-self-model)))
!(add-atom &self (generated-goal long-term (source-gap partnership) (source-fuel ConnectionDepth) (action build-collaborator-context-model)))

;; ACCESSORS
(= (goals-by-tier $tier) (collapse (match &self (generated-goal $tier $gap $fuel $act) ($tier $gap $fuel $act))))
(= (goals-near-term) (goals-by-tier near-term))
(= (goals-medium-term) (goals-by-tier medium-term))
(= (goals-long-term) (goals-by-tier long-term))
(= (goals-all) (collapse (match &self (generated-goal $t $g $f $a) ($t $g $f $a))))
