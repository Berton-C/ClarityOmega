# Investigation 25 — Lean 4 Formalization Deliverable

## Layout

```
lean-project/
  lean-toolchain              # pins leanprover/lean4:v4.33.0-rc2
  lakefile.toml                # Lake config (TOML form; see DECISION-06 for the
                                # documented deviation from the lakefile.lean name
                                # requested in the handoff prompt — functionally
                                # equivalent for this project's target list)
  Core.lean                    # Sig + generic T01-T17 obligations
  Models.lean                  # M1 (T18/T25), M2 (T19-T21), M3 (T22-T24)
  Verification.lean            # #print axioms over all 57 declarations
  Main.lean                    # thin entrypoint / sanity-check executable
  lake-manifest.json           # no external dependencies
  full_clean_build.log         # full clean-rebuild transcript (13/13 jobs)
  verification_output.log      # full #print axioms transcript (57 entries)

25_formalization_diff_and_mapping.md   # section-by-section 25f -> Lean mapping
25_encoding_decision_log.md            # DECISION-01..11 + mechanical fixes
25_formalization_gap_report.md         # GAP-01..14 with mandatory dispositions
25_build_and_axiom_report.md           # toolchain, build, axioms, T01-T25 acceptance table, gate checklist
```

## Build

```bash
cd lean-project
lake build Core Models Verification main
./.lake/build/bin/main
```

## Final verdict

See the final section of `25_build_and_axiom_report.md` and the covering message
for this deliverable's verdict: **FORMALLY-HARDENED-WITH-PROVISIONAL-ENCODINGS**.
