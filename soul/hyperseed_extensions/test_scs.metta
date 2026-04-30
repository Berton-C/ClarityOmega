!(import! &self lib_quantale)

;; Test 1: q-meet on bare pbits
!(q-meet (mk-pbit 0.6 0.8) (mk-pbit 0.9 0.7))

;; Test 2: q-mul on bare pbits
!(q-mul (mk-pbit 0.8 0.9) (mk-pbit 0.7 0.85))

;; Test 3: q-geq
!(q-geq (mk-pbit 0.8 0.9) (mk-pbit 0.6 0.7))

;; Test 4: q-residuate
!(q-residuate (mk-pbit 0.8 0.9) (mk-pbit 0.6 0.8))

;; Test 5: edge-weight lookup
!(edge-weight (Cons (edge node-a node-b (mk-pbit 0.8 0.9)) Nil) node-a node-b)

;; Test 6: full SCS on tiny 2-node network
!(self-continuity-score
  (pfn (Cons node-a (Cons node-b Nil))
       (Cons (edge node-a node-b (mk-pbit 0.8 0.9)) Nil))
  (pfn (Cons node-a (Cons node-b Nil))
       (Cons (edge node-a node-b (mk-pbit 0.7 0.85)) Nil)))
