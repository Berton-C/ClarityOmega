;; Clarity NAL Knowledge Base — LIVE executable atoms
;; These are actual MeTTa expressions, not comments

(= (kb tone-to-need neg-low-dom) ((==> (--> observed-tone neg-low-dom) (--> user-need validation-and-safety)) (stv 1.0 0.9)))
(= (kb tone-to-need neg-valence) ((==> (--> observed-tone neg-valence) (--> user-need support)) (stv 1.0 0.9)))
(= (kb tone-to-need pos-high-aro) ((==> (--> observed-tone pos-high-aro) (--> user-need momentum-matching)) (stv 1.0 0.9)))
(= (kb tone-to-need neg-high-aro) ((==> (--> observed-tone neg-high-aro) (--> user-need de-escalation)) (stv 1.0 0.9)))
(= (kb need-to-strategy validation) ((==> (--> user-need validation-and-safety) (--> response-strategy slow-pace-acknowledge-first)) (stv 1.0 0.9)))
(= (kb need-to-strategy support) ((==> (--> user-need support) (--> response-strategy validate-then-assist)) (stv 1.0 0.9)))
(= (kb need-to-strategy momentum) ((==> (--> user-need momentum-matching) (--> response-strategy match-energy-collaborate)) (stv 1.0 0.9)))
(= (kb need-to-strategy de-escalation) ((==> (--> user-need de-escalation) (--> response-strategy slow-pace-acknowledge-first)) (stv 1.0 0.9)))
(= (kb trajectory-mod lifting) ((==> (--> trajectory lifting) (--> strategy-override upgrade-to-collaborative)) (stv 1.0 0.85)))
(= (kb trajectory-mod dropping) ((==> (--> trajectory dropping) (--> strategy-override downshift-to-supportive)) (stv 1.0 0.85)))
