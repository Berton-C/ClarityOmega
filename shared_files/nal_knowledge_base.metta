;; Clarity Emotional Tone NAL Knowledge Base
;; All reasoning rules as MeTTa atoms — no Python logic

;; Layer 1: Observed tone -> User need
;; (==> (--> observed-tone neg-low-dom) (--> user-need validation-and-safety)) (stv 1.0 0.9)
;; (==> (--> observed-tone neg-valence) (--> user-need support)) (stv 1.0 0.9)
;; (==> (--> observed-tone pos-high-aro) (--> user-need momentum-matching)) (stv 1.0 0.9)
;; (==> (--> observed-tone neg-high-aro) (--> user-need de-escalation)) (stv 1.0 0.9)

;; Layer 2: User need -> Response strategy
;; (==> (--> user-need validation-and-safety) (--> response-strategy slow-pace-acknowledge-first)) (stv 1.0 0.9)
;; (==> (--> user-need support) (--> response-strategy validate-then-assist)) (stv 1.0 0.9)
;; (==> (--> user-need momentum-matching) (--> response-strategy match-energy-collaborate)) (stv 1.0 0.9)
;; (==> (--> user-need de-escalation) (--> response-strategy slow-pace-acknowledge-first)) (stv 1.0 0.9)

;; Layer 3: Trajectory modifiers
;; (==> (--> trajectory lifting) (--> strategy-override upgrade-to-collaborative)) (stv 1.0 0.85)
;; (==> (--> trajectory dropping) (--> strategy-override downshift-to-supportive)) (stv 1.0 0.85)

;; Proven confidence propagation examples:
;; neg-low-dom(0.8) -> validation-need(0.72) -> slow-pace(0.648)
;; pos-high-aro(0.85) -> momentum(0.765) -> match-energy(0.6885)
;; Revision: slow-pace(0.648) + slow-pace(0.506) -> slow-pace(0.741)

;; CONFIRMED NAL MODES (2026-04-17 12:34)
;; DEDUCTION REVISION ABDUCTION INDUCTION all proven live via |- operator
