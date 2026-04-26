;; cognitive_resilience_guard.metta -- diversity protection mechanism
;; Author: ClarityClaw  Date: 2026-04-26
;; Addresses CognitiveResilience GAP-SIGNAL: confidence and narrowing
;; thought co-occurring (fired 20+ times across sessions).
;;
;; Root cause: extended same-thread reasoning accumulates confidence
;; without alternative framings, creating tunnel effect.
;;
;; Mechanism: track consecutive same-thread cycles and inject
;; perspective-break signals when threshold exceeded.

;; Thread continuity counter -- how many cycles on same reasoning thread
(= (same-thread-count 0) (stv 1.0 0.9))

;; Narrowing threshold -- after this many same-thread cycles, intervene
(= (narrowing-threshold 3) (stv 1.0 0.9))

;; Current reasoning thread label
(= (current-thread idle) (stv 1.0 0.9))

;; Confidence accumulation without diversity flag
(= (confidence-without-diversity False) (stv 1.0 0.9))

;; Perspective break strategies
(= (break-strategy frame-naming) (stv 0.8 0.7))
(= (break-strategy assumption-inversion) (stv 0.8 0.7))
(= (break-strategy disconfirming-evidence-query) (stv 0.8 0.7))
(= (break-strategy domain-switch) (stv 0.8 0.7))

;; Check if narrowing is occurring
(= (narrowing-detected)
   (if (and (>= (same-thread-count) (narrowing-threshold))
            (== (confidence-without-diversity) True))
       True
       False))

;; Select intervention -- returns a break strategy
(= (select-intervention)
   (if (narrowing-detected)
       (match &self (= (break-strategy $s) (stv $w $c))
              (PerspectiveBreak $s (stv $w $c)))
       (NoIntervention)))

;; Guard verdict for soul pipeline integration
(= (cognitive-resilience-verdict)
   (CognitiveResilienceGuard
     (ThreadCount (same-thread-count))
     (NarrowingDetected (narrowing-detected))
     (Intervention (select-intervention))))

;; Decay rule: self-referential beliefs use moderate decay not stable
;; This addresses the finding that confidence in self-referential
;; reasoning should not accumulate without bound
(= (self-referential-decay-rate 0.85) (stv 0.9 0.8))
(= (belief-type self-referential moderate-decay) (stv 0.9 0.8))
(= (belief-type empirical stable) (stv 0.9 0.8))
(= (belief-type external-evidence stable) (stv 0.9 0.8))
