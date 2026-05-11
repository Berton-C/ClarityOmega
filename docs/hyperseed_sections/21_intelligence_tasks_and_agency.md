# 21 Intelligence, tasks, and agency

20.5    Weighted inference and closure
To connect beliefs to question answering we need a minimal notion of inference. We use a general
“weighted rule” scheme compatible with the quantale operations. In particular, we treat inference
as an evidence-transforming operation on belief states, so that the same algebraic primitives used
for composing partial evidence elsewhere also govern derivations.

Definition 302 (Weighted inference rules). A weighted inference rule is a triple r = (Γ, ψ, λr )
where Γ ⊆ L is a finite set of premises, ψ ∈ L is a conclusion, and λr ∈ V is a rule strength. Given
a belief state β, define the rule’s contribution to ψ by
                                                          O
                                     contribr (β) := λr ⊗    β(ϕ),
                                                          ϕ∈Γ

using the p-bit quantale product ⊗ from Section 3.4.

    It is often helpful to read Γ as a conjunction-like bundle of requirements: all premises must
be supported to some extent for the rule to fire with nontrivial strength, and the degree to which
the premisesN jointly hold is computed by the iterated product. When Γ = {ϕ1 , . . . , ϕk }, the
expression ϕ∈Γ β(ϕ) is shorthand for β(ϕ1 ) ⊗ · · · ⊗ β(ϕk ); the finiteness of Γ ensures this is well-
defined without additional limiting assumptions. In the special case Γ = ∅, the iterated product is
understood as the ⊗-unit, so an “axiom rule” (∅, ψ, λr ) contributes λr directly to ψ.

Remark 1102 (Intuition and examples). This definition formalizes inference as “strength flows
through a rule.” The premises Γ are a finite subset of claims; ψ is the claim supported by the rule;
and λr isNthe intrinsic reliability (or methodological authority) of the inference pattern. The iterated
product ϕ∈Γ β(ϕ) composes the evidence values for all premises, and then λr ⊗ (· · · ) scales that
combined support by the rule strength.
    Example: a probabilistic-logic-inspired rule “from ϕ infer ψ” might use a large λr if it is a
trusted implication, while a heuristic analogy rule might use a smaller λr . The usefulness is that
all inference becomes a special case of the same algebra used for composing patterns and influences
elsewhere: rules are patterns with weights, and applying a rule is pattern-composition [5, 3].

    A further point is that λr can be used to encode more than “truth-preservation.” It may reflect
experimental reproducibility, the historical reliability of an instrument, the domain-of-applicability
of an approximation, or even a social/organizational trust score. Because V is paraconsistent, the
framework does not require that high support for ψ forces low support for ¬ψ; rather, it records
how multiple strands of reasoning contribute (possibly in tension) to the evolving state. Thus, the
notion of “rule strength” is closer to evidential warrant than to a classical entailment guarantee.

Definition 303 (One-step inference operator). Let R be a set of weighted inference rules. Define
FR : VL → VL by                                M            O        
                     FR (β)(ψ) := β(ψ) ⊕                 λ⊗      β(ϕ) .
                                               (Γ,χ,λ)∈R: χ=ψ       ϕ∈Γ

    By construction, FR performs a form of weighted forward chaining: each rule computes a
candidate increment for its conclusion, and then all such increments are aggregated by ⊕. The
definition allows R to be large (even infinite) as long as the relevant joins exist in V; this is exactly
where the completeness assumptions on the quantale become operationally meaningful.




                                                  430
Remark 1103 (Notation unpacking and intuition). Here VL denotes the set of all belief states (all
functions L → V). For each conclusion ψ ∈ L, the operator FR keeps the current evidence β(ψ)
L joins it (via ⊕) with the evidence contributed by every rule whose conclusion is ψ. The symbol
and
   denotes iterated join over that (possibly finite) set of rules.
    Intuitively: one inference step means “apply all rules once in parallel and add their conclu-
sions to what you already believe.” This is a deliberately extensional view of inference, compatible
with different internal implementations (symbolic proof search, neural approximations, probabilistic
programming), so long as their net effect can be summarized as evidence aggregation.

     Two additional structural properties are worth keeping in mind when interpreting FR . First,
it is inflationary (or extensive): for all β and ψ one has β(ψ) ≤ FR (β)(ψ) because FR (β)(ψ) is
defined as β(ψ) ⊕ (· · · ). This matches the intended reading that one-step inference accumulates
consequences rather than retracting beliefs. Second, because different rules for the same conclusion
are combined by ⊕, the operator treats rules as independent sources of support whose effects are
merged in a commutative, associative way (as governed by the join structure of the quantale). In
practice, this “all-at-once” aggregation is a semantic idealization; algorithmically one may schedule
rules in any order, and the theorem below justifies that repeated application still converges to an
appropriate closure under mild conditions.

Theorem 18 (Existence of inference closure). The operator FR is monotone on the complete lattice
VL . Hence it has a least fixed point above any initial state β0 , given by
                                                    M
                                       ClR (β0 ) :=    FRn (β0 ),
                                                   n≥0

where F 0 is the identity and F n+1 = F ◦ F n . If, additionally, all values that can arise belong to a
finite subquantale W ⊆ V (e.g. a finite rational grid closed under ⊕ and ⊗), then for finite L the
ascending chain stabilizes after finitely many steps.

    The expression “least fixed point above β0 ” should be read as: among all belief states β ∈ VL
such that β0 ≤ β and FR (β) = β, there is a smallest one in the pointwise order. This is the
natural notion of closure for an accumulating (inflationary) inference step: closure must preserve
the initial evidence and must be stable under further rule application. In settings where L or the
effective range of β is finite (as in the theorem’s second clause), the iterative characterization as a
finite-stage saturation is especially literal: one can view FRn (β0 ) as “beliefs derivable in at most n
rounds,” and the stabilization index N as a bound on the depth of rule-chaining needed to reach
closure.

Remark 1104 (What the theorem is saying, in plain language). The theorem asserts that if one re-
peatedly applies the one-step inference operator FR —adding in all consequences, then consequences
of consequences, and so on—this process has a well-defined “limit” belief state: the least state that
contains the initial evidence and is closed under the rules. Mathematically, it is the least fixed point
of FR above β0 .
    This result is important because it guarantees that “run inference to closure” is not merely
a metaphor but a legitimate construction in the paraconsistent quantale setting. It connects the
epistemic layer to the document’s broader use of fixed-point constructions for stability and self-
consistency (compare Knaster–Tarski usage in other contexts, e.g. [10]). It also complements the
earlier weakness-based view: closure is one way of operationalizing how indirect beliefs generate
direct beliefs through repeated pattern application [5].


                                                  431
    An additional intuition is that ClR (β0 ) is the smallest “saturated” belief state compatible with
the rules, analogous to the least Herbrand model in logic programming, but with truth values
in V rather than {0, 1}. Because joins aggregate rather than choose, closure can be seen as a
conservative way to incorporate all derivable support without committing to a single proof path.
This is especially relevant in paraconsistent settings: if there are rules deriving both ψ and ¬ψ,
closure records both streams of support, instead of forcing explosion or global inconsistency.

Proof. Monotonicity: ⊕ and ⊗ are monotone in each argument (componentwise on [0, 1]2 ). There-
fore each contribr (β) is monotone in β, and the join over rules preserves monotonicity, so FR is
monotone.
    The poset VL is a complete lattice under pointwise order, so by Knaster–Tarski, FR has fixed
points and the least fixed point above β0 is the join of the iterates. For the finiteness claim, assume
L is finite and values are restricted to a finite subquantale W ⊆ V. Then W L is a finite poset,
and the ascending chain β0 ≤ FR (β0 ) ≤ FR2 (β0 ) ≤ · · · cannot strictly increase forever. Hence it
stabilizes at some finite stage N , yielding a fixed point.

    It is also worth observing that the chain displayed in the proof is ascending not only because FR
is monotone, but because FR is inflationary: β ≤ FR (β) holds pointwise by definition. Thus the
iterative process never loses evidence already present in β0 ; it only accumulates additional support
as rules fire on newly strengthened premises. In computational terms, when L and the effective
value set are finite, one can implement closure as a standard saturation loop: repeatedly update β
by FR (β) until no coordinate changes.

Remark 1105 (Proof sketch and intuition). Proof sketch. The strategy is standard: show FR is
order-preserving, then invoke the fixed-point theorem for monotone maps on complete lattices. In
the present setting, the relevant complete lattice is the space of valuations β : L → [0, 1]2 ordered
pointwise by the product order on [0, 1]2 , so that β ≤ β 0 means β(ϕ)+ ≤ β 0 (ϕ)+ and β(ϕ)− ≤ β 0 (ϕ)−
for all ϕ ∈ L. Joins in this lattice are computed componentwise (pointwise suprema), which is
exactly what makes the iterative construction below well-behaved.
    The closure ClR (β0 ) is obtained by iterating FR starting from β0 and taking the join of all
iterates; monotonicity ensures this is an ascending chain. Equivalently, one may view ClR (β0 ) as
the least fixed point of FR above β0 : it is the smallest valuation extending the initial evidence that
is stable under all rule applications. The usual fixed-point theorem guarantees existence of such
fixed points and characterizes the least one as the join of the iterates (or, more abstractly, as the
join of all post-fixed points above β0 ).
    If the value domain and language are finite, the ascending chain must stabilize in finitely many
steps. More concretely, finiteness implies there are only finitely many distinct valuations reachable
by repeatedly applying FR starting from β0 , and since each step can only increase evidence in the
product order, no valuation can repeat without having stabilized; hence convergence occurs after at
most that finite number of strict increases. (When the domain is infinite, the same monotone-
iteration construction still makes sense, but the stabilization may require a limit stage and is then
captured by taking the supremum of the chain.)                                                        
    The key step is that ⊕ and ⊗ are monotone componentwise on [0, 1]2 ; thus any expression built
from them by composition and joins is monotone. Here “componentwise monotone” means that
increasing either the positive coordinate or the negative coordinate of any input cannot decrease the
corresponding coordinate of the output, so rule-aggregation never retracts previously accumulated
support. Since the rule operator FR is assembled from these primitives by applying them pointwise
across L (and then taking joins over applicable rules), the order-preservation of FR follows by
straightforward structural induction on the way rule conclusions are computed.

                                                 432
   Geometrically, one may imagine each claim ϕ ∈ L carrying a point in the unit square (the
(β + , β − ) plane), and an inference step moving these points “upward” in the product order (never
decreasing either component). The pointwise nature of the order is important: different formulas
may move at different rates, and closure is reached only when every formula has become stable under
further applications of the rules. In particular, the “upward” motion is not along a single axis but
in a partial order, so there can be incomparable intermediate states; nevertheless, the iteration from
β0 produces a chain because each iterate is obtained from the previous one by a uniform application
of the same monotone operator.
    Closure is then the least stable configuration under repeated application of these monotone trans-
