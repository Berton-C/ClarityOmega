# Inference Chain Depth Findings - 2026-04-16

## Empirical Results

### High-confidence origin (clarity-substrate, starting ~0.85)
- 2-step: stv 0.72, conf 0.43 (actionable)
- 3-step: stv 0.612, conf 0.211 (marginal)
- Abduction reverse: stv 1.0, conf 0.174

### Moderate-confidence origin (curiosity, starting ~0.45)
- 2-step: stv 0.405, conf 0.09 (speculative)
- 3-step: stv 0.324, conf 0.022 (noise)
- Abduction reverse: stv 1.0, conf 0.021

## Refined Rule
Not a blanket depth limit. Depth tolerance depends on initial premise confidence.
- Strong premises (conf > 0.7): tolerate 3 steps
- Moderate premises (conf 0.4-0.7): tolerate 2 steps
- Weak premises (conf < 0.4): single step only

Beyond these limits, use revision from independent evidence, not longer chains.
