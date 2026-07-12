;; soul_namespace_structural_harness.metta
;; Tests whether soul-namespace membership can be detected STRUCTURALLY with no
;; string ops and no false-negative enumeration gap. Inline-tagged results
;; (RESULT-N value) per the proven pattern.
;;
;; THE REFRAME: do not test the soul- prefix lexically (no string ops exist).
;; Instead, a single constructor adds a soul-namespace atom AND tags its
;; membership in one operation, so a NOVEL head is tagged the moment it is
;; constructed. Membership is guaranteed by construction, closing the registry's
;; first-occurrence gap. Candidates below test whether this composes natively.

;; ================================================================
;; CANDIDATE S1: tag-at-construction constructor
;; A constructor that, given a target atom, both performs the add AND records
;; the membership tag. Detection then matches the tag. The novelty gap closes
;; because you cannot construct a soul-namespace atom WITHOUT tagging it.
;; ================================================================
;; The constructor (returns the add result, side-effect tags membership):
(= (soul-ns-construct $head $body)
   (let $tagged (add-atom &self (soul-ns-member $head))
      (add-atom &self (soul-instance $head $body))))

;; Detection: is this head a tagged soul-namespace member?
(= (soul-head-is-member? $head)
   (if (> (size-atom (collapse (match &self (soul-ns-member $head) $head))) 0)
       True False))

;; ----- TEST S1: construct two soul atoms, a novel one, then detect -----
;; Construct a known and a NOVEL head (one never enumerated anywhere).
!(soul-ns-construct soul-note "x")
!(soul-ns-construct soul-brand-new-never-seen "y")

!(RESULT-1 (soul-head-is-member? soul-note))
!(RESULT-2 (soul-head-is-member? soul-brand-new-never-seen))
!(RESULT-3 (soul-head-is-member? regular-atom))

;; ================================================================
;; CANDIDATE S2: detect via the atomspace itself (no separate tag)
;; Hypothesis: if soul-namespace atoms are added to &self, then a head "is a
;; soul-namespace head" iff &self already contains an atom whose head is that
;; symbol. Test whether we can match "any atom with head $h" structurally.
;; This needs NO registry and NO tag if it works: membership = "exists in &self".
;; ================================================================
;; Seed some real soul atoms as they would exist:
!(add-atom &self (soul-pattern-x compass))
!(add-atom &self (soul-priority-hierarchy core))

;; Can we match an atom by its head symbol with a variable body?
!(RESULT-4 (size-atom (collapse (match &self (soul-pattern-x $b) $b))))
!(RESULT-5 (size-atom (collapse (match &self (soul-priority-hierarchy $b) $b))))
;; And a non-existent head -> 0:
!(RESULT-6 (size-atom (collapse (match &self (nonexistent-head-zzz $b) $b))))

;; ================================================================
;; CANDIDATE S3: does the reader split a hyphenated symbol at all?
;; Last check on the narrow direction: any native op exposing symbol structure.
;; ================================================================
!(RESULT-7 (decons-atom (soul-note)))
!(RESULT-8 (get-type soul-note))

;; ----- target-head extraction (proven) reused for the full chain -----
!(RESULT-9 (car-atom (car-atom (cdr-atom (cdr-atom (quote (add-atom &self (soul-note x))))))))

;; ----- FULL CHAIN S1: extract head, then membership check (tag-at-construction) -----
!(RESULT-10 (let $h (car-atom (car-atom (cdr-atom (cdr-atom (quote (add-atom &self (soul-note x)))))))
   (soul-head-is-member? $h)))
!(RESULT-11 (let $h (car-atom (car-atom (cdr-atom (cdr-atom (quote (add-atom &self (regular-atom x)))))))
   (soul-head-is-member? $h)))
