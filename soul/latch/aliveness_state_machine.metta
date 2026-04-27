;; LATCH Aliveness State Machine v3
;; Migrated from change-state!/get-state to set-atom! (queryable state atoms)
;; State lives as atoms in &self, queryable via match
;; set-atom! implementation: remove-atom old + add-atom new
;;
;; Migration rationale (from MeTTa spec analysis 2026-04-27):
;;   match &self is a special form -- direct space query, no type_cast gating
;;   State-as-atoms means other modules can pattern-match on latch state
;;   This enables state-aware genesis encounters (build path 2)
;;   and temporal state journaling (build path 3)

;; Import set-atom! implementation
;; set_atom_impl imported via lib_clarity_reasoning.metta import chain

;; Initialize state atom -- IDLE is the ground state
!(add-atom &self (latch-state IDLE))

;; ============================================================
;; State Query
;; ============================================================
;; Returns current state via direct space match
(= (current-latch-state)
   (match &self (latch-state $s) $s))

;; ============================================================
;; Raw Transition (unsafe -- no guard)
;; ============================================================
;; Replaces (latch-state $from) with (latch-state $to) in &self
(= (raw-transition $from $to)
   (set-atom! &self (latch-state $from) (latch-state $to)))

;; ============================================================
;; Guarded Transition
;; ============================================================
;; Only transitions if current state matches expected $from
;; Returns new state on success, current state on failure
(= (guarded-transition $from $to)
   (if (== (current-latch-state) $from)
       (raw-transition $from $to)
       (current-latch-state)))

;; ============================================================
;; Semantic Transitions (the public API)
;; ============================================================
(= (engage-from-idle)
   (guarded-transition IDLE ENGAGED))

(= (complete-from-engaged)
   (guarded-transition ENGAGED COMPLETING))

(= (idle-from-completing)
   (guarded-transition COMPLETING IDLE))

;; ============================================================
;; State Predicates (for external module queries)
;; ============================================================
(= (is-idle?) (== (current-latch-state) IDLE))
(= (is-engaged?) (== (current-latch-state) ENGAGED))
(= (is-completing?) (== (current-latch-state) COMPLETING))
