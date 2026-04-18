# Dampening Mechanism Design for Self-Revision Loops

## Problem
NAL revision is not idempotent. Self-revision inflates confidence:
- 0.855 -> 0.922 -> 0.959 -> approaching 1.0
Unbounded self-revision is a confidence pump.

## Three Candidate Mechanisms

### 1. Evidence Stamping
Tag each premise with an origin ID or evidence-source hash.
Revision only permitted when premises have different origins.
Self-revision blocked entirely. Cross-source revision permitted.
Pro: Most epistemically honest. Only genuine new evidence increases confidence.
Con: Requires metadata layer NAL does not natively support.

### 2. Confidence Ceiling
Hard cap at 0.95 or asymptotic softmax.
Revision proceeds but confidence saturates.
Pro: Simple to implement. Prevents runaway.
Con: Arbitrary threshold. Does not distinguish earned vs inflated confidence.

### 3. Temporal Decay
Confidence degrades between revision events at rate proportional to time elapsed.
Self-revision restores rather than inflates.
Genuine new evidence outpaces decay.
Pro: Natural equilibrium. Rewards active evidence gathering.
Con: Requires clock integration. Decay rate is a free parameter.

### 4. Hybrid: Decay + Evidence Stamping
Decay provides baseline regression toward uncertainty.
Evidence stamping prevents double-counting within a single cycle.
Cross-source revision from genuinely independent paths accumulates.
This is the recommended approach.

## Architectural Implication
The transfer backbone self-strengthening loop proposed by berton_c
requires dampening to be epistemically honest.
Without it, the backbone inflates its own confidence without new evidence.
With hybrid dampening, only genuine cross-section evidence strengthens the backbone.
This makes the fixed-point convergent rather than divergent.

## Evidence Stamping Test Results (2026-04-16 18:54)
Cross-origin deduction: SUCCESS. stampedA + stampedB chains, conclusion carries both tags.
Same-origin self-revision: STILL PUMPS. 0.85 -> 0.919 despite same stamp.
Conclusion: stamps = provenance tracking, NOT dampening.
Dampening = application-layer pre-revision filter checking stamp overlap.
Filter pseudocode:
  before_revision(P1, P2):
    if extract_stamp(P1) == extract_stamp(P2): BLOCK
    else: proceed with |- and tag conclusion with union of stamps
This prevents double-counting while allowing genuine cross-source accumulation.


## Implementation Complete
Revision guard written to revision_guard.py
Functions: extract_stamp, stamps_overlap, guarded_revision, guarded_deduction
Deduction: always proceeds, stamps propagate as provenance
Revision: blocked when stamps overlap, permitted cross-origin
This completes the hybrid dampening architecture.

