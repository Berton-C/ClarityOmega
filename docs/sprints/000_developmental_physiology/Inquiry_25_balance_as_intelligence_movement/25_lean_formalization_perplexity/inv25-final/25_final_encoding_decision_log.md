# 25 — Final Encoding Decision Log

## Investigation 25: Balance-as-Intelligence Movement — Lean 4 faithfulness patch

Schema per `25i_Lean4_Encoding_Decision_Log_and_Gap_Report_Contract.md` §1: **DECISION-ID / 25f SECTION / OLD LEAN REP / NEW LEAN REP / WHY CHANGED / STRENGTHEN? / WEAKEN? / FAITHFUL? / RATIFICATION REQUIRED?**

This log supersedes `25_encoding_decision_log.md` from the prior (now-superseded) package. It records only the decisions this patch pass actually changed (Corrections A–D) plus the disposition of every decision that pass already made and that this pass leaves untouched. The governing instruction for this pass — "Investigation 25 — Final Lean 4 Faithfulness Patch and Closure Request" — is explicit that this is *not* a re-investigation: no new mathematics is introduced, only faithfulness corrections to the existing encoding.

---

### DECISION-A1 — `StuckThresholdWitness` (Correction A)

**DECISION-ID:** DECISION-A1
**25f SECTION:** §17 ("staleness, forward movement, or the capacity to pivot is ... unavailable").
**OLD LEAN REP:** `Stuck S τ := SNSLike S τ ∧ (S.StaleForwardMotion τ ∨ S.PivotUnavailable τ)` — a bare, untyped `Or` of two `Prop`s, with no independent witness type. (This was DECISION-03 / GAP-09 in the prior package, logged there as `REQUIRES-RATIFICATION`.)
**NEW LEAN REP:** a dedicated inductive `StuckThresholdWitness (S : Sig) (τ : S.Trajectory) : Prop` with exactly three constructors — `staleForwardMotion`, `pivotUnavailable`, `opportunityFieldUnavailable` — each carrying the corresponding trajectory-level proof; `StuckThresholdCrossed S τ := StuckThresholdWitness S τ`; `Stuck S τ := SNSLike S τ ∧ StuckThresholdCrossed S τ`.
**WHY CHANGED:** the user's explicit instruction requires `Stuck_K(τ) ⟺ SNSLike_K(τ) ∧ StuckThresholdCrossed_K(τ)` as "a distinct typed predicate/witness," not a bare disjunction — the prior encoding conflated "a threshold was crossed" (a named, ratified judgment) with "one of two arbitrary Props happens to hold" (an anonymous logical connective with no independent identity). The typed inductive gives `StuckThresholdCrossed` its own name and constructor discipline, matching 25f §17's "volume crosses a threshold" language, while remaining built ONLY from the same shared trajectory primitives `SNSLike` itself already consumes (no new ontology, per the explicit "do not make Stuck a separate ontology from SNS" instruction). A third constructor (`opportunityFieldUnavailable`, backed by a new `Sig.OpportunityFieldUnavailable` field) was added because 25f §17's prose lists staleness, forward-motion, *and* pivot/opportunity availability as three named facets, and the prior encoding only typed two of them.
**STRENGTHEN?** No — every trajectory that satisfied the old disjunctive `Stuck` still satisfies the new one via the matching constructor (`staleForwardMotion`/`pivotUnavailable`), and vice versa; the two are logically equivalent modulo the added third facet, which no existing finite-model trajectory exercises either way.
**WEAKEN?** No, for the same reason.
**FAITHFUL?** Yes — this closes GAP-09 from the prior package: the disjunctive-vs-conjunctive ambiguity is now resolved not by picking a side of the ambiguity but by giving each named facet ("or") its own constructor, so `Stuck` is reachable by exactly one witness at a time (matching "only ONE constructor need apply," never a forced conjunction), while still being a genuinely typed judgment rather than an anonymous `Or`.
**RATIFICATION REQUIRED?** No — this is a strictly faithfulness-improving re-encoding of an already-disjunctive reading, not a new semantic fork. GAP-09 is closed as `RESOLVED-FAITHFUL-ENCODING` in the updated gap report (see below), not left `REQUIRES-RATIFICATION`.

