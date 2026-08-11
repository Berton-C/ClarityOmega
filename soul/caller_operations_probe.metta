; ============================================================
; Caller Operations Probe: settle the caller-language fork empirically
; ============================================================
; Purpose: the caller-language decision (MeTTa vs Python) rests on ONE
; empirical unknown: does the MeTTa runtime handle the caller's hardest
; operations cleanly, or does it surface rebuild-cycle pain? This harness
; builds the caller's actual hardest operations and runs them, so the fork
; is decided by measurement instead of argument.
;
; The caller's operations decompose into:
;   (A) read pending observations         -> collapse-match (PROVEN: task_state)
;   (B) write/remove pending atoms          -> add/remove-atom (PROVEN: task_state)
;   (C) atomic replace of an atom           -> set-atom! (PROVEN: task_state)
;   (D) |- NAL revision on counts           -> UNPROVEN standalone
;   (E) read-modify-write the efficacy atom -> compose C+D (UNPROVEN together)
;
; A, B, C are already proven by task_state_writers.metta in production.
; This harness probes D and E, the only unproven operations, plus a full
; resolve-cycle simulation (F) that chains them as the caller would.
;
; HARNESS DESIGN NOTE: the caller stores efficacy as COUNTS
; (invocations, successes), not as (stv f c). Revision is therefore a
; count update, not a stv-merge. We probe BOTH the count-update form (what
; the caller actually does) AND a native |- form (in case the substrate
; prefers stv-merge), so the result tells us which representation the
; runtime handles more cleanly.
;
; HOW TO RUN: load this file via run.sh (no registry dependency; it is
; self-contained). Paste the reduction output back.
; ============================================================


; ============================================================
; SEED: an efficacy atom in counts form, plus one in stv form
; ============================================================
; Counts form (what the caller uses): invocations and successes.
(capability-efficacy test-cap (counts invocations: 4 successes: 3))

; stv form (the alternative representation): frequency, confidence.
(cap-efficacy-stv test-cap (stv 0.75 0.8))


