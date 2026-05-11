# 17 Consciousness, reflective will, and autonomy

emergent, context-sensitive convenience (Hyperseed-Concepts ?? and ??). This inversion matters
in engineering terms as well: in adaptive systems, the representational vocabulary and the modeled
objects can both change, so insisting on fixed identity would force one either into brittle bookkeeping
or into ignoring precisely the developmental dynamics one wants to describe [19, 5].

16.2    Approximate morphisms of quantale-weighted networks
Self-continuity and mind–world correspondence are both defined by Hyperseed using “approximate
morphisms” between pattern-flow networks. We now make this precise in a form that is compatible
with enriched-category theory.

Definition 214 (Quantale-weighted directed graphs). A V-weighted directed graph (briefly, a
V-graph) is a pair G = (X, G) where X is a set of nodes and

                                           G:X ×X →V

assigns a weight to each ordered pair of nodes. We write G(x, y) for the weight on the directed edge
x → y.

Remark 848 (Intuition and examples for V-graphs). A V-graph is the simplest object that can carry
graded relational structure. If V = [0, 1] with ≤ the usual order and ⊗ interpreted as multiplication
or min, then G(x, y) can be read as the strength of an influence or a similarity from x to y. If
V = [0, 1]2 (a p-bit domain), then G(x, y) can record positive and negative evidence for that influence
simultaneously, echoing the earlier paraconsistent attitude [23, 24].
    This definition is useful because both “mind” and “world” can be represented as such graphs:
nodes stand for tokens in the representational scheme, and edges for pattern-conditioned flow,
predictive linkage, or habitual propagation (Hyperseed-Concepts 132 and 131). The key point is
that we do not assume the node sets match across time or across domains; instead we will compare
graphs by maps between node sets.

Definition 215 (Residuation). Because V is a quantale, the map u ⊗ (−) preserves arbitrary joins
and hence has a right adjoint. Define the residuum (implication) by
                                          _
                                u → v := {w ∈ V : u ⊗ w ≤ v}.

Equivalently, for all u, v, w one has

                                   u⊗w ≤v       iff    w ≤ (u → v).

Remark 849 (Notation and intuition for the residuum). The symbol → here is not material
implication from classical logic; it is the residuated implication determined by ⊗. The defining
equivalence
                                    u ⊗ w ≤ v ⇐⇒ w ≤ (u → v)
says that (u → v) is the largest degree w such that combining u with w does not exceed v. One
may read it as: “given that u holds to some degree, how much slack is available to reach v?” In
quantitative settings it behaves like a best-possible conditional bound; in paraconsistent settings it
functions as a controlled, non-explosive form of implication, which is precisely why residuation is
valuable in the Hyperseed stack [3].




                                                 334
