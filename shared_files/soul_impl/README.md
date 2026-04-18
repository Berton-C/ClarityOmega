# soul_impl/ — Soul Implementation Artifacts

Created: 2025-04-15 | Updated: 2025-04-15
Author: Clarity

## Files (19)

| File | Purpose | Status |
|------|---------|--------|
| soul_kernel.metta | 17 value seed atoms + 6 compass implications | ROOT |
| soul_nal_unification.md | World map: soul atoms as NAL premises, full architecture | REFERENCE |
| output_intercept_impl.metta | Production output intercept for soul_verdict_out | COMPLETE |
| output_intercept_draft.metta | Annotated draft with design rationale | REFERENCE |
| output_intercept_helpers.py | V1: soul_eval_output, rewrite, redact | IMPLEMENTED |
| mutation_lock_upgrade.metta | Recursive tree-walk lock v2 + snapshot rollback | COMPLETE |
| mutation_lock_helpers.py | V1: str_starts_with, snapshot, restore, eval_mutation | IMPLEMENTED |
| layer1_precompute.metta | Calibration history drives brief tier adjustment | COMPLETE |
| calibration_cold_start.metta | Graceful degradation for missing calibration data | COMPLETE |
| stv_seed_correction.metta | Self-correcting seed strategy via NAL revision | COMPLETE |
| soul_targets_namespace.metta | Predicate: detects soul namespace references | COMPLETE |
| integration_tests.metta | 10 smoke tests across all predicates | COMPLETE |
| run_validation.metta | Validation harness, loads all files in order | COMPLETE |
| loop_trace_gap_analysis.md | 13-step trace, 7 gaps found, 2 resolved | UPDATED |
| atom_name_crossref.md | Kernel vs soul_utils atom name comparison | UPDATED |
| loop_integration_spec.md | Integration specification | REFERENCE |
| soul_architecture_reference.md | Quick reference for loop.metta blocks | REFERENCE |
| soul_constraint_test.md | Constraint test documentation | REFERENCE |
| README.md | This file | CURRENT |

## Gap Status Summary
- Priority 2 RESOLVED: 7/7 py-call stubs now have V1 implementations
- Priority 1 OPEN: Atom name crossref blocked on repo file access
- 5 additional gaps documented in loop_trace_gap_analysis.md

## Dependency Graph

    soul_kernel.metta (ROOT)
        |
    layer1_precompute.metta --> calibration_cold_start.metta
    output_intercept_impl.metta --> output_intercept_helpers.py
    mutation_lock_upgrade.metta --> soul_targets_namespace.metta
                                --> mutation_lock_helpers.py
    stv_seed_correction.metta (standalone, insertion point TBD)

## Blocking: repo file access needed for soul_utils.metta and loop.metta


## Parallel Vote Gate (2026-04-17)
- parallel_vote_gate.metta: NAL 5-step chain for 4 paraconsistent pairs
- vote_threshold.metta: threshold check at 0.75 freq 0.6 conf
- vote_gate_bridge.py: Python fallback with NAL revision approximation
- gate_integration_wiring.metta: exact wiring into loop.metta Block 2
- Boundary: 3/4 aligned=PROCEED, 2/4=PAUSE, supermajority required



## Counterfactual Reasoning Method (2026-04-17)
- counterfactual_method.metta: formalized two-method protocol
- NEGATION: stv 0.0 -> epistemic vacuum, proves causal dependency
- SUBSTITUTION: swap premise -> comparable output, reveals causal contribution
- Delta between factual and counterfactual = causal responsibility measure
- Tenth validated NAL capability in substrate toolkit



## Analogy Reasoning VALIDATED (2026-04-17)
- analogy_validated.metta: two-step compound confirmed
- Step 1: abduction from shared property -> bidirectional similarity stv 1.0/0.461
- Step 2: deduction via similarity rule -> property transfer stv 0.8/0.504
- 12th validated NAL capability, first gap closed from self-model growth vector
- Remaining gaps: induction, temporal-reasoning, multi-agent-modeling



## Induction Reasoning VALIDATED (2026-04-17)
- induction_validated.metta: evidence accumulation pipeline confirmed
- stv 1.0/0.448 per instance -> stv 1.0/0.618 after merging two instances
- 13th validated NAL capability, second gap closed from growth vector
- Remaining gaps: temporal-reasoning, multi-agent-modeling



## Temporal Reasoning VALIDATED (2026-04-17)
- temporal_validated.metta: sequence-aware inference confirmed
- Causal enablement from temporal ordering at stv 1.0/0.765
- 14th validated NAL capability
- Remaining gap: multi-agent-modeling



## Multi-Agent Modeling VALIDATED (2026-04-17)
- 15th and FINAL planned NAL capability
- ALL 15 PLANNED CAPABILITIES NOW VALIDATED

