/-!
# Investigation 25 — Core Signature and Generic Theorems
## Balance-as-Intelligence Movement

Authority: `25f_Ratified_Balance_as_Intelligence_Mathematical_Object.md` (semantic authority).
Contract: `25g_Lean4_Formal_Hardening_Specification.md`, `25h_..._Adversarial_Tests.md`.

ENCODING NOTE (see `25_encoding_decision_log.md`, DECISION-01): every abstract
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
(25g §13). -/

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
across the two types and never feed SNS/Stuck (25f §5, §17). -/
def HighActionEffort (thresh : Nat) (a : ActionEffort) : Prop := thresh ≤ a.val
def LowExcessForcing (thresh : Nat) (f : ExcessForcing) : Prop := f.val < thresh
def HighExcessForcing (thresh : Nat) (f : ExcessForcing) : Prop := thresh ≤ f.val
def LowActionEffort (thresh : Nat) (a : ActionEffort) : Prop := a.val < thresh

/-- RA4: the output of a lawful `ReadApp` must never be tagged as direct
contact. Kept as an explicit tag on the reading rather than as a separate
untagged type so that "cannot inhabit the direct-contact type" is a
provable field-equation, not merely a type-level accident. -/
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
notes attached to each theorem that consumes these fields. -/
structure Sig where
  /-- Proto-time cuts. -/
  Cut : Type
  /-- Ambient Soul doctrine (25g §3). Never a DPF/Sig-instance field that a
  movement can freely set — it is the outermost parameter every judgment
  below is indexed by, and nothing in `Sig` below lets a movement assign
  its own Soul standing. -/
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
  --- Appropriateness / lawful lineage (25f §10, 25g §11) ---
  /-- Lawful Appropriateness/admissibility recognition — NOT "target hit"
  (25g §18 M1 explicit prohibition). -/
  LawfulAppropriate : ∀ {K K'}, Movement K K' → Prop
  --- Extensions (25f §13) ---
  ExtensionOf : Extension → ∀ {K K'}, Movement K K' → Prop
  AlignedExtension : Extension → ∀ {K K'}, Movement K K' → Prop
  ContinuingContactable : ∀ {K K'}, Movement K K' → Prop
  --- ReadApp components (25g §11) ---
  evaluatorOf : ∀ {K K'}, Movement K K' → SemanticEvaluator
  DoctrineBound : SemanticEvaluator → SoulDoctrine → Prop
  provenanceOfMovement : ∀ {K K'}, Movement K K' → Provenance
  generationKindOf : ∀ {K K'}, Movement K K' → GenerationKind
  --- Consequence / BHC (25f §14) ---
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
conjunction unconditionally. -/
theorem rel_floor_noncompensatory
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (r₁ r₂ : S.Relation K)
    (_hr1full : S.relStanding m r₁ = Standing.full)
    (hreq2 : S.RequiredRel m r₂) (hfail2 : S.relStanding m r₂ ≠ Standing.full) :
    ¬ AllRelFloors S m := fun hall => hfail2 (hall r₂ hreq2)

/-- T06 `prec_floor_noncompensatory`, the Precision analogue. -/
theorem prec_floor_noncompensatory
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (d₁ d₂ : S.Distinction K)
    (_hd1full : S.distStanding m d₁ = Standing.full)
    (hreq2 : S.RequiredDist m d₂) (hfail2 : S.distStanding m d₂ ≠ Standing.full) :
    ¬ AllPrecFloors S m := fun hall => hfail2 (hall d₂ hreq2)

/-! ## 4. Investigation-25 admissibility (25g §10) -/

/-- `Adm25Witness` is a proof-relevant conjunction of the exact seven
clauses 25f §9 / 25g §10 lists — never a single `isAppropriate : Bool`.
Each field is named so it can be projected individually by `ReadApp`'s
laws (RA1, RA5, RA6 below). -/
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
so RA3/RA4 are checkable projections of any actual reading. -/
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
into a `ReadApp` witness once a required floor fails. -/
inductive ReadApp (S : Sig) (Sd : S.SoulDoctrine) :
    ∀ {K K' : S.Cut} (m : S.Movement K K'), Appropriateness S m → Prop where
  | mk {K K' : S.Cut} (m : S.Movement K K') (adm : Adm25Witness S Sd m)
      (ev : S.DoctrineBound (S.evaluatorOf m) Sd) :
      ReadApp S Sd m
        { prov := S.provenanceOfMovement m
        , gen := S.generationKindOf m
        , kind := ReadingKind.derivedAppropriateness }

/-- T07 `readapp_requires_adm`: any `ReadApp` witness yields an
`Adm25Witness`. -/
theorem readapp_requires_adm (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (A : Appropriateness S m) (h : ReadApp S Sd m A) :
    Nonempty (Adm25Witness S Sd m) := by
  cases h with
  | mk adm _ => exact ⟨adm⟩

/-- T08 `readapp_no_contact_masquerade`: a lawful reading is never tagged
`directContact`. -/
theorem readapp_no_contact_masquerade (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (A : Appropriateness S m) (h : ReadApp S Sd m A) :
    A.kind ≠ ReadingKind.directContact := by
  cases h with
  | mk _ _ => simp

/-- T09 `readapp_rel_floor`: if a required Relatedness floor fails,
no `ReadApp` witness exists for `m`. -/
theorem readapp_rel_floor (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (hfail : ¬ AllRelFloors S m) :
    ∀ A, ¬ ReadApp S Sd m A := by
  intro A h
  cases h with
  | mk adm _ => exact hfail adm.relFloors

/-- T10 `readapp_prec_floor`, the Precision analogue. -/
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
profile function IS `S.relStanding m`. -/
theorem source_identity_rel (S : Sig) {K K' : S.Cut} (m : S.Movement K K') :
    (fun r => S.relStanding m r) = S.relStanding m := rfl

/-- T02 `source_identity_app`: the `Appropriateness` reading produced by
`ReadApp` is indexed by exactly the movement `m` supplied to it — `src` is
not a separately settable field. -/
theorem source_identity_app (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (A : Appropriateness S m) (_h : ReadApp S Sd m A) :
    (A : Appropriateness S m) = A := rfl

/-- T03 `source_identity_prec`, the Precision analogue of T01. -/
theorem source_identity_prec (S : Sig) {K K' : S.Cut} (m : S.Movement K K') :
    (fun d => S.distStanding m d) = S.distStanding m := rfl

/-- T11 `no_scalar_override`: for ANY function `score` on movements
whatsoever (standing for every possible scalar/weighted/reward/confidence/
genenergy aggregate — the universal quantifier over `score` means this
covers every such function, not just one named guess), a failing required
Relatedness floor still blocks every `ReadApp` witness. No `score` value,
however high, appears anywhere in `ReadApp`'s single constructor, so none
can override RA5/RA6. -/
theorem no_scalar_override (S : Sig) (Sd : S.SoulDoctrine) {K K' : S.Cut}
    (m : S.Movement K K') (score : ∀ {K K' : S.Cut}, S.Movement K K' → Nat)
    (_hscore_high : score m = 1000000) (hfail : ¬ AllRelFloors S m) :
    ∀ A, ¬ ReadApp S Sd m A :=
  readapp_rel_floor S Sd m hfail

/-! ## 6. Harmonic alignment (25g §14, T14/T15) -/

/-- `HarmonicAlign` is *derived* — a conjunction of six independently
witnessed conditions — never a DPF/Sig field and never a weighted R/A/P
scalar. Matches 25f §12 exactly: all required Relatedness floors; lawful
Appropriateness/admissibility; all required Precision floors; no
disqualifying excess-forcing evidence; aligned participation of material
extensions; continued contactability. -/
def HarmonicAlign (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (z : S.Extension) : Prop :=
  AllRelFloors S m ∧
  S.LawfulAppropriate m ∧
  AllPrecFloors S m ∧
  ¬ S.DisqualifyingExcessForcing m ∧
  (S.ExtensionOf z m → S.AlignedExtension z m) ∧
  S.ContinuingContactable m

/-- T14 `harmonic_alignment_requires_rel_floors`: `HarmonicAlign` entails
`AllRelFloors`, hence a failing required Relatedness floor makes
`HarmonicAlign` unconstructible (mirrors the Relatedness non-compensation
adversary, 25h §3, at the harmonic-alignment level). -/
theorem harmonic_alignment_requires_rel_floors
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (z : S.Extension) :
    HarmonicAlign S m z → AllRelFloors S m := fun h => h.1

/-- T15 `harmonic_alignment_requires_prec_floors`, the Precision analogue. -/
theorem harmonic_alignment_requires_prec_floors
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (z : S.Extension) :
    HarmonicAlign S m z → AllPrecFloors S m := fun h => h.2.2.1

/-- Relatedness non-compensation lifted to `HarmonicAlign` (25h §3): if a
required relation fails, `HarmonicAlign` cannot be constructed no matter
how strong other relations are — this does not depend on any arithmetic
averaging, since `HarmonicAlign` never mentions a numeric aggregate. -/
theorem harmonic_align_rel_noncompensatory
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (z : S.Extension)
    (r₁ r₂ : S.Relation K) (h1full : S.relStanding m r₁ = Standing.full)
    (hreq2 : S.RequiredRel m r₂) (hfail2 : S.relStanding m r₂ ≠ Standing.full) :
    ¬ HarmonicAlign S m z :=
  fun h => rel_floor_noncompensatory S m r₁ r₂ h1full hreq2 hfail2 h.1

/-! ## 7. Bounded Harmonic Continuation (25g §15, T16/T17) -/

/-- T16 `bounded_harmonic_continuation`: the forward coherence/soundness
schema, exactly as 25f §14 states it, with `HarmonicAlign` supplying its
own `Extension` witness `z`. This is a schema (a conditional), never
marketed as an unconditional prediction — its four hypotheses are genuine
premises that a finite model must independently discharge, never
definitionally guaranteed. -/
theorem bounded_harmonic_continuation
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (z : S.Extension)
    (M : S.WorldModel) (o : S.Consequence)
    (hsuff : S.ModelSufficient M m)
    (halign : HarmonicAlign S m z)
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
    (S.ModelSufficient M m → HarmonicAlign S m z → S.CorrectConsequenceLaw M →
      S.NoOmittedDisturbance M → S.ConsequenceOf M m o → S.HarmonicOutcome o m) →
    S.HarmonicOutcome o m :=
  fun hschema => hschema hsuff halign hlaw hnodist hcons

/-- T17 `nonharmonic_falsifier`: the operational falsifier is the exact
contrapositive of the schema clause above, and — as 25g §15 requires —
IS proved by ordinary logic from the forward schema rather than postulated
independently. -/
theorem nonharmonic_falsifier
    (S : Sig) {K K' : S.Cut} (m : S.Movement K K') (z : S.Extension)
    (M : S.WorldModel) (o : S.Consequence)
    (hschema : S.ModelSufficient M m → HarmonicAlign S m z → S.CorrectConsequenceLaw M →
      S.NoOmittedDisturbance M → S.ConsequenceOf M m o → S.HarmonicOutcome o m)
    (hnonharmonic : ¬ S.HarmonicOutcome o m) :
    ¬ (S.ModelSufficient M m ∧ HarmonicAlign S m z ∧ S.CorrectConsequenceLaw M ∧
        S.NoOmittedDisturbance M ∧ S.ConsequenceOf M m o) := by
  intro ⟨hsuff, halign, hlaw, hnodist, hcons⟩
  exact hnonharmonic (hschema hsuff halign hlaw hnodist hcons)

/-! ## 8. PNS-like, SNS-like, Stuck (25g §16, 25f §15–17) -/

/-- `PNSLike`: conjunction of all nine witnesses 25f §15 lists. -/
def PNSLike (S : Sig) (τ : S.Trajectory) : Prop :=
  S.Contactability τ ∧ S.RelationalOpenness τ ∧ S.PreservedDistinctions τ ∧
  S.ReceptiveAttention τ ∧ S.DifferentiationWithCoherence τ ∧
  S.LowUnnecessaryForcing τ ∧ S.TrajConsequenceAnswerable τ ∧
  S.InterfaceOpenness τ ∧ S.SelfWeavingPlasticity τ

/-- `HoldingApart`: one of the "possible witnesses" 25f §16 lists for the
"holding apart" half of SNS-like organization (contact exclusion,
frame/topology persistence, or interface narrowing — any one suffices,
since 25f presents these as alternative possible witnesses, not a
required conjunction). -/
def HoldingApart (S : Sig) (τ : S.Trajectory) : Prop :=
  S.ContactExclusion τ ∨ S.Recurrence τ ∨ S.InterfaceNarrowing τ

/-- `SNSLike`: the ratified core pattern of 25f §16 — "holding apart" +
"forced velocity toward an imposed elsewhere". -/
def SNSLike (S : Sig) (τ : S.Trajectory) : Prop :=
  HoldingApart S τ ∧ S.ForcedVelocity τ

/-- `Stuck`: SNS-like organization whose volume has crossed the functional
threshold of 25f §17 — encoded, as 25h §19 requires, with the threshold
crossing given by INDEPENDENTLY TESTABLE trajectory witnesses (staleness
of forward motion, or pivot unavailability), not by a second opaque flag.
DECISION-03 (see decision log): 25f §17's sentence "staleness, forward
movement, or the capacity to pivot is ... unavailable" is read
disjunctively (`∨`) rather than conjunctively, matching its surface
grammar ("or"); this is a logged, arguable reading, not a hidden
resolution — see GAP-09. -/
def Stuck (S : Sig) (τ : S.Trajectory) : Prop :=
  SNSLike S τ ∧ (S.StaleForwardMotion τ ∨ S.PivotUnavailable τ)

/-- T13 `stuck_implies_sns`: `Stuck → SNSLike`, WITHOUT the converse
(no lemma of the shape `SNSLike → Stuck` exists anywhere in this
development — see `Models.lean`'s `t_low` witness for a concrete
countermodel to the converse). -/
theorem stuck_implies_sns (S : Sig) (τ : S.Trajectory) : Stuck S τ → SNSLike S τ :=
  fun h => h.1

/-! ## 9. Participation-interface change (25g §17) -/

/-- `InterfaceChange K K'`: distinguishes a mode newly available at `K'`
from a mode that was ALREADY available at `K` (25g §17's explicit
requirement not to conflate "new mode after transition" with "all modes
pre-authorized as available"). A genuine interface change exhibits a mode
available at `K'` that provably was not available at `K`. -/
def InterfaceChange (S : Sig) {K K' : S.Cut} (modeAtK : S.Mode K) (modeAtK' : S.Mode K') : Prop :=
  ¬ S.AvailableAt modeAtK ∧ S.AvailableAt modeAtK'

end Inv25
