# Corner-Gate v2 Code Drafts (for Clarity's analysis)

Status: DRAFTS for code analysis. Nothing here is wired. Files map to the
build steps in corner_gate_v2_design.md Section 7 (as amended v1.1, v1.2).

| File | Destination at build time | Build step |
|---|---|---|
| q_geq_addition.metta | appended to lib_clarity_reasoning/lib_quantale.metta | B1 |
| cycle_trace.metta | soul/cycle_trace.metta (new, pure) | B2 |
| cycle_trace_writers.metta | soul/cycle_trace_writers.metta (new, writers) | B2 |
| corner_state.metta | soul/corner_gap/corner_state.metta (new, pure) | B2 basic, B3 full |
| corner_window_writers.metta | soul/corner_gap/corner_window_writers.metta (new, writers) | B4 |
| corner_gate_v2_patch.metta | edits into soul/corner_gap/corner_gate.metta | B4 |
| helper_py_addition.py | appended to src/helper.py | B2 |
| loop_hook_changes.md | the four loop.metta hook changes, exact lines | B2/B4 |

Constraints honored throughout: C12 (no match inside if; every match lives in
its own reader), ASCII only, no RMW, ADR-005 superpose clears, ADR-007
substrate-externalized control flow, ADR-008 hands-format-numbers-only,
single-head recursive dispatch via if on () (P3 fork precedent).

CONFIRM items for Clarity (REPL-checkable before B1):
1. let-bound repr then match on the bound variable (cmd-in-corner-window?).
2. cons-atom availability in this runtime (filter-corner-cmds); fallback shape
   noted in the file if absent.
3. Recursive max-repeat-acc cost at window scale (max ~10 cycles of commands).
4. Partial-drop semantics: when the filter drops some commands and passes
   others, real results flow and the drop surfaces only in next cycle's
   CORNER-STATE block. Full-drop cycles get the v2 feedback as results.
   Acceptable, or should a partial-drop notice ride the results channel too?
