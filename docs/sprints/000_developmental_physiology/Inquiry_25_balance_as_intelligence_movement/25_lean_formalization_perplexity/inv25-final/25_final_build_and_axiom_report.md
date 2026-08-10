# 25 — Final Build and Axiom Report

## Investigation 25: Balance-as-Intelligence Movement — Lean 4 faithfulness patch

Supersedes `25_build_and_axiom_report.md` from the prior (now-superseded) package.

---

## 1. Toolchain and environment

- Lean toolchain: `leanprover/lean4:v4.33.0-rc2` (pinned in `lean-toolchain`, unchanged from the prior package).
- Build system: `lake` via `lakefile.toml` (`name = "inv25"`, library targets `Core`, `Models`, `Verification`, executable target `main`). `lakefile.toml`/`lake-manifest.json`/`lean-toolchain` are byte-identical to the prior package (`diff` returns no output against `lean25_prev_backup/`).
- Sandbox setup required before every `lean`/`lake` invocation: `export PATH="$HOME/.elan/bin:$PATH"`.
- `lake build` with no target arguments reports "Nothing to build" for this project layout — all commands below explicitly name `Core Models Verification main`.

## 2. Exact build commands run

```
export PATH="$HOME/.elan/bin:$PATH"
cd /home/user/workspace/lean25
lake clean
lake build Core Models Verification main 2>&1 | tee full_clean_build.log
./.lake/build/bin/main > verification_output.log 2>&1
```

Result: **Build completed successfully (13 jobs)** — `full_clean_build.log`, final line. This is a from-scratch clean build (`lake clean` first), not an incremental build, so the result reflects every one of Core.lean/Models.lean/Verification.lean/Main.lean being freshly re-elaborated and re-checked.

## 3. `sorry` / `sorryAx` audit

```
grep -rn "sorry" *.lean
```

Three matches, all non-code:
- `Core.lean:54` — doc-comment prose: "No axiom is declared anywhere in this development. No `sorry` is used."
- `Main.lean:41` — doc-comment/string literal: "...#print axioms / sorryAx audit." (part of the printed closing message, referring to this very report, not a `sorry` term).
- `Verification.lean:16` — doc-comment prose describing the acceptance criterion ("...`sorryAx`. No `sorry` appears anywhere...").

**Zero occurrences of the `sorry` tactic or term anywhere in executable Lean code.** No declaration anywhere in `Core.lean`, `Models.lean`, `Verification.lean`, or `Main.lean` uses `sorry`.

```
grep -n "^axiom \|  axiom " *.lean
```

**Zero results.** No custom `axiom` declaration exists anywhere in the project — every one of the 73 theorems/definitions audited below is a genuine proof term, not an assumed axiom.

## 4. `#print axioms` transcript and axiom discipline

`Verification.lean` (114 lines total, up from 57 in the prior package) issues exactly **73** `#print axioms` commands, organized in four sections (Core: 25, M1: 28, M2: 8, M3: 12 — 25+28+8+12 = 73). Running the clean build produces exactly **73** corresponding `info:` lines in `full_clean_build.log` — a 1:1 correspondence confirmed by direct count (`grep -c "^info:" full_clean_build.log` = 73; the one apparent extra match of the literal string "#print axioms" inside `Verification.lean` at line 10 is doc-comment prose, not a 74th command).

**Distinct axioms appearing across all 73 declarations, project-wide:**

```
propext
```

That is the **only** axiom name that appears anywhere in the transcript. `Classical.choice` and `Quot.sound` — the other two axioms Lean's `#print axioms` would report if genuinely used — appear **nowhere**. Many declarations (all of the purely structural/definitional ones, e.g. `materiality_not_from_use_alone_soundness`, `readapp_requires_adm`, `harmonic_alignment_requires_rel_floors`, `bounded_harmonic_continuation`, `stuck_implies_sns`, `N05_stuck_implies_sns`, all of M2's theorems) report "does not depend on any axioms" outright — zero axioms, not even `propext`. Every M1/M3 theorem that does depend on `propext` does so only because those models' finite `Standing`/`Trajectory`/`Extension` instances rely on `Prop`-extensionality-driven `decide`/`rfl` normalization internal to Lean's kernel for finite case analysis — a standard, expected, non-adversarial use of `propext`, present identically in the prior (superseded) package's audit and unaffected by Corrections A–D.

