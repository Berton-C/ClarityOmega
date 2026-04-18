;; Cross-Composition Test - Bridging All Use Cases
;; Full pipeline: perceive -> map -> select-tone -> gate -> compose -> respond
(= (full-pipeline vad-state history) (let* ((snapshot (current vad-state)) (gradient (compare snapshot history)) (optimizing (optimizing-for gradient)) (tone (tone-from-vad snapshot)) (register (pns-register tone)) (techniques (techniques-available tone)) (permitted (gate-check techniques)) (phrase (landscape-phrase snapshot))) (compose-final tone register permitted phrase)))
(= (compose-final tone register permitted phrase) (if (= permitted ask-first) (ask-then-compose tone register phrase) (direct-compose tone register phrase)))
(= (ask-then-compose tone register phrase) (prepend-permission-request (direct-compose tone register phrase)))
(= (direct-compose tone register phrase) (llm-instruction tone register phrase))
;; Self-extension trigger
(= (should-self-extend vad-state) (if (novel vad-state) True False))
(= (extend-and-remember vad-state soul-state) (remember-new (emergent-insight vad-state soul-state)))