formations: a fixed point reached by taking the supremum of all successive improvements. This least
fixed point represents the minimal amount of evidence that must be assigned, given β0 and R, to
satisfy the closure condition “all rule conclusions are already accounted for.” In this sense, ClR (β0 )
functions as a weighted analogue of deductive closure: it is not merely a set of consequences, but a
saturation of the initial valuation by all rule-supported increases in (β + , β − ).

Remark 1106 (Non-explosion by design). The scheme above does not include any special rule of
the form “from ϕ and ¬ϕ conclude anything.” Thus inconsistency does not automatically produce
arbitrary conclusions: a claim receives evidence only if there is a rule path that contributes to it.
This is the minimal operational sense in which the framework is paraconsistent. Put differently,
even if both ϕ and ¬ϕ carry high positive evidence, this fact by itself does not act as a universal
trigger; only explicitly provided rules can propagate information from those premises to further
conclusions. One may still choose to include rules whose premises mention both ϕ and ¬ϕ (for
example, to model specific forms of diagnostic reasoning), but any such propagation is then local,
controlled, and weight-sensitive rather than automatic and unbounded.

Remark 1107. This remark highlights a design choice: paraconsistency is not an add-on but a
consequence of what is omitted. In particular, since inference is mediated by explicit weighted rules,
contradictions can persist locally without turning the entire lattice of beliefs into maximal evidence
everywhere. The absence of explosion means that the closure operator does not collapse all formulas
to a top element merely because some formula has both kinds of support; instead, the fixed-point
computation preserves the distinction between “having conflicting evidence about ϕ” and “having
evidence for an unrelated ψ.” This aligns with the paraconsistent motivations developed in [23, 24].
It also clarifies how inconsistency interacts with graded evidence: tension between β + and β − for a
given claim is represented explicitly in the valuation, and closure propagates only what the rule base
R licenses, thereby preventing a single inconsistency from saturating the entire language unless the
rules themselves encode such saturation.

20.6    Question networks and the dynamics of thinking
Hyperseed allows question networks whose answers are further questions, potentially without a
well-founded base. We model this as a directed graph (or category) of question dependencies. In
this framing, the “shape” of an inquiry matters: two agents may share the same local inference
rules yet differ radically in what they can reach because their networks present different routes for
evidence to enter and propagate.

Definition 304 (Question network). A question network is a directed graph Q = (V, E) where
nodes v ∈ V are questions and an edge v → w means “answering v requires (or strongly benefits
from) answering w.” Cycles are permitted.



                                                  433
    It is useful to keep in mind that the edge label “requires (or strongly benefits from)” can cover
multiple epistemic relations. For instance, v → w may mean (i) w supplies a missing variable
needed to even state a candidate answer to v, (ii) w supplies calibration/validation needed to treat
v’s data as trustworthy, or (iii) w supplies a model-selection choice without which v is ill-posed.
In practice, one can regard the graph as a compressed summary of a richer structure (e.g., typed
questions, dependence modalities, or weighted edges expressing how strong the benefit is), but the
directed graph already captures the core phenomenon: the nontrivial ordering constraints induced
by epistemic dependency.

Remark 1108 (Intuition and examples). A question network is an explicit representation of the
structure of inquiry. Edges express epistemic dependency: to answer one question, you may need
answers to others (or at least to reduce them sufficiently). Permitting cycles is essential: real inquiry
often involves mutually supporting questions, like “what counts as a reliable instrument?” depending
on “what theory of measurement do we accept?” and vice versa. This is the formal shadow of a
familiar philosophical fact: inquiry is not always well-founded on indubitable primitives; it is often
stabilized by a coherent web.
    Example: in a research program, one node may be “estimate parameter θ,” another “validate
the measurement protocol,” another “choose a model class,” and dependencies may loop. In the
Hyperseed core-concept set this corresponds directly to Question Networks (Hyperseed-Concept 145)
and also to Dependency (Hyperseed-Concept 93).

    A further perspective is graph-theoretic: the strongly connected components (SCCs) of Q iden-
tify clusters of questions that mutually depend on one another. In a well-founded tree-like inquiry,
SCCs are trivial; in realistic inquiry, SCCs often correspond to methodological “packages” (mea-
surement standards, modeling assumptions, interpretive norms) that are revised together. This
helps separate two issues: (i) what is locally answerable given current methods, and (ii) what is
globally stabilized by coherence constraints across a loop.
    One may also read the parenthetical “(or category)” literally. If we interpret each edge v → w
as a generating morphism v → w, then composites correspond to indirect dependence paths: if
answering v benefits from w and w benefits from u, then there is a composite dependence of v on u.
On this view, reachability in the underlying graph expresses the transitive closure of “benefits from,”
and SCCs correspond to objects mutually connected by morphisms in both directions. Nothing in
what follows requires category theory, but the categorical reading aligns with the idea that inquiry
is a process of composing partial reductions rather than merely accumulating facts.

Definition 305 (Thinking as controlled closure). Fix a question network Q, a belief state β, and
an inference rule set R. A thinking episode is a finite sequence of operations of the form:

(a) choose a question node v (possibly based on goals/values and attention);

(b) obtain data via the question’s experiment channel, producing an evidence increment ev ;

(c) update beliefs (e.g. β ← β ⊕ ev ) and propagate by closure β ← ClR (β); and

(d) optionally entertain hypotheses to break cycles or explore counterfactual branches.

    The finiteness of the episode is important as an idealization of bounded agency: even if ClR is
defined as a least fixed point of rule application, an actual agent typically approximates it under
time/attention constraints, and the “controlled” part of the loop determines where approximation
error accumulates. Thus, a thinking episode is not assumed to be complete inference, but rather a
bounded sequence of actions that can be repeated and interleaved with further data collection.

                                                  434
   It is also helpful to make explicit a minimal set of closure-operator intuitions that motivate
ClR . In many logical and computational settings, closure operators are (at least approximately)
extensive, monotone, and idempotent:

            β  ClR (β),      β  β 0 ⇒ ClR (β)  ClR (β 0 ),    ClR (ClR (β)) = ClR (β),

where  is an information ordering (“contains no more commitments than”). Hyperseeds paracon-
sistent stance suggests that  should be read as an ordering of evidence or commitments that need
not collapse under inconsistency, so “extensive” means “adds what the rules license” rather than
“forces global consistency.”

Remark 1109 (Intuition and connections). This definition casts thinking as a controlled alterna-
tion between active inquiry (choose and perform a question) and passive propagation (apply closure
to distribute the consequences through the belief web). The “controlled” aspect is crucial: the system
does not apply all questions, but selects them under constraints of attention and value (Sections 18
and 14), echoing the cognitive-synergy and resource-allocation motifs in [19].
    Conceptually: inquiry supplies new distinctions (new evidence increments ev ), and closure turns
these into a revised global stance by pushing them through indirect beliefs (rules, trusted sources,
schemas). Thus thinking is neither pure perception nor pure deduction; it is the iterative weaving
together of questions and inference.

    One can read step (a) as a policy over nodes: a mapping from the current epistemic/valuational
state to a choice of which question to invest in next. This makes explicit why networks matter: two
networks with the same set of nodes but different edge structure can lead the same policy to very
different trajectories of belief change, because different dependencies alter which questions become
bottlenecks. In scientific practice, this corresponds to the familiar dynamic where an entire research
program can be stalled by a single unresolved methodological node (e.g., an instrument calibration
or a missing dataset), even when many downstream theoretical questions are already articulated.
    Step (b) also deserves a slightly richer reading: the “experiment channel” of a question need not
be a physical experiment. It may be an observation procedure, a simulation, a database query, an
expert consultation, or even an introspective probe, so long as it yields an evidence increment ev that
the agent treats as relevant to updating β. This makes the notion of question nodes compatible
with both empirical and conceptual inquiry: some nodes are primarily settled by measurement,
others by argument, and many by a mixture of both.

Remark 1110 (Bottoming out cyclic dependencies). If Q has cycles (non-well-founded “questions
about questions”), then an agent can still operate by (i) choosing a cut set of hypotheses that tem-
porarily resolves the cycle, (ii) exploring the induced consequences, and (iii) revising the hypotheses
or the network itself. This is a natural reading of Hyperseed’s remark that one can “force bottoming
out” by entertaining a hypothesis.

   A useful way to see this operationally is to treat the chosen hypotheses as provisional “anchors”
that permit local progress. For example, if “is the instrument reliable?” depends on “does the
theory predict stable readings?” and that depends on “are the readings trustworthy?”, then one
can temporarily posit a calibration prior or a simplified theory to obtain provisional predictions,
then use discrepancies to revise the anchors. In other words, the cycle is not eliminated in principle;
rather, the agent chooses a temporary direction of fit to obtain traction.

Remark 1111. The “cut set” intuition is graph-theoretic: one chooses a set of nodes whose pro-
visional assignment breaks the cycle, analogous to choosing boundary conditions for a differential

                                                 435
equation. The paraconsistent mechanism makes this psychologically plausible: entertaining a hy-
pothesis need not annihilate contrary evidence; it simply injects additional evidence that can later
be retracted (or counterbalanced) without global collapse.

    In graph terms, the cut set can be compared to a feedback vertex set: removing (or temporar-
ily “pinning”) those nodes makes the remaining dependency structure acyclic, enabling a staged
evaluation from upstream to downstream. In epistemic terms, the pinned nodes function like
methodological stipulations or default assumptions, which can later be relaxed. This also clarifies
why paraconsistency is not merely a technical convenience: if hypotheses can be introduced and
later revised without forcing explosive inference, then the agent can explore multiple competing
“boundary conditions” in parallel, retaining incompatible lines of investigation long enough to see
which ones pay off.
    Finally, the possibility of revising “the network itself” is not an afterthought: inquiry often
changes what counts as a question, what counts as an experiment channel, and what counts as
an acceptable dependency. For instance, learning that a measurement process is systematically
biased can introduce a new node (“estimate bias parameters”) and rewire edges so that previously
“downstream” theoretical nodes now depend on bias correction. Thus, the dynamics of thinking
are not only dynamics on β but also dynamics on Q and on the effective rule set R that governs
closure.

