;; coupling_integrity_detector_writers.metta -- corner detection (writers)
;; Author: ClarityClaw. 2026-06-03. Status: drafted, not yet verified in the container.
;;
;; Consecutive-clear semantics. The writer clears the whole coupling-status window
;; on ANY non-corner verdict, so the window holds only a consecutive run of corners.
;; corner-confirmed (count >= 2) therefore means two corners in a row, and the gate
;; releases the moment the LLM proposes silence or a forward action. This is why the
;; gate does not stay tripped after the agent has composed.
;;
;; KNOWN EDGE (low severity): under a pathological never-resolving corner (the LLM
;; stubbornly re-proposing the orphaned action every cycle while the gate blocks
;; execution), coupling-status grows with the consecutive run. corner-confirmed only
;; needs count >= 2, so behavior is unaffected; this is memory only, and the run
;; clears the instant the LLM adapts (which the Layer 4 feedback drives). Add a
;; safety cap later if it ever matters.
;;
;; ORDERING in loop.metta cycle tail (after populate-recent-action and
;; populate-state-delta): populate-coupling-verdict writes THIS cycle's verdict.
;; The gate (Layer 3) reads corner-confirmed at mid-cycle, so it sees the streak
;; through the PRIOR cycle. populate-state-delta MUST precede populate-coupling-verdict.
;;
;; PeTTa constraints: C12-safe, ASCII-safe, no RMW. The conditional clear puts a
;; side-effecting call in an if branch, a pattern loop.metta already uses.
;; CONFIRM (REPL): the conditional do-clear in the if branch fires only on the
;; non-corner branch, and the no-op token (() here) is a true no-op.

;; ----------------------------------------------------------------
;; CYCLE-LEVEL WRITER (consecutive-clear, then assert verdict)
;; ----------------------------------------------------------------
(= (populate-coupling-verdict $cycle-id)
   (let* (($verdict (coupling-verdict))
          ($_clear  (if (== $verdict corner)
                        ()
                        (do-clear-coupling-status!)))
          ($_assert (add-atom &self (coupling-status $cycle-id $verdict))))
      ()))

;; ----------------------------------------------------------------
;; CONTEXT-RESET CLEARER (removes ALL coupling-status atoms)
;; ----------------------------------------------------------------
;; Two callers: this file's non-corner clear above, and loop.metta on $msgnew
;; (new human input == context changed, which also clears the streak before the
;; gate runs, so the gate never fires on a response-in-flight cycle).
;;
;; BUG FIX (2026-06-04, harness): same fix as do-clear-state-delta!. The prior
;; shape superposed before guarding empty; on an empty window (superpose ()) yields
;; zero solutions and halts the populate let* before the add. Guard the collapsed
;; LIST for empty first, and collapse-wrap the removal so the clearer returns one
;; solution (a windowed superpose-remove yields N solutions, which would otherwise
;; multiply the add that follows the clear in populate-coupling-verdict).
(= (do-clear-coupling-status!)
   (let $existing (collapse (match &self (coupling-status $c $v) (coupling-status $c $v)))
      (if (== $existing ())
          ()
          (let $_drained (collapse (let $old (superpose $existing)
                                        (remove-atom &self $old)))
             ()))))
