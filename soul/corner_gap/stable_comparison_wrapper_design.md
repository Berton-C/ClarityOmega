## Stable-Comparison Wrapper Design

Problem: classify-state-delta uses results-novel as a forward-gate condition. Timestamp-only diffs cause spurious results-novel=True, producing false-positive forward verdicts.

Solution: Strip time-varying fields before comparison.

Steps:
1. canonicalize-result: remove TIME and rolling fields, normalize whitespace
2. results-novel compares canonical forms, not raw
3. Regression test: same content, different timestamps = results-novel=False

Invariants:
- Gate fires for genuinely novel results
- Gate does not fire on timestamp-only diffs
- No change to gate structure

Risks:
- False-negative if canonicalization strips too much (mitigate: conservative, only known-rolling fields)
- Maintenance burden if strip list grows (mitigate: config constant)

Status: Design complete. Awaiting implementation.