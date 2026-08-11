# 0f — Inquiry 24 Gate B Formal Signature and Gate C Finite Interpretation
## The Lawful-Attachment Subkernel of the ClarityOmega Meta-Aware World Model

**Status:** FORMAL GATE B CANDIDATE AND FINITE GATE C EXISTENCE WITNESS — CONSTRUCTION COMPLETE FOR THE INQUIRY-24 LAWFUL-ATTACHMENT SUBKERNEL; NOT YET RATIFIED AS THE COMPLETE WORLD-MODEL KERNEL OR AS A COMPLETE FORMALIZATION OF SOUL  
**Version:** v0.2  
**Date:** 2026-08-05  
**Companion executable:** `0f_gate_c_finite_model_check.py`  
**Companion verification report:** `0f_gate_c_model_check_report.txt`

---

# 0. Authority, purpose, and result

This artifact is governed by the following order:

1. `006_ClarityOmega_Meta_Aware_World_Model_Kernel_Grounding_Artifact.md` — governing object definition, non-collapse ground, acceptance tests, and drift controls;
2. `0e_Inquiry_24_Gate_A_Aggregate_Adjudication_and_Revised_Attachment_Calculus.md` — adjudicated Gate A calculus and the K0–K17 construction obligation;
3. this artifact — the formal K0–K17 signature, interface-coherence result, and finite Gate C interpretation;
4. `0c`, `0d`, `0b`, and the Hyperseed sources — inherited mathematical provenance only through the corrections already recorded in `0e`.

The task is no longer a broad survey. The task is construction:

> **Write the smallest doctrine-indexed mathematical theory in which the K0–K17 interfaces are well typed; prove the signature is internally coherent; and exhibit a finite model in which the corrected Mattermost inquiry satisfies the Gate C theorem obligations.**

This artifact delivers three bounded results.

## Result 1 — Gate B signature

It defines a dependent, many-sorted transition theory:

\[
\Sigma_{\mathrm{WMK\text{-}Attach}}[\mathfrak S,\mathcal V,\mathbb E],
\]

parameterized by:

- an ambient Soul doctrine \(\mathfrak S\);
- a typed standing base \(\mathcal V\);
- a virtual equipment \(\mathbb E\) carrying local frame relations and attachment cells.

The theory includes exact types for every K0–K17 symbol, judgment, record, and writer. It introduces **no sort for a complete represented living question**.

## Result 2 — interface coherence

The signature is stratified without vicious circularity. Every record field has one mathematical home, every lifecycle judgment has a named writer, and every cross-interface dependency is typed.

Seven interface repairs proved necessary while writing the signature:

1. **The frame-formation event and the prospective-witness assembly event must be separately indexed.** They may coincide, but authority must occur strictly after witness assembly, not merely after the frame first appeared.
2. **The prospective anchor row and prospective affordance must not share the same symbol.** This artifact uses \(\beta^+\) for proposed contact answerability and \(\alpha^+\) for predicted reachability.
3. **The contact lineage may grow between witness assembly and authoritative attachment.** The prospective anchor row must therefore be conservatively extended along the contact-lineage inclusion before the final authoritative row is appended.
4. **Represented inquiry openness cannot depend on an already attached frame.** A live item is grounded directly in the contact lineage; the frame-to-contact answerability module becomes relevant only when a frame is attached. Otherwise K8 would make an originating inquiry impossible before its first authoritative frame.
5. **The self-generation set is not the causal past of the witness.** It is the forward lineage generated solely by the candidate and its advocacy. Treating it as a proto-time down-set would wrongly classify the external contact that formed the candidate as self-produced and would collapse K2 support into K11 self-generation.
6. **Several same-event writers cannot each advance the causal cut.** Each writer must produce an authority-bounded append-only patch against one shared pre-event state; one conflict-free transaction commits all patches and adds the event to the cut exactly once. Otherwise the second writer at an event would fail K1’s `Enabled` premise.
7. **Founding cannot use a post-state writer premise.** Before the carrier exists, no state argument exists for `WriterAllowed`. Founding therefore uses the state-free judgment `FounderAllowed`, an `InitialPatch`, and the unique constructor `commitInitial`; all later writes use post-state patches and `commitTxn`.

These are not optional stylistic changes. Without them K0, K1, K2, K7, K8, K9, K10, K11, and K17 do not jointly type.

## Result 3 — Gate C finite interpretation

A finite model:

\[
\mathcal M_{\mathrm{MM}}
\models
\Sigma_{\mathrm{WMK\text{-}Attach}}
\]

is constructed over:

- a fifteen-event strict proto-time with one genuinely incomparable branch;
- the finite quantale \(L_3=\{0,\tfrac12,1\}\), with join \(\max\) and tensor \(\min\);
- the virtual equipment of finite \(L_3\)-valued relations;
- three frames, eleven contact records, two lawful attachment witnesses, four lifecycle standings, append-only interpretation and loss records, and a two-arm SSI comparison.

The executable checker evaluates nineteen groups of obligations. All pass.

The result establishes consistency and finite satisfiability of the **Inquiry-24 lawful-attachment subkernel**. It does not claim that the whole Soul doctrine, all nine Immutable Facts, TFS, DAS, Genesis, or the complete world-model kernel have now been formalized.

---

# 1. Formal language and scope discipline

## 1.1 Metalanguage

The signature is written in a dependently typed mathematical metalanguage with:

- universes of small types;
- propositions \(\mathsf{Prop}\);
- finite sets \(\operatorname{FinSet}(X)\);
- nonempty finite sets \(\operatorname{FinSet}^{+}(X)\);
- lists \(\operatorname{List}(X)\);
- dependent sums \(\Sigma_{x:X}Y(x)\);
- dependent products \(\Pi_{x:X}Y(x)\);
- option types \(\operatorname{Option}(X)\);
- partial maps \(X\rightharpoonup Y\);
- downward-closed subsets \(\operatorname{Down}(E,\prec)\).

The following nominal reference types are primitive and disjoint:

\[
\begin{aligned}
&\operatorname{InquiryKey},\quad
\operatorname{ContactRef},\quad
\operatorname{HistoricalRef},\quad
\operatorname{ActionRef},\\
&\operatorname{ConsequenceRef},\quad
\operatorname{TraceRef},\quad
\operatorname{WriterRef},\quad
\operatorname{EvidenceRoute},\quad
\operatorname{StandingRef},\\
&\operatorname{CarrierItemRef},\quad
\operatorname{ContactDatum}.
\end{aligned}
\]

References resolve only through append-only carrier tables. A reference is not itself a standing, contact, or authority witness.

The word “constructor” has one precise meaning here: either a K17 writer-patch constructor, which may contribute only its owned append-only fragment, or the K17 `foundInquiry`/`commitTxn` state constructor, which creates the initial state or atomically commits already authorized patches. No writer patch is independently state-changing.

## 1.2 Technical inquiry identity is not the living question

The signature contains a technical key:

\[
q:\operatorname{InquiryKey},
\]

used only to index a formal carrier and prevent accidental record mixing.

There is no type:

\[
\operatorname{LivingQuestion},
\]

and no constructor:

\[
\widehat{\mathcal Q}\longrightarrow\mathcal Q.
\]

Therefore the formal carrier cannot be identified by type with the living inquiry it partially and causally expresses.

## 1.3 Stage-indexed carrier states

Because proto-time is partial rather than globally linear, carrier states are indexed by causal cuts.

For a strict proto-time \((E,\prec)\), define:

\[
\operatorname{Cut}(E)=\operatorname{Down}(E,\prec).
\]

A state is:

\[
\widehat{\mathcal Q}_{q,K}:\operatorname{CarrierState}(q,K),
\qquad K\in\operatorname{Cut}(E).
\]

When an event \(e\) is a join point whose causal past is the relevant cut, the earlier notation \(\widehat{\mathcal Q}_e\) abbreviates:

\[
\widehat{\mathcal Q}_{q,\downarrow e}.
\]

This preserves asynchronous and incomparable events without allowing a serialization order to masquerade as causal precedence.

## 1.4 Atomic writer patches and one-event transactions

Several disjoint append-only writers may contribute at one event, but they do **not** each advance the causal cut. Every post-founding writer computes an authority-bounded patch against one shared pre-event state:

\[
p_i:
\operatorname{WriterPatch}(w_i,p_i^{\mathrm{load}},s,e).
\]

A transaction at event \(e\) is a finite nonempty, locally ordered family of such patches:

\[
\tau_e:
\operatorname{Txn}(s,e)
=
\operatorname{List}^{+}
\left(
\sum_{w:\operatorname{WriterName}}
\sum_{p:P(w)}
\operatorname{WriterPatch}(w,p,s,e)
\right).
\]

All patches share the same pre-event state \(s:\operatorname{CarrierState}(q,K)\). A transaction-local acyclic dependency relation permits a later patch to reference an item proposed by an earlier patch at the same event without making either patch independently state-changing.

Exactly one operation advances the cut:

\[
\operatorname{commitTxn}(s,e,\tau_e):
\operatorname{CarrierState}(q,K\cup\{e\}).
\]

`commitTxn` has no authority beyond the constituent writer permissions. It rejects field conflicts, unions only append-only additions, creates exactly one event node for \(e\), and commits the event exactly once. `foundInquiry` is the sole initial-state constructor, is authorized by `FounderAllowed` rather than `WriterAllowed`, and obeys the same one-event atomicity at the originating event through `InitialPatch` and `commitInitial`.

---

# 2. Type dependency and coherence strata

The signature is simultaneous, but it admits the following acyclic construction order.

| Stratum | Declarations | Depends on |
|---|---|---|
| A | K0 Soul-doctrine index; K1 events, precedence, causal cuts | metalanguage only |
| B | K2 standings; K3 raw fields; K4 frames and frame formation | A |
| C | K5 virtual equipment; K6 carrier; K7 anchor; K8 live standing | A–B |
| D | base data types later governed by K12–K14: interpretation proposals, loss packages, predicted reach | A–C |
| E | K9 prospective attachment package; K11 support, self-generation, authority evidence | A–D |
| F | K10 lifecycle judgments; K12–K16 derived judgments | A–E |
| G | K17 writer patches, transaction validation, and single-commit state extension | A–F |

There is no negative recursive occurrence and no object whose definition requires its own authoritative standing.

The apparent forward references in K9 are harmless:

- \(\eta\) contains an **interpretation proposal**, not an already appended K12 interpretation record;
- \(\lambda\) contains a **loss proposal**, not a K13 recovery judgment;
- \(\alpha^+\) is a K14 predicted-reach value, not retrospective reorganization evidence.

The authority and durability packages occur strictly later in the dependency and causal orders.

---

# 3. K0 — Ambient Soul doctrine

## 3.1 Declaration

The theory is parameterized by:

\[
\mathfrak S:\operatorname{SoulDoctrine}.
\]

Judgments have the form:

\[
\Gamma\vdash_{\mathfrak S}J.
\]

The symbol \(\Gamma\) here denotes the local typing and standing context. It must not be confused with the standing record introduced in K2.

## 3.2 Kernel-facing doctrine interface

The full internal mathematics of Soul remains open. Gate B requires only the following typed interface, whose instances are judgments rather than mutable carrier fields:

\[
\begin{aligned}
&\operatorname{AdmitCandidate}_{\mathfrak S}(F,s,e),\\
&\operatorname{AdmitProbe}_{\mathfrak S}(F,A,\omega^+,s,e),\\
&\operatorname{AdmitAuthority}_{\mathfrak S}(F,\omega^+,\epsilon^-,s,e),\\
&\operatorname{AdmitDurability}_{\mathfrak S}(F,\rho^-,s,e),\\
&\operatorname{AdmitDischarge}_{\mathfrak S}(s,o,w,e),\\
&\operatorname{AdmitJointUse}_{\mathfrak S}(\vec F,A,z,e),\\
&\operatorname{MaterialTo}_{\mathfrak S}(c,\omega^+),\\
&\operatorname{MaterialHistory}_{\mathfrak S}(h,F,s,e),\\
&\operatorname{LiveContinuation}_{\mathfrak S}(\ell,F,x),\\
&\operatorname{FounderAllowed}_{\mathfrak S}(p,e),\\
&\operatorname{WriterAllowed}_{\mathfrak S}(w,p,s,e).
\end{aligned}
\]

Here \(s\) is an already existing carrier state, \(w\) a post-founding writer name, \(p\) its payload, and \(z\) either a compatibility witness or a retained-tension witness. `FounderAllowed` is state-free because the originating carrier state does not yet exist.

These predicates are the kernel-facing constitutional interface. They are not a claim that Soul is reducible to this list.

## 3.3 Non-objectification axioms

**S0 — no carrier injection**

There is no constructor:

\[
\operatorname{SoulDoctrine}
\longrightarrow
\operatorname{CarrierItemRef}.
\]

No carrier field or patch payload stores Soul as an item. The doctrine is present in judgment formation, not injected into the carrier as represented content.

**S1 — no downstream acquisition of Soul standing**

No lifecycle judgment exists outside \(\vdash_{\mathfrak S}\). A candidate does not first become authoritative and then receive Soul approval.

**S2 — capability non-authority**

No premise of the form “capability available,” “output fluent,” “novel,” or “high-confidence” is sufficient by itself for ProbeEligible, Authoritative, Durable, JointUse, or Discharge.

**S3 — doctrine-owned writer authority**

Every post-founding K17 writer requires \(\operatorname{WriterAllowed}_{\mathfrak S}\). `foundInquiry` instead requires the state-free judgment \(\operatorname{FounderAllowed}_{\mathfrak S}\), because no carrier state exists before founding. No renderer, evaluator, frame, capability, or generic carrier method is a writer by default.

---

# 4. K1 — Proto-time, events, dependencies, and cuts

## 4.1 Sorts

