# Compass Integration - Ready for Agent Loop

## Status: VALIDATED on Real MeTTa

All compass expressions execute through live |- operator and return numeric stv results.

## Entry Point

```python
from compass_e2e import compass_evaluate
result = compass_evaluate(draft_text, metta_fn)
# result = {'pass': bool, 'flags': [...], 'scores': {...}}
```

## metta_fn Contract

- Takes: string MeTTa expression (e.g. '(|- ((--> X Y) (stv f c)) ...)')
- Returns: string MeTTa result (e.g. '[((--> X Z) (stv f c))]')
- This maps directly to the agent loop metta skill

## Files

1. metta_compass_real.py - tokenizer + expression generator
2. stv_parser.py - parses metta output to numeric stv
3. compass_gate.py - threshold gating on scores
4. compass_e2e.py - main entry point (compass_evaluate)
5. compass_agent_adapter.py - adapter patterns
6. compass_loop_wiring.md - architecture spec
7. compass_real_test.py - real value validation
8. compass_live_test.py - live expression documentation

## Confirmed Real MeTTa Results

- agency deduction: f=0.765 c=0.6561
- wonder deduction: f=0.855 c=0.69
- thinking deduction: f=0.9 c=0.73
- attention deduction: f=0.765 c=0.62
- agency revision: f=0.713 c=0.726
- wonder revision: f=0.835 c=0.794