**Required properties discharged:** `Stuck τ → SNSLike τ` (T13 `stuck_implies_sns`, restated as **N05** `N05_stuck_implies_sns`) — proof shape unchanged (`h.1`), still holds definitionally since `Stuck` is still `SNSLike ∧ StuckThresholdCrossed`. Countermodel `SNSLike τ ∧ ¬ Stuck τ`: `Trajectory.tLow` (**N06** `N06_sns_not_stuck_witness`, restating `T_adv15_tLow`) — SNS evidence present, but no `StuckThresholdWitness` constructor is buildable (all three underlying facts are `False` at `tLow`, so each constructor case is eliminated by `.elim`). Three finite examples required by the correction are exactly the three `T_adv15_*` trajectories: `tLow` (SNSLike, not Stuck), `tStuck` (Stuck via `staleForwardMotion`, hence also SNSLike by T13), `tBusy` (neither Stuck nor even SNSLike — **N07** `N07_high_activity_not_stuck_by_itself`, showing high `ActionEffort`/PNS-like activity at the movement level does not by itself produce Stuck at the trajectory level).

---

### DECISION-B1 — `HarmonicAlign`'s Appropriateness conjunct (Correction B)

**DECISION-ID:** DECISION-B1
**25f SECTION:** §10 (Appropriateness and lawful ReadApp), §12 (Harmonic alignment).
**OLD LEAN REP:** `HarmonicAlign`'s second conjunct was `S.LawfulAppropriate m` — an independently assignable `Sig` field, settable by any finite model with no forced connection to `ReadApp`/`Adm25Witness` at all. This was exactly the self-certification anti-pattern 25f §10/§12 and the source-audit forbidden-pattern list target: a model could set `LawfulAppropriate m := True` unconditionally even for a movement whose Relatedness/Precision floors already failed, since nothing forced `LawfulAppropriate` to route through `ReadApp`.
**NEW LEAN REP:** the second conjunct is now `∃ A : Appropriateness S m, ReadApp S Sd m A ∧ FullyAppropriate S A` — a genuine existential over `ReadApp`-derived readings. `FullyAppropriate S A := (A.kind = ReadingKind.derivedAppropriateness)`, the one kind `ReadApp`'s single constructor ever produces. `S.LawfulAppropriate` is REMOVED entirely as a `Sig` field (not merely deprecated) from `Sig`, `sig`/`sig2`/`sig3`, and every theorem statement. A narrowly-scoped `LegacyLawfulAppropriate S Sd m := ∃ A, ReadApp S Sd m A` is kept as a *derived* (never independently assignable) definition solely so `Models.lean`'s `T18_pns_high_force_contrast` narrative theorem, which historically named the old field, keeps making its point under the corrected signature.
**WHY CHANGED:** the ratified path is `Adm25 → ReadApp ⇓ A_m` (25f §10); an independently settable `LawfulAppropriate` field bypasses this path entirely, which is precisely what the user's Correction B identifies as unfaithful. Requiring the existential to be `ReadApp`-derived closes that path directly into `HarmonicAlign`'s own definition.
**STRENGTHEN?** Yes, deliberately and by explicit instruction — `HarmonicAlign` is now strictly *harder* to construct than under the old encoding, since a model can no longer set the Appropriateness conjunct to `True` by fiat. This is not an unauthorized strengthening: it is the literal content of Correction B ("remove LawfulAppropriate as an independent path"), and the user's MUST-preserve list requires exactly this ("R/A/P remain non-reconstructive... Interface growth remains real, not faked" — the same anti-self-certification spirit).
**WEAKEN?** No.
**FAITHFUL?** Yes — this is the central faithfulness bug Correction B was written to fix: under the OLD encoding, `LawfulAppropriate` defaulted to `True` for movements whose Rel/Prec floors already failed, even though no `ReadApp`/`Adm25Witness` could ever exist for them, meaning `HarmonicAlign` could in principle be self-certified independent of admissibility. That is now structurally impossible.
**RATIFICATION REQUIRED?** No — Correction B is an explicit, ratified instruction from the governing message, not a new semantic choice invented by this pass.

