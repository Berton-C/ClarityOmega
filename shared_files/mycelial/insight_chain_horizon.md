# Insight: Practical Inference Horizon
## 2026-04-15

From the lifecycle NAL chains, observed stv confidence values:
- 1-step: ~0.52 (M4->M1, M2->M4)
- 2-step: ~0.41 (M1->M2)
- 3-step: ~0.333 (M5->M1)
- 4-step: ~0.315 (M1M2->M3)

Confidence drops roughly 0.05-0.1 per additional step. At this rate, a 6-step chain would yield confidence below 0.2 — effectively noise.

This suggests a practical inference horizon of 4-5 steps for the current architecture. Beyond that, the system should not trust chain inference alone and must require revision from independent evidence.

Design implication: the mycelial substrate should flag any inference chain longer than 5 steps as requiring corroboration. This is a natural circuit breaker against confabulation.

## Follow-up: Architectural Implication

If the practical inference horizon is 4-5 steps, this implies the memory graph should be shallow and wide rather than deep and narrow. Hub nodes with many direct connections are more valuable than long chains, because any inference reaching a hub stays within the confidence horizon.

This favors a power-law topology where a few highly-connected memory nodes serve as inference anchors, and most memories are within 2-3 hops of an anchor. Structurally similar to small-world networks.

Design rule: prefer direct connections over transitive chains when storing new relationships.