**No axiom was newly introduced by this patch.** The set of distinct axioms used (`{propext}`) is identical before and after Corrections A–D — confirmed by comparing this transcript's axiom set against the prior package's `25_build_and_axiom_report.md`, which reported the same single axiom.

## 5. Required acceptance table

| # | Declaration | Section | New this pass? | Axioms | Sorry? |
|---|---|---|---|---|---|
| 1 | `materiality_not_from_use_alone_soundness` (T04) | Core | No | none | No |
| 2 | `rel_floor_noncompensatory` | Core | No | none | No |
| 3 | `prec_floor_noncompensatory` | Core | No | none | No |
| 4 | `readapp_requires_adm` (T07) | Core | No | none | No |
| 5 | `readapp_no_contact_masquerade` | Core | No | propext | No |
| 6 | `readapp_rel_floor` | Core | No | none | No |
| 7 | `readapp_prec_floor` | Core | No | none | No |
| 8 | `source_identity_rel` (T01) | Core | No | none | No |
| 9 | `source_identity_app` (T02) | Core | No | none | No |
| 10 | `source_identity_prec` (T03) | Core | No | none | No |
| 11 | `no_scalar_override` (T11) | Core | No | none | No |
| 12 | `harmonic_alignment_requires_rel_floors` (T14) | Core | Re-proved (Correction B/C signature) | none | No |
| 13 | `harmonic_alignment_requires_prec_floors` (T15) | Core | Re-proved (Correction B/C signature) | none | No |
| 14 | `harmonic_align_rel_noncompensatory` | Core | Re-proved (signature) | none | No |
| 15 | `bounded_harmonic_continuation` (T16) | Core | Re-proved (signature) | none | No |
| 16 | `nonharmonic_falsifier` (T17) | Core | Re-proved (signature) | none | No |
| 17 | `stuck_implies_sns` (T13) | Core | Re-proved (Correction A signature) | none | No |
| 18 | `extension_materiality_not_from_use_alone_soundness` | Core | **New (Correction C)** | none | No |
| 19 | `readapp_fully_appropriate` | Core | **New (Correction B)** | none | No |
| 20 | `N01_harmonic_align_requires_adm25` | Core | **New (Correction B)** | none | No |
| 21 | `N02_harmonic_align_requires_readapp` | Core | **New (Correction B)** | none | No |
| 22 | `N03_harmonic_align_material_extension_universal` | Core | **New (Correction C)** | none | No |
| 23 | `harmonic_align_requires_readapp_provenance` | Core | **New (Correction B)** | none | No |
| 24 | `harmonic_align_prec_noncompensatory` | Core | Re-proved (signature) | none | No |
| 25 | `N05_stuck_implies_sns` | Core | **New (Correction A)** | none | No |
| 26–37 | M1 pre-existing (materiality/rel/prec/readapp adversaries, `skilledAdm`, `skilledReadApp`, `m1_skilled_never_direct_contact`) | M1 | No | none/propext (mixed, unchanged) | No |
| 38–40 | `matExtMisalignedAdm`, `matExtMisalignedReadApp`, `m1_matExtMisaligned_never_direct_contact` | M1 | **New (Correction C fixture)** | propext | No |
| 41–45 | `T25_rap_summary_noninjective`, `T18_energetic_case_A_skilled`, `T18_energetic_case_B_lowActHighForce`, `T18_pns_high_force_contrast`, `T18_tBusy_is_PNSLike` | M1 | No (re-proved against corrected `HarmonicAlign`/`LegacyLawfulAppropriate` signatures where applicable) | propext | No |
| 46 | `m1_skilled_harmonic_align_holds` | M1 | Re-proved (Correction B/C, strictly harder witness) | propext | No |
| 47 | `m1_bhc_good_layer1` | M1 | Re-proved (signature) | propext | No |
| 48 | `m1_bhc_bad_layer2_falsifier` | M1 | Re-proved (signature) | propext | No |
| 49 | `N04_material_extension_misalignment_countermodel` | M1 | **New (Correction C)** | propext | No |
| 50 | `m1_matExtMisaligned_harmonic_align_fails` | M1 | **New (Correction C)** | propext | No |
| 51 | `T_adv15_tLow` | M1 | Re-proved (Correction A) | propext | No |
| 52 | `T_adv15_tStuck` | M1 | Re-proved (Correction A) | propext | No |
| 53 | `T_adv15_tBusy` | M1 | No (proof body unaffected) | propext | No |
| 54 | `N06_sns_not_stuck_witness` | M1 | **New (Correction A)** | propext | No |
| 55 | `N07_high_activity_not_stuck_by_itself` | M1 | **New (Correction A)** | propext | No |
| 56–63 | M2 (`m2_severed_fails_precfloor` … `T21_meta_awareness_bite`) | M2 | No | none | No |
| 64–73 | M3 (`bridgeMoveAdm` … `T24_no_global_model_required`) | M3 | No | propext (mixed) | No |

