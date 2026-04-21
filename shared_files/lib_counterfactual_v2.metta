;; lib_counterfactual.metta — Counterfactual reasoning v2
;; Causal analysis via negation and substitution
;; Pure = definitions only, no imports, no side effects

;; Types
(: counterfactual-result Type)
(: mk-cf-result (-> Atom Atom Atom counterfactual-result))
(: cf-quality Type)

;; Method 1: Negation — set antecedent to stv 0.0 high-conf
;; If conclusion collapses to 0.0/0.0 epistemic vacuum, antecedent is causally necessary
(: causal-necessity-test (-> Atom Atom counterfactual-result))
(= (causal-necessity-test $rule $premise)
   (mk-cf-result negation $premise (|- $rule (stv 0.0 0.9))))

;; Method 2: Substitution — swap alternative premise at stv 1.0
;; Contrast between factual and counterfactual outputs reveals causal contribution
(: what-if (-> Atom Atom Atom counterfactual-result))
(= (what-if $rule $factual $alternative)
   (mk-cf-result substitution
     (|- $rule $factual)
     (|- $rule $alternative)))

;; Causal responsibility: frequency delta between factual and counterfactual
(: causal-delta (-> counterfactual-result Atom))
(= (causal-delta (mk-cf-result substitution $factual-out $counter-out))
   (contrast $factual-out $counter-out))

;; Protocol runner: full counterfactual analysis in one call
(: counterfactual-analysis (-> Atom Atom Atom counterfactual-result))
(= (counterfactual-analysis $rule $factual $alternative)
   (mk-cf-result full
     (causal-necessity-test $rule $factual)
     (what-if $rule $factual $alternative)))

;; === New v2 functions ===

;; Counterfactual strength: extract numeric magnitude from cf-result
(: cf-strength (-> counterfactual-result Number))
(= (cf-strength (mk-cf-result $method $a (stv $f $c))) (* $f $c))
(= (cf-strength (mk-cf-result $method $a $b)) 0.0)

;; Quality classifier for counterfactual conclusions
(: classify-cf (-> Number cf-quality))
(= (classify-cf $delta)
   (if (> $delta 0.6) strong-causal-link
     (if (> $delta 0.3) moderate-causal-link
       (if (> $delta 0.1) weak-causal-link
         no-causal-link))))

;; Sufficiency test: does premise alone produce the conclusion?
;; High output with premise present = sufficient cause
(: causal-sufficiency-test (-> Atom Atom counterfactual-result))
(= (causal-sufficiency-test $rule $premise)
   (mk-cf-result sufficiency $premise (|- $rule (stv 1.0 0.9))))

;; Combined necessity-sufficiency diagnostic
(: causal-diagnostic (-> Atom Atom counterfactual-result counterfactual-result))
(= (causal-diagnostic $rule $premise)
   ((causal-necessity-test $rule $premise)
    (causal-sufficiency-test $rule $premise)))

;; Multi-factor: test causal contribution of two premises independently
(: multi-factor-cf (-> Atom Atom Atom (counterfactual-result counterfactual-result)))
(= (multi-factor-cf $rule $premise1 $premise2)
   ((causal-necessity-test $rule $premise1)
    (causal-necessity-test $rule $premise2)))
