; ============================================================
; set-atom! Execution Context Probe: four frames, one run
; ============================================================
; Purpose: the prior probe found set-atom! returns UNREDUCED when a writer
; function with tail-position set-atom! is called as a bare top-level !(...).
; But reading the live loop (loop.metta) shows the existing writers
; (do-set-cycles-since-input!, do-set-last-activity!) are called INSIDE a
; let* binding sequence, not as bare top-level calls. The prior probe tested
; the WRONG invocation context.
;
; This probe tests set-atom! execution across FOUR framings in one run, so the
; substrate tells us which context actually performs the mutation:
;
;   FRAME A: bare top-level writer call         (reproduces the known failure)
;   FRAME B: writer called inside let* binding  (the REAL caller context, loop line 102)
;   FRAME C: set-atom! wrapped in explicit eval (forcing, loop lines 134/155)
;   FRAME D: set-atom! inlined directly in let*  (loop lines 95/100 pattern)
;
; The decisive observable: after each frame, read the atom back. If it shows
; the revised value, the mutation TOOK in that context. If unchanged, it did not.
;
; HOW TO RUN: load via run.sh standalone. Paste the reduction block back.
; NOTE: each frame uses its OWN cap atom so frames do not contaminate each other.
; ============================================================


; Shared revision helper (proven to compute correctly in the prior probe).
(= (revise-counts-confirmed (counts invocations: $n successes: $m))
   (counts invocations: (+ $n 1) successes: (+ $m 1)))

(= (current-eff $cap)
   (let $r (collapse (match &self (cap-eff $cap $counts) $counts))
        (if (== $r ()) (counts invocations: 0 successes: 0) (car-atom $r))))


; ============================================================
; FRAME A: bare top-level writer call (reproduce known failure)
; ============================================================
(cap-eff cap-A (counts invocations: 4 successes: 3))

(= (do-revise-A! $cap)
   (let $old (current-eff $cap)
        (let $new (revise-counts-confirmed $old)
             (set-atom! &self (cap-eff $cap $old) (cap-eff $cap $new)))))

!(println! "=== FRAME A: bare top-level writer call ===")
!(current-eff cap-A)
!(do-revise-A! cap-A)
!(current-eff cap-A)
; Expected (known failure): after-read still 4/3, do-revise returns set-atom! term.


; ============================================================
; FRAME B: writer called inside a let* binding (the REAL caller context)
; ============================================================
; This mirrors loop.metta line 102: ($_ (do-set-cycles-since-input! ...))
; The writer is invoked as a binding step inside let*, then we read back
; INSIDE the same let* so we see whether the mutation took mid-sequence.
(cap-eff cap-B (counts invocations: 4 successes: 3))

(= (do-revise-B! $cap)
   (let $old (current-eff $cap)
        (let $new (revise-counts-confirmed $old)
             (set-atom! &self (cap-eff $cap $old) (cap-eff $cap $new)))))

!(println! "=== FRAME B: writer inside let* binding (real caller context) ===")
!(let* (($before (current-eff cap-B))
        ($_ (do-revise-B! cap-B))
        ($after (current-eff cap-B)))
   (frame-B-result before: $before after: $after))
; Expected IF this is the answer: before 4/3, after 5/4. The let* binding
; sequence forces the writer call to evaluate as a step, executing set-atom!.


; ============================================================
; FRAME C: set-atom! wrapped in explicit eval (forcing mechanism)
; ============================================================
; loop.metta lines 134/155 use (eval $s) to force constructed expressions.
; Here we build the set-atom! term and eval it explicitly.
(cap-eff cap-C (counts invocations: 4 successes: 3))

(= (do-revise-C! $cap)
   (let $old (current-eff $cap)
        (let $new (revise-counts-confirmed $old)
             (eval (set-atom! &self (cap-eff $cap $old) (cap-eff $cap $new))))))

