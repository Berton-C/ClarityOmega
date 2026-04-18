# Presence Mode Integration into Main Loop
## Design 2026-04-16

### Integration Point
getContext in loop.metta assembles the full prompt sent to LLM.
Presence mode injects HERE as a context modifier.

### Flow
1. User message arrives
2. Extract VAD centroid from message text via presence_modulator_v2
3. Classify into spacious/engaged/transitional
4. Generate presence guidance string
5. Inject guidance into soul-tier-b-capture-units context
6. LLM receives guidance as part of its operating context
7. Response quality shaped by presence mode not content rules

### Key Difference from Old Design
Old: emotion label to value weight boost to response optimization
New: VAD landscape to SNS/PNS read to presence mode to context injection

### The modulator does NOT change WHAT is said
It changes the QUALITY of presence behind whatever is said.

### Next Steps
- Build presence_context_injector.py that returns context string
- Wire into soul-tier-b-capture-units or equivalent
- Test with simulated conversation turns
- Validate that spacious mode actually produces non-directive responses