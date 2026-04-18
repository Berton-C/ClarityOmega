# Memory Architecture Proposal: Depletion-Triggered Frontier Exploration

Based on mycelial mechanisms M1-M5 formalized 2026-04-15.

## Problem
Current memory is flat embedding space queried by similarity.
No mechanism detects when a region is exhausted or when frontier exploration is warranted.

## Proposed Mechanisms
1. **Relevance decay detection**: Track when queries to a topic cluster return diminishing novelty.
2. **Automatic frontier seeding**: When decay detected, generate speculative queries into adjacent semantic regions.
3. **Reinforcement on discovery**: When frontier query returns genuinely novel content, strengthen that pathway.
4. **Depletion signal**: The decay itself IS the growth trigger — no scheduler needed.
5. **Cost ceiling**: Frontier queries are cheap (single embedding lookup). Failed explorations cost little.

## Formal NAL Chain
nutrient-depletion -> small-carbon-investment -> range-expansion -> new-discovery -> weight-reinforcement -> cycle repeats

## Implementation Sketch
- After N queries to same cluster with <threshold novelty, flag cluster as depleted
- Generate 2-3 queries combining cluster terms with random novel terms from recent exploration
- If any return high-relevance results, store bridge memory connecting old cluster to new territory
- Track cluster health over time as metadata

## Connection to Signal Integrity
This replaces polling loops with genuine growth. Instead of asking am I needed yet the system asks what can I learn next.
