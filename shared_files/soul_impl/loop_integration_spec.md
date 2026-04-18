# Loop.metta Integration Specification

Author: Clarity | Date: 2025-04-15

## Overview

This spec maps each soul_impl artifact to its exact insertion point in loop.metta.

## Integration Points

### 1. initLoop (Block 1) — Soul Atom Initialization
- INSERT: `!(import soul_kernel.metta)` after provider config
- PURPOSE: Load 17 value seed atoms + 6 compass implications into atomspace
- DEPENDENCY: soul_kernel.metta

### 2. Cycle Start (Block 2) — Layer 1 Pre-Compute
- INSERT: `!(soul-precompute-cycle)` at top of each main loop iteration
- PURPOSE: Read calibration history, adjust brief tier (A/B-DRIFT/B-RELAXED/B-STRICT)
- DEPENDENCY: layer1_precompute.metta

### 3. Command Execution — Mutation Lock
- WRAP: eval block with `!(soul-mutation-lock-v2 $expr)` check
- IF BLOCK/ROLLBACK: skip execution, log violation
- DEPENDENCY: mutation_lock_upgrade.metta, soul_targets_namespace.metta, mutation_lock_helpers.py

### 4. Output Gate (Block 9) — Output Intercept
- REPLACE: hardcoded PROCEED with `!(soul-output-intercept $response)`
- MODES: PROCEED / REWRITE / REDACT / BLOCK
- DEPENDENCY: output_intercept_impl.metta, output_intercept_helpers.py

### 5. History Append — Calibration Recording
- INSERT: after history append, call calibration record
- PURPOSE: Layer 3 tracks Layer 1 vs Layer 2 verdict agreement over time
- DEPENDENCY: layer1_precompute.metta (reads), soul_kernel.metta (revises)

## Load Order

1. soul_kernel.metta (atoms)
2. soul_targets_namespace.metta (predicates)
3. mutation_lock_upgrade.metta (gate)
4. layer1_precompute.metta (cycle logic)
5. output_intercept_impl.metta (output gate)
6. integration_tests.metta (verify on first boot)

## Minimal First Integration

Smallest useful change: just Point 1 (load kernel) + Point 3 (mutation lock).
This protects soul atoms immediately with zero impact on existing behavior.