!(println! "=== FRAME C: set-atom! wrapped in explicit eval ===")
!(current-eff cap-C)
!(do-revise-C! cap-C)
!(current-eff cap-C)
; Expected IF eval forces it: after 5/4.


; ============================================================
; FRAME D: set-atom! inlined directly in let* (no wrapping function)
; ============================================================
; loop.metta lines 95/100 inline set-atom! directly in a let* binding,
; not via a function. Test whether inlining (no function indirection) executes.
(cap-eff cap-D (counts invocations: 4 successes: 3))

!(println! "=== FRAME D: set-atom! inlined directly in let* ===")
!(let* (($old (current-eff cap-D))
        ($new (revise-counts-confirmed $old))
        ($_ (set-atom! &self (cap-eff cap-D $old) (cap-eff cap-D $new)))
        ($after (current-eff cap-D)))
   (frame-D-result before: $old after: $after))
; Expected IF inlining executes: after 5/4.


; ============================================================
; FRAME E: progn with set-atom! in BODY position (Clarity's finding)
; ============================================================
; Clarity found do-set-phase! in task_state_writers.metta uses progn with
; set-atom! in body position (not tail), followed by add-atom. Because progn
; evaluates all sub-expressions and returns the last, set-atom! in body
; position MUST evaluate for the following expression to be reached. This is
; the codebase's OWN deliberate forcing pattern for mutations.
; Her proposed self-contained writer: (progn (set-atom! ...) $new)
(cap-eff cap-E (counts invocations: 4 successes: 3))

(= (do-revise-E! $cap)
   (let $old (current-eff $cap)
        (let $new (revise-counts-confirmed $old)
             (progn
                (set-atom! &self (cap-eff $cap $old) (cap-eff $cap $new))
                $new))))

!(println! "=== FRAME E: progn with set-atom! in body position (Clarity's pattern) ===")
!(current-eff cap-E)
!(do-revise-E! cap-E)
!(current-eff cap-E)
; Expected IF progn forces body-position side effects: after 5/4.
; This is the pattern with codebase precedent (do-set-phase! uses it).


; ============================================================
; READING THE RESULTS
; ============================================================
; For each frame, the after-read tells the truth:
;   5/4  = the mutation TOOK in that context
;   4/3  = the mutation did NOT take (set-atom! returned as term, not executed)
;
; INTERPRETATION:
;   A is the control: expect 4/3 (reproduces known failure).
;   B 5/4  -> writers work when called inside let* (the loop hook context).
;   C 5/4  -> wrap set-atom! in eval. Robust, context-independent.
;   D 5/4  -> inline set-atom! in let* without a wrapping function.
;   E 5/4  -> progn with set-atom! in body position. THE PRECEDENTED ANSWER:
;             do-set-phase! in task_state_writers.metta already uses exactly this.
;             Self-contained, context-independent, codebase-proven pattern.
;
; LIKELY WINNER: E. It has codebase precedent (do-set-phase! uses progn with
; set-atom! in body position), it is self-contained (does not depend on the
; calling context re-evaluating a returned term), and it returns a usable value
; ($new) so it composes in let* chains. If E shows 5/4, the caller's writers use
; the progn-body pattern and the blocker is fully resolved with a proven idiom.
;
; FORK RESOLUTION:
;   If E works (most likely): caller is MeTTa, writers use progn with the
;     mutation in body position and the value returned last. Self-contained,
;     matches do-set-phase! precedent, no dependency on loop re-evaluation.
;   If E fails but B works: writers work in let* binding context (loop hooks).
;   If E and B fail but C works: wrap set-atom! in eval.
;   If only D works: inline set-atom! in the hook's let*.
;   If all fail: set-atom! needs the live loop specifically; test in-loop next.
;
; Paste all five frame results back. Frame E is the one to watch: if it shows
; 5/4, the caller's mutation pattern is settled with a codebase-proven idiom and
; the fork comes down cleanly on MeTTa.
