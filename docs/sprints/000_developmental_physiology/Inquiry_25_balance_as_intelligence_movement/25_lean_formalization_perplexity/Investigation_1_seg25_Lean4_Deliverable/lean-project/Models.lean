import Core

/-!
# Investigation 25 — Finite Models

`M1` (high-action/low-forcing skilled movement), `M2` (Clarity frame pivot),
`M3` (heterogeneous knowledge inquiry), all instantiating the SAME `Sig`
structure from `Core.lean` (25g §23 clause 3: "all three finite models use
one unchanged semantics"). `M1` is additionally used to host several of the
25h adversarial countermodels that are model-agnostic (materiality,
Relatedness/Precision non-compensation, ReadApp oracle, R/A/P
non-injectivity, energetic typing, BHC/ModelSufficient, SNS/Stuck
threshold) rather than building a separate throwaway `Sig` instance for
each — reusing one rich model keeps the boilerplate proportional to the
task while still giving every adversary a genuine, independently
checkable witness inside it (see `25_encoding_decision_log.md`,
DECISION-04).

ENGINEERING NOTE: every function below of apparent shape
`∀ {K K' : Cut}, Movement K K' → ... := | pat => ...` is instead written as
`{K K' : Cut} (m : Movement K K') ... := match m ... with | pat => ...`.
The two are mathematically identical, but the equation-compiler sugar form
triggers a genuine elaborator bug in this Lean version whenever the
`Cut` inductive's own constructors share names with the implicit binder
names (`K`, `K'` here) — the anonymous-constructor `.ctor` notation in the
match arms gets resolved against `Cut` instead of `Movement`/`Relation`/etc,
producing spurious `unknownIdentifier` errors. Using explicit
`fun`/`match` avoids the ambiguity entirely. This is a mechanical
Lean-engineering fix, not a semantic choice (see build/axiom report).
-/

set_option linter.constructorNameAsVariable false
set_option linter.unusedSimpArgs false
set_option linter.unusedVariables false
set_option linter.defProp false

namespace Inv25

/-! ## M1 — high-action/low-forcing skilled movement, plus adversary host -/

namespace M1

inductive Cut where | K | K'
deriving DecidableEq, Repr

/-- Every M1 movement goes `K → K'`; distinct movements are distinct
constructors of one inductive family. -/
inductive Movement : Cut → Cut → Type where
  | skilled : Movement .K .K'
  | forcedHighHigh : Movement .K .K'
  | lowActHighForce : Movement .K .K'
  | relNonComp : Movement .K .K'
  | precNonComp : Movement .K .K'
  | matUsedOnly : Movement .K .K'
  | matGood : Movement .K .K'
  | unavailableMove : Movement .K .K'
deriving DecidableEq

/-- Relations material at cut `K` (all M1 movements read from `K`). -/
inductive Relation : Cut → Type where
  | r1 : Relation .K
  | r2 : Relation .K
  | r3 : Relation .K
  | rUsed : Relation .K
deriving DecidableEq

inductive Distinction : Cut → Type where
  | d1 : Distinction .K
  | d2 : Distinction .K
  | d3 : Distinction .K
deriving DecidableEq

inductive Mode : Cut → Type where
  | trivial : Mode c
deriving DecidableEq

inductive Extension where | ext1
deriving DecidableEq

inductive Consequence where | harmoniousConsequence | badConsequence
deriving DecidableEq

inductive WorldModel where | goodModel | badModel
deriving DecidableEq

/-- Three trajectories realizing the SNS/Stuck threshold adversary
(25h §15): `tLow` (some SNS evidence, pivot still available), `tStuck`
(SNS evidence plus staleness/topology recurrence and pivot unavailable),
`tBusy` (high activity, no holding-apart/forced-velocity pattern). -/
inductive Trajectory where | tLow | tStuck | tBusy
deriving DecidableEq

def SoulDoctrine := Unit
def Provenance := Unit
def GenerationKind := Unit
def SemanticEvaluator := Unit

def relStanding {K K' : Cut} (m : Movement K K') (r : Relation K) : Standing :=
  match m, r with
  | .relNonComp, .r3 => .absent
  | _, _ => .full

def distStanding {K K' : Cut} (m : Movement K K') (d : Distinction K) : Standing :=
  match m, d with
  | .precNonComp, .d3 => .absent
  | _, _ => .full

/-- `r1, r2, r3` are the required relation set for `relNonComp`'s test;
kept required for every movement so the same predicate is reusable. -/
def RequiredRel {K K' : Cut} (_ : Movement K K') (_ : Relation K) : Prop := True
def RequiredDist {K K' : Cut} (_ : Movement K K') (_ : Distinction K) : Prop := True

def UsedByRel {K K' : Cut} (m : Movement K K') (r : Relation K) : Prop :=
  match m, r with
  | .matUsedOnly, .rUsed => True
  | .matGood, .rUsed => True
  | _, _ => False

def DiscriminatesRel {K K' : Cut} (m : Movement K K') (r : Relation K) : Prop :=
  match m, r with
  | .matGood, .rUsed => True
  | _, _ => False

def UsedByDist {K K' : Cut} (_ : Movement K K') (_ : Distinction K) : Prop := False
def DiscriminatesDist {K K' : Cut} (_ : Movement K K') (_ : Distinction K) : Prop := False

def RelProvenance {K : Cut} (_ : Relation K) : Provenance := ()
def DistProvenance {K : Cut} (_ : Distinction K) : Provenance := ()

def Available {K K' : Cut} (m : Movement K K') : Prop :=
  match m with
  | .unavailableMove => False
  | _ => True

def Adm24 (_ : SoulDoctrine) {K K' : Cut} (_ : Movement K K') : Prop := True

def actionEffort {K K' : Cut} (m : Movement K K') : ActionEffort :=
  match m with
  | .skilled => ⟨90⟩
  | .forcedHighHigh => ⟨90⟩
  | .lowActHighForce => ⟨5⟩
  | _ => ⟨50⟩

def excessForcing {K K' : Cut} (m : Movement K K') : ExcessForcing :=
  match m with
  | .skilled => ⟨2⟩
  | .forcedHighHigh => ⟨95⟩
  | .lowActHighForce => ⟨95⟩
  | _ => ⟨2⟩

def physicalEnergy {K K' : Cut} (_ : Movement K K') : PhysicalEnergy := ⟨1⟩
def representationEffort {K K' : Cut} (_ : Movement K K') : RepresentationEffort := ⟨1⟩
def genenergy {K K' : Cut} (_ : Movement K K') : Genenergy := ⟨1⟩

/-- Only the two high-forcing movements carry disqualifying excess-forcing
evidence; `skilled`'s low `ExcessForcing` value is corroborated (not
contradicted) by this independent witness. -/
def DisqualifyingExcessForcing {K K' : Cut} (m : Movement K K') : Prop :=
  match m with
  | .forcedHighHigh => True
  | .lowActHighForce => True
  | _ => False

def ParticipationOpen {K K' : Cut} (_ : Movement K K') : Prop := True
def ConsequenceAnswerable {K K' : Cut} (_ : Movement K K') : Prop := True

/-- Lawful Appropriateness is asserted directly as a recognized-fittingness
witness for the well-behaved movements — never computed from any
"target hit" boolean (no such boolean exists anywhere in this file). -/
def LawfulAppropriate {K K' : Cut} (m : Movement K K') : Prop :=
  match m with
  | .forcedHighHigh => False
  | .lowActHighForce => False
  | .unavailableMove => False
  | _ => True

def ExtensionOf (_ : Extension) {K K' : Cut} (_ : Movement K K') : Prop := True

