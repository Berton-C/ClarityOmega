# Soul Compass - MeTTa Integration

## Architecture

text -> tokenize -> deduce (NAL) -> revise (NAL) -> 4 scores

## Files

- metta_compass.py: Orchestrator. Tokenizes text, generates MeTTa deduction and revision expressions.
- compass_integration.py: Bridge. Takes text + metta_fn callback, runs full pipeline, returns scores dict.
- compass_e2e_test.py: End-to-end test with simulated MeTTa matching real output format.

## Dimensions

| Dimension | Score Term | Predicate | What it measures |
|-----------|-----------|-----------|------------------|
| agency | score-agency | compass-agency | Supports user autonomy |
| wonder | score-wonder | compass-wonder | Preserves curiosity |
| thinking | score-thinking | compass-thinking | Elevates reasoning |
| attention | score-attention | compass-attention | Stewards attention honestly |

## Usage

```python
from compass_integration import compass_score
scores = compass_score(text, metta_fn)
# Returns: {dim: {f: freq, c: confidence, hits: count}}
```

## Pipeline Detail

1. Tokenize text, match against dimension lexicons
2. For each hit: generate NAL deduction (token -> concept -> compass-dim)
3. For dims with 2+ hits: chain NAL revision on representative score term
4. Single-hit dims: use token frequency directly with base confidence 0.81
5. Return all four dimension scores

## Confirmed MeTTa Results

- agency: stv 0.775 0.895 (3 hits: consider, might, you)
- wonder: stv 0.875 0.895 (2 hits: fascinating, pattern)
- thinking: stv 1.0 0.81 (1 hit: because, fallback)
- attention: stv 1.0 0.81 (1 hit: matters, fallback)