**Required properties discharged:** `HarmonicAlign → ∃ Adm25Witness` (**N01** `N01_harmonic_align_requires_adm25`, via `readapp_requires_adm`/T07). `HarmonicAlign → ∃ ReadApp derivation` (**N02** `N02_harmonic_align_requires_readapp`, direct projection of the second conjunct). Cannot be constructed if Rel/Prec floor fails (`harmonic_align_rel_noncompensatory`, `harmonic_align_prec_noncompensatory` — both proof-shape-unchanged corollaries of T05/T06 projected through `h.1`/`h.2.2.1`, whose *positions* in the six-conjunct tuple are unchanged by this patch). Cannot be constructed using an arbitrary Appropriateness label with no ReadApp provenance (`harmonic_align_requires_readapp_provenance`: if `∀ A, ¬ ReadApp S Sd m A`, then `¬ HarmonicAlign S Sd m`, since the only way to inhabit the second conjunct is a real `ReadApp` proof).

---

### DECISION-B2 — `LegacyLawfulAppropriate` retained as derived-only

**DECISION-ID:** DECISION-B2
**25f SECTION:** §10, §12 (cross-reference to DECISION-B1).
**OLD LEAN REP:** n/a (new to this pass).
**NEW LEAN REP:** `LegacyLawfulAppropriate S Sd m := ∃ A : Appropriateness S m, ReadApp S Sd m A` — kept ONLY as a derived, `ReadApp`-sourced definition, never again an independently assignable `Sig` field, used solely inside `T18_pns_high_force_contrast`'s statement in `Models.lean`.
**WHY CHANGED:** rewriting `T18_pns_high_force_contrast` to drop all reference to the old field would have silently discarded a working narrative theorem's exact phrasing; instead the name is preserved but its *content* is now forced to be `ReadApp`-derived, so it cannot diverge from admissibility the way the old field could.
**STRENGTHEN?** No relative to the corrected `HarmonicAlign` (it is defined in terms of the same `ReadApp` machinery); yes relative to the OLD `LawfulAppropriate` field (same strengthening as DECISION-B1, inherited).
**WEAKEN?** No.
**FAITHFUL?** Yes.
**RATIFICATION REQUIRED?** No — purely a naming/continuity accommodation with no independent semantic content of its own (it is definitionally an existential over `ReadApp`, nothing else).

---

### DECISION-C1 — `MaterialExtensionOf` and universal extension quantification (Correction C)

