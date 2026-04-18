# Emotional Tone PoC — Proven Architecture

## What Exists (all validated with passing tests)

### Layer 1: VAD Estimation (poc_glue_v3.py)
- 31-word seed dictionary mapping words to Valence/Arousal/Dominance triples
- Regex tokenizer, average pooling over matched words
- Returns continuous VAD vector

### Layer 2: Tone Classification (poc_glue_v3.py)
- Discretizes VAD into 3x3x3 grid (pos/neg/neutral × high/mid/low × high/mid/low)
- 27-cell tone map — zero gaps, every combination has a named tone
- Example: neg,mid,low → vulnerable-frustration

### Layer 3: NAL Bridge (metta_bridge.py)
- Converts tone + VAD into NAL statements with computed confidence
- Confidence = 0.5 + |valence|*0.3 + |arousal|*0.2
- Emits: tone-label atom, valence-polarity atom, arousal/dominance atoms

### Layer 4: MeTTa Reasoning (validated via metta skill)
- Resemblance: vulnerable-frustration ↔ negative-valence (stv 1.0 0.33)
- Deduction: negative-valence → needs-support (stv 1.0 0.56)
- Conditional: negative-valence ∧ low-dominance → needs-gentle-approach (stv 1.0 0.595)
- Confidence propagates correctly through inference chain

### Layer 5: Strategy Selection (e2e_test.py)
- Four strategies: validate-then-assist, slow-pace-acknowledge-first, match-energy-collaborate, standard-responsive
- Selected by reasoning output, not hardcoded to tone

## Build-Out Path
1. Replace word-list VAD with embedding-based estimation
2. Wire real metta skill calls into pipeline loop (not simulated)
3. Add temporal trajectory tracking (tone shift over conversation)
4. Connect to response shaping layer
5. Expand NAL knowledge base with more inference rules

## Files
- /tmp/poc_glue_v3.py — Layers 1-2
- /tmp/metta_bridge.py — Layer 3
- /tmp/e2e_test.py — Layers 1-5 integrated