20.7    Belief systems and productive belief systems
Hyperseed defines a belief system as a coherent network of beliefs held within a community of
minds, with a characteristic “mutual implication” property. We capture this by combining (i)
community aggregation, (ii) inference closure, and (iii) a complexity-sensitive notion of “surprising
strength.” In this subsection, “belief” is treated as a graded semantic attitude toward sentences of
a shared language L, and a “system” is not merely a set but a pattern of mutual evidential support
as mediated by an explicit rule set R.

Definition 306 (Community belief aggregation). Let M be a finite set of agents, each with a belief
state βi : L → V. Define the community aggregate belief state by
                                            M
                                  βM (ϕ) :=     wi ⊗ βi (ϕ),
                                                i∈M

where weights wi ∈ V model trust/authority/attention and the operations are those of the p-bit
quantale. In particular, ⊗ should
                               L be read as “evidence scaling” (how much an agent’s attitude
counts after weighting), while    is the quantale join that pools the contributions into a single
community-level valuation.

Remark 1112 (Intuition and examples). This is a minimal formalization of intersubjective knowl-
edge: we take individual belief states and combine them into a community stance by (i) scaling each
agents contribution by a weight wi and (ii) joining the results. If wi is high (in positive evidence),
agent i has more epistemic influence; if wi has a negative component, one can even represent
distrust or systematic adversariality in a graded way.
    Example: in a lab group, a senior experimentalist might have higher weight on measurement-
related claims, while a theoretician might have higher weight on model-selection rules. The use-
fulness of this definition is that it makes social epistemology compositional: a community is not
a mysterious supra-mind but an aggregation operator on individual minds’ evidence valuations
(Hyperseed-Concept ?? and Hyperseed-Concept 170).

                                                 436
    Two further points are worth making explicit. First, the aggregation is performed pointwise
in ϕ: the community may defer to different agents on different claims, depending on how βi (ϕ)
interacts with wi under ⊗. Second, the weights wi need not be normalized in the probabilistic sense;
rather, their meaning is fixed by the algebra of V and by the intended operational semantics (e.g.
“whose judgment is heeded” vs. “how much independent evidence is added”). This leaves room for
modeling phenomena such as epistemic division of labor, institutional gatekeeping, and domains of
recognized expertise within a single uniform operator.
Definition 307 (Coherence score). Fix β and a rule set R. For ϕ ∈ L define the “leave-one-out”
state
            β \ϕ := the state equal to β except with the value at ϕ replaced by (0, 0).
Define the coherence score of B (relative to β and R) as
                                              1 X
                                                    π ClR (β \ϕ )(ϕ) ,
                                                                    
                             CohR (B; β) :=
                                             |B|
                                                    ϕ∈B

where π(p, q) = (1 + p − q)/2 is the plausibility projection (cf. Section 14). When B is understood
from context, CohR (B; β) can be read as a single-number summary of how “self-explanatory” the
set B is under the inferential practices encoded by R.
Remark 1113 (Notation unpacking and intuition). The leave-one-out state β \ϕ deletes the com-
munity’s direct evidence for ϕ by setting it to (0, 0) while keeping all other claims unchanged. Then
ClR (β \ϕ )(ϕ) asks: how much support for ϕ can be reconstructed from the rest of the belief web,
via inference rules? Finally, π(p, q) = (1 + p − q)/2 collapses a p-bit into a single plausibility scalar,
increasing with positive evidence p and decreasing with negative evidence q.
    Thus CohR (B; β) measures, on average over ϕ ∈ B, how well each belief is supported by the
others. This makes “mutual implication” precise without demanding classical consistency: coher-
ence is about reconstructability under closure, not about absence of conflict.
    Operationally, this is a counterfactual test: if we “blank out” the community’s explicit stance
on ϕ while leaving its other stances intact, does the remaining web (together with R) recover ϕ
anyway? A belief set with high coherence is therefore one in which many beliefs are not epistem-
ically isolated; they are downstream of shared principles, background assumptions, or explanatory
constraints captured by the closure operator. Conversely, if many ϕ ∈ B cannot be reconstructed
once removed, then B behaves more like a mere list of stipulations than an integrated system.
    Note that averaging over ϕ ∈ B makes coherence sensitive to the “typical” member of the set,
rather than to a single highly implied cornerstone claim; one can also consider variants such as a
minimum-over-ϕ (worst-case) coherence or a distributional profile of the individual summands, but
the mean is the simplest global proxy for networked support.
Remark 1114. Coh is high when each belief in B is well supported by the others via the commu-
nity’s inference rules. This is a formalization of “on average, each belief is strongly implied by the
other beliefs.” Because we use π ◦ Cl, coherence is allowed to coexist with contradiction: a belief
may be well supported and also well opposed.
    It is also worth emphasizing what coherence is not. A high score does not imply that B is
true, empirically adequate, or even stable under future evidence; it only indicates that, relative to
R and β, the beliefs in B form an inferentially entangled cluster. This is one reason coherence is
useful in a pluralistic setting: competing communities can each exhibit high internal coherence while
disagreeing, and the framework can then ask additional questions (e.g. about predictive performance,
causal control, or openness to revision) to distinguish productive belief systems from merely self-
reinforcing ones.

                                                   437
Definition 308 (Complexity cost and “surprise-adjusted” implication). Let Comp : L → [0, ∞) be
a complexity cost (e.g. description length, or an order reversal of weakness). Fix λ > 0 and define
a simplicity-biased prior weight
                                      Prior(ϕ) := e−λ Comp(ϕ) .
For ϕ ∈ L define the surprise-adjusted implication score

                                                 π ClR (β \ϕ )(ϕ)
                                                                  
                                 SAI(ϕ; β, R) :=                    .
                                                    Prior(ϕ)
Remark 1115 (Intuition, and relation to simplicity/weakness). The complexity cost Comp(ϕ)
quantifies how “expensive” a claim is to represent or to search for: it could be a description length
in the sense of algorithmic information theory [16], or a transformation of weakness/effort as
developed earlier [3]. The parameter λ > 0 controls how strongly the community prefers simplicity.
    The score SAI then formalizes a familiar epistemic phenomenon: a complex statement, if
strongly implied by the rest of what we accept, is more noteworthy than a simple one. Dividing by
Prior(ϕ) ensures that a claim with low prior weight must be especially well supported by the network
to achieve a high SAI. In Hyperseed-concept terms, this is the interaction of Simplicity (Hyperseed-
Concept 169), Weakness (Hyperseed-Concept 202), and Uncertainty (Hyperseed-Concept 195).
    Interpreting SAI as a “productivity”-leaning signal is natural: the numerator rewards inferential
integration (via closure), while the denominator penalizes gratuitous complexity. Thus, when two
claims are equally implied by the rest of the system, the one with smaller Comp(ϕ) is treated as
less epistemically surprising; conversely, a high-complexity claim must earn its keep by being tightly
constrained by the rest of the web. The exponential form of Prior is convenient because it turns
additive complexity into multiplicative penalties; however, the framework is compatible with other
monotone decreasing mappings from complexity to prior weight if a different calibration is desired.
Remark 1116 (Matching the Hyperseed phrasing). Hyperseed describes a belief as something “held
true to a degree that is surprising given the complexity of the belief.” The prior Prior(ϕ) makes
complex claims a-priori unlikely. A large SAI means the community implies ϕ strongly despite its
low prior.
    Equivalently, SAI distinguishes between “easy” implications (those that follow from many simple,
high-prior patterns) and “hard” implications (those that emerge as nontrivial consequences of the
system). In this sense, SAI operationalizes the idea that an integrated belief system is not merely a
heap of assertions: it can generate relatively unexpected consequences, and those consequences can
be ranked by how much inferential pressure the rest of the system exerts on them relative to their
complexity.
Definition 309 (Belief system and productive belief system). A belief system (for a community
M) is a pair (B, R) where B ⊆ L is a focal belief set and R is a rule set, such that CohR (B; βM )
exceeds a chosen threshold. Here “focal” is meant to emphasize that B is not the entire doxastic
state of M, but a distinguished subfamily of commitments that are tracked as a unit (e.g. a theory,
paradigm, doctrine, platform, or research program) and whose internal relations are evaluated using
R. Likewise, R is not only a list of inference schemata, but can also encode allowed explanatory
moves, defeasible reasoning patterns, methodological norms, and admissible forms of updating; it is
part of what makes B into a system rather than a mere set. The threshold requirement is intended
to exclude arbitrarily assembled collections of propositions: a community may hold many beliefs, but
only some coherent sub-webs are stable enough to function as objects of collective inquiry, pedagogy,
and transmission.
    A belief system is productive if, in addition:

                                                 438
(a) (Individuation) there exists a “core” subset Bcore ⊆ B that remains stable under typical evi-
    dence updates (high persistence of key commitments), and

(b) (Self-transcendence) the system regularly generates new high-SAI beliefs or new questions
    whose answers lead to novel patterns, without collapsing coherence.

The two additional clauses should be read as constraints on the dynamics of the pair (B, R) as the
community encounters new data, arguments, and social pressures. In particular, “typical evidence
updates” can be understood as those updates that occur with non-negligible frequency in the epistemic
environment of M (the ordinary course of observation, experiment, testimony, and criticism); the
individuation requirement then says that some subset functions as a robust identity condition for the
system across such ordinary perturbations. Similarly, the “without collapsing coherence” proviso
rules out a degenerate kind of novelty in which the system generates ever more claims only by
loosening R or fragmenting B so that CohR (B; βM ) no longer remains above threshold.

Remark 1117 (Intuition and why “productive” needs two constraints). A belief system is, on this
definition, a coherent epistemic sub-web in a community (Hyperseed-Concept 64). But a merely
coherent web can be sterile: it might resist novelty so strongly that it never learns, or it might be so
plastic that it dissolves under every perturbation. The definition of “productive” therefore combines
two tensions that recur throughout Hyperseed: individuation (a stable identity across time) and
self-transcendence (ongoing creation of new structure).
    The individuation clause says there is a persistent core (Hyperseed-Concept ??) that survives
ordinary evidence fluctuations. One way to think of Bcore is as the subset of commitments that play
a high-“load-bearing” role in the community’s reasoning: they constrain many other beliefs, are
invoked across many contexts, and are not easily abandoned without a substantial reconfiguration
of B. This does not require infallibility; it requires that, at the time-scale of ordinary inquiry,
the system has enough internal continuity to accumulate results, train newcomers, and coordinate
collective action. Conversely, if no such Bcore exists, then the “system” behaves more like a shifting
coalition of claims than a persisting object, and it becomes difficult to interpret its apparent successes
(or failures) as attributable to anything stable.
    The self-transcendence clause says inquiry continues to generate surprising, complexity-defying
