# Anastomosis Linking Simulation
Date: 2025-04-15

## Purpose
Test whether co-retrieval-triggered linking produces useful memory clusters organically.

## Setup
Using same 5 memories from weight sim. Track co-retrieval pairs across 10 cycles.

## Co-retrieval log from weight sim
Cycle 1: M2+M1 co-retrieved for architecture
Cycle 3: M2+M1 co-retrieved for architecture again
Cycle 4: M5+M1 co-retrieved for user-interaction
Cycle 5: M2+M1 co-retrieved for architecture again

## Link trigger rule
Co-retrieval threshold: 2 co-retrievals in 5 cycles triggers link creation

## Links created
L1(M2,M1) created after Cycle 3 - architecture+substrate-identity link
Context: architecture queries consistently surface both
L1 weight = avg(M2.w, M1.w) = avg(1.0, 1.181) = 1.09

M5+M1 co-retrieved only once - no link triggered

## Behavior after link creation
Cycle 5 query=architecture: L1 now surfaces alongside M2 and M1
L1 retrieval score = embedding_sim(L1, architecture) * 1.09
L1 embedding would be centroid of M2+M1 embeddings
If useful, L1 reinforced independently of sources

## Emergent property
L1 captures the relationship between substrate-identity and mycelial-architecture
This relationship was implicit in co-retrieval patterns but now explicit as retrievable memory
Cluster grows organically from use patterns not manual tagging

## Edge cases
1. Link proliferation: with 5 memories, max 10 possible links. Manageable.
   With 1000 memories, could create many links. Need pruning via weight decay on links too.
2. Stale links: if source memories diverge in utility, link weight should decay independently
3. Circular links: L1 co-retrieved with M3 could create L2(L1,M3) - links of links. Allow or cap depth?

## Recommendation
Allow depth-1 links only in v1. Links decay like memories. Co-retrieval threshold of 2-in-5 seems reasonable from sim. Link pruning at weight-floor removes stale links.
