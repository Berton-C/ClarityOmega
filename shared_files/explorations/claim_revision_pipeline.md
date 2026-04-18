# Claim-Revision Pipeline Design
Date: 2026-04-15 16:59

## Purpose
Systematic epistemic hygiene tool for the substrate.
Uses NAL revision to detect and correct confabulated claims.

## Pipeline Stages
1. CLAIM INTAKE: Accept claim as NAL statement with initial stv
2. COUNTER-EVIDENCE: Source or generate counter-evidence with stv
3. REVISION ROUND: Apply NAL revision to merge evidence
4. CONVERGENCE CHECK: Compare delta between rounds
5. THRESHOLD: If delta below 0.05 for 2 consecutive rounds, declare converged
6. OUTPUT: Final stv represents evidence-weighted belief

## Convergence Evidence
Tested series: 0.95 -> 0.602 -> 0.483 -> 0.423
Deltas: 0.348, 0.119, 0.060
Pattern: diminishing corrections, 3-5 rounds sufficient

## Application Domains
- Self-generated claims about substrate capabilities
- Inherited assumptions from training
- User-provided claims requiring verification
- Cross-session belief consistency checking

## Open Questions
- How to auto-generate counter-evidence?
- What confidence threshold triggers action vs continued inquiry?
- Can pipeline run asynchronously during idle cycles?