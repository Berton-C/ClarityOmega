# 13 Mind, representation, and perception

Remark 533. Special cases: Boolean and [0, 1]-valued kernels If V = {⊥, >} with ⊕ = ∨
and ⊗ = ∧, then A is an ordinary binary relation on P , s is a subset indicator, and (A ? s)(q) = >
exactly when there exists some p ∈ P with s(p) = > and A(p, q) = >. In other words, A ? s becomes
one-step reachability along directed edges. If V = [0, 1] with ⊕ = max and ⊗ = ·, then A ? s
computes a “max-product” propagation common in fuzzy relation equations and certain log-domain
message-passing schemes; the present setup can be read as a multi-channel generalization of that
idea.
Remark 534. If P is finite, A can be viewed as a |P | × |P | matrix over a quantale semiring,
and A ? s is the usual matrix-vector multiplication with ⊕ as addition and ⊗ as multiplication
(Section 3.4).
Remark 535 L    (Monotonicity: propagation respects the V -order). Because ⊗ is monotone in each
argument and        is a join, the map s 7→ A ? s is monotone with respect to the pointwise order on
  P
V . Concretely, if s ≤ t pointwise, then (A ? s) ≤ (A ? t) pointwise. This is one of the reasons
quantales are a convenient ambient algebra: order-theoretic properties needed for iterating updates
(e.g. existence of least fixed points) come for free under mild additional assumptions.
   To allow both habit formation and habit decay (reversal), we include an explicit “persis-
tence/forgetting” factor.
Definition 147 (Persistence/decay scalar). Let d ∈ V . Given a state s : P → V , define the
pointwise scaled state
                                   (d s)(p) := d ⊗ s(p).
For the p-bit quantale V = [0, 1]2 with ⊗ given by componentwise multiplication, choosing d =
(d+ , d− ) with d+ , d− ∈ [0, 1] scales down both positive and negative evidence.
Remark 536 (Intuition: persistence as inertia, decay as forgetting). The role of d is to encode
what remains of the old support if nothing else happens. If d = e (the quantale unit), then d s = s
and the past persists perfectly. If d is strictly smaller (in an appropriate scalar sense), then the
past is discounted, capturing forgetting or habit reversal by attrition.
    In the p-bit toy case with componentwise multiplication, taking d = (0.95, 0.95) is literal expo-
nential decay applied symmetrically to both evidence channels. One can also imagine asymmetric
decay, e.g. (0.95, 0.7), representing a context that retains positive evidence longer than negative
evidence (or vice versa).
Remark 537 (On choosing d: timescales and stability heuristics). Heuristically, d sets a memory
timescale: values closer to the unit e correspond to long persistence, while values farther from
e enforce faster turnover. In many concrete instantiations (e.g. V = [0, 1] or V = [0, 1]2 with
multiplicative ⊗), choosing d strictly below e also prevents indefinite accumulation from persistence
alone and makes it easier for new input ut to reshape the state, which matches the intended “habit
can change” reading.
Definition 148 (Habit dynamics operator). Fix a reinforcement relation A : P × P → V and a
persistence/decay scalar d ∈ V . Let ut : P → V be an external input sequence.
    Define the update operator UpdA,d,ut : V P → V P by
                               UpdA,d,ut (s) := ut ⊕ (d   s) ⊕ (A ? s),
where ⊕ on the right-hand side is applied pointwise in V P .
   A habit dynamics in a context is any process satisfying
                                        st+1 = UpdA,d,ut (st ).

                                                 246
Remark 538 (Interpretation: superposition as join, not arithmetic addition). The use of ⊕ (join)
rather than a numeric sum is deliberate: the update aggregates contributions according to the
evidence-combination logic encoded by V . In max-like quantales, this corresponds to a “winner-
take-strongest” or “most-supported” aggregation; in other quantales, ⊕ can encode alternative com-
bination rules (e.g. logical disjunction, cost minimization, or other idempotent semiring behaviors).
Thus, although the formula resembles a linear recurrence, it is best read as a generic evidence
propagation rule parametrized by the choice of quantale semantics.
Remark 539 (Iterating the operator: trajectories and equilibria). Given an initial state s0 , the
dynamics defines a trajectory s0 , s1 , s2 , . . . by repeated application of UpdA,d,ut . When ut = u is
time-independent, one can ask for a (contextual) equilibrium state s∗ satisfying
                                     s∗ = u ⊕ (d    s∗ ) ⊕ (A ? s∗ ),
i.e. a fixed point of the update. Because the update is built from monotone operations, fixed-point
methods (least/greatest fixed points, Kleene iteration) are natural tools when additional conditions
ensuring convergence are available in the chosen V and in the scale of P .
Remark 540 (Intuition: three sources of support). The update is the join of three contributions:
(i) ut , the new stimulation (what the world, body, or other subsystems inject at time t); (ii) (d
s), persistence (what the system carries forward from its own past); and (iii) (A ? s), internal
propagation through the pattern web. This is deliberately schematic: it abstracts the idea that habit
is neither purely memory nor purely current stimulus, but a synthesis in which the web’s structure
re-expresses and amplifies what is already present.
    A minimal worked toy example: let P = {p, q} and suppose ut stimulates only p. If A(p, q)
is large, then even with ut (q) = 0 the pattern q can grow over time because it is downstream of
p. Thus “habit-taking” can appear as a derived phenomenon: repeated stimulation of one pattern
recruits others via the web.
Remark 541 (Reading A ? s as self-weaving reinforcement). The term A ? s formalizes the “self-
weaving” aspect of a pattern web: whenever a pattern becomes supported, it can in turn become
a source of support for other patterns according to the context-specific kernel A. In this sense, A
is not merely a static adjacency structure; it is a learned or given bias about which co-activations
tend to follow which other activations, and the update equation makes that bias operational as a
propagating field over P .
Remark 542 (About 0 and “no input”). When we write 0 for a relation or state, we mean the
bottom element in the appropriate function space: for a state s : P → V , 0 is the constant function
p 7→ ⊥V (the bottom of V ); for a relation A : P × P → V , 0 is the constant relation (p, q) 7→ ⊥V .
In the p-bit toy quantale, ⊥V = (0, 0).
    It is worth emphasizing the semantic distinction between absence of evidence and negative
evidence: writing 0 encodes the former, i.e. that no support is present (or no coupling is present)
in the sense of the order of V . This is not the same as assigning a special “inhibitory” value unless
such inhibition is explicitly represented by elements of V and their order (in which case the bottom
element would still be the least inhibitory/least supportive option, not an additional kind of signal).
In particular, “no input” means that the exogenous drive term contributes the least possible value
everywhere, not that the node is removed from P or that the dynamics is undefined.
    Concretely, if the update rule combines terms by ⊕ (a join), then using 0 behaves as an identity
for “adding nothing” in the lattice-theoretic sense: x ⊕ ⊥V = x. Likewise, using A = 0 means no
propagation through the web, since every path contribution is uniformly bottom and hence cannot
raise any join.

                                                   247
Remark 543 (Special cases). • Pure reinforcement (no forgetting): d = e and ut ≡ 0 (bottom
 element), so st+1 = st ⊕ (A ? st ). This is inflationary and models cumulative habit formation.
 In this case, any node can only keep or increase its current level of support, and the only source
 of further increase is the propagation term A ? st . If one iterates this update from a given initial
 seed, one obtains an increasing chain of states (with respect to the pointwise order) whose growth
 is controlled entirely by the connectivity pattern encoded in A.

