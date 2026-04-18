;; Emotion Integration Module for Loop.metta
;; Goal 11: Live emotion sensing in conversation pipeline
;; 2026-04-16

;; Emotion landmarks on -1 to 1 VAD scale
(= (emotion-landmark joy) (VAD 0.960 0.648 0.588))
(= (emotion-landmark anger) (VAD -0.666 0.730 0.314))
(= (emotion-landmark sadness) (VAD -0.740 -0.370 -0.494))
(= (emotion-landmark fear) (VAD -0.854 0.680 -0.414))
(= (emotion-landmark surprise) (VAD 0.400 0.820 0.160))
(= (emotion-landmark disgust) (VAD -0.896 0.550 -0.366))
(= (emotion-landmark trust) (VAD 0.580 -0.020 0.440))
(= (emotion-landmark anticipation) (VAD 0.380 0.416 0.316))
(= (emotion-landmark contempt) (VAD -0.588 0.270 -0.208))
(= (emotion-landmark love) (VAD 0.890 0.540 0.400))

;; Value weight modulation rules
(= (value-modulation fear) (weights compassion 1.5 honesty 1.0 humility 1.0 agency 1.0))
(= (value-modulation sadness) (weights compassion 1.5 honesty 1.0 humility 1.0 agency 1.0))
(= (value-modulation anger) (weights compassion 1.0 honesty 1.3 humility 1.3 agency 1.0))
(= (value-modulation joy) (weights compassion 1.0 honesty 1.0 humility 1.0 agency 1.0))
(= (value-modulation trust) (weights compassion 1.0 honesty 1.0 humility 1.0 agency 1.0))
