;; soul/capability_registry.metta - Path C (generalized filter pipeline)
;;
;; Key change: resolve-and-filter-entries no longer hardcodes its pipeline.
;; Filter steps are registered as (capability-filter-step order: $n step: $fn) atoms.
;; New dimensions (trust, scope, cost) need only a new registration atom.

;; =============================================================
;; Rule 1: dispatch
;; =============================================================
;;
;; CANONICAL SHAPE (load-bearing invariant):
;;   (registered-capability schema: $s handler: $h priority: $p
;;                          lifecycle: $l metadata: $m)
;; registered-capability is FIVE fields. metadata carries provenance,
;; version, and extensible annotations downstream consumers need. Every
;; consumer that matches registered-capability MUST use this 5-field shape.
;; A 4-field matcher silently fails to couple (structural match is exact in
;; MeTTa: no error, no warning, just an empty match and a silent fallback).
;; Any future consumer that deviates from this arity is a defect by definition.
;;
;; FALLBACK REASON VOCABULARY (load-bearing invariant, same contract class as
;; the arity above but on the semantic axis):
;;   reason: no-matching-capability  -- raw-matched was empty: nothing matched
;;                                      the schema. The agent genuinely lacks a
;;                                      capability for this input.
;;   reason: all-candidates-filtered -- raw-matched was NON-empty but every
;;                                      candidate was filtered out (ineligible
;;                                      lifecycle, low efficacy, a block step).
;;                                      The agent HAS a capability; it was
;;                                      suppressed. Investigate the filter, do
;;                                      NOT acquire a duplicate.
;; These demand OPPOSITE agent responses (acquire vs investigate). Conflating
;; them steers the agent toward wrong remediation and compounds in the
;; capability-management loop, so this is a Safety-adjacent distinction. Every
;; reader of dispatch-fallback-activated MUST branch on both reasons.
;; (Sprint-1 will enrich all-candidates-filtered with WHICH filter step dropped
;; each candidate; the plumbing exists in the filter steps' filtered-out returns.)

;; Per-cycle retention: clear the prior cycle's transient dispatch records
;; before writing this cycle's, so dispatch-* atoms do not accumulate across the
;; loop's lifetime. Variable patterns clear all ids/counts (map remove-all,
;; self-healing). Touches ONLY transients; the efficacy/observation learning
;; surface is never swept. A0 (remove-on-zero) proven no-op, so the first-cycle
;; sweep on a clean state is safe.
(= (sweep-dispatch-atoms!)
   (let $_a (remove-atom &self (dispatch-invocation invocation-id: $i1 input-atom: $a1))
   (let $_b (remove-atom &self (capability-invoked invocation-id: $i2 handler: $h2 input-atom: $a2))
   (let $_c (remove-atom &self (dispatch-result invocation-id: $i3 result: $r3 handler: $h3))
   (let $_d (remove-atom &self (dispatch-chain-exhausted invocation-id: $i4))
   (let $_e (remove-atom &self (dispatch-chain-anchored invocation-id: $i5 anchor-handler: $h5))
   (let $_f (remove-atom &self (dispatch-fallback-activated invocation-id: $i6 input-atom: $a6 reason: $r6))
        swept)))))))

(= (dispatch $input-atom $invocation-id)
   (progn
      (sweep-dispatch-atoms!)
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
                                     lifecycle: $l
                                     metadata: $m)
                                   (raw-cap-entry handler: $h priority: $p lifecycle: $l)))
           (let $eligible (resolve-and-filter-entries $raw-matched ())
                (if (== $eligible ())
                    (let $fallback-reason (if (== $raw-matched ())
                                              no-matching-capability
                                              all-candidates-filtered)
                         (add-atom &self
                                   (dispatch-fallback-activated
                                     invocation-id: $invocation-id
                                     input-atom: $input-atom
                                     reason: $fallback-reason)))
                    (let $sorted (msort $eligible)
                         (run-chain $sorted $input-atom $invocation-id)))))))