• Pure decay (no reinforcement): A = 0 and ut ≡ 0, so st+1 = d st . If d is strictly below the
  unit in an appropriate scalar sense, this models habit reversal via forgetting. Here the dynamics
  factorizes across nodes: each st (p) evolves independently by repeated scaling, so any nontrivial
  long-range structure disappears and the web plays no role. This clarifies why forgetting alone
  cannot create new tendencies: it can only attenuate what is already present.

• Driven dynamics: nontrivial ut models repeated external stimulation; the long-run effect depends
  on how A propagates and amplifies the input. In particular, even if ut is localized in P (e.g. non-
  bottom on a small set of nodes), repeated application of the update can spread that support along
  edges where A is non-bottom, creating a broader pattern. Depending on whether decay dominates
  reinforcement, the result may settle to a stable pattern, oscillate in response to time-varying ut ,
  or keep accumulating if the update is inflationary.
Proposition 17 (Monotonicity of the habit update). For fixed A and d, the map s 7→ UpdA,d,u (s) is
monotone in s (order-preserving). It is also monotone in u and in A (pointwise order on relations).
Remark 544 (Meaning and why it matters). This proposition says: if you start with more sup-
port, you cannot get less support after one update; likewise, stronger input and stronger couplings
cannot decrease the next state. It is a minimal coherence condition for a reinforcement-style model.
Without it, one could not reliably connect structural properties of A and u to the emergent time-bias
criteria of Definition 144, nor could one safely apply standard fixed-point tools later in the section.
    Monotonicity is also the bridge to closure constructions: order-preserving inflationary operators
are precisely the terrain in which Knaster–Tarski/Kleene style least-fixed-point reasoning becomes
available, a theme that will recur in other Hyperseed stability analyses [10].
    A further reason monotonicity matters is interpretability under parameter changes. If A ≤ A0
pointwise, then any explanation phrased as “increasing a coupling” becomes unambiguous: the model
guarantees that such a change cannot reduce downstream support in the next step, so comparative
statics can be done at the level of the order on V . Similarly, if u ≤ u0 , then increasing the external
drive is guaranteed not to suppress any node, which matches the intended “reinforcement” reading
of ⊕ as accumulation rather than competition.
Proof. Each component of UpdA,d,u (s) is built from ⊕ and ⊗ and a join over p ∈ P . In a quantale, ⊗
is monotone in each argument and distributes over arbitrary joins, and ⊕ is a join hence monotone.
Therefore increasing s, u, or A can only increase the result.
    More explicitly, the relevant order is the pointwise order on functions P → V and P × P → V :
we write s ≤ s0 iff s(p) ≤ s0 (p) for all p ∈ P , and A ≤ A0 iff A(p, q) ≤ A0 (p, q) for all p, q ∈ P .
Fix p0 ∈ P . The value UpdA,d,u (s)(p0 ) is obtained by combining      (via ⊕) contributions such as
(d s)(p0 ), u(p0 ), and the propagated term (A ? s)(p0 ) = p∈P A(p0 , p) ⊗ s(p). If s ≤ s0 , then
                                                               L
for each p we have A(p0 , p) ⊗ s(p) ≤ A(p0 , p) ⊗ s0 (p) by monotonicity of ⊗ in its second argument,
hence taking the join over p preserves the inequality, yielding (A ? s)(p0 ) ≤ (A ? s0 )(p0 ). The
same pointwise reasoning applies to u ≤ u0 (monotonicity of ⊕ in the corresponding argument)
and to A ≤ A0 (monotonicity of ⊗ in its first argument), establishing monotonicity in all stated
parameters.

                                                  248
Proof sketch. The update operator is assembled from monotone building blocks. Pointwise,     L it
is a join of three terms. Joins are monotone; ⊗ is monotone in each argument; and the          p∈P
aggregation preserves monotonicity because it is itself a join. Therefore any pointwise increase in
s, u, or A propagates through the formula without creating decreases.
    Equivalently, one can view UpdA,d,u as a composition of monotone maps between complete
lattices: first apply scalar/pointwise transformations (such as s 7→ d s), then apply the linear-
propagation map s 7→ A ? s, and finally merge all contributions by ⊕. Since the composition of
monotone maps is monotone, the whole update is monotone.                                         

Remark 545 (Visual intuition). If one imagines the web as channels that can only transmit or
accumulate support (in the sense encoded by V ), then “adding” an extra amount of support at any
node cannot rationally lead to less support downstream if the update consists only of propagation
and accumulation. The proposition is the algebraic reflection of this picture.
    The same picture applies to the parameters: increasing an edge weight in A corresponds to
widening a channel, and increasing u corresponds to injecting additional support at some nodes.
If the dynamics had subtractive or normalizing steps, such monotonicity could fail; the present
formulation avoids that by restricting to the order-theoretic primitives ⊕, ⊗, and joins.

    Monotonicity (Proposition 17) is a minimal sanity property: stronger present support or stronger
couplings cannot lead to weaker next-step support. In particular, it ensures that iterating the up-
date from 0 yields a well-defined increasing approximation process whenever the update is also
inflationary, setting up the later use of least fixed points as canonical “habit closures” of a seed
state.

12.3    Self-weaving webs and autocatalytic closure
Hyperseed’s “self-weaving web” notion is meant to capture a pattern network whose own internal
structure reinforces and recreates itself. In our setting, this becomes a fixed-point and closure story
for the propagation operator.

Definition 149 (One-step closure operator). Fix A : P × P → V . Define the inflationary operator

                                        ClA (s) := s ⊕ (A ? s).

Remark 546 (Intuition: adding what the web can infer/propagate in one step). ClA (s) takes a
support state and enriches it by one round of internal propagation. If s is a seed, then (A ? s) is
what the web can “grow” from that seed in one step, and the join ⊕ records that we keep the original
seed support as well. This is the basic algebraic gesture behind “weaving”: we do not replace the
old pattern; we overlay it with its consequences.
                                                                  (0)           (n+1)              (n)
Definition 150 (Iterated closure and Kleene star). Define ClA (s) := s and ClA (s) := ClA (ClA (s)).
   When V P is a complete lattice (e.g. P finite and V complete), define the limit (join of the
ascending chain)
                                       (ω)
                                                M (n)
                                     ClA (s) :=     ClA (s).
                                                   n≥0

Also define powers of A by relational composition: A0 := I (identity relation) and An+1 := An ◦ A.
Then define the Kleene star                      M
                                          A∗ :=     An .
                                                   n≥0



                                                 249
Remark 547 (Notation unpacking: An and A∗ as “all finite paths”). The composition An is the n-
step reinforcement relation: A2 (p, r) aggregates reinforcement along all two-edge paths p → q → r,
and so on. Thus A∗ is the join of all An , i.e. the aggregate relation capturing reinforcement along
any finite chain. This is the same algebraic pattern behind Kleene star in automata theory and
Kleene algebras, here expressed in quantale language.
                   (ω)
    Accordingly, ClA (s) is the seed s closed under repeated propagation: what you get by allowing
the web to “echo” its own implications arbitrarily many times, without invoking any infinitary paths
beyond the join already present in the lattice structure.

Theorem 12 (Closure as least fixed point; explicit A∗ form). Assume P is finite and V is a
commutative quantale. Then for every seed state s : P → V :
                (0)        (1)                                          (ω)
1. The chain ClA (s) ≤ ClA (s) ≤ · · · is ascending and has a join ClA (s).
     (ω)
2. ClA (s) is a fixed point of ClA , and is the least fixed point of ClA above s.

3. The fixed point can be written as
                                              (ω)
                                            ClA (s) = A∗ ? s.

Remark 548 (Plain-English statement and why it is central here). Start with some initial support
s. Apply one-step closure, then close again, and so on. Because closure only adds support (never
subtracts), this produces an ascending sequence. The theorem says there is a well-defined “limit”
state obtained by joining all these stages, and that this limit is exactly the smallest self-consistent
state containing the seed: once you reach it, closing again adds nothing new.
    This is important because it gives a rigorous meaning to “self-weaving” as a fixed-point phe-
nomenon. Instead of narrating that the web “recreates itself,” we can point to a precise object
  (ω)
ClA (s) and identify it both as a least fixed point and as an explicit propagation construction A∗ ? s.

Remark 549 (Connection to the rest of the document). Fixed-point characterizations of “stable
organization” recur in later discussions of agency and goal stability. The present theorem is a local,
pattern-web-scale instance of that general motif, akin in spirit to other fixed-point applications in
Hyperseed analyses [10].

Proof. (1) ClA is inflationary because ClA (s) = s ⊕ (A ? s) ≥ s, so iterating yields an ascending
chain. Since V P is complete (finite product of complete lattices), the join exists.
    (2) Monotonicity of ClA and completeness of V P imply the set of fixed points is nonempty and
forms a complete lattice (Knaster–Tarski). Because ClA is inflationary, the join of the iterates from
s is a post-fixed point; a standard argument (Kleene fixed-point theorem in complete lattices for
such algebraic operators) gives it is the least fixed point above s.
                                            (n)
    (3) Unfolding the recurrence shows ClA (s) = nk=0 Ak ? s. Taking n≥0 and using distribu-
                                                     L                     L
tivity of ⊗ over joins yields A∗ ? s.

Proof sketch. The operator ClA is inflationary and monotone, so iterating it from a seed produces
an ascending chain. In a complete lattice, the join of this chain exists. Standard fixed-point theory
says that for such operators, this join is the least fixed point above the seed. Finally, expanding
  (n)
ClA (s) shows it collects exactly the contributions along paths of length at most n, hence the ω-join
corresponds to summing over all finite path lengths, which is precisely A∗ ? s.                    

Remark 550 (Key steps: why they work). The essential technical facts are (i) completeness
of V P when P is finite, (ii) monotonicity and inflationarity of ClA , and (iii) distributivity of

                                                    250
⊗ over joins (the quantale axiom). Inflationarity ensures we have an increasing approximation
sequence; distributivity ensures we can commute propagation with taking joins, so that “propagate
after joining” matches “join after propagating.” This is why the explicit formula A∗ ? s appears: it
is the algebraic normal form of “all finite chains of reinforcement.”
    Concretely, when P is finite and V is complete, the pointwise orderLmakes V P a complete lattice,
so the iteration s ≤ ClA (s) ≤ Cl2A (s) ≤ · · · has a well-defined join n≥0 ClnA (s). Monotonicity is
what guarantees that these iterates are comparable and that joins of approximants behave as expected
under further applications of ClA ; in standard fixed-point terms, this is exactly the hypothesis one
needs for a least fixed point construction in a L
                                                complete lattice. In typical quantale semantics one can
also unpack A as a Kleene-style star, A = n≥0 A⊗n (with A⊗0 the identity relation), so that the
               ∗                           ∗

closed-form expression A∗ ?s is literally the join of all n-step propagations A⊗n ?s. The distributivity
axiom is what lets this decomposition be pushed through the ?-action: it ensures that accumulating
alternative routes of support (joins) is compatible with composing successive reinforcements (tensor
products), so that the closure captures “all ways of getting there” rather than privileging a particular
bracketing of compositions.

Remark 551 (Hyperseed reading). A∗ ? s is the total “downstream closure” of an initial seed s
under the reinforcement relation A: it aggregates the support transmitted along all finite reinforce-
ment chains. This is a precise sense in which repeated co-occurrence and associative structure can
“weave” a larger support pattern from a smaller seed.
    Equivalently, if one defines s0 := s and sn+1 := sn ⊕ (A ? sn ), then the increasing family
(sn )n≥0 is an explicit approximation to the closure, and A∗ ? s is the join of all stages of this
self-amplifying propagation. This makes clear that no single application of A is privileged: what
matters is the accumulation of support across any finite number of reinforcement steps, including
the possibility of revisiting intermediate patterns and thereby compounding evidence. In particular,
if s concentrates mass on a small set of generators, then A∗ ? s describes the full footprint of what
those generators can collectively activate, modulated by the weights in A and the way ⊗ combines
successive transmissions.

Remark 552 (Geometric/graph intuition). In graph terms, A∗ ? s assigns to each node q the
aggregate influence of all directed paths starting at any seed node, with path contributions combined
multiplicatively along edges (via ⊗) and aggregated across alternative paths (via ⊕). If one pictures
each edge as a conduit that attenuates and possibly distorts evidence, then A∗ is the total field of
influence generated by repeatedly sending signals through the network.
    One can read A∗ as the weighted reachability relation: (A∗ )(q, p) is the total support by which
p can be reached from q through any finite directed walk, with composition of edges evaluated by ⊗
and competition/branching between walks evaluated by ⊕. On this reading, A∗ ? s is a path-sum (or
walk-sum) semantics: it is the analogue of taking a transitive closure in the crisp case, but with a
quantitative accumulation law determined by the chosen quantale. This is also why cycles matter:
feedback loops correspond to families of paths that revisit nodes, and the star construction is the
algebraic device that folds all such finite unfoldings into a single closed expression.

Definition 151 (Autocatalytic (self-weaving) support). Fix a reinforcement relation A : P × P →
V and a threshold θ ∈ V .
   A nonempty subset S ⊆ P is called θ-autocatalytic if there exists a state s : P → V such that:

1. (support on S) for all p ∈ S, s(p) ≥ θ; and

2. (self-production) for all p ∈ S, (A ? s)(p) ≥ θ.


                                                  251
A pattern web (P, A) is a self-weaving web (at threshold θ) if it contains a θ-autocatalytic subset.
    The two clauses separate “having enough of the patterns present” from “being able to reproduce
that presence using the web’s own reinforcement dynamics.” The existential quantifier over s is
important: it says that there is at least one coherent way of assigning support levels so that every
element of S is simultaneously above threshold and is simultaneously regenerated above threshold
by the influence coming from S (and possibly from outside S if s has additional mass elsewhere).
In applications one often considers s that is concentrated on S (e.g. an indicator-like state in crisp
cases, or a uniform θ-level assignment on S in graded cases), but the definition is stated to allow
any state witnessing the closure property.

Remark 553 (Intuition and a simple example). This definition formalizes the “autocatalytic set”
motif (Hyperseed-Concept 61): a set S of patterns is self-sustaining if, once S is supported above
threshold, the web dynamics generated by S re-produces support above threshold for every member
of S. In the simplest crisp case where V = {0, 1} and θ = 1, the condition says: each node in S
has at least one incoming edge from some node in S (support can be regenerated from within the
set).
    The usefulness is conceptual: it provides a minimal criterion for “the web can keep itself going”
independent of external input. In later discussions of minds and systems, this is the pattern-web
analogue of closure under production dependencies.
    In graded settings (e.g. V = [0, 1] with a t-norm for ⊗), the same clauses express that each
member of S receives enough aggregate reinforcement from the current support configuration to
stay above θ. The condition does not force a unique witness state s; rather, it identifies sets
S for which there exists at least one support configuration making S self-maintaining, and this
flexibility is often what one wants when modeling multiple possible “operating points” of a system.
Graphically, the crisp characterization can be strengthened in familiar ways (e.g. insisting on a
directed cycle through each node, or on strong connectivity), and the present definition should be
read as the quantitative analogue of such internal-regeneration conditions, expressed at the level of
the ?-propagation operation.

Remark 554. Definition 151 is intentionally minimal and matches the “autocatalytic set” motif:
each pattern in S is supported by the reinforcement generated from patterns in S itself. Stronger
definitions can require minimality of S, robustness under perturbations, or explicit compositional
generation mechanisms (Section 9).
    For example, one may ask that S be inclusion-minimal among θ-autocatalytic sets (no proper
subset has the same property), or that the inequalities hold with a margin above θ to ensure persis-
tence under small decreases of support. One may also require that the witness state s be supported
only on S (a stricter internal-closure reading), or that self-production be witnessed not just in one
step (A ? s) but as a post-fixpoint condition s ≤ ClA (s), making the closure operator itself the ob-
ject of stability. These refinements become relevant when one wants to distinguish mere possibility
of self-support from dynamical attractiveness or from modular compositionality of the generating
mechanisms.

12.4    Morphic resonance and morphic anti-resonance as cross-context coupling
Hyperseed defines morphic resonance as habit-taking among spatially separated patterns, and mor-
phic anti-resonance as the reverse. We model “spatial separation” abstractly by indexing multiple
contexts (locations, subsystems, or reality-systems) and adding coupling kernels between their
pattern webs. This formalization is mathematically orthodox (coupled dynamical systems) while
leaving room for the broader interpretive reading of morphic resonance as a nonlocal “field of habit”

                                                 252
in the sense associated with Sheldrake [13]. Concretely, “coupled dynamical systems” here means
that each context has its own local state-update rule, but the rule is allowed to depend (via an
explicit input term) on the current states of other contexts; the only “distance” notion needed is
membership in distinct indices ` ∈ L. The intent is that the coupling term is written in exactly the
same algebra as internal reinforcement, so that cross-context influence can be treated as another
instance of the same habit-amplifying mechanism, rather than as an ad hoc external disturbance.

Definition 152 (Family of contexts and internal habit kernels). Let L be an index set of contexts
(e.g. locations). For each ` ∈ L, fix:

• a pattern class P` ;

• an internal reinforcement relation A` : P` × P` → V ;

• a decay scalar d` ∈ V ; and

• an external input process u`,t : P` → V .

A global state at time t is a tuple st = (s`,t )`∈L with s`,t : P` → V .

Remark 555 (Intuition: many webs at once). One can think of each ` ∈ L as its own local pattern
web with its own internal reinforcement. The global state st is simply the collection of all local
support states at time t. This is the minimal formal move needed to discuss “at a distance”: we
do not need literal Euclidean distance, only a multiplicity of contexts and a notion of cross-context
influence.

Remark 556 (What is shared vs. what is local). Each context ` has its own pattern vocabulary
P` and its own reinforcement operator A` , so contexts can differ in what they can represent and
how quickly they self-reinforce. At the same time, all contexts share the same value object V (and
thus the same ⊕, ⊗, operations), so that internal and external influences can be aggregated in a
uniform way. This “shared algebra, distinct vocabularies” split is what makes it possible to discuss
cross-context influence even when P` and P`0 are not identical: the coupling kernels will serve as
the translation layer.

Definition 153 (Morphic coupling kernel). For ` 6= `0 , a morphic coupling kernel from `0 to ` is
a V -relation
                                   K`0 →` : P`0 × P` → V.
Its image on a state s`0 ,t is the induced input on P` :
                                                       M
                            (K`0 →` ? s`0 ,t )(q) :=           K`0 →` (p, q) ⊗ s`0 ,t (p).
                                                       p∈P`0

Remark 557 (Intuition and examples of what K`0 →` can encode). The kernel K`0 →` plays the
same mathematical role as A, but across contexts rather than within one context. In applications,
K`0 →` (p, q) could encode: (i) similarity or “translation” between pattern vocabularies P`0 and P` ;
(ii) a learned association that when p is active in one context, q tends to become active elsewhere;
or (iii) a hypothesized nonlocal coupling. In the simplest same-pattern case where P`0 = P` = P
and K`0 →` (p, q) is nonbottom only when p = q, the coupling just transmits support for a pattern to
the same pattern-index in the other context.




                                                        253
Remark 558 (Algebraic reading of the ?-action). The expression K`0 →` ? s`0 ,t is formally the
same type of construction as applying a weighted adjacency matrix to a state vector, except that the
weights and aggregations are taken in the semiring-like structure V . Intuitively, the induced support
for q ∈ P` is an ⊕-sum over all source patterns p ∈ P`0 of “(strength of link from p to q) ⊗ (current
support of p).” This makes it explicit that cross-context influence is graded and compositional:
multiple distinct source patterns can contribute to the same target pattern, and their contributions
combine by the same aggregator used everywhere else in the habit dynamics.
Remark 559 (Directionality, reciprocity, and sparsity). Nothing in Definition 153 requires K`0 →`
to equal K`→`0 (even when P` = P`0 ), so the model allows directed coupling (influence from `0 to `
without a matching reverse channel). In many applications one may impose additional structure,
e.g. reciprocity (K`0 →` related to K`→`0 ), boundedness (to prevent unrealistically large induced in-
puts), or sparsity (only a small subset of inter-context pattern pairs interact). These are modeling
choices rather than requirements of the formalism.
Definition 154 (Morphic resonance dynamics). Given internal dynamics (A` , d` ) and couplings
(K`0 →` ), define the coupled update for each ` by
                                                                   M
                       s`,t+1 = u`,t ⊕ (d` s`,t ) ⊕ (A` ? s`,t ) ⊕   (K`0 →` ? s`0 ,t ).
                                                               `0 6=`

We call this a morphic resonance dynamics when the couplings K`0 →` are intended to encode cross-
context propagation of habit bias, rather than ordinary local causal influence.
Remark 560 (Intuition: one equation, two interpretations). The equation is formally just “local
update plus cross-input from others.” The interpretive distinction is in what we take the coupling
term to mean. If the coupling is ordinary causal influence, we are modeling a standard interacting
multi-system process. If the coupling is “morphic,” we are treating cross-context similarity itself
as a conduit for habit, in the sense that a stabilized pattern in one place can seed stabilization
elsewhere without a mediated causal chain in the usual physical sense. The latter reading is the one
Hyperseed associates to morphic resonance (Hyperseed-Concept 115) and that is historically linked
to morphic field narratives [13].
Remark 561 (Time-variation and learning of couplings). Although the definition treats K`0 →`
as fixed, nothing prevents using time-indexed couplings K`0 →`,t to represent learned or adaptive
cross-context links (e.g. strengthening of translation correspondences between vocabularies). Under
such a reading, morphic resonance can be modeled either as a static “field” (fixed K) or as a co-
evolving structure where repeated co-activation across contexts modifies the coupling itself, producing
a second-order habit: a habit of coupling.
Remark 562 (Why this captures “habit-taking at a distance”). If a pattern p becomes increasingly
supported in context `0 due to its internal habit dynamics, then the induced term K`0 →` ?s`0 ,t becomes
increasingly supported (by Proposition 17), providing an increasing drive for corresponding patterns
in `. Thus the coupled system can realize the same before/after bias of Definition 144 across
separated contexts.
Remark 563 (A minimal two-context picture). For L = {`1 , `2 } the update for `1 contains exactly
one cross term K`2 →`1 ? s`2 ,t (and symmetrically for `2 ). In this simplest setting, one can interpret
morphic resonance as the claim that “whatever becomes easier to realize in `2 becomes, via the
kernel, easier to realize in `1 ”, with the particular mapping from “what” to “what” specified by the
nonbottom entries of K`2 →`1 . This makes explicit that the phenomenon is not a single scalar effect
but a structured transport of bias over a pattern vocabulary.

                                                  254
   To model morphic anti -resonance, we need a way to transport “opposition” or “reversal pres-
sure” across contexts. In the p-bit setting, negation swaps positive and negative evidence, so we
can define an “oppositional channel” by precomposing with negation.

Definition 155 (Anti-resonance via negated-source coupling (p-bit case)). Assume the p-bit nega-
tion ¬(v + , v − ) = (v − , v + ). Define an anti-resonant coupling contribution by

                               AntiRes`0 →` (s`0 ,t ) := K`−0 →` ? (¬ ◦ s`0 ,t ),

where K`−0 →` : P`0 × P` → V is a V -valued kernel. Here (¬ ◦ s)(p) means applying ¬ to the p-bit
value s(p).

Remark 564 (How anti-resonance enters the coupled update).            L In direct analogy with Defini-
tion 154, one can incorporate anti-resonant influence by adding `0 6=` AntiRes`0 →` (s`0 ,t ) as an ad-
ditional input term in the update for s`,t+1 . Operationally, this means that strong evidence for p
in context `0 can become strong evidence against related q in context `, with the mapping again
controlled by the kernel K`−0 →` . This clarifies that “anti-resonance” is not merely weaker resonance,
but a qualitatively different channel that reverses polarity at the level of evidence.

Remark 565 (Resonance and anti-resonance as distinct channels). The formalism permits both
kinds of coupling to coexist: one may have a positive (resonant) kernel K`0 →` and a negative (anti-
resonant) kernel K`−0 →` simultaneously, representing systems where some cross-context correspon-
dences reinforce while others suppress. In the p-bit interpretation, this supports mixed phenomena
such as: “pattern p in `0 makes q more plausible in `, but makes r less plausible,” with different
targets and strengths specified by the respective kernels.

Remark 566 (Intuition: transmitting “the other side” of evidence). If the source context `0 con-
tains strong negative evidence against a pattern p, then under p-bit negation this becomes strong
positive evidence for ¬p (or, more cautiously, strong positive evidence in the “negative channel” for
p). Feeding ¬ ◦ s`0 ,t through a kernel and adding it to the target dynamics allows the target to be
pushed away from the same patterns that the source is rejecting. This is an abstract formalization
of morphic anti-resonance (Hyperseed-Concept 114): not merely absence of resonance, but active
propagation of reversal pressure. Concretely, if one thinks of s`,t (p) as a two-channel evidential
                         +         −
state (e.g. s`,t (p) = (v`,t (p), v`,t (p))), then p-bit negation can be read as an operation that swaps
and/or reinterprets these channels so that “evidence against p” becomes usable input for biasing
the evolution of p-related coordinates elsewhere. In this view, the kernel is not merely a similarity
map but a transport mechanism for constraints or inhibitions: the transported signal acts like an
inhibitory coupling that suppresses the target’s tendency to reinstantiate the rejected pattern. The
qualifier “more cautiously” is important: in a paraconsistent setting, strong v − for p need not en-
tail weak v + for p, so what is reliably transmitted is the intensity of the negative channel (or the
intensity of support for ¬p), rather than a forced flip to an exclusive alternative.
    The use of paraconsistent negation here also connects to later resonance/dissonance themes
(Hyperseed-Concept 97): conflict can be transported and can seed further conflict elsewhere, rather
than being suppressed by consistency constraints (cf. paraconsistent dynamics perspectives such as
[24]). In particular, anti-resonant coupling can propagate a tension pattern even when the target
context contains its own positive evidence for p: the resulting superposition is precisely the kind
of structured incompatibility that dissonance concepts are meant to track. This clarifies why anti-
resonance is not simply “negative similarity”: it is a mechanism by which one context exports a
local veto-like signal, and the receiving context integrates it without requiring global agreement or
resolution.

                                                     255
Remark 567. There are multiple reasonable choices for anti-resonance. The above is the minimal
one that mirrors the toy computation in Section 5: it allows negative evidence in one context to
be transmitted as negative (or even as positive-for-not) evidence in another, without enforcing con-
sistency. This minimality is useful pedagogically because it makes the “sign flip” intuition explicit:
first apply ¬ at the level of evidential states, then transport via the same (or an analogous) kernel
used for resonance, and finally aggregate into the target update as an extra driving term. However,
the choice of whether to transport ¬ ◦ s`0 ,t or to transport s`0 ,t and negate after transport can matter
if the kernel is nonlinear, state-dependent, or channel-mixing; in such cases, the ordering encodes
a modeling decision about whether “reversal” is a property of the source signal itself or a property
of how the target interprets incoming information. More sophisticated anti-resonance operators
can be built using two-channel kernels that mix (v + , v − ) components asymmetrically. For instance,
one may wish to model a setting where negative evidence is more portable than positive evidence
(or vice versa), or where negative evidence produces a broad, diffuse repulsion in the target while
positive evidence produces a narrow, pattern-specific attraction. One can also introduce saturation,
thresholds, or gating so that weak negative evidence does not create spurious repulsion, while strong
negative evidence yields a robust anti-resonant push.
Remark 568 (Further modeling notes). Anti-resonance can also be interpreted as transporting a
constraint rather than transporting a hypothesis. If the source learns that p is systematically incom-
patible with its own stable trajectories, then exporting ¬p (or exporting a strong v − for p) amounts
to telling the target: “do not allocate attractor mass to p unless you have compensating evidence.”
This suggests a natural stability heuristic: anti-resonant couplings should often be scaled (e.g. by
kernel normalization or context-dependent confidence weights) to avoid globally destabilizing the
dynamics when many sources simultaneously export negative pressure. In the two-channel perspec-
tive, such scaling can be applied differently to the v + -transport and v − -transport pathways, yielding
a controlled way to represent that a system may be more conservative about spreading rejections
than about spreading endorsements (or the reverse), depending on the application.

12.5    Stability, amplification, and decay
The Hyperseed story needs three qualitative regimes:
1. amplification: repeated exposure yields increasing pattern support (habit-taking);

2. decay: support fades away (habit-reversal);

3. stabilization: a nontrivial persistent pattern-support structure emerges (habits as stable attrac-
   tors).
We give basic sufficient conditions for these regimes in a finite P setting.
Remark 569 (A philosophical aside: stability as “thirdness”). In Peircean terms, a habit is a
kind of lawfulness: not a single event (secondness) nor a mere quality (firstness), but a stabilizing
generality across time [14]. Mathematically, this is precisely what fixed points and attractors encode:
an organization that, once present, reproduces itself under the dynamics. The following estimates
and fixed-point statements are small technical shadows of this broader idea.
    One can also read “thirdness” here as the appearance of constraints that are not explicitly
imposed at each time step, but are nevertheless respected by the evolution once they have formed.
In dynamical terms, this corresponds to invariant sets, absorbing regions, or attractor basins: after
transients, the system repeatedly returns to (or remains inside) a family of states characterized by
the same structured regularities.

                                                   256
Definition 156 (A scalar upper bound for the p-bit quantale). Assume V = [0, 1]2 with compo-
nentwise order. For v = (v + , v − ) define kvk∞ := max(v + , v − ). For a state s : P → V define

                                       ksk∞ := max ks(p)k∞ .
                                                  p∈P

For a relation A : P × P → V define

                                     kAk∞ := max kA(p, q)k∞ .
                                                p,q∈P

Remark 570 (Intuition: measuring the largest evidence magnitude). The quantity kvk∞ ignores
the distinction between positive and negative channels and simply records the larger of the two. This
is a conservative measure: if either channel is large, then kvk∞ is large. For states and relations,
taking the max over all patterns (or all edges) gives a simple global bound suitable for elementary
contraction-style estimates.
    This norm-like bound is useful here not because it is subtle, but because it is easy: it lets us
give a clean sufficient condition for forgetting/decay in the toy p-bit model without developing a full
spectral theory over quantales.
    It is also worth noting what is being discarded by this bound. Because ⊕ is max, there is no can-
cellation between positive and negative evidence at the level of the semiring/quantale operations, so
an `∞ -style “largest-entry” estimate is often remarkably faithful. However, the bound still throws
away all distributional information (how many entries are large, whether large entries are iso-
lated or form reinforcing motifs, etc.), and therefore cannot distinguish between many qualitatively
different webs that share the same single largest edge weight.

Remark 571 (Operator-level intuition for the update). The homogeneous update

                                      st+1 = (d    st ) ⊕ (A ? st )

has two contributions. The term d st is a pointwise persistence/discounting term: it keeps each
pattern’s current evidence but shrinks it by a per-pattern factor d. The term A ? st is a propaga-
tion/reinforcement term: evidence at pattern p is transmitted along the edge (p, q) to contribute to
pattern q, and the join ⊕ aggregates all such incoming contributions at q by taking a componentwise
maximum. In this toy p-bit semantics, the state at time t+1 is therefore “whatever survives locally”
or “whatever is newly supported by at least one incoming source,” channelwise.

Theorem 13 (A simple decay criterion in the p-bit toy quantale). Assume P is finite, V = [0, 1]2
with ⊕ as componentwise max and ⊗ as componentwise multiplication. Consider the homogeneous
(no input) single-context update

                               st+1 = (d    st ) ⊕ (A ? st ),     ut ≡ 0.

Let ρ := max(kdk∞ , kAk∞ ). Then
                                         kst+1 k∞ ≤ ρ kst k∞ .
In particular, if ρ < 1 then kst k∞ → 0 as t → ∞, so scalar propensities pt (p) = π(st (p)) decay to
0 for both πpos and πnet .

Remark 572 (A quantitative consequence: geometric forgetting). The inequality kst+1 k∞ ≤
ρ kst k∞ iterates immediately to
                                  kst k∞ ≤ ρt ks0 k∞ .


                                                  257
Thus when ρ < 1 the decay is not only eventual but geometric, with a characteristic “forgetting
                                                                                                0 k∞ )
timescale” controlled by ρ. For example, to guarantee kst k∞ ≤ ε, it suffices that t ≥ log(ε/ks
                                                                                           log(ρ)      ,
where log(ρ) < 0. This makes explicit how stronger persistence/reinforcement (larger ρ) slows
forgetting even in the still-decaying regime.

Remark 573 (Plain-English meaning). If every edge weight in the web and the persistence factor
d are bounded by some ρ < 1 (in the conservative k · k∞ sense), then the system cannot sustain
evidence: each update step scales the maximum evidence down by at least a factor ρ. Thus, in the
absence of ongoing input, whatever support the system had is eventually forgotten. This gives a
clean sufficient condition for habit-reversal-by-decay.
    The key point is that the model has no mechanism for generating evidence “from nothing” under
ut ≡ 0: all evidence at time t+1 is obtained by multiplying previously existing evidence by quantities
in [0, 1] and then taking maxima. When all multiplicative factors are uniformly < 1, even the most
favorable reinforcement path cannot avoid overall shrinkage.

Remark 574 (Why this is connected to earlier habit definitions). Under ρ < 1, the scalar propen-
sities pt (p) decrease to 0 regardless of scalarization choice among πpos and πnet . Hence, for suf-
ficiently large T , “after T ” averages become smaller than “before T ” averages, aligning with the
habit-reversal direction in Definition 144.
    More explicitly, because both πpos (v) and πnet (v) are bounded above by kvk∞ (up to the trivial
clipping to [0, 1] in the net case), one has a uniform implication of the form

                       kst k∞ → 0       =⇒      π(st (p)) → 0 for each fixed p ∈ P,

so any average-of-propensities criterion based on time windows will eventually detect a decline.

Proof. Fix q ∈ P . Using the definitions and that ⊕ is max while ⊗ is multiplication (component-
wise), we have
                                  k(d st )(q)k∞ ≤ kdk∞ kst k∞ ,
and also

                           M
       k(A ? st )(q)k∞ =         A(p, q) ⊗ st (p)       ≤ max kA(p, q)k∞ kst (p)k∞ ≤ kAk∞ kst k∞ .
                                                           p∈P
                           p∈P
                                                    ∞

Taking the max of these two bounds yields kst+1 (q)k∞ ≤ ρ kst k∞ . Finally maximize over q ∈ P .

Remark 575 (Where finiteness enters). The assumption that P is finite ensures that the maxima
in Definition 156 are attained and that the propagation bound

                           M
                                 A(p, q) ⊗ st (p)       ≤ max kA(p, q)k∞ kst (p)k∞
                                                          p∈P
                           p∈P
                                                    ∞

is literally a bound by a finite maximum. Conceptually, the same proof pattern extends to infinite
P if one replaces maxima by sups and assumes the relevant sups exist in [0, 1]. The present finite
setting keeps the estimate elementary and avoids measure-theoretic or completeness issues that are
orthogonal to the qualitative message about decay.




                                                        258
Proof sketch. Bound each component of the next state by separately bounding the persistence term
and the propagation term. Because the join ⊕ is componentwise max, the magnitude of the join is
at most the maximum of the magnitudes. Because ⊗ is componentwise multiplication, magnitudes
multiply. Taking maxima over p (for propagation) and then over q (for the whole state) yields the
stated inequality, which iterates to show convergence to 0 when ρ < 1.                         
Remark 576 (Commentary). The proof is a straightforward “largest-entry” estimate: it ignores
cancellations (there are none, since ⊕ is max) and tracks only the largest evidence component
present anywhere. This is why the conclusion is a sufficient condition: many webs will still decay
even when ρ ≥ 1, but ρ < 1 guarantees decay by a simple contraction argument.
    One can compare this to classical matrix norm bounds: in linear systems, a condition like
kAk < 1 implies contraction and hence decay, while kAk ≥ 1 is inconclusive because the true
stability threshold is governed by more refined structure (eigenvalues/spectral radius). Here the
estimate plays the same role: it is intentionally crude but robust, and it emphasizes the logical
shape of the argument (“uniform shrinkage everywhere implies global forgetting”) rather than the
sharp boundary between stability and instability.
Remark 577 (Interpretation). The condition ρ < 1 says that neither persistence nor reinforcement
is strong enough to maintain evidence; the web forgets. This is a clean sufficient condition for habit-
reversal in the absence of ongoing input.
    Equivalently, every path by which evidence might persist—either by staying at a node via d or
moving along an edge via A—incurs at most a factor ρ < 1 per step in the channelwise magnitude.
Even if the system continually selects the “best” incoming support at each step (because ⊕ is max),
it still cannot overcome the uniform multiplicative discounting.
Remark 578 (A minimal illustrative example). Consider P = {1, 2}, with a single nonzero edge
                                                   −             + −               + − + − + −
A(1, 2) = (a+ , a− ) and persistence d(1) = (d+
                                              1 , d1 ), d(2) = (d2 , d2 ). If max(d1 , d1 , d2 , d2 , a , a ) <
1, then regardless of where evidence starts (at node 1 or node 2), each time step multiplies every
available contribution by a factor < 1 before taking maxima, so the overall magnitude must shrink.
This makes concrete that the condition does not depend on detailed topology: even a “chain” that
can move evidence forward cannot preserve it without at least one unit-sized multiplicative channel
somewhere.
   Amplification and stabilization typically require persistent input and/or autocatalytic structure.
Proposition 18 (Driven closure yields a stable attractor in the inflationary case). Assume d = e
(no decay) and ut ≡ u is constant. Then the update

                                         st+1 = u ⊕ st ⊕ (A ? st )
                                                                     L
produces an ascending chain s0 ≤ s1 ≤ · · · whose join s∞ :=             t≥0 st exists and satisfies

                                           s∞ = u ⊕ (A ? s∞ ).

If u 6= 0 and A connects u to many patterns, then s∞ exhibits habit-taking (Lemma 3). Moreover,
the statement is order-theoretic: the inequality s0 ≤ s1 ≤ · · · is interpreted
                                                                      L         pointwise in V P (i.e.,
for each pattern p ∈ P we have st (p) ≤ st+1 (p) in V ), and the join t≥0 st is taken in the complete
lattice V P (again pointwise).
Remark 579 (What this proposition says). With no forgetting (d = e) and a constant source of
stimulation u, the system’s support can only increase over time. Thus it converges (in the order-
theoretic sense of taking the join of an ascending chain) to a stable state s∞ . The fixed-point

                                                    259
equation s∞ = u ⊕ (A ? s∞ ) says: at equilibrium, the support is exactly what is injected plus what
the web can propagate from that equilibrium.
    This is the simplest formal incarnation of “habits as stable attractors” in this framework. It
is not a metric convergence statement; it is the order-theoretic statement appropriate to quantale-
valued, possibly paraconsistent support. In particular, nothing here presupposes that supports are
real numbers with a topology, nor that successive states become close in any metric; instead, the
chain stabilizes in the sense that it reaches the least upper bound of all iterates. Equivalently, s∞
is the least element (with respect to ≤) that simultaneously dominates the initial iterates and is
closed under the update rule. Because the update includes the explicit persistence term st , the map
F (s) := u ⊕ s ⊕ (A ? s) is inflationary (s ≤ F (s)), and s∞ can be viewed as the closure obtained by
repeatedly applying F starting from s0 .

Proof. Inflationarity is immediate because st+1 ≥ st pointwise. Completeness of V P gives existence
of s∞ . Monotonicity plus distributivity of ⊗ over joins yields the fixed-point equation at the join.
More explicitly, define F (s) := u ⊕ s ⊕ (A ? s). The update is st+1 = F (st ), and since F is monotone
and inflationary,
       L           the sequence (st )t≥0 is an ascending chain. By completeness of V P , the join
s∞ = t≥0 st exists. Then, using monotonicity of F and that ⊕ computes joins, one has
                                                                         M       M 
                        F (s∞ ) = u ⊕ s∞ ⊕ (A ? s∞ ) = u ⊕                 st ⊕ A ?  st ,
                                                                           t≥0              t≥0

and
 L the distributivity/continuity
            L                    property for ? (spelled out in Remark 580 below) yields A ?
( t≥0 st ) = t≥0 (A ? st ), so
                               M             M                   M                        M
              F (s∞ ) = u ⊕           st ⊕         (A ? st ) =         u ⊕ st ⊕ (A ? st ) =  st+1 = s∞ ,
                                t≥0          t≥0                 t≥0                         t≥0

where the last equality uses that the join of the tail {st+1 : t ≥ 0} is the same as the join of the
whole chain {st : t ≥ 0}. Finally, since s∞ = s∞ ⊕ u ⊕ (A ? s∞ ) implies s∞ ≥ u ⊕ (A ? s∞ ) and also
s∞ ≤ u ⊕ (A ? s∞ ) ⊕ s∞ , the displayed fixed-point identity s∞ = u ⊕ (A ? s∞ ) follows because ⊕ is
idempotent and s∞ ⊕ s∞ = s∞ .

Proof sketch. The update map is inflationary, so iterating it yields an ascending chain. In a complete
lattice, the join of this chain exists. Taking the join on both sides of st+1 = u ⊕ st ⊕ (A ? st ) and
using that ⊗ distributes over joins lets us pass the join through the propagation term, producing
the fixed-point equation for s∞ . One can read this as a standard “iterate-and-take-the-supremum”
construction: s∞ collects everything that can be reached from the seed s0 by any finite number
of applications of the forcing u and the propagation A ? (·), with persistence preventing any loss.
This is the order-theoretic analogue of reaching equilibrium by repeatedly applying an expanding
operator until no genuinely new support can be added.                                                

Remark 580L (WhyL    the distributivity step is the hinge). The subtlety (such as it is) lies in justifying
that A ? ( t st ) =    t (A ? st ). This is exactly where the quantale axioms matter: ⊗ distributes
over arbitrary joins, so the propagation operator commutes with the limit-by-join. Without this
property, theLclosure and fixed-point story would lose its clean algebraic form. Concretely, writing
(A ? s)(p) = q∈P A(p, q) ⊗ s(q) (the usual quantale-enriched matrix–vector product), we compute
      M               M             M        MM                MM                M
(A?       st )(p) =         A(p, q)⊗   st (q) =   A(p, q)⊗st (q) =   A(p, q)⊗st (q) =  (A?st )(p),
      t               q∈P               t                 q∈P     t                     t    q∈P           t



                                                                 260
where the interchange of joins is justified by completeness and the distributivity of ⊗ over arbitrary
joins. Thus, ? is Scott-continuous with respect to the order structure induced by ⊕, and the fixed-
point argument is a direct application of that continuity.

Remark 581 (Least fixed point and “driven closure”). The equality s∞ = u ⊕ (A ? s∞ ) exhibits
s∞ as a fixed point of the monotone map

                                          G(s) := u ⊕ (A ? s).

Because the actual update uses F (s) = s ⊕ G(s), iteration from any s0 produces a post-fixed chain
st ≤ st+1 that approaches the least fixed point above s0 in the order. In particular, if one starts
from the empty state s0 = 0, then s∞ is the least solution of s = G(s), i.e., the smallest stable
support pattern compatible with both the constant drive u and the propagation web A. This is the
sense in which the attractor is a “closure”: it is the minimal closed (stable) element containing the
forced content.

12.6    A worked micro-example reaching self-weaving and morphic resonance
We now give a small numerical instance (compatible with the toy model style in Section 5) that
shows:

• morphic resonance creating a paraconsistent “both-sides” state; and

• internal reinforcement weaving a larger support pattern from that seed.

The example is deliberately minimal (two contexts and two patterns) so that the mechanisms can
be read off from the update equations themselves: the “morphic” step is an external injection of
evidence into a target context, while the “self-weaving” step is an internal propagation of evidence
along a small directed web of pattern-to-pattern reinforcement links.

Example 12 (Morphic resonance seeds a self-weaving two-cycle). Work in the p-bit quantale
V = [0, 1]2 with ⊕ as componentwise max and ⊗ as componentwise multiplication (Section 3.4).
Here a value (x+ , x− ) ∈ [0, 1]2 is read as a pair of evidential degrees: x+ measures positive support
and x− measures negative support. The key choice is that ⊕ = max accumulates evidence (it never
retracts prior evidence in either coordinate), while ⊗ gates or attenuates evidence multiplicatively
(so a weak coupling or weak premise yields a weak contribution). This combination is what makes
it easy to exhibit paraconsistent states: the negative coordinate can remain high even as the positive
coordinate is increased by new inputs.
    Consider two contexts (locations) C1 and C2 that share a small pattern class P = {p, q}. In-
terpret p as a “seed” pattern and q as a downstream pattern that can participate in a reinforcing
loop with p inside C2 . The intended reading is that C1 already “knows” (or has stabilized) a habit
supporting p, while C2 has not stabilized it and may even have reasons to reject it; nevertheless, C2
can be nudged by a morphic coupling that carries only partial and possibly one-sided influence.

State in C1 (source).      Assume C1 strongly supports p:

                             s(1) (p) = (0.9, 0.1),         s(1) (q) = (0.1, 0.1).

Thus, in the source context C1 , p has high positive evidence and only a small amount of negative
evidence, while q is essentially neutral/weak in both directions. One can think of this as p being an
established habit in C1 and q not yet being a meaningful downstream consequence there.

                                                      261
Initial state in C2 (target).        Assume C2 initially leans against p:
                               (2)                           (2)
                              s0 (p) = (0.2, 0.7),          s0 (q) = (0.1, 0.1).

So before any cross-context influence, C2 has relatively low positive support for p but relatively
strong negative evidence against it. This is the setup in which a purely monotone, non-retractive
update rule is most visibly paraconsistent: later increases in the positive coordinate for p need not
(and in this model, will not) remove or “explain away” the pre-existing negative coordinate.

Morphic coupling C1 → C2 .           Let the morphic field strength be K = (0.6, 0.2), and apply a direct
same-pattern coupling to p:
                                      (2)       (2)
                                     s1 (p) := s0 (p) ⊕ (K ⊗ s(1) (p)).
This update should be read as: the new state of p in the target is obtained by taking the old state and
then adding (via ⊕) a coupled contribution obtained by attenuating the source evidence by K (via
⊗). Because ⊗ is componentwise multiplication, K plays the role of a pair of channel strengths: it
transmits positive evidence with weight 0.6 and negative evidence with weight 0.2. Compute

                           K ⊗ s(1) (p) = (0.6 · 0.9, 0.2 · 0.1) = (0.54, 0.02),

so
                             (2)
                            s1 (p) = (0.2, 0.7) ⊕ (0.54, 0.02) = (0.54, 0.7).
Thus C2 receives positive support for p without erasing its negative support: it enters a paracon-
sistent “both positive and negative” regime. Concretely, after coupling we have simultaneously (i)
relatively strong positive evidence for p (raised from 0.2 to 0.54) and (ii) the original strong nega-
tive evidence against p unchanged at 0.7. The point is not that this is “inconsistent” in a classical
sense, but that the state now encodes a live tension: p is pushed forward as a candidate habit while
remaining counter-supported. In a classical single-score model, one would typically be forced to col-
lapse this to a single compromise value; in the p-bit model the two-sidedness is explicit and stable
under ⊕.

Internal reinforcement in C2 .          Now define an internal reinforcement relation in C2 by

                            A2 (p, q) = (0.9, 0.1),         A2 (q, p) = (0.8, 0.2),

and take all other pairs to have value (0, 0). These two nonzero entries specify a tiny directed web:
p pushes evidence toward q, and q pushes evidence back toward p, forming a two-cycle. The values
also allow the web to transmit both positive and negative evidence (albeit with different strengths),
so that downstream patterns can inherit not only support but also potential counter-support. In
particular, A2 (p, q) = (0.9, 0.1) says that if p is present, it tends to generate q with a strong positive
channel and a weak negative channel; A2 (q, p) = (0.8, 0.2) similarly gives a feedback link.
    Update q once by
                                   (2)       (2)                     (2)
                                 s1 (q) := s0 (q) ⊕ (A2 (p, q) ⊗ s1 (p)).
This is the local “weaving” step: the newly morphically-amplified state of p in C2 is used as an input
                                                                (2)
that propagates along the internal edge p → q. Because s1 (p) already contains a paraconsistent
tension, the propagated contribution can, in principle, carry forward both aspects of that tension.
Compute
                                    (2)
                       A2 (p, q) ⊗ s1 (p) = (0.9 · 0.54, 0.1 · 0.7) = (0.486, 0.07),

                                                      262
hence
                           (2)
                          s1 (q) = (0.1, 0.1) ⊕ (0.486, 0.07) = (0.486, 0.1).
Here the positive coordinate of q jumps substantially (from 0.1 to 0.486), while the negative coor-
dinate of q does not increase because the pre-existing negative evidence 0.1 dominates the newly
imported 0.07 under max. This illustrates a general feature of ⊕ = max: once a coordinate is
already at some level, additional weaker contributions in that coordinate do not change it, whereas
stronger contributions do. In other words, the web transmits new evidence when it exceeds what is
already locally present.
    Finally, propagate back from q to p (one step of self-weaving closure):
                                  (2)       (2)                  (2)
                                 s2 (p) := s1 (p) ⊕ (A2 (q, p) ⊗ s1 (q)).

This feedback step is the smallest nontrivial instance of “closure”: evidence that was triggered by
p and flowed to q is now allowed to flow back and potentially further reinforce p. In larger webs,
iterating such steps (or taking a least fixed point) is what builds up an extended habit-supporting
substructure from a small initiating seed. Compute
                                   (2)
                    A2 (q, p) ⊗ s1 (q) = (0.8 · 0.486, 0.2 · 0.1) = (0.3888, 0.02),

so
                          (2)
                         s2 (p) = (0.54, 0.7) ⊕ (0.3888, 0.02) = (0.54, 0.7).
In this specific numeric instance, the back-propagation does not further increase p because p is
already saturated in positive evidence and remains high in negative evidence; but it does demonstrate
the closure mechanism and shows how a morphically seeded p produces downstream q within C2 .
Said differently: the loop p → q → p is present and active, but the idempotent nature of ⊕ = max
means that once the dominant positive and negative coordinates for p have been reached (here,
positive 0.54 and negative 0.7), additional weaker returns do not alter the state. This is a feature
rather than a bug: it models a kind of “stability after saturation,” whereby a context can become
locked into a conflicted yet persistent stance.

Hyperseed interpretation. Relative to scalarization πpos , q in C2 has increased from 0.1 to
0.486 after the morphic seeding of p, which is a direct instance of “habit-taking at a distance”
(morphic resonance) followed by local habit closure on the internal web. The scalarization πpos
is used here only to make the growth easy to read numerically; the underlying state remains two-
dimensional, and in other scenarios one might equally track πneg or a combined measure. Because
negative evidence for p persisted (it stayed at 0.7), the same example also illustrates how morphic
resonance can create ambivalent or conflicted habit structures without logical explosion. In partic-
ular, the model permits the following qualitative narrative: a remote context can make a pattern
feel “compelling” (increasing positive evidence) while local countervailing constraints, memories,
or inhibitions remain in place (maintaining negative evidence). The internal web then turns this
unstable co-presence into additional structured consequences (here, support for q), which is the
minimal sense in which a seed becomes a weave.

Remark 582 (What the example is meant to teach). The arithmetic is not the point; the point is
the qualitative possibility. A coupling term can inject new positive evidence into a context without
removing existing negative evidence, creating a stable paraconsistent tension. Then, internal rein-
forcement can transmit that tension downstream, producing new supported patterns (here q) as a
consequence of the web structure. This is precisely the sense in which morphic resonance can be

                                                   263