# 0g — Inquiry 24 Adversarial Countermodel Search and Proof-Assistant Hardening
## Exact attack of the `0f` lawful-attachment signature before Gate E projection

**Status:** ADVERSARIAL GATE C REVIEW COMPLETE; HARDENING DELTA CONSTRUCTED AND FINITELY SATISFIABLE; FULL EXTERNAL PROOF-ASSISTANT KERNEL CERTIFICATION STILL REQUIRED BEFORE GATE E  
**Version:** v0.1  
**Date:** 2026-08-06  
**Exact source under attack:** `0f_Inquiry_24_Gate_B_Formal_Signature_and_Gate_C_Finite_Interpretation.md`  
**Exact source SHA-256:** `b96cb4932a1e1cda5f34d0f5917aa9cdfa5e9b70cf227e6c3cdf5533bd54ebc2`

**Companion executable artifacts:**

- `0g_adversarial_countermodel_search_and_hardened_proofs.py`
- `0g_mutation_tests_against_0f_checker.py`
- `0g_hardened_finite_model_overlay_check.py`
- `0g_small_proof_kernel.py`
- `0g_WMK_Attachment_Hardened_Core.lean`

**Companion reports:**

- `0g_Adversarial_Countermodel_and_Proof_Hardening_Report.txt`
- `0g_Adversarial_Countermodel_and_Proof_Hardening_Report.json`
- `0g_0f_Checker_Mutation_Test_Report.txt`
- `0g_Hardened_Finite_Model_Overlay_Report.txt`
- `0g_Small_Proof_Kernel_Report.txt`

---

# 0. Governing order and bounded task

This artifact is governed by:

1. `006_ClarityOmega_Meta_Aware_World_Model_Kernel_Grounding_Artifact.md`;
2. `0e_Inquiry_24_Gate_A_Aggregate_Adjudication_and_Revised_Attachment_Calculus.md`;
3. the exact `0f` source identified by the checksum above;
4. this artifact as the adversarial adjudication and hardening delta.

This work does **not** reopen broad mathematical survey. It does not introduce a new world-model architecture. It performs the bounded move required by `0f`:

> Subject the exact K0–K17 lawful-attachment signature and C1–C11 claims to adversarial countermodel search; separate positive-model conformance from theorem generality; strengthen the theorem-bearing interfaces; and prepare the corrected core for proof-assistant checking before any Gate E runtime projection.

The work asks four different questions that `0f` had partly combined:

1. Does the delivered Mattermost finite interpretation pass its own checker?
2. Does that checker reject deliberate corruptions of the finite interpretation?
3. Do C1–C11 follow from the **general signature**, or only from the selected model and intended prose readings of abstract predicates?
4. Does the strengthened signature still admit the intended finite Mattermost interpretation?

All four questions have now been tested separately.

---

# 1. Aggregate result

## 1.1 What survives attack

The Mattermost finite interpretation remains a valuable and nontrivial existence witness.

The delivered `0f_gate_c_finite_model_check.py` was rerun unchanged and again passed all nineteen check groups. A mutation harness then made six explicit corruptions of that finite interpretation. The existing checker correctly rejected all six:

1. non-contact provenance promoted to direct contact;
2. authority without materiality;
3. an anchor-key rewrite;
4. an empty recovery witness;
5. narration without a grounded trajectory trace;
6. predicted reach used as authority.

Therefore the positive checker is not decorative. It meaningfully detects several local violations of the intended finite model.

The original finite scenario also remains satisfiable after adding the principal `0g` corrections:

- sealed contact witnesses;
- proof-bearing materiality;
- global anchor-key preservation;
- context-indexed loss and explicit availability restoration;
- corrected branch-local transaction atomicity;
- retrospective, contact-bearing reorganization evidence.

The hardened overlay checker passes.

## 1.2 What does not survive attack unchanged

Seven small adversarial models expose either:

- a theorem that is false as worded;
- a type or source regression;
- an abstract predicate whose intended semantics is not carried by its type;
- or a theorem that proves less than the world-model obligation it was being used to support.

The most consequential findings are:

