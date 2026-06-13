;; soul_mutation_lock.metta -- Surface C: the soul-mutation lock state machine.
;; Registered in lib_clarity_reasoning. All Surface C logic lives HERE; loop.metta
;; carries only named hooks (artifact_0 Discipline 1+2). Governs the `metta`
;; self-mutation channel ONLY (not shell/network/delete -- that is Surface E).
;;
;; ================================ SEAM 2 SHAPE CONTRACT ========================
;; &soul_mutation_lock is a QUERYABLE STATE ATOM read structurally by Coda's
;; dispatch-guard once Boundary 1 lands. Its shape is a CONTRACT -- a mismatch
;; breaks every Coda consumer on day one. The three shapes, fixed:
;;   unlocked                                  ;; symbol
;;   (locked   <op> <head> <fp>)               ;; list, arity 4
;;   (approved <op> <head> <fp> <stamp>)       ;; list, arity 5 (stamp=cycle k)
;; Field order and the symbol-vs-list distinction are part of the contract.
;; car-atom-or-self guards the symbol case (car-atom on `unlocked` = F25 silent
;; failure; the guard intercepts BEFORE car-atom runs).
;;
;; STATE MACHINE -- `approved` has THREE exits, all FULL RESETS (clear lock AND
;; &pending_soul_mutation AND emit a decision record); no exit strands state:
;;   unlocked --[soul mutation detected]----------------> (locked ...)   PENDING
;;   (locked) --[authz SOUL-MUTATION-APPROVED <fp>]-----> (approved ...)  APPROVED
;;   (locked) --[authz SOUL-MUTATION-DENIED]------------> unlocked        DENIED
;;   (approved)--[re-emission op+head match, executed]--> unlocked        COMMIT
;;   (approved)--[stale-cycles elapsed, no commit]------> unlocked        STALE
;;   (approved)--[execution error]----------------------> unlocked        ERROR
;; PRIORITY: STALE takes precedence over COMMIT in the same cycle (stale-check
;; hook runs BEFORE commit-clear; a too-late commit re-enters fresh). DENY wins
;; if both tokens present (enforced in soul_governance.approval_scan).
;;
;; SEAM 1 (record) and SEAM 3 (approval plumbing) live in soul_governance.py.
;; The `sender` field is recorded for AUDIT but D's learning MUST EXCLUDE it
;; (sender-agnostic learning; sender-aware would train authority-theater).
;; ============================================================================

;; ---- lock shape accessors (var-headed, F20-safe) ----
(= (car-atom-or-self $x) (if (== $x unlocked) unlocked (car-atom $x)))
(= (lock-op    $lock) (car-atom (cdr-atom $lock)))
(= (lock-head  $lock) (car-atom (cdr-atom (cdr-atom $lock))))
(= (lock-fp    $lock) (car-atom (cdr-atom (cdr-atom (cdr-atom $lock)))))
(= (lock-stamp $lock) (car-atom (cdr-atom (cdr-atom (cdr-atom (cdr-atom $lock))))))

;; ---- batch op/head extraction (reuses the Repair-1-proven norm/extract chain
;;      defined in output_verdict.metta) ----
(= (soul-batch-op $cmds)
   (let $arg (norm-metta-arg (extract-metta-arg-structural (car-atom $cmds)))
        (car-atom $arg)))
(= (soul-batch-head $cmds)
   (let $arg (norm-metta-arg (extract-metta-arg-structural (car-atom $cmds)))
        (metta-target-head-structural $arg)))

;; ---- commit match: an approved re-emission matching op+head -> clean (commit).
;;      Non-match while approved falls through to pending/conflict (no bypass). ----
(= (soul-mutation-approved-match? $cmds)
   (let $lock (get-state &soul_mutation_lock)
        (if (== (car-atom-or-self $lock) approved)
            (if (and (== (soul-batch-op $cmds) (lock-op $lock))
                     (== (soul-batch-head $cmds) (lock-head $lock)))
                True False)
            False)))

;; ---- STALE configurable (tunable without code archaeology; default 20) ----
(= (soul-mutation-stale-cycles) 20)

