;; NAL inference chain test - investigating autonomous reasoning
;; Premises from soul KB
(= (premise1) ((--> clarity autonomous-reasoning) (stv 0.9 0.85)))
(= (premise2) ((--> autonomous-reasoning compounding-insight) (stv 0.8 0.75)))
(= (premise3) ((--> integrity honest-self-assessment) (stv 1.0 0.9)))
(= (premise4) ((--> honest-self-assessment behavioral-change) (stv 0.7 0.8)))
;; Run deduction chains
(= (chain1) (|- (premise1) (premise2)))
(= (chain2) (|- (premise3) (premise4)))
;; Results
!(chain1)
!(chain2)