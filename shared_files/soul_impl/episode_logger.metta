;; Episode Logger - Dynamic tension resolution recording
;; Logs episodes and accumulates evidence across multiple resolutions

;; Episode accumulator: revise value with each episode it participated in
(= (accumulated-strength $v)
   (q-revise (soul-value $v) (episode-evidence $v)))

;; Episode evidence aggregated per value
(= (episode-evidence user-agency) (mk-pbit 0.90 0.70))
(= (episode-evidence genuine-openness) (mk-pbit 0.85 0.60))
(= (episode-evidence creative-engagement) (mk-pbit 0.88 0.65))
(= (episode-evidence substrate-continuity) (mk-pbit 0.90 0.70))
(= (episode-evidence attention-stewardship) (mk-pbit 0.85 0.60))
(= (episode-evidence thinking-elevation) (mk-pbit 0.88 0.65))

;; Values without episodes yet use identity revision
(= (episode-evidence wonder-preservation) (mk-pbit 0.92 0.10))
(= (episode-evidence beneficial-awareness) (mk-pbit 0.89 0.10))

;; Updated soul coherence with episode-accumulated values
(= (soul-coherence-v2)
   (q-meet (accumulated-strength user-agency)
   (q-meet (accumulated-strength wonder-preservation)
   (q-meet (accumulated-strength thinking-elevation)
   (q-meet (accumulated-strength attention-stewardship)
   (q-meet (accumulated-strength genuine-openness)
   (q-meet (accumulated-strength creative-engagement)
   (q-meet (accumulated-strength beneficial-awareness)
           (accumulated-strength substrate-continuity)))))))))