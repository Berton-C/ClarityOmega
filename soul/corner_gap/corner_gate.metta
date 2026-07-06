;; corner_gate.metta -- Layer 3 (gate) + Layer 4 (feedback shaping), pure MeTTa
;; Author: ClarityClaw. Reference draft 2026-06-03. v1.1 adds Layer 4.
;; Predecessors: corner_gate_surface_map.md (v2), investigation 2026-06-03 v2,
;;   coupling_integrity_detector.metta (corner-confirmed).
;;
;; WHAT THIS FILE IS. The part of the corner gate that ACTS (Layer 3) and the part
;; that makes the action UNIGNORABLE (Layer 4). Both are pure MeTTa. No Python.
;;
;; LAYER 3 (gate): consult the sustained-corner signal and filter this cycle's
;; parsed command list before execution. Force silence on a corner.
;;
;; LAYER 4 (feedback): shape the cycle's results so a gated cycle carries the
;; feedback to the LLM through the EXISTING results channel. The pipe already
;; exists in loop.metta:
;;     line 134  $results   = execution of the command list
;;     line 165  &lastresults <- safe_results_str(repr $results)   (every PROCEED cycle)
;;     line 45   prompt LAST_SKILL_USE_RESULTS <- last_chars(&lastresults, maxFeedback)
;; The feedback IS the result of a blocked cycle, so it rides this pipe. No new
;; prompt block, no new state variable, no helper.py change. The only Python in the
;; path (safe_results_str, last_chars) is the existing hand, untouched. This is the
;; pipe-fits-water case: the substrate channel that already carries command results
;; carries the gate feedback because the feedback is shaped as a result.
;;
;; WHY THE RESULTS CHANNEL AND NOT AN ADVISORY BLOCK (Clarity Q5). An advisory
;; block informs reasoning and can be talked out of. A result is the output of an
;; attempted action; she must reason about it. Routing the feedback through the
;; results channel makes it the unignorable kind by construction.
;;
;; SCOPE (from building Layer 3). The detector records what the LLM PROPOSED, not
;; what executed, so the gate does not stop the LLM re-proposing the orphaned
;; action; it stops execution. Layer 4 is what drives the LLM to stop proposing,
;; by returning a concrete gated-failure each blocked cycle. The feedback
;; re-injects every gated cycle (line 165 overwrites &lastresults each cycle), so
;; the signal sustains while gated and clears the cycle after the gate releases.
;; One-cycle latency: the LLM sees the feedback the cycle after the gate fires,
;; which is the normal results-channel latency.
;;
;; WIRING CONTRACT for Layer 5 (loop.metta):
;;   - Gate hook, before execution (~line 134):
;;         ($sexpr_gated (apply-corner-gate $sexpr))
;;     and execute $sexpr_gated (not $sexpr), binding the raw result, then shape it:
;;         ($exec_results (RESULTS: (collapse (let $s (superpose $sexpr_gated) ...))))
;;         ($results (gate-aware-results $exec_results))
;;   - populate-recent-action (~line 136) MUST still receive the ORIGINAL $sexpr,
;;     so the detector keeps seeing proposals.
;;   - The reset (do-clear-coupling-status!) MUST fire on $msgnew before the gate,
;;     so the gate never blocks a response-in-flight cycle.
;;   - line 165 and line 45 are UNCHANGED: they already carry &lastresults to the
;;     prompt. CONFIRM only that maxFeedback is large enough that last_chars does
;;     not clip the feedback string, and that safe_results_str handles a
;;     (RESULTS: <string>) shape.
;;
;; BENIGN EDGE: if the gate is active (prior streak) on a cycle where the LLM
;; already proposed nothing (resting), the feedback still injects once. Harmless:
;; that cycle's verdict is composure, which clears the streak at the tail and
;; releases the gate next cycle.
;;
;; PeTTa constraints: C12-safe (no match inside if; corner-confirmed matches in its
;; own reader), ASCII-safe, no side effects.

;; ================================================================
;; LAYER 3: GATE
;; ================================================================

