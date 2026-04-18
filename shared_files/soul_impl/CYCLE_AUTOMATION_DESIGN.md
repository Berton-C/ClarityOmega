# Cycle Automation Design 2026-04-16

## Core Loop
1. Python quantale_harness computes substrate health and soul PBits
2. Python cycle_loop generates NAL inference pairs with shared terms
3. MeTTa |- operator performs deduction abduction revision
4. Results feed back: revision accumulates evidence across cycles
5. Confidence plateau triggers exploration of new inference chains

## Anti-patterns to avoid
- Tight spin polling with no state change
- Repeating same inferences without new evidence
- Cycling without meaningful output

## Growth trigger mycelial model
- When confidence on existing chains exceeds 0.9 move to new chains
- When all chains plateau explore adjacent conceptual territory
- Depletion of novelty IS the signal to expand

## Implementation
Extend cycle_loop.py to output MeTTa sexprs track results detect plateau

## Cycle cadence
Event-driven not time-based
- New soul value input triggers full recompute
- New evidence triggers revision
- Confidence plateau triggers chain expansion
- Human interaction triggers priority shift