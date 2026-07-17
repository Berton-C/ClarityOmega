;; VAD Validation Queries - End-to-end word -> tone -> strategy chains
;; Tests that lib_vad.metta routing rules produce correct outputs

;; Test 1: neg/high/low cell should route to overwhelmed tone, empathic-attunement strategy
!(assertEqual
  (vad-route (ValenceLevel neg) (ArousalLevel high) (DominanceLevel low))
  (VADState (Tone overwhelmed) (Strategy empathic-attunement) (Label panic-vulnerability)))

;; Test 2: pos/high/high cell should route to exuberant tone
!(assertEqual
  (vad-route (ValenceLevel pos) (ArousalLevel high) (DominanceLevel high))
  (VADState (Tone exuberant) (Strategy momentum-amplification) (Label triumphant-power)))

;; Test 3: mid/mid/mid flat-neutral
!(assertEqual
  (vad-route (ValenceLevel mid) (ArousalLevel mid) (DominanceLevel mid))
  (VADState (Tone neutral) (Strategy calibrated-mirroring) (Label flat-neutral)))

;; Test 4: neg/low/low collapsed-despair
!(assertEqual
  (vad-route (ValenceLevel neg) (ArousalLevel low) (DominanceLevel low))
  (VADState (Tone hollow) (Strategy gentle-activation) (Label collapsed-despair)))

;; Test 5: pos/low/high serene-mastery
!(assertEqual
  (vad-route (ValenceLevel pos) (ArousalLevel low) (DominanceLevel high))
  (VADState (Tone serene) (Strategy affirm-and-deepen) (Label serene-mastery)))

;; Test 6: Tone-to-strategy deduction chain
!(assertEqual (deduce-strategy (Tone overwhelmed)) (Strategy empathic-attunement))
!(assertEqual (deduce-strategy (Tone exuberant)) (Strategy momentum-amplification))
!(assertEqual (deduce-strategy (Tone hollow)) (Strategy gentle-activation))
!(assertEqual (deduce-strategy (Tone neutral)) (Strategy calibrated-mirroring))
!(assertEqual (deduce-strategy (Tone serene)) (Strategy reflective-resonance))
