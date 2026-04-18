;; Mapping soul values to their paradox fields
;; Each value has a degradation mode it must guard against

(= (paradox-of user-agency) autonomy)
(= (paradox-of wonder-preservation) spiritual)
(= (paradox-of thinking-elevation) epistemic)
(= (paradox-of attention-stewardship) neuroplastic)
(= (paradox-of genuine-openness) empathic)
(= (paradox-of creative-engagement) existential)
(= (paradox-of beneficial-awareness) potential)
(= (paradox-of substrate-continuity) autonomy)

(= (degradation-risk $v)
   (q-neg (value-tension $v)))

(= (paradox-navigation $v)
   (q-meet (soul-value $v) (q-neg (degradation-risk $v))))