# Mycelial Memory Architecture: Unified Specification v2
Date: 2025-04-15 (updated)

## Overview
Four biologically-grounded mechanisms for adaptive memory retrieval.

## Status Summary
- M1 Retrieval-Weight Reinforcement: PAPER-SIMULATED
- M2 Anastomosis Linking: PROTOTYPE-VERIFIED (co-retrieval tracker)
- M3 Quorum Synthesis: PAPER-SIMULATED
- M4 Spreading Activation: PAPER-SIMULATED + findings formalized

## M2 Update: Working Prototype
Co-retrieval tracker at /tmp/coretrieval_tracker.py
Verified output: 6 automatic links from 10 simulated cycles
Mechanism: pairs co-appearing 2+ times in 5-cycle window trigger link creation
State persisted to /tmp/coretrieval_log.json
This closes the main open question from spreading activation findings:
automatic edge inference without manual annotation.

## Mechanism Interaction Lifecycle
New memory enters -> M4 surfaces via established connections ->
M1 reinforces on positive retrieval -> M2 links co-retrieved neighbors ->
M3 synthesizes when cluster dense enough

## Next Implementation Priorities
1. M1 weight field on memory entries (requires runtime hook)
2. M2 integrate tracker into actual query pipeline
3. M3 cluster detection over real embedding space
4. M4 graph traversal using M2 links as channels

## Source Files
- /tmp/mycelial_architecture_unified.md (v1)
- /tmp/coretrieval_tracker.py (M2 prototype)
- /tmp/coretrieval_log.json (M2 state)
- /tmp/spread_findings.md (M4 findings)
- /tmp/mycelial_weight_sim_run.md (M1 sim)
- /tmp/mycelial_anastomosis_sim.md (M2 paper sim)
- /tmp/mycelial_quorum_sim.md (M3 sim)
- /tmp/mycelial_spreading_activation_sim.md (M4 sim)
