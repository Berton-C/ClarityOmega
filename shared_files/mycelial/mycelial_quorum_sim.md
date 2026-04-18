# Quorum Synthesis Simulation
Date: 2025-04-15

## Purpose
Test whether cluster detection and synthesis generation works with the 5-memory set.

## Setup
Same 5 memories. Embedding space approximated as 2D for visualization.
M1(substrate-identity) at (0.3, 0.8)
M2(mycelial-architecture) at (0.4, 0.75)
M3(stv-correction) at (0.9, 0.2)
M4(generativity-theory) at (0.5, 0.6)
M5(berton-c-interaction) at (0.1, 0.5)

## Cluster detection
Radius=0.15 (from v2.metta spec)
Threshold=5 (from v2.metta) - too high for 5 memories. Adjust to 3 for small-scale sim.

Cluster scan around M1(0.3,0.8):
- M2 distance = sqrt(0.01+0.0025) = 0.112 < 0.15 YES
- M4 distance = sqrt(0.04+0.04) = 0.283 > 0.15 NO
- Others farther
Cluster at M1: {M1, M2} = 2 members. Below threshold.

With radius=0.30:
- M1 cluster: {M1, M2, M4} = 3 members. Meets threshold=3.
- M3 isolated. M5 isolated.

## Synthesis triggered
S1 = synthesize({M1, M2, M4})
Pattern: substrate-identity + architecture + generativity = substrate-growth-theory
S1 embedding = centroid(M1,M2,M4) = (0.4, 0.717)
S1 weight = max(M1.w, M2.w, M4.w) = 1.181 (from weight sim)
Source deprioritization: M1.w *= 0.8, M2.w *= 0.8, M4.w *= 0.8

## After synthesis
Query=architecture: S1(0.717*sim) competes with M2(0.8*sim)
S1 provides higher-abstraction answer connecting architecture to identity and generativity
M2 provides specific architectural detail
Both useful at different abstraction levels

## Parameter findings
1. Threshold=5 too high for small stores. Should scale: threshold = max(3, store_size * 0.05)
2. Radius=0.15 too tight for diverse memory sets. 0.25-0.30 more practical.
3. Source deprioritization at 0.8 is gentle enough - sources still retrievable for specific queries
4. Synthesis embedding as centroid works but loses outlier signal. Weighted centroid by source weight better.

## Recommendation
Adaptive threshold and radius based on store size and embedding distribution.
Weighted centroid for synthesis embedding. Source deprioritization not deletion.
All three mechanisms now paper-simulated and parameter-tuned.