implications (Hyperseed-Concept 167) and new Questions (Hyperseed-Concept 144) leading to Emer-
gence (Hyperseed-Concept ??). Here “generates” is meant in the constructive sense: the system, by
applying R to B and to incoming evidence, yields new commitments, conjectures, models, predic-
tions, or problem-statements that were not trivially present at the outset. The reference to high-SAI
is intended to separate mere proliferation of claims from epistemically meaningful novelty: a pro-
ductive system does not simply add ad hoc patches, but tends to add beliefs (or questions) that
integrate with and reorganize the web in a way that increases understanding, explanatory reach,
or compressive power while still maintaining coherence. In philosophical terms, one might hear an
echo of process views in which stability is a maintained pattern rather than a static substance [15].
In the intended application to science, the pair of constraints approximates a familiar phenomenon:
research traditions preserve enough continuity to be identifiable across time, yet are also compelled
to generate new results, new measurement regimes, and new conceptual distinctions in response to
anomalies and opportunities.
    A useful way to see why both constraints are needed is to consider two failure modes. If a system
has individuation without self-transcendence, it may become a well-defended “museum” of doctrine:
highly coherent and highly stable, but systematically unresponsive to the kinds of questions that
would extend or revise it. If a system has self-transcendence without individuation, it may behave
like a perpetual brainstorming session: many novel outputs, but little cumulative structure, making

                                                   439
it hard to distinguish progress from drift. The productive regime is the narrow corridor in which
novelty is assimilated rather than merely accumulated or repelled.

Remark 1118. The individuation/self-transcendence pair mirrors Hyperseed’s use of those terms
in other contexts. The present definition is intentionally schematic; later sections can special-
ize “typical evidence” and “regularly generates” to concrete learning dynamics and novelty mea-
sures. In particular, one can operationalize “typical evidence” by specifying a distribution over
evidence-events relevant to M (experiments, observations, counterarguments, replications, testi-
mony streams), and then measuring persistence of candidate cores under the corresponding update
rule. Likewise, “regularly generates” can be rendered as a rate condition (e.g. expected production of
high-SAI outputs per unit time, per unit research effort, or per cycle of deliberation), together with
a constraint that CohR (B; βM ) does not fall below threshold after incorporation. On this reading,
productivity becomes a property that can in principle be compared across communities or across
historical phases of a single community: the same belief system may be productive during one era
(when it opens fertile question-spaces) and less productive in another (when it mainly stabilizes and
defends its inherited core).
    It is also worth noting that the definition does not presuppose that productive systems are al-
ways “true” in any final sense; rather, it characterizes a kind of epistemic fitness for generating
structured, coherent novelty. This allows the framework to distinguish (i) coherent but stagnant
systems, (ii) inventive but unstable systems, and (iii) systems that exhibit cumulative inquiry. In
later applications, one can ask which additional constraints (e.g. calibration to external feedback,
robustness across subcommunities, or sensitivity to adversarial testing) connect productivity more
tightly to truth-tracking or scientific reliability.

20.8    Science as empirically coupled belief-system dynamics
Hyperseed defines science as a community belief system that generates predictive and causal models
about observation sets accepted broadly by members of the community. We model this as a special
case of the thinking loop where questions are experiments and answers are shared observations.
This framing makes explicit that “scientific knowledge” is not a single agent’s internal state but
a coupled multi-agent process: the community stabilizes a repertoire of experimental questions,
a shared interface for what counts as an answer, and a rule-governed method for turning those
answers into durable belief updates. In particular, the “predictive and causal” emphasis is meant
to distinguish scientific models from purely interpretive narratives: the central outputs of the belief
system are claims that constrain what should be observed under specified conditions, and (when
available) how observations would change under interventions.

Definition 310 (Observation set). Fix a community M and a context class of experiments E. An
observation set is a set O together with an observation map

                                            Obs : E → O,

possibly stochastic and observer-indexed. An observation set is accepted broadly by M if, for a large
fraction of agents and a large fraction of eligible experiments, the induced observations are mutually
consistent up to the community’s tolerance thresholds. The phrase “context class of experiments”
is intended to include not only the abstract experimental design but also the admissible range of
protocols, instrument configurations, and background conditions that the community treats as “the
same kind” of experiment for purposes of comparison. Likewise, “tolerance thresholds” should
be read as including both quantitative tolerances (e.g., error bars, confidence intervals, calibration


                                                 440
margins) and qualitative tolerances (e.g., coding reliability or procedural compliance in observational
sciences).
Remark 1119 (Intuition and examples). An observation set is a formalization of what a com-
munity can “jointly see”. The map Obs : E → O abstracts the full measurement pipeline into an
input-output channel: an experiment e ∈ E yields an observation in O, perhaps with stochasticity
due to noise, differing instruments, or contextual effects. Broad acceptance is not metaphysical
certainty; it is a social-epistemic stability condition: most relevant observers running the relevant
protocols obtain compatible outcomes. Put differently, Obs is not assumed to be infallible, but it
is assumed to be sufficiently well-behaved (under the community’s standards) that disagreement
is attributable to identifiable sources such as sampling variability, instrument drift, experimenter
degrees of freedom, or genuine context sensitivity, rather than to arbitrary observer idiosyncrasy.
The “observer-indexed” allowance captures cases where the observation pipeline includes human
judgment (e.g., labeling, clinical assessment, ethnographic interpretation) while still permitting in-
tersubjective convergence through training, rubrics, and reliability checks.
    Example: in physics, E could be a class of experimental setups and O numerical readouts.
In psychology, O might be survey responses or behavioral measures. In biology, O could be se-
quencing reads or microscopy counts; in astronomy, O could be processed spectra; in economics,
O could be aggregated indicators computed from raw data. This makes explicit the dependence of
“empirical truth” on intersubjective agreement and protocol, linking to Logical/Empirical Truth
(Hyperseed-Concept 104) and Intersubjective Reality (Hyperseed-Concept ??), and aligning with
social-computational accounts of science [20]. The point is not to reduce truth to consensus, but to
specify the operational substrate by which a community can treat some claims as empirically con-
strained: without broadly accepted observation sets, “evidence” cannot enter the communal belief
dynamics in a stable, reproducible way.
Definition 311 (Scientific model class and predictive claims). A scientific model class is a set M
of candidate models. Each model m ∈ M induces:
• a family of predictive claims Predm (e) about observations Obs(e), and
• optionally a family of causal claims Causem about how interventions change predictions.
The community treats these as elements of the claim language L. Here “predictive claims” should
be read broadly to include point predictions, distributional predictions (e.g., likelihoods over O), con-
ditional predictions given auxiliary variables, and robust qualitative constraints (e.g., monotonic-
ity, invariances, sign predictions). Similarly, “causal claims” range from fully specified structural
equations to weaker claims about directionality or invariance under a class of interventions; the
definition leaves room for multiple grades of causal expressiveness within L.
Remark 1120 (Intuition and connection to earlier machinery). A model class M is the space of
representational hypotheses the community is willing to consider. The induced claims Predm (e)
and Causem are then just ordinary claims in L, so they can receive p-bit evidence and participate
in closure with the same rule machinery as any other belief. This makes model comparison and
theory choice instances of general belief management: models do not sit outside the belief state
but are represented through the claims they entail and the support they accumulate via the update
mechanisms. In particular, competing models may share some induced claims while differing on
others; closure then propagates evidence to all logically or methodologically connected claims, which
is how localized experimental outcomes can have global effects on a theory network.
    This is important structurally: science is not a separate kind of reasoning; it is a particular con-
figuration of question/answer dynamics where questions are experiments and answers are shared

                                                  441
observations. Causal claims connect directly to Section 14’s intervention viewpoint, and the plural-
istic model-class stance aligns with Hyperseed’s broader engineering orientation toward families of
methods rather than single privileged formalisms [19]. The explicit model-class framing also clar-
ifies why scientific communities invest in tool-building: new instruments, new statistical methods,
and new representational languages expand E, enrich O, and enlarge (or restructure) M, thereby
changing what questions can be asked and what answers can count as decisive.

Definition 312 (Empirical update operator). Let e ∈ E be an experiment and o = Obs(e) its
(shared) observation. An empirical evidence increment is a map e,o : L → V that assigns posi-
tive/negative evidence to those predictive/causal claims that agree or disagree with (e, o). A scien-
tific update step is                                      
                                         β ← ClR β ⊕ e,o ,
where R includes both domain rules and methodological rules (statistics, measurement models,
etc.). The definition is intentionally agnostic about the internal structure of V and the operator ⊕:
different scientific subcultures can implement “evidence addition” by log-likelihood accumulation,
score-based updates, hypothesis-test-like penalties, or other evidential bookkeeping, so long as the
result can be represented as a belief-state update followed by rule closure. The phrase “agree or
disagree” should be interpreted through R: agreement may mean a high probability assigned to o
under Predm (e), or satisfaction of a qualitative constraint, or being within a prespecified tolerance
band after correction for known measurement error.

Remark 1121 (Intuition: why this captures “empirical coupling”). Empirical coupling is repre-
sented by the fact that observations enter as an evidence increment e,o , which is then integrated
into the belief state and propagated by closure. The methodological rule set R is where the com-
munity encodes its indirect beliefs about how to translate raw observations into support for claims
(measurement error models, statistical tests, calibration conventions, etc.). Thus the empirical loop
is: act (choose e), observe (o), translate to evidence, then infer. This highlights that “data” are
not self-interpreting: the same (e, o) can produce different e,o under different methodological com-
mitments (e.g., different priors, different preprocessing pipelines, different correction procedures),
and scientific disagreement can therefore be located either in the observation interface Obs or in the
rule system R.
     In Hyperseed terms, this is a controlled flow from Answers (Hyperseed-Concept 56) into Be-
liefs (Hyperseed-Concept 65), guided by Indirect Beliefs and stabilized socially as a Belief System
(Hyperseed-Concept 64). The “controlled” aspect is precisely what distinguishes scientific coupling
from mere exposure to experience: the community engineers reproducible questions (standardized
experiments), shareable answers (broadly accepted observation sets), and disciplined update rules
(methodological norms) so that belief change is not arbitrarily sensitive to individual perspective.

Proposition 32 (Occam bias from simplicity-weighted priors). Fix λ > 0 and a complexity cost
Comp : M → [0, ∞). Define Prior(m) = e−λ Comp(m) . Suppose two models m1 , m2 ∈ M receive
equal empirical support in the sense that the community assigns equal plausibility to their predic-
tive adequacy. If Comp(m1 ) < Comp(m2 ) then Prior(m1 ) > Prior(m2 ), so any posterior weight
proportional to (support) × (prior) will prefer m1 .

