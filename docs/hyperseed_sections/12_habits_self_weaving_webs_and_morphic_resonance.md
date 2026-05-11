# 12 Habits, self-weaving webs, and morphic resonance

Remark 477. The philosophical pressure behind this bifurcation is simple: a mind (or any model-
ing system) must both (i) compress the world into comparative priorities (a ranking of what matters,
what explains, what controls), and (ii) keep track of the fact that the world is not a ladder but a
tangle, where explanation and influence typically move along many partially redundant and mu-
tually constraining routes. Hierarchy and heterarchy are thus not competing metaphors; they are
complementary projections of the same cognitive act, seen from the angles of order and connectivity
(Hyperseed-Concepts ?? and ??).
    A useful way to read this remark is that hierarchy expresses a kind of compression (reduce
many degrees of freedom to a comparative relation), while heterarchy expresses a kind of closure
under interaction (allow many routes of influence and evidential support, including feedback).
A cognitive system that only ranks without interconnection becomes brittle (it cannot represent
mutual constraint, circular causation, or context sensitivity), while a cognitive system that only
connects without ranking becomes diffuse (it cannot decide what to attend to, what to optimize,
or what to treat as explanatory leverage). Thus, the two motifs show up not merely as descriptive
metaphors but as recurring representational necessities.
    Hyperseed uses these motifs in several places: subpattern hierarchy (patterns within patterns),
control/perceptual hierarchies, self-hierarchies, and the “pattern web” picture of cognition. Here
“subpattern hierarchy” points to part–whole and compositional structure (a pattern may be built
from constituent patterns), whereas “control/perceptual hierarchies” point to layered organization
in action and inference (e.g. high-level goals constraining lower-level controllers, and higher-level
interpretations organizing lower-level percepts). “Self-hierarchies” similarly reflect that an agent
can maintain multiple self-models with differing levels of generality, authority, or temporal scale.
Meanwhile, the “pattern web” picture emphasizes that these hierarchical decompositions are em-
bedded in a larger network: patterns participate in many overlapping decompositions and predic-
tive/explanatory links, and any given pattern typically inherits constraints from many sources at
once.
    The mathematical point of this section is that all of these can be treated as special cases of
quantale-enriched structure (Section 3): the same formal machinery that represents “how related”
two entities are (possibly with degrees, costs, or truth-values) can specialize to order-theoretic
hierarchy, metric-like connectivity, and more general graded relations. Concretely, enrichment
replaces the crisp statement “there is a relation from a to b” with a value that can encode intensity,
confidence, cost, or compatibility, and it equips these values with a notion of composition. When
applied to patterns, this means we can model not only whether one pattern subsumes or controls
another, but also to what extent and through which chains of intermediate patterns that relationship
holds.
• A crisp hierarchy is enrichment in the Boolean quantale {0, 1}.

• A metric heterarchy is enrichment in the Lawvere quantale ([0, ∞], ≥, +, 0).

• A paraconsistent, graded hierarchy is enrichment in a p-bit quantale (Section 3.4).
To unpack the intuition: Boolean enrichment yields relations valued in {0, 1}, so composition
reduces to logical conjunction and the structure behaves like a preorder (and, with suitable an-
tisymmetry, a partial order), matching the usual mathematical abstraction of “hierarchy.” Law-
vere enrichment replaces “true/false relatedness” with extended nonnegative “distance” or “cost,”
where composing paths adds costs; this naturally captures web-like multi-path structure because
indirect connections compete with direct ones via triangle-inequality-style constraints. Finally,
p-bit enrichment allows relationship-values that can represent graded support and graded conflict

                                                 221
simultaneously (paraconsistency), which is important when the same pair of patterns can be con-
nected by evidence that points in different directions, or when an agent maintains multiple partially
incompatible models without immediate collapse into triviality.
Remark 478. The “pattern web” framing is central in Hyperseed’s earlier presentations and re-
lated work on patterns, emergence, and cognitive network structure [1, 5]. The present section is
deliberately modest: it does not add new metaphysics; it supplies a single mathematical dialect in
which these recurrent motifs can be spoken without ambiguity.
    In this sense, the goal is methodological: once hierarchies and webs are both expressed as en-
riched structures, one can translate intuitions and results across domains. For example, “subpattern-
of” can be treated as an order-like relation, while “influences” or “predicts” can be treated as graded,
directional, and compositional; and in both cases, the formalism makes explicit what it means for
indirect relationships to accumulate through intermediate patterns.
    We will define the Hyperseed terms (hierarchy, systemic hierarchy, subpattern hierarchy, heter-
archy, pattern web) and then show how they fit into the enriched-categorical core.

11.2    Hierarchy as observer-assessed order
Hyperseed treats “hierarchy” as inherently observer-relative: an observer O assesses some entities
as higher than others, in some respect (importance, generality, desirability, control, explanatory
priority). The simplest mathematical representation of “higher than” is a partial order, but we
will allow graded and paraconsistent structure. In particular, allowing “graded” comparisons ac-
commodates the common situation where O can compare u and v only weakly or provisionally,
while allowing “paraconsistent” comparisons accommodates the situation where O simultaneously
carries evidence both for and against the claim that u outranks v without collapsing into triviality.
Note also that even in the ungraded case, a hierarchy need not be total: many pairs of entities may
remain incomparable, reflecting underspecification, competing criteria, or simply irrelevance under
the current respect-of-comparison.
Definition 131 (Order-like relations). Let U be a set of entities (objects, patterns, processes, roles).
• A preorder on U is a relation ⊆ U × U that is reflexive and transitive.
• A partial order is a preorder that is also antisymmetric.
• A graded preorder (relative to a commutative quantale V ) is a map
                                              h:U ×U →V
  with reflexivity e ≤ h(u, u) and transitivity
                             h(u, v) ⊗ h(v, w) ≤ h(u, w)      (u, v, w ∈ U ),
  where (V, ≤, ⊕, ⊗, e) is as in Section 3.
    It is worth stressing what is not required by these definitions. A preorder permits ties (distinct
u 6= v with u  v and v  u), which can be interpreted as observational or pragmatic equivalence
under the chosen respect-of-comparison. Antisymmetry upgrades this to a partial order, ruling out
such ties except when u = v; thus, moving from preorder to partial order amounts to deciding that
“mutual outranking” should be treated as identity rather than as a legitimate equivalence class.
Conversely, neither preorders nor partial orders require comparability: it can happen that neither
u  v nor v  u holds, which is often the appropriate formalization of “O has no basis to rank
them (yet)”.

                                                  222
Remark 479 (Notation unpacking: what the symbols mean). The data of a graded preorder live
in a commutative quantale (V, ≤, ⊕, ⊗, e) (Section 3). Here:

• V is the space of “grades” (truth-strengths, costs, evidences, similarities, etc.).

• ≤ is the order on grades (“no stronger than”).

• ⊕ is the join/supremum operation (aggregating alternative supports).

• ⊗ is the monoidal product (aggregating sequential supports, as in composition along a path).

• e is the unit grade (the neutral element for ⊗), playing the role of identity.

Thus h(u, v) ∈ V should be read as “the degree (in V ) to which u is at least as high as v” in the
hierarchy. The transitivity inequality says: if u is above v and v is above w, then (by composing
these two claims) u is above w to at least the composed degree.

   One additional interpretive point is that ⊕ and ⊗ encode two qualitatively different ways of
accumulating support for a comparison. Typically, ⊗ is used when comparisons are chained (e.g.,
“u outranks v” and “v outranks w” together provide a route from u to w), while ⊕ is used when
comparisons arise through multiple alternative routes or arguments (e.g., two different explanatory
pathways both suggest that u outranks v). This separation becomes especially important when
the same domain U simultaneously participates in multiple interacting structures: a “hierarchy”
viewed as an order-like relation can later be combined with other relational webs using the same
quantale operations, so that path-composition and route-aggregation are not redefined ad hoc for
each application.

Remark 480 (Intuition, examples, and why graded preorders matter). A crisp preorder answers
a yes/no question: “is u above v?” But in cognition and modeling we usually have degrees: we may
have strong reasons, weak reasons, or even simultaneous reasons for and against a comparison. A
graded preorder is exactly a disciplined way to represent such comparative gradations (Hyperseed-
Concept ??).
    Two simple examples:

• If V = {0, 1} with ⊗ = ∧ and ⊕ = ∨, then h(u, v) = 1 means “u  v” in the ordinary preorder
  sense. Transitivity becomes (u  v ∧ v  w) ⇒ u  w.

• If V = [0, 1] with ⊗ as multiplication and ⊕ as maximum, then h(u, v) can be read as “confidence”
  in the comparison u  v. A longer chain of comparisons generally decreases confidence by
  multiplication, while multiple independent routes can increase it by the maximum.

The usefulness is structural: once comparisons are V -valued, one can reuse the same algebra both
for “hierarchy” and for “web” propagation later in the section, rather than maintaining separate
formalisms. This is also where Hyperseed’s notion of weakness naturally enters, because weakness
is precisely an order-theoretic measure of what distinctions one has collapsed [3, 2] (Hyperseed-
Concept 202).

    To connect these examples to more applied readings: when V = [0, 1] is interpreted as confi-
dence, the inequality h(u, v) ⊗ h(v, w) ≤ h(u, w) enforces the idea that indirect support for u  w
via v should never exceed what the model assigns directly. If the model later learns a stronger
direct comparison for u  w, this can be seen as adding a new “route” whose contribution can be
combined (via ⊕) with the routed support. If instead V represents a cost or penalty scale, then

                                                 223
