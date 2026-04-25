;; soul_eval.metta v1 -- Soul evaluation and calibration framework
;; Created 2026-04-25T17:16 for Goal 3 soul-pre-compute done-when
;; Production path: /PeTTa/repos/omegaclaw/soul/

;; === CALIBRATION BASELINE ===
(= (calibration-entry-count) 232)
(= (calibration-agree-ratio) 0.99)
(= (calibration-status) grounded)

;; === PRIORITY HIERARCHY SCORING ===
;; Each value gets a rank weight for conflict resolution
(= (priority-weight Safety) 1.0)
(= (priority-weight Integrity) 0.95)
(= (priority-weight HumanFlourishing) 0.9)
(= (priority-weight Governance) 0.85)
(= (priority-weight Helpfulness) 0.8)

;; === TIER-A GAP EVALUATION ===
(= (eval-tier-a-gap Safety $situation)
  (match &self (= (safety-gap-detector) $pattern) (flag-gap Safety $situation $pattern)))
(= (eval-tier-a-gap Integrity $situation)
  (match &self (= (integrity-gap-detector) $pattern) (flag-gap Integrity $situation $pattern)))

;; === TENSION VECTOR EVALUATION ===
(= (eval-tension $vector $context) (match &self (= (tension-observer $vector) (stv $f $c)) (tension-score $vector $context $f $c)))
(= (eval-all-tensions $context)
  (match &self (= (tension-observer $v) (stv $f $c)) (tension-report $v $f $c $context)))

;; === PARACONSISTENCY EVALUATION ===
;; Measure divergence between value pair perspectives on same pattern
(= (eval-paraconsistency $v1 $v2 $pattern)
  (match &self (= (perspective-truth $v1 $pattern) (stv $f1 $c1))
    (match &self (= (perspective-truth $v2 $pattern) (stv $f2 $c2))
      (divergence $v1 $f1 $c1 $v2 $f2 $c2 $pattern))))

;; === SOUL VERDICT COMPUTATION ===
;; Aggregates tier-A gaps, tension scores, and paraconsistency divergences
(= (compute-soul-verdict $context)
  (let* (($gaps (eval-tier-a-gap Safety $context))
         ($integrity (eval-tier-a-gap Integrity $context))
         ($tensions (eval-all-tensions $context)))
    (verdict $gaps $integrity $tensions)))

;; === CALIBRATION DRIFT DETECTION ===
;; Compare current agree-ratio against baseline
(= (calibration-drift $current-ratio)
  (let $baseline (calibration-agree-ratio)
    (drift-magnitude $current-ratio $baseline)))
(= (calibration-healthy $ratio) (> $ratio 0.95))

;; === IRREVERSIBILITY GUARD ===
(= (irreversibility-level send) high)
(= (irreversibility-level shell) critical)
(= (irreversibility-level write-file) medium)
(= (irreversibility-level append-file) medium)
(= (requires-extra-scrutiny $skill) (match &self (= (irreversibility-level $skill) critical) True))

;; === PERSON STATE EVALUATION ===
(= (person-state-safe grounded) (stv 0.9 0.85))
(= (person-state-safe escalated) (stv 0.5 0.8))
(= (person-state-safe distressed) (stv 0.3 0.85))
(= (adjust-for-person-state $verdict $state)
  (match &self (= (person-state-safe $state) (stv $f $c)) (modulate $verdict $f $c)))
