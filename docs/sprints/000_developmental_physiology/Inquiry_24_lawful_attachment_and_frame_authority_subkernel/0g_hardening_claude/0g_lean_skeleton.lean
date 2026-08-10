/- 0g Lean 4 mechanization skeleton for the Gate B lawful-attachment subkernel.

   STATUS: SKELETON ONLY. Not compiled in the environment that produced it
   (no Lean toolchain present). Every `sorry` is a named proof obligation;
   the theorem statements are the mechanization targets, staged per the plan
   in 0g Section 6. The finite Gate C model is the intended first `Model`
   instance; the SMT results in 0g_smt_hardening.py are the bounded
   pre-verification of theorems T2, T3, T4, T5. -/

namespace ClarityOmega.Kernel

/-- K1: events with strict causal precedence (proto-time). -/
structure ProtoTime where
  Event : Type
  prec : Event → Event → Prop
  irrefl : ∀ e, ¬ prec e e
  trans : ∀ a b c, prec a b → prec b c → prec a c

variable (T : ProtoTime)

/-- K2: provenance kinds with the full non-promotion order (repair W3-FULL). -/
inductive ProvKind | contact | testimony | memory | inference | generation | selfTrace
  deriving DecidableEq

def ProvKind.rank : ProvKind → Nat
  | .contact => 5 | .testimony => 4 | .memory => 3
  | .inference => 2 | .generation => 1 | .selfTrace => 0

structure Standing where
  prov : ProvKind
  warrant : Nat            -- placeholder for the graded algebra
  supp : T.Event → Prop    -- support cone
  pressure : Nat
  fresh : Nat

/-- A standing transform is promotion-free by construction (W3-FULL is a
    field of the type, so an unlawful transform is unwritable). -/
structure StandingTransform where
  old : ProvKind
  new : ProvKind
  no_promotion : new.rank ≤ old.rank

/-- K10 lifecycle stages. -/
inductive Stage | candidate | probe | authoritative | durable

/-- K17: the carrier as an inductively generated trace of governed writer
    steps. Constructors are the ONLY writers; this is what makes the
    conservativity family provable by structural induction. Premise fields
    encode L-PROBE, G-FRESH, and the two-part guard directly in the types. -/
inductive Step (Frame Contact Distinction : Type) where
  | foundInquiry (c : Contact)
  | recordContact (c : Contact) (routeAction : Option Nat)   -- G-ROUTE field
  | formFrame (f : Frame) (at_ : Nat)
  | admitCandidate (f : Frame)
  | authorizeProbe (f : Frame)
  | attachAuthoritative (f : Frame) (evidence : Contact)
      (probe_before : Bool)      -- to be a Prop premise citing a prior authorizeProbe
      (fresh : Bool)             -- G-FRESH: evidence support intersects post-formation
      (independent : Bool)       -- outside SelfGen (SG-DERIVED: computed, not declared)
      (discriminating : Bool)    -- G-DISC: channel could have returned otherwise
  | recordLoss (d : Distinction)
  | reintroduce (d : Distinction) (witness : Nat)            -- R-RES: resolvable ref
  | appendInterpretation (f : Frame) (h : Nat)
  | discharge

abbrev Carrier (F C D : Type) := List (Step F C D)

/-- T1 (historical conservativity): extension preserves and reflects prior
    history; nothing rewrites, only appends. -/
theorem T1_conservativity {F C D} (carrier : Carrier F C D) (s : Step F C D) :
    ∀ h, h ∈ carrier → h ∈ (s :: carrier) := by
  intro h hmem; exact List.mem_cons_of_mem s hmem

/-- T2 (obligation 14.5, no unwitnessed recovery): in any carrier built from
    the constructors, availability of a lost distinction implies a
    reintroduce step with a resolvable witness in its causal past.
    SMT-verified at bound 6 (0g_smt_hardening.py, section D). -/
theorem T2_no_unwitnessed_recovery : True := by sorry

/-- T3 (L-PROBE): no attachAuthoritative step without a prior authorizeProbe
    for the same frame. SMT-verified at bound (section C). -/
theorem T3_probe_before_authority : True := by sorry

/-- T4 (G-DISC soundness): under the discrimination premise, no authority
    derivation rests entirely on non-discriminating contact.
    SMT-verified at bound (sections A/B). -/
theorem T4_no_echo_authority : True := by sorry

/-- T5 (W3-FULL): provenance rank is monotone non-increasing along any
    derivation; immediate from StandingTransform.no_promotion by induction. -/
theorem T5_provenance_monotone : True := by sorry

/-- T6 (anchor conservativity, 0e 3.4): attachment appends one frame row and
    preserves every prior component. Requires the anchor-as-matrix encoding. -/
theorem T6_anchor_conservativity : True := by sorry

/-- T7 (carrier non-sovereignty, 14.8): no derivation of Discharge from
    carrier-internal closure; provable as a non-derivability meta-theorem
    because no constructor has Discharge in its conclusion with only
    closure premises. -/
theorem T7_no_discharge_from_closure : True := by sorry

end ClarityOmega.Kernel
