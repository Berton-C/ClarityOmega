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
;; Section 1: do-bootstrap-task-state!
;; Section 2: do-set-cycles-since-input!, do-set-last-activity!
;; Section 3: do-set-phase!, do-resolve-pending-thread!
;; ================================================================

;; ================================================================
;; SECTION 1: BOOTSTRAP WRITER
;; Called once from loop.metta initLoop, before any per-cycle writers.
;; For each scalar atom: if absent from &self, add-atom the default.
;; ================================================================

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
;; ================================================================

(= (do-set-cycles-since-input! $new-value)
   (let $old (current-cycles-since-input)
      (set-atom! &self (cycles-since-input $old) (cycles-since-input $new-value))))

(= (do-set-last-activity! $timestamp)
   (let $old (current-last-activity)
      (set-atom! &self (last-activity $old) (last-activity $timestamp))))

;; ================================================================
;; SECTION 3: RESPONSE-STREAM SKILLS
;; Called from Clarity's response stream via skill registry.
;; do-*! naming convention. C12-safe throughout.
;; ================================================================

;; (do-set-phase! $new-phase)
;;   Reads current-phase. If same, no-op. Else replaces atom
;;   and records (task-phase-transition $old $new (get_time)).
;;   v1: no validation; accepts any phase atom value.
(= (do-set-phase! $new-phase)
   (let $current (current-phase)
      (if (== $current $new-phase)
          _
          (progn
             (set-atom! &self (task-phase $current) (task-phase $new-phase))
             (add-atom &self (task-phase-transition $current $new-phase (get_time)))))))

;; (do-resolve-pending-thread! $topic)
;;   Finds (pending-thread $topic $timestamp) via collapse-match.
;;   If absent, silent no-op. If found, remove-atom with exact pattern.
(= (do-resolve-pending-thread! $topic)
   (let $ts (collapse (match &self (pending-thread $topic $t) $t))
      (if (== $ts ())
          _
          (remove-atom &self (pending-thread $topic $ts)))))

;; (is-valid-anchor-value? $v)
;;   Returns True if $v is in the valid anchor set (Section 4.5 of spec),
;;   False otherwise. Primary: Safety, Integrity, HumanFlourishing,
;;   Governance, Helpfulness. Secondary: WonderPreservation,
;;   CreativeTranscendence, TimeCoherence, PurposeBeyondUtility,
;;   SharedUnderstanding, AgencyBalance.
(= (is-valid-anchor-value? $v)
   (if (== $v Safety) True
   (if (== $v Integrity) True
   (if (== $v HumanFlourishing) True
   (if (== $v Governance) True
   (if (== $v Helpfulness) True
   (if (== $v WonderPreservation) True
   (if (== $v CreativeTranscendence) True
   (if (== $v TimeCoherence) True
   (if (== $v PurposeBeyondUtility) True
   (if (== $v SharedUnderstanding) True
   (if (== $v AgencyBalance) True
       False))))))))))))

;; (do-set-phase-with-anchor! $new-phase $value $reason)
;;   Same shape as do-set-phase! plus conditional anchor record.
;;   If $current == $new-phase: no-op.
;;   Else: replace phase, add transition, conditionally add anchor.
;;   $value must be in valid anchor set; if invalid, anchor skipped
;;   but phase transition proceeds. v1 baseline silent-skip behavior.
(= (do-set-phase-with-anchor! $new-phase $value $reason)
   (let $current (current-phase)
      (if (== $current $new-phase)
          _
          (progn
             (set-atom! &self (task-phase $current) (task-phase $new-phase))
             (add-atom &self (task-phase-transition $current $new-phase (get_time)))
             (if (is-valid-anchor-value? $value)
                 (add-atom &self (task-phase-anchor $new-phase $value (get_time) $reason))
                 _)))))

;; (find-min-ts $best $rest) - eviction internal
;;   Recursive min-finder over ($topic $timestamp) pairs. $best is the
;;   current best pair; $rest is the remaining list to scan.
;;   Returns the pair with minimum $timestamp.
(= (find-min-ts $best ()) $best)
(= (find-min-ts ($best-topic $best-ts) (($t $ts) $rest))
   (if (< $ts $best-ts)
       (find-min-ts ($t $ts) $rest)
       (find-min-ts ($best-topic $best-ts) $rest)))

;; (oldest-pending-thread) - eviction internal
;;   Wraps find-min-ts with collapse-match. Returns ($topic $timestamp)
;;   of pending-thread atom with smallest timestamp, or () if no pending
;;   threads exist.
(= (oldest-pending-thread)
   (let $all (collapse (match &self (pending-thread $t $ts) ($t $ts)))
      (if (== $all ())
          ()
          (find-min-ts (car-atom $all) (cdr-atom $all)))))

;; (do-add-pending-thread! $topic)
;;   Adds (pending-thread $topic (get_time)) to &self. After adding,
;;   checks count via count-pending-threads. If > 7, evicts oldest
;;   (FIFO) via oldest-pending-thread + remove-atom. If <= 7, no-op.
(= (do-add-pending-thread! $topic)
   (let $now (get_time)
      (progn
         (add-atom &self (pending-thread $topic $now))
         (if (> (count-pending-threads) 7)
             (let $oldest (oldest-pending-thread)
                (if (== $oldest ())
                    _
                    (let $old-topic (car-atom $oldest)
                       (let $old-ts (car-atom (cdr-atom $oldest))
                          (remove-atom &self
                             (pending-thread $old-topic $old-ts))))))
             _))))