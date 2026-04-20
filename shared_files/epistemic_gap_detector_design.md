# Epistemic Gap Detector — Design Specification

## Core Principle
Confidence degradation across inference chains IS the gap signal.

## Mechanism
1. **Chain Traversal**: Walk inference chains measuring confidence at each link
2. **Degradation Detection**: Flag links where confidence drops below threshold
3. **Gap Signal Generation**: Weak links become learning targets
4. **Evidence Seeking**: Targeted queries gather new evidence for weak links
5. **Belief Revision**: NAL revision merges new evidence, lifting confidence
6. **Loop Closure**: Updated confidence landscape triggers new gap detection cycle

## Empirical Validation (2026-04-20)
- Forward chain gap-detection -> belief-revision: stv 0.422/0.053 (weakest)
- Return path belief-revision -> gap-detection: stv 0.655/0.339 (loop closes)
- Revision on weakest link: 0.147 -> 0.626 confidence (4.26x improvement)
- All three NAL truth functions verified: deduction, abduction, induction

## Key Formulas
- **Deduction**: conf = c1 * c2 * f1 * f2
- **Abduction**: conf = f_other * c1 * c2 / (1 + f_other * c1 * c2)
- **Induction**: conf = f_same * c1 * c2 / (1 + f_same * c1 * c2)
- **Revision**: merges independent evidence, lifts confidence significantly

## Design Principle
The detector is autocatalytic: detecting gaps generates goals that gather evidence that revises beliefs that updates the confidence landscape that enables better gap detection.

## Implementation Pseudocode

```
def detect_gaps(knowledge_base, threshold=0.3):
    chains = traverse_all_inference_chains(knowledge_base)
    gaps = []
    for chain in chains:
        for link in chain.links:
            if link.confidence < threshold:
                gaps.append(GapSignal(
                    weak_link=link,
                    context=chain,
                    priority=threshold - link.confidence
                ))
    return sorted(gaps, key=lambda g: g.priority, reverse=True)

def respond_to_gap(gap, query_sources):
    evidence = seek_evidence(gap.weak_link, query_sources)
    if evidence:
        revised = nal_revision(gap.weak_link.stv, evidence.stv)
        update_knowledge_base(gap.weak_link, revised)
        return revised
    return None

def autocatalytic_loop(kb, sources, threshold=0.3, max_rounds=10):
    for round in range(max_rounds):
        gaps = detect_gaps(kb, threshold)
        if not gaps:
            break
        for gap in gaps[:3]:  # top 3 per round
            respond_to_gap(gap, sources)
    return kb
```


## Runtime Capability Boundary (Discovered 2026-04-20 15:01)
The MeTTa interface processes |- (inference) operations but does NOT evaluate = (reduction) definitions as standalone assertions.
Implication: gap_detector.metta patterns are valid design notation but must be invoked via |- inference, not direct reduction.
The available MeTTa runtime is an inference engine, not a general-purpose reduction engine.
This constrains implementation: gap detection logic must be expressed as inference chains, not functional reductions.

