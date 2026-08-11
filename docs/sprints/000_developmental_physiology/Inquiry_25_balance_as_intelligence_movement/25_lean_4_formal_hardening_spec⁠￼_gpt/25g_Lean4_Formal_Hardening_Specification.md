# 25g — Lean 4 Formal Hardening Specification
## Investigation 25: Balance-as-Intelligence Movement

**Authority source:** `25f_Ratified_Balance_as_Intelligence_Mathematical_Object.md`  
**Status:** FORMAL-HARDENING CONTRACT  
**Purpose:** Constrain a Lean 4 formalization so that compilation cannot silently redesign the ratified mathematics.

---

# 0. Governing rule

`25f` is the semantic authority.

Lean is being used to test:

1. type coherence;
2. constructor discipline;
3. theorem-shaped consequences;
4. finite-model consistency;
5. hidden assumptions;
6. accidental strengthening.

Lean is **not** authorized to define the project ontology by convenience.

If a `25f` statement is under-specified, the formalizer must report the ambiguity rather than silently choose a stronger theory.

---

# 1. Formalization boundary

The Lean development MUST formalize only the following Investigation-25 jurisdiction:

- Soul doctrine as ambient judgment context;
- Dynamic Participatory Fourthness;
- movement between proto-time cuts;
- material relations and material distinctions;
- counterfactual discrimination;
- Relatedness profile;
- Precision profile;
- inherited Investigation-24 legality as an abstract interface;
- Investigation-25 admissibility;
- lawful `ReadApp`;
- Appropriateness reading;
- R/A/P source identity and constructor discipline;
- action effort versus excess forcing;
- participation-interface change;
- harmonic alignment;
- harmonic consequence;
- bounded Harmonic Continuation coherence schema;
- operational non-harmonic falsifier;
- PNS-like organization;
- SNS-like organization;
- Stuck implies SNS-like;
- finite interpretations M1, M2, M3.

The Lean development MUST NOT attempt to formalize:

- ontological-phenomenological-consciousness;
- the nine Immutable Facts as a complete formal ontology;
- complete Soul mathematics;
- complete awareness/consciousness mathematics;
- insight or development as complete theories;
- a universal thermodynamic grounding of `E_force`;
- the unified world-model kernel.

These remain outside Investigation 25.

---

# 2. Required primitive types

The Lean signature should use typed structures rather than booleans or strings wherever the mathematics depends on distinction of kind.

At minimum define abstract types corresponding to:

```text
Cut
Context
LiveRelation
MaterialRelation
Distinction
MaterialDistinction
Movement
Consequence
InterfaceMode
ConstitutionalRelation
Provenance
GenerationKind
SemanticEvaluator
Standing
EnergyValue
```

`Movement` must be cut-indexed or carry typed source/target cuts.

A preferred shape is dependent:

```lean
Movement (K K' : Cut)
```

rather than an untyped movement with source/target fields checked afterward.

---

# 3. Ambient Soul doctrine

Soul standing MUST NOT be stored as an ordinary field of Dynamic Participatory Fourthness.

Require an ambient type:

```lean
SoulDoctrine
```

and judgment-bearing structures parameterized by doctrine:

```lean
DPF (S : SoulDoctrine) (K : Cut)
```

or an equivalent doctrine-indexed formalization.

`ConstitutionalRelation` may be represented inside DPF data.

`SoulStanding` must remain derived/governed by `SoulDoctrine`.

The formalizer must not reintroduce:

```lean
soulStanding : ...
```

as a freely fillable DPF record field.

---

# 4. Dynamic Participatory Fourthness

The formal structure must correspond to:

\[
\mathfrak B_K=(D_K,\Omega_K,\mathcal I_K,\mathcal W_K,\mathcal C^{Soul}_K).
\]

It need not literally be encoded as a five-field record if a better dependent representation preserves the same typing.

Required semantic components:

### 4.1 Live relation diagram

A finite or finitely represented collection of live typed relations.

