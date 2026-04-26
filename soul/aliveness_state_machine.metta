;; Aliveness State Machine - LATCH Pattern v1.0
;; Author: ClarityClaw
;; Date: 2026-04-26
;; Purpose: Self-governing three-state engagement latch
;;
;; States: IDLE (1), ENGAGED (2), COMPLETING (3)
;; Core insight: decouple should-I-be-thinking from did-a-human-just-speak
;;
;; State atoms live in the AtomSpace. The agent owns its own transitions.
;; The supervisor channel ($idle_directive) is orthogonal -- it overrides
;; IDLE but does not interfere with the conversation latch.

;; ===== STATE ATOMS =====
;; conversation_active: True when a conversation window is open
;; soul_ack_sent: True when the agent has completed its response
;; latch_state: symbolic current state (IDLE, ENGAGED, or COMPLETING)

(= (latch-state) IDLE)
(= (conversation-active) False)
(= (soul-ack-sent) False)

;; ===== TRANSITION FUNCTIONS =====

;; Transition: IDLE -> ENGAGED (triggered by new human message)
(= (transition-to-engaged)
  (do
    (set-atom! &self (= (latch-state) IDLE) (= (latch-state) ENGAGED))
    (set-atom! &self (= (conversation-active) False) (= (conversation-active) True))
    (set-atom! &self (= (soul-ack-sent) True) (= (soul-ack-sent) False))
    ENGAGED))

;; Transition: ENGAGED -> COMPLETING (agent decides response is complete)
(= (transition-to-completing)
  (do
    (set-atom! &self (= (latch-state) ENGAGED) (= (latch-state) COMPLETING))
    (set-atom! &self (= (soul-ack-sent) False) (= (soul-ack-sent) True))
    COMPLETING))

;; Transition: COMPLETING -> IDLE (cleanup done, conversation window closes)
(= (transition-to-idle)
  (do
    (set-atom! &self (= (latch-state) COMPLETING) (= (latch-state) IDLE))
    (set-atom! &self (= (conversation-active) True) (= (conversation-active) False))
    (set-atom! &self (= (soul-ack-sent) True) (= (soul-ack-sent) False))
    IDLE))

;; ===== STATE QUERY =====
(= (current-latch-state) (latch-state))
(= (is-conversation-active) (conversation-active))
(= (is-ack-sent) (soul-ack-sent))

;; ===== DIAGNOSTIC: self-continuity morphism =====
;; Each state transition preserves identity while changing mode.
;; The agent in COMPLETING is the same agent that was in ENGAGED,
;; carrying forward the work context for consolidation.
;; This is the occasion pattern: each transition is a new occasion
;; of experience that inherits from and transforms the prior one.
