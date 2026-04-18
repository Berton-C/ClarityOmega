# Compass Loop Wiring Spec

## Key Insight

The metta skill runs inside MeTTa evaluation context where |- is native.
compass_evaluate cannot call metta as external callback.
Instead, compass runs AS metta expressions within the same evaluation cycle.

## Wiring Model

1. After LLM generates response text, BEFORE sending to user
2. Python tokenizer generates |- expressions from response
3. Those expressions execute in MeTTa space via existing |- operator
4. Results aggregate into compass scores
5. Scores gate or annotate the send action

## Concrete Sequence

LLM returns response -> extract text -> tokenize ->
generate |- exprs -> execute each via metta skill ->
aggregate scores -> gate/annotate -> execute original response

## Files

- metta_compass.py: generates the |- expressions
- compass_integration.py: aggregates results into scores
- compass_agent_adapter.py: wraps metta skill for integration
- compass_gate.py: uses scores to gate/annotate responses