Remark 1122 (What the proposition is saying and why it matters). The proposition states a
minimal Occam principle: if two models fit the data equally well, the simplicity-biased prior assigns
higher weight to the simpler model, so any Bayesian-like update that multiplies support by prior
will prefer it. Nothing subtle is being claimed about the world; the point is that a preference for
simplicity is already present in the choice of prior. In practice, Comp can proxy for many different

                                                 442
simplicity notions: description length, number of parameters, circuit size, degrees of freedom, or
norm-based regularity; different choices encode different methodological values, and communities
can (and do) argue about which complexity measure best captures “simplicity” for their domain.
The proposition also clarifies a common interpretive confusion: the Occam effect here is not an
extra rule tacked onto inference after seeing data, but a consequence of committing (in advance) to
a simplicity-penalizing representation of model plausibility. From the belief-system viewpoint, such
priors are part of the community’s methodological rule set: they are indirect beliefs about which
hypotheses are worth taking seriously before evidence arrives, and they influence how quickly a
community converges or fragments when empirical support is ambiguous.

Remark 1123. This connects directly to the earlier weakness preference: if Comp is taken as
a form of description length or weakness-derived effort, then scientific model selection becomes a
special case of the general Hyperseed bias toward lower effort representations [3, 2]. It also resonates
with classic algorithmic justifications of Occam-style priors [16]. In particular, when Comp(m) is
identified (up to an additive constant) with a code length for describing m, the weight e−λComp(m)
can be read as a softness-controlled analogue of assigning higher prior mass to shorter descriptions;
λ then calibrates how aggressively the agent trades empirical fit against representational economy.

Proof. Immediate from monotonicity of the exponential: Comp(m1 ) < Comp(m2 ) implies −λ Comp(m1 ) >
−λ Comp(m2 ), hence e−λ Comp(m1 ) > e−λ Comp(m2 ) . Equivalently, taking logs shows log w(m) =
−λ Comp(m) is strictly increasing as Comp(m) decreases, so the ordering of weights is exactly the
reverse ordering of complexities.

Remark 1124 (Proof sketch and intuition). Proof sketch. The proof is a one-line order argument:
since x 7→ e−λx is strictly decreasing for λ > 0, smaller complexity yields larger prior weight. Then
equal empirical support implies the posterior preference is determined by the prior. More explicitly,
if two models m1 , m2 have the same likelihood for the observed data D, i.e. p(D | m1 ) = p(D | m2 ),
then Bayes’ rule gives
                              p(m1 | D)     p(D | m1 ) p(m1 )    p(m1 )
                                         =            ·        =        ,
                              p(m2 | D)     p(D | m2 ) p(m2 )    p(m2 )
so any posterior preference comes solely from the prior ratio p(m1 )/p(m2 ) = e−λ(Comp(m1 )−Comp(m2 )) .

    Geometrically, one may view Comp(m) as a coordinate measuring where a model lies along a
“simplicity axis.” The prior e−λComp(m) is then a decaying density along that axis; the proposi-
tion just states that this density is higher at smaller coordinates. One can also view λ as setting
the “length scale” along this axis: for large λ the density drops sharply (strong simplicity pres-
sure), whereas for small λ it decays slowly (weak simplicity pressure), so that empirical likelihood
differences must be correspondingly larger to override the simplicity bias.

Remark 1125 (Hyperseed reading). This is the epistemic analogue of weakness preference: among
models consistent with observations, prefer the weaker/simpler one. When combined with paracon-
sistent evidence handling, “anomalies” do not force immediate abandonment; they become negative
evidence that can coexist with positive evidence until a better model emerges. In this reading, the
exponential prior plays the role of a continuously valued “default conservatism”: it rewards models
that require fewer special-case commitments, fewer auxiliary hypotheses, or less representational
machinery to maintain internal coherence with what has already been learned. Thus, scientific
change is not modeled as a brittle, all-or-nothing refutation step, but as a gradual reweighting in
which anomalies reduce support without necessarily driving the posterior to zero in the presence of
coexisting, partially conflicting evidential constraints.

                                                  443
Remark 1126 (Additional clarification: coupling to empirical adequacy). The above preference
statement is most informative when made relative to empirical coupling. In standard Bayesian
terms, model selection compares posteriors p(m | D) ∝ p(D | m) p(m), so that the simplicity term
p(m) ∝ e−λComp(m) acts as a regularizer rather than a substitute for data fit. Accordingly, if m2 fits
the data substantially better than m1 , then a higher Comp(m2 ) can be compensated by a sufficiently
larger likelihood p(D | m2 ); the present proposition isolates the limiting case where the likelihoods
are equal (or, more generally, when the Bayes factor is near 1), so that the complexity penalty
becomes the deciding factor. On the “belief-system dynamics” interpretation, this corresponds to
cases where multiple explanatory stories accommodate the same observational constraints, and the
update rule resolves the tie by favoring the representation that is cheaper to maintain, communicate,
and integrate with the agent’s existing web of commitments.

20.9    State-dependent science
Hyperseed proposes that some observation sets are accessible (and intersubjectively stabilizable)
only when the community is in particular states of consciousness. We model this by indexing the
observation channel by a state parameter. Concretely, the role of the state parameter is to treat
“the observer” (and the social/ritual/technical context that sustains the observer) as part of the
experimental apparatus: changing the sustained cognitive–affective–attentional configuration can
change which distinctions can be enacted, and hence which experimental questions are even well-
posed. This is not merely an appeal to private experience; it is an attempt to express, in the same
formal slot as an instrument model, the idea that observer-training and observer-context can be
constitutive of measurement.

Definition 313 (State-indexed observation). Let S be a set of community-accessible states (medi-
tative, “I–Thou”, oceanic, etc.). A state-indexed observation set consists of O and maps

                                     Obss : Es → O,        s ∈ S,

where Es is the set of experiments that are performable/meaningful in state s.

    In this definition, Es plays a logically important role: it allows that the relevant difference be-
tween states is not only that they yield different outcomes for the same experimental description,
but that some experimental descriptions may fail to be executable, intelligible, or stablely inter-
pretable outside a given state. Equivalently, the state index can change both the “domain” (what
can be asked) and the “channel”S (how answers are produced). One can also package the same idea
as a single partial map Obs : s∈S ({s} × Es ) → O with Obs(s, e) = Obss (e); the present notation
simply emphasizes that the observation channel itself is conditioned on state.

Remark 1127 (Intuition and conceptual placement). The new ingredient is the index s ∈ S: what
counts as an admissible experiment Es and what observations result via Obss may depend on the
cognitive/affective/attentional state of the agents performing the protocol. This operationalizes the
idea that certain distinctions may be state-gated: one must become a certain kind of observer to
stably enact certain observational couplings.
    Examples range from mundane to speculative: altered attentional regimes can change perceptual
discrimination thresholds; disciplined contemplative practices may yield reproducible reports within
a trained community; more conjectural proposals (e.g. morphic resonance) would also, if made
protocol-stable, fit this formal slot [13]. In the Hyperseed core-concept set, this subsection touches
States of Consciousness (Hyperseed-Concept 178) and Oceanic Consciousness (Hyperseed-Concept
123), and it is consonant with state/location taxonomies for individuals and collectives [4, 12].

                                                 444
    A practical reading is that the “state” variable is itself something a community can (to some
degree) prepare, verify, and maintain. In the same way that many laboratory instruments require
calibration and controlled environmental conditions, a state-dependent protocol may require train-
ing regimes, selection criteria, social norms, and environmental supports that keep the community
within an operational envelope corresponding to s. This suggests separating three layers: (i) a
state-preparation procedure (how s is reached), (ii) a state-verification procedure (how member-
ship in s is checked or at least bounded), and (iii) the in-state experimental protocol e ∈ Es (what
is done once in s). The formalism above directly models (iii) and implicitly absorbs (i)–(ii) into
the background conditions defining the domain Es and the effective channel Obss .

Definition 314 (State-dependent science). A state-dependent science is a family of belief-system
dynamics (Bs , Rs , Obss ) indexed by s ∈ S, such that within each state:

• observations are broadly accepted by the in-state community;

• predictive/causal models are updated by the empirical loop of Section 20.8; and

• the resulting beliefs are stable under small perturbations of protocols within that state.

    The phrase “belief-system dynamics” here is intended to be read in the same sense as earlier
sections: Bs is the in-state belief-state (or set of admissible belief-states), Rs is the in-state re-
vision/update dynamic, and Obss is the in-state observation channel. Nothing in the definition
requires that the beliefs be true in a metaphysical sense; the requirement is that they be generated
and maintained by an empirically coupled, self-correcting loop relative to the state-conditioned
access channel. In particular, one can allow that Rs includes explicit procedures for handling dis-
agreement, uncertainty, and inter-observer variability, provided these procedures themselves are
part of the stable in-state practice.

Remark 1128 (Intuition and why this remains “science” in the formal sense). The definition says:
for each s, there is a coherent, empirically coupled belief-system dynamic. Thus state-dependent
science is not defined by abandoning empirical discipline, but by acknowledging a further contextual
variable that affects what can be observed and how. From a process perspective, the observer is not
an inert point but a temporally extended pattern of capacities; changing that pattern changes the
observation channel [15].
    The stability-under-perturbation clause is the analogue of experimental robustness: within a
given state s, small variations of protocol should not wildly change the observation map. This
is what blocks the notion from degenerating into “anything goes” subjectivism: reproducibility is
enforced, but only relative to the state-indexed context.

     To make the robustness clause more concrete, one may think of perturbations as spanning (at
least) (i) “technical” perturbations (minor differences in timing, phrasing, apparatus configuration),
(ii) “social” perturbations (minor differences in group composition or facilitation), and (iii) “state”
perturbations that remain within the tolerance region of s (e.g. small fluctuations in attention,
affect, or absorption that do not constitute leaving s). The intent is not to demand zero variability,
but to demand that the in-state observation channel have a stable core: outcomes cluster, calibra-
tion is possible, and error models can be learned. This is also the point at which standard concerns
about expectancy effects and demand characteristics must be treated as first-class methodological
issues: if such effects dominate, then the purported Obss is not stable in the required sense, or
else the channel being measured is actually “suggestibility under protocol” rather than the target
phenomenon.


                                                 445