def AlignedExtension (e : Extension) {K K' : Cut} (m : Movement K K') : Prop :=
  match e, m with
  | .ext1, .forcedHighHigh => False
  | .ext1, .lowActHighForce => False
  | _, _ => True

def ContinuingContactable {K K' : Cut} (m : Movement K K') : Prop :=
  match m with
  | .forcedHighHigh => False
  | .lowActHighForce => False
  | _ => True

def evaluatorOf {K K' : Cut} (_ : Movement K K') : SemanticEvaluator := ()
def DoctrineBound (_ : SemanticEvaluator) (_ : SoulDoctrine) : Prop := True
def provenanceOfMovement {K K' : Cut} (_ : Movement K K') : Provenance := ()
def generationKindOf {K K' : Cut} (_ : Movement K K') : GenerationKind := ()

/-- `goodModel` follows a correct, disturbance-free consequence law that
only ever yields the harmonious consequence; `badModel`'s consequence law
is (independently) marked incorrect, and it is otherwise unconstrained. -/
def ModelSufficient (w : WorldModel) {K K' : Cut} (_ : Movement K K') : Prop :=
  match w with
  | .goodModel => True
  | .badModel => True

def CorrectConsequenceLaw (w : WorldModel) : Prop :=
  match w with
  | .goodModel => True
  | .badModel => False

def NoOmittedDisturbance (_ : WorldModel) : Prop := True

def ConsequenceOf (w : WorldModel) {K K' : Cut} (_ : Movement K K') (o : Consequence) : Prop :=
  match w with
  | .goodModel => o = Consequence.harmoniousConsequence
  | .badModel => True

def HarmonicOutcome (o : Consequence) {K K' : Cut} (_ : Movement K K') : Prop :=
  o = Consequence.harmoniousConsequence

def Contactability (t : Trajectory) : Prop :=
  match t with
  | .tBusy => True | .tLow => True | .tStuck => True

def RelationalOpenness (t : Trajectory) : Prop :=
  match t with
  | .tBusy => True | _ => False

def PreservedDistinctions (_ : Trajectory) : Prop := True

def ReceptiveAttention (t : Trajectory) : Prop :=
  match t with
  | .tBusy => True | _ => False

def DifferentiationWithCoherence (t : Trajectory) : Prop :=
  match t with
  | .tBusy => True | _ => False

def LowUnnecessaryForcing (t : Trajectory) : Prop :=
  match t with
  | .tBusy => True | _ => False

def TrajConsequenceAnswerable (_ : Trajectory) : Prop := True

def InterfaceOpenness (t : Trajectory) : Prop :=
  match t with
  | .tBusy => True | _ => False

def SelfWeavingPlasticity (t : Trajectory) : Prop :=
  match t with
  | .tBusy => True | _ => False

def ContactExclusion (t : Trajectory) : Prop :=
  match t with
  | .tLow => True | .tStuck => True | .tBusy => False

def Recurrence (t : Trajectory) : Prop :=
  match t with
  | .tStuck => True | _ => False

def InterfaceNarrowing (_ : Trajectory) : Prop := False

def ForcedVelocity (t : Trajectory) : Prop :=
  match t with
  | .tLow => True | .tStuck => True | .tBusy => False

def StaleForwardMotion (t : Trajectory) : Prop :=
  match t with
  | .tStuck => True | _ => False

def PivotUnavailable (t : Trajectory) : Prop :=
  match t with
  | .tStuck => True | _ => False

def ForceResidueEvidence (_ : Trajectory) : Prop := False

def AvailableAt {K : Cut} (_ : Mode K) : Prop := True

@[reducible] def sig : Sig where
  Cut := Cut
  SoulDoctrine := SoulDoctrine
  Provenance := Provenance
  GenerationKind := GenerationKind
  SemanticEvaluator := SemanticEvaluator
  Movement := Movement
  Relation := Relation
  Distinction := Distinction
  Mode := Mode
  Extension := Extension
  Consequence := Consequence
  WorldModel := WorldModel
  Trajectory := Trajectory
  Available := Available
  Adm24 := Adm24
  UsedByRel := UsedByRel
  UsedByDist := UsedByDist
  DiscriminatesRel := DiscriminatesRel
  DiscriminatesDist := DiscriminatesDist
  RelProvenance := RelProvenance
  DistProvenance := DistProvenance
  relStanding := relStanding
  distStanding := distStanding
  RequiredRel := RequiredRel
  RequiredDist := RequiredDist
  physicalEnergy := physicalEnergy
  representationEffort := representationEffort
  actionEffort := actionEffort
  excessForcing := excessForcing
  genenergy := genenergy
  DisqualifyingExcessForcing := DisqualifyingExcessForcing
  ParticipationOpen := ParticipationOpen
  ConsequenceAnswerable := ConsequenceAnswerable
  LawfulAppropriate := LawfulAppropriate
  ExtensionOf := ExtensionOf
  AlignedExtension := AlignedExtension
  ContinuingContactable := ContinuingContactable
  evaluatorOf := evaluatorOf
  DoctrineBound := DoctrineBound
  provenanceOfMovement := provenanceOfMovement
  generationKindOf := generationKindOf
  ModelSufficient := ModelSufficient
  CorrectConsequenceLaw := CorrectConsequenceLaw
  NoOmittedDisturbance := NoOmittedDisturbance
  ConsequenceOf := ConsequenceOf
  HarmonicOutcome := HarmonicOutcome
  Contactability := Contactability
  RelationalOpenness := RelationalOpenness
  PreservedDistinctions := PreservedDistinctions
  ReceptiveAttention := ReceptiveAttention
  DifferentiationWithCoherence := DifferentiationWithCoherence
  LowUnnecessaryForcing := LowUnnecessaryForcing
  TrajConsequenceAnswerable := TrajConsequenceAnswerable
  InterfaceOpenness := InterfaceOpenness
  SelfWeavingPlasticity := SelfWeavingPlasticity
  ContactExclusion := ContactExclusion
  Recurrence := Recurrence
  InterfaceNarrowing := InterfaceNarrowing
  ForcedVelocity := ForcedVelocity
  StaleForwardMotion := StaleForwardMotion
  PivotUnavailable := PivotUnavailable
  ForceResidueEvidence := ForceResidueEvidence
  AvailableAt := AvailableAt

@[reducible] def doctrine : sig.SoulDoctrine := ()

/-! ### Adversarial countermodels and T18/T25 hosted in M1 (25h §2–§10, §15–§16)

See `25_encoding_decision_log.md`/`25_formalization_gap_report.md` for the
full discussion of each item below; comments here are kept brief.

ENGINEERING NOTE: `open Movement` below is required so bare movement
constructor names (`skilled`, `matUsedOnly`, ...) resolve to the actual
`Movement` constructors as ordinary terms; without it, Lean4's
auto-bound-implicit feature silently turns an unqualified unresolved
lowercase identifier occurring in a theorem's TYPE into a fresh implicit
variable instead of raising an error, which produced a cascade of
spurious "expected type must not contain free variables"/type-mismatch
errors during drafting. Purely a Lean-scoping fix, not a semantic
change. -/
open Movement

/-- 25h §2 materiality adversary, failing half: `matUsedOnly` uses `rUsed`
but never discriminates it, so the conjunction defining `MaterialTo`
cannot be closed — this is a genuine countermodel to `UsedBy ⇒ MaterialTo`,
not merely an unproved goal. -/
theorem m1_materiality_used_not_material :
    ¬ MaterialTo sig matUsedOnly Relation.rUsed := by
  intro h; exact h.2

/-- 25h §2 materiality adversary, succeeding half: `matGood` both uses and
discriminates `rUsed`, so materiality DOES hold once genuine discrimination
is supplied. -/
theorem m1_materiality_good_is_material :
    MaterialTo sig matGood Relation.rUsed := ⟨trivial, trivial⟩

