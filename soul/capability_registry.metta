;; soul/capability_registry.metta
;; ClarityOmega Sprint 0 Phase 1 - Capability Registry Dispatcher
;; Path B Integrated Version (observation + efficacy)
;;
;; Per sprint_0_phase_1_design_v3.2.md Section 5A (Operational Specification).
;; Phase D verified 5 of 6 success criteria.
;; Criterion 5 (handler error isolation) is a KNOWN LIMITATION; see below.
;;
;; PATH B ADDITIONS: efficacy tracking and success-criterion as first-class
;; atom shapes, following the same observation-override pattern as lifecycle
;; and priority. The pipe is shaped to carry efficacy data from day one.
;;
;; ARCHITECTURAL PRINCIPLES (per v3.2):
;;
;; - Bind-then-act (BTA-1): all computed arguments to add-atom are let-bound
;;   first. Direct function calls in argument position fail silently (no-op).
;;
;; - Indirect-call composition: Handler invocations are always indirect (via
;;   reduce/2). Runtime primitives must be empirically validated for indirect-
;;   call composition before assuming they work in dispatcher rules.
;;
;; - Broadcast dispatch: all matching capabilities fire in priority order,
;;   not just the highest-priority match. Decision anchor stops the chain.
;;
;; - Decision anchor (NOT halt atom): the primary act is the handler's
;;   decision; chain-stopping is the structural consequence.
;;
;; - Single-pass dispatch: handler-emitted atoms do NOT cause additional
;;   intra-cycle dispatch. Re-dispatch requires explicit new (dispatch ...) call.
;;
;; - Control flow lives in atoms, not in function calls.
;;
;; - Resolvable fields: lifecycle, priority, AND efficacy are dynamically
;;   resolvable via external observation atoms. This enables external
;;   governance without editing registration atoms.
;;
;; - Efficacy as data: capabilities declare their own success criteria.
;;   The registry carries efficacy data structurally, not as retrofit.
;;
;;
;; KNOWN LIMITATION (Phase D Criterion 5):
;;
;; Handlers that throw a hard exception during indirect invocation
;; terminate the dispatch chain silently. No dispatch-result is written,
;; no anchor check, no recursion to subsequent handlers.
;; Phase 1 ships with the discipline: handlers must not crash.
;; Phase 1.5 addresses isolation through runtime fix or Error-return contract.


;; =============================================================
;; Rule 1: dispatch
;; =============================================================

(= (dispatch $input-atom $invocation-id)
   (progn
      (add-atom &self
                (dispatch-invocation
                  invocation-id: $invocation-id
                  input-atom: $input-atom))
      (let $raw-matched (collapse
                            (match &self
                                   (registered-capability
                                     schema: $input-atom
                                     handler: $h
                                     priority: $p
                                     lifecycle: $l)
                                   (raw-cap-entry handler: $h priority: $p lifecycle: $l)))
           (let $eligible (resolve-and-filter-entries $raw-matched ())
                (if (== $eligible ())
                    (add-atom &self
                              (dispatch-fallback-activated
                                invocation-id: $invocation-id
                                input-atom: $input-atom
                                reason: no-matching-capability))
                    (let $sorted (msort $eligible)
                         (run-chain $sorted $input-atom $invocation-id)))))))


;; =============================================================
;; Resolution and Eligibility Helpers
;; =============================================================

;; Resolve lifecycle: external observation overrides registration value.
(= (resolve-lifecycle $handler $registered-value)
   (let $obs (collapse (match &self
                             (capability-lifecycle-observation
                               handler: $handler
                               lifecycle: $observed)
                             $observed))
        (if (== $obs ())
            $registered-value
            (car-atom $obs))))

;; Check eligibility: data-driven via eligible-lifecycle atoms.
(= (eligible? $lifecycle)
   (let $check (collapse (match &self (eligible-lifecycle $lifecycle) True))
        (if (== $check ()) False True)))

;; Resolve priority: external observation overrides registration value.
(= (resolve-priority $handler $registered-value)
   (let $obs (collapse (match &self
                             (capability-priority-observation
                               handler: $handler
                               priority: $observed)
                             $observed))
        (if (== $obs ())
            $registered-value
            (car-atom $obs))))

