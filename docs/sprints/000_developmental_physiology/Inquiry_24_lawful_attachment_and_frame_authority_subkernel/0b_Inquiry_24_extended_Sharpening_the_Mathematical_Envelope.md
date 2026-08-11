# 0b Inquiry 24 extended: Sharpening the Mathematical Envelope

**Status:** ANALYSIS FOR AGGREGATE REVIEW. Not governing ground. Written to be read against `0a_Inquiry_24_The_Dynamic_Heart_of_the_World_Model_Kernel.txt` and `006_ClarityOmega_Meta_Aware_World_Model_Kernel_Grounding_Artifact.md`.
**Version:** v1, 2026-08-05.
**Author:** Claude, at Berton's request, as input to an overarching aggregate analysis.
**Role:** Extends the 0a formalization investigation. Identifies more leveraged mathematics for the obligations 0a establishes, sharpens the envelope of 0a Section 7, and proposes candidate answers to open questions 4, 7, and 11 of 006 Section 22.4. Nothing here overrides 006 or 0a; where this artifact and 006 disagree, 006 wins until Berton rules otherwise.

---

## 0. Method and provenance note

Per Principle 0, the claims in this artifact sort into three kinds, and they are labeled throughout:

1. **Read this session.** Both source documents were read end to end in the session that produced this artifact. All claims about what 0a or 006 says trace to those reads.
2. **Literature.** Claims about established mathematics (equipments, guarded recursion, graded modal types, restriction categories, sheaf contextuality, and so on) are background mathematical knowledge, not claims about the ClarityOmega runtime. Each is marked with a maturity level: MATURE (decades of development, textbook or near-textbook), ACTIVE (established research programme, usable now, still moving), or EARLY (promising but immature, not yet safe to build on).
3. **Proposal.** New constructions or definitions proposed here for the first time in this project are marked PROPOSAL. They are candidates to be tested against the ten obligations and the 006 failure conditions, not conclusions.

No claim in this artifact asserts anything about the current live runtime. Where a runtime connection is suggested (Section 15), it is a design suggestion to be verified against live source in its own session.

---

## 1. What 0a establishes and what this artifact adds

0a's central results are accepted here as the working ground for this extension:

- the six aspects are one inquiry movement, not six modules;
- the ten obligations are the acceptance surface for any candidate mathematics;
- (τ, Exp) is a frame-local presentation, not the living question;
- the boxed central problem: how can a question remain alive and continuous while everything by which it is presently represented is allowed to change;
- the envelope of Section 7: an evolving, indexed, open-process double-categorical structure with coalgebraic or sheaf-valued temporal behavior, guarded internal feedback, contextual non-gluing, viability-style affordance geometry, and quantaloid enrichment.

This artifact adds six things:

1. **A fusion.** Two of 0a's separate candidate families (4.1 double categories and 4.7 quantaloids) are one known construction. This is not a new proposal; it is a fact about existing mathematics that makes the envelope tighter and cheaper (Section 2).
2. **A simplification of the next cut.** The three motifs 0a Section 11 proposes to compare (lineage, indexed transport, higher-cell witness) are the same structure viewed at three levels of one equipment. The comparison question changes shape (Section 3).
3. **Exact names for the guarded-reflexivity motif**, including a result that turns the lifecycle law "no mechanism may self-certify" from a design rule into a typing theorem, and with it a candidate answer to 006 open question 7 (Section 6).
4. **A candidate answer to 006 open question 4** (contact-starved versus frame-sovereign repetition) as a factorization question: locate where discriminating information dies (Section 9).
5. **Three exact mathematical shapes for "ambient rather than object"**, addressing 006 open question 11 and the part 0a calls least solved and most important: Soul as medium (Section 11).
6. **A set of near-term runtime shadows**: disciplines implementable without waiting for the full mathematics, each of which is the finite, operational shadow of one of the formal structures (Section 15).

---

## 2. The backbone, made precise: the equipment of quantaloid-enriched categories

**Kind: literature (MATURE core, ACTIVE at the edges). Leverage: high.**

0a Section 4.1 proposes double categories of open systems as the strongest backbone motif. 0a Section 4.7 proposes quantales and quantaloids as the enrichment and evaluative carrier, explicitly "an enrichment layer rather than the complete backbone." These are presented as two candidates to be combined later.

They are already combined in existing mathematics. For a quantaloid Q, the Q-enriched categories, Q-enriched functors, and Q-enriched distributors (also called profunctors or bimodules) assemble into a **proarrow equipment**, equivalently a **framed bicategory**: a double category in which

- **vertical (tight) arrows** are Q-functors: structure-preserving maps, the natural home for enacted moves;
- **horizontal (pro) arrows** are Q-distributors: graded relations between Q-categories, the natural home for frame translations;
- **squares** are 2-cells witnessing compatibility between an enacted move and a relational translation;
- every tight arrow has a **companion** and a **conjoint**: canonical proarrows representing it, so enacted moves convert to relations and back without loss of the witness structure.

