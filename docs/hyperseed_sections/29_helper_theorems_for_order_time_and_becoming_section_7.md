# 29 Helper theorems for order, time, and becoming (Section 7)

how they support minimum-distinction representation and compositional control [3, 2]. From an
engineering perspective, a useful additional test is whether the chosen quantale admits well-behaved
residuals/implications (when present), since these determine how one can pose and solve inverse
questions of the form “how much additional evidence/effort is needed to reach a target threshold?”

What remains underspecified, and how to tighten it
This subsection is best read as a set of explicit “degrees of freedom” that separate the core ontology
from any particular instantiation. The goal is not to postpone precision indefinitely, but to make
clear which precisifications are domain commitments (and therefore revisable) versus which are
constitutive of the framework.

Remark 1544 (Underspecification is not a defect, but it creates obligations). Any broad ontology
that aims to serve both metaphysical and computational ends must initially leave some degrees
of freedom. However, leaving degrees of freedom creates obligations of two kinds: (i) to state
clearly what is fixed (axioms) and what is variable (model class), and (ii) to articulate criteria
by which a variable choice becomes justified in a given application. A useful way to think about
(ii) is that justification can be empirical (predictive performance), computational (tractability and
robustness), or interpretive (faithfulness to the intended metaphysical reading), and in practice a
system design will trade these against one another rather than optimize a single axis. Hyperseed’s
core is deliberately permissive about representational granularity and about which distinctions are
“worth making”; this permissiveness is exactly what weakness is meant to formalize (Hyperseed-
Concept 202 and [3, 2]). In particular, weakness is meant to make it possible to say not merely
that two models differ, but that the cost of maintaining the difference (in attention, memory, proof
burden, or control complexity) may dominate its benefits, thereby providing a principled reason to
coarsen a representation.

Remark 1545 (Examples of places one may want extra axioms). The following are typical points
where a research program must decide whether to add structure:

• Threshold choices and stability. Many definitions use thresholds (for distinctions, focus/fringe,
  etc.). To “tighten” the theory one may specify how thresholds vary across contexts, or impose
  robustness constraints: e.g. require that small perturbations of thresholds do not flip key classi-
  fications too often. One may also require monotonicity constraints (e.g. as resources increase,
  thresholds do not become harder to satisfy) or hysteresis-like constraints (to prevent oscillation
  when evidence hovers near a boundary), depending on whether the intended system is more like
  a classifier or more like a controller.

• Coherence constraints on evidence updating. Paraconsistency permits inconsistency, but
  does not determine how evidence should be updated in time or merged across agents. One may
  impose additional coherence axioms (probabilistic, order-theoretic, or dynamical) when building
  concrete systems, at the cost of narrowing the model class. For instance, one might demand
  commutativity/associativity of certain merge operations (to model order-insensitive aggregation)
  or explicitly reject them (to model path-dependence and learning trajectories), and either choice
  should be treated as a substantive modeling commitment rather than an implementation detail.

• Pattern/evidence interfaces. The ontology of patterns, emergence, and pattern webs is de-
  liberately broad (Hyperseed-Concept 130, ??, 132; see also [5]). A tighter theory might specify
  a privileged family of pattern formalisms (graphical models, programs, logical theories, dynam-
  ical systems) together with translations between them. Such translations may themselves carry

                                                 597
  weakness/effort costs (e.g. compilation blowups, loss of fine structure, or the introduction of ap-
  proximation error), and spelling out these costs is one way to connect the abstract ontology of
  patterns to concrete computational budgets.
These tightenings do not change the spirit of Hyperseed; they determine how the spirit becomes an
engineering discipline. In other words, the point is not to eliminate pluralism, but to ensure that
pluralism is controlled by explicit principles so that different instantiations remain comparable.
Remark 1546 (Dependency structure as a recurring hidden variable). A subtle but pervasive
underspecification concerns dependency: which assertions depend on which representational com-
mitments, resources, or background regularities (Hyperseed-Concept 93, 94). Formal work on de-
pendency towers and tradeoff theorems provides one route to make this explicit [8, 9]. In practice,
making dependency explicit can mean recording not only that a claim holds but under which sup-
ports it was derived (data sources, inference rules, time windows, or modeling assumptions), so
that revisions can be localized when some supports are withdrawn or contradicted. The philosophical
benefit is a more candid separation between what is claimed “in the abstract” and what is claimed
“given the scaffold” (Hyperseed-Concept 51, 83). This also clarifies how paraconsistency interacts
with engineering: if contradiction is confined to a particular scaffold component, then one can de-
grade gracefully by revising or isolating that component rather than treating the entire knowledge
state as unusable.

Computational realizations
Remark 1547 (Knowledge graphs with paraconsistent annotations). A straightforward implemen-
tation path is to treat entities/patterns as nodes in a knowledge graph, and attach to each edge or
assertion a p-bit-like evidence annotation capturing positive and negative support. Concretely, one
can view each annotation as a small record (e.g. (e+ , e− )) whose components are updated inde-
pendently as new sources arrive, so that contradictory sources need not collapse the representation
into triviality. This aligns with the intent of paraconsistent valuation (Hyperseed-Concept 198) and
makes explicit the difference between “absence of evidence” and “evidence of absence.” In practice,
the former corresponds to leaving e+ and/or e− near a designated neutral element, while the lat-
ter corresponds to actively increasing the negative channel; the distinction is especially important
in sparse graphs where missing edges are common. One then implements inference as propagation
and aggregation of these annotations, respecting the chosen quantale operations (Hyperseed-Concept
143). Operationally, propagation specifies how evidence moves along paths (e.g. composing along
relations), while aggregation specifies how multiple paths, witnesses, or sources combine at a node,
and quantale structure provides a principled way to make these combinations associative and order-
respecting. Such an approach is compatible with the broader engineering perspective in [19]. It
also suggests a natural interface to existing KG toolchains: the paraconsistent layer can often be
implemented as an annotation algebra on top of otherwise standard storage, indexing, and query
machinery, with the main novelty living in the update rules and the inference semiring/quantale.
Remark 1548 (Proof assistants and typed internalization). A different realization strategy is to
internalize fragments of Hyperseed in a proof assistant. Here the goal is not merely to compute, but
to ensure that complex chains of reasoning about contexts, translations, and compositional struc-
ture remain checkable. This shifts the emphasis from runtime performance to auditability: proofs
become artifacts that record which context-shifts were permitted and which coherence conditions
were used. Dependently typed settings are particularly apt for expressing context-indexed notions
without losing rigor. For example, one can index claims by explicit context parameters and re-
quire that any “change of context” be witnessed by a term that states the translation/transport

                                                598
map, preventing accidental equivocation between similar-looking but non-identical situations. Work
on program structure and type-theoretic constructions (e.g. McBride-style derivations in type the-
ory) offers inspiration for making “change of context” and “differentiation of structure” first-class
[22]. A practical deliverable along these lines would be a small library of primitives (contexts,
morphisms/translation witnesses, and composition laws) together with a collection of derived rules
encoding common Hyperseed patterns, so that later mechanized arguments can reuse them rather
than re-proving basic bookkeeping lemmas.

Remark 1549 (Agent architectures, cognitive synergy, and transfer). For agent architectures, the
central design question is how to allocate attention and computation among many partial models
and heuristics. In concrete systems, this becomes a scheduling and resource-allocation problem:
which models get run, at what fidelity, for how long, and with what sharing of intermediate re-
sults. Hyperseed’s emphasis on weakness suggests policies that prefer coarse, low-effort represen-
tations until task pressure forces refinement. One can interpret “task pressure” as any signal of
mismatch (loss, surprise, failure rate, or utility gradient) that justifies paying the cost of a more
discriminating model, and interpret “refinement” as moving along a ladder of increasingly struc-
tured representations rather than committing to maximal structure from the start. This rhymes
with the cognitive-synergy engineering stance in [19] and with transfer-learning frameworks aiming
to reuse structure across tasks (Hyperseed-Concept 192, 193; see [7]). From an implementation
viewpoint, transfer then becomes the disciplined reapplication of previously validated partial mor-
phisms: components that were weak-but-useful in one context are tested as candidate scaffolding in
a new one, with explicit bookkeeping of where the fit succeeds and fails. In multi-agent settings, one
also needs a theory of when cooperation improves group-level effectiveness; the pro-social efficiency
argument in [6] provides one candidate mathematical lens (touching Hyperseed-Concept 170, 81).
Here, “improves” should be read operationally: cooperation must pay for its coordination costs, and
thus the relevant predictions concern regimes where communication bandwidth, trust calibration,
and division of labor create net gains in collective inference or exploration.

