; ============================================================
; Capability Registry Path C: Caller-Interface Verification Harness
; ============================================================
; Purpose: verify the two registry behaviors the NACE caller depends on,
; against the ACTUAL atom shapes in capability_registry_path_c_draft.metta,
; so the caller is built on a verified interface rather than assumed shapes.
;
; The caller depends on exactly two registry behaviors:
;   INTERFACE 1 (caller's log hook reads this): dispatch writes
;     (capability-invoked invocation-id: $id handler: $h input-atom: $atom)
;     for each capability that runs in the chain. The log hook reads these
;     to know which capabilities were dispatched this cycle.
;   INTERFACE 2 (caller's write target is consumed here): the
;     efficacy-filter-step resolves efficacy and filters on a 0.3 threshold.
;     The caller writes learned efficacy; the filter step must consume it.
;
; HOW TO RUN (in the clarity_omega container):
;   Load capability_registry_path_c_draft.metta first, then load this file,
;   OR paste both together. The harness seeds capabilities, runs dispatch,
;   and inspects the atoms the registry wrote.
;
; This harness writes ONLY test atoms (test- prefixed handlers and a
; test eligible-lifecycle). It does not modify registry code.
; ============================================================


; ============================================================
; SEED: eligibility config + three test capabilities
; ============================================================
; The registry's eligible? checks for (eligible-lifecycle $l) atoms.
; Without this, every capability is filtered out at the lifecycle step.
(eligible-lifecycle active)

; Three test capabilities at different efficacy levels to exercise
; the filter step's threshold (0.3):
;   test-cap-high   declared efficacy 0.9  -> should pass
;   test-cap-low    declared efficacy 0.1  -> should be filtered out
;   test-cap-default no efficacy-rate atom  -> defaults to 1.0 -> should pass
(registered-capability schema: (test-request data: $d) handler: test-cap-high    priority: 100 lifecycle: active)
(registered-capability schema: (test-request data: $d) handler: test-cap-low     priority: 90  lifecycle: active)
(registered-capability schema: (test-request data: $d) handler: test-cap-default priority: 80  lifecycle: active)

; Declared baseline efficacy rates (efficacy-filter-step reads capability-efficacy-rate)
(capability-efficacy-rate handler: test-cap-high rate: 0.9)
(capability-efficacy-rate handler: test-cap-low  rate: 0.1)
; test-cap-default deliberately has NO rate atom -> filter step defaults to 1.0

; Minimal handlers: each returns a marker (not decision-anchor, so the
; chain runs all of them rather than anchoring on the first).
(= (test-cap-high $input)    test-cap-high-ran)
(= (test-cap-low $input)     test-cap-low-ran)
(= (test-cap-default $input) test-cap-default-ran)


; ============================================================
; TEST 1: dispatch runs and writes capability-invoked atoms
; ============================================================
; INTERFACE 1 verification. After dispatch, the caller's log hook will
; read (capability-invoked ...) atoms. Confirm they get written, and for
; WHICH handlers (the filtered-out test-cap-low should NOT appear).
;
; Expected: capability-invoked atoms for test-cap-high and test-cap-default,
; NOT for test-cap-low (filtered out at efficacy 0.1 < 0.3).
!(println! "=== TEST 1: run dispatch ===")
!(dispatch (test-request data: payload-1) test-inv-001)

!(println! "=== TEST 1a: capability-invoked atoms written (INTERFACE 1) ===")
!(collapse (match &self
      (capability-invoked invocation-id: test-inv-001 handler: $h input-atom: $a)
      $h))
; Expected: (test-cap-high test-cap-default) in some order.
; test-cap-low absent = efficacy filter worked = INTERFACE 2 also confirmed.


; ============================================================
; TEST 2: efficacy filter step gates on threshold (INTERFACE 2)
; ============================================================
; Direct confirmation that test-cap-low (efficacy 0.1) was filtered and
; test-cap-high (0.9) and test-cap-default (1.0 default) passed.
; We re-derive the eligible set the same way dispatch does.
!(println! "=== TEST 2: eligible set after filter pipeline ===")
!(let $raw (collapse
         (match &self
                (registered-capability schema: (test-request data: $d)
                                       handler: $h priority: $p lifecycle: $l)
                (raw-cap-entry handler: $h priority: $p lifecycle: $l)))
      (resolve-and-filter-entries $raw ()))
; Expected: cap-entry atoms for test-cap-high and test-cap-default only.
; test-cap-low filtered. Confirms the 0.3 threshold gates correctly.


; ============================================================
; TEST 3: efficacy OBSERVATION override changes the outcome
; ============================================================
; The caller will eventually write learned efficacy. Today the filter step
; reads capability-efficacy-observation as an override. Confirm the override
; path works: push test-cap-low's efficacy UP via observation, and it should
; now pass the filter.
(capability-efficacy-observation handler: test-cap-low efficacy: 0.8)

!(println! "=== TEST 3: test-cap-low after efficacy observation override 0.8 ===")
!(let $raw (collapse
         (match &self
                (registered-capability schema: (test-request data: $d)
                                       handler: $h priority: $p lifecycle: $l)
                (raw-cap-entry handler: $h priority: $p lifecycle: $l)))
      (resolve-and-filter-entries $raw ()))
; Expected: now ALL THREE pass (test-cap-low's 0.1 baseline overridden to 0.8).
; This confirms the override mechanism the caller's learned-efficacy write
; will eventually flow through. NOTE: this is the OBSERVATION atom, not the
; learned counts atom. See the GAP note below.


; ============================================================
; TEST 4: fallback when nothing matches
; ============================================================
; INTERFACE robustness. Dispatch an input no capability matches.
; Confirm dispatch-fallback-activated is written (the caller should treat
; a fallback cycle as "no capability dispatched" = nothing to log).
!(println! "=== TEST 4: dispatch unmatched input ===")
!(dispatch (unmatched-request foo: bar) test-inv-002)

!(println! "=== TEST 4a: fallback atom written ===")
!(collapse (match &self
      (dispatch-fallback-activated invocation-id: test-inv-002 input-atom: $a reason: $r)
      ($a $r)))
; Expected: one atom, reason no-matching-capability.


; ============================================================
; READING THE RESULTS  +  THE GAP THE CALLER MUST CLOSE
; ============================================================
; PASS criteria:
;   TEST 1a: capability-invoked written for test-cap-high and test-cap-default,
;            NOT test-cap-low. (INTERFACE 1 confirmed: caller log hook has
;            real atoms to read; filtered capabilities correctly absent.)
;   TEST 2:  eligible set = test-cap-high + test-cap-default only.
;            (INTERFACE 2 confirmed: efficacy threshold gates dispatch.)
;   TEST 3:  after observation override, test-cap-low passes too.
;            (Override path confirmed: this is how learned efficacy reaches
;            the filter TODAY.)
;   TEST 4a: fallback atom written for unmatched input.
;
; THE GAP (critical for the caller build):
;   The efficacy-filter-step reads TWO efficacy sources today:
;     (capability-efficacy-rate handler: $h rate: $r)        -- declared baseline
;     (capability-efficacy-observation handler: $h efficacy: $e) -- override
;   It does NOT read a learned counts atom like
;     (capability-efficacy capability: $h invocations: $n successes: $m ...)
;   The NACE caller writes LEARNED efficacy as counts. For the filter step
;   to consume what the caller learns, ONE of these must happen:
;     (a) the caller writes its learned efficacy into the OBSERVATION atom
;         (capability-efficacy-observation), reusing the existing override
;         path. Simplest. The learned value IS the override. But it conflates
;         "machine-learned" with "externally-observed," losing that distinction.
;     (b) efficacy-filter-step is extended to read the learned counts atom in
;         its resolution order: observation > learned > declared > default.
;         Cleaner separation. Requires a small edit to efficacy-filter-step.
;   Recommendation: (b). It keeps learned efficacy distinct from external
;   observation, matches the caller contract's resolution-order section, and
;   the edit is small (one more collapse-match in efficacy-filter-step,
;   inserted between observation and declared-baseline).
;
; Paste all test outputs back to Berton. The GAP is not a harness failure;
; it is the one registry edit the caller build depends on, surfaced by
; reading the real draft.
