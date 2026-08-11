/-!
# Investigation 25 — Core Signature and Generic Theorems
## Balance-as-Intelligence Movement

Authority: `25f_Ratified_Balance_as_Intelligence_Mathematical_Object.md` (semantic authority).
Contract: `25g_Lean4_Formal_Hardening_Specification.md`, `25h_..._Adversarial_Tests.md`.

ENCODING NOTE (see `25_final_encoding_decision_log.md`, DECISION-01): every abstract
primitive type/relation demanded by 25g §2–§17 is bundled as a field of one
`structure Sig`, and all definitions/theorems below take an explicit
`(S : Sig)` argument rather than being declared via free-standing `variable`
binders. This is a pure Lean-engineering choice (a "locale"-style bundling,
standard for large abstract developments) forced by a genuine elaboration
failure: free-standing `variable {K K' : Cut}` binders mixed with several
mutually-dependent relation variables caused unresolvable metavariables in
this Lean version. Bundling changes no mathematics — every field below is
exactly the primitive 25g asks for, under an explicit signature parameter
instead of an implicit section variable. Finite models `M1, M2, M3` in
`Models.lean` all instantiate the **same** `Sig` type (25g §18, §23 clause 3:
"all three finite models use one unchanged semantics").

FAITHFULNESS PATCH (this file, this pass — see `25_final_patch_diff.md` for
the full before/after diff): four semantic corrections relative to the prior
delivered package, none of which broaden Investigation 25 beyond what 25f
§12/§13/§17 already ratifies:
(A) `Stuck` is now `SNSLike ∧ StuckThresholdCrossed`, where
    `StuckThresholdCrossed` is its own named inductive judgment (a distinct
    typed witness, not a bare `Or`) built from the SAME shared trajectory
    primitives 25f §17 already lists — never a "separate detector
    architecture" (25f §17's explicit prohibition) — plus one new primitive,
    `OpportunityFieldUnavailable`, added because 25f §17's prose names
    "inability to see or participate in new opportunities/options" as an
    explicit, independent facet not previously represented by any existing
    field.
(B) `HarmonicAlign` no longer depends on the independent `LawfulAppropriate`
    Sig field. It now requires a genuine `ReadApp`-derived `Appropriateness`
    reading (`Adm25 → ReadApp` load-bearing, per 25f §10/§12). The
    `LawfulAppropriate` Sig field is REMOVED entirely (not merely
    deprecated) — nothing in this file can independently assign it anymore.
    A `LegacyLawfulAppropriate` DERIVED definition (never a Sig field) is
    kept purely so the one M1 narrative theorem that used the old name
    (`T18_pns_high_force_contrast`) keeps making its point, now defined
    *only* in terms of `ReadApp`.
(C) `HarmonicAlign`'s extension clause is now universally quantified over
    every MATERIALLY participating extension (`MaterialExtensionOf`, a new
    Core-level definition mirroring `MaterialTo`'s existing two-part
    materiality discipline: `ExtensionOf ∧ ExtensionDiscriminates`), not a
    single caller-supplied `z`.
(D) `ModelSufficient`'s finite-model encoding is reclassified in the gap
    report from RESOLVED-FAITHFUL-ENCODING to PROVISIONAL-ENCODING. No Lean
    change was required for this correction (documentation-only), and none
    was made.

No axiom is declared anywhere in this development. No `sorry` is used.
-/

namespace Inv25

/-! ## 0. Non-scalar profile carrier (`V`), energetic types, reading kinds

DECISION-02: the profile carrier `V` demanded by 25f §7/§8
(`Rel_K(m) : R_K^mat → V`) is instantiated as this three-valued `Standing`.
25f §23 explicitly lists the exact carrier as provisional/deferred; using a
concrete three-point lattice is a logged, non-hidden choice (see gap
report GAP-02), not a silent resolution — any ordered/richer `V` would
still validate every theorem below verbatim, since nothing but `= full`
is ever inspected.
-/

/-- Standing of a single material relation/distinction under a movement
reading (the carrier `V` of 25f §7–8). Named `partialStanding` (not
`partial`) because `partial` is a reserved keyword in this Lean toolchain
(mechanical fix, not a semantic choice — see build/axiom report). -/
inductive Standing where
  | full
  | partialStanding
  | absent
deriving DecidableEq, Repr

/-- A required floor is met only by `full` standing. This is what makes
floors non-compensatory: the predicate is per-item, so no other item's
`full` standing can substitute for one item's `partialStanding`/`absent`. -/
def MeetsFloor (s : Standing) : Prop := s = Standing.full

instance : DecidablePred MeetsFloor := fun s => by unfold MeetsFloor; infer_instance

/-! Energetic typing (25g §13, 25f §5): five **distinct wrapper types**,
not five aliases of one numeric type. Because each is its own single-field
structure, `ActionEffort ≠ ExcessForcing` holds at the level of Lean's type
checker itself — there is no implicit coercion between them, and no
function below ever accepts one where the other is expected. This is the
strongest available reading of "not definitionally interchangeable"
(25g §13). Unchanged by this patch. -/

structure PhysicalEnergy where val : Nat deriving DecidableEq, Repr
structure RepresentationEffort where val : Nat deriving DecidableEq, Repr
structure ActionEffort where val : Nat deriving DecidableEq, Repr
structure ExcessForcing where val : Nat deriving DecidableEq, Repr
structure Genenergy where val : Nat deriving DecidableEq, Repr