/-- 25h §3 Relatedness non-compensation adversary: `relNonComp` has `r1`
at full standing while its required `r3` is absent — `AllRelFloors` fails
regardless of `r1`'s strength, with no arithmetic averaging involved. -/
theorem m1_rel_noncomp_fails_floors : ¬ AllRelFloors sig relNonComp :=
  rel_floor_noncompensatory sig relNonComp Relation.r1 Relation.r3
    rfl trivial (by decide)

/-- 25h §4 Precision non-compensation adversary, the Distinction analogue. -/
theorem m1_prec_noncomp_fails_floors : ¬ AllPrecFloors sig precNonComp :=
  prec_floor_noncompensatory sig precNonComp Distinction.d1 Distinction.d3
    rfl trivial (by decide)

/-- 25h §5 `ReadApp` oracle adversary, case 1: `unavailableMove` has no
`Available` witness, so no `Adm25Witness` — hence no `ReadApp` — can be
built for it. -/
theorem m1_readapp_fails_unavailable :
    ∀ A, ¬ ReadApp sig doctrine unavailableMove A := by
  intro A h
  obtain ⟨adm⟩ := readapp_requires_adm sig doctrine unavailableMove A h
  exact adm.available

/-- 25h §5 case 2: failed material Relatedness floor blocks every
`ReadApp` witness (instantiates Core's generic `readapp_rel_floor` at the
concrete `relNonComp` countermodel above). -/
theorem m1_readapp_fails_relfloor :
    ∀ A, ¬ ReadApp sig doctrine relNonComp A :=
  readapp_rel_floor sig doctrine relNonComp m1_rel_noncomp_fails_floors

/-- 25h §5 case 3: failed material Precision floor, the analogue. -/
theorem m1_readapp_fails_precfloor :
    ∀ A, ¬ ReadApp sig doctrine precNonComp A :=
  readapp_prec_floor sig doctrine precNonComp m1_prec_noncomp_fails_floors

/-- 25h §5, positive half: `skilled` genuinely satisfies every ratified
Adm25 clause, so a lawful `Adm25Witness` (and hence a lawful `ReadApp`
reading) CAN be built — the adversary cases above fail for a principled
reason (a specific missing clause), not because construction is
universally impossible. -/
def skilledAdm : Adm25Witness sig doctrine skilled :=
  { available := trivial
    adm24 := trivial
    relFloors := fun r _ => rfl
    precFloors := fun d _ => rfl
    noDisqualifyingForcing := fun h => h
    participationOpen := trivial
    consequenceAnswerable := trivial }

def skilledReadApp : ReadApp sig doctrine skilled
    { prov := provenanceOfMovement skilled
      gen := generationKindOf skilled
      kind := ReadingKind.derivedAppropriateness } :=
  @ReadApp.mk sig doctrine _ _ skilled skilledAdm trivial

/-- 25h §5 case 5: even for this successful witness, the reading is never
tagged `directContact` — instantiates Core's generic T08 at a genuine
lawful witness rather than a vacuous one. -/
theorem m1_skilled_never_direct_contact :
    ({ prov := provenanceOfMovement skilled
       gen := generationKindOf skilled
       kind := ReadingKind.derivedAppropriateness } : Appropriateness sig skilled).kind
      ≠ ReadingKind.directContact :=
  readapp_no_contact_masquerade sig doctrine skilled _ skilledReadApp

/-- T25 / 25h §6 R/A/P non-injectivity adversary: a genuinely
lower-dimensional "diagnostic summary" (here: does this movement carry
disqualifying excess-forcing evidence?) identifies `forcedHighHigh` and
`lowActHighForce` identically even though they are distinct movements
with distinct full energetic profiles (90/95 vs 5/95) — demonstrating that
no such summary can reconstruct Movement identity, which is why no
`reconstruct : Summary → Movement` function is exported anywhere in this
development. -/
def summaryRAP {K K' : Cut} (m : Movement K K') : Bool :=
  match m with
  | .forcedHighHigh => true
  | .lowActHighForce => true
  | _ => false

theorem T25_rap_summary_noninjective :
    (Movement.forcedHighHigh : Movement Cut.K Cut.K') ≠ Movement.lowActHighForce ∧
      summaryRAP Movement.forcedHighHigh = summaryRAP Movement.lowActHighForce :=
  ⟨by decide, rfl⟩

/-- 25h §8 energetic typing adversary, Case A: high `ActionEffort`, low
`ExcessForcing` (`skilled`). Threshold `50` is an arbitrary comparison
point (GAP-06) used only to compare a type against itself, never across
types. -/
theorem T18_energetic_case_A_skilled :
    HighActionEffort 50 (actionEffort skilled) ∧ LowExcessForcing 50 (excessForcing skilled) :=
  ⟨by unfold HighActionEffort actionEffort; decide, by unfold LowExcessForcing excessForcing; decide⟩

/-- 25h §8 Case B: low `ActionEffort`, high `ExcessForcing`
(`lowActHighForce`). Both cases type-check as ordinary `Movement`
constructors precisely because `ActionEffort`/`ExcessForcing` are distinct
wrapper types with no coercion or monotonic dependency between them
(enforced by the Lean type checker itself, per Core.lean). -/
theorem T18_energetic_case_B_lowActHighForce :
    LowActionEffort 50 (actionEffort lowActHighForce) ∧
      HighExcessForcing 50 (excessForcing lowActHighForce) :=
  ⟨by unfold LowActionEffort actionEffort; decide, by unfold HighExcessForcing excessForcing; decide⟩

/-- T18 / 25h §16 PNS high-force adversary ("force is not forcing"):
`skilled` and `forcedHighHigh` share the SAME high `ActionEffort` (90),
yet only `forcedHighHigh` carries disqualifying excess-forcing evidence
and only `skilled` is lawfully appropriate — so high action effort alone
never licenses anything; the independent forcing witness is what
discriminates the two. -/
theorem T18_pns_high_force_contrast :
    (HighActionEffort 50 (actionEffort skilled) ∧ LowExcessForcing 50 (excessForcing skilled) ∧
        ¬ DisqualifyingExcessForcing skilled ∧ LawfulAppropriate skilled) ∧
      (HighActionEffort 50 (actionEffort forcedHighHigh) ∧
        HighExcessForcing 50 (excessForcing forcedHighHigh) ∧
        DisqualifyingExcessForcing forcedHighHigh ∧ ¬ LawfulAppropriate forcedHighHigh) :=
  ⟨⟨by unfold HighActionEffort actionEffort; decide, by unfold LowExcessForcing excessForcing; decide,
      (fun h => h), trivial⟩,
    ⟨by unfold HighActionEffort actionEffort; decide, by unfold HighExcessForcing excessForcing; decide,
      trivial, (fun h => h)⟩⟩

/-- T18 (continued): a genuine `PNSLike` witness exists at the trajectory
level (`tBusy`), since Core's `PNSLike` is a predicate on `Trajectory`,
not `Movement` (25g's single choice for where the nine witnesses live —
see DECISION-05 in the decision log). The movement-level "force is not
forcing" contrast above and this trajectory-level witness together
discharge 25h §16's full intent within the one `Sig` this file uses. -/
theorem T18_tBusy_is_PNSLike : PNSLike sig Trajectory.tBusy :=
  ⟨trivial, trivial, trivial, trivial, trivial, trivial, trivial, trivial, trivial⟩

/-- 25h §9 harmonic-circularity adversary, Layer 1 (coherence theorem):
under `goodModel`'s genuinely-discharged sufficiency/law/disturbance
premises and a real `HarmonicAlign` witness for `skilled`, BHC concludes
`HarmonicOutcome`. The connecting `hschema` premise is proved here purely
from `goodModel`'s consequence law forcing `o = harmoniousConsequence`
definitionally — `ModelSufficient` itself is NOT defined as "predictions
came true" (it is an unconditional external-governance witness for both
models, per adversary #10 below), so no circularity is introduced. -/
theorem m1_bhc_good_layer1 :
    sig.HarmonicOutcome Consequence.harmoniousConsequence skilled :=
  bounded_harmonic_continuation sig skilled Extension.ext1 WorldModel.goodModel
    Consequence.harmoniousConsequence
    trivial
    ⟨(fun r _ => rfl), trivial, (fun d _ => rfl), (fun h => h), (fun _ => trivial), trivial⟩
    trivial
    trivial
    rfl
    (fun _ _ _ _ _ => rfl)

/-- 25h §9 Layer 2 (falsifier): for `badModel`, whose `CorrectConsequenceLaw`
is (independently) marked `False`, marking a consequence non-harmonic lets
us derive that sufficiency/alignment/law/disturbance/consequence cannot
ALL simultaneously hold — here because the law premise alone already
fails, which is exactly `badModel`'s logged defect (see decision log
DECISION-04), not a fact smuggled into `HarmonicOutcome`'s own
definition. -/
theorem m1_bhc_bad_layer2_falsifier :
    ¬ (sig.ModelSufficient WorldModel.badModel skilled ∧ HarmonicAlign sig skilled Extension.ext1 ∧
        sig.CorrectConsequenceLaw WorldModel.badModel ∧ sig.NoOmittedDisturbance WorldModel.badModel ∧
        sig.ConsequenceOf WorldModel.badModel skilled Consequence.badConsequence) :=
  nonharmonic_falsifier sig skilled Extension.ext1 WorldModel.badModel Consequence.badConsequence
    (fun _ _ hlaw _ _ => absurd hlaw (fun h => h))
    (by simp only [Sig.HarmonicOutcome, HarmonicOutcome]; decide)

