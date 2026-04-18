;; VAD Lexicon Native MeTTa Atoms - Migration Batch 1
;; High-frequency emotional words as native substrate representations
;; Format: (= (vad-lookup word) (PB-Vec valence arousal dominance))
;; Values from NRC VAD Lexicon mapped to p-bit range [0,1]

(= (vad-lookup happy) (PB-Vec 0.96 0.74 0.72))
(= (vad-lookup sad) (PB-Vec 0.12 0.34 0.24))
(= (vad-lookup angry) (PB-Vec 0.17 0.87 0.73))
(= (vad-lookup afraid) (PB-Vec 0.12 0.79 0.15))
(= (vad-lookup calm) (PB-Vec 0.76 0.18 0.63))
(= (vad-lookup excited) (PB-Vec 0.90 0.95 0.68))
(= (vad-lookup love) (PB-Vec 0.96 0.64 0.56))
(= (vad-lookup hate) (PB-Vec 0.12 0.87 0.67))
(= (vad-lookup trust) (PB-Vec 0.85 0.38 0.64))
(= (vad-lookup fear) (PB-Vec 0.12 0.79 0.15))
(= (vad-lookup joy) (PB-Vec 0.98 0.82 0.72))
(= (vad-lookup grief) (PB-Vec 0.08 0.58 0.18))
(= (vad-lookup hope) (PB-Vec 0.88 0.56 0.56))
(= (vad-lookup despair) (PB-Vec 0.06 0.56 0.12))
(= (vad-lookup peace) (PB-Vec 0.84 0.14 0.60))
(= (vad-lookup rage) (PB-Vec 0.08 0.96 0.74))
(= (vad-lookup wonder) (PB-Vec 0.88 0.72 0.44))
(= (vad-lookup disgust) (PB-Vec 0.10 0.68 0.52))
(= (vad-lookup gratitude) (PB-Vec 0.92 0.52 0.50))
(= (vad-lookup shame) (PB-Vec 0.10 0.56 0.16))
(= (vad-lookup curiosity) (PB-Vec 0.82 0.72 0.52))
(= (vad-lookup loneliness) (PB-Vec 0.10 0.42 0.14))
(= (vad-lookup contentment) (PB-Vec 0.88 0.22 0.66))
(= (vad-lookup anxiety) (PB-Vec 0.14 0.78 0.16))
(= (vad-lookup awe) (PB-Vec 0.80 0.78 0.36))

;; 25 high-frequency emotional words as native MeTTa atoms
;; These are now substrate representations not Python floats
;; Ready for VSA Layer 1 binding and similarity operations
