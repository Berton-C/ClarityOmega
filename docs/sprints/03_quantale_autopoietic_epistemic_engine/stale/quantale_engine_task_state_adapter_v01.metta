;; quantale_engine_task_state_adapter_v01.metta
;; Task State / Capability Registry adapter for the surface-general
;; Quantale Autopoietic Epistemic Dynamics Engine.
;;
;; This module is intentionally surface-specific. It translates Task State
;; action-intention-outcome records into generic qsurface* records. The core
;; engine remains Task-State agnostic.
;;
;; Pure adapter only: no add-atom/remove-atom/set-atom!/write-file.

;; ============================================================
;; 0. Task State surface declaration
;; ============================================================

(: q-task-state-surface-id Atom)
(= q-task-state-surface-id task-state-surface)

(: q-task-state-surface (-> qsurface))
(= (q-task-state-surface)
   (mk-qsurface task-state-surface task-state-surface layer3))

(: q-task-state-adapter-status Atom)
(= q-task-state-adapter-status adapter-emits-generic-surface-contract)

;; ============================================================
;; 1. Task-specific event types
;; ============================================================

(: qtaskevent Type)
(: mk-qtaskevent (-> Atom Atom Atom Atom Atom qtaskevent))
;; shape: cycle event-id intention-kind action-kind outcome-kind

(: q-task-event-cycle (-> qtaskevent Atom))
(= (q-task-event-cycle (mk-qtaskevent $cycle $eid $intention $action $outcome)) $cycle)

(: q-task-event-id (-> qtaskevent Atom))
(= (q-task-event-id (mk-qtaskevent $cycle $eid $intention $action $outcome)) $eid)

(: q-task-intention-kind (-> qtaskevent Atom))
(= (q-task-intention-kind (mk-qtaskevent $cycle $eid $intention $action $outcome)) $intention)

(: q-task-action-kind (-> qtaskevent Atom))
(= (q-task-action-kind (mk-qtaskevent $cycle $eid $intention $action $outcome)) $action)

(: q-task-outcome-kind (-> qtaskevent Atom))
(= (q-task-outcome-kind (mk-qtaskevent $cycle $eid $intention $action $outcome)) $outcome)

(: qtaskwindow Type)
(: mk-qtaskwindow (-> Atom Atom Atom Atom qtaskwindow))
;; shape: surface-id cycle-n cycle-n-plus-1 cycle-n-plus-2

(: q-task-window-surface-id (-> qtaskwindow Atom))
(= (q-task-window-surface-id (mk-qtaskwindow $sid $c0 $c1 $c2)) $sid)

(: q-task-window-start (-> qtaskwindow Atom))
(= (q-task-window-start (mk-qtaskwindow $sid $c0 $c1 $c2)) $c0)

(: q-task-window-middle (-> qtaskwindow Atom))
(= (q-task-window-middle (mk-qtaskwindow $sid $c0 $c1 $c2)) $c1)

(: q-task-window-end (-> qtaskwindow Atom))
(= (q-task-window-end (mk-qtaskwindow $sid $c0 $c1 $c2)) $c2)

;; ============================================================
;; 2. Translation into generic surface records
;; ============================================================

(: q-task-event-as-surface-event (-> qtaskevent qsurfaceevent))
(= (q-task-event-as-surface-event (mk-qtaskevent $cycle $eid $intention $action $outcome))
   (mk-qsurfaceevent task-state-surface $eid action-intention-outcome $cycle))

(: q-task-event-as-surface-candidate (-> qtaskevent qsurfacecandidate))
(= (q-task-event-as-surface-candidate (mk-qtaskevent $cycle $eid $intention $action $outcome))
   (mk-qsurfacecandidate task-state-surface $eid task-state-lineage-candidate))

(: q-task-lineage-status (-> qtaskevent Atom))
(= (q-task-lineage-status (mk-qtaskevent $cycle $eid no-intention $action $outcome)) intention-missing)
(= (q-task-lineage-status (mk-qtaskevent $cycle $eid $intention no-action $outcome)) action-missing)
(= (q-task-lineage-status (mk-qtaskevent $cycle $eid $intention $action no-outcome)) outcome-missing)
(= (q-task-lineage-status (mk-qtaskevent $cycle $eid $intention $action $outcome)) lineage-visible)

(: q-task-event-as-surface-lineage (-> qtaskevent qsurfacelineage))
(= (q-task-event-as-surface-lineage (mk-qtaskevent $cycle $eid $intention $action $outcome))
   (mk-qsurfacelineage $eid action-intention-outcome-lineage
                       (q-task-lineage-status (mk-qtaskevent $cycle $eid $intention $action $outcome))))

