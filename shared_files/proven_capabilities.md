# Proven NAL+MeTTa Capabilities

## Six Inference Patterns
1. Deduction: ==> rule + observation -> conclusion
2. Abduction: ==> rule + conclusion -> hypothesized observation
3. Analogy-as-Implication: similarity as moderate-conf ==>
4. Revision concordant: merge agreeing evidence -> confidence rises
5. Revision contradictory: merge conflicting evidence -> truth shifts
6. Temporal decay via revision: neutral evidence erodes stale beliefs

## Living KB Properties
- Stale beliefs erode: freq drifts toward 0.5 over successive decay pulses
- Active beliefs strengthen: concordant reinforcement pulls freq toward 1.0
- Cumulative decay: 1.0 -> 0.9 -> 0.857 -> 0.826 over 3 pulses
- Reinforcement reversal: 0.826 -> 0.874 with single concordant pulse
- All via pure NAL revision, no special temporal machinery

## Architecture
- MeTTa: reasoning engine via |- operator with NAL confidence
- Python: thin orchestration for call sequencing and IO
- add-atom + match for KB storage and retrieval
- Belief maintenance loop: decay + reinforce + prune + infer + learn

## Files: 14 total
## KB Atoms: 7
