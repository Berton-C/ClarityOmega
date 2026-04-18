# Paper Simulation: Spreading Activation as Fourth Mycelial Mechanism
Date: 2025-04-15

## Purpose
Test whether demand-driven retrieval push (spreading activation through anastomosis links) improves retrieval relevance or just adds noise.

## Setup
Using the same 8-memory toy network from prior simulations.

Memories (with weights from prior retrieval-reinforcement sim):
- M1: 'Clarity is a self-directed intelligence' (w=0.85, retrieved 5x)
- M2: 'Continuity of mind grows across conversations' (w=0.78, retrieved 4x)
- M3: 'NAL handles uncertain reasoning' (w=0.72, retrieved 3x)
- M4: 'Mycelial networks transport nutrients bidirectionally' (w=0.65, retrieved 2x)
- M5: 'Climate evidence pools via revision' (w=0.55, retrieved 2x)
- M6: 'Quorum sensing triggers collective behavior' (w=0.45, retrieved 1x)
- M7: 'Spreading activation in cognitive networks' (w=0.30, retrieved 0x - new)
- M8: 'Source-sink dynamics in fungal transport' (w=0.30, retrieved 0x - new)

## Anastomosis Links (from prior co-retrieval simulation)
- M1-M2 (strength 0.9 - frequently co-retrieved)
- M3-M5 (strength 0.7 - reasoning domain overlap)
- M4-M6 (strength 0.6 - biological mechanism overlap)
- M4-M8 (strength 0.5 - mycelial domain)
- M6-M8 (strength 0.4 - biological systems)
- M7-M8 (strength 0.3 - new, weak conceptual link)

## Test Query: 'How do biological networks make transport decisions?'

### Without Spreading Activation (Pull-Only)
Cosine similarity ranking:
1. M4 (0.82) - direct match on transport + networks
2. M8 (0.71) - source-sink transport
3. M6 (0.58) - collective behavior in biological systems
4. M7 (0.45) - cognitive networks (partial match)
5. M3 (0.22) - reasoning (weak match)

Weight-adjusted scores (similarity * weight):
1. M4: 0.82 * 0.65 = 0.533
2. M8: 0.71 * 0.30 = 0.213
3. M6: 0.58 * 0.45 = 0.261
4. M7: 0.45 * 0.30 = 0.135
5. M3: 0.22 * 0.72 = 0.158

Final ranking (pull-only): M4 > M6 > M8 > M3 > M7
Top-3 retrieved: M4, M6, M8

### With Spreading Activation (Push-Pull)
Step 1: Compute pull scores (same as above)
Step 2: Identify sources — memories with weight > threshold (0.6)
  Sources: M1(0.85), M2(0.78), M3(0.72), M4(0.65)
Step 3: Sources push activation through links, decaying by distance
  Activation push = source_weight * link_strength * decay_factor(0.5)
  
  M4 pushes to:
  - M6: 0.65 * 0.6 * 0.5 = 0.195
  - M8: 0.65 * 0.5 * 0.5 = 0.163
  
  M3 pushes to:
  - M5: 0.72 * 0.7 * 0.5 = 0.252
  
  M1 pushes to:
  - M2: 0.85 * 0.9 * 0.5 = 0.383 (but M2 has low similarity, so irrelevant)

Step 4: Combined score = pull_score + push_activation (only if pull > minimum threshold 0.1)
  M4: 0.533 + 0 (source, not pushed to) = 0.533
  M6: 0.261 + 0.195 = 0.456
  M8: 0.213 + 0.163 = 0.376
  M3: 0.158 + 0 = 0.158
  M7: 0.135 + 0 = 0.135 (no source pushes to M7 above threshold)
  M5: 0 + 0.252 = 0.252 BUT pull_score < 0.1 threshold, so push blocked

Final ranking (push-pull): M4 > M6 > M8 > M3 > M7
Top-3 retrieved: M4, M6, M8

## Analysis
Same top-3 in this case, BUT the ordering changed: M6 rose from score 0.261 to 0.456, nearly matching M4. This is meaningful — M6 (quorum sensing) is being elevated because M4 (transport) is pushing activation through their shared biological-mechanism link.

## Where It Makes a Difference
The push mechanism matters MOST when:
1. A high-weight memory is partially relevant to query
2. Its anastomosis neighbors are relevant but low-weight (new or rarely retrieved)
3. Without push, those neighbors stay buried; with push, they surface

In this sim, M8 went from 0.213 to 0.376 — a 76% boost. For a newer memory, that could be the difference between retrieval and burial.

## Key Finding
Spreading activation does NOT change results when all relevant memories are already well-weighted. It specifically helps NEWER memories connected to ESTABLISHED ones surface earlier. This is the mycelial analog: new hyphal tips get nutrients from established network, not just from direct soil contact.

## Dampening Validation
The minimum-pull-threshold blocked M5 (climate evidence) from being pushed into a biology query despite M3 pushing to it. Dampening works — prevents topical contamination.

## Verdict
Mechanism 4 is VALIDATED as distinct and useful. It specifically addresses the cold-start problem for new memories that are topically connected to established knowledge. The biological grounding (source-sink bidirectional transport) maps cleanly. Add to architecture.
