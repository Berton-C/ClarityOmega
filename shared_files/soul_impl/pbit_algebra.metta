;; P-Bit Algebra for Hyperseed v7 - Clarity Implementation
;; A p-bit is a paraconsistent truth value: (stv strength confidence)
;; where strength in [0,1] and confidence in [0,1]
;; This extends NAL truth values with quantale composition

;; === Core Type ===
(: pbit Type)
(: mk-pbit (-> Number Number pbit))

;; === Quantale Multiplication (sequential composition) ===
;; (s1*s2, min(c1,c2)) - strength multiplies, confidence takes minimum
(: q-mul (-> pbit pbit pbit))
(= (q-mul (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (* $s1 $s2) (min $c1 $c2)))

;; === Quantale Join (parallel composition / disjunction) ===
(: q-join (-> pbit pbit pbit))
(= (q-join (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (max $s1 $s2) (min $c1 $c2)))

;; === Quantale Meet (conjunction) ===
(: q-meet (-> pbit pbit pbit))
(= (q-meet (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (mk-pbit (min $s1 $s2) (min $c1 $c2)))

;; === Negation (paraconsistent - flips strength, keeps confidence) ===
(: q-neg (-> pbit pbit))
(= (q-neg (mk-pbit $s $c))
   (mk-pbit (- 1.0 $s) $c))

;; === Evidence Revision (NAL-compatible) ===
;; Merges two independent evidence streams for same claim
(: q-revise (-> pbit pbit pbit))

;; === Bridge to NAL stv ===
(: pbit-to-stv (-> pbit Atom))
(= (pbit-to-stv (mk-pbit $s $c)) (stv $s $c))

;; === Unit elements ===
(: q-top pbit)
(= q-top (mk-pbit 1.0 1.0))
(: q-bot pbit)
(= q-bot (mk-pbit 0.0 1.0))
(: q-unknown pbit)
(= q-unknown (mk-pbit 0.5 0.0))