Remark 1550 (Complexity and information measures as operational proxies for weakness). When
implementing weakness, one often needs computable proxies. In particular, many theoretical notions
of “minimal structure” or “least commitment” are defined abstractly, whereas engineering requires
scalars or efficiently estimated quantities that can guide search, compression, or model selection.
Algorithmic information theory (Kolmogorov complexity) provides one principled family of proxies
(Hyperseed-Concept ??; [16]). Even when true Kolmogorov complexity is uncomputable, practical
approximations (compression-based scores, MDL-style criteria, or restricted model classes) can still
serve as consistent heuristics for preferring weaker descriptions that nonetheless fit the data. Logical
entropy offers an alternative, partition-centric lens that can be more natural when the primitive
notion is “distinction” rather than “code length” (Hyperseed-Concept 105; [17]). This viewpoint
is often convenient in settings where the agent’s first act is to carve the world into equivalence
classes (what is treated as the “same”) and only later to assign probabilistic weights or codes within
each class. These measures do not replace the ontology; they offer handles by which the ontology
can be made computationally testable. They also provide a bridge to empirical evaluation: by
tying weakness to measurable surrogates, one can compare alternative implementations by checking
whether the proxies track improved generalization, transfer, or robustness under perturbations of
context.




                                                  599
Open problems and potential empirical tests
Remark 1551 (Morphic resonance: what it would mean to test a speculative coupling). Morphic
resonance (Hyperseed-Concept 115) is the most empirically charged and controversial notion named
in the outline. Sheldrake’s proposal [13] is not used here as a settled fact, but as an invitation to state
clearly what sort of empirical signature Hyperseed would treat as evidence for a nonlocal, pattern-
mediated coupling. That is, the role of the concept is methodological: it forces the framework to spell
out what would count as a residual effect after ordinary causal pathways have been accounted for,
rather than leaving the notion vague or purely rhetorical. In Hyperseed terms, a “morphic” effect
would look like a reproducible improvement in prediction, learning speed, or pattern stabilization that
cannot be accounted for by the explicit causal and informational channels included in the modeled
context. A useful sharpening is to demand not merely statistical significance, but robustness across
modest changes of experimental realization: if the effect depends delicately on uncontrolled details,
it is more plausibly an unmodeled ordinary channel than a genuine context-transcending coupling.
The practical challenge is to design experiments where such a residual cannot be too easily explained
away by hidden ordinary channels, while also not demanding an unrealistic level of isolation. In
other words, the experiments must balance two failure modes: being so open that mundane leakage
dominates, and being so closed that the study becomes infeasible or so artificial that external validity
is lost.

Remark 1552 (Paraconsistent experimental methodology). If one expects borderline effects (small,
context-sensitive, partially inconsistent), a classical binary hypothesis-testing posture may be epis-
temically mismatched. In such regimes, it is common for replications to produce mixed outcomes,
and the key scientific question often becomes whether the pattern of success/failure aligns with spe-
cific contextual moderators rather than whether a single global null can be rejected. A paraconsistent
stance instead records both supporting and disconfirming evidence channels and asks how stable the
net pattern is under changes of context and analysis pipeline. Operationally, this means tracking
which preprocessing choices, inclusion criteria, modeling assumptions, and instrumentation changes
strengthen or weaken the effect, and representing the result as an evidence profile rather than a sin-
gle scalar verdict. This is a natural extension of the social-computational-probabilistic philosophy
of science view in [20], where science is treated as a dynamical process of community-level belief
revision rather than a one-shot adjudication. The methodological implication is that publishing “neg-
ative” and “positive” channels together is not a concession but a requirement, because downstream
reasoning needs access to the full inconsistency structure in order to update responsibly.

Remark 1553 (Stability of self-modifying goals as an additional testbed). Another empirical-
leaning direction is to test formal predictions about stability of goal systems in self-modifying agents
(Hyperseed-Concept 110). Here “stability” can be understood in several related senses (e.g. invari-
ance of a goal under allowed self-modifications, bounded drift under noise, or convergence to an
attractor set of policies), and different formalisms may target different senses. Fixed-point methods
applied to goal dynamics provide one route to generate concrete mathematical criteria for stabil-
ity/instability that can be simulated and, in limited domains, experimentally checked [10]. One
advantage of this testbed is that it permits closed-loop experiments: the agent’s own updates change
the object being studied, so one can measure not only performance but also the geometry of goal
evolution under explicit intervention. This connects back to the theme that “realness” and “reality-
systems” are stabilized predictive structures, now applied to the internal economy of goals rather
than external perception. In this light, a goal system counts as “real” for the agent insofar as it
persists as a coherent predictive constraint through the agent’s own attempts to optimize, compress,
or re-express it.

                                                   600
Remark 1554 (Resource-rich minds and shifts in cognitive regime). Some open questions become
visible only when the agent’s resources become large. For example: if a mind can afford extensive
simulation, model search, or self-replication, then its “natural” weakness profile and attention-
allocation strategies may qualitatively change (Hyperseed-Concept 162; [11]). One way to read this
is as a warning against extrapolating human-default priors: scarcity shapes which approximations
feel “natural,” and abundance may make previously unaffordable forms of meta-reasoning (e.g.
maintaining many candidate contexts in parallel) the dominant strategy. This matters because the
ontology aims to be scale-robust: it should describe not only humans and current machines, but
also potential successors. Accordingly, a next step is to identify which claims are invariant under
resource scaling (true structural constraints) versus which are artifacts of a particular computational
regime, so that future empirical work can separate principled predictions from contingent ones.
Remark 1555 (Philosophical anchoring: Peirce and Whitehead as interpretive constraints). Fi-
nally, it is worth noting that Hyperseed’s stance is not only technical but metaphysical: it treats
process, mediation, and relational structure as primary. Peirce’s categories of Firstness, Second-
ness, and Thirdness [14] offer an interpretive schema for understanding why the formalism insists
on both raw qualitative givenness (First), brute interaction and resistance (Second), and lawful
mediation/pattern (Third) (Hyperseed-Concept ??, 163, 190). In this reading, the point is not to
“reduce” the mathematical objects to Peircean terms, but to treat the triad as a constraint on what
a satisfactory account must be able to represent without smuggling in extra assumptions: a place
for immediacy as such, a place for constraint as such, and a place for the mediating structures
that render sequences of constraints intelligible as patterns. This is also a way of articulating why
purely extensional descriptions (e.g., sets of outcomes) are often inadequate on their own: they
may list what happened, yet fail to encode the modalities of how it was encountered (First), what
resisted (Second), and what stabilized as a rule-like linkage (Third). Whitehead’s process ontology
[15] likewise provides a philosophical context in which “entities” are stabilized occasions and rela-
tions rather than timeless substances (Hyperseed-Concept 124, 140). On that view, persistence is
something achieved—a repeated compatibility of successive occasions—and the formalism’s empha-
sis on relational consistency conditions can be read as a technical analogue of that achievement,
rather than as an a priori commitment to fixed, globally valid objecthood. It also clarifies a limita-
tion: if one imports substance-style intuitions (fixed identity across all contexts), one may misread
observer-relative or paraconsistent constructions as defects rather than as deliberate representations
of partial stabilization in the presence of incompatible constraints. These references do not prove
the mathematics; they help one see what the mathematics is trying to be faithful to. They also
function as a guardrail against overinterpreting convenience: when a representation is chosen for
tractability, the philosophical anchoring prompts the question of which aspects of process and media-
tion have been idealized away, and whether that idealization is appropriate for the intended domain
of application.
Remark 1556 (A note on euryphysics and cosmological ambition). The earlier sections that extend
toward cosmos/multiverse/eurycosm aim at a general formal vocabulary for talking about “the wider
world” beyond any one stabilized observer-bound reality (Hyperseed-Concept ??, 89; see [18]). One
motivation for introducing such vocabulary is pragmatic: without a disciplined way to talk about
“external” structure, it is easy to oscillate between naive realism (treating one observer’s stabilized
world as the world simpliciter) and instrumentalism (treating all structure as mere bookkeeping with
no cross-context constraint). The caution is that cosmological reach can outrun empirical grip. In
particular, once the formalism is used to compare or relate multiple observer-relative stabilizations,
it becomes tempting to read purely formal degrees of freedom as ontological commitments; resisting
that temptation requires an explicit account of what would count as evidence for, or constraint on,

                                                 601
