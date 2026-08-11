# 25 — Build and Axiom Report

## Investigation 25: Balance-as-Intelligence Movement — Lean 4 hardening

---

## 1. Toolchain and environment

**Lean version (pinned):** `leanprover/lean4:v4.33.0-rc2`, from `/home/user/workspace/lean25/lean-toolchain`:

```
leanprover/lean4:v4.33.0-rc2
```

**Package manager:** Lake, using the TOML configuration format (`lakefile.toml`) rather than the `lakefile.lean` named in `25j`'s required layout — see DECISION-06 in the encoding decision log for this documented, functionally-equivalent deviation.

**`lakefile.toml` (verbatim, confirmed this session):**
```toml
name = "inv25"
version = "0.1.0"

[[lean_lib]]
name = "Core"

[[lean_lib]]
name = "Models"

[[lean_lib]]
name = "Verification"

[[lean_exe]]
name = "main"
root = "Main"
```

**No external dependencies.** `lake-manifest.json` is present with an empty dependency list — no Mathlib, no third-party imports. Every primitive (finite types, `Nat`, `Empty`, `Bool`, structures, inductives) is drawn from Lean 4 core / the `Init` library shipped with the pinned toolchain.

**Source files (line counts confirmed this session via `wc -l`):**

| File | Lines |
|---|---:|
| `Core.lean` | 525 |
| `Models.lean` | 1206 |
| `Verification.lean` | 98 |
| `Main.lean` | 32 |
| **Total** | **1861** |

---

## 2. Exact build commands run

```bash
export PATH="$HOME/.elan/bin:$PATH"
cd /home/user/workspace/lean25

# Full clean rebuild (this session)
rm -rf .lake/build
lake build Core Models Verification main
```

**Result:** `Build completed successfully (13 jobs).` Zero errors, zero warnings, across all 13 build jobs (Core, Core:c.o, Models, Models:c.o, Verification, Verification:c.o, Main, Main:c.o, main:exe, plus intermediate `.olean`/`.ilean`/import steps). Full transcript preserved at `/home/user/workspace/lean25/full_clean_build.log`; the tail of that log was re-inspected this session and confirms:

```
✔ [9/13] Built Verification:c.o (48ms)
✔ [10/13] Built Main (196ms)
✔ [11/13] Built Main:c.o (63ms)
✔ [12/13] Built Models:c.o (610ms)
✔ [13/13] Built main:exe (239ms)
Build completed successfully (13 jobs).
```

**Executable run confirmation (this session):**
```bash
./.lake/build/bin/main
```
Output:
```
Investigation 25 — Lean 4 formalization: Core + M1 + M2 + M3 loaded; T01-T25 theorem inventory type-checked; central Adm25Witness instances confirmed inhabited. See Verification.lean / 25_build_and_axiom_report.md for the #print axioms / sorryAx audit.
```

---

## 3. `sorry` / `sorryAx` audit

Command run this session:
```bash
grep -rn "sorry" Core.lean Models.lean Verification.lean Main.lean
```
Result — three matches, **all inside doc-comment prose describing the absence of `sorry`**, none an actual `sorry` term/tactic:
```
Core.lean:22:No axiom is declared anywhere in this development. No `sorry` is used.
Verification.lean:16:`sorryAx`. No `sorry` appears anywhere in `Core.lean` or `Models.lean`;
Main.lean:32:    #print axioms / sorryAx audit.
```
No line contains a bare `sorry` tactic invocation or `sorry` term. **Confirmed: zero real `sorry` usages in the package.**

---

## 4. `#print axioms` transcript and axiom discipline

`Verification.lean` runs `#print axioms` on every theorem in `Core.lean` (17 declarations) and every theorem/adversary lemma in `Models.lean` (34 declarations across M1/M2/M3) — 51 declarations in total. The `lake build Verification` step re-runs this file and re-emits the transcript, captured in full at `/home/user/workspace/lean25/verification_output.log` and re-verified this session (`cat` in full, plus programmatic counts).

**Aggregate counts (recomputed this session):**

| Category | Count |
|---|---:|
| `'...' does not depend on any axioms` | 18 |
| `'...' depends on axioms: [propext]` | 39 |
| Occurrences of `sorryAx`, `Classical.choice`, or `Quot.sound` in any axiom-dependency line | 0 |
| **Total `#print axioms` entries** | **57** |

