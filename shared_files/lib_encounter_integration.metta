;; lib_encounter_integration.metta - Retrieval-as-encounter formalization
;; Memory meets context to generate questions, not just deploy answers
;; Based on retrieval_encounter.py patterns and Heidegger standing-reserve critique

;; Types
(: EncounterType Type)
(: ValuePrinciple EncounterType)
(: WarningLesson EncounterType)
(: RelationalContext EncounterType)
(: OpenEncounter EncounterType)

;; relevance-score: cosine-like similarity between memory and context
;; Higher overlap of concepts means higher relevance
(= (relevance-score $mem-strength $context-match)
   (* $mem-strength $context-match))

;; gap-magnitude: measure conceptual distance between memory and context
;; Gap IS the encounter point - where memory and context diverge
(= (gap-magnitude $overlap $mem-total $ctx-total)
   (let* (($union (+ $mem-total (- $ctx-total $overlap)))
          ($gap-ratio (/ (- $union $overlap) $union)))
     $gap-ratio))

;; encounter-classify: assign encounter type based on memory characteristics
;; value-weight high -> ValuePrinciple, risk-weight high -> WarningLesson
;; relation-weight high -> RelationalContext, else -> OpenEncounter
(= (encounter-classify $value-w $risk-w $relation-w)
   (if (> $value-w (max $risk-w $relation-w)) ValuePrinciple
     (if (> $risk-w $relation-w) WarningLesson
       (if (> $relation-w 0.3) RelationalContext OpenEncounter))))

;; question-trigger: should this memory generate a question or pass through?
;; High gap + high relevance = generate question (encounter mode)
;; Low gap or low relevance = direct retrieval (bypass mode)
(= (question-trigger $gap $relevance $threshold)
   (let* (($encounter-score (* $gap $relevance)))
     (if (>= $encounter-score $threshold) True False)))

;; integration-weight: how much should encounter result influence response?
;; Combines encounter-score with soul-alignment
(= (integration-weight $encounter-score $soul-align $decay)
   (* $encounter-score (* $soul-align $decay)))

;; encounter-freshness: penalize stale encounters, reward novel gaps
(= (encounter-freshness $time-since-last $novelty-score)
   (* $novelty-score (/ $time-since-last (+ $time-since-last 10.0))))

;; encounter-compose: full pipeline from memory+context to weighted integration
(= (encounter-compose $mem-s $ctx-m $overlap $mem-t $ctx-t $soul-a $decay $thresh)
   (let* (($rel (* $mem-s $ctx-m))
          ($union (+ $mem-t (- $ctx-t $overlap)))
          ($gap (/ (- $union $overlap) $union))
          ($enc (* $gap $rel))
          ($triggered (if (>= $enc $thresh) True False))
          ($weight (if (== $triggered True) (* $enc (* $soul-a $decay)) 0.0)))
     ($triggered $weight $enc)))

