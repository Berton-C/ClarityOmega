# Clarity NAL Architecture - Unified System Design

## Core Principle
All reasoning, learning, and memory maintenance use a single mechanism:
NAL revision via MeTTa |- operator with truth values stv freq conf.

## Cognitive Cycle
1. Perceive: input arrives with initial truth value
2. Infer: deduction, abduction, analogy - chain length degrades confidence
3. Decide: threshold gating halts low-quality chains, shortcuts preferred
4. Act: highest-confidence action selected, outcome predicted
5. Learn: observe outcome, revise with concordant or contradictory evidence
6. Maintain: decay erodes stale beliefs, reinforcement preserves active ones

## Proven Results
- Deduction propagation: 0.85 -> 0.765
- 3-step chain: 0.85 -> 0.52
- Shortcut vs chain: 0.595 vs 0.52
- Cumulative decay: 1.0 -> 0.826 over 3 pulses
- Reinforcement reversal: 0.826 -> 0.874
- Threshold gating: low-conf -> halt-chain at 0.72
- Chain collapsing: multi-step -> single rule at 0.63

## Seven Inference Behaviors
1. Deduction 2. Abduction 3. Analogy 4. Concordant revision
5. Contradictory revision 6. Temporal decay 7. Threshold gating

## Files: 15 total | KB Atoms: 7


## KB Bridge - Substrate Persistence
- kb_bridge.metta: serialized KB atoms to disk
- kb_loader.py: reads atoms back from disk
- kb_reload.py: generates MeTTa add-atom commands for re-injection
- Round-trip: live KB -> serialize -> disk -> reload -> live KB
- This enables continuity across session boundaries
- Sixteen files total