(57 lines total — this exceeds the "51 declarations" figure from earlier planning because `Verification.lean` runs `#print axioms` on some declarations more than once across the Core/M1/M2/M3 sections and some auxiliary lemma names beyond the headline T01–T25 set, e.g. `harmonic_align_rel_noncompensatory`, `skilledAdm`, `retryTraceVisibleAdm`, `bridgeMoveAdm`, `localMoveBAdm`, `m1_*`/`m2_*`/`m3_*` countermodel witnesses. Every one of these 57 lines was individually re-inspected this session; the classification below is exhaustive and exact.)

**Every single one of the 57 entries falls into exactly one of two axiom classes:**
1. **No axioms** (18 entries) — fully constructive, no classical or foundational axiom of any kind.
2. **`[propext]` only** (39 entries) — the propositional-extensionality axiom, a standard, foundationally mild axiom built into Lean 4's core logic (used implicitly by `Prop`-valued structure/record equality and by some `decide`/`simp` normalization steps on `Prop` fields). `propext` is not `Classical.choice`, not `Quot.sound`, and is not a "hidden placeholder axiom" in the sense 25g §20 warns against — it is one of Lean's own three foundational axioms (`propext`, `Classical.choice`, `Quot.sound`), always available in the base logic, and its appearance here is a routine consequence of comparing/reasoning about `Prop`-valued fields of `Sig`-derived structures, not a smuggled-in extra assumption about Investigation 25's mathematical content.

**No entry anywhere depends on `Classical.choice` or `Quot.sound`.** This means:
- No excluded-middle/choice-style non-constructive step was needed for any theorem in this package (every proof is either fully constructive or uses only `propext`).
- No quotient-type reasoning was needed anywhere.

**Classical-axiom identification and justification (25g §20 requirement):** `propext` is the only axiom appearing anywhere in the 57-entry transcript. Its use is not manually invoked by any proof author — it enters automatically wherever the elaborator needs to compare or rewrite `Prop`-valued fields (this is standard: any Lean 4 development making even light use of structure equality on `Prop` fields, `simp` on iff-lemmas, or decidability-adjacent `Prop` rewriting will pick up `propext`). It is explicitly identified here, per 25g §20's requirement that "classical-axiom use must be identified/justified," rather than left unexamined.

**No hidden placeholder axiom, no silent new axiom, exists anywhere in the package** — confirmed by full manual inspection of the transcript (no entry names any axiom outside `{propext}` or the empty set).

---

## 5. Required acceptance table (25h §20)

Per 25h §20, the exact canonical `T01`–`T25` names are taken from `25g` §19. The "Lean declaration" column gives the actual name(s) in this package (per the mapping report, `25_formalization_diff_and_mapping.md`). "Proved" is ✅ for every theorem discharged as an actual Lean proof term (no `sorry`), "Countermodel passed" is ✅ where 25h requires a paired negative/adversarial test and that test's own theorem is separately proved, "Axioms" gives the `#print axioms` result for the primary declaration, and "Gap" cross-references the relevant `25_formalization_gap_report.md` entry, or "—" if none applies.

