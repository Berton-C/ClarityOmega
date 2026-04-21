;; lib_induction.metta — Inductive reasoning via NAL v2
;; Pattern: observe instances sharing subject, generalize, revise to strengthen
;; Pure = definitions only, no imports, no side effects

;; Types
(: induction-result Type)
(: mk-induction (-> Atom Atom pbit induction-result))
(: induction-quality Type)

;; Step 1: Inductive generalization from shared subject
;; Given (-> S M) and (-> S P), infer (-> M P) at low confidence
(: inductive-generalize (-> Atom Atom Atom pbit))
(= (inductive-generalize $subject $prop-m $prop-p)
   (let $r (|- ((--> $subject $prop-m) (stv 1.0 0.9))
               ((--> $subject $prop-p) (stv 1.0 0.9)))
     (case $r
       ((((--> $x $y) (stv $f $c)) (stv $f $c))
        (_ (stv 0.5 0.1))))))

;; Step 2: Evidence accumulation via revision
(: accumulate-evidence (-> pbit pbit pbit))
(= (accumulate-evidence $ev1 $ev2)
   (let $r (|- ((--> induction-target induction-property) $ev1)
               ((--> induction-target induction-property) $ev2))
     (case $r
       ((((--> $x $y) (stv $f $c)) (stv $f $c))
        (_ (stv 0.5 0.1))))))

;; Full pipeline: two instances generalized then revised
(: induction-pipeline (-> Atom Atom Atom Atom Atom induction-result))
(= (induction-pipeline $subj1 $subj2 $shared-cat $target-prop $label)
   (let $g1 (inductive-generalize $subj1 $shared-cat $target-prop)
     (let $g2 (inductive-generalize $subj2 $shared-cat $target-prop)
       (let $merged (accumulate-evidence $g1 $g2)
         (mk-induction $label $target-prop $merged)))))

;; === New v2 functions ===

;; Induction strength scorer
(: induction-strength (-> induction-result Number))
(= (induction-strength (mk-induction $label $prop (stv $f $c)))
   (* $f $c))

;; Quality classifier for inductive conclusions
(: classify-induction (-> induction-result induction-quality))
(= (classify-induction $ir)
   (let $s (induction-strength $ir)
     (if (> $s 0.5) robust-induction
       (if (> $s 0.3) moderate-induction
         (if (> $s 0.15) tentative-induction
           insufficient-evidence)))))

;; Three-instance pipeline: stronger generalization from three observations
(: induction-pipeline-3 (-> Atom Atom Atom Atom Atom Atom induction-result))
(= (induction-pipeline-3 $s1 $s2 $s3 $shared $target $label)
   (let $g1 (inductive-generalize $s1 $shared $target)
     (let $g2 (inductive-generalize $s2 $shared $target)
       (let $m12 (accumulate-evidence $g1 $g2)
         (let $g3 (inductive-generalize $s3 $shared $target)
           (let $final (accumulate-evidence $m12 $g3)
             (mk-induction $label $target $final)))))))

;; Confidence floor filter: only pass inductions above threshold
(: induction-filter (-> induction-result Number induction-result))
(= (induction-filter (mk-induction $l $p (stv $f $c)) $min-conf)
   (if (> $c $min-conf)
     (mk-induction $l $p (stv $f $c))
     (mk-induction $l $p (stv 0.0 0.0))))