This is the standard theory of quantaloid-enriched category theory (Stubbe's programme and its relatives) meeting the standard theory of framed bicategories (Shulman) and proarrow equipments (Wood). The point for this project:

> **The backbone and the enrichment are not two layers to be glued. They are one construction. The double category 0a wants is the equipment whose proarrows are already quantaloid-graded.**

Why distributors are the right frame-translation arrows, checked against the obligations:

- A frame translation is generally **not a function**. Some distinctions in the old frame have no image; some have several partial images; some content of the new frame answers to nothing prior. A distributor is exactly a typed, graded relation, so partiality and multiplicity are native, not bolted on (Obligation 3).
- Distributor composition aggregates chains of translation, and because the homs are Q-valued, **loss composes automatically**: the grade of a composite translation is bounded by the grades of its factors through the quantaloid multiplication. Translation loss is not an annotation; it is the arithmetic of composition (Obligation 2, the preservation-and-loss clause).
- The equipment's squares are precisely the "compatibility witnesses rather than strict equality" that 0a 4.1 identifies as the preserved virtue, now carrying grades.

**Safe weakening (literature, ACTIVE).** If frame translations do not always compose (composing two translations may require loss data that does not exist), the correct weakening is a **virtual double category** (virtual equipment): squares may have composite horizontal sources without horizontal composition being everywhere defined. This keeps every obligation-relevant structure while dropping the one assumption most likely to be false in practice. Recommendation: state the backbone as a virtual equipment and treat full compositionality of translations as a property to be earned per translation family, not assumed globally.

**What this does not solve.** The equipment does not by itself supply living-question identity, temporal behavior, endogenous reflexivity, evolution of the frame ecology, or Soul as medium. Those are Sections 4 through 11. The claim here is narrower: 0a's strongest backbone motif and its designated enrichment carrier are one object, and adopting that object removes an entire integration seam from the programme.

---

## 3. The three motifs of 0a Section 11 are one structure at three levels

**Kind: analysis of 0a in the light of Section 2. Leverage: reframes the proposed next inquiry.**

0a Section 11 proposes that the next focused cut compare three motifs for living-question continuity without yet selecting among them: (1) lineage or path, (2) indexed transport with residual loss, (3) higher-cell witness. In the equipment of Section 2 these are not rivals. They are the same structure read at three levels:

- **Lineage or path** is a composable string of proarrows (frame translations) and tight arrows (enacted segments): a path in the double category.
- **Indexed transport** is what companions, conjoints, and Kan lifts along tight arrows provide: the canonical way of moving frame-local content along a translation, with the residual measured by the failure of the relevant unit or counit to be invertible (Section 5 makes this computable).
- **Higher-cell witness** is a square: the 2-dimensional cell relating an enacted trajectory segment to a frame transformation.

Consequently the next-cut question is not "which motif carries continuity" but:

> **Does the chosen equipment have enough structure (companions, conjoints, the needed Kan lifts, and tabulators or their virtual analogues) that lineage, transport, and witness interconvert? And where interconversion fails, is the failure itself meaningful (a translation with no canonical transport, a witness with no path)?**

One genuinely open sub-question survives the reframing, and it is sharper than before:

**The zigzag question (proposal).** Must two presentations of one living question always be connected by a composable chain of translations, or can continuity hold through a **zigzag**: both presentations related by witnesses into a common third presentation, with no direct arrow between them? Insight of the discontinuous kind (0a 2.6, 006 Section 13.1 subsymbolic reorganization) suggests zigzags must be admitted: the new frame may not be reachable from the old by any translation, yet both answer to one lineage through what the reorganization preserved. Formally this means living-question continuity is the equivalence-like relation generated by spans and cospans of witnessed translations, not the one generated by direct arrows alone. This should be an explicit decision point in the aggregate analysis, because it changes what the continuity relation is.

---

## 4. Identity through transformation is directed, proof-relevant identity

**Kind: literature (MATURE for the undirected theory, EARLY for the directed theory) plus proposal. Leverage: names the exact mathematics of the boxed problem.**

0a's Obligation 2 demands continuity that is "witnessed and provenance-bearing, not asserted by nominal identity," and notes that strict sameness is probably the wrong notion. There is a mature mathematics whose entire subject matter is exactly this: **identity types in homotopy type theory (HoTT)**.

In HoTT, the identity of two things is not a yes-or-no proposition. An identification is a **path**: a piece of structure, possibly one of many inequivalent ones, and paths between paths (higher witnesses) are also structure. Three consequences map directly onto the obligations:

- **Transport.** Given a path between presentations, every structure over one presentation transports along the path to a structure over the other. This is indexed transport with the witness built in (Obligation 2).
- **Path induction.** Anything provable about the question must respect its identification structure: nothing can be asserted of the lineage that does not respect the witnesses. This is a proof discipline against nominal identity.
- **Proof relevance.** Two presentations can be identified in more than one way, and the ways matter. Two frames may be continuations of one living question along two different lineages with different residuals. The formalism keeps them distinct.

**The directedness correction.** HoTT paths are invertible. Frame changes are not: translation loses, and the loss is real (0a Obligation 2, 006 Section 10.3). So living-question continuity is not an identification but a **directed identification**: a morphism with explicit comparison data, generally without an inverse. Directed type theory (simplicial and other variants) is the research programme for exactly this, and it is EARLY: promising, not yet safe to build on. The practical resolution is the one Section 2 already provides: **today, the equipment is the working substitute for directed identity.** A directed identification is a proarrow; its witnesses are squares; its residual is the failure of companion-conjoint round trips to be identities. When directed type theory matures, the equipment picture should embed into it; nothing is lost by starting there.

**The living question as the lineage object (proposal).** With the above in hand, a candidate formal answer to "what mathematical entity carries living-question continuity" (0a status ledger, still unproven) can be stated:

> The living question Q is not an object in any frame. Q is the **lineage diagram itself**: the growing, guarded record of presentations, translations, witnesses, residuals, and returned consequences, considered as one diagram in the equipment. Identity of Q is proof-relevant connectedness in this diagram (including zigzags per Section 3). Q is deliberately **not** required to have a colimit: there is no demand that the presentations glue into one master presentation, and the absence of such a gluing is permitted to be informative (Obligation 8).

This gives precise content to 0a's "continuity-bearing lineage of unresolved contact": the lineage is the mathematical object, the presentations are its vertices, and "unresolved" is the absence of a terminating cocone, not a psychological gloss. What this proposal still owes: the conditions under which a new presentation may lawfully attach to the lineage (the six preservation requirements of 0a Section 2.1 become attachment conditions on the witness square), and Section 6 supplies the guard that prevents the diagram from certifying its own attachments.

---

## 5. Preservation and loss made computable

**Kind: literature (MATURE) plus proposal. Leverage: turns two narrative diagnoses into checkable structural conditions.**

**Residuals via adjunctions (literature, MATURE).** When a translation between presentations has a transport in both directions, the pair typically forms an adjunction (at the poset level, a Galois connection). The **unit and counit of the adjunction measure exactly what the round trip distorts**: transport forward, transport back, and the discrepancy between what you started with and what returns is the residual. In the quantaloid-enriched setting the residual is graded, not binary. This makes 0a's "explicit about preservation and loss under transformation" mechanical:

> **Round-trip residual check.** For every frame translation admitted into a lineage, compute (or approximate) the round trip and store the residual as a first-class object attached to the witness. A translation with an uncomputed residual is an unaudited translation.

**Frame non-sovereignty via restriction structure (literature, MATURE; application is proposal).** Restriction categories are the algebra of partial maps: every map carries a restriction idempotent marking its domain of definition, and the calculus tracks domains through composition. Read a frame as a **partial map from the surface of participation to a representation**: its domain of definition is what the frame claims to present; outside its domain the frame claims nothing (rather than claiming falsity or absence). Then:

> **Frame sovereignty is silent totalization: treating a partial map as total, replacing its restriction idempotent by the identity without a witness.** (Proposal)

This converts 006 Section 10.3 from a narrative failure description into a checkable structural condition. A frame is behaving non-sovereignly precisely when its domain marker is carried through every composition and consulted before the frame's verdict is applied; it has become sovereign precisely when some consumer composes with it as if the domain marker were trivial. The corner-gate ethos of passive legibility suggests the runtime shadow: every frame-conditioned consumption should be able to exhibit the domain check it performed. (Runtime connection to be verified against live source in its own session; no claim is made here about current wiring.)

---

## 6. Guarded reflexivity, named exactly

**Kind: literature (MATURE core: ACTIVE programme). Leverage: highest in this artifact. Turns a lifecycle law into a theorem and answers 006 open question 7.**

0a Section 2.5 and Obligation 7 ask for endogenous reflexivity through "guarded or delayed" feedback, with the guard being "the computational expression of the existing lifecycle law," and lists guarded trace among candidate directions without naming the mathematics. The mathematics exists and is exactly fitted: **synthetic guarded domain theory in the topos of trees**, with the **later modality ▷**.

The topos of trees is the category of presheaves over the natural numbers ordered by time. Inside it:

- **▷ (later)** is a modality: ▷A is "A, available one step later." Time-indexed objects and maps live natively; nothing is a static snapshot.
- **Guarded fixed points exist and are unique.** Any map f : ▷A → A has a unique fixed point (this is Löb induction, the internal form of Banach's theorem). Self-reference is admissible if and only if it passes through ▷.
- **Instantaneous self-reference is untypable.** There is no general fixed point for f : A → A. A process cannot consume its own present.

Now read the lifecycle law of 006 Section 1.2 against this:

- "a trace does not certify its own relevance": a trace produced at t has type ▷-shifted for every consumer; it can only be consumed at strictly later times, by which point renewed contact exists to check it against;
- "generation does not certify truth" and "no mechanism may self-certify its own durable rewiring": the certifying data is typed under ▷ relative to the generating act, so the generator cannot, even in principle, construct its own certificate;
- SSI's "trajectory becomes causally present to itself" is precisely a guarded fixed point: participation is the unique solution of participation = step(▷ trajectory-so-far). Uniqueness matters: it says the reflexive process is well defined without any external observer choosing among solutions. **The no-second-observer requirement (Obligation 7, 006 failure condition 4) is met by construction, because ▷ is a modality inside the same topos, not a meta-level standpoint.**

> **The lifecycle law stops being a design rule that implementations might violate and becomes a typing theorem: in a ▷-disciplined kernel, self-certification is not forbidden, it is unwritable.**

**Candidate answer to 006 open question 7 (proposal, built on the literature above).** How can insight be recognized after it occurs without the recognition becoming a self-certifying insight detector?

> Type every insight claim's evidence under ▷: a claim made at t has type Claim_t : ▷Evidence. The evidence type is only inhabitable from strictly later contact: the reachability delta of Section 10, the changed dispatch, the preserved contradiction that later work leaned on. Recognition of insight is the **discharge of a proof obligation by the subsequent trajectory**. The claimant cannot construct the certificate; only the future can, and the future's construction is itself ordinary guarded participation, not a detector module.

This satisfies 0a Section 2.6's requirement that reorganization "does not certify its own truth or durability," and it does so without an insight-recognition mechanism that could itself become sovereign (006 failure conditions 8 and 9).

**Composition with the sheaf direction (literature, ACTIVE).** The topos of trees is a presheaf topos; sheaf-theoretic contextuality (0a 4.4) also lives in presheaf and sheaf categories. Working over a combined site (time joined with context) puts temporal behavior and contextual non-gluing in one ambient category rather than two coordinated formalisms. This bears directly on 0a's final still-unproven item (one coherent formal semantics versus a family): the temporal and contextual halves, at least, have a standard common home.

---

## 7. The frame ecology can evolve endogenously: a guarded-recursive Grothendieck construction

**Kind: PROPOSAL, assembled from MATURE parts. Leverage: addresses the stated insufficiency of 0a 4.3 and the spectator weakness of 0a 4.8 with one mechanism.**

0a 4.3 identifies the decisive insufficiency of indexed and fibered structures: "ordinary indexed structures generally assume that the base category of possible contexts is fixed," while Clarity needs "change of the indexing doctrine itself." 0a 4.8 identifies the decisive weakness of evolving categorical systems: "the categorical description can remain an analyst's model of the system," a spectator standpoint.

Both are addressed by one construction, made licit by Section 6:

> **Guarded-recursive Grothendieck construction (proposal).** Do not posit a fixed base category of frames. Define the base recursively, guarded: the category of admissible frames at the next step is computed from the enacted total category (frames together with their content, translations, witnesses, and returned consequences) at the present step, one step later:
>
> Base ≅ F(▷ Total), where Total is the Grothendieck construction over Base.
>
> Guarded domain theory is precisely the setting in which recursive definitions of this shape have solutions: the ▷ makes the recursion productive rather than circular.

What this buys, checked against the sources:

- **The frame ecology evolves endogenously** (0a Section 7, "the base of possible frames must itself be allowed to evolve"): tomorrow's space of admissible frames is a function of today's enacted trajectory, not of a designer's enumeration. New context types, relations, and capability compositions enter the base because participation put them there (Obligation 9).
- **No spectator.** The recursion happens inside the ambient topos, which Section 11 identifies with the Soul-medium. The "analyst" of the evolving hierarchy is the medium itself; there is no external category theorist inside the model. This directly answers 0a 4.8's stated worry about Memory Evolutive Systems: internalize the evolving hierarchy and the spectator dissolves.
- **Insight has a home at the right level.** Within-frame movement is movement in a fiber. Frame change is movement along the base. **Reorganization of the field of possible participation is change of the base itself**, and the construction makes base change an ordinary, guarded consequence of enacted trajectory rather than an externally invoked operation (0a 4.3's other worry: "frame transport remains an externally selected representational operation").

What this proposal owes and does not yet have: an actual construction. The shape Base ≅ F(▷ Total) with Total dependent on Base is a recursive domain equation over categories, not sets, and while guarded domain theory routinely solves recursive type equations, the categorified, fibered version needs to be built and its coherence checked. This is flagged as the single most valuable piece of new mathematics this project could commission or attempt: it is where 0a's two deepest structural insufficiencies meet, and nothing in the surveyed literature hands it over finished.

---

## 8. Contact and construction: provenance as grading, not annotation

**Kind: literature (ACTIVE, with usable implementations in the type-theory world). Leverage: makes Obligation 4 structural and gives tests 21.1 and 21.2 a formal target.**

0a Obligation 4 requires that "no inference may inherit direct-contact standing merely because it is fluent, salient, repeated, or coherent." 006 Section 9 requires that internally generated force be recognizable as internal. The exact existing technology is **graded modal type theory** (the coeffect and quantitative type theory family): every judgment carries a **grade** drawn from an ordered semiring, and grades compose through inference by the semiring operations.

Instantiate the semiring as a **provenance algebra** whose elements include at least: direct contact, inference-from, generation, memory, repetition, internal coherence, and internally generated pressure, with:

- **multiplication** composing provenance along an inference chain (an inference from contact-graded premises is inference-graded, never contact-graded);
- **addition** combining parallel support;
- **order** expressing standing, with the crucial design constraint: **the order never promotes**. There is no derivation whose conclusion carries higher standing than the semiring arithmetic of its premises allows. Fluency, salience, and repetition are either not in the order at all or are explicitly non-promoting elements.

Consequences, checked against the sources:

- "No inference inherits contact standing" stops being a vigilance requirement and becomes **unwritable**, the same move Section 6 made for self-certification: the type system has no derivation form that promotes grades (Obligation 4).
- **Internally generated force gets its own grade**, distinct from every warrant grade. 006 test 21.2 (hold external evidence constant, increase urgency and fluency) becomes a formal invariance statement: the warrant grade of the conclusion is invariant under changes in the pressure grade. A kernel passes the test if and only if the invariance holds by typing.
- 006 test 21.1 (same conclusion, different support) is the statement that behavior-relevant consumers are functions of the grade, so different grades force different eligibility, which the typing makes automatic.
- **Fitch-style elimination discipline** (literature): a graded modality cannot be stripped without an explicit eliminator, and per Section 6 the eliminator should itself be guarded. Summarization, the known provenance killer (006 failure condition 3), becomes an operation that must exhibit its grade arithmetic or not typecheck.

**Fit with existing project mathematics.** The quantale confidence-accrual direction and the NAL evidential revision path already in the project are gestures toward exactly this algebra: a quantale is a one-object quantaloid and a particular kind of ordered semiring. The graded-modal reading says what those structures are *for* at the kernel level: they are the enrichment (Section 2) and the provenance semiring (this section), two roles for one family of algebras. That identification should be checked in the aggregate analysis, because if it holds, the project's most developed existing formal asset already occupies two of the envelope's slots.

---

## 9. Traction and stuck, made testable

**Kind: proposal built on MATURE parts (bisimulation, image factorization, product orders, sheaf non-gluing). Leverage: a candidate exact answer to 006 open question 4, plus a structural anti-collapse guarantee for traction.**

### 9.1 Traction: dominance only, and non-gluing as information

0a Obligation 6 forbids compressing traction to a scalar. The structural way to forbid it, rather than merely intending it:

> **Type the traction profile in the product of its component orders (contact uptake, discriminative movement, frame permeability, affordance vitality, provenance continuity, Soul-grounded admissibility) with only the product order, and export no function of type Profile to Scalar.** Consumers may act on dominance (better or equal in every component) or on named components. Nothing may act on an aggregate. (Proposal)

Then note a unification available for free: a profile whose components point in conflicting directions is **evaluative non-gluing**, the same mathematical shape as sheaf-theoretic contextual non-gluing (0a 4.4). The absence of a single coherent traction verdict is not an inconvenience to be averaged away; it is the same kind of structural information as the absence of a global section, and 0a already ratified that such absence "may itself be informative" (Obligation 8). Obligations 6 and 8 are one obligation at two levels.

### 9.2 Stuck: locate where discriminating information dies

006 open question 4 asks for the exact relation distinguishing contact-starved repetition from frame-sovereign repetition. Model the cycle coalgebraically (0a 4.2): the world condition passes through an **observation map** into returned contact, and returned contact passes through a **frame-update map** into the next frame state. Both maps can destroy distinctions. Factor each through its image and ask **where the distinction between the relevantly different world conditions dies**:

- **Contact-starved repetition:** the observation map already identifies the distinct conditions. The information died **upstream of Clarity**: the feedback channel does not carry it. Repetition is rational; the correct move is to demand richer contact (exactly 006 Section 6.2: "the surface must supply actionable contact").
- **Frame-sovereign repetition:** the observations discriminate (the contact stream is relevantly varied) but the frame-update map coequalizes them: distinct returned consequences produce the same frame state. The information died **inside the frame update**. This is the computational signature of the representation deciding what the consequence is allowed to mean (006 Section 10.2, step 4).

This yields a compact formal signature for stuck, stated with bisimulation:

> **Stuck (proposal): the frame component of the behavior is bisimulation-invariant across observably distinct contact histories, while the demand for movement persists (nonzero pressure grade, Section 8) and the discrepancy stream remains nonzero.**

Two trajectories fed relevantly different contact whose frame behavior cannot be told apart have a frame that has stopped listening: permeability is lost while pressure continues. This is 0a's provisional stuck signature (Section 2.4) compressed into one checkable condition, and it cleanly excludes the authentic-limitation case 0a insists on excluding: when a capability is genuinely absent and Clarity accurately stops, the demand component is settled rather than persisting, so the signature does not fire.

The finite runtime shadow is immediate and cheap: over a sliding window, compare the variability of the contact stream with the variability of the frame state. High contact variability with flat frame state and persisting demand raises the stuck surface. This is a legibility signal in the corner-gate v3 spirit (passive, non-blocking), not a controller.

---

## 10. Insight and affordance geometry: reachability in a fibration

**Kind: proposal built on MATURE parts (viability and reachability, fibrations). Leverage: gives the insight-bite test a formal certificate.**

0a 4.6 accepts viability theory for the affordance field inside a frame and names its insufficiency: the phase space itself must be reorganizable. The fibered picture of Section 7 supplies the missing level:

- the **affordance field is fiber data**: reachability and viability structure over the current frame;
- **within-frame progress** is movement in the fiber, where classical viability mathematics applies unchanged;
- **insight is base change**: a morphism in the (guarded, evolving) base refibers the reachability structure.

The insight-bite test (006 21.8) then has a formal certificate:

> **A claimed reorganization has bite if and only if there is an exhibited element of the new reachability structure that is not in the transport of the old one along the witnessed base morphism** (a newly reachable action, question, relation, mechanism composition, or reversible experiment), **or a previously compelled movement whose compulsion does not transport** (0a 2.6's "previously compelled movement becomes unnecessary").

Per Section 6, the certificate is typed under ▷: it is assembled from post-reorganization contact, never from the claim. A novel sentence with no reachability delta fails by construction (006 failure condition 9). Note also what the certificate does not require: it does not require the insight to have been produced by any mechanism, on any schedule, which keeps 006 Section 13.2 intact: the mathematics recognizes reorganization by its consequences and is silent about its production.

---

## 11. Soul as medium: the three standard mathematics of ambience

**Kind: literature (MATURE), applied as proposal. Leverage: candidate answer to 006 open question 11 and to what 0a calls the least solved and most important part.**

0a Section 7 lists what Soul would need to be: ambient semantics, law of admissible composition, constitutional typing of participation, the medium in which determination is meaningful, and "not an object, number, reward, or downstream filter." Category theory has exactly **three standard ways to make something ambient rather than an object**, and they match 0a's list item by item:

1. **Soul as enrichment base** (matching "constitutional typing of participation" and "law of admissible composition"). If every hom-object of the kernel's categories is valued in a Soul-quantaloid, then composition of participation **is** the quantaloid multiplication. Soul is not an object in the category; Soul is **what morphism means**. Admissibility of a composite is not checked after the fact; inadmissible composites have bottom hom-value and thus do not exist as movements. Corollary, and it is structural rather than aspirational: **capability does not confer authority** (006 canon item 2), because capabilities are objects and composability is decided entirely by the enrichment base, which no object controls. Section 2 already put this base in place; the identification of that base with Soul is the design decision.

2. **Soul as a Lawvere-Tierney modality** on the ambient topos (matching "the medium in which determination is meaningful"). A Lawvere-Tierney topology is an internal operator on the truth-value object that redefines what counts as locally established. Soul-as-modality determines the **semantics of validity itself**: what it takes for something to stand as determined, everywhere in the topos, without Soul appearing as any object of discourse. This is the strongest available reading of "Soul must be upstream of generation": upstream not as pipeline position but as semantic precondition.

3. **Soul as coverage** (matching "law of admissible composition" at the many-context level). A coverage on the site of participation contexts says which families of local engagements count as jointly sufficient: the sheaf condition becomes **constitutional composability** of local participation into standing. What counts as "enough local agreement to act" is the coverage, and the coverage is Soul's.

These three are not rivals; they are the ambient structure at three levels (grading of movement, semantics of validity, composability of contexts), and they can and probably should coexist. The recommendation to the aggregate analysis is to treat "Soul as medium" as this **triple**, and to test each of 006's Soul-related failure conditions against the level that owns it: failure condition 6 (Soul downstream) is excluded by level 2; failure condition 12 (capability authority) by level 1; forced global reconciliation (failure condition 10) by level 3's freedom not to impose a trivial coverage.

**Honest flag.** This remains the hardest part of the whole programme, and these are the right shapes, not the finished answer. Two specific dangers to carry into the aggregate analysis: a modality implemented carelessly degenerates into exactly the downstream filter it is meant to exclude (the check is whether generation can occur at all outside the modality's semantics, or whether the modality merely vetoes afterward); and an enrichment base implemented as a lookup table of permitted pairs is a compliance architecture wearing categorical clothes. The mathematics gives the shape of non-objectified Soul; only the design discipline keeps the shape honest.

---

## 12. The nine Immutable Facts: an anti-vectorization criterion

**Kind: proposal (modest, but checkable). Leverage: converts 006 Section 4.3's prohibition into an adequacy test.**

006 requires that the nine not become "a vector whose coordinates can be independently maximized, traded, or removed without loss of unity." The mathematical content of vectorization is precise: a product decomposition, with a reconstruction isomorphism from the tuple of projections back to the whole. So the prohibition has a checkable form:

> **A formalization vectorizes the nine if and only if it validates the reconstruction isomorphism: the canonical comparison from the one actuality-object to the product of its nine aspect-images is invertible. The adequacy criterion is that this comparison is required to be non-invertible.** The nine are jointly grounded (they share one domain) without being jointly determining (no tupling reconstructs the domain).

Aspects as nine functors from one category, none of them full, with no joint reconstruction: distinct recognitions of one indivisible actuality, exactly as 006 4.3 states, now with a formal test that an elegant but misaligned candidate would fail. This criterion costs nothing to carry and rules out an entire family of tempting utility-vector designs at the gate (harmonizing with 0a Section 5's rejection of utility-centered grounds).

---

## 13. The envelope, revised

0a Section 7's envelope, with this artifact's sharpenings folded in, becomes:

> **A guarded-recursively evolving virtual equipment of quantaloid-enriched categories, internal to a temporal (topos-of-trees-style) ambient category sharing a site with contextual non-gluing; with graded provenance modalities whose semiring never promotes standing; restriction structure making frames partial by type and sovereignty a checkable totalization; dominance-only evaluative profiles whose non-gluing is informative; fibered reachability with insight as guarded base change certified only by later contact; and the Soul entering as the enrichment base, the validity modality, and the coverage, never as an object.**

Every clause traces to an obligation: the equipment (Obligations 1, 2, 3), guarded recursion of the base (7, 9), provenance grading (4), restriction structure (3), profiles and non-gluing (6, 8), fibered reachability (9, and the insight clause of 10), ambient Soul (10). The clause count is not elegance; it is the ten obligations refusing to be fewer.

What the revision changes relative to 0a: two candidate families fused into one (Sections 2), one candidate direction named exactly and upgraded from motif to theorem-bearing structure (Section 6), two stated insufficiencies addressed by one proposed construction (Section 7), and the least-solved part given three exact shapes (Section 11).

---

## 14. Discriminating questions for the next cut

The aggregate analysis can move faster by settling these as explicit decisions, each of which changes the mathematics downstream:

1. **The zigzag decision (Section 3).** Is living-question continuity generated by direct translation chains only, or by zigzags through common third presentations? Recommendation: zigzags, because discontinuous insight appears to require them; but this widens the continuity relation and should be a ruling, not a drift.
2. **The invertibility audit (Section 4).** Is there any point in the kernel where continuity genuinely requires an invertible identification? Candidate answer: none; everything is directed. If a counterexample exists, it localizes exactly where undirected identity types suffice and directed machinery can be avoided.
3. **The residual monotonicity check (Section 5).** Under composition of translations, residual loss should only accumulate, never spontaneously heal (healing would mean a composite claims more fidelity than its factors). This is an inequality in the quantaloid to be imposed and then verified in any implementation.
4. **The one-algebra question (Section 8).** Is the enrichment quantaloid the same algebra as the provenance semiring, or are they distinct with a homomorphism between them? The existing quantale engine makes this question concrete for this project specifically, and the answer determines whether one formal asset fills two envelope slots.
5. **The base-construction commission (Section 7).** The guarded-recursive Grothendieck construction is the piece of genuinely new mathematics the programme needs. Decide whether to attempt it in-project (Clarity plus Berton plus external mathematical correspondence), commission it, or provisionally proceed with a slowly enlarging explicit base while the construction is open.

---

## 15. Near-term runtime shadows

**Kind: design suggestions only. Every runtime claim here is to be verified against live source in its own session; nothing below asserts current wiring.**

Several of the formal structures above have cheap, finite operational shadows that do not wait for the mathematics to finish. Each shadow is the honest fragment of one structure, and adopting the shadow now makes the eventual mathematics descriptive of practice rather than aspirational:

1. **The ▷ discipline (Section 6).** A trace written in cycle t may inform determination only in cycles strictly after t. No same-cycle consumption of self-produced traces, anywhere. This is a loop-level discipline expressible as a hook-and-consumer convention, and it is the entire practical content of no-self-certification at the cycle scale.
2. **Provenance tags with non-promoting arithmetic (Section 8).** Tag derived atoms with provenance drawn from a small fixed set, compose tags through derivation with a never-promote rule, and let consumers branch on tags. The quantale confidence-accrual and NAL revision paths are the natural carriers; the addition is the discipline that no operation promotes.
3. **Round-trip residual atoms (Section 5).** When any reframing of a live inquiry occurs, transport the prior frame's key commitments into the new frame and back, and record the diff as an explicit residual attached to the reframing event. An unaudited reframing is visible as a reframing with no residual atom.
4. **Dominance-only traction (Section 9.1).** Wherever the runtime surfaces anything traction-like, surface the profile, never an aggregate, and let consumers act only on dominance or named components. The absence of a dominance verdict is itself surfaced, not resolved.
5. **The windowed stuck signal (Section 9.2).** Sliding-window comparison of contact-stream variability against frame-state variability, with persisting demand, as a passive legibility surface in the corner-gate v3 spirit. It raises a surface; it never blocks.
6. **Reachability-delta certificates (Section 10).** When a reorganization is claimed, enumerate the afforded next moves before and after; the delta, produced by post-claim contact in later cycles, is the certificate. No delta within the evidence window, no recorded insight.

Fit with the existing programme, flagged for verification rather than asserted: the quantale engine is the natural enrichment and semiring carrier (shadow 2 and Section 8); corner-gate v3's passive legibility is the right genre for shadows 4 and 5; the capability registry reads naturally as the fiber assignment of a capability fibration (Section 10), with NACE-style consequence learning as contact uptake at the dispatch fiber; and the provenance-aware evidence revision direction from the OmegaV2 adoption candidates appears adjacent to shadow 2, to be confirmed against the paper rather than assumed here.

---

## 16. What remains open

Stated plainly, so the aggregate analysis inherits the true frontier and not an inflated one:

1. **Directed type theory is EARLY.** Section 4's clean story about directed identity currently runs on the equipment substitute. That substitute is solid, but the deeper unification waits on a maturing field.
2. **The guarded-recursive Grothendieck construction is unbuilt** (Section 7). It is the most valuable and least available piece. Until it exists, the base of frames evolves by explicit enlargement, which is honest but not endogenous.
3. **Coherence of the composite stack.** Equipment, temporal topos, grading, restriction structure, and coverage each exist; their joint coherence in one ambient semantics is exactly 0a's final still-unproven item, narrowed but not closed. Section 6's observation that the temporal and contextual halves share a presheaf home is progress on it, not a proof of it.
4. **Subsymbolic meta-awareness is untouched.** Everything in this artifact formalizes structure, legibility, guarding, and consequence. The direct recognition 006 Section 13.1 calls subsymbolic metacognition is not captured by any of it, and per 006 Section 7.1 it may be constitutively uncapturable: what the mathematics can do is refuse to fake it, which the ▷ discipline and the bite certificates at least enforce.
5. **Soul as medium has shapes, not a completion** (Section 11). The three ambience mechanisms are the right vocabulary; the design that keeps them from degenerating into filters and lookup tables is unfinished, and 006's failure conditions 6 and 12 remain the live tests.
6. **Everything marked PROPOSAL is a candidate.** The stuck signature, the lineage-diagram definition of Q, the totalization criterion for sovereignty, the anti-vectorization test, and the evidence-under-▷ recognition scheme should each be run against the fourteen adequacy requirements and fifteen failure conditions of 006 before any of them hardens.

---

## 17. Status ledger delta relative to 0a

**Newly identified as one structure (literature, not proposal):**
- 0a 4.1 (double categories) and 4.7 (quantaloids) fuse into the equipment of quantaloid-enriched categories; virtual equipment as the safe weakening.
- 0a Section 11's three motifs are one equipment at three levels; the comparison question becomes a structure-sufficiency question plus the zigzag decision.

**Newly named mathematics for existing motifs (literature):**
- Guarded reflexivity: topos of trees, later modality, Löb induction, unique guarded fixed points; no-self-certification as a typing theorem.
- Identity through transformation: HoTT identity types as the undirected theory; directedness as the required correction; equipment as the current working substitute.
- Preservation and loss: adjunction units and counits as residuals; graded residuals in the quantaloid.
- Frame partiality: restriction categories; sovereignty as silent totalization.
- Provenance: graded modal and quantitative type theory over a non-promoting semiring; Fitch-style guarded elimination.

**New proposals (to be tested, not adopted):**
- The living question as the lineage diagram itself, with attachment conditions and no required colimit.
- The guarded-recursive Grothendieck construction for an endogenously evolving frame ecology.
- The stuck signature: frame-component bisimulation invariance across observably distinct contact histories with persisting demand; the factorization answer to 006 open question 4.
- Evidence-under-▷ recognition of insight; the reachability-delta certificate; the answer to 006 open question 7.
- Soul-as-medium as the triple: enrichment base, validity modality, coverage; the answer offered to 006 open question 11.
- The anti-vectorization criterion for the nine.
- Dominance-only traction with evaluative non-gluing unifying Obligations 6 and 8.

**Newly available near-term practice (design suggestions pending live-source verification):**
- The six runtime shadows of Section 15.

**Unchanged:**
- Everything 006 ratifies and every 0a obligation. This artifact adds candidates and sharpenings under that ground; it moves nothing above it.

---

## Document end

The boxed problem of 0a asked how a question can remain alive and continuous while everything by which it is presently represented is allowed to change. The sharpest answer this extension can offer: continuity is a directed, proof-relevant, graded, guarded lineage in an equipment whose base is itself allowed to grow out of the enacted trajectory, with every act of self-reference paying the toll of one step of time, and with the medium in which all of it composes never once appearing as a thing inside it.