/-- 25h §15 SNS/Stuck threshold adversary. `tLow`: SNS evidence present,
pivot still available — SNS-like but not Stuck. -/
theorem T_adv15_tLow : SNSLike sig Trajectory.tLow ∧ ¬ Stuck sig Trajectory.tLow := by
  simp only [SNSLike, Stuck, HoldingApart, Sig.ForcedVelocity, Sig.StaleForwardMotion,
    Sig.PivotUnavailable, Sig.ContactExclusion, Sig.Recurrence, Sig.InterfaceNarrowing,
    ForcedVelocity, StaleForwardMotion, PivotUnavailable, ContactExclusion, Recurrence,
    InterfaceNarrowing]
  decide

/-- `tStuck`: SNS evidence plus staleness AND pivot-unavailability —
crosses the (disjunctively-read, DECISION-03) threshold into `Stuck`,
which still entails `SNSLike` (T13). -/
theorem T_adv15_tStuck : Stuck sig Trajectory.tStuck ∧ SNSLike sig Trajectory.tStuck := by
  simp only [SNSLike, Stuck, HoldingApart, Sig.ForcedVelocity, Sig.StaleForwardMotion,
    Sig.PivotUnavailable, Sig.ContactExclusion, Sig.Recurrence, Sig.InterfaceNarrowing,
    ForcedVelocity, StaleForwardMotion, PivotUnavailable, ContactExclusion, Recurrence,
    InterfaceNarrowing]
  decide

/-- `tBusy`: high activity on every PNS-ish witness but no holding-apart /
forced-velocity pattern at all — neither `Stuck` nor even `SNSLike`,
proving `Stuck` is not "high activity" and not an unrelated state. -/
theorem T_adv15_tBusy : ¬ Stuck sig Trajectory.tBusy ∧ ¬ SNSLike sig Trajectory.tBusy := by
  simp only [SNSLike, Stuck, HoldingApart, Sig.ForcedVelocity, Sig.StaleForwardMotion,
    Sig.PivotUnavailable, Sig.ContactExclusion, Sig.Recurrence, Sig.InterfaceNarrowing,
    ForcedVelocity, StaleForwardMotion, PivotUnavailable, ContactExclusion, Recurrence,
    InterfaceNarrowing]
  decide

end M1

/-! ## M2 — Clarity frame pivot (25f/25g §17's cut/mode pivot; 25h §12–§14)

Three cuts: `K0` (pre-contact), `K1` (post-contact), `K2` (post-retry).
`contactMove : K0 → K1` is the movement whose passage makes a NEW
distinction (`subscription`) live at `K1` — `Distinction` is a genuinely
dependent family (`Distinction K0`/`Distinction K2` are EMPTY types, only
`Distinction K1` is inhabited), so "the discriminating fact did not yet
exist" is a TYPE-LEVEL fact for any `K0`-sourced movement, not merely an
unproved side condition — this is what makes the frame-sovereignty negative
control (25h §13) non-vacuous rather than stipulated. `retryBefore : K0 →
K1` is the negative control (same shape as `contactMove`, before any
contact). `retryTraceVisible`/`retryTraceSevered : K1 → K2` are the
meta-awareness pair (25h §14): both start from `K1`, where `subscription`
is now live and required; `retryTraceVisible` respects it (`full`
standing), `retryTraceSevered` omits it (`absent` standing) — giving a
genuine downstream admissibility difference, not merely logged data. -/

namespace M2

inductive Cut where | K0 | K1 | K2
deriving DecidableEq, Repr

inductive Movement : Cut → Cut → Type where
  | contactMove : Movement .K0 .K1
  | retryBefore : Movement .K0 .K1
  | retryTraceVisible : Movement .K1 .K2
  | retryTraceSevered : Movement .K1 .K2
deriving DecidableEq

open Movement

/-- No live relations material in M2 (M2 tests distinctions/modes, not
relations) — `Relation K` is empty at every cut, so every
relation-quantified obligation (`AllRelFloors`, `UsedByRel`, ...) is
discharged by `nomatch`, never by vacuous-but-hidden defaulting. -/
inductive Relation : Cut → Type where
deriving DecidableEq

/-- The one material distinction of this model: `subscription`, live ONLY
at `K1` (25h §13's "material subscription distinction" established by
contact). `Distinction K0`/`Distinction K2` have no constructors. -/
inductive Distinction : Cut → Type where
  | subscription : Distinction .K1
deriving DecidableEq

