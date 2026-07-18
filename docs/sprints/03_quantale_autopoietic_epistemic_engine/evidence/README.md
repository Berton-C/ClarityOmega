# v08.7.2 Engine Evidence Surface

This directory holds the runtime-trace evidence for the v08.7.2 epistemic dynamics
engine, promoted out of `shared_files/` (which `.gitignore` ignores wholesale, so
these artifacts were one container cleanup from being lost) into tracked space so the
Research Programme document and any external reviewer can cite a durable path instead
of private scratch.

It is the proof-of-execution half of the engine's evidence. The spec-and-ladder half
already lives one level up in this sprint directory: the v08.7.2 validation ladder
(`quantale_engine_validation_ladder_v08_7_2_SOUL_EVOLUTIONARY_CANONICAL_TOPOLOGY.metta`),
the engine guide, the durable-evolutionary-governance handoff, and the design control
matrix. This directory adds what those cannot show on their own: the engine actually
reducing and producing its surfaces in a runtime-representative boot.

## Evidence vocabulary

Same ladder the programme document binds itself to, no lower rung implying a higher one:

- **LIVE**: running in the production cognitive loop, verified by exercise.
- **VERIFIED-ISOLATED**: built and proven in a harness or standalone boot, not in the
  live decision path.
- **VERIFIED-ISOLATED (runtime-representative)**: captured from a harness that boots the
  engine in the live-body or production-boot path and traces what actually reduced.
  Stronger than a pure standalone probe, weaker than LIVE. This is where every trace
  below sits.

What none of these traces claim: that the engine is wired into the live loop's
decisions. That remains SPECIFIED (the apply scripts exist in staging) per the
programme document Section 1.

## The traces, and what each proves

`runtime_traces/` (json is machine-readable, md is the human-readable companion):

- **v08_7_2_live_body_runtime_trace_20260706_105032** — the engine's live-body topology
  (durable, runtime, pending, validation, restart, rejected surfaces) computing at
  boot. Proves the topology reduces and populates in a runtime-representative boot.
  Backed by the 80-probe `_v08_7_2_live_body_*` suite.
- **v08_7_2_live_import_runtime_trace_20260706_091732 / _092754 / _094611** — the live
  semantic import surface: canon-eligibility, illegal runtime-to-canon jump blocked,
  validation-is-not-approval, genesis-output-without-route blocked, negative claims
  blocked. Proves the durability and canon semantics reduce live, three runs for
  stability. Backed by the 80-probe `_v08_7_2_live_import_*` suite and the captured
  outputs in `shared_files/raw_live_import_probe_outputs/`.
- **v08_7_2_production_boot_atomspace_trace_20260706_121837 / _122104** — the engine
  loaded on the production boot path with the atomspace inspected. Proves the engine
  loads and its atoms are present and queryable in production boot, two runs.
- **v08_7_2_query_surface_discovery_trace_20260706_132734** — discovery of the engine's
  queryable surfaces. Proves the exposed operations are discoverable live.

## Reproduction

Each trace regenerates from its harness (promoted here into `harnesses/`, source of
truth in `staging/`):

- live_body trace ← `quantale_v08_7_2_live_body_runtime_harness_v01_4.py`
- live_import traces ← `quantale_v08_7_2_live_import_runtime_harness_v01_2.py`
- production_boot traces ← `quantale_v08_7_2_production_boot_atomspace_inspection_harness_v01_0.py`
- query_surface trace ← `quantale_v08_7_2_production_query_surface_discovery_v01_1.py`
- soul-evolutionary topology ← `quantale_v08_7_2_soul_evolutionary_topology_harness_v01_6.py`

The probe suites they run over (the `_v08_7_2_live_body_*`, `_v08_7_2_live_import_*`,
and `_v08_7_2_production_boot_probe_*` inputs) stay in `shared_files/` as regenerable
inputs; they are reproducible from the harness plus the tracked engine and ladder, so
they are referenced rather than committed to avoid several hundred files of scratch
entering git. The lineage traces for the v08.7 durable-evolutionary-governance
protocol (`v08_7_durable_evolutionary_governance_trace_*`, 2026-07-05) are available in
`shared_files/` and can be promoted the same way if the durability-protocol lineage is
wanted as tracked evidence.