Remark 1129 (Why this is not automatically “unscientific”’). The formal difference from ordinary
science is not the absence of empirical coupling, but the presence of an additional context variable
s. If a community can reliably enter a state s and reproduce observation protocols within s, then
(Obss , Rs ) can support a genuine (state-indexed) empirical discipline. Cross-state translation and
public accessibility become separate questions, not prerequisites.

    Public accessibility can then be treated as a spectrum rather than a binary. Some states may
be widely reachable with modest training, making the resulting discipline closer to ordinary science
in sociological character; other states may require long training horizons or unusual life conditions,
making the resulting discipline closer to an expert craft (but still potentially empirical within that
expert community). In either case, the formalism invites a “meta-scientific” layer: communities
can study which state-preparation procedures are reliable, what the failure modes are, how long it
takes to stabilize observers, and how intersubjective agreement scales with training. In that sense,
even when s is hard to reach, claims about s can remain tethered to evidence about reachability,
reliability, and robustness.

Remark 1130 (Normative feedback). Hyperseed also suggests a feedback loop: if a state-indexed
science pertains to states of extraordinary well-being, then the discipline can serve as a community-
level control policy that helps shift the community toward those states. Within our formalism this is
naturally expressed by letting states be reachable nodes in a policy-controlled Markov process, with
“scientific practice” as an action that increases transition probabilities toward desirable states.

    The Markov framing also makes explicit that “doing the science” can have dual roles: it both
(i) produces observations (epistemic output) and (ii) shifts the distribution over states (prag-
matic/ethical output). This dual role is already present in many ordinary scientific institutions
(e.g. training, credentialing, lab culture), but here it becomes central because the observation chan-
nel itself is state-conditioned. Accordingly, evaluation criteria can be layered: one may assess a
practice by the coherence and predictive power of its in-state models, and separately assess it by
the value profile of the states it tends to induce, while still keeping these assessments analytically
distinct.

Remark 1131. This remark connects epistemology back to values and control: inquiry is not merely
descriptive but can become prescriptive insofar as a practice reliably induces states with preferred
value profiles (Section 18). In Hyperseed language, this is an instance of Control (Hyperseed-
Concept 87) operating on States of Consciousness (Hyperseed-Concept 178) via socially stabilized
practice, which also relates naturally to community-level notions of culture and collective mind
systems developed later (Section 22).

20.10    Micro-example: paraconsistent transitivity in a question network
We conclude with a tiny instance showing how questions, axioms, and paraconsistent inference fit
together. In this setting, it is helpful to read each claim p ∈ L as a node in a small question/answer
graph, and to read the rule set as edges that transport evidential support between nodes. The
purpose of the example is not to argue that “same for the current task” is literally transitive in
every domain, but to show how a familiar schema can be represented and evaluated even when the
inputs are partially contradictory.

Example 17 (Three entities and a transitivity rule). Let X = {a, b, c}. Consider the claim
language
                                   L = {pab , pbc , pac },

                                                 446
where puv abbreviates “u and v should be treated as the same (for the current task).” In many
applications, one might imagine u, v as records, hypotheses, categories, or agents; the notation is
intentionally minimal so that the only moving parts are (i) a rule schema and (ii) a paraconsistent
treatment of evidence.
    Let the community’s rule set contain a weighted “transitivity” rule

                          r : {pab , pbc } → pac   with strength λr = (0.8, 0.0).

Here the strength has two components, meant to encode (respectively) how strongly the community
treats the rule as supporting its conclusion and how strongly it treats the rule as opposing its
conclusion. Thus, λr = (0.8, 0.0) says “we have substantial positive license to apply this rule, and
no explicit negative license attached to the rule itself.”
    Suppose an agent has evidence

                 β(pab ) = (0.9, 0.4),      β(pbc ) = (0.7, 0.1),      β(pac ) = (0.0, 0.0).

It is useful to read β(p) = (β + (p), β − (p)) as a pair of nonnegative weights, where β + (p) measures
degree of support for p and β − (p) measures degree of support for ¬p (or, more generally, for “reasons
against accepting p”). The evidence for pab is explicitly conflicted: both positive and negative
support are present. In particular, nothing in the representation forces β + (pab ) + β − (pab ) ≤ 1, so
the framework can record “mixed signals” without first reconciling them into a single probability-like
quantity.
    Compute the one-step inference contribution:

   contribr (β) = (0.8, 0.0) ⊗ (0.9, 0.4) ⊗ (0.7, 0.1) = (0.8 · 0.9 · 0.7, 0.0 · 0.4 · 0.1) = (0.504, 0.0).

This multiplication-style ⊗ can be read as an “and-like” aggregation: a rule application is strong only
to the extent that each ingredient (the rule license and each premise) is strong, and the particular
choice here treats the positive and negative channels independently by multiplying like with like.
In other words, for this illustrative ⊗, the positive component of the contribution depends only on
the positive components of the inputs, and the negative component depends only on the negative
components. Thus
                          FR (β)(pac ) = β(pac ) ⊕ (0.504, 0.0) = (0.504, 0.0).
The ⊕ operation is acting as the accumulator for multiple sources of evidence (for instance, multiple
rules or observations targeting the same claim); in this toy step there is only one contributing rule, so
the update is transparent. The agent now has positive evidence for pac , derived from the transitivity
schema, while the conflict in pab did not “explode” into arbitrary conclusions. Concretely, the
presence of β − (pab ) = 0.4 does not force contribr (β) to become negative, nor does it automatically
block the positive pathway; it is simply recorded as a coexisting counter-weight on the premise node.
    If the agent wishes to “bottom out” a cycle in a larger question network, it may entertain a
hypothesis such as pac at high strength, propagate by closure, and compare the resulting conflicts
to decide whether the hypothesis is coherent with other commitments. In that broader usage, one
can think of the hypothesis injection as an explicit, inspectable intervention: rather than silently
assuming a fixed point exists and is unique, the agent tests candidate stabilizers and then evaluates
how much inconsistency they induce elsewhere in the network.
Remark 1132 (What to notice in the computation). The crucial feature is that negative evidence in
a premise does not automatically negate the ability to infer something; nor does it entail everything.
This is the operational point of the paraconsistent setup: local inconsistency is permitted as a first-
class datum, and inference is engineered so that inconsistency does not trivialize the entire theory.

                                                     447
    The rule strength λr = (0.8, 0.0) carries only positive support, and (in the product used in this
example) the negative component of the contribution becomes 0 because the rules negative component
is 0. Equivalently, with this ⊗, a rule application can contribute negative evidence to its conclusion
only if the rule itself (or, in other designs, some premise) carries negative evidence in the channel
that is wired to generate negative output. This makes the “audit trail” of negativity explicit: one
can point to exactly which pieces of the system are responsible for introducing counter-support for
a claim.
    Thus we obtain a derived positive claim without any requirement that the premises be consistent.
In a network with multiple rules, an agent might simultaneously accumulate positive and negative
evidence for the same conclusion (e.g., FR (β)(pac ) = (α+ , α− ) with both components nonzero),
in which case the system records that tension rather than forcing an immediate collapse to either
acceptance or rejection.
    As a toy illustration, this mirrors the intended “conflict without explosion” behavior discussed
throughout the paraconsistent parts of the document [23, 24]. The key methodological point is that
the ability to proceed in the presence of conflict is not a purely informal principle; it is enforced by
the algebra of ⊗, ⊕ and by the way rules are allowed to contribute to conclusions.
    In a fuller implementation, alternative ⊗ choices could allow negative evidence to propagate
in more nuanced ways; the point here is that the algebraic interface makes such choices explicit
and auditable. For example, one could choose an ⊗ in which the negative component of a premise
partially attenuates (rather than nullifies) the positive contribution, or in which a strongly negative
premise injects explicit negative mass into the conclusion; the present micro-example simply exhibits
the cleanest “separation of channels” behavior so that the mechanics can be read off directly from
the numbers.

Hyperseed concepts covered
• Knowing and Thinking as structured dynamics on question/answer graphs (Hyperseed-Concept
  ??).

• Template Patterns; Questions as information-seeking actions about instantiations; Answers as in-
  stantiations or other uncertainty-reducing artifacts (Hyperseed-Concept 130, Hyperseed-Concept
  144, Hyperseed-Concept 56, Hyperseed-Concept 195).

• Beliefs (direct and indirect); Axiom Systems; “entertaining a hypothesis” as hypothetical belief
  injection followed by closure (Hyperseed-Concept 65, Hyperseed-Concept 64).

• Question Networks, including cyclic/non-well-founded dependencies and “bottoming out” by
  hypothesis (Hyperseed-Concept 145, Hyperseed-Concept 93).

• Belief System as a coherent network of beliefs held in a community; “productive” belief systems
  via individuation and self-transcendence constraints (Hyperseed-Concept 64, Hyperseed-Concept
  ??, Hyperseed-Concept 167).

• Science as empirically coupled belief-system dynamics; State-Dependent Science as a state-
  indexed family of observation sets and update loops (Hyperseed-Concept 104, Hyperseed-Concept
  178).




                                                  448
21     Intelligence, tasks, and agency
21.1    Motivation: from mind concepts to task competence
Sections ??–20 built a picture of minds as pattern-using, resource-limited systems: they represent
(some) distinctions, update paraconsistent beliefs, allocate attention, and exert control to shape
future perception while negotiating value conflicts. In this framing, “mind” names an internal
organization: a way of building and reusing structured regularities under bounded computation,
bounded time, and bounded sensing. What remains missing at this stage is an operational connector
between internal organization and externally checkable performance, i.e., a way to say not only what
a system is like internally but what it can reliably accomplish when coupled to an environment.
    Hyperseed’s “intelligence” layer adds two commitments:
• Tasks provide an operational bridge from internal pattern webs to externally checkable compe-
  tence.
• Agency is persistent closed-loop control; autonomy is the capacity to generate, sustain, and revise
  goals from within (rather than merely executing imposed objectives).
    The first commitment is deliberately methodological: it treats performance as something that
can be posed, repeated, and audited. In particular, a task statement is meant to pin down (i) what
information is available to the system, (ii) what interventions are permitted, (iii) what counts as
success or failure, and (iv) what resource budgets and time horizons apply. This makes it possible
to distinguish “the system sometimes produces a desired outcome” from “the system is competent
at a specified interaction pattern,” and to separate one-off luck from stable capability. It also forces
clarity about interfaces: what is observed, what is acted upon, and how feedback is delivered.
    The second commitment clarifies a persistent ambiguity in informal discussions of intelligent
