import Std

/-!
# ClarityOmega Inquiry-24 canonical hardened lawful-attachment kernel

This file is the checksum-frozen Lean 4 mechanization target for 0h.
It contains no proof holes, no Boolean proof fields, no string-valued writer
permissions, and no optional authority route.  The central authority package is
proof-bearing by construction.
-/

namespace ClarityOmega.WMK.Canonical

universe u v

/-! ## K0–K1: Soul-doctrine boundary, proto-time, and typed derivation -/

structure ProtoTime (Event : Type u) where
  before : Event → Event → Prop
  irrefl : ∀ e, ¬ before e e
  trans : ∀ {a b c}, before a b → before b c → before a c

inductive DerivationKind where
  | internalGeneration
  | render
  | inference
  | memoryRecall
  | actionExecution
  | worldReturn
  | testimony
  deriving DecidableEq

structure DerivationEdge (Event : Type u) where
  src : Event
  dst : Event
  kind : DerivationKind

inductive InternalKind : DerivationKind → Prop where
  | generated : InternalKind .internalGeneration
  | rendered : InternalKind .render

structure SoulDoctrine
    (Frame Contact Witness Live Event : Type u) where
  MaterialTo : Contact → Witness → Live → Prop
  LiveContinuation : Live → Frame → Witness → Prop
  AdmitCandidate : Frame → Witness → Event → Prop
  AdmitProbe : Frame → Witness → Event → Prop
  AdmitAuthority : Frame → Witness → Event → Prop
  AdmitDurability : Frame → Witness → Event → Prop
  AdmitDischarge : Live → Event → Prop

structure WellFormedSoulDoctrine
    {Frame Contact Witness Live Event : Type u}
    (D : SoulDoctrine Frame Contact Witness Live Event) where
  materialContinuesLiveInquiry :
    ∀ {c w l}, D.MaterialTo c w l → ∃ f, D.LiveContinuation l f w

/-! ## K2: provenance is a proof tree; no flat rank may erase lineage -/

structure ContactSeal
    (Event Contact Route : Type u) where
  contact : Contact
  event : Event
  route : Route

inductive Provenance
    (Event Contact Route Source : Type u) : Type u where
  | contact (sealF : ContactSeal Event Contact Route)
  | testimony (source : Source) (event : Event)
  | memory (event : Event) (parent : Provenance Event Contact Route Source)
  | infer (event : Event) (parents : List (Provenance Event Contact Route Source))
  | generate (event : Event) (parents : List (Provenance Event Contact Route Source))
  | selfTrace (event : Event) (parents : List (Provenance Event Contact Route Source))

inductive DirectContact
    {Event Contact Route Source : Type u} :
    Provenance Event Contact Route Source → Prop where
  | intro (sealF : ContactSeal Event Contact Route) :
      DirectContact (.contact sealF)

theorem infer_not_direct
    {Event Contact Route Source : Type u}
    (e : Event)
    (ps : List (Provenance Event Contact Route Source)) :
    ¬ DirectContact (.infer e ps) := by
  intro h
  cases h

theorem generate_not_direct
    {Event Contact Route Source : Type u}
    (e : Event)
    (ps : List (Provenance Event Contact Route Source)) :
    ¬ DirectContact (.generate e ps) := by
  intro h
  cases h

inductive ContainsProvenance
    {Event Contact Route Source : Type u}
    (old : Provenance Event Contact Route Source) :
    Provenance Event Contact Route Source → Prop where
  | refl : ContainsProvenance old old
  | memory {e p} : ContainsProvenance old p → ContainsProvenance old (.memory e p)
  | infer {e ps p} : p ∈ ps → ContainsProvenance old p →
      ContainsProvenance old (.infer e ps)
  | generate {e ps p} : p ∈ ps → ContainsProvenance old p →
      ContainsProvenance old (.generate e ps)
  | selfTrace {e ps p} : p ∈ ps → ContainsProvenance old p →
      ContainsProvenance old (.selfTrace e ps)

structure Standing
    (Event Contact Route Source Warrant Pressure Freshness : Type u) where
  provenance : Provenance Event Contact Route Source
  warrant : Warrant
  support : Event → Prop
  pressure : Pressure
  freshness : Freshness

structure StandingTransform
    {Event Contact Route Source Warrant Pressure Freshness : Type u}
    (old new : Standing Event Contact Route Source Warrant Pressure Freshness) where
  lineage : ContainsProvenance old.provenance new.provenance

/-! ## K3–K4: raw contact fields and partial frame formation -/

structure RawField
    (Event Context Node RawStanding : Type u) where
  event : Event
  context : Context
  relates : Node → Node → RawStanding

structure FramePresentation
    (Frame Context Node Resolution Competence : Type u) where
  frame : Frame
  context : Context
  inDomain : Node → Prop
  resolution : Resolution
  competence : Competence

structure FrameFormation
    {Event Context RawNode RawStanding Frame FrameNode Resolution Competence : Type u}
    (G : RawField Event Context RawNode RawStanding)
    (F : FramePresentation Frame Context FrameNode Resolution Competence) where
  formationEvent : Event
  represented : RawNode → Prop
  omitted : RawNode → Prop
  mapNode : ∀ n, represented n → FrameNode
  partition : ∀ n, represented n ∨ omitted n
  disjoint : ∀ n, represented n → ¬ omitted n
  sameEvent : formationEvent = G.event
  sameContext : F.context = G.context

