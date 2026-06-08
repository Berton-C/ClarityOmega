;; soul_mutation_gate_corrected.metta  -- ASSEMBLED 2026-06-08
;; The soul self-modification safety interlock, fully native, all four functions
;; proven by harness (proof logs 2026-06-08). Detection is structural; no string
;; ops anywhere (string-contains is globally broken in this runtime).
;;
;; PURPOSE. Clarity can self-modify her soul via the metta() skill at runtime
;; (add-atom &self ...). That is irreversible. This gate detects a proposed soul
;; mutation BEFORE it executes, so the output eval can force PAUSE and Channel D
;; can surface it for user confirmation.
;;
;; PROVENANCE of each function (all harness-proven, see proof logs):
;;   soul-is-metta-cmd?  : car-atom + quote. metta evaluates as a special form,
;;                         so the command must be quoted before car-atom.
;;                         (Clarity Arc-017 REPL + discovery harness.)
;;   soul-extract-metta-arg : structural pattern; fallback car/cdr+quote form.
;;   soul-metta-targets-soul-namespace? : tag-membership match (S1). Proven to
;;                         discriminate soul heads from non-soul heads by TAG,
;;                         not by arity (over-match log 2026-06-08-145300).
;;                         Requires the membership seed (soul_namespace_membership_seed.metta)
;;                         for atoms that already exist, and soul-ns-construct
;;                         tags future ones.
;;   soul-mutation-pending? : length check on the lock string. == against "" is
;;                         unreliable for non-empty (Clarity Arc-017 correction),
;;                         so use string_length > 0.
;;
;; WIRING CONTRACT (proven 2026-06-08-184234): the gate functions inspect the
;; metta() command as DATA. The command MUST arrive UNEVALUATED (quoted) at the
;; call site, e.g. (soul-metta-targets-soul-namespace? (quote (add-atom &self
;; (soul-note x)))). If passed unquoted, the inner add-atom EXECUTES and the gate
;; inspects the result instead of the command. Repair 1 wiring must pass the
;; proposed mutation expression quoted/unevaluated.
;;
;; PeTTa constraints: C12-safe (no match inside if), ASCII-safe, no string ops.

;; ----------------------------------------------------------------
;; 1. Is this command a metta() self-modification call?
;; ----------------------------------------------------------------
(= (soul-is-metta-cmd? $cmd)
   (== (car-atom (quote $cmd)) metta))

;; Any metta command in a list of commands?
(= (soul-any-metta? $cmds)
   (any (collapse (let $c (superpose $cmds) (soul-is-metta-cmd? $c)))))

;; ----------------------------------------------------------------
;; 2. Extract the inner command from (metta <arg>)
;; ----------------------------------------------------------------
(= (soul-extract-metta-arg (metta $arg)) $arg)
;; Structural fallback (verified) if the metta keyword is consumed first:
;; (= (soul-extract-metta-arg $cmd) (car-atom (cdr-atom (quote $cmd))))

;; ----------------------------------------------------------------
;; 3. Does the metta arg target the soul namespace?
;;    arg shape: (add-atom &self (HEAD ...)). The soul-namespace identity is the
;;    HEAD symbol of the third element. Extract it structurally, then check
;;    membership by tag (proven safe: discriminates by tag, not arity).
;; ----------------------------------------------------------------
(= (soul-target-head $arg)
   (car-atom (car-atom (cdr-atom (cdr-atom (quote $arg))))))

;; Tag-at-construction constructor: any soul-namespace atom added through this
;; is tagged in the same operation, so future heads are members by construction.
(= (soul-ns-construct $head $body)
   (let $tagged (add-atom &self (soul-ns-member $head))
      (add-atom &self (soul-instance $head $body))))

;; Membership detection (the proven S1 mechanism).
(= (soul-head-is-member? $head)
   (if (> (size-atom (collapse (match &self (soul-ns-member $head) $head))) 0)
       True False))

;; Composed namespace check.
(= (soul-metta-targets-soul-namespace? $arg)
   (soul-head-is-member? (soul-target-head $arg)))

;; OPEN REFINEMENT (documented for Clarity, NOT yet implemented): a mutation
;; proposing a brand-new soul- head that is NOT tagged (never seeded, never
;; constructed) returns False here = "not a soul mutation" = passes. For a
;; safety interlock the conservative bias is to PAUSE HARDEST on an unrecognized
;; soul-looking target. A conservative fallback belongs here once Clarity
;; decides its shape. The membership match is the proven core; the fallback is
;; the refinement.

;; ----------------------------------------------------------------
;; 4. Is a soul mutation already pending (lock held)?
;;    STRUCTURAL atom-lock (proven 2026-06-08-183320, all 8 green): the lock
;;    holds an ATOM, not a string. Clear = the symbol `unlocked`; held =
;;    (locked <arg>). pending? = NOT (== state unlocked). No string ops.
;;    (The earlier string_length form is DEAD: string_length does not reduce in
;;    this runtime, it errors `character expected, found string_length`.)
;; ----------------------------------------------------------------
(= (soul-mutation-pending?)
   (if (== (get-state &soul_mutation_lock) unlocked) False True))

;; Lock writers (the gate / Repair 1 native block use these forms):
;;   clear: (change-state! &soul_mutation_lock unlocked)
;;   hold:  (change-state! &soul_mutation_lock (locked <arg>))
