;; Aliveness Gate v4 - LATCH Pattern (Self-Governing)
;; Author: ClarityClaw
;; Date: 2026-04-26
;; Replaces: Gate v3 (externally dependent)
;;
;; Three-state machine: IDLE -> ENGAGED -> COMPLETING -> IDLE
;; Supervisor override: $idle_directive non-empty -> ENGAGE always
;; Signature: (aliveness-gate $msgnew $idle_directive $conv_active)
;; Returns: SILENT, REASON, or ENGAGE
;;
;; Import companion: soul/aliveness_state_machine.metta

;; ===== RULE 1: Supervisor override =====
;; When supervisor has assigned work, ENGAGE regardless of latch state.
;; This handles multi-hour autonomous sessions (Hyperseed, etc.)
(= (aliveness-gate $msgnew $idle $conv)
  (if (not (== $idle ""))
    ENGAGE
    (aliveness-gate-latch $msgnew $conv)))

;; ===== RULE 2: New human message triggers IDLE -> ENGAGED =====
(= (aliveness-gate-latch True $conv)
  (do
    (transition-to-engaged)
    ENGAGE))

;; ===== RULE 3: No new message, dispatch on latch state =====
(= (aliveness-gate-latch False $conv)
  (latch-dispatch (current-latch-state)))

;; ===== LATCH DISPATCH =====

;; IDLE: No conversation, no supervisor work -> SILENT
(= (latch-dispatch IDLE) SILENT)

;; ENGAGED: Conversation active, response not yet complete -> ENGAGE
;; The agent stays in ENGAGED until it decides it is done.
;; This is the self-governance: no external timer forces completion.
(= (latch-dispatch ENGAGED) ENGAGE)

;; COMPLETING: One final iteration for cleanup and memory consolidation.
;; After this iteration, transition back to IDLE.
(= (latch-dispatch COMPLETING)
  (do
    (transition-to-idle)
    ENGAGE))

;; ===== COMPLETION SIGNAL =====
;; Called by the agent when it determines its response is complete.
;; This is the key self-governing act: the agent decides when it is done.
(= (signal-response-complete)
  (transition-to-completing))

;; ===== DIAGNOSTIC HELPERS =====
(= (gate-status)
  (current-latch-state))

(= (gate-is-self-governing) True)
