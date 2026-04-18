;; Counterfactual Reasoning Method for NAL
;; Date: 2026-04-17
;; Two methods compared and validated:
;;
;; METHOD 1: NEGATION (stv 0.0 high-conf)
;; Result: 0.0/0.0 epistemic vacuum - evidence destroyed
;; Use case: modeling complete absence, detecting dependency
;; If chain produces 0.0/0.0, the antecedent IS causally necessary
;;
;; METHOD 2: SUBSTITUTION (swap alternative premise at stv 1.0)
;; Result: positive stv propagates normally
;; Use case: what-if analysis, comparing alternative worlds
;; Contrast between factual and counterfactual outputs = causal contribution
;;
;; PROTOCOL:
;; 1. Run factual chain with actual premise values
;; 2. Run substitution chain with alternative premise
;; 3. Compare conclusions - difference reveals causal structure
;; 4. Optionally run negation chain to confirm dependency
;;
;; Example: autonomy-service alignment
;; Factual (aligned stv 0.0): confident-execution stv 0.0/0.0 (vacuum)
;; Counterfactual (aligned stv 1.0): confident-execution stv 1.0/0.729
;; Delta: 1.0 frequency swing = full causal responsibility

;; Reusable counterfactual runner
(= (counterfactual-compare $rule $factual-premise $counter-premise)
   (contrast
     (|- $rule $factual-premise)
     (|- $rule $counter-premise)))
