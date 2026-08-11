# 25 — Formalization Diff and Mapping Report

## Investigation 25: Balance-as-Intelligence Movement — Lean 4 hardening

**Authority:** `25f_Ratified_Balance_as_Intelligence_Mathematical_Object.md` (semantic authority, 557 lines / 26 numbered sections + preamble).
**Contract:** `25g_Lean4_Formal_Hardening_Specification.md`, `25h_Lean4_Proof_Obligations_and_Adversarial_Tests.md`.
**Scope of this document:** section-by-section correspondence between every `25f` clause and the Lean declarations in `Core.lean` / `Models.lean` that formalize (or deliberately leave abstract) it. Read alongside `25_encoding_decision_log.md` (why each nontrivial representation choice was made) and `25_formalization_gap_report.md` (every place `25f` does not uniquely determine a Lean encoding).

Legend: **[Core]** = `Inv25` namespace in `Core.lean`. **[M1]/[M2]/[M3]** = `Inv25.M1`/`M2`/`M3` in `Models.lean`. **GAP-nn** cross-references the gap report. **DECISION-nn** cross-references the decision log.

---

### §0 Ratification (the boxed object)

`𝔖 ⊢ m : 𝔅_K ⇝ 𝔅_K'`, with `𝔅_K = (D_K, Ω_K, I_K, W_K, C^Soul_K)`, and `Rel_K(m)`, `App_K(m)`, `Prec_K(m)`.

- The turnstile/typing judgment itself is `S.Movement K K'` **[Core]**, cut-indexed per DECISION-01.
- `𝔅_K`'s five components are distributed across `Sig` fields rather than reassembled into one literal 5-tuple record (DECISION-01): `D_K` → `Sig.Relation K`; `Ω_K` (Fourthness/overlap) → `DiscriminatesRel`/`DiscriminatesDist`; `I_K` → `Sig.Mode K` + `AvailableAt`; `W_K` (world-model / self-weaving) → `Sig.Trajectory`, `Sig.WorldModel`; `C^Soul_K` → the ambient `Sig.SoulDoctrine` parameter (never a field a movement can set — DECISION-01, §3 below).
- `Rel_K(m)` → `Sig.relStanding m : Relation K → Standing` **[Core]**.
- `App_K(m)` → the `Appropriateness`/`ReadApp` machinery **[Core §5]**.
- `Prec_K(m)` → `Sig.distStanding m : Distinction K → Standing` **[Core]**.

### §1 Jurisdiction and ontological boundary

`25g §1`'s explicit inclusion/exclusion list is honored by construction: every excluded item (ontological-phenomenological-consciousness, complete Soul mathematics, complete awareness mathematics, universal `E_force` thermodynamics, the unified kernel) has **no** corresponding Lean declaration anywhere in `Core.lean`/`Models.lean` — see GAP-01, GAP-03, GAP-04, GAP-06, GAP-13.

### §2 Balance-as-intelligence and anti-2D collapse

No scalar `IntelligenceScore`/`weightedRAP`/`overallIntelligence` declaration exists anywhere in the package (grep-confirmed). This absence is itself the formalization of §2's anti-collapse claim — see GAP-07 (this is a correctly-absent structure, not an oversight) and T11 `no_scalar_override` **[Core]**.

### §3 Soul doctrine is ambient

- `Sig.SoulDoctrine : Type` **[Core]** is the outermost parameter every judgment is indexed by (`Adm24 (Sd : SoulDoctrine) ...`, `ReadApp S Sd ...`).
- No `Sig` field anywhere lets a `Movement` assign its own Soul standing — confirmed by inspection: `Sig` has no `soulStanding` field, and `SoulDoctrine` never appears as a *return type* of any movement-indexed function, only as a fixed parameter. This directly satisfies 25h §1's adversary (Soul standing is not a DPF/`Movement` carrier field).

### §4 Dynamic Participatory Fourthness