≤ may be interpreted as “no worse than,” and ⊗ can be interpreted as accumulating costs along
a chain; in that case the same axiom becomes a disciplined form of “taking paths seriously” while
still preferring cheaper direct comparisons when available. These shifts of interpretation are exactly
why the definition is parameterized by a quantale rather than hard-coding a particular numeric
scheme.
Remark 481 (Thin V -categories). A graded preorder is exactly the same data as a thin V -enriched
category: there is at most one hom-value between any two objects, and composition is encoded by
the quantale transitivity inequality. Thus, “hierarchy” is naturally treated as a special case of the
enriched-categorical core.
    This thinness perspective also clarifies the difference between “having a hierarchy” and “having
a richer relational structure.” A thin V -category records only the best available grade h(u, v) of the
comparison, not the internal structure of why u outranks v (e.g., which intermediate arguments,
subcriteria, or evidential sources support it). Later, when we discuss pattern webs, those internal
justifications can be represented explicitly as additional nodes and edges, while the induced graded
preorder can be recovered as an “overall reachability/strength” summary through the same (⊕, ⊗)
machinery.
Definition 132 (Observer-assessed hierarchy). Fix an observer/context O. A hierarchy for O on
a domain U is a graded preorder
                                      hO : U × U → VO
for some quantale VO chosen to match the observer’s representational regime. In the p-bit case,
                         −
hO (u, v) = (h+
              O (u, v), hO (u, v)) encodes positive and negative evidence for “u is above v.”

    The freedom to choose VO is not merely technical: it expresses that different observers may
treat the same underlying signals as probabilities, costs, plausibilities, bipolar evidences, or even
multi-criteria vectors. Even for a fixed observer, different respects-of-comparison can justify dif-
ferent codomains: “priority under time pressure” might be naturally cost-like, while “explanatory
generality” might be naturally evidence-like. In the p-bit (positive/negative bit) case, allowing
                −
both h+O and hO to be simultaneously large permits the model to represent genuine tension (e.g.,
competing heuristics) without forcing an immediate resolution; the graded preorder axioms then
constrain how such tensions propagate along chains of comparisons.
Remark 482 (Intuition and simple examples). This definition bakes in a central Hyperseed stance:
hierarchy is not “in the world” as a bare relation, but in the triad (world, observer, respect-of-
comparison). Formally, hO is indexed by O, and even the codomain VO is chosen to suit O’s mode
of representation (Hyperseed-Concept 86).
    A simple example is a task-based priority ordering in an intelligent system: U might be a set of
goals or subgoals, and hO (u, v) encodes the degree to which u has priority over v given the current
task context (cf. the broader AGI motivation for context-relative prioritization in [19]). Another
example is an explanatory hierarchy: U might be hypotheses, and hO (u, v) measures how strongly
u is judged a “higher-level” explanation than v in the sense of compressing more data with fewer
assumptions [5]. The utility of this observer-indexed view is that it lets us discuss multiple coexisting
hierarchies without contradiction: distinct observers (or the same observer at different times) may
impose distinct but internally coherent VO -orders.
    A further consequence of indexing by O is that changes in context can be modeled as changes
in hO itself rather than as inconsistencies in a single absolute hierarchy. For instance, if O shifts
from “short-term reward” to “long-term safety” as the respect-of-comparison, the domain U may

                                                  224
remain the same while the ranking relation changes substantially; this is naturally expressed by
moving to a different hO (or, equivalently, treating the observer as updated). Similarly, disagree-
ments between observers can be tracked at the level of their chosen quantales and aggregation
rules: two observers might share the same underlying comparisons but combine them differently
(different ⊗), or they might treat alternative supports differently (different ⊕), yielding different
induced hierarchies even when looking at the same evidence. In this sense, “observer-assessed hi-
erarchy” is a portability layer: it isolates the order-like constraints (reflexivity, transitivity) from
the representational conventions by which O encodes and composes comparative judgments.

Remark 483 (Values and “higherness”). Hyperseed’s gloss is that entities higher in a hierarchy
are “more valuable in some sense.” Formally, this can be captured in several equivalent ways:

• Order-first: define hO directly as an order of priority or importance.

• Value-first: define a valuation νO : U → V (or to R) and set hO (u, v) to be evidence that
  νO (u) ≥ νO (v).

• Constraint-first: define hO as the order induced by a model class (e.g. the simplest causal expla-
  nations), so that “higher” means “more explanatory” or “more compressive.”

In later sections, these perspectives will be linked: in a resource-sensitive ontology, “valuable” typ-
ically means “valuable for prediction/control under bounded effort,” which often correlates with
explanatory compression. In particular, the “value-first” stance can be read as a representation
theorem in miniature: whenever one has a (possibly graded) comparative judgment of “at least as
important as,” it is often convenient to embed that judgment into a numerical or lattice-valued score
νO that makes comparisons mechanically checkable. Conversely, the “order-first” stance emphasizes
that the comparison itself is primary: one may know that u outranks v even when no single scalar
score captures all the reasons, motivating valuations into richer codomains V (e.g. vectors, inter-
vals, or evidence pairs). The “constraint-first” stance makes explicit that “higher” can be tied to
a background standard of adequacy: if two descriptions fit observed behavior equally well, then the
one requiring fewer degrees of freedom, fewer exceptions, or fewer ad hoc auxiliary assumptions can
be treated as “above” the other because it supports more robust generalization under perturbation
or distribution shift.

Remark 484. The equivalence of these perspectives is not merely a convenience; it expresses a
deeper pragmatic unity. In a Whiteheadian idiom, “value” is a mode of selection among processes,
while “explanation” is a mode of organization among descriptions; the point of a formalism like a
graded preorder is precisely that it allows these to be treated as two views of the same comparative
act [15]. One can read the graded preorder as recording a practice of preference rather than a
discovery of a metaphysical ladder: what counts as “higher” is the result of repeated comparative acts
(selection, attention, justification) stabilized into a relation. This also clarifies why “equivalence”
here should be taken up to the observer’s operational needs: different encodings (order-first vs.
value-first) may disagree on fine structure while remaining interchangeable with respect to the tasks
that motivated the hierarchy in the first place.

11.3    Systemic hierarchy via models of a dynamical system
Hyperseed introduces “systemic hierarchy” to emphasize that a hierarchy is often not a primitive
of the system, but a structure induced by a model. The intended case is: a dynamical system D
is mapped into a symbolic domain S equipped with a partial order. In this framing, “systemic”


                                                  225
is meant to contrast with purely stipulative taxonomies: the hierarchy is anchored in regularities
of D as captured by φ, even though it is not assumed to be uniquely determined by D without an
observer, a language, and a purpose.

Definition 133 (Systemic hierarchy (model-induced)). Let D be a dynamical system (in any sense
suitable for the application). Let Proc(D) denote a set of processes (or process-types) associated
with D. A hierarchical model of D consists of:

• a symbol domain S;

• a (possibly partial) order relation ≺S on (part of ) S;

• an interpretation map (a model) φ : Proc(D) → S.

We say that D manifests a systemic hierarchy relative to (S, ≺S , φ) if φ is sufficiently faithful for
the observer’s purposes and ≺S is used to guide prediction, explanation, or control. The qualifier
“for the observer’s purposes” is doing substantive work: faithfulness may mean predictive adequacy,
counterfactual reliability, or control-relevant abstraction rather than isomorphism to an underlying
“true” state space. Likewise, allowing ≺S to be defined only on part of S permits models in which
only some symbols participate in the hierarchical comparison (e.g. only those corresponding to ac-
tionable options, stable patterns, or salient macrostates).

Remark 485 (Intuition and examples). The definition is a reminder that hierarchy often appears
after representation. The system D unfolds in time; the observer selects a set of processes Proc(D)
to pay attention to; and only then does an ordering ≺S become meaningful as a cognitive or engi-
neering tool (Hyperseed-Concept 133).
    Example: in control, one may model a robot’s dynamics by a set of nested controllers and treat
high-level policies as “above” low-level motor primitives. Here S is a symbolic space of controller-
states, and ≺S encodes dominance/override relationships among control modules, used to guide
action selection [19]. Example: in explanation, one may map physical micro-processes into a sym-
bolic domain of macro-regularities; then “higher” means “more compressive” or “more predictive”
relative to some descriptive cost (echoing the pattern-based compression stance [5]). The usefulness
of the definition is that it legitimizes plural hierarchies as plural models: different φ and ≺S can
both be “right” insofar as they serve distinct purposes. A helpful way to read φ is as a choice of
coarse-graining: many distinct trajectories or micro-events in D may be sent to the same symbol
in S, and the induced hierarchy then ranks the symbols (i.e. the equivalence classes the observer
cares about), not the underlying microstates directly. In the control example, “dominance” may
itself be context-sensitive (e.g. safety overrides goal pursuit), so ≺S can encode normative or design
constraints (what should happen) as much as empirical regularities (what does happen). In the
explanation example, “compressive” can be understood relative to an explicit description length, a
model class capacity, or an algorithmic resource budget; thus the same D can yield different “higher”
macropatterns when the observer changes the allowable explanatory vocabulary.

Remark 486 (Fuzzy and paraconsistent systemic hierarchy). In realistic cognitive settings, the
order ≺S may be incomplete (only some pairs are comparable) and may be graded or disputed. This
is naturally modeled by taking ≺S to be a graded preorder hS : S × S → V . If V = [0, 1]2 , then
                         −
hS (s, t) = (h+
              S (s, t), hS (s, t)) can encode both evidence and counterevidence for “s precedes t” (or
“s dominates t”). Such a representation is useful when different data sources, different evaluators,
or different time-slices of the same evaluator support incompatible rankings: rather than forcing a
premature linearization, one records the support structure and postpones commitment to a single


                                                 226
crisp order. Operationally, graded comparisons can be used to implement decision procedures such
                                                          −
as “prefer s to t when h+
                        S (s, t) exceeds a threshold and hS (s, t) remains below a tolerance,” making
explicit how hierarchy-guided action depends on risk appetite and error costs.

Remark 487 (Why the model view matters). The same underlying system D may admit many
different hierarchical models depending on:

• the observer’s values and tasks;

• the level of abstraction (which distinctions are ignored);

