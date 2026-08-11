# 25 — Final Formalization Mapping Report

## Investigation 25: Balance-as-Intelligence Movement — Lean 4 faithfulness patch

**Authority:** `25f_Ratified_Balance_as_Intelligence_Mathematical_Object.md` (semantic authority).
**Contract:** `25g_Lean4_Formal_Hardening_Specification.md`, `25h_Lean4_Proof_Obligations_and_Adversarial_Tests.md`.
**Scope of this document:** section-by-section correspondence between every `25f` clause and the CORRECTED Lean declarations in `Core.lean`/`Models.lean`, revised for Corrections A–D. This supersedes `25_formalization_diff_and_mapping.md` from the prior package. Sections unaffected by Corrections A–D are reproduced with their original mapping (they did not change); sections §10, §12, §13, §14, §16, §17 are rewritten to reflect the corrected encoding.

Legend: **[Core]** = `Inv25` namespace in `Core.lean`. **[M1]/[M2]/[M3]** = `Inv25.M1`/`M2`/`M3` in `Models.lean`. **GAP-nn**/**DECISION-nn** cross-reference the final gap report / final decision log.

---

### §0 Ratification (the boxed object) — unchanged

`𝔖 ⊢ m : 𝔅_K ⇝ 𝔅_K'` → `S.Movement K K'` **[Core]**, per DECISION-01. No change from Corrections A–D.

### §1–§8 — unchanged

Jurisdiction boundary (GAP-01), anti-2D-collapse (GAP-07, T11 `no_scalar_override`), Soul-doctrine-as-ambient-parameter (§3), Dynamic Participatory Fourthness (§4), energetic typing (§5, GAP-03/GAP-06), Materiality (§6, T04 `materiality_not_from_use_alone_soundness` — now ALSO exercised at the extension level via `extension_materiality_not_from_use_alone_soundness`, see §13 below), Relatedness (§7, T05), Precision (§8, T06) are all unaffected by Corrections A–D and map exactly as in the prior package's mapping report.

### §9 Admissibility inherits Inquiry-24 law — unchanged

`Adm25Witness` **[Core §4]** — the proof-relevant seven-field structure — is unchanged in shape; it is now, however, load-bearing in a NEW way: `HarmonicAlign`'s redesigned second conjunct forces every `HarmonicAlign` witness to route through a genuine `ReadApp` (which itself requires an `Adm25Witness`, RA1), making `Adm25`'s presence *provable* from `HarmonicAlign` (N01), not merely available as an unconnected sibling structure.

### §10 Appropriateness and lawful ReadApp — **CORRECTED (Correction B)**

`ReadApp` **[Core §5]** itself (RA1–RA8, T07–T11) is unchanged. What changed is how `HarmonicAlign` *consumes* a `ReadApp`-derived reading: previously via an independently assignable `LawfulAppropriate` field (bypassing the RA1–RA8 discipline entirely for `HarmonicAlign`'s purposes); now via a genuine `∃ A, ReadApp S Sd m A ∧ FullyAppropriate S A` existential (DECISION-B1). `FullyAppropriate` **[Core §5/§6]** is a new definition: `A.kind = ReadingKind.derivedAppropriateness`, the one kind `ReadApp`'s single constructor ever produces — proved automatic for any `ReadApp` witness by `readapp_fully_appropriate`. `LegacyLawfulAppropriate` **[Core §5/§6]** is kept ONLY as a derived (`∃ A, ReadApp S Sd m A`), never-independently-assignable definition (DECISION-B2), used solely by `T18_pns_high_force_contrast` **[M1]** for narrative continuity.

### §11 R/A/P inseparability and constructor discipline — unchanged

T01/T02/T03 (`source_identity_rel`/`_app`/`_prec`) and T25 `T25_rap_summary_noninjective` **[M1]** are unaffected; `HarmonicAlign`'s redesign does not touch R/A/P source-identity.

### §12 Harmonic alignment — **CORRECTED (Corrections B, C)**

`HarmonicAlign_K(m)` → `HarmonicAlign` **[Core §6]**, now taking an explicit `Sd : S.SoulDoctrine` parameter and dropping the caller-supplied extension parameter entirely. The six conjuncts, in order:

1. `AllRelFloors S m` (unchanged)
2. **CORRECTED (B):** `∃ A : Appropriateness S m, ReadApp S Sd m A ∧ FullyAppropriate S A` (was `S.LawfulAppropriate m`)
3. `AllPrecFloors S m` (unchanged)
4. `¬ S.DisqualifyingExcessForcing m` (unchanged)
5. **CORRECTED (C):** `∀ z : S.Extension, MaterialExtensionOf S z m → S.AlignedExtension z m` (was `S.ExtensionOf z m → S.AlignedExtension z m` for a single caller-supplied `z`)
6. `S.ContinuingContactable m` (unchanged)

Conjunct *positions* 1/3/4/6 are unchanged from the prior package by explicit design, so T14 (`h.1`) and T15 (`h.2.2.1`) projections remain valid unchanged. New theorems **N01**–**N04** and `harmonic_align_requires_readapp_provenance`/`harmonic_align_prec_noncompensatory` are the direct discharge of the correction's required properties (see DECISION-B1/DECISION-C1 in the final decision log for full detail). `m1_skilled_harmonic_align_holds` **[M1]** is the concrete non-vacuous witness that a real movement (`skilled`) still satisfies the strictly-harder corrected definition.

### §13 Extensions and consequence — **CORRECTED (Correction C)**

`ExtensionOf`, `AlignedExtension`, `ContinuingContactable` **[Core §1]** remain opaque `Sig` primitives (GAP-05 unaffected). NEW: `MaterialExtensionOf S z m := S.ExtensionOf z m ∧ S.ExtensionDiscriminates z m` **[Core §2]**, mirroring `MaterialTo`'s §6 discipline (DECISION-C1), with its own soundness theorem `extension_materiality_not_from_use_alone_soundness` (the extension-level analogue of T04). `Sig.ExtensionDiscriminates`/`Sig.OpportunityFieldUnavailable` are new `Sig` fields, instantiated per-model in M1/M2/M3's `sig`/`sig2`/`sig3` records (replacing the removed `LawfulAppropriate` field slot). M1's `matExtMisaligned` movement and `extBad`/`extIrrelevant` extensions **[M1]** are the concrete adversarial instantiation exercising N04 and the four required adversarial tests (see DECISION-C1).

### §14 Bounded Harmonic Continuation — hardened status — **re-stated signature, unchanged content**

T16 `bounded_harmonic_continuation` / T17 `nonharmonic_falsifier` **[Core §7]** are re-stated against the new `HarmonicAlign S Sd m` signature (drops the caller-supplied `z`, adds the `Sd` parameter the corrected definition requires) — no mathematical content changes; `HarmonicAlign` is still supplied as one opaque premise among five, and the `hschema` connecting-premise structure (GAP-08) is untouched. `m1_bhc_good_layer1`/`m1_bhc_bad_layer2_falsifier` **[M1]** are re-proved against `m1_skilled_harmonic_align_holds` (the new, strictly-harder-to-construct `HarmonicAlign` witness for `skilled`). `ModelSufficient`'s definition is UNCHANGED (Correction D explicitly forbids redesigning BHC) — only its documentation classification moves from `RESOLVED-FAITHFUL-ENCODING` to `PROVISIONAL-ENCODING` (GAP-10, DECISION-D1); this is a docs-only correction with zero Lean source changes to `ModelSufficient` itself.

### §15 PNS-like organization — unchanged

`PNSLike`'s nine conjuncts **[Core §8]** are unaffected by Correction A (which targets `Stuck`, not `PNSLike`). `T18_tBusy_is_PNSLike` **[M1]** unchanged.

### §16 SNS-like organization — unchanged structure, now load-bearing for Correction A

`HoldingApart` (disjunction) and `SNSLike` (`HoldingApart ∧ ForcedVelocity`) **[Core §8]** are UNCHANGED definitions — the explicit instruction "do not make Stuck a separate ontology from SNS" is satisfied precisely because `Stuck`'s redesign (below) still wraps this same, untouched `SNSLike`.

### §17 Stuck is SNS above a functional threshold — **CORRECTED (Correction A)**

`Stuck_K(τ) ⟺ SNSLike_K(τ) ∧ StuckThresholdCrossed_K(τ)` → `Stuck S τ := SNSLike S τ ∧ StuckThresholdCrossed S τ` **[Core §8]**, where `StuckThresholdCrossed S τ := StuckThresholdWitness S τ`, a new three-constructor inductive (`staleForwardMotion`/`pivotUnavailable`/`opportunityFieldUnavailable`) built from the same shared trajectory primitives `SNSLike` already consumes plus one new field, `Sig.OpportunityFieldUnavailable` (DECISION-A1; supersedes the old bare-`Or` reading, GAP-09 now `RESOLVED-FAITHFUL-ENCODING`). T13 `stuck_implies_sns` (`Stuck → SNSLike`, **no** converse — grep-confirmed) is unchanged in proof shape (`h.1`), restated as **N05**. The three-trajectory threshold adversary is re-proved against the typed witness: `T_adv15_tLow` (SNSLike, not Stuck — **N06**), `T_adv15_tStuck` (Stuck via the `staleForwardMotion` constructor, hence also SNSLike), `T_adv15_tBusy` (neither Stuck nor SNSLike — **N07**, the explicit "high activity ≠ Stuck" negative control) **[M1]**.

### §18–§26 — unchanged

Open-ended possibility / interface growth (§18, T20/T23, unaffected by Corrections A–D — the anti-fake `AvailableAt` match-on-cut discipline, DECISION-09, is untouched), Awareness jurisdiction-limited use (§19, GAP-01), Relationship to Inquiry 24 (§20, GAP-12), MeTTa projection (§21, GAP-13, out of scope), Ratification falsifiers (§22, GAP-14), Canonical/provisional ledger (§23, cross-referenced to GAP-02/03/04/05/06/13 plus the newly-provisional GAP-10), Evidence already earned (§24, M1/M2/M3 design origin), Final ratification claim (§25), Investigation-25 closure (§26) are all unaffected by Corrections A–D and map exactly as in the prior package.

---

## Theorem-inventory cross-reference (25g §19 + new obligations)

See `25_final_build_and_axiom_report.md` for the full T01–T25 + N01–N07 table with proof status and `#print axioms` results. Summary: **T01–T25 remain fully discharged** under the corrected signatures (T13/T14/T15/T16/T17/T18/T_adv15_* all re-proved against the new `HarmonicAlign`/`Stuck` shapes with no regression — see the final decision log's mechanical-fixes appendix for the two elaborator-level fixes this required). **N01–N07 are newly discharged** as the direct proof obligations of Corrections A/B/C: N01 (`HarmonicAlign → ∃ Adm25Witness`), N02 (`HarmonicAlign → ∃ ReadApp`), N03 (`HarmonicAlign → ∀ material extension aligned`), N04 (material-extension-misalignment countermodel), N05 (`Stuck → SNSLike`, restated), N06 (SNS-not-Stuck witness, restated), N07 (high-activity-not-Stuck-by-itself). T12's naming deviation (DECISION-11, content proved under `T18_energetic_case_A_skilled`) is unaffected and carried forward unchanged.
</content>