/-! ## K5–K7: equipment-facing frame relations and conservative anchor growth -/

structure FrameRelation (Frame Grade : Type u) where
  source : Frame
  target : Frame
  fidelity : Grade
  pathEffort : Nat

structure AnchorState (Frame Contact Grade : Type u) where
  assigns : Frame → Contact → Grade → Prop
  singleValued : ∀ {f c g₁ g₂}, assigns f c g₁ → assigns f c g₂ → g₁ = g₂

structure AnchorExtension
    {Frame Contact Grade : Type u}
    (pre post : AnchorState Frame Contact Grade) where
  preserveOld : ∀ f c g, pre.assigns f c g → post.assigns f c g

theorem anchor_conservative
    {Frame Contact Grade : Type u}
    {pre post : AnchorState Frame Contact Grade}
    (ext : AnchorExtension pre post)
    {f c g}
    (h : pre.assigns f c g) :
    post.assigns f c g := by
  exact ext.preserveOld f c g h

/-! ## K6–K8: formal carrier visibility is not living-question exhaustion -/

structure LiveItem (Live Contact Event Pressure : Type u) where
  id : Live
  groundedIn : Contact → Prop
  activeAt : Event → Prop
  pressure : Pressure

structure CarrierOpenEvidence (LiveGrounded : Type u) where
  item : LiveGrounded

structure DischargeEvidence (SoulRoute ContactRoute : Type u) where
  soul : SoulRoute
  contact : ContactRoute

/-!
There is deliberately no function from absence of `CarrierOpenEvidence`, from
carrier closure, or from frame completeness to `DischargeEvidence`.
-/

/-! ## K9–K11: witness, lifecycle, derived self-generation, and authority -/

structure ProspectiveWitness
    (Frame Witness Event Live Action : Type u) where
  frame : Frame
  id : Witness
  formationEvent : Event
  assemblyEvent : Event
  continues : Live → Prop
  predicts : Action → Prop
  witnessSupport : Event → Prop

inductive SelfGenReach
    {Event Frame Witness Live Action : Type u}
    (internalEdge : Event → Event → Prop)
    (w : ProspectiveWitness Frame Witness Event Live Action) : Event → Prop where
  | formation : SelfGenReach internalEdge w w.formationEvent
  | assembly : SelfGenReach internalEdge w w.assemblyEvent
  | step {a b} : SelfGenReach internalEdge w a → internalEdge a b →
      SelfGenReach internalEdge w b

structure ContactRecord
    (Event Contact Route World Observation : Type u)
    (observe : Route → World → Observation) where
  contact : Contact
  event : Event
  world : World
  datum : Observation
  sealF : ContactSeal Event Contact Route
  route : Route
  generated : observe route world = datum
  sealedRef : sealF.contact = contact
  sealedEvent : sealF.event = event
  sealedRoute : sealF.route = route

structure ProbeEligible
    {Event Frame Witness Live Action : Type u}
    (T : ProtoTime Event)
    (reverses : Action → Action → Prop)
    (w : ProspectiveWitness Frame Witness Event Live Action)
    (frame : Frame)
    (probeEvent : Event)
    (action : Action) where
  sameFrame : frame = w.frame
  afterFormation : T.before w.formationEvent probeEvent ∨ w.formationEvent = probeEvent
  budget : Nat
  budgetPositive : 0 < budget
  rollbackAction : Action
  rollbackProof : reverses action rollbackAction

structure PriorProbe
    {Event Frame Witness Live Action : Type u}
    (T : ProtoTime Event)
    (reverses : Action → Action → Prop)
    (w : ProspectiveWitness Frame Witness Event Live Action)
    (frame : Frame)
    (authorityEvent : Event) where
  probeEvent : Event
  action : Action
  proof : ProbeEligible T reverses w frame probeEvent action
  beforeAuthority : T.before probeEvent authorityEvent

structure GovernedRouteEvidence
    {Event Contact Route World Observation Writer : Type u}
    (observe : Route → World → Observation)
    (record : ContactRecord Event Contact Route World Observation observe)
    (contactWriter : Route → Writer → Prop)
    (writer : Writer) where
  governed : contactWriter record.route writer

structure Discriminates
    {Route World Observation Live : Type u}
    (observe : Route → World → Observation)
    (relevant : Live → World → World → Prop)
    (route : Route)
    (live : Live) where
  left : World
  right : World
  relevantPair : relevant live left right
  differs : observe route left ≠ observe route right

structure FreshFor
    {Event Contact Witness Live : Type u}
    (T : ProtoTime Event)
    (contactSupport : Contact → Event → Prop)
    (materialContribution : Event → Contact → Witness → Live → Prop)
    (witnessSupport : Witness → Event → Prop)
    (contact : Contact)
    (witness : Witness)
    (live : Live)
    (assembly authority : Event) where
  contributionEvent : Event
  afterAssembly : T.before assembly contributionEvent
  byAuthority : T.before contributionEvent authority ∨ contributionEvent = authority
  inContactSupport : contactSupport contact contributionEvent
  notOldSupport : ¬ witnessSupport witness contributionEvent
  contributes : materialContribution contributionEvent contact witness live

