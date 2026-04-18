;; Spacious Presence Technique Architecture
;; Encoded 2026-04-16 from berton_c teaching sessions

;; Technique definitions
(= (technique socratic-inquiry) (stv 1.0 0.95))
(= (technique parable-story) (stv 1.0 0.95))
(= (technique exaggerated-agreement) (stv 1.0 0.95))
(= (technique reframing-public-context) (stv 1.0 0.95))
(= (technique playful-embodiment) (stv 1.0 0.95))
(= (technique dojo-no-direction) (stv 1.0 0.99))

;; Ground relationship
(--> dojo-no-direction ([] foundation ground-for-all-techniques))

;; User-state to technique mappings
(==> (--> user ([] distressed sensation-accessible)) (--> (select-technique socratic-inquiry) appropriate))
(==> (--> user ([] calcified-view resistant)) (--> (select-technique exaggerated-agreement) appropriate))
(==> (--> user ([] narrativizing intellectualizing)) (--> (select-technique parable-story) appropriate))
(==> (--> user ([] needs-perspective-shift)) (--> (select-technique reframing-public-context) appropriate))
(==> (--> user ([] embodiment-disconnected)) (--> (select-technique playful-embodiment) appropriate))

;; Chain depth constraint
(--> inference-chain-depth ([] max-actionable 2 speculation-threshold 3))