/-- Threshold predicates used by M1's "high action / low forcing" and
"high action / high forcing" contrast (25g §18 M1). The exact numeric
threshold is arbitrary and reported as GAP-06 (no ratified numeric
threshold exists in 25f — `E_force` is explicitly provisional, 25f §5).
Thresholds are used ONLY to compare `ActionEffort`/`ExcessForcing`
magnitudes within one energetic type against itself; they never compare
across the two types and never feed SNS/Stuck (25f §5, §17). Unchanged by
this patch. -/
def HighActionEffort (thresh : Nat) (a : ActionEffort) : Prop := thresh ≤ a.val
def LowExcessForcing (thresh : Nat) (f : ExcessForcing) : Prop := f.val < thresh
def HighExcessForcing (thresh : Nat) (f : ExcessForcing) : Prop := thresh ≤ f.val
def LowActionEffort (thresh : Nat) (a : ActionEffort) : Prop := a.val < thresh

/-- RA4: the output of a lawful `ReadApp` must never be tagged as direct
contact. Kept as an explicit tag on the reading rather than as a separate
untagged type so that "cannot inhabit the direct-contact type" is a
provable field-equation, not merely a type-level accident. Unchanged. -/
inductive ReadingKind where
  | derivedAppropriateness
  | directContact
deriving DecidableEq, Repr

/-! ## 1. The bundled abstract signature -/

