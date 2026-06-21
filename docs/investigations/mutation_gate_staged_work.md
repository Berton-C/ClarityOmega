# Staged work: Mutation Gate (parallel vote gate for soul_verdict_out)

**Status:** Staged, near-ready. Package complete. Awaiting live-cycle validation window. NOT Sprint 0-Coda scope.
**Date recorded:** 2026-05-26
**Confidence at staging:** 0.986 (synthetic boundary validation complete)
**Surfaced during:** Sprint 0-Coda Phase B (Clarity raised prior work; recorded so it does not decay)

---

## What it is

A parallel vote gate that replaces the original hardcoded `PROCEED` in `soul_verdict_out`. Instead of a hardcoded verdict, the gate takes parallel votes and resolves PROCEED vs PAUSE by threshold.

This is soul-intercept-chain / governance-flow work. It is distinct from the capability-registry (Sprint 0-Coda) work; Sprint 0-Coda does not touch it and it does not touch Sprint 0-Coda.

## Validation status

Validated across all five boundary scenarios (synthetic):

| Vote tally | Verdict |
|-----------|---------|
| 4-0 | PROCEED |
| 3-1 | PROCEED (at boundary) |
| 2-2 | PAUSE |
| 1-3 | PAUSE |
| 0-4 | PAUSE |

Confidence 0.986, assessed ready to ship pending one thing: a live validation window.

## The package

- `parallel_vote_gate.metta`
- `vote_threshold.metta`
- `vote_gate_bridge.py`
- `gate_integration_wiring.metta`
- `test_boundary.py`
- `gate_rules.json` — makes the gate extensible via config rather than hardcoded logic (the thresholds and rules live in config, not in code)

## What remains before ship

Validation window: run against 5-10 live cycles to confirm the Python fallback matches the NAL boundary table under real conditions, not just synthetic tests. The synthetic boundary tests all pass; the open question is whether the live behavior matches the table when real verdicts flow through.

## Why it is recorded here rather than acted on

This is staged capability work that became relevant context during Sprint 0-Coda Phase B but is not Sprint 0-Coda scope. Recording it so it does not decay between now and its validation window. It replaces hardcoded behavior in `soul_verdict_out`, which is an architectural change to the governance-flow side of the soul intercept chain — when it ships, it likely warrants an ADR (the hardcoded-PROCEED → vote-gate change is a governance-architecture decision).

## Relationship to the broader architecture

The vote gate is governance-flow infrastructure. In the pipes/flows/meta-awareness lens (Sprint 0-Coda Phase A Section 0), governance flow is the privileged subset of flow because governance failure is a Safety-tier deficit. The hardcoded `PROCEED` is a governance flow that does not actually evaluate; the vote gate makes the governance evaluation real. This is consistent with the direction the architecture is moving (governance made structural and inspectable rather than hardcoded), but it is its own work-package with its own validation discipline, separate from the capability-registry track.

## Next step when picked up

Schedule the 5-10 live-cycle validation window. One observed divergence between the Python fallback and the NAL boundary table under live conditions means the gate is not yet ready; clean cycles across the window confirm ship-readiness. After validation, write the ADR for the hardcoded-PROCEED → vote-gate governance change.