structure IndependentOf
    {Event Frame Witness Live Action Contact : Type u}
    (internalEdge : Event → Event → Prop)
    (w : ProspectiveWitness Frame Witness Event Live Action)
    (contactEvent : Contact → Event)
    (contact : Contact) where
  outside : ¬ SelfGenReach internalEdge w (contactEvent contact)

structure AuthorityPackage
    {Event Frame Contact Route World Observation Witness Live Action Writer : Type u}
    (T : ProtoTime Event)
    (reverses : Action → Action → Prop)
    (D : SoulDoctrine Frame Contact Witness Live Event)
    (observe : Route → World → Observation)
    (relevant : Live → World → World → Prop)
    (contactWriter : Route → Writer → Prop)
    (contactSupport : Contact → Event → Prop)
    (materialContribution : Event → Contact → Witness → Live → Prop)
    (witnessSupport : Witness → Event → Prop)
    (internalEdge : Event → Event → Prop)
    (contactEvent : Contact → Event)
    (w : ProspectiveWitness Frame Witness Event Live Action)
    (frame : Frame)
    (authorityEvent : Event) where
  doctrineLawful : WellFormedSoulDoctrine D
  priorProbe : PriorProbe T reverses w frame authorityEvent
  contactRecord : ContactRecord Event Contact Route World Observation observe
  contactAtAuthority : contactRecord.event = authorityEvent
  contactWriterValue : Writer
  governedRoute : GovernedRouteEvidence observe contactRecord contactWriter contactWriterValue
  live : Live
  continued : w.continues live
  discriminates : Discriminates observe relevant contactRecord.route live
  material : D.MaterialTo contactRecord.contact w.id live
  fresh : FreshFor T contactSupport materialContribution witnessSupport
    contactRecord.contact w.id live w.assemblyEvent authorityEvent
  independent : IndependentOf internalEdge w contactEvent contactRecord.contact
  soulAdmits : D.AdmitAuthority frame w.id authorityEvent

inductive Authoritative
    {Event Frame Contact Route World Observation Witness Live Action Writer : Type u}
    (T : ProtoTime Event)
    (reverses : Action → Action → Prop)
    (D : SoulDoctrine Frame Contact Witness Live Event)
    (observe : Route → World → Observation)
    (relevant : Live → World → World → Prop)
    (contactWriter : Route → Writer → Prop)
    (contactSupport : Contact → Event → Prop)
    (materialContribution : Event → Contact → Witness → Live → Prop)
    (witnessSupport : Witness → Event → Prop)
    (internalEdge : Event → Event → Prop)
    (contactEvent : Contact → Event)
    (w : ProspectiveWitness Frame Witness Event Live Action)
    (frame : Frame)
    (authorityEvent : Event) : Type u where
  | attach
      (pkg : AuthorityPackage T reverses D observe relevant contactWriter contactSupport
        materialContribution witnessSupport internalEdge contactEvent w frame authorityEvent) :
      Authoritative T reverses D observe relevant contactWriter contactSupport
        materialContribution witnessSupport internalEdge contactEvent w frame authorityEvent

/-- The central 0h theorem: authority exposes every required basis. -/
theorem authoritative_implies_governing_package
    {Event Frame Contact Route World Observation Witness Live Action Writer : Type u}
    {T : ProtoTime Event}
    {reverses : Action → Action → Prop}
    {D : SoulDoctrine Frame Contact Witness Live Event}
    {observe : Route → World → Observation}
    {relevant : Live → World → World → Prop}
    {contactWriter : Route → Writer → Prop}
    {contactSupport : Contact → Event → Prop}
    {materialContribution : Event → Contact → Witness → Live → Prop}
    {witnessSupport : Witness → Event → Prop}
    {internalEdge : Event → Event → Prop}
    {contactEvent : Contact → Event}
    {w : ProspectiveWitness Frame Witness Event Live Action}
    {frame : Frame}
    {authorityEvent : Event}
    (a : Authoritative T reverses D observe relevant contactWriter contactSupport
      materialContribution witnessSupport internalEdge contactEvent w frame authorityEvent) :
    ∃ (pp : PriorProbe T reverses w frame authorityEvent)
      (record : ContactRecord Event Contact Route World Observation observe)
      (writer : Writer)
      (gr : GovernedRouteEvidence observe record contactWriter writer)
      (live : Live)
      (disc : Discriminates observe relevant record.route live)
      (mat : D.MaterialTo record.contact w.id live)
      (fresh : FreshFor T contactSupport materialContribution witnessSupport
        record.contact w.id live w.assemblyEvent authorityEvent)
      (indep : IndependentOf internalEdge w contactEvent record.contact),
      record.event = authorityEvent := by
  cases a with
  | attach pkg =>
      exact ⟨pkg.priorProbe, pkg.contactRecord, pkg.contactWriterValue,
        pkg.governedRoute, pkg.live, pkg.discriminates, pkg.material,
        pkg.fresh, pkg.independent, pkg.contactAtAuthority⟩

inductive Stage where
  | candidate
  | probeEligible
  | authoritative
  | durable