;; Resolve efficacy: external observation overrides registration value.
;; Same pattern as lifecycle and priority resolution.
(= (resolve-efficacy $handler $registered-value)
   (let $obs (collapse (match &self
                             (capability-efficacy-observation
                               handler: $handler
                               efficacy-rate: $observed)
                             $observed))
        (if (== $obs ())
            $registered-value
            (car-atom $obs))))

;; Efficacy-based eligibility check.
;; If no minimum-efficacy-threshold exists, all handlers pass.
;; Backwards compatible: efficacy filtering is opt-in.
(= (efficacy-eligible? $efficacy-rate)
   (let $threshold (collapse (match &self (minimum-efficacy-threshold $t) $t))
        (if (== $threshold ())
            True
            (let $min (car-atom $threshold)
                 (if (>= $efficacy-rate $min) True False)))))

;; Destructure raw-cap-entry
(= (extract-raw-handler (raw-cap-entry handler: $h priority: $p lifecycle: $l)) $h)
(= (extract-raw-priority (raw-cap-entry handler: $h priority: $p lifecycle: $l)) $p)
(= (extract-raw-lifecycle (raw-cap-entry handler: $h priority: $p lifecycle: $l)) $l)

;; Resolve-and-filter: lifecycle resolution, eligibility check,
;; priority resolution, and now efficacy resolution and eligibility.
(= (resolve-and-filter-entries () $acc) $acc)

(= (resolve-and-filter-entries $candidates $acc)
   (let $head (car-atom $candidates)
        (let $tail (cdr-atom $candidates)
             (let $handler (extract-raw-handler $head)
                  (let $reg-lifecycle (extract-raw-lifecycle $head)
                       (let $res-lifecycle (resolve-lifecycle $handler $reg-lifecycle)
                            (if (eligible? $res-lifecycle)
                                (let $reg-priority (extract-raw-priority $head)
                                     (let $res-priority (resolve-priority $handler $reg-priority)
                                          ;; Efficacy resolution: check registered efficacy
                                          ;; and external observations. Filter if below threshold.
                                          (let $reg-efficacy (collapse
                                                (match &self
                                                  (capability-efficacy-rate
                                                    handler: $handler
                                                    rate: $r)
                                                  $r)))
                                               (let $res-efficacy
                                                    (if (== $reg-efficacy ())
                                                        1.0
                                                        (resolve-efficacy $handler
                                                          (car-atom $reg-efficacy)))
                                                    (if (efficacy-eligible? $res-efficacy)
                                                        (resolve-and-filter-entries $tail
                                                          (cons-atom (cap-entry priority: $res-priority handler: $handler) $acc))
                                                        (resolve-and-filter-entries $tail $acc))))))
                                (resolve-and-filter-entries $tail $acc))))))))


;; =============================================================
;; Rule 2: base case for run-chain (empty list)
;; =============================================================

(= (run-chain () $input-atom $invocation-id)
   chain-complete)


;; =============================================================
;; Rule 3: recursive chain walker
;; =============================================================

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


;; =============================================================
;; Efficacy Companion Atoms (Path B addition)
;; =============================================================
;;
;; (capability-success-criterion handler: $h criterion: $c)
;; Declares what success looks like for a given handler.
;; The criterion is an atom shape, not a boolean. Each capability
;; defines success in its own vocabulary. The dispatcher does not
;; interpret the criterion; it makes it available for external
;; observation and evaluation. Optional: handlers can register
;; without declaring a criterion.
;;
;; (capability-efficacy-rate handler: $h rate: $r)
;; The handler current efficacy rate. Can be set at registration time
;; and updated by external observation (same override pattern).
;;
;; (capability-efficacy-observation handler: $handler efficacy-rate: $observed)
;; External observation of efficacy rate. Overrides the registered value.
;;
;; (minimum-efficacy-threshold $t)
;; Optional seed atom. If present, handlers below threshold are filtered.
;; If absent, no efficacy-based filtering (backwards compatible).


;; =============================================================
;; Seed Atoms (boot initialization)
;; =============================================================
;;
;; Lifecycle eligibility:
;;   (eligible-lifecycle active)
;;   (eligible-lifecycle degraded)
;;
;; Efficacy (optional - Path B):
;;   (minimum-efficacy-threshold 0.5)  ;; remove if no efficacy filtering
