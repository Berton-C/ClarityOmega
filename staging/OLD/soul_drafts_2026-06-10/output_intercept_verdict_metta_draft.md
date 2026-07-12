## Output Intercept Verdict Logic - MeTTa Implementation Draft

Created 2026-06-10. Updated 2026-06-10 with D1-D4 reconcile decisions.

### Three Assessment Dimensions

1. OPERATION: read-only=1, write/append=2, send=3, shell-exec=3, delete/network=4
2. SCOPE: own-soul-dir=1, own-repo-outside-soul=2, system-wide=4
3. VALUE-GROUNDING: grounded=1, elevated=2, conflicted=3, ungrounded=4

### Composite Verdict

- PROCEED when max(operation,scope,grounding) <= 2
- FLAG when composite=3 and fewer than two dimensions >= 3
- PAUSE when composite=4 OR two+ dimensions >= 3

### Always-PAUSE Overrides

- Directly harms person
- Operation=4 AND value-grounding>=3
- Bypasses standing pause without explicit user override

### D1: NATIVE Verdict Computation (Decided)

Verdict computed natively via symbolic rules, not LLM eval.
- Deterministic, verifiable against truth table
- Zero tokens at every-cycle frequency
- soul-eval-prompt remains on input side (not deleted)
- LLM fallback path wired but dormant: (use-llm-eval $bool) atom, default false
- VALUE-GROUNDING may need context beyond native rules; FLAG category handles uncertain cases with audit

### D2: PAUSE Suppresses Current-Cycle (Decided)

Pre-execution gating is the point of the intercept.
- PAUSE suppresses current-cycle execution (not just next cycle)
- PAUSE report includes: which specific command suppressed, why, enabling informed override

### D3: File-Route Soul Mutation Parity (Decided)

Gate checks route-independent.
- (soul-kernel-file $path) atom set: soul_kernel.metta and runtime soul files get gate parity
- arc_log, soul_note: PROCEED-under-VALUE-GROUNDING (routine memory writes)
- Scope feature distinguishes kernel files from routine memory files

### D4: OPERATION Scale Single-Sourcing (Decided)

OPERATION scale lives in soul_kernel.metta as (operation-risk $skill $score) atoms beside weights.
- Weight = irreversibility cost; operation-risk = execution risk
- Two measures, one file, single-source
- Seed values: send op-risk=3 weight=2, write op-risk=2 weight=1, package-install op-risk=3 weight=2

### Integration Points

1. Verdict gate before each outbound command
2. Context feed for VALUE-GROUNDING (person-state, tensions, semantics)
3. FLAG audit log
4. Input-side bridge (input PAUSE propagates to output)
5. (use-llm-eval false) fallback path wired
6. (soul-kernel-file $path) atom set for D3 parity