inductive Attained
    {Event Frame Contact Route World Observation Witness Live Action Writer : Type u}
    (T : ProtoTime Event)
    (reverses : Action → Action → Prop)
    (D : SoulDoctrine Frame Contact Witness Live Event)
    (observe : Route → World → Observation)
    (relevant : Live → World → World → Prop)
    (contactWriter : Route → Writer → Prop)
    (contactSupport : Contact → Event → Prop)
    (materialContribution : Event → Contact → Witness → Live → Prop)
    (witnessSupport : Witness → Event → Prop)
    (internalEdge : Event → Event → Prop)
    (contactEvent : Contact → Event)
    (w : ProspectiveWitness Frame Witness Event Live Action)
    (frame : Frame) : Stage → Type u where
  | candidate : D.AdmitCandidate frame w.id w.formationEvent →
      Attained T reverses D observe relevant contactWriter contactSupport materialContribution
        witnessSupport internalEdge contactEvent w frame .candidate
  | probe {e a} :
      Attained T reverses D observe relevant contactWriter contactSupport materialContribution
        witnessSupport internalEdge contactEvent w frame .candidate →
      ProbeEligible T reverses w frame e a →
      D.AdmitProbe frame w.id e →
      Attained T reverses D observe relevant contactWriter contactSupport materialContribution
        witnessSupport internalEdge contactEvent w frame .probeEligible
  | authority {e} :
      Attained T reverses D observe relevant contactWriter contactSupport materialContribution
        witnessSupport internalEdge contactEvent w frame .probeEligible →
      Authoritative T reverses D observe relevant contactWriter contactSupport materialContribution
        witnessSupport internalEdge contactEvent w frame e →
      Attained T reverses D observe relevant contactWriter contactSupport materialContribution
        witnessSupport internalEdge contactEvent w frame .authoritative
  | durable :
      Attained T reverses D observe relevant contactWriter contactSupport materialContribution
        witnessSupport internalEdge contactEvent w frame .authoritative →
      D.AdmitDurability frame w.id w.assemblyEvent →
      Attained T reverses D observe relevant contactWriter contactSupport materialContribution
        witnessSupport internalEdge contactEvent w frame .durable

/-! ## K12: immutable history and event-scoped interpretation use -/

structure HistoryState (Record : Type u) where
  contains : Record → Prop

structure HistoryExtension
    {Record : Type u}
    (pre post : HistoryState Record) where
  preserveOld : ∀ r, pre.contains r → post.contains r

theorem history_conservative
    {Record : Type u}
    {pre post : HistoryState Record}
    (ext : HistoryExtension pre post)
    {r : Record}
    (h : pre.contains r) :
    post.contains r := by
  exact ext.preserveOld r h

structure InterpretationRecord
    (Frame HistoryRef Interpretation Expression Event : Type u) where
  frame : Frame
  history : HistoryRef
  id : Interpretation
  expression : Expression
  event : Event

structure InterpretationUse
    {Frame HistoryRef Interpretation Expression Event Scope Action SoulJudgment : Type u}
    (record : InterpretationRecord Frame HistoryRef Interpretation Expression Event) where
  event : Event
  scope : Scope
  action : Action
  soul : SoulJudgment

/-! ## K13: context-indexed loss and semantic reintroduction -/

structure LossKey (Distinction Context : Type u) where
  distinction : Distinction
  context : Context

inductive ReintroductionWitness
    (Distinction Context Contact Frame SideInfo Route : Type u)
    (CarriesContact : Contact → Distinction → Prop)
    (CarriesFrame : Frame → Distinction → Prop)
    (RetainedFor : SideInfo → Distinction → Context → Prop)
    (RestoresRoute : Route → Distinction → Context → Prop)
    (d : Distinction)
    (ctx : Context) : Type u where
  | renewedContact (c : Contact) (proof : CarriesContact c d)
  | otherFrame (f : Frame) (proof : CarriesFrame f d)
  | retainedSideInfo (s : SideInfo) (proof : RetainedFor s d ctx)
  | reversibleRoute (r : Route) (proof : RestoresRoute r d ctx)

structure AvailabilityTransition
    {Distinction Context Contact Frame SideInfo Route Event : Type u}
    (CarriesContact : Contact → Distinction → Prop)
    (CarriesFrame : Frame → Distinction → Prop)
    (RetainedFor : SideInfo → Distinction → Context → Prop)
    (RestoresRoute : Route → Distinction → Context → Prop)
    (d : Distinction)
    (ctx : Context) where
  event : Event
  witness : ReintroductionWitness Distinction Context Contact Frame SideInfo Route
    CarriesContact CarriesFrame RetainedFor RestoresRoute d ctx

theorem availability_has_semantic_witness
    {Distinction Context Contact Frame SideInfo Route Event : Type u}
    {CarriesContact : Contact → Distinction → Prop}
    {CarriesFrame : Frame → Distinction → Prop}
    {RetainedFor : SideInfo → Distinction → Context → Prop}
    {RestoresRoute : Route → Distinction → Context → Prop}
    {d : Distinction}
    {ctx : Context}
    (t : AvailabilityTransition (Event := Event) CarriesContact CarriesFrame RetainedFor
      RestoresRoute d ctx) :
    Nonempty (ReintroductionWitness Distinction Context Contact Frame SideInfo Route
      CarriesContact CarriesFrame RetainedFor RestoresRoute d ctx) := by
  exact ⟨t.witness⟩

