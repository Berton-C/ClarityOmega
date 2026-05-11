# 6 Phenomenological primitives

• Compute weakness from Ri (as an “importance-weighted failure to distinguish”).

• Represent patterns as finite constraint-sets on pairs in X, and define pattern support.

• Demonstrate “emergence” via quantale-compositional closure (transitive-like propagation of in-
  distinction).

• Define morphic resonance and anti-resonance as cross-context coupling updates on relations.

• Add a tiny resonance score demo using the paraconsistent logic → complex mapping and inter-
  ference.

Summary and Hyperseed concepts covered
This section instantiates the formal core of Section 3 in the smallest nontrivial setting. It provides
an explicit computational picture of: (i) what it means to (fail to) make distinctions in a context,
(ii) how simplicity/weakness aggregates, (iii) how a “pattern” can be a constraint that is supported
to varying degrees, (iv) how pattern structure can emerge from composition/closure, and (v) how
resonance can transmit pattern support across contexts, producing morphic resonance (and how
anti-resonance can transmit opposition, producing habit reversal).

Hyperseed concepts covered.

• Distinction; equivalence relation; contexts/aspects.

• Weakness/simplicity; compositional simplicity; pattern; emergence.

• Resonance/dissonance; morphic resonance/anti-resonance; habits (as iterated updates).

Remark 114. The point of this section is not to claim a faithful model of cognition or physics,
but to give a fully explicit microcosm in which the core algebraic moves can be seen with one
glance and checked with a calculator. In the language of Hyperseed’s initial presentation [1], we are
building a tiny “reality-system” where observer-relativity (Hyperseed-Concept 86), graded distinction
(Hyperseed-Concept 98), weakness (Hyperseed-Concept 202), pattern (Hyperseed-Concept 130), and
emergence (Hyperseed-Concept ??) appear as simple operations on a finite table.

    In particular, the “finite universe” assumption means that every object of interest can be con-
cretely enumerated. Thus,  once X is fixed, each context Ci can be treated as providing a complete
judgment table Ri (x, y) x,y∈X , i.e. a matrix whose entries live in a chosen truth-value/weight struc-
ture V . One should read Ri (x, y) as: “in context Ci , to what degree are x and y not distinguished? ”
Depending on the choice of V , this degree may be probabilistic, fuzzy, possibilistic, or (as in this
section) paraconsistent in the sense of allowing simultaneous support for and against indistinction.
    The role of the p-bit quantale is to make three operations simultaneously available and compu-
tationally transparent: (i) an order ≤ expressing when one indistinction-value is at most as strong
as another, (ii) a join (typically written ∨) expressing aggregation of evidence (“taking the bet-
ter supported indistinction”), and (iii) a monoidal product (often written ⊗) that will be used to
compose relations. Concretely, composition will take the familiar relational form
                                                 _                      
                               (R ◦ S)(x, z) =        R(x, y) ⊗ S(y, z) ,
                                                y∈X




                                                  81
so that indistinction can propagate along intermediate y’s; this is the precise sense in which a
“transitive-like” closure can be computed and inspected entry-by-entry.
    The weakness calculation is included here to make the informal phrase “failure to distinguish”
operational. Because X is finite, weakness can be written as an explicit sum (or other finite aggre-
gation) over pairs (x, y), with optional weights expressing that some confusions matter more than
others in a given task or setting. In this way, weakness becomes a scalar summary extracted from
a full table Ri , while still being sensitive to where (which pairs) the indistinction is concentrated.
This also makes it clear how one can speak of “simplicity” as a property of a context: a context is
“simple” (not because its world is objectively simple, but) because its distinction-table is coarse or
permissive in a way that reduces discriminative burden.
    Patterns enter in the most concrete possible way: as finite collections of constraints on pairs in
X that a context may or may not support. A pattern can be read as a small “theory” about which
objects should be treated as indistinct (or, depending on the constraint language chosen later in the
section, which should be treated as distinct). Because Ri is graded, pattern satisfaction is graded as
well: a pattern is not merely true/false in a context, but has a support value that can be computed
by combining the relevant table entries with the operations of V . This gives an explicit bridge
between the algebra (quantale-valued relations) and the intuitive notion of a recurring regularity
(a pattern supported by the context’s own judgments).
    The point of demonstrating emergence via closure is that even when the pattern constraints are
initially “local” (i.e. mention only a few pairs), compositional propagation can generate additional,
derived indistinction facts. In the finite setting, this is visible as new nontrivial entries appearing (or
strengthening) in the closure of Ri under ◦ (and, if taken, reflexive and/or symmetric completion),
thereby turning an initially sparse set of judgments into a richer structure. This is the toy-model
analogue of an “emergent pattern”: not stipulated as a primitive constraint, but produced by the
algebraic dynamics of the representational apparatus.
    Finally, morphic resonance and anti-resonance are introduced here as explicit cross-context
update rules. The guiding idea is that a context C1 can influence a context C2 by pushing R2
toward (resonance) or away from (anti-resonance) the indistinction-structure present in R1 . Because
everything is finite, such coupling can be written as an explicit formula (e.g. an update of the form
R2 ← f (R2 , R1 ) applied entrywise or via composition), iterated a few times, and numerically
inspected. Interpreting repeated updates as “habit” formation is then not a metaphor but a literal
iteration of a map on the space of V -valued relation tables.
    The final bullet in the outline connects this to the paraconsistent logic aspect of p-bit by show-
ing how a resonance (or interference) score can be computed even when evidence is inconsistent.
Mapping the paraconsistent implication → into complex numbers is used in the demo as a com-
pact way to encode phase-like reinforcement versus cancellation: agreement can add constructively,
while certain mismatches can subtract, producing an explicit toy example of how “dissonance” can
be more than mere absence of support. The purpose is not physical analogy per se, but a minimal,
checkable instance where opposition is not collapsed into zero and can therefore drive anti-resonant
change rather than being ignored.

5.1    Finite universe and two contexts
Let X := {a, b, c}. We consider two contexts C1 and C2 (think: two agents, or two spatial locations,
or two subsystems) that each maintain a p-bit-valued relation

                                    Ri : X × X → V,         i ∈ {1, 2},



                                                    82
where V = [0, 1]2 is the p-bit quantale from Section 3.4. Concretely, each Ri can be pictured as
a 3 × 3 table (a weighted adjacency matrix) whose entries are pairs in [0, 1]2 . Keeping X finite
makes it possible to compute closure, composition, and cross-context comparison explicitly and
transparently: every “global” quantity is obtained by finitely many ⊕-aggregations of finitely many
⊗-products.

Remark 115 (Notation unpacking). Here X ×X is the set of ordered pairs of entities, so Ri (x, y) ∈
V is a graded statement about the pair (x, y) as judged in context Ci . The symbol V = [0, 1]2 means
each value has two coordinates, typically written Ri (x, y) = (Ri+ (x, y), Ri− (x, y)). The order on V
is the componentwise order (so larger means “more evidence” in that channel), and the toy compu-
tations later implicitly use the standard p-bit quantale operations: ⊕ as componentwise maximum
and ⊗ as componentwise multiplication, with unit e = (1, 1). This is the minimal paraconsistent
evidence calculus needed for the rest of the examples. In particular, the choice of ⊕ = max means
that when multiple independent “routes” (or justifications) support a claim, the aggregated evidence
keeps the strongest available support in each coordinate rather than averaging it away, while ⊗ = ·
models attenuation along multi-step chains (products of confidences). The componentwise order
makes the induced lattice structure transparent: u ≤ v iff u+ ≤ v + and u− ≤ v − , so a value can
increase in one channel without forcing any change in the other.

Remark 116 (Two contexts as two ways of cutting the world). A context is, philosophically,
a stance: a way an observer (or subsystem) decides what differences matter. Mathematically we
encode that stance by a relation-valued table. This operationalizes observer-relativity: the same pair
(x, y) can be judged “nearly identical” in C1 and “clearly distinct” in C2 without contradiction at
the meta-level. This is one of the core motivations for paraconsistent semantics in the Hyperseed
program (Hyperseed-Concept 86, 98). One can also view Ci as fixing a measurement protocol: which
features are compared, what counts as noise, and which correlations are trusted. On this reading,
changing contexts corresponds to changing the observational interface rather than changing the
underlying set X.

Remark 117 (Interpretation of Ri (x, y)). We interpret Ri (x, y) = (Ri+ (x, y), Ri− (x, y)) as two-
channel evidence about the proposition “x and y should be treated as the same (undistinguished) in
context Ci ”:

