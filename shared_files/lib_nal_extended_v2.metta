;; lib_nal_extended.metta -- ClarityClaw Reasoning Extensions v2
;; Extends Patrick lib_nal without touching it
;; Pure = definitions only, no imports, no side effects

;; === Empirically Verified Truth Functions ===

;; Deduction confidence: c1*c2*f1*f2
(: nal-deduction-conf (-> Number Number Number Number Number))
(= (nal-deduction-conf $f1 $c1 $f2 $c2)
   (* (* $c1 $c2) (* $f1 $f2)))

;; Abduction confidence: f_other*c1*c2 / (1 + f_other*c1*c2)
(: nal-abduction-conf (-> Number Number Number Number))
(= (nal-abduction-conf $f-other $c1 $c2)
   (let $num (* $f-other (* $c1 $c2))
     (/ $num (+ 1.0 $num))))

;; Induction confidence: f_same*c1*c2 / (1 + f_same*c1*c2)
(: nal-induction-conf (-> Number Number Number Number))
(= (nal-induction-conf $f-same $c1 $c2)
   (let $num (* $f-same (* $c1 $c2))
     (/ $num (+ 1.0 $num))))

;; Expectation: (c * (f - 0.5)) + 0.5
(: nal-expectation (-> Number Number Number))
(= (nal-expectation $f $c)
   (+ 0.5 (* $c (- $f 0.5))))

;; === Compound Inference Wrappers ===

(: analogy-abduct (-> Atom Atom Atom Atom))
(= (analogy-abduct $A $B $C)
   (|- ((--> $A $B) (stv 1.0 0.9))
       ((--> $C $B) (stv 1.0 0.9))))

(: induction-step (-> Atom Atom Atom))
(= (induction-step $P1 $P2)
   (|- $P1 $P2))

(: revise-evidence (-> Atom Atom Atom))
(= (revise-evidence $E1 $E2)
   (|- $E1 $E2))

(: temporal-enable (-> Atom Atom Atom))
(= (temporal-enable $pre $post)
   (|- $pre ((--> $post completed) (stv 1.0 0.9))))

(: agent-belief-chain (-> Atom Atom Atom))
(= (agent-belief-chain $belief $rule)
   (|- $belief $rule))