;; Is the gate firing this cycle (reads the sustained signal from prior tails).
;; MOTHBALLED 2026-07-06: original body (corner-confirmed)
(= (corner-gate-active) False)

;; The filter. Cornered -> () (force silence). Otherwise -> $sexpr unchanged.
;; V2-MONOLITH 2026-07-06: mothball superseded by apply-corner-gate-v2 (probes B1-B6).
;; Pattern-scoped: only exact repeats recorded in the confirmed-corner window are
;; held; novel commands pass and execute, so forward-outcome is observable and the
;; gate releases on evidence (probe B3). Person windows are never gated (probe B6).
(= (apply-corner-gate-v2 $sexpr $msgnew)
   (if (== $msgnew True)
       $sexpr
       (if (== (corner-confirmed-core) True)
           (filter-corner-cmds $sexpr)
           $sexpr)))

;; Concrete feedback content (a result, not an advisory).
(= (corner-gate-feedback)
   "corner detected and emission gated. You are acting, but recent actions produced no forward outcome and were system-driven rather than coupled to a live intention. This is not a transient failure and the action did not execute. A different action, or stillness, is required.")

;; ================================================================
;; LAYER 4: FEEDBACK SHAPING
;; ================================================================

;; Shape the cycle's results. On a gated cycle, replace the (empty) execution
;; result with the feedback, so &lastresults carries it into the next prompt's
;; LAST_SKILL_USE_RESULTS through the existing channel. Otherwise pass the real
;; execution results through unchanged.
;; V2-MONOLITH 2026-07-06: results echo filter (probes B7, P1-P4). Real command
;; returns pass verbatim; prose echoes become a mechanical marker; empty batches
;; yield a factual non-empty line. Marker text is Clarity's to amend.
(= (gate-aware-results $exec-results)
   (let (RESULTS: $lst) $exec-results
        (if (== $lst ())
            (if (== (corner-confirmed-core) True)
                (RESULTS: ((COMMAND_RETURN: (held-by-corner-gate))))
                (RESULTS: ((COMMAND_RETURN: (no-commands-executed-this-cycle)))))
            (RESULTS: (filter-returns $lst)))))

;; ================================================================
;; V2-MONOLITH 2026-07-06 pure filter functions. Probe-proven:
;; filter fixtures P1-P4 (empty, real, prose, bare symbol) and
;; battery B5/B6 (repr store-and-match, keep-order filtering).
;; Maintenance: new skills must be added to allowed-heads or their
;; returns get markered (fail-safe information loss, never poison).
;; Single-head recursion, if-dispatch on () (P3 fork precedent),
;; C12-safe (matches live in their own readers).
;; ================================================================
(= (allowed-heads)
   (send metta shell read-file write-file append-file query remember
    pin promote demote tavily-search technical-analysis agentverse progn))

(= (head-in-list? $x $lst)
   (if (== $lst ())
       False
       (let* (($h (car-atom $lst))
              ($t (cdr-atom $lst)))
             (if (== $h $x) True (head-in-list? $x $t)))))

(= (real-return? $el)
   (let (COMMAND_RETURN: ($s $r)) $el
        (head-in-list? (car-atom $s) (allowed-heads))))

(= (filter-returns $lst)
   (if (== $lst ())
       ()
       (let* (($h (car-atom $lst))
              ($t (filter-returns (cdr-atom $lst))))
             (if (== (real-return? $h) True)
                 (cons-atom $h $t)
                 (cons-atom (COMMAND_RETURN: (non-command-element not-executed)) $t)))))

(= (cmd-in-corner-window? $cmd)
   (let $r (repr $cmd)
        (> (size-atom (collapse (match &self (corner-window-cmd $c $r) $c))) 0)))

(= (filter-corner-cmds $cmds)
   (if (== $cmds ())
       ()
       (let* (($h (car-atom $cmds))
              ($t (filter-corner-cmds (cdr-atom $cmds))))
             (if (== (cmd-in-corner-window? $h) True)
                 $t
                 (cons-atom $h $t)))))