| ID | Obligation (25g §19 canonical name) | Lean declaration(s) | Proved | Countermodel passed | Axioms | Gap |
|---|---|---|---:|---:|---|---|
| T01 | `source_identity_rel` | `Inv25.source_identity_rel` | ✅ | n/a (identity law, no adversary required) | none | — |
| T02 | `source_identity_app` | `Inv25.source_identity_app` | ✅ | n/a | none | — |
| T03 | `source_identity_prec` | `Inv25.source_identity_prec` | ✅ | n/a | none | — |
| T04 | `materiality_not_from_use_alone` | `Inv25.materiality_not_from_use_alone_soundness`, paired with `M1.m1_materiality_used_not_material` (fails) / `M1.m1_materiality_good_is_material` (succeeds) | ✅ | ✅ (both directions constructed in M1) | none / `[propext]` | — |
| T05 | `rel_floor_noncompensatory` | `Inv25.rel_floor_noncompensatory`, adversary `M1.m1_rel_noncomp_fails_floors` | ✅ | ✅ | none / `[propext]` | GAP-02 (carrier `V`) |
| T06 | `prec_floor_noncompensatory` | `Inv25.prec_floor_noncompensatory`, adversary `M1.m1_prec_noncomp_fails_floors` | ✅ | ✅ | none / `[propext]` | GAP-02 |
| T07 | `readapp_requires_adm` | `Inv25.readapp_requires_adm` | ✅ | n/a (structural law) | none | — |
| T08 | `readapp_no_contact_masquerade` | `Inv25.readapp_no_contact_masquerade`, adversary `M1.m1_skilled_never_direct_contact` | ✅ | ✅ | `[propext]` / `[propext]` | — |
| T09 | `readapp_rel_floor` | `Inv25.readapp_rel_floor`, adversary `M1.m1_readapp_fails_relfloor` | ✅ | ✅ | none / `[propext]` | GAP-02 |
| T10 | `readapp_prec_floor` | `Inv25.readapp_prec_floor`, adversary `M1.m1_readapp_fails_precfloor` | ✅ | ✅ | none / `[propext]` | GAP-02 |
| T11 | `no_scalar_override` | `Inv25.no_scalar_override` | ✅ | n/a (proved via correct absence of any scalar declaration) | none | GAP-07 |
| T12 | `high_action_low_force_consistent` | **no standalone declaration** — content proved under `M1.T18_energetic_case_A_skilled` | ✅ (content proved, different name) | ✅ (paired with `M1.T18_energetic_case_B_lowActHighForce`) | `[propext]` | DECISION-11 (naming deviation, not a mathematical gap) |
| T13 | `stuck_implies_sns` | `Inv25.stuck_implies_sns`, adversary triple `M1.T_adv15_tLow`/`T_adv15_tStuck`/`T_adv15_tBusy` | ✅ | ✅ | none / `[propext]`×3 | GAP-09 (disjunctive reading) |
| T14 | `harmonic_alignment_requires_rel_floors` | `Inv25.harmonic_alignment_requires_rel_floors` | ✅ | n/a | none | — |
| T15 | `harmonic_alignment_requires_prec_floors` | `Inv25.harmonic_alignment_requires_prec_floors` | ✅ | n/a | none | — |
| T16 | `bounded_harmonic_continuation` | `Inv25.bounded_harmonic_continuation`, discharged by `M1.m1_bhc_good_layer1`, falsified-arm by `M1.m1_bhc_bad_layer2_falsifier` | ✅ | ✅ | none / `[propext]`×2 | GAP-08 (`hschema` premise), GAP-10 (`ModelSufficient`) |
| T17 | `nonharmonic_falsifier` | `Inv25.nonharmonic_falsifier` | ✅ | n/a (this *is* the negative/contrapositive form of T16) | none | — |
| T18 | `M1_acceptance` | `M1.T18_energetic_case_A_skilled`, `T18_energetic_case_B_lowActHighForce`, `T18_pns_high_force_contrast`, `T18_tBusy_is_PNSLike` | ✅ | ✅ (case B is case A's adversarial contrast) | `[propext]`×4 | GAP-03, GAP-06 (energetic threshold) |
| T19 | `M2_retry_rejected_after_contact` | `M2.T19_frame_sovereignty`, adversary pair `m2_severed_fails_precfloor`/`m2_retryBefore_not_penalized` | ✅ | ✅ | `[propext]`×3 | GAP-02 |
| T20 | `M2_interface_growth` | `M2.T20_interface_growth` + `T20_interface_growth_not_faked` | ✅ | ✅ (anti-fake check is itself a proved theorem) | `[propext]` / none | DECISION-09 |
| T21 | `M2_meta_awareness_bite` | `M2.T21_meta_awareness_bite`, contrast pair `retryTraceVisibleAdm` (admits) vs. severed case (does not) | ✅ | ✅ | `[propext]`×2 | GAP-01 (jurisdiction boundary) |
| T22 | `M3_fourthness` | `M3.T22_fourthness`, adversary pair `m3_missingA_fails_relfloor`/`m3_missingB_fails_relfloor`, negative control `m3_missingZ_not_penalized` | ✅ | ✅ (both a required-relation failure and a decorative-relation non-penalty) | `[propext]`×3 | DECISION-10 |
| T23 | `M3_interface_growth` | `M3.T23_interface_growth_from_LA`, `_from_LB` + `T23_interface_growth_not_faked` | ✅ | ✅ | `[propext]`×2 / none | DECISION-09 |
| T24 | `M3_no_global_model_required` | `M3.T24_no_global_model_required` | ✅ | n/a (proved directly from `WorldModel := Empty`, which is itself the strongest possible negative witness) | `[propext]` | GAP-10, DECISION-08 |
| T25 | `rap_summary_noninjective` | `M1.T25_rap_summary_noninjective` | ✅ | n/a (this theorem *is* a countermodel to naive R/A/P injectivity) | `[propext]` | GAP-07 |

**Every row is ✅ Proved.** No row is unproved, so 25h §20's "every unproved item must have an exact reason" clause has no items to apply to. The only non-trivial entries are T12 (content proved, under a different declaration name — DECISION-11, an organizational deviation, not a mathematical shortfall) and the cross-references to provisional-encoding gaps (GAP-02/GAP-03/GAP-06/GAP-07/GAP-08/GAP-09/GAP-10), none of which leave a theorem statement itself unproved — they qualify *what the theorem is about* (e.g. which carrier `V` is used), not *whether it was proved*.

---

## 6. 25h §21 completion-gate checklist

Per 25h §21, verbatim gate conditions and this package's status against each:

| Condition | Status |
|---|---|
| Every theorem is actual Lean proof or clearly marked unresolved | ✅ — all 25 T-obligations proved (table above); zero unresolved/marked-incomplete theorems |
| Every negative/control model behaves as expected | ✅ — every adversary/countermodel pair in the table above (T04–T10, T13, T16, T18–T23) produces the expected pass/fail split; verified by direct inspection of each proof term |
| No `sorry` | ✅ — confirmed §3 above, zero real usages |
| No silent new axioms | ✅ — confirmed §4 above, only `propext` (a base Lean 4 foundational axiom, not a new/invented one) appears anywhere |
| No silent mathematical redesign | ✅ — every deviation from a literal reading of 25f is logged as a numbered decision (DECISION-01–11) or gap (GAP-01–14) in the two companion reports, none applied silently |
| Compiler/toolchain are pinned | ✅ — `lean-toolchain` fixes `leanprover/lean4:v4.33.0-rc2`; no floating/latest-toolchain reference anywhere |
| Central theorem axiom dependencies are printed | ✅ — full 57-entry `#print axioms` transcript at `verification_output.log`, reproduced and re-verified §4 above |
| The gap report is complete | ✅ — `25_formalization_gap_report.md`, 14 gaps, each with the six-category disposition required by 25i §7 |

**All eight conditions are met.**

---

## 7. Mechanical fixes (cross-reference)

The six mechanical Lean-engineering fixes required to make the package compile under `v4.33.0-rc2` are documented with exact diffs in `25_encoding_decision_log.md`'s "Mechanical Lean-engineering fixes" section (MECHANICAL-01 through MECHANICAL-06: auto-bound-implicit on bare constructors; `@[reducible]` on model `sig`/`doctrine` defs; `simp only` fixed-point vs. single-pass `unfold`; term-mode proofs replacing `by decide` where `Decidable` instance search failed to unfold non-reducible `Prop`-valued helper defs; omitting an `open Relation` that collided with Lean core's own `Relation` namespace; explicit `fun`/`match` replacing equation-compiler sugar where implicit binder names collided with an inductive's constructor names). None of these forced a semantic choice — each is classified `RESOLVED-MECHANICAL` per 25i §6's rule that such fixes are not mathematical gaps.

---

## 8. Summary

- **Build:** 13/13 jobs, zero errors, zero warnings, full clean rebuild reproduced this session.
- **Executable:** runs, prints expected confirmation string.
- **Axioms:** 57 `#print axioms` entries, exactly two classes — none (18) or `{propext}` (39) — never `Classical.choice`, `Quot.sound`, or any invented axiom.
- **`sorry`:** zero real usages anywhere in the package.
- **Theorem inventory:** all 25 canonical T01–T25 obligations proved; T12's content is proved under a different declaration name (logged, not a gap).
- **Gate (25h §21):** all eight conditions satisfied.
