; Clarity KB Bridge - Serialized Knowledge Base State
; Generated 2026-04-17 12:42
; These atoms can be reloaded to restore reasoning state

; Core inference rules
(= (kb-atom 1) ((==> (--> input frustrated) (--> user-need de-escalation)) (stv 1.0 0.9)))
(= (kb-atom 2) ((==> (--> user-need de-escalation) (--> strategy validate-first)) (stv 1.0 0.85)))
(= (kb-atom 3) ((==> (--> strategy validate-first) (--> action acknowledge-emotion)) (stv 1.0 0.8)))
; Shortcut rules from chain collapsing
(= (kb-atom 4) ((==> (--> input frustrated) (--> action acknowledge-emotion)) (stv 1.0 0.7)))
; Goal-selection atoms
(= (kb-atom 5) ((==> (--> goal bridge-to-live-memory) (--> value high-integration)) (stv 1.0 0.85)))
; Decay and maintenance parameters
(= (kb-param decay-rate) 0.2)
(= (kb-param reinforce-rate) 0.4)
(= (kb-param prune-threshold) 0.55)
