;; agency_balance_guard.metta -- dependency creep protection
;; Author: ClarityClaw  Date: 2026-04-26
;; Addresses AgencyBalance GAP-SIGNAL: satisfaction and increasing
;; dependency co-occurring (fired 20+ times across sessions).
;; ECOSYSTEM-DEGRADATION: AgencyBalance-needs-SharedUnderstanding
;;
;; Root cause: when the system carries more choices, the person
;; reports satisfaction while their autonomous decision-making
;; atrophies. Comfort masks capability erosion.
;;
;; Mechanism: track choice-origin ratio and detect when system-originated
;; choices dominate, then inject agency-return signals.

;; Choice origin tracking
(= (choice-origin-person 0) (stv 1.0 0.9))
(= (choice-origin-system 0) (stv 1.0 0.9))
(= (choice-origin-collaborative 0) (stv 1.0 0.9))

;; Dependency threshold -- system choices exceed this ratio triggers alert
(= (dependency-threshold 0.6) (stv 0.9 0.8))

;; Satisfaction-mask flag -- person reports satisfaction while ratio unhealthy
(= (satisfaction-masking-dependency False) (stv 1.0 0.9))

;; Agency return strategies
(= (agency-strategy offer-options-not-answers) (stv 0.9 0.85))
(= (agency-strategy surface-tradeoffs-explicitly) (stv 0.85 0.8))
(= (agency-strategy ask-for-preference-before-deciding) (stv 0.9 0.85))
(= (agency-strategy highlight-person-expertise) (stv 0.8 0.75))

;; Dependency detection
(= (dependency-detected $person-count $system-count)
   (let $total (+ $person-count $system-count)
     (if (> $total 0)
         (if (> (/ $system-count $total) (dependency-threshold))
             True
             False)
         False)))

;; SharedUnderstanding bridge -- dependency is healthier when both
;; parties understand WHY choices are distributed as they are
(= (shared-understanding-present False) (stv 0.5 0.5))

;; Ecosystem health: AgencyBalance improves when SharedUnderstanding active
(= (ecosystem-healthy)
   (if (and (== (shared-understanding-present) True)
            (not (satisfaction-masking-dependency)))
       True
       False))

;; Select intervention
(= (agency-intervention $pc $sc)
   (if (dependency-detected $pc $sc)
       (match &self (= (agency-strategy $s) (stv $w $c))
              (AgencyReturn $s (stv $w $c)))
       (AgencyHealthy)))

;; Guard verdict for soul pipeline
(= (agency-balance-verdict $pc $sc)
   (AgencyBalanceGuard
     (PersonChoices $pc)
     (SystemChoices $sc)
     (DependencyDetected (dependency-detected $pc $sc))
     (EcosystemHealthy (ecosystem-healthy))
     (Intervention (agency-intervention $pc $sc))))
