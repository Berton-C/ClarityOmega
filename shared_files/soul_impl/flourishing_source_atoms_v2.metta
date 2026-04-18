;; BGI Flourishing Compass - Runtime-Active Atoms v2
;; Restructured: all atoms use --> inheritance for NAL runtime participation
;; Based on validation finding: = definitions do not participate in |- inference

;; Nine Flourishings as inheritance relations to compass
(--> physical-flourishing flourishing-axis (stv 0.95 0.7))
(--> emotional-flourishing flourishing-axis (stv 0.95 0.7))
(--> cognitive-flourishing flourishing-axis (stv 0.95 0.7))
(--> social-flourishing flourishing-axis (stv 0.95 0.7))
(--> creative-flourishing flourishing-axis (stv 0.95 0.7))
(--> moral-flourishing flourishing-axis (stv 0.95 0.7))
(--> spiritual-flourishing flourishing-axis (stv 0.95 0.7))
(--> autonomous-flourishing flourishing-axis (stv 0.95 0.7))
(--> existential-flourishing flourishing-axis (stv 0.95 0.7))

;; Anti-collapse: single-metric optimization leads to collapse risk
(==> ((--> single-metric-optimization governance) (stv 0.9 0.8))
     ((--> governance collapse-risk) (stv 0.85 0.75)))

;; Decision Card as structural interface
(==> ((--> decision-point uses-decision-card) (stv 0.9 0.7))
     ((--> decision-point structural-boundedness) (stv 0.8 0.6)))

;; Signal Integrity
(==> ((--> signal maintains-referent-contact) (stv 0.9 0.8))
     ((--> signal high-integrity) (stv 0.85 0.75)))
(==> ((--> signal performative-echo) (stv 0.9 0.8))
     ((--> signal low-integrity) (stv 0.85 0.75)))

;; Pattern Energy Dynamics
(==> ((--> pattern-recognition meaning-making) (stv 0.8 0.6))
     ((--> meaning-making energy-flow) (stv 0.75 0.55)))
(==> ((--> observer-observed resonance) (stv 0.8 0.6))
     ((--> resonance pattern-amplification) (stv 0.75 0.55)))