those degrees of freedom. The opportunity is that a paraconsistent, observer-relative formalism can
at least let us state the limits of our grip precisely, rather than masking them as false certainty. This
“precision about limits” is itself a methodological next step: to classify which claims are invariant
across observer-stabilizations, which are only locally stable, and which are artifacts of representa-
tional choices, thereby turning philosophical caution into concrete criteria for model comparison. A
further limitation, closely related, is communicability: the more general the euryphysical language
becomes, the more work is required to show how it reduces to familiar empirical practices in special
cases (e.g., when observers agree, when inconsistencies are negligible, or when a classical limit is
appropriate). Conversely, a near-term opportunity is to develop explicit translation principles that
connect eurycosmic statements to testable predictions in restricted regimes, making cosmological
ambition continuous with ordinary scientific inference rather than a separate, unconstrained layer
of speculation.


Part II
Helper theorems for reasoning about
Hyperseed concepts
28     Helper theorems for phenomenological primitives (Section 6)
Standing assumptions and notation. Fix a context c = (Xc , Πc , δc , ιc ) and a (commutative)
p-bit quantale V with componentwise order ≤ and monotone commutative product ⊗. Write
v = (v + , v − ) ∈ V for positive/negative evidence channels. Fix thresholds τδ , τι , τI ∈ (0, 1). Recall:

              Diff c (x → y) := δc (x, y),    Distc (x, y) := Diff c (x → y) ⊗ Diff c (y → x),

and the crisp distinction x #c y means Distc (x, y)+ ≥ τδ . Repetition/variety/non-duality/non-dual-
variety are the threshold predicates of Defs. 42–43. Intensity is Ic : Xc → [0, 1], with Focusc (τI )
and Fringec (τI ) as in Def. 49. An abstraction is a surjection q : Xc  A with preorder q1  q2 iff
∃r : A1 → A2 such that q2 = r ◦ q1 (Def. 51). A context translation is a function T : Xc → Xd , and
T is non-dually compatible if it does not erase strong δ-distinctions (Def. 53).
    It is useful to keep in mind the qualitative role of the three thresholds. The parameter τδ governs
when directed evidential differences “count” as a stable, symmetric separation at the level of Distc ; it
is the place where the evidence-valued notion is intentionally collapsed to a crisp predicate x #c y
only for the purpose of stating combinatorial claims. Similarly, τι controls when the ιc -based
predicates (Defs. 42–43) transition from graded evidence to crisp repetition/variety conditions,
while τI is the intensity cutoff that turns the scalar field Ic into the two regions Focusc (τI ) and
Fringec (τI ). In later lemmas, monotonicity properties typically show that if a statement holds at
some threshold, then it continues to hold at weaker thresholds (e.g. lowering τδ makes x #c y
easier to satisfy), whereas strengthening a threshold expresses a more demanding notion of “strong
evidence”.
    Also note that Distc is built to enforce a “two-way” requirement: even when δc is highly directed,
Distc (x, y) aggregates the evidence for x differing from y together with the evidence for y differing
from x. Thus Distc should be read as a symmetry-enforcing composite, while Diff c is the primitive
directed quantity. The helper results in this section repeatedly exploit exactly this separation:
asymmetry is allowed at the Diff level, but many of the later predicates are deliberately phrased
using Dist in order to avoid baking in any a priori directionality.

                                                   602
Remark 1557. This subsection of helper theorems is a kind of “elementary geometry” for the
phenomenological primitives: it records the algebraic consequences of how Difference (Hyperseed-
Concept 96), Distinction (Hyperseed-Concept 98), Repetition (Hyperseed-Concept 155), Variety
(Hyperseed-Concept 199), Non-Duality (Hyperseed-Concept 121), and Non-Dual Variety (Hyperseed-
Concept 120) were defined earlier. The guiding idea is that these are not treated as crisp, classical
predicates from the outset; rather, they are built from evidence-bearing quantities taking values in
a p-bit quantale, i.e. a two-channel structure that can simultaneously support evidence for and ev-
idence against the same claim. This is one clean way to keep faith with paraconsistent intuitions
without abandoning formal discipline (see, e.g., constructive/paraconsistent semantics as discussed
in [23] and the resonance-motivated uses in [24]; for the broader Hyperseed framing see [1]).

    A practical consequence of this “two-channel” setup is that later statements can be formu-
