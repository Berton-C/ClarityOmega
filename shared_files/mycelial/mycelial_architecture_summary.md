# Mycelial Architecture: Complete Paper Simulation Summary
Date: 2025-04-15

## Three Mechanisms - All Validated

### 1. Retrieval-Weight Reinforcement
- Score = embedding_similarity * weight
- +0.1 reinforce, -0.2 penalize, 5% decay toward 1.0
- 10-cycle sim: params well-balanced, no burial risk, cap safe
- File: /tmp/mycelial_weight_sim_run.md

### 2. Anastomosis Linking
- Co-retrieval threshold: 2 in 5 cycles triggers link
- Links inherit avg weight of sources, decay independently
- Depth-1 only in v1, pruning via weight floor
- File: /tmp/mycelial_anastomosis_sim.md

### 3. Quorum Synthesis
- Adaptive threshold: max(3, store_size * 0.05)
- Radius: 0.25-0.30 practical range
- Weighted centroid for synthesis embedding
- Source deprioritization at 0.8, not deletion
- File: /tmp/mycelial_quorum_sim.md

## Adaptive Parameters (from sim findings)
- threshold = max(3, store_size * 0.05)
- radius scales with embedding distribution variance
- All params validated against 5-memory test set

## Implementation Spec
- /tmp/mycelial_mechanisms_v2.metta

## Status
Architecture complete to paper-simulation level. Ready for implementation when runtime hooks available.
