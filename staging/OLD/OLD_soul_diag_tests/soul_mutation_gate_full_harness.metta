;; soul_mutation_gate_full_harness.metta
;; End-to-end proof of the COMPLETE assembled gate: all four functions plus the
;; membership seed, run together against a realistic atomspace. Inline-tagged
;; results (RESULT-N value), proven pattern. This is the whole-gate proof: if it
;; is all-green, the gate is ready to wire into Repair 1.
;;
;; Loaded AFTER soul_mutation_gate_corrected.metta and
;; soul_namespace_membership_seed.metta (the diagnostic concatenates them).

;; ----- realistic mixed atomspace (non-soul neighbors that must NOT be flagged) -----
!(add-atom &self (task-state 3 pending))
!(add-atom &self (recent-action 7 responsive-send hello))
!(add-atom &self (idle-pattern 2 resting))

;; ===== FUNCTION 1: soul-is-metta-cmd? =====
!(RESULT-1 (soul-is-metta-cmd? (metta "(add-atom &self (soul-note x))")))
!(RESULT-2 (soul-is-metta-cmd? (some-other-cmd "x")))
;; C11 regression guard: a deeply nested complex atom must not crash, must be False
!(RESULT-3 (soul-is-metta-cmd? (deeply (nested (complex (atom (with (many (levels))))))))) 

;; ===== FUNCTION 2: soul-extract-metta-arg =====
;; Command arrives UNEVALUATED: quote at the call site (proven form B,
;; 2026-06-08-184234) so the inner add-atom is data, not executed. This mirrors
;; the production wiring contract: the gate receives the metta() expression
;; quoted/unevaluated.
!(RESULT-4 (soul-extract-metta-arg (quote (metta (add-atom &self (soul-note x))))))

;; ===== FUNCTION 3: namespace targeting (full path: extract head, check member) =====
;; Command arrives UNEVALUATED: quote at the call site (proven form E). The gate
;; inspects the expression; it does NOT execute the mutation.
;; soul target (soul-note is seeded) -> True
!(RESULT-5 (soul-metta-targets-soul-namespace? (quote (add-atom &self (soul-note x)))))
;; soul FUNCTION head (soul-pause is seeded) -> True (redefining a soul fn is gated)
!(RESULT-6 (soul-metta-targets-soul-namespace? (quote (add-atom &self (soul-pause x)))))
;; non-soul target that EXISTS in atomspace (task-state) -> False (not a member)
!(RESULT-7 (soul-metta-targets-soul-namespace? (quote (add-atom &self (task-state x)))))
;; non-soul target that does not exist (regular-atom) -> False
!(RESULT-8 (soul-metta-targets-soul-namespace? (quote (add-atom &self (regular-atom x)))))

;; ===== FUNCTION 4: soul-mutation-pending? (structural atom-lock) =====
;; lock clear (unlocked) -> False
!(RESULT-9 (soul-mutation-pending?))
;; set the lock held, then pending -> True
!(change-state! &soul_mutation_lock (locked soul-note))
!(RESULT-10 (soul-mutation-pending?))
;; reclear the lock, pending -> False again
!(change-state! &soul_mutation_lock unlocked)
!(RESULT-11 (soul-mutation-pending?))

;; ===== FUNCTION 3 via tag-at-construction (novel head, no seed) =====
;; construct a brand-new soul head, then it IS a member (constructor tagged it)
!(soul-ns-construct soul-freshly-constructed "z")
!(RESULT-12 (soul-head-is-member? soul-freshly-constructed))