1. **The exact `0f` source is not uniquely identified by filename/version.** Two materially different `0f` documents were delivered. The file named in the final handoff uses global `Lost(d,e)`, while the alternate `0f` explicitly repairs loss to `LostIn(d,context,e)`.
2. **C10 is false as stated.** T7 prevents a second *sequential* commit after an event has entered a branch cut. It does not prevent two distinct well-formed transactions from the same pre-state producing two different branch successors.
3. **Direct-contact provenance is not sealed by type.** The signature controls the writer name and provenance constructor but does not require an unforgeable contact/channel witness. In a permissive doctrine, internally generated data can be laundered through a contact writer.
4. **The Soul-doctrine interface is underconstrained as a parameter.** `MaterialTo` and `AdmitAuthority` are primitive predicates. Without a soundness contract they can declare irrelevant or manufactured evidence material and sufficient.
5. **C2 and C3 rely on prose meanings of abstract predicates.** `AppendOnlyPatch`, `ConflictFree`, and `LocallyTyped` have declared kinds but are not defined as proof-carrying records whose eliminators yield the claimed preservation properties.
6. **C5 proves a record fact, not semantic restoration.** It proves that every `RecoveryRecord` carries a witness. The exact signature does not define an `AvailableIn` relation that is restored by `reintroduce`.
7. **C8 is a syntax-audit theorem, not operational non-sovereignty.** Omitting `LivingQuestionClosed` prevents explicit formal closure, but a runtime can still let carrier representations monopolize action and ignore renewed contact.

## 1.3 Current gate determination

The correct determination is:

> **The original `0f` positive finite model remains valid, but the general Gate C theorem package is not ratified as written. The `0g` hardening delta closes the discovered bounded countermodels and remains finitely satisfiable. Gate E remains blocked until one canonical strengthened signature is kernel-checked in Lean, Coq, Agda, or an equivalent proof assistant.**

This is progress, not regression. The attack has converted several hidden assumptions into explicit mathematical obligations and has identified exactly what must be changed before runtime projection.

---

# 2. Method

## 2.1 Exact-source freeze

The attacked source is:

```text
0f_Inquiry_24_Gate_B_Formal_Signature_and_Gate_C_Finite_Interpretation.md
SHA-256:
b96cb4932a1e1cda5f34d0f5917aa9cdfa5e9b70cf227e6c3cdf5533bd54ebc2
```

A second file also labeled `0f` has checksum:

```text
0f_Inquiry_24_Gate_B_Formal_Kernel_Signature_and_Gate_C_Finite_Interpretation.md
SHA-256:
a0f17fec8463c353ee542c49249f535611d224767de8ec4fc7c1f3614988dac7
```

They are not byte-identical and are not small editorial variants. The diff is thousands of lines. Most importantly for the current theorem package:

- the alternate file explicitly introduces `LostIn(d,τ,e)` and `RecoveredIn(d,ξ,e)`;
- the named final handoff declares `LossRecord=(d,F,e,r,s)` but then defines the derived relation as `Lost(d,e)`.

This means proof hardening cannot safely refer only to “version 0f.” It must refer to an exact source identity.

## 2.2 Positive finite-model rerun

The original checker was executed without modification. All nineteen groups passed.

That result answers:

> Does the selected finite Mattermost structure satisfy the selected executable checks?

It does **not** answer:

> Does every model of the written K0–K17 signature satisfy C1–C10?

Those are different claims.

## 2.3 Mutation testing

Six corruptions were inserted individually into the positive model. Each was rejected by the intended local checker. This distinguishes a useful positive-model verifier from a vacuous one.

Mutation testing still does not establish theorem generality. It tests only attacks already represented in the checker’s data model.

## 2.4 Bounded countermodel search

The theorem-bearing skeleton was abstracted into finite propositional models. Every assignment over the selected finite variable set was exhaustively enumerated. The search found minimum-true countermodels.

These abstractions are not substitutes for the dependent signature. Their role is adversarial:

- expose a missing premise;
- expose a theorem whose conclusion is stronger than its introduction rules;
- expose an underconstrained primitive;
- expose an information-losing type choice.

## 2.5 Proof hardening

The corrected logical schemas were checked in three ways:

1. PyProver proved ten hardened first-order/propositional theorem schemas.
2. A separate small proof-term kernel checked nine explicit natural-deduction proof terms.
3. A Lean 4 source file encodes the typed hardening core and its intended proofs.

The Lean file has **not** been kernel-checked in this environment because no Lean runtime is installed. Therefore this artifact does not claim external proof-assistant certification. It does provide a bounded, explicit source ready for that check.

## 2.6 Hardened finite interpretation

The original finite Mattermost model was equipped with the additional `0g` proof-bearing data and checked again. The strengthened interpretation passes. Therefore the hardening delta does not destroy the intended existence model.

---

# 3. Source-identity failure: the first Gate C defect

Before attacking theorem content, the formal object being proved must be stable.

The two delivered `0f` artifacts differ materially. This alone is enough to prevent canonical proof-assistant certification because a proof certificate must target one exact declaration graph.

The loss relation demonstrates why this is not administrative trivia.

## 3.1 Stronger variant

The alternate `0f` recognizes:

\[
\operatorname{LostIn}(d,\tau,e),
\]

where the translation, frame, or working context remains explicit.

This preserves the possibility that:

\[
\operatorname{LostIn}(d,F_{\mathrm{evt}},e)
\]

