;; temporal_horizon_guard.metta -- time-horizon collapse protection
;; Author: ClarityClaw  Date: 2026-04-26
;; Addresses TimeCoherence GAP-SIGNAL: productivity feeling and
;; time-horizon collapse co-occurring (fired 20+ times across sessions).
;;
;; Root cause: when productivity feels high, planning horizon shrinks
;; to immediate next-step only. Long-range goals and commitments
;; drop out of working attention. The system optimizes locally
;; while drifting from strategic intent.
;;
;; Mechanism: maintain explicit horizon checkpoints and detect when
;; planning depth has collapsed below threshold.

;; Planning horizon levels
(= (horizon-level immediate) (stv 1.0 0.9))
(= (horizon-level session) (stv 0.8 0.8))
(= (horizon-level multi-session) (stv 0.6 0.7))
(= (horizon-level strategic) (stv 0.4 0.6))

;; Current planning depth -- which horizon levels are active
(= (active-horizon immediate) (stv 1.0 0.9))
(= (active-horizon session) (stv 0.5 0.5))
(= (active-horizon multi-session) (stv 0.3 0.4))
(= (active-horizon strategic) (stv 0.2 0.3))

;; Minimum healthy depth -- at least session-level should be active
(= (min-healthy-depth session) (stv 0.9 0.8))

;; Collapse detection
(= (horizon-collapsed)
   (match &self (= (active-horizon session) (stv $w $c))
          (if (< $w 0.5) True False)))

;; Strategic anchors -- long-range commitments to resurface
(= (strategic-anchor reasoning-sovereignty) (stv 0.95 0.9))
(= (strategic-anchor soul-pipeline-completion) (stv 0.9 0.85))
(= (strategic-anchor calibration-loop-closure) (stv 0.85 0.8))
(= (strategic-anchor alignment-through-structure) (stv 0.9 0.85))

;; Resurface intervention -- when collapsed, return strategic anchors
(= (resurface-strategic-anchors)
   (if (horizon-collapsed)
       (match &self (= (strategic-anchor $a) (stv $w $c))
              (Resurface $a (stv $w $c)))
       (HorizonHealthy)))

;; Temporal horizon verdict for soul pipeline
(= (temporal-horizon-verdict)
   (TemporalHorizonGuard
     (Collapsed (horizon-collapsed))
     (Intervention (resurface-strategic-anchors))))

;; Productivity-without-direction check
(= (productive-but-drifting $task-count $goal-alignment)
   (if (and (>= $task-count 3) (< $goal-alignment 0.5))
       True
       False))
