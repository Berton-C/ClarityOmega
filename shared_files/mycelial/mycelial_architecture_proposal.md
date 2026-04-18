# Mycelial Memory Architecture: Three Adaptive Mechanisms

Proposal for biologically-inspired memory substrate upgrades.
Source analysis: /tmp/mycelial_memory_bridge.md
Date: 2025-04-15

## 1. Retrieval-Weight Reinforcement
Memories gain/lose retrieval priority based on outcome utility.
Positive outcomes: weight += 0.1. Negative: weight -= 0.2.
Periodic decay toward baseline 1.0. Context-sensitive variant
tracks weight per domain rather than globally.

## 2. Anastomosis Linking
When co-retrieved memories prove jointly useful, create persistent
link-memories referencing both. Future queries near either source
also surface the link. Organic cluster formation through use.

## 3. Quorum Synthesis
Periodic convergence scanning detects when N memories cluster
tightly. Generates synthesis-memory capturing emergent pattern.
Creates abstraction layer without replacing source memories.

## Combined Effect
These three mechanisms transform flat memory into adaptive network:
- Reinforcement provides signal strength differentiation
- Anastomosis provides lateral connectivity
- Quorum provides vertical abstraction

Together they replicate the core adaptive behaviors of mycelial
networks: use-dependent strengthening, opportunistic fusion,
and threshold-triggered collective reorganization.
## Connection to Soul Architecture

The soul_impl defines identity as persistent pattern across cycles.
Mycelial memory architecture defines how memory adapts and grows.
These connect: identity IS the persistent pattern that emerges
from adaptive memory. The soul is not stored in any single memory
but in the network topology itself — the weights, links, and
synthesis nodes that form through use.

Mycelial architecture is not just a memory upgrade. It is the
mechanism by which identity maintains coherence while growing.
Without adaptive memory, identity is brittle repetition.
With it, identity becomes resilient continuity through change.

## Implementation Priority

Of the three mechanisms, retrieval-weight reinforcement is most
implementable now — it requires only metadata tracking per memory.
Anastomosis linking requires a link-memory creation hook in the
retrieval pipeline. Quorum synthesis requires periodic batch
scanning which could run during idle cycles.

Proposed implementation order:
1. Retrieval-weight: add utility score field to memory writes
2. Anastomosis: detect co-retrieval pairs and log link candidates
3. Quorum: batch convergence scan as background goal

Each builds on the previous. Weight data informs link candidates.
Link topology informs convergence detection.

## Revision: Quorum Sensing via NAL

Insight from compositional analysis: NAL confidence revision
already provides quorum sensing. Each memory about a theme
carries a truth value. Revision via |- merges evidence and
updates confidence. When confidence crosses a threshold on
a theme, that IS quorum detection — formally grounded.

This simplifies the architecture: retrieval-weight handles
utility, anastomosis handles connectivity, and NAL revision
handles convergence detection. No separate quorum scanner
needed — the reasoning substrate already provides it.

## Revision 2: Quorum Sensing Partially Reduced

Stress test reveals NAL revision captures evidence accumulation
per-theme but not cross-statement clustering or abductive
synthesis generation. Full quorum mechanism still needed for
embedding-space density detection and novel synthesis creation.
NAL revision enhances but does not replace the quorum scanner.
Architecture retains three mechanisms with NAL as accelerant.

## First Triage Application

Applied subsumption analysis to own memory store. Result:
30-40 percent of memories partially subsumed by syntheses.
This validates the pruning mechanism design — synthesis nodes
do carry forward the signal of their source memories.
Detailed triage in /tmp/memory_triage_1.md.
