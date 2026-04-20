;; lib_paraconsistent.metta -- ClarityClaw paraconsistent reasoning
;; Type-tightened per Patrick types-as-contracts rule
;; Pure MeTTa, no Python

;; --- Type declarations ---
(: tension-class Type)
(: held-pair Type)
(: mk-held (-> Atom Atom tension-class held-pair))
(: dual-revise (-> Atom Atom Atom))
(: indeterminate? (-> Atom Atom Bool))
(: value-conflict (-> Atom Atom tension-class))
(: suspend (-> Atom Atom held-pair))
(: tension-choice (-> held-pair Atom Atom))

;; --- Dual revision: revise contradictory evidence ---
(= (dual-revise $pos $neg)
   (|- $pos $neg))

;; --- Indeterminacy test ---
(= (indeterminate? (stv $f1 $c1) (stv $f2 $c2))
   (if (and (> $c1 0.5) (> $c2 0.5))
     (if (> (- $f1 $f2) 0.3) True False)
     False))

;; --- Value conflict classifier ---
(= (value-conflict (stv $f1 $c1) (stv $f2 $c2))
   (if (and (> $f1 0.7) (> $f2 0.7))
     (mk-held (stv $f1 $c1) (stv $f2 $c2) high-tension)
     (if (and (> $f1 0.4) (> $f2 0.4))
       (mk-held (stv $f1 $c1) (stv $f2 $c2) moderate-tension)
       (mk-held (stv $f1 $c1) (stv $f2 $c2) low-tension))))

;; --- Suspend judgment: hold both without collapsing ---
(= (suspend $a $b)
   (mk-held $a $b unresolved))

;; --- Tension choice: pick from held pair by threshold ---
(= (tension-choice (mk-held $a $b $t) (stv $ft $ct))
   (if (> $ft 0.5) $a $b))
