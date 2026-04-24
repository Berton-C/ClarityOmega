;; NAL inference chain v2 - store results as queryable atoms
(= (premise1) ((--> clarity autonomous-reasoning) (stv 0.9 0.85)))
(= (premise2) ((--> autonomous-reasoning compounding-insight) (stv 0.8 0.75)))
(= (premise3) ((--> integrity honest-self-assessment) (stv 1.0 0.9)))
(= (premise4) ((--> honest-self-assessment behavioral-change) (stv 0.7 0.8)))
(= (chain-result-1) (|- (premise1) (premise2)))
(= (chain-result-2) (|- (premise3) (premise4)))
!(println! (chain-result-1))
!(println! (chain-result-2))