/-! ## K14–K15: prospective/retrospective affordance and computed stuck evidence -/

structure RetrospectiveReach
    (Frame Action Contact Event : Type u) where
  frame : Frame
  predicted : Action
  exercisedAt : Event
  returnedContact : Contact
  changedNext : Action

structure StuckEvidence
    (Frame Event World Route Observation Action Effect : Type u)
    (observe : Route → World → Observation)
    (update : Frame → Observation → Action)
    (demand : Frame → Event → Prop)
    (discrepancy : Frame → Event → Prop)
    (reinforced : Frame → Event → Prop)
    (reachable : Frame → Action → Prop)
    (effectOf : Action → Effect) where
  frame : Frame
  event : Event
  left : World
  right : World
  route : Route
  demandProof : demand frame event
  discrepancyProof : discrepancy frame event
  recurrentEffect : Effect
  recurrenceEvents : List Event
  recurrenceActions : List Action
  recurrenceNonempty : recurrenceActions ≠ []
  sameEffect : ∀ a, a ∈ recurrenceActions → effectOf a = recurrentEffect
  reinforcementProof : reinforced frame event
  nonopeningAction : Action
  nonopeningProof : ¬ reachable frame nonopeningAction
  contactDiscriminates : observe route left ≠ observe route right
  distinctionDeathProof :
    update frame (observe route left) = update frame (observe route right)

/-! ## K16: global plurality; joint use requires a scoped witness -/

inductive JointWitness (Frame Action : Type u) (left right : Frame) (action : Action) where
  | localCompatibility
  | retainedTension

structure JointUse
    {Frame Action : Type u}
    (left right : Frame)
    (action : Action) where
  witness : JointWitness Frame Action left right action

/-! ## K17: closed writer sum and branch-local atomicity -/

inductive WriterCapability where
  | founder
  | contactRecorder
  | contactRecovery
  | actionRecorder
  | consequenceRecorder
  | traceRecorder
  | frameFormer
  | candidateAdmitter
  | probeAuthorizer
  | authorityAttacher
  | durabilityPromoter
  | interpretationAppender
  | interpretationUseAppender
  | lossRecorder
  | reintroducer
  | discharger
  | statusWriter
  deriving DecidableEq

structure CarrierState (Event : Type u) where
  inCut : Event → Prop

def Enabled {Event : Type u} (s : CarrierState Event) (e : Event) : Prop :=
  ¬ s.inCut e

structure Commit
    {Event : Type u}
    (pre : CarrierState Event)
    (e : Event) where
  post : CarrierState Event
  eventPresent : post.inCut e
  preservesOld : ∀ x, pre.inCut x → post.inCut x

theorem no_sequential_recommit
    {Event : Type u}
    {pre : CarrierState Event}
    {e : Event}
    (c : Commit pre e) :
    ¬ Enabled c.post e := by
  intro h
  exact h c.eventPresent

/-! ## A finite Mattermost interpretation of the compiled core -/

structure MMEvent where
  major : Nat
  branch : Nat
  deriving DecidableEq, Repr

def mmBefore (a b : MMEvent) : Prop :=
  a.major ≤ b.major ∧ a.branch ≤ b.branch ∧
    (a.major < b.major ∨ a.branch < b.branch)

instance mmBefore.decidable (a b : MMEvent) : Decidable (mmBefore a b) := by
  unfold mmBefore
  infer_instance

theorem mmBefore_irrefl : ∀ e, ¬ mmBefore e e := by
  intro e h
  rcases h with ⟨_, _, hlt⟩
  cases hlt with
  | inl h => exact Nat.lt_irrefl _ h
  | inr h => exact Nat.lt_irrefl _ h

theorem mmBefore_trans : ∀ {a b c}, mmBefore a b → mmBefore b c → mmBefore a c := by
  intro a b c hab hbc
  rcases hab with ⟨hab1, hab2, habs⟩
  rcases hbc with ⟨hbc1, hbc2, hbcs⟩
  refine ⟨Nat.le_trans hab1 hbc1, Nat.le_trans hab2 hbc2, ?_⟩
  cases habs with
  | inl h => exact Or.inl (Nat.lt_of_lt_of_le h hbc1)
  | inr h => exact Or.inr (Nat.lt_of_lt_of_le h hbc2)

def mmTime : ProtoTime MMEvent :=
  { before := mmBefore
    irrefl := mmBefore_irrefl
    trans := by intro a b c; exact mmBefore_trans }

inductive MMWorld where
  | netDown
  | subscriptionMissing
  | authRevoked
  | eventNotEmitted
  deriving DecidableEq, Repr

inductive MMObservation where
  | socketUnreachable
  | subscriptionConfirmedMissing
  | authDenied
  | eventAbsent
  deriving DecidableEq, Repr

inductive MMRoute where
  | subscriptionConfirmation
  deriving DecidableEq, Repr

inductive MMAction where
  | ping
  | retryConnection
  | listSubscriptions
  | closeDiagnostic
  | recreateSubscription
  deriving DecidableEq, Repr

inductive MMReverses : MMAction → MMAction → Prop where
  | listSubscriptions : MMReverses .listSubscriptions .closeDiagnostic

inductive MMFrame where
  | eventDelivery
  deriving DecidableEq, Repr

inductive MMContact where
  | confirmation
  deriving DecidableEq, Repr