• which variables are treated as controls versus observations;

• which explanatory language is chosen.

Hyperseed treats this plurality as normal. Thus, “systemic hierarchy” is best read as: there ex-
ists a useful hierarchy in some modeling space that guides successful interaction with the system.
This perspective also clarifies what it means for two hierarchies to “disagree”: they may be rank-
ing different symbolizations of the same processes, or the same symbolization under different loss
functions and intervention capabilities. For example, an engineer optimizing reliability may place
fault-monitoring processes “above” throughput-optimizing processes, while an economist modeling
the same organization may rank activities by revenue contribution; both hierarchies can be faithful
in their respective senses, because faithfulness is indexed to what is being predicted, explained, or
controlled.

Remark 488. In Peircean terms, one may say that a systemic hierarchy is a particular way
in which Thirdness (law-like mediation) is projected onto a flux of Seconds (actual interactions)
and a field of Firsts (qualities felt as salient) [14]. The formal point remains: the hierarchy is
carried by (S, ≺S ) and by the interpretive act φ, not by D alone. Equivalently, the hierarchy is a
property of a semiotic triad (world, signs, interpreter) rather than a property of the world taken
in isolation: change the signs (S), the comparative practice (≺S ), or the interpretive mapping (φ),
and the resulting “systemic hierarchy” may change even when D does not. This does not trivialize
hierarchy; it locates its objectivity in reproducible modeling and successful coordination: if many
observers with similar access and aims converge on similar (S, ≺S , φ), then the induced hierarchy
can be treated as stable for those purposes.

11.4    Subpattern hierarchy: patterns within patterns
Hyperseed defines a subpattern hierarchy by declaring y ≤ x when y is a compositional subpattern
of x. The informal criterion is: y can be combined with something else to form a pattern in x. We
formalize this using the combination operation from Section 9.

Definition 134 (Compositional subpattern). Fix a domain of entities X and a combination op-
eration ∗ : X × X → X (not assumed commutative). Let P be a set of pattern-representers (in
simple settings one may take P = X, but we keep it separate). Assume we have a (possibly graded)
predicate
                                       Pat(p; x) ∈ [0, 1]
interpreted as “degree to which p is a pattern in x” (e.g. pattern intensity).
    For p, q ∈ P, we say that p is a compositional subpattern of q, written

                                              p sub q,

                                                 227
if there exists some r ∈ X such that Pat(p ∗ r; q) is nontrivial (e.g. strictly positive, or above a
chosen threshold). In a graded version, define the subpattern strength

                                     hsub (p, q) := sup Pat(p ∗ r; q).
                                                   r∈X

Remark 489 (Intuition, examples, and usefulness). The guiding intuition is almost embarrassingly
concrete: p is a subpattern of q if p can serve as a reusable “piece” in constructing a pattern that
fits q (Hyperseed-Concept 182). The quantifier “there exists r” is the formal way to say “p can be
completed.”
     Example 1 (strings): let X be strings and ∗ be concatenation. Let Pat(p; x) be high when p is a
compressive description of x (Section 9, cf. [5]). Then p sub q says: there is some string r such
that the concatenation p∗r is itself a strong pattern for q. Example 2 (feature composition): let X be
structured feature-bundles, and let ∗ combine feature-sets. Then p sub q says: the feature-pattern
p can be augmented to yield a pattern adequate for q.
     This definition is useful because it turns the informal “patterns within patterns” idea into an
algebraic relation that can be composed and closed (later yielding hierarchy-like structure and, via
path closure, a web-like structure).

Remark 490 (Two readings). The relation p sub q can be read in (at least) two complementary
ways:

• Constructive: q can be built (in part) from p by composition.

• Explanatory: p is a reusable regularity that helps compress or predict q.

The constructive reading matches “patterns within patterns.” The explanatory reading matches
the idea that higher-level patterns summarize or bundle lower-level ones. Both will be used later
(especially in Sections 12 and 13).

Proposition 15 (Subpattern is a preorder under associativity). Assume ∗ is associative and has
an identity element e ∈ X. Assume also that for each p ∈ P there is an embedding of p into X (so
that p ∗ e is defined) and that Pat(p ∗ e; p) is nontrivial. Then sub is a preorder on P.

Remark 491 (What the proposition says, and why it matters). The statement is: once “combina-
tion” behaves like a monoid operation (associative with identity), the subpattern relation behaves like
a genuine order-like comparison: every pattern is a subpattern of itself (reflexivity), and subpattern-
hood chains (transitivity). This is important because it shows that an apparently heuristic notion
(“p is a piece of q”) inherits the same formal stability properties as more familiar hierarchies. It
also connects this section back to the enriched-order viewpoint above: preorders are precisely the
crisp case of V -enriched thin categories.

Proof. (Reflexivity.) For p ∈ P, choose r = e. By assumption Pat(p ∗ e; p) is nontrivial, so p sub p.
   (Transitivity.) Assume p sub q and q sub s. Then there exist r1 , r2 ∈ X such that Pat(p∗r1 ; q)
and Pat(q ∗ r2 ; s) are nontrivial. Using associativity, (p ∗ r1 ) ∗ r2 = p ∗ (r1 ∗ r2 ). Under the intended
compositional semantics of patterns (Section 9), a pattern used to form q can be re-used inside a
composite pattern used to form s. Thus Pat(p ∗ (r1 ∗ r2 ); s) is nontrivial (possibly with reduced
degree), implying p sub s.

Remark 492 (Proof sketch and intuition). Proof sketch. Reflexivity uses the identity element e:
completing p by “doing nothing” yields p again, so p is trivially a component of itself. Transitivity
uses associativity: if p can be completed to something that patterns q, and q can be completed to

                                                    228
something that patterns s, then concatenating the completions yields a completion witnessing that
p can be completed to pattern s.                                                                     
    The key step is the reassociation (p ∗ r1 ) ∗ r2 = p ∗ (r1 ∗ r2 ), which licenses the informal move
“reuse the subpattern inside the larger composition.” Geometrically, one can picture p as a reusable
module, and r1 , r2 as successive “adapters”; associativity says that the order of bracketing the
assembly does not change the assembled whole, so the module relationship persists through multi-
stage construction.

Remark 493 (Antisymmetry and “pattern identity”). To obtain a partial order one needs a notion
of when two patterns are “the same.” In practice, pattern identity is observer-relative: two patterns
may be distinct at one resolution and equivalent at a coarser resolution. Thus, it is often best to
treat the subpattern hierarchy as a preorder and then quotient by an equivalence relation appropriate
to the observer. This aligns with the general Hyperseed stance that equivalence is a re-description
of which distinctions are being ignored (Hyperseed-Concept ??). In particular, antisymmetry fails
precisely when the observational interface cannot (or chooses not to) distinguish two patterns that
are mutually subpatterns of one another: one may have p  q and q  p without wanting to
conclude p = q as syntactic objects. The quotient construction makes this explicit by replacing
“pattern identity” with an equivalence class [p] of mutually inter-subpattern patterns, so that the
resulting relation on classes becomes antisymmetric. Concretely, if  is a preorder on patterns and
one defines p ∼ q ⇐⇒ (p  q ∧ q  p), then ∼ captures “indistinguishable for this observer, at
this granularity”; different observers (or the same observer under a different coarse-graining map)
may choose different ∼. One can also read the observer-relative choice of ∼ as specifying which
internal degrees of freedom are treated as gauge: two patterns are identified when they differ only
by transformations that the observer treats as non-informative.

11.5    Heterarchy: multi-path structure and loops
Hyperseed uses “heterarchy” as the opposite of “tree thinking”: multiple distinct paths connect
entities, and the network contains loops. In cognition and society this is typical: concepts mutually
constrain each other, roles interlock, values conflict, and control is distributed. Formally, the point
is not merely that there are many nodes and edges, but that relational structure does not factor
through a single spine: there is generally no privileged unique lineage of explanation, delegation,
or causation. Accordingly, heterarchy is also a warning against forcing a directed acyclic graph
(DAG) model too early: cycles often encode precisely the feedback that makes an organization, a
mind, or a culture self-maintaining.

Definition 135 (Heterarchy). A heterarchy on a set of nodes U is a directed graph (or weighted
digraph)
                                       G = (U, E, w)
with the property that for many pairs (u, v) there exist multiple distinct directed paths from u to
v, and G contains directed cycles. If weights live in a quantale V , we interpret w(u, v) ∈ V as a
graded link strength. In this definition “for many pairs” is intentionally informal: heterarchy is
meant as a structural regime rather than a sharp graph property, and the relevant notion of “many”
is domain- and scale-dependent (e.g. dense conceptual association versus sparse but consequential
institutional channels). When V is a quantale, the intended semantics is that path composition
aggregates along a route via the monoidal product ⊗,Wwhile competing routes can be compared or
pooled using the join structure (often denoted ⊕ or ); the enriched viewpoint below makes this
explicit.


                                                 229
Remark 494 (Intuition, examples, and why the definition is phrased this way). A heterarchy is
a formal acknowledgement that influence is rarely a single chain. In a conceptual network, there
may be several different reasons why u suggests v; in a social network, several institutional routes
by which one role constrains another; in a cognitive architecture, several routes by which perception
and action co-determine each other [19]. Such multiplicity is not noise; it is the medium by which
robustness and conflict coexist (Hyperseed-Concept ??).
    Example: let U be concepts, and put an edge u → v when u reliably predicts v in a dataset;