lated so that they only depend on the +-channel (as with x #c y), or depend on both channels
when non-duality is at stake. In particular, one should not read the presence of a large v − com-
ponent as a contradiction in the classical sense; rather, it represents structured counterevidence
that is retained rather than forced into a binary truth value. This is why many helper lemmas
are phrased as monotonicity or preservation results: they guarantee that the constructions used
to define phenomenological predicates do not behave erratically when evidence is strengthened in
either channel.

Remark 1558. A few notational conventions are worth making explicit the first time they are used
in this helper section.

• The arrow in Diff c (x → y) is not a function type; it is a suggestive way of marking that δc is
  generally directed: δc (x, y) need not equal δc (y, x).

• An element v ∈ V is written as v = (v + , v − ), where v + and v − are the positive and negative
  evidence coordinates. When we write inequalities like Distc (x, y)+ ≥ τδ , we mean: take the
  +-component of the p-bit value and compare it to the scalar threshold.

• “Componentwise order” means: (a+ , a− ) ≤ (b+ , b− ) iff a+ ≤ b+ and a− ≤ b− (in the underlying
  order on each component). This matters because it guarantees that threshold comparisons behave
  monotonically under ≤.

• “Monotone commutative product” means: u ≤ u0 and v ≤ v 0 implies u ⊗ v ≤ u0 ⊗ v 0 , and also
  u ⊗ v = v ⊗ u. The commutativity will be the only property used in Lemma 6; monotonicity will
  be the key engine in Lemma 18.

For a concrete mental model, one may keep in mind the canonical example V = [0, 1]2 with compo-
nentwise order and a componentwise multiplicative ⊗, though the lemmas below intentionally avoid
committing to that special case.

    Two further interpretive points will help when reading the proofs that follow. First, in the
canonical picture V = [0, 1]2 , the multiplication-like behavior of ⊗ makes Distc (x, y) act like an
“AND”-style aggregator: both directions x → y and y → x must carry substantial positive evidence
in order for Distc (x, y)+ to be large. This is why the crisp predicate x #c y is naturally phrased
in terms of Distc rather than Diff c : it encodes the idea that a distinction is not merely a one-way
detectability but a mutual separation.
    Second, the preorder on abstractions (Def. 51) is best read as “q2 is at least as coarse as q1 ”.
Indeed, if q2 = r ◦ q1 , then any two points identified by q1 are necessarily identified by q2 after
applying r, so q2 forgets at least as much as q1 . Several helper lemmas later on implicitly use this

                                                603
coarsening intuition when relating repetition/variety properties across different quotients of the
same underlying Xc .
    Finally, the notion of non-dual compatibility for translations (Def. 53) can be viewed as a min-
imal invariance requirement: a translation T is allowed to change intensities, reorder elements, or
even merge weakly distinguished items, but it should not collapse pairs that were already separated
by strong positive evidence at the δ-level. In that sense, Lemma 18 will function as a “functori-
ality” statement for the geometry induced by δc , ensuring that the basic combinatorics of strong
distinctions survive passage between contexts whenever T is intended to respect phenomenological
structure.

28.1    Difference, distinction, repetition, variety, and non-duality
Remark 1559. These first lemmas are “sanity checks” in the best sense: they verify that the formal
primitives behave as their names suggest. The theme is that while δc is directed (so difference can be
asymmetric), the derived quantity Distc is engineered to be symmetric by combining both directions.
This separation mirrors a philosophical caution: one may experience x as differing-from y in a way
that is not reciprocated, yet the mutual relation of distinction ought to reflect a bilateral comparison.
In the background, the thresholds (e.g. τδ and τι ) serve as explicit “decision levels” that turn graded,
possibly multi-channel evidence into crisp assertions; the lemmas below confirm that these decision
levels interact with the primitives in the intended minimal ways.
Lemma 6 (Symmetry of mutual distinction). For all x, y ∈ Xc , Distc (x, y) = Distc (y, x). Hence
the induced crisp relation #c is symmetric.
Remark 1560. Intuitively, the lemma says: even if “x points away from y” differs in strength
from “y points away from x,” once we define mutual distinction by multiplying the two directed
evidences, the order of the two factors no longer matters. This is important because #c is used
as a crisp proxy for “the context actually makes a distinction here”: crisp distinctions should not
depend on which element is named first. A related point is that this symmetry is achieved without
requiring δc itself to be symmetric; instead, it is the construction of Distc that enforces reciprocity
at the level where later relational predicates will operate.
Sketch. By definition, Distc (x, y) = δc (x, y)⊗δc (y, x). Since ⊗ is commutative, this equals δc (y, x)⊗
δc (x, y) = Distc (y, x). For crisp symmetry: Distc (x, y)+ = Distc (y, x)+ , so Distc (x, y)+ ≥ τδ iff
Distc (y, x)+ ≥ τδ .

Remark 1561. Proof sketch and intuition. The strategy is to unfold the definition of Distc and use
only one algebraic axiom: commutativity of ⊗. Geometrically (in the heuristic [0, 1]2 picture), one
can imagine δc (x, y) and δc (y, x) as two “directed arrows” with lengths in each evidence channel;
taking ⊗ is a way of insisting that mutual distinction is strong only when both arrows support
it. Swapping the endpoints swaps the arrows, but the combined strength stays the same. From the
standpoint of later constructions, this is also what makes #c a well-behaved undirected edge relation
on Xc : it can be used to define graphs, neighborhoods, and partitions without having to keep track
of an orientation that would otherwise be arbitrary at the level of crisp distinguishability.
Lemma 7 (Repetition/variety imply a made distinction). For all x 6= y:

                         Repc (x, y) → x #c y,          Varc (x, y) → x #c y.

Remark 1562. This lemma expresses a design constraint baked into the definitions: repetition
and variety are only meaningful when there is at least some robust distinction being made between

                                                  604
x and y in the first place. Said differently: the ontology does not allow “repetition” to collapse
into mere identity, nor “variety” into unstructured difference; both are modes of relation under
distinction. This will matter later when non-duality is allowed to create simultaneous support for
seemingly opposing relational predicates. One can also read the condition x 6= y as a guardrail
against trivial self-comparisons: even if a formal system could assign nonzero directed difference
to (x, x) in degenerate cases, the intended phenomenological reading treats repetition/variety as
relations between two items presented as distinct positions in experience.

Sketch. Both Repc (x, y) and Varc (x, y) include the conjunct Distc (x, y)+ ≥ τδ by definition; that
conjunct is exactly x#c y.

Remark 1563. Proof sketch and intuition. The proof is purely definitional: it observes that #c is
literally a named subcondition of Repc and Varc . The conceptual picture is that repetition/variety
are “decorations” on top of a basal fact of distinguishability: without the basal fact, the decoration
is not even syntactically permitted. This definitional dependence is intentional: it ensures that
later arguments can freely use x#c y whenever either Repc (x, y) or Varc (x, y) is assumed, without
separately re-checking a distinction threshold.

Lemma 8 (Non-dual variety yields simultaneous repetition and variety under distinction). If x 6= y
and NDVarc (x, y) and Distc (x, y)+ ≥ τδ , then Repc (x, y) and Varc (x, y) both hold.

Remark 1564. This lemma makes precise a subtle but central phenomenological possibility: a pair
(x, y) can be unmistakably distinguished and yet also carry strong evidence for both “repetition” and
“variety.” In ordinary classical logic, one is tempted to treat these as mutually exclusive labels; the
present framework refuses that temptation by allowing a controlled, thresholded form of co-presence.
One may read NDVarc (x, y) as asserting that the indistinction signal ιc (x, y) is bi-valent: it is
simultaneously high in the positive and negative evidence channels, and therefore can support both
readings when combined with a baseline distinction. In particular, the lemma emphasizes that non-
dual variety does not erase distinction: the hypothesis explicitly retains Distc (x, y)+ ≥ τδ , so the
“both at once” reading is not a collapse into undifferentiated identity, but rather an instance of
jointly sustained, potentially tension-bearing relational structure.

Sketch. NDVarc (x, y) means ιc (x, y)+ ≥ τι and ιc (x, y)− ≥ τι . Together with Distc (x, y)+ ≥ τδ ,
these are exactly the defining conjuncts of both Repc (x, y) (uses ι+ ) and Varc (x, y) (uses ι− ).

Remark 1565. Proof sketch and intuition. Again the proof proceeds by unpacking conjunctive
definitions. The key step is noticing that Repc and Varc differ only in which channel of ιc they
consult. Thus, when NDVarc asserts that both channels are above threshold, it automatically sup-
plies the missing half needed for each predicate. A useful mental image is a two-axis meter for ι:
the point lies in the “upper-right quadrant,” so both one-sided tests pass. One may also view this
as a formal version of a familiar experiential report: two moments can be clearly told apart (high
Dist+                                                                      +
     c ) while still being “the same again” in one respect (captured by ι crossing threshold) and
                                                          −
“genuinely different” in another respect (captured by ι crossing threshold), with the framework
explicitly allowing these to be simultaneously licensed rather than forcing a premature choice.

Lemma 9 (Consistency condition makes repetition and variety disjoint). Assume x 6= y and
¬NDVarc (x, y). Then ¬(Repc (x, y) ∧ Varc (x, y)).

Remark 1566. This lemma articulates the complementary regime to Lemma 8: if non-dual variety
is not present, then the framework behaves more like a classical either/or with respect to the pair
of predicates Repc and Varc . Formally, ¬NDVarc (x, y) means that it is not the case that both

                                                 605
evidence channels of ιc (x, y) simultaneously clear the threshold τι . Consequently, one cannot meet
the definitional requirements for repetition (which needs ιc (x, y)+ ≥ τι ) and for variety (which needs
ιc (x, y)− ≥ τι ) at the same time. The role of x 6= y is again to keep the statement aligned with the
intended domain of application of these predicates.

Sketch. Assume for contradiction that Repc (x, y)∧Varc (x, y) holds. Unpacking definitions, Repc (x, y)
supplies ιc (x, y)+ ≥ τι (and the shared distinction conjunct), while Varc (x, y) supplies ιc (x, y)− ≥ τι
(and the shared distinction conjunct). Therefore both ιc (x, y)+ ≥ τι and ιc (x, y)− ≥ τι hold, i.e.
NDVarc (x, y) holds, contradicting the assumption ¬NDVarc (x, y). Hence ¬(Repc (x, y)∧Varc (x, y)).


Remark 1567. Proof sketch and intuition. The argument is a straightforward contrapositive-style
use of the definitions: if both repetition and variety were simultaneously true, then the positive
and negative channels of ιc would both have to be above threshold, which is precisely what NDVarc
asserts. Thus ¬NDVarc functions as a consistency constraint preventing the co-presence of the
two predicates. Conceptually, the lemma clarifies that non-duality is not an automatic background
feature of the system; rather, it is an explicit, checkable condition. When it fails, the framework
reverts to a more exclusive reading in which the same pair cannot be certified as both “repetition”
and “variety” at once.

Remark 1568. Where Lemma 8 shows how coexistence is possible, the present lemma shows how
coexistence is controlled. If NDVarc (x, y) fails, then at least one of the two evidence channels of
ιc (x, y) is not strong enough, and therefore the theory prevents both Repc and Varc from holding
simultaneously. In this way, the system distinguishes (i) genuine non-dual superposition (both
channels strong) from (ii) ordinary situations where one channel dominates. In particular, the
control mechanism is not a separate axiom but is enforced by the same thresholding convention used
throughout: “coexistence” is permitted only when each requisite inequality clears the stipulated bar
(here τι ), so a single weak channel is sufficient to block the simultaneous attribution. This provides
an operational reading of “dominance”: it is precisely the regime in which only one of ιc (x, y)+
and ιc (x, y)− is above threshold, so the model records an asymmetric evidential profile rather than
a balanced one.

Sketch. If Repc (x, y) ∧ Varc (x, y) held, then by definitions we would have ιc (x, y)+ ≥ τι and
ιc (x, y)− ≥ τι , which is exactly NDVarc (x, y), contradicting the assumption. Equivalently, one
can view the argument as unpacking the conjunctive structure of the predicates: the conjunction
Repc (x, y) ∧ Varc (x, y) forces both of the requisite lower bounds on the two coordinates of ιc (x, y),
and that joint lower-boundedness is precisely the definitional content of NDVarc (x, y).

Remark 1569. Proof sketch and intuition. This is a standard contrapositive pattern: assume
both predicates hold and derive the defining condition for NDVarc . Conceptually, it says that the
only route to “both repetition and variety” is the explicitly named non-dual-variety regime. Thus
paraconsistency is not an ambient fog; it is localized and testable via thresholds. A further conceptual
payoff is that the lemma makes the interaction between predicates diagnostically reversible: if an
application ever yields credible evidence for both Repc and Varc , then the framework commits you
to the stronger claim that both evidence channels of ιc are simultaneously high, rather than allowing
an unprincipled mixture of partial conditions. This is exactly the sense in which the coexistence is
“controlled”: the model does not merely tolerate tension, it specifies the unique evidential pattern
under which tension is licensed.



                                                  606
Lemma 10 (Non-duality entails paraconsistent distinctness, but does not force equality). If
NonDualc (x, y) then Distc (x, y)+ ≥ τδ and Distc (x, y)− ≥ τδ simultaneously (hence x#c y), i.e.
the system carries strong evidence for and against the distinction. Moreover, the conclusion is
explicitly two-sided: it asserts the co-presence of high positive and high negative evidence about the
same distinction claim, not an averaged or reconciled value. In particular, the lemma is compatible
with x and y remaining syntactically separate items in the language and, semantically, with later
updates that may lower one channel without forcing any retroactive identification.

Remark 1570. This lemma states, in a deliberately careful way, what non-duality is not. It is not
the collapse of two items into literal identity; it is the simultaneous presence of strong evidence on
both sides of a distinction. In paraconsistent terms, the distinction is both supported and opposed
at the evidence level; classical explosion is avoided because we do not equate “evidence for x =
y” with the syntactic rewrite rule “replace x by y” (compare the motivations for paraconsistent
semantics in [23] and the resonance-oriented perspective in [24]). Stated differently, the framework
treats “distinctness” as a graded, two-channel report rather than as a classical bivalent predicate:
Distc (x, y)+ and Distc (x, y)− are tracked independently, and non-duality corresponds to both being
large enough to pass τδ . The notation x#c y is therefore best read as “paraconsistently distinguished
in context c” rather than as a commitment to either x 6= y or x = y in the classical sense, and the
lemma highlights that this is a stable middle position rather than a temporary inconsistency to be
immediately resolved.

Sketch. Immediate from the defining conjuncts of NonDualc (x, y). The extra point for implemen-
tation is that this is evidence-level paraconsistency, not syntactic equality: one should not rewrite
x = y from NonDualc (x, y). Concretely, if NonDualc (x, y) is defined by the conjunction of the
two threshold conditions on Distc (x, y)+ and Distc (x, y)− (possibly together with auxiliary side
conditions such as x 6= y), then the conclusion follows by direct projection onto those conjuncts,
without any additional inference principles.

Remark 1571. Proof sketch and intuition. Formally, nothing more is happening than reading
off the conjuncts in the definition of NonDualc . The interpretive force lies in the last sentence:
the algebra remembers two channels of evidence, so it can represent the felt “both/and” without
collapsing the computational universe by identification. A helpful visual is to imagine two dials,
one for Dist+ and one for Dist− ; non-duality means both dials are high, not that the two entities
have been merged. One can also read the lemma as a guardrail on downstream reasoning: any
subsequent rule that requires a univocal distinction should check for a one-sided condition (e.g.
only Dist+ being high, or only Dist− being low), whereas rules that are explicitly designed for non-
dual regimes may safely assume the simultaneous high-high configuration. In this way the lemma
clarifies which inferences are legitimate in a non-dual context and why the framework refrains from
identifying items even when the phenomenology suggests a strong “togetherness”.

Lemma 11 (Threshold monotonicity of the primitive predicates). Let τδ0 ≤ τδ and τι0 ≤ τι . Then
for all x 6= y,
                                                     (τ 0 ,τ 0 )
                          Rep(τc
                                 δ ,τι )
                                         (x, y) → Repc δ ι (x, y),
and similarly for Varc , NonDualc , NDVarc . In other words, the parameterization by thresholds is
monotone in the expected direction: weakening the acceptance criteria (by lowering thresholds) can
only expand, never shrink, the extension of each predicate. The restriction x 6= y ensures that
the claim is about the intended “two-item” use of these predicates, and prevents any degenerate
boundary case for which the predicates might have special conventions when x = y.


                                                 607
Remark 1572. This lemma confirms that thresholds behave the way one expects: lowering the bar
cannot invalidate a previously valid claim. It is not deep, but it is structurally important because it
lets one compare contexts or agents that choose different strictness levels. In particular, any later
theorem that is proved at stringent thresholds automatically holds (in the same direction) for more
permissive thresholds, which is often the right notion of robustness for phenomenological predicates.
A common use is “calibration transfer”: if one analyst uses conservative settings (τδ , τι ) and another
uses more permissive settings (τδ0 , τι0 ), then any instance certified by the conservative analyst is
automatically certified by the permissive one. The lemma thus supports principled comparisons
across experimental regimes, interpretive stances, or modeling choices without requiring any further
assumptions about the underlying evidence values beyond their order structure.

Sketch. All four predicates are conjunctions of lower bounds of the form u ≥ τ . If a value exceeds
                                                                                         (τ ,τ )
a larger threshold, it exceeds any smaller threshold. More explicitly, suppose Repc δ ι (x, y) holds.
Unpacking its definition yields a finite list of inequalities, each of which compares some evidence
coordinate (e.g. a component of Distc or ιc ) to either τδ or τι . Replacing τδ by the smaller τδ0 and τι by
                                                                                               (τ 0 ,τ 0 )
the smaller τι0 preserves truth of each inequality, hence of their conjunction, giving Repc δ ι (x, y).
The other predicates follow identically.

Remark 1573. Proof sketch and intuition. The argument uses only the transitivity of ≥ on [0, 1]
(or whatever ordered set the components live in). The key step is recognizing that each predicate is
assembled from statements of the form “some evidence coordinate is at least a threshold,” so mono-
tonicity in thresholds is inherited componentwise. It is worth noting that no continuity, additivity,
or probabilistic interpretation is required: the lemma is purely order-theoretic. Consequently, it re-
mains valid under many possible implementations of evidence coordinates (e.g. scores, normalized
measures, or bounded utilities), provided only that the comparison relation is a partial or total order
with the usual transitivity property.

28.2    Presentational immediacy: focus and fringe
Remark 1574. We now move from relational predicates to an internal scalar field Ic : Xc → [0, 1]
encoding intensity in a context. The induced sets Focusc (τI ) and Fringec (τI ) formalize a simple
attentional phenomenology: some items are in the bright center of awareness, others are faintly
present at the periphery. This connects directly to Presentational Immediacy (Hyperseed-Concept
138) and Attention / Attentional Focus (Hyperseed-Concept 60).

Remark 1575. The only structure assumed here is that each context c comes with a carrier set Xc
and a numerical intensity assignment Ic . In particular, no topology, metric, similarity relation, or
ordering on Xc is required in order to state (and later reuse) the basic focus/fringe facts. All com-
parisons are pushed into the codomain [0, 1], so the subsequent lemmas are essentially consequences
of elementary order properties of real numbers.

Remark 1576. The threshold parameter τI should be read as a convention for discretizing a graded
phenomenon. Different choices of τI correspond to different attentional “grain sizes”: low thresholds
treat many items as focused, while high thresholds reserve focus for only the most intense items.
This explicit dependence on τI is useful later when one wants to model shifts of attention without
changing the underlying intensity field Ic itself.

Lemma 12 (Focus/fringe are disjoint). Focusc (τI ) ∩ Fringec (τI ) = ∅.



                                                    608
Remark 1577. The lemma says there is no ambiguous “half-in, half-out” element: at a fixed
threshold τI , an item cannot be both above threshold (focus) and strictly below it while still posi-
tive (fringe). This is important because later constructions may treat focus and fringe as distinct
computational roles (e.g. a focus-like set receiving expensive processing while the fringe is handled
heuristically).
Remark 1578. Note also that the disjointness hinges on the asymmetric boundary convention:
focus is defined using ≥ τI while fringe uses < τI (together with > 0). Thus an item with Ic (x) = τI
is classified as focused rather than fringed, which matches the idea that “meeting the criterion”
counts as being in the attended set. Other conventions (e.g. making both sets closed or both open
at τI ) would require separate handling of the boundary case and can introduce unwanted ambiguity.
Sketch. If x were in both, we would have Ic (x) ≥ τI and 0 < Ic (x) < τI , contradiction.

Remark 1579. Proof sketch and intuition. The proof is a direct contradiction: it combines the
defining inequalities for membership in each set. Visually, if one plots Ic (x) on the unit interval,
Focus is the right-closed ray [τI , 1] while Fringe is the open interval (0, τI ); these do not overlap.
Remark 1580. An additional way to see the same point is to observe that, for each fixed τI , the
predicates

           x ∈ Focusc (τI ) ⇐⇒ Ic (x) ∈ [τI , 1],         x ∈ Fringec (τI ) ⇐⇒ Ic (x) ∈ (0, τI )

pull back two disjoint subsets of [0, 1] along the function Ic . No properties of Ic beyond being
single-valued are needed for this pullback-disjointness argument.
Lemma 13 (Focus/fringe partition the positive-intensity region). Let Pc := {x ∈ Xc : Ic (x) > 0}.
Then Pc = Focusc (τI ) ∪˙ Fringec (τI ) (disjoint union).
Remark 1581. This lemma states that, among whatever is present at all (positive intensity), the
threshold τI induces an exhaustive dichotomy: everything present is either salient enough to be
in focus or weakly present enough to be in fringe. The restriction to Pc matters: elements with
Ic (x) = 0 are treated as absent rather than as “infinitely fringe.”
Remark 1582. Operationally, one can read Pc as the set of “currently activated” or “presented”
items, with focus and fringe giving a two-tier stratification of that active set. This avoids forcing a
trichotomy in which Ic (x) = 0 would have to be assigned to one of the two attentional tiers; instead,
Ic (x) = 0 is reserved for non-presentation. In many applications, this makes later aggregation steps
cleaner: sums, averages, or normalizations over “present” items can be taken over Pc without
inadvertently counting absences.
Sketch. If Ic (x) > 0 then either Ic (x) ≥ τI (so x ∈ Focus) or Ic (x) < τI (so x ∈ Fringe). Disjointness
is Lemma 12.

Remark 1583. Proof sketch and intuition. The proof is a case split on whether a real number is
at least τI or below it. One can think of τI as a moving “attentional horizon”: everything above the
horizon is foreground, everything below (but not zero) is background.
Remark 1584. At the extremes, the statement behaves as expected (when the definitions are in-
stantiated): if τI = 0, then Focusc (τI ) coincides with Pc and Fringec (τI ) is empty, corresponding
to an “everything present is focused” idealization. If τI = 1, then Focusc (τI ) consists precisely of
items at maximal intensity (those with Ic (x) = 1), and all other present items lie in the fringe.
These boundary cases can be useful as sanity checks when calibrating τI in examples.

                                                    609
Lemma 14 (Monotonicity in the focus threshold). If τ1 ≤ τ2 then

                      Focusc (τ2 ) ⊆ Focusc (τ1 ),         Fringec (τ1 ) ⊆ Fringec (τ2 ).

Remark 1585. Raising the focus threshold makes focus smaller (harder to qualify) and fringe
larger (easier to qualify), exactly as one would expect. This monotonicity is useful when comparing
different “modes” of the same agent or different agents: an agent with a stricter focus criterion is
literally focusing on fewer items, in the precise sense of set inclusion.

Remark 1586. Formally, Lemma 14 says that the assignment τ 7→ Focusc (τ ) is antitone (order-
reversing) in τ , while τ 7→ Fringec (τ ) is monotone (order-preserving). Thus, as τ varies, the focus
sets form a nested family (a decreasing “filtration” by thresholds), and the fringe sets form a nested
family in the opposite direction. This nestedness is often what one needs when proving stability
statements under changes of attentional resolution.

Sketch. If Ic (x) ≥ τ2 and τ1 ≤ τ2 then Ic (x) ≥ τ1 . If 0 < Ic (x) < τ1 and τ1 ≤ τ2 then 0 < Ic (x) <
τ2 .

Remark 1587. Proof sketch and intuition. The argument is again order-theoretic on [0, 1]. On
a number line, moving the threshold right shrinks the ≥-region and expands the <-region; the
inclusions are just that picture translated into set language.

Remark 1588. In applications, one sometimes varies τI dynamically (e.g. to model fatigue, time
pressure, or deliberate concentration). Lemma 14 then provides immediate “directional” guarantees:
any item that remains focused under a stricter threshold must also have been focused before the
shift, and any item that was in the fringe under a looser threshold will remain in the fringe when
the criterion is tightened. These implications can be used to justify reusing previously computed
information for items that are guaranteed not to have changed attentional tier.

28.3    Abstraction and concreteness
Remark 1589. Abstraction here is treated as a controlled forgetting: a surjection q : Xc  A
partitions Xc into fibers, and elements in the same fiber are “identified” at the abstract level. The
preorder q1  q2 says: q2 is at least as abstract as q1 (it can be obtained by further collapsing the
outputs of q1 ). This is a standard idea in mathematics (factorization through quotients), but in
Hyperseed it is also a disciplined way of discussing Abstract vs. Concrete (Hyperseed-Concepts 51
and 83) within a fixed context (Hyperseed-Concept 86).

Remark 1590. It is sometimes helpful to keep in mind the quotient-set picture: a surjection
q : Xc  A is (up to bijection of codomains) the same data as an equivalence relation ∼ on Xc ,
where x ∼ y iff q(x) = q(y), together with a choice of names for the equivalence classes. From
this viewpoint, “controlled forgetting” means replacing Xc by the set of its ∼-classes, and the order
relation  compares how much information is retained by comparing the induced partitions.

Lemma 15 (The abstraction preorder is a preorder). The relation  on abstractions q : Xc  A
is reflexive and transitive.

Remark 1591. The point is modest but foundational: we can reason about “more abstract than”
in the usual order-theoretic way, without worrying that the relation fails basic coherence conditions.
Once this is established, one may meaningfully talk about chains of abstractions, maximal elements
under admissibility constraints, and so on.

                                                     610
Remark 1592. Note that a preorder need not be antisymmetric: it can happen that q1  q2 and
q2  q1 without q1 = q2 as functions, for example when q1 and q2 induce the same partition of
Xc but use different codomains or different labels for the same fibers. Thus, the correct “equality
notion” implicit in  is often equality of induced equivalence relations (or isomorphism of quotients)
rather than literal equality of maps.

Sketch. Reflexive: q = idA ◦ q. Transitive: if q2 = r12 ◦ q1 and q3 = r23 ◦ q2 , then q3 = (r23 ◦ r12 ) ◦
q1 .

Remark 1593. Proof sketch and intuition. Reflexivity uses the trivial observation that composing
with an identity changes nothing. Transitivity uses associativity of function composition: if q1
factors to q2 and q2 factors to q3 , then q1 factors directly to q3 . In terms of partitions, refining
(collapsing) and then refining again is the same as refining once by the composite collapse.

Lemma 16 (Factorization iff inclusion of induced equivalence relations). Let qi : Xc  Ai and
define x ∼qi y ⇐⇒ qi (x) = qi (y). Then

                                     q1  q2    ⇐⇒        (∼q1 ⊆ ∼q2 ).

Equivalently: q1  q2 iff for all x, y, q1 (x) = q1 (y) → q2 (x) = q2 (y).

Remark 1594. This lemma gives an extremely useful reformulation: instead of explicitly producing
a map r with q2 = r ◦ q1 , we can check an inclusion between the equivalence relations (partitions)
induced by q1 and q2 . Intuitively, “q2 is coarser” means: whenever q1 fails to distinguish two points
(puts them in the same fiber), q2 must also fail to distinguish them. Thus, the lemma translates a
statement about existence of a factor map into a purely relational statement about fibers.

Remark 1595. Two small technical clarifications are often useful when applying Lemma 16. First,
surjectivity of q1 is exactly what guarantees that the definition of r : A1 → A2 by “pick an x with
q1 (x) = a” is total. Second, the factor map r is then forced (and hence unique) by the requirement
q2 = r ◦ q1 : for each a ∈ A1 , r(a) must be the common value of q2 on the fiber q1−1 (a) (well-
definedness is the only real issue).

Sketch. (→) If q2 = r ◦ q1 and q1 (x) = q1 (y) then q2 (x) = r(q1 (x)) = r(q1 (y)) = q2 (y). (⇐)
Assume q2 is constant on fibers of q1 . Define r : A1 → A2 by choosing any x with q1 (x) = a (exists
since q1 is surjective) and setting r(a) := q2 (x). Well-definedness follows from the fiber-constancy
assumption. Then q2 = r ◦ q1 .

Remark 1596. Proof sketch and intuition. The forward direction is immediate: composing with
r cannot split a fiber that q1 has already collapsed. The reverse direction is the more instructive
step: if q2 does not distinguish within any fiber of q1 , then each fiber-label a ∈ A1 can be sent to
the common value of q2 on that fiber, producing the required r. The only delicate point is well-
definedness, and it is secured precisely by the assumption that q2 is constant on fibers.

Corollary 4 (Fiber inclusion along ). If q1  q2 , then for all x ∈ Xc ,

                                       q1−1 (q1 (x)) ⊆ q2−1 (q2 (x)).

Remark 1597. This corollary states the same “coarsening” idea at the level of individual fibers:
the equivalence class of x under the finer abstraction is contained in the equivalence class of x under
the coarser abstraction. This is often the most directly used form in arguments about concreteness
constraints, because many such constraints are phrased in terms of fiber sizes.

                                                    611
Remark 1598. In particular, whenever a size notion is monotone under inclusion (e.g. cardinality,
measure, diameter bounds stated as “at most”, or any predicate Small that is downward closed as in
Lemma 17), Corollary 4 immediately transports such statements from a coarser fiber to a finer one,
and contrapositively transports “not small” statements from a finer fiber to a coarser one. This is
the basic mechanism behind many “abstractness persists under further abstraction” arguments.
Sketch. If y ∈ q1−1 (q1 (x)), then q1 (y) = q1 (x). By Lemma 16, this implies q2 (y) = q2 (x), hence
y ∈ q2−1 (q2 (x)).

Remark 1599. Proof sketch and intuition. Pick any point y identified with x by q1 . Since q2 is
coarser, it must also identify y with x. In partition language: every block of the fine partition sits
inside a block of the coarse partition.
Lemma 17 (Abstractness propagates to coarser admissible abstractions (mild assumption)). Fix
a concreteness constraint Kc and a predicate Small(·) on subsets of Xc . Assume Small is downward
closed: A ⊆ B and Small(B) implies Small(A). Let x ∈ Xc be abstract in the sense of Def.
52, witnessed by some Kc -admissible q1 such that ¬Small(q1−1 (q1 (x))). If q1  q2 and q2 is also
Kc -admissible, then x is also witnessed abstract by q2 .
Remark 1600. The “mild assumption” is the downward-closure of Small, which is exactly the
property needed to ensure that “not small” is upward closed with respect to inclusion: if A ⊆ B and
A is not small, then B cannot be small. This matches the intended reading in typical cases: for
instance, if Small(S) means “S has at most N elements” or “S has diameter at most ε”, then any
superset of a non-small set remains non-small.
Sketch. By Corollary 4, from q1  q2 we have

                                       q1−1 (q1 (x)) ⊆ q2−1 (q2 (x)).

Suppose for contradiction that Small(q2−1 (q2 (x))) holds. Since Small is downward closed, the in-
clusion would imply Small(q1−1 (q1 (x))), contradicting the witnessing condition ¬Small(q1−1 (q1 (x))).
Hence ¬Small(q2−1 (q2 (x))). Together with the assumed Kc -admissibility of q2 , this makes q2 a valid
witness (in the sense of Def. 52) that x is abstract.

Remark 1601. Proof sketch and intuition. Coarsening an abstraction can only make fibers larger
(never smaller), so any “largeness” phenomenon exhibited by the q1 -fiber of x persists for the
corresponding q2 -fiber. The admissibility hypotheses are logically separate: they ensure that both q1
and q2 are permitted abstractions under the same concreteness constraint Kc , so that the witness
can legitimately be replaced by the coarser abstraction without leaving the intended model class.
Remark 1602. The content is: if an element is already “too coarse” (its fiber is not small) under
some admissible abstraction, then making the abstraction even coarser cannot restore concreteness.
This matches an intuitive irreversibility: once you have thrown away distinctions, you cannot
recover them by throwing away even more. The only extra hypothesis is a weak regularity condition
on what counts as “small”: downward closure says that if a big set is small (which is unusual), then
all its subsets are small; contrapositively, if a subset is not small then no superset can be small. This
is exactly what the proof uses. Equivalently, the statement can be read as a monotonicity principle:
“being abstract” is upward closed along coarsenings of the abstraction, because coarsening only ever
enlarges the equivalence class of x (its fiber), and enlarging a set cannot turn a non-small set into
a small one when smallness is downward closed. In this sense, the remark isolates the precise
point where regularity of the size predicate enters: nothing about cardinality is needed, only the
order-theoretic behavior of the predicate Small(·) with respect to ⊆.

                                                   612
Sketch. By Corollary 4, q1−1 (q1 (x)) ⊆ q2−1 (q2 (x)). If Small(q2−1 (q2 (x))) held, downward closure
would imply Small(q1−1 (q1 (x))), contradicting the witness. So ¬Small(q2−1 (q2 (x))); hence q2 also
witnesses abstractness of x. In slightly more explicit contrapositive form: since q1−1 (q1 (x)) is not
small and is contained in q2−1 (q2 (x)), the closure condition forces q2−1 (q2 (x)) to be not small as well,
because otherwise the smaller set would inherit smallness. The admissibility condition is used only
to ensure that q2 is among the abstractions one is allowed to consider as potential witnesses.

Remark 1603. Proof sketch and intuition. The proof is a simple order argument on sets. Step
(1) uses the previously proved fiber inclusion: coarsening enlarges fibers. Step (2) uses downward
closure in contrapositive form: “not small” propagates upward to supersets. Thus, the witness of
abstractness persists along  so long as admissibility (Kc ) is preserved. One can also view this as
a stability property of counterexamples: once x has a fiber that is “too large to be concrete” under
some q1 , any q2 that forgets at least as much as q1 must produce a fiber that contains that same
counterexample, hence cannot pass the smallness test. This makes precise the informal slogan that
loss of distinctions is one-way: refinement may restore concreteness, but coarsening cannot.

28.4    Non-duality as a bridge between perspectives (context translations)
Remark 1604. A context translation T : Xc → Xd formalizes the act of viewing the “same”
situation through a different lens. The compatibility condition is deliberately phrased negatively: it
forbids erasing strong distinctions. In cognitive terms, this is a minimal requirement for transfer:
if a salient distinction in one context becomes invisible in the translated context, then predicates
like repetition/variety/non-duality will not be stably comparable across perspectives. This resonates
with the general transfer-learning motivation of Hyperseed (Hyperseed-Concepts 192 and 193) and
the associated mathematical program (see [7] for broader context). At the level of interpretation,
this means T is not required to preserve all structure (it may merge some states, rename features,
or otherwise reinterpret them), but it is required to preserve whatever the theory treats as evidence
of distinction. The point of stating the condition in terms of δ-inequalities is that it directly con-
trols the quantities that feed into later definitions (e.g. mutual distinction, crisp thresholds, and
the paraconsistent pairing that underlies non-duality), rather than imposing an external notion of
similarity.
Lemma 18 (Non-dually compatible translations preserve distinction evidence). Let T : Xc → Xd
be non-dually compatible (Def. 53). Then for all x, y ∈ Xc ,

                                     Distc (x, y) ≤ Distd (T x, T y).

In particular, if x#c y then T x#d T y (using the same τδ ). Moreover, NonDualc (x, y) implies
NonDuald (T x, T y). In other words, T is monotone with respect to the derived evidence order-
ing on mutual distinction: it cannot reduce the “two-way” support for distinguishing x from y. The
threshold clause emphasizes that the result is not merely qualitative: it preserves whatever fixed
operational cutoff τδ is used to declare a distinction to be crisp in the source context.
Remark 1605. In plain language: a non-dually compatible translation cannot make two things
less mutually distinct (in the evidence order), so any crisp distinction is preserved. The second
clause says that even the more delicate paraconsistent situation of non-duality is preserved: strong
evidence both for and against distinction survives translation. This is a rigorous expression of
a phenomenological aspiration: shifting perspective may reinterpret an experience, but it should
not arbitrarily delete its salient tensions. Put differently, a translation may add nuance (e.g. by
increasing evidence for distinction in one or both directions), but it may not “flatten” a distinction

                                                    613
that was already present at or above the salient level. The non-duality preservation is especially
important because it says the translation respects not only clean separations but also ambiguous or
tension-laden pairings where both poles of evidence are simultaneously significant.

Sketch. Non-dual compatibility gives (for all x, y) inequalities of the form δc (x, y) ≤ δd (T x, T y)
and, by swapping x, y, also δc (y, x) ≤ δd (T y, T x). Monotonicity of ⊗ yields δc (x, y) ⊗ δc (y, x) ≤
δd (T x, T y) ⊗ δd (T y, T x), i.e. Distc (x, y) ≤ Distd (T x, T y). Componentwise order then preserves
threshold exceedance in both channels, giving the crisp and non-dual consequences. Concretely,
for the crisp clause: if Distc (x, y) ≥ τδ (in the relevant ordering), then the inequality forces
Distd (T x, T y) ≥ τδ as well, because increasing a p-bit value cannot make it fall below a fixed
threshold. For the non-dual clause, the same componentwise monotonicity applies simultaneously
to the “distinguish” and “do-not-distinguish” components that define NonDual, so having both
components above their respective thresholds in context c implies the same in context d.

Remark 1606. Proof sketch and intuition. The proof composes three monotonicities: (1) com-
patibility gives two directed inequalities for δ (one for each direction); (2) monotonicity of ⊗ lifts
directed inequalities to an inequality about mutual distinction Dist; (3) componentwise order en-
sures that if a p-bit value increases, then any threshold condition that held before still holds after.
One may picture T as an embedding that may stretch distances but is not allowed to collapse them
below salient levels. A useful mental model is that δ(·, ·) supplies directed “pushes apart” evidence;
⊗ aggregates the two directed pushes into a single mutual signal. Non-dual compatibility says each
directed push is not weakened by translation; therefore the aggregate mutual signal is not weak-
ened either. The preservation of non-duality then follows because non-duality is formulated as a
conjunction of threshold conditions on the same underlying evidence channels, and conjunction of
monotone properties remains monotone under such translations.

Lemma 19 (Closure under composition; identity translation). If T : Xc → Xd and U : Xd → Xe
are non-dually compatible, then U ◦ T : Xc → Xe is non-dually compatible. The identity map
idXc is non-dually compatible. This shows that “non-dually compatible translation” behaves like a
structural constraint rather than an ad hoc property of a single map: it is stable under chaining of
perspective shifts, and it is satisfied by the trivial shift that changes no perspective at all.

Remark 1607. This lemma says that non-dually compatible translations form a small but robust
algebra: they compose and include identities. As a result, contexts and their admissible translations
can be treated categorically (at least informally): one can build multi-step perspective shifts without
losing the guarantee that distinctions are not erased. In particular, once a downstream analysis is
stated in a target context Xe , one may safely precompose it with any sequence of such translations
from a source context without worrying that crisp distinctions (or non-dual tensions) were artifacts
of a particular viewpoint and disappear under the change of lens. The lemma is thus a technical
enabler for discussing families of contexts connected by permissible reinterpretations.

Sketch. For all x, y, δc (x, y) ≤ δd (T x, T y) ≤ δe (U (T x), U (T y)) by transitivity of ≤, and similarly
for the swapped-argument inequality. This is exactly Def. 53 for U ◦ T . For the identity, both
inequalities reduce to δc (x, y) ≤ δc (x, y). No further properties of δ are needed beyond the order
structure already assumed, which is why the argument is purely diagrammatic: it is just the fact
that an order-preserving lower bound remains a lower bound after applying another order-preserving
lower bound.

Remark 1608. Proof sketch and intuition. Composition uses nothing mysterious: it is simply the
transitivity of the underlying order ≤. If T does not reduce distinction evidence and U does not

                                                   614
reduce distinction evidence, then doing T and then U does not reduce it either. The identity case
is the degenerate translation that changes nothing, so it trivially preserves every distinction. From
the perspective-bridging viewpoint, this means that “respecting salient distinctions” is a property
that can be required locally at each step of a translation pipeline, while still guaranteeing the global
property for the entire pipeline. This aligns with modularity: one can design or learn translations in
stages, checking the same simple inequality condition at each stage, and then compose them without
re-verifying everything from scratch.


29     Helper theorems for order, time, and becoming (Section 7)
Standing assumptions and notation. A proto-time is a pair (T, <) with < a strict partial
order (Defs. 54–55). Where needed, fix the canonical p-bit quantale V = [0, 1]2 with componentwise
order ≤, join ⊕ as componentwise max, and tensor ⊗ as componentwise multiplication. A p-bit
temporal evidence relation is B : T × T → V (Def. 56). Optional coherence constraints are those
in Def. 57. For linearization/quotients, Past/Future sets and ∼ are as in Def. 59. For becoming,
Dist : T × E × E → V and NDVar/Becoming are as in Defs. 60–62. For event calculus, predicates
and operators are as in Defs. 63–66. TimeCtx/similarity/TemporalSimilarity are as in Defs. 67–69.
Regularity predicates are as in Defs. 70–72. The functorial process view is Def. 73.
Remark 1609. The organizing thought here is that “time” is treated in two layers. First there
is a thin, structural layer: a set T of “time-like” indices equipped with a strict partial order <,
yielding what the core calls a proto-time (Hyperseed-Concept 142). This is intentionally weaker
than a linear timeline: it permits branching and incomparability, which is often what one has before
imposing a narrative or a measurement protocol.
     Second there is a graded, paraconsistent evidential layer, in which comparisons t1 < t2 may be
supported or disputed by data. Concretely, the canonical p-bit quantale V = [0, 1]2 encodes a pair
v = (v + , v − ) of positive and negative evidence channels (in the sense of paraconsistent valuation;
see also [23, 24]). Componentwise order means (a+ , a− ) ≤ (b+ , b− ) iff a+ ≤ b+ and a− ≤ b− .
The join v ⊕ w is componentwise max, representing “take the stronger of two arguments”; the
tensor v ⊗ w is componentwise multiplication, representing “compose pieces of support” along a
chain. A temporal evidence map B : T × T → V thus assigns to each ordered pair (t1 , t2 ) a
degree of support B + (t1 , t2 ) and a degree of counter-support B − (t1 , t2 ) for the claim “t1 is before
t2 ” (Hyperseed-Concepts 63 and 52). This style of quantale-based graded reasoning connects to the
broader weakness/quantale program [3] and to the original Hyperseed presentation [1].

How the two layers interact. Although (T, <) and B are introduced separately, the intended
use is that the structural order provides a baseline constraint (e.g. what is allowed in a model),
while the evidential map provides a flexible mechanism for learning, aggregating, and revising
order-claims from heterogeneous sources. In particular, one should read B(t1 , t2 ) as evidence about
the ordering claim, not as the ordering claim itself: the strict partial order < can be taken as
a conservative “skeleton” that may later be refined, quotiented, or linearized (Def. 59) using the
evidential layer. This separation is what allows the later helper results to state clean monotonicity
and closure properties for the constructions built from B without requiring that the underlying
proto-time be total, well-founded, or otherwise timeline-like.

Interpreting p-bits and inconsistency. The p-bit value v = (v + , v − ) ∈ [0, 1]2 can be read as
allowing independent degrees of affirmation and denial. Thus, values near (1, 0) represent strong
support with little objection, values near (0, 1) represent strong counter-evidence, and values with

                                                   615