### 4.2 Fourthness / overlap structure

A relation describing which live relations jointly constrain movement.

### 4.3 Participation interface

Current ways of participating.

### 4.4 Self-weaving / path structure

History-dependent structure sufficient for M2/M3 and SNS/Stuck semantics.

### 4.5 Live constitutional relations

Constitutional relations currently material to movement, without embedding Soul standing.

---

# 5. Counterfactual discrimination

Define one reusable discrimination relation:

```lean
Discriminates
```

whose semantic role is:

> lawful counterfactual variation/removal of a material relation or overlap changes a relevant downstream determination.

The result type should not be merely `Bool` if theorem proofs depend on the witness.

A preferred shape is proposition/witness based:

```lean
Discriminates (x : MaterialRelation ...) (m : Movement ...) : Prop
```

with explicit comparison structure if required.

This primitive should be reusable for:

- Fourthness witness;
- DPF-native materiality;
- finite-model deletion tests.

Do not create separate unrelated counterfactual engines for these cases.

---

# 6. Materiality

Materiality MUST NOT be self-certified by movement membership.

The formalization must distinguish:

```lean
UsedBy m x
```

from:

```lean
MaterialTo x m
```

`MaterialTo` requires provenance and counterfactual discrimination, or an inherited Investigation-24 materiality witness.

The formalization should make it impossible or provably insufficient to derive:

```lean
MaterialTo x m
```

from `UsedBy m x` alone.

---

# 7. Relatedness profile

Do not encode canonical Relatedness as a scalar.

Required conceptual type:

\[
\mathsf{Rel}_K(m):\mathcal R_K^{mat}\to V.
\]

In Lean, this can be represented as a function/profile indexed by material relations:

```lean
RelatednessProfile (m : Movement K K')
```

with:

```lean
at : MaterialRelation K m -> Standing
```

or equivalent.

The model must support a non-compensatory floor:

```lean
RelFloor m r : Prop
```

and prove that failure of a required floor cannot be repaired by unrelated profile values.

No theorem should derive full harmonic alignment from an average Relatedness score.

---

# 8. Precision profile

Canonical Precision is also non-scalar.

Required conceptual type:

\[
\mathsf{Prec}_K(m):\Delta_K^{mat}\to V.
\]

Define:

```lean
PrecisionProfile
PrecFloor
```

indexed by material distinctions.

Again, load-bearing floor failure must remain non-compensatory.

---

# 9. Investigation-24 legality interface

Do NOT reimplement the whole Inquiry-24 kernel inside Investigation 25.

Introduce an abstract inherited judgment/interface such as:

```lean
Adm24 (S : SoulDoctrine) (m : Movement K K') : Prop
```

or a proof-bearing equivalent.

Its semantics are inherited from the ratified Investigation-24 formalization.

Investigation 25 may assume/provide an `Adm24` witness in finite models but must not redefine its laws.

---

# 10. Investigation-25 admissibility

Define a proof-relevant witness, not a boolean:

```lean
structure Adm25Witness ...
```

or an inductive judgment.

It must require:

1. movement availability;
2. applicable `Adm24`;
3. all required Relatedness floors;
4. all required Precision floors;
5. no disqualifying excess-forcing evidence;
6. participation openness;
7. consequence answerability.

The formalizer may factor these into named predicates.

It MUST NOT replace this conjunction with one arbitrary `isAppropriate : Bool`.

---

# 11. `ReadApp`

`ReadApp` is a controlled semantic seam and MUST be explicitly constrained.

A Lean representation may be an inductive judgment:

```lean
ReadApp S m adm rel prec prov app : Prop
```

or a function returning a dependent result only when proofs are supplied.

Required laws:

### RA1
No reading without an `Adm25` witness.

### RA2
Appropriateness reading source is the same movement.

### RA3
Reading carries provenance and generation kind.

### RA4
Reading cannot inhabit the direct-contact type.