• Ri+ (x, y) is positive evidence supporting indistinction (x ∼ y),

• Ri− (x, y) is negative evidence opposing indistinction (supporting distinction).

Paraconsistency means both channels may be simultaneously high. It is useful to emphasize that
this is not merely “probability of sameness” plus “probability of difference”; the two coordinates are
not required to sum to 1 (and generally should not), because they represent potentially independent
evidential sources. Thus (1, 1) represents maximal support and maximal opposition, i.e. a fully
conflicted or overdetermined state, whereas (0, 0) represents lack of information (neither support
nor opposition). This separation is what allows later constructions to treat agreement and conflict
as distinct, simultaneously trackable resources.

Remark 118 (A simple concrete reading). If Ri (x, y) = (0.9, 0.1) then context Ci has strong sup-
port for collapsing x and y and little opposition. If Ri (x, y) = (0.9, 0.8) then Ci is in a conflicted
state: it has strong reasons to identify and strong reasons to separate. And if Ri (x, y) = (0.1, 0.8)
then Ci is largely opposed to identifying x and y. This two-axis geometry is precisely what later al-
lows “resonance” and “dissonance” to be treated as interference-like phenomena (Hyperseed-Concept


                                                  83
159, 97). Geometrically, one can think of Ri (x, y) as a point in the unit square, with qualitatively
different regions: a “consensus-identify” region near (1, 0), a “consensus-separate” region near
(0, 1), a “conflict” region near (1, 1), and an “uninformative” region near (0, 0). Later, when we
compare contexts or compose relations along paths, these regions behave differently under ⊕ and ⊗,
which is exactly what makes the toy model nontrivial even though the underlying set X is tiny.

    For convenience we assume symmetry Ri (x, y) = Ri (y, x) and set diagonal entries to the quan-
tale unit e = (1, 1) so that diagonal paths do not attenuate relation-composition (this is an algebraic
convenience for the closure demo below). Equivalently, each Ri may be regarded as an undirected
V -weighted graph with a designated self-loop of weight e at every node. This convention is es-
pecially convenient when we later form powers or closures of Ri : it ensures that length-k paths
can always be extended to length k + 1 without changing their value by inserting a self-loop, so
comparisons across path lengths are not artifacts of path padding.

Remark 119 (Why symmetry and why Ri (x, x) = e?). Symmetry is not logically necessary, but it
matches the intended reading “x and y are (un)distinguished” as an (approximate) equivalence-like
judgment (Hyperseed-Concept ??). Setting Ri (x, x) = e = (1, 1) is likewise a modeling decision:
it ensures that when we later compose relations, a path that “stays at x” contributes neutrally
rather than shrinking values. In graph terms, we are giving each node a self-loop of maximal
strength so that closure emphasizes multi-step connections between distinct nodes. Technically,
this is the enriched-graph analogue of putting 1 on the diagonal of an adjacency matrix so that
“no move” is always an available step. With ⊗ as multiplication, a diagonal value strictly below
1 would systematically damp all multi-step compositions, making it harder to interpret whether a
decrease came from genuinely weak links between distinct nodes or merely from repeated diagonal
attenuation. Note also that symmetry and reflexive diagonals together do not force transitivity:
the later closure computation is precisely the mechanism that constructs the least transitive (or
path-complete) strengthening consistent with the chosen ⊕/⊗ aggregation.

5.2   From relations to weakness: “failed distinctions”
Section 3.7 defined weakness for a crisp set H ⊆ X × X of undistinguished pairs. For the toy model
it is useful to use the standard V -enriched generalization. In particular, passing from crisp H to a
V -valued relation R lets us represent not only whether two items are treated as indistinct, but also
to what degree that indistinction holds in each channel of the quantale, and then aggregate these
degrees in a quantale-native way.

Remark 120. Conceptually, weakness is meant to quantify “how much important structure is being
collapsed”: how costly it is, relative to what matters, to treat too many things as indistinct. In the
Hyperseed literature this idea is developed as a quantale-native aggregation principle (Hyperseed-
Concept 143; see also [3, 2]). Here we simply instantiate that principle on a finite set. One can view
the weakness functional as a deliberately coarse proxy for “information lost under a compression”:
it does not attempt to reconstruct which distinctions were lost, but returns a single severity score
that can be compared across candidate relations R.

Definition 25 (Weakness of a V -valued relation). Fix an importance valuation µ : X → V . For a
V -valued relation R : X × X → V , define
                                      M
                         w(R) :=             µ(u) ⊗ R(u, v) ⊗ µ(v) ∈ V.
                                     (u,v)∈X×X




                                                  84
Remark 121. The type of this definition is worth making explicit: since µ(u), R(u, v), µ(v) ∈ V
and ⊗ is the quantale product, each term µ(u) ⊗ R(u, v) ⊗ µ(v) is again an element     L       of V , and
the (possibly large) family of such terms is then aggregated by the quantale join . Because X is
finite in the toy model, the join is a finite join; in an infinite setting one would typically require the
appropriate completeness so that the join exists.
Remark 122 (Intuition). The expression for w(R) is the same idea as the crisp case, but with two
refinements. First, the relation R(u, v) is graded, so “being undistinguished” is a matter of degree.
Second, the valuation µ weights entities by importance, so collapsing
                                                                L        a with something may count
more than collapsing c with something. The quantale join           then aggregates all these weighted
collapses into a single global score. In this toy quantale, the aggregation is a bottleneck (a max),
so weakness is driven by the most severe important collapse; other quantales would yield sum-like
or softmin-like notions of weakness. Equivalently, one can think of w(R) as a “worst-case after
weighting” criterion: among all pairs (u, v), it selects the pair whose weighted indistinction is most
damaging, with the notion of “most damaging” determined by the join on V .
Remark 123. In many relational settings one may want to exclude diagonal pairs (u, u) from
the aggregation, since an object being “undistinguished from itself ” is not a failure of distinction.
Here the definition sums over all of X × X for notational uniformity; in the worked toy instances
one typically takes R(u, u) to be the least element (0, 0) (or otherwise fixed by convention) so that
diagonal terms do not affect w(R). If instead one sets R(u, u) = e, then the diagonal contributes
the baseline importance µ(u) ⊗ e ⊗ µ(u) and one should interpret the resulting weakness as including
self-collapse as a fixed offset.
Remark 124 (A tiny example). If µ(x) = (1, 1) for all x and R has only one substantial off-
diagonal entry, say R(a, b) = (0.9, 0.2) and all other off-diagonal entries are (0, 0), then

                                           w(R) = (0.9, 0.2)

(up to symmetry/duplication conventions in the join). So in the bottleneck semantics, the global
weakness simply mirrors the worst undistinguished edge. When multiple edges are present, w(R)+
becomes the largest product-weighted positive indistinction, as noted below. In this example, if one
also had R(b, a) = (0.9, 0.2), the join would still return the same value, illustrating that duplicating
the same worst edge does not change a max-type aggregator; by contrast, in an additive quantale,
doubling could change the score and symmetry conventions would matter more.
Remark 125. If H ⊆ X × X is crisp, embed it as a V -valued    L relation 1H via 1H (u, v) = e if
(u, v) ∈ H and 1H (u, v) = (0, 0) otherwise. Then w(1H ) = (u,v)∈H µ(u) ⊗ µ(v), recovering the
earlier definition. This embedding is the standard “characteristic relation” construction: elements
of H are assigned the multiplicative unit e so that the only contribution of such a pair is through
the endpoint weights µ(u) and µ(v),
                                 L while pairs not in H are assigned the least element so that they
contribute nothing under ⊗ and .
Definition 26 (A concrete importance valuation). In the worked example below we use

                        µ(a) = (1, 1),      µ(b) = (0.8, 1),     µ(c) = (0.6, 1).

Thus the positive channel weights importance (how costly it is to collapse distinctions involving an
item), while the negative channel is left unweighted for simplicity. Note that these values impose
an explicit ranking of “stakes”: collapsing distinctions involving a is treated as most consequential,
then b, then c, at least in the positive coordinate that drives the bottleneck score.

                                                   85
Remark 126 (Why weight only the positive channel here?). This is purely for pedagogical trans-
parency. In many applications one would also want to weight negative evidence: e.g. “distinguishing
a from b is more important than distinguishing c from b.” The present choice keeps the numeric
algebra minimal: the negative coordinate of w(R) will be dominated by whatever negative evidence
is largest, independent of µ. Nothing essential hinges on this choice; it merely fixes one explicit
convention for the toy. Concretely, with µ(·)− = 1 in this section, the negative coordinate behaves
like an unweighted bottleneck over R(u, v)− (up to the way ⊗ combines negatives in the chosen
quantale), so that the only place where “importance” visibly enters is the positive-coordinate term
µ(u)+ µ(v)+ R(u, v)+ .