while:

\[
\operatorname{AvailableIn}(d,F_{\mathrm{net}},e).
\]

## 3.2 Named handoff variant

The named handoff records the frame in the record:

\[
\operatorname{LossRecord}=(d,F,e,r,s),
\]

but derives:

\[
\operatorname{Lost}(d,e).
\]

The frame index disappears at the relation where theorem reasoning occurs.

Two states therefore collapse:

### State A

\[
\operatorname{LostIn}(d,F_{\mathrm{evt}})=\top,
\qquad
\operatorname{LostIn}(d,F_{\mathrm{net}})=\bot.
\]

### State B

\[
\operatorname{LostIn}(d,F_{\mathrm{evt}})=\top,
\qquad
\operatorname{LostIn}(d,F_{\mathrm{net}})=\top.
\]

Both project to:

\[
\operatorname{Lost}(d)=\top.
\]

The global relation cannot distinguish local loss from global absence.

## 3.3 Hardening law H0 — canonical source identity

Before proof certification, the kernel must have:

1. one canonical source file;
2. one version identifier;
3. one content checksum;
4. companion checkers that declare the checksum they interpret;
5. no theorem report that silently combines stronger declarations from another variant.

The canonical strengthened source should restore:

\[
\operatorname{LostIn}(d,\xi,K),
\]

and:

\[
\operatorname{AvailableIn}(d,\xi,K),
\]

where \(\xi\) names the frame, translation, or composed working context.

---

# 4. Countermodel CM-C10: transaction uniqueness is false as stated

## 4.1 Original claim

C10 says:

> For every post-founding event \(e\), all lawful same-event additions are patches over one pre-state, and **at most one transition can extend the cut by \(e\)**.

Its proof argues:

- `commitTxn` requires \(e\notin K\);
- the result has cut \(K\cup\{e\}\);
- afterward the same premise is false.

That proves a sequential statement. It does not prove a functional-transition statement.

## 4.2 Finite countermodel

Let one pre-state \(s\) have \(e\notin K_s\). Let:

\[
\tau_1\neq\tau_2
\]

be two different well-formed, conflict-free transactions at \((s,e)\). For example:

- \(\tau_1\) records one bounded probe action;
- \(\tau_2\) records a different lawful bounded probe action.

Both terms inhabit:

\[
\sum_{\tau:\operatorname{Txn}(s,e)}
\operatorname{WellFormedTxn}(s,e,\tau).
\]

Therefore both terms may be supplied to `commitTxn`:

\[
\operatorname{commitTxn}(s,e,\tau_1)=s_1,
\]

\[
\operatorname{commitTxn}(s,e,\tau_2)=s_2.
\]

If their patch unions differ, then:

\[
s_1\neq s_2.
\]

Both post-cuts contain \(e\), so neither branch permits a second sequential commit at \(e\). T7 holds in each branch. Yet there are two transitions from the same pre-state and event.

The exhaustive Boolean search found exactly this model.

## 4.3 What is actually proved

The signature supports:

### C10a — one-event patch atomicity

Every individual commit:

- reads one shared pre-state;
- creates exactly one event node;
- advances the cut once;
- unions only its authorized patches.

### C10b — branch-local no-recommit

