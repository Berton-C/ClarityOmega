/-!
# ClarityOmega WMK lawful-attachment hardening core

This file is a bounded Lean 4 encoding of the theorem-bearing corrections found
by the 0g adversarial review of the exact 0f signature.  It intentionally does
not re-open the mathematical survey and does not attempt to encode the full
virtual equipment, quantaloid, or Soul doctrine.

Status: proof-assistant source prepared for Lean 4 kernel checking.  The present
execution environment did not contain a Lean runtime, so this source has not
been kernel-checked here.  The companion Python adversarial search and
PyProver proof run are executable and were run successfully.
-/

namespace ClarityOmega.WMK.Hardened

universe u v

/-! ## H0: direct contact is sealed by construction -/

section ContactSeal

variable (ContactRef Event Datum : Type u)

structure ContactSeal where
  ref : ContactRef
  event : Event

inductive Provenance where
  | contact (seal : ContactSeal ContactRef Event)
  | testimony (event : Event)
  | memory (event : Event)
  | infer (event : Event) (parents : List (Provenance ContactRef Event))
  | generate (event : Event) (parents : List (Provenance ContactRef Event))
  | selfTrace (event : Event) (parents : List (Provenance ContactRef Event))

inductive DirectContact : Provenance ContactRef Event → Prop where
  | intro (seal : ContactSeal ContactRef Event) :
      DirectContact (Provenance.contact seal)

structure ContactRecord where
  datum : Datum
  seal : ContactSeal ContactRef Event

variable {ContactRef Event Datum}

 theorem infer_not_direct
    (event : Event) (parents : List (Provenance ContactRef Event)) :
    ¬ DirectContact (Provenance.infer event parents) := by
  intro h
  cases h

 theorem generate_not_direct
    (event : Event) (parents : List (Provenance ContactRef Event)) :
    ¬ DirectContact (Provenance.generate event parents) := by
  intro h
  cases h

 theorem selfTrace_not_direct
    (event : Event) (parents : List (Provenance ContactRef Event)) :
    ¬ DirectContact (Provenance.selfTrace event parents) := by
  intro h
  cases h

 theorem contact_record_has_seal
    (r : ContactRecord ContactRef Event Datum) :
    Nonempty (ContactSeal ContactRef Event) := by
  exact ⟨r.seal⟩

end ContactSeal

/-! ## H1: no authority from a closure-only basis -/

 theorem no_authority_from_closure_only
    {Authority ClosureOnly Later Material OutsideSelfGen : Prop}
    (authorityBasis : Authority → Later ∧ Material ∧ OutsideSelfGen)
    (closureHasNoBasis : ClosureOnly → ¬ (Later ∧ Material ∧ OutsideSelfGen)) :
    ClosureOnly → ¬ Authority := by
  intro hClosure hAuthority
  exact closureHasNoBasis hClosure (authorityBasis hAuthority)

/-! ## H2: authority evidence exposes the guarded material basis -/

structure AuthorityEvidence
    (Later Material OutsideSelfGen SealedContact : Prop) where
  later : Later
  material : Material
  outsideSelfGen : OutsideSelfGen
  sealedContact : SealedContact

structure Authoritative
    (Later Material OutsideSelfGen SealedContact : Prop) where
  evidence : AuthorityEvidence Later Material OutsideSelfGen SealedContact

 theorem authority_is_guarded
    {Later Material OutsideSelfGen SealedContact : Prop}
    (a : Authoritative Later Material OutsideSelfGen SealedContact) :
    Later ∧ Material ∧ OutsideSelfGen ∧ SealedContact := by
  exact ⟨a.evidence.later, a.evidence.material,
    a.evidence.outsideSelfGen, a.evidence.sealedContact⟩

/-! ## H3: anchor and history extension are proof-carrying -/

section Conservativity

variable (Frame Contact Grade : Type u)

structure AnchorState where
  lookup : Frame → Contact → Option Grade

structure AnchorExtension
    (pre post : AnchorState Frame Contact Grade) where
  preserveOld : ∀ (f : Frame) (c : Contact) (g : Grade),
    pre.lookup f c = some g → post.lookup f c = some g

variable {Frame Contact Grade}

 theorem anchor_conservative
    {pre post : AnchorState Frame Contact Grade}
    (ext : AnchorExtension Frame Contact Grade pre post)
    {f : Frame} {c : Contact} {g : Grade}
    (h : pre.lookup f c = some g) :
    post.lookup f c = some g := by
  exact ext.preserveOld f c g h

variable (Record : Type v)

structure HistoryState where
  contains : Record → Prop