Remark 850 (Example computations). If V = [0, 1] and ⊗ = min, then
                                        (
                                          1 if u ≤ v,
                               u→v=
                                          v if u > v,

so the implication is “perfect” when u is already no stronger than v, and otherwise degrades to v.
If instead ⊗ is multiplication, then u → v behaves like a truncated ratio (v/u capped at 1), again
matching the idea of a maximal compensating factor. These examples illustrate why residuation is
the right tool for measuring how well a map preserves edges: it compares source edge-strength with
target edge-strength in a way consistent with the quantale’s native combination operator.

Definition 216 (Degree of a structure-preserving map). Let G = (X, G) and H = (Y, H) be
V-graphs and let f : X → Y be a function. Define the preservation degree of f by
                                        ^
                                             G(x, x0 ) → H(f (x), f (x0 )) .
                                                                          
                       deg(f ; G, H) :=
                                           x,x0 ∈X

Equivalently, q ≤ deg(f ; G, H) if and only if

                         G(x, x0 ) ⊗ q ≤ H(f (x), f (x0 ))     for all x, x0 ∈ X.

We say that f is a q-approximate morphism G → H if q ≤ deg(f ; G, H).

Remark 851 (Intuition for deg(f ; G, H) and why the meet appears).VThe degree deg(f ; G, H)
measures the worst-case adequacy of f over all edges in G. The meet x,x0 enforces a universal
constraint: the map is only as good as its weakest-preserved relational link. The equivalent condition

                                     G(x, x0 ) ⊗ q ≤ H(f (x), f (x0 ))

should be read as: if an edge in G has strength G(x, x0 ), then after discounting by q it must still fit
under the corresponding edge in H. Thus q quantifies a uniform level of tolerated degradation.
    A simple example: if G and H encode similarity graphs, and f maps internal concepts to
external referents, then q bounds how much similarity structure is lost under interpretation. This
is useful because it yields a single composable number capturing the fidelity of a whole map, which
will allow us to speak rigorously about continuity and correspondence without assuming any hard
identity of tokens.

Remark 852 (Relation to enriched functors). If G and H are actually V-categories (reflexive
and transitive in the V-enriched sense), then q-approximate morphisms with q = 1 are precisely
V-enriched functors. The definition above is intentionally more general: it applies to raw weighted
graphs and can be combined with a closure operation (e.g. reflexive-transitive closure) when one
wants a genuine enriched categorical semantics.

Remark 853 (Why we avoid requiring categorical axioms here). Requiring reflexivity/transitivity
at the outset would build in a strong coherence assumption that many empirical pattern webs do not
satisfy before closure or smoothing. Hyperseed repeatedly emphasizes that cognition begins in rough,
partially contradictory data and only later acquires stable structure via closure processes (compare
Hyperseed-Concepts 72 and ??). The present choice therefore keeps the interface maximally general
while remaining compatible with enriched-category intuitions when the additional axioms hold.
    More concretely: reflexivity and transitivity are precisely the axioms that would let a V-graph be
regarded (after suitable interpretation) as the hom-object assignment of a V-enriched category, where

                                                     335
identities and composition are already “baked into” the structure. By postponing these axioms, we
allow the weights G(x, x0 ) to be read as raw affinities, similarities, causal supports, or co-occurrence
strengths, without presuming that self-links are maximally strong or that indirect support must be
mediated by ⊗ in a globally consistent way. The closure/smoothing steps can then be understood as
the point at which the empirical web is forced into (or approximated by) a more coherent, category-
like regime, rather than assuming coherence from the beginning.

Theorem 14 (Composition law for approximate morphisms). Let G = (X, G), H = (Y, H), and
K = (Z, K) be V-graphs. For functions f : X → Y and g : Y → Z,

                            deg(g ◦ f ; G, K) ≥ deg(f ; G, H) ⊗ deg(g; H, K).

In particular, if f is a q1 -approximate morphism and g is a q2 -approximate morphism, then g ◦ f
is a (q1 ⊗ q2 )-approximate morphism.
    It is worth stressing what the direction of the inequality encodes: the composite cannot be worse
than the tensor-combination of the two degradations, but it may be better in special cases (for
instance, if g collapses distinctions that were responsible for f ’s worst violations, or if the feasibility
constraints become looser after passing through H). Thus the theorem provides a guaranteed lower
bound on composite fidelity rather than an exact formula.

Remark 854 (What the composition law says, and why it matters). In plain terms: if f preserves
the structure of G inside H up to degradation q1 , and g preserves the structure of H inside K up
to degradation q2 , then the composite g ◦ f preserves the structure of G inside K up to the com-
bined degradation q1 ⊗ q2 . This is the algebraic statement that “approximate structure preservation
composes.”
    The result is crucial for everything that follows: self-continuity will be defined by chaining
together approximate morphisms across successive time-slices, and mind–world correspondence will
be used inside control and prediction loops (Section 14). Without a composition law, these degrees
would not behave like a stable currency of fidelity across multiple steps.
    Two limiting cases help anchor the interpretation. First, when deg(f ; G, H) is the monoidal unit
(of V) so that f is “exact” in the sense of not requiring any weakening, the theorem reduces to the
familiar closure of exact structure preservation under composition. Second, in common numerical
quantales (e.g. V = [0, 1] with ⊗ as multiplication or a t-norm), the combination q1 ⊗q2 matches the
intuition that independent degradations multiply, so long chains decay in a controlled, algebraically
predictable way rather than in an ad hoc manner.

Proof. Let q1 := deg(f ; G, H) and q2 := deg(g; H, K). By definition of deg, for all x, x0 ∈ X,

                                      G(x, x0 ) ⊗ q1 ≤ H(f (x), f (x0 ))

and for all y, y 0 ∈ Y ,
                                      H(y, y 0 ) ⊗ q2 ≤ K(g(y), g(y 0 )).
Apply the second inequality with y = f (x) and y 0 = f (x0 ) and compose:

      G(x, x0 ) ⊗ (q1 ⊗ q2 ) = (G(x, x0 ) ⊗ q1 ) ⊗ q2 ≤ H(f (x), f (x0 )) ⊗ q2 ≤ K(g(f (x)), g(f (x0 ))).

Thus (q1 ⊗ q2 ) satisfies the defining feasibility condition for deg(g ◦ f ; G, K), so deg(g ◦ f ; G, K) ≥
q1 ⊗ q2 .
    Note that the proof uses only the basic quantale/enrichment primitives already in play: the
monotonicity of ⊗ in each argument (so inequalities can be tensored on the right), and associativity

                                                     336
(so “weakening twice” is unambiguous). No reflexivity or transitivity assumptions on G, H, K are
needed, which is consistent with the preceding remark about avoiding categorical axioms at this
stage.

Remark 855 (Proof sketch and geometric intuition). Proof sketch. Use the equivalent characteri-
zation of deg: a lower bound q is feasible exactly when every edge in the source, weakened by q, fits
under the corresponding edge in the target. Apply this twice (first for f , then for g) and associate
the tensor product to conclude feasibility for g ◦ f with weakening q1 ⊗ q2 .                        
    The key step is substituting y = f (x) and y 0 = f (x0 ) so that the second inequality speaks about
exactly the images of the nodes used in the first inequality. Associativity of ⊗ then ensures the
degradation factors combine cleanly. Visually: think of each morphism as allowing you to “shrink”
all edge weights by a factor and still embed them into the next graph; doing this twice multiplies (or
otherwise ⊗-combines) the shrinkage.
    Order-theoretically, the same picture can be read as follows: the set of feasible degradations for
a map is downward closed in V (if q works, any weaker q 0 ≤ q works), and deg is the best achievable
bound among them. The theorem exhibits an explicit feasible element for the composite—namely
q1 ⊗ q2 —so the degree of the composite must lie above that element in the V-order. This viewpoint
clarifies why the statement is a ≥ bound on degrees even though it arises from chaining ≤ constraints
on weakened edges.

16.3    Self-continuity as approximate self-morphism across time
We now instantiate the preceding definitions on time-indexed pattern-flow networks.
Definition 217 (Pattern-flow network). Fix a system S (as modeled by observer O) and a time
interval I. A pattern-flow network for S on I is a V-graph

                                       FS,I : XS,I × XS,I → V,

where XS,I is a set of nodes representing specific entities or pattern-tokens, and where FS,I (a, b)
quantifies the extent to which pattern that “first appears” in a subsequently appears in b over the
interval I. The precise estimator used to compute FS,I (a, b) is observer-dependent and may include
sub-interval weighting (temporal discounting).
Remark 856 (Intuition and examples for pattern-flow networks). A pattern-flow network is a
time-slice summary of “how patterns propagate” inside the modeled system. If nodes are tokens like
belief X, memory Y, action schema Z, then FS,I (a, b) measures how reliably activity or content
associated with a predicts or feeds into activity/content associated with b during I. This packages
the Hyperseed emphasis on Pattern and Process (Hyperseed-Concepts 130 and 140) in a way that
is directly comparable across times and across domains.
    For a simple example, let a = “see cup” and b = “reach cup”. Then a high value FS,I (a, b)
indicates that within the interval I the perceptual token “see cup” tends to be followed by (or to
support) the action token “reach cup.” If V is paraconsistent, then FS,I (a, b) may simultaneously
record evidence for and against the flow, capturing the fact that behavior can be context-fragmented
or internally conflicted.
Remark 857 (Why observer-dependence is not a defect). The estimator for FS,I is allowed to be
observer-dependent because “pattern” is already observer-relative in Hyperseed: it depends on the
distinctions the observer can draw and the resources it allocates (Sections 9 and 15). Rather than
pretending away this relativity, we keep it explicit and then build invariants (like morphism degrees)
that remain meaningful under representational change [5, 19].

                                                 337
Definition 218 (Pattern-flow-network self-continuity). Let I and J be successive time intervals.
The pattern-flow-network self-continuity of S from I to J is
                                              _                         
                         SCS (I → J) :=              deg f ; FS,I , FS,J .
                                            f :XS,I →XS,J

We say that S has θ-self-continuity from I to J if SCS (I → J) ≥ θ.
Remark 858 (Intuition: continuity as best possible relabeling). This definition says: among all
possible ways of matching (or “translating”) the system’s internal tokens at time-slice I into tokens
at time-slice J, pick the one that best preserves the flow structure; that best achievable degree is
SCS (I → J). So continuity is not “are the tokens identical?” but “can we find a renaming under
which the organizational dynamics remain largely the same?” This is exactly the kind of continuity
one expects in developing or learning systems, where representational vocabulary shifts while deeper
regularities persist (Hyperseed-Concept 166; compare [5]).
    As a toy example, suppose a child first uses a token dog and later refines it into dog and wolf.
The node sets differ across time, but there may be a map f that sends earlier dog into later dog
and preserves many flow relations (e.g. “seeing dog” → “fear”), yielding high self-continuity despite
vocabulary refinement.
Remark 859 (Interpretation). SCS (I → J) is the best achievable degree of structure preservation
between the system’s pattern-flow network on I and on the next interval J. The definition allows
the system to “rename” internal nodes across time via the map f . This is essential when the
representational vocabulary itself evolves.
                                                       W
Remark 860 (Why use a join over maps?). The join f plays the role of an existential quantifier
in the quantale: it says “there exists a correspondence between times that works this well.” This
existential flavor is appropriate because the system need not commit to a single privileged identity
map; different contexts and downstream tasks may induce different best correspondences. This flex-
ibility will matter again when we discuss mind–world correspondence, where multiple incompatible
interpretations of the world may coexist without explosion [23, 24].
Corollary 2 (Longer-horizon self-continuity along a realized chain). Suppose we have a chain of
successive intervals I0 → I1 → · · · → In . Then

             SCS (I0 → In ) ≥ SCS (I0 → I1 ) ⊗ SCS (I1 → I2 ) ⊗ · · · ⊗ SCS (In−1 → In ).

Remark 861 (What the chain inequality means). If the system is fairly continuous from one slice
to the next, then it is at least that continuous over multiple steps, with the degree decaying (at
worst) by repeated combination via ⊗. This is the formal statement that “continuity compounds”
rather than resets. It connects directly back to Theorem 14: the corollary is essentially the repeated
application of compositionality, but lifted through the join-over-maps definition of SCS .
Proof. Choose (for each k) a map fk : XS,Ik → XS,Ik+1 whose degree approximates SCS (Ik → Ik+1 ).
More explicitly, for any tolerance parameter δ  0 (in the order of V, or after scalarization if one
prefers a numerical proxy), one may pick fk so that its degree is within δ of the join defining
SCS (Ik → Ik+1 ); this is the standard “ε-optimizer” maneuver when the supremum is not attained.
Then Theorem 14 shows that the composition fn−1 ◦ · · · ◦ f0 has degree at least the stated tensor
product. Here the tensor product encodes the cumulative degradation under composition: each
step contributes a factor in V, and the quantale multiplication (or its chosen monoidal operation)
aggregates these factors in the same order as the composites. Taking joins over choices of the fk

                                                  338
yields the inequality. In other words, since SCS (I0 → In ) is defined as the join of degrees over all
candidate maps XS,I0 → XS,In , it must dominate the degree of any particular composite built from
near-optimal adjacent witnesses.

Remark 862 (Proof sketch and intuition). Proof sketch. Pick near-optimal matching maps between
each adjacent pair of slices, compose them into a single map from I0 to In , use the composition law
to bound the degree of this composite map, and then observe that SCS (I0 → In ) is the join over all
such maps, so it must be at least as large as the degree of this particular composite.               
    The only subtlety is the use of “approximates”: since the join defining SCS may not be attained
by a single maximizer, one chooses maps close enough to the supremum for the intended application.
Conceptually, the statement says that if you can translate your internal vocabulary forward slice-
by-slice, you can translate it forward over the whole horizon by composing those translations, with
predictable loss. A useful way to read the quantale-valued inequality is as a generalized “triangle
inequality” (or, depending on ⊗, a multiplicative analogue): stepwise continuity lower-bounds long-
range continuity, but cannot in general prevent decay as n grows. This also clarifies why the result is
framed as a lower bound: composing specific witnesses constructs one admissible long-range witness,
and the join defining SCS (I0 → In ) can only be larger when additional direct correspondences exist
that are not decomposable into the chosen stepwise maps.

Relative-information self-continuity. Hyperseed distinguishes pattern-flow-network self-continuity
from a more “information geometric” notion: the mind at I and the mind at J should share a large
amount of relative information. To express this in a quantale-friendly way, we use a monotone
scalarization of V. This shift is deliberate: the morphism-based notion is invariant under relabel-
ings (and thus tracks structural persistence), whereas an information-style comparison presupposes
a shared coordinate system (a fixed node set) and then measures numerical drift within that coor-
dinate system.

Remark 863 (Connection to information theory). This “relative-information” variant resonates
with classical measures of model drift and state distance. When V is ultimately derived from prob-
abilistic quantities, one may connect the divergence to familiar information-theoretic functionals
[16, 17]. Hyperseed’s point, however, is not to privilege any single divergence, but to keep the
interface open while preserving monotonicity and composability. In particular, the monotonicity
requirement ensures that “more disagreement in V” (in the ambient order) cannot be mapped to
a smaller scalar penalty, so that downstream bounds and thresholds behave predictably when one
refines or coarsens the underlying edge annotations.

Definition 219 (Scalarization and graph divergence). A scalarization is a monotone map k · k :
V → [0, ∞]. Given two V-graphs G = (X, G) and H = (X, H) on the same node set, define the
edgewise divergence                     X
                         D(G, H) :=            G(x, x0 ) − H(x, x0 ) ,
                                         (x,x0 )∈X×X

where subtraction is interpreted componentwise when V is a product domain (e.g. a p-bit quantale),
and otherwise D is taken as a schematic placeholder for any reasonable scalar divergence induced
by k · k. We say that G and H have ε-relative-information proximity if D(G, H) ≤ ε. When X
is infinite (or merely large), the same definition can be read as selecting a summation convention
(e.g. absolute convergence, truncation, or a weighted sum), depending on the modeling choice; the
present formulation isolates the conceptual ingredient, namely an edgewise comparison mediated by
a monotone scalarization.


                                                 339
Remark 864 (Intuition and examples for scalarization). A scalarization k · k is simply a way of
extracting a nonnegative “size” or “cost” from a V-value. For V = [0, 1] one might take kuk = 1 − u
(turning similarity into distance) or kuk = u (treating u itself as a magnitude). For V = [0, 1]2 one
might take k(p, q)k = p + q or k(p, q)k = max(p, q), depending on whether one wants to penalize
total evidence mass or only the strongest polarity.
    The divergence D(G, H) then sums edgewise differences. This is useful when the node set is
held fixed (e.g. a stable vocabulary) and one wants to quantify how much the network changed in
a numerical sense. It complements the morphism-based continuity, which is structurally invariant
under relabeling and thus better suited to developmental regimes where the vocabulary itself evolves.
One can also view D(G, H) as a “Hamming-like” comparison generalized to weighted, typed edges:
rather than counting mismatched symbols, it accumulates per-edge disagreement costs determined
by k · k. If desired, one may normalize by |X|2 (when finite) to obtain an average per-edge drift;
the unnormalized form is often preferable when absolute drift magnitude, rather than density, is the
salient quantity (e.g. when small localized changes matter less than widespread global rewiring).

Remark 865 (Two complementary views). Pattern-flow self-continuity (existence of a high-weight
approximate morphism) is a structural condition. Relative-information proximity is a numerical
condition. They are related but not identical: self-continuity allows nontrivial relabelings and can
hold even when many edge weights drift, provided the drift is coherent under the relabeling. For
example, if a system consistently renames an internal symbol (or splits one concept into two with
a systematic bookkeeping map), then a high-degree morphism may still exist even though a naive
edgewise comparison on a fixed node set would report substantial divergence. Conversely, a small
D(G, H) can occur even when no good relabeling exists (e.g. many small but incoherent edge per-
turbations), so the two notions probe different failure modes.

Remark 866 (Why keep both notions). In applications, one often wants both: structural con-
tinuity to justify that a system is still “the same agent” in the operational sense, and numerical
proximity to detect subtle instability within a fixed representational frame. Hyperseed treats these
as complementary lenses rather than competing definitions, reflecting a broader methodological plu-
ralism: different invariants answer different questions about persistence (Hyperseed-Concept 200).
In particular, structural continuity is naturally adapted to scenarios where the system’s represen-
tational basis is itself part of the dynamical state (so comparing raw coordinates is ill-posed), while
numerical proximity is adapted to monitoring and validation tasks in a fixed interface (so that
deviations can be alarmed on a stable scale).

Reflective self-continuity. Hyperseed further distinguishes reflective self-continuity: the sys-
tem is explicitly aware (in its own representational language) of its continuity. Formally this requires
a notion of internal self-models and declarative content, developed in Section 17. In the present sec-
tion we only note the minimal scaffold: reflective self-continuity arises when a self-model contains
an explicit representation of (approximate) morphisms witnessing SCS (I → J), and this represen-
tation is used in attention and control (Sections 15 and 14). One can think of this as internalizing
not only the fact that “there exists a correspondence,” but also storing (possibly schematically) the
correspondence itself as an object that can be queried, composed, revised, and used as a premise
in planning.

Remark 867 (Why reflectivity is an extra requirement). A system may be continuous without
having a representational handle on that fact, just as a river may persist as a process without rep-
resenting its own persistence. Reflective self-continuity adds a meta-level constraint: the continuity
witness must appear as content in the system’s representational economy and must be actionable

                                                  340
(able to steer attention or control). This anticipates the closure phenomena discussed later in the
consciousness layer (Section 17) and aligns with fixed-point flavored analyses of self-model stability
[10]. Operationally, reflectivity is what allows the agent to treat identity-over-time as a manipulable
hypothesis: it can allocate resources to maintaining a correspondence, detect when the correspon-
dence degrades, and initiate repair (e.g. by learning a new alignment map) rather than merely
exhibiting continuity as an unexamined byproduct of dynamics.

16.4    Development as continuity plus expanding capability
Hyperseed defines development as the conjunction of self-continuity with the acquisition of funda-
mentally new capabilities over time, typically in a way that extends and enriches rather than ob-
soletes earlier capabilities. To formalize this we separate the “identity” condition (self-continuity)
from a capability preorder. This targets Development as a core notion (Hyperseed-Concept 95)
and also interfaces naturally with task-based views of intelligence [19]. In particular, the separa-
tion makes explicit that (i) continuity is about who or what persists across change, whereas (ii)
capability is about what can be done and how well, which may increase, plateau, or even partially
regress while still remaining “the same system” in the sense of Section 16. This also anticipates
later discussions where apparent “improvement” in one regime can be explained by changes in
attention, habit structure, or observation/interface layers rather than by a simple accumulation of
skills.

Definition 220 (Capability profile and capability preorder). Fix a family G of goals (or tasks)
that may be relevant to the system. For each interval I, define a capability profile as a function

                                              CapS (I) : G → V,

where CapS (I)(g) quantifies the system’s ability to achieve goal g (as modeled by O) when operating
in the regime represented by I. The pointwise order on VG defines a preorder:

                CapS (I)  CapS (J)     iff     CapS (I)(g) ≤ CapS (J)(g) for all g ∈ G.

Remark 868 (Regimes, evaluation protocol, and dependence on O). The phrase “regime repre-
sented by I” is intended to cover not only internal state (weights, memory, habits) but also eval-
uation conditions: the distribution of inputs encountered, the available tools, and the interface by
which success on g is measured. Formally, this dependence is pushed into the observation/evaluation
machinery O, so that CapS (I)(g) is not an abstract Platonic competence but an operational quan-
tity: it is always relative to the channel through which performance is read out and aggregated over
I. This matters in later sections on mind–world correspondence: an apparent gain in capability
can sometimes be a gain in alignment between internal representation and the evaluation context,
without a commensurate increase in underlying generality.

Remark 869 (Intuition and examples for capability profiles). A capability profile is a many-goal,
graded generalization of the idea of “competence.” For each g ∈ G (say, “solve linear equations,”
“cooperate with peers,” or “navigate a room”), the value CapS (I)(g) records how well the system
can achieve g during interval I, in the same quantale-valued language used elsewhere.
    For example, if V = [0, 1], then CapS (I)(g) can be interpreted as success probability or normal-
ized performance. If V is p-bit-valued, then CapS (I)(g) can represent simultaneous evidence for
and against competence (e.g. the system sometimes succeeds and sometimes fails in incompatible
contexts). The preorder  then formalizes the natural notion that “J is at least as capable as I”
when it is no worse on any goal in the family.

                                                    341
Remark 870 (Scope of G and “fundamentally new” capabilities). The family G should be un-
derstood as a modeling choice: it may be narrow (a benchmark suite), broad (a library of tasks
parameterized by context), or even implicitly defined (e.g. by a goal generator used in training).
In practice, “fundamentally new capabilities” correspond to strict improvements on goals that were
previously low or undefined in the relevant evaluation scheme, or to the appearance of new goals that
become salient as the system interacts with richer environments. The formalism can accommodate
either view: one may keep G fixed and track new abilities as movement from low to high values on
previously included goals, or allow G to expand over time and interpret development as the ability
to maintain performance on incumbent goals while raising performance on newly introduced ones.

Remark 871 (Why a preorder rather than a total order). Capabilities across diverse tasks are
rarely totally comparable: one system may improve at g1 while regressing at g2 . The preorder
keeps the formalism honest about partial comparability and dovetails with later value-paraconsistent
and multi-objective reasoning (Section 18). In engineering terms, this is also the right level of
abstraction for discussing tradeoffs and dependency constraints across skill acquisition [9, 8].

Remark 872 (Strict improvement and ties). Because  is only a preorder, it may identify dis-
tinct profiles as mutually comparable in both directions (i.e. ties up to the induced equivalence).
Accordingly, CapS (I) ≺ CapS (J) in Definition 221 should be read as “CapS (I)  CapS (J) and not
CapS (J)  CapS (I),” i.e. a strict increase on at least one goal without any decrease on any goal.
This notion is intentionally strong; later variants can weaken it by allowing bounded losses on a
small set of goals, which is often necessary for resource-bounded agents.

Definition 221 (Development path). A sequence of successive intervals I0 → I1 → · · · is a
development path for S if there exists a threshold θ ∈ V such that:

(a) (continuity) SCS (Ik → Ik+1 ) ≥ θ for all k;

 (b) (nontrivial growth) there exist infinitely many k such that CapS (Ik ) ≺ CapS (Ik+1 );

 (c) (enrichment bias) for typical goals g with high previous capability, CapS (Ik )(g) does not sharply
     decrease when new goals are added.

Condition (c) is qualitative; in concrete models it is replaced by a quantitative constraint (e.g.
bounded loss on a weighted set of incumbent goals).

Remark 873 (On the continuity threshold θ). The single threshold θ serves as a tunable notion of
“identity granularity”: higher θ demands a stronger form of persistence across steps, while lower
θ tolerates more drift. One can equivalently think of θ as picking out a subcategory of transitions
regarded as identity-preserving, or as a robustness margin that separates development from replace-
ment. In empirical settings, θ can be chosen to reflect how stable an external observer (or the
system itself, via self-modeling) must judge the system to be in order to treat its learning trajectory
as belonging to one continuing agent.

Remark 874 (Quantitative surrogates for enrichment bias). A common quantitative replacement
for (c) is to fix, at each step k, an “incumbent” subset Gkinc ⊆ G of goals deemed already mastered,
together with weights wk (g) emphasizing what must not be forgotten, and then require a bounded
drop such as
                                                  X                             X
 inf CapS (Ik+1 )(g)−CapS (Ik )(g) ≥ −ε or              wk (g) CapS (Ik+1 )(g) ≥      wk (g) CapS (Ik )(g)−ε,
g∈Gkinc
                                                   g∈Gkinc                        g∈Gkinc


                                                  342
interpreting subtraction and summation in whatever enrichment of V is being used. When V is
not numeric, the same idea can be phrased order-theoretically as a constraint that the restriction of
CapS (Ik+1 ) to Gkinc remains above a designated lower envelope. This connects directly to catastrophic
forgetting in continual learning, where development requires not merely acquiring new tasks but
retaining competence on earlier ones under distribution shift.

Remark 875 (Intuition: development is not mere change). Condition (a) insists that the system
remains recognizably continuous: development is not a replacement of one system by another un-
related system. Condition (b) insists that something genuinely new keeps appearing: without it, a
perfectly stable adult-like agent would count as “developing” just by persisting. Condition (c) is the
“enrich rather than erase” clause: it encodes the idea that development, in the Hyperseed sense, is
not simply optimization for a moving target but a bias toward retaining earlier competences while
acquiring new ones.
    A simple example is language learning: early competence at phoneme discrimination should not
be destroyed by later acquisition of syntax; rather, later skills should build on earlier ones. This
is also precisely where resource-bounded systems encounter tradeoffs, and why Hyperseed connects
development to attention allocation and dependency management [19, 9].

Remark 876 (Local regressions and realistic trajectories). The definition allows that between some
consecutive intervals, CapS (Ik+1 ) may fail to dominate CapS (Ik ): development paths can include
plateaus and periods of reorganization. The requirement is only that strict improvements occur
infinitely often, capturing the idea of an open-ended trajectory rather than a one-off training phase.
In practice, one may also consider softened variants of (b) that measure improvement relative to a
curriculum, or that require strict growth on a sequence of increasingly complex goal families, which
better captures development under shifting environments and expanding affordances.

Remark 877 (Self-transcendence as a special case). Hyperseed treats “self-transcendence” as a
form of development. In the present framework, a mathematically simple proxy is: self-transcendence
corresponds to development in which the self/other boundary function σI changes in a way that re-
duces conflict on the boundary (smaller ∂Self θ (I)) while preserving continuity. This is only a proxy;
richer formalizations depend on the resonance machinery (Sections 12 and 17).

Remark 878 (Why the proxy focuses on the boundary region). The boundary region ∂Self θ (I)
concentrates the system’s “ontological tension” about what counts as self. A reduction in this re-
gion (at fixed continuity) formalizes, in one clean variable, the intuition that the self becomes less
conflicted about its own scope. In experiential terms this can correspond to a shift toward non-dual
integration (Hyperseed-Concept 121); in control terms it can reduce internal contention for atten-
tional resources (Section 15); and in resonance terms it can reflect an increase in coherence across
subsystems (compare [5, 13] for broader resonance motifs).

Remark 879 (Boundary shrinkage versus capability expansion). The proxy for self-transcendence
is intentionally orthogonal to the capability preorder: a system may become less conflicted about
self/other while gaining, losing, or redistributing task capabilities. Nevertheless, in many practical
settings boundary clarification can indirectly support capability growth by reducing internal inter-
ference (fewer competing self-models) and by improving the mind–world interface through which
goals are perceived and pursued. This provides a conceptual bridge between “development” in the
skill-acquisition sense and “development” in the integration/non-duality sense: both can be viewed
as trajectories that increase coherence while maintaining sufficient self-continuity to count as the
same ongoing agent.


                                                 343
16.5    Mind–world correspondence via pattern-flow morphisms
Hyperseed’s “mind–world correspondence” is a generalized notion of world-model quality. It is
defined in terms of approximate morphisms between two pattern-flow networks: one describing
relevant entities inside the system (mind/brain organization), and one describing relevant entities
in the environment. This corresponds to Mind-World Correspondence as a core notion (Hyperseed-
Concept 112) and is aligned with the engineering view that a model is good insofar as it supports
successful prediction and control [19, 20]. A key point is that “quality” here is not identified with
any particular representational format (e.g. propositional symbols, neural features, latent-state
vectors): it is identified with the existence of a structure-preserving translation between whatever
internal units the system uses and whatever external regularities are relevant to its task-context.

Definition 222 (Internal and external pattern-flow networks). Fix a system S and interval I. Let
MS,I be a pattern-flow network on a set XS,Iin representing internal entities (states, representations,

memory items, action schemas). Let ES,I be a pattern-flow network on a set XS,I        out representing

relevant external entities (objects, events, social partners, affordances) in the environment. Both
are V-graphs.

Remark 880 (Further intuition on what MS,I and ES,I are tracking). The interval parameter
I is included to allow both networks to be context- and history-sensitive: the system’s internal
organization (what distinctions it makes salient, which memory items are active, which policies
are available) may change over time, and the relevant external “world” being tracked may likewise
shift (lighting changes, new interlocutors appear, different tools become available). Treating MS,I
and ES,I as V-graphs emphasizes that “edges” encode graded strengths of pattern-flow rather than
binary relations: the same pair of nodes can have weak, moderate, or strong flow depending on the
circumstances and on the semantics of V.

Remark 881 (Intuition: why two networks?). The internal network MS,I describes how patterns
propagate within the system’s own representational economy: which internal tokens lead to which
others. The external network ES,I describes how patterns propagate in the environment as the
system experiences or models it: which external events lead to which others, which affordances follow
which contexts, and so on. By keeping these separate, Hyperseed avoids the simplistic assumption
that the system’s internal vocabulary is already “the same as” the world’s vocabulary.
    A simple example is a robot with an internal node heat warning and an external node high temperature.
The system may need to learn a correspondence between these nodes even if their internal causal
neighborhoods differ in detail. The value of this definition is that it sets up the exact mathematical
situation in which a correspondence morphism can be sought.

Remark 882 (Many-to-one, partiality, and re-encoding). Nothing in the setup requires f to be
injective: distinct internal states can legitimately map to the same external entity when the system
uses multiple internal encodings (e.g. a fast heuristic feature and a slower deliberative concept) that
nevertheless pick out the same worldly regularity. Conversely, a single internal node may correspond
only coarsely to a cluster of external nodes; in practice this is handled either by allowing XS,Iout to

contain suitably coarse-grained external entities (equivalence classes, macro-objects) or by viewing f
as selecting a task-relevant proxy in the environment graph. If one wants to model representational
“gaps” explicitly, one can also interpret the supremum over f as ranging over maps defined on a
chosen subset of XS,Iin (with the subset-selection encoded into the domain), but the present definition

keeps the interface simple and delegates such choices to goal-conditioning below.



                                                 344
Definition 223 (Mind–world correspondence score). The mind–world correspondence score of S
on interval I is                        _
                       MWCS (I) :=              deg(f ; MS,I , ES,I ).
                                                in →X out
                                            f :XS,I  S,I

We say that S has θ-mind–world correspondence on I if MWCS (I) ≥ θ.
                                         W                                                 W
Remark 883 (About the supremum              and what is being optimized). The operator       is the
join/supremum in the order on V (or, when V is numerical, simply the least upper bound). Con-
ceptually, MWCS (I) is an “optimal achievable” alignment score: it asks for the best interpretive
translation f available, rather than committing a priori to a particular hand-chosen  W decoding of
internal states. When the set of candidate
                                      W       maps is finite (e.g. finite node sets),  reduces to a
maximum; in more general settings,      expresses that correspondence is defined by an optimization
principle even when a maximizer may not be unique (or may only be approached). This choice
matches the intended role of MWCS (I) as a capability-like quantity: a system should not be penal-
ized for having multiple equally good internal codings of the same external structure.
Remark 884 (How deg(f ; MS,I , ES,I ) should be read). The degree deg(f ; MS,I , ES,I ) measures
how well the translation f preserves pattern-flow constraints from the internal graph to the external
graph. Operationally, it can be read as the largest q ∈ V such that f is a q-approximate morphism (in
the sense used throughout the pattern-flow formalism): higher q means that whenever there is strong
internal flow from x to x0 , there is correspondingly strong external flow from f (x) to f (x0 ). This
is why MWCS (I) is naturally interpreted as “world-model quality”: it evaluates whether internal
dynamics can be soundly reinterpreted as statements about the environment, rather than merely
being internally coherent.
Remark 885 (Intuition and examples for MWCS (I)). The score MWCS (I) is the best achiev-
able degree to which internal pattern-flow can be interpreted as external pattern-flow. It asks: is
there a translation f from internal tokens to external tokens such that internal edge-structure (flow
regularities) survives under interpretation?
    For example, if internally the system has a rule-like flow see red → stop and externally there is
a flow red light → cars stop, then a map sending see red 7→ red light and stop 7→ cars stop
will score highly when these flows align. The usefulness is that correspondence becomes a measurable,
composable quantity that can feed into capability profiles and control policies, without requiring
perfect isomorphism between mind and world. A further advantage is that the criterion is inherently
relational: it does not demand that individual nodes be “correctly named” or that internal tokens
have any privileged semantics in isolation; it only demands that the transition/implication structure
among tokens can be matched to a transition/implication structure among worldly entities.
Remark 886 (Goal-conditioned correspondence). Hyperseed notes that mind–world morphisms
are often strongest on the subgraphs most relevant to the system’s active goals. A convenient
formalization is to use a goal-dependent node-filter Ug,I ⊆ XS,I in and V            out
                                                                              g,I ⊆ XS,I representing the
internal/external entities relevant to goal g on I. Define
                                            _                                     
                       MWCS (I; g) :=              deg f ; MS,I |Ug,I , ES,I |Vg,I .
                                         f :Ug,I →Vg,I

The family g 7→ MWCS (I; g) can be used as one component of the capability profile CapS (I).
In many systems, the filters Ug,I and Vg,I can be understood as formal counterparts of attention
and state-abstraction: they specify which internal distinctions the system is actually deploying,
and which external distinctions matter for success, for the particular goal and time window under
consideration.

                                                    345
Remark 887 (Why goal-conditioning is philosophically natural). What counts as a “relevant”
portion of the world is not fixed; it is indexed by purpose, attention, and action (Hyperseed-Concepts
??, 60, 87). Goal-conditioned correspondence makes this indexicality explicit, preventing the notion
of world-model quality from silently smuggling in an observer-independent ontology. In Russell’s
idiom, it avoids treating “the world” as a single completed totality; it treats it as a structured field
carved by inquiry and action. Put differently, it treats correspondence as a relation between an
agent’s operative semantics and a task-salient slice of environmental structure, rather than as a
once-and-for-all alignment between two complete descriptions.
Lemma 4 (Transport of predicted flow under correspondence). Assume V is ordered so that larger
values mean “stronger flow”. Let f : XS,I in → X out be a q-approximate morphism from M
                                                S,I                                     S,I to
                                       0
ES,I . Then for all internal nodes x, x ,
                                 MS,I (x, x0 ) ⊗ q ≤ ES,I (f (x), f (x0 )).
In particular, if the system uses MS,I as a predictive model of external flow (under the interpretation
f ), then the correspondence degree q provides an explicit lower bound on the predicted external flow
strength.
Remark 888 (What this lemma says and why it is important). The lemma is the operational heart
of mind–world correspondence: it says that an approximate morphism is exactly the kind of object
that allows the system to transport predictions from internal dynamics to external dynamics. If
q is high, then strong internal flow MS,I (x, x0 ) guarantees strong external flow between the inter-
preted nodes; if q is low, the guarantee weakens accordingly. This makes correspondence actionable:
the score is not merely a descriptive similarity measure, but a quantitative certificate about which
inferences made in the internal model remain valid (up to degree q) when read as claims about the
environment. It also clarifies why ⊗ appears: the same conjunction-like operator that combines
evidence or flow within the V-semantics is used to discount internal strength by the quality of the
interpretation.
Remark 889 (Practical reading: robustness, calibration, and failure modes). When MWCS (I) is
low, the system may still exhibit rich internal dynamics, but those dynamics do not reliably “latch
onto” the environment: internal transitions may correspond to spurious correlations, hallucinated
causal links, or purely self-referential loops. When MWCS (I) is high only for certain goals g, the
system may be well-calibrated in domains it actively trains on or attends to, while remaining poorly
grounded elsewhere; this matches the empirical observation that competent behavior can be highly
domain-local. In design terms, raising correspondence can be pursued either by improving MS,I
(learning better internal predictive structure), improving ES,I (using a better external abstraction
of the environment), or improving the map f (learning a better grounding/decoder); the definition
is agnostic about which of these is the appropriate intervention.
Remark 890. This connects back to Section 14: prediction and control require not just a model,
but a way to interpret model-variables as world-variables. Here that interpretive act is formalized
as f , and its reliability is summarized by q. In particular, f plays the role of an “observational
semantics” that turns internal distinctions (nodes and edges in the internal pattern-flow network)
into externally meaningful distinctions (nodes and edges in the world pattern-flow network), so that
claims like “x tends to lead to x0 ” can be transported to claims like “f (x) tends to lead to f (x0 ).”
The scalar (or truth-degree) q is then a single, uniform lower bound on how well this transportation
preserves edge-constraints across all internal pairs, thereby separating the questions “what is the
agent internally representing?” (encoded by MS,I ) and “how accurate is that representation when
interpreted externally?” (encoded by q and f together).

                                                   346
Proof. Immediate from the definition of q-approximate morphism. More explicitly: the statement
of the lemma is exactly the defining inequality (or its equivalent reformulation via the degree
deg( · ; · , · )), so no additional construction is required beyond instantiating the definition with the
particular internal and external edge-structures under discussion.

Remark 891 (Proof sketch and intuition). Proof sketch. Unpack the definition: q ≤ deg(f ; MS,I , ES,I )
is equivalent to MS,I (x, x0 ) ⊗ q ≤ ES,I (f (x), f (x0 )) for all x, x0 . Here ⊗ is the monoidal product
of the underlying truth-value/weight structure (e.g. a t-norm in a fuzzy setting, multiplication in a
probabilistic-weight setting, or ∧ in an order-theoretic setting), and ≤ is the corresponding entail-
ment/order on edge-weights; thus the inequality states that “internal support, discounted by q, is
never stronger than the external support after interpretation.”                                        
    There is no further trick: the lemma simply names, in predictive language, the inequality that
constitutes “being an approximate morphism.” Geometrically, q is the uniform amount by which
internal edge strengths may be discounted so that the interpreted edges fit inside the world graph.
Equivalently, q can be read as a global safety margin: if q = 1 then f is fully structure-preserving at
the level of edge-weights (an exact morphism in the chosen enrichment), while smaller q quantifies
how much one must “shrink” internal claims to guarantee external validity. This is useful when
internal edges encode strong expectations or control-relevant dependencies that are only partially
realized in the world: the same f may remain meaningful even as conditions change, by lowering q
to reflect reduced reliability rather than abandoning the interpretive mapping entirely.

Remark 892 (Why this is a useful notion of “world model”). A classical world model in AI typically
consists of: (i) a representational vocabulary for external states, and (ii) a transition/prediction
structure on that vocabulary. Mind–world correspondence adds two important generalizations: (1) it
does not assume the internal vocabulary matches the external one; and (2) it measures fidelity by the
existence of an approximate structure-preserving map, not by equality of probability distributions.
This is well-suited to observer-relative modeling and to cases where multiple incompatible models
coexist (paraconsistency). One consequence is that the internal model may be coarser (many-to-one)
or refined (one-to-many, via auxiliary internal distinctions) relative to the world description, and
the framework still assigns a clear quantitative notion of adequacy: the question becomes whether
there exists an f that makes the internal transition claims conservatively true about the world, up to
the uniform slack q. In contrast, equality (or close match) of full distributions typically presupposes
a shared event space and a shared semantics of state variables; here those assumptions are replaced
by an explicit correspondence map. Moreover, the approximate-morphism criterion aligns with the
practical role of a model in control: for action selection, one often needs sound (non-overconfident)
predicted constraints more than perfectly calibrated probabilities, and the inequality MS,I (x, x0 ) ⊗
q ≤ ES,I (f (x), f (x0 )) is exactly such a soundness condition after interpretation. When the agent
maintains multiple internal descriptions that disagree, paraconsistency becomes manageable because
each description can be paired with its own (f, q) witness of partial correspondence, rather than
forcing premature reconciliation into a single globally consistent probabilistic account.

Remark 893 (Relation to transfer and abstraction). The use of a morphism f as an interpretation
map parallels the role of representation mappings in transfer learning: one succeeds by finding a
structure-preserving translation between domains. Hyperseed’s stance is that “modeling the world” is
itself a transfer problem between internal and external pattern-flow networks [7]. This also clarifies
why mind–world correspondence is a natural ingredient in general intelligence: it is the quantita-
tive form of “having the right abstractions” (Hyperseed-Concept 51). Concretely, if an agent has
learned an internal pattern-flow network in a latent space (shaped by its sensors, embodiment, or
prior tasks), then applying that competence to a new environment requires a map f that aligns latent

                                                  347
nodes and transitions with externally meaningful ones; the parameter q then measures how much
of the learned relational structure survives that alignment. In this sense, abstraction is not merely
discarding detail, but creating internal variables whose induced transition structure admits a high-q
morphism into a broad class of world-structures. This viewpoint also supports compositionality:
when correspondences can be chained (e.g. internal → intermediate → external), one can interpret
successive abstractions as composing morphisms, where the effective reliability degrades in a con-
trolled way (typically through the monoidal product of the respective q values). Such compositional
degradation formalizes an intuitive fact about transfer: each additional representational “gap” may
introduce some loss, but good abstractions are exactly those for which the loss remains bounded and
predictable across contexts.

16.6    Space as a structure on which correspondences are defined
Hyperseed uses “space” in a broad sense: not only physical space, but also conceptual/semantic
spaces on which similarity, neighborhood, and correspondences can be formulated. A pattern web
already induces a notion of distance/similarity between entities. Here we package the minimal
structure needed for correspondence-based reasoning. This connects to Space as a core notion
(Hyperseed-Concept 173) and to the general idea that similarity is not merely geometric but can
be representational and process-relative.
    In particular, the relevant “space” may be tied to a task, a sensorimotor loop, or a model
class: two entities can count as “near” when they are hard to distinguish by the agent’s available
measurements, when they afford similar actions, or when they play the same role in a recurrent
process (even if they are far apart geometrically). This makes the choice of space part of the
agent’s theory of what distinctions matter, and it is precisely these distinctions that later support
self/world separation and the persistence of identity across time.

Definition 224 (Enriched spaces). A V-space is a V-category S (objects with V-valued hom/similarity)
together with a chosen scalarization k · k : V → [0, ∞]. The induced extended pseudo-metric on ob-
jects is
                                        dS (a, b) := S(a, b) .
Depending on V and k · k, this may behave like a similarity, a cost, or a distance.

    A useful way to read Definition 224 is as a separation between (i) a compositional notion of
comparison, encoded by enrichment (how comparisons compose along paths), and (ii) a numerical
projection used for heuristics, thresholds, and optimization. The enrichment supplies the analogue
of a “triangle inequality” at the V-level (via composition in the V-category), while the scalarization
supplies a computable summary. In applications, the scalarization is often chosen to be monotone
and to respect the intended direction of comparison (e.g. “larger in V means more similar” versus
“larger means more costly”), but the definition is deliberately permissive: the agent may carry
multiple scalarizations for different downstream uses (planning, clustering, anomaly detection), all
over the same underlying enriched structure.

Remark 894 (Intuition and examples for V-spaces). A V-space is an enriched generalization of a
metric space: instead of real-valued distances, we have V-valued comparisons S(a, b). If V = [0, ∞]
ordered oppositely and ⊗ is addition, then one recovers the Lawvere view of generalized metric
spaces; if V = [0, 1] with ⊗ = min one obtains a fuzzy similarity space.
    The scalarization k · k then turns enriched similarities into an ordinary extended pseudo-metric
dS that can be used for numerical reasoning (e.g. nearest neighbors), while preserving the option
to work directly in V when composability is more important. This is useful because correspondence

                                                 348
reasoning often needs both: categorical structure for compositional semantics and scalar distances
for optimization.

    One practical intuition is that S(a, b) can encode typed or structured evidence of relatedness
that would be lost by prematurely collapsing to a number. For instance, V could record not only
a magnitude but also the “mode” of similarity (perceptual, functional, linguistic), or it could be a
product quantale that combines independent channels of evidence. Scalarization then becomes an
explicit design choice: when projecting to [0, ∞], one decides how to trade off these channels, which
in turn affects what the agent treats as stable identity versus incidental variation. This makes it
easier to state, within the same formalism, both (a) hard correspondences induced by strong and
consistent evidence, and (b) soft correspondences that are provisional and revisable.
    It is also important that dS is only required to be an extended pseudo-metric: distinct objects
may have zero distance (indistinguishability at the agent’s resolution), and distances may be infinite
(no meaningful comparison available). Both behaviors occur naturally in developmental settings,
where early representations may collapse many distinct world states, and later refinement splits
them as new sensors, concepts, or actions become available.

Definition 225 (Correspondence space). Let M = (X in , M ) and E = (X out , E) be V-graphs.
A correspondence space for (M, E) is a V-space S together with maps i : X in → Ob(S) and
e : X out → Ob(S). The pair (i, e) induces a V-valued correspondence relation

                         RS (x, y) := S(i(x), e(y))     (x ∈ X in , y ∈ X out ).

    This definition is intentionally weak: i and e need not be injective (multiple tokens can be
embedded to the same point of S, representing aliasing or abstraction), and they need not preserve
any structure beyond whatever regularities are captured by the induced relation RS . In particular, i
and e can be read as representation functions: they say how the agent chooses to represent internal
items and external items in a common comparison medium. When these representation functions
change over time (learning, sensor drift, concept acquisition), the correspondence space view still
applies by treating i and e as time-indexed families, so that development becomes movement (or
re-embedding) within a stable S, or else co-development of S itself.

Remark 895 (Intuition: an interlingua for comparison). The correspondence space S plays the
role of a shared medium in which internal and external entities can be compared. The maps i and e
embed internal tokens and external tokens into this medium, and RS (x, y) then measures how well
internal token x matches external token y in the space.
    For example, if S is ordinary physical space, then i may map internal body-schema tokens to
physical locations and e may map external objects to their locations, making correspondence spatial.
If S is a semantic embedding space, then i and e may map tokens to vectors, making correspondence
conceptual. The utility of this definition is that it supports a third mode of correspondence reasoning:
not only by direct morphisms f , but also by metric/neighbor structure in S (Hyperseed-Concept 59).

    The “interlingua” reading is especially apt when internal and external tokens have different
native structures (different feature vocabularies, different temporal granularities, different modali-
ties). Rather than forcing a direct alignment X in ↔ X out , one chooses S so that the agent can ask
meaningful comparative questions: Which external candidates lie in the neighborhood of an internal
hypothesis? Which internal states cluster around the same external referent? Which correspon-
dences remain stable under small perturbations of sensors or attention? These are neighborhood
questions, and they can be answered even when no single crisp morphism is yet justified.


                                                  349
Remark 896 (Interpretation). A correspondence space provides an “interlingua” in which internal
and external entities can be compared. When S is physical space (or spacetime), i and e may repre-
sent embodied localization. When S is a conceptual space, i and e encode semantic embeddings. In
either case, approximate morphisms M → E can be seen as arising from (or inducing) regularities
in RS .

    One can also regard RS as a field of constraints that guides the search for morphisms. A high-
quality morphism f typically selects, for each x ∈ X in , an output f (x) lying in a high-similarity
region of the slice y 7→ RS (x, y), while also respecting relational constraints coming from the
edges/flows of M and E. Conversely, if repeated successful morphisms are found over time, they
provide empirical pressure to adjust i, e, or S so that the corresponding pairs become nearer, i.e.
so that the interlingua becomes better adapted to the agent’s world.

Remark 897 (Why introduce correspondence spaces if we already have morphisms?). The mor-
phism view (f with degree q) is crisp and compositional, but it chooses a single matching. A corre-
spondence space supports softer, many-to-many relations: one can represent ambiguity and polysemy
as neighborhoods rather than as a hard assignment. This is especially important in paraconsistent
settings, where it may be rational for a system to retain multiple incompatible correspondences until
further evidence or action resolves them [24, 23].

    In addition, the correspondence-space view makes explicit room for partial alignment. When
the agent only knows how to compare some internal tokens to some external tokens (because other
tokens are newly formed, occluded, or not currently observable), a crisp morphism may be forced
to guess, whereas RS can simply remain diffuse or uninformative on those pairs. This matters
for continuity of self-models: the agent can maintain a persistent “core” alignment (e.g. body
schema) while leaving peripheral correspondences unresolved, thereby avoiding the need to collapse
uncertainty into premature commitments.

Example 14 (A minimal embodied correspondence sketch). Consider a toy agent with internal
nodes X in = {body, pain, reach} and external nodes X out = {arm, heat, cup}. Suppose M encodes
the internal regularity “pain follows heat-on-body” and “reach tends to precede cup-in-hand,” while
E encodes the external regularity “heat tends to follow contact between arm and heat source” and
“cup-in-hand tends to follow reaching.” A correspondence map f sending body 7→ arm, pain 7→
heat, and reach 7→ reach (if a matching external token exists) will have high degree precisely
when these flow regularities align. The same data can be represented by a correspondence space S
in which body and arm are close, pain and heat are close, and so on.
    In such examples, the self/other boundary (Section 16.1) can also be grounded: body tends to be
a persistent, highly self-evidenced node, while cup is typically other-evidenced, and pain may live
on the paraconsistent boundary (both “me” and “not-me”).

    To connect this sketch to continuity and development: if the agent experiences repeated episodes
in which reach is followed by cup-contact and then by proprioceptive changes in arm, the neighbor-
hood structure in S can support a stable triangulation between intended action, observed outcome,
and body state. On this reading, “self” corresponds not to a single node but to a region (or
subspace) of S that is repeatedly implicated by high-confidence internal–external correspondences
across time, while “other” corresponds to regions that are only indirectly predictable or only spo-
radically coupled. This also clarifies how paraconsistency can be localized: incompatible evidence
can be retained as multiple nearby candidates in S (a multi-modal neighborhood) until interaction
reduces the ambiguity.


                                                350
Remark 898 (Reading the example as a miniature theory of embodiment). The example shows
how embodiment can be described without reducing “mind–world matching” to direct identity of
variables. The correspondence f is justified not because pain and heat are the same thing, but
because their relational roles in their respective networks align. In particular, what matters is
that the incoming and outgoing constraints of the nodes (how they co-vary with other nodes, what
they modulate, and what they are modulated by) are preserved up to the tolerance encoded by the
enrichment: the match is a claim about structural position in a web of dependencies, not about
shared intrinsic labels. This is precisely the structuralist spirit behind the morphism definitions. At
the same time, the mention of the boundary illustrates how “self ” is not merely the set of internal
nodes: it is the subset that the system treats as self-evidenced, potentially with a nontrivial boundary
region, echoing Self vs. Other (Hyperseed-Concept 165). One can read the “boundary region” as
the locus where evidence is mixed or contested (e.g. partially self-generated and partially externally
driven), so that self/other is not a crisp partition but a graded or even paraconsistent classification
that can still support stable control policies. On this reading, embodiment is the practical situation
in which the system must maintain a workable correspondence despite such mixed provenance, and
the morphism formalism supplies a way to state when the correspondence is coherent enough to
guide action.

Summary of Hyperseed concepts handled in this section. The constructions above provide
rigorous handles for:

• Self/other boundary: a (possibly paraconsistent) self-evidence function and induced self/other
  groupings. Here the function operationalizes “what counts as mine” as a rule for tagging states
  or flows, while allowing inconsistent or context-sensitive tagging without collapse.

• Self-continuity: existence (and degree) of high-weight approximate morphisms between succes-
  sive internal pattern-flow networks. The weight (or enrichment value) makes continuity a matter
  of degree rather than an all-or-nothing identity, which matches the phenomenology of gradual
  change, interruption, and recovery.

• Relative-information self-continuity: proximity of time-slice networks under a scalar diver-
  gence. This provides a complementary summary statistic that can be compared across systems
  or scales, even when explicit node-to-node matching is underdetermined.

• Reflective self-continuity: flagged here, and developed further in Section 17 using self-model
  recursion. The key additional requirement is that some of the preserved structure is explic-
  itly about the system’s own continuity claims (i.e. meta-representations that constrain future
  updates).

• Development: continuity plus expanding capability profile. In the present language, capabil-
  ities correspond to families of morphisms or controlled transformations that become available,
  so development can be tracked as an enlarging repertoire together with sufficient diachronic
  coherence.

• Pattern flow networks and mind–world correspondence: approximate morphisms be-
  tween internal and external flow networks. This treats “aboutness” as a map between relational
  structures (the dynamics of internal patterns and the dynamics attributed to the world), rather
  than as a static lookup table of symbols.




                                                  351
• Space: an enriched correspondence space on which mind/world embeddings can be compared.
  Concretely, this is the arena in which different candidate correspondences (or embeddings) can
  be measured against one another, so that “spatial” comparison is recovered as comparison of
  mappings by their induced distortions, costs, or constraint-violations.

Remark 899 (How these pieces compose with the rest of the document). Self/other boundary
feeds into attention and control by determining what is treated as “inside” the locus of action (Sec-
tions 15 and 14). This matters because downstream optimization and resource allocation typically
presuppose a boundary: credit assignment, risk attribution, and intervention selection all depend
on which variables are treated as under the agent’s remit versus merely observed. Self-continuity
and development provide the diachronic scaffold needed for later discussions of reflective will and
consciousness (Section 17), where closure and self-reference become explicit. In particular, with-
out a notion of “same system over time” (even only approximately), recursive self-modeling would
have no stable target, and reflective endorsement would be ill-posed. Mind–world correspondence
is the bridge from internal pattern dynamics to external prediction and intervention, providing a
quantale-valued measure of model adequacy that remains meaningful under vocabulary drift and
paraconsistent evidence [19, 20]. The quantale-valued aspect is what allows adequacy to be aggre-
gated and compared even when evidence is multi-graded or partially ordered (e.g. different kinds
of constraint satisfaction that do not collapse to a single probability), and the paraconsistent tol-
erance is what prevents isolated contradictions from trivializing the evaluation. In this sense, the
same enriched structure that supports “space” as a comparison domain also supports robustness
of correspondence across re-parameterizations, relabelings, and incremental revision of the internal
vocabulary.


17     Consciousness, reflective will, and autonomy
17.1    Orientation: what gets formalized here
By this point in the reconstruction we have: (i) paraconsistent p-bit evidence values and a p-bit-
quantale substrate (Section 3, especially Sections 3.2–3.4); (ii) pattern webs and habit dynam-
ics (Sections 11–12); (iii) mind/representation/perception and semiotic modes (Section 13); (iv)
prediction/control and temporal composition (Section 14); (v) attention and synergy as resource-
allocation over competing processes (Section ??); and (vi) self/continuity as a context-dependent
boundary and a constraint on self-model evolution (Section 16).
    Hyperseed’s consciousness layer is not introduced as a new primitive, but as a closure phe-
nomenon involving:

• global accessibility of some representational content (“what is present to experience”),

• integration/coherence across multiple subsystems (often mediated by resonance),

• self-reference in the weak (non-explosive) sense appropriate to paraconsistent settings,

• and control leverage: conscious contents can steer attention and action.

The goal of this section is to pin down a small mathematical interface for these ideas that is
compatible with: (1) observer-relativity; (2) paraconsistency; and (3) resource sensitivity.
    What is meant by “small interface” is that we are not trying to axiomatize everything that
could be called conscious life, but to isolate the minimal structural commitments that let the
earlier pieces talk to each other in a recognizably “conscious” regime. Concretely, the earlier

                                                352
machinery already provides (a) a semantics of graded, possibly inconsistent evidence; (b) a dynamics
in which patterns stabilize into habits; and (c) an attentional scheduler that allocates limited
computational and behavioral bandwidth. The present task is to specify when these ingredients
collectively implement a globally available, integrated, self-involving representation that also has
downstream causal consequences for control. In other words, consciousness will be treated as a
particular kind of functional closure in the agent’s ongoing inference–attention–action loop, rather
than as an extra ontological ingredient.
    It is important that all four bullets above are intended to be read in a way that respects para-
consistency. “Global accessibility” does not mean that all modules agree, or that a single classical
“belief state” is broadcast without contradiction; rather, it means that certain representational
items become accessible as shared constraints across multiple processes even when those processes
maintain divergent or locally inconsistent p-bit valuations. Likewise, “integration/coherence” is not
synonymous with full logical consistency: it is closer to the notion that, at the level relevant for
control and report, the system achieves a stable working alignment between competing evidence
streams, typically via resonance or other synergy mechanisms introduced earlier. A system can
therefore exhibit conscious access to a content while still containing unresolved tensions (e.g., com-
peting interpretations of the same stimulus), and the formalism must allow such tensions to be
represented without collapse into triviality.
    The emphasis on “control leverage” also ties this section to the forthcoming themes of reflective
will and autonomy. A content is not merely conscious because it is present in some inner arena; it
is conscious, in the present reconstruction, to the extent that it participates in the causal economy
that selects policies, re-allocates attention, and reshapes habits. This point matters because the
step from consciousness to autonomy is not made by adding a new faculty, but by showing how
globally accessible and self-referential contents can modulate the very mechanisms that generate
future attention distributions, action tendencies, and self-model updates. In this sense, reflective
will is anticipated here as a special case of control leverage: the system can represent not only
world-directed contents, but also the structure of its own decision situation (including conflicts,
constraints, and higher-order preferences), and thereby change what it will do next under resource
limitations.
    Observer-relativity enters at two levels. First, “what is present to experience” is not treated
as an absolute, system-independent predicate, but as indexed to a modeling context: different
observers (or different internal meta-models) may disagree about which contents are globally ac-
cessible, or even about the granularity at which “contents” are individuated. Second, the closure
phenomenon itself is evaluated relative to a chosen decomposition into subsystems and channels
(perception, memory, valuation, motor control, etc.), so that the same underlying dynamics can
be described at multiple scales. This is aligned with the earlier treatment of self/continuity as
context-dependent: the boundary of “the experiencing system” and the boundary of “the con-
scious workspace” need not coincide, and both are subject to pragmatic constraints from modeling
and control.
    Resource sensitivity is similarly not an afterthought but a defining constraint. Global acces-
sibility cannot be taken to mean unlimited broadcast; it must be implemented as a selective,
capacity-limited mechanism that trades off precision, breadth, and speed. Integration is likewise
bounded: coherence must be measured relative to limited attention and finite synergy budgets,
rather than as an ideal limit of perfect mutual consistency. In paraconsistent terms, this means
that the system may carry contradictions forward when the cost of resolving them exceeds the
value, and that consciousness can co-exist with such tolerated inconsistency as long as the resulting
closure remains stable enough to support coordinated action.



                                                 353
Remark 900. Philosophically, the stance here is deliberately anti-mysterian: “consciousness”
(Hyperseed-Concept 85) is treated neither as an ineffable substance nor as a mere synonym for be-
havior, but as a particular organizational closure in the dynamics of evidence, attention (Hyperseed-
Concept 60), and control. The formalism is a kind of austere Russellian bookkeeping: we do not
pretend to capture the whole phenomenology, but we insist that whatever consciousness is, it must
show up as a stable pattern in the inferential and control economy of a bounded system [1, 19].

17.2     A minimal interface: evidence states, workspace closure, and access
17.2.1    Languages and evidence states
Fix an observer/context Ob (a mind, or mind-plus-reality slice). Let LOb be a finite (or at least well-
founded) set of propositions the observer can represent at the current level of modeling granularity.
Elements of LOb may include:

• world propositions, e.g. “there is an apple on the table”;

• bodily propositions, e.g. “the left arm is moving”;

• internal propositions, e.g. “I feel tension” (self-report tokens in the sense of Section 13);

• relational propositions, e.g. “A tends to lead to B” (predictive implication from Section 14).

Definition 226 (p-bit evidence state). An evidence state for Ob is a map

                     E : LOb → V = [0, 1]2 ,      ϕ 7→ E(ϕ) = (E + (ϕ), E − (ϕ)).

We order evidence states pointwise by the componentwise order on V.

Remark 901. Intuitively, an evidence state is the observer’s current “epistemic posture” toward
each representable proposition: E + (ϕ) is how much support there is for ϕ, while E − (ϕ) is how much
support there is for “not-ϕ”. The crucial choice is that we store both numbers explicitly rather than
forcing them to sum to 1 (as in ordinary probability) or to be mutually exclusive (as in classical
truth values). This is the p-bit move from earlier sections, aligned with constructive/paraconsistent
semantics such as those explored in paraconsistent logics and their computational interpretations
[23, 24].
    A simple example is a tiny language LOb = {ϕ, ψ} where E(ϕ) = (0.9, 0.1) (strongly supported)
while E(ψ) = (0.7, 0.8) (both supported and opposed). The latter represents a situation of genuine
tension: the system has substantial evidence on both sides. The pointwise order means that E ≤ E 0
precisely when every proposition has no less positive evidence and no less negative evidence in E 0
than in E; i.e. E 0 is, in this formal sense, “more evidenced” than E. This definition is useful
because it makes the space of epistemic states into an ordered structure well-suited to monotone
“closure” operators and fixed-point reasoning later in the section.

Remark 902 (Paraconsistency is a feature). Allowing (E + (ϕ), E − (ϕ)) with E + (ϕ) + E − (ϕ) > 1
is essential to modeling: (1) borderline predicates (“soggy predicates” in Hyperseed’s terminology;
Hyperseed-Concept 172); (2) perceptual conflict (ambiguous or adversarial signals); (3) value con-
flict (next section; Hyperseed-Concept 198); and (4) self-referential modeling without explosion.

Remark 903 (Granularity and well-foundedness). The “finite (or at least well-founded)” condition
on LOb is not intended to deny that agents can in principle form arbitrarily complex thoughts, but
to delimit a current workspace-level interface at a given moment of modeling. In practice, LOb

                                                 354
can be taken as the set of propositions currently expressible in the agent’s active representational
scheme (including compressed, schematic, or indexical propositions), while the well-foundedness
assumption is what makes iterative closure constructions converge rather than chasing an infinite
regress of ever-finer re-representations. This also matches the intended use of evidence states as
interfaces: they summarize what is currently at stake for the agent, not an exhaustive ontology of
the world.

17.2.2   Subsystem reports and attention-weighted integration
Let M be a finite index set of concurrently running subsystems/modules for Ob (perception streams,
memory retrieval, imagination, verbal thought, somatic monitoring, etc.). Each module produces
its own evidence state.
Definition 227 (Module evidence and attention weights). For each m ∈ M, let
                                           Em : LOb → V
be the evidence state generated by module m. Let a : M → [0, 1] be an attention allocation, with
a(m) interpreted as the fraction of available cognitive resource dedicated to m (cf. Section ??).
Remark 904. This definition separates two things that are often conflated in informal discussion:
(i) what a module computes (its evidence state Em ), and (ii) how much the system is currently
“listening” to that module (the allocation a(m)). A classical cognitive-science picture might call
this a distinction between local processing and global broadcast; Hyperseed frames it in terms of
genenergy bottlenecks and attentional focus (Hyperseed-Concept 60) [19].
    As a small example, one can imagine M = {vision, memory} and a proposition ϕ = “there is a
cat”. Vision might output Evision (ϕ) = (0.8, 0.2) while memory, primed by a recent cat discussion,
outputs Ememory (ϕ) = (0.6, 0.4). If attention is mostly on vision, say a(vision) = 0.9, then vision
dominates the integrated story; if attention shifts to memory, the integrated state changes without
any change in the modules’ intrinsic computations. This is useful because it gives a precise handle
on the idea that “conscious content depends on attention” without reducing either to the other.
    To combine module reports we use the p-bit-quantale operations. We need a way to treat a real
attention weight as a quantale element.
Definition 228 (Scalar embedding into p-bit values). For α ∈ [0, 1] define its diagonal embedding
into V by
                                    α := (α, α) ∈ [0, 1]2 .
Remark 905. The diagonal embedding is the simplest way to regard a scalar “strength” α as
affecting both positive and negative evidence magnitudes uniformly. It is not the only possibility,
but it is the most conservative: α is treated as a resource-like multiplier rather than as a truth-
value bias. For instance, 0.5 ⊗ Em (ϕ) will (given the p-bit-quantale tensor from Section 3.4) act
like scaling down the module’s contribution in a symmetric way.
Remark 906 (Why uniform scaling is the right default). Uniform scaling is appropriate when
attention is interpreted as bandwidth or gain rather than as valence. In that reading, allocating
less attention to a module reduces the magnitude of whatever it would have contributed, regardless
of whether that contribution is for or against a given ϕ. This matches the intended role of attention
in a minimal interface: it gates access to the workspace rather than directly changing the module’s
internal epistemic stance. More expressive embeddings (e.g. scaling E + and E − differently, or
mixing them) can be treated as additional modeling assumptions about bias, framing, or motivated
cognition, but are not required for the basic global-workspace story developed here.

                                                355
Definition 229 (Attention-weighted integration (pre-closure)). Given module evidence states {Em }m∈M
and attention weights a, define the integrated pre-closure evidence state Epre by
                                       M
                         Epre (ϕ) :=        a(m) ⊗ Em (ϕ),       ϕ ∈ LOb ,
                                        m∈M

where ⊕ and ⊗ are the p-bit-quantale join and tensor (Section 3.4), applied pointwise over LOb .

Remark 907. The choice of ⊕ in the integration step implements a minimal “accumulation of
support” picture: the workspace-facing state records whatever evidence is currently contributed by
any attended module, without forcing premature reconciliation of conflicts. Because ⊕ is monotone
and associative, increasing attention to a module or strengthening a module’s own evidence state can
only move Epre upward in the pointwise order (i.e. toward “more evidenced”). This monotonicity is
one of the reasons for setting the interface up in an order-theoretic way: it ensures that later closure
steps (which will also be monotone) can be studied using fixed-point and convergence arguments
rather than ad hoc case analyses.                       P
     Note also that no normalization condition such as m∈M a(m) = 1 is required for the definition
to make sense: a(m) is interpreted as a resource fraction relative to a maximal per-module gain,
and the quantale operations already enforce the codomain constraint to [0, 1]2 . If one does impose
a normalization constraint, it can be viewed as an additional model of limited global resource, but
it is not logically necessary for defining Epre .

Remark 908 (Integration does not resolve contradiction). Even after integration, it is possible
(and often expected) that Epre (ϕ) has both large positive and large negative components. This is
not a bug: on the present view, “what is globally available” is not identical to “what is already
consistent”. The workspace can contain tensions (e.g. perceptual ambiguity, competing predictions,
or value conflict) and the next modeling step—workspace closure—is where inferential propagation
and constraint satisfaction are represented. Keeping contradiction visible at the interface level is
precisely what prevents the system from spuriously collapsing into a single forced narrative when
the underlying evidence is genuinely mixed.

Remark 909. This is useful because attention is meant to be a capacity allocation (genenergy
budget) more than a semantic commitment: turning down attention should reduce how strongly a
module’s results enter the global workspace, regardless of whether those results are pro-ϕ or anti-ϕ.
In later sections, one can generalize this to non-diagonal embeddings to model systematic biases
(e.g. anxiety amplifying negative evidence), but the diagonal case provides a clean baseline. In
particular, the diagonal case isolates the purely “gain control” role of attention: it scales a module’s
contribution without reinterpreting its internal polarity structure. This matters when one wants the
algebra to distinguish what is represented (the evidence values themselves) from how strongly it
competes for global access (the weight), so that attenuation can be understood as lowering broadcast
priority rather than as a change of mind about ϕ.

Definition 230 (Attention-weighted aggregation operator). Define the integrated evidence state
Γa ({Em }m∈M ) by                           M
                             (Γa E• )(ϕ) :=    a(m) ⊗ Em (ϕ),
                                                m∈M

where ⊕, ⊗ are the join and tensor of the p-bit quantale (Section 3.4), applied pointwise in ϕ.

Remark 910. Notation check: E• is a convenient “bundle” notation for the family {Em }m∈M , and
(Γa E• )(ϕ) denotes the V-value assigned to proposition ϕ after aggregating all module contributions

                                                  356
                                  L
with weights a(m). The symbol        is the quantale join over the finite index set M, and the tensor
⊗ is the quantale’s multiplicative operation; both act in V = [0, 1]2 and here are applied separately
for each proposition ϕ (“pointwise in ϕ”).
    It is helpful to keep in view the ambient order: evidence states are compared pointwise in ϕ,
and values in V = [0, 1]2 are compared componentwise (so “more evidence” means no less positive
support and no less negative support, as determined by the order specified in Section 3.4). With this
convention, both ⊕ and ⊗ are monotone in each argument, which ensures that increasing a module’s
evidence or increasing its attention weight cannot decrease the integrated result. This monotonicity
is one of the reasons for using quantale operations rather than an ad hoc averaging rule.
    The overline in a(m) is doing conceptual work: it is the embedding that turns an attention scalar
(a resource or gain parameter) into an element of the evidence-value algebra so that it can interact
with Em (ϕ) via ⊗. In the diagonal baseline, this embedding treats positive and negative channels
symmetrically, so that “listening less” to a module downweights its entire evidential profile rather
than selectively distorting one channel.
    Intuitively, Γa is a formal version of “what you get when you listen to multiple voices according
to how much attention you grant them.” A minimal example with two modules m = 1, 2 gives

                            (Γa E• )(ϕ) = a(1) ⊗ E1 (ϕ) ⊕ a(2) ⊗ E2 (ϕ).

In this two-module case one can already see the separation between within-module structure (what-
ever constraints relate Em (ϕ) across different ϕ) and between-module arbitration (implemented by
⊕ after attention-weighting). The join ⊕ should be read as an “integration” or “pooling” operation
internal to the chosen semantics: it may behave like a max-like merge, a bounded sum, or another
quantale join, but in all cases it provides a principled way of expressing that multiple sources can
contribute to the global evidential standing of the same proposition.
    The utility of this definition is compositionality: once module outputs and attention weights live
in the same algebraic setting, later “workspace closure” can be written as a map on evidence states
without having to mention the modules again. Equally importantly, Γa makes explicit what parts of
the story are architectural (the choice of M, the attention allocation a, and the integration rule)
and what parts are semantic (the evidence values that the modules compute). This distinction will
matter when comparing different hypotheses about deficits of access: e.g. whether a failure is due
to low attention (small a(m)), weak local evidence (small Em (ϕ)), or the downstream effects of
workspace dynamics (the behavior of W below).

Remark 911 (Interpretation). This makes explicit a Hyperseed-compatible picture: conscious-
accessible content is a product of representation plus attention. Low-attention modules may still
compute rich content, but it will not appear strongly in the integrated state unless it is “amplified” by
attention. One can also read this as a minimal formal analogue of the common distinction between
availability (a module has computed something) and access (that content is poised to influence
report, planning, or control): Γa converts a distributed availability profile {Em } into a single access-
oriented evidential profile by explicitly modulating each module with its current attentional gain.
On this view, attention does not create representational content; it changes which already-computed
contents become decision-relevant in the global aggregate.

17.2.3    Global accessibility and workspace closure
Hyperseed’s “conscious/unconscious” contrast can be modeled as a distinction between:

• content that is globally accessible for downstream reasoning/control/report; and


                                                  357