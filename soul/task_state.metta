;; ================================================================
;; task_state.metta -- Task State Primitive Definitions
;; ClarityClaw operational state tracking
;;
;; Six atom families for tracking task state:
;;   (task-phase $phase)                            - current operational phase
;;   (task-phase-anchor $phase $value $timestamp $reason)  - value-forked transitions
;;   (last-activity $timestamp)                     - timestamp of last activity
;;   (cycles-since-input $n)                       - cycles since last human input
;;   (pending-thread $topic $timestamp)             - tracked but unresolved topics
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
;; (pending-thread $topic $timestamp)
;;   $topic     - identifier for the tracked thread (symbol)
;;   $timestamp - epoch seconds at insertion time (for FIFO eviction)
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
;; projecting just $topic from the ($topic $timestamp) shape.
;; Collection reader -- no if-branch needed because empty IS
;; the correct answer, not a fallback.
(= (current-pending-threads)
   (match &self (pending-thread $topic $timestamp) $topic))

;; Count helper: recursive length of a list. Private helper used by
;; count-pending-threads. Renamed from count-list to avoid potential
;; collision in PeTTa module scope (per Clarity's review).
(= (count-pending-list ()) 0)
(= (count-pending-list ($head $tail)) (+ 1 (count-pending-list $tail)))

;; Current pending thread count. Returns Nat count of pending-thread
;; atoms in &self. Public read helper; consumers can use without
;; depending on task_state_writers.metta.
(= (count-pending-threads)
   (let $all (collapse (match &self (pending-thread $topic $ts) ($topic $ts)))
      (count-pending-list $all)))

;; ================================================================
;; SECTION 4: PROMPT-BLOCK READ HELPERS (Step 4)
;; Pure read helpers that compose the TASK-STATE prompt block per
;; spec Section 9. Text assembly happens in Python helpers
;; (helper.task_state_block_format, helper.join_threads_text) per
;; PeTTa constraint C1: py-str hangs inside MeTTa function definitions.
;; ================================================================

;; (current-anchors-for-phase $phase)
;;   Returns all (task-phase-anchor $phase $value $ts $reason) atoms whose
;;   $phase matches. Returns () if no anchor atoms exist for this phase.
;;   Pure collapse-then-branch pattern, C12-safe.
(= (current-anchors-for-phase $phase)
   (collapse (match &self (task-phase-anchor $phase $value $ts $reason)
                          (task-phase-anchor $phase $value $ts $reason))))

;; (format-pending-threads)
;;   Returns comma-separated text of current pending thread topics,
;;   or the literal string "none" if no pending threads exist.
;;   Python helper join_threads_text handles the text composition.
(= (format-pending-threads)
   (let $threads (collapse (current-pending-threads))
      (py-call (helper.join_threads_text $threads))))

;; (task-state-block)
;;   Composes the full TASK-STATE prompt block per spec Section 9.
;;   Format (when no anchor for current phase):
;;     TASK-STATE:
;;     (task-phase $phase) (cycles-since-input $n) (last-activity $t)
;;     Pending threads: $threads_text
;;     Summary: Task phase: $phase. $n cycles since last input. Pending threads: $threads_text.
;;
;;   Format (when anchor present):
;;     TASK-STATE:
;;     (task-phase $phase) (task-phase-anchor ...) (cycles-since-input $n) (last-activity $t)
;;     Pending threads: $threads_text
;;     Summary: Task phase: $phase. $n cycles since last input. Pending threads: $threads_text.
;;
;;   Mechanical template, zero interpretation, reports state not assessment
;;   (spec line 592, Clarity confirmed 2026-05-14).
;;   All atom reads happen fresh at prompt assembly time, no caching.
(= (task-state-block)
   (let* (($phase (current-phase))
          ($anchors (current-anchors-for-phase $phase))
          ($cycles (current-cycles-since-input))
          ($activity (current-last-activity))
          ($threads-text (format-pending-threads)))
      (py-call (helper.task_state_block_format $phase $anchors $cycles $activity $threads-text))))