; ============================================================
; PROBE D1: count-update revision (the caller's actual revision)
; ============================================================
; A confirmed outcome increments BOTH invocations and successes.
; A disconfirmed outcome increments invocations only.
; This is pure arithmetic on the counts. Define the revision functions
; and run them. If the runtime handles this cleanly, the caller's core
; learning operation is proven in MeTTa.

(= (revise-counts-confirmed (counts invocations: $n successes: $m))
   (counts invocations: (+ $n 1) successes: (+ $m 1)))

(= (revise-counts-disconfirmed (counts invocations: $n successes: $m))
   (counts invocations: (+ $n 1) successes: $m))

; Derived truth expectation on read (canonical NAL-standard formula):
;   frequency = successes / invocations
;   confidence = invocations / (invocations + 1)
;   te = frequency*confidence + 0.5*(1-confidence)
(= (counts-te (counts invocations: $n successes: $m))
   (let $f (/ $m $n)
        (let $c (/ $n (+ $n 1))
             (+ (* $f $c) (* 0.5 (- 1 $c))))))

!(println! "=== PROBE D1: count-update revision ===")
; Confirmed: 4/3 -> 5/4
!(revise-counts-confirmed (counts invocations: 4 successes: 3))
; Disconfirmed: 4/3 -> 5/3
!(revise-counts-disconfirmed (counts invocations: 4 successes: 3))
; te of the starting counts (3/4 freq, 4/5 conf): 0.75*0.8 + 0.5*0.2 = 0.7
!(counts-te (counts invocations: 4 successes: 3))


; ============================================================
; PROBE D2: native |- revision on stv (the alternative)
; ============================================================
; If the substrate has |- as a NAL revision operator, probe it directly.
; This tells us whether stv-merge is available and clean, in case we prefer
; storing efficacy as stv rather than counts.
; NOTE: |- may or may not be defined in core; if this errors, that itself
; is the finding (stv-merge needs library import, counts form is simpler).

!(println! "=== PROBE D2: native |- revision on stv (may error; that is data) ===")
!(|- (cap-efficacy-stv test-cap (stv 0.75 0.8)) (cap-efficacy-stv test-cap (stv 1.0 0.1)))


; ============================================================
; PROBE E: read-modify-write the efficacy atom (compose C + D)
; ============================================================
; The caller's resolve step: read current efficacy, compute revised, set-atom!
; to replace. This is the read-modify-write that task_state proves for scalars
; but has NOT been proven for a structured counts atom. Define the writer and
; run it, then read back to confirm the replace took within this invocation.

(= (current-efficacy $cap)
   (let $r (collapse (match &self (capability-efficacy $cap $counts) $counts))
        (if (== $r ()) (counts invocations: 0 successes: 0) (car-atom $r))))

(= (do-revise-efficacy-confirmed! $cap)
   (let $old (current-efficacy $cap)
        (let $new (revise-counts-confirmed $old)
             (set-atom! &self (capability-efficacy $cap $old)
                              (capability-efficacy $cap $new)))))

!(println! "=== PROBE E: read-modify-write efficacy (resolve step) ===")
; Before: should read (counts invocations: 4 successes: 3)
!(current-efficacy test-cap)
; Apply confirmed revision
!(do-revise-efficacy-confirmed! test-cap)
; After: should read (counts invocations: 5 successes: 4) IF set-atom! took
; within this invocation. This is the critical test: does the read-modify-write
; compose correctly in a single fresh-atomspace invocation?
!(current-efficacy test-cap)


; ============================================================
; PROBE F: full resolve-cycle simulation (the caller's whole inner loop)
; ============================================================
; Chain the operations as the caller would in one resolve pass:
;   1. read a pending observation
;   2. classify it (here: hand-seeded as confirmed)
;   3. revise the efficacy
;   4. write a resolved-invocation audit atom
;   5. remove the pending atom
; If this whole chain runs clean, the caller's inner loop is proven in MeTTa
; and the caller is small enough that MeTTa wins on code-preservation.

(pending-invocation test-cap cycle: 100 criterion: predicate)

(= (resolve-one-pending! $cap $cycle $outcome)
   (let $old (current-efficacy $cap)
        (let $new (if (== $outcome confirmed)
                      (revise-counts-confirmed $old)
                      (revise-counts-disconfirmed $old))
             (let $unit (set-atom! &self (capability-efficacy $cap $old)
                                         (capability-efficacy $cap $new))
                  (let $audit (add-atom &self
                                 (resolved-invocation $cap cycle: $cycle outcome: $outcome))
                       (remove-atom &self
                          (pending-invocation $cap cycle: $cycle criterion: predicate)))))))

!(println! "=== PROBE F: full resolve-cycle ===")
; Run the resolve for the seeded pending, confirmed outcome
!(resolve-one-pending! test-cap 100 confirmed)
; Confirm efficacy revised (now 6/5 if E already ran 4->5, or 5/4 if isolated):
!(current-efficacy test-cap)
; Confirm resolved-invocation audit atom written:
!(collapse (match &self (resolved-invocation test-cap cycle: $c outcome: $o) ($c $o)))
; Confirm pending removed (should be empty):
!(collapse (match &self (pending-invocation test-cap cycle: $c criterion: $cr) $c))


; ============================================================
; READING THE RESULTS  +  THE FORK DECISION
; ============================================================
; PROBE D1 expected:
;   (counts invocations: 5 successes: 4)
;   (counts invocations: 5 successes: 3)
;   0.7  (the truth expectation; may print as a float)
;   -> If these compute correctly, the caller's revision arithmetic works in MeTTa.
;
; PROBE D2 expected:
;   EITHER a revised stv (|- is available and clean)
;   OR an error / unreduced expression (|- needs a library import).
;   Either outcome is data: if it errors, the counts form (D1) is the simpler
;   representation and we use that. If it works, stv-merge is also available.
;
; PROBE E expected:
;   first read:  (counts invocations: 4 successes: 3)
;   after revise: (counts invocations: 5 successes: 4)
;   -> THE CRITICAL ONE. If the second read shows 5/4, then read-modify-write
;      composes within a single invocation and the caller's resolve step works.
;      If the second read still shows 4/3, set-atom! did NOT take within the
;      invocation, which is a real runtime constraint the caller must design
;      around (and a point in favor of Python-first).
;
; PROBE F expected:
;   efficacy revised, resolved-invocation present, pending empty.
;   -> If this whole chain runs clean, the caller's inner loop is proven in
;      MeTTa end to end. Caller is small, port cost approaches zero, MeTTa wins.
;
; THE FORK DECISION, read from the probes:
;   ALL CLEAN (D1 computes, E composes, F chains)  -> build caller in MeTTa.
;       The hardest operations work; the caller is small; no port later.
;   E FAILS (read-modify-write does not compose)   -> Python-first.
;       The runtime fights the caller's core operation; build on mature ground,
;       port later as a deliberate step.
;   D2 ERRORS but D1/E/F clean                      -> MeTTa with counts form.
;       Use counts representation (D1), not stv-merge; caller still works in MeTTa.
;
; Paste all probe outputs back. This settles the fork by measurement.