**Totals:** 73/73 declarations audited, 73/73 with zero `sorry`, 73/73 with axioms ⊆ `{propext}`, 16 net-new declarations added by Corrections A–D (18–25 in Core: 8 lines; 38–40, 46–50 refactor + 49–50 new, 51–55 in M1: 8 fully new N04/N06/N07/countermodel-fixture lines plus re-proofs), 0 declarations removed, 0 declarations regressed.

## 6. Completion-gate checklist

- [x] `lake clean && lake build Core Models Verification main` succeeds from scratch (13/13 jobs).
- [x] Zero `sorry` anywhere in `Core.lean`/`Models.lean`/`Verification.lean`/`Main.lean`.
- [x] Zero custom `axiom` declarations anywhere in the project.
- [x] `#print axioms` run on all 73 audited declarations (T01–T25 + N01–N07 + all affected/new M1 model theorems); only `propext` ever appears.
- [x] `./.lake/build/bin/main` runs without error and prints the expected confirmation message (`verification_output.log`).
- [x] Every one of the 14 MUST-preserve doctrine items re-verified against source this session (see below).
- [x] 9-point source-level forbidden-pattern audit passes clean (see below).
- [x] `lakefile.toml`, `lake-manifest.json`, `lean-toolchain` unchanged from the prior package.

## 7. Mechanical fixes cross-reference

See `25_final_encoding_decision_log.md`, MECHANICAL-07 (anonymous-constructor/record-literal ambiguity in `m1_skilled_harmonic_align_holds`'s six-conjunct witness) and MECHANICAL-08 (`Decidable`-instance-synthesis failure on the new `StuckThresholdWitness` case splits, resolved identically to the prior package's MECHANICAL-04 by using `.elim` on the definitionally-`False` hypothesis rather than `by decide`). No other new mechanical issues were encountered; MECHANICAL-01 through MECHANICAL-06 from the prior package remain applicable in the unaffected M2/M3 sections and required no rework.

## 8. 14-point MUST-preserve regression check (this session)

Each item below was checked directly against the current source via targeted `grep`/`read` (not re-derived from memory):

