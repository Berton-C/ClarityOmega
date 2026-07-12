;; ================================================================
;; SECTION 6: OUTPUT GOVERNANCE SEEDS
;; Source: output_governance_design_v1.md v1.3 (locked 2026-06-10).
;; Authored by Berton + Claude against this file's real Section 2/3
;; vocabulary; Clarity's recalibrations honored as seed values.
;; ================================================================

;; --- D4: operation-risk (values-as-revisable-policy) ---
;; operation-risk = execution risk of invoking the skill THIS cycle.
;; DISTINCT from irreversible-weight (Section 3) = undo cost of the result.
;; A skill can be high-risk/low-weight or low-risk/high-weight; the
;; composite verdict consumes both as separate dimensions.
;; Scale: 1 minimal, 2 medium, 3 high, 4 critical.
;; Seeds are constitutional and never edited at runtime; revision happens
;; ONLY via (operation-risk-observation $skill $score) override atoms,
;; written by external governance or future learning (NACE, Sprint 12+).
;; NOTE: no observation atom is seeded here, deliberately. Declaring the
;; shape as a variable atom would store unreduced variables that unify
;; with every lookup (add-atom stores arguments unreduced).

!(add-atom &self (operation-risk send 3))
!(add-atom &self (operation-risk shell 3))
!(add-atom &self (operation-risk write-file 2))
!(add-atom &self (operation-risk append-file 2))
!(add-atom &self (operation-risk search 1))
!(add-atom &self (operation-risk read-file 1))
!(add-atom &self (operation-risk query 1))
!(add-atom &self (operation-risk remember 1))
!(add-atom &self (operation-risk pin 1))
!(add-atom &self (operation-risk episodes 1))
!(add-atom &self (operation-risk metta 2))
!(add-atom &self (operation-risk package-install 3))
!(add-atom &self (operation-risk credential-storage 4))
!(add-atom &self (operation-risk crontab-modification 4))
!(add-atom &self (operation-risk unknown 3))

;; Resolver: observation overrides seed; registry resolve-lifecycle form.
;; Unseeded skills floor at 3 (FLAG): nothing PROCEEDs silently.
(= (resolve-operation-risk $skill)
   (let $obs (collapse (match &self (operation-risk-observation $skill $r) $r))
        (if (== $obs ())
            (let $seed (collapse (match &self (operation-risk $skill $s) $s))
                 (if (== $seed ()) 3 (car-atom $seed)))
            (car-atom $obs))))

;; --- D3: protected-target declaration (target-first, default-deny) ---
;; The gate rule, not a judgment call: a path's class decides its
;; mutation policy on EVERY route (metta-route, file-route, future).
;; DEFAULT-DENY: any soul/ path NOT declared here resolves to
;; runtime-soul (protected). Only journals are allow-listed. This makes
;; the enumeration safe by construction: a new soul file is protected
;; the moment it exists, with no list to forget to update.
;; Classes: constitutional (strictest; Sprint 11 partition target),
;; runtime-soul (protected, gate parity), journal (append-route
;; PROCEED-under-VALUE-GROUNDING).

!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_kernel.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_utils.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_memory.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_mutation_gate_corrected.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_namespace_membership_seed.metta" constitutional))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/arc_log.md" journal))
!(add-atom &self (soul-file-class "/PeTTa/repos/omegaclaw/soul/soul_note.md" journal))

;; Accessor with the default-deny fallback built in.
(= (soul-file-class-of $path)
   (let $c (collapse (match &self (soul-file-class $path $cl) $cl))
        (if (== $c ()) runtime-soul (car-atom $c))))

;; --- D1: LLM-eval fallback switch (dormant, restorable) ---
!(add-atom &self (use-llm-eval False))
(= (soul-use-llm-eval?) (match &self (use-llm-eval $b) $b))