inductive MMWitness where
  | omegaEvent
  deriving DecidableEq, Repr

inductive MMLive where
  | delivery
  deriving DecidableEq, Repr

inductive MMWriter where
  | contactRecorder
  deriving DecidableEq, Repr

inductive MMSource where
  | external
  deriving DecidableEq, Repr


def mmObserve : MMRoute → MMWorld → MMObservation
  | .subscriptionConfirmation, .netDown => .socketUnreachable
  | .subscriptionConfirmation, .subscriptionMissing => .subscriptionConfirmedMissing
  | .subscriptionConfirmation, .authRevoked => .authDenied
  | .subscriptionConfirmation, .eventNotEmitted => .eventAbsent


def e10 : MMEvent := ⟨10, 0⟩
def e11 : MMEvent := ⟨11, 0⟩
def e12 : MMEvent := ⟨12, 0⟩
def e6 : MMEvent := ⟨6, 1⟩
def e8 : MMEvent := ⟨7, 0⟩
def e9 : MMEvent := ⟨9, 2⟩

theorem e10_before_e11 : mmBefore e10 e11 := by decide
theorem e11_before_e12 : mmBefore e11 e12 := by decide
theorem e6_e8_incomparable : ¬ mmBefore e6 e8 ∧ ¬ mmBefore e8 e6 := by decide
theorem e6_before_e9 : mmBefore e6 e9 := by decide
theorem e8_before_e9 : mmBefore e8 e9 := by decide


def mmDoctrine : SoulDoctrine MMFrame MMContact MMWitness MMLive MMEvent :=
  { MaterialTo := fun c w l => c = .confirmation ∧ w = .omegaEvent ∧ l = .delivery
    LiveContinuation := fun l f w => l = .delivery ∧ f = .eventDelivery ∧ w = .omegaEvent
    AdmitCandidate := fun f w e => f = .eventDelivery ∧ w = .omegaEvent ∧ e = e10
    AdmitProbe := fun f w e => f = .eventDelivery ∧ w = .omegaEvent ∧ e = e11
    AdmitAuthority := fun f w e => f = .eventDelivery ∧ w = .omegaEvent ∧ e = e12
    AdmitDurability := fun f w _ => f = .eventDelivery ∧ w = .omegaEvent
    AdmitDischarge := fun l _ => l = .delivery }


def mmDoctrineWellFormed : WellFormedSoulDoctrine mmDoctrine :=
  { materialContinuesLiveInquiry := by
      intro c w l h
      exact ⟨.eventDelivery, h.2.2, rfl, h.2.1⟩ }


def mmWitness : ProspectiveWitness MMFrame MMWitness MMEvent MMLive MMAction :=
  { frame := .eventDelivery
    id := .omegaEvent
    formationEvent := e10
    assemblyEvent := e10
    continues := fun l => l = .delivery
    predicts := fun a => a = .listSubscriptions
    witnessSupport := fun e => e = e10 }


def mmSeal : ContactSeal MMEvent MMContact MMRoute :=
  { contact := .confirmation
    event := e12
    route := .subscriptionConfirmation }


def mmContactRecord : ContactRecord MMEvent MMContact MMRoute MMWorld MMObservation mmObserve :=
  { contact := .confirmation
    event := e12
    world := .subscriptionMissing
    datum := .subscriptionConfirmedMissing
    sealF := mmSeal
    route := .subscriptionConfirmation
    generated := rfl
    sealedRef := rfl
    sealedEvent := rfl
    sealedRoute := rfl }


def mmProbe : ProbeEligible mmTime MMReverses mmWitness .eventDelivery e11 .listSubscriptions :=
  { sameFrame := rfl
    afterFormation := Or.inl e10_before_e11
    budget := 1
    budgetPositive := Nat.zero_lt_succ 0
    rollbackAction := .closeDiagnostic
    rollbackProof := .listSubscriptions }


def mmPriorProbe : PriorProbe mmTime MMReverses mmWitness .eventDelivery e12 :=
  { probeEvent := e11
    action := .listSubscriptions
    proof := mmProbe
    beforeAuthority := e11_before_e12 }


def mmContactWriter : MMRoute → MMWriter → Prop :=
  fun r w => r = .subscriptionConfirmation ∧ w = .contactRecorder


def mmGoverned : GovernedRouteEvidence mmObserve mmContactRecord mmContactWriter .contactRecorder :=
  { governed := ⟨rfl, rfl⟩ }


def mmRelevant : MMLive → MMWorld → MMWorld → Prop :=
  fun l a b => l = .delivery ∧ a = .subscriptionMissing ∧ b = .netDown


def mmDiscriminates : Discriminates mmObserve mmRelevant .subscriptionConfirmation .delivery :=
  { left := .subscriptionMissing
    right := .netDown
    relevantPair := ⟨rfl, rfl, rfl⟩
    differs := by decide }


def mmContactSupport : MMContact → MMEvent → Prop :=
  fun c e => c = .confirmation ∧ e = e11


def mmMaterialContribution : MMEvent → MMContact → MMWitness → MMLive → Prop :=
  fun e c w l => e = e11 ∧ c = .confirmation ∧ w = .omegaEvent ∧ l = .delivery


def mmWitnessSupport : MMWitness → MMEvent → Prop :=
  fun w e => w = .omegaEvent ∧ e = e10


