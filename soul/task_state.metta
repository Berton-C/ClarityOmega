;; ================================================================
;; task_state.metta -- Task State Primitive Definitions
;; ClarityClaw operational state tracking
;;
;; Six atom families for tracking task state:
;;   (task-phase $phase)                            - current operational phase
;;   (task-phase-anchor $phase $value $timestamp $reason)  - value-forked transitions
;;   (last-activity $timestamp)                     - timestamp of last activity
;;   (cycles-since-input $n)                       - cycles since last human input
;;   (pending-thread $topic)                       - tracked but unresolved topics
;;   (task-phase-transition $from $to $timestamp)  - transition history
;;
;; Valid phases (Section 5):
;;   attending        - default, waiting for input or between tasks
;;   engaged          - actively processing a human message
;;   research         - gathering information or exploring
;;   response-drafting - composing output
;;   idle             - no activity, self-directed mode
;;   waiting          - deliberately waiting (timer, async)
;;   reflecting       - self-reflection, reviewing internal state
;;   boundary-detected - boundary condition detected, system responding
;;
;; Pure definitions only. C12-safe (no match inside if).
;; Side-effecting writers (do-*!) land in task_state_writers.metta.
;; Skills land in Step 3.
;; ================================================================

;; ================================================================
;; SECTION 1: ATOM SHAPES
;; These define the structure of each atom family.
;; Scalar atoms maintain exactly one instance at a time.
;; Accumulation atoms grow over the session.
;; ================================================================

;; Scalar atoms (one instance at a time, replaced on change)
;; (task-phase $phase)
;;   $phase ? {attending, engaged, research, response-drafting, idle, waiting, reflecting, boundary-detected}
;;
;; (cycles-since-input $n)
;;   $n ? Nat (non-negative integer, incremented each cycle)
;;
;; (last-activity $timestamp)
;;   $timestamp ? Nat (epoch seconds)

;; Accumulation atoms (zero or more instances, added over time)
;; (task-phase-anchor $phase $value $timestamp $reason)
;;   $phase     - the phase being entered
;;   $value     - the soul value that warranted surfacing this transition
;;   $timestamp - when the anchor was recorded (epoch seconds)
;;   $reason    - why this value was engaged for this transition
;;
;; (pending-thread $topic)
;;   $topic - identifier for the tracked thread (symbol)
;;
;; (task-phase-transition $from $to $timestamp)
;;   $from      - previous phase
;;   $to        - new phase
;;   $timestamp - when the transition occurred (epoch seconds)

;; ================================================================
;; SECTION 2: BOOTSTRAP VALUES
;; Scalar atoms are bootstrapped conditionally by loop.metta initLoop
;; via task_state_writers.metta (do-bootstrap-task-state!).
;; That function checks &self for each scalar atom; if absent, adds
;; the default. This avoids dual-atom ambiguity when persistence
;; restoration (ChromaDB) writes a restored value ? the guard
;; prevents a bare file-load default from coexisting with the
;; restored atom.
;;
;; Accumulation atoms have no bootstrap values:
;; (task-phase-anchor ...)       -- added by set-phase-with-anchor skill
;; (pending-thread ...)          -- added by add-pending-thread skill
;; (task-phase-transition ...)  -- added by set-phase skill
;; ================================================================

;; ================================================================
;; SECTION 3: PURE READ HELPERS
;; C12-safe: collapse-then-branch pattern for scalar readers.
;; No match inside if. No side effects. All (= ...) definitions.
;; ================================================================

;; Current phase. Returns attending if no task-phase atom exists.
(= (current-phase)
   (let $result (collapse (match &self (task-phase $p) $p))
      (if (== $result ())
          attending
          (car-atom $result))))

;; Current cycles since last input. Returns 0 if no atom exists.
(= (current-cycles-since-input)
   (let $result (collapse (match &self (cycles-since-input $n) $n))
      (if (== $result ())
          0
          (car-atom $result))))

;; Current last-activity timestamp. Returns 0 if no atom exists.
(= (current-last-activity)
   (let $result (collapse (match &self (last-activity $t) $t))
      (if (== $result ())
          0
          (car-atom $result))))

;; Current pending threads. Returns all pending-thread topics,
;; or () if none exist. Collection reader -- no if-branch needed
;; because empty IS the correct answer, not a fallback.
(= (current-pending-threads)
   (match &self (pending-thread $topic) $topic))