;; LATCH Pattern Implementation for Aliveness Gate
;; Author: ClarityClaw
;; Date: 2026-04-26
;; Purpose: Self-governing engagement window management
;;
;; This replaces the single-signal MESSAGE-IS-NEW gate with a
;; two-atom latch that sustains engagement across iterations.

;; === STATE ATOMS ===
;; conversation_active: latches ON when human message arrives,
;; stays ON until ClarityClaw signals completion.
;; soul_ack_sent: tracks whether response is complete.

(= (conversation_active) False)
(= (soul_ack_sent) False)

;; === LATCH GATE FUNCTION ===
;; Returns ENGAGE or SILENT based on latch state.

(= (latch-gate $msgnew)
   (if (== $msgnew True)
       (let () (set-latch-on) ENGAGE)
       (if (== (conversation_active) True)
           (if (== (soul_ack_sent) False)
               ENGAGE
               (let () (set-latch-off) ENGAGE))
           SILENT)))

;; === LATCH CONTROL ===

(= (set-latch-on)
   (do (remove-atom &self (= (conversation_active) False))
       (add-atom &self (= (conversation_active) True))
       (remove-atom &self (= (soul_ack_sent) True))
       (add-atom &self (= (soul_ack_sent) False))))

(= (set-latch-off)
   (do (remove-atom &self (= (conversation_active) True))
       (add-atom &self (= (conversation_active) False))))

(= (signal-ack-sent)
   (do (remove-atom &self (= (soul_ack_sent) False))
       (add-atom &self (= (soul_ack_sent) True))))

;; === USAGE ===
;; Call (latch-gate $msgnew) where $msgnew is True/False.
;; When response is complete, call (signal-ack-sent).
;; Next iteration: gate sees ack=True, runs one more cycle, then deactivates.
;;
;; KEY ADVANTAGE OVER GATE V2:
;; No external idle_directive needed. The agent self-regulates.
;; Engagement tracks actual conversation state, not external signals.
;; Trust requirement: agent must call signal-ack-sent when truly done.
