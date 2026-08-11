;; ================================================================
;; invocation_counter.metta -- candidate (iii) invocation-id source
;; Sprint 0-Coda Phase B, gensym-invocation-id resolution
;;
;; Candidate (i) eliminated: no gensym-equivalent primitive in runtime
;; (Clarity verified 2026-05-26, conclusive across manifest/.metta/.py
;; plus failed direct evaluation).
;;
;; Candidate (iii): atomspace-stored counter, substrate-first-aligned
;; per ADR-007. Counter lives as (invocation-counter $n) atom, queryable
;; via !(match &self (invocation-counter $n) $n).
;;
;; Pattern matched EXACTLY to task_state_writers.metta proven idiom:
;;   - bootstrap: collapse-match-then-conditional-add
;;   - increment: set-atom! with exact old value as from-argument
;;   - C12-safe: no match inside if; collapse-then-branch throughout
;;   - Mirror pattern: AtomSpace atoms only, no change-state!
;;
;; THIS IS A CLAUDE FIRST-DRAFT for three-way review.
;; Substrate authorship is Clarity's; this draft exists because current
;; duplicate-engagement / parsing reliability made a clean multi-step
;; substrate-authoring handoff shaky. Clarity reviews and revises; the
;; MeTTa she approves is the MeTTa that lands.
;;
;; DESIGN CHOICES (challengeable in review):
;;   1. Placement (iii-a): increment happens before dispatch is called;
;;      fresh id passed into dispatch as existing argument. Dispatch
;;      primitive signature UNCHANGED (preserves v6 Change 0).
;;   2. Counter is an atomspace atom (invocation-counter $n), not a
;;      state variable. Inspectable, ADR-007-aligned.
;;   3. Increment uses set-atom! (the proven task_state idiom), not
;;      change-state! (unreliable in let*) and not separate remove/add.
;;   4. Returned id is the post-increment value. First call returns 1.
;;      Counter atom and returned id stay in lockstep.
;;   5. Bootstrap seeds (invocation-counter 0) if absent. Called once
;;      from initLoop alongside do-bootstrap-task-state!, OR co-located
;;      bootstrap call (see OPEN QUESTION below).
;; ================================================================

;; ----------------------------------------------------------------
;; READ HELPER (pure): current-invocation-counter
;; Returns current $n, or 0 if the atom does not yet exist.
;; collapse-then-branch; C12-safe.
;; ----------------------------------------------------------------
(= (current-invocation-counter)
   (let $result (collapse (match &self (invocation-counter $n) $n))
      (if (== $result ())
          0
          (car-atom $result))))

;; ----------------------------------------------------------------
;; BOOTSTRAP: do-bootstrap-invocation-counter!
;; If (invocation-counter $n) absent from &self, add default 0.
;; Idempotent: safe to call every initLoop; only seeds once.
;; Mirrors do-bootstrap-task-state! pattern exactly.
;; ----------------------------------------------------------------
(= (do-bootstrap-invocation-counter!)
   (let $result (collapse (match &self (invocation-counter $n) $n))
      (if (== $result ())
          (add-atom &self (invocation-counter 0))
          _)))

;; ----------------------------------------------------------------
;; INCREMENT-AND-RETURN: next-invocation-id!
;; Reads current $n via pure helper, computes $n+1, replaces the atom
;; via set-atom! (exact old value as from-argument), returns $n+1.
;;
;; Precondition: do-bootstrap-invocation-counter! has run (atom exists).
;; If bootstrap has NOT run, current-invocation-counter returns 0, the
;; set-atom! from-pattern (invocation-counter 0) will not match any atom,
;; and the replace silently no-ops -- which is why bootstrap must precede
;; first call. This is the same precondition task_state per-cycle writers
;; carry (their header line 42).
;; ----------------------------------------------------------------
(= (next-invocation-id!)
   (let $old (current-invocation-counter)
      (let $new (+ $old 1)
         (progn
            (set-atom! &self (invocation-counter $old) (invocation-counter $new))
            $new))))

;; ================================================================
;; OPEN QUESTION FOR REVIEW (Clarity's substrate-eye needed):
;;
;; Q-A: set-atom! return value and progn sequencing.
;;   do-set-cycles-since-input! (task_state_writers line 45-47) uses
;;   set-atom! as the LAST expression in its let, returning set-atom!'s
;;   own return value (the writers do not need a return value; they are
;;   called for side effect). Here, next-invocation-id! must return $new
;;   AFTER the set-atom! side effect. The progn wraps (set-atom! ...) then
;;   $new so the side effect fires and then $new is returned. QUESTION:
;;   does progn reliably sequence side-effect-then-return in PeTTa here,
;;   or does the nondet/lazy evaluation order risk returning $new before
;;   set-atom! commits? If risk exists, the task_state writers never hit
;;   it because they do not depend on post-write return ordering. This is
;;   the one place this counter diverges from the proven idiom's usage.
;;
;; Q-B: placement of bootstrap call.
;;   Option 1: add (do-bootstrap-invocation-counter!) to initLoop right
;;     after (do-bootstrap-task-state!). Clean, co-located with the other
;;     bootstrap, fires once at startup.
;;   Option 2: co-locate inside next-invocation-id! as a guard (call
;;     bootstrap at the top of every increment). Self-contained but adds
;;     a collapse-match to every dispatch. Slight per-cycle cost.
;;   Lean: Option 1 (initLoop bootstrap), matching task_state precedent.
;;
;; Q-C: same-cycle collision.
;;   If dispatch fires at most once per cycle (which Sprint 0-Coda's
;;   getContext insertion guarantees -- one skill-request per getContext
;;   call), the counter increments once per cycle and collision cannot
;;   occur. If a future capability dispatches multiple times per cycle,
;;   the no-atomic-RMW constraint means two next-invocation-id! calls in
;;   the same cycle could read the same $old before either writes. For
;;   Sprint 0-Coda this is not a risk (one dispatch per cycle). Flag for
;;   Sprint 1 if multi-dispatch-per-cycle capabilities arrive.
;; ================================================================

;; ----------------------------------------------------------------
;; SEED (if Q-B Option 1 is NOT chosen and co-located seeding preferred,
;; this line seeds at file load; otherwise initLoop bootstrap handles it).
;; Commented out pending Q-B resolution:
;; (invocation-counter 0)
;; ----------------------------------------------------------------