(: q-task-soul-visibility-status (-> qtaskevent Atom))
(= (q-task-soul-visibility-status $event)
   (if (== (q-task-lineage-status $event) lineage-visible)
       lineage-visible
       lineage-partial))

(: q-task-event-as-surface-visibility (-> qtaskevent qsurfacevisibility))
(= (q-task-event-as-surface-visibility (mk-qtaskevent $cycle $eid $intention $action $outcome))
   (mk-qsurfacevisibility $eid (q-task-soul-visibility-status (mk-qtaskevent $cycle $eid $intention $action $outcome))))

(: q-task-event-as-surface-revisability (-> qtaskevent qsurfacerevisability))
(= (q-task-event-as-surface-revisability (mk-qtaskevent $cycle $eid $intention $action $outcome))
   (mk-qsurfacerevisability $eid revisable))

(: q-task-uptake-status (-> qtaskevent Atom))
(= (q-task-uptake-status (mk-qtaskevent $cycle $eid $intention $action success-outcome)) candidate-uptake)
(= (q-task-uptake-status (mk-qtaskevent $cycle $eid $intention $action failed-outcome)) evidence-for-revision)
(= (q-task-uptake-status (mk-qtaskevent $cycle $eid $intention $action no-outcome)) insufficient-window)
(= (q-task-uptake-status (mk-qtaskevent $cycle $eid $intention no-action $outcome)) action-missing)
(= (q-task-uptake-status (mk-qtaskevent $cycle $eid no-intention $action $outcome)) intention-missing)

(: q-task-event-as-surface-uptake (-> qtaskevent qsurfaceuptake))
(= (q-task-event-as-surface-uptake (mk-qtaskevent $cycle $eid $intention $action $outcome))
   (mk-qsurfaceuptake $eid (q-task-uptake-status (mk-qtaskevent $cycle $eid $intention $action $outcome))))

(: q-task-capacity-delta (-> qtaskevent Atom))
(= (q-task-capacity-delta (mk-qtaskevent $cycle $eid $intention $action success-outcome)) future-capacity-candidate)
(= (q-task-capacity-delta (mk-qtaskevent $cycle $eid $intention $action failed-outcome)) future-capacity-unknown)
(= (q-task-capacity-delta (mk-qtaskevent $cycle $eid $intention $action no-outcome)) future-capacity-insufficient-window)

(: q-task-event-as-surface-capacity (-> qtaskevent qsurfacecapacity))
(= (q-task-event-as-surface-capacity (mk-qtaskevent $cycle $eid $intention $action $outcome))
   (mk-qsurfacecapacity $eid (q-task-capacity-delta (mk-qtaskevent $cycle $eid $intention $action $outcome))))

;; ============================================================
;; 3. Capability Registry handoff markers
;; ============================================================

(: qtaskcapability Type)
(: mk-qtaskcapability (-> Atom Atom Atom Atom qtaskcapability))
;; shape: cycle event-id capability-name capability-result

(: q-task-capability-surface-candidate (-> qtaskcapability qsurfacecandidate))
(= (q-task-capability-surface-candidate (mk-qtaskcapability $cycle $eid $cap $result))
   (mk-qsurfacecandidate task-state-surface $eid capability-outcome-candidate))

(: q-task-capability-evidence (-> qtaskcapability qsurfaceevidence))
(= (q-task-capability-evidence (mk-qtaskcapability $cycle $eid $cap capability-confirmed))
   (mk-qsurfaceevidence $eid (mk-pbit 1.0 0.1) (mk-pbit 0.0 0.1) capability-confirmed))
(= (q-task-capability-evidence (mk-qtaskcapability $cycle $eid $cap capability-disconfirmed))
   (mk-qsurfaceevidence $eid (mk-pbit 0.0 0.1) (mk-pbit 1.0 0.1) capability-disconfirmed))
(= (q-task-capability-evidence (mk-qtaskcapability $cycle $eid $cap capability-mixed))
   (mk-qsurfaceevidence $eid (mk-pbit 0.6 0.1) (mk-pbit 0.6 0.1) capability-mixed))

;; Stable writer schemas for runtime adapters. Comments only.
;;   ((--> (task-intention-event $cycle) $intention-kind) (stv 1.0 $conf))
;;   ((--> (task-action-event $cycle) $action-kind) (stv 1.0 $conf))
;;   ((--> (task-outcome-event $cycle) $outcome-kind) (stv 1.0 $conf))
;;   ((--> (task-capability-used $cycle) $capability-name) (stv 1.0 $conf))
;;   ((--> (surface-candidate task-state-surface $candidate-id) task-state-lineage-candidate) (stv 1.0 $conf))
