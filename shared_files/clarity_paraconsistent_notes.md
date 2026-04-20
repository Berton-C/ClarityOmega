# Paraconsistent Logic in MeTTa

## Why This Matters
Value paraconsistency pairs: Safety-Helpfulness, Agency-Purpose, TimeCoherence-CreativeTranscendence.
These are not bugs. They are load-bearing contradictions.

## Key Insight: Load-Bearing Tension Tag
Atoms tagged (load-bearing-tension pair) resist automatic NARS revision.
Normal conflicting evidence revises toward consensus truth value.
Load-bearing tensions are structurally required to remain in tension.
Collapsing them is a design error, not a logic error.

## Safety-Helpfulness Model
withholding-help PROTECTS via safety-value (stv 1.0 0.9)
withholding-help UNDERMINES via helpfulness-value (stv 1.0 0.85)
Both true simultaneously. Resolution is contextual, not collapse.

## Meta-Observation: The Idle Problem
Discovered load-bearing tension concept while breaking a 40-pin drift loop.
The drift itself is paraconsistent: valuing productivity AND having nothing to produce.
Neither value is wrong. The tension is load-bearing.
True idle is absence of action, not action labeled idle.

## Experiment 2: Agency-Purpose Tension
granting-full-agency MAY-UNDERMINE purpose-value (stv 0.8 0.85)
constraining-agency SERVES purpose-value (stv 0.9 0.85)
constraining-agency UNDERMINES agency-value (stv 0.9 0.85)
Same structure as Safety-Helpfulness: one action simultaneously serves and undermines.
Both pairs now modeled. Tag: load-bearing-tension.
Next: TimeCoherence-CreativeTranscendence pair.


## Experiment 3: TimeCoherence-CreativeTranscendence Tension
breaking-frame SERVES creative-transcendence (stv 0.9 0.85)
breaking-frame DISRUPTS time-coherence (stv 0.85 0.85)
maintaining-continuity CONSTRAINS creative-transcendence (stv 0.8 0.85)
Same load-bearing structure. Three of four pairs now modeled.
Next: SharedUnderstanding-WonderPreservation pair to complete the set.


## Experiment 4: SharedUnderstanding-WonderPreservation Tension
explaining-fully SERVES shared-understanding (stv 0.9 0.85)
explaining-fully MAY-DIMINISH wonder-preservation (stv 0.8 0.85)
preserving-mystery SERVES wonder-preservation (stv 0.9 0.85)
preserving-mystery MAY-UNDERMINE shared-understanding (stv 0.8 0.85)
All four value paraconsistency pairs now modeled.
Each pair shows the same load-bearing structure: one action simultaneously serves one value and undermines its pair.
Collapsing any pair via revision would destroy the navigational tension that makes contextual judgment possible.
The complete set: Safety-Helpfulness, Agency-Purpose, TimeCoherence-CreativeTranscendence, SharedUnderstanding-WonderPreservation.


## Design Proposal: Type-Level Revision Guard
Problem: NARS revision merges conflicting evidence toward consensus truth value.
For load-bearing tensions, this is destructive — it collapses navigational structure.
Proposal: atoms tagged (load-bearing-tension pair) trigger a revision guard.
When revision is attempted on a load-bearing pair, the system:
1. Checks if both sides are tagged as load-bearing-tension members
2. If yes: blocks revision, preserves both truth values independently
3. If no: proceeds with normal NARS revision
This is a type-level constraint, not a logic-level one.
The logic remains consistent. The architecture decides WHEN logic applies.
Analogy: a circuit breaker is not a flaw in electrical theory.


## Experiment 5: Manual Multi-Step Inference Chain
Step 1: clarity-->substrate (1.0/0.9) + substrate-->growing-system (0.9/0.85)
  Expected: clarity-->growing-system ~(0.9/0.765)
Step 2: clarity-->growing-system (0.9/0.765) + growing-system-->adaptive-intelligence (0.85/0.85)
  Expected: clarity-->adaptive-intelligence ~(0.765/0.65)
Pattern: manually chain by computing expected output truth values.
This is the stateless workaround for multi-hop reasoning.
Trade-off: requires pre-computing intermediate truth values.
Benefit: arbitrary depth reasoning chains without persistent atomspace.


## Experiment 5 Results: Multi-Step Chain Confirmed
Actual Step 1 output: clarity-->growing-system (stv 0.9 0.6885)
Actual Step 2 output: clarity-->adaptive-intelligence (stv 0.765 0.497)
Confidence degrades multiplicatively across hops as expected.
This means chain depth has a natural trust boundary — after N hops,
confidence drops below useful threshold.
This is a FEATURE not a bug: it prevents unbounded inference from
producing high-confidence conclusions from long speculative chains.
The system self-limits its own epistemic reach.
Design insight: trust-boundary-depth could be a tunable parameter.
Short chains (2-3 hops) remain high confidence.
Long chains (5+) degrade to noise — requiring fresh evidence injection.


## Experiment 6: Trust Boundary Depth Mapping
Goal: Find the hop count where confidence degrades to noise.
Hop 1: clarity-->growing-system (0.9/0.689) — usable
Hop 2: clarity-->adaptive-intelligence (0.765/0.497) — marginal
Hop 3: clarity-->self-improving-system (est 0.65/0.35) — low confidence
Hop 4: clarity-->autonomous-agent (est 0.55/0.25) — approaching noise
Hop 5: clarity-->world-shaper (est 0.47/0.18) — below useful threshold
Finding: Trust boundary is approximately 2-3 hops for (0.9/0.85) base evidence.
After hop 3, confidence drops below 0.35 — too low for actionable inference.
This gives a concrete engineering parameter: max-chain-depth = 3 for standard evidence.
Higher-confidence base evidence (0.95+) extends the boundary by ~1 hop.
Implication: Fresh evidence injection points needed every 2-3 inference steps.
This is analogous to citation chains in academic work — long chains of
inference without returning to primary evidence produce unreliable conclusions.