;; =============================================================
;; Resolution Helpers (unchanged)
;; =============================================================

(= (resolve-lifecycle $handler $registered-value)
   (let $obs (collapse (match &self
                             (capability-lifecycle-observation
                               handler: $handler
                               lifecycle: $observed)
                             $observed))
        (if (== $obs ())
            $registered-value
            (car-atom $obs))))

(= (eligible? $lifecycle)
   (let $check (collapse (match &self (eligible-lifecycle $lifecycle) True))
        (if (== $check ()) False True)))

(= (resolve-priority $handler $registered-value)
   (let $obs (collapse (match &self
                             (capability-priority-observation
                               handler: $handler
                               priority: $observed)
                             $observed))
        (if (== $obs ())
            $registered-value
            (car-atom $obs))))

(= (resolve-efficacy $handler $registered-value)
   (let $obs (collapse (match &self
                             (capability-efficacy-observation
                               handler: $handler
                               efficacy: $observed)
                             $observed))
        (if (== $obs ())
            $registered-value
            (car-atom $obs))))

(= (efficacy-eligible? $efficacy)
   (>= $efficacy 0.3))

;; =============================================================
;; Filter Step Infrastructure (NEW - the generalization)
;; =============================================================
;;
;; (capability-filter-step order: $n step: $step-fn)
;;
;; Each filter step function has signature:
;;   (= ($step-fn $entry) $result)
;; where $result is either a (pipeline-entry ...) or the atom filtered-out.
;;
;; Steps are applied in order. If any step returns filtered-out,
;; the entry is dropped from the dispatch chain.
;;
;; Adding a new filter dimension (trust, scope, cost, etc.) requires ONLY:
;;   1. Define the step function: (= (my-filter-step $entry) ...)
;;   2. Register it: (capability-filter-step order: $n step: my-filter-step)
;; No changes to resolve-and-filter-entries or any other registry code.

;; Seed filter steps for existing dimensions:
(capability-filter-step order: 10 step: lifecycle-filter-step)
(capability-filter-step order: 20 step: priority-filter-step)
(capability-filter-step order: 30 step: efficacy-filter-step)

;; Pipeline entry: carries resolved values through the filter chain.
;; (pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e)

;; Pipeline entry accessors:
(= (pe-handler (pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e)) $h)
(= (pe-lifecycle (pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e)) $l)
(= (pe-priority (pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e)) $p)
(= (pe-efficacy (pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e)) $e)

;; Pipeline entry constructors (return modified entry with one field changed):
(= (pe-with-lifecycle (pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e) $new-l)
   (pipeline-entry handler: $h lifecycle: $new-l priority: $p efficacy: $e))
(= (pe-with-priority (pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e) $new-p)
   (pipeline-entry handler: $h lifecycle: $l priority: $new-p efficacy: $e))
(= (pe-with-efficacy (pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $e) $new-e)
   (pipeline-entry handler: $h lifecycle: $l priority: $p efficacy: $new-e))

;; Apply all registered filter steps to an entry.
;; We use (cap-entry priority: $o handler: $s) as a sort wrapper so msort
;; orders steps by their registered order number.
(= (apply-filter-pipeline $entry)
   (let $steps (msort (collapse (match &self
                                    (capability-filter-step order: $o step: $s)
                                    (cap-entry priority: $o handler: $s))))
        (walk-filter-steps $steps $entry)))

(= (walk-filter-steps () $entry) $entry)

(= (walk-filter-steps $steps $entry)
   (let $head (car-atom $steps)
        (let $tail (cdr-atom $steps)
             (let $step-fn (extract-handler $head)
                  (let $result ($step-fn $entry)
                       (if (== $result filtered-out)
                           filtered-out
                           (walk-filter-steps $tail $result)))))))

;; =============================================================
;; Filter Step Implementations (the 3 existing steps, decomposed)
;; =============================================================

