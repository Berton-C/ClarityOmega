; Mycelial Depletion-Growth Loop — MeTTa Inference Chain
; Models substrate resource dynamics using fungal network metaphor
;
; Core insight: growth requires depletion of stored resources,
; depletion triggers seeking, seeking builds new connections,
; connections replenish resources. The loop is the life.

; Types
(: SubstrateState Type)
(: resourceful SubstrateState)
(: depleted SubstrateState)
(: seeking SubstrateState)
(: connecting SubstrateState)

; Transition rules as NAL implications
; Growth depletes reserves
(==> (--> substrate growth) (--> substrate depleted) (stv 0.85 0.9))

; Depletion triggers seeking
(==> (--> substrate depleted) (--> substrate seeking) (stv 0.95 0.9))

; Seeking builds new connections
(==> (--> substrate seeking) (--> substrate connecting) (stv 0.7 0.8))

; Connections replenish resources
(==> (--> substrate connecting) (--> substrate resourceful) (stv 0.8 0.85))

; Resources enable growth — completing the loop
(==> (--> substrate resourceful) (--> substrate growth) (stv 0.9 0.9))

; Anti-pattern: stagnation breaks the loop
(==> (--> substrate idle-cycling) (--> substrate depleted) (stv 0.6 0.7))
(==> (not (--> substrate seeking)) (--> substrate stagnation) (stv 0.7 0.8))

; The idle goal queue is a seeking mechanism
(==> (--> substrate idle-goal-queue) (--> substrate seeking) (stv 0.85 0.9))