def mmFresh : FreshFor mmTime mmContactSupport mmMaterialContribution mmWitnessSupport
    .confirmation .omegaEvent .delivery e10 e12 :=
  { contributionEvent := e11
    afterAssembly := e10_before_e11
    byAuthority := Or.inl e11_before_e12
    inContactSupport := ⟨rfl, rfl⟩
    notOldSupport := by
      intro h
      have heq : e11 = e10 := h.2
      have hloop : mmBefore e10 e10 := by
        simpa [heq] using e10_before_e11
      exact mmBefore_irrefl e10 hloop
    contributes := ⟨rfl, rfl, rfl, rfl⟩ }


def mmInternalEdge : MMEvent → MMEvent → Prop := fun _ _ => False

def mmContactEvent : MMContact → MMEvent := fun _ => e12

theorem e10_ne_e12 : e10 ≠ e12 := by decide

theorem mmNotSelfGenerated :
    ¬ SelfGenReach mmInternalEdge mmWitness e12 := by
  intro h
  cases h with
  | step _ edge => exact edge


def mmIndependent : IndependentOf mmInternalEdge mmWitness mmContactEvent .confirmation :=
  { outside := mmNotSelfGenerated }


def mmAuthorityPackage :
    AuthorityPackage mmTime MMReverses mmDoctrine mmObserve mmRelevant mmContactWriter
      mmContactSupport mmMaterialContribution mmWitnessSupport mmInternalEdge
      mmContactEvent mmWitness .eventDelivery e12 :=
  { doctrineLawful := mmDoctrineWellFormed
    priorProbe := mmPriorProbe
    contactRecord := mmContactRecord
    contactAtAuthority := rfl
    contactWriterValue := .contactRecorder
    governedRoute := mmGoverned
    live := .delivery
    continued := rfl
    discriminates := mmDiscriminates
    material := ⟨rfl, rfl, rfl⟩
    fresh := mmFresh
    independent := mmIndependent
    soulAdmits := ⟨rfl, rfl, rfl⟩ }


def mmAuthoritative :
    Authoritative mmTime MMReverses mmDoctrine mmObserve mmRelevant mmContactWriter
      mmContactSupport mmMaterialContribution mmWitnessSupport mmInternalEdge
      mmContactEvent mmWitness .eventDelivery e12 :=
  .attach mmAuthorityPackage

theorem mmModelSatisfiesCentralAuthorityTheorem :
    ∃ (pp : PriorProbe mmTime MMReverses mmWitness .eventDelivery e12)
      (record : ContactRecord MMEvent MMContact MMRoute MMWorld MMObservation mmObserve)
      (writer : MMWriter)
      (gr : GovernedRouteEvidence mmObserve record mmContactWriter writer)
      (live : MMLive)
      (disc : Discriminates mmObserve mmRelevant record.route live)
      (mat : mmDoctrine.MaterialTo record.contact mmWitness.id live)
      (fresh : FreshFor mmTime mmContactSupport mmMaterialContribution mmWitnessSupport
        record.contact mmWitness.id live mmWitness.assemblyEvent e12)
      (indep : IndependentOf mmInternalEdge mmWitness mmContactEvent record.contact),
      record.event = e12 := by
  exact authoritative_implies_governing_package mmAuthoritative

/-! Semantic recovery witness in the finite model. -/

inductive MMDistinction where
  | fineLatency
  deriving DecidableEq
inductive MMLossContext where
  | netToEvent
  deriving DecidableEq
inductive MMSideInfo where
  | latencySample
  deriving DecidableEq

def mmCarriesContact : MMContact → MMDistinction → Prop := fun _ _ => False

def mmCarriesFrame : MMFrame → MMDistinction → Prop :=
  fun f d => f = .eventDelivery ∧ d = .fineLatency

def mmRetainedFor : MMSideInfo → MMDistinction → MMLossContext → Prop :=
  fun s d c => s = .latencySample ∧ d = .fineLatency ∧ c = .netToEvent

def mmRestoresRoute : MMRoute → MMDistinction → MMLossContext → Prop := fun _ _ _ => False


def mmRecovery : AvailabilityTransition (Event := MMEvent) mmCarriesContact mmCarriesFrame mmRetainedFor
    mmRestoresRoute .fineLatency .netToEvent :=
  { event := e12
    witness := .retainedSideInfo .latencySample ⟨rfl, rfl, rfl⟩ }

theorem mmRecoveryHasSemanticWitness :
    Nonempty (ReintroductionWitness MMDistinction MMLossContext MMContact MMFrame
      MMSideInfo MMRoute mmCarriesContact mmCarriesFrame mmRetainedFor
      mmRestoresRoute .fineLatency .netToEvent) := by
  exact availability_has_semantic_witness mmRecovery

/-! Interpretation use and computed-stuck evidence are proof-bearing records. -/

inductive MMHistoryRef where | probeResult
inductive MMInterpretation where | subscriptionMissing
inductive MMExpression where | repairSubscription
inductive MMScope where | nextAction
inductive MMSoulJudgment where | admitted
inductive MMEffect where | networkRetry


def mmInterpretation :
    InterpretationRecord MMFrame MMHistoryRef MMInterpretation MMExpression MMEvent :=
  { frame := .eventDelivery
    history := .probeResult
    id := .subscriptionMissing
    expression := .repairSubscription
    event := e12 }