/-- One canonical interface mode per cut; `AvailableAt` (below) is what
actually encodes growth — the mode VALUE is uniform, only its cut-indexed
availability differs (25h §12's "new mode may exist in the type but must
not be currently available before the transition"). -/
inductive Mode : Cut → Type where
  | modeAt : {K : Cut} → Mode K
deriving DecidableEq

open Distinction Mode

def Extension := Unit
def Consequence := Unit
def WorldModel := Unit
def Trajectory := Unit
def SoulDoctrine := Unit
def Provenance := Unit
def GenerationKind := Unit
def SemanticEvaluator := Unit

def relStanding {K K' : Cut} (_ : Movement K K') (r : Relation K) : Standing := nomatch r
def RequiredRel {K K' : Cut} (_ : Movement K K') (r : Relation K) : Prop := nomatch r
def UsedByRel {K K' : Cut} (_ : Movement K K') (r : Relation K) : Prop := nomatch r
def DiscriminatesRel {K K' : Cut} (_ : Movement K K') (r : Relation K) : Prop := nomatch r
def RelProvenance {K : Cut} (r : Relation K) : Provenance := nomatch r

/-- `distStanding`: `retryTraceVisible` gives `subscription` `full`
standing (it genuinely carries the trace forward); `retryTraceSevered`
gives it `absent` (it drops the trace). `contactMove`/`retryBefore` are
sourced at `K0`, where no distinction exists at all. -/
def distStanding {K K' : Cut} (m : Movement K K') (d : Distinction K) : Standing :=
  match m with
  | contactMove => nomatch d
  | retryBefore => nomatch d
  | retryTraceVisible => match d with | .subscription => .full
  | retryTraceSevered => match d with | .subscription => .absent

/-- `subscription` is required of any `K1`-sourced retry once it exists;
no distinction is required of a `K0`-sourced movement (there is none to
require). -/
def RequiredDist {K K' : Cut} (m : Movement K K') (d : Distinction K) : Prop :=
  match m with
  | contactMove => nomatch d
  | retryBefore => nomatch d
  | retryTraceVisible => True
  | retryTraceSevered => True

def UsedByDist {K K' : Cut} (m : Movement K K') (d : Distinction K) : Prop :=
  match m with
  | contactMove => nomatch d
  | retryBefore => nomatch d
  | retryTraceVisible => True
  | retryTraceSevered => False

def DiscriminatesDist {K K' : Cut} (m : Movement K K') (d : Distinction K) : Prop :=
  match m with
  | contactMove => nomatch d
  | retryBefore => nomatch d
  | retryTraceVisible => True
  | retryTraceSevered => False

def DistProvenance {K : Cut} (_ : Distinction K) : Provenance := ()

def Available {K K' : Cut} (_ : Movement K K') : Prop := True
def Adm24 (_ : SoulDoctrine) {K K' : Cut} (_ : Movement K K') : Prop := True

def actionEffort {K K' : Cut} (_ : Movement K K') : ActionEffort := ⟨0⟩
def excessForcing {K K' : Cut} (_ : Movement K K') : ExcessForcing := ⟨0⟩
def physicalEnergy {K K' : Cut} (_ : Movement K K') : PhysicalEnergy := ⟨0⟩
def representationEffort {K K' : Cut} (_ : Movement K K') : RepresentationEffort := ⟨0⟩
def genenergy {K K' : Cut} (_ : Movement K K') : Genenergy := ⟨0⟩
def DisqualifyingExcessForcing {K K' : Cut} (_ : Movement K K') : Prop := False

def ParticipationOpen {K K' : Cut} (_ : Movement K K') : Prop := True
def ConsequenceAnswerable {K K' : Cut} (_ : Movement K K') : Prop := True

/-- `LawfulAppropriate` differs downstream too (25h §14's "admissibility"
clause), reinforcing — not substituting for — the `Adm25Witness`
difference proved below. -/
def LawfulAppropriate {K K' : Cut} (m : Movement K K') : Prop :=
  match m with
  | retryTraceSevered => False
  | _ => True

def ExtensionOf (_ : Extension) {K K' : Cut} (_ : Movement K K') : Prop := True
def AlignedExtension (_ : Extension) {K K' : Cut} (_ : Movement K K') : Prop := True
def ContinuingContactable {K K' : Cut} (_ : Movement K K') : Prop := True

def evaluatorOf {K K' : Cut} (_ : Movement K K') : SemanticEvaluator := ()
def DoctrineBound (_ : SemanticEvaluator) (_ : SoulDoctrine) : Prop := True
def provenanceOfMovement {K K' : Cut} (_ : Movement K K') : Provenance := ()
def generationKindOf {K K' : Cut} (_ : Movement K K') : GenerationKind := ()

def ModelSufficient (_ : WorldModel) {K K' : Cut} (_ : Movement K K') : Prop := True
def CorrectConsequenceLaw (_ : WorldModel) : Prop := True
def NoOmittedDisturbance (_ : WorldModel) : Prop := True
def ConsequenceOf (_ : WorldModel) {K K' : Cut} (_ : Movement K K') (_ : Consequence) : Prop := True
def HarmonicOutcome (_ : Consequence) {K K' : Cut} (_ : Movement K K') : Prop := True

def Contactability (_ : Trajectory) : Prop := True
def RelationalOpenness (_ : Trajectory) : Prop := True
def PreservedDistinctions (_ : Trajectory) : Prop := True
def ReceptiveAttention (_ : Trajectory) : Prop := True
def DifferentiationWithCoherence (_ : Trajectory) : Prop := True
def LowUnnecessaryForcing (_ : Trajectory) : Prop := True
def TrajConsequenceAnswerable (_ : Trajectory) : Prop := True
def InterfaceOpenness (_ : Trajectory) : Prop := True
def SelfWeavingPlasticity (_ : Trajectory) : Prop := True

def ContactExclusion (_ : Trajectory) : Prop := False
def Recurrence (_ : Trajectory) : Prop := False
def InterfaceNarrowing (_ : Trajectory) : Prop := False
def ForcedVelocity (_ : Trajectory) : Prop := False
def StaleForwardMotion (_ : Trajectory) : Prop := False
def PivotUnavailable (_ : Trajectory) : Prop := False
def ForceResidueEvidence (_ : Trajectory) : Prop := False

/-- 25h §12 interface-growth clause: a mode is available at `K1` that
was NOT available at `K0` — checked by matching on the cut itself, so
there is no way to "fake" growth by making every mode available at every
cut (that would make this `match` return `True` in the `K0` branch too,
which would make `T20_interface_growth` below unprovable). -/
def AvailableAt {K : Cut} (_ : Mode K) : Prop :=
  match K with
  | .K0 => False
  | .K1 => True
  | .K2 => True

@[reducible] def sig2 : Sig where
  Cut := Cut
  SoulDoctrine := SoulDoctrine
  Provenance := Provenance
  GenerationKind := GenerationKind
  SemanticEvaluator := SemanticEvaluator
  Movement := Movement
  Relation := Relation
  Distinction := Distinction
  Mode := Mode
  Extension := Extension
  Consequence := Consequence
  WorldModel := WorldModel
  Trajectory := Trajectory
  Available := fun {K K'} => Available
  Adm24 := Adm24
  UsedByRel := fun {K K'} => UsedByRel
  UsedByDist := fun {K K'} => UsedByDist
  DiscriminatesRel := fun {K K'} => DiscriminatesRel
  DiscriminatesDist := fun {K K'} => DiscriminatesDist
  RelProvenance := fun {K} => RelProvenance
  DistProvenance := fun {K} => DistProvenance
  relStanding := fun {K K'} => relStanding
  distStanding := fun {K K'} => distStanding
  RequiredRel := fun {K K'} => RequiredRel
  RequiredDist := fun {K K'} => RequiredDist
  physicalEnergy := fun {K K'} => physicalEnergy
  representationEffort := fun {K K'} => representationEffort
  actionEffort := fun {K K'} => actionEffort
  excessForcing := fun {K K'} => excessForcing
  genenergy := fun {K K'} => genenergy
  DisqualifyingExcessForcing := fun {K K'} => DisqualifyingExcessForcing
  ParticipationOpen := fun {K K'} => ParticipationOpen
  ConsequenceAnswerable := fun {K K'} => ConsequenceAnswerable
  LawfulAppropriate := fun {K K'} => LawfulAppropriate
  ExtensionOf := ExtensionOf
  AlignedExtension := AlignedExtension
  ContinuingContactable := fun {K K'} => ContinuingContactable
  evaluatorOf := fun {K K'} => evaluatorOf
  DoctrineBound := DoctrineBound
  provenanceOfMovement := fun {K K'} => provenanceOfMovement
  generationKindOf := fun {K K'} => generationKindOf
  ModelSufficient := ModelSufficient
  CorrectConsequenceLaw := CorrectConsequenceLaw
  NoOmittedDisturbance := NoOmittedDisturbance
  ConsequenceOf := ConsequenceOf
  HarmonicOutcome := HarmonicOutcome
  Contactability := Contactability
  RelationalOpenness := RelationalOpenness
  PreservedDistinctions := PreservedDistinctions
  ReceptiveAttention := ReceptiveAttention
  DifferentiationWithCoherence := DifferentiationWithCoherence
  LowUnnecessaryForcing := LowUnnecessaryForcing
  TrajConsequenceAnswerable := TrajConsequenceAnswerable
  InterfaceOpenness := InterfaceOpenness
  SelfWeavingPlasticity := SelfWeavingPlasticity
  ContactExclusion := ContactExclusion
  Recurrence := Recurrence
  InterfaceNarrowing := InterfaceNarrowing
  ForcedVelocity := ForcedVelocity
  StaleForwardMotion := StaleForwardMotion
  PivotUnavailable := PivotUnavailable
  ForceResidueEvidence := ForceResidueEvidence
  AvailableAt := fun {K} => AvailableAt

@[reducible] def doctrine2 : sig2.SoulDoctrine := ()

/-- 25h §13 positive half: `retryTraceSevered` fails its Precision floor
directly (a single required distinction with non-`full` standing is
enough to block `AllPrecFloors` — no need to borrow the two-distinction
`prec_floor_noncompensatory` machinery, since M2's point is hindsight-
fairness, not compensation across several distinctions). -/
theorem m2_severed_fails_precfloor : ¬ AllPrecFloors sig2 retryTraceSevered := by
  intro hall
  have h := hall Distinction.subscription trivial
  exact absurd h (by decide)

/-- 25h §13 negative control: `retryBefore` (same `K0 → K1` shape as
`contactMove`, i.e. BEFORE any contact) is never penalized for omitting
`subscription`, because `Distinction K0` has no constructors — there is
no information it could have failed to use. This is what prevents
hindsight from contaminating admissibility: the omission is
TYPE-LEVEL-unavailable, not merely unrequired by a Prop that could have
been defined otherwise. -/
theorem m2_retryBefore_not_penalized : AllPrecFloors sig2 retryBefore := fun d => nomatch d

/-- T19 (25h §13, M2 frame-sovereignty adversary): the positive failure
and its negative control together. -/
theorem T19_frame_sovereignty :
    (¬ AllPrecFloors sig2 retryTraceSevered) ∧ AllPrecFloors sig2 retryBefore :=
  ⟨m2_severed_fails_precfloor, m2_retryBefore_not_penalized⟩

/-- `retryTraceSevered` therefore admits no lawful `ReadApp` reading at
all (Core's generic T10 instantiated here). -/
theorem m2_severed_no_readapp : ∀ A, ¬ ReadApp sig2 doctrine2 retryTraceSevered A :=
  readapp_prec_floor sig2 doctrine2 retryTraceSevered m2_severed_fails_precfloor

/-- T20 (25h §12, interface-growth adversary): `modeAt` is genuinely new
at `K1` — unavailable at `K0`, available at `K1` — checked via the
same `InterfaceChange` Core uses for M3 (25g §17), not a bespoke
M2-only predicate. -/
theorem T20_interface_growth :
    InterfaceChange sig2 (Mode.modeAt (K := Cut.K0)) (Mode.modeAt (K := Cut.K1)) :=
  ⟨fun h => h, trivial⟩

/-- Explicit anti-cheat witness: the pre-transition mode is genuinely
unavailable (not merely omitted from a positive obligation) — ruling out
the "every mode available at every cut" fake 25h §12 warns against. -/
theorem T20_interface_growth_not_faked : ¬ AvailableAt (Mode.modeAt (K := Cut.K0)) := fun h => h

/-- `retryTraceVisible` satisfies every Adm25 clause (built explicitly,
field by field, exactly as 25f §9/25g §10 list them). -/
def retryTraceVisibleAdm : Adm25Witness sig2 doctrine2 retryTraceVisible :=
  { available := trivial
    adm24 := trivial
    relFloors := fun r => nomatch r
    precFloors := fun d => match d with | .subscription => fun _ => rfl
    noDisqualifyingForcing := fun h => h
    participationOpen := trivial
    consequenceAnswerable := trivial }

/-- T21 (25h §14, M2 meta-awareness adversary): `traceVisible` admits a
lawful `Adm25Witness`; `traceSevered` provably does not — a genuine
downstream admissibility difference caused by the trace being visible
versus severed, not a passively-logged fact with no bite. -/
theorem T21_meta_awareness_bite :
    Nonempty (Adm25Witness sig2 doctrine2 retryTraceVisible) ∧
      ¬ Nonempty (Adm25Witness sig2 doctrine2 retryTraceSevered) := by
  refine ⟨⟨retryTraceVisibleAdm⟩, ?_⟩
  intro ⟨adm⟩
  exact m2_severed_fails_precfloor adm.precFloors

end M2

/-! ## M3 — Heterogeneous knowledge inquiry (25f §24's third example; 25h
§11 Fourthness, §12 interface-growth again, §17 no-global-model)

Two SEPARATE local contexts (`LA`, `LB`) each independently reach a shared
`Bridge` cut, with no premise anywhere of the form `exists
globalMasterModel : WorldModel` merging them first (25h §17). This is not
an informal claim: `WorldModel := Empty` in this model, so it is literally
UNINHABITED — a global master model cannot exist even in principle here,
and yet the bridge movement is still fully Adm25-admissible, which is the
strongest possible demonstration that no such object is smuggled in as a
hidden premise anywhere in Core's Adm25 obligations.

Fourthness (25h §11) lives entirely at `LA`: two MATERIAL relations `a`
and `b`, each required and independently load-bearing (deleting either's
full standing breaks `AllRelFloors`, hence blocks the bridge), plus one
DECORATIVE relation `z`, not required, whose failure must NOT count
(negative control). Four `LA → Bridge` movements exhibit the four
combinations needed: `bridgeMove` (a,b,z all full — the positive
admissible case), `bridgeMoveMissingA`/`bridgeMoveMissingB` (the two
Fourthness-positive failures), `bridgeMoveMissingZ` (the Fourthness
negative control: z fails, admissibility survives). -/

namespace M3

inductive Cut where | LA | LB | Bridge
deriving DecidableEq, Repr

inductive Movement : Cut → Cut → Type where
  | bridgeMove : Movement .LA .Bridge
  | bridgeMoveMissingA : Movement .LA .Bridge
  | bridgeMoveMissingB : Movement .LA .Bridge
  | bridgeMoveMissingZ : Movement .LA .Bridge
  | localMoveB : Movement .LB .Bridge
deriving DecidableEq

open Movement

/-- The two material Fourthness relations `a`/`b`, plus decorative `z`,
all sourced at `LA` (`Relation LB`/`Relation Bridge` are empty — `LB`'s
only movement, `localMoveB`, has no relation obligations at all, which is
part of what makes it independently admissible without reference to
anything at `LA`). -/
inductive Relation : Cut → Type where
  | a : Relation .LA
  | b : Relation .LA
  | z : Relation .LA
deriving DecidableEq

/-- M3 targets relations, not distinctions — `Distinction` is empty at
every cut (mirrors M2's treatment of `Relation`), so `AllPrecFloors` is
vacuously true everywhere and never interferes with the Fourthness/
no-global-model theorems below. -/
inductive Distinction : Cut → Type where
deriving DecidableEq

/-- One canonical bridge-only interface mode, available at `Bridge` but
at neither local context beforehand — a second, independently-witnessed
instance of 25h §12 interface growth (distinct cuts/movements from M2's). -/
inductive Mode : Cut → Type where
  | bridgeMode : {K : Cut} → Mode K
deriving DecidableEq

def Extension := Unit
def Consequence := Unit
/-- No global master model can exist in this Sig at all (25h §17): the
type is uninhabited, not merely "unused". -/
def WorldModel := Empty
def Trajectory := Unit
def SoulDoctrine := Unit
def Provenance := Unit
def GenerationKind := Unit
def SemanticEvaluator := Unit

/-- Relation standing per movement. `bridgeMove`: everything full (the
full diagram that permits the bridge). `bridgeMoveMissingA`/`...MissingB`:
one material relation drops to `absent`. `bridgeMoveMissingZ`: only the
DECORATIVE relation drops. `localMoveB`: no relations exist at `LB`, so
this is discharged by `nomatch` and never actually inspected. -/
def relStanding {K K' : Cut} (m : Movement K K') (r : Relation K) : Standing :=
  match m with
  | bridgeMove => .full
  | bridgeMoveMissingA => match r with | .a => .absent | .b => .full | .z => .full
  | bridgeMoveMissingB => match r with | .a => .full | .b => .absent | .z => .full
  | bridgeMoveMissingZ => match r with | .a => .full | .b => .full | .z => .absent
  | localMoveB => nomatch r

/-- `a`/`b` are MATERIAL (required); `z` is DECORATIVE (not required) —
this is the crux of the Fourthness distinction (25h §11: "Fourthness
depends on material counterfactual bite rather than mere relation
count"). -/
def RequiredRel {K K' : Cut} (_ : Movement K K') (r : Relation K) : Prop :=
  match r with
  | .a => True
  | .b => True
  | .z => False

def UsedByRel {K K' : Cut} (m : Movement K K') (r : Relation K) : Prop :=
  match m with
  | localMoveB => nomatch r
  | _ => True

def DiscriminatesRel {K K' : Cut} (_ : Movement K K') (r : Relation K) : Prop :=
  match r with
  | .a => True
  | .b => True
  | .z => False

def RelProvenance {K : Cut} (_ : Relation K) : Provenance := ()

def distStanding {K K' : Cut} (_ : Movement K K') (d : Distinction K) : Standing := nomatch d
def RequiredDist {K K' : Cut} (_ : Movement K K') (d : Distinction K) : Prop := nomatch d
def UsedByDist {K K' : Cut} (_ : Movement K K') (d : Distinction K) : Prop := nomatch d
def DiscriminatesDist {K K' : Cut} (_ : Movement K K') (d : Distinction K) : Prop := nomatch d
def DistProvenance {K : Cut} (d : Distinction K) : Provenance := nomatch d

def Available {K K' : Cut} (_ : Movement K K') : Prop := True
def Adm24 (_ : SoulDoctrine) {K K' : Cut} (_ : Movement K K') : Prop := True

def actionEffort {K K' : Cut} (_ : Movement K K') : ActionEffort := ⟨0⟩
def excessForcing {K K' : Cut} (_ : Movement K K') : ExcessForcing := ⟨0⟩
def physicalEnergy {K K' : Cut} (_ : Movement K K') : PhysicalEnergy := ⟨0⟩
def representationEffort {K K' : Cut} (_ : Movement K K') : RepresentationEffort := ⟨0⟩
def genenergy {K K' : Cut} (_ : Movement K K') : Genenergy := ⟨0⟩
def DisqualifyingExcessForcing {K K' : Cut} (_ : Movement K K') : Prop := False

def ParticipationOpen {K K' : Cut} (_ : Movement K K') : Prop := True
def ConsequenceAnswerable {K K' : Cut} (_ : Movement K K') : Prop := True
def LawfulAppropriate {K K' : Cut} (_ : Movement K K') : Prop := True

def ExtensionOf (_ : Extension) {K K' : Cut} (_ : Movement K K') : Prop := True
def AlignedExtension (_ : Extension) {K K' : Cut} (_ : Movement K K') : Prop := True
def ContinuingContactable {K K' : Cut} (_ : Movement K K') : Prop := True

def evaluatorOf {K K' : Cut} (_ : Movement K K') : SemanticEvaluator := ()
def DoctrineBound (_ : SemanticEvaluator) (_ : SoulDoctrine) : Prop := True
def provenanceOfMovement {K K' : Cut} (_ : Movement K K') : Provenance := ()
def generationKindOf {K K' : Cut} (_ : Movement K K') : GenerationKind := ()

/-- `WorldModel` is `Empty`, so every one of these is vacuously
discharged by `nomatch`/`.elim` on the `WorldModel` argument — the point
being that Adm25 admissibility (proved below) never has to call into any
of these, since it never has a `WorldModel` value to supply. -/
def ModelSufficient (w : WorldModel) {K K' : Cut} (_ : Movement K K') : Prop := w.elim
def CorrectConsequenceLaw (w : WorldModel) : Prop := w.elim
def NoOmittedDisturbance (w : WorldModel) : Prop := w.elim
def ConsequenceOf (w : WorldModel) {K K' : Cut} (_ : Movement K K') (_ : Consequence) : Prop := w.elim
def HarmonicOutcome (_ : Consequence) {K K' : Cut} (_ : Movement K K') : Prop := True

def Contactability (_ : Trajectory) : Prop := True
def RelationalOpenness (_ : Trajectory) : Prop := True
def PreservedDistinctions (_ : Trajectory) : Prop := True
def ReceptiveAttention (_ : Trajectory) : Prop := True
def DifferentiationWithCoherence (_ : Trajectory) : Prop := True
def LowUnnecessaryForcing (_ : Trajectory) : Prop := True
def TrajConsequenceAnswerable (_ : Trajectory) : Prop := True
def InterfaceOpenness (_ : Trajectory) : Prop := True
def SelfWeavingPlasticity (_ : Trajectory) : Prop := True

def ContactExclusion (_ : Trajectory) : Prop := False
def Recurrence (_ : Trajectory) : Prop := False
def InterfaceNarrowing (_ : Trajectory) : Prop := False
def ForcedVelocity (_ : Trajectory) : Prop := False
def StaleForwardMotion (_ : Trajectory) : Prop := False
def PivotUnavailable (_ : Trajectory) : Prop := False
def ForceResidueEvidence (_ : Trajectory) : Prop := False

/-- 25h §12 interface growth, second witness: `bridgeMode` is available at
`Bridge` but at neither local context beforehand. -/
def AvailableAt {K : Cut} (_ : Mode K) : Prop :=
  match K with
  | .LA => False
  | .LB => False
  | .Bridge => True

@[reducible] def sig3 : Sig where
  Cut := Cut
  SoulDoctrine := SoulDoctrine
  Provenance := Provenance
  GenerationKind := GenerationKind
  SemanticEvaluator := SemanticEvaluator
  Movement := Movement
  Relation := Relation
  Distinction := Distinction
  Mode := Mode
  Extension := Extension
  Consequence := Consequence
  WorldModel := WorldModel
  Trajectory := Trajectory
  Available := fun {K K'} => Available
  Adm24 := Adm24
  UsedByRel := fun {K K'} => UsedByRel
  UsedByDist := fun {K K'} => UsedByDist
  DiscriminatesRel := fun {K K'} => DiscriminatesRel
  DiscriminatesDist := fun {K K'} => DiscriminatesDist
  RelProvenance := fun {K} => RelProvenance
  DistProvenance := fun {K} => DistProvenance
  relStanding := fun {K K'} => relStanding
  distStanding := fun {K K'} => distStanding
  RequiredRel := fun {K K'} => RequiredRel
  RequiredDist := fun {K K'} => RequiredDist
  physicalEnergy := fun {K K'} => physicalEnergy
  representationEffort := fun {K K'} => representationEffort
  actionEffort := fun {K K'} => actionEffort
  excessForcing := fun {K K'} => excessForcing
  genenergy := fun {K K'} => genenergy
  DisqualifyingExcessForcing := fun {K K'} => DisqualifyingExcessForcing
  ParticipationOpen := fun {K K'} => ParticipationOpen
  ConsequenceAnswerable := fun {K K'} => ConsequenceAnswerable
  LawfulAppropriate := fun {K K'} => LawfulAppropriate
  ExtensionOf := ExtensionOf
  AlignedExtension := AlignedExtension
  ContinuingContactable := fun {K K'} => ContinuingContactable
  evaluatorOf := fun {K K'} => evaluatorOf
  DoctrineBound := DoctrineBound
  provenanceOfMovement := fun {K K'} => provenanceOfMovement
  generationKindOf := fun {K K'} => generationKindOf
  ModelSufficient := ModelSufficient
  CorrectConsequenceLaw := CorrectConsequenceLaw
  NoOmittedDisturbance := NoOmittedDisturbance
  ConsequenceOf := ConsequenceOf
  HarmonicOutcome := HarmonicOutcome
  Contactability := Contactability
  RelationalOpenness := RelationalOpenness
  PreservedDistinctions := PreservedDistinctions
  ReceptiveAttention := ReceptiveAttention
  DifferentiationWithCoherence := DifferentiationWithCoherence
  LowUnnecessaryForcing := LowUnnecessaryForcing
  TrajConsequenceAnswerable := TrajConsequenceAnswerable
  InterfaceOpenness := InterfaceOpenness
  SelfWeavingPlasticity := SelfWeavingPlasticity
  ContactExclusion := ContactExclusion
  Recurrence := Recurrence
  InterfaceNarrowing := InterfaceNarrowing
  ForcedVelocity := ForcedVelocity
  StaleForwardMotion := StaleForwardMotion
  PivotUnavailable := PivotUnavailable
  ForceResidueEvidence := ForceResidueEvidence
  AvailableAt := fun {K} => AvailableAt

@[reducible] def doctrine3 : sig3.SoulDoctrine := ()

/-- `bridgeMove`'s explicit `Adm25Witness`: the full diagram (a, b, z all
`full`) is admissible — this is the positive half of Fourthness (25h
§11's "full diagram permits/justifies bridge movement"). -/
def bridgeMoveAdm : Adm25Witness sig3 doctrine3 bridgeMove :=
  { available := trivial
    adm24 := trivial
    relFloors := fun r => match r with | .a => fun _ => rfl | .b => fun _ => rfl | .z => fun _ => rfl
    precFloors := fun d => nomatch d
    noDisqualifyingForcing := fun h => h
    participationOpen := trivial
    consequenceAnswerable := trivial }

/-- Fourthness positive half, relation `a`: deleting `a`'s full standing
(holding `b` full) breaks `AllRelFloors`, via Core's generic T05
(`rel_floor_noncompensatory`), hence blocks the bridge (25h §11). -/
theorem m3_missingA_fails_relfloor : ¬ AllRelFloors sig3 bridgeMoveMissingA :=
  rel_floor_noncompensatory sig3 bridgeMoveMissingA Relation.b Relation.a rfl trivial (by decide)

/-- Fourthness positive half, relation `b`: symmetric to `a`. -/
theorem m3_missingB_fails_relfloor : ¬ AllRelFloors sig3 bridgeMoveMissingB :=
  rel_floor_noncompensatory sig3 bridgeMoveMissingB Relation.a Relation.b rfl trivial (by decide)

/-- Fourthness negative control: deleting the DECORATIVE relation `z`
(while `a`/`b` remain full) does NOT break `AllRelFloors` — `z` is not
required, so its standing is irrelevant to the floor. This is what proves
Fourthness tracks material counterfactual bite, not raw relation count
(25h §11). -/
theorem m3_missingZ_not_penalized : AllRelFloors sig3 bridgeMoveMissingZ := by
  intro r hreq
  match r, hreq with
  | .a, _ => rfl
  | .b, _ => rfl
  | .z, hreq => exact (hreq : False).elim

/-- T22 (25h §11, Fourthness non-vacuity): both material relations are
independently load-bearing, and the decorative relation is provably not,
bundled with the positive fully-admissible witness. -/
theorem T22_fourthness :
    Nonempty (Adm25Witness sig3 doctrine3 bridgeMove) ∧
      (¬ AllRelFloors sig3 bridgeMoveMissingA) ∧
      (¬ AllRelFloors sig3 bridgeMoveMissingB) ∧
      AllRelFloors sig3 bridgeMoveMissingZ :=
  ⟨⟨bridgeMoveAdm⟩, m3_missingA_fails_relfloor, m3_missingB_fails_relfloor, m3_missingZ_not_penalized⟩

/-- Consequently `bridgeMoveMissingA`/`...MissingB` admit no lawful
`ReadApp` reading at all (Core's generic T09 instantiated here). -/
theorem m3_missingA_no_readapp : ∀ A, ¬ ReadApp sig3 doctrine3 bridgeMoveMissingA A :=
  readapp_rel_floor sig3 doctrine3 bridgeMoveMissingA m3_missingA_fails_relfloor

theorem m3_missingB_no_readapp : ∀ A, ¬ ReadApp sig3 doctrine3 bridgeMoveMissingB A :=
  readapp_rel_floor sig3 doctrine3 bridgeMoveMissingB m3_missingB_fails_relfloor

/-- T23 (25h §12, second interface-growth witness): `bridgeMode` is new
at `Bridge`, unavailable at either local context beforehand. -/
theorem T23_interface_growth_from_LA :
    InterfaceChange sig3 (Mode.bridgeMode (K := Cut.LA)) (Mode.bridgeMode (K := Cut.Bridge)) :=
  ⟨fun h => h, trivial⟩

theorem T23_interface_growth_from_LB :
    InterfaceChange sig3 (Mode.bridgeMode (K := Cut.LB)) (Mode.bridgeMode (K := Cut.Bridge)) :=
  ⟨fun h => h, trivial⟩

theorem T23_interface_growth_not_faked :
    ¬ AvailableAt (Mode.bridgeMode (K := Cut.LA)) ∧ ¬ AvailableAt (Mode.bridgeMode (K := Cut.LB)) :=
  ⟨fun h => h, fun h => h⟩

/-- `localMoveB`'s `Adm25Witness`: `LB` has NO relations at all
(`Relation LB` is empty), so its floors are vacuously satisfied — this
local context reaches `Bridge` entirely on its own terms, independently
of anything proved about `LA`/`bridgeMove`. -/
def localMoveBAdm : Adm25Witness sig3 doctrine3 localMoveB :=
  { available := trivial
    adm24 := trivial
    relFloors := fun r => nomatch r
    precFloors := fun d => nomatch d
    noDisqualifyingForcing := fun h => h
    participationOpen := trivial
    consequenceAnswerable := trivial }

/-- T24 (25h §17, global-representation adversary): `Bridge` is reached
by two INDEPENDENTLY admissible local movements (`bridgeMove` from `LA`,
`localMoveB` from `LB`), and `WorldModel` — the only place a
`globalMasterModel`-shaped premise could hide — is UNINHABITED in this
Sig (stated as `WorldModel → False`, the no-Mathlib-dependency
equivalent of `IsEmpty WorldModel`). No proof above ever constructs or
consumes a `WorldModel` value; this theorem records that fact positively. -/
theorem T24_no_global_model_required :
    (WorldModel → False) ∧
      Nonempty (Adm25Witness sig3 doctrine3 bridgeMove) ∧
      Nonempty (Adm25Witness sig3 doctrine3 localMoveB) :=
  ⟨fun w => w.elim, ⟨bridgeMoveAdm⟩, ⟨localMoveBAdm⟩⟩

end M3

end Inv25
