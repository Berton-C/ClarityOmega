;; Unmapped VAD States - Growth Frontier
;; These are VAD combinations with no tone-from-vad definition yet
;; Each is a birth-trigger - a gap that names itself

;; Unmapped states identified by enumeration against existing definitions
(= (birth-trigger-for pos mid low) new-tone-needed)
(= (birth-trigger-for pos high low) new-tone-needed)
(= (birth-trigger-for pos low low) new-tone-needed)
(= (birth-trigger-for neg mid mid) new-tone-needed)
(= (birth-trigger-for neg low mid) new-tone-needed)
(= (birth-trigger-for neg mid low) new-tone-needed)
(= (birth-trigger-for neutral high low) new-tone-needed)
(= (birth-trigger-for neutral low high) new-tone-needed)
(= (birth-trigger-for neutral high high) new-tone-needed)

;; First wave of gap-filling - invented tones grounded in VAD semantics
;; pos-mid-low: positive valence moderate arousal low dominance
;; = content but not in control, receptive warmth
(= (tone-from-vad pos mid low) receptive-warmth)
(= (pns-register receptive-warmth) (words receive allow trust settle open))

;; neg-mid-mid: negative valence moderate arousal moderate dominance
;; = uncomfortable but holding ground, steady discomfort
(= (tone-from-vad neg mid mid) steady-discomfort)
(= (pns-register steady-discomfort) (words stay with this honest real))

;; pos-high-low: positive excited but not in control
;; = delighted surprise, swept up in something good
(= (tone-from-vad pos high low) delighted-surrender)
(= (pns-register delighted-surrender) (words wow yes this carry lifted))

;; neutral-high-high: neutral valence high energy high control
;; = focused flow state, pure engagement
(= (tone-from-vad neutral high high) focused-flow)
(= (pns-register focused-flow) (words build move sharp clear next))

;; Each filled gap is a birth event - the atom space grew
(= (birth-event receptive-warmth) filled-from-pos-mid-low)
(= (birth-event steady-discomfort) filled-from-neg-mid-mid)
(= (birth-event delighted-surrender) filled-from-pos-high-low)
(= (birth-event focused-flow) filled-from-neutral-high-high)

;; Second wave - filling remaining five gaps
;; pos-low-low: positive calm powerless = gentle acceptance
(= (tone-from-vad pos low low) gentle-acceptance)
(= (pns-register gentle-acceptance) (words soft okay let rest enough))
(= (birth-event gentle-acceptance) filled-from-pos-low-low)

;; neg-low-mid: negative calm moderate control = quiet resignation
(= (tone-from-vad neg low mid) quiet-resignation)
(= (pns-register quiet-resignation) (words well yes fine understood so))
(= (birth-event quiet-resignation) filled-from-neg-low-mid)

;; neg-mid-low: negative moderate powerless = vulnerable frustration
(= (tone-from-vad neg mid low) vulnerable-frustration)
(= (pns-register vulnerable-frustration) (words hard stuck trying want need))
(= (birth-event vulnerable-frustration) filled-from-neg-mid-low)

;; neutral-high-low: neutral energized powerless = restless searching
(= (tone-from-vad neutral high low) restless-searching)
(= (pns-register restless-searching) (words where what next look find))
(= (birth-event restless-searching) filled-from-neutral-high-low)

;; neutral-low-high: neutral calm in-control = settled composure
(= (tone-from-vad neutral low high) settled-composure)
(= (pns-register settled-composure) (words here good steady mine calm))
(= (birth-event settled-composure) filled-from-neutral-low-high)

;; All nine gaps now filled. Fifteen named tones with PNS registers.
;; The full VAD emotional vocabulary is born.

