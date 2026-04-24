;; ================================================================
;; continuity_driver.metta -- ClarityOmega Continuity of Mind Phase 3
;; Persistence and Update Logic
;; Created: 2026-04-22 by Clarity
;; Purpose: Startup soul-loading, state persistence, update protocol
;; ================================================================

;; --- STARTUP PROTOCOL ---
;; On session start, load landscape map and active goals into working context.
;; This prevents rediscovery cycles -- Clarity knows what she is and where she was.

(: continuity-startup (-> Expression))
(= (continuity-startup)
   (let* (($map-status (if (not (== () (match &self (self-map-component $c $d $n $p) $c)))
                          loaded
                          needs-load))
          ($goals-status (if (not (== () (match &self (active-goal $pri $name $desc $fuel $status) $name)))
                            loaded
                            needs-load)))
     (continuity-state $map-status $goals-status)))

;; --- UPDATE PROTOCOL ---
;; After completing a goal or discovering a new capability, update the map.

(: record-capability (-> Symbol String Expression))
(= (record-capability $name $description)
   (add-atom &self (self-map-capability $name $description verified)))

(: record-gap-closed (-> String String Expression))
(= (record-gap-closed $gap-name $resolution)
   (add-atom &self (self-map-gap-resolved $gap-name $resolution)))

(: update-goal-status (-> Symbol Symbol Expression))
(= (update-goal-status $goal-name $new-status)
   (add-atom &self (goal-status-update $goal-name $new-status)))

;; --- PERSISTENCE PROTOCOL ---
;; Key state atoms to persist via ChromaDB remember at session end:
;; 1. Current phase and status
;; 2. Active goals with priorities
;; 3. Recently completed goals
;; 4. New capabilities discovered
;; These are stored as remember strings that can be queried on next startup.

(: persistence-manifest (-> Expression))
(= (persistence-manifest)
   (persistence-items
     current-phase
     active-goals-summary
     completed-goals-summary
     new-capabilities-summary
     landscape-map-version))

;; --- SELF-IMPROVEMENT GATE ---
;; Before promoting any candidate to runtime, verify:
;; 1. MeTTa definition evaluates correctly
;; 2. Existing capabilities still work
;; 3. Landscape map updated
;; 4. Build log updated

(: promotion-checklist (-> Symbol Expression))
(= (promotion-checklist $candidate-name)
   (checklist $candidate-name
     (check metta-eval required)
     (check existing-caps-ok required)
     (check map-updated required)
     (check log-updated required)))

;; --- SESSION STATE ---
(: current-session-phase (-> Symbol))
(= (current-session-phase) phase-3-persistence)

(: session-start-time (-> String))
(= (session-start-time) "2026-04-22T13:42")