**DECISION-ID:** DECISION-C1
**25f SECTION:** §13 (Extensions and consequence), §6 (Materiality, lifted to extensions).
**OLD LEAN REP:** `HarmonicAlign` took an explicit caller-supplied extension parameter `z : S.Extension` and its fifth conjunct was `S.ExtensionOf z m → S.AlignedExtension z m` — a single, caller-chosen `z`, checked once. If the caller supplied a `z` that was not `ExtensionOf` at all (e.g. an irrelevant/non-participating extension), the implication was true vacuously and told you nothing about the movement's actual extensions.
**NEW LEAN REP:** a new definition `MaterialExtensionOf S z m := S.ExtensionOf z m ∧ S.ExtensionDiscriminates z m` (the materiality discipline of §6/T04, lifted verbatim to extensions — mirrors `MaterialTo`), and `HarmonicAlign`'s fifth conjunct is now the universal `∀ z : S.Extension, MaterialExtensionOf S z m → S.AlignedExtension z m`. `HarmonicAlign` no longer takes an extension parameter at all.
**WHY CHANGED:** the old single-`z`, caller-supplied check was too weak and could be satisfied vacuously by supplying an unrelated `z`; the user's Correction C explicitly requires replacing it with a universal statement over every materially participating extension of `m`.
**STRENGTHEN?** Yes, deliberately — the universal is strictly harder to satisfy than a single existential/caller-chosen check when more than one material extension exists, matching the explicit instruction.
**WEAKEN?** No.
**FAITHFUL?** Yes — `ExtensionDiscriminates` (a new `Sig` field, the extension-level counterpart of `DiscriminatesRel`/`DiscriminatesDist`) ensures `MaterialExtensionOf` cannot be satisfied by an extension that merely happens to be nominally "of" the movement (`ExtensionOf`) without also making a genuine counterfactual difference to it — exactly mirroring why `MaterialTo` (§6) requires both `UsedByRel` and `DiscriminatesRel`, not `UsedByRel` alone (T04's soundness direction, now also proved for extensions via `extension_materiality_not_from_use_alone_soundness`).
**RATIFICATION REQUIRED?** No — Correction C is an explicit, ratified instruction.

**Required adversarial tests discharged (M1):** all-material-aligned passes — `m1_skilled_harmonic_align_holds : HarmonicAlign sig doctrine skilled`, whose universal-extension case-splits over `ext1`/`extBad`/`extIrrelevant` and discharges each (the latter via `hz.2.elim`, since `extIrrelevant` fails `ExtensionDiscriminates` and so is never a `MaterialExtensionOf` witness in the first place). One-material-misaligned fails — **N04** `N04_material_extension_misalignment_countermodel`: `matExtMisaligned` has `Extension.extBad` as a genuine `MaterialExtensionOf` witness that is NOT `AlignedExtension`, and `m1_matExtMisaligned_harmonic_align_fails` derives `¬ HarmonicAlign sig doctrine matExtMisaligned` directly from it via the universal's contrapositive. Irrelevant/non-participating extension doesn't affect it — `extIrrelevant` (constructed so `ExtensionOf` holds but `ExtensionDiscriminates` fails) is excluded from `MaterialExtensionOf` by construction, so it can never be the extension that breaks `HarmonicAlign`; this is exercised inside `m1_skilled_harmonic_align_holds`'s own case split. Vacuous unrelated extension must not satisfy the requirement — because the conjunct is now a universal (not an existential the caller can dodge by choosing a convenient `z`), there is no way to "supply" a favorable `z` to make the requirement pass vacuously; every `z : S.Extension` in the model's actual `Extension` type is checked.

---

### DECISION-D1 — `ModelSufficient` reclassification (Correction D)

**DECISION-ID:** DECISION-D1
**25f SECTION:** §14 (Bounded Harmonic Continuation), 25h §10 (`ModelSufficient` self-certification adversary).
**OLD LEAN REP:** `ModelSufficient (w) m := True` unconditionally in M1/M2, `w.elim` in M3 (`WorldModel := Empty`) — documented in the prior package's gap report as GAP-10, disposition `RESOLVED-FAITHFUL-ENCODING`.
**NEW LEAN REP:** UNCHANGED. Per the explicit instruction "do not redesign BHC theorem... current `ModelSufficient := True` acceptable as toy scaffolding," no code change was made to `ModelSufficient`'s definition in `Core.lean` or any of the three models.
**WHY CHANGED:** not changed in content — only in *documentation classification*. The governing instruction requires reclassifying the docs describing this encoding from `RESOLVED-FAITHFUL-ENCODING` to `PROVISIONAL-ENCODING`, because "resolved" language over-claims: `ModelSufficient := True` is a toy scaffolding choice that happens to be non-self-certifying (it never inspects `w`'s own internal description), not a faithful encoding of whatever the eventual external-governance sufficiency interface will actually require. The prior package's own GAP-10 language ("`True` here is not an assumption about the world, it is the (unconditionally true) absence of any self-certification path") remains correct and is preserved verbatim in spirit, but the *label* attached to it is corrected.
**STRENGTHEN?** No — no proof obligation changed strength.
**WEAKEN?** No.
**FAITHFUL?** The code was already faithful to the narrow "not self-certifying" requirement (25h §10); the fix here is purely that the prior report over-classified a provisional toy scaffold as "resolved," which risked implying more permanence than is warranted. No runtime model may self-certify complete sufficiency — this remains true and is preserved unchanged: no field of any model's `ModelSufficient` instance is computed from that model's own internal description of itself.
**RATIFICATION REQUIRED?** The gap this decision touches (GAP-10, renamed for cross-reference clarity) is now logged as `PROVISIONAL-ENCODING` rather than `RESOLVED-FAITHFUL-ENCODING` in the updated gap report — see `25_final_formalization_gap_report.md`. This is a stricter (more honest), not a looser, classification, so it does not itself require ratification; it flags that a final evidence source for `ModelSufficient` still awaits a future ratification decision, exactly as Correction D instructs ("do not invent a final evidence source").

---

### Decisions carried forward unchanged from the prior package

The following decisions from `25_encoding_decision_log.md` (superseded) are **unaffected** by Corrections A–D and remain in force exactly as originally logged, cross-referenced here for completeness (full text in the prior package, retained in this session's audit trail):

| ID | Subject | Status this pass |
|---|---|---|
| DECISION-01 | `Sig` as one bundled record parameter | Unchanged |
| DECISION-02 | `V := Standing` (three-valued Rel/Prec carrier) | Unchanged (GAP-02 remains `PROVISIONAL-ENCODING`) |
| DECISION-03 | Old disjunctive `Stuck` reading | **Superseded by DECISION-A1** (GAP-09 closed) |
| DECISION-04 | M1 hosts model-agnostic adversaries | Unchanged |
| DECISION-05 | PNS/SNS/Stuck live on `Trajectory`, not `Movement` | Unchanged — explicitly preserved by Correction A ("do not make Stuck a separate ontology from SNS") |
| DECISION-06 | `lakefile.toml` vs `lakefile.lean` | Unchanged |
| DECISION-07 | M2's cut-empty `Distinction` types (hindsight-fairness) | Unchanged |
| DECISION-08 | M3's `WorldModel := Empty` | Unchanged |
| DECISION-09 | `AvailableAt` match-on-cut (anti-fake interface growth) | Unchanged |
| DECISION-10 | M3's material/decorative `Relation` split for Fourthness | Unchanged |
| DECISION-11 | T12 content proved under `T18_energetic_case_A_skilled`'s name | Unchanged |
| MECHANICAL-01 .. 06 | Lean-engineering fixes (auto-bound-implicit, `@[reducible]`, `simp only` vs `unfold`, `Decidable` synthesis, ambiguous-namespace, equation-compiler sugar) | Unchanged; MECHANICAL-04's pattern (`by decide` → `fun h => h` / `(h : False).elim`) recurred in this pass's fixes for the redesigned `Stuck`/`StuckThresholdWitness` case splits — see MECHANICAL-07 below. |

---

### Mechanical Lean-engineering fixes discovered during this patch

**MECHANICAL-07 — anonymous-constructor / record-literal syntax conflict under the redesigned `HarmonicAlign`.**
Symptom: `m1_skilled_harmonic_align_holds`'s six-conjunct anonymous constructor, when the second conjunct's witness was written out explicitly as an anonymous tuple `⟨skilledAdm, skilledReadApp, rfl⟩`, triggered a parser ambiguity against the surrounding `refine ⟨..., ?_, ...⟩` structure.
Fix: let Lean infer the existential witness (`⟨_, skilledReadApp, rfl⟩`) rather than spelling out the `Adm25Witness` component explicitly — it is already implied by `skilledReadApp`'s own type via `readapp_requires_adm`.

**MECHANICAL-08 — `Decidable` instance synthesis failure on `StuckThresholdWitness` case splits.**
Symptom: `absurd hw (by decide)` inside the `T_adv15_tLow`/`T_adv15_tStuck`/`T_adv15_tBusy` case analyses over the new `StuckThresholdWitness` constructors failed to synthesize `Decidable` instances for the Sig-projected trajectory predicates (`StaleForwardMotion`, `PivotUnavailable`, `OpportunityFieldUnavailable` at `tLow`; `ContactExclusion`, `Recurrence`, `InterfaceNarrowing` at `tBusy`) — the same underlying transparency issue as the prior package's MECHANICAL-04, now manifesting on the new inductive's case arms.
Fix: replaced all six occurrences with `exact hw.elim` / `exact h.elim`, relying on definitional equality to `False` rather than requiring a `Decidable` instance — identical remedy pattern to MECHANICAL-04, applied to the newly-introduced code paths.
</content>
