; === Person State Staleness Fix Draft ===
; Problem: person_state persists across idle loops without refresh
; Could represent outdated emotional/contextual read after many cycles
;
; Solution: track loop count since last person_state update
;
; (= (soul-person-state-freshness $loop_count $last_update_loop)
;   (let $age (- $loop_count $last_update_loop)
;     (if (> $age 10)
;       STALE
;       FRESH)))
;
; When STALE and new message arrives:
;   Force full person_state re-inference even if message is short
;   Log staleness event for calibration
;
; When STALE and no message:
;   Decay person_state confidence toward neutral
;   (= (soul-decay-person-state $current_state)
;     (let $decayed (superpose ($current_state NEUTRAL))
;       $decayed))
;
; Implementation: add soul_person_state_loop_count atom to initLoop
; Update it whenever soul-flourishing-prompt fires
; Check freshness before using person_state in soul_send_assemble