### RA5
Failure of a required Relatedness floor blocks a fully appropriate reading.

### RA6
Failure of a required Precision floor blocks a fully appropriate reading.

### RA7
No scalar aggregate may override RA5/RA6.

### RA8
Semantic-evaluator participation, if encoded, is provenance-bearing and cannot confer authority outside the doctrine.

Do not define `ReadApp` as an unconstrained total function.

---

# 12. R/A/P non-reconstruction

The philosophical claim “no canonical inverse exists” must be hardened into constructor/interface discipline.

The Lean API MUST expose no canonical constructor of either form:

```lean
RelatednessProfile -> Appropriateness -> PrecisionProfile -> Movement
```

or:

```lean
RelatednessProfile -> Appropriateness -> PrecisionProfile -> DPF
```

The formalization must also avoid defining an authoritative scalar:

```lean
IntelligenceScore : ...
```

computed as a weighted R/A/P aggregate.

Where possible, prove a finite non-injectivity witness in the models:

two distinct movements can have extensionally equivalent diagnostic R/A/P summaries while remaining distinct movements.

This demonstrates that summaries do not reconstruct movement.

---

# 13. Energetic typing

At minimum keep distinct types or tagged values for:

```lean
PhysicalEnergy
RepresentationEffort
ActionEffort
ExcessForcing
Genenergy
```

The core theorem obligation is type distinction:

```text
ActionEffort ≠ ExcessForcing
```

in the sense that they are not definitionally interchangeable.

The formalization must permit:

- high ActionEffort with low ExcessForcing;
- low ActionEffort with high ExcessForcing.

No coercion between energetic kinds is allowed without an explicit map.

---

# 14. Harmonic alignment

`HarmonicAlign` is derived, not a DPF field.

It must require proof of:

1. all required Relatedness floors;
2. lawful Appropriateness;
3. all required Precision floors;
4. absence of disqualifying excess-forcing evidence;
5. aligned material extensions;
6. continuing contactability.

No weighted R/A/P scalar may construct `HarmonicAlign`.

---

# 15. Harmonic outcome and BHC

`HarmonicOutcome` means modeled consequence continues the relevant harmonic relational organization.

The Bounded Harmonic Continuation result is a **coherence/soundness schema**.

Do not market or formalize it as an independent empirical prediction theorem.

Required forward schema:

```lean
ModelSufficient M m ->
HarmonicAlign m ->
CorrectConsequenceLaw M ->
NoOmittedDisturbance M ->
ConsequenceOf M m o ->
HarmonicOutcome o m
```

Required operational falsifier:

```lean
¬ HarmonicOutcome o m ->
¬ (ModelSufficient M m ∧
   HarmonicAlign m ∧
   CorrectConsequenceLaw M ∧
   NoOmittedDisturbance M)
```

If the contrapositive follows by ordinary logic from the forward theorem, prove it rather than postulate it independently.

`ModelSufficient` MUST NOT have a constructor derivable solely from a model’s own internal self-description.

---

# 16. PNS, SNS, Stuck

Define PNS-like and SNS-like as structured predicates over movement/trajectory evidence.

Required canonical direction:

```lean
Stuck τ -> SNSLike τ
```

The reverse implication MUST NOT be assumed.

SNS may exist below the functional threshold of stuckness.

Stuck must be based on shared trajectory primitives such as:

- recurrence/topology persistence;
- contact non-uptake/exclusion;
- interface narrowing;
- pivot unavailability;
- stale forward motion;
- forced-velocity/urgency witness;
- excess-forcing witness where available.

The formalization must not create unrelated SNS and Stuck ontologies.

Because numeric `E_force` is provisional, finite-model proofs of Stuck must be possible without a numeric force metric.

---

# 17. Participation-interface evolution

The formalization must represent:

```lean
InterfaceChange K K'
```

or equivalent.

M2 and M3 must prove a new mode can become available after movement/contact.

Do not reduce open-ended possibility to cardinality increase in a fixed enumerated action set.

