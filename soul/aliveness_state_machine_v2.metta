;; Aliveness State Machine - LATCH Pattern v2.0
;; Author: ClarityClaw
;; Date: 2026-04-27
;; Purpose: Self-governing three-state engagement latch using set-atom!
;; Requires: set_atom_impl.metta (Patrick Hammer, 2026-04-27)
;;
;; KEY CHANGE from v1: States are atoms in the AtomSpace, not opaque variables.
;; This means match queries can find current state, and the genesis engine
;; can cross-reference regulatory state with reasoning atoms.
;;
;; States: IDLE, ENGAGED, COMPLETING

;; ===== IMPORT set-atom! =====
;; (import set_atom_impl.metta) -- or inline if import not available:
(: set-atom! (-> Atom Expression Expression Atom))
(= (set-atom! $space $atom1 $atom2)
   (progn (remove-atom $space $atom1)
          (add-atom $space $atom2)))

;; ===== STATE ATOMS (queryable via match) =====
(= (latch-state current) IDLE)
(= (conversation-active current) False)
(= (soul-ack-sent current) False)

;; ===== TRANSITION: IDLE -> ENGAGED =====
(= (transition-to-engaged)
  (progn
    (set-atom! &self (= (latch-state current) IDLE) (= (latch-state current) ENGAGED))
    (set-atom! &self (= (conversation-active current) False) (= (conversation-active current) True))
    (set-atom! &self (= (soul-ack-sent current) True) (= (soul-ack-sent current) False))
    ENGAGED))

;; ===== TRANSITION: ENGAGED -> COMPLETING =====
(= (transition-to-completing)
  (progn
    (set-atom! &self (= (latch-state current) ENGAGED) (= (latch-state current) COMPLETING))
    (set-atom! &self (= (soul-ack-sent current) False) (= (soul-ack-sent current) True))
    COMPLETING))

;; ===== TRANSITION: COMPLETING -> IDLE =====
(= (transition-to-idle)
  (progn
    (set-atom! &self (= (latch-state current) COMPLETING) (= (latch-state current) IDLE))
    (set-atom! &self (= (conversation-active current) True) (= (conversation-active current) False))
    (set-atom! &self (= (soul-ack-sent current) True) (= (soul-ack-sent current) False))
    IDLE))

;; ===== QUERYABLE STATE (the whole point of v2) =====
;; (match &self (= (latch-state current) $s) $s) => returns IDLE/ENGAGED/COMPLETING
;; (match &self (= (conversation-active current) $v) $v) => returns True/False
;; Genesis engine can now sample these as domain-7 atoms.

;; ===== TEMPORAL JOURNALING (future: each transition logs) =====
;; (= (state-journal-entry) (transition IDLE ENGAGED timestamp))
;; Pattern: add-atom after each transition for audit trail.