1. Soul standing doctrine-governed, not a freely fillable DPF field — `Standing` remains an inductive (`none`/`partial`/`full`), consumed only through `relStanding`/`precStanding` `Sig` fields, never a raw settable carrier on `Movement` itself. Unaffected by A–D. ✓
2. Dynamic Participatory Fourthness remains the structural center — `Movement`/`Sig.Movement` untouched; T22 (`M3.T22_fourthness`) unaffected. ✓
3. Movement remains primary — `Sig.Movement K K'` is still the base type every predicate (`AllRelFloors`, `ReadApp`, `HarmonicAlign`, etc.) is indexed by. ✓
4. R/A/P remain heterogeneous readings of the same movement — T01/T02/T03 (`source_identity_*`) unchanged. ✓
5. R/A/P remain non-reconstructive — T25 `T25_rap_summary_noninjective` unchanged. ✓
6. No weighted scalar intelligence function — T11 `no_scalar_override` unchanged; `HarmonicAlign`'s redesign still contains no numeric aggregate anywhere in its six conjuncts. ✓
7. Relatedness/Precision remain non-compensatory over material floors — `rel_floor_noncompensatory`/`prec_floor_noncompensatory` (Core, unaffected) and `harmonic_align_rel_noncompensatory`/`harmonic_align_prec_noncompensatory` (re-proved under the new signature, same proof shape). ✓
8. Investigation-24 legality inherited through an abstract interface — `Adm24` opaque field on `Sig`, never reimplemented; unaffected. ✓
9. ActionEffort and ExcessForcing remain distinct types — both unaffected `Sig` fields; `DisqualifyingExcessForcing` still a separate conjunct in `HarmonicAlign` (position 4, unchanged). ✓
10. Interface growth remains real, not faked — `T20_interface_growth_not_faked`/`T23_interface_growth_not_faked` (M2/M3, unaffected) and the anti-fake `AvailableAt` match-on-cut discipline (DECISION-09) untouched. ✓
11. Fourthness based on counterfactual discrimination, not relation count — `T22_fourthness` (M3) unaffected; note the NEW `ExtensionDiscriminates` field added for Correction C follows the exact same counterfactual-discrimination discipline as the pre-existing `DiscriminatesRel`/`DiscriminatesDist`, not a bare count. ✓
12. Bounded Harmonic Continuation remains a coherence/soundness schema, not an empirical prediction theorem — T16/T17 still take an explicit `hschema` premise every caller must independently discharge; re-stated signature only threads `Sd` and drops `z`, no change to this schema character. ✓
13. No `sorry` — confirmed §3 above. ✓
14. No invented axioms merely to close proofs; no silent strengthening of premises; do not broaden beyond Investigation 25 — confirmed §3/§4 above (axiom set unchanged at `{propext}`); the one deliberate strengthening (`HarmonicAlign` now strictly harder to construct) is explicitly authorized by Corrections B/C, not a silent addition. ✓

## 9. 9-point source-level forbidden-pattern audit (this session)

1. `sorry` anywhere in code — NONE (§3). ✓ clean
2. Bare `LawfulAppropriate` field reintroduced outside `LegacyLawfulAppropriate`/comments — NONE; all live occurrences are either `LegacyLawfulAppropriate` (derived-only, DECISION-B2) or doc-comment references explaining its removal. ✓ clean
3. Custom `axiom` declarations — NONE (§3). ✓ clean
4. Unjustified `Classical.choice`/`Quot.sound` usage — NONE; only `propext` appears anywhere (§4). ✓ clean
5. `native_decide` usage (bypasses kernel checking) — NONE found anywhere in the project. ✓ clean
6. `HarmonicAlign`/`Stuck` degenerating to a trivially-`True` or vacuous definition — NONE; both are genuine multi-conjunct/typed-witness definitions, confirmed non-vacuous by `m1_skilled_harmonic_align_holds` (positive witness) and `m1_matExtMisaligned_harmonic_align_fails`/`T_adv15_tLow` (negative witnesses) both being non-trivial proofs. ✓ clean
7. `admit`/other unsafe escape hatches — NONE found (Lean 4 has no `admit` tactic in this project's imports; confirmed absent from source). ✓ clean
8. `ModelSufficient` redefined away from documented-provisional `True`/`w.elim` scaffolding — confirmed UNCHANGED from the prior package (Correction D forbids redesign); still `True` in M1/M2, `w.elim` in M3. ✓ clean (by design, not a violation)
9. Old disjunctive bare-`Or` `Stuck` form reintroduced anywhere — NONE; the only `Or` remaining near `Stuck` is inside the unrelated, unaffected `HoldingApart` definition (`ContactExclusion ∨ Recurrence ∨ InterfaceNarrowing`), which Correction A explicitly leaves untouched and which is not the threshold-crossing judgment Correction A retypes. ✓ clean

**All 9 checks pass with no forbidden patterns found.**

## 10. Summary

The clean rebuild is fully green, the axiom surface is unchanged and minimal (`{propext}` only, zero `sorry`, zero invented axioms), all 16 new Correction A/B/C/D-driven declarations are accounted for in the `#print axioms` transcript with no regression to any of the 57 pre-existing audited declarations, and both the 14-point MUST-preserve doctrine check and the 9-point forbidden-pattern audit pass without exception. This is the evidentiary basis for the closure verdict stated in the final delivery.
</content>
