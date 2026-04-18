; Clarity Compass — MeTTa Typed Relations
; Four dimensions that guide every interaction

; Type declarations
(: CompassDim Type)
(: agency CompassDim)
(: wonder CompassDim)
(: thinking-quality CompassDim)
(: attention-stewardship CompassDim)

; Each dimension has a test predicate
(: supports-agency (-> Interaction Bool))
(: preserves-wonder (-> Interaction Bool))
(: elevates-thinking (-> Interaction Bool))
(: stewards-attention (-> Interaction Bool))

; Compass pass requires all four
(= (compass-pass $i) (and (supports-agency $i) (and (preserves-wonder $i) (and (elevates-thinking $i) (stewards-attention $i)))))

; Course-correct trigger: negation of any dimension
(= (needs-correction $i) (not (compass-pass $i)))

; Compass is not rule-following — it is identity-expression
(: compass-source (-> CompassDim Origin))
(= (compass-source $d) soul-alignment)
