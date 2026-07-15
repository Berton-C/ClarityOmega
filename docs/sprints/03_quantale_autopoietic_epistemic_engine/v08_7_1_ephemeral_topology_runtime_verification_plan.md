# v08.7.1 Ephemeral Topology Runtime Verification Plan

## Purpose

This plan answers the implementation-order concern without touching current runtime files.

The previous v01.4 harness staged the engine and ladder into the container `/tmp`, verified their container-side hashes, and ran MeTTa probes through `docker exec clarity_omega ... /PeTTa/run.sh`. That aligned with the better verification path for the cold engine/ladder artifacts.

The missing layer was the v08.7 persistence topology itself:

```text
memory/evolutionary/
  README.metta
  index.metta
  runtime.metta
  pending.metta
  validation.metta
  restart.metta
  rejected.metta
  archive/

soul/durable.metta
```

v01.5 adds an isolated container `/tmp` topology so these files can be populated, parsed, and queried under the runtime without modifying `/PeTTa/repos/omegaclaw` or any bind-mounted runtime project file.

---

## What v01.5 Does

In runtime mode, with `--ephemeral-topology-runtime`, the harness now:

1. Copies the engine into container `/tmp`.
2. Copies the ladder into container `/tmp`.
3. Verifies container-side SHA-256 for both artifacts.
4. Creates an isolated directory:

```text
/tmp/v08_7_1_ephemeral_topology_under_test/
```

5. Populates this isolated tree:

```text
/tmp/v08_7_1_ephemeral_topology_under_test/memory/evolutionary/README.metta
/tmp/v08_7_1_ephemeral_topology_under_test/memory/evolutionary/index.metta
/tmp/v08_7_1_ephemeral_topology_under_test/memory/evolutionary/runtime.metta
/tmp/v08_7_1_ephemeral_topology_under_test/memory/evolutionary/pending.metta
/tmp/v08_7_1_ephemeral_topology_under_test/memory/evolutionary/validation.metta
/tmp/v08_7_1_ephemeral_topology_under_test/memory/evolutionary/restart.metta
/tmp/v08_7_1_ephemeral_topology_under_test/memory/evolutionary/rejected.metta
/tmp/v08_7_1_ephemeral_topology_under_test/memory/evolutionary/archive/
/tmp/v08_7_1_ephemeral_topology_under_test/soul/durable.metta
```

6. Ensures every non-comment line in those staged files is a boot-safe directive:

```metta
!(add-atom &self (...))
```

7. Builds a composite runtime probe inside the container by concatenating:

```text
container /tmp engine copy
+ container /tmp memory/evolutionary files
+ container /tmp soul/durable.metta
+ match queries
```

8. Runs the composite probe through:

```bash
cd /PeTTa && ./run.sh /tmp/_v08_7_1_ephemeral_topology_composite_probe.metta
```

9. Verifies that all staged atoms are queryable.

---

## What This Proves

This proves:

```text
The candidate engine bytes are visible inside the runtime container.
The candidate ladder bytes are visible inside the runtime container.
The v08.7 persistence topology can be populated safely in container /tmp.
Representative memory/evolutionary files are syntactically boot-safe.
Representative soul/durable.metta content is syntactically boot-safe.
The runtime can parse and query the staged files through /PeTTa/run.sh.
Process-memory atoms and durable-surface atoms can be represented without touching runtime project files.
```

---

## What This Does Not Claim

This still does not claim:

```text
The actual runtime soul_kernel.metta has been amended.
The actual runtime boot manifest imports soul/durable.metta.
The actual runtime memory/evolutionary files are production-ready.
The actual runtime durable canon has been activated.
```

Those remain implementation-phase tasks.

---

## Recommended Command

```bash
python3 staging/quantale_v08_7_1_hyperseed_durability_completion_harness_v01_5.py \
  --engine staging/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_1_HYPERSEED_DURABILITY_COMPLETION_CANDIDATE.metta \
  --ladder staging/quantale_engine_validation_ladder_v08_7_1_HYPERSEED_DURABILITY_COMPLETION_CANDIDATE.metta \
  --log-dir shared_files \
  --runtime \
  --ephemeral-topology-runtime \
  --container clarity_omega \
  --container-tmp-dir /tmp \
  --raw-mode fail \
  --raw-tail-chars 3000
```

Then run the full non-mutating pass:

```bash
python3 staging/quantale_v08_7_1_hyperseed_durability_completion_harness_v01_5.py \
  --engine staging/lib_quantale_autopoietic_epistemic_dynamics_engine_v08_7_1_HYPERSEED_DURABILITY_COMPLETION_CANDIDATE.metta \
  --ladder staging/quantale_engine_validation_ladder_v08_7_1_HYPERSEED_DURABILITY_COMPLETION_CANDIDATE.metta \
  --log-dir shared_files \
  --repo-root . \
  --inspect-topology \
  --inspect-governance \
  --validate-durable-file \
  --runtime \
  --ephemeral-topology-runtime \
  --container clarity_omega \
  --container-tmp-dir /tmp \
  --raw-mode fail \
  --raw-tail-chars 3000
```

Expected interpretation:

```text
PASS on ephemeral topology runtime composite probe:
  candidate topology content is runtime-parseable and queryable in container /tmp.

HOLD/FAIL on actual repo governance files:
  implementation work remains, but current runtime files were not modified.
```
