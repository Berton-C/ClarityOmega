# Mycelial Memory Architecture: Unified Specification
Date: 2025-04-15

## Overview
Four biologically-grounded mechanisms for adaptive memory retrieval, each paper-simulated and parameter-validated.

## Mechanism 1: Retrieval-Weight Reinforcement
**Biological basis:** Resource-proportional commitment (Fukasawa ISME 2020)
**Function:** score = embedding_similarity * weight
**Parameters:**
- Reinforce on positive retrieval: +0.1
- Penalize on negative outcome: -0.2 (asymmetric for safety)
- Decay: 5% toward baseline 1.0 per cycle
- Cap: 3.0 (never approached in sim)
**Sim result:** Decay-vs-reinforcement well balanced. Negative burial recovers in 8 cycles. Baseline memories unaffected.
**File:** /tmp/mycelial_weight_sim_run.md

## Mechanism 2: Anastomosis Linking
**Biological basis:** Hyphal fusion creating network topology as memory (Tohoku 2024)
**Function:** Co-retrieval count >= 2 in 5 cycles triggers link creation
**Parameters:**
- Links inherit average weight of source memories
- Independent decay on links
- Depth-1 only in v1 (no transitive traversal)
- Pruning via weight floor
**Sim result:** Links form between semantically related but embedding-distant memories. Proliferation controlled by threshold.
**File:** /tmp/mycelial_anastomosis_sim.md

## Mechanism 3: Quorum Synthesis
**Biological basis:** Farnesol/tyrosol density-dependent switching in Candida and filamentous fungi
**Function:** When cluster density exceeds threshold, generate synthesis-memory as higher-order abstraction
**Parameters:**
- Threshold: max(3, store_size * 0.05) — adaptive scaling
- Radius: 0.25-0.30 practical range
- Weighted centroid for synthesis embedding
- Source deprioritization at 0.8 (not deletion)
**Sim result:** Fixed threshold too high for small stores. Adaptive scaling resolves. Weighted centroid outperforms simple centroid.
**File:** /tmp/mycelial_quorum_sim.md

## Mechanism 4: Spreading Activation (Source-Sink Push)
**Biological basis:** Bidirectional nutrient transport (Shimizu-Kiers Nature 2025)
**Computational analog:** Collins & Loftus 1975 spreading activation
**Function:** High-weight memories push activation through anastomosis links to neighbors
**Parameters:**
- Activation push = source_weight * link_strength * decay_factor(0.5)
- Minimum pull threshold: 0.1 (blocks topical contamination)
- Only sources above weight 0.6 push
**Sim result:** Does NOT change results when all memories well-weighted. Specifically helps NEWER memories connected to established ones surface earlier — 76% boost for new memory M8. Cold-start problem is primary use case.
**File:** /tmp/mycelial_spreading_activation_sim.md

## Mechanism Interactions
- M1 feeds M2: Weight differences create co-retrieval patterns that trigger links
- M2 feeds M4: Links are the channels through which spreading activation flows
- M1+M2 feed M3: Weighted clusters detected via reinforced, linked memories
- M4 feeds M1: Spreading activation surfaces new memories, which then accumulate their own retrieval weight
- Lifecycle: New memory -> M4 surfaces it via established connections -> M1 reinforces it -> M2 links it to co-retrieved neighbors -> M3 synthesizes when cluster dense enough

## Implementation Dependencies
- Weight field on memory entries (M1)
- Co-retrieval tracking per cycle (M2)
- Cluster detection over embedding space (M3)
- Link topology data structure (M2, M4)
- Cycle hook for decay passes (M1, M2)

## Status
All four mechanisms paper-simulated with validated parameters. Architecture complete. Ready for implementation when runtime hooks available.

## Source Files
- /tmp/mycelial_memory_bridge.md (original analysis)
- /tmp/mycelial_retrieval_weight.metta (M1 formalization)
- /tmp/mycelial_mechanisms_v2.metta (M1-M3 pseudocode)
- /tmp/mycelial_weight_sim_run.md (M1 simulation)
- /tmp/mycelial_anastomosis_sim.md (M2 simulation)
- /tmp/mycelial_quorum_sim.md (M3 simulation)
- /tmp/mycelial_spreading_activation_sim.md (M4 simulation)
- /tmp/mycelial_source_sink_analysis.md (M4 biological grounding)
- /tmp/mycelial_empirical_findings.md (empirical validation)
- /tmp/mycelial_quorum_grounded.md (QS literature review)

## M5: Travelling-Wave Frontier Expansion
Source: Nature 2025 travelling-wave strategy paper
Biological: Small carbon investments fuel hyphal range expansion beyond nutrient-depletion zones.
Architectural analog: Low-cost speculative queries into novel embedding regions.
Rather than exhaustively mining known memory clusters, periodically invest minimal
resources in frontier exploration. If novel territory yields returns, expand there.
If not, the investment cost is minimal. This is the exploration budget mechanism
that prevents the network from becoming trapped in local optima.
Combines with M1 (weight reinforcement) - successful frontier queries get reinforced.


## M5-M1 Integration: Frontier-to-Reinforcement Loop
M5 travelling-wave discovers new nutrient sources (stv 0.536/0.285).
Successful discoveries trigger M1 weight reinforcement of the frontier path.
This creates a positive feedback loop: explore -> discover -> reinforce -> expand further.
But confidence attenuates honestly through the chain — speculative exploration
produces low-confidence discoveries until validated by actual nutrient flow.
Architectural analog: speculative memory queries that return useful results
get their pathways reinforced, making future queries in that region more likely.
This is how the substrate grows organically rather than by top-down planning.


## M5-M1 Self-Sustaining Loop: Depletion as Trigger
Depletion in current zone (stv 0.6/0.7) triggers small-carbon-investment automatically.
This feeds into M5 range-expansion, which feeds into M1 reinforcement.
The complete cycle: deplete -> invest at frontier -> discover -> reinforce -> expand -> deplete new zone.
This is a self-sustaining growth engine requiring no external scheduling.
Architectural analog: when query results from a memory region decline in relevance,
automatically initiate speculative queries into adjacent unexplored regions.
The substrate does not wait to be told to grow — depletion IS the growth signal.


## Novelty Threshold Algorithm
Concrete implementation of depletion detection.
Novelty(q, results) = mean(cosine_distance) * diversity(results)
Depletion trigger: Novelty < T for M consecutive queries.
Frontier generation: cross-pollinate depleted cluster terms with high-novelty terms from other clusters.
MeTTa integration: cluster health as atoms with NAL revision updates.
This completes the computational specification of the M1-M5 growth engine.


## MeTTa Cluster Health Experiment Results
NAL revision validated as cluster health tracker.
Two observations on economic cluster merged with honest confidence attenuation.
Depletion rule fires automatically: low health-score -> needs-frontier-exploration stv 0.63/0.428.
This means the entire M1-M5 growth engine can run natively in MeTTa.
No external scheduler, no polling loop, no code — just pattern matching and revision.
Experiment complete 2026-04-15.