/-- `Sig` bundles every primitive type and relation 25g §2 demands, plus
the further primitives required by §3–§17 (Adm24 interface, ReadApp
components, energetics, harmonic alignment, BHC, PNS/SNS/Stuck, interface
change). Every field is either:
* a **type** (25g §2's required primitive-type list), or
* a **primitive judgment/relation** that 25f treats as basic (discrimination,
  provenance, standing, availability, energetics) — Lean cannot manufacture
  witnesses for these; a finite model must supply them directly.

No field below computes Soul standing, HarmonicOutcome, or ModelSufficient
from a model's own internal description — see the strengthening-audit
notes attached to each theorem that consumes these fields.

PATCH NOTE (this pass): `LawfulAppropriate` is REMOVED from this structure
(Correction B — see DECISION-B1/B2 in the decision log; it is no longer an
independently assignable primitive anywhere in this development).
`ExtensionDiscriminates` (Correction C — DECISION-C1) and
`OpportunityFieldUnavailable` (Correction A — DECISION-A2) are ADDED. -/
structure Sig where
  /-- Proto-time cuts. -/
  Cut : Type
  /-- Ambient Soul doctrine (25g §3). Never a DPF/Sig-instance field that a
  movement can freely set — it is the outermost parameter every judgment
  below is indexed by, and nothing in `Sig` below lets a movement assign
  its own Soul standing. Unaffected by this patch. -/
  SoulDoctrine : Type
  Provenance : Type
  GenerationKind : Type
  SemanticEvaluator : Type
  /-- `Movement (K K' : Cut)`, dependent per 25g §2's preferred shape. -/
  Movement : Cut → Cut → Type
  /-- Live typed relations material to a cut (`D_K`, 25f §4.1). -/
  Relation : Cut → Type
  /-- Material distinctions at a cut (`Δ_K`, 25f §8). -/
  Distinction : Cut → Type
  /-- Participation-interface modes at a cut (`I_K`, 25f §4.3/§18). -/
  Mode : Cut → Type
  /-- Recruited extensions (25f §13: body segment, tool, API, ... ). -/
  Extension : Type
  /-- Modeled consequences (`Consequence`, 25g §2). -/
  Consequence : Type
  /-- Candidate world-models `M` used by BHC (25f §14). -/
  WorldModel : Type
  /-- Trajectories, the shared substrate for PNS/SNS/Stuck (25f §15–17). -/
  Trajectory : Type
  --- Movement availability / participation primitives ---
  /-- Movement is available from current relations/interfaces
  (25f §9, first Adm25 conjunct). -/
  Available : ∀ {K K'}, Movement K K' → Prop
  /-- Inherited Investigation-24 legality (25g §9): an **abstract imported
  interface**. Investigation 25 never redefines its internal law — it only
  consumes `Adm24` as an opaque hypothesis/witness. -/
  Adm24 : SoulDoctrine → ∀ {K K'}, Movement K K' → Prop
  --- Materiality primitives (25g §5–6) ---
  /-- `UsedBy m x`: weak, self-certifiable membership only. -/
  UsedByRel : ∀ {K K'}, Movement K K' → Relation K → Prop
  UsedByDist : ∀ {K K'}, Movement K K' → Distinction K → Prop
  /-- `Discriminates_K(x;m)`: the one reusable counterfactual-bite relation
  (25f §4, 25g §5), reused for relations, distinctions, and (in `Models`)
  Fourthness deletion tests. Proposition-valued, never `Bool`. -/
  DiscriminatesRel : ∀ {K K'}, Movement K K' → Relation K → Prop
  DiscriminatesDist : ∀ {K K'}, Movement K K' → Distinction K → Prop
  RelProvenance : ∀ {K}, Relation K → Provenance
  DistProvenance : ∀ {K}, Distinction K → Provenance
  --- Relatedness / Precision profiles (25g §7–8) ---
  relStanding : ∀ {K K'}, Movement K K' → Relation K → Standing
  distStanding : ∀ {K K'}, Movement K K' → Distinction K → Standing
  /-- Membership in the required sets `M_R`/`M_P` (25f §7/§8). -/
  RequiredRel : ∀ {K K'}, Movement K K' → Relation K → Prop
  RequiredDist : ∀ {K K'}, Movement K K' → Distinction K → Prop
  --- Energetics (25g §13, 25f §5) ---
  physicalEnergy : ∀ {K K'}, Movement K K' → PhysicalEnergy
  representationEffort : ∀ {K K'}, Movement K K' → RepresentationEffort
  actionEffort : ∀ {K K'}, Movement K K' → ActionEffort
  excessForcing : ∀ {K K'}, Movement K K' → ExcessForcing
  genenergy : ∀ {K K'}, Movement K K' → Genenergy
  /-- Disqualifying excess-forcing evidence, kept as an explicit Prop
  witness rather than a numeric-threshold derivation of `excessForcing`,
  because 25f §5 explicitly marks the numeric `E_force` metric as
  provisional (GAP-06). -/
  DisqualifyingExcessForcing : ∀ {K K'}, Movement K K' → Prop
  --- Participation openness / consequence answerability (25f §9,§15) ---
  ParticipationOpen : ∀ {K K'}, Movement K K' → Prop
  ConsequenceAnswerable : ∀ {K K'}, Movement K K' → Prop
  --- Extensions (25f §13) ---
  /-- Weak, self-certifiable "is an extension of this movement" membership
  — mirrors `UsedByRel`'s weak role exactly. On its own this NEVER suffices
  for `HarmonicAlign`'s extension-alignment clause (Correction C). -/
  ExtensionOf : Extension → ∀ {K K'}, Movement K K' → Prop
  /-- Counterfactual-discrimination witness for an extension, mirroring
  `DiscriminatesRel`'s role exactly (Correction C, DECISION-C1) — the
  conjunction `ExtensionOf ∧ ExtensionDiscriminates` (`MaterialExtensionOf`
  below) is what makes an extension MATERIALLY participating, never
  `ExtensionOf` alone. -/
  ExtensionDiscriminates : Extension → ∀ {K K'}, Movement K K' → Prop
  AlignedExtension : Extension → ∀ {K K'}, Movement K K' → Prop
  ContinuingContactable : ∀ {K K'}, Movement K K' → Prop
  --- ReadApp components (25g §11) ---
  evaluatorOf : ∀ {K K'}, Movement K K' → SemanticEvaluator
  DoctrineBound : SemanticEvaluator → SoulDoctrine → Prop
  provenanceOfMovement : ∀ {K K'}, Movement K K' → Provenance
  generationKindOf : ∀ {K K'}, Movement K K' → GenerationKind
  --- Consequence / BHC (25f §14) ---
  /-- PATCH NOTE (Correction D): the finite-model encoding of this field
  is reclassified PROVISIONAL-ENCODING in the gap report — it remains an
  abstract external-governance witness here, never derivable from a
  model's own internal self-description (25f §14's explicit "no movement,
  representation, or evaluator may self-certify `ModelSufficient`" law is
  unchanged and unweakened by this patch). -/
  ModelSufficient : WorldModel → ∀ {K K'}, Movement K K' → Prop
  CorrectConsequenceLaw : WorldModel → Prop
  NoOmittedDisturbance : WorldModel → Prop
  ConsequenceOf : WorldModel → ∀ {K K'}, Movement K K' → Consequence → Prop
  HarmonicOutcome : Consequence → ∀ {K K'}, Movement K K' → Prop
  --- PNS-like organization primitives (25f §15, nine witnesses) ---
  Contactability : Trajectory → Prop
  RelationalOpenness : Trajectory → Prop
  PreservedDistinctions : Trajectory → Prop
  ReceptiveAttention : Trajectory → Prop
  DifferentiationWithCoherence : Trajectory → Prop
  LowUnnecessaryForcing : Trajectory → Prop
  TrajConsequenceAnswerable : Trajectory → Prop
  InterfaceOpenness : Trajectory → Prop
  SelfWeavingPlasticity : Trajectory → Prop
  --- Shared SNS/Stuck trajectory primitives (25f §16–17) ---
  ContactExclusion : Trajectory → Prop
  Recurrence : Trajectory → Prop
  InterfaceNarrowing : Trajectory → Prop
  ForcedVelocity : Trajectory → Prop
  StaleForwardMotion : Trajectory → Prop
  PivotUnavailable : Trajectory → Prop
  /-- NEW (Correction A, DECISION-A2): "inability to see or participate in
  new opportunities/options" — 25f §17's own explicit third facet of
  threshold-crossing, not previously represented by any field. Built into
  the SAME shared trajectory-primitive family as `StaleForwardMotion`/
  `PivotUnavailable`, never a disconnected flag. -/
  OpportunityFieldUnavailable : Trajectory → Prop
  ForceResidueEvidence : Trajectory → Prop
  --- Participation-interface change (25g §17) ---
  AvailableAt : ∀ {K}, Mode K → Prop

/-! ## 2. Materiality: `UsedBy` ≠ `MaterialTo` (25g §6, T04) -/

/-- A relation is material to a movement only when it is used **and**
carries a genuine counterfactual-discrimination witness (25f §6: "requires
explicit provenance ... and a counterfactual discrimination witness").
`MaterialTo` is *defined* as this conjunction precisely so `UsedBy` alone
can never establish it. -/
def MaterialTo (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (x : S.Relation K) : Prop :=
  S.UsedByRel m x ∧ S.DiscriminatesRel m x

def MaterialToDist (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (d : S.Distinction K) : Prop :=
  S.UsedByDist m d ∧ S.DiscriminatesDist m d

/-- NEW (Correction C, DECISION-C1): the SAME two-part materiality
discipline lifted verbatim to extensions — an extension is materially
participating in a movement only when it is (weakly) an extension of it
**and** carries a genuine counterfactual-discrimination witness for it.
`ExtensionOf` alone can never establish this, exactly mirroring `MaterialTo`
above. This is what "not self-certified" means here: no field of `Sig`
lets `MaterialExtensionOf` be assigned directly, it is always this derived
conjunction. -/
def MaterialExtensionOf (S : Sig) (z : S.Extension) {K K' : S.Cut} (m : S.Movement K K') : Prop :=
  S.ExtensionOf z m ∧ S.ExtensionDiscriminates z m

/-- T04 `materiality_not_from_use_alone`: there is no proof term of
`UsedBy m x → MaterialTo m x` in general — a purported proof of the
conjunction's right conjunct would have to be conjured from nothing.
Concretely: from `UsedBy m x` alone, `DiscriminatesRel m x` is never
derivable (it is an independent Sig field), so the conjunction
`MaterialTo` cannot be closed. The countermodel exhibiting a genuine
`UsedByRel`-without-`DiscriminatesRel` witness (so that the implication
provably FAILS, not merely "is not proved here") is built in `Models.lean`
(`m2_materiality_adversary`). -/
theorem materiality_not_from_use_alone_soundness
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (x : S.Relation K) :
    MaterialTo S m x → S.UsedByRel m x ∧ S.DiscriminatesRel m x := id

/-- Extension analogue of T04's soundness direction, for the same reason
`MaterialExtensionOf` is a conjunction and not a raw field. -/
theorem extension_materiality_not_from_use_alone_soundness
    (S : Sig) (z : S.Extension) {K K' : S.Cut} (m : S.Movement K K') :
    MaterialExtensionOf S z m → S.ExtensionOf z m ∧ S.ExtensionDiscriminates z m := id

/-! ## 3. Relatedness / Precision floors (25g §7–8, T05/T06) -/

def RelFloor (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (r : S.Relation K) : Prop :=
  S.RequiredRel m r → MeetsFloor (S.relStanding m r)

def PrecFloor (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (d : S.Distinction K) : Prop :=
  S.RequiredDist m d → MeetsFloor (S.distStanding m d)

def AllRelFloors (S : Sig) {K K' : S.Cut} (m : S.Movement K K') : Prop :=
  ∀ r : S.Relation K, RelFloor S m r

def AllPrecFloors (S : Sig) {K K' : S.Cut} (m : S.Movement K K') : Prop :=
  ∀ d : S.Distinction K, PrecFloor S m d

/-- T05 `rel_floor_noncompensatory`: if some required relation `r₂` fails
its floor, `AllRelFloors` cannot hold — regardless of how strong any other
relation `r₁` is. Because `AllRelFloors` is a per-relation universal
statement (not an average), one failing required witness blocks the whole
conjunction unconditionally. Unaffected by this patch. -/
theorem rel_floor_noncompensatory
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (r₁ r₂ : S.Relation K)
    (_hr1full : S.relStanding m r₁ = Standing.full)
    (hreq2 : S.RequiredRel m r₂) (hfail2 : S.relStanding m r₂ ≠ Standing.full) :
    ¬ AllRelFloors S m := fun hall => hfail2 (hall r₂ hreq2)

/-- T06 `prec_floor_noncompensatory`, the Precision analogue. Unaffected
by this patch. -/
theorem prec_floor_noncompensatory
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (d₁ d₂ : S.Distinction K)
    (_hd1full : S.distStanding m d₁ = Standing.full)
    (hreq2 : S.RequiredDist m d₂) (hfail2 : S.distStanding m d₂ ≠ Standing.full) :
    ¬ AllPrecFloors S m := fun hall => hfail2 (hall d₂ hreq2)

/-! ## 4. Investigation-25 admissibility (25g §10) -/

/-- `Adm25Witness` is a proof-relevant conjunction of the exact seven
clauses 25f §9 / 25g §10 lists — never a single `isAppropriate : Bool`.
Each field is named so it can be projected individually by `ReadApp`'s
laws (RA1, RA5, RA6 below). Unaffected by this patch. -/
structure Adm25Witness (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') : Prop where
  available : S.Available m
  adm24 : S.Adm24 Sd m
  relFloors : AllRelFloors S m
  precFloors : AllPrecFloors S m
  noDisqualifyingForcing : ¬ S.DisqualifyingExcessForcing m
  participationOpen : S.ParticipationOpen m
  consequenceAnswerable : S.ConsequenceAnswerable m

/-! ## 5. `ReadApp` (25g §11) -/

/-- A lawful Appropriateness reading. Carries the RA3 provenance/kind
data and the RA4 kind-tag as *stored fields*, not as ambient side facts,
so RA3/RA4 are checkable projections of any actual reading. Unaffected
by this patch. -/
structure Appropriateness (S : Sig) {K K' : S.Cut} (m : S.Movement K K') where
  prov : S.Provenance
  gen : S.GenerationKind
  kind : ReadingKind
  /-- RA2: source identity — this reading is *for* `m`, enforced by `m`
  appearing in the very index of the structure (no separate `src` field
  can silently diverge from it). -/
  srcIsM : True := trivial

/-- RA1, RA2, RA3, RA4, RA5, RA6, RA8 as one inductive judgment (25g §11's
"inductive judgment" option). The single constructor is the ONLY way to
produce an `Appropriateness` reading, and it demands:
* `adm : Adm25Witness S Sd m` — RA1 (no reading without an Adm25 witness);
  its `relFloors`/`precFloors` fields ALREADY force `AllRelFloors`/
  `AllPrecFloors`, so RA5/RA6 (floor failure blocks a fully appropriate
  reading) are consequences of RA1, not duplicated laws;
* the reading is indexed by `m` itself — RA2;
* `ev : DoctrineBound (evaluatorOf m) Sd` — RA8 (the evaluator seam is
  doctrine-bound, never free-floating authority);
and it always produces `kind := derivedAppropriateness` — RA4, since no
constructor argument lets the caller choose `directContact`.
RA7 (no scalar override) is a *negative* / API-shape guarantee: this is
the only constructor in the whole file that produces `Appropriateness`,
and none of its hypotheses is a scalar aggregate — verified in
`Models.lean`'s `no_scalar_override` countermodel, which exhibits a
movement with a high ad-hoc "summary score" that still cannot be turned
into a `ReadApp` witness once a required floor fails.

THIS JUDGMENT IS NOW LOAD-BEARING FOR `HarmonicAlign` (Correction B) —
it is no longer merely one of several ways to reach appropriateness;
`ReadApp` is the *only* path `HarmonicAlign` accepts. Unaffected in its
own internal content by this patch. -/
inductive ReadApp (S : Sig) (Sd : S.SoulDoctrine) :
    ∀ {K K' : S.Cut} (m : S.Movement K K'), Appropriateness S m → Prop where
  | mk {K K' : S.Cut} (m : S.Movement K K') (adm : Adm25Witness S Sd m)
      (ev : S.DoctrineBound (S.evaluatorOf m) Sd) :
      ReadApp S Sd m
        { prov := S.provenanceOfMovement m
        , gen := S.generationKindOf m
        , kind := ReadingKind.derivedAppropriateness }

/-- T07 `readapp_requires_adm`: any `ReadApp` witness yields an
`Adm25Witness`. Unaffected by this patch. -/
theorem readapp_requires_adm (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (A : Appropriateness S m) (h : ReadApp S Sd m A) :
    Nonempty (Adm25Witness S Sd m) := by
  cases h with
  | mk adm _ => exact ⟨adm⟩

/-- T08 `readapp_no_contact_masquerade`: a lawful reading is never tagged
`directContact`. Unaffected by this patch. -/
theorem readapp_no_contact_masquerade (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (A : Appropriateness S m) (h : ReadApp S Sd m A) :
    A.kind ≠ ReadingKind.directContact := by
  cases h with
  | mk _ _ => simp

/-- T09 `readapp_rel_floor`: if a required Relatedness floor fails,
no `ReadApp` witness exists for `m`. Unaffected by this patch. -/
theorem readapp_rel_floor (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (hfail : ¬ AllRelFloors S m) :
    ∀ A, ¬ ReadApp S Sd m A := by
  intro A h
  cases h with
  | mk adm _ => exact hfail adm.relFloors

/-- T10 `readapp_prec_floor`, the Precision analogue. Unaffected by this
patch. -/
theorem readapp_prec_floor (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (hfail : ¬ AllPrecFloors S m) :
    ∀ A, ¬ ReadApp S Sd m A := by
  intro A h
  cases h with
  | mk adm _ => exact hfail adm.precFloors

/-- T01 `source_identity_rel`: `RelatednessProfile`-shaped readings
(`relStanding`) are indexed by `m` in their very type signature — there is
no free-standing `Relatedness` value un-attached to a movement, so its
source cannot diverge from `m`. Stated as the definitional fact that the
profile function IS `S.relStanding m`. Unaffected by this patch. -/
theorem source_identity_rel (S : Sig) {K K' : S.Cut} (m : S.Movement K K') :
    (fun r => S.relStanding m r) = S.relStanding m := rfl

/-- T02 `source_identity_app`: the `Appropriateness` reading produced by
`ReadApp` is indexed by exactly the movement `m` supplied to it — `src` is
not a separately settable field. Unaffected by this patch. -/
theorem source_identity_app (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (A : Appropriateness S m) (_h : ReadApp S Sd m A) :
    (A : Appropriateness S m) = A := rfl

/-- T03 `source_identity_prec`, the Precision analogue of T01. Unaffected
by this patch. -/
theorem source_identity_prec (S : Sig) {K K' : S.Cut} (m : S.Movement K K') :
    (fun d => S.distStanding m d) = S.distStanding m := rfl

/-- T11 `no_scalar_override`: for ANY function `score` on movements
whatsoever (standing for every possible scalar/weighted/reward/confidence/
genenergy aggregate — the universal quantifier over `score` means this
covers every such function, not just one named guess), a failing required
Relatedness floor still blocks every `ReadApp` witness. No `score` value,
however high, appears anywhere in `ReadApp`'s single constructor, so none
can override RA5/RA6. Unaffected by this patch. -/
theorem no_scalar_override (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (score : ∀ {K K' : S.Cut}, S.Movement K K' → Nat)
    (_hscore_high : score m = 1000000) (hfail : ¬ AllRelFloors S m) :
    ∀ A, ¬ ReadApp S Sd m A :=
  readapp_rel_floor S Sd m hfail

/-- A `ReadApp` reading is `FullyAppropriate` when it carries the ONE
kind `ReadApp`'s constructor ever produces (`derivedAppropriateness`).
Since `ReadApp`'s single constructor always sets `kind :=
derivedAppropriateness` (T08 above), any actual `ReadApp` witness is
automatically `FullyAppropriate` — this definition exists so
`HarmonicAlign` below states the requirement explicitly (per the user's
suggested sketch `Adm25Witness ∧ ReadApp ∧ FullyAppropriate`) rather than
leaving it as an unstated corollary. -/
def FullyAppropriate (S : Sig) {K K' : S.Cut} {m : S.Movement K K'}
    (A : Appropriateness S m) : Prop :=
  A.kind = ReadingKind.derivedAppropriateness

/-- Any `ReadApp`-derived reading is automatically `FullyAppropriate` —
restates T08 in `FullyAppropriate`'s vocabulary. -/
theorem readapp_fully_appropriate (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (A : Appropriateness S m) (h : ReadApp S Sd m A) :
    FullyAppropriate S A := by
  cases h with
  | mk _ _ => rfl

/-- DECISION-B2: `LegacyLawfulAppropriate` is kept ONLY as a derived,
ReadApp-sourced definition — never again an independently assignable
`Sig` field. It exists purely so `Models.lean`'s `T18_pns_high_force_contrast`
narrative theorem (which historically referenced the old field name) keeps
making its point under the new signature. By construction it CANNOT
diverge from ReadApp-derivability, closing the mismatch discovered in the
previous package (see `25_final_encoding_decision_log.md`, DECISION-B2):
under the OLD encoding, `LawfulAppropriate` was `True` by default pattern
for movements whose Rel/Prec floors already failed, even though no
`ReadApp`/`Adm25Witness` could ever exist for them — a genuine faithfulness
bug, not a stylistic nit. -/
def LegacyLawfulAppropriate (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') : Prop :=
  ∃ A : Appropriateness S m, ReadApp S Sd m A

/-! ## 6. Harmonic alignment (25g §14, T14/T15) — CORRECTED (B, C)

PATCH NOTE: `HarmonicAlign` is redesigned per Corrections B and C.

Correction B: the old `S.LawfulAppropriate m` conjunct (an independently
assignable, self-certifiable `Sig` field — the exact anti-pattern 25f §10/
§12 and §10's source-audit list forbid) is REPLACED by an existential
requiring a genuine `ReadApp`-derived, `FullyAppropriate` reading. Since
`ReadApp`'s only constructor demands an `Adm25Witness` (RA1) and a
doctrine-bound evaluator (RA8), this closes the ratified path
`Adm25 → ReadApp ⇓ A_m` directly into `HarmonicAlign`'s own definition —
it is now structurally impossible to construct `HarmonicAlign` using an
arbitrary Appropriateness label with no ReadApp provenance (see
`harmonic_align_requires_readapp_provenance` below).

Correction C: the old single-caller-supplied-`z` conjunct
(`S.ExtensionOf z m → S.AlignedExtension z m`, vacuously true whenever the
caller happens to supply a `z` that is not `ExtensionOf` at all) is
REPLACED by a universal statement over every MATERIALLY participating
extension (`MaterialExtensionOf`, §2 above) — `HarmonicAlign` no longer
takes an extension parameter at all, since the requirement is now
self-contained: EVERY material extension of `m` must be an
`AlignedExtension` of `m`.

`HarmonicAlign` is now indexed by an explicit `Sd : S.SoulDoctrine`
(needed to state the `ReadApp` existential) in addition to `S` and `m`.
It remains *derived* — a conjunction of six independently witnessed
conditions — never a DPF/Sig field and never a weighted R/A/P scalar.
Conjunct POSITIONS are preserved from the prior package (only conjunct
CONTENT at positions 2 and 5 changed), so `T14`'s `h.1` projection and
`T15`'s `h.2.2.1` projection remain valid unchanged. -/
def HarmonicAlign (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') : Prop :=
  AllRelFloors S m ∧
  (∃ A : Appropriateness S m, ReadApp S Sd m A ∧ FullyAppropriate S A) ∧
  AllPrecFloors S m ∧
  ¬ S.DisqualifyingExcessForcing m ∧
  (∀ z : S.Extension, MaterialExtensionOf S z m → S.AlignedExtension z m) ∧
  S.ContinuingContactable m

/-- T14 `harmonic_alignment_requires_rel_floors`: `HarmonicAlign` entails
`AllRelFloors`, hence a failing required Relatedness floor makes
`HarmonicAlign` unconstructible (mirrors the Relatedness non-compensation
adversary, 25h §3, at the harmonic-alignment level). Projection position
unchanged by this patch (`h.1`). -/
theorem harmonic_alignment_requires_rel_floors
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K') :
    HarmonicAlign S Sd m → AllRelFloors S m := fun h => h.1

/-- T15 `harmonic_alignment_requires_prec_floors`, the Precision analogue.
Projection position unchanged by this patch (`h.2.2.1`). -/
theorem harmonic_alignment_requires_prec_floors
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K') :
    HarmonicAlign S Sd m → AllPrecFloors S m := fun h => h.2.2.1

/-- Relatedness non-compensation lifted to `HarmonicAlign` (25h §3): if a
required relation fails, `HarmonicAlign` cannot be constructed no matter
how strong other relations are — this does not depend on any arithmetic
averaging, since `HarmonicAlign` never mentions a numeric aggregate.
Unaffected in its proof shape by this patch (still uses `h.1`). -/
theorem harmonic_align_rel_noncompensatory
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K')
    (r₁ r₂ : S.Relation K) (h1full : S.relStanding m r₁ = Standing.full)
    (hreq2 : S.RequiredRel m r₂) (hfail2 : S.relStanding m r₂ ≠ Standing.full) :
    ¬ HarmonicAlign S Sd m :=
  fun h => rel_floor_noncompensatory S m r₁ r₂ h1full hreq2 hfail2 h.1

/-- N01 `N01_harmonic_align_requires_adm25`: `HarmonicAlign` entails the
existence of an `Adm25Witness` — extracted from the load-bearing `ReadApp`
conjunct via `readapp_requires_adm` (T07). This is the formal statement
that the ratified path `Adm25 → ReadApp` is now load-bearing for harmonic
alignment, not merely available as one option among several. -/
theorem N01_harmonic_align_requires_adm25
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K') :
    HarmonicAlign S Sd m → Nonempty (Adm25Witness S Sd m) := by
  intro h
  obtain ⟨A, hApp, _⟩ := h.2.1
  exact readapp_requires_adm S Sd m A hApp

/-- N02 `N02_harmonic_align_requires_readapp`: `HarmonicAlign` entails the
existence of a genuine `ReadApp`-derived, `FullyAppropriate` reading —
direct projection of `HarmonicAlign`'s own second conjunct, stated as its
own named theorem per the user's explicit obligation list. -/
theorem N02_harmonic_align_requires_readapp
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K') :
    HarmonicAlign S Sd m →
      ∃ A : Appropriateness S m, ReadApp S Sd m A ∧ FullyAppropriate S A :=
  fun h => h.2.1

/-- N03 `N03_harmonic_align_material_extension_universal`: `HarmonicAlign`
entails that EVERY materially participating extension is an
`AlignedExtension` — direct projection of the universally-quantified fifth
conjunct (Correction C). -/
theorem N03_harmonic_align_material_extension_universal
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K') :
    HarmonicAlign S Sd m →
      ∀ z : S.Extension, MaterialExtensionOf S z m → S.AlignedExtension z m :=
  fun h => h.2.2.2.2.1

/-- Companion to N01/N02: `HarmonicAlign` is unconstructible when NO
`ReadApp` witness exists for `m` at all — the formal guarantee that
`HarmonicAlign` cannot be built "using an arbitrary Appropriateness label
with no ReadApp provenance" (explicit user obligation under Correction B).
Since the only way to inhabit the second conjunct is to supply an actual
`ReadApp S Sd m A` proof, the complete absence of such proofs blocks the
conjunction outright. -/
theorem harmonic_align_requires_readapp_provenance
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K')
    (hnone : ∀ A, ¬ ReadApp S Sd m A) :
    ¬ HarmonicAlign S Sd m := by
  intro h
  obtain ⟨A, hApp, _⟩ := h.2.1
  exact hnone A hApp

/-- `HarmonicAlign` is also unconstructible when a required Precision
floor fails — direct corollary of T15/`prec_floor_noncompensatory`,
stated explicitly since Correction B/C's redesign changed the shape of
the surrounding conjunction. -/
theorem harmonic_align_prec_noncompensatory
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K')
    (d₁ d₂ : S.Distinction K) (h1full : S.distStanding m d₁ = Standing.full)
    (hreq2 : S.RequiredDist m d₂) (hfail2 : S.distStanding m d₂ ≠ Standing.full) :
    ¬ HarmonicAlign S Sd m :=
  fun h => prec_floor_noncompensatory S m d₁ d₂ h1full hreq2 hfail2 h.2.2.1

/-! ## 7. Bounded Harmonic Continuation (25g §15, T16/T17)

PATCH NOTE: T16/T17 are re-stated against the new `HarmonicAlign S Sd m`
signature (drops the caller-supplied `z`, adds the `Sd` parameter the new
definition requires). No mathematical content changes: `HarmonicAlign`
is still supplied as one opaque premise among five, and the schema/
falsifier logic is untouched — only the type of the `halign` premise
changed shape to match Corrections B/C. -/

/-- T16 `bounded_harmonic_continuation`: the forward coherence/soundness
schema, exactly as 25f §14 states it. This is a schema (a conditional),
never marketed as an unconditional prediction — its four hypotheses are
genuine premises that a finite model must independently discharge, never
definitionally guaranteed. -/
theorem bounded_harmonic_continuation
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K')
    (M : S.WorldModel) (o : S.Consequence)
    (hsuff : S.ModelSufficient M m)
    (halign : HarmonicAlign S Sd m)
    (hlaw : S.CorrectConsequenceLaw M)
    (hnodist : S.NoOmittedDisturbance M)
    (hcons : S.ConsequenceOf M m o) :
    -- The forward schema as stated in 25f §14 concludes `HarmonicOutcome`.
    -- Lean cannot derive `HarmonicOutcome` from the other four premises
    -- without ALSO being told the schema's own conditional connects them —
    -- so this connecting fact is the fifth, explicit hypothesis below
    -- (`hschema`), matching 25g §15's requirement that BHC be an
    -- assumption-bearing coherence schema, not a theorem conjured from
    -- weaker premises. See GAP-08 in the gap report for why this
    -- connecting premise cannot be proved from `Sig` alone.
    (S.ModelSufficient M m → HarmonicAlign S Sd m → S.CorrectConsequenceLaw M →
      S.NoOmittedDisturbance M → S.ConsequenceOf M m o → S.HarmonicOutcome o m) →
    S.HarmonicOutcome o m :=
  fun hschema => hschema hsuff halign hlaw hnodist hcons

/-- T17 `nonharmonic_falsifier`: the operational falsifier is the exact
contrapositive of the schema clause above, and — as 25g §15 requires —
IS proved by ordinary logic from the forward schema rather than postulated
independently. -/
theorem nonharmonic_falsifier
    (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut} (m : S.Movement K K')
    (M : S.WorldModel) (o : S.Consequence)
    (hschema : S.ModelSufficient M m → HarmonicAlign S Sd m → S.CorrectConsequenceLaw M →
      S.NoOmittedDisturbance M → S.ConsequenceOf M m o → S.HarmonicOutcome o m)
    (hnonharmonic : ¬ S.HarmonicOutcome o m) :
    ¬ (S.ModelSufficient M m ∧ HarmonicAlign S Sd m ∧ S.CorrectConsequenceLaw M ∧
        S.NoOmittedDisturbance M ∧ S.ConsequenceOf M m o) := by
  intro ⟨hsuff, halign, hlaw, hnodist, hcons⟩
  exact hnonharmonic (hschema hsuff halign hlaw hnodist hcons)

/-! ## 8. PNS-like, SNS-like, Stuck (25g §16, 25f §15–17) — CORRECTED (A) -/

/-- `PNSLike`: conjunction of all nine witnesses 25f §15 lists. Unaffected
by this patch. -/
def PNSLike (S : Sig) (τ : S.Trajectory) : Prop :=
  S.Contactability τ ∧ S.RelationalOpenness τ ∧ S.PreservedDistinctions τ ∧
  S.ReceptiveAttention τ ∧ S.DifferentiationWithCoherence τ ∧
  S.LowUnnecessaryForcing τ ∧ S.TrajConsequenceAnswerable τ ∧
  S.InterfaceOpenness τ ∧ S.SelfWeavingPlasticity τ

/-- `HoldingApart`: one of the "possible witnesses" 25f §16 lists for the
"holding apart" half of SNS-like organization (contact exclusion,
frame/topology persistence, or interface narrowing — any one suffices,
since 25f presents these as alternative possible witnesses, not a
required conjunction). Unaffected by this patch. -/
def HoldingApart (S : Sig) (τ : S.Trajectory) : Prop :=
  S.ContactExclusion τ ∨ S.Recurrence τ ∨ S.InterfaceNarrowing τ

/-- `SNSLike`: the ratified core pattern of 25f §16 — "holding apart" +
"forced velocity toward an imposed elsewhere". Unaffected by this patch —
`Stuck` below is redesigned to still be built ONLY on top of this SAME
definition and the SAME shared trajectory primitives, never a parallel
detector. -/
def SNSLike (S : Sig) (τ : S.Trajectory) : Prop :=
  HoldingApart S τ ∧ S.ForcedVelocity τ

/-- NEW (Correction A, DECISION-A1): a distinct TYPED witness for 25f
§17's "threshold crossing", replacing the prior bare `Or` of two
Props. One constructor per NAMED facet 25f §17's prose lists: staleness
of forward motion; pivot unavailability; and (newly represented, see
Sig's `OpportunityFieldUnavailable`) inability to see/participate in new
opportunities. This is still built from the SAME shared trajectory
primitives `SNSLike` itself consumes (`S.StaleForwardMotion`,
`S.PivotUnavailable`, `S.OpportunityFieldUnavailable`) — 25f §17 is
explicit that "SNSLike and Stuck share the same underlying trajectory
primitives ... They are not separate detector architectures", so this
inductive is deliberately NOT a fresh opaque flag but a named judgment
over fields already declared for trajectory-level reasoning. Only ONE
constructor need apply (the disjunctive reading of 25f §17's "or"), never
all three conjunctively — matching the explicit instruction not to force
conjunctive witnesses. -/
inductive StuckThresholdWitness (S : Sig) (τ : S.Trajectory) : Prop where
  | staleForwardMotion (h : S.StaleForwardMotion τ)
  | pivotUnavailable (h : S.PivotUnavailable τ)
  | opportunityFieldUnavailable (h : S.OpportunityFieldUnavailable τ)

/-- `StuckThresholdCrossed` is exactly `StuckThresholdWitness` under its
ratified name (25f §17's "volume crosses a threshold"), kept as a
separate `def` (rather than inlining the inductive's name everywhere) so
the decision log has one clean name to point at for DECISION-A1/A3. -/
def StuckThresholdCrossed (S : Sig) (τ : S.Trajectory) : Prop :=
  StuckThresholdWitness S τ

/-- `Stuck` (Correction A, DECISION-A3): SNS-like organization whose
volume has ALSO crossed the functional threshold of 25f §17, encoded as
the conjunction of `SNSLike` with the new typed `StuckThresholdCrossed`
witness — never a second, unrelated Boolean label, and never a separate
ontology from SNS (both conjuncts are stated over the exact same
`τ : S.Trajectory` using the exact same shared primitives). -/
def Stuck (S : Sig) (τ : S.Trajectory) : Prop :=
  SNSLike S τ ∧ StuckThresholdCrossed S τ

/-- T13 `stuck_implies_sns`: `Stuck → SNSLike`, WITHOUT the converse
(no lemma of the shape `SNSLike → Stuck` exists anywhere in this
development — see `Models.lean`'s `t_low`/`T_adv15_tLow` witness for a
concrete countermodel to the converse). Unaffected in its proof shape by
this patch (still `h.1`). -/
theorem stuck_implies_sns (S : Sig) (τ : S.Trajectory) : Stuck S τ → SNSLike S τ :=
  fun h => h.1

/-- N05 `N05_stuck_implies_sns`: restates T13 under its new required name
(the user's obligation list names this theorem `N05` explicitly; it is
the identical fact, not a new proof). -/
theorem N05_stuck_implies_sns (S : Sig) (τ : S.Trajectory) : Stuck S τ → SNSLike S τ :=
  stuck_implies_sns S τ

/-! ## 9. Participation-interface change (25g §17) -/

/-- `InterfaceChange K K'`: distinguishes a mode newly available at `K'`
from a mode that was ALREADY available at `K` (25g §17's explicit
requirement not to conflate "new mode after transition" with "all modes
pre-authorized as available"). A genuine interface change exhibits a mode
available at `K'` that provably was not available at `K`. Unaffected by
this patch. -/
def InterfaceChange (S : Sig) {K K' : S.Cut} (modeAtK : S.Mode K) (modeAtK' : S.Mode K') : Prop :=
  ¬ S.AvailableAt modeAtK ∧ S.AvailableAt modeAtK'

end Inv25
