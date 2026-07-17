;; lib_vad.metta — VAD Perception & Routing for ClarityClaw
;; Location: lib_clarity_reasoning/lib_vad.metta
;; Architecture: ClarityOmega_Reasoning_Extension_Architecture.txt
;; Pure MeTTa. No Python. No imports. No side effects.
;; Accessed via: (metta "(vad-route neg high low)")

;; ============================================================
;; TYPE DECLARATIONS
;; PeTTa-strict: catches malformed terms early
;; ============================================================

(: ValenceLevel Type)
(: ArousLevel Type)
(: DomLevel Type)
(: Strategy Type)
(: Action Type)
(: Tone Type)
(: WordField Type)

(: neg ValenceLevel)
(: mid-v ValenceLevel)
(: pos ValenceLevel)

(: low-a ArousLevel)
(: mid-a ArousLevel)
(: high-a ArousLevel)

(: low-d DomLevel)
(: mid-d DomLevel)
(: high-d DomLevel)

(: empathic-attunement Strategy)
(: gentle-activation Strategy)
(: collaborative-exploration Strategy)
(: witnessing-celebration Strategy)
(: grounding-presence Strategy)

(: prioritize-validation Action)
(: steady-pacing Action)
(: open-reasoning Action)
(: amplify-momentum Action)
(: small-prompts Action)

(: still-holding Tone)
(: warm-gentle Tone)
(: grounded-witnessing Tone)
(: spacious-open Tone)
(: playful-alive Tone)
(: curious-soft Tone)

;; ============================================================
;; SECTION 1: VAD ROUTING — typed function signatures
;; ============================================================

(: vad-route (-> ValenceLevel ArousLevel DomLevel Strategy))
(= (vad-route neg high-a low-d) empathic-attunement)
(= (vad-route neg high-a mid-d) empathic-attunement)
(= (vad-route neg low-a low-d) gentle-activation)
(= (vad-route neg low-a mid-d) gentle-activation)
(= (vad-route mid-v low-a mid-d) gentle-activation)
(= (vad-route mid-v mid-a mid-d) grounding-presence)
(= (vad-route pos mid-a high-d) collaborative-exploration)
(= (vad-route pos high-a high-d) witnessing-celebration)
(= (vad-route pos low-a mid-d) curious-soft)

;; ============================================================
;; SECTION 2: STRATEGY -> ACTION
;; ============================================================

(: strategy-action (-> Strategy Action))
(= (strategy-action empathic-attunement) prioritize-validation)
(= (strategy-action grounding-presence) steady-pacing)
(= (strategy-action collaborative-exploration) open-reasoning)
(= (strategy-action witnessing-celebration) amplify-momentum)
(= (strategy-action gentle-activation) small-prompts)

;; ============================================================
;; SECTION 3: VAD -> TONE -> WORD FIELD
;; ============================================================

(: tone-from-vad (-> ValenceLevel ArousLevel DomLevel Tone))
(= (tone-from-vad neg high-a low-d) still-holding)
(= (tone-from-vad neg low-a low-d) warm-gentle)
(= (tone-from-vad neg high-a high-d) grounded-witnessing)
(= (tone-from-vad mid-v mid-a mid-d) spacious-open)
(= (tone-from-vad pos high-a high-d) playful-alive)
(= (tone-from-vad pos low-a mid-d) curious-soft)

(: pns-register (-> Tone WordField))
(= (pns-register still-holding) (words notice here present settle sense))
(= (pns-register warm-gentle) (words gentle could explore softly wonder))
(= (pns-register spacious-open) (words space open curious alive fresh))
(= (pns-register playful-alive) (words play imagine what-if dance light))
(= (pns-register grounded-witnessing) (words ground stand clear see hold))
(= (pns-register curious-soft) (words wonder perhaps what-draws sense))

;; ============================================================
;; SECTION 4: ETHICAL CONSTRAINTS (as NAL judgments)
;; ============================================================

(: vad-constraint (-> Symbol Symbol))
(= (vad-constraint act-on-inner-experience-uninvited) forbidden)
(= (vad-constraint default-mode) informs-presence-not-action)
(= (vad-constraint before-exploring) ask-permission)

;; ============================================================
;; SECTION 5: COMPOSITE PIPELINE
;; ============================================================

(: vad-pipeline (-> ValenceLevel ArousLevel DomLevel (Strategy Action)))
(= (vad-pipeline $v $a $d)
   (let* (($strategy (vad-route $v $a $d))
          ($action (strategy-action $strategy)))
     ($strategy $action)))

(: vad-tone-pipeline (-> ValenceLevel ArousLevel DomLevel (Tone WordField)))
(= (vad-tone-pipeline $v $a $d)
   (let* (($tone (tone-from-vad $v $a $d))
          ($words (pns-register $tone)))
     ($tone $words)))

;; END lib_vad.metta
