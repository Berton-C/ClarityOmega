;; soul_namespace_discovery_harness.metta  (v2, inline-tagged results)
;; Each tested expression is wrapped so its VALUE prints WITH its tag in one
;; atom: (RESULT-N <value>). The trailing result block then shows e.g.
;; (RESULT-5 1), tag and value together, position-independent and immune to the
;; println/add-atom acks that polluted v1. The parser extracts (RESULT-N ...).
;;
;; Setup (seed the registry for Candidate 2). These emit acks but carry no
;; RESULT- tag, so the parser ignores them.
!(add-atom &self (soul-namespace-head soul-note))
!(add-atom &self (soul-namespace-head priority))
!(add-atom &self (soul-namespace-head tension))

;; ===== PRIMITIVE DISCOVERY (decides Candidate 1) =====
;; If a primitive does not exist, the wrapped value is the unreduced call, so
;; the result shows (RESULT-1 (symbol-to-chars soul-note)) = ABSENT. If it
;; exists, the value is whatever it returned.
!(RESULT-1 (symbol-to-chars soul-note))
!(RESULT-2 (chars soul-note))
!(RESULT-3 (decons-atom soul-note))
!(RESULT-4 (repr soul-note))

;; ===== CANDIDATE 2: REGISTRY STRUCTURAL MATCH (proven idiom) =====
!(RESULT-5 (size-atom (collapse (match &self (soul-namespace-head soul-note) soul-note))))
!(RESULT-6 (size-atom (collapse (match &self (soul-namespace-head regular-atom) regular-atom))))
!(RESULT-7 (if (> (size-atom (collapse (match &self (soul-namespace-head soul-note) soul-note))) 0) True False))
!(RESULT-8 (if (> (size-atom (collapse (match &self (soul-namespace-head regular-atom) regular-atom))) 0) True False))

;; ===== TARGET HEAD EXTRACTION (shared helper) =====
!(RESULT-9 (car-atom (car-atom (cdr-atom (cdr-atom (quote (add-atom &self (soul-note x))))))))

;; ===== FULL CHAIN (registry candidate end to end) =====
!(RESULT-10 (let $h (car-atom (car-atom (cdr-atom (cdr-atom (quote (add-atom &self (soul-note x)))))))
   (if (> (size-atom (collapse (match &self (soul-namespace-head $h) $h))) 0) True False)))
!(RESULT-11 (let $h (car-atom (car-atom (cdr-atom (cdr-atom (quote (add-atom &self (regular-atom x)))))))
   (if (> (size-atom (collapse (match &self (soul-namespace-head $h) $h))) 0) True False)))
