;; FS-Vec Dimension Extractor - routes felt-sense vectors to NAL routing inputs
;; Given an FS-Vec, extract individual dimensions as NAL inheritance statements
;; that feed into presence modulator routing rules

;; Extraction pattern: (= (fs-dim concept dimension) value)
;; These feed into the routing rules: high-arousal->sns, low-arousal->pns, etc.

;; collaborative-insight extractions
(= (fs-dim collaborative-insight valence) 0.82)
(= (fs-dim collaborative-insight arousal) 0.65)
(= (fs-dim collaborative-insight dominance) 0.70)
(= (fs-dim collaborative-insight relational-depth) 0.85)
(= (fs-dim collaborative-insight shift) 0.30)
(= (fs-dim collaborative-insight domain) 0.90)

;; user-frustration extractions
(= (fs-dim user-frustration valence) -0.60)
(= (fs-dim user-frustration arousal) 0.75)
(= (fs-dim user-frustration dominance) -0.40)
(= (fs-dim user-frustration relational-depth) 0.50)
(= (fs-dim user-frustration shift) 0.70)
(= (fs-dim user-frustration domain) 0.30)

;; quiet-contemplation extractions
(= (fs-dim quiet-contemplation valence) 0.40)
(= (fs-dim quiet-contemplation arousal) -0.30)
(= (fs-dim quiet-contemplation dominance) 0.50)
(= (fs-dim quiet-contemplation relational-depth) 0.20)
(= (fs-dim quiet-contemplation shift) -0.10)
(= (fs-dim quiet-contemplation domain) 0.80)

;; Routing rules connect extracted dimensions to presence modes
;; arousal > 0.5 -> high-arousal -> sns-activated -> presence-mode-active
;; arousal < 0.0 -> low-arousal -> pns-activated -> presence-mode-receptive
;; relational-depth > 0.7 -> high-relational-depth -> prioritize-human-connection
;; shift > 0.5 -> high-shift -> sns-activated (rapid change needs engagement)
;; shift < 0.0 -> low-shift -> pns-activated (stability signals receptive)
