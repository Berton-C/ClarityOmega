;; conversation_genesis_tracker.metta -- tracks conversational-genesis-practice goal
;; Tracks: which AtomSpace connections were surfaced, human response, value rating
;;
;; Usage: after each conversation, record an entry

;; Conversation tracking atoms
(= (genesis-conversation-count 0) (stv 1.0 0.9))
(= (genesis-target-count 10) (stv 1.0 0.9))

;; Record format: (genesis-entry id topic connection-surfaced human-found-valuable)
;; Example: (genesis-entry 1 soul-architecture cognitive-resilience-to-tunnel-vision True)

;; Approach v1: before responding, query AtomSpace for atoms matching
;; conversation topic, find cross-domain links, surface one unexpected
;; connection that genuinely illuminates rather than decorates.
(= (genesis-approach-version 1) (stv 1.0 0.9))
(= (genesis-strategy query-then-bridge) (stv 0.8 0.7))