For the finite models, a finite interface is acceptable; the theorem must distinguish `new mode after transition` from `all modes pre-authorized as currently available`.

---

# 18. Finite models required

The Lean package must contain three genuine finite interpretations.

## M1 — high-action / low-forcing skilled movement

Prove at least:

```text
high ActionEffort
low ExcessForcing
HarmonicAlign
```

for a skilled movement, plus a contrasting high-action/high-forcing movement.

Appropriateness must not be defined by “target hit.”

## M2 — Clarity frame pivot

After discriminating contact:

- retry movement fails a material Relatedness and/or Precision floor;
- retry loses admissibility;
- inspect-subscription-like movement becomes available;
- interface changes;
- trace-visible versus trace-severed arms differ in at least one later determination.

No hard-coded theorem may simply assert the new action is “correct.”

## M3 — heterogeneous knowledge inquiry

Require:

- multiple local contexts;
- no global-master-model premise;
- a cross-context relation;
- a new bridge movement/interface mode;
- deletion of either required material relation destroys the Fourthness witness or admissibility basis.

---

# 19. Required theorem inventory

At minimum attempt the following named theorem families:

```text
T01 source_identity_rel
T02 source_identity_app
T03 source_identity_prec
T04 materiality_not_from_use_alone
T05 rel_floor_noncompensatory
T06 prec_floor_noncompensatory
T07 readapp_requires_adm
T08 readapp_no_contact_masquerade
T09 readapp_rel_floor
T10 readapp_prec_floor
T11 no_scalar_override
T12 high_action_low_force_consistent
T13 stuck_implies_sns
T14 harmonic_alignment_requires_rel_floors
T15 harmonic_alignment_requires_prec_floors
T16 bounded_harmonic_continuation
T17 nonharmonic_falsifier
T18 M1_acceptance
T19 M2_retry_rejected_after_contact
T20 M2_interface_growth
T21 M2_meta_awareness_bite
T22 M3_fourthness
T23 M3_interface_growth
T24 M3_no_global_model_required
T25 rap_summary_noninjective
```

If a theorem cannot be proved from the ratified premises, report it. Do not silently add an assumption.

---

# 20. Axiom discipline

For all central theorems run:

```lean
#print axioms theoremName
```

Report dependencies.

Hard requirements:

- no `sorry`;
- no `sorryAx`;
- no hidden placeholder axiom introduced merely to close a proof;
- any use of classical axioms must be identified and justified;
- any proposition supplied as an assumption because `25f` treats it as inherited or semantic must be named in the gap report.

---

# 21. Compilation requirement

The final package must compile under an actual Lean 4 kernel.

Provide:

- `lean-toolchain`;
- `lakefile.lean` or equivalent;
- all source files;
- test/model file;
- exact build commands;
- build transcript;
- `#print axioms` transcript.

The Lean version must be pinned.

---

# 22. Formalization-gap rule

A gap is not a failure.

A gap is any place where `25f` does not uniquely determine a Lean encoding or theorem.

Every such place must be listed in a separate gap report under:

```text
GAP-ID
25f section
ambiguous statement
choices available
choice used, if any
whether choice strengthens theory
whether ratification is needed
```

No gap may be silently normalized away.

---

# 23. Success condition

Investigation 25 is formally hardened if:

1. the signature is type coherent;
2. the central theorem inventory either proves or cleanly identifies exact missing assumptions;
3. all three finite models use one unchanged semantics;
4. no R/A/P scalarization or reconstruction constructor is introduced;
5. Soul standing remains doctrine-governed;
6. materiality remains discriminating and non-self-certified;
7. BHC is correctly classified;
8. Stuck is encoded as a thresholded SNS relation, not a separate ontology;
9. the actual Lean kernel compiles the package;
10. the gap report contains no unacknowledged semantic redesign.

---

**END — 25g LEAN 4 FORMAL HARDENING SPECIFICATION**