structure HistoryExtension
    (pre post : HistoryState Record) where
  preserveOld : ∀ r : Record, pre.contains r → post.contains r

variable {Record}

 theorem history_conservative
    {pre post : HistoryState Record}
    (ext : HistoryExtension Record pre post)
    {r : Record}
    (h : pre.contains r) :
    post.contains r := by
  exact ext.preserveOld r h

end Conservativity

/-! ## H4: loss and recovery remain context-indexed -/

section Recovery

variable (Distinction LossContext Witness : Type u)

structure LossKey where
  distinction : Distinction
  context : LossContext

structure RecoveryRecord where
  key : LossKey Distinction LossContext
  witness : Witness

structure AvailabilityTransition where
  recovery : RecoveryRecord Distinction LossContext Witness

variable {Distinction LossContext Witness}

 theorem availability_transition_has_witness
    (t : AvailabilityTransition Distinction LossContext Witness) :
    ∃ w : Witness, t.recovery.witness = w := by
  exact ⟨t.recovery.witness, rfl⟩

end Recovery

/-! ## H5: lifecycle evidence is non-collapsible -/

inductive Stage where
  | candidate
  | probeEligible
  | authoritative
  | durable

inductive Attained (Frame : Type u) (f : Frame) : Stage → Type u where
  | candidate : Attained Frame f Stage.candidate
  | probe : Attained Frame f Stage.candidate →
      Attained Frame f Stage.probeEligible
  | authorityFromCandidate : Attained Frame f Stage.candidate →
      Attained Frame f Stage.authoritative
  | authorityFromProbe : Attained Frame f Stage.probeEligible →
      Attained Frame f Stage.authoritative
  | durable : Attained Frame f Stage.authoritative →
      Attained Frame f Stage.durable

 theorem durable_contains_authority
    {Frame : Type u} {f : Frame}
    (d : Attained Frame f Stage.durable) :
    Attained Frame f Stage.authoritative := by
  cases d with
  | durable a => exact a

/-! ## H6: branch-local transaction atomicity, without false determinism -/

section Transaction

variable (Event : Type u)

structure CarrierState where
  inCut : Event → Prop

def Enabled (s : CarrierState Event) (e : Event) : Prop :=
  ¬ s.inCut e

structure Commit (pre : CarrierState Event) (e : Event) where
  post : CarrierState Event
  eventPresent : post.inCut e

variable {Event}

 theorem no_sequential_recommit
    {pre : CarrierState Event} {e : Event}
    (c : Commit Event pre e) :
    ¬ Enabled Event c.post e := by
  intro hEnabled
  exact hEnabled c.eventPresent

/-!
No theorem of the form

  Commit pre e → Commit pre e → successors are equal

is asserted.  The original C10 uniqueness wording is intentionally weakened:
branch-local atomicity does not erase alternative lawful transactions.
-/

end Transaction

/-! ## H7: global plurality and scoped joint use -/

section JointUse

variable (Frame Action : Type u)

inductive JointWitness (left right : Frame) (action : Action) where
  | localCompatibility
  | retainedTension

structure JointUse (left right : Frame) (action : Action) where
  witness : JointWitness Frame Action left right action

variable {Frame Action}

 theorem joint_use_has_scoped_witness
    {left right : Frame} {action : Action}
    (j : JointUse Frame Action left right action) :
    Nonempty (JointWitness Frame Action left right action) := by
  exact ⟨j.witness⟩

end JointUse

/-! ## H8: retrospective reorganization evidence contains causal bite -/

structure ReorganizationEvidence
    (ExercisedReach ReturnedContact ConsequenceUptake : Prop) where
  exercised : ExercisedReach
  returnedContact : ReturnedContact
  consequenceUptake : ConsequenceUptake

 theorem reorganization_has_returned_contact
    {ExercisedReach ReturnedContact ConsequenceUptake : Prop}
    (r : ReorganizationEvidence ExercisedReach ReturnedContact ConsequenceUptake) :
    ReturnedContact := by
  exact r.returnedContact

/-! ## H9: CarrierOpen and living-inquiry discharge stay different judgments -/

structure CarrierOpenEvidence (LiveGroundedItem : Type u) where
  item : LiveGroundedItem

structure DischargeEvidence (SoulRoute ContactRoute : Type u) where
  soul : SoulRoute
  contact : ContactRoute

/-!
There is deliberately no function from CarrierOpenEvidence, its absence, or a
carrier-completeness witness to DischargeEvidence.  This is a signature audit,
not a semantic proof that runtime action can never become representation-
sovereign; that stronger obligation remains a Gate E intervention test.
-/

end ClarityOmega.WMK.Hardened