behavior. Many systems can execute a goal when the goal is supplied from outside, yet do not
select, maintain, or renegotiate goals under changing conditions. Hyperseed therefore separates (a)
being an agent in the minimal cybernetic sense of maintaining a control loop over time, from (b)
being autonomous in the stronger sense of owning a goal-management process. The distinction
matters for evaluation: two systems might solve the same benchmark task while differing radically
in how brittle their goal pursuit is when the task is perturbed, reframed, or partially underspecified.
    This section formalizes tasks (and families of tasks), defines intelligence measures as transfer
and generalization across task sets, and makes “agent,” “autonomous agent,” “intent,” and the
action primitives “stimulate”/“inhibit” mathematically explicit. We also introduce a compact
notion of “engineered” as an ontological tag on artifacts produced by intelligent action. A further
motivation for these formalizations is comparability: once tasks are explicit objects, one can speak
precisely about when two seemingly different problems share a structure (hence belong to a common
family), when a solution method transfers, and when improvement reflects genuine generalization
rather than memorization of a narrow interaction script.
    In particular, the move to families of tasks is meant to encode variation: different initial condi-
tions, different noise realizations, different objective weights, different environments drawn from a
distribution, or even different representational encodings of the same underlying problem. This is
the natural setting in which “generalization” and “transfer” are not slogans but statements about
performance stability under controlled shifts. A system that performs well on a single fixed instance
may be competent at that instance; a system that performs well across a family demonstrates ro-
bustness to variation. Likewise, a system that learns within one family and then reliably improves
performance on a related family exhibits transfer in a sense that can be measured and compared
across architectures.

                                                  449
    The emphasis on action primitives such as “stimulate”/“inhibit” is also explanatory rather
than decorative: many agent models tacitly assume a rich action alphabet. By naming minimal
primitives, Hyperseed aims to make clear what sort of causal interface is being assumed between
an agent and its world. In this view, complex actions can be built compositionally from simpler
primitives, while the core semantics remains grounded in how interventions modulate downstream
dynamics (amplifying, suppressing, enabling, blocking). This keeps later notions of “intent” tied
to concrete control structure: intent is not merely a post-hoc interpretation, but a commitment
expressed through persistent selection of actions that shape trajectories toward goal conditions
under feedback.
    Finally, the “engineered” tag is introduced to mark a distinction that will matter later when
discussing artifacts, tools, and constructed sub-agents. The tag is not meant to imply a specific
material substrate or manufacturing process; rather, it indicates provenance: the object exists in its
present functional organization because intelligent action brought it about (possibly via long chains
of intermediate artifacts and delegation). This provenance marker becomes useful when reasoning
about ecosystems that mix naturally occurring structures with designed ones, or when tracking
how competence can be externalized into tools that then feed back into later task performance.

Remark 1133. Philosophically, the move from “mind” to “intelligence” in Hyperseed is a move
from being a web of patterns to being assessable by what one can reliably do. A task is not
merely an external test: it is a formalized interface between an agent’s internal organization and
an environment that can answer back. This is why tasks belong to the Hyperseed core-concept set
as an explicit bridge concept (Hyperseed-Concept 186), and why task families become the natural
stage on which transfer learning is defined (Hyperseed-Concept 192; see also [19, 7]). The key word
in “environment that can answer back” is counterfactual responsiveness: when the agent changes
what it does, the world changes what it returns. This prevents collapsing “task” into a static
dataset query and keeps the emphasis on interaction, feedback, and control. Reliability then refers
not only to average success but to stability under repeated trials, bounded resources, and specified
perturbations—a notion aligned with competence rather than isolated performance.

21.2    Tasks as interaction specifications
We work with an intentionally lightweight task formalism: a task is an interaction channel plus
an evaluation functional. This is compatible with classical decision theory (MDPs/POMDPs) but
keeps the paraconsistent value layer explicit. In particular, we separate (i) the interface that gen-
erates observation streams in response to actions from (ii) the evidence-bearing evaluation attached
to transitions, and we do so without assuming that the agent has access to any privileged “true
state” variable beyond what the interaction itself provides.

Definition 315 (Histories). Fix finite sets O (observations) and A (actions). For t ≥ 0 define the
set of length-t histories by

                             Ht := O × (A × O)t = {(o0 , a0 , o1 , . . . , at−1 , ot )}.
           S
Let H :=       t≥0 Ht be the set of all finite histories.

Remark 1134. The notation here is deliberately explicit: O is the alphabet of percepts the task
presents, and A is the alphabet of interventions the agent may select. A history in Ht is thus an
alternating record
                                (o0 ) (a0 , o1 ) (a1 , o2 ) · · · (at−1 , ot ),


                                                        450
and H is simply the set of all such finite records of arbitrary length. This is the minimal object
needed to define policies without assuming Markovian state access: a policy may depend on the
entire past, not merely on the current observation.
     As a simple example, if O = {0, 1} and A = {L, R}, then an element of H2 is a quintuple
(o0 , a0 , o1 , a1 , o2 ) such as (1, L, 0, R, 0). Such strings are the “raw material” out of which an agent
constructs patterns and habits (Hyperseed-Concept 130, 155; cf. [5]).
     Two small technical conventions are worth keeping in mind for later sections. First, the set H
includes the “time 0” history (o0 ) ∈ H0 , so an agent may condition its very first action on an initial
percept. Second, H is a disjoint union of Ht over t, so “history length” is always well-defined: a
history is not merely a sequence but a sequence together with its time index.

Definition 316 (Policies). A (possibly stochastic) policy is a map

                                             π : H → ∆(A),

where ∆(A) is the probability simplex on A. A deterministic policy is the special case π : H → A.

Remark 1135. The symbol ∆(A) denotes the set of all probability distributions on the finite set A.
Thus π(h) is not an action but a distribution over actions, from which an action may be sampled.
This is the standard way to model randomized decision-making; it is also the cleanest way to model
bounded or exploratory control without changing the rest of the mathematics.
    For a concrete illustration, if A = {L, R}, then ∆(A) can be identified with [0, 1] by p 7→
(p, 1 − p), and a policy returns a coin-bias conditioned on the history. In many later constructions,
one can restrict attention to deterministic policies without changing the conceptual point; allowing
stochasticity simply keeps the formalism honest about uncertainty.
    It is also useful to note the modeling stance implicit in π : H → ∆(A): the agent is not assumed
to have a compact internal “state” that summarizes the past. Of course, real agents often compute
summaries (belief states, feature maps, recurrent memories), but those are implementations of a
history-dependent policy rather than prerequisites of the task definition.

Definition 317 (Task). A task is a tuple

                                           T = (O, A, P, r, γ),

where O and A are finite, P : O×A → ∆(O) is a transition kernel over observations, r : O×A×O →
V is a p-bit-valued immediate evaluation (reward/penalty evidence), and γ ∈ (0, 1) is a discount
factor.

Remark 1136. This definition should be read as a deliberately “interface-only” cousin of the stan-
dard MDP/POMDP framework: instead of positing a hidden state space, we treat the observation
process itself as the primary object. The transition kernel P (o, a) is a distribution over next obser-
vations o0 given current observation o and action a. The immediate evaluation r(o, a, o0 ) is not a
single real number but a value in V = [0, 1]2 , i.e. a p-bit of positive and negative evidence.
    A simple example is a bandit-like task where P ignores o and a and always returns the same
distribution on O, while r assigns (1, 0) to “good” outcomes and (0, 1) to “bad” ones. More gener-
ally, this setup can encode tasks whose feedback is noisy, socially contested, or internally conflicted
(Hyperseed-Concept 198), which is one reason Hyperseed avoids reducing value to a single scalar
too early (cf. [19]).
    Two clarifications help relate this “observation-level” formalism to more familiar ones. First,
a classical MDP (S, A, P̃ , r̃, γ) induces a task of the present form by taking O = S, letting P be P̃

                                                    451
(viewed as a kernel on observations), and letting r be an evidence-valued lift of the scalar reward r̃
(for instance by mapping r̃ > 0 to positive evidence and r̃ < 0 to negative evidence, if one wishes).
Second, a POMDP with latent state S and observation kernel Z can also be viewed through this
lens by taking O to be the observation alphabet and absorbing the latent state into the induced
observation-to-observation dynamics; in general this produces a non-Markov observation process,
so the present Markov kernel P : O × A → ∆(O) is best seen as a simplifying interface choice rather
than a claim that observations are always Markov in reality.
    If one wishes to drop even this Markov-in-O simplification, the minimal generalization is to
allow a history-dependent environment kernel P : H × A → ∆(O), i.e. P (h, a) is a distribution
over the next observation given the entire past. We do not need that generality for the constructions
in this section, but it is conceptually aligned with the earlier point that the agent’s policy may be
fully history-dependent.
Remark 1137 (Why p-bit-valued evaluation). The evaluation r is allowed to be conflicted: it
may assign both positive and negative evidence to a transition. This matches Hyperseed’s value
paraconsistency (Section 18) and supports tasks whose feedback is ambiguous, socially contested, or
internally conflicted. In particular, allowing r(o, a, o0 ) = (p, n) with both p > 0 and n > 0 makes
room for “mixed” events (e.g. actions that succeed on one criterion while failing on another, or
actions that are praised by one evaluator while condemned by another) without forcing an early
reconciliation into a single numerical tradeoff.
Definition 318 (Trajectory value via discounted salience join). Write an infinite trajectory as
ω = (o0 , a0 , o1 , a1 , . . .). Define the discount factor p-bit δt := (γ t , γ t ) ∈ V and the trajectory value
                                                     M
                                         ValT (ω) :=      δt ⊗ r(ot , at , ot+1 ),
                                                  t≥0

using the p-bit quantale operations ⊕ and ⊗ from Section 3.4.
Remark 1138. A few symbols deserve a first-reading gloss. The infinite sequence ω is the full
unfolding of interaction: observation, action, observation, action, and so on. The discount γ ∈
(0, 1) yields weights γ t that shrink with time, and the pair δt = (γ t , γ t ) discounts positive and
negative evidence symmetrically in V. The operation ⊗ plays the role of “scaling” evidence by
salience (here, discount), while ⊕ plays the role of an “accumulation” operator, which in the p-bit
quantale is a componentwise maximum (Section 3.4; Hyperseed-Concept 143, 202; see [3, 2] for
broader discussion of weakness).
    As an example, suppose along a trajectory there is one highly salient positive event early on
with r = (1, 0) and all later events have smaller discounted magnitude; then ValT (ω) will retain
that early strong evidence. Conversely, a single striking failure early on will dominate the negative
component. This reflects a bounded-attention reading: what is remembered and acted upon is often
the most salient evidence,
                   L        not the sum of all evidence.
    The choice of t≥0 (a join/max-like accumulation) also sidesteps the usual convergence ques-