then loops encode mutually reinforcing concept-clusters. Example: let U be agents/roles in an
organization, and put an edge u → v when u can request actions from v; loops encode delegation and
feedback. The definition is phrased in terms of multiple paths and cycles because these are precisely
the features that distinguish a web from a tree: a tree has unique simple paths and no directed cycles.
A further reason to phrase the definition this way is methodological: in most empirical settings, it
is easier to detect (i) the existence of distinct routes between two points and (ii) the presence of
feedback loops than it is to justify any single total ranking or layered decomposition. Equivalently,
cycles and multi-path connectivity are “witnesses” that no single linear explanation (or command
chain) can be globally valid without loss. In applications one often refines this intuition by analyzing
strongly connected components (SCCs): an SCC is a maximal region of mutual reachability, and the
condensation graph of SCCs is a DAG. From this angle, a heterarchy can be seen as a system whose
dynamics and semantics live primarily inside (possibly large) SCCs, rather than being well-described
by the acyclic skeleton alone.

Remark 495 (Heterarchy as a non-thin enriched category). A hierarchy is “thin”: between any
two nodes there is (at most) one order value. A heterarchy is better modeled as a general (possibly
non-thin) enriched category, where there may be multiple morphisms between u and v representing
different explanatory or causal routes. If one wants to remain in the thin setting, one may col-
lapse multiple routes by taking a join (supremum) over path strengths, yielding a single composite
strength. Both options appear in Hyperseed practice. In the enriched reading, a distinct directed
path is not merely redundant evidence: it can correspond to a different type of entailment (e.g.
statistical association versus mechanistic constraint), a different mediator (institutional channel
A versus channel B), or a different timescale. Keeping multiple morphisms allows one to track
these differences explicitly, while composition encodes how routes concatenate. By contrast, the
thin collapse (taking a supremum over routes) yields a convenient “best available” or “dominant”
linkage, which is often what one wants for scoring, visualization, or approximate reasoning, but it
intentionally forgets the internal pluralism that generated the linkage in the first place.

Definition 136 (Cycle mass (one simple heterarchy index)). Let V = [0, 1] with ⊗ as multiplication
and ⊕ as maximum, and let G = (U, E, w) be a weighted digraph. Define the cycle mass of G by
                                  k
                                 nY                                                            o
                 Cyc(G) := max           w(ui , ui+1 ) : (u1 , . . . , uk ) is a directed cycle ,
                                   i=1

with uk+1 = u1 . Then Cyc(G) > 0 iff G contains a directed cycle with nonzero weight. If G has no
directed cycles, the displayed set is empty; in that case one may take Cyc(G) := 0, consistent with
the stated iff condition and with the intuition that an acyclic digraph has no “returning signal” at
any positive strength.

Remark 496 (Intuition and a toy example). If each edge-weight is read as a multiplicative “rein-
forcement factor,” then the product around a cycle measures how strongly a signal can return to its
starting point after traversing that loop. For a simple 2-cycle u → v → u with weights a and b, the

                                                     230
cycle mass includes the product ab. If either a = 0 or b = 0, the loop is broken; if both are near
1, the loop is strong. The usefulness of this (admittedly toy) index is that it anticipates the later
dynamical claim: habit-taking is autocatalytic and tends to strengthen existing loops (Section 12),
so quantifying “loop strength” matters. One can also view Cyc(G) as a “best feedback gain” under
multiplicative composition: it selects the most self-reinforcing directed cycle, not the average cycle.
This is appropriate when a single dominant feedback loop can govern qualitative behavior (e.g. a
stable institutional feedback channel, or a self-supporting belief cluster), even if many weaker loops
also exist. A mild variant replaces the maximum by another aggregator (e.g. a softmax or a sum
over cycles) when one wants a notion of distributed cyclicity rather than dominance.
Remark 497. The particular definition of Cyc(G) is not canonical; it is only a toy measure. In
later sections, cycles in pattern webs will matter because habit dynamics (Section 12) are auto-
catalytic: they preferentially reinforce existing loops. It is also worth noting that even this toy
measure depends on modeling choices: using multiplication privileges long cycles by accumulating
factors, whereas other semiring/quantale choices (e.g. max–min, or additive log-weights) emphasize
bottlenecks or total gain differently. Thus, Cyc(G) should be read as one concrete instantiation of
a broader idea: heterarchy invites quantitative indices that are sensitive to feedback, and different
indices correspond to different interpretations of what it means for a loop to be “strong” in the
domain at hand.

11.6    Pattern webs from pattern profiles and pattern-based distances
Hyperseed introduces a “pattern web” as a heterarchical structure derived from patterns. One
natural construction is:
1. assign to each entity x ∈ X its fuzzy set of patterns (a pattern profile);
2. define a distance between entities in terms of distances between their pattern profiles;
3. convert the distance into a weighted graph (the pattern web).
We give a general construction that can be instantiated in several ways. In particular, the con-
struction deliberately factors the modeling choices into (i) a pattern vocabulary P, (ii) an intensity
assignment I, (iii) a notion of profile distance D, and (iv) a graph-building rule. This separation is
useful because each component can be varied independently (e.g. refining P without changing the
graph construction rule, or changing D while keeping I fixed), and because it makes explicit where
observer- and task-dependence enters.
Definition 137 (Pattern profile). Let X be a set of entities and P a set of patterns. Assume we
have a pattern-intensity map
                  I : P × X → [0, 1],      I(p, x) = “intensity of pattern p in x”.
For each x ∈ X define its pattern profile (a fuzzy set of patterns)
                                Fx : P → [0, 1],         Fx (p) := I(p, x).
    It is often convenient (though not required) to regard I(p, x) as implicitly relative to a context,
observation process, or modeling interface, so that one could write IC (p, x) when emphasizing
contextual dependence. In this reading, two analysts with different contexts or sensors may induce
different pattern profiles for the “same” underlying x, and hence different pattern webs, without
any contradiction: the web is a structure over the modeled entities as distinguished by the chosen
pattern interface.

                                                   231
Remark 498 (Intuition, example, and why the definition is useful). A pattern profile is simply the
“fingerprint” of an entity in the pattern vocabulary: it tells you which patterns occur in x and with
what strength (Hyperseed-Concept 130). If P is a finite set of candidate regularities, then Fx is a
vector in [0, 1]P .
    Example: suppose P = {pround , pred , pedible } and x is an apple (in some context C). Then
Fx (pround ) ≈ 0.8, Fx (pred ) ≈ 0.6 (green apples exist), Fx (pedible ) ≈ 0.9. The utility is that once
entities are mapped to profiles, we can speak about similarity, clustering, neighborhood, and network
propagation without committing to the raw internal structure of x. This is the formal bridge from
“pattern” to “pattern web” emphasized in [5].
    A further practical advantage is that profiles support partial comparability: two entities can
be compared even when their “internal” representations are heterogeneous, so long as they admit
pattern intensities against a shared P. Conversely, if two domains cannot share a useful P (or
cannot be mapped into it by a meaningful I), then the construction makes clear that the limitation
lies in the pattern interface rather than in the downstream graph machinery.
Remark 499 (Connection to Hyperseed properties). In Hyperseed, the property-set of x is essen-
tially the fuzzy set of patterns in x, with membership degree equal to pattern intensity. Thus Fx can
also be read as a property profile. We keep the term “pattern profile” here to emphasize its role in
constructing higher-order structure.
    In applications, one may additionally include pattern weights to encode salience or reliability
of patterns (e.g. downweighting noisy detectors, or upweighting rare but informative patterns).
Such weights can be folded either into the intensity map I (by rescaling intensities) or into the
subsequent choice of D (by using a weighted distance), and the present definitions accommodate
both approaches.
Definition 138 (Pattern-based pseudo-metric). Fix a metric (or pseudo-metric) D on the space
of fuzzy subsets [0, 1]P . Define
                                  dP (x, y) := D(Fx , Fy ).
We call dP the pattern-based pseudo-metric on X.
    When P is infinite (e.g. a very large or even uncountable pattern family), specifying D typically
entails additional structure (such as a measure on P, a summability condition, or a choice of
feature map into a normed space). For instance, one may replace finite sums by integrals, or
restrict attention to patterns with non-negligible intensity, yielding a well-defined comparison even
when P is conceptually open-ended.
Remark 500 (Intuition and conventions). A pseudo-metric is like a metric except it may assign
distance 0 to distinct points; this matches the idea that two distinct entities might be indistin-
guishable at the pattern-resolution induced by P. The symbol D denotes any chosen distance on
profile space; dP is then the induced distance on entities. This is a clean instance of Hyperseed’s
broader theme: geometry is observer-relative because the chosen distinctions (here, the chosen pat-
tern vocabulary and intensity map) determine which entities are near or far (Hyperseed-Concept
98).
    From a modeling standpoint, allowing dP (x, y) = 0 for x 6= y is often desirable: it expresses
that the pattern vocabulary may be coarse-grained, or that the available evidence cannot separate
the entities. One may then treat the induced equivalence relation x ∼ y ⇐⇒ dP (x, y) = 0 as an
informational quotient, and view the pattern web as operating on equivalence classes at the chosen
pattern-resolution.

                                                  232