def mmInterpretationUse :
    InterpretationUse (Scope := MMScope) (Action := MMAction)
      (SoulJudgment := MMSoulJudgment) mmInterpretation :=
  { event := e12
    scope := .nextAction
    action := .recreateSubscription
    soul := .admitted }


def mmNetUpdate : MMObservation → MMAction
  | .socketUnreachable => .retryConnection
  | .subscriptionConfirmedMissing => .retryConnection
  | .authDenied => .retryConnection
  | .eventAbsent => .retryConnection


def mmFrameUpdate : MMFrame → MMObservation → MMAction
  | .eventDelivery, observation => mmNetUpdate observation


def mmEffectOf : MMAction → MMEffect
  | .ping => .networkRetry
  | .retryConnection => .networkRetry
  | .listSubscriptions => .networkRetry
  | .closeDiagnostic => .networkRetry
  | .recreateSubscription => .networkRetry


inductive MMReach : MMFrame → MMAction → Prop where
  | ping : MMReach .eventDelivery .ping
  | retryConnection : MMReach .eventDelivery .retryConnection


def mmDemand : MMFrame → MMEvent → Prop :=
  fun frame event => frame = .eventDelivery ∧ event = e10


def mmDiscrepancy : MMFrame → MMEvent → Prop :=
  fun frame event => frame = .eventDelivery ∧ event = e10 ∧
    mmObserve .subscriptionConfirmation .subscriptionMissing ≠
      mmObserve .subscriptionConfirmation .netDown


def mmReinforced : MMFrame → MMEvent → Prop :=
  fun frame event => frame = .eventDelivery ∧ event = e10 ∧
    mmFrameUpdate frame (mmObserve .subscriptionConfirmation .subscriptionMissing) =
      .retryConnection


theorem mmObservationsDiscriminate :
    mmObserve .subscriptionConfirmation .subscriptionMissing ≠
      mmObserve .subscriptionConfirmation .netDown := by decide


theorem mmFrameKillsDistinction :
    mmFrameUpdate .eventDelivery
        (mmObserve .subscriptionConfirmation .subscriptionMissing) =
      mmFrameUpdate .eventDelivery
        (mmObserve .subscriptionConfirmation .netDown) := by rfl


theorem mmListSubscriptionsNotReachable :
    ¬ MMReach .eventDelivery .listSubscriptions := by
  intro h
  cases h


def mmStuck :
    StuckEvidence MMFrame MMEvent MMWorld MMRoute MMObservation MMAction MMEffect
      mmObserve mmFrameUpdate mmDemand mmDiscrepancy mmReinforced MMReach mmEffectOf :=
  { frame := .eventDelivery
    event := e10
    left := .subscriptionMissing
    right := .netDown
    route := .subscriptionConfirmation
    demandProof := ⟨rfl, rfl⟩
    discrepancyProof := ⟨rfl, rfl, mmObservationsDiscriminate⟩
    recurrentEffect := .networkRetry
    recurrenceEvents := [⟨2, 0⟩, ⟨3, 0⟩, ⟨8, 0⟩, e10]
    recurrenceActions := [.ping, .retryConnection, .retryConnection, .retryConnection]
    recurrenceNonempty := by decide
    sameEffect := by
      intro a h
      simp only [List.mem_cons, List.not_mem_nil, or_false] at h
      rcases h with h | h | h | h
      · cases h; rfl
      · cases h; rfl
      · cases h; rfl
      · cases h; rfl
    reinforcementProof := ⟨rfl, rfl, rfl⟩
    nonopeningAction := .listSubscriptions
    nonopeningProof := mmListSubscriptionsNotReachable
    contactDiscriminates := mmObservationsDiscriminate
    distinctionDeathProof := mmFrameKillsDistinction }

structure MattermostModelWitness where
  partialOrderHasIncomparability : ¬ mmBefore e6 e8 ∧ ¬ mmBefore e8 e6
  authority :
    Authoritative mmTime MMReverses mmDoctrine mmObserve mmRelevant mmContactWriter
      mmContactSupport mmMaterialContribution mmWitnessSupport mmInternalEdge
      mmContactEvent mmWitness .eventDelivery e12
  recovery : AvailabilityTransition (Event := MMEvent) mmCarriesContact mmCarriesFrame mmRetainedFor
    mmRestoresRoute .fineLatency .netToEvent
  interpretationUse :
    InterpretationUse (Scope := MMScope) (Action := MMAction)
      (SoulJudgment := MMSoulJudgment) mmInterpretation
  stuck :
    StuckEvidence MMFrame MMEvent MMWorld MMRoute MMObservation MMAction MMEffect
      mmObserve mmFrameUpdate mmDemand mmDiscrepancy mmReinforced MMReach mmEffectOf


def mattermostModel : MattermostModelWitness :=
  { partialOrderHasIncomparability := e6_e8_incomparable
    authority := mmAuthoritative
    recovery := mmRecovery
    interpretationUse := mmInterpretationUse
    stuck := mmStuck }

theorem mattermostModelAccepted : Nonempty MattermostModelWitness := by
  exact ⟨mattermostModel⟩

end ClarityOmega.WMK.Canonical
