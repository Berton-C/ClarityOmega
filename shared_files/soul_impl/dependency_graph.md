# Substrate Dependency Graph
## Generated 2026-04-16 10:13

Shows which files reference which, based on cross-reference scan.

### Core Kernel (most referenced)
- **soul_kernel.metta** — referenced by:
  - berton_soul_kernel.metta, berton_soul_utils.metta, run_validation.metta
  - soul_loop.metta, soul_phase2_prototype.metta, soul_targets_namespace.metta
  - source_to_kernel_mapping.md, soul_architecture_reference.md
  - soul_constraint_test.md, soul_nal_unification.md
  - substrate_manifest.md, SUBSTRATE_INDEX.md, README.md

### Compass Cluster
- **compass_metta.metta** <-- compass_scenario_tests.metta, compass_scenario_tests_v2.metta, cross_domain_transfer_test.metta, decision_card_prototype.md, decision_card_002.md, response_compass_prototype.metta

### Flourishing Cluster
- **flourishing_source_atoms.metta** <-- flourishing_source_atoms_v2.metta, mycelial_loop.metta
- **flourishing_source_atoms_v2.metta** <-- integration_tests.metta, layer1_precompute.metta

### Idle/Loop Management Cluster (new, 2026-04-16)
- **idle_loop_constraint.md** <-- sleep_primitive_spec.md, idle_goal_queue.md, mycelial_loop.metta
- **idle_goal_queue.md** <-- (self-referencing task log)
- **mycelial_loop.metta** <-- sleep_primitive_spec.md
- **sleep_primitive_spec.md** <-- (terminal node, references idle_loop_constraint.md and mycelial_loop.metta)

### Output Intercept Chain
- **output_intercept_draft.metta** --> output_intercept_impl.metta --> output_intercept_helpers.py

### Mutation Lock Chain
- **mutation_lock_upgrade.metta** <-- mutation_lock_helpers.py, person_state_staleness_fix.metta

### Calibration
- **calibration_cold_start.metta** <-- stv_seed_correction.metta

### Index/Meta Files
- **SUBSTRATE_INDEX.md** — references nearly all files
- **substrate_manifest.md** — references all files (one-line descriptions)
- **README.md** — references key entry points
- **atom_name_crossref.md** — references all .metta files
- **loop_trace_gap_analysis.md** — references loop_integration_spec.md, soul_loop.metta

### Isolated Files (no inbound references detected)
- epistemic_gap_detector.metta
- metta_runtime_findings.md
- test_python_helpers.py

## Structural Notes
- soul_kernel.metta is the highest-connectivity hub (13+ references)
- The idle/loop cluster is self-contained and internally coherent
- 3 files appear isolated — candidates for integration or pruning per artifact_quality_checklist.md Q5
