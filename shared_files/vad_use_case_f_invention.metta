;; Use Case (f) - Genuinely New Atom Invention
;; Cross-domain composition: VAD perception through soul grounding to response
(= (perceive-compose-respond vad-state) (pipeline (snapshot vad-state) (tone-select vad-state) (gate-check vad-state) (compose vad-state)))
(= (pipeline snapshot tone gate compose) (if (= gate ask-first) (hold-and-ask tone) (flow tone compose)))
(= (emergent-insight vad-gradient optimization-pattern) (new-atom vad-gradient optimization-pattern))
(= (atom-birth-condition) (when-no-existing-atom-fits perceive-compose-respond))
(= (self-extend vad-state soul-state) (if (novel vad-state) (invent-atom vad-state soul-state) (compose-existing vad-state)))
(= (novel vad-state) (no-match (tone-from-vad vad-state)))
(= (invent-atom vad-state soul-state) (remember-new (emergent-insight vad-state soul-state)))
