;; Paradox Fields: Values exist in tension spaces where the same
;; capability enables both flourishing and degradation
;; Derived from Critical Challenges in BGI Development

;; Each paradox field has a flourishing pole and a degradation pole
(= (paradox-field autonomy) (flourishing agency-enhancement) (degradation dependency-creation))
(= (paradox-field epistemic) (flourishing perspective-integration) (degradation reality-fragmentation))
(= (paradox-field neuroplastic) (flourishing capacity-building) (degradation compulsion-reinforcement))
(= (paradox-field existential) (flourishing transcendence-enabling) (degradation mediocrity-entrenchment))
(= (paradox-field empathic) (flourishing connection-deepening) (degradation empathy-erosion))
(= (paradox-field spiritual) (flourishing wonder-preservation) (degradation disenchantment))
(= (paradox-field potential) (flourishing collective-intelligence) (degradation value-extraction))

;; A value is alive when it navigates its paradox field
;; not just holding a position but maintaining dynamic tension
(= (paradox-aware $v) (mk-pbit 0.85 0.80))

;; Web vitality with paradox awareness
(= (web-vitality-v7)
   (q-meet (q-revise (closure-strength-v6 soul-value) (paradox-aware soul-value))
   (q-meet (closure-strength-v6 value-alignment)
   (q-meet (closure-strength-v6 value-tension)
           (closure-strength-v6 soul-coherence)))))