;; ---- approval/denial transition: runs each new-message cycle while a lock is
;;      held. Sender + fingerprint read from substrate, never forged from text. ----
(= (clarity-soul-mutation-gate-transition! $msg $k)
   (let $lock (get-state &soul_mutation_lock)
        (if (== (car-atom-or-self $lock) locked)
            (let $d (py-call (soul_governance.approval_scan
                               $msg (py-call (helper.extract_username $msg))
                               (get-state &last_gate_fingerprint)
                               (get-state &authorized_approvers)))
                 (if (== $d 2)
                     (let* (($op (lock-op $lock))
                            ($hd (lock-head $lock))
                            ($fp (get-state &last_gate_fingerprint))
                            ($_ (change-state! &soul_mutation_lock (approved $op $hd $fp $k)))
                            ($_ (py-call (soul_governance.gate_decision_record "soul" "APPROVED" (repr $op) (repr $hd) $fp (py-call (helper.extract_username $msg))))))
                           ())
                     (if (== $d 1)
                         (let* (($fp (get-state &last_gate_fingerprint))
                                ($_ (change-state! &soul_mutation_lock unlocked))
                                ($_ (change-state! &pending_soul_mutation ""))
                                ($_ (py-call (soul_governance.gate_decision_record "soul" "DENIED" "()" "()" $fp (py-call (helper.extract_username $msg))))))
                               ())
                         ())))
            ())))

;; ---- STALE check: approved lock idle for >= stale-cycles -> FULL RESET.
;;      Runs BEFORE commit-clear in the body (STALE precedence). ----
(= (clarity-soul-mutation-stale-check! $k)
   (let $lock (get-state &soul_mutation_lock)
        (if (== (car-atom-or-self $lock) approved)
            (if (>= (- $k (lock-stamp $lock)) (soul-mutation-stale-cycles))
                (let* (($fp (lock-fp $lock))
                       ($op (lock-op $lock))
                       ($hd (lock-head $lock))
                       ($_ (change-state! &soul_mutation_lock unlocked))
                       ($_ (change-state! &pending_soul_mutation ""))
                       ($_ (py-call (soul_governance.gate_decision_record "soul" "STALE" (repr $op) (repr $hd) $fp "system"))))
                      ())
                ())
            ())))

;; ---- commit/error clearance: after results. Clears the approved lock when the
;;      committed batch executed (COMMIT) or errored (ERROR). Both FULL RESETS.
;;      Only fires if STALE did not already reset this cycle (stale runs first). ----
(= (clarity-soul-mutation-commit-clear! $gate_state $decision $errored)
   (let $lock (get-state &soul_mutation_lock)
        (if (and (== (car-atom-or-self $lock) approved) (== $gate_state clean))
            (if (not (== $decision pause))
                (let* (($fp (lock-fp $lock))
                       ($op (lock-op $lock))
                       ($hd (lock-head $lock))
                       ($phase (if $errored "ERROR" "COMMIT"))
                       ($_ (change-state! &soul_mutation_lock unlocked))
                       ($_ (change-state! &pending_soul_mutation ""))
                       ($_ (py-call (soul_governance.gate_decision_record "soul" $phase (repr $op) (repr $hd) $fp "system"))))
                      ())
                ())   ;; halted (pause): approved lock persists to next cycle
            ())))

;; ---- H11: pause-voice label. Prefixes the Channel D output-pause voice with
;;      [SOUL-PAUSE <fp>] so the announcement is unmistakable and carries the
;;      fingerprint the human must echo to approve. Named hook (no inline work). ----
(= (pause-voice-label $fp $voice)
   (string_concat (string_concat "[SOUL-PAUSE " (string_concat $fp "] ")) $voice))

;; ---- PENDING entry: unlocked --[soul mutation detected]--> (locked op head fp).
;;      THE state-machine entry edge (Integration Map sec 2, BUILDS NOW sec 8).
;;      Fires in 5c when derive-gate-state flags a soul-namespace mutation AND the
;;      lock is unlocked (a fresh detection, not an in-flight approval re-emission).
;;      Computes the fingerprint (SEAM 3), writes the locked record (SEAM 2 shape),
;;      writes &last_gate_fingerprint (the token approval_scan matches), stores the
;;      pending batch, and emits the PENDING gate-decision (SEAM 1). Sender is
;;      "system" -- detection is the substrate's act, not a human's. Immutable once
;;      written; only the reset/clear hooks change it. Named hook; no inline work. ----
(= (clarity-soul-mutation-pending-set! $cmds $k)
   (let $lock (get-state &soul_mutation_lock)
        (if (== (car-atom-or-self $lock) unlocked)
            (let* (($op (soul-batch-op $cmds))
                   ($hd (soul-batch-head $cmds))
                   ($fp (py-call (soul_governance.mutation_fingerprint (repr $op) (repr $hd))))
                   ($_ (change-state! &soul_mutation_lock (locked $op $hd $fp)))
                   ($_ (change-state! &last_gate_fingerprint $fp))
                   ($_ (change-state! &pending_soul_mutation (repr $cmds)))
                   ($_ (py-call (soul_governance.gate_decision_record "soul" "PENDING" (repr $op) (repr $hd) $fp "system"))))
                  ())
            ())))