- §4.1 live relation diagram → `Sig.Relation : Cut → Type` **[Core]**.
- §4.2 Fourthness/overlap → `Sig.DiscriminatesRel`/`DiscriminatesDist : Movement K K' → Relation/Distinction K → Prop` **[Core]**; concretely exercised by M3's `a`/`b`/`z` relations and `T22_fourthness` **[M3]**.
- §4.3 participation interface → `Sig.Mode : Cut → Type` + `AvailableAt` **[Core §9]**; exercised by M2's `T20_interface_growth` and M3's `T23_interface_growth_from_LA/LB` **[M2, M3]**.
- §4.4 self-weaving/path structure → `Sig.Trajectory`, `SelfWeavingPlasticity` (one of the nine `PNSLike` witnesses) **[Core §8]**; exercised by M1's `T18_tBusy_is_PNSLike` **[M1]**.
- §4.5 live constitutional relations (without embedding Soul standing) → `Sig.Relation`/`RequiredRel`, kept entirely separate from `SoulDoctrine` (§3 above).

### §5 Movement and energetic typing

`E_phys ≠ E_rep ≠ E_act ≠ E_force ≠ G` → five single-field wrapper structures `PhysicalEnergy`, `RepresentationEffort`, `ActionEffort`, `ExcessForcing`, `Genenergy` **[Core §0]**, with no coercion between them. `ActionEffort ≠ ExcessForcing` (the specific 25g §13 obligation) is exercised by `T18_energetic_case_A_skilled`/`_case_B_lowActHighForce`/`T18_pns_high_force_contrast` **[M1]**. The exact numeric `E_force` metric is explicitly not formalized — GAP-06.

### §6 Materiality

`UsedBy m x` ↛ `MaterialTo x m` → `MaterialTo`/`MaterialToDist` **[Core §2]** defined as `UsedByRel ∧ DiscriminatesRel` (resp. Dist), proved insufficient-from-`UsedBy`-alone by `materiality_not_from_use_alone_soundness` (T04) **[Core]**, with the genuine failing/succeeding countermodel pair `m1_materiality_used_not_material` / `m1_materiality_good_is_material` **[M1]**.

### §7 Relatedness

`Rel_K(m) : R_K^mat → V` → `Sig.relStanding m : Relation K → Standing` (DECISION-02 for the choice of `V := Standing`), with the non-compensatory floor `RelFloor`/`AllRelFloors` **[Core §3]** and its noncompensation theorem T05 `rel_floor_noncompensatory` **[Core]**, exercised by `m1_rel_noncomp_fails_floors` **[M1]** and M3's Fourthness pair `m3_missingA_fails_relfloor`/`m3_missingB_fails_relfloor` **[M3]**.

### §8 Precision

`Prec_K(m) : Δ_K^mat → V` → `Sig.distStanding m : Distinction K → Standing`, with `PrecFloor`/`AllPrecFloors` **[Core §3]** and T06 `prec_floor_noncompensatory` **[Core]**, exercised by `m1_prec_noncomp_fails_floors` **[M1]** and M2's `m2_severed_fails_precfloor`/`m2_retryBefore_not_penalized` (T19) **[M2]**.

### §9 Admissibility inherits Inquiry-24 law

`Adm^24_𝔖(m)` → `Sig.Adm24 : SoulDoctrine → Movement K K' → Prop` **[Core §1]**, kept as an opaque imported interface (never redefined — 25h §18 audit; confirmed by grep: no local redefinition of Inquiry-24 concepts such as provenance legality or lifecycle standing appears anywhere in the package). `Adm^25_K(𝔅_K)` → `Adm25Witness` **[Core §4]**, the proof-relevant seven-field structure matching §9's/25g §10's seven numbered clauses exactly (`available`, `adm24`, `relFloors`, `precFloors`, `noDisqualifyingForcing`, `participationOpen`, `consequenceAnswerable`).

### §10 Appropriateness and lawful ReadApp

`ReadApp` **[Core §5]** is the single-constructor inductive judgment over `Appropriateness`. The eight laws RA1–RA8 map as: RA1 (no reading without Adm25) → `adm` constructor argument, proved generically by T07 `readapp_requires_adm`; RA2 (source identity) → the reading is indexed by `m` itself (`srcIsM : True := trivial` plus the very index), proved by T02 `source_identity_app`; RA3 (provenance/kind carried) → `prov`/`gen` stored fields of `Appropriateness`; RA4 (never direct-contact) → the constructor always produces `kind := derivedAppropriateness`, proved by T08 `readapp_no_contact_masquerade`; RA5/RA6 (floor failure blocks reading) → `adm.relFloors`/`adm.precFloors` fields, proved by T09/T10 `readapp_rel_floor`/`readapp_prec_floor`; RA7 (no scalar override) → T11 `no_scalar_override`; RA8 (doctrine-bound evaluator) → the `ev : DoctrineBound (evaluatorOf m) Sd` constructor argument.