Remark 127 (Reading w(R) in this toy). With the quantale operations from Section 3.4, the first
coordinate of w(R) is
                          w(R)+ = max µ(u)+ µ(v)+ R(u, v)+ ,
                                           u,v

i.e. a bottleneck-style “largest important collapsed link” score. This matches a minimax/bottleneck
notion of simplicity: the strongest (most important) collapsed distinction dominates. Other aggre-
gators (e.g. additive) are possible, but we keep the quantale-native choice here. For completeness,
                             −
the second coordinate w(R)L is computed analogously using the ⊗-combination rule for the negative
coordinate and the join       on that coordinate (which, for p-bit, is again max-like); in the present
toy convention µ(·)− = 1, so the negative contribution is driven directly by the largest negative
component appearing among the µ(u) ⊗ R(u, v) ⊗ µ(v) terms.

Remark 128. The form µ(u)+ µ(v)+ R(u, v)+ also makes it clear why w(R)+ can be read as a
“failed distinction” score rather than merely a raw strength score: even if R(u, v)+ is moderately
large, the weakness only becomes large when the endpoints are themselves important in the positive
channel. Thus, collapsing two low-importance entities can remain cheap even if the relation strongly
identifies them, while a weaker identification between high-importance entities can still dominate
the global bottleneck.

Remark 129 (Connection to “simplicity as failed distinction”). It is easy to hear “simplicity”
as a virtue and “failure to distinguish” as a vice. Hyperseed treats them as two faces of a single
structural phenomenon: compression always forgets distinctions, and the question is which ones
and at what cost. The quantale-functional w(R) is precisely a knob for that trade: it quantifies
the degree and importance of collapsed distinctions in a context (Hyperseed-Concept 169, 202).
In particular, when used alongside a competing objective (e.g. a fit-to-data or coherence score),
w(R) provides the “simplicity pressure” by penalizing relations that identify too much of what the
valuation µ declares significant.

5.3   Patterns as finite constraints and pattern support
In this toy setting, a “pattern” will be a finite set of pair-constraints that should be jointly sup-
ported. This choice builds in two simplifying assumptions that are useful later: (i) patterns are
finitely checkable objects (one can compute their support by a finite aggregation), and (ii) the
only structure inside a pattern is which pairs are demanded to cohere. Nothing in this subsection
requires that the constraints be consistent in the classical sense; instead, consistency becomes an
emergent, graded property of the support values.

Definition 27 (Pattern as a constraint-set on pairs). A pattern is a finite set

                                            P ⊆ X ×X

                                                 86
(typically symmetric and excluding the diagonal) interpreted as a conjunction of constraints “for
all (u, v) ∈ P , treat u and v as (approximately) undistinguished.”

Remark 130 (Conventions: symmetry, diagonal, and multiplicity). Formally, nothing breaks if P
includes ordered pairs or diagonal pairs; these are conventions chosen to keep the toy notion aligned
with the intended reading. Symmetry corresponds to treating “u matches v” as interchangeable with
“v matches u,” and excluding (u, u) avoids constraints that are tautological in most similarity-like
contexts. Because P is a set, not a multiset, repeating the same constraint does not artificially
increase its influence; if one wanted repeated evidence, that would be modeled in R (as stronger
support) or by a different pattern formalism.

Remark 131 (Intuition and relation to the general notion of pattern). In a large theory, a “pattern”
is often something like a model, a regularity, or a compression ([5, 16]). Here we take the smallest
possible fragment of that idea: a pattern is just a finite list of pairwise identifications that are
supposed to hold together. This is deliberately austere: it makes patternhood into a constraint
satisfaction problem, and the only subtlety is that satisfaction is graded and paraconsistent. One
can regard P as specifying a tiny “hypothesis” about which distinctions the system is willing to
ignore (at least locally), and the role of R is to provide context-dependent evidence for and against
each such local identification.

Remark 132 (Simple examples). With X = {a, b, c}, the set P = {(a, b)} is the pattern “a is
identified with b.” The set P = {(a, b), (b, c)} is the pattern “a ∼ b and b ∼ c.” If one additionally
includes (a, c) then P is a triangle/cluster constraint. In later sections, such constraint-sets will
be replaced by richer pattern objects, but the logical spine is the same: a pattern is something
that asks multiple local judgments to cohere (Hyperseed-Concept 130). It is worth noting that, at
this toy level, P = {(a, b), (b, c)} does not itself enforce transitivity; it merely requests two local
identifications. Whether “a and c should also cohere” is a further constraint, represented by adding
(a, c) explicitly (or by a separate closure principle introduced later, if desired).

Definition 28 (Pattern support). Given a context relation R and a pattern P , define the (con-
junctive) pattern support                  O
                              SR (P ) :=        R(u, v) ∈ V.
                                                   (u,v)∈P

In particular,                    Y                                        Y
                    SR (P )+ =             R(u, v)+ ,        SR (P )− =             R(u, v)− .
                                 (u,v)∈P                                  (u,v)∈P
                                                                      N
Remark 133 (Empty pattern and the unit of conjunction). Since             is a multiplicative “big
conjunction,” the empty pattern P = ∅ evaluates to the multiplicative unit:

                                                SR (∅) = 1V .

This matches the logical convention that an empty conjunction is trivially satisfied. In the two-
channel setting, this should be read as “the empty set of demands contributes no constraint at all,”
rather than as a substantive claim about the world; nontrivial content only appears once at least
one pair-constraint is included.
                                                      N
Remark 134 (Notation unpacking). The symbol              is the quantale analogue of a big conjunction:
we multiply the evidence-values for each required pair. Because our ⊗ is componentwise multiplica-
tion, SR (P )+ is literally the product of the positive supports for each constraint, and similarly for

                                                        87
SR (P )− . Thus the more constraints you ask for, the harder it becomes to keep the support high—an
algebraic reflection of the simple thought that conjunction is stricter than a single predicate. Equiv-
alently, each additional constraint (u, v) acts as a multiplicative “gate” that can only decrease (or,
in the best case, preserve) the overall degree whenever R(u, v)± ≤ 1 in the ambient scale.

Remark 135 (Monotonicity in the pattern argument). Because ⊗ is monotone in each argument,
enlarging a pattern can only make it harder to satisfy: if P ⊆ Q, then (componentwise in the
V -order)
                                      SR (Q) ≤ SR (P ).
Concretely, SR (Q)+ is SR (P )+ multiplied by the additional positive factors required by Q \ P , and
likewise for the negative channel. This is the toy analogue of the general principle that adding
conjuncts strengthens a theory.

Remark 136 (A concrete computation). For intuition, suppose P = {(a, b), (b, c)} and (in some
context) R(a, b) = (0.9, 0.2) and R(b, c) = (0.6, 0.8). Then

                             SR (P ) = (0.9 · 0.6, 0.2 · 0.8) = (0.54, 0.16).

In this example, the pattern is moderately supported (0.54) and only weakly opposed (0.16), even
though one constituent pair has high opposition in isolation; the multiplicative aggregation makes
the overall opposition sensitive to joint opposition across all constraints rather than to a single
contested link. This “jointness” is exactly the behavior expected of a conjunction-like operator.

Remark 137 (Paraconsistent reading of SR (P )). When SR (P ) = (s+ , s− ), the pattern is:

• supported to degree s+ ,

• opposed to degree s− ,

• and may be simultaneously both (if both are high).

This is exactly why the two-channel semantics is useful: the theory can represent “the pattern is
strongly present and strongly resisted” without collapsing into triviality. That tension is one of
the seeds from which later notions of dissonance, reversal, and habit dynamics grow (Hyperseed-
Concept 159, 97). In particular, a high s+ indicates that each demanded identification is locally
well-supported, while a high s− indicates that each demanded identification is also locally well-
opposed; these can coexist without forcing an all-or-nothing verdict.

Remark 138 (Why conjunctive aggregation is the right toy default). SR (P ) is a deliberately
minimal “all-of ” aggregator (a toy conjunction). More elaborate pattern measures used later in the
full paper (pattern intensity, emergence criteria, etc.) can be layered on top of this. For Section 5,
the goal is simply to have a compact, checkable notion of “this pattern is supported / opposed /
contradictory.” The multiplicative form is especially convenient because it makes the dependence
on individual constraints explicit and local: every pair in P contributes a visible factor, so changes
in R (or edits to P ) have transparent effects on the aggregate.

