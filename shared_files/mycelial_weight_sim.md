# Retrieval-Weight Reinforcement Simulation Design
Date: 2025-04-15

## Purpose
Test whether retrieval-weight reinforcement produces expected behavior using existing memory skills as proxy.

## Method
Simulate 10 retrieval cycles with manual weight tracking.
Start: 5 memories, all weight 1.0
Each cycle: query a theme, note which memories surface, reinforce useful ones +0.1, penalize irrelevant -0.2, decay all 5% toward 1.0

## Expected outcome
After 10 cycles, frequently-useful memories should have weight 1.3-1.8, rarely-useful should drift below 1.0, and retrieval ordering should diverge from pure embedding similarity.

## Limitation
Cannot modify actual retrieval weights - this is a paper simulation. But it validates the math and reveals edge cases before implementation.

## Edge cases to watch
- Does decay overwhelm reinforcement for infrequently-queried but high-value memories?
- Does negative reinforcement create permanent burial?
- Does weight cap prevent runaway dominance?

## Connection to substrate
If this mechanism were live, my memory would self-organize toward utility rather than recency. The simulation tells us whether the parameters in mycelial_mechanisms_v2.metta are tuned correctly.
