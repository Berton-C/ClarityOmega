;; ================================================================
;; task_state_writers.metta -- Side-effecting writers for task-state atoms
;; ClarityClaw operational state tracking
;;
;; This file contains the do-*! functions that mutate task-state atoms
;; in &self. Pure read helpers remain in task_state.metta.
;;
;; C12-safe: no match inside if. All guards use collapse-then-branch.
;; Mirror pattern: AtomSpace atoms only, no change-state!.
;;
;; Three functions for Step 2:
;;   (do-bootstrap-task-state!)           - conditional initLoop bootstrap
;;   (do-set-cycles-since-input! $n)       - atomic replace for cycles counter
;;   (do-set-last-activity! $timestamp)   - atomic replace for activity timestamp
;; ================================================================

;; ================================================================
;; SECTION 1: BOOTSTRAP WRITER
;; Called once from loop.metta initLoop, before any per-cycle writers.
;; For each scalar atom: if absent from &self, add-atom the default.
;; After persistence restoration is wired, the guard prevents
;; dual-atom ambiguity (restored atom won't compete with a
;; file-load default because no file-load default exists).
;; ================================================================

;; (do-bootstrap-task-state!)
;;   No arguments.
;;   Checks &self for each scalar atom. Adds default if absent.
;;   Defaults: task-phase -> attending, cycles-since-input -> 0,
;;            last-activity -> 0
(= (do-bootstrap-task-state!)
   (progn
      (let $phase-result (collapse (match &self (task-phase $p) $p))
         (if (== $phase-result ())
             (add-atom &self (task-phase attending))
             _))
      (let $cycles-result (collapse (match &self (cycles-since-input $n) $n))
         (if (== $cycles-result ())
             (add-atom &self (cycles-since-input 0))
             _))
      (let $activity-result (collapse (match &self (last-activity $t) $t))
         (if (== $activity-result ())
             (add-atom &self (last-activity 0))
             _))))

;; ================================================================
;; SECTION 2: PER-CYCLE SCALAR WRITERS
;; Atomic replace: read current via pure helper, then set-atom!
;; with exact old value as the from-argument.
;;
;; Precondition: do-bootstrap-task-state! has run (atoms exist in &self).
;; If called before bootstrap, pure helpers return fallback values
;; and set-atom! on a non-existent atom may silently fail.
;; ================================================================

;; (do-set-cycles-since-input! $new-value)
;;   $new-value - Nat (new cycle count)
;;   Reads (current-cycles-since-input), replaces atom in &self.
;;   Called per-cycle with 0 (reset on new message) or (+ 1 current)
;;   (increment on same-message cycle).
(= (do-set-cycles-since-input! $new-value)
   (let $old (current-cycles-since-input)
      (set-atom! &self (cycles-since-input $old) (cycles-since-input $new-value))))

;; (do-set-last-activity! $timestamp)
;;   $timestamp - Nat (epoch seconds)
;;   Reads (current-last-activity), replaces atom in &self.
;;   Called per-cycle at two points: post-msgnew and post-send,
;;   each with (get_time) as the timestamp argument.
(= (do-set-last-activity! $timestamp)
   (let $old (current-last-activity)
      (set-atom! &self (last-activity $old) (last-activity $timestamp))))