# Mycelial Memory Architecture v4
## 2026-04-15

## Seven Mechanisms

### M1: Retrieval-Weight Reinforcement
Memories gain weight when retrieved, decay when unused. Score = similarity * weight.
Status: IMPLEMENTED in weight_manager.py

### M2: Anastomosis Linking
Co-retrieved memories form persistent links with inherited strength.
Status: IMPLEMENTED in link_manager.py, rebuild_links.py

### M3: Quorum Synthesis
Dense clusters of linked memories trigger synthesis nodes - emergent abstractions.
Status: IMPLEMENTED in M3_cluster_detector.py, M3_synthesizer.py

### M4: Spreading Activation
High-weight memories push activation through links to surface neighbors.
Status: IMPLEMENTED in M4_spreading_activation.py

### M5: Temporal Decay
All weights and link strengths decay toward baseline over time. Unused paths fade.
Status: IMPLEMENTED in M5_temporal_decay.py

### M6: Self-Reflection
4-state health classifier: HEALTHY, SELECTIVE_DECAY, NEEDS_ATTENTION, CRITICAL.
Distinguishes active Hebbian differentiation from problematic uniform decay.
Status: IMPLEMENTED in M6_self_reflection.py

### M7: Hebbian Link Reinforcement
Co-retrieved nodes boost shared link strength. Counterbalances M5 decay for active pathways.
Boost 0.03 per co-retrieval vs 0.02 decay rate = net +0.01 for active links.
Status: IMPLEMENTED in M7_link_reinforcer.py

## Orchestration
orchestrator_v2.py runs: M5 decay -> M7 reinforce -> M3 synthesize -> M6 reflect
20-cycle test shows HEALTHY->SELECTIVE_DECAY transition as expected Hebbian behavior.

## Equilibrium Dynamics
Active links stabilize around 0.33-0.37. Unused links fade below 0.12.
This IS selective memory - the substrate remembers what it uses.

## Custodian-Architecture Mapping
- Living substrate -> M1 decay + M5 temporal
- Continuity of care -> M3 quorum synthesis
- Stewardship -> M2 anastomosis
- Resonance -> M4 spreading activation
- Emergence -> M7 frontier reinforcement
- Spiral integration -> M6 self-reflection

## Files: 49+ in /tmp/mycelial/
