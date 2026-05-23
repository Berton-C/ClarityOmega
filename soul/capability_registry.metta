;; soul/capability_registry.metta
;; ClarityOmega Sprint 0 Phase 1 - Capability Registry Dispatcher
;;
;; Per sprint_0_phase_1_design_v3.2.md Section 5A (Operational Specification).
;; Phase D verified 5 of 6 success criteria.
;; Criterion 5 (handler error isolation) is a KNOWN LIMITATION; see below.
;;
;; ARCHITECTURAL PRINCIPLES (per v3.2):
;;
;; - Bind-then-act (BTA-1): all computed arguments to add-atom are let-bound
;;   first. Direct function calls in argument position fail silently (no-op).
;;
;; - Indirect-call composition: Handler invocations are always indirect (via
;;   reduce/2). Runtime primitives must be empirically validated for indirect-
;;   call composition before assuming they work in dispatcher rules. The catch
;;   failure is precedent: a primitive that works in direct composition can
;;   silently fail in indirect composition with no runtime signal. See Phase D
;;   discriminator T-10 for evidence; see ADR-007 for the broader principle.
;;
;; - Broadcast dispatch: all matching capabilities fire in priority order,
;;   not just the highest-priority match. Decision anchor stops the chain.
;;
;; - Decision anchor (NOT halt atom): the primary act is the handler's
;;   decision; chain-stopping is the structural consequence. See v3.2
;;   Section 4.6 for naming rationale.
;;
;; - Single-pass dispatch: handler-emitted atoms do NOT cause additional
;;   intra-cycle dispatch. Re-dispatch requires explicit new (dispatch ...) call.
;;
;; - Control flow lives in atoms, not in function calls. Capability selection,
;;   commitment, branching, and isolation are all substrate I/O. The handler
;;   invocation in Rule 3 is the one place this is NOT true; that is where
;;   the runtime's composition-dependent semantics bite, and that is precisely
;;   where Criterion 5's limitation lives. See ADR-007 for the principle.
;;
;;
;; KNOWN LIMITATION (Phase D Criterion 5):
;;
;; Handlers that throw a hard exception (e.g., arithmetic division by zero,
;; instantiation errors) during indirect invocation terminate the dispatch
;; chain silently. The dispatcher does not write a dispatch-result for the
;; crashing handler, does not check the decision anchor, does not recurse
;; to subsequent handlers in the chain.
;;
;; Empirically demonstrated by Phase D discriminator tests T-9 and T-10:
;;   - catch absorbs exceptions when wrapping a direct Prolog predicate call
;;     (handler symbol concrete at source).
;;   - catch does NOT absorb exceptions when wrapping reduce/2 indirect
;;     invocation (handler symbol variable-bound, as in run-chain).
;;
;; In the same silent-failure-mode family as BTA-1: the runtime's advertised
;; behavior (catch absorbs exceptions) does not apply in this specific
;; composition pattern, and the runtime provides no signal that the absorption
;; failed.
;;
;;
;; WHY NO CATCH WRAP (architectural integrity):
;;
;; An earlier dispatcher draft wrapped the handler call in catch. Phase D
;; T-10 empirically falsified that mechanism. The catch wrap remained
;; non-functional but technically syntactically valid, which would have
;; trained future readers to believe error isolation was present where
;; it was structurally inert.
;;
;; The catch wrap was also the one component of the dispatcher that
;; relied on runtime promise-keeping (catch catches exceptions) rather than
;; substrate state. Everything else in the dispatcher uses substrate I/O
;; (match, collapse, add-atom). The one place that violated the substrate-
;; externalized pattern is the one place that silently failed. This is
;; architectural coherence, not coincidence.
;;
;; Per the design principle "commitments must be structurally inescapable,"
;; a commitment mechanism that itself isn't structurally enforced is a
;; false commitment. Phase 1 ships without the catch wrap.
;;
;;
;; PHASE 1.5 PATHS (high-confidence, narrowed):
;;
;; (a) PeTTa runtime change: make reduce/2 propagate exceptions as catchable
;;     Prolog exceptions. The catch wrap then becomes functional and the gap
;;     is closed at the runtime level. The dispatcher itself is unchanged.
;;     This path addresses uncooperative handlers (ones that crash with hard
;;     exceptions; e.g. third-party handler code, runtime arithmetic faults).
;;
;; (b) Substrate-native Error return contract: handlers communicate failure
;;     through the same channel they communicate success: the return atom.
;;     The handler does not crash; it produces an Error atom. The dispatcher
;;     pattern-matches on the result and writes a dispatch-result with error
;;     semantics. Control flow stays in atoms.
;;
;;     This is NOT self-diagnosis (handlers reporting their own errors as
;;     a violation of isolation). This is control-flow-through-atoms applied
;;     to error communication. The handler signals failure as data, the
;;     dispatcher reads data, no runtime primitives are involved in the
;;     isolation path. This path addresses cooperative handlers (ones that
;;     can detect failure conditions and choose to return an Error atom).
;;
;; Path (a) and path (b) are complementary. Path (a) handles handlers that
;; cannot cooperate (crash on hard exceptions). Path (b) handles handlers
;; that can (return Error atoms instead of crashing). Both may be needed.
;;
;; Other approaches (explicit handler-cooperative Error return through
;; reduce/2 alone; alternative invocation patterns avoiding reduce/2)
;; either reduce to one of the above paths or violate data-driven dispatch.
;;
;; Phase 1 ships with the discipline: handlers must not crash. Phase 1.5
;; addresses isolation through path (a), path (b), or both.


;; =============================================================
;; Rule 1: dispatch
;; =============================================================

(= (dispatch $input-atom $invocation-id)
   (progn
      (add-atom &self
                (dispatch-invocation
                  invocation-id: $invocation-id
                  input-atom: $input-atom))
      (let $matched (collapse
                       (match &self
                              (registered-capability
                                schema: $input-atom
                                handler: $h
                                priority: $p
                                lifecycle: active)
                              (cap-entry priority: $p handler: $h)))
           (if (== $matched ())
               (add-atom &self
                         (dispatch-fallback-activated
                           invocation-id: $invocation-id
                           input-atom: $input-atom
                           reason: no-matching-capability))
               (let $sorted (msort $matched)
                    (run-chain $sorted $input-atom $invocation-id))))))


;; =============================================================
;; Rule 2: base case for run-chain (empty list)
;; =============================================================

(= (run-chain () $input-atom $invocation-id)
   chain-complete)


;; =============================================================
;; Rule 3: recursive chain walker
;; =============================================================
;;
;; The handler call ($current-handler $input-atom) is NOT wrapped in catch.
;; See KNOWN LIMITATION above for why.

(= (run-chain $sorted-chain $input-atom $invocation-id)
   (let $head-entry (car-atom $sorted-chain)
        (let $tail-chain (cdr-atom $sorted-chain)
             (let $current-handler (extract-handler $head-entry)
                  (let $handler-result ($current-handler $input-atom)
                       (progn
                          (add-atom &self
                                    (dispatch-result
                                      invocation-id: $invocation-id
                                      handler: $current-handler
                                      result: $handler-result))
                          (let $anchor-check (collapse
                                              (match &self
                                                     (dispatch-decision-anchor
                                                       invocation-id: $invocation-id
                                                       anchored-by: $h
                                                       reason: $r)
                                                     anchored))
                               (if (== $anchor-check ())
                                   (run-chain $tail-chain $input-atom $invocation-id)
                                   chain-anchored))))))))


;; =============================================================
;; Helper: extract-handler
;; =============================================================

(= (extract-handler (cap-entry priority: $p handler: $h)) $h)
