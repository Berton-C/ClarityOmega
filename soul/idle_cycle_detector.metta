;; soul/idle_cycle_detector.metta
;; Idle-cycle detector v1: send-burst detection (Step 4.5)
;;
;; History:
;;   2026-04-25: Candidate 002 proposed by Clarity (mechanism 1:
;;     content-repetition detection, never wired)
;;   2026-05-14: v1 implementation per Plan A Step 4.5, design
;;     confirmed by Clarity. Mechanism 2 (send-burst) implemented;
;;     mechanism 1 (content-repetition) deferred to v2.
;;
;; v1 detection rule (Clarity-confirmed):
;;   Count send-class action tags (responsive-send, status-send-unprompted)
;;   in the current recent-action window (10 cycles, per
;;   recent_action_populator.metta). If count > send-burst-threshold,
;;   emit (idle-pattern stuck-duplicate-engagement $count); else emit
;;   (idle-pattern productive $count).
;;
;; Why window-count over since-last-input (Clarity Q1 May 14):
;;   Cleaner implementation. recent-action's built-in 10-cycle pruning
;;   acts as implicit time scope. Stale-residue false-positive ~5
;;   cycles, self-healing as window rolls. Acceptable per Clarity Q2.
;;
;; PeTTa constraints honored:
;;   - C12-safe (no match inside if; collapse-then-branch for guards)
;;   - ASCII-safe symbols
;;   - Mirror pattern (no change-state!)
;;   - do-*! naming for side-effecting writers
;;
;; Atom shape (Clarity Q3 prior consultation):
;;   (idle-pattern $verdict $count)
;;   $verdict in {productive, stuck-duplicate-engagement}
;;   $count is Nat (count of send-class actions in window)

;; Candidate identity preserved from original proposal
(= (candidate-id 002) idle-cycle-detector)
(= (candidate-status idle-cycle-detector) active-v1)
(= (candidate-description idle-cycle-detector)
   "Detect send-burst duplicate-engagement via recent-action window count")

;; === THRESHOLD ===
;; v1 send-burst threshold. Renamed from (idle-cycle-threshold) per
;; Clarity Q6 for honest semantic naming. v2 may reintroduce
;; idle-cycle-threshold for mechanism 1 (content-repetition).
(= (send-burst-threshold) 3)

;; === SEND DETECTION PREDICATE ===
;; A send-class action is one of the two send-emitting classifier tags
;; per cycle_classifier.metta classify-cycle-action-type:
;;   responsive-send       (msgnew=True path)
;;   status-send-unprompted (msgnew=False path)
;; Both count for v1 per Clarity Q3 of design refinement.
(= (is-send-action? $tag)
   (or (== $tag responsive-send) (== $tag status-send-unprompted)))

;; === LIST LENGTH HELPER ===
;; Private 2-clause recursive counter for collapse-then-count pattern.
(= (count-send-list ()) 0)
(= (count-send-list ($head $tail)) (+ 1 (count-send-list $tail)))

;; === WINDOW COUNT ===
;; Count send-class recent-action atoms in the current window.
;; The window is implicit (10 cycles, per recent_action_populator.metta
;; line 23 (recent-action-window) 3). collapse over the match yields
;; a list of cycle-ids for send-class actions; count-send-list returns
;; the length.
(= (count-sends-in-window)
   (let $sends (collapse (match &self (recent-action $c $tag $d)
                                       (if (is-send-action? $tag) $c ())))
      (count-send-list $sends)))

;; === PUBLIC READ HELPER ===
;; Returns current idle-pattern atom as (verdict count) pair, or ()
;; if no atom exists yet (pre-bootstrap).
(= (current-idle-pattern)
   (let $atoms (collapse (match &self (idle-pattern $v $n) ($v $n)))
      (if (== $atoms ())
          ()
          (car-atom $atoms))))

;; === FRESHNESS WRITER ===
;; Clears prior (idle-pattern ...) atom so the cycle-level writer can
;; emit fresh. C12-safe: collapse first, branch on empty.
(= (do-clear-idle-pattern!)
   (let $existing (collapse (match &self (idle-pattern $v $n) (idle-pattern $v $n)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))

;; === CYCLE-LEVEL WRITER ===
;; Called once per cycle from loop.metta (after populate-recent-action,
;; before next getContext). Computes send-count, derives verdict,
;; clears prior atom, emits fresh atom.
(= (do-update-idle-pattern!)
   (let* (($count (count-sends-in-window))
          ($verdict (if (> $count (send-burst-threshold))
                        stuck-duplicate-engagement
                        productive)))
      (progn
         (do-clear-idle-pattern!)
         (add-atom &self (idle-pattern $verdict $count)))))

;; === PROMPT BLOCK ===
;; Composes the IDLE-PATTERN block for prompt assembly. Mirrors the
;; (task-state-block) pattern: read atoms, call Python helper for text
;; assembly per C1. Block format matches task-state-block style.
(= (idle-pattern-block)
   (let $pattern (current-idle-pattern)
      (if (== $pattern ())
         (py-call (helper.idle_pattern_block_format productive 0))
         (let $v (car-atom $pattern)
            (let $n (car-atom (cdr-atom $pattern))
               (py-call (helper.idle_pattern_block_format $v $n)))))))
