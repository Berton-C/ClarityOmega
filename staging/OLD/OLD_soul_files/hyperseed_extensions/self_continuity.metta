;; Self-Continuity Substrate -- Section 16.3 Operational Implementation
;; Hyperseed uses tensor product notation (otimes) for composition.
;; In lib_quantale this is q-mul. We use q-mul throughout.
;; q-mul implements: (mk-pbit (* s1 s2) (min c1 c2))
;;
;; Design decision: SCS is defined as the degree of the IDENTITY map
;; between successive pattern-flow network snapshots. Rationale:
;; Component 2h asks "did my patterns persist as themselves" not
;; "what is the optimal renaming." The identity map is always a valid
;; lower bound on the canonical join-over-all-maps SCS (Def 218),
;; and it is what 2h actually needs. This eliminates map enumeration.

;; === Helper: q-geq (componentwise comparison on pbits) ===
(= (q-geq (mk-pbit $s1 $c1) (mk-pbit $s2 $c2))
   (if (>= $s1 $s2) (if (>= $c1 $c2) True False) False))

;; === Helper: first-of and last-of for interval lists ===
(= (first-of (Cons $x $rest)) $x)
(= (last-of (Cons $x Nil)) $x)
(= (last-of (Cons $x $rest)) (last-of $rest))

;; === Pattern-Flow Network representation ===
;; A pfn is: (pfn node-list edge-list)
;; An edge is: (edge source target weight) where weight is mk-pbit
;; A node-list is: (Cons node-a (Cons node-b ... Nil))

;; === Definition 216: deg-map (canonical form) ===
;; Degree of a map f between structures P1 P2 is the meet over all
;; edges (a,b) in P1 of the residuation: edge-weight-in-P2(f(a),f(b))
;; residuated by edge-weight-in-P1(a,b).
;; For identity map: f(a)=a, f(b)=b, so we compare matching edges.

;; Lookup edge weight in a pfn
(= (edge-weight Nil $s $t) (mk-pbit 0.0 1.0))
(= (edge-weight (Cons (edge $s $t $w) $rest) $s $t) $w)
(= (edge-weight (Cons (edge $x $y $w) $rest) $s $t)
   (if (== ($x $y) ($s $t)) $w (edge-weight $rest $s $t)))

;; Residuation: a residuated by b = a / b (in pbit: strength ratio, min confidence)
(= (q-residuate (mk-pbit $sa $ca) (mk-pbit $sb $cb))
   (if (> $sb 0.0)
       (mk-pbit (min 1.0 (/ $sa $sb)) (min $ca $cb))
       (mk-pbit 1.0 (min $ca $cb))))

;; deg-map over identity: meet over all edges of residuation
(= (deg-map-edges Nil $edges2) (mk-pbit 1.0 1.0))
(= (deg-map-edges (Cons (edge $s $t $w1) $rest) $edges2)
   (q-meet (q-residuate (edge-weight $edges2 $s $t) $w1)
           (deg-map-edges $rest $edges2)))

;; Definition 216 top-level
(= (deg-map (pfn $nodes1 $edges1) (pfn $nodes2 $edges2))
   (deg-map-edges $edges1 $edges2))

;; === Definition 217: theta-self-continuous ===
(= (theta-self-continuous $pfn1 $pfn2 $theta)
   (q-geq (self-continuity-score $pfn1 $pfn2) $theta))

;; === Definition 218: self-continuity-score (identity map form) ===
(= (self-continuity-score $pfn1 $pfn2)
   (deg-map $pfn1 $pfn2))

;; === Theorem 14: chain-continuity-bound ===
;; For a chain of intervals, SCS composes via q-mul
(= (chain-continuity-bound (Cons $i Nil)) (mk-pbit 1.0 1.0))
(= (chain-continuity-bound (Cons (interval $pfn1 $pfn2) Nil))
   (self-continuity-score $pfn1 $pfn2))
(= (chain-continuity-bound (Cons (interval $pfn1 $pfn2) $rest))
   (q-mul (self-continuity-score $pfn1 $pfn2)
          (chain-continuity-bound $rest)))

;; === Corollary 2: continuity-held-across ===
(= (continuity-held-across $intervals $theta)
   (q-geq (chain-continuity-bound $intervals) $theta))