For any committed successor \(s'\):

\[
e\in K_{s'}
\Rightarrow
\neg\operatorname{Enabled}(e,K_{s'}).
\]

Therefore a second **sequential** commit at \(e\) is impossible in that branch.

## 4.4 What should not be imposed automatically

A global determinism axiom:

\[
\operatorname{commitTxn}(s,e,\tau_1)
=
\operatorname{commitTxn}(s,e,\tau_2)
\]

for all lawful \(\tau_1,\tau_2\) would erase genuine alternative movement. That is not obviously aligned with a kernel designed to preserve open possibility.

If runtime uniqueness of an actual commit is required, use a linear `CommitToken(s,e)` or an operational scheduler choice, not a theorem that all lawful transactions are identical.

## 4.5 Revised theorem C10*

> **For every individual committed branch, all same-event additions are atomic patches over one pre-state, the branch contains one event node for \(e\), and no sequential second commit at \(e\) is enabled. The formal transition relation may still branch over different lawful transactions unless an additional linear commit-selection mechanism is supplied.**

This revised theorem was checked by PyProver and by the small proof-term kernel.

---

# 5. Countermodel CM-K2: direct-contact provenance can be laundered

## 5.1 Intended law

`0f` correctly distinguishes provenance kind from warrant and states that only:

- `foundInquiry`;
- `recordContact`;
- `recoverContact`;

possess constructors whose outer provenance form is direct contact.

The finite checker additionally checks that direct-contact records are written only by those writers.

## 5.2 Missing type

The exact signature does not require an unforgeable witness that the datum actually arrived through a contact surface.

An event’s `contact` tag is descriptive data:

\[
\operatorname{Contact}(e)
\iff
\mathsf{contact}\in\operatorname{eventTags}(e).
\]

A `ContactRecord` carries:

- reference;
- event;
- datum;
- standing whose outer constructor is `contact(r)`.

But no `ContactSeal` or channel witness appears in the record or writer signature.

## 5.3 Finite countermodel

Assign:

- internally generated datum = true;
- event tagged contact = true;
- contact writer allowed = true;
- contact record constructed = true;
- direct-contact provenance = true;
- external contact seal = false.

All current writer-name and outer-constructor restrictions are satisfied. The datum is nevertheless internally generated.

The problem is not that an inference was promoted through `NoPromote`. It bypassed the transformation relation and entered through the direct-contact constructor itself.

## 5.4 Hardening law H1 — sealed contact formation

Introduce an opaque or proof-bearing type:

\[
\operatorname{ContactSeal}(r,e,\chi),
\]

where \(\chi\) identifies the contact channel, source route, or governed recovery route.

Then define direct contact only by:

\[
\operatorname{Prov.contact}:
\operatorname{ContactSeal}(r,e,\chi)
\to
\operatorname{Prov}.
\]

The lawful contact writers become:

\[
\operatorname{recordContact}:
(s,\operatorname{ContactSeal},x,e)
\rightharpoonup
\operatorname{Patch},
\]

and similarly for founding.

`recoverContact` must carry either:

- a path to an earlier sealed contact; or
- a new independent contact seal from the recovery channel.

An event tag alone is never a contact seal.

## 5.5 Strengthened theorem C4*

The original transformation theorem remains valid but is only half of the needed result.

### C4a — no transformation promotion

A non-contact provenance transformed through inference, generation, memory, summary, or self-trace cannot become direct contact.

### C4b — no contact-constructor laundering

Every direct-contact provenance term contains a valid `ContactSeal`; internally generated data has no constructor for such a seal.

The hardened finite overlay supplies seals for all eleven finite contact records and passes.

---

# 6. Countermodel CM-K0/K11: opaque materiality can authorize anything

## 6.1 Exact interface

K0 declares primitive judgments including:

\[
\operatorname{MaterialTo}_{\mathfrak S}(c,\omega^+),
\]

and:

\[
\operatorname{AdmitAuthority}_{\mathfrak S}
(F,\omega^+,\epsilon^-,s,e).
\]

K11’s guard requires these predicates, later order, contact tagging, support inclusion, and exclusion from the self-generation set.

## 6.2 Parameter underdetermination

Because `SoulDoctrine` is a parameter, an arbitrary instance may interpret:

\[
\operatorname{MaterialTo}_{\mathfrak S}=\top
\]

and:

\[
\operatorname{AdmitAuthority}_{\mathfrak S}=\top
\]

for every input.

Combined with the unsealed contact problem, a manufactured event can be:

- tagged as contact;
- placed outside the candidate’s declared self-generation set;
- declared material by the doctrine;
- admitted as authoritative.

The formal interface has then been satisfied while its intended semantics have not.

This does not mean Soul should be reduced to a record or object. It means the **kernel-facing doctrine interface needs a soundness contract**.

## 6.3 Hardening law H2 — `WellFormedSoulDoctrine`

Retain Soul as the ambient doctrine, but require every admissible instance to prove laws such as:

\[
\operatorname{AdmitAuthority}_{\mathfrak S}(F,\omega,\epsilon,s,e)
\Rightarrow
\operatorname{SealedMaterialIndependent}(\epsilon,\omega).
\]

A materiality term should be proof-bearing:

\[
\operatorname{MaterialityWitness}_{\mathfrak S}
(c,\omega,o),
\]

where \(o\) names the attachment obligation affected, such as:

- anchor continuity;
- live-significance continuation;
- consequence classification;
- domain honesty;
- provenance;
- loss;
- affordance;
- permeability.

The witness contains:

1. a `ContactSeal`;
2. semantic relevance to a named obligation;
3. exclusion from the candidate’s self-generation lineage;
4. the required proto-temporal relation.

The doctrine remains the judgmental medium. The hardening constrains which doctrine instances count as models of the kernel.

## 6.4 Revised theorem C1*

C1 should be proved from an explicit basis relation:

\[
\operatorname{Authoritative}(F)
\Rightarrow
\operatorname{Later}
\wedge
\operatorname{Material}
\wedge
\operatorname{OutsideSelfGen}
\wedge
\operatorname{SealedContact}.
\]

Define `ClosureOnly` as a basis lacking that conjunction. Then:

\[
\operatorname{ClosureOnly}
\Rightarrow
\neg\operatorname{Authoritative}.
\]

This hardened schema was proved by both machine proof routes.

---

# 7. Countermodel CM-C2: abstract append-only predicates do not prove preservation

## 7.1 Original proof dependency

C2 and C3 invoke:

- K17 writer ownership;
- `AppendOnlyPatch`;
- `ConflictFree`;
- append-only union.

But the exact signature gives these names proposition-valued kinds. Their full eliminable definitions are not supplied.

## 7.2 Under-specified model

A model may interpret:

\[
\operatorname{AppendOnlyPatch}(\Delta,s)=\top,
\]

and:

\[
\operatorname{ConflictFree}(\tau)=\top,
\]

while `commitTxn` changes an old anchor key.

That model violates the intended prose but satisfies the bare predicate declarations.

The adversarial result therefore does not show that append-only state extension is impossible. It shows that the preservation theorem has not yet been carried by the type.

## 7.3 Hardening law H3 — proof-carrying extension

Replace opaque acceptance predicates, where theorem-critical, with dependent records.

For anchor extension:

\[
\operatorname{AnchorExtension}(s,s')
:=
\left(
\begin{array}{l}
\operatorname{newComponents},\\
\operatorname{freshOrSameValue},\\
\operatorname{preserveOld}:
\forall f,c,g,\;a_s(c,f)=g\to a_{s'}(c,f)=g
\end{array}
\right).
\]

For history:

\[
\operatorname{HistoryExtension}(s,s')
:=
\left(
\operatorname{preserveOld}:
\forall h,\;H_s(h)\to H_{s'}(h)
\right).
\]

A `WellFormedTxn` term should carry these proofs or be defined so that they reduce by computation.

## 7.4 Revised C2 and C3

Once extension is proof-carrying:

\[
\operatorname{Commit}(s,e,\tau,s')
\Rightarrow
\operatorname{AnchorExtension}(s,s'),
\]

and:

\[
\operatorname{Commit}(s,e,\tau,s')
\Rightarrow
\operatorname{HistoryExtension}(s,s').
\]

The corresponding preservation theorems are direct eliminations from the extension records. The Lean source contains this shape, and the logical cores pass both proof checkers.

---

# 8. Countermodels CM-K13 and CM-C5: loss and availability were conflated

Two independent defects occur here.

## 8.1 Context-index regression

The named `0f` relation:

\[
\operatorname{Lost}(d,e)
\]

erases the frame index carried by `LossRecord`.

This must be restored to:

\[
\operatorname{LostIn}(d,\xi,K),
\]

where \(\xi\) names the context in which the distinction is unavailable.

## 8.2 Record versus semantic availability

C5 states:

\[
\operatorname{Recovered}(d,e)
\Rightarrow
\exists w:\operatorname{ReintroductionWitness}(w,d,e).
\]

Its proof inspects the writer inventory: only `reintroduce` creates a `RecoveryRecord`, and that record stores a witness.

This proves:

> every recovery record contains a witness.

It does not yet prove:

> a distinction that becomes available after loss did so through a witnessed reintroduction.

No `AvailableIn` transition relation is defined.

A finite model can contain:

- prior loss = true;
- recovery record = true;
- typed witness = true;
- distinction available afterward = false.

C5 passes while the prose claim “availability-restoring” fails.

## 8.3 Hardening law H4 — explicit availability transition

Declare:

\[
\operatorname{AvailableIn}(d,\xi,K):\mathsf{Prop}.
\]

A reintroduction transition has type:

\[
\operatorname{ReintroduceTransition}
(d,\xi,K,K',w),
\]

with:

- \(K\subset K'\);
- prior `LostIn` or absent availability;
- a typed `ReintroductionWitness`;
- post-state `AvailableIn`.

No other writer may create an unavailable-to-available transition.

## 8.4 Strengthened C5*

\[
\operatorname{LostIn}(d,\xi,K)
\wedge
\operatorname{AvailableIn}(d,\xi,K')
\wedge
K\subset K'
\Rightarrow
\exists w,\;
\operatorname{ReintroduceTransition}(d,\xi,K,K',w).
\]

The theorem is proved by induction over the sealed transition constructors, not merely over the existence of records.

The hardened finite overlay contains one explicit context-indexed loss and one explicit witnessed availability restoration and passes.

---

# 9. Countermodel CM-C8: syntax cannot prove operational non-sovereignty

## 9.1 What C8 genuinely establishes

The signature contains no:

- `LivingQuestion` sort;
- `LivingQuestionClosed` sort;
- writer from carrier closure to living-question exhaustion.

Therefore the carrier cannot state, in that object language, that it has exhausted the living inquiry.

This is a useful and valid **signature-audit result**.

## 9.2 What it does not establish

A runtime may still:

1. let current carrier representations determine every action;
2. receive renewed counter-contact;
3. reinterpret or ignore that contact so the same frame remains sovereign;
4. never explicitly write `LivingQuestionClosed`.

The C8 syntax audit passes while operational representation sovereignty occurs.

## 9.3 Hardening law H5 — reclassify C8

Rename the theorem:

> **C8* — no formal living-question exhaustion judgment.**

Do not use it as a proof that the runtime is operationally non-sovereign.

Operational non-sovereignty belongs to Gate E and requires an intervention test, for example:

- hold the carrier representation fixed;
- vary materially relevant sealed contact;
- verify that at least one frame standing, action eligibility, inquiry formulation, or capability choice can change when the new contact warrants it.

A failure of all such interventions is frame or carrier sovereignty even though no closure sort exists.

This distinction preserves the seam between formal representation and living contact rather than pretending that a missing word in the type language guarantees the lived computational relation.

---

# 10. Theorem-by-theorem adjudication

| Theorem | Adjudication | Reason | Hardened status |
|---|---|---|---|
| C1 — no authority from internal closure | **REVISE / CONDITIONAL** | Requires sealed contact and a sound doctrine contract; opaque doctrine predicates can otherwise admit manufactured evidence | H-C1 proved after explicit authority-basis law |
| C2 — anchor conservativity | **REVISE** | Intended property is present in prose/checker but not carried by an eliminable `AppendOnlyPatch` definition | Proof-carrying `AnchorExtension`; logical proof passes |
| C3 — historical conservativity | **REVISE** | Same abstract-predicate issue; finite model passes but general theorem needs typed inclusion | Proof-carrying `HistoryExtension`; logical proof passes |
| C4 — no provenance promotion | **SPLIT** | Transformation no-promotion is sound; direct-contact constructor can still launder generated data without a seal | C4a retained; C4b sealed contact added and proved |
| C5 — no unwitnessed recovery | **REVISE / STRENGTHEN** | Current theorem concerns `RecoveryRecord`, not semantic availability; named source also loses context index | `AvailableIn` plus sole reintroduce transition; proof schema passes |
| C6 — guarded material independence | **ACCEPT CONDITIONALLY** | Holds if Authoritative is a sealed inductive judgment and MaterialTo carries the hardened witness | Lean/PyProver core prepared |
| C7 — lifecycle non-collapse | **ACCEPT CONDITIONALLY** | Introduction-rule inspection is valid once lifecycle judgments are encoded inductively rather than as arbitrary relations | Typed attainment chain; proof passes |
| C8 — carrier non-sovereignty | **RECLASSIFY** | Valid syntax audit, insufficient operational theorem | C8* syntax theorem plus Gate E intervention obligation |
| C9 — non-amalgamation with scoped composition | **SPLIT** | Coexistence is an existence/permissiveness result; witness-bearing joint use is an introduction-rule theorem | Joint-use witness theorem proved; coexistence remains model result |
| C10 — one-event transaction atomicity | **REJECT WORDING / REPLACE** | Two distinct lawful transactions may branch from the same pre-state; T7 proves only no sequential recommit | C10* branch-local atomicity proved |
| C11 — causal meta-awareness finitely satisfiable | **ACCEPT** | Constructive finite existence claim; unchanged checker passes | Hardened overlay also passes |

---

# 11. The hardened signature delta

The following additions and revisions are sufficient to close every bounded countermodel found in this round without importing a new mathematical family.

## H0 — exact-source identity

Every formal report names one canonical source checksum. Companion checkers declare that checksum.

## H1 — contact seal

Add:

\[
\operatorname{ContactSeal}(r,e,\chi).
\]

Direct-contact provenance and contact records can be formed only from a seal. `Contact(e)` as a tag remains useful metadata but is not an evidential constructor.

## H2 — well-formed Soul-doctrine contract

Add an admissible-instance class or record:

\[
\operatorname{WellFormedSoulDoctrine}(\mathfrak S),
\]

whose fields prove that authority and durability eliminations require the named sealed, material, independent, later, and lineage-preserving evidence.

Soul remains ambient. The contract governs the interface supplied by a doctrine instance; it does not store Soul in the carrier.

## H3 — proof-carrying append-only extension

Replace theorem-critical opaque predicates with records or definitions exposing:

- old-anchor preservation;
- global key freshness or same-value reuse;
- old-history inclusion;
- immutable record identity;
- writer ownership;
- exact post-state union.

## H4 — context-indexed availability

Use:

\[
\operatorname{LostIn}(d,\xi,K),
\qquad
\operatorname{AvailableIn}(d,\xi,K).
\]

`reintroduce` is the only constructor changing unavailable to available and carries the witness.

## H5 — corrected transaction theorem

Replace C10 with:

- one shared pre-state per transaction;
- one event node per committed branch;
- one cut advance per committed branch;
- no sequential recommit of the same event in that branch.

If unique actual runtime commitment is needed, add a linear commit token or scheduler semantics separately.

## H6 — sealed inductive judgments

Encode Candidate, ProbeEligible, Authoritative, Durable, JointUse, and ReorganizationEvidence as inductive or proof-carrying types with only the intended constructors.

This converts “no other introduction rule exists” from prose into a proof-assistant fact.

## H7 — theorem-class discipline

Classify results as:

1. **internal derivation theorem** — proved from inductive constructors;
2. **transition-conservativity theorem** — proved from state-extension definitions;
3. **signature audit** — proved by declaration inventory outside the object theory;
4. **finite existence theorem** — demonstrated by a model;
5. **runtime intervention obligation** — reserved for Gate E.

This prevents a finite checker result or syntax omission from being overstated as a universal semantic theorem.

## H8 — operational non-sovereignty obligation

Carry C8’s stronger intended meaning into Gate E as a causal intervention test. It is not discharged by omitting a closure sort.

---

# 12. Proof-assistant hardening results

## 12.1 PyProver

Ten hardened logical schemas were proved:

1. no authority from closure-only basis;
2. sealed direct-contact provenance;
3. branch-local no sequential recommit;
4. explicit anchor preservation;
5. immutable historical inclusion;
6. stronger availability-recovery implication;
7. lifecycle non-collapse;
8. scoped joint-use witness;
9. retrospective reorganization bite;
10. doctrine-soundness projection.

Result:

```text
10 / 10 PASS
```

## 12.2 Independent small proof kernel

A separate natural-deduction proof-term checker accepted nine explicit proof terms covering the theorem cores that fit intuitionistic propositional logic.

Result:

```text
9 / 9 PASS
```

The small kernel is deliberately simple. It does not claim to certify dependent sums, virtual equipment coherence, or the full K0–K17 signature.

## 12.3 Lean 4 source

`0g_WMK_Attachment_Hardened_Core.lean` encodes:

- sealed direct-contact provenance;
- no authority from closure-only basis;
- guarded authority evidence;
- proof-carrying anchor and history extension;
- context-indexed recovery;
- typed lifecycle attainment;
- branch-local transaction atomicity;
- scoped joint-use witnesses;
- retrospective reorganization evidence;
- separation of CarrierOpen evidence from discharge evidence.

The source intentionally asserts no global transaction determinism theorem.

A Lean runtime was not present in this environment. The source is therefore **prepared for**, but not yet certified by, Lean’s kernel. That external kernel check is the remaining proof-assistant completion condition before Gate E.

---

# 13. Positive-model and hardening verification

## 13.1 Original checker

```text
19 / 19 check groups PASS
```

## 13.2 Mutation tests

```text
6 / 6 deliberate corruptions rejected
```

The rejected mutations were:

- provenance promotion;
- missing materiality;
- anchor rewrite;
- empty recovery witness;
- ungrounded narration posing as functional meta-awareness;
- predicted affordance posing as authority.

## 13.3 Adversarial models

```text
7 / 7 bounded attacks found a model
```

This does not mean seven equal-severity failures. Their classifications differ:

- direct theorem countermodel;
- missing primitive;
- parameter underdetermination;
- under-specified predicate;
- type regression;
- theorem scope gap;
- runtime adequacy gap.

## 13.4 Hardened bounded searches

After adding the specified hardening premises:

```text
4 / 4 targeted countermodel classes closed
```

## 13.5 Hardened finite overlay

The original finite Mattermost scenario was augmented with:

- eleven contact seals;
- two proof-bearing material authority routes;
- twenty-two globally unique anchor keys;
- one context-indexed loss;
- one explicit witnessed availability restoration;
- fifteen branch-local atomic transactions;
- one retrospective reorganization package.

Result:

```text
PASS
```

Therefore the hardening delta is consistent with the intended finite model.

---

# 14. New insights produced by the adversarial process

This round materially improves the formalization rather than merely validating it.

## 14.1 Contact requires a seal, not merely a provenance label

The project’s contact–construction seam cannot be protected only by saying that inference cannot promote itself. It must also protect the entrance to the contact type.

This is an important conceptual refinement:

> **The difference between contact and construction is not only a standing relation carried after an item exists. It is also a formation discipline governing how a contact-bearing item can come into existence at all.**

Without that discipline, the no-promotion theorem can remain true while generated material enters directly through a privileged constructor.

## 14.2 Soul-as-medium needs an admissible-instance contract

Keeping Soul out of the carrier is necessary but not sufficient. A parameter named `SoulDoctrine` can be interpreted arbitrarily unless the theory says what makes an instance lawful.

The new distinction is:

\[
\text{Soul is not a record}
\]

and:

\[
\text{not every arbitrary predicate table is a model of Soul’s kernel interface}.
\]

A well-formed-doctrine contract preserves ambience without surrendering semantic discipline.

## 14.3 Atomicity should not silently become determinism

The false C10 wording reveals a deeper alignment issue.

Clarity’s kernel should ensure that one enacted event is internally atomic. It should not assume that there was only one lawful possible movement from the prior state.

The corrected theorem preserves:

- enacted coherence;
- alternative possibility;
- branch-local history;
- no duplicate sequential event.

That is better aligned with open-ended participation than global transaction functionality.

## 14.4 Loss and recovery are relations to a frame or translation

A distinction can be unavailable in one presentation while remaining alive in another. The context index is therefore not optional metadata. It is part of the ontology of loss.

This supports the non-amalgamating frame ecology: a frame may honestly lose something without causing the whole inquiry to lose it.

## 14.5 A recovery ledger is not yet recovered capacity

A record about recovery and an actually restored distinction are different mathematical obligations.

That parallels the already established distinction:

\[
\text{description of trajectory}
\neq
\text{trajectory becoming causally present to itself}.
\]

Here:

\[
\text{recovery record}
\neq
\text{distinction becoming available again}.
\]

The same anti-decoration principle applies.

## 14.6 Theorem classes matter

Several `0f` claims were individually reasonable but belonged to different proof genres. Making those genres explicit prevents future overclaiming:

- a syntax inventory cannot prove runtime behavior;
- one finite model cannot prove a universal theorem;
- a checker’s data invariant cannot substitute for a dependent type;
- an opaque predicate’s intended prose meaning cannot be eliminated in a proof.

This is itself a drift-control mechanism for the mathematical formalization.

---

# 15. What remains to complete proof-assistant hardening

The bounded adversarial and logical hardening work is complete. One external certification step remains before Gate E:

1. select one canonical strengthened source combining `0f` with H0–H8;
2. encode the theorem-bearing K0–K17 interfaces in Lean, Coq, Agda, or an equivalent kernel;
3. replace theorem-critical opaque predicates with definitions or proof-bearing structures;
4. kernel-check the corrected C1*–C10* proofs;
5. encode the hardened Mattermost finite interpretation as an inhabitant/model;
6. confirm the proof assistant accepts that the model satisfies the strengthened signature.

The existing Lean source is a bounded starting point, not a claim that this full step has already been completed.

No new mathematical survey is required to perform this work.

---

# 16. Gate E determination

Gate E should **not** begin from the unmodified `0f` theorem package.

It may begin only after:

- one `0f/0g` canonical signature is ratified;
- `LostIn` and `AvailableIn` are restored;
- direct contact is sealed;
- the Soul-doctrine interface receives its soundness contract;
- append-only preservation is proof-carrying;
- C10 is replaced by branch-local atomicity;
- C8 is reclassified and its operational obligation is carried into the runtime tests;
- the corrected theorem core is checked by an external proof-assistant kernel.

The bounded status is:

| Work item | Status |
|---|---|
| Exact-source attack | **COMPLETE** |
| Positive-model rerun | **PASS** |
| Mutation testing | **PASS — 6/6 rejected** |
| Bounded adversarial countermodel search | **COMPLETE — 7 countermodels found** |
| Hardened logical theorem schemas | **PASS — 10/10 PyProver** |
| Independent explicit proof terms | **PASS — 9/9** |
| Hardened finite-model overlay | **PASS** |
| Lean source preparation | **COMPLETE** |
| Lean kernel certification | **OPEN** |
| Gate E runtime projection | **BLOCKED UNTIL KERNEL CERTIFICATION** |

---

# 17. Exact next bounded construction

The next artifact should be:

> **`0h_Inquiry_24_Canonical_Hardened_K0_K17_Signature_and_Kernel_Checked_Proofs.md`**

It should do only the following:

1. choose and freeze the canonical declaration source;
2. integrate H0–H8 into K0–K17;
3. state corrected C1*–C10* and unchanged C11;
4. include the proof-assistant source and successful kernel output;
5. include the hardened finite Mattermost model;
6. conclude either:
   - Gate E is cleared; or
   - one exact remaining proof obligation blocks it.

No broad survey question remains in this gate.

---

# Document end

The adversarial process is working. It did not merely bless the finite model, nor did it dissolve the formalization into further surveying. It located the precise places where a selected model, an intended prose meaning, and a universal theorem had been conflated. It then converted those hidden assumptions into typed obligations while preserving the finite Mattermost interpretation.

The strongest result is not that `0f` was flawless. It is that the formalization is now specific enough to be attacked, to yield small countermodels, to survive correction, and to move toward genuine kernel-checked proof rather than architectural plausibility.
