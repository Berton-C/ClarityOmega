# Corner-Gate v3 Coupling-Legibility Payload Manifest

**Payload revision:** A.5  
**Installation revision:** B.3  
**Status:** RATIFICATION CANDIDATE  
**Date:** 2026-07-12

## Corrective change

A.4 placed the callable symbol `write-file` in the head position of an
expression intended as list data. The production transpiler interpreted the
expression as a function invocation and aborted payload compilation.

A.5 uses an inert tag and removes it with `cdr-atom`:

```metta
(= (coupling-known-heads)
   (let $tagged
        (coupling-known-heads-data
          write-file append-file shell remember read-file query episodes metta
          send pin search tavily-search technical-analysis)
     (cdr-atom $tagged)))
```

This returns the exact original known-command list while preventing callable
head interpretation.

## Frozen artifact identities

```text
0665131e1491bced69a8ab3e5870637a6a9757b45375fee3095d17ade540cc81  coupling_legibility.metta
50662dc45167fa044bec280d4da47f6f67dafaf8c10f7e6ce9c8a7a65ecfc940  coupling_legibility_writers.metta
de3183e1f3504e2201d6ef80ec6e6650534b80d491e4df7efa38a099f1e87e54  coupling_legibility_helper_payload.py
6eef7fbfabbc904be9adeaedac0126b4dc0c86768e8e7427140f5b8f072efb4f  apply_corner_gate_v3_monolith.py
d27ead5d76fb92cb66ca71f1a6223cc9f35d3b4757feae63d6816a54cdc1a8c9  validate_corner_gate_v3_monolith.py
dc58e68b2eb523a46626b530164a338f0380a0250453416a05fe89e7b9c753e0  validate_corner_gate_v3_candidate_closure.py
29eeeeed72c0659856666bbca887ffdc4b28bd7815b5d5ff62dd5fa23cadf66e  patch_corner_gate_v3_a5_b3.py
```

## Required pre-apply commands

```bash
python3 staging/apply_corner_gate_v3_monolith.py \
  --repo-root . \
  --dry-run

python3 staging/validate_corner_gate_v3_candidate_closure.py \
  --repo-root . \
  --image clarityomega-clarityclaw:latest \
  --platform linux/amd64 \
  --evidence-log /tmp/cg-v3-a5-b3/evidence/v3_candidate_import_closure.log
```

## Apply command

```bash
python3 staging/apply_corner_gate_v3_monolith.py \
  --repo-root . \
  --apply
```

## Reverse command

```bash
python3 staging/apply_corner_gate_v3_monolith.py \
  --repo-root . \
  --reverse \
  --apply
```

## Required semantic results

```text
schema                     v3-18-field
write-file surface         runtime-output
write-file command class   action-class
unknown-head surface       no-contact
unknown-head class         neutral
```

The exact known-head list remains:

```text
(write-file append-file shell remember read-file query episodes metta
 send pin search tavily-search technical-analysis)
```

The candidate validator must also prove that `gate-aware-results` appends a
ground `COUPLING-STATE-LINE` while preserving `probe-result`.

## Evidence basis

See:

```text
CG3_RUNTIME_CRASH_INVESTIGATION.md
evidence/
```
