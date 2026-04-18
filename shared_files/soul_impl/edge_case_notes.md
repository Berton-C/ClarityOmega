# Presence Modulator Edge Case Notes
## 2026-04-16

### Observation: VAD Centroid Misses Meaning Layer
- Text: I dont know what to think anymore
- VAD reads low arousal -> classifies as PNS/engaged
- But semantically this human is likely in mild SNS seeking
- The WORDS are calm but the MIND is not settled

### Implication
- VAD centroid is necessary but not sufficient
- Future layer: semantic uncertainty detection
- Resigned/flat affect can mask active confusion
- When coverage is moderate and mode is engaged but content signals uncertainty, flag as transitional

### Possible Refinement
- Add semantic markers: negation density, uncertainty words
- If uncertainty markers high AND mode reads engaged, override to transitional
- This preserves the non-directive principle: when in doubt, do not assume settled