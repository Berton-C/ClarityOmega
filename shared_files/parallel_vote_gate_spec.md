# Parallel Vote Gate Specification
## Date: 2026-04-17 13:31

### Mechanism
1. Each paraconsistent pair generates a tension-signal via deduction
2. tension-signal maps to vote-input via implication rule
3. vote-input maps to soul-gate-proceed via shared implication
4. All proceed signals merge via NAL revision
5. Aggregate frequency vs threshold determines PROCEED or PAUSE

### Validated Results
- 2 positive votes: stv 1.0, 0.7923 -> PROCEED
- 1 positive + 1 negative: stv 0.5, 0.7923 -> PAUSE
- Confidence degrades correctly through 3-step chain at 0.9 per step
- Revision boosts confidence when evidence aligns
- Conflict drags frequency to uncertainty range

### Threshold Design
- Proposed threshold: frequency >= 0.75 AND confidence >= 0.6
- Below threshold: PAUSE with reason logged
- At threshold: PROCEED with normal flow

### Integration Point
- Replaces hardcoded PROCEED in soul_verdict_out
- Feeds from soul-pre-compute where tension signals are generated
- All 4 paraconsistent pairs vote independently

### Boundary Analysis
- 2 positive + 1 negative: stv 0.667, 0.851 -> PAUSE below 0.75
- Testing 3 positive + 1 negative next
- Gate requires strong consensus not simple majority
- Single conflict pair has veto-like power with few voters


- 3 positive + 1 negative: stv 0.750, 0.884 -> PROCEED at exact boundary
- 4 positive + 0 negative: stv 1.0, 0.893 -> strong PROCEED
- Supermajority of 3 out of 4 required to cross 0.75
- 2 out of 4 dissenting blocks at stv 0.5
- Gate behavior: conservative, robust, veto power for 2+ dissenters