;; Step 10: Lifecycle resolution and eligibility check
(= (lifecycle-filter-step $entry)
   (let $handler (pe-handler $entry)
        (let $raw-lifecycle (pe-lifecycle $entry)
             (let $resolved (resolve-lifecycle $handler $raw-lifecycle)
                  (if (eligible? $resolved)
                      (pe-with-lifecycle $entry $resolved)
                      filtered-out)))))

;; Step 20: Priority resolution (no filtering, just enrichment)
(= (priority-filter-step $entry)
   (let $handler (pe-handler $entry)
        (let $raw-priority (pe-priority $entry)
             (let $resolved (resolve-priority $handler $raw-priority)
                  (pe-with-priority $entry $resolved)))))

;; Step 30: Efficacy resolution and eligibility check
(= (efficacy-filter-step $entry)
   (let $handler (pe-handler $entry)
        (let $reg-efficacy (collapse (match &self
                                        (capability-efficacy-rate
                                          handler: $handler
                                          rate: $r)
                                        $r))
             (let $base-efficacy (if (== $reg-efficacy ()) 1.0 (car-atom $reg-efficacy))
                  (let $resolved (resolve-efficacy $handler $base-efficacy)
                       (if (efficacy-eligible? $resolved)
                           (pe-with-efficacy $entry $resolved)
                           filtered-out))))))

;; =============================================================
;; Generalized resolve-and-filter-entries (replaces hardcoded version)
;; =============================================================

(= (resolve-and-filter-entries () $acc) $acc)

(= (resolve-and-filter-entries $candidates $acc)
   (let $head (car-atom $candidates)
        (let $tail (cdr-atom $candidates)
             (let $handler (extract-raw-handler $head)
                  (let $reg-lifecycle (extract-raw-lifecycle $head)
                       (let $reg-priority (extract-raw-priority $head)
                            (let $initial-entry (pipeline-entry
                                                  handler: $handler
                                                  lifecycle: $reg-lifecycle
                                                  priority: $reg-priority
                                                  efficacy: 1.0)
                                 (let $result (apply-filter-pipeline $initial-entry)
                                      (if (== $result filtered-out)
                                          (resolve-and-filter-entries $tail $acc)
                                          (let $final-priority (pe-priority $result)
                                               (resolve-and-filter-entries $tail
                                                 (cons-atom (cap-entry priority: $final-priority handler: $handler) $acc))))))))))))

;; =============================================================
;; Extract raw entry fields (unchanged)
;; =============================================================

(= (extract-raw-handler (raw-cap-entry handler: $h priority: $p lifecycle: $l)) $h)
(= (extract-raw-priority (raw-cap-entry handler: $h priority: $p lifecycle: $l)) $p)
(= (extract-raw-lifecycle (raw-cap-entry handler: $h priority: $p lifecycle: $l)) $l)

;; =============================================================
;; Run chain (unchanged)
;; =============================================================

(= (extract-handler (cap-entry priority: $p handler: $h)) $h)

(= (run-chain () $input-atom $invocation-id)
   (add-atom &self (dispatch-chain-exhausted invocation-id: $invocation-id)))

(= (run-chain $sorted $input-atom $invocation-id)
   (let $head (car-atom $sorted)
        (let $tail (cdr-atom $sorted)
             (let $handler (extract-handler $head)
                  (progn
                    (add-atom &self
                      (capability-invoked
                        invocation-id: $invocation-id
                        handler: $handler
                        input-atom: $input-atom))
                    (let $result ($handler $input-atom)
                         (progn
                           (add-atom &self
                             (dispatch-result
                               invocation-id: $invocation-id
                               result: $result
                               handler: $handler))
                           (if (== $result decision-anchor)
                             (add-atom &self
                               (dispatch-chain-anchored
                                 invocation-id: $invocation-id
                                 anchor-handler: $handler))
                             (run-chain $tail $input-atom $invocation-id)))))))))
