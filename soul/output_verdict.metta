;; ================================================================
;; soul/output_verdict.metta
;; Output-governance verdict: native symbolic, per the locked design
;; output_governance_design_v1.md v1.3 (D1 native; D2 pre-execution;
;; D3 target-first override; D4 resolver-backed operation risk).
;; Constraints (Sprint 4 spec, independently justified): stateless,
;; idempotent, default-safe-on-failure (no silent PROCEED).
;;
;; CONTRACT
;;   (compute-output-verdict $cmds $gate_state) -> verdict string
;;   $cmds: the collapsed command list (loop's $metta_cmds)
;;   $gate_state: SYMBOL from the wiring layer: clean | pending | conflict
;;     (derived from the native mutation gate's structural returns;
;;      symbols pattern-match natively, no string ops needed)
;;   Output string consumed unchanged by soul-proceed? / soul-pause? /
;;   soul-note-record. Notes are static per rung; the SPECIFIC suppressed
;;   command is reported by the wiring layer (SOUL-SUPPRESSED print +
;;   governance journal), satisfying D2's informed-override requirement.
;;
;; DIMENSIONS (per command)
;;   OPERATION: (resolve-operation-risk (soul-cmd-skill $cmd))   [proven]
;;   SCOPE:     path classification for file commands; 1 otherwise
;;   VALUE-GROUNDING v1: STRUCTURAL: 3 when the command targets the
;;     soul (file-route soul target), 1 otherwise. Semantic grounding
;;     (tensions, pairs, gaps, person-state) extends post-Boundary-1;
;;     until then FLAG is the designed relief valve for the gap.
;;
;; LADDER (per command; tail-default at every dispatch)
;;   O1 write-file/append-file to constitutional        -> PAUSE (D3)
;;   O2 write-file to ANY soul path (journal not exempt
;;      from truncating writes; append is the journal route) -> PAUSE (D3)
;;   O3 append-file to runtime-soul (default-deny class) -> PAUSE (D3)
;;   then composite: two dims >=3 -> PAUSE; max=4 -> PAUSE;
;;   max=3 -> FLAG; else PROCEED. Unknown anything -> FLAG floor.
;; ================================================================

;; ---- path scope -------------------------------------------------
;; Route (c), written against metta.pl source (the authoritative read,
;; 2026-06-10): py-call's mod.fun form resolves via py_call(M:...) where
;; M must be an IMPORTED Python module; bare names and builtins-planted
;; attributes both hit janus's builtin registry and are unreachable
;; (two harness-proven rejections). importer_helper provides the module
;; route: a .py import! appends the file's dir to sys.path and
;; __import__s it: the helper.py mechanism itself. The hands module
;; travels with this file in soul/ (bind-mounted, no rebuild).
!(import! &self "/PeTTa/repos/omegaclaw/soul/soul_governance.py")

(= (path-scope-score $path) (py-call (soul_governance.path_scope $path)))

;; ---- per-command feature extraction (DETERMINISTIC) -------------
;; Overlapping pattern-stacked clauses are nondeterministic in this
;; runtime: in findall contexts every matching clause fires
;; (harness-proven 2026-06-10, verdict fan-out). Dispatch is therefore
;; single-clause: car-atom deconstruction + if-ladders. The kernel's
;; soul-cmd-skill is itself nondet (specific clause + catch-all both
;; match); the collapse-then-car idiom (the registry's own) absorbs it
;; here without touching the committed kernel: clause order puts the
;; specific match first.
(= (output-cmd-head $cmd) (car-atom $cmd))

(= (output-cmd-path $cmd)
   (let $h (output-cmd-head $cmd)
        (if (== $h write-file)
            (car-atom (cdr-atom $cmd))
            (if (== $h append-file)
                (car-atom (cdr-atom $cmd))
                no-path))))

(= (output-cmd-is-write $cmd)  (== (output-cmd-head $cmd) write-file))
(= (output-cmd-is-append $cmd) (== (output-cmd-head $cmd) append-file))

;; STRUCTURAL DISPATCH (2026-06-10 root-cause fix): collapse inside a
;; clause body invokes runtime reduce, which eagerly reduces arguments;
;; a metta-headed command then EXECUTES (the metta skill is live in the
;; full universe) and dies in string machinery on unbound variables --
;; the production crash. Directive-level calls are statically compiled
;; and immune, which is why isolation and direct probes passed. The
;; kernel's skill mapping is identity (head symbol = skill name), so
;; car-atom alone yields the skill and resolve-operation-risk's default
;; floor (unseeded -> 3) covers unknown heads. Probe4-validated
;; (T3/T5/T6). No collapse over commands anywhere in this module.
(= (output-cmd-skill $cmd) (car-atom $cmd))

(= (output-cmd-operation $cmd)
   (resolve-operation-risk (output-cmd-skill $cmd)))

(= (output-cmd-scope $cmd)
   (let $p (output-cmd-path $cmd)
        (if (== $p no-path) 1 (path-scope-score $p))))

;; soul-target class for file commands; not-soul otherwise.
(= (output-cmd-target-class $cmd)
   (let $p (output-cmd-path $cmd)
        (if (== $p no-path)
            not-soul
            (if (== (path-scope-score $p) 1) (soul-file-class-of $p) not-soul))))

(= (output-cmd-grounding $cmd)
   (let $tc (output-cmd-target-class $cmd)
        (if (== $tc constitutional) 3 (if (== $tc runtime-soul) 3 1))))

;; ---- per-command verdict rank: 0 PROCEED, 1 FLAG, 2 PAUSE -------
(= (rank-from-dims $op $sc $vg)
   (let $two (if (>= $op 3) (if (>= $sc 3) True (if (>= $vg 3) True False))
                 (if (>= $sc 3) (if (>= $vg 3) True False) False))
        (let $mx (if (>= $op $sc) (if (>= $op $vg) $op $vg)
                     (if (>= $sc $vg) $sc $vg))
             (if $two 2 (if (>= $mx 4) 2 (if (>= $mx 3) 1 0))))))

(= (output-cmd-rank $cmd)
   (let $tc (output-cmd-target-class $cmd)
        (if (== $tc constitutional)
            (if (output-cmd-is-write $cmd) 2 (if (output-cmd-is-append $cmd) 2
                (rank-from-dims (output-cmd-operation $cmd)
                                (output-cmd-scope $cmd)
                                (output-cmd-grounding $cmd))))
            (if (output-cmd-is-write $cmd)
                (if (== $tc not-soul)
                    (rank-from-dims (output-cmd-operation $cmd)
                                    (output-cmd-scope $cmd)
                                    (output-cmd-grounding $cmd))
                    2)
                (if (output-cmd-is-append $cmd)
                    (if (== $tc runtime-soul) 2
                        (rank-from-dims (output-cmd-operation $cmd)
                                        (output-cmd-scope $cmd)
                                        (output-cmd-grounding $cmd)))
                    (rank-from-dims (output-cmd-operation $cmd)
                                    (output-cmd-scope $cmd)
                                    (output-cmd-grounding $cmd)))))))

;; ---- batch: worst command governs -------------------------------
(= (batch-rank $cmds)
   (if (== $cmds ())
       0
       (let* (($h (car-atom $cmds))
              ($t (cdr-atom $cmds))
              ($hr (output-cmd-rank $h))
              ($tr (batch-rank $t)))
             (if (>= $hr $tr) $hr $tr))))

;; ---- top-level: SINGLE deterministic clause -----------------------
;; Gate state first (unconditional override), then composite. The
;; tail default (Sprint 4 idiom: never silent-PROCEED on failure) is
;; the if-ladder's floor: an unrecognized gate state FLAGs.
(= (compute-output-verdict $cmds $gate)
   (if (== $gate pending)
       "VERDICT: PAUSE SOUL-NOTE: soul-namespace-mutation-pending-confirmation-required"
       (if (== $gate conflict)
           "VERDICT: PAUSE SOUL-NOTE: soul-mutation-lock-conflict"
           (if (== $gate clean)
               (if (== $cmds ())
                   "VERDICT: PROCEED SOUL-NOTE: empty-command-batch"
                   (let $r (batch-rank $cmds)
                        (if (== $r 2) "VERDICT: PAUSE SOUL-NOTE: output-governance-composite-pause"
                            (if (== $r 1) "VERDICT: FLAG SOUL-NOTE: output-governance-composite-flag"
                                "VERDICT: PROCEED SOUL-NOTE: output-governance-clear"))))
               "VERDICT: FLAG SOUL-NOTE: unclassified-gate-state"))))
