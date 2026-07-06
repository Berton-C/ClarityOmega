;; === corner_gate_v2_patch.metta ===
;; DRAFT for Clarity's analysis. Destination: these definitions EDIT INTO
;; soul/corner_gap/corner_gate.metta at build step B4 (the v1 apply-corner-gate
;; and gate-aware-results bodies are replaced; originals preserved in comments
;; per the mothball-comment convention).
;;
;; Pattern-scoped enforcement with structural release (design Sections 3, 10):
;; only commands whose exact repr appears in the corner-window record are
;; suppressed; anything different passes, executes, makes line 173 nonempty
;; and line 174 novel, flips forward-outcome, and the streak writers release
;; the gate. msgnew exemption lives HERE, not in the loop hook (Discipline 1).

;; Is this exact command form in the confirmed-corner record?
;; repr is LET-BOUND before the match (REPL CONFIRM item 1; the bound-variable
;; match is the pre-approved safe shape from the F1.1 lesson family).
(= (cmd-in-corner-window? $cmd)
   (let $r (repr $cmd)
        (> (size-atom (collapse (match &self (corner-window-cmd $c $r) $c))) 0)))

;; Keep-order filter. Single-head recursion, if-dispatch on () (P3 fork
;; precedent). cons-atom availability is REPL CONFIRM item 2; if absent, the
;; fallback shape is an accumulator building via collapse of a superpose over
;; kept elements, to be settled in her analysis.
(= (filter-corner-cmds $cmds)
   (if (== $cmds ())
       ()
       (let* (($h (car-atom $cmds))
              ($t (filter-corner-cmds (cdr-atom $cmds))))
             (if (== (cmd-in-corner-window? $h) True)
                 $t
                 (cons-atom $h $t)))))

;; The v2 gate: person-window exempt (commitment 4), graded firing
;; (commitment 5, corner-confirmed-core via q-geq), pattern-scoped
;; (commitment 2).
(= (apply-corner-gate-v2 $sexpr $msgnew)
   (if (== $msgnew True)
       $sexpr
       (if (== (corner-confirmed-core) True)
           (filter-corner-cmds $sexpr)
           $sexpr)))

;; v2 feedback: informational, names mechanism, no stillness demand
;; (commitment 6). Substrate-callable; Clarity amends at will.
(= (corner-gate-feedback-v2)
   "CORNER: this cycle repeated command forms that recently produced no forward outcome, and those exact forms were held back. Any different command passes and executes. A new move is the exit.")

;; v2 results shaping: replace results with feedback ONLY when the whole
;; batch was held (full drop) on a non-msgnew confirmed cycle. Partial drops
;; let real results flow; the held signature surfaces in next cycle's
;; CORNER-STATE block (CONFIRM item 4 for Clarity: is that sufficient?).
;; Arity: the loop passes $results, $sexpr_gated, and $msgnew (one call,
;; logic in this file, Discipline 1).
(= (gate-aware-results-v2 $results $sexpr-gated $msgnew)
   (if (== $msgnew True)
       $results
       (if (== (corner-confirmed-core) True)
           (if (== (size-atom (collapse (superpose $sexpr-gated))) 0)
               (RESULTS: (corner-gate-feedback-v2))
               $results)
           $results)))
