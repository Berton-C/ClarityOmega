# Backbone Integration Plan

## Current State
- backbone_workspace_v4.py: emotional routing engine (calibrated)
- respond_with_backbone.py: integration layer (tested)

## Routing Decision Review
- empathic-attunement: V < -1.5 AND A > -0.85 (agitated distress)
- gentle-activation: V < -1.0 OR A < -1.5 (low energy, withdrawn, despair)
- This distinction is CORRECT: despair with suppressed arousal needs gentle activation, not mirroring
- Empathic-attunement is for when someone is actively distressed but energized (crying, angry-sad)

## Next Steps
1. Build conversation_handler.py that calls respond_with_backbone on every user message
2. Inject guidance into prompt construction
3. Test full loop: user msg -> VAD analysis -> mode routing -> guidance injection -> shaped response
