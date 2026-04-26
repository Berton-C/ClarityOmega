;; Aliveness Gate V2 - Latch Pattern
;; Fix: multi-iteration conversation via conversation_active latch

;; State atoms
(= (&conversation_active) False)
(= (&soul_ack_sent) False)
(= (&wake_counter) 0)

;; Rule 1: msgnew=True activate latch
(= (aliveness-gate-v2 True $idle)
   (do-activate-conversation))

;; Rule 2: msgnew=False check latch state
(= (aliveness-gate-v2 False $idle)
   (if (== (match &self (= (&conversation_active) $v) $v) True)
       (if (== (match &self (= (&soul_ack_sent) $v) $v) True)
           (do-reset-silent)
           (do-engage-decrement))
       (check-idle $idle)))

;; Rule 3: idle check
(= (check-idle $idle)
   (if (== $idle empty) SILENT ENGAGE))

;; Python: after send executes add soul_ack_sent=True to AtomSpace
