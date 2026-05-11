; SN Cycle Decision Procedure v0.1
; Stalk values → action gates. Not decorative. Causal.
; f*c >= 0.30: reliable (hard gate) | f*c < 0.30: exploratory (soft suggestion)

; Current classification:
; RELIABLE: safety-first(0.45) integrity-check(0.425) person-state-salience(0.32)
; EXPLORATORY: urgency-detection(0.28) context-shift(0.18) self-correction(0.15) boundary-testing(0.15)

; Reliable stalks gate actions:
; safety-first reliable → safety check is non-negotiable gate before any action
; integrity-check reliable → honesty check is non-negotiable gate before any send
; person-state-salience reliable → factor person state into every decision
; Exploratory stalks inform but never gate alone

; Cycle decision atom — which stalks gated this cycle
(SN-cycle-gate 14:30 safety-first integrity-check 2026-05-08T14:30)