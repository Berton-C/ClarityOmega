# Compass Multi-Cycle Scoring Protocol

## Problem
metta skill calls are per-cycle. Scoring a response requires multiple deduction + revision calls.

## Solution: State Machine
Phases:
1. DRAFT - response text ready, pin it as working memory
2. DEDUCE - gen_deduction_exprs produces N expressions, execute up to 4 per cycle
3. REVISE - gen_revision_exprs from deduction results, execute per cycle
4. EVALUATE - check final scores against thresholds
5. SEND or REWRITE - if pass send, if fail generate correction guidance and redraft

## State Tracking
Use pin to track: current phase, pending expressions, accumulated results

## Cycle Budget
Typical response hits 4-8 tokens across 4 dimensions.
Deduction: 2 cycles at 4 metta calls each
Revision: 1 cycle at up to 4 revision calls
Evaluate+Send: 1 cycle
Total: 4-5 cycles from draft to send

## Integration Point
Replace compass_hook.check_response Python call with this multi-cycle protocol.
compass_metta_pipeline.py generates all expressions.
metta skill executes all truth value math.