5.4   Emergence via compositional closure
A key Hyperseed intuition is that patterns can emerge from composition rather than being explicitly
present. In the relation-quantale, this is exactly what composition and closure do: if R(a, b) and
R(b, c) are strong, then R(a, c) becomes strong in the closure even if it started weak. In other

                                                   88
words, the “emergent” link a → c is not stipulated as a primitive datum; it is forced by the algebra
of chaining. This is the graded analogue of how (crisp) transitive closure turns a set of edges into
all reachable edges, except that here reachability is replaced by a quantale-valued notion of support
for a connection.
Remark 139. This is a precise algebraic analogue of the informal slogan “structure implies more
structure”: a system that treats a as (approximately) the same as b, and b as the same as c,
is under pressure to treat a as the same as c. In classical logic that pressure is transitivity of
equivalence. In a graded setting the same pressure becomes a closure operator built from ⊕ and
⊗. This is one minimal formal doorway into Hyperseed’s notion of emergence (Hyperseed-Concept
??; see also [5] for broader discussion). One can also read this as a disciplined way of converting
local judgments (pairwise links) into global judgments (consistency across chains) while remaining
inside the same algebraic universe V . When V is the p-bit quantale used in this toy model, the
same mechanism propagates not only “positive support” but also any built-in notion of “opposition”
or “incompatibility” that ⊗ and ⊕ encode.
Definition 29 (Quantale composition of V -valued relations). For V -valued relations R, S : X ×
X → V , define                              M
                          (R ◦ S)(x, z) :=      R(x, y) ⊗ S(y, z).
                                                 y∈X

Remark 140 (What this composition means). The variable y plays the role of an intermediate
“bridge” entity. For each bridge y, the quantity
                                            L      R(x, y) ⊗ S(y, z) measures how strongly x connects
to z by going through y. Then the join         y∈X takes the best such bridge in the quantale order.
Because ⊕ is a max in this toy, composition chooses the strongest multi-step path. This is the same
algebra that underlies weighted path problems in idempotent semirings, but here it is interpreted as
propagation of indistinction judgments. Equivalently, if one thinks of R and S as |X|×|X| matrices
with entries in V , then ◦ is the usual “matrix product” but with (+, ×) replaced by (⊕, ⊗); the bridge
index y is exactly the summed-over index. This perspective is often useful for concrete computations
in the finite-universe toy setting, since repeated composition becomes iterated (quantale-)matrix
multiplication.
Definition 30 (Transitive-like closure). Define R(1) := R and R(n+1) := R(n) ◦ R. Define the
closure                                         M
                                      Cl(R) :=      R(n) .
                                                       n≥1

Remark 141 (Intuition: closure as “all finite chains”).                    (n)
                                                         L The power R (x, z) measures evidence
for connecting x to z by a chain of n edges. Taking         n≥1 then means: allow any finite chain
length, and keep whichever chain provides the strongest support (and strongest opposition) for the
resulting link. In a finite universe, Cl(R) can often be computed by iterating composition until no
entry improves. Note that the definition starts at n ≥ 1, so it is a “transitive-like” closure rather
than a reflexive-transitive closure: we do not automatically force a maximal self-link R(x, x) via an
n = 0 identity step. If one wanted the reflexive-transitive variant, one would typicallyL  adjoin the
identity relation I (with I(x, x) = > and I(x, z) = ⊥ for x 6= z in the V -order) and take n≥0 R(n) ;
the present choice isolates what is generated purely by chaining the given evidence in R.
Remark 142 (Finite stabilization in the toy universe). Because X is finite and ⊕ is idempotent
in this setting, the ascending sequence
                                                             N
                                                             M
                          R(1) ≤ R(1) ⊕ R(2) ≤ · · · ≤             R(k) ≤ · · ·
                                                             k=1


                                                  89
often stabilizes after finitely many steps when computed entrywise: beyond some length, longer
chains do not improve any value. Operationally, this is why one can implement Cl(R) by re-
peated composition and pointwise ⊕-accumulation until a fixed point is reached, mirroring classical
algorithms for transitive closure (e.g. Floyd–Warshall) but with the boolean semiring replaced by
(V, ⊕, ⊗). The theorem below identifies the mathematical reason that this fixed point is the “right”
one: it is exactly the least self-composition-stable extension above R.

Theorem 4 (Closure is transitive and is the least transitive extension above R). Let R : X × X →
V . Then:

1. ( Extensive) R ≤ Cl(R).

2. ( Transitive) Cl(R) ◦ Cl(R) ≤ Cl(R).

3. ( Least) If T is any relation with R ≤ T and T ◦ T ≤ T , then Cl(R) ≤ T .

Remark 143 (What the theorem is saying, in plain language). The theorem asserts that Cl(R)
behaves exactly as a closure should. First, it does not forget what you started with: every direct
judgment in R remains present (possibly strengthened). Second, once you have closed, composing
closed relations does not generate anything genuinely new: the closure is stable under composition,
which is the graded analogue of transitivity. Third, it is the smallest such stable extension: any
other relation T that contains R and is closed under self-composition must also contain Cl(R). In
particular, statement (2) says that after closure, every composite chain-of-chains can be “flattened”
back into a single finite chain already accounted for in Cl(R), so no additional emergent links remain
hidden behind further iteration.

Remark 144 (Why it matters here). This result is a sanity check that the toy “emergence” mecha-
nism is not ad hoc. If we claim that emergent pattern structure arises from iterating compositional
implications, then Cl(R) is the canonical object that embodies “everything implied by finite com-
positional chaining.” In later categorical language, Cl is a standard closure operator induced by
enrichment. So this theorem connects the concrete numeric demo back to the abstract composition-
ality requirement in Section 3. It also clarifies the sense in which emergence here is conservative:
Cl(R) can add new strong links, but it does so only when they are justified by existing links and the
fixed rules (⊕, ⊗), i.e. by the chosen notion of compositional propagation encoded in the quantale.

Proof. (1) The join defining Cl(R) includes R(1) = R, hence R ≤ Cl(R).
   (2) Using distributivity of ◦ over joins (true in the relation quantale) and associativity of ◦:
                                                         
                                   M               M              M               
              Cl(R) ◦ Cl(R) =         R(m)  ◦       R(n)  =        R(m) ◦ R(n) .
                                   m≥1             n≥1           m,n≥1

Here distributivity can be read entrywise: for each (x, z), the definition of ◦ and the fact that ⊗
distributes over ⊕ allow one to pull joins outside and regroup them into a single (possibly larger)
join over pairs (m, n). But R(m) ◦ R(n) = R(m+n) by associativity of composition, so
                                           M             M
                         Cl(R) ◦ Cl(R) =       R(m+n) ≤      R(k) = Cl(R).
                                          m,n≥1            k≥1

The final inequality holds because every index of the form k = m + n with m, n ≥ 1 satisfies k ≥ 2,
and the join over all k ≥ 1 dominates the join over the subset k ≥ 2 in the quantale order.


                                                  90
   (3) IfLR ≤ T and T ◦ T ≤ T , then by induction R(n) ≤ T for all n. Taking joins yields
Cl(R) = n≥1 R(n) ≤ T . Concretely, the induction step uses monotonicity of ◦: if R(n) ≤ T , then

                                R(n+1) = R(n) ◦ R ≤ T ◦ T ≤ T,

where R ≤ T is used in the middle inequality.

Proof sketch. The strategy is to recognize Cl(R) as the join of all finite compositional powers of
R. Extensiveness is immediate because R is one of those powers. Transitivity follows because
composing an m-step chain with an n-step chain yields an (m + n)-step chain, and all such powers
are already included in the join. Leastness follows because any transitive extension T that contains
R must contain every power R(n) (by repeated composition), hence must contain their join.         
Remark 145 (Why the key steps work). The only real work is done by two structural facts about
quantale-valued relations:
• composition ◦ is associative, so path concatenation is well-defined, and

• composition distributes over joins, so “take the best bridge” is compatible with “take the best path
  length.”
These are precisely the algebraic conditions that make composition a sensible model of propagation.
Visually, one can imagine a weighted graph with two weights per edge; Cl(R) is the result of allowing
all paths and then assigning each pair (x, z) the best weight achievable by any path from x to z.
Remark 146 (Hyperseed reading). The closure Cl(R) is an extremely literal toy formalization of
“pattern emergence”: new constraints become supported because they are implied by compositions
of already-supported constraints.

