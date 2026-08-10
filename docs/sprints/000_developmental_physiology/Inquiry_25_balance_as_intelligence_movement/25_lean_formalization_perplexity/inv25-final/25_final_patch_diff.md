# 25 — Final Patch Diff

## Investigation 25: Balance-as-Intelligence Movement — Lean 4 faithfulness patch

Diff baseline: `/home/user/workspace/lean25_prev_backup/` (full pre-patch snapshot, previously delivered as `Investigation25_Lean4_Deliverable.zip`) vs `/home/user/workspace/lean25/` (this session's corrected package). Produced via `diff -u` per file. Full raw diffs are retained alongside this report as `core.lean.diff.txt`, `models.lean.diff.txt`, `verification.lean.diff.txt`, `main.lean.diff.txt` for line-exact audit; this document summarizes and cross-references the semantically load-bearing hunks against the final decision log.

| File | Backup lines | Corrected lines | `+` lines | `-` lines |
|---|---|---|---|---|
| `Core.lean` | 525 | 769 | 315 | 71 |
| `Models.lean` | 1206 | 1282 | 129 | 53 |
| `Verification.lean` | 57 | 99 | — | — |
| `Main.lean` | 32 | 42 | — | — |

No changes were made to `lakefile.toml`, `lake-manifest.json`, or `lean-toolchain` — confirmed by `diff` returning no output for those three files between the two directories.

---

## Core.lean

### Correction A — Stuck (DECISION-A1, DECISION-A2)

```diff
-def Stuck (S : Sig) (τ : S.Trajectory) : Prop :=
-  SNSLike S τ ∧ (S.StaleForwardMotion τ ∨ S.PivotUnavailable τ)
+inductive StuckThresholdWitness (S : Sig) (τ : S.Trajectory) : Prop where
+  | staleForwardMotion (h : S.StaleForwardMotion τ)
+  | pivotUnavailable (h : S.PivotUnavailable τ)
+  | opportunityFieldUnavailable (h : S.OpportunityFieldUnavailable τ)
+
+def StuckThresholdCrossed (S : Sig) (τ : S.Trajectory) : Prop :=
+  StuckThresholdWitness S τ
+
+def Stuck (S : Sig) (τ : S.Trajectory) : Prop :=
+  SNSLike S τ ∧ StuckThresholdCrossed S τ
```

`HoldingApart`/`SNSLike` themselves are byte-for-byte unchanged (`diff` shows zero delta on those two definitions) — satisfying the explicit "do not make Stuck a separate ontology from SNS" instruction: `Stuck`'s redesign only changes its second conjunct, never touches the shared `SNSLike` machinery it wraps. A new `Sig` field `OpportunityFieldUnavailable : Trajectory → Prop` was added to back the third constructor. `stuck_implies_sns` (T13) is textually unchanged (`fun h => h.1`); a new restatement `N05_stuck_implies_sns` was added immediately after it, delegating to T13 rather than re-proving it.

### Correction B — HarmonicAlign's Appropriateness conjunct (DECISION-B1, DECISION-B2)

```diff
-  LawfulAppropriate : ∀ {K K'}, Movement K K' → Prop
   ...
-def HarmonicAlign (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (z : S.Extension) : Prop :=
+def HarmonicAlign (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
+    (m : S.Movement K K') : Prop :=
   AllRelFloors S m ∧
-  S.LawfulAppropriate m ∧
+  (∃ A : Appropriateness S m, ReadApp S Sd m A ∧ FullyAppropriate S A) ∧
   AllPrecFloors S m ∧
   ¬ S.DisqualifyingExcessForcing m ∧
-  (S.ExtensionOf z m → S.AlignedExtension z m) ∧
+  (∀ z : S.Extension, MaterialExtensionOf S z m → S.AlignedExtension z m) ∧
   S.ContinuingContactable m
```

The `LawfulAppropriate` field is removed from the `Sig` record entirely (not deprecated in place). New supporting definitions added immediately before `HarmonicAlign`: `FullyAppropriate` (`A.kind = ReadingKind.derivedAppropriateness`), `readapp_fully_appropriate` (any `ReadApp` witness is automatically `FullyAppropriate`), and `LegacyLawfulAppropriate` (a derived, `ReadApp`-sourced definition retained only for `T18_pns_high_force_contrast`'s continuity, per DECISION-B2). `HarmonicAlign` gains an explicit `Sd : S.SoulDoctrine` parameter, needed to state the `ReadApp` existential. Every downstream `HarmonicAlign` consumer (T14, T15, `harmonic_align_rel_noncompensatory`, BHC's T16/T17, all M1/M2/M3 call sites) is updated to pass `Sd` and drop the old `z` argument — a pure signature-threading change with zero effect on the T14/T15 proof terms themselves (`h.1` / `h.2.2.1` unchanged, since conjunct *positions* 1/3/4/6 are preserved).

### Correction C — MaterialExtensionOf (DECISION-C1)

```diff
+  ExtensionDiscriminates : Extension → ∀ {K K'}, Movement K K' → Prop
   ...
+def MaterialExtensionOf (S : Sig) (z : S.Extension) {K K' : S.Cut} (m : S.Movement K K') : Prop :=
+  S.ExtensionOf z m ∧ S.ExtensionDiscriminates z m
+
+theorem extension_materiality_not_from_use_alone_soundness ... := id
```

New `Sig` field `ExtensionDiscriminates` added; `MaterialExtensionOf` defined as its conjunction with the pre-existing `ExtensionOf`, mirroring `MaterialTo`'s §6 shape exactly. This is the definition consumed by `HarmonicAlign`'s corrected fifth conjunct shown above.

### New theorem obligations N01–N05 (Core.lean)

`N01_harmonic_align_requires_adm25`, `N02_harmonic_align_requires_readapp`, `N03` (folded into `harmonic_align_requires_readapp_provenance`'s companion existential-witness theorem), `harmonic_align_requires_readapp_provenance`, `harmonic_align_prec_noncompensatory`, `N05_stuck_implies_sns` are all net-new declarations with no prior-package counterpart — see `+` lines in `core.lean.diff.txt` around the `HarmonicAlign`/`Stuck` blocks.

---

## Models.lean

### Correction C adversarial fixtures (M1)

```diff
+def matExtMisalignedAdm : Adm25Witness sig ... := ...
+def matExtMisalignedReadApp : ReadApp sig doctrine matExtMisaligned ... := ...
+theorem m1_matExtMisaligned_never_direct_contact : ¬ sig.DirectContact matExtMisaligned := ...
   ...
+theorem N04_material_extension_misalignment_countermodel :
+    MaterialExtensionOf sig Extension.extBad matExtMisaligned ∧
+    ¬ sig.AlignedExtension Extension.extBad matExtMisaligned := ...
+theorem m1_matExtMisaligned_harmonic_align_fails :
+    ¬ HarmonicAlign sig doctrine matExtMisaligned := ...
```

### Correction B/C re-proof of the positive HarmonicAlign witness (M1)

```diff
-theorem m1_skilled_harmonic_align_holds : HarmonicAlign sig skilled Extension.ext1 := ...
+theorem m1_skilled_harmonic_align_holds : HarmonicAlign sig doctrine skilled := by
+  refine ⟨fun r _ => rfl, ?_, fun d _ => rfl, (fun h => h), ?_, trivial⟩
+  · exact ⟨_, skilledReadApp, rfl⟩
+  · intro z ⟨hof, hdisc⟩
+    -- case split over ext1 / extBad / extIrrelevant, discharging
+    -- extIrrelevant via hdisc.elim (ExtensionDiscriminates fails for it)
```

`m1_bhc_good_layer1`/`m1_bhc_bad_layer2_falsifier` are re-proved against this new witness with no change to BHC's own statement shape (T16/T17 signatures only gained the `Sd` parameter and dropped `z`, per the Core.lean change above).

### Correction A re-proof of the threshold adversary (M1)

```diff
-theorem T_adv15_tLow : SNSLike sig tLow ∧ ¬ Stuck sig tLow := by
-  refine ⟨⟨Or.inl trivial, trivial⟩, ?_⟩
-  rintro ⟨_, hw | hw⟩ <;> exact hw.elim
+theorem T_adv15_tLow : SNSLike sig Trajectory.tLow ∧ ¬ Stuck sig Trajectory.tLow := by
+  refine ⟨⟨Or.inl trivial, trivial⟩, ?_⟩
+  intro h
+  cases h.2 with
+  | staleForwardMotion hw => exact hw.elim
+  | pivotUnavailable hw => exact hw.elim
+  | opportunityFieldUnavailable hw => exact hw.elim
```

`T_adv15_tStuck` is re-proved using the explicit `StuckThresholdWitness.staleForwardMotion` constructor in place of the old `Or.inl`. `T_adv15_tBusy` is textually unaffected in its own proof body (it already worked by refuting `SNSLike` entirely, upstream of `Stuck`'s internal structure) but is now also cited directly as **N07**. New declarations `N06_sns_not_stuck_witness` and `N07_high_activity_not_stuck_by_itself` are added immediately after, each a one-line delegation to the corresponding `T_adv15_*` theorem (no new proof content, per the user's obligation-list naming requirement).

**M2 and M3 are unaffected** — `diff` shows zero delta inside the M2/M3 sections of `Models.lean`; both models' `sig2`/`sig3` records gained the two new required `Sig` fields (`ExtensionDiscriminates`, `OpportunityFieldUnavailable`) with trivial/vacuous instantiations (`fun _ _ => True`/`fun _ => False`-style stubs consistent with those models' existing minimal-instantiation style), but no M2/M3 theorem statement or proof term changed.

---

## Verification.lean

Sixteen new `#print axioms` lines were added across three insertion points (Core section: 8 lines for `extension_materiality_not_from_use_alone_soundness`, `readapp_fully_appropriate`, `N01`/`N02`/`N03`, `harmonic_align_requires_readapp_provenance`, `harmonic_align_prec_noncompensatory`, `N05_stuck_implies_sns`; M1 section, two insertion points: 3 lines for `matExtMisalignedAdm`/`matExtMisalignedReadApp`/`m1_matExtMisaligned_never_direct_contact`, and 5 lines for `m1_skilled_harmonic_align_holds`/`N04_material_extension_misalignment_countermodel`/`m1_matExtMisaligned_harmonic_align_fails`/`N06_sns_not_stuck_witness`/`N07_high_activity_not_stuck_by_itself`). No existing `#print axioms` line was removed or renamed — every one of the prior package's audited declarations still appears verbatim, confirming zero regression in the axiom-audit surface. Net: 57 lines → 99 lines; 51 audit lines → 73 audit lines (see `25_final_build_and_axiom_report.md` for the full transcript).

## Main.lean

Two new `Nonempty` sanity checks added (`Nonempty (HarmonicAlign M1.sig M1.doctrine M1.Movement.skilled)`, `Nonempty (Stuck M1.sig M1.Trajectory.tStuck)`) plus the pre-existing `SNSLike`/`tLow` check retained; the final `IO.println` message text updated to name this pass's report file. Net: 32 lines → 42 lines. No change to `main`'s control flow or exit behavior.

---

## Net semantic-delta summary

| Correction | Core.lean | Models.lean | Net effect on provability |
|---|---|---|---|
| A (Stuck) | `Stuck` redefined via new `StuckThresholdWitness` inductive; `SNSLike`/`HoldingApart` untouched | `T_adv15_*` re-proved against typed witness; N06/N07 added | Logically equivalent to the old disjunctive reading for all three existing example trajectories; strictly more informative (named constructors) |
| B (HarmonicAlign/ReadApp) | `LawfulAppropriate` field removed; `FullyAppropriate`/`readapp_fully_appropriate`/`LegacyLawfulAppropriate` added; `HarmonicAlign`'s 2nd conjunct replaced | `m1_skilled_harmonic_align_holds` re-proved with `ReadApp`-derived witness | Strictly harder to construct `HarmonicAlign` than before (deliberate, per instruction) |
| C (Extensions) | `ExtensionDiscriminates` field + `MaterialExtensionOf` added; `HarmonicAlign`'s 5th conjunct replaced with universal | `matExtMisaligned`/`extBad`/`extIrrelevant`/N04 added | Strictly harder to construct `HarmonicAlign`; closes the prior vacuity |
| D (ModelSufficient) | No code change | No code change | None — docs-only reclassification (see final gap report GAP-10) |

All four corrections compose without conflict: `HarmonicAlign`'s six-conjunct shape after this patch is `AllRelFloors ∧ (∃ A, ReadApp ∧ FullyAppropriate) ∧ AllPrecFloors ∧ ¬DisqualifyingExcessForcing ∧ (∀z, MaterialExtensionOf → AlignedExtension) ∧ ContinuingContactable`, and `Stuck`'s shape after this patch is `SNSLike ∧ StuckThresholdCrossed` where `StuckThresholdCrossed` is the new three-constructor inductive — both re-verified building cleanly together via the full clean rebuild recorded in `25_final_build_and_axiom_report.md`.
</content>