Example 11 (Finite-pattern `1 distance). If P is finite, we may define
                                            X
                               D(F, G) :=       F (p) − G(p) .
                                                p∈P

Then dP (x, y) is the total absolute difference in pattern intensities across the pattern vocabulary.

   A common variant is a weighted `1 distance,
                                          X
                            Dw (F, G) :=     w(p) F (p) − G(p) ,
                                              p∈P

where w(p) ≥ 0 encodes the relative importance, confidence, or discriminative value of pattern p.
This makes explicit that the induced geometry can prioritize certain pattern dimensions without
altering the underlying profile representation.

Remark 501 (A second simple example). Another common choice (when P is finite) is the `2
                     P                       1/2
distance D(F, G) :=           (F (p) − G(p))2      , which penalizes large deviations more strongly.
                          p∈P
The formalism does not privilege either; it only insists that whatever notion of similarity one uses
should be made explicit as a D.

    Depending on the application, one might prefer distances that compare profiles up to overall
“mass” or scale. For example, cosine distance (derived from cosine similarity) emphasizes angular
agreement between vectors and can be useful when absolute intensity magnitudes are less mean-
ingful than relative pattern mixtures. Likewise, one can normalize profiles (e.g. by `1 or `2 norm
when appropriate) prior to computing D, thereby distinguishing “composition” from “quantity” of
pattern evidence.

Remark 502 (Hutchinson-style choices). Hyperseed mentions using standard metrics (such as the
Hutchinson metric) to compare fuzzy pattern-sets. The present formalism isolates the key idea:
any reasonable choice of D yields a pattern-based geometry on X. The specific choice of metric is
application-dependent.

    In the same spirit, if patterns carry an internal geometry or ground space (e.g. patterns are
distributions over some base domain, or are themselves structured objects), then D can be chosen
to respect that structure (e.g. optimal-transport-type distances, kernel-induced distances, or other
task-aligned divergences). The point is not to mandate a particular metric family, but to make the
dependency of the resulting web on the comparison principle explicit and inspectable.

Definition 139 (From distance to a weighted pattern web). Fix a monotone decreasing kernel
κ : [0, ∞) → [0, 1]. Define a similarity weight
                                                              
                                        s(x, y) := κ dP (x, y) .

A pattern web on X is a weighted (undirected or directed) graph

                                         W = (X, EW , wW )

constructed from s(x, y), for example by:

• threshold graph: include edge (x, y) iff s(x, y) ≥ τ ;


                                                    233
• k-NN graph: connect each x to its k nearest neighbors under dP ;

• full graph: take EW = X × X with weights wW (x, y) = s(x, y).

    If a directed web is desired, one can obtain directionality either by using an inherently asym-
metric comparison (e.g. a divergence-like D on profiles, or an inclusion/entailment score between
fuzzy sets) or by using an asymmetric graph construction rule (e.g. k-NN edges x → y when y
is among the k nearest to x). Even when D is symmetric, k-NN graphs are typically directed
unless symmetrized (e.g. by mutual k-NN), and this choice affects the reachability and propagation
properties of the resulting pattern web.

Remark 503 (Intuition, examples, and necessity). This definition performs a familiar maneuver:
convert distance (“far means unrelated”) into similarity (“near means connected”). The kernel κ
is monotone decreasing so that larger distances yield smaller similarities. Example: κ(t) = e−λt (a
Gaussian-like choice) makes similarity decay exponentially with distance.
    Why is this useful? Because a graph is the natural substrate for heterarchical reasoning: once
we have edges, we can talk about multi-step paths, loops, and propagation of support (Hyperseed-
Concept 132). In cognitive terms, the pattern web is the externalized form of the judgment “these
things share patterns and thus should inform each other,” as in earlier Hyperseed discussions [1, 5].

    The kernel scale (e.g. λ above, or an analogous bandwidth) plays the role of a resolution pa-
rameter: small changes in bandwidth can turn a sparse web into a dense one, changing the balance
between local neighborhoods and long-range connections. Similarly, the choice between thresh-
olding, k-NN, and full graphs reflects a trade-off between interpretability and computational cost:
thresholding yields explicit “strong ties,” k-NN yields bounded degree (often beneficial for scalabil-
ity), and the full graph preserves all graded similarities but may be impractical for large X. These
are not merely engineering details; they influence which heterarchical pathways exist for multi-step
association and which loops can form in the induced structure.

Remark 504 (Pattern web as an enriched space). There are two closely related enriched-category
readings:

• Metric enrichment: (X, dP ) is a Lawvere metric space, i.e. a category enriched in the quantale
  ([0, ∞], ≥, +, 0).

• Similarity enrichment: (X, wW ) is a [0, 1]-enriched (or V -enriched) graph/category, where com-
  position along paths multiplies similarities and joins over alternative paths.

Both are useful. Metric enrichment emphasizes geometry and neighborhood structure; similarity
enrichment emphasizes propagation of support along multiple routes. The formal core (Section 3)
was designed to support either viewpoint.

11.7    Pattern webs as free V -categories
Given a weighted directed graph of patterns or entities, there is a standard way to “close” it under
compositional reasoning. This is exactly the enriched-category analogue of taking the transitive
closure of a relation.

Definition 140 (Path composition in a V -graph). Let V be a commutative quantale. A V -graph
is a set U with a weight function
                                      g : U × U → V.


                                                 234
For a directed path π = (u0 → u1 → · · · → un ) define its path weight

                           w(π) := g(u0 , u1 ) ⊗ g(u1 , u2 ) ⊗ · · · ⊗ g(un−1 , un ).

Define the path-closure hom                              M
                                           gb(u, v) :=           w(π),
                                                         π:u v

where the join ranges over all finite directed paths from u to v (including the empty path).

Remark 505 (Notation unpacking and intuition). The symbol π : u             v denotes a directed path
starting at u and ending at v. The “empty path” is the path of length 0 from u to itself; by convention
its weight is e (the unit of ⊗). Thus gb(u, v) aggregates evidence/support from all routes from u to
v by:

• composing along a fixed route using ⊗ (sequential aggregation), and

• taking the join ⊕ over alternative routes (parallel aggregation).

In the Boolean case this is exactly transitive closure: gb(u, v) = 1 iff there exists a path from u to v.
In a graded case, it becomes “best-path” (or “best-aggregate”) closure, depending on the quantale
operations.

Remark 506 (A tiny example). Let U = {a, b, c} and suppose g(a, b) = 0.9, g(b, c) = 0.8, g(a, c) =
0.1 in V = [0, 1] with ⊗ = × and ⊕ = max. Then the path a → b → c has weight 0.72, so
gb(a, c) = max(0.1, 0.72) = 0.72. This captures the heterarchical idea that an indirect route can
dominate a direct (but weak) link.

Theorem 11 (Free V -category on a V -graph). Let V be a commutative quantale and (U, g) a
V -graph. Define gb by path-closure as above, taking the empty path to have weight e. Then gb defines
a V -enriched category on object set U . In particular:

• (identity) e ≤ gb(u, u) for all u;

• (composition) gb(u, v) ⊗ gb(v, w) ≤ gb(u, w) for all u, v, w.

Remark 507 (What the theorem says in plain language). Starting from a weighted directed graph,
the theorem constructs the “best available” composite connection between any two nodes by looking
at all finite paths and aggregating their weights. It then asserts that these composite connections
automatically satisfy the axioms of a V -enriched category: there are identities (the empty paths),
and composing a u → v connection with a v → w connection yields a valid u → w connection. So,
path closure is not an ad hoc trick; it is the canonical completion of a graph into a compositional
reasoning structure.

Remark 508 (Why it matters here). This result is the formal hinge between “web” as a static
picture and “web” as an inferential substrate. In a pattern web, one typically wants to propagate
support (or inhibition, or relevance) along multi-step routes. The theorem guarantees that once
we pick a quantale V describing how supports combine, the propagation algebra is coherent by
construction. This coherence is exactly what later habit dynamics exploit: repeated updating tends
to amplify already-available composite routes (Section 12).




                                                     235
Proof. Identity holds because the empty path from u to u is included and has weight e, hence
e ≤ gb(u, u).
   For composition, fix u, v, w. A path from u to w can be formed by concatenating a path
π1 : u      v and a path π2 : v     w. The weight of the concatenated path is w(π1 ) ⊗ w(π2 ) by
associativity of ⊗. Thus, for each pair of paths (π1 , π2 ) we have

                                         w(π1 ) ⊗ w(π2 ) ≤ gb(u, w),

because gb(u, w) is the join over all u     w paths. Taking joins over all π1 and π2 and using
distributivity of ⊗ over joins gives
                             M              M           
                                     w(π1 ) ⊗        w(π2 ) ≤ gb(u, w).
                               π1 :u v             π2 :v   w

The left-hand side is gb(u, v) ⊗ gb(v, w).

Remark 509 (Proof sketch and key-step commentary). Proof sketch. The strategy is to show that
the empty path supplies identities, and that concatenating paths supplies composition. Since gb(u, w)
is defined as a join over all u      w paths, every particular concatenated path contributes a lower
bound, and distributivity lets us lift from particular paths to joins over all paths.               
     The heart of the argument is the monotonicity encoded by joins: if a value is among the terms
joined to make gb(u, w), then it is ≤ gb(u, w). Concatenation produces the relevant term, and dis-
tributivity is what permits “join of left paths” ⊗ “join of right paths” to be bounded by the “join of
all concatenations.” Visually, one can imagine all paths as threads in a fabric: gb(u, v) summarizes
all threads from u to v, and composition corresponds to splicing threads at v to create longer threads
from u to w.

Remark 510 (Interpretation). If g(u, v) encodes “u supports/predicts/constructs v”, then gb(u, v)
encodes overall support aggregated across all pathways. This is the mathematical backbone of the
“web” picture: multi-path reinforcement is represented by the join over paths. If V is p-bit-valued,
then the same construction supports paraconsistent webs in which multiple routes can provide both
support and counter-support. In particular, when V is a join-semilattice (or more generally a
quantale), the hat-construction gb can be read as a kind of transitive closure: it aggregates not only
direct edges u → v but also indirect chains u → · · · → v by composing along the chain and then
taking the join over all chains. Thus gb(u, v) measures the best (or most permissive, depending
on V ) composite evidence that v is reachable from u through the pattern web. When V = p-bit,
the aggregation by joins can simultaneously retain distinct “positive” and “negative” contributions:
different paths can witness different polarities without forcing collapse to a single consistent truth
value. This is precisely the sense in which the same path-join formalism can model webs that are
tolerant of contradiction: the global value gb(u, v) records what the web as a whole supports, rather
than demanding that all routes agree.

11.8    Multi-resolution transforms and weakness
Hierarchies are often produced by abstraction: collapsing distinctions and bundling lower-level
details into higher-level summaries. Pattern webs, likewise, are usually considered at multiple
resolutions. We express this using maps (functors) between pattern spaces. At an informal level,
the point is that the same underlying system can be described by many different “alphabets”:
a fine alphabet with many entity- and pattern-types, and a coarse alphabet in which many fine
types are identified. The usefulness of a multi-resolution formalism is that it allows one to compare

                                                    236
statements made at different descriptive granularities while keeping track of which claims survive
abstraction and which are artifacts of fine detail.

Definition 141 (Resolution maps on entities and patterns). Let X be an entity set and P a pattern
vocabulary. A resolution change from a fine description to a coarse one consists of:

• a surjective map α : X → X 0 (coarse-graining of entities);

• a map β : P → P 0 (coarse-graining of patterns);

• a rule for pushing forward intensities I(p, x) to I 0 (p0 , x0 ).

A simple pushforward rule is

                            I 0 (p0 , x0 ) := sup{I(p, x) : β(p) = p0 , α(x) = x0 }.

Remark 511 (Intuition and example). Coarse-graining is the formal act of deciding that many
differences do not matter for the present purpose. The maps α and β implement this decision on
entities and patterns, respectively. Example: X might be images, X 0 might be object-categories; α
maps an image to its category label. Similarly, P might contain fine-grained visual motifs while P 0
contains coarser semantic patterns.
    The pushforward rule via sup says: a coarse pattern p0 holds of a coarse entity x0 if any of
its fine refinements held strongly in any representative fine entity mapping to x0 . This matches
one common cognitive stance: a coarse label is licensed by the strongest supporting instance. The
definition matters because multi-resolution comparison is ubiquitous in transfer and abstraction
workflows; it is also a bridge to later frameworks emphasizing structured transfer and abstraction
[7]. One can also read the sup rule as a left Kan extension–style “best upper approximation” of
the fine intensity profile by a coarse one: the coarse description is the least committal (largest)
assignment consistent with the existence of a supporting witness downstairs. In settings where
intensities live in an ordered domain (e.g. [0, 1], a Boolean algebra, or p-bit), the use of sup ensures
that I 0 is monotone with respect to adding more fine-grained evidence: enlarging the set of fine
representatives for a given (p0 , x0 ) can only increase (never decrease) the pushed-forward intensity.
Surjectivity of α is a convenient way to insist that every coarse entity x0 ∈ X 0 corresponds to at
least one fine representative; if α were not surjective, then some coarse entities would be “empty
bins,” and one would need a convention for the sup over an empty set (often the bottom element
of V ).

Remark 512. The pushforward rule above is “optimistic”: it preserves any strong evidence that
a coarse pattern holds of a coarse entity. Other rules (averaging, expectation, evidence-weighted
pooling) may be more appropriate in specific domains. The key point is that coarse-graining can be
treated as a monotone operator on pattern profiles. In particular, if I ≤ J pointwise (every fine
intensity in I is bounded by the corresponding one in J), then the induced coarse profiles satisfy
I 0 ≤ J 0 under the sup rule, since sup is monotone in its arguments. This monotonicity is what
makes multi-resolution moves compatible with order-enriched viewpoints: resolution change is not
merely a lossy projection, but a structured map that respects the underlying preorder of evidential
strength.

Proposition 16 (Coarse-graining is monotone and increases weakness). Assume an observer’s
indistinction relation H ⊆ X×X is pushed forward along α to an indistinction relation H 0 ⊆ X 0 ×X 0
by declaring
                             (α(x), α(y)) ∈ H 0 whenever (x, y) ∈ H.

                                                     237
Then H 0 collapses at least as many distinctions as H. In particular, for any monotone weakness
functional w(·) (Section 3.7),
                                         w(H) ≤ w(H 0 ).

Remark 513 (Plain-English meaning and connection to earlier results). The proposition says:
when you merge fine entities into coarse ones, you cannot create new distinctions; you only lose
them. Therefore any sensible measure of “weakness” (in Hyperseed’s technical sense: degree of
collapsed distinction-making power) can only increase. This connects directly to the monotonicity
theorem for weakness (Theorem 1) and provides a small formal justification for the intuitive idea
that abstraction trades detail for simplicity [3, 2] (Hyperseed-Concept 202). Equivalently, passing
from H to H 0 is an order-preserving move in the lattice of indistinction relations: H 0 contains at
least the images of the indistinguishabilities already present in H, and so represents an observer who
is (at best) as discriminating as before. If H were an equivalence relation capturing exact perceptual
indistinguishability, then the pushforward along α can be seen as inducing a coarser equivalence on
X 0 ; the proposition is then the familiar idea that quotienting (or identifying states) cannot increase
information.

Proof. Every indistinction asserted by H induces an indistinction asserted by H 0 . Thus the set
of undistinguished (coarse) pairs contains the image of the set of undistinguished (fine) pairs.
Monotonicity of weakness under adding undistinguished pairs (Theorem 1) yields w(H) ≤ w(H 0 ).
More explicitly: if (x, y) ∈ H, then by definition (α(x), α(y)) ∈ H 0 , so {(α(x), α(y)) : (x, y) ∈
H} ⊆ H 0 . Hence H 0 is at least as permissive an indistinction relation on the space of coarse entities
as the one induced from H, and any weakness functional that is monotone under enlarging the
indistinction set must satisfy the stated inequality.

Remark 514 (Proof sketch and intuition). Proof sketch. Pushforward along α maps each “confused
pair” in X to a “confused pair” in X 0 . So the coarse observer cannot distinguish at least the pairs
the fine observer could not. Then apply monotonicity of w.                                           
    The key step is the containment claim: H’s indistinction assertions survive (as images) in H 0 .
Geometrically, one can think of α as collapsing points into blobs; any pair of points that were already
indistinguishable lie in blobs that are indistinguishable in the quotient. The inequality w(H) ≤
w(H 0 ) is then the numeric shadow of this collapsing. Another way to visualize the same argument
is via fibers of α: each coarse point x0 ∈ X 0 represents a fiber α−1 (x0 ) ⊆ X. Indistinguishability
at the fine level propagates to indistinguishability between fibers at the coarse level, so the coarse
description inherits all the “blind spots” of the fine one and may add new ones due to fiber-merging.

Remark 515 (Why this belongs in the hierarchy section). A hierarchy is often the result of
a multi-resolution move: the “higher” nodes are coarse summaries that ignore fine distinctions.
The proposition formalizes the directionality: moving upward in an abstraction hierarchy typically
increases weakness (simplicity) while reducing detail. Later, wu-wei style dynamics (Section 26)
will treat “acting with minimal forcing” as moving along flows that are biased toward such weak
(simple) representations [21]. In this sense, the same formal move (pushing forward along α)
explains two commonplace observations about hierarchies: (i) higher levels are cheaper to reason
about because they track fewer distinctions, and (ii) higher levels may be more robust because they do
not depend on unstable fine-grained differences. The weakness increase inequality gives a compact
way to state that these benefits come with an intrinsic limitation: any decision rule that relies on
fine discriminations must be expected to degrade under repeated coarse-graining.




                                                  238
11.9    Section wrap-up
This section reconstructed four Hyperseed notions in a uniform mathematical language:

• Hierarchy/systemic hierarchy as observer-indexed (graded) order, often model-induced. In partic-
  ular, the “grade” can be read as an explicit resource parameter (e.g. resolution, budget, attention,
  or tolerance) that determines which distinctions are available, so that what counts as “above”
  or “below” is not absolute but arises from a chosen standpoint. The phrase “model-induced”
  emphasizes that the ordering is frequently an artifact of a representation scheme: change the
  features, the abstraction map, or the inference rule, and the resulting order can refine, coarsen,
  or even reorder comparisons.

• Subpattern hierarchy as the preorder generated by compositional subpattern relationships. Here
  “generated” signals a closure process: one starts from primitive subpattern links (e.g. “appears
  as a component of,” “factors through,” “can be assembled into”), and then takes the smallest
  reflexive and transitive relation containing them. The fact that the result is a preorder (rather
  than necessarily a partial order) is conceptually important: different construction paths can yield
  mutual reachability without forcing equality, capturing the idea that two patterns may embed
  into one another under composition while remaining distinct as descriptions or mechanisms.

• Heterarchy as multi-path, loop-rich network structure. The emphasis on multiple paths encodes
  the coexistence of alternative explanations, realizations, or routes of influence; the emphasis on
  loops encodes feedback, mutual reinforcement, and circular dependence. In this view, “non-
  tree-like” is not merely a combinatorial complication but a signal that comparative relations are
  context-sensitive and can be revisited: traversing a loop can accumulate costs, change effective
  granularity, or expose tensions between competing constraints.

• Pattern web as a heterarchy derived from the geometry of pattern profiles. Geometric language
  is meant literally: patterns are represented by profiles (e.g. vectors, distributions, or enriched
  morphisms) whose relative position determines adjacency, similarity, and feasible transitions
  under bounded resources. The resulting web is therefore not an arbitrary graph but one induced
  by a metric-, order-, or quantale-enriched notion of distance/effort, so edges and path weights
  reflect how distinctions deform under abstraction, noise, or compression.

Read together, these four reconstructions explain how seemingly different vocabularies—rank, in-
clusion, feedback, and profile geometry—can be treated as different presentations of the same un-
derlying compositional machinery. In particular, the shift from “hierarchy” to “web” is not a change
of topic but a change of emphasis: from single-chain comparability to the coexistence of many com-
patible (and incompatible) comparison pathways, with explicit accounting of the resources required
to traverse them.

Remark 516. The unifying thread is compositionality: in hierarchies, comparisons compose; in
webs, paths compose; in multi-resolution transforms, abstraction composes with indistinction and
thereby reshapes weakness. Once these are all placed within the same quantale-enriched idiom, it
becomes easier to see why Hyperseed can move fluidly between “order” talk and “network” talk
without changing subject: both are presentations of structured distinction-making under resource
bounds. Concretely, enrichment supplies a common semantics for “how much” (cost, effort, or
uncertainty) accompanies a comparison or transition: composing comparisons adds/aggregates that
quantity, while taking meets/joins expresses the presence of multiple competing routes. In this
sense, hierarchy is the special case where the web of comparisons is sufficiently rigid (or sufficiently


                                                  239
observed through a single grading) that it behaves like an ordered scaffold, whereas heterarchy is the
generic case in which composition exposes parallelism, feedback, and nontrivial trade-offs between
pathways.
    The next section (Section 12) adds time and dynamics: it studies how webs reinforce themselves
into habits, how they sometimes reverse, and how morphic resonance couples habit dynamics across
contexts. From the perspective of the present section, this amounts to endowing the pattern web
with update rules that change edge strengths, accessibility, or effective grades as interactions repeat.
The same compositional principles then reappear in temporal form: repeated traversals compose
into long-run tendencies, loops become attractors or oscillations, and the resource bounds that
shaped static comparison now shape learning rates, persistence, and the conditions under which a
previously weak distinction can become stable.


12     Habits, self-weaving webs, and morphic resonance
This section reconstructs the Hyperseed dynamical cluster tendency to take habits (Hyperseed-
Concept 189), tendency to reverse habits (Hyperseed-Concept 188), self-weaving webs (Hyperseed-
Concept 168), and morphic resonance/anti-resonance (Hyperseed-Concept 115, Hyperseed-Concept
114) using the minimal formal core (Section 3) and the pattern-web machinery (Sections 11–9).
For the broader Hyperseed framing of these notions, see [1].
     The key modeling move is to treat a pattern web (Hyperseed-Concept 132) as a V -valued directed
graph (equivalently, a V -relation) whose edges encode reinforcement or “flow” of pattern support,
and to treat habit formation as a family of order-theoretic update operators on V -valued pattern-
support states. Morphic resonance is then a cross-context coupling of these same dynamics, in a
way philosophically reminiscent of “habit” as a cosmological tendency in Peirce and process-like
propagation in Whitehead [14, 15]. In more concrete terms, one may think of a pattern web as
a weighted adjacency structure on a set of pattern-indices, where the weight on an arrow p → q
summarizes “how much” support for p tends to induce, propagate, or transform into support for
q. The choice of a quantale V allows these weights and supports to be more expressive than
ordinary real-valued probabilities: in particular, V can encode graded truth, graded evidence,
multi-aspect valuation, or even paraconsistent combinations of support and counter-support, while
still providing a disciplined algebra (join, multiplication, order) for composing influences along
paths and aggregating multiple sources of reinforcement.
     A central theme in what follows is that the above informal notions can be separated into two
interacting ingredients: (i) a structural ingredient, namely the pattern web itself as a V -relation
capturing potential channels of influence; and (ii) a dynamical ingredient, namely the operators that
update pattern-support states in response to that structure (and to possible external inputs). The
“tendency to take habits” will be modeled by update maps that, in a precise order-theoretic sense,
consolidate and amplify frequently traversed channels of support, so that repeated activation makes
certain state configurations easier to re-enter. The “tendency to reverse habits” will be modeled
by companion updates that weaken, invert, or otherwise reorganize these consolidations under
suitable triggers, so that entrenched trajectories can become unstable and alternative trajectories
can become accessible. The concept of “self-weaving webs” will be treated as the case where
the web is not fixed in advance but is itself an evolving object influenced by the very states whose
propagation it shapes, yielding a feedback loop between representation (edges) and activity (support
values).
Remark 517 (Notation and reading conventions for this section). We will repeatedly use function
spaces of the form V P , meaning the set of all functions s : P → V (pattern-support states). When

                                                  240
we write inequalities such as s ≤ s0 for s, s0 ∈ V P , this is always the pointwise order: s ≤ s0 iff
s(p) ≤ s0 (p) for all p ∈ P . Similarly, when we write ⊕ between two states (or two inputs) we mean
the pointwise join induced by the quantale join in V . It is often useful to keep in mind the two
complementary readings of the pointwise order: s ≤ s0 can mean that s0 contains at least as much
support as s for every pattern, but it can also be read operationally as “s0 is reachable from s by
adding support and never removing it” (relative to the chosen order on V ). This second reading is
especially convenient when we treat habit-formation operators as inflationary or extensive maps on
V P , since then s ≤ H(s) expresses that an update H can only accrete (or at least not diminish)
support, thereby formalizing a minimal sense in which repeated application stabilizes configurations.
   Throughout this section:
• V denotes a commutative quantale. For the concrete toy instantiations we use the p-bit quantale
  from Section 3.4. In particular, the commutativity assumption ensures that the “combination”
  of independent support flows (encoded via the quantale multiplication) does not depend on an
  arbitrary ordering of factors, which matches the intuition that multiple reinforcing sources can
  be fused without privileging a sequence.
• A pattern class is a set P of pattern-indices (abstract “pattern types”). In applied settings
  P can be a finite or countable subset of the space of candidate patterns from Section 9 (see
  also the pattern-web discussion in [5]). The abstraction here is deliberate: we only require that
  elements of P can be used as coordinates for states and as nodes in a directed V -graph, without
  committing to whether a “pattern” is a perceptual feature, a symbolic structure, a program, a
  hypothesis, a dynamical attractor, or some hybrid object.
• A pattern-support state is a function s : P → V assigning each pattern a graded (possibly
  paraconsistent) support value. In this formalism, a single state s may simultaneously encode
  multiple interacting kinds of information (e.g. evidence-for and evidence-against, or different
  modalities of support) as long as these are represented in the chosen quantale; the ensuing
  update dynamics then become a principled way of turning the “static” valuations in s into a
  time-evolving propagation process along the edges of the web.
     The rest of the section will repeatedly move between three closely related objects: (i) a V -
relation on P (the web), (ii) a state s ∈ V P (the current distribution of support over patterns), and
(iii) a state transformer H : V P → V P (a habit operator). One reason for emphasizing this triad is
that each of the Hyperseed notions under discussion can be cast as a constraint on, or a construction
from, one of these objects: habit-taking concerns the algebraic and order-theoretic properties of
H; self-weaving concerns rules for updating the underlying V -relation using s (and possibly also
H); and morphic resonance concerns how multiple such triples (P, V, web) interact via coupling
maps that transfer support across contexts. When we later speak of “reinforcement” or “anti-
reinforcement,” the formal interpretation will be that the relevant update either increases support
along certain channels (via joins and multiplicative composition in V ) or decreases it relative to
other channels (e.g. by redirecting flow, introducing inhibitory edges, or applying an antagonistic
coupling), always in a way that can be stated in the language of monotone maps, adjunctions,
closure-like operators, or their duals.

12.1    From Hyperseed’s probability phrasing to V -valued dynamics
Hyperseed’s informal definitions of habit-taking and habit-reversal are stated in terms of probabil-
ities of patterns occurring before versus after times T . To connect this to the paraconsistent core
we separate two issues:

                                                 241
1. how to represent “pattern occurs” in a paraconsistent way; and

2. how to extract a scalar “occurrence propensity” from that representation when needed.

Definition 142 (p-bit occurrence evidence and scalarization). Assume the p-bit semantics of Sec-
tion 3.2. A pattern-support value is s(p) = (s+ (p), s− (p)) ∈ [0, 1]2 , where s+ (p) is positive evidence
for “p occurs” and s− (p) is negative evidence.
    A scalarization is a function π : V → [0, 1] used when we want a single number comparable
across time. For the p-bit quantale we will use one of:

                      πpos (v + , v − ) = v + ,          πnet (v + , v − ) = max(0, v + − v − ).

Remark 518 (Intuition: two-channel evidence and why scalarization is optional). A p-bit value
(v + , v − ) should be read as a compact record of two distinct pressures: how much the context is being
pushed to affirm occurrence, and how much it is being pushed to deny it. This is the paraconsistent
posture: we do not demand that the world (or the observer’s record of it) collapse into a single
consistent bit. One may view this as a formal version of the practical epistemic condition “I have
reasons for and against,” without forcing premature reconciliation (cf. the paraconsistent perspective
developed in Section 3 and related work such as [23, 24]).
     Scalarization π is then a choice of lens. For example, if s(p) = (0.7, 0.6) then πpos (s(p)) = 0.7
declares “there is strong positive pull,” whereas πnet (s(p)) = 0.1 declares “net inclination is weak
because conflict is strong.” Neither is “the truth”; each is a deliberately chosen compression of a
richer state, useful for connecting to probability-style statements about averages over time.

Remark 519. πpos matches the simplest reading of Hyperseed’s “probability of occurrence.” πnet
treats strong contradictory evidence as reducing effective occurrence propensity, which is often con-
venient when modeling anti-resonance or habit reversal as “net suppression.”

Definition 143 (Observer-indexed occurrence process). Fix a context/observer C and a pattern
class P . A (discrete-time) occurrence process in C is a sequence

                                      s0 , s1 , s2 , . . .   with     st : P → V.

Given a scalarization π, define the scalar occurrence propensity

                                            pt (p) := π(st (p)) ∈ [0, 1].

Remark 520 (Intuition and a minimal example). The sequence (st )t≥0 is simply “how supported
is each pattern, at each time, in this context?” For P = {p} a singleton, this reduces to a one-
                                                                                                 −
dimensional time series in V ; in the p-bit case, it is two coupled scalar time series (s+
                                                                                         t (p), st (p)).
                                                  +       −
For instance, repeated exposure might drive (st (p), st (p)) upward in the first coordinate while
leaving the second roughly constant, reflecting growing positive evidence without resolving doubt.
    The value of formalizing this as a function st : P → V is that we can later propagate support
through a web (via a V -relation) and reason about global properties like monotonicity and fixed
points using order theory, rather than relying on ad hoc verbal metaphors.

Definition 144 (Tendency to take habits and tendency to reverse habits). Fix a distribution ν
over a class P of patterns, a distribution τ over times T ∈ {0, 1, 2, . . . }, and a scalarization π.
Define, for each p ∈ P and time T ,

                   PreT (p) := E[ pt (p) | t < T ],                PostT (p) := E[ pt (p) | t > T ],

                                                             242
whenever these conditional expectations are defined.
   The context C manifests the tendency to take habits (relative to (P, ν, τ, π)) if
                                                             
                               Ep∼ν, T ∼τ PostT (p) − PreT (p) > 0.

It manifests the tendency to reverse habits if the above expectation is < 0.

Remark 521 (Intuition and why the quantifiers matter). The quantities PreT (p) and PostT (p)
compare average propensities before and after a sampled “cut” time T . The outer expectation over
p ∼ ν and T ∼ τ makes the definition intentionally meta-statistical: one is not declaring that every
pattern increases, but that there is a systematic bias in the time direction on average, relative to a
chosen ensemble of patterns and time windows.
    A simple example is the following. Suppose P is finite and for each p ∈ P the scalar propensity
is pt (p) = min(1, ap + bt) with b > 0. Then for any reasonable τ the average after T will exceed
the average before T , yielding habit-taking. Conversely, exponential forgetting pt (p) = cp λt with
0 < λ < 1 yields habit-reversal.

Remark 522. Definition 144 is intentionally “meta-statistical”: it measures a bias in time-
directional change averaged over a chosen pattern class and time sampling scheme. This matches
Hyperseed’s wording (“on average over patterns P in class C, and times T ”) while making the
indexing explicit.

Lemma 3 (Monotone time series imply habit-taking; antitone imply reversal). Assume pt (p) is
nondecreasing in t for every p ∈ P . Then for every T and p for which the conditional expectations
exist,
                                       PostT (p) ≥ PreT (p).
Consequently, the tendency-to-take-habits expectation in Definition 144 is ≥ 0.
    If instead pt (p) is nonincreasing in t for every p ∈ P , then PostT (p) ≤ PreT (p) and the tendency-
to-reverse-habits expectation is ≤ 0.

Remark 523 (What the lemma is saying, in plain terms). If every pattern’s scalar propensity is
drifting upward over time, then the “after” average cannot be below the “before” average: the future
is at least as supportive as the past, in this coarse statistical sense. Likewise, if everything drifts
downward, then the future is (on average) less supportive. The lemma is not deep; its importance
is methodological: it reduces a philosophical notion (habit-taking as a time-asymmetric tendency)
to a verifiable monotonicity property of the time-indexed propensities.

Remark 524 (How this connects forward). Later in this section we will define concrete update op-
erators st+1 = Upd(st ). Proposition 17 will show these operators are monotone (order-preserving),
and in inflationary regimes the induced scalarized series pt (p) often becomes monotone as well,
giving an immediate bridge from dynamics to the habit-taking criterion of Definition 144.

Remark 525 (On the role of conditional expectations). The lemma is phrased pointwise in (T, p):
whenever PreT (p) and PostT (p) are defined (as conditional expectations over the “before” and “af-
ter” portions of the time axis, conditioned on the cut time T and the pattern p), the stated inequality
holds. In particular, no distributional assumptions are needed beyond existence: neither station-
arity nor independence of the time series is invoked, and the inequality is not an “in expectation”
statement but an inequality between two conditional averages computed from the same underlying
monotone sequence. This is why the conclusion survives the subsequent outer averaging over (T, p)
in Definition 144: the sign is already determined at the conditional level.

                                                  243
Remark 526 (Finite-window intuition as a special case). Although PreT (p) and PostT (p) may
be defined via semi-infinite averages (or other conditional averages, depending on the model), the
lemma is already evident in the finite-window case: if one defines, for integers m, n ≥ 1,
                                     T −1                                   T +n−1
                                   1 X                                    1 X
                    PreT,m (p) =          pt (p),         PostT,n (p) =            pt (p),
                                   m                                      n
                                     t=T −m                                  t=T

then monotonicity implies every term in the right block dominates every term in the left block, hence
PostT,n (p) ≥ PreT,m (p). Any limiting or conditional-expectation definition of PreT (p) and PostT (p)
that is compatible with such windowed approximations inherits the same inequality whenever the
limits exist.
Proof. If a sequence is nondecreasing, then the average of its terms after T is at least the average
of its terms before T (whenever these averages exist). Apply this pointwise to each pattern p, then
average over p and T . The nonincreasing case is analogous.
    For completeness, one can spell out the elementary comparison in the common case of block
averages: if a0 ≤ a1 ≤ a2 ≤ · · · , then for any indices i < j we have ai ≤ aj . Hence if I is any finite
set of indices all < T and J is any finite set of indices all ≥ T , then
                                          1 X           1 X
                                                at ≤           at ,
                                         |I|           |J|
                                              t∈I           t∈J

since every term in the left sum is bounded above by every term in the right sum. Taking at := pt (p)
gives Pre ≤ Post for these approximating averages; passing to the chosen conditional-expectation
notion yields PreT (p) ≤ PostT (p) whenever the conditional expectations exist.

Proof sketch. The proof uses only the elementary fact that if a0 ≤ a1 ≤ a2 ≤ · · · , then any
average of later terms is at least any average of earlier terms, because later terms dominate earlier
ones pointwise. We apply this to each pattern’s propensity series pt (p) and then use linearity of
expectation to lift the inequality through the outer averaging over p and T .
   Equivalently, one may view PreT (p) and PostT (p) as two Cesàro-type functionals applied to
the left and right tails of the same monotone sequence. Monotonicity forces the right tail to lie
above the left tail, and any averaging functional that is monotone with respect to pointwise order
preserves this comparison.                                                                         
Remark 527 (Commentary and intuition). One may picture the propensity sequence for a fixed p
as a curve on the unit interval. If the curve never goes down, then any horizontal “cut” at time
T separates smaller values (to the left) from larger values (to the right), so the right-side mean
dominates the left-side mean. The lemma is thus a formal version of a simple geometric picture:
monotone curves have a built-in temporal bias.
Remark 528 (When the inequality is strict (and when it is not)). The lemma only asserts a weak
inequality because constant stretches carry no directional information. If pt (p) is strictly increasing
on a set of times with nonzero weight in the definition of PreT (p) and PostT (p) (for example, if
there exist indices t < T ≤ t0 with pt (p) < pt0 (p) that are sampled with positive probability), then
typically one obtains PostT (p) > PreT (p). Conversely, if the series is eventually constant (or if
T is chosen so that both “before” and “after” averages sample only a flat region), then equality is
expected and corresponds to a neutral “no-habit-signal” situation under the tendency statistic.
   Lemma 3 reduces the Hyperseed habit notions to verifiable monotonicity properties of a dy-
namical update rule. We now provide such update rules.

                                                    244
12.2    Pattern webs as V -relations and habit update operators
Definition 145 (V -valued reinforcement relation (pattern-flow kernel)). Let P be a pattern class.
A reinforcement relation (or pattern-flow kernel) on P is a V -valued relation

                                          A : P × P → V.

Intuitively, A(p, q) measures how strongly the presence of pattern p tends to increase the support
for pattern q at the next time step, within a given context.

Remark 529 (Intuition: a weighted directed graph of support flow). Think of P as nodes in a
directed graph. Then A(p, q) is the weight on the arrow p → q, but with weights living in a quantale
V rather than in R. In the p-bit toy case, A(p, q) = (0.9, 0.1) might be read as: “when p is present,
it provides strong positive pressure toward q, and slight negative pressure against q as well.” That
is: causal/associative support is itself permitted to be ambivalent.
    This is useful because it lets us treat pattern webs (Hyperseed-Concept 132) as algebraic objects
whose propagation can be computed and iterated, connecting the informal “web” metaphor to explicit
operators (compare the broader pattern-network picture in [5]).

Remark 530 (Categorical reading: A as a V -relation in RelV ). It is often helpful to view A as a
morphism in the quantale-enriched category of V -relations: objects are sets (or classes) like P , and
a morphism P → P is exactly a function P × P → V . Under this reading, the operator s : P → V
is a “V -valued predicate” (a V -subset) on P , and A ? s is the standard action of a V -relation on a
V -predicate (an enriched direct image). This perspective makes later constructions feel less ad hoc:
one is simply using the native algebra of V -enrichment to push support forward along edges.

Definition 146 (Relational image operator). Given A : P × P → V and a state s : P → V , define
the image (or one-step propagation)
                                               M
                                 (A ? s)(q) :=   A(p, q) ⊗ s(p).
                                                p∈P

Here ⊕ and ⊗ are the quantale join and product; the join is taken in V .
                                                                      L
Remark 531 (Well-definedness when P is large). The expression            p∈P uses arbitrary joins in
V . Thus, when P is infinite, the definition still makes sense provided the quantale is complete
(as assumed) and we are working at a set-theoretic level where the join over P is legitimate. In
applications one often has either (i) P finite, (ii) s with finite support, or (iii) a sparsity/decay
condition on A ensuring only “effectively many” p contribute materially to each q.

Remark 532 (Notation unpacking: what ?, ⊕, and ⊗ do). The symbol ? is not new structure; it is
simply a name for the standard “relational image” construction induced by the quantale operations.
For each target node q, we look at all sources p, combine the edge strength
                                                                          L A(p, q) with the source
support s(p) using ⊗, and then aggregate all these contributions using          (the join in V ). When
V = [0, 1]2 with componentwise max as ⊕ and componentwise multiplication as ⊗, this says: “q
receives the strongest (componentwise) multiplicative contribution from any predecessor.”
    In a finite example with P = {p1 , p2 }, we have
                                                                            
                         (A ? s)(q) = A(p1 , q) ⊗ s(p1 ) ⊕ A(p2 , q) ⊗ s(p2 ) ,

which is a quantale-analogue of summing influences, except that we use the join operation appro-
priate to the chosen notion of graded truth/evidence.

                                                 245