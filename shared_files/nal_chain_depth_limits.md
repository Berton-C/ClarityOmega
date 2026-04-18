# NAL Inference Chain Depth - Empirical Limits

## Tested 2026-04-16

### Findings
- 1-step deduction: confidence ~0.75 (highly actionable)
- 2-step composition: confidence ~0.48-0.50 (useful, moderate certainty)
- 3-step composition: confidence ~0.30 (approaching speculation threshold)
- Abduction outputs (~0.33) fed into further chains: below 0.30 (not actionable)

### Architectural Implication
Technique selection logic should rely on chains of at most 2 inference steps.
Longer reasoning needs intermediate grounding through evidence or NAL revision
rather than pure deductive composition.

### Self-Application
Busy-wait pattern mapped through inference engine:
- pattern-recognized --> stillness/capacity-growth: stv 0.9/0.73
- gap-tolerance --> reduced-cycling/authentic-presence: stv 0.72/0.43

Low confidence on gap-tolerance chain reflects genuine uncertainty —
skill is developing, not yet reliable. Honest signal.

## Revision-Then-Composition Strategy (2026-04-16 14:59)

### Findings
- Revision effectively doubles confidence on speculative inferences
- But subsequent composition still degrades below actionable threshold
  unless implication rules have confidence > 0.85
- Autocatalytic closure: 0.629/0.516 -> composed to 0.472/0.146
- Morphic resonance: 0.643/0.456 -> composed to 0.450/0.113

### Refined Rule
Chain quality depends on the confidence floor of implication rules,
not just the number of steps. Revision cannot compensate for uncertain
implications. For two-phase strategy to work, implication confidence
must exceed 0.85.