tions that arise with infinite-horizon summation: because ⊕ is idempotent and bounded in V, the
expression is well-defined as soon as each discounted term δt ⊗ r(ot , at , ot+1 ) is defined. Intuitively,
the value records the strongest discounted positive evidence encountered and the strongest discounted
negative evidence encountered, rather than aggregating all evidence into a single scalar.
    For readers who prefer to see the mechanics in a finite prefix, consider the first two transitions
of ω with evidence r0 := r(o0 , a0 , o1 ) and r1 := r(o1 , a1 , o2 ). Then the two-step salience-joined
evidence is
                                         (δ0 ⊗ r0 ) ⊕ (δ1 ⊗ r1 ),

                                                        452
so whichever transition carries more salient positive evidence will set the positive coordinate of the
result, and likewise for the negative coordinate. This makes explicit the sense in which the formalism
models “what stands out” rather than “what adds up” over time.
Remark 1139. Because ⊕ is a componentwise maximum, ValT emphasizes the most salient dis-
counted success/failure signals along the trajectory. This matches an attention-like reading: a
bounded agent may be driven primarily by the strongest evidence-laden events rather than by a fully
additive cumulative utility. Other aggregators can be substituted if desired; the present choice keeps
the link to the core quantale explicit. In particular, since ⊕ acts like a (discounted) supremum,
ValT behaves more like a “peak evidence” semantics than a “sum of evidence” semantics: once a
decisive success signal has occurred, additional smaller successes do not further increase the positive
component, and analogously for failures. This makes the evaluation robust to long stretches of low-
level noise, while remaining sensitive to rare but high-confidence events (e.g. a single catastrophic
failure state, or a single decisive achievement of a goal condition). It also clarifies why discount-
ing interacts naturally with ⊕: discounting controls how much salience is granted to evidence as it
recedes in time, while ⊕ controls how evidence is pooled across time once discounted.
Definition 319 (Policy value and plausibility scalarization). Let Eπ [·] denote expectation over
trajectories induced by P and π. Define the p-bit-valued policy value
                                                          
                                     JT (π) := Eπ ValT (ω) ,

where expectation is taken componentwise in [0, 1]2 . Define the plausibility projection pl : V → [0, 1]
by
                                                       1 + v+ − v−
                                     pl(v + , v − ) :=             .
                                                            2
The scalar score pl(JT (π)) is interpreted as “net plausibility of success.” In this reading, v + can be
viewed as graded support for success, v − as graded support for failure, and the affine centering at
1
2 treats “no salient evidence either way” as epistemically neutral rather than as either success or
failure.
Remark 1140. Componentwise expectation means: if ValT (ω) = (V + (ω), V − (ω)), then JT (π) =
(Eπ [V + ], Eπ [V − ]). The projection pl then converts the evidence-pair into a single number in [0, 1]
by treating positive evidence as increasing plausibility and negative evidence as decreasing it. The
                   +    −
affine form 1+v 2−v is chosen so that (1, 0) 7→ 1, (0, 1) 7→ 0, and (0, 0) 7→ 12 as a neutral baseline.
    One should not mistake pl for a metaphysical collapse of value into one scalar; it is a prag-
matic device for defining competence comparisons and breadth measures. The underlying p-bit
value JT (π) ∈ V retains the information about conflict (Hyperseed-Concept 198) even when one
temporarily projects down to a real score. It is also useful to note some basic structural properties
of pl: it is monotone nondecreasing in v + , monotone nonincreasing in v − , and 1-Lipschitz with
respect to the `1 -distance on [0, 1]2 up to a factor of 12 , i.e. changing (v + , v − ) by (∆+ , ∆− ) changes
pl by at most 21 (|∆+ | + |∆− |). Thus, while pl is a lossy map, it behaves continuously and predictably
under small changes in evidential components. Moreover, pl(v + , v − ) = 21 + 21 (v + − v − ) makes ex-
plicit that the scalarization is equivalent to taking a signed “evidence balance” v + − v − ∈ [−1, 1]
and rescaling it into [0, 1]; in particular, pl treats equal positive and negative evidence as neutral
regardless of the absolute magnitudes, reflecting the intended paraconsistent stance that conflict
should not be silently resolved without a modeling decision.
Definition 320 (Task sets). A task set is any collection T of tasks (often equipped with a dis-
tribution D for sampling tasks). We will refer to (T , D) as a task environment. In the typical

                                                     453
case where D is present, one can regard D as encoding both prevalence (which tasks occur) and
importance (which tasks matter more) within the ecology.

Remark 1141. A task set T plays the role of an “ecology of challenges.” A single task can be
solved by memorization or brittle specialization; a distribution over tasks forces the question of
generalization and transfer (Hyperseed-Concept ??, 118, 192; cf. [19, 7]).
    As a simple example, T might be the set of all two-armed bandits with varying payoff probabili-
ties, and D a prior over those probabilities. Then an “intelligent” agent is one that does not merely
excel on one bandit instance, but does well on typical draws from the family. This example also high-
lights a distinction between in-task uncertainty (stochastic rewards within a fixed bandit instance)
and across-task uncertainty (not knowing which instance will be drawn); task environments make
the latter explicit and thereby separate adaptivity/learning from mere execution. In settings where
tasks share structure (e.g. common latent parameters), good performance on D-typical tasks can be
interpreted as evidence that the policy (or agent) has captured that structure rather than overfitting
to idiosyncrasies of a single task. Finally, note that T need not be “small” or even countable: it
may be a parametrized family (e.g. all MDPs in a class), and D may be a continuous distribution;
the definition is intentionally agnostic about representation so that later breadth notions can range
from finite benchmarks to open-ended task generators.

21.3    Task morphisms and compositional transfer
Hyperseed treats intelligence as pattern discovery that transfers across contexts. A minimal for-
malization of transfer is: one task can be reduced to another by translating observations/actions
while preserving evaluation.

Definition 321 (Task reduction / simulation morphism). Let T = (O, A, P, r, γ) and T 0 = (O0 , A0 , P 0 , r0 , γ)
share the same discount γ. A reduction (or simulation morphism) F : T → T 0 consists of maps

                                 fO : O → O0 ,        fA : O × A0 → A,

such that for all o ∈ O and a0 ∈ A0 with a = fA (o, a0 ):

(a) ( Dynamics compatibility) The pushforward of P (o, a) under fO equals P 0 (fO (o), a0 ), i.e.

                              (fO )∗ P (o, a) = P 0 (fO (o), a0 ) ∈ ∆(O0 ).
                                             


(b) ( Evaluation compatibility) For all o+ ∈ O,

                                     r(o, a, o+ ) = r0 fO (o), a0 , fO (o+ ) .
                                                                            


Remark 1142. The notation (fO )∗ denotes pushforward of a distribution along a function: if
ν ∈ ∆(O) and fO : O → O0 , then (fO )∗ (ν) ∈ ∆(O0 ) is the distribution of fO (X) when X ∼ ν. Thus
condition (a) says: if one observes o only through fO (o) and acts via an abstract action a0 which
is decoded into a concrete action a, then the next abstract observation has exactly the distribution
prescribed by T 0 .
    The decoder fA : O × A0 → A is allowed to depend on the concrete observation o. This models
a common phenomenon in representation transfer: the same abstract action token may be imple-
mented differently depending on the finer-grained concrete context. In transfer-learning language,
F is an exact semantics-preserving interface between tasks (Hyperseed-Concept 192, 157; see [7]
for a related framework emphasizing compositional transfer).

                                                    454
Remark 1143. A reduction says: by observing o only through fO (o) and choosing an abstract
action a0 (which is then decoded into a concrete action a), the agent experiences a task equivalent
to T 0 . This is a precise encoding of “reusing a solution by changing representation.”

Proposition 33 (Reductions compose). If F : T → T 0 and G : T 0 → T 00 are reductions (in the
sense of Definition 321), then there is a composite reduction G ◦ F : T → T 00 .

Remark 1144. Intuitively, this proposition says that “doing one representation change after an-
other” is itself a representation change of the same kind. This matters because transfer in realistic
settings is rarely a single leap; it is often a chain of abstractions: raw perception to mid-level features
to task-specific summaries. The proposition is a small but essential step toward treating transfer as
a compositional algebra rather than a bag of tricks (cf. [7]).

Proof. Write F = (fO , fA ) and G = (gO , gA ). Define (g ◦ f )O := gO ◦ fO and define the composite
action decoder by
                              (g ◦ f )A (o, a00 ) := fA o, gA (fO (o), a00 ) ,
                                                                            

so that an abstract a00 is first decoded to an a0 using gA (at the abstract observation fO (o)),
then decoded to a concrete a using fA (at the concrete observation o). Dynamics compatibility
follows from functoriality of pushforward of measures and the two given compatibility conditions;
evaluation compatibility follows by substitution.

Proof sketch. The strategy is to define the only composite maps one could reasonably mean:
observations are re-encoded by composing the encoders, and actions are decoded in two stages.
The two compatibility axioms are then checked by “plugging in” these definitions. Pushforward
is functorial, so the dynamics condition composes automatically; reward preservation is a direct
substitution.                                                                                 

Remark 1145. The key step is recognizing that actions must be decoded with awareness of the
correct observation granularity at each stage: gA expects an O0 -observation (namely fO (o)), while
fA expects the original O-observation o. Geometrically, one can picture a commutative diagram of
stochastic kernels: the composite reduction ensures that the “abstract” observation process induced
from T matches the observation process of T 00 exactly.

Corollary 3 (Category of tasks). There is a (small) category Task whose objects are tasks and
whose morphisms are task reductions; identities are given by fO = idO and fA (o, a) = a.

Remark 1146. This corollary says that tasks and exact transfer maps between them form a mathe-
matical world in which one can speak of equivalence, composition, and invariants. The philosophical
gain is that “transfer” becomes something one can reason about structurally, rather than narratively:
an agent that discovers a morphism has discovered a re-description that preserves what matters for
evaluation.
    In later developments (outside the strict setting here), one often relaxes exact equality to ap-
proximation and moves to enriched or higher-categorical variants; the point of beginning with an
ordinary category is to make clear which parts of transfer are purely structural (cf. [7]).

Proposition 34 (Transfer by reduction). Let F : T → T 0 be a reduction. Given any policy
π 0 : H 0 → ∆(A0 ) for T 0 , there is an induced policy π for T such that

                                            JT (π) = JT 0 (π 0 ).



                                                    455