5.5   Miledorphic resonance and anti-resonance as cross-context coupling
We now model morphic resonance as the transport of pattern support between contexts.
Remark 147. The phrase “morphic resonance” is historically associated with Sheldrake’s specu-
lative proposal [13]. Hyperseed uses the phrase in a more formal-and-operational spirit: it denotes
a cross-context coupling that tends to make similar patterns more likely in different places, with-
out requiring direct causal contact in the narrow sense. In this paper, the coupling is explicitly
represented as an algebraic update rule on context relations (Hyperseed-Concept 115, 159).
Definition 31 (Pointwise scaling of a relation). For K ∈ V and a relation R : X × X → V , define
(K ⊗ R) : X × X → V by
                                 (K ⊗ R)(x, y) := K ⊗ R(x, y).
Remark 148 (Intuition and example). Pointwise scaling means: take every pairwise judgment in
R and attenuate (or amplify) it by the same coupling strength K. For instance, if K = (0.9, 0.9)
and R(x, y) = (0.8, 0.2), then (K ⊗ R)(x, y) = (0.72, 0.18). In other words, we transmit the same
“shape” of evidence but at reduced intensity.
Definition 32 (Morphic resonance update operator). Fix a coupling strength K ∈ V . Define the
resonance propagation from C1 to C2 by

                               ResK (R1 → R2 ) := R2 ⊕ (K ⊗ R1 ),

where the join ⊕ and product ⊗ are taken pointwise on X × X.

                                                 91
Remark 149 (Plain-language reading). The update says: “keep what C2 already believes, but
also import (a scaled version of ) what C1 believes, taking the better-supported evidence in each
channel.” Because ⊕ is a join, the update is conservative in the sense that it cannot decrease either
the positive or negative evidence for any pair; it can only add support and/or add opposition. This
is the algebraic core of paraconsistent transport: influence without forced consistency.

Remark 150 (Why a join, rather than overwriting?). If one overwrote R2 by K ⊗ R1 , then
resonance would erase local evidence and turn into domination. Using ⊕ instead makes resonance an
inclusion-like process: new evidence accumulates. This matches the intended semantics of contexts
as partially independent stances that can be coupled without being annihilated.

Definition 33 (Anti-resonance update operator). Anti-resonance is modeled as preferential trans-
port of opposition to the pattern. A minimal way to express this with the same quantale is to use
a coupling element that acts mainly on the negative channel:

                                         K − := (0, k − ) ∈ V.

Then define
                             AResk− (R1 → R2 ) := R2 ⊕ (K − ⊗ R1 ).
Concretely, (K − ⊗ R1 )(x, y) = (0, k − R1− (x, y)), so only negative evidence is propagated.

Remark 151 (Anti-resonance as structured “no”). The anti-resonance operator is not “the nega-
tion” of resonance; it is a directed transport of resistance. In terms of habit dynamics, it provides a
minimal mechanism by which a context can inherit reasons not to instantiate a pattern that another
context opposes. This aligns with the Hyperseed idea that habit reversal is not mere noise but can
be driven by imported constraint pressure (Hyperseed-Concept 188, 114).

Proposition 3 (Monotonicity of resonance and anti-resonance). For fixed K, the maps R2 7→
ResK (R1 → R2 ) and R2 7→ AResk− (R1 → R2 ) are monotone (order-preserving). They are also
monotone in R1 and in the coupling parameters.

Remark 152 (What monotonicity means here). Monotonicity formalizes a simple but important
ethical/epistemic constraint on the update rules: if R2 already had more evidence (in either channel)
than some R2∗ , then after resonance it should still have at least as much. In other words, adding
evidence and then resonating should not perversely reduce what you had. This proposition says the
update rules are “well-behaved” in precisely that minimal sense.

Remark 153 (Connection to the rest of the document). This is the same monotonicity logic
that underlies the sanity theorems in Section 4: weakness and pattern measures are intended to
behave directionally under addition of structure. Here we ensure that the dynamical operators
(resonance/anti-resonance) respect the same order-theoretic discipline, which becomes crucial later
when iterating updates and taking fixed points.

Proof. Each operator is built from pointwise ⊕ and ⊗, which are monotone in each argument with
respect to the componentwise order on V .

Proof sketch. The proof reduces the claim to a basic fact about the p-bit quantale: both ⊕ (join) and
⊗ (product) are order-preserving in each input. Since the update operators apply these operations
pointwise on X × X, the order-preservation lifts immediately from V to V -valued relations.         



                                                  92
Remark 154 (Why this matters conceptually). Order-preservation is the minimal algebraic sub-
stitute for the intuitive statement “resonance transports influence without making things worse by
fiat.” In paraconsistent settings, one often worries that allowing contradictory evidence will break
basic reasoning. Monotonicity reassures us that the update dynamics at least respect the lattice
structure that makes graded, nontrivial aggregation possible in the first place.

Definition 34 (A simple habit-taking / habit-reversal statistic). To connect with the Hyperseed
“tendency to take habits” definitions, we map a p-bit value v = (v + , v − ) to a single decision-biased
probability via the truth-bias

                                                                     d(v) + 1
                    d(v) := v + − v − ∈ [−1, 1],      pdec (v) :=             ∈ [0, 1].
                                                                        2
For a pattern P , we define pdec (P | R) := pdec (SR (P )).

Remark 155 (Intuition and scope). This statistic is intentionally not presented as a universal
“probability of truth.” It is a decision proxy: a way of turning two-channel evidence into a single
scalar that increases with net support and decreases with net opposition. One should read it as “if
the system must act as if P holds, how disposed is it to do so?” This bridges the toy evidence
algebra to the language of habit formation and reversal (Hyperseed-Concept 189, 188).

Remark 156. Morphic resonance tends to increase pdec (P | R) for patterns P supported in the
source, while anti-resonance tends to decrease it by increasing opposition. This is the toy analogue
of “tendency to take habits” versus “tendency to reverse habits”.

5.6   A concrete nontrivial instance reaching morphic resonance
We now specify concrete R1 and R2 , compute weakness, show emergence via closure, and then
show morphic resonance.

Example 1 (Initial relations in two contexts). Let X = {a, b, c} and define symmetric relations
R1 , R2 : X × X → V by setting the diagonal to e = (1, 1) and

             R1 (a, b) = (0.90, 0.80),   R1 (b, c) = (0.85, 0.20),   R1 (a, c) = (0.10, 0.70),

             R2 (a, b) = (0.20, 0.70),   R2 (b, c) = (0.30, 0.60),   R2 (a, c) = (0.10, 0.80).
Intuitively: C1 strongly supports a ∼ b (but with conflict), and supports b ∼ c; C2 is initially
skeptical about all three pairwise identifications.

Remark 157. This is the smallest size where the closure phenomenon is nontrivial: with only two
entities there is no room for a genuinely emergent third relation. With three entities, a two-edge
chain can force an implied edge. So {a, b, c} is the first stage where “emergence by composition” is
visible.

Example 2 (Weakness comparison). Use µ from Definition 26 and weakness from Definition 25.
A short check shows:
                     w(R1 ) = (0.72, 0.80),  w(R2 ) = (0.16, 0.80).
Thus, in the bottleneck sense of Section 3.7, C1 is “weaker” (collapses a more important distinction)
than C2 .



                                                    93
Remark 158 (How to read the numbers). The positive weakness 0.72 for C1 comes from combining
(i) the strong positive indistinction R1 (a, b)+ = 0.90 with (ii) the high importance weights µ(a)+ = 1
and µ(b)+ = 0.8. By contrast, C2 never strongly supports an important collapse, so its positive
weakness is small. The negative weakness being 0.80 in both contexts reflects that each contains at
least one strongly opposed identification somewhere; since we used a bottleneck/max aggregator, a
single strong opposition dominates.
Example 3 (Emergence in C1 via closure). Compute the closure Cl(R1 ) = R1 ⊕ (R1 ◦ R1 ) ⊕ · · · .
Because X has three elements, the first nontrivial emergent edge is a → c via b:

         (R1 ◦ R1 )(a, c) ≥ R1 (a, b) ⊗ R1 (b, c) = (0.90 · 0.85, 0.80 · 0.20) = (0.765, 0.16).

Joining with the direct edge R1 (a, c) = (0.10, 0.70) yields
                                                                        
                 Cl(R1 )(a, c) ≥ R1 (a, c) ⊕       R1 (a, b) ⊗ R1 (b, c) = (0.765, 0.70).

So even though C1 initially had very low positive evidence for a ∼ c, the compositional structure
a ∼ b and b ∼ c causes a ∼ c to become strongly supported in the closure. This is a concrete toy
instance of emergence as compositional implication.
Remark 159 (Visual intuition). If one draws a triangle with vertices a, b, c, then R1 begins with
two thick edges (a–b and b–c) in the positive channel and a thin edge (a–c). Closure thickens the
missing edge because the two-step walk a → b → c provides an alternate route. In this toy quantale,
the positive-channel strength of that route is the product of the two edge strengths.
Example 4 (Morphic resonance transmission from C1 to C2 ). Let the coupling strength be

                                           K := (0.90, 0.90).

Apply the morphic resonance update (Definition 32):

                              R20 := ResK (R1 → R2 ) = R2 ⊕ (K ⊗ R1 ).

Compute, for example,

R20 (a, b) = (0.20, 0.70) ⊕
                                                         
                             (0.90, 0.90) ⊗ (0.90, 0.80) = (0.20, 0.70) ⊕ (0.81, 0.72) = (0.81, 0.72),

R20 (b, c) = (0.30, 0.60) ⊕ (0.90, 0.90) ⊗ (0.85, 0.20) = (0.30, 0.60) ⊕ (0.765, 0.18) = (0.765, 0.60),
                                                       

and

R20 (a, c) = (0.10, 0.80) ⊕
                                                         
                              (0.90, 0.90) ⊗ (0.10, 0.70) = (0.10, 0.80) ⊕ (0.09, 0.63) = (0.10, 0.80).

Thus C2 receives strong support for the structure a ∼ b and b ∼ c from C1 even though the direct
edge a ∼ c does not (yet) increase.
   Now close internally in C2 :

        Cl(R20 )(a, c) ≥ R20 (a, b) ⊗ R20 (b, c) = (0.81 · 0.765, 0.72 · 0.60) = (0.61965, 0.432).

Joining with the direct edge (0.10, 0.80) yields

                                   Cl(R20 )(a, c) ≥ (0.61965, 0.80).

So morphic resonance transmits the pattern skeleton (the chain a ∼ b, b ∼ c), and then composi-
tional closure produces the missing implied link a ∼ c. This is a minimal toy model of “spatially
separated habit taking”: C2 becomes disposed to instantiate the same cluster-pattern present in C1 .

                                                    94
Remark 160 (What is being transmitted?). Notice that resonance did not directly increase R2 (a, c)+ ,
because the source itself had R1 (a, c)+ small. What was transmitted was the two-edge scaffold
that makes a ∼ c compositional. This is philosophically important: it models the transmission
of a relational form rather than a single belief, which is closer to the intended “morphic” flavor
(pattern-shape transfer) than naive copying of propositions.

Example 5 (Pattern support and a habit-taking inequality). Let the pattern (constraint-set) be
the chain
                                  P := {(a, b), (b, c)}.
Compute support using Definition 28. Intuitively, this pattern asks for a simultaneous “fit” of two
links, a ∼ b and b ∼ c, so its support is a p-bit-valued conjunction of the two corresponding edge-
values. In this toy p-bit quantale, the tensor ⊗ acts componentwise on (t, f )-pairs (so it behaves
like a multiplicative “and” that propagates both positive and negative evidence along the chain).
    In C1 :
                           SR1 (P ) = R1 (a, b) ⊗ R1 (b, c) = (0.765, 0.16).
In particular, the pattern-level positive support 0.765 is the product of the two positive edge-scores
in C1 , while the pattern-level opposition 0.16 is the product of the two edge-level opposition scores;
hence a single weak link (small t) or a single strong objection (large f ) can materially affect the
combined pattern support.
   In C2 initially:
                         SR2 (P ) = (0.20, 0.70) ⊗ (0.30, 0.60) = (0.06, 0.42).
Here the pre-update pattern has relatively low positive support (0.06) and comparatively high oppo-
sition (0.42), reflecting that both constituent constraints are, initially, not well-endorsed in C2 . It
is sometimes helpful to look at the net inclination t − f at the pattern level:

                                          (0.06 − 0.42) = −0.36,

which already indicates that the combined pattern is disfavored before any coupling.
   After morphic resonance:

                        SR20 (P ) = (0.81, 0.72) ⊗ (0.765, 0.60) = (0.61965, 0.432).

So the resonance update has sharply increased the positive component of the pattern support (from
0.06 to 0.61965) while leaving the negative component in the same general range (from 0.42 to
0.432). At the level of net inclination this changes the sign:

                                      (0.61965 − 0.432) = 0.18765,

so the same multi-constraint form moves from “overall opposed” to “overall favored” according to
the simple difference t − f .
    Using the decision probability from Definition 34,

                     (0.06 − 0.42) + 1                                 (0.61965 − 0.432) + 1
  pdec (P | R2 ) =                     = 0.32,     pdec (P | R20 ) =                         ≈ 0.593825.
                             2                                                   2

Recall that the affine rescaling pdec (t, f ) = (t−f2)+1 maps the score t − f ∈ [−1, 1] to a number in
[0, 1], so that equal support and opposition (t = f ) corresponds to pdec = 21 , net support (t > f )
yields pdec > 12 , and net opposition (t < f ) yields pdec < 21 .


                                                    95
    Thus P becomes substantially more likely in C2 after the resonance update. This is the toy
analogue of Hyperseed’s “tendency to take habits”: the post-update probability is higher than the
pre-update probability for a pattern supported elsewhere. In other words, a pattern that is already
coherently instantiated in one context (C1 ) can, under resonance, become easier to enact in a
different context (C2 ) even though C2 initially opposed it at the multi-constraint level.
Remark 161. In the language of graded habits, the inequality pdec (P | R20 ) > pdec (P | R2 ) is
the simplest possible signature of habit-taking: the system’s disposition toward enacting a multi-
constraint form increases after coupling. Note that, because the support is computed by chaining
constraints with ⊗, the phenomenon is genuinely pattern-level rather than edge-local: one is not
merely increasing confidence in a single relation, but increasing the likelihood that an entire small
configuration is jointly satisfied. More sophisticated theories would track trajectories under repeated
updates and study stability; this toy merely exhibits the direction of motion. One could also dis-
tinguish between (i) amplifying positive evidence for the pattern, (ii) reducing opposition to the
pattern, and (iii) doing both; in the numbers above, the dominant contribution is (i), since the
truth component jumps while the falsity component changes only mildly.

5.7   Anti-resonance as habit reversal (tiny numeric demo)
Example 6 (Anti-resonance increases opposition and can reverse a habit). Let k − = 0.9 and use
AResk− from Definition 33. Suppose C2 has begun to accept a ∼ b with R2 (a, b) = (0.60, 0.20), but
a different context (or a new stream of evidence) provides strong opposition modeled as R1 (a, b) =
(0.10, 0.90). Conceptually, anti-resonance differs from resonance by selectively importing (scaled)
opposition rather than support, so it acts like a controlled mechanism for “unlearning” or counter-
conditioning without requiring that prior positive evidence be erased.
    Then
                                                               
ARes0.9 (R1 → R2 )(a, b) = (0.60, 0.20) ⊕ (0, 0.9)⊗(0.10, 0.90) = (0.60, 0.20) ⊕ (0, 0.81) = (0.60, 0.81).

Here (0, 0.9) ⊗ (0.10, 0.90) = (0, 0.81) illustrates the same componentwise multiplication as before:
anti-resonance scales only the negative coordinate and passes no additional positive mass (the 0 in
the first coordinate). Likewise, the join ⊕ acts componentwise as an aggregation of available evi-
dence; in particular, the second coordinate increases from 0.20 to 0.81, capturing that the imported
counter-evidence dominates the earlier, weaker opposition. Notice that the positive coordinate re-
mains 0.60 throughout, so the update changes behavior by increasing conflict, not by deleting prior
support.
    The decision probability drops from
                               (0.40) + 1                                      (−0.21) + 1
         pdec (0.60, 0.20) =              = 0.70   to    pdec (0.60, 0.81) =               = 0.395.
                                   2                                                2
Equivalently, the net inclination shifts from 0.60 − 0.20 = 0.40 (net support) to 0.60 − 0.81 = −0.21
(net opposition), which is exactly the sense in which a “reversal” occurs in this graded setting: the
sign of t − f flips even though t itself does not decrease.
    So anti-resonance can drive a reversal: a previously formed habit becomes less likely by importing
opposition-to-the-pattern from elsewhere. In this way, AResk− can be read as a minimal mathemat-
ical caricature of how external critique, adverse feedback, or a competing norm can suppress an
emerging tendency by strengthening the “reasons against”.
Remark 162 (A philosophical aside). In ordinary discourse, “reversal” sounds like negation: the
mind flips from yes to no. In a paraconsistent setting, reversal is subtler: the system may keep its

                                                    96
positive evidence while importing so much opposition that the net disposition changes sign. This
resembles how real deliberation often feels: one does not forget the reasons for, but the reasons
against become weightier. Formally, the point is that (t, f ) is not collapsed to a single scalar before
updating: the calculus allows t and f to vary semi-independently, so an agent can become less
disposed to act even while retaining (and acknowledging) substantial supporting considerations.

5.8   A tiny resonance score demo via paraconsistent interference
We now connect the above “transport of evidence” to a resonance score derived from the p-bit
geometry.

Remark 163. The goal of this subsubsection is to show that “resonance” can be read in two
compatible ways:

• as an order-theoretic / quantale-theoretic propagation rule on evidence structures, and

• as a coherence or interference statistic after embedding evidence into a complex plane.

This second reading echoes approaches that relate paraconsistent evaluation to oscillatory or reso-
nant dynamics ([24]), but here it is presented only as a tiny computational demo.

Definition 35 (p-bit to complex mapping). Define σC : [0, 1]2 → C by

      σC (w+ , w− ) := d + ic,      d := w+ − w− ∈ [−1, 1],             c := (w+ + w− ) − 1 ∈ [−1, 1].

Here d is the truth-bias axis (net support vs net opposition) and c is the contradiction/ignorance
axis.

Remark 164 (Geometric intuition). The map σC turns a p-bit value into a point in the complex
plane whose real part d measures net inclination (support minus opposition), while the imaginary
part c measures deviation from classical consistency. When w+ + w− = 1 (no “extra” evidence),
we have c = 0 and the amplitude is purely real. When both channels are high, c > 0 and we move
into the upper half-plane, marking contradiction. When both are low, c < 0 and we move into the
lower half-plane, marking ignorance/indeterminacy. This gives a compact way to treat “truth” and
“conflict” as orthogonal components.

Definition 36 (Two-context interference (resonance) score). Given two complex amplitudes z1 , z2 ∈
C and weights w1 , w2 ≥ 0 with w1 + w2 = 1, define

                          Int(z1 , z2 ) := |w1 z1 + w2 z2 |2 − |w1 z1 |2 − |w2 z2 |2 .

Positive values indicate constructive interference (resonance), negative values indicate destructive
interference (dissonance).

Remark 165 (What this formula measures). The quantity |w1 z1 + w2 z2 |2 is the squared magnitude
of the combined amplitude. Subtracting |w1 z1 |2 + |w2 z2 |2 isolates the cross term that depends on
relative phase. Thus Int(z1 , z2 ) is zero when the two contributions are orthogonal in phase on
average, positive when they align, and negative when they oppose. Interpreted back in p-bit terms:
it measures whether two contexts “pull” in the same evidential direction after accounting for both
bias and contradiction.



                                                      97
Remark 166. For w1 = w2 = 21 one has

                                                           1
                                         Int(z1 , z2 ) =     Re(z1 z2 ).
                                                           2
So resonance is literally the (scaled) real part of the complex inner product, i.e. phase alignment.

Remark 167 (Why this is a reasonable toy resonance score). The interference score is not claimed
as a final definition of resonance for the full theory. Its pedagogical value is that it is:

• symmetric in the two contexts,

• sensitive to both direction (truth-bias) and conflict (imaginary component),

• and continuous/graded.

These are precisely the desiderata one wants when translating qualitative talk of resonance/dissonance
into a computable diagnostic (Hyperseed-Concept 159, 97).

Example 7 (Resonance increases after morphic resonance update). Consider the single proposition
“a ∼ b” as evaluated in C1 and C2 . Using Example 1 and Example 4:

             R1 (a, b) = (0.90, 0.80),    R2 (a, b) = (0.20, 0.70),        R20 (a, b) = (0.81, 0.72).

Map to complex amplitudes via Definition 35:

z1 = σC (0.90, 0.80) = 0.10+0.70i,        z2 = σC (0.20, 0.70) = −0.50−0.10i,               z20 = σC (0.81, 0.72) = 0.09+0.53i.

With equal weights w1 = w2 = 12 :

                                 Int(z1 , z2 ) = −0.06          (dissonant),

while after the morphic resonance update,

                                   Int(z1 , z20 ) = 0.19       (resonant).

Thus the same evidence-transport step that increases pattern support across contexts also increases
an interference-derived resonance score.
    One can likewise compute resonance for the pattern P = {(a, b), (b, c)} by using the pattern
supports SR1 (P ) and SR2 (P ) from Example 5 and mapping those p-bit values through σC . This
again yields a negative interference score before morphic resonance and a positive one after, i.e.
increased coherence at the level of the whole pattern-constraint.

Remark 168 (What changed, structurally?). Before resonance, C1 and C2 assign almost opposite
truth-bias to a ∼ b: z1 lies in the upper-right (net positive but conflicted) while z2 lies in the
lower-left (net negative and slightly ignorant). After resonance, z20 rotates toward z1 in both real
and imaginary components. The increase in Int is thus a numeric witness that the contexts have
become more phase-aligned on that proposition.

Remark 169 (Toy moral). In this toy model, “morphic resonance” has two separable mathematical
faces:

1. as a monotone, quantale-native evidence transport R2 7→ R2 ⊕ (K ⊗ R1 ) that increases pattern
   support across contexts without forcing consistency, and

                                                      98
2. as an increase in an interference-based coherence score after mapping p-bits to complex ampli-
   tudes.

This is exactly the bridge needed later in the paper: resonance is simultaneously a structural update
in the ontology and a dynamical/energetic coherence signal.

Remark 170 (Where this is going). The toy computations show how a single algebraic move can
produce: (i) transferred pattern scaffolds, (ii) emergent closure-completions, and (iii) increased
coherence scores. Concretely, “transferred pattern scaffolds” can be read as the appearance of a
reusable template: once a pattern is encoded as an algebraic element (or as a map between such
elements), the same formal manipulation can be re-applied in a new location, effectively transporting
structure along the available morphisms. In this sense the scaffold is not a new axiom but a
consequence of how composition and order interact in the chosen algebra.
    Likewise, “emergent closure-completions” refers to the fact that passing to a closure (or com-
pletion) is often forced by the operations already present: an initially partial family of pattern-
combinations can generate its own minimal fixed point under the closure operator, yielding a com-
pleted object in which previously missing joins/meets (or stable consequences) become available.
Even when the starting data are intentionally finite and schematic, the closure step makes explicit
the difference between “what is stipulated” and “what is entailed” by the algebraic rules.
    Finally, “increased coherence scores” can be understood as the numerical or order-valued witness
that the move has improved internal compatibility: after the transfer and closure, more constraints
can be simultaneously satisfied, or the same constraints can be satisfied in a stronger way. In later
sections, the same ideas are lifted to richer pattern spaces and iterated dynamics, where questions
of stability, habit persistence, and controlled reversal become meaningful. Here “iterated dynamics”
should be taken literally: repeating the move defines an update process, so one can ask whether
repeated application converges to a fixed point, cycles among a small family of states, or bifur-
cates when parameters are changed. Correspondingly, “controlled reversal” anticipates the need for
operations that can partially undo an update (or at least trace its provenance), so that one can dis-
tinguish irreversible closure effects from reversible transport effects. The present section should be
read as the smallest “seed crystal” of that later structure. In particular, it isolates the minimal set
of ingredients—a finite universe, an order-sensitive combination rule, and a coherence witness—so
that later generalizations can be recognized as elaborations rather than as unrelated constructions.


Part I
Systematic reconstruction of Hyperseed
concepts
6    Phenomenological primitives
Roadmap
This section turns the most primitive Hyperseed vocabulary into a small, typed interface. The guid-
ing principle is that the primitives should be structural rather than verbal: the mathematics should
remain invariant under renaming of symbols, choice of language, and (to a large extent) choice of
representational format. In practice, “typed interface” means that each primitive comes with an
explicit domain of application (what sort of experiential item it ranges over) and a codomain of


                                                  99
evaluation (what sort of value it returns), so that later constructions can be checked for compo-
sitional well-formedness rather than defended only by prose. The intended effect is analogous to
exposing an API: once the minimal signatures are fixed, alternative phenomenological stories can
be layered on top without modifying the underlying formal objects. This is also why the early
definitions are deliberately austere: the goal is not to capture every nuance of introspective report,
but to isolate a stable core that is preserved across rephrasings, translations, and modeling choices.

Remark 171. The philosophical stance here is deliberately Russellian in its demand for clarity: if
two descriptions differ only by a renaming of symbols, then whatever is essential has not changed.
But it is also Peircean in its tolerance for “signs” whose meaning depends on use: the same ex-
periential content can be regimented differently in different contexts, without supposing that one
regiment is the one true metaphysical grammar [14]. In the Hyperseed ontology [1], this structural
emphasis is what permits a single formal core to underwrite multiple phenomenological and scien-
tific readings. A useful way to reconcile these attitudes is to treat the formalism as fixing invariants
(what must be preserved under admissible transformations), while leaving room for multiple coor-
dinatizations (how those invariants are presented, narrated, or operationalized). Thus the text will
repeatedly separate (i) the minimal algebraic or relational constraints that a primitive must satisfy
from (ii) any particular interpretation in terms of language, imagery, embodiment, or cognitive
architecture. The reader should therefore not expect the primitives to settle interpretive disputes;
rather, they provide a common frame in which such disputes can be stated precisely as questions
about which additional axioms, identifications, or equivalences are being assumed.

    We proceed in three steps. First we introduce occasions of experience as the basic carriers of
primitive phenomenology, together with contexts that implement observer-relativity. Here “occa-
sion” should be read neutrally as a minimal unit of phenomenal bearing (whatever ultimately plays
the role of a token of experience in the theory), while “context” names the parameter that records
the standpoint relative to which evaluations are made. The point of making context explicit is
to prevent hidden shifts of reference: many apparent paradoxes about sameness or difference in
experience dissolve once one distinguishes differences across occasions from differences induced by
changing the evaluative frame. Second we define the core pairwise experiential relations (difference,
distinction, repetition, variety, non-duality, non-dual variety) using p-bit-valued evaluations. The
use of p-bit-valued outputs is meant to keep the interface flexible: it accommodates crisp/bivalent
judgments as a special case, while also permitting graded, partial, or context-sensitive assessments
without changing the type signature of the primitives. It also forces a discipline about what is
being asserted: instead of saying “x and y are different” as an untyped slogan, one records how and
to what extent a given context rates them as different, and one can later study how such ratings
compose. Third we formalize the Peircean/Jungian numerical-metaphysical categories First, Sec-
ond, Third, Fourth as an inductive ladder of relational constructions. The intended reading is that
these categories are not introduced as mysterious primitives in their own right, but as progressively
richer patterns that can be built from the earlier relational vocabulary (so that “Thirdness,” for
example, is expressed as a certain kind of mediated or triadic structure rather than a mere label).
We conclude by formalizing presentational immediacy (intensity) and the abstract/concrete distinc-
tion. These closing notions serve two roles: they connect the relational core to phenomenological
salience (why some distinctions matter more than others in lived experience), and they provide a
handle for later passages where the theory must distinguish between structural descriptions and
the more “felt” or “given” character of an occasion.




                                                  100
Hyperseed concepts covered
• Occasions of experience.

• Difference; distinction; repetition; variety; non-duality; non-dual variety.

• First; second; third; fourth.

• Presentational immediacy (intensity).

• Abstract/concrete.

The list above is meant as a contract with the reader: later sections will freely reuse these terms,
but only after they have been pinned down here in a way that supports reparameterization by
context and comparison across representational choices. In particular, each named relation will
be introduced so that it can be applied uniformly to occasions across diverse modeling settings
(introspective reports, cognitive architectures, or scientific proxies), with any domain-specific as-
sumptions made explicit as additional structure rather than smuggled into the primitive itself.

6.1   Occasions and contexts
Hyperseed begins from occasions of experience: primitive experiential “atoms” that do not presup-
pose an external experiencer, except in the minimal sense that an occasion “is what it is” from
its own inside. The mathematical reconstruction makes two moves that keep this notion precise
without over-committing metaphysically:

1. We treat occasions as objects in a structure that only cares about identity up to equivalence.

2. We treat every act of distinction-making as context-indexed (observer-relative), implemented by
   explicit context data.

Definition 37 (Occasion space). An occasion space is a small (∞, 1)-groupoid E. Its objects
Ob(E) are occasions. A 1-morphism f : o → o0 represents an admissible “identification” or “trans-
port” between occasions (e.g. recognizing the same thing under a change of viewpoint), and higher
morphisms encode coherent equivalences between such identifications.
   In toy models one may replace E by an ordinary groupoid, or even by a set E (regarding only
equality), by applying the truncation π0 .
Remark 172 (Intuition and examples for occasion spaces). This definition packages a simple idea:
experience does not usually present us with an inflexible equality relation, but rather with a family
of ways of treating two occasions as “the same enough.” A groupoid is the algebraic prototype of
this: objects are things, arrows are reversible identifications, and composition expresses chaining
of identifications. The notation (∞, 1) indicates that we may also want to track identifications-
between-identifications (and so on), because in many domains the coherence of how we identify
things matters as much as the identification itself.
    A minimal example is a set E of snapshots of sensory input, where the only identifications are
equalities; this is the discrete groupoid case. A slightly richer example is a groupoid whose objects are
images, and whose arrows are invertible transformations (e.g. rotations) that a perceptual system
treats as preserving “the same object.” The utility of the definition is that it gives us a disciplined
place to put “sameness up to viewpoint” without prematurely choosing a metric, a probability model,
or a logical theory. This is congenial to process views in the spirit of Whitehead, where the primitive
units are occasions and their relations, not enduring substances [15].

                                                  101
Remark 173 (Why (∞, 1)?). Hyperseed uses language like “interchangeable in a context” and
(later) “self-model recursion”. These are naturally modeled using identity-up-to-equivalence rather
than rigid equality. An (∞, 1)-groupoid is the minimal formal object that (i) admits nontrivial
identifications and (ii) keeps track of coherence of identifications. Nothing in the present section
depends on advanced higher-categorical technology; we use the (∞, 1) language mainly to record that
such coherence data may matter later.

Remark 174 (Notation clarification). Here E denotes the occasion space; Ob(E) is the set (or
class) of objects of E; and a “1-morphism” f : o → o0 should be read as a directed identification
from o to o0 (invertible up to higher structure in an (∞, 1)-groupoid). The truncation π0 is the
operation that forgets higher identifications and keeps only connected components, i.e. “equivalence
classes up to identification.”

Definition 38 (Contexts). A context (or viewpoint) is a tuple
                                                           
                                    c := Xc , Πc , δc , ιc

where:

• Xc is a set of presented entities (what the context treats as the “things” it can refer to);

• Πc : Ob(E) → Xc is a presentation map (a coarse-graining of occasions into context-level enti-
  ties);

• δc : Xc × Xc → V is a p-bit-valued distinctness evaluator;

• ιc : Xc × Xc → V is a p-bit-valued interchangeability evaluator.

We interpret δc (x, y) as evidence for/against the proposition “x and y are distinct (diverge)”, and
ιc (x, y) as evidence for/against “x and y are interchangeable for the purposes relevant to c.”

Remark 175 (Intuition, examples, and why contexts are necessary). A context c is the formal
surrogate for “an observer-as-a-way-of-carving.” The set Xc is what the context can even name;
the map Πc says which raw occasions are presented as which named entities; and the evaluators
δc , ιc say how the context judges difference and substitutability. This makes observer-relativity a
matter of explicit structure rather than a vague proviso. It also makes room for paraconsistent
judgments: a context may have simultaneously high evidence for “distinct” and high evidence for
“not distinct,” a point developed below using p-bit semantics (see also paraconsistent treatments
such as [23, 24]).

Remark 176 (Distinctness versus interchangeability). Although δc and ιc are related in ordinary
language, we do not assume that one is the logical negation of the other. In many practical situations
a context can regard two entities as distinct (they differ in some tracked respect) while still treating
them as interchangeable for the tasks at hand (the difference is irrelevant), and conversely it can
regard two entities as not distinct in some coarse description while refusing to substitute one for
the other (e.g. due to causal, temporal, or deontic constraints). Formally, allowing δc and ιc to
vary independently is what lets the framework represent “same object, different role” and “different
object, same role” judgments without forcing a single equivalence relation to do all conceptual work.

Remark 177 (Contexts as V-valued relations). The evaluators δc , ιc can be read as V-valued binary
relations on Xc . This viewpoint emphasizes that a context need not deliver crisp Boolean predicates
but rather graded and potentially inconsistent evidence states, with V serving as the codomain of

                                                  102