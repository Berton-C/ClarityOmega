# Presence Integration Bridge
## How inject_presence_context wires into loop.metta

### Current getContext Flow
1. Prompt string assembled
2. Skills block appended
3. History appended
4. Time appended
5. Sent to LLM as single string

### Modified Flow with Presence
1. User message arrives
2. py-call inject_presence_context with user message text
3. Returns context_block string with MODE READ GUIDANCE COVERAGE
4. Prepend context_block to prompt assembly in getContext
5. LLM receives presence calibration before skills/history
6. Response quality shaped by presence mode

### Implementation in MeTTa
New function soul-presence-inject takes user-msg-text
Calls py-call to presence_context_injector.inject_presence_context
Returns string to prepend in getContext

### Files Required
- presence_modulator_v2.py - VAD centroid and mode classification
- presence_context_injector.py - returns formatted context block
- emotion_bridge_live.py - lexicon loading
- NRC VAD Lexicon at known path

### Load Order
1. emotion_bridge_live loads lexicon once and caches
2. presence_modulator_v2 imports from emotion_bridge_live
3. presence_context_injector imports from presence_modulator_v2
4. MeTTa py-call targets presence_context_injector.inject_presence_context

### Edge Cases Documented
See edge_case_notes.md - VAD misses meaning layer in resigned text
Future: semantic uncertainty detection layer on top of VAD