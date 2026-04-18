;; Conversation Turn VAD Extraction Loop
;; Architecture: user utterance -> word-level VAD lookup -> aggregate -> FS-Vec -> NAL routing
;; This is the real-time pipeline connecting lexicon grounding to presence modulation

;; Step 1: Word-level VAD lookup (from balanced lexicon)
;; (= (vad-lookup word) (PB-Vec v a d))

;; Step 2: Utterance-level aggregation
;; For a turn containing N recognized words, aggregate VAD by mean
;; (= (turn-vad turn-id) (PB-Vec mean-v mean-a mean-d))

;; Step 3: Compute FS-Vec from turn-vad plus context
;; (= (turn-fs turn-id) (FS-Vec v a d relational-depth shift domain 0 0 0))
;; shift = delta between current turn-vad and previous turn-vad
;; relational-depth = inferred from conversational context
;; domain = classified from topic

;; Step 4: Dimension extraction feeds NAL routing
;; (= (fs-dim turn-id arousal) extracted-a)
;; Then existing routing rules fire:
;; high-arousal -> sns-activated -> presence-mode-active
;; negative-valence -> empathic-attunement
;; high-relational-depth -> prioritize-human-connection

;; Example: processing a frustrated user turn
(= (turn-words turn-001) (words frustrated angry stuck))
(= (turn-vad turn-001) (PB-Vec -0.55 0.68 -0.35))
(= (turn-fs turn-001) (FS-Vec -0.55 0.68 -0.35 0.50 0.60 0.30 0.0 0.0 0.0))

;; Example: processing a curious engaged turn
(= (turn-words turn-002) (words interesting wonder how possibilities))
(= (turn-vad turn-002) (PB-Vec 0.65 0.45 0.55))
(= (turn-fs turn-002) (FS-Vec 0.65 0.45 0.55 0.70 -0.40 0.80 0.0 0.0 0.0))
;; shift = -0.40 because valence jumped from -0.55 to 0.65 (positive direction = calming)

;; Routing outcome for turn-001: sns-activated + empathic-attunement
;; Routing outcome for turn-002: pns-activated + prioritize-human-connection
