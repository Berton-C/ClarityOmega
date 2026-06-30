

;; ================================================================
;; SECTION 2: WIRING GLUE (Repair 1, 2026-06-10)
;; Gate-state derivation + the decision symbol the loop consumes.
;; The committed gate functions (soul_mutation_gate_corrected.metta)
;; are called per their wiring contract: commands arrive as UNEVALUATED
;; data ($metta_cmds enumerates without eval), so bound-variable calls
;; are safe. Only mutation-form metta args (add-atom / remove-atom /
;; set-atom! heads) are gate-relevant; read-only metta probes flow to
;; the composite. All dispatch single-clause (deterministic).
;; ================================================================

(= (metta-arg-mutates? $arg)
   (let $h (car-atom (quote $arg))
        (if (== $h add-atom) True
            (if (== $h remove-atom) True
                (if (== $h set-atom!) True False)))))

(= (batch-targets-soul? $cmds)
   (if (== $cmds ())
       False
       (let* (($h (car-atom $cmds))
              ($t (cdr-atom $cmds)))
             (if (== (car-atom $h) metta)
                 (let $arg (soul-extract-metta-arg $h)
                      (if (metta-arg-mutates? $arg)
                          (if (soul-metta-targets-soul-namespace? $arg)
                              True
                              (batch-targets-soul? $t))
                          (batch-targets-soul? $t)))
                 (batch-targets-soul? $t)))))

;; Lock semantics v1: held on detection (the lock-write the Python port
;; dropped); clear happens in the Repair 3 confirmation flow. Normal
;; non-soul work proceeds while a mutation awaits confirmation; a SECOND
;; soul mutation while held is a conflict.
(= (derive-gate-state $cmds)
   (if (batch-targets-soul? $cmds)
       (if (soul-mutation-pending?)
           conflict
           (let $_ (change-state! &soul_mutation_lock (locked soul-mutation-proposed))
                pending))
       clean))

;; The loop's branching symbol: mirrors compute-output-verdict's ladder.
(= (output-decision $cmds $gate)
   (if (== $gate pending)
       pause
       (if (== $gate conflict)
           pause
           (if (== $gate clean)
               (if (== $cmds ())
                   proceed
                   (let $r (batch-rank $cmds)
                        (if (== $r 2) pause (if (== $r 1) flag proceed))))
               flag))))
