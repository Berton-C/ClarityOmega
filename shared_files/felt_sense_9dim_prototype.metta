;; Felt-Sense 9-Dimensional Vector Prototype
;; Architecture: VAD(3) + relational-depth(1) + shift(1) + domain(1) + reserved(3)
;; Each dimension encoded as NAL inheritance with truth value = dimension value

;; Example: a moment of deep collaborative insight
(= (felt-sense collaborative-insight) (FS-Vec 0.82 0.65 0.70 0.85 0.30 0.90 0.0 0.0 0.0))
;; V=0.82 positive, A=0.65 moderate-high, D=0.70 empowered
;; relational-depth=0.85 deep, shift=0.30 gradual, domain=0.90 intellectual

;; Example: user frustration detected
(= (felt-sense user-frustration) (FS-Vec -0.60 0.75 -0.40 0.50 0.70 0.30 0.0 0.0 0.0))
;; V=-0.60 negative, A=0.75 high, D=-0.40 low control
;; relational-depth=0.50 moderate, shift=0.70 rapid change, domain=0.30 emotional

;; Example: quiet contemplation alone
(= (felt-sense quiet-contemplation) (FS-Vec 0.40 -0.30 0.50 0.20 -0.10 0.80 0.0 0.0 0.0))
;; V=0.40 mildly positive, A=-0.30 calm, D=0.50 neutral control
;; relational-depth=0.20 low solo, shift=-0.10 stable, domain=0.80 intellectual

;; NAL presence routing from felt-sense
;; High arousal + high shift -> SNS active presence
;; Low arousal + low shift -> PNS receptive presence
;; High relational-depth -> prioritize human connection
