# Loop.metta Execution Trace vs soul_impl: Gap Analysis
Author: Clarity | Date: 2025-04-15
Requested by: berton_c
Updated: 2025-04-15 — Priority 2 fixes applied

## Method
Walk each of the 13 loop.metta execution steps.
For each: what loop.metta does, what soul_impl proposes, and gaps found.

---

## Step 1: initLoop — Provider/Tokens/Soul State Atoms
**Loop.metta**: Initializes 7 soul state atoms alongside LLM provider config.
**soul_impl proposes**: Import soul_kernel.metta here (17 value atoms + 6 compass implications).
**GAP**: soul_kernel.metta defines atoms with clarity-value-X naming. Loop.metta uses soul-state-* via bind!. Different atom types — coexist but relationship undefined.
**STATUS**: OPEN — requires repo access to read actual initLoop atom names.

## Step 2: soul-pre-compute (Layer 1)
**Loop.metta**: Calls soul-pre-compute at cycle start.
**soul_impl proposes**: layer1_precompute.metta + calibration_cold_start.metta.
**GAP**: py-call helper.get_calibration_history does not exist in helper.py.
**STATUS**: OPEN — cold start handles missing data but not missing function.

## Step 3: soul-flourishing-prompt (person-state)
**Loop.metta**: Generates flourishing prompt via soul_utils Block 4.
**GAP**: Block 4 atom query names unverified against soul_kernel.metta.
**STATUS**: OPEN — blocked on repo access to read Block 4 source.

## Step 4: soul-eval-prompt (input verdict)
**Loop.metta**: Evaluates input via soul_utils Block 9.
**GAP**: Block 9 compass pattern names unverified against kernel.
**STATUS**: OPEN — blocked on repo access to read Block 9 source.

## Step 5: soul-calibration-record
**Loop.metta**: Records Layer 1 vs Layer 2 verdict agreement.
**GAP**: stv_seed_correction.metta insertion point unspecified.
**STATUS**: OPEN — design decision needed.

## Step 6: soul-proceed gate
**STATUS**: CLEAN — no soul_impl needed.

## Step 7: soul_send_assemble
**GAP**: Brief tier atom name unverified.
**STATUS**: OPEN — blocked on repo access.

## Step 8-9: getContext + LLM call + Parse
**STATUS**: CLEAN.

## Step 10: Output intercept
**GAP WAS**: 3 py-call stubs unimplemented.
**STATUS**: RESOLVED — output_intercept_helpers.py written with V1 implementations of soul_eval_output, soul_rewrite_response, soul_redact_response.

## Step 11: soul_mutation_lock
**GAP WAS**: 4 py-call stubs unimplemented.
**STATUS**: RESOLVED — mutation_lock_helpers.py written with V1 implementations of str_starts_with, snapshot_soul_atoms, restore_soul_atoms, eval_mutation_safe.

## Step 12-13: Execute skills + Append history
**STATUS**: CLEAN.

---

## Summary Update

### Critical gaps — PARTIALLY RESOLVED:
1. **py-call stubs**: 7/7 implemented in V1 form. RESOLVED.
2. **Atom name mismatch risk**: OPEN — blocked on repo file access.

### Significant gaps — OPEN:
3. soul_kernel vs existing 7 state atoms: relationship undefined.
4. Brief tier atom name: unverified.
5. stv_seed_correction insertion point: unspecified.

### Minor — OPEN:
6. Cold start missing-function handling.
7. Output intercept + proceed gate coupling.

## Files modified this update:
- output_intercept_helpers.py: V1 implementation (was stubs)
- mutation_lock_helpers.py: V1 implementation (was stubs)