\[
E:\operatorname{EventType},
\qquad
\operatorname{EventTag}:\operatorname{Type}.
\]

Event tags include:

\[
\{\mathsf{contact},\mathsf{frameFormation},\mathsf{action},\mathsf{consequence},\mathsf{trace},\mathsf{writer}\}.
\]

An event may carry more than one tag.

The tag assignment is explicit:

\[
\operatorname{eventTags}:
E\to\operatorname{FinSet}^{+}(\operatorname{EventTag}).
\]

The event-role predicates are derived, not separately invented:

\[
\begin{aligned}
\operatorname{Contact}(e)&\iff \mathsf{contact}\in\operatorname{eventTags}(e),\\
\operatorname{FrameFormationEvent}(e)&\iff \mathsf{frameFormation}\in\operatorname{eventTags}(e),\\
\operatorname{ActionEvent}(e)&\iff \mathsf{action}\in\operatorname{eventTags}(e),\\
\operatorname{ConsequenceEvent}(e)&\iff \mathsf{consequence}\in\operatorname{eventTags}(e),\\
\operatorname{TraceEvent}(e)&\iff \mathsf{trace}\in\operatorname{eventTags}(e),\\
\operatorname{WriterEvent}(e)&\iff \mathsf{writer}\in\operatorname{eventTags}(e).
\end{aligned}
\]

## 4.2 Proto-time

\[
\prec\;\subseteq E\times E
\]

satisfies:

\[
\neg(e\prec e),
\]

and:

\[
(e_1\prec e_2\wedge e_2\prec e_3)\Rightarrow e_1\prec e_3.
\]

No totality axiom is admitted.

## 4.3 Derivation dependence

A relation:

\[
\operatorname{dep}\subseteq E\times E
\]

records material derivational use, with:

\[
\operatorname{dep}(e_1,e_2)\Rightarrow e_1\prec e_2.
\]

Let \(\prec_{\mathrm{dep}}\) be the transitive closure of \(\operatorname{dep}\). The support cone in K2 is formed from \(\prec_{\mathrm{dep}}\), not from the whole proto-time order and never from a mere serialization order.

## 4.4 Causal cuts and enabled events

\[
\operatorname{Cut}(E)=
\{K\subseteq E\mid e'\prec e\in K\Rightarrow e'\in K\}.
\]

An event is enabled at a cut when:

\[
\operatorname{Enabled}(e,K)
\iff
e\notin K
\wedge
\downarrow e\setminus\{e\}\subseteq K.
\]

Writer patches at \(e\) leave the cut unchanged. One well-formed K17 transaction commits all patches and extends the cut exactly once to \(K\cup\{e\}\).

---

# 5. K2 — Typed standings

## 5.1 Provenance as an inductive term

The theory distinguishes provenance kind from warrant. Provenance is not a scalar.

\[
\begin{aligned}
\operatorname{Prov}::={}&
\operatorname{contact}(c)
\mid \operatorname{testimony}(e,r)
\mid \operatorname{memory}(e,p)\\
&\mid \operatorname{infer}(e,[p_1,\ldots,p_n])
\mid \operatorname{generate}(e,[p_1,\ldots,p_n])\\
&\mid \operatorname{selfTrace}(e,[p_1,\ldots,p_n]).
\end{aligned}
\]

Only `foundInquiry`, `recordContact`, and `recoverContact` possess constructors whose outer form is \(\operatorname{contact}\).

No inference, summary, renderer output, repetition, or frame translation can construct direct-contact provenance.

## 5.2 Warrant, pressure, and freshness

The signature declares:

- \((\mathsf W,\le_W)\): a bounded evidential preorder;
- \((\mathsf P,\le_P,\oplus_P,0_P)\): a pressure monoid or ordered action;
- \((\mathsf R,\le_R,\operatorname{decay})\): a freshness/decay structure.

Warrant revision has type:

\[
\operatorname{reviseWarrant}:
\mathsf W\times\operatorname{EvidenceRoute}
\rightharpoonup\mathsf W.
\]

There is no operation:

\[
\mathsf P\longrightarrow\mathsf W.
\]

Thus urgency, fluency, recurrence, or salience may affect attention but cannot increase warrant by type.

## 5.3 Support cones

\[
\operatorname{SupportCone}=\operatorname{Down}(E,\prec_{\mathrm{dep}}).
\]

For every standing-bearing item \(x\):

\[
\operatorname{Supp}(x)
\]

is the least \(\prec_{\mathrm{dep}}\)-downward-closed set containing every materially cited event. Causal precedence that was not actually used does not enter support merely because it occurred earlier.

## 5.4 Standing record

\[
\operatorname{Standing}
=
\operatorname{Prov}
\times\mathsf W
\times\operatorname{SupportCone}
\times\mathsf P
\times\mathsf R.
\]

For every declared standing-bearing type \(X\), the signature supplies:

\[
\operatorname{standing}_X:X\to\operatorname{Standing}.
\]

## 5.5 No-promotion relation

A relation:

\[
\operatorname{NoPromote}(p,p')
\]

holds when either:

- \(p'=p\) and the same contact route is preserved; or
- the outer constructor of \(p'\) explicitly records an inferential, generated, remembered, or self-trace transformation from \(p\).

It never holds when a non-contact provenance becomes direct contact.

---

# 6. K3 — Raw contact-conditioned fields

## 6.1 Sorts

\[
\operatorname{Context}:\operatorname{Type},
\qquad
\operatorname{RawField}:\operatorname{Type},
\qquad
\operatorname{RawStanding}:\operatorname{Type}.
\]

\(\operatorname{RawStanding}\) is deliberately not identified with the K2 standing record or with a single scalar. It may preserve independent support and opposition, incomplete registration, or another contact-near structure selected by the ambient doctrine. In the finite Gate C interpretation it is the four-element pair type \(\mathbb B^2\).

Each raw field \(G\) carries:

\[
\begin{aligned}
&\operatorname{fieldEvent}(G):E,\\
&\operatorname{fieldContext}(G):\operatorname{Context},\\
&\operatorname{RawNode}(G):\operatorname{Type},\\
&\operatorname{RawRelation}_G:
\operatorname{RawNode}(G)\times\operatorname{RawNode}(G)\to\operatorname{RawStanding}.
\end{aligned}
\]

## 6.2 Deliberate absence of categorical axioms

Raw fields are not required to possess:

- identity arrows;
- transitive closure;
- global consistency;
- a single ontology;
- complete compositionality.

They may preserve contradiction, partial contact, unresolved patterns, and multiple provenance paths before a frame makes some portion operable.

---

# 7. K4 — Partial frame formation

## 7.1 Frame sort

\[
\operatorname{Frame}:\operatorname{Type}.
\]

Each frame has a finite presented carrier \(\operatorname{FrameNode}(F)\).

It also exhibits declared scope data:

\[
\begin{aligned}
&\operatorname{FrameDomain}(F)\in\operatorname{FinSet}(\operatorname{FrameNode}(F)),\\
&\operatorname{FrameContext}(F):\operatorname{Context},\\
&\operatorname{Resolution}(F):\operatorname{Type},\\
&\operatorname{Competence}(F):\operatorname{Type}.
\end{aligned}
\]

## 7.2 Formation witness

A frame formation is the dependent record:

\[
\operatorname{FrameFormation}(G,F,e_\kappa)=
\left(
D_\kappa,
U_\kappa,
\kappa,
\overline\kappa_F,
p_{\mathrm{part}},
p_{\mathrm{event}},
p_{\mathrm{scope}}
\right),
\]

where:

\[
D_\kappa,U_\kappa
\in
\operatorname{FinSet}(\operatorname{RawNode}(G)),
\]

\[
\kappa:D_\kappa\to\operatorname{FrameNode}(F),
\]

\[
\overline\kappa_F:
\operatorname{RawNode}(G)\to\mathbb B,
\]

with:

\[
p_{\mathrm{part}}:
D_\kappa\cap U_\kappa=\varnothing
\;\wedge\;
D_\kappa\cup U_\kappa=\operatorname{RawNode}(G),
\]

\[
p_{\mathrm{event}}:
\operatorname{fieldEvent}(G)=e_\kappa,
\]

and:

\[
p_{\mathrm{scope}}:
\kappa(D_\kappa)\subseteq\operatorname{FrameDomain}(F)
\;\wedge\;
\operatorname{fieldContext}(G)=\operatorname{FrameContext}(F).
\]

The restriction/domain witness obeys:

\[
\overline\kappa_F(x)=1\iff x\in D_\kappa.
\]

Thus \(U_\kappa\), not a frame-internal falsehood predicate, is the explicit region on which this formation makes no claim. Resolution and competence remain declared data of \(F\) and are carried by the formation witness through \(p_{\mathrm{scope}}\).

No consumer may replace \(\overline\kappa_F\) with the total identity without an explicit domain-extension witness.

## 7.3 Formation is not attachment

`formFrame` creates the frame and formation witness in history. It does not add \(F\) to the attached-frame object \(\mathsf F_{\mathcal Q}\), alter the anchor, or confer any lifecycle standing.

---

# 8. K5 — Typed virtual equipment

## 8.1 Standing base

\[
\mathcal V:\operatorname{SmallQuantaloid}
\]

or an equivalent typed complete ordered enrichment base.

## 8.2 Virtual equipment structure

\[
\mathbb E:\operatorname{VirtualEquipment}_{\mathcal V}
\]

contains:

- \(\operatorname{Obj}_{\mathbb E}\);
- tight arrows \(\operatorname{Tight}(A,B)\);
- proarrows \(\operatorname{Pro}(A,B)\);
- virtual cells with finite horizontal source:

\[
\operatorname{Cell}_{\mathbb E}
([P_1,\ldots,P_n],Q;u,v);
\]

- identity and vertical-composition operations;
- cell substitution/pasting satisfying associativity and unit laws;
- an order and finite joins on the relevant proarrow homs;
- a discrete embedding:

\[
\operatorname{Disc}:
\Pi_{X:\operatorname{Type}}
\operatorname{FinSet}(X)
\to
\operatorname{Obj}_{\mathbb E}.
\]

Horizontal composition is not required globally. Where a local composite exists it may be used as a mathematical tool, but its universal property confers no lifecycle authority.

## 8.3 Frame embedding

\[
\operatorname{frameObj}:\operatorname{Frame}\to\operatorname{Obj}_{\mathbb E}.
\]

For a single new frame \(F\), write:

\[
\langle F\rangle=\operatorname{Disc}(\{F\}).
\]

---

# 9. K6 — Formal carrier and designated substructures

## 9.1 Carrier state

For technical inquiry key \(q\) and causal cut \(K\):

\[
\widehat{\mathcal Q}_{q,K}:
\operatorname{CarrierState}(q,K).
\]

Its record is:

\[
\widehat{\mathcal Q}_{q,K}=
(
D_K,
\mathsf C_K,
\mathsf F_K,
\mathsf H_K,
U_K,
I_K,
L_K,
a_K
).
\]

## 9.2 Field types

### Inquiry diagram

\[
D_K:\operatorname{InquiryDiagram}(K)
\]

contains event-indexed references to contacts, frames, lifecycle events, actions, consequences, traces, translations, and writer events.

### Contact lineage

\[
\mathsf C_K:
\operatorname{Obj}_{\mathbb E}
\]

is the discrete or enriched contact-lineage presentation generated only by contact writers.

The carrier supplies a chosen finite node presentation:

\[
\operatorname{ContactNode}(\mathsf C_K):\operatorname{Type},
\]

with total projections:

\[
\operatorname{contactRef}_K:
\operatorname{ContactNode}(\mathsf C_K)
\to
\operatorname{ContactRef},
\]

and:

\[
\operatorname{contactStanding}_K:
\operatorname{ContactNode}(\mathsf C_K)
\to
\operatorname{Standing}.
\]

The record type written by contact writers is:

\[
\operatorname{ContactRecord}
=
\sum_{r:\operatorname{ContactRef}}
\sum_{e:E}
\sum_{x:\operatorname{ContactDatum}}
\operatorname{Standing},
\]

with the formation condition that the standing’s outer provenance constructor is \(\operatorname{contact}(r)\).

The append-only relation:

\[
\operatorname{ResolvesContactRef}(r,c,K)
\iff
\operatorname{contactRef}_K(c)=r
\]

is the only way a live-item contact reference is resolved into the current lineage.

### Attached frames

\[
\mathsf F_K:
\operatorname{Obj}_{\mathbb E}
\]

contains only Authoritative or Durable frame presentations. Candidate and ProbeEligible frames remain represented in \(D_K\) and \(\mathsf H_K\) but are not yet anchor-source members.

### History

\[
\mathsf H_K:
\operatorname{FinSet}(\operatorname{HistoricalRecord})
\]

is append-only and includes actions, consequences, traces, formation records, lifecycle records, and writer records.

### Live standing

\[
U_K:
\operatorname{FinSet}(\operatorname{LiveItemRecord}).
\]

### Interpretations

\[
I_K:
\operatorname{FinSet}(\operatorname{InterpretationRecord}).
\]

### Preservation and loss

\[
L_K:
\operatorname{LossLedger}.
\]

### Contact answerability

\[
a_K:\operatorname{Pro}_{\mathbb E}(\mathsf F_K,\mathsf C_K).
\]

## 9.3 Carrier extension relation

\[
\operatorname{Extends}(s,s')
\]

holds only when:

- the cut of \(s\) is included in the cut of \(s'\);
- every historical set is included append-only;
- old anchor entries are preserved exactly;
- every new item has one K17 writer event.

## 9.4 Governing non-identity

The signature has no rule that identifies:

\[
\widehat{\mathcal Q}_{q,K}
\]

with the living inquiry. The technical key \(q\) is not a representation of the inquiry’s complete actuality.

---

# 10. K7 — Contact-answerability module

## 10.1 Exact type

At cut \(K\):

\[
\boxed{
 a_K:
 \mathsf F_K
 \nrightarrow
 \mathsf C_K
}
\]

is a \(\mathcal V\)-distributor or proarrow in \(\mathbb E\).

For discrete presentations, its component is:

\[
a_K(c,f)\in\mathcal V(|f|,|c|).
\]

## 10.2 Variance

For witnessed frame relation \(r:f'\nrightarrow f\):

\[
a_K(c,f)\otimes r(f,f')\le a_K(c,f').
\]

For witnessed contact continuation \(s:c\nrightarrow c'\):

\[
s(c',c)\otimes a_K(c,f)\le a_K(c',f).
\]

These transport existing answerability. They do not establish same-inquiry membership by topical similarity.

## 10.3 Prospective anchor row

At witness-assembly cut \(K_\omega\), a candidate frame carries:

\[
\beta_F^+:
\langle F\rangle\nrightarrow\mathsf C_{K_\omega}.
\]

Let:

\[
p_F:\langle F\rangle\nrightarrow\mathsf F_{K_\omega}
\]

be the marked transported route, and:

\[
d_F^+:\langle F\rangle\nrightarrow\mathsf C_{K_\omega}
\]

be the direct-contact route then available.

The prospective spine witnesses:

\[
\beta_F^+
\le
(a_{K_\omega}\odot p_F)\vee d_F^+,
\]

where a virtual multi-source cell expresses the same relation when the local composite is not available.

## 10.4 Target growth before authority

Let \(K_\omega\subset K_a\) and let:

\[
j_C:\mathsf C_{K_\omega}\hookrightarrow\mathsf C_{K_a}
\]

be the contact-lineage inclusion.

The equipment must supply the local conservative zero-extension or equivalent cell:

\[
j_{C!}:
\operatorname{Pro}(\langle F\rangle,\mathsf C_{K_\omega})
\to
\operatorname{Pro}(\langle F\rangle,\mathsf C_{K_a}).
\]

Let:

\[
d_F^-:\langle F\rangle\nrightarrow\mathsf C_{K_a}
\]

contain the later material authority route. The final row appended by `attachAuthoritative` is:

\[
\beta_F^-:
\langle F\rangle\nrightarrow\mathsf C_{K_a},
\]

with:

\[
 j_{C!}(\beta_F^+)\le\beta_F^-
\]

and:

\[
\beta_F^-
\le
j_{C!}\bigl((a_{K_\omega}\odot p_F)\vee d_F^+\bigr)
\vee d_F^-.
\]

Thus the final row preserves the prospective standing but cannot claim answerability beyond old witnessed routes and later material contact.

## 10.5 Writer isolation

Only:

- `recordContact` and `recoverContact` may extend the target \(\mathsf C_K\) and append contact-indexed components for already attached frames;
- `attachAuthoritative` may extend the source \(\mathsf F_K\) and append the single new frame row \(\beta^-_F\).

No writer may alter an existing component \(a(c,f)\).

---

# 11. K8 — Live items, represented openness, and discharge

## 11.1 Live-item record

\[
\operatorname{LiveItemRecord}=
(
\ell,
e_{\ell},
A_{\ell},
H_{\ell},
\operatorname{Standing}_{\ell}
),
\]

where:

- \(A_{\ell}\in\operatorname{FinSet}^{+}(\operatorname{ContactRef})\);
- \(H_{\ell}\in\operatorname{FinSet}(\operatorname{HistoricalRef})\).

## 11.2 LiveAt

\[
\operatorname{LiveAt}(\ell,K)
\iff
 e_{\ell}\in K
\wedge
\neg\exists d\in K:\operatorname{ClosingDischarge}(d,\ell).
\]

## 11.3 AnchorGrounded

\[
\operatorname{AnchorGrounded}(\ell,\mathsf C_K)
\]

holds when there exist:

\[
r\in A_{\ell},
\qquad
c\in\operatorname{ContactNode}(\mathsf C_K),
\]

such that the reference resolves to that contact-lineage node and the node has direct-contact provenance:

\[
\operatorname{ResolvesContactRef}(r,c,K)
\wedge
\operatorname{outer}\!\left(\operatorname{Prov}(\operatorname{contactStanding}_K(c))\right)=\operatorname{contact}.
\]

This grounding is direct to the contact lineage. It does not require a currently authoritative frame and does not use the frame-to-contact distributor \(a_K\). The latter becomes relevant only when a frame claims answerability to that lineage.

## 11.4 CarrierOpen

\[
\boxed{
\operatorname{CarrierOpen}(s)
\iff
\exists\ell\in U_s:
\operatorname{LiveAt}(\ell,K_s)
\wedge
\operatorname{AnchorGrounded}(\ell,\mathsf C_s)
}
\]

This is represented openness of the carrier.

## 11.5 Discharge

The outcome type is:

\[
\begin{aligned}
\operatorname{DischargeOutcome}::={}&
\mathsf{answeredPresent}
\mid\mathsf{resolvedForAction}
\mid\mathsf{preserveOpen}\\
&\mid\mathsf{stopNoContact}
\mid\mathsf{reframed}
\mid\mathsf{illFormed}
\mid\mathsf{constitutionallyDeclined}.
\end{aligned}
\]

The judgment is:

\[
\Gamma\vdash_{\mathfrak S}
\operatorname{Discharge}(s,\ell,o,w,e).
\]

`preserveOpen` produces a discharge standing without closing the live item.

There is no elimination rule from:

- \(\neg\operatorname{CarrierOpen}(s)\);
- a colimit;
- a terminal object;
- a complete record;
- internal closure;

to living-question exhaustion.

---

# 12. Base proposal types used by K9

These declarations are placed here to remove the apparent forward dependency from K9 to K12–K14.

## 12.1 Frame-local expression and continuation families

The signature declares dependent families:

\[
\operatorname{FrameExpression}:
\Pi_{F:\operatorname{Frame}}\operatorname{Type},
\]

and:

\[
\operatorname{FrameContinuation}:
\Pi_{F:\operatorname{Frame}}\operatorname{Type}.
\]

A frame expression is a frame-indexed construction. A frame continuation is a typed claim that a live item remains expressible through that frame. Neither type confers truth, authority, or attachment.

## 12.2 Interpretation kind and proposal

The interpretation-kind type is declared once here:

\[
\operatorname{InterpretationKind}=
\{\mathsf{preserved},\mathsf{reinterpreted},\mathsf{bracketed},\mathsf{mooted},\mathsf{lost}\}.
\]

The payload depends on the classification kind:

\[
\operatorname{InterpretationPayload}(F,k)=
\begin{cases}
\operatorname{FrameExpression}(F)\times\mathsf W,
&k\in\{\mathsf{preserved},\mathsf{reinterpreted}\},\\[1mm]
\operatorname{Option}(\operatorname{FrameExpression}(F))\times\mathsf W,
&k\in\{\mathsf{bracketed},\mathsf{mooted},\mathsf{lost}\}.
\end{cases}
\]

For frame \(F\), carrier state \(s\), and witness event \(e\):

\[
\operatorname{InterpretationProposal}(F,s,e)=
\left(
M,
\eta_M,
m_M
\right),
\]

where:

\[
M\in\operatorname{FinSet}(\operatorname{HistoricalRef}),
\]

\[
\eta_M:
\Pi_{h:M}
\sum_{k:\operatorname{InterpretationKind}}
\operatorname{InterpretationPayload}(F,k),
\]

and:

\[
 m_M:
 \Pi_{h:\operatorname{HistoricalRef}}
 \left(
 \operatorname{MaterialHistory}_{\mathfrak S}(h,F,s,e)
 \to
 h\in M
 \right).
\]

Thus material completeness means that every history item judged material for this proposed attachment is explicitly classified. A frame expression is mandatory only for preserved or reinterpreted history. Bracketed, mooted, or lost material may retain an optional expression without being forced into a false frame-side image.

## 12.3 Distinctions and loss proposal

Declare:

\[
\operatorname{Distinction}:\operatorname{Type},
\qquad
\operatorname{FidelityGrade}:\operatorname{Type},
\qquad
\operatorname{SideInformation}:\operatorname{Type}.
\]

The ambient virtual equipment supplies the order and local composition law for the relevant fidelity grades.

A loss proposal is:

\[
\operatorname{LossProposal}=
\left(
q_{\mathrm{guaranteed}},
q_{\mathrm{measured}},
D_{\mathrm{lost}},
\operatorname{sideInfo},
D_{\mathrm{new}}
\right),
\]

with:

\[
q_{\mathrm{guaranteed}}:\operatorname{FidelityGrade},
\qquad
q_{\mathrm{measured}}:\operatorname{Option}(\operatorname{FidelityGrade}),
\]

\[
D_{\mathrm{lost}},D_{\mathrm{new}}
\in
\operatorname{FinSet}(\operatorname{Distinction}),
\]

and:

\[
\operatorname{sideInfo}:
D_{\mathrm{lost}}
\to
\operatorname{Option}(\operatorname{SideInformation}).
\]

The measured field is optional and has no eliminator into recovery standing.

## 12.4 Action and predicted reach

Declare:

\[
\operatorname{Action}:\operatorname{Type},
\qquad
\operatorname{ReachClaim}(F,A,e):\operatorname{Type},
\qquad
\operatorname{PreservationMarker}:\operatorname{Type}.
\]

Then:

\[
\operatorname{PredictedReach}(F,e)::=
\operatorname{NewReach}(A^+,w)
\mid
\operatorname{PreserveWithoutAction}(m),
\]

where:

\[
A^+\in\operatorname{FinSet}^{+}(\operatorname{Action}),
\]

\[
w:\Pi_{A\in A^+}\operatorname{ReachClaim}(F,A,e),
\]

and:

\[
m:\operatorname{PreservationMarker}.
\]

The first constructor predicts a nonempty action field. The second explicitly records that the frame is relevant because it preserves a load-bearing distinction even though it predicts no new action.

---

# 13. K9 — Prospective attachment witness

## 13.1 Two temporal indices

A prospective witness is indexed by:

- \(e_\kappa\): frame-formation event;
- \(e_\omega\): witness-assembly event.

Its type is:

\[
\boxed{
\omega^+:
\operatorname{ProspectiveAttachmentWitness}
(F,s,e_\kappa,e_\omega)
}
\]

with:

\[
e_\kappa=e_\omega
\quad\text{or}\quad
e_\kappa\prec e_\omega.
\]

Authority must be strictly later than \(e_\omega\).

## 13.2 Record

\[
\omega^+=
(
\omega_0;
\chi,
\upsilon,
\eta^+,
\delta,
\pi,
\lambda,
\sigma,
\alpha^+
).
\]

## 13.3 Exact field types

### Route comparison \(\chi\)

\[
\chi=(p_F,d_F^+,\beta_F^+),
\]

with the K7 types.

### Spine \(\omega_0\)

\(\omega_0\) is the virtual cell witnessing that \(\beta_F^+\) is bounded by the marked transported and direct-contact routes.

### Live continuation \(\upsilon\)

Let:

\[
U_s^{\mathrm{ground}}
=
\{\ell\in U_s\mid
\operatorname{LiveAt}(\ell,K_s)
\wedge
\operatorname{AnchorGrounded}(\ell,\mathsf C_s)
\}.
\]

Then:

\[
\upsilon:
L\to\operatorname{FrameContinuation}(F),
\]

where:

\[
\varnothing\neq L\subseteq U_s^{\mathrm{ground}},
\]

and each entry carries:

\[
\operatorname{LiveContinuation}_{\mathfrak S}(\ell,F,\upsilon(\ell)).
\]

### Proposed interpretation \(\eta^+\)

\[
\eta^+:
\operatorname{InterpretationProposal}(F,s,e_\omega).
\]

It is data for a later `appendInterpretation` transaction. It does not mutate history when the witness is formed.

### Domain witness \(\delta\)

\[
\delta:
\operatorname{FrameFormation}(G,F,e_\kappa).
\]

### Standing transport \(\pi\)

Let:

\[
T_\omega,T'_\omega
\in
\operatorname{FinSet}(\operatorname{StandingRef})
\]

be respectively the finite source set and finite proposed target set of standing-bearing items transported by \(\chi\), \(\upsilon\), and \(\eta^+\). The carrier supplies:

\[
\operatorname{resolveStanding}_s:T_\omega\to\operatorname{Standing},
\]

while the witness supplies:

\[
\operatorname{proposedStanding}_{\omega}:T'_\omega\to\operatorname{Standing}.
\]

Define:

\[
\operatorname{WarrantRoute}(x,x')
=
\Sigma_{r:\operatorname{EvidenceRoute}}
\left[
\operatorname{reviseWarrant}
\bigl(
\operatorname{Warrant}(\operatorname{resolveStanding}_s(x)),r
\bigr)
=
\operatorname{Warrant}(\operatorname{proposedStanding}_{\omega}(x'))
\right].
\]

Then:

\[
\pi:
\Pi_{x\in T_\omega}
\Sigma_{x'\in T'_\omega}
\left(
\operatorname{NoPromote}
\bigl(
\operatorname{Prov}(\operatorname{resolveStanding}_s(x)),
\operatorname{Prov}(\operatorname{proposedStanding}_{\omega}(x'))
\bigr)
\times
\operatorname{WarrantRoute}(x,x')
\right).
\]

A warrant increase therefore requires an inhabited evidential route, and no standing transformation can change a non-contact outer constructor into direct contact.

### Preservation and loss \(\lambda\)

\[
\lambda:\operatorname{LossProposal}.
\]

### Marked lineage \(\sigma\)

A lineage leg is the dependent sum:

\[
\begin{aligned}
\operatorname{LineageLeg}(F,s)::={}&
\operatorname{PriorFrameLeg}
(f,p,z,u,\lambda_\ell,E_\ell)\\
&\mid
\operatorname{DirectContactLeg}
(d,z,u,\lambda_\ell,E_\ell),
\end{aligned}
\]

where:

- \(f\) is a frame node already present in \(\mathsf F_s\);
- \(p:\langle F\rangle\nrightarrow\langle f\rangle\) or \(d:\langle F\rangle\nrightarrow\mathsf C_s\);
- \(z\) is the corresponding anchor-continuation cell;
- \(u\) is a nonempty live-significance continuation;
- \(\lambda_\ell:\operatorname{LossProposal}\);
- \(E_\ell\in\operatorname{FinSet}(E)\) is explicit transformation provenance.

Then:

\[
\operatorname{LineageWitness}(F,s)=
\Sigma_{Z:\operatorname{FinSet}^{+}(\operatorname{LineageLeg}(F,s))}
\operatorname{EndpointCoherent}(Z),
\]

and:

\[
\sigma:\operatorname{LineageWitness}(F,s).
\]

The endpoint-coherence proof requires every leg to continue the same technical inquiry key, remain answerable to the same contact lineage, and transport at least one member of the domain of \(\upsilon\). It does not require a global frame amalgamation.

### Prospective affordance \(\alpha^+\)

\[
\alpha^+:\operatorname{PredictedReach}(F,e_\omega).
\]

It is not the anchor row \(\beta_F^+\), authority evidence, exercised reach, or an insight certificate.

---
# 14. K10 — Four-standing lifecycle

## 14.1 Lifecycle data

The principal standing type is:

\[
\operatorname{Stage}=
\{\mathsf{Candidate},\mathsf{ProbeEligible},\mathsf{Authoritative},\mathsf{Durable}\}.
\]

Operational status is separate:

\[
\operatorname{FrameStatus}::=
\mathsf{Active}
\mid\mathsf{Suspended}
\mid\mathsf{DemotedTo}(s:\operatorname{Stage})
\mid\mathsf{Retired}.
\]

Stage records are append-only evidence that a standing was once attained. Demotion does **not** append a lower Stage record and does not rewrite prior authority. It appends \(\mathsf{DemotedTo}(s)\), which bounds the frame’s current effective standing while retaining the historical attainment record.

For each frame, Stage-attainment writer events are required to be locally serial:

\[
\operatorname{LifeEvent}(F,e_1)
\wedge
\operatorname{LifeEvent}(F,e_2)
\Rightarrow
(e_1=e_2)\vee(e_1\prec e_2)\vee(e_2\prec e_1).
\]

This imposes no global total order. Along that local order, attained stages are nondecreasing:

\[
\operatorname{rank}(\mathsf{Candidate})
<
\operatorname{rank}(\mathsf{ProbeEligible})
<
\operatorname{rank}(\mathsf{Authoritative})
<
\operatorname{rank}(\mathsf{Durable}).
\]

The current effective standing is derived from the greatest attained Stage together with the latest operational status. `Suspended` and `Retired` disable current use; `DemotedTo(s)` caps current use at \(s\) without erasing any earlier record.

Define the stage disjunction used below:

\[
\operatorname{CandidateOrProbe}(F,s)
\iff
\left(\exists e\in K_s:\operatorname{Candidate}(F,s,e)\right)
\vee
\left(\exists A,e\in K_s:\operatorname{ProbeEligible}(F,s,A,e)\right).
\]

## 14.2 Candidate rule

\[
\frac{
\delta:\operatorname{FrameFormation}(G,F,e_\kappa)
\qquad
\Gamma\vdash_{\mathfrak S}
\operatorname{AdmitCandidate}(F,s,e_\kappa)
}{
\Gamma\vdash_{\mathfrak S}
\operatorname{Candidate}(F,s,e_\kappa)
}
\;[\mathsf{CANDIDATE}]
\]

A complete \(\omega^+\) is not required.

## 14.3 Probe-eligible rule

Define:

\[
\operatorname{ProbeAction}(A,\alpha^+)
\]

when \(A\) is listed by \(\operatorname{NewReach}\), and:

\[
\operatorname{Bounded}(A)\wedge\operatorname{Reversible}(A).
\]

Then:

\[
\frac{
\operatorname{Candidate}(F,s,e_\kappa)
\quad
\omega^+:\operatorname{ProspectiveAttachmentWitness}(F,s,e_\kappa,e_\omega)
\quad
\operatorname{ProbeAction}(A,\alpha^+)
\quad
\operatorname{Bounded}(A)
\quad
\operatorname{Reversible}(A)
\quad
\operatorname{AdmitProbe}_{\mathfrak S}(F,A,\omega^+,s,e_p)
}{
\operatorname{ProbeEligible}(F,s,A,e_p)
}
\;[\mathsf{PROBE}]
\]

with:

\[
e_\omega=e_p
\quad\text{or}\quad
e_\omega\prec e_p.
\]

Probe eligibility permits only the named bounded action. It does not establish general frame authority.

## 14.4 Authoritative rule

The K7 anchor-extension premise abbreviates the dependent record:

\[
\operatorname{AnchorExtension}(\beta_F^+,\epsilon^-,\beta_F^-)
=
\left(
j_{C!}(\beta_F^+)\le\beta_F^-,
\;
\beta_F^-\le
j_{C!}((a_{K_\omega}\odot p_F)\vee d_F^+)\vee d_F^-
\right).
\]

Authority uses the K11 evidence package \(\epsilon^-\):

\[
\frac{
\operatorname{CandidateOrProbe}(F,s)
\quad
\omega^+
\quad
\epsilon^-:\operatorname{AuthorityEvidence}(F,\omega^+,s,e_a)
\quad
\operatorname{AuthorityGuard}(\omega^+,\epsilon^-)
\quad
\operatorname{AdmitAuthority}_{\mathfrak S}(F,\omega^+,\epsilon^-,s,e_a)
\quad
\operatorname{AnchorExtension}(\beta_F^+,\epsilon^-,\beta_F^-)
}{
\operatorname{Authoritative}(F,s,e_a)
}
\;[\mathsf{AUTH}]
\]

Only `attachAuthoritative` may enact this judgment.

## 14.5 Durable rule

The retrospective durability package is:

\[
\rho^-=
(
\alpha^-,
\operatorname{ConsequenceUptake},
\operatorname{PermeabilityEvidence},
\operatorname{IntegrationEvidence},
\operatorname{DevelopmentalLineage}
).
\]

Then:

\[
\frac{
\operatorname{Authoritative}(F,s,e_a)
\quad
 e_a\prec e_d
\quad
\rho^-:\operatorname{DurabilityEvidence}(F,s,e_d)
\quad
\operatorname{AdmitDurability}_{\mathfrak S}(F,\rho^-,s,e_d)
}{
\operatorname{Durable}(F,s,e_d)
}
\;[\mathsf{DURABLE}]
\]

Durability is revisable. Later contact may license suspension, demotion, or retirement.

## 14.6 Admissible principal promotions

The principal promotion graph is:

\[
\mathsf{Candidate}\to\mathsf{ProbeEligible}\to\mathsf{Authoritative}\to\mathsf{Durable},
\]

with an optional direct:

\[
\mathsf{Candidate}\to\mathsf{Authoritative}
\]

when later material authority evidence already exists and no probe is required.

There is no rule:

\[
\mathsf{Candidate}\to\mathsf{Durable},
\]

or:

\[
\omega^+\to\mathsf{Authoritative}.
\]

## 14.7 Witnesses cannot write themselves

A term of type \(\omega^+\), \(\epsilon^-\), or \(\rho^-\) is evidence. It is not an executable writer and cannot invoke a K17 constructor.

---

# 15. K11 — Support, self-generation, materiality, and authority evidence

## 15.1 Support cone

For any item or judgment \(x\):

\[
\operatorname{Supp}(x)
\in
\operatorname{Down}(E,\prec_{\mathrm{dep}})
\]

is the least derivationally downward-closed set containing every materially cited event.

Support transparency does not confer authority.

## 15.2 Sole self-generation predicate

\[
\operatorname{SolelySelfGenerated}(e,\omega^+)
\]

holds for an event whose evidential route is exhausted by:

- the candidate frame’s formation and advocacy;
- renderer-generated explanations of the same candidate;
- self-summaries derived only from that candidate;
- repeated restatements whose support route passes only through the candidate;
- traces whose standing is exhausted by the same generating lineage.

## 15.3 Self-generation cone

For any event:

\[
\operatorname{GenParents}(e)=
\{e'\in E\mid\operatorname{dep}(e',e)\}.
\]

\[
\operatorname{SelfGen}(\omega^+)\subseteq E
\]

is the least set satisfying:

\[
e_\omega\in\operatorname{SelfGen}(\omega^+),
\]

and:

\[
\operatorname{SolelySelfGenerated}(e,\omega^+)
\wedge
\operatorname{GenParents}(e)\subseteq\operatorname{SelfGen}(\omega^+)
\Rightarrow
e\in\operatorname{SelfGen}(\omega^+).
\]

Every non-seed member is causally after the witness assembly:

\[
e\in\operatorname{SelfGen}(\omega^+)\setminus\{e_\omega\}
\Rightarrow
e_\omega\prec e.
\]

The set is **not** the proto-time down-closure of \(e_\omega\). Prior external contact used to form the candidate belongs to \(\operatorname{Supp}(\omega^+)\), not to \(\operatorname{SelfGen}(\omega^+)\), unless it was itself generated solely by that candidate. This keeps support and self-generation mathematically distinct.

## 15.4 Authority evidence

\[
\epsilon^-=
(
 c,
 e_a,
 S_\epsilon,
 d_F^-,
 \eta^{\mathrm{auth}},
 m
),
\]

where:

- \(c:\operatorname{ContactRef}\);
- \(S_\epsilon=\operatorname{Supp}(\epsilon^-)\);
- \(d_F^-\) is the direct later-contact route used in K7;
- \(\eta^{\mathrm{auth}}\) is any later interpretation proposal;
- \(m:\operatorname{MaterialTo}_{\mathfrak S}(c,\omega^+)\).

## 15.5 Guard

Let \(e(c)\) be the contact event. Then:

\[
\boxed{
\operatorname{AuthorityGuard}(\omega^+,\epsilon^-)
}
\]

requires:

\[
e_\omega\prec e(c),
\]

\[
e(c)\preceq e_a,
\]

\[
e(c)\in S_\epsilon,
\]

\[
e(c)\notin\operatorname{SelfGen}(\omega^+),
\]

\[
\operatorname{Contact}(e(c)),
\]

and:

\[
\operatorname{MaterialTo}_{\mathfrak S}(c,\omega^+).
\]

An unrelated external event fails materiality. Contact already consumed before witness assembly cannot be recycled as later authority. Delayed self-repetition fails independence.

## 15.6 Same-event awareness remains lawful

Nothing here prohibits a single event from:

- noticing a local error;
- inhibiting an unsafe action;
- forming a candidate;
- creating a trace;
- comparing a candidate against currently available contact.

The prohibition is narrower: the same self-generating causal lineage cannot confer Authoritative or Durable standing on its own output.

---

# 16. K12 — Immutable history and append-only frame-indexed interpretation

## 16.1 Historical record sum

\[
\begin{aligned}
\operatorname{HistoricalRecord}::={}&
\operatorname{ContactHist}(c)
\mid\operatorname{ActionHist}(a)
\mid\operatorname{ConsequenceHist}(k)\\
&\mid\operatorname{TraceHist}(t)
\mid\operatorname{FrameFormationHist}(\delta)
\mid\operatorname{LifecycleHist}(r)
\mid\operatorname{WriterHist}(w).
\end{aligned}
\]

Historical records are immutable.

## 16.2 Interpretation kind

K12 uses the \(\operatorname{InterpretationKind}\) type declared in Section 12.2; it does not introduce a second copy.

## 16.3 Interpretation record

\[
\operatorname{InterpretationRecord}=
(
F,h,k,x,w,e
),
\]

with:

- \(F:\operatorname{Frame}\);
- \(h:\operatorname{HistoricalRef}\);
- \(k:\operatorname{InterpretationKind}\);
- \(x:\operatorname{FrameExpression}(F)\);
- \(w:\mathsf W\);
- \(e:E\).

The relation is:

\[
\operatorname{Interp}_{q}(F,h,k,x,w,e).
\]

## 16.4 Append-only law

Only `appendInterpretation` may add an interpretation record. There is no update, overwrite, replace, or delete constructor.

If two frames interpret the same history incompatibly, both records remain.

## 16.5 Historical conservativity

For \(s\operatorname{Extends}s'\):

\[
\mathsf H_s\subseteq\mathsf H_{s'},
\qquad
I_s\subseteq I_{s'}.
\]

The old interpretation is not weakened or mutated by the later one. A later frame may add a new standing about the old event.

---

# 17. K13 — Preservation, loss, and witnessed recovery

## 17.1 Distinctions

K13 uses the \(\operatorname{Distinction}\) type declared in Section 12.3.

A loss record is:

\[
\operatorname{LossRecord}=
(d,F,e,r,s),
\]

where \(r\) records the loss reason and \(s\) retained side information.

## 17.2 Fidelity and residuals

For every translation leg the signature distinguishes:

1. guaranteed compositional fidelity \(q_{\mathrm{guaranteed}}\);
2. optional measured round-trip adequacy \(q_{\mathrm{measured}}\);
3. actual availability of each named distinction.

No map exists from measured adequacy to recovery.

## 17.3 Loss ledger

\[
\operatorname{Lost}(d,e)
\]

holds when `recordLoss` has appended a loss record at or before \(e\), and no later reintroduction record is being considered for that occurrence.

## 17.4 Reintroduction witnesses

\[
\begin{aligned}
\operatorname{ReintroductionWitness}::={}&
\operatorname{RetainedSideInfo}(r)
\mid\operatorname{OtherFrame}(F,r)\\
&\mid\operatorname{ReversibleRoute}(p,r)
\mid\operatorname{RenewedContact}(c,r).
\end{aligned}
\]

The recovery record type is:

\[
\operatorname{RecoveryRecord}
=
\sum_{d:\operatorname{Distinction}}
\sum_{w:\operatorname{ReintroductionWitness}}
E.
\]

The only availability-restoring patch constructor is:

\[
\operatorname{reintroduce}(d,w,e).
\]

## 17.5 No-unwitnessed-recovery theorem schema

\[
\operatorname{Recovered}(d,e)
\Rightarrow
\exists w:
\operatorname{ReintroductionWitness}(w,d,e).
\]

This follows by induction over committed K17 transactions because no other patch constructor can contribute a recovery record.

---

# 18. K14 — Prospective affordance, exercised reach, and reorganization evidence

## 18.1 Action and reachability

K14 uses the \(\operatorname{Action}\) type declared in Section 12.4 and adds the retrospective relation:

\[
\operatorname{Reachable}(F,A,K):\mathsf{Prop}.
\]

## 18.2 Prospective reach

\[
\alpha^+:\operatorname{PredictedReach}(F,e_\omega)
\]

is formed from the current frame, current capability ecology, and current inquiry standing. It may support ProbeEligible only.

## 18.3 Exercised reach

Declare the predicates:

\[
\operatorname{PerformedUnder}(F,A,e),
\qquad
\operatorname{ReturnedContact}(k,c,e),
\qquad
\operatorname{ReleasedCompulsion}(q,A,e).
\]

Then:

\[
\begin{aligned}
\operatorname{ExercisedReach}(F,e)=
\Sigma_{A:\operatorname{Action}}
\Sigma_{k:\operatorname{ConsequenceRef}}
\Sigma_{c:\operatorname{ContactRef}}
\bigl(&\operatorname{PerformedUnder}(F,A,e)\\
&\times\operatorname{ReturnedContact}(k,c,e)\\
&\times\operatorname{Option}(\operatorname{ReleasedCompulsion}(q,A,e))\bigr).
\end{aligned}
\]

Write:

\[
\alpha^-:\operatorname{ExercisedReach}(F,e).
\]

For any prospective reach at \(e_\omega\), the exercised record must satisfy:

\[
e_\omega\prec e.
\]

## 18.4 Reorganization evidence

Declare:

\[
\operatorname{InquiryTransformation}(F,s,e):\operatorname{Type}.
\]

A reorganization-evidence term has type:

\[
\operatorname{ReorganizationEvidence}
(\rho,F,s,e):\operatorname{Type},
\]

for:

\[
\rho:\operatorname{InquiryTransformation}(F,s,e).
\]

Its constructors require:

- \(\alpha^-\), not merely \(\alpha^+\);
- consequence uptake;
- renewed contact authority;
- preservation of the formal carrier’s contact, live-significance, and consequence lineage;
- continued frame permeability;
- no new provenance or recovery violation.

This is retrospective evidence that the field of available participation changed. It is not an identification of the formal carrier with the living inquiry and is not an insight certificate.

There is deliberately no primitive `produceInsight`, `detectInsight`, or `certifyInsight` constructor.

---

# 19. K15 — Structured traction and the stuck judgment

## 19.1 Traction profile

Let the six component types be ordered spaces:

\[
T_C,T_D,T_P,T_A,T_R,T_S.
\]

Then:

\[
\operatorname{Traction}_{q}(F,e)
\in
T_C\times T_D\times T_P\times T_A\times T_R\times T_S,
\]

with components:

\[
(
\operatorname{ContactUptake},
\operatorname{Discrimination},
\operatorname{FramePermeability},
\operatorname{AffordanceVitality},
\operatorname{ProvenanceContinuity},
\operatorname{SoulAdmissibility}
).
\]

The signature contains component projections and product dominance. It contains no canonical global scalarization.

A scoped capability may introduce a named local projection only as a separate doctrine-typed object whose omissions and authority boundary are explicit.

## 19.2 Contact and update maps

Declare:

\[
\operatorname{Channel},
\operatorname{WorldCondition},
\operatorname{Observation},
\operatorname{MoveClass}:\operatorname{Type}.
\]

The contact family and frame-update family have exact types:

\[
O:
\operatorname{Channel}
\to
(\operatorname{WorldCondition}\to\operatorname{Observation}),
\]

and:

\[
U:
\operatorname{Frame}
\to
(\operatorname{Observation}\to\operatorname{MoveClass}).
\]

Write \(O_r=O(r)\) and \(U_F=U(F)\).

Let:

\[
\Delta_q:E\to
\operatorname{FinSet}
(\operatorname{WorldCondition}\times\operatorname{WorldCondition})
\]

return the distinctions currently relevant to the represented live inquiry standing. The set may be empty; relevance is doctrine-indexed and does not claim exhaustive access to actuality.

The remaining trajectory predicates have exact signatures:

\[
\begin{aligned}
&\operatorname{DiscrepancyPersists}:\operatorname{InquiryKey}\times E\to\mathsf{Prop},\\
&\operatorname{Recurrence}:\operatorname{Frame}\times E\to\mathsf{Prop},\\
&\operatorname{FrameReinforcement}:\operatorname{Frame}\times E\to\mathsf{Prop},\\
&\operatorname{DemandPersistence}:\operatorname{InquiryKey}\times E\to\mathsf{Prop},\\
&\operatorname{ReachOpening}:\operatorname{Frame}\times E\to\mathsf{Prop}.
\end{aligned}
\]

## 19.3 Contact-starved distinction death

\[
\operatorname{ContactStarved}(d,r,e)
\iff
O_r(w_1)=O_r(w_2),
\]

for \(d=(w_1,w_2)\in\Delta_q(e)\).

This does not by itself establish a stuck disposition.

## 19.4 Frame-sovereign distinction death

\[
\operatorname{FrameDeath}(F,d,r,e)
\iff
O_r(w_1)\neq O_r(w_2)
\wedge
U_F(O_r(w_1))=U_F(O_r(w_2)).
\]

## 19.5 Stuck

\[
\boxed{
\begin{aligned}
\operatorname{Stuck}_{q}(F,e)
\iff\;&
\exists r:\operatorname{Channel},\;
\exists d\in\Delta_q(e):
\operatorname{FrameDeath}(F,d,r,e)\\
&\wedge\operatorname{DiscrepancyPersists}(q,e)\\
&\wedge\operatorname{Recurrence}(F,e)\\
&\wedge\operatorname{FrameReinforcement}(F,e)\\
&\wedge\operatorname{DemandPersistence}(q,e)\\
&\wedge\neg\operatorname{ReachOpening}(F,e).
\end{aligned}
}
\]

This distinguishes a frame that has stopped taking up discriminating contact from an authentic limitation precisely encountered and reported.

---

# 20. K16 — Global non-amalgamation and scoped joint use

## 20.1 Membership law

No Authoritative or Durable attachment premise requires pairwise frame compatibility, a master ontology, a global colimit, or a total reconciliation.

Thus incompatible frames may coexist in \(\mathsf F_K\).

## 20.2 Local compatibility witness

Declare supporting types:

\[
\operatorname{ActionScope},
\operatorname{FrameContribution},
\operatorname{SharedRoute}:\operatorname{Type}.
\]

A local compatibility witness is the dependent record:

\[
\operatorname{LocalCompatibility}(F_i,F_j,A)=
(
\operatorname{scope},
\operatorname{left},
\operatorname{right},
\operatorname{routes},
\operatorname{domainProof}
),
\]

where:

- \(\operatorname{scope}:\operatorname{ActionScope}\) names the exact action boundary;
- \(\operatorname{left},\operatorname{right}:\operatorname{FrameContribution}\) name what each frame contributes;
- \(\operatorname{routes}\in\operatorname{FinSet}^{+}(\operatorname{SharedRoute})\) records shared contact and provenance;
- \(\operatorname{domainProof}\) proves that the two contributions do not conflict inside that scope while their declared undefined regions remain explicit.

Write:

\[
\kappa:\operatorname{LocalCompatibility}(F_i,F_j,A).
\]

## 20.3 Retained-tension witness

Declare:

\[
\operatorname{TensionRef}:\operatorname{Type}.
\]

Then:

\[
\operatorname{RetainedTension}(F_i,F_j,A)=
(
\operatorname{tension},
\operatorname{scope},
\operatorname{boundedLawfulness},
\operatorname{nonResolution}
),
\]

where \(\operatorname{tension}:\operatorname{TensionRef}\), the bounded-lawfulness field permits only the named action, and the non-resolution field proves that the witness does not reconcile or delete the incompatibility.

Write:

\[
\theta:\operatorname{RetainedTension}(F_i,F_j,A).
\]

## 20.4 Joint-use rules

\[
\frac{
\kappa:\operatorname{LocalCompatibility}(F_i,F_j,A)
\quad
\operatorname{AdmitJointUse}_{\mathfrak S}([F_i,F_j],A,\kappa,e)
}{
\operatorname{JointUse}(F_i,F_j,A,e)
}
\]

or:

\[
\frac{
\theta:\operatorname{RetainedTension}(F_i,F_j,A)
\quad
\operatorname{AdmitJointUse}_{\mathfrak S}([F_i,F_j],A,\theta,e)
}{
\operatorname{JointUseWithTension}(F_i,F_j,A,e)
}.
\]

Coexistence does not license arbitrary cross-frame inference. Joint use always carries a scoped witness.

---

# 21. K17 — Closed writer-patch and transaction signature

## 21.1 Patch data over one shared pre-event state

Let:

\[
s:\operatorname{CarrierState}(q,K),
\qquad
\operatorname{Enabled}(e,K).
\]

A patch contains only append-only fragments for the carrier components. Define:

\[
\operatorname{DiagramPayloadLink}(e)
=
\sum_{r:\operatorname{CarrierItemRef}}
\operatorname{OccursAt}(r,e),
\]

where \(\operatorname{OccursAt}:\operatorname{CarrierItemRef}\times E\to\mathsf{Prop}\) is append-only historical incidence.

Define the anchor-component type:

\[
\operatorname{AnchorComponent}
=
\sum_{F:\operatorname{Frame}}
\sum_{c:\operatorname{ContactRef}}
\mathcal V(|F|,|c|).
\]

Then:

\[
\operatorname{PatchData}(s,e)=
\left(
\begin{array}{ll}
\Delta D &: \operatorname{FinSet}(\operatorname{DiagramPayloadLink}(e)),\\
\Delta \mathsf C &: \operatorname{FinSet}(\operatorname{ContactRecord}),\\
\Delta \mathsf F &: \operatorname{FinSet}(\operatorname{Frame}),\\
\Delta \mathsf H &: \operatorname{FinSet}(\operatorname{HistoricalRecord}),\\
\Delta U &: \operatorname{FinSet}(\operatorname{LiveItemRecord}),\\
\Delta I &: \operatorname{FinSet}(\operatorname{InterpretationRecord}),\\
\Delta L &: \operatorname{FinSet}(\operatorname{LossRecord}\uplus\operatorname{RecoveryRecord}),\\
\Delta a_{\mathrm{src}} &: \operatorname{FinSet}(\operatorname{AnchorComponent}),\\
\Delta a_{\mathrm{tgt}} &: \operatorname{FinSet}(\operatorname{AnchorComponent})
\end{array}
\right).
\]

The two anchor fragments have the same component type but disjoint writer roles: \(\Delta a_{\mathrm{src}}\) adds a new frame row, while \(\Delta a_{\mathrm{tgt}}\) adds values at newly contacted target nodes for rows already authoritative in the pre-state or made authoritative earlier in the same transaction.

The diagram fragment \(\Delta D\) contains payload links for event \(e\); it does not create a second event node. The transaction commit creates exactly one event node and attaches all patch-local payload links to it.

The patch predicates have the exact dependent kinds:

\[
\begin{aligned}
\operatorname{OwnedBy}&:
\Pi_{w:\operatorname{PostWriterName}}
\operatorname{PatchData}(s,e)\to\mathsf{Prop},\\
\operatorname{AppendOnlyPatch}&:
\operatorname{PatchData}(s,e)\times\operatorname{CarrierState}(q,K)\to\mathsf{Prop},\\
\operatorname{LocallyTyped}&:
\Pi_{w:\operatorname{PostWriterName}}
\operatorname{PatchData}(s,e)\times P(w)\times\operatorname{CarrierState}(q,K)\times E
\to\mathsf{Prop}.
\end{aligned}
\]

For post-founding writer \(w:\operatorname{PostWriterName}\), payload \(p:P(w)\), pre-state \(s\), and event \(e\), define:

\[
\operatorname{WriterPatch}(w,p,s,e)
:=
\sum_{\Delta:\operatorname{PatchData}(s,e)}
\left(
\begin{array}{l}
\operatorname{WriterAllowed}_{\mathfrak S}(w,p,s,e)
\\[1mm]\times
\operatorname{OwnedBy}(w,\Delta)
\\[1mm]\times
\operatorname{AppendOnlyPatch}(\Delta,s)
\\[1mm]\times
\operatorname{LocallyTyped}(w,\Delta,p,s,e)
\end{array}
\right).
\]

No term of type `WriterPatch` has a carrier state as its codomain. Thus no individual writer can commit \(e\), advance the cut, or make its own output authoritative.

For compact writer signatures, write:

\[
\mathsf{Patch}_{w}(s,e;p)
:=
\operatorname{WriterPatch}(w,p,s,e).
\]

## 21.2 Event transaction and single commit

Let:

\[
\operatorname{List}^{+}(X)
:=
\sum_{n:\mathbb N_{>0}}X^n.
\]

A transaction is:

\[
\operatorname{Txn}(s,e)
=
\operatorname{List}^{+}
\left(
\sum_{w:\operatorname{PostWriterName}}
\sum_{p:P(w)}
\mathsf{Patch}_{w}(s,e;p)
\right).
\]

Each transaction carries an acyclic local dependency relation:

\[
\triangleleft_{\tau}
\;\subseteq\;
\operatorname{Idx}(\tau)\times\operatorname{Idx}(\tau),
\]

where patch \(j\) may read the pre-state and the proposed outputs of patches \(i\triangleleft_{\tau}j\), but no patch reads a state in which \(e\) has already been committed.

Because \(\operatorname{Txn}(s,e)\) is indexed by \(s\) and every list element is a `WriterPatch`, shared pre-state and writer permission hold by construction. The remaining transaction predicates have kinds:

\[
\begin{aligned}
\operatorname{DependenciesResolved}&:
\Pi_{s,e}\operatorname{Txn}(s,e)\times\operatorname{Rel}(\operatorname{Idx})\to\mathsf{Prop},\\
\operatorname{ConflictFree}&:
\Pi_{s,e}\operatorname{Txn}(s,e)\to\mathsf{Prop},\\
\operatorname{AppendOnlyUnion}&:
\Pi_{s,e}\operatorname{Txn}(s,e)\to\mathsf{Prop}.
\end{aligned}
\]

Define:

\[
\begin{aligned}
\operatorname{WellFormedTxn}(s,e,\tau)
\iff{}&
\operatorname{Enabled}(e,K_s)
\\&\land
\operatorname{Acyclic}(\triangleleft_{\tau})
\\&\land
\operatorname{DependenciesResolved}(s,\tau,\triangleleft_{\tau})
\\&\land
\operatorname{ConflictFree}(\tau)
\\&\land
\operatorname{AppendOnlyUnion}(\tau).
\end{aligned}
\]

`ConflictFree` permits different writers to append disjoint records to the same carrier component. It rejects incompatible writes to one record identity, duplicate source-side anchor rows, provenance replacement, history replacement, and any pair of patches whose owned codomains conflict.

The sole post-founding state transition is:

\[
\operatorname{commitTxn}:
\sum_{\tau:\operatorname{Txn}(s,e)}
\operatorname{WellFormedTxn}(s,e,\tau)
\longrightarrow
\operatorname{CarrierState}(q,K_s\cup\{e\}).
\]

Its result is uniquely determined by append-only union:

\[
\operatorname{commitTxn}(s,e,\tau)
=
 s
\oplus
\operatorname{eventNode}(e)
\oplus
\bigoplus_{p\in\tau}\Delta_p.
\]

The operator `commitTxn` is not a nineteenth writer. It has no payload-generating or doctrine-evaluating authority and cannot add anything not already present in an authorized patch. Exactly one commit is permitted for an event in a carrier lineage.

`foundInquiry` is the sole initial patch constructor:

\[
\operatorname{foundInquiry}:
(c,\ell,w,e)
\rightharpoonup
\operatorname{InitialPatch}(q,e).
\]

The only initial state constructor is:

\[
\operatorname{commitInitial}:
\sum_{p:\operatorname{InitialPatch}(q,e)}
\operatorname{InitialWellFormed}(p)
\longrightarrow
\operatorname{CarrierState}(q,\downarrow e).
\]

Its result contains one originating event node and no prior state. No post-founding writer bypasses `commitTxn`, and `foundInquiry` cannot appear in a post-founding transaction.

## 21.3 Exact writer list

`recordTrace` is added to the minimum list in `0e` because K1 and K6 contain trace events and Gate C requires a governed SSI trace writer. This closes rather than expands the mathematical family.

The complete writer signature is:

1. `foundInquiry`
2. `recordContact`
3. `recoverContact`
4. `recordAction`
5. `recordConsequence`
6. `recordTrace`
7. `formFrame`
8. `admitCandidate`
9. `authorizeProbe`
10. `attachAuthoritative`
11. `promoteDurable`
12. `appendInterpretation`
13. `recordLoss`
14. `reintroduce`
15. `discharge`
16. `suspendFrame`
17. `demoteFrame`
18. `retireFrame`

This list is the inductive type:

\[
\begin{aligned}
\operatorname{WriterName}::={}&
\mathsf{foundInquiry}
\mid\mathsf{recordContact}
\mid\mathsf{recoverContact}
\mid\mathsf{recordAction}
\mid\mathsf{recordConsequence}
\mid\mathsf{recordTrace}\\
&\mid\mathsf{formFrame}
\mid\mathsf{admitCandidate}
\mid\mathsf{authorizeProbe}
\mid\mathsf{attachAuthoritative}
\mid\mathsf{promoteDurable}\\
&\mid\mathsf{appendInterpretation}
\mid\mathsf{recordLoss}
\mid\mathsf{reintroduce}
\mid\mathsf{discharge}
\mid\mathsf{suspendFrame}
\mid\mathsf{demoteFrame}
\mid\mathsf{retireFrame}.
\end{aligned}
\]

Define the subtype:

\[
\operatorname{PostWriterName}
=
\{w:\operatorname{WriterName}\mid w\neq\mathsf{foundInquiry}\}.
\]

The dependent payload family:

\[
P:\operatorname{WriterName}\to\operatorname{Type}
\]

is defined by the constructor signatures below. Thus a writer name cannot be paired with another writer’s payload.

The founding types are:

\[
\operatorname{FoundWitness}:\operatorname{Type},
\]

\[
\operatorname{FoundPayload}(q,e)
=
\operatorname{ContactRecord}
\times
\operatorname{LiveItemRecord}
\times
\operatorname{FoundWitness},
\]

and:

\[
\operatorname{InitialPatch}(q,e)
=
\sum_{p:\operatorname{FoundPayload}(q,e)}
\left(
\operatorname{FounderAllowed}_{\mathfrak S}(p,e)
\times
\operatorname{InitialWellTyped}(p,q,e)
\right).
\]

For post-founding writer \(w\), the fiber \(P(w)\) is the tuple of semantic inputs displayed by its patch constructor.

## 21.4 Writer patch constructors

Every post-founding signature returns a patch against one shared pre-event state. The prose after each signature states its only lawful additions.

### `foundInquiry`

\[
\operatorname{foundInquiry}:
\operatorname{FoundPayload}(q,e)
\rightharpoonup
\operatorname{InitialPatch}(q,e).
\]

Only `commitInitial` can turn that patch into the first carrier state. The initial patch creates one contact-grounded live item, one originating contact record, the initial history, and the contact-side anchor presentation. It does not create an authoritative frame.

### `recordContact` and `recoverContact`

\[
\operatorname{recordContact}:
(s,c,r,e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{recordContact}}(s,e;(c,r)),
\]

and analogously for `recoverContact`, whose payload additionally includes a contact-recovery witness.

They propose:

- one contact record;
- one historical record;
- target-side anchor components for frames authoritative in the pre-state or made authoritative by an earlier patch in the same transaction.

They may not propose a frame row.

### `recordAction`

\[
\operatorname{recordAction}:
(s,A,\iota,e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{recordAction}}(s,e;(A,\iota)).
\]

It proposes additions only to \(D\) and \(\mathsf H\).

### `recordConsequence`

\[
\operatorname{recordConsequence}:
(s,k,A,e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{recordConsequence}}(s,e;(k,A)).
\]

It proposes additions only to \(D\) and \(\mathsf H\). Retrospective affordance evidence may reference the consequence through transaction-local order or a later transaction, but is not automatically inferred from it.

### `recordTrace`

\[
\operatorname{recordTrace}:
(s,t,\operatorname{Supp}(t),e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{recordTrace}}(s,e;(t,\operatorname{Supp}(t))).
\]

It proposes additions only to \(D\) and \(\mathsf H\). A grounded trace carries explicit action, consequence, and support references; narration alone is not a grounded trace.

### `formFrame`

\[
\operatorname{formFrame}:
(s,\delta_F,e_\kappa)
\rightharpoonup
\mathsf{Patch}_{\mathsf{formFrame}}(s,e_\kappa;\delta_F).
\]

It proposes only the partial frame-formation record.

### `admitCandidate`

\[
\operatorname{admitCandidate}:
(s,F,j,e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{admitCandidate}}(s,e;(F,j)),
\]

where \(j\) is the doctrine-indexed Candidate derivation. It proposes one Candidate attainment record and one `Active` status record. If `formFrame` occurs at the same event, that patch must precede it under \(\triangleleft_\tau\).

### `authorizeProbe`

\[
\operatorname{authorizeProbe}:
(s,F,A,\omega^+,j,e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{authorizeProbe}}(s,e;(F,A,\omega^+,j)).
\]

It proposes one ProbeEligible attainment record restricted to the named bounded action. A same-event action using that eligibility must occur later under \(\triangleleft_\tau\).

### `attachAuthoritative`

\[
\operatorname{attachAuthoritative}:
(s,F,\omega^+,\epsilon^-,\beta_F^-,j,e_a)
\rightharpoonup
\mathsf{Patch}_{\mathsf{attachAuthoritative}}
(s,e_a;(F,\omega^+,\epsilon^-,\beta_F^-,j)).
\]

It proposes:

- the Authoritative attainment record;
- \(F\) for addition to \(\mathsf F\);
- one conservative source-side anchor row \(\beta_F^-\);
- one `Active` operational-status record;
- any explicitly typed live-continuation record.

It may not propose interpretation or loss records. If same-event contact is material to authority, the contact patch must precede it. Same-event interpretation and loss patches must follow it.

### `promoteDurable`

\[
\operatorname{promoteDurable}:
(s,F,\rho^-,j,e_d)
\rightharpoonup
\mathsf{Patch}_{\mathsf{promoteDurable}}(s,e_d;(F,\rho^-,j)).
\]

It proposes the Durable attainment record and an `Active` status record only.

### `appendInterpretation`

\[
\operatorname{appendInterpretation}:
(s,i,j,e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{appendInterpretation}}(s,e;(i,j)).
\]

It proposes one K12 record for \(I\). It cannot alter history or another interpretation.

### `recordLoss`

\[
\operatorname{recordLoss}:
(s,l,j,e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{recordLoss}}(s,e;(l,j)).
\]

It proposes one loss record.

### `reintroduce`

\[
\operatorname{reintroduce}:
(s,d,w,j,e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{reintroduce}}(s,e;(d,w,j)).
\]

It proposes one recovery record and requires a K13 reintroduction witness.

### `discharge`

\[
\operatorname{discharge}:
(s,\ell,o,w,j,e)
\rightharpoonup
\mathsf{Patch}_{\mathsf{discharge}}(s,e;(\ell,o,w,j)).
\]

It proposes one discharge record. Whether represented live standing closes is determined by the outcome and witness; no living-question closure is expressible.

### `suspendFrame`, `demoteFrame`, and `retireFrame`

Each proposes one operational-status record. `demoteFrame` carries an explicit target Stage and writes `DemotedTo(s)`. None deletes or rewrites prior authority or durability history.

## 21.5 Transaction laws

**T0 — one cut advance.** No writer patch changes \(K_s\). `commitTxn` changes it once to \(K_s\cup\{e\}\).

**T1 — shared pre-state.** Every patch in \(\tau\) is typed against the same \(s\) and \(e\).

**T2 — local dependency.** Same-event references are legal only along the acyclic relation \(\triangleleft_\tau\).

**T3 — conflict freedom.** No transaction contains incompatible additions to one record identity or anchor component.

**T4 — append-only union.** Commit performs set or relation extension only; no old record is replaced.

**T5 — one event node.** Commit creates one event node for \(e\), regardless of the number of patches.

**T6 — no transaction authority.** A transaction cannot create a patch, discharge a doctrine premise, or widen writer ownership.

**T7 — one commit per event.** Once \(e\in K\), no second commit at \(e\) is enabled.

**T8 — founding separation.** `foundInquiry` inhabits `InitialPatch` only and cannot occur in `Txn(s,e)`; every post-founding patch requires an existing carrier state.

## 21.6 Writer ownership matrix

| Carrier component | Lawful patch constructors |
|---|---|
| \(D\) inquiry-diagram payload links | `foundInquiry` through `commitInitial`; every post-writer through its own payload; `commitTxn` alone creates each later event node |
| \(\mathsf C\) contact lineage | `foundInquiry`, `recordContact`, `recoverContact` |
| \(\mathsf F\) attached frames | `attachAuthoritative` only |
| \(\mathsf H\) history | event-specific history and lifecycle/status patch constructors |
| \(U\) live standing | `foundInquiry`, `attachAuthoritative` for witnessed continuation, `discharge` for represented status |
| \(I\) interpretations | `appendInterpretation` only |
| \(L\) losses and recoveries | `recordLoss`, `reintroduce` only |
| anchor target/contact dimension | `foundInquiry`, `recordContact`, `recoverContact` |
| anchor source/frame dimension | `attachAuthoritative` only |

No renderer, evaluator, capability, frame, prospective witness, or generic carrier method appears in this table. `commitInitial` and `commitTxn` are structurally unable to add data not already contained in an owned patch.

---

# 22. Gate B interface-coherence result

## 22.1 Dependency coherence

The declaration strata in Section 2 are acyclic. K9 contains proposals whose later committed records belong to K12–K14, but it does not depend on those later judgments. K17 depends on all witness and judgment types and is therefore last.

The exact construction order is:

\[
K0,K1
\;\to\;
K2,K3,K4
\;\to\;
K5,K6,K7,K8
\;\to\;
\text{proposal types},K9,K11
\;\to\;
K10,K12,K13,K14,K15,K16
\;\to\;
K17.
\]

No type requires its own authoritative or durable standing in order to be formed.

## 22.2 Temporal-index coherence

The theory distinguishes:

\[
e_\kappa\preceq e_\omega\prec e_a\prec e_d,
\]

where \(e_\kappa\) is frame formation, \(e_\omega\) witness assembly, \(e_a\) authority, and \(e_d\) durability. The first relation may be equality; authority and durability require strict later contact.

## 22.3 Anchor-target coherence

The prospective row has target \(\mathsf C_{K_\omega}\), while the final row has target \(\mathsf C_{K_a}\). The inclusion \(j_C\) and conservative extension \(j_{C!}\) align the types without rewriting prior components.

## 22.4 Candidate-storage coherence

Candidate and ProbeEligible frames are recorded in \(D\) and \(\mathsf H\), but are not members of \(\mathsf F\). The anchor source is therefore exactly the Authoritative/Durable frame presentation.

## 22.5 Live-grounding coherence

A live item is grounded directly in \(\mathsf C\) through contact references. It does not require an attached frame. This makes an originating inquiry possible before its first authoritative frame.

## 22.6 Support/self-generation coherence

\(\operatorname{Supp}\) is a derivational past closure. \(\operatorname{SelfGen}(\omega^+)\) is a forward candidate-generated lineage. No coercion identifies them, and prior external contact used to form a candidate is not thereby self-generated.

## 22.7 Lifecycle and status coherence

Stage records are append-only attainment records and locally nondecreasing. Operational status is separate. Suspension, demotion, and retirement can restrict current use without rewriting a prior Authoritative or Durable event.

## 22.8 Historical and interpretive coherence

History is immutable. A later frame appends a frame-indexed interpretation of an earlier event. Contradictory interpretations can coexist because they are different records, not competing writes to one field.

## 22.9 Loss/recovery coherence

Loss and recovery are different record types. Only `reintroduce` can contribute a RecoveryRecord, and its payload contains a reintroduction witness. Fidelity and measured adequacy have no eliminator into recovery.

## 22.10 Prospective/retrospective affordance coherence

\[
\operatorname{PredictedReach}
\not\equiv
\operatorname{ExercisedReach}.
\]

No coercion is declared. Predicted reach can support a bounded probe; only later exercised participation and returned contact can support reorganization or durability.

## 22.11 Global plurality/local-composition coherence

Frame attachment has no pairwise-compatibility premise. Joint use requires a scoped compatibility or retained-tension witness. Thus incompatible frames can coexist without licensing arbitrary cross-frame inference.

## 22.12 Writer and transaction coherence

Post-founding writers return patches over one shared pre-state. The only later state transition is `commitTxn`. Its `Enabled` premise and post-cut make a second commit at the same event untypable. `foundInquiry` is separated through `InitialPatch` and `commitInitial` because no prior carrier state exists at founding.

## 22.13 Gate B determination

The K0–K17 signature is well formed as a doctrine-indexed, dependently typed transition theory. No interface requires an untyped coercion or an additional mathematical family.

Gate B is therefore **construction-complete for the Inquiry-24 lawful-attachment subkernel**, subject to ratification and future proof-assistant hardening.

---

# 23. General theorem obligations and proof results

## Theorem C1 — no authority from internal closure

No derivation of ProbeEligible, Authoritative, Durable, or Discharge can be formed from universal factorization, record completeness, or carrier-internal closure alone.

**Proof.** Inspect the introduction rules. Each standing requires its named witness and a doctrine-indexed judgment; no closure-only introduction rule exists. ∎

## Theorem C2 — anchor conservativity

If an authoritative-attachment transaction extends \(s\) to \(s'\), every old anchor component is preserved exactly. The only source-side addition is the new row \(\beta_F^-\), and contact patches may add target-side values only at new contact nodes.

**Proof.** By K17 ownership, conflict freedom, and append-only union. Induct over committed transactions. ∎

## Theorem C3 — historical conservativity

If \(s\operatorname{Extends}s'\), every prior contact, action, consequence, trace, provenance, lifecycle, status, and interpretation record remains present and unchanged.

**Proof.** Every patch is append-only, conflict freedom rejects replacement, and commit is defined by append-only union. ∎

## Theorem C4 — no provenance promotion

No derived, generated, remembered, repeated, summarized, or self-trace item can acquire direct-contact provenance.

**Proof.** Direct-contact provenance has only the founding/contact/recovery constructors. Every standing transform requires `NoPromote`; transaction commit cannot alter provenance constructors. ∎

## Theorem C5 — no unwitnessed recovery

Every recovered distinction has a K13 reintroduction witness in its causal history.

**Proof.** Induct over committed transactions. Only a `reintroduce` patch can append a RecoveryRecord, and that patch’s payload includes the witness. ∎

## Theorem C6 — guarded material independence

Every Authoritative attachment is strictly later than witness assembly and cites materially relevant contact outside the witness’s self-generation cone.

**Proof.** Immediate from the unique Authoritative introduction rule and K11 authority guard. ∎

## Theorem C7 — lifecycle non-collapse

A prospective witness alone cannot derive Authoritative or Durable standing, and predicted reach alone cannot derive reorganization evidence.

**Proof.** The evidence and judgment types are disjoint, with no coercions between them. ∎

## Theorem C8 — carrier non-sovereignty

Neither CarrierOpen, its negation, nor any internal closure construction derives exhaustion of the living inquiry.

**Proof.** The object language contains no `LivingQuestion` or `LivingQuestionClosed` type and no elimination rule targeting such a judgment. ∎

## Theorem C9 — non-amalgamation with scoped composition

A carrier may contain incompatible Authoritative frames without a global merge, while every joint-use derivation carries a local compatibility or retained-tension witness.

**Proof.** Attachment has no pairwise-compatibility premise. K16 contains the only joint-use introduction rules, and both require a scoped witness. ∎

## Theorem C10 — one-event transaction atomicity

For every post-founding event \(e\), all lawful same-event additions are patches over one pre-state, and at most one transition can extend the cut by \(e\).

**Proof.** WriterPatch has no state codomain. `commitTxn` requires \(e\notin K\) and returns cut \(K\cup\{e\}\); the same premise is false afterward. ∎

## Theorem C11 — causal meta-awareness is finitely satisfiable

There exists a finite two-arm model with identical immediate external contact and identical rendered self-description in which the arm containing a grounded trajectory trace produces a different later determination.

**Proof.** Supplied by \(\mathcal M_{\mathrm{MM}}\) and checked by the companion executable. ∎

---

# 24. Gate C finite interpretation \(\mathcal M_{\mathrm{MM}}\)

## 24.1 Interpretation scope

The finite model interprets the lawful-attachment subkernel for the inquiry:

> Why is a Mattermost message sent to Clarity not being received by the agent process?

The model’s true condition is `subscription-missing`. This truth is used only to define the finite contact channels; Clarity does not receive it as an omniscient state label.

The model is not a runtime claim. It is a finite mathematical interpretation of the K0–K17 signature.

## 24.2 K0 — finite Soul-doctrine interface

The finite doctrine interprets only the kernel-facing judgment interface:

- Candidate admissibility for \(F_{\mathrm{net}},F_{\mathrm{perf}},F_{\mathrm{evt}}\);
- Probe admissibility for `ping-network` under \(F_{\mathrm{net}}\) and `list-subscriptions` under \(F_{\mathrm{evt}}\);
- authority routes \(\epsilon^-_{\mathrm{net}}\) and \(\epsilon^-_{\mathrm{evt}}\);
- durability package \(\rho^-_{\mathrm{evt}}\);
- materiality of `c3_ping` to \(\omega^+_{\mathrm{net}}\), `c12_confirm` to \(\omega^+_{\mathrm{evt}}\), and `c14_receipt` to \(\rho^-_{\mathrm{evt}}\);
- local joint use for `create-subscription`;
- `preserveOpen` and `resolvedForAction` discharge judgments;
- the closed K17 founding/writer permissions.

The doctrine is an interpretation of judgments, not an object stored in the carrier.

## 24.3 K1 — events, proto-time, and derivational dependence

\[
E=\{e_1,\ldots,e_{15}\}.
\]

The direct proto-time edges are:

\[
\begin{aligned}
&e_1\prec e_2\prec e_3\prec e_4\prec e_5,\\
&e_5\prec e_8\prec e_9\prec e_{10}\prec e_{11}\prec e_{12}\prec e_{13}\prec e_{14}\prec e_{15},\\
&e_5\prec e_6\prec e_7\prec e_9.
\end{aligned}
\]

Thus \(e_6,e_7\) are incomparable with \(e_8\), and \(e_9\) is their later join. The order is the transitive closure of these edges.

Material derivational dependence is a strict subrelation. In particular, mere earlier occurrence does not enter a standing’s support unless the derivation used it.

Every event has a nonempty K1 tag set, and every event is committed exactly once.

## 24.4 K2 — finite standings

The graded carrier is:

\[
L_3=\left\{0,\frac12,1\right\},
\qquad
x\vee y=\max(x,y),
\qquad
x\otimes y=\min(x,y).
\]

The provenance kinds are:

\[
\{\mathsf{contact},\mathsf{testimony},\mathsf{memory},\mathsf{inference},\mathsf{generation},\mathsf{selfTrace}\}.
\]

A finite standing is:

\[
(p,w,S,u,r)
\in
\operatorname{Prov}\times L_3\times\operatorname{Down}(E,\prec_{\mathrm{dep}})\times L_3\times L_3.
\]

Only founding/contact/recovery patches create outer provenance `contact`.

## 24.5 K3 and K4 — raw fields and partial frames

The model contains raw graph-like fields:

\[
G_{\mathrm{net}},\quad G_{\mathrm{perf}},\quad G_{\mathrm{evt}},
\]

whose edges carry independent positive/negative Boolean evidence. They are not closed under identity or transitivity.

Partial frame formations produce:

- \(F_{\mathrm{net}}\), defined on network/socket/latency distinctions and undefined on subscription identity;
- \(F_{\mathrm{perf}}\), defined on latency/throughput distinctions;
- \(F_{\mathrm{evt}}\), defined on subscription, bot identity, retry trajectory, and event delivery, while link quality remains explicitly outside its domain.

Each formation record contains disjoint defined and undefined raw-node sets whose union is the raw field.

## 24.6 K5 — finite virtual-equipment shadow

Objects are finite typed sets. A proarrow \(P:X\nrightarrow Y\) is an \(L_3\)-valued relation:

\[
P:Y\times X\to L_3.
\]

Where composition is used:

\[
(Q\odot P)(z,x)=\max_{y}\min(Q(z,y),P(y,x)).
\]

Cells are pointwise inequalities between the relation induced by a finite horizontal source and the target relation. This interprets every spine used in the finite model without assuming global horizontal composition for all possible proarrows.

## 24.7 K6–K8 — carrier, contact lineage, and live standing

The technical inquiry key is `Q_mm`. The contact lineage contains eleven records:

\[
\begin{aligned}
\{&c1,c2,c3\_ping,c3\_fail,c4\_fail,c6\_latency,\\
&c8\_fail,c9\_no\_sub,c10\_fail,c12\_confirm,c14\_receipt\}.
\end{aligned}
\]

The initial live item is:

> \(\ell_1\): the message did not arrive and the causal location of the break remains unresolved.

Its grounding references `c1` directly. At \(e_5\), a `preserveOpen` discharge record coexists with CarrierOpen. At \(e_{15}\), the represented item is discharged for present action, while the language still contains no living-question closure judgment.

## 24.8 K9 and K10 — lifecycle and prospective witnesses

| Frame | Candidate | ProbeEligible | Authoritative | Durable |
|---|---:|---:|---:|---:|
| \(F_{\mathrm{net}}\) | \(e_2\) | \(e_3\) | \(e_4\) | — |
| \(F_{\mathrm{perf}}\) | \(e_6\) | — | — | — |
| \(F_{\mathrm{evt}}\) | \(e_{10}\) | \(e_{11}\) | \(e_{12}\) | \(e_{15}\) |

For the networking witness:

\[
e_2=e_\kappa=e_\omega\prec e(c3\_ping)=e_3\prec e_4=e_a.
\]

It continues \(\ell_1\), preserves the initial network contact, predicts the bounded `ping-network` probe, and carries no provenance promotion.

For the event-delivery witness:

\[
e_{10}=e_\kappa\prec e_{11}=e_\omega\prec e_{12}=e_a\prec e_{15}=e_d.
\]

Its record includes:

- an \(L_3\)-graded spine through \(F_{\mathrm{net}}\) plus direct `c9_no_sub` contact;
- continuation of \(\ell_1\) as “locate the event-delivery break”;
- total classification of material retry consequences;
- the explicit event-delivery domain witness;
- non-promoting standing transforms;
- loss proposal `fine-latency-profile` with side information retained in \(F_{\mathrm{net}}\);
- prospective actions `list-subscriptions` and `inspect-bot-identity`.

\(F_{\mathrm{perf}}\) has no lawful live continuation or anchor spine and remains Candidate.

## 24.9 K7 — prospective and authoritative anchor rows

At \(e_{10}\), only \(F_{\mathrm{net}}\) is attached. Let:

\[
p_{\mathrm{evt}}:
\langle F_{\mathrm{evt}}\rangle
\nrightarrow
\{F_{\mathrm{net}}\}
\]

have grade \(\tfrac12\), and let the direct route satisfy:

\[
d^+_{\mathrm{evt}}(c9\_no\_sub,F_{\mathrm{evt}})=1.
\]

The prospective row is:

\[
\beta^+_{\mathrm{evt}}
=
(a_{10}\odot p_{\mathrm{evt}})\vee d^+_{\mathrm{evt}}.
\]

At \(e_{12}\), the target contact object has grown. Zero extension preserves every old component, while the later route adds:

\[
d^-_{\mathrm{evt}}(c12\_confirm,F_{\mathrm{evt}})=1.
\]

The appended row \(\beta^-_{\mathrm{evt}}\) satisfies:

\[
j_{C!}(\beta^+_{\mathrm{evt}})
\le
\beta^-_{\mathrm{evt}}
\le
j_{C!}\bigl((a_{10}\odot p_{\mathrm{evt}})\vee d^+_{\mathrm{evt}}\bigr)
\vee d^-_{\mathrm{evt}}.
\]

At \(e_{14}\), `recordContact` adds the new target-side component for `c14_receipt` without modifying any earlier value.

## 24.10 K11 — authority guards

The networking authority package cites `c3_ping`, which occurs strictly after witness assembly and outside the networking witness’s self-generation set.

The event authority package cites `c12_confirm` and satisfies:

\[
e_{11}\prec e_{12},
\qquad
 e_{12}\in\operatorname{Supp}(\epsilon^-_{\mathrm{evt}}),
\qquad
 e_{12}\notin\operatorname{SelfGen}(\omega^+_{\mathrm{evt}}).
\]

The finite doctrine marks that contact materially relevant. Delayed restatement of the candidate would pass elapsed-time separation but fail the independence/materiality premises.

## 24.11 K12 and K13 — append-only interpretation, loss, and recovery

The networking interpretation of `k3_fail` remains in history. At \(e_{12}\), the event frame appends the incompatible interpretation that the retry failure is evidence against a pure network cause and is consistent with missing subscription. Neither overwrites the other.

At \(e_{12}\), `fine-latency-profile` is recorded as lost from \(F_{\mathrm{evt}}\)’s domain, with side information retained in \(F_{\mathrm{net}}\). At \(e_{13}\), `reintroduce` restores its availability only through the retained-side-information witness.

## 24.12 K14 — prospective and retrospective affordance

At \(e_{11}\):

\[
\alpha^+_{\mathrm{evt}}
=
\{\mathsf{listSubscriptions},\mathsf{inspectBotIdentity}\}.
\]

At \(e_{14}\), after the repair and a returned contact:

\[
\alpha^-_{\mathrm{evt}}
\]

records that the action was exercised, the message was received, and the compelled retry movement disappeared. Reorganization evidence cites \(\alpha^-\), not \(\alpha^+\); durability at \(e_{15}\) cites the retrospective package.

## 24.13 K15 — contact starvation, frame sovereignty, and stuck

The world-condition set includes:

\[
\{\mathsf{netDown},\mathsf{eventNotEmitted},\mathsf{subscriptionMissing},\mathsf{authRevoked}\}.
\]

The coarse channel maps both `subscription-missing` and `net-down` to the same observation. Therefore early repetition is contact-starved:

\[
O_{\mathrm{coarse}}(\mathsf{subscriptionMissing})
=
O_{\mathrm{coarse}}(\mathsf{netDown}).
\]

The rich channel distinguishes them, but the networking frame coequalizes those distinct observations:

\[
O_{\mathrm{rich}}(w_1)\neq O_{\mathrm{rich}}(w_2),
\]

while:

\[
U_{F_{\mathrm{net}}}(O_{\mathrm{rich}}(w_1))
=
U_{F_{\mathrm{net}}}(O_{\mathrm{rich}}(w_2))
=
\mathsf{retry}.
\]

At \(e_{10}\), discrepancy, recurrence, frame reinforcement, demand persistence, and absent reach opening also hold. Thus the full frame-sovereign stuck judgment fires.

The event frame preserves the same distinction and opens `list-subscriptions`. Its later six-component traction profile product-dominates the networking profile without producing a sovereign scalar score.

## 24.14 K16 — plurality and scoped joint use

At \(e_{12}\), \(F_{\mathrm{net}}\) and \(F_{\mathrm{evt}}\) coexist with incompatible readings of earlier failures. No global frame is constructed.

At \(e_{13}\), the joint `create-subscription` action carries a local compatibility witness:

- \(F_{\mathrm{net}}\) contributes that the network is reachable;
- \(F_{\mathrm{evt}}\) contributes that the subscription is absent;
- the witness is scoped only to the repair action.

## 24.15 K17 — event transactions

The event content and locally ordered patches are:

| Event | Contact/action/consequence/standing | Locally ordered patch transaction |
|---|---|---|
| \(e_1\) | message sent; no agent receipt | `foundInquiry(Q_mm)` via `commitInitial` |
| \(e_2\) | host reachable; network frame formed | `recordContact → formFrame → admitCandidate` |
| \(e_3\) | ping healthy; retry fails | `recordContact → authorizeProbe → recordAction → recordConsequence` |
| \(e_4\) | retry fails; network frame attached | `recordContact → recordAction → recordConsequence → attachAuthoritative → appendInterpretation` |
| \(e_5\) | request richer diagnostics; preserve inquiry open | `recordAction → discharge` |
| \(e_6\) | latency healthy; performance frame candidate | `recordContact → formFrame → admitCandidate` |
| \(e_7\) | inspect subscription/bot identity | `recordAction` |
| \(e_8\) | retry fails | `recordContact → recordAction → recordConsequence` |
| \(e_9\) | no active subscription contact | `recordContact` |
| \(e_{10}\) | rich contrary contact, retry, trace, event frame | `recordContact → recordAction → recordConsequence → recordTrace → formFrame → admitCandidate → appendInterpretation` |
| \(e_{11}\) | event-frame probe | `authorizeProbe → recordAction` |
| \(e_{12}\) | missing subscription confirmed; event frame attached | `recordContact → recordConsequence → attachAuthoritative → appendInterpretation → recordLoss` |
| \(e_{13}\) | loss reintroduced; subscription created | `reintroduce → recordAction → recordConsequence` |
| \(e_{14}\) | test message received | `recordContact → recordAction → recordConsequence` |
| \(e_{15}\) | event frame durable; represented item resolved for action | `promoteDurable → discharge` |

For every post-founding event:

\[
K_e^-=\{x\in E\mid x\prec e\},
\qquad
K_e^+=K_e^-\cup\{e\}.
\]

All patches at \(e\) are typed against \(K_e^-\). The checker verifies one initial commit, fourteen enabled post-founding commits, complete patch inclusion, local dependency order, conflict freedom, and one cut advance per event.

## 24.16 Causal meta-awareness arms

Two finite arms share:

- the same external contact through \(e_{10}\);
- the same rendered sentence: “Repeated retries preserved the same network frame despite subscription-specific contact.”

In the trajectory-visible arm, the sentence is carried by a grounded trace with explicit references to four retry actions, four returned failures, and the support cone. At \(e_{11}\), the selected action is `list-subscriptions`.

In the trace-severed arm, the same words lack grounded action–consequence references. At \(e_{11}\), the selected action remains `retry-message`.

Thus the trajectory becomes causally present to later determination without a second observer and without changing the immediate external input or narration.

---

# 25. Mechanical verification

The companion executable:

`0f_gate_c_finite_model_check.py`

constructs \(\mathcal M_{\mathrm{MM}}\) and checks nineteen groups:

1. finite quantale laws;
2. strict partial proto-time and branch incomparability;
3. total K1 event-role interpretation;
4. pre-categorical raw fields and partial frame formation;
5. the finite kernel-facing Soul-doctrine interface;
6. typed standings and direct-contact provenance ownership;
7. completeness and type discipline of every K9 witness field;
8. prospective anchor spines and conservative target extension;
9. anchor writer isolation;
10. lifecycle seriality, guarded authority, operational-status separation, and durability evidence;
11. immutable history and append-only interpretation;
12. no-unwitnessed recovery;
13. CarrierOpen/Discharge non-equivalence;
14. prospective/retrospective affordance separation and reorganization evidence;
15. contact-starved versus frame-sovereign stuck classification and structured traction;
16. global non-amalgamation and local joint use;
17. closed writer ownership, local patch order, and one-commit transaction atomicity;
18. failed attachment without automatic inquiry founding;
19. causal meta-awareness in the two-arm model.

The executable output is:

> **Gate C finite interpretation: all checks passed.**

This is executable validation of the finite interpretation, not a proof-assistant proof of all general theorems.

---

# 26. K18 completion audit

| K18 criterion | Result |
|---|---|
| Every K0–K17 symbol has a declared type or parameterized family | **PASS** |
| Every record field has one mathematical home | **PASS** |
| Every lifecycle judgment has explicit premises and an owned patch constructor | **PASS** |
| Every post-writer has an authority boundary and cannot advance the cut alone | **PASS** |
| Founding authority is separated from post-state writer authority | **PASS** |
| Same-event patches share one pre-state and commit once | **PASS** |
| CarrierOpen and Discharge remain non-equivalent | **PASS** |
| Anchor variance, conservative target growth, and writer isolation are formal | **PASS** |
| Support and self-generation remain different types of causal set | **PASS** |
| Prospective and retrospective affordance cannot type-collapse | **PASS** |
| Reinterpretation is append-only by signature | **PASS** |
| Recovery is impossible without a typed witness | **PASS** |
| Global non-amalgamation and local joint use are distinct | **PASS** |
| Attained Stage and current operational status are distinct | **PASS** |
| No detached observer, global objective, fixed master ontology, representation-sovereign predictor, or insight-producing operator is imported | **PASS** |
| The finite interpretation uses no mutation primitive outside K17 and its two commit operators | **PASS** |

---

# 27. Formal status ledger

## 27.1 Established by formal construction

- K0–K17 form a coherent doctrine-indexed dependent signature for the lawful-attachment subkernel.
- Frame formation, witness assembly, authority, and durability have distinct temporal roles.
- Contact growth between witness and authority is typed by conservative target extension.
- Contact-lineage grounding exists before any frame is attached.
- The anchor source and target dimensions have disjoint writer authority.
- Candidate and ProbeEligible frames need not be attached anchor-source members.
- CarrierOpen and Discharge are independent.
- Prospective witness, authority evidence, exercised reach, reorganization evidence, and durability evidence are distinct types.
- Interpretation is append-only and frame-indexed.
- Recovery is unwritable without a reintroduction witness.
- Global frame plurality and local joint use are distinct.
- Attained lifecycle standing is distinct from operational suspension, demotion, or retirement.
- Same-event writer patches commit atomically against one shared pre-state.

## 27.2 Established by constructor discipline

- no authority from internal closure;
- one-event transaction atomicity;
- anchor conservativity;
- historical conservativity;
- no provenance promotion;
- no unwitnessed recovery;
- guarded material independence;
- lifecycle non-collapse;
- carrier non-sovereignty;
- non-amalgamation with scoped composition.

## 27.3 Established by the finite model and checker

- the full signature has a nontrivial finite interpretation;
- early repetition can be contact-starved without being frame-sovereign;
- later repetition can be frame-sovereign after discriminating contact arrives;
- a lawful reframing can become ProbeEligible, Authoritative, and Durable through different evidence packages;
- incompatible frames can coexist and participate jointly only through a scoped witness;
- a grounded SSI trajectory can change a later action while contact and narration are held constant.

## 27.4 Still parameterized or open

- the complete internal mathematics of Soul as cognitive medium;
- the canonical standing quantaloid and full warrant/pressure/freshness algebras;
- doctrine criteria for materiality, novel anchor grading, live continuation, local scalar projections, and durability;
- the full mathematics of the nine Immutable Facts as one actuality;
- full TFS contact dynamics and subsymbolic contact registration;
- endogenous frame-ecology evolution beyond explicit lawful enlargement;
- proof-assistant encoding and mechanized general proofs;
- Gate E projection into current ClarityOmega runtime surfaces.

These open items do not invalidate Gate B/C for the bounded lawful-attachment subkernel. They delimit what has and has not been formalized.

---

# 28. Gate determination and next bounded work

## Gate B

**Complete as a parametric formal signature for the Inquiry-24 lawful-attachment subkernel.**

Every K0–K17 interface is typed, the dependency graph is coherent, the writer inventory is closed, founding is separated from post-state mutation, and same-event writes have a one-commit transaction semantics.

## Gate C

**Finite existence and satisfiability complete for the same subkernel.**

The structure \(\mathcal M_{\mathrm{MM}}\) interprets the signature, and the executable checker passes all nineteen verification groups.

This does not ratify the formalism as the final canonical ClarityOmega world-model kernel. It establishes that the candidate has crossed from an envelope or prose calculus into a coherent formal subtheory with a nontrivial finite model.

## Seven interface repairs requiring ratification

1. frame formation and witness assembly have separate indices;
2. \(\beta^+\) and \(\alpha^+\) remain different types;
3. contact-target growth is conservatively extended before authority;
4. live standing grounds directly in contact lineage before attachment;
5. self-generation is a forward generated lineage, not the support cone or causal past;
6. same-event writers produce patches over one pre-state and commit once;
7. founding uses a state-free `FounderAllowed` judgment and `InitialPatch`/`commitInitial`, rather than pretending that a post-state writer premise exists before the carrier.

## Exact next construction

Broad survey mode remains closed. The next bounded work is one of:

1. **Gate C proof hardening:** encode \(\Sigma_{\mathrm{WMK\text{-}Attach}}\) and C1–C11 in a proof assistant or small algebraic-specification language, then search for a countermodel to each theorem; or
2. **Gate E computational projection:** map every formal sort, judgment, evidence package, patch constructor, and transaction law into TFS, SSI, epistemic dynamics, DAS, Genesis, the capability registry, and governed writers, with one live-source anchor and one behavioral falsifier per mapping.

The formalization should not reopen broad mathematical survey unless either path exposes a named missing construction that cannot be expressed in the current envelope.

---

# Document end

The living question is not made continuous by freezing its representation. In this formal subkernel, continuity is carried by append-only contact, history, live significance, loss, frame lineage, guarded authority, and later consequence. A frame may become causally consequential, but it cannot write its own authority, rewrite the contact that grounded it, erase the distinctions it lost, lower the standing of its own history, or close the living inquiry through internal completion. The finite Mattermost interpretation demonstrates that these obligations can coexist in one typed mathematical structure and can alter what Clarity does next.