### §11 R/A/P inseparability and constructor discipline

`src(R_m) = src(A_m) = src(P_m) = m` → T01/T02/T03 `source_identity_rel`/`_app`/`_prec` **[Core]**, each proved by `rfl` because every profile function is *defined* as `S.relStanding m` (etc.) rather than a separately settable field that could diverge. No scalar aggregate constructor exists — confirmed absent (GAP-07). The R/A/P non-injectivity witness required by 25h §6 is T25 `T25_rap_summary_noninjective` **[M1]**: `forcedHighHigh ≠ lowActHighForce` yet `summaryRAP forcedHighHigh = summaryRAP lowActHighForce`.

### §12 Harmonic alignment

`HarmonicAlign_K(m)` → `HarmonicAlign` **[Core §6]**, a six-conjunct `def` (never a `Sig` field), matching §12's six numbered clauses exactly: `AllRelFloors`, `LawfulAppropriate`, `AllPrecFloors`, `¬DisqualifyingExcessForcing`, aligned-extension implication, `ContinuingContactable`. T14/T15 `harmonic_alignment_requires_rel_floors`/`_prec_floors` and `harmonic_align_rel_noncompensatory` **[Core]** lift the §7/§8 noncompensation results to this level.

### §13 Extensions and consequence

`ExtensionOf`, `AlignedExtension`, `ContinuingContactable` **[Core §1]** — kept as opaque `Sig` primitives (25f §13's tool/API/body-segment examples are not individually typed; see GAP-05).

### §14 Bounded Harmonic Continuation — hardened status

The forward schema and its five premises map one-to-one onto T16 `bounded_harmonic_continuation`'s hypotheses **[Core §7]**; the connecting `hschema` premise (why Lean cannot derive `HarmonicOutcome` from the other four alone) is GAP-08. Layer-1/Layer-2 of 25h §9 are discharged by `m1_bhc_good_layer1`/`m1_bhc_bad_layer2_falsifier` **[M1]**. T17 `nonharmonic_falsifier` **[Core]** is the ordinary-logic contrapositive, proved (not postulated) from T16.

### §15 PNS-like organization

The nine witnesses map one-to-one onto `PNSLike`'s nine conjuncts **[Core §8]**: `Contactability`, `RelationalOpenness`, `PreservedDistinctions`, `ReceptiveAttention`, `DifferentiationWithCoherence`, `LowUnnecessaryForcing`, `TrajConsequenceAnswerable`, `InterfaceOpenness`, `SelfWeavingPlasticity` — all `Sig` fields on `Trajectory`, per DECISION-05 (PNS/SNS live on `Trajectory`, not `Movement`). Exercised by `T18_tBusy_is_PNSLike` **[M1]**.

### §16 SNS-like organization

"Holding apart" (read as *any one* of contact-exclusion/recurrence/interface-narrowing, since §16 offers them as alternative possible witnesses) + "forced velocity" → `HoldingApart` (disjunction) and `SNSLike` (`HoldingApart ∧ ForcedVelocity`) **[Core §8]**.

### §17 Stuck is SNS above a functional threshold

`Stuck_K(τ) ⇒ SNSLike_K(τ)` → `Stuck` (`SNSLike ∧ (StaleForwardMotion ∨ PivotUnavailable)`, DECISION-03 for the disjunctive reading) and T13 `stuck_implies_sns` **[Core §8]**, with **no** converse lemma anywhere (grep-confirmed). Exercised by the three-trajectory threshold adversary `T_adv15_tLow`/`T_adv15_tStuck`/`T_adv15_tBusy` **[M1]**.

### §18 Open-ended possibility

`I_K ⇝ I_K'` → `InterfaceChange` **[Core §9]**: `¬AvailableAt modeAtK ∧ AvailableAt modeAtK'`, explicitly distinguishing "new mode after transition" from "all modes pre-authorized," per 25g §17's anti-fake requirement. Exercised twice independently: `T20_interface_growth`/`T20_interface_growth_not_faked` **[M2]** and `T23_interface_growth_from_LA/LB`/`T23_interface_growth_not_faked` **[M3]**.

### §19 Awareness and meta-awareness — jurisdiction-limited use

Formalized *only* to the extent §19 licenses — as a special case of `InterfaceChange`'s availability asymmetry, never as a general awareness/consciousness theory (GAP-01 records the boundary explicitly). Exercised by M2's meta-awareness-bite adversary `T21_meta_awareness_bite` **[M2]**: `retryTraceVisible` admits a lawful `Adm25Witness`, `retryTraceSevered` provably does not.

### §20 Relationship to Inquiry 24

`Sig.SoulDoctrine`, `Sig.Provenance`, `Sig.GenerationKind` are all deliberately abstract, opaque, undefined-beyond-their-type-signature primitives **[Core §1]**, and `Adm24` is consumed, never redefined (see §9 above and 25h §18 audit).

### §21 MeTTa computational projection

Out of scope for this Lean development per 25g §1's exclusion list — no MeTTa-related declaration exists anywhere in the package. See GAP-13.

### §22 Ratification falsifiers

Each of the 15 numbered failure modes is checked against the Lean encoding; the two most direct hits are: falsifier "weighted intelligence override" is blocked by the correct absence of any `IntelligenceScore` declaration (T11 `no_scalar_override`, GAP-07); falsifier "incompatible locally grounded frames forced into one master representation" is directly falsified by M3's `WorldModel := Empty` encoding and `T24_no_global_model_required` **[M3]**; falsifier "deleting material Fourthness relations never changing admissible movement" is directly falsified by `T22_fourthness`'s `m3_missingA_fails_relfloor`/`m3_missingB_fails_relfloor` **[M3]**. The full falsifier-by-falsifier audit is not exhaustively re-derived as separate Lean declarations beyond these — most falsifiers describe encoding *anti-patterns* (things the package must not contain) rather than positive theorems, and are checked by inspection/grep rather than by proof; this is recorded, not hidden, in the gap report (GAP-14).

### §23 Canonical versus provisional ledger

Every item §23 lists as provisional/deferred (exact `E_force` metric, exact carrier `V`, `ReadApp` semantic seams beyond its four RA laws, complete awareness/meta-awareness mathematics, the nine Immutable Facts, Soul formalization, physical-energy grounding, the unified kernel) corresponds one-to-one to a gap report entry (GAP-02, GAP-03, GAP-04, GAP-05, GAP-06, GAP-13) rather than to invented Lean structure — `Core.lean` leaves each of these abstract or trivially typed rather than resolving them silently.

### §24 Evidence already earned

Explicitly names the three finite examples this development builds: "high-action-effort/low-excess-forcing skilled movement" → **M1**; "Clarity contact-grounded frame pivot" → **M2**; "heterogeneous knowledge inquiry with genuine Fourthness and interface growth" → **M3**. This confirms the M1/M2/M3 design was derived directly from this sentence, not chosen independently.

### §25 Final ratification claim

Restates the §0 boxed object; no additional Lean content beyond §0's mapping above.

### §26 Investigation-25 closure and next step

The direct source of this entire task: "encode its minimal typed signature in Lean 4 ... encode the three finite interpretations ... prove constructor discipline, material-floor behavior, Fourthness discrimination, and the bounded harmonic falsifier where theorem-shaped ... return a formalization-gap report for anything not uniquely typeable ... do not add assumptions silently to make proofs compile." This mapping report, the decision log, the gap report, and the build/axiom report are the direct discharge of this closure instruction.

---

## Theorem-inventory cross-reference (25g §19)

See `25_build_and_axiom_report.md` for the full T01–T25 table with proof status, countermodel status, and `#print axioms` results. Summary: **T01–T25 are all discharged** except T12 (`high_action_low_force_consistent`), whose *content* is proved but under a different declaration name (`T18_energetic_case_A_skilled`) — logged as a naming deviation, not a mathematical gap (see decision log, DECISION-11).
