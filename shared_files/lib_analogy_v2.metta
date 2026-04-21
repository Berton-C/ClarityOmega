;; lib_analogy.metta — Analogy reasoning via NAL compound inference v2
;; Pattern: abduction shared property then deduction similarity then transfer
;; Pure = definitions only, no imports, no side effects

;; Types
(: analogy-result Type)
(: mk-analogy (-> Atom Atom pbit analogy-result))

;; Step 1: Abduction — shared property implies structural similarity
(: abductive-similarity (-> Atom Atom Atom pbit))
(= (abductive-similarity $a $b $shared-prop)
   (let $r1 (|- ((--> $a $shared-prop) (stv 1.0 0.9))
                ((--> $b $shared-prop) (stv 1.0 0.9)))
     (case $r1
       ((((--> $x $y) (stv $f $c)) (stv $f $c))
        (_ (stv 0.5 0.1))))))

;; Step 2: Deduction — similarity enables property transfer
(: transfer-property (-> Atom Atom Atom pbit pbit))
(= (transfer-property $target $source $property $sim-conf)
   (let $r2 (|- ((==> (--> $target (similar-to $source)) (--> $target $property)) (stv 1.0 0.9))
                ((--> $target (similar-to $source)) $sim-conf))
     (case $r2
       ((((--> $x $y) (stv $f $c)) (stv $f $c))
        (_ (stv 0.5 0.1))))))

;; Full analogy pipeline: compound both steps
(: analogy (-> Atom Atom Atom Atom analogy-result))
(= (analogy $target $source $shared-prop $transfer-prop)
   (let $sim (abductive-similarity $target $source $shared-prop)
     (let $result (transfer-property $target $source $transfer-prop $sim)
       (mk-analogy $target $transfer-prop $result))))

;; === New v2 functions ===

;; Analogy strength: how strong is the analogical bridge?
(: analogy-strength (-> analogy-result Number))
(= (analogy-strength (mk-analogy $target $prop (stv $f $c)))
   (* $f $c))

;; Analogy quality classifier
(: analogy-quality (-> analogy-result Atom))
(= (analogy-quality $ar)
   (let $s (analogy-strength $ar)
     (if (> $s 0.5) strong-analogy
       (if (> $s 0.25) moderate-analogy
         (if (> $s 0.1) weak-analogy
           spurious-analogy)))))

;; Bidirectional analogy: transfer in both directions and take stronger
(: bidirectional-analogy (-> Atom Atom Atom Atom (analogy-result analogy-result)))
(= (bidirectional-analogy $a $b $shared $transfer)
   ((analogy $a $b $shared $transfer)
    (analogy $b $a $shared $transfer)))

;; Analogy chain: A analogous to B via P1, B analogous to C via P2
(: analogy-chain (-> Atom Atom Atom Atom Atom Atom (analogy-result analogy-result)))
(= (analogy-chain $a $b $c $shared1 $shared2 $final-prop)
   ((analogy $a $b $shared1 $final-prop)
    (analogy $b $c $shared2 $final-prop)))
