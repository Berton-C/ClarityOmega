# 8 Effort, resistance, and simplicity

Remark 230 (Alternative tensors and modeling choices). The use of componentwise multiplica-
tion is a clean default because it is monotone and matches the usual “independent conjunction”
intuition for graded evidence. However, nothing essential forces this particular t-norm: depending
on the application, one might replace multiplication by min (for a bottleneck interpretation), by
the Lukasiewicz t-norm (for a bounded-sum interpretation), or by a learned monotone aggregator,
provided it remains compatible with the chosen order on V . The present subsection only needs
that V is a quantale so that such aggregations compose associatively and distribute over suprema,
enabling systematic propagation of temporal evidence in networks rather than ad hoc case-by-case
combination.

Remark 231 (Why keep a crisp proto-time at all?). A useful stance is: the world (or an internal
simulation) may realize a crisp partial order (T, <), while a bounded observer maintains only B. Al-
ternatively, one can work entirely with B and treat “proto-time” as an emergent crisp skeleton (e.g.
the set of pairs whose B + exceeds a threshold) when needed. This split between an (ideal) underly-
ing order and a (bounded) evidential surrogate is also a way to separate ontological questions (what
actually happened) from epistemic and computational questions (what can be inferred, stored, and
composed under constraints), which is the main methodological role played here by paraconsistent
grading.

Remark 232 (A practical reading: skeletonization by threshold). In computation, one often picks
a threshold θ and defines a derived crisp relation t1 <θ t2 iff B + (t1 , t2 ) ≥ θ (or by a net score).
This is not merely a convenience: it is an explicit model of the act of “making time definite”
by expending effort to force a decision, a theme that reappears when simplicity and weakness are
defined as observer-relative resource tradeoffs [2, 3]. One may also impose auxiliary tie-breaking
rules at the skeletonization stage (for instance, requiring simultaneously that B − (t1 , t2 ) ≤ ε for
some small ε) to avoid declaring an edge “present” precisely when the system is signaling strong
internal disagreement.

Remark 233 (From evidence to derived temporal structures). Once a crisp skeleton <θ is ex-
tracted, standard constructions become available: one can take its transitive reduction (to obtain
a Hasse-like diagram), compute its strongly connected components (to diagnose cycles created by
thresholding), or topologically sort it when it happens to be acyclic. Conversely, one can remain in
the enriched setting and compute a graded transitive closure by taking suprema over all intermediary
chains, in direct analogy with path problems in weighted graphs, but with weights in V and compo-
sition given by ⊗. The purpose of these remarks is not to fix a single pipeline, but to make explicit
that B is meant to be operational: it is a data structure on which one can run order-theoretic and
graph-theoretic procedures, either before or after discretization, depending on the resource budget
and the desired degree of commitment.

7.4   Linear time axes as serializations and quotients
A linear time axis is a special case of proto-time: a total (linear) order. Hyperseed also suggests
a specific quotienting move: group together events with the same “before-set” and “after-set”. In
the present section it is helpful to keep two distinct operations conceptually separate: serialization
(choosing a linear order that respects a given proto-time) and coarse-graining (identifying events
that the proto-time already fails to distinguish). The quotienting move is of the second kind: it
does not “decide” any new comparisons, but only collapses redundancies in the order-theoretic
description of temporal location.



                                                 129
Definition 59 (Linear time axis). A linear time axis is a proto-time (L, ≺) where ≺ is a strict
total order: for all distinct `1 , `2 ∈ L, either `1 ≺ `2 or `2 ≺ `1 . Equivalently, ≺ is irreflexive
and transitive, and it satisfies totality (comparability) on distinct elements; in many texts this is
packaged as a trichotomy principle for ≺ on L.

Remark 234 (Intuition and examples). A strict total order is the familiar “single-file” time of
classical narratives and many physics models: every two distinct times are comparable. For exam-
ple, (Z, <) is a linear time axis; so is any finite list with its left-to-right order. Linear axes are
computationally convenient because they allow iteration “from past to future” without branching
cases. But they are also epistemically assertive: they force comparability even where proto-time
may honestly have none (e.g. concurrent events). The later remark on information loss makes this
precise. One may also distinguish discrete linear axes (like Z) from dense ones (like (Q, <)): both
are linear time axes, but they support different intuitions about “next” moments and granularity.
The present development does not assume discreteness; what matters is total comparability.

Definition 60 (Past/future sets and quotient-by-indistinguishability). Let (T, <) be a proto-time.
Define for each t ∈ T :

                    Past(t) := {u ∈ T : u < t},       Future(t) := {u ∈ T : t < u}.

Define an equivalence relation ∼ on T by

                  t ∼ t0   ⇐⇒      Past(t) = Past(t0 ) and Future(t) = Future(t0 ).

Let [t] denote the equivalence class of t, and let T /∼ be the set of classes. Define a relation < on
T /∼ by
                [t] < [t0 ] ⇐⇒ t < t0 for some (equivalently any) representatives.
In order-theoretic language, Past(t) is the strict down-set of t and Future(t) is the strict up-set of
t. The pair (Past(t), Future(t)) can therefore be read as a complete “order signature” of how t sits
inside (T, <), ignoring any additional labels on events.

Remark 235 (Intuition: quotienting as “time slicing”). The pair (Past(t), Future(t)) describes the
“causal address” of t inside the partial order: what lies strictly before it and what lies strictly after
it. Two elements with the same past and future are indistinguishable with respect to the order-
theoretic information available; quotienting identifies them. In temporal terms, this implements a
rigorous version of “simultaneous at the current grain”: if the order cannot distinguish t and t0 , the
quotient refuses to pretend otherwise.
    A simple example is a proto-time with two incomparable events x and y occurring after an
initial event s and before a final event e. Then x and y have the same past {s} and the same future
{e}, hence x ∼ y and they collapse to a single slice. This is useful as a canonical compression
of proto-time prior to attempting linearization. It is worth noting that ∼ is generally finer than
“incomparability”: two incomparable events need not be equivalent, because they may have different
sets of predecessors or successors. Thus the quotient is not merely “turn all antichains into points,”
but rather “merge only those nodes whose entire comparative context agrees.”

Lemma 1 (The quotient order is well-defined and strict). The relation < on T /∼ is well-defined
and makes (T /∼, <) a strict partial order.

Remark 236 (What the lemma asserts, in plain language). The definition of [t] < [t0 ] is only
meaningful if it does not depend on which representatives t ∈ [t] and t0 ∈ [t0 ] we pick. The lemma

                                                  130
says exactly this: the quotient construction does not introduce ambiguity, and it preserves the
essential “no cycles” and “compositional precedence” properties of a strict order. This result is
conceptually important because it licenses the quotient as an information-preserving coarse-graining
of time: we are not smuggling in extra structure, merely collapsing what the order already cannot
tell apart. In particular, after quotienting, distinct classes are automatically order-distinguishable:
if [t] 6= [t0 ], then either their past sets differ or their future sets differ (by definition of ∼), so the
quotient has removed precisely the “duplicate addresses” and nothing more.

Proof. Well-definedness: suppose t ∼ s and t0 ∼ s0 with t < t0 . If s 6< s0 , then either (i) s0 = s
(impossible since t < t0 and t ∼ s would force incompatible past/future sets), (ii) s0 < s, which
together with t < t0 and the equalities of past/future sets implies a contradiction with transitiv-
ity/irreflexivity in (T, <), or (iii) s and s0 incomparable, which again contradicts the equality of
past/future sets across the ∼-classes once one representative is comparable. Strictness: irreflexivity
and transitivity descend to the quotient because any cycle in the quotient would lift to a cycle in
T . A more explicit way to see the “equivalently any representatives” clause is as follows. Assume
t < t0 and s ∼ t, s0 ∼ t0 . Then t ∈ Past(t0 ), hence t ∈ Past(s0 ) because Past(t0 ) = Past(s0 ). Since
Past(t) = Past(s) and t < t0 , we also have that every predecessor of t is a predecessor of s, and
conversely; in particular, the statement “t is before s0 ” transfers to “s is before s0 ” by comparing
down-sets at s0 and using transitivity in (T, <) to rule out the alternative possibilities s0 = s and
s0 < s. Thus s < s0 . This establishes that if one pair of representatives witnesses [t] < [t0 ], then
all pairs do. For strictness, irreflexivity on classes follows because [t] < [t] would require some
representative t < t, impossible. Transitivity follows because if [a] < [b] and [b] < [c], pick repre-
sentatives a < b and b0 < c with b0 ∼ b; by well-definedness one may replace b0 with b and obtain
a < b < c, hence a < c and therefore [a] < [c].

Remark 237 (Proof sketch and key ideas). The strategy is to show that ∼-equivalent elements
have exactly the same comparability profile. If t ∼ s, then every element that is before t is before s,
and every element after t is after s. Hence, if t is comparable to t0 , then s must be comparable to
any s0 ∼ t0 in the same direction; otherwise the past/future sets would differ. Once well-definedness
is secured, irreflexivity and transitivity are inherited because any violation in the quotient would
correspond to a directed cycle among representatives in T , which cannot exist in a strict partial
order.
    Visually, one may imagine the Hasse diagram of (T, <): the quotient merges nodes that have
identical “upward” and “downward” reachability sets. Such a merge cannot create a new directed
cycle, because cycles are already forbidden in the original graph. Another way to phrase the same
idea is that ∼ identifies vertices with identical strict principal ideals and filters; this is a standard
“separation” step in order theory that removes redundant copies of the same abstract position in
the poset.

Remark 238 (Why this quotient matters). The quotient T /∼ collapses “simultaneity at the ob-
server’s grain”: events with the same causal/narrative placement become a single “time-slice”. Even
after quotienting, the resulting order need not be total; concurrency remains possible. What changes
is that concurrency is no longer obscured by multiple indistinguishable nodes: the remaining incom-
parabilities in T /∼ represent genuine branching (or genuine lack of information) that cannot be
removed without making an additional modeling choice, such as selecting a linear extension.

Theorem 5 (Finite proto-times admit linear extensions). If (T, <) is a finite proto-time, then
there exists a strict total order ≺ on T such that t1 < t2 implies t1 ≺ t2 . Such a ≺ is called a linear
extension (or topological sort) of (T, <).


                                                    131
   A linear extension can be viewed as a systematic “tie-breaking” of incomparabilities: whenever
the proto-time does not constrain the order of two events, the extension chooses one of the two
possible orientations while keeping all required precedence relations intact. For finite T , such an
extension may be constructed algorithmically by repeatedly selecting a <-minimal element (an
event with no strict predecessors), placing it next on the linear axis, and removing it; strictness
ensures no cycles, so this process terminates. The existence of multiple linear extensions is typical
and is precisely one formal measure of how much concurrency or underdetermination a proto-time
contains.

Remark 239 (Meaning and importance). This theorem says that for a finite proto-time we can
always choose a “story order” that respects all the precedence constraints, even if the underlying
structure is branching or concurrent. In practice, this is what allows one to render a partial order
as a sequence for purposes of simulation, explanation, logging, or training a model that expects
sequential input. The result is not that linear time is fundamental, but that linear time is always
available as a representation for finite structures.
    A useful way to read this is: whenever the only temporal facts you insist on are of the form “t1
must occur before t2 ,” you can always embed those facts into a single list, provided the system is finite
and has no cycles. This is the mathematical justification behind routine engineering constructions
such as topological sorting of a dependency graph, or choosing an execution order for independent
tasks that still respects required prerequisites.
    This connects directly to the earlier warning that linearization loses information: the theorem
guarantees existence of a serialization, while the later remark clarifies that such a serialization
is typically many-to-one and hence not invertible. In other words, the existence result is about
compatibility (there is at least one linear narrative that does not contradict the proto-time), whereas
the information-loss warning is about identifiability (many different proto-times can collapse to the
same linear narrative once concurrency is forced into an order).

Proof. Induct on |T |. For |T | = 0, 1 the claim is trivial. Assume the claim holds for all smaller
finite sets. Because < is a strict partial order on a finite set, there exists a minimal element m ∈ T
(i.e. no u ∈ T satisfies u < m). Remove m to obtain T 0 := T \ {m}, and restrict < to T 0 . By
induction, T 0 admits a linear extension ≺0 . Define ≺ on T by placing m first and then following ≺0
on T 0 . Minimality of m ensures that no constraint u < m is violated, and all constraints within T 0
are respected by construction.
     For clarity on the existence of m: if every element had a predecessor, we could build a descending
chain t0 > t1 > t2 > · · · by repeatedly choosing a predecessor. In a finite set such a process must
eventually repeat an element, producing a cycle, which contradicts the irreflexivity/transitivity of
a strict partial order. Hence at least one element has no predecessor and is minimal. The same
argument also highlights why finiteness is essential for this simple induction: in infinite posets a
minimal element need not exist, so one cannot always “start” a linear narrative without adding
extra choice principles or additional structure.

Remark 240 (Proof sketch, and a visual intuition). The proof is the standard “peel off a minimal
element” argument: in any finite acyclic directed graph, there is at least one node with no incoming
edges. Place such a node first; then repeat on the remaining graph. The inductive step works because
removing a minimal element cannot destroy the strict-order property on what remains, and placing
it first cannot violate any constraint since nothing was required to precede it.
     Geometrically, imagine repeatedly shaving off the “earliest” layer of events in the Hasse diagram.
A linear extension is just the record of this shaving process. Different choices of minimal element
at each step correspond to different linear narratives compatible with the same proto-time.

                                                   132
    From an algorithmic perspective, this is exactly the idea behind a topological sort: at each step
one selects an available event (one with no unmet prerequisites), outputs it, and deletes it from the
dependency graph. The “visual intuition” is therefore not merely metaphorical; it directly encodes
a constructive procedure for producing a serialization, and it makes explicit where nondeterminism
enters (namely, whenever there is more than one currently-minimal event).

Remark 241 (Information loss under linearization). A linear extension preserves all constraints
t1 < t2 but destroys explicit incomparability: if t1 and t2 were incomparable in <, the extension still
forces either t1 ≺ t2 or t2 ≺ t1 . Hence linearization is generally a many-to-one representation of
proto-time.
    Equivalently, the linear order ≺ adds extra comparabilities that were not entailed by <. These
additional pairwise decisions are exactly what a serialization must supply in order to become a total
order, but they should be read as choices of presentation rather than as new facts about precedence
in the original proto-time. In applications, this is why one should treat the resulting sequence as an
annotated view of the underlying partial order, not as a faithful encoding of all its structure.

Remark 242 (Why “information loss” is philosophically substantive). The point is not merely
technical. When a system commits to a linear axis, it is choosing one possible way of resolving
concurrency and ambiguity; this choice can feed back into prediction, responsibility assignment, and
causal explanation. Hyperseed treats such commitments as aspects of cognitive effort and design,
not as inevitable reflections of reality [5].
    In particular, once incomparable events are forced into an order, downstream reasoning may
begin to treat the imposed order as if it were evidentially supported (e.g. inferring causal direction
from narrative order, or attributing agency based on who “acted first”). The philosophical weight
comes from the fact that such inferences are not just errors in bookkeeping; they can systematically
bias models of agency, credit, blame, or counterfactual dependence whenever concurrency is a real
feature of the underlying situation.

Remark 243 (Serialization as a quotient viewpoint). It is often useful to describe the many-to-one
aspect more structurally. Fixing a partial order (T, <), each linear extension ≺ can be seen as a
choice of totalization: it retains all required relations but adds enough additional comparisons to
make every pair comparable. Conversely, if one starts from a total order ≺ on T and “forgets” which
comparisons were merely chosen to resolve incomparability, one recovers only a coarser object—
some partial order compatible with ≺—and many distinct partial orders may be compatible with the
same ≺.
    From this perspective, passing from proto-time to a linear time axis behaves like quotienting by
an equivalence relation that identifies structures that differ only in how they arrange events that
were originally concurrent. The theorem guarantees that at least one representative exists on the
linear side for every finite proto-time, while the information-loss remark explains why the projection
to that quotient is not injective.

7.5   Becoming as boundary non-duality
Hyperseed defines becoming as a relation between temporally adjacent entities whose boundary is
“non-dual”: it is not crisply determined whether the two are distinct or identical near the transition.
   To model this, we assume:

• a proto-time (T, <),

• a set E of entities (or entity-representations),

                                                 133
• and a p-bit-valued distinction (or equivalence) relation whose value may vary by time.
Remark 244 (Proto-time versus physical time). The order (T, <) is intentionally weak: it provides
temporal precedence without committing to a metric, topology, or even continuity. This allows
the same formalism to cover discrete update steps (e.g. iterations of a learning algorithm), event
sequences (e.g. observations in an experiment), or continuous physical time as a special case. When
additional structure exists (e.g. a topology or a metric), it can be used to make the notion of
“neighborhood” in Definition 63 more explicit, but the core idea of becoming does not require it.
Definition 61 (Time-indexed distinction relation). Let E be a set of entities and T a proto-time
carrier. A time-indexed distinction relation is a map

                                        Dist : T × E × E → V,

where Dist(t; x, y) = (d+ , d− ) records evidence at time t that x and y are distinct (positive) and
evidence that they are not distinct (negative).
Remark 245 (Notation and intended reading). The notation Dist(t; x, y) is a three-argument
evaluation: first pick a time t ∈ T , then two entities x, y ∈ E, and obtain a p-bit value in V . The
first coordinate d+ supports the proposition “x and y are distinct at t,” and the second coordinate d−
supports its opposition. This is an instance of the general Hyperseed notion Distinction (Hyperseed-
Concept 98) made time-dependent, so that identity and difference can vary across a transition.
Remark 246 (Optional structural constraints on Dist). The definition does not require Dist(t; x, y) =
Dist(t; y, x), nor any form of reflexivity such as Dist(t; x, x) being maximally non-distinct. This is
deliberate: in some applications the distinction judgment is viewpoint-dependent (e.g. an asym-
metric classifier, or a directed comparability relation where x is treated as a refinement of y but
not conversely). When symmetry and reflexivity are appropriate, they can be imposed as modeling
assumptions, for example:

                        Dist(t; x, y) = Dist(t; y, x),    Dist(t; x, x) ≈ (0, 1).

Likewise, some domains may benefit from a weak “triangle-type” constraint (distinctions compose),
but becoming as boundary non-duality does not presuppose such coherence.
Remark 247 (Interpreting the value space V ). The comparison Dist(t; x, y) ≥ (θ, θ) presumes a
coordinatewise preorder on V (e.g. (a+ , a− ) ≥ (b+ , b− ) iff a+ ≥ b+ and a− ≥ b− ). Intuitively, larger
d+ means more support for “distinct,” while larger d− means more support for “not distinct.” In this
sense, non-duality is not the absence of information, but the presence of competing information. If
V additionally supports operations such as negation, conjunction, or normalization (as many p-bit-
style constructions do), those can later be used to define derived notions like “net distinctness” or
confidence-weighted salience, but they are not required for the basic definitions here.
Remark 248 (Intuition and examples). If E contains successive snapshots of a physical object,
Dist(t; x, y) can be read as “how much the observer at time t treats the snapshot x as different from
snapshot y.” In cognition, x and y might be two concepts or two internal states; during learning,
a system may oscillate between treating them as the same category and as different ones, yielding
paraconsistent values.
    The usefulness of time-indexing is that it avoids baking identity into the entities themselves.
Instead of asking “are x and y the same?”, we ask “under what temporal and contextual conditions
does the system treat them as distinct?” This is a formal handle on the otherwise slippery boundary
language used in becoming.

                                                   134
Remark 249 (Context dependence and “who” is doing the distinguishing). In practice, Dist often
aggregates multiple sources: sensory measurements, internal inference, linguistic labels, and social
or institutional criteria for sameness. Time-indexing allows these sources to shift in influence: the
same pair (x, y) can become more or less distinct as attention changes, as measurement resolution
improves, or as the governing equivalence standard is revised. Thus, even when the underlying
world-state changes smoothly, the distinction relation may change non-monotonically, which is one
of the main reasons a paraconsistent representation is useful in boundary regimes.

Definition 62 (Non-dual variety at time t). We say entities x, y ∈ E display non-dual variety at
time t if
                Dist(t; x, y) is strongly paraconsistent, e.g. Dist(t; x, y) ≥ (θ, θ)
for a chosen threshold θ ∈ (0, 1]. Intuitively: there is simultaneously strong evidence for “distinct”
and strong evidence for “not distinct”.

Remark 250 (Alternative strong-paraconsistency criteria). The coordinatewise threshold condition
is a simple sufficient test. Depending on how V is constructed, one might instead use a scalarization
such as min(d+ , d− ) ≥ θ, or require that both coordinates be high relative to total support (e.g.
d+ /(d+ + d− ) ≈ 1/2 with large d+ + d− ), distinguishing non-duality from mere uncertainty. The
present definition keeps the criterion explicit and easily checked, while leaving room for domain-
specific refinements.

Remark 251 (Intuition: a boundary where both stories are true). Non-dual variety is the formal
way of saying: at the boundary, the system has reasons to keep the two relata apart and reasons to
identify them, and neither reason is negligible. A classic illustrative situation is a gradual morph: as
a shape continuously changes from a circle to a square, there can be a region where classification as
“circle” and as “not circle” both have strong support. Another is the Ship of Theseus: near certain
thresholds, identity can be supported by continuity of function while non-identity is supported by
replacement of parts.
    The threshold θ is a modeling choice: higher θ demands stronger simultaneous support. This
definition instantiates the Hyperseed notion Non-Dual Variety (Hyperseed-Concept 120), and makes
explicit why a paraconsistent truth space is convenient: it lets us represent such boundary states
without collapsing into triviality.

Remark 252 (Non-dual variety versus indeterminacy). It is useful to separate conflict from lack
of evidence. A boundary is “non-dual” in the intended sense when there is substantial support
on both sides; this differs from a case where both d+ and d− are small (the system simply has
not formed a judgment). In applications, this difference often corresponds to whether the system is
actively maintaining competing models or interpretations (non-duality) versus being under-informed
(ignorance).

Definition 63 (Becoming along a proto-time). Fix a proto-time (T, <) and a time-indexed dis-
tinction relation Dist. We say x ∈ E becomes y ∈ E (along (T, <)) if there exist t1 < t2 and an
interval (or neighborhood) U ⊆ T with t1 ≤ u ≤ t2 for u ∈ U such that:

1. (Temporal succession) x is salient/present up to (near) t1 and y is salient/present from (near)
   t2 onward (the salience notion can be instantiated later via pattern intensity or attention),

2. (Boundary non-duality) for all u ∈ U near the transition, x and y display non-dual variety at
   u,


                                                  135
3. (Outside the boundary) away from U , x and y are (comparatively) more distinguishable (e.g.
   Dist(t; x, y) is not strongly paraconsistent).
Remark 253 (Making “interval” and “near” precise). If T is equipped only with an order, “in-
terval” can be read in the order-theoretic sense (e.g. a convex subset) and “near” can be treated
informally as “close to the transition region in the ordering.” If T has a topology or metric, one can
instead take U to be an open neighborhood of a boundary time t∗ , or a small window [t∗ − ε, t∗ + ε],
and interpret clause (2) as holding throughout that window. The definition is written to accom-
modate both discrete and continuous settings: in discrete time, U might be a short run of indices
where judgments flip or overlap; in continuous time, it can represent a genuine boundary band.
Remark 254 (Salience as a needed companion notion). Clause (1) separates what exists in the
representational universe from what is currently active for the system. Without salience, x and y
could both be permanently present in E (as representations) while never participating in a transition.
Later formalizations can operationalize salience via attention weights, activation levels, pattern
intensities, or selection functions; the present definition only requires that the model be able to say
“x is what we are tracking before” and “y is what we are tracking after.”
Remark 255 (Multiple boundaries and staged becoming). The definition allows U to be any
neighborhood capturing the transition; in many realistic cases, there may be several disjoint or par-
tially overlapping boundary regions (e.g. repeated back-and-forth reclassifications during learning).
One can model such cases either by taking U to include the full transition band, or by treating
becoming as occurring in stages x → z → y with successive boundary intervals. This flexibility
matters in paraconsistent regimes, where the path of distinctions can be non-monotone even when
the underlying process is directed.
Remark 256 (Intuition and why this definition is structured as it is). The definition isolates
three ingredients that are often conflated in informal talk about change: (i) there is a before/after
placement (t1 < t2 ), (ii) there is a boundary region where identity is unsettled (paraconsistent non-
duality), and (iii) outside that region the system regains the ability to treat the two as distinct. The
third clause is crucial: without it, one might confuse becoming with permanent ambiguity or with
simple synonymy.
    A simple example is phase change: “water becomes ice.” Around the melting/freezing point,
the system may simultaneously recognize crystalline structure (supporting distinction) and fluidity
(supporting non-distinction with the earlier state), depending on measurement scale and noise.
Another example is conceptual learning: a child may treat whales as fish, then as mammals; during
the transition there can be a period of mixed judgments that is naturally modeled as non-dual variety.
    This definition implements the Hyperseed notion Becoming (Hyperseed-Concept 62) in a way
compatible with process ontology: becoming is not a primitive arrow glued onto time, but a pattern
of changing distinction structure along proto-time [15].
Remark 257 (Why clause (3) matters for explanatory power). Clause (3) ensures that the bound-
ary region functions as a localized site of tension rather than a global feature of the pair (x, y).
In empirical terms, it supports counterfactual diagnostics: if we sample times well before and well
after the transition, the model should usually predict that the system can again make a stable dis-
tinction (or stable identification) according to its standards. This makes becoming detectable from
time series of judgments: one looks for a band of strong paraconsistency bracketed by regions of
relative determinacy.
Remark 258 (Sorites-style boundaries). The third clause encodes the intended “boundary” behav-
ior: becoming is not permanent identity, but a transition region where identity/distinction is not

                                                  136
crisply settled. Paraconsistent truth values let us represent such boundaries without forcing collapse
to triviality.
    One can read this as a Sorites-friendly stance: across a chain of micro-variations, it is generally
unreasonable to demand that each step preserve a classical predicate (e.g. “same object”) while also
insisting that the endpoints differ classically. The boundary region is precisely where the theory
records that both continuist and discontinuist descriptions have non-negligible support. In particular,
the role of a p-bit value is not to “decide” the boundary but to keep track of how much the available
constraints and observations support each side of the would-be dichotomy.

Remark 259 (Aesthetic aside: boundary as a locus of form). There is an aesthetic dimension
here: boundaries are where classification fails gracefully rather than catastrophically. In the present
formalism, the boundary is not a logical defect but a region where the system explicitly represents
competing commitments. This is mathematically tractable and, arguably, phenomenologically faith-
ful (Hyperseed-Concept 53).
    More concretely: if a classification scheme is forced to return a single crisp label everywhere, then
any perturbation near the boundary produces discontinuous “label flicker,” which is both computa-
tionally brittle and experientially unlike how agents often cope with vague transitions. By contrast,
allowing the boundary to carry structure—here, two-channel support/denial that can coexist—turns
the boundary into a site where form can be articulated (e.g. by gradients of support, by competing
explanations, or by alternative decompositions of a process into events). This makes the boundary
a locus for further inference rather than an error condition.

7.6     A paraconsistent, quantale-valued event calculus
Hyperseed’s “event and process calculi” discussion can be realized cleanly by taking the standard
event calculus vocabulary and interpreting all core predicates in the p-bit quantale V . This subsec-
tion instantiates Event and Process Calculi (Hyperseed-Concept ??) in a way that is algebraically
continuous with the rest of the document.
    The guiding idea is that “temporal reasoning” is not a separate module with its own ad hoc
uncertainty mechanics; rather, it is another place where the same algebra of evidence is applied.
In particular, we want the same operations that combine perceptual cues or conceptual constraints
to also combine (i) evidence that an event occurs, (ii) evidence that it changes a fluent, and (iii)
evidence that the fluent holds over an interval.

7.6.1    Signature and intended semantics
Definition 64 (Event calculus signature (paraconsistent, quantale-valued)). Fix:

• a proto-time carrier (T, <),

• a set A of actions/events,

• a set F of fluents (time-varying propositions).

A p-bit-valued event calculus assigns:

                                      Happens : A × T → V,
                                       HoldsAt : F × T → V,
                                       Initiates : A × F × T → V,
                                    Terminates : A × F × T → V.

                                                  137
Remark 260 (Time structure and modeling latitude). The modest assumption “proto-time carrier
(T, <)” is deliberately weak: in applications one may take T to be discrete (e.g. N for step-indexed
simulation), continuous (e.g. R for physical time), partially ordered (for branching-time or concur-
rency models), or even an interval domain when the primary observations are temporally coarse.
What matters for the present subsection is that < provides enough structure to state propagation
constraints from earlier to later times. The quantale-valued semantics then handles gradedness and
inconsistency orthogonally to the choice of temporal granularity.
Remark 261 (Notation unpacking: actions, fluents, and V ). Here A is the set of event-types (or
action-tokens, depending on modeling choice), and F is the set of fluents, i.e. propositions whose
holding status may vary over time. The codomain V = [0, 1]2 means each predicate returns a two-
channel evidence value. Thus Happens(a, t) = (h+ , h− ) is evidence for/against “event a happens
at time t,” and similarly for the other predicates.
    It is important that the two channels are not required to sum to 1 (as they would in a probabilistic
simplex), nor to be complements; this is what permits “boundary” and “conflict” states such as
(0.8, 0.7), which would otherwise be disallowed. Conversely, complete ignorance may be represented
by something like (0, 0), where neither support nor denial is available.
Remark 262 (Intuition, examples, and why this signature is useful). In classical event calculus,
HoldsAt(f, t) is Boolean; here it is graded and paraconsistent. This matters precisely at boundaries:
a fluent like “the door is open” may have conflicting evidence from different sensors; an initiation
rule may be supported by a learned model but contradicted by a physics-based model. By putting
all these predicates in the same quantale-valued space, we can aggregate evidence compositionally
rather than by ad hoc priority rules.
    As a minimal example, let F = {f } and A = {a}. If Happens(a, t) is high and Initiates(a, f, t) is
high, we can infer support for HoldsAt(f, t0 ) at later times, subject to clipping/termination evidence.
This provides a concrete “time reasoning” layer compatible with Hyperseed’s broader pattern-based
cognitive architecture [19].
    A slightly richer example illustrates the boundary use-case directly. Suppose a is “push door”
and f is “door open.” A camera may support HoldsAt(f, t) while a latch sensor denies it; simul-
taneously, the dynamics model may support Initiates(a, f, t) while a safety interlock model supports
Terminates(a, f, t) (e.g. the push triggers a mechanism that closes the door). In a Boolean setting
this can force inconsistent axioms; here it yields a controlled state of tension that can be resolved
(if at all) by additional evidence, temporal propagation, or explicit bias terms.
Remark 263 (Why p-bit values here?). In realistic temporal reasoning, the boundary of when an
event happens, whether a fluent holds, and whether an action initiates/terminates a fluent are all
uncertain and can be mutually conflicting. The p-bit representation makes these conflicts explicit
and composable.
    Technically, the point is that the same algebraic operations used elsewhere in the document
(e.g. ⊗ for conjunction-like composition and ⊕ for proof/evidence accumulation) can be reused here
without special casing time. This uniformity is what makes the approach “algebraically continuous”:
temporal inference becomes another instance of quantale-enriched constraint propagation rather than
an isolated logical subsystem.

7.6.2   Monotone rule evaluation over a quantale
A convenient semantics for Horn-style rules over a quantale is: conjunction is interpreted by the
tensor ⊗, and alternative proofs are aggregated by join ⊕ (in V this is componentwise max). This
yields a monotone “proof accumulation” logic.

                                                  138
Remark 264 (Connection to standard event calculus axioms). Classical event calculus is often
presented with axiom schemata for persistence (inertia), initiation, termination, and “clipping”
(events that end a fluent’s holding). The present subsection does not repeat the full axiom inventory;
instead it isolates the evaluation principle that makes those axioms computationally well-behaved in
the quantale-valued setting. When the familiar axiom schemata are added, each becomes a Horn-
style rule (or a family of such rules) whose body combines pieces of evidence, and whose head
accumulates whatever support those bodies provide.

Definition 65 (Quantale-valued implication schema). Let P, Q1 , . . . , Qn be predicate symbols with
appropriate arities. A quantale-valued rule has the form

                                 P (~x) ⇐ Q1 (~x1 ) ∧ · · · ∧ Qn (~xn ),

and is evaluated pointwise by

                                JP (~x)K ≥ JQ1 (~x1 )K ⊗ · · · ⊗ JQn (~xn )K.

If multiple rules (or multiple instantiations) derive the same head, their contributions are joined
using ⊕.

Remark 265 (Reading the inequality direction). The use of “≥” reflects that rules provide lower
bounds on the evidence for the head: any derivation gives at least some support/denial profile
for P (~x), and additional derivations can only increase that profile via joins. This matches the
fixpoint view where one starts from minimal information and iteratively accumulates consequences
until closure. In proof-theoretic terms, the model is the least assignment that satisfies all such
inequalities.

Remark 266 (Intuition: proofs as resources that accumulate). The tensor ⊗ plays the role of
“and”: to support the head, we must support each body literal, and the combined support is the mul-
tiplicative accumulation of those supports. The join ⊕ plays the role of “or”: multiple derivations
contribute, and we keep the strongest support (componentwise maximum in the p-bit quantale). This
is the algebraic analogue of how one informally reasons with multiple pieces of evidence: a chain is
only as strong as its weakest link (multiplication attenuates), but parallel arguments compete and
the best available argument dominates (maximum selects).
    The usefulness of this schema is that it yields a monotone immediate-consequence operator,
enabling least-fixpoint semantics and iterative computation, a theme reused later when stability
properties of self-modifying systems are studied via fixpoints [10].
    In the p-bit case, the same rule simultaneously propagates positive and negative information. For
instance, if one body literal strongly denies a condition, then the negative channel can propagate
through ⊗ in a controlled way. This is exactly the mechanism that lets “boundary” regions be
stable under inference: the system can accumulate both pro and con evidence without exploding into
triviality, while still allowing later evidence to tilt the balance.

Remark 267 (Negation and non-monotonicity). Classical event calculus uses negation-as-failure
(e.g. “not clipped”) and circumscription. In the present paper we keep the algebraic core monotone
and represent negative information explicitly via the negative component of p-bit values. Non-
monotone defaults (frame assumptions) are then expressed by an additional weakness bias (Sec-
tion 8), rather than by embedding classical negation-as-failure into the core semantics.
    This separation is especially relevant for temporal reasoning because inertia is a default: in a
purely monotone setting, one does not want the mere absence of termination evidence to behave

                                                    139
like a hard fact. Instead, “persistence” can be treated as a defeasible contribution whose weight is
governed by effort/weakness tradeoffs, while explicit termination evidence contributes on the same
algebraic footing as other sources of information.

Remark 268 (Why monotonicity is a design choice). Monotonicity means: adding evidence cannot
invalidate previous inferences, it can only enrich them. This is not how human default reasoning
always behaves; however, it is how the present algebraic layer behaves so that computation and
compositional semantics remain tractable. Departures from monotonicity are pushed to explicit
bias terms and effort/weakness tradeoffs [3, 2], which makes the source of “non-monotone behavior”
inspectable.
    From an implementation perspective, monotonicity also aligns with streaming and incremental
updates: as new observations arrive, one can update Happens or HoldsAt values and rerun (or
incrementally maintain) the immediate-consequence operator without needing to retract inferences
at the algebraic level. Any retraction-like behavior is then a matter of shifting bias, discounting
stale evidence, or changing the governing rules—all of which are explicit modeling moves rather
than hidden in the semantics of negation.

7.6.3   Clipping and inertia (paraconsistent sketch)
We now give one clean paraconsistent way to express inertia. First define a derived predicate
Clipped(f ; t1 , t2 ) meaning that between t1 and t2 there is evidence that some action terminates f .

Definition 66 (Clipped (derived; paraconsistent sketch)). Define the p-bit value
                                        M
               Clipped(f ; t1 , t2 ) :=    Happens(a, u) ⊗ Terminates(a, f, u).
                                           a∈A
                                          u∈T :
                                        t1 <u<t2

When Clipped+ is high there is strong evidence that f was terminated in (t1 , t2 ). When Clipped−
is high there is strong evidence against such termination.

Remark 269 (Intuition and a simple example). This definition says: f is clipped on the interval
if there exists some event a at some intermediate time u that both happens and terminates f ; the
degree of evidence is aggregated over all such candidates by ⊕ (max). If there are multiple possible
terminating events, we keep the strongest combined evidence among them.
    For example, suppose two events might terminate a fluent, but only one is strongly supported
by sensor data; then Clipped+ will reflect the stronger candidate. Conversely, if we have explicit
evidence that no terminating events occurred (perhaps from a reliable log), this can raise Clipped−
and thereby later support inertia.

    We then express inertia as: if f holds at t1 and there is no (or weak) evidence that it was
clipped before t2 , then f holds at t2 .

Definition 67 (Inertia update operator (paraconsistent sketch)). Define an operator Φ on assign-
ments to HoldsAt by
                                                   M
        (Φ HoldsAt)(f, t2 ) := HoldsAt0 (f, t2 ) ⊕   HoldsAt(f, t1 ) ⊗ ¬Clipped(f ; t1 , t2 ),
                                                     t1 ∈T :
                                                     t1 <t2

where HoldsAt0 encodes initial conditions and ¬ is the p-bit involution ¬(v + , v − ) = (v − , v + ).


                                                   140
Remark 270 (Notation and meaning of ¬ in this setting). The involution ¬(v + , v − ) = (v − , v + )
simply swaps positive and negative evidence channels. Thus ¬Clipped(f ; t1 , t2 ) is evidence for/against
“unclipped” obtained by swapping the channels of the clipped evidence. This is not classical negation;
it is a bookkeeping operation appropriate to the p-bit evidence interpretation, and it is compatible
with the monotone proof-accumulation semantics described above.

Remark 271 (Intuition: inertia as propagation through gaps). The update says: f holds at t2
either because it is an initial fact HoldsAt0 (f, t2 ), or because there exists an earlier time t1 where
f held and the interval (t1 , t2 ) carries counter-evidence to termination. One may view this as a
kind of temporal path propagation: holding status flows forward unless clipped, and the quantale
operations determine how strongly it flows.
    This is the temporal analogue of closure constructions used elsewhere (e.g. composition/closure
of relations in the toy model section): local constraints propagate globally by repeated application of
a monotone operator until a fixpoint is reached [7].

Remark 272. Using ¬Clipped here is not “absence of evidence”; it is the explicitly represented
counter-evidence (or support for “unclipped”). This is consistent with the paraconsistent stance:
one can simultaneously carry evidence that a termination occurred and evidence that it did not, and
inertia will then yield a correspondingly paraconsistent holding status.

Theorem 6 (Existence of least fixpoint for monotone temporal inference). Assume T is finite and
all event-calculus rules are built using only ⊕, ⊗, and monotone operations on V . Then the induced
immediate-consequence operator (e.g. Φ above) is monotone on the complete lattice of assignments
(V F ×T , ≤) and hence has a least fixpoint.

Remark 273 (What the theorem says and why it matters). The theorem guarantees that the it-
erative “accumulate evidence until stable” procedure is not merely heuristic: there exists a least
stable assignment of truth values consistent with the rules. This is crucial for making the event
calculus a well-defined semantic object rather than just a collection of update equations. It also
connects temporal reasoning to the same fixpoint machinery used elsewhere in Hyperseed-style anal-
yses of stability and self-reference [10]: time inference becomes a special case of order-theoretic
stabilization.

Proof. V F ×T is a complete lattice under pointwise order. Each clause contribution is monotone
because ⊗ and ⊕ are monotone in each argument, and joins over index sets preserve monotonicity.
Therefore the overall operator is monotone. By the Knaster–Tarski theorem, a monotone operator
on a complete lattice has a least fixpoint.

Remark 274 (Proof sketch and intuition). The high-level strategy is: (i) identify the space of
all candidate interpretations as an ordered set, (ii) show the update operator never reverses or-
der (monotonicity), and then (iii) invoke the general fixpoint theorem. Pointwise order on V F ×T
means: one assignment is ≤ another if it assigns ≤-smaller p-bit values to every fluent-time pair.
Monotonicity follows because ⊗ and ⊕ are monotone operations and because taking a join (supre-
mum) over any family of monotone expressions preserves monotonicity. A visual intuition is to
imagine starting from the bottom assignment (no evidence anywhere) and repeatedly applying Φ to
“grow” the set of supported conclusions. Because the update can only add or strengthen evidence
(never retract it), the sequence ascends in the lattice and must stabilize in finitely many steps when
T is finite. The stabilized point is the least fixpoint. In more algebraic terms, this is the famil-
iar picture behind Kleene iteration for monotone operators: starting at ⊥ and iterating Φ yields
an increasing chain whose supremum is a fixpoint, and when the underlying carrier is finite (or,

                                                  141
more generally, when the lattice has finite height) the chain cannot strictly increase forever. The
least-fixpoint characterization is important conceptually because it encodes a minimality principle:
nothing is concluded unless it is forced by the update rules, and no extra evidence is introduced
beyond what is generated by repeated rule application.

7.7   Time contexts and temporal similarity
Hyperseed defines several important “event regularity” notions using the idea that each timepoint
comes with a time context (what holds then), and that nearby/similar timepoints have similar time
contexts. The key modeling move is to treat temporal structure as being (at least partly) induced
by patterns in fluent valuations: rather than assuming a fixed external metric on T , we derive a
notion of proximity from how the world is described at those times. This is especially natural when
T is a proto-time carrier (e.g. a partially ordered or otherwise non-metric structure) and when
different observers may coarse-grain or refine what distinctions matter.

Definition 68 (Time context). Fix an event calculus instance with fluent set F and proto-time
carrier T . The time context at time t ∈ T is the vector of fluent truth values

                           TimeCtx(t) := HoldsAt(f, t) f ∈F ∈ V F .
                                                            


Remark 275 (Intuition and example). TimeCtx(t) is the full “state description” of what is (para-
consistently) true at time t, as far as the chosen fluent vocabulary can express. For example, if
F = {DoorOpen, LightOn} then TimeCtx(t) is the ordered pair of p-bit values assigned to these
two propositions at time t. This concept operationalizes the idea that a timepoint is not merely
a coordinate but a bundle of conditions; it is an explicit bridge between ordering-based time and
state-based dynamics. Note that TimeCtx(t) depends on the chosen fluent set F: refining the vo-
cabulary (splitting one fluent into several more specific ones) generally increases the dimension of
V F and can make previously indistinguishable timepoints separable, while a coarser vocabulary can
collapse distinct situations into the same apparent context. In this sense, a “time context” is not
a metaphysically complete state of the world but an observer-relative description at a particular
granularity.

Definition 69 (Truth-value projection and similarity). Choose any monotone scalar projection
π : V → [0, 1]; two useful examples are
                                                                          1
                     πpos (v + , v − ) = v + ,      πnet (v + , v − ) =     1 + (v + − v − ) .
                                                                                            
                                                                          2
Define a similarity on V by

                                    simV (v, w) := 1 − |π(v) − π(w)|.

Define time-context similarity for t1 , t2 ∈ T by
                                         1 X                                      
                   simT (t1 , t2 ) :=        simV HoldsAt(f, t1 ), HoldsAt(f, t2 ) .
                                        |F|
                                             f ∈F

Remark 276 (Notation and modeling choice). The map π compresses a two-channel p-bit value
to a single scalar in [0, 1] so that we can use a simple absolute-difference similarity. πpos measures
similarity of positive support only; πnet measures a signed “net support” that discounts negative


                                                        142
evidence. Different projections correspond to different stances about how to treat contradiction:
one may focus on what is supported, or on the balance between support and opposition.
    The similarity simT (t1 , t2 ) is just the average similarity across all fluents; it is a computable
proxy for “how similar the world looks at t1 and t2 in this vocabulary.” Because simV takes values
in [0, 1], so does simT , and the endpoints have a clear reading: simT (t1 , t2 ) = 1 exactly when
π(HoldsAt(f, t1 )) = π(HoldsAt(f, t2 )) for every f ∈ F, while smaller values quantify the average
magnitude of disagreement under the chosen projection. The monotonicity requirement on π (with
respect to the lattice order on V ) ensures that strengthening evidence in V cannot perversely decrease
the projected scalar in a way that would invert comparisons; this makes similarity judgments stable
under the “adding evidence” dynamics of the underlying paraconsistent calculus.

Remark 277 (Why similarity is defined via projection rather than directly in V ). One could
define a similarity directly on V = [0, 1]2 using a 2D metric, but the projection method makes
explicit which aspect of the paraconsistent value is being compared. This is philosophically in the
spirit of Hyperseed: similarity is not an absolute given but an observer-relative construction, and
the choice of π is part of the observer model. Technically, the projection also makes it easy to swap
in alternative scalar summaries without changing the surrounding definitions: for instance, one
could use π(v + , v − ) = max(v + , 1 − v − ) to privilege “unopposed support,” or π(v + , v − ) = 1 − v − to
track absence of counterevidence. Each such choice corresponds to a different operational meaning
of “two truth values being close.”

Remark 278 (Basic properties of the induced similarities). For any fixed projection π, simV
is symmetric and satisfies simV (v, v) = 1 for all v ∈ V , hence simT (t, t) = 1 for all t ∈ T .
However, simV (and therefore simT ) is generally not transitive when turned into a crisp relation
via thresholding: it is possible to have t1 similar to t2 and t2 similar to t3 while t1 is not similar
to t3 , especially when similarity is defined by an average across fluents and disagreements are
distributed across different coordinates. This non-transitivity is not a bug in the present setting: it
reflects the familiar phenomenon that “looks similar” is typically a neighborhood notion rather than
an equivalence relation, and it supports a flexible notion of continuity that does not require global
clustering.

Definition 70 (Temporal similarity). Fix a threshold τ ∈ (0, 1]. Define

                         TemporalSimilarity(t1 , t2 ) to hold if simT (t1 , t2 ) ≥ τ.

Remark 279 (Intuition and example). TemporalSimilarity(t1 , t2 ) is a derived crisp predicate that
says: the system treats the two timepoints as “close enough” in state-space. For instance, if τ =
0.95, then only timepoints with very similar fluent valuations are considered temporally similar.
This definition is useful because it allows qualitative temporal predicates (like “continuous”) to be
stated without assuming a numeric metric on T ; similarity is derived from what holds, not from an
external clock. In particular, one can speak about “local smoothness” of a trajectory t 7→ TimeCtx(t)
by requiring that successive or causally adjacent timepoints (as given by the proto-time structure)
satisfy TemporalSimilarity, even when there is no canonical notion of successor in T .

Remark 280. Other choices are possible and sometimes preferable: e.g. using a weighted average
over fluents, or using quantale weakness (Section 8) to measure how many distinctions between
time contexts are collapsed by a given observer. The present choice is intentionally simple and
computable. A weighted average can encode domain knowledge (some fluents are more salient or
more reliably sensed) by assigning larger weights to dimensions that should dominate similarity
judgments, and it can also mitigate the effect of many irrelevant fluents washing out a small but

                                                     143
important change. Likewise, replacing the absolute-difference form with a different scalar similarity
(e.g. a kernel) can change how sharply similarity decays, which in turn affects which temporal
patterns count as regularities.

Remark 281 (Connection to weakness and observer-dependent coarse-graining). If an observer
collapses many differences between time contexts (Hyperseed-Concept 202), then many pairs (t1 , t2 )
will become temporally similar under that observer’s projection and aggregation scheme. This pro-
vides a direct route from effort/simlicity theory to the phenomenology of “time flowing smoothly”
versus “time being jagged” [3]. Concretely, weakening can be understood as reducing effective reso-
lution in V F : distinct vectors of p-bit values that would be separated by a high-effort observer may
map to nearby (or identical) projected summaries under a low-effort observer, thereby increasing
simT on average. Under this lens, temporal coarse-graining is not merely subsampling in T ; it is
a transformation of the state-description map t 7→ TimeCtx(t) that changes which variations are
treated as signal versus noise.

7.8   Persistent, continuous, increasing, decreasing
Hyperseed lists several meta-predicates about events/fluents. We implement these as constraints
on the trajectory t 7→ HoldsAt(f, t) relative to the proto-time order and the temporal similarity
relation. In this reading, these meta-predicates are not additional primitive symbols; rather, they
are properties of an interpreted event-calculus model, checkable from the induced HoldsAt relation
together with whatever auxiliary similarity/projection structure the modeler provides.

Definition 71 (Continuous fluent (relative to a proto-time)). A fluent f ∈ F is continuous (relative
to (T, <), TemporalSimilarity) if for all t1 , t2 ∈ T ,
                                                                                
            TemporalSimilarity(t1 , t2 ) → simV HoldsAt(f, t1 ), HoldsAt(f, t2 ) ≥ η

for a chosen threshold η ∈ (0, 1].

    It is often convenient to read TemporalSimilarity(t1 , t2 ) as designating a class of “small” or
“contextually close” temporal transitions, even when T is discrete or only partially organized by <.
Similarly, simV can be instantiated as a kernel, a cosine similarity on embeddings, or 1 − distV (·, ·)
for some value-space distance; the point is that continuity is asserted in the value space V rather
than in T . Note also that η acts as a tunable tolerance: taking η = 1 forces invariance of HoldsAt
on all temporally similar pairs, whereas smaller η permits controlled variation.

Remark 282 (Intuition and example). Continuity here is not about infinitesimals; it is about
stability under the chosen notion of temporal similarity. If t1 and t2 look similar in their overall
time contexts, then f should not change much between them. For example, if “temperature” is
represented as a fluent and the system regards two moments as similar in relevant conditions, then
the temperature fluent should have similar values at those moments. This captures a qualitative
sense of continuity appropriate to proto-time, where T may not carry a metric topology.
    The definition is useful because it separates “what counts as a small time change” (encoded by
TemporalSimilarity) from “what counts as a small fluent change” (encoded by simV and η). Both
are observer-relative and can be tuned.

   A useful operational consequence is that continuity can be evaluated as a family of constraints,
one per temporally-similar pair, and therefore can be implemented either as a hard logical ax-
iom or as a soft penalty in a probabilistic/optimization layer. For instance, in a weighted setting


                                                 144
one may penalize violations by a hinge loss max{0, η − simV (HoldsAt(f, t1 ), HoldsAt(f, t2 ))} when-
ever TemporalSimilarity(t1 , t2 ) holds, thereby allowing noisy observations while still encoding the
intended smoothness bias.

Definition 72 (Persistent fluent (relative to a proto-time)). A fluent f ∈ F is persistent if it
is continuous and, additionally, its truth-value varies only weakly across the entire interval be-
tween initiation and termination, i.e. there exists  ≥ 0 such that whenever t1 < t2 and f holds
“throughout” [t1 , t2 ] (as determined by the event calculus instance), then

                             |π(HoldsAt(f, t1 )) − π(HoldsAt(f, t2 ))| ≤ .

    The phrase “holds throughout” can be understood in the event-calculus sense: f is supported
on the interval because it is initiated at or before t1 , not terminated before t2 , and inertia (or
the chosen persistence axioms) propagate its holding status across intermediate times. When T is
dense or when HoldsAt is only partially observed, this “throughout” condition is best viewed as
a model-relative judgment rather than a syntactic universal quantification over all t ∈ [t1 , t2 ]; the
intended meaning is that the theory treats the interval as one of uninterrupted holding.

Remark 283 (Intuition and why persistence is stronger than continuity). Continuity constrains
local change: nearby time contexts should not flip the fluent abruptly. Persistence adds a global
bound: across any span where the fluent is considered to hold, its projected value should not drift
by more than . For example, “the light is on” may be persistent if it remains stably supported from
switch-on to switch-off, even if minor sensor noise causes small fluctuations. By contrast, a fluent
like “the music is loud” might be continuous but not persistent if it rises and falls gradually.
    This definition is useful because it lets us distinguish steady conditions from smooth evolutions.
The parameter  makes explicit how much variation is tolerated before we stop calling the fluent
persistent.

    Two limiting cases help orient the parameter choices. If  = 0 and π is chosen so that
π(HoldsAt(f, t)) is Boolean-valued, then the persistence constraint forces literal invariance of the
projected value on any “holding” span, which aligns with the classical intuition of a fluent remain-
ing true until terminated. At the other extreme, if  is large (e.g.  = 1 for π : V → [0, 1]), the
additional persistence clause becomes vacuous and persistence collapses back toward continuity;
in that regime, the distinction between “steady” and “smoothly varying” is pushed back into the
choice of η and TemporalSimilarity.

Definition 73 (Increasing/decreasing fluent). Fix a scalar projection π : V → [0, 1]. A fluent f is
increasing (relative to (T, <)) if for all t1 < t2 ,

                               π(HoldsAt(f, t1 )) ≤ π(HoldsAt(f, t2 )).

Similarly, f is decreasing if for all t1 < t2 ,

                               π(HoldsAt(f, t1 )) ≥ π(HoldsAt(f, t2 )).

   In proto-time, < need not be a complete order; it may be a partial order encoding precedence.
The above monotonicity clauses should then be read as applying to all comparable pairs t1 < t2 .
In particular, if t1 and t2 are incomparable (neither t1 < t2 nor t2 < t1 ), the definition does
not constrain π(HoldsAt(f, t1 )) versus π(HoldsAt(f, t2 )), which matches the idea that monotone
“change over time” is only meaningful along directed temporal reachability.


                                                  145
Remark 284 (Intuition and examples). Monotonicity is stated after projection to a scalar because
“increasing” is inherently a scalar notion. For example, if f represents “confidence that a goal is
achieved,” one might take π = πpos and ask that positive support does not decrease over time. If f
represents “amount of fuel remaining,” one might impose decreasingness.
    This is useful as a compact way to express directed change, and it can be combined with the earlier
event calculus machinery: one can infer monotone trends from initiation/termination patterns and
inertia, then check them against observed HoldsAt values as a consistency constraint.
    It is also useful to note the interaction between increasing and decreasing: if a fluent is both
increasing and decreasing with respect to the same π and order <, then π(HoldsAt(f, t)) must
be constant on each chain in (T, <) (i.e. on each totally ordered subset). This captures the idea
that “no upward drift” together with “no downward drift” yields stability, but only relative to the
comparabilities present in proto-time.
Remark 285 (Non-persistent events). Hyperseed notes that continuous/increasing/decreasing are
most relevant for non-persistent events. In our formalization, persistence is the strong constraint
(low total variation over a span), while continuity and monotonicity constrain only local or direc-
tional change. Thus a non-persistent fluent may be continuous yet non-constant, or increasing yet
not persistent.
    One can also mix these predicates to express common qualitative regimes. For example, “warm-
ing up” can be modeled as (i) continuous with respect to a chosen temporal similarity and (ii)
increasing with respect to a temperature projection π, without being persistent; conversely, “being
connected to WiFi” might be persistent (small ) but neither increasing nor decreasing (no directed
trend is intended, only stability when it holds).
Remark 286 (A conceptual bridge to emergence). When a fluent violates persistence but satisfies
continuity, it suggests the presence of a smooth transformation rather than a stable condition. Such
smooth transformations are often where new patterns become detectable (emergence as a change in
compressibility), foreshadowing the pattern and emergence layer in Section 9 [5].
    In particular, continuity provides a baseline expectation of “no abrupt jumps” under the sys-
tem’s own notion of temporal neighborhood, so sustained deviations from persistence can be in-
terpreted as structured drift rather than noise. This is precisely the regime in which higher-level
descriptions (e.g. a slowly varying latent factor, a staged process, or a new macro-variable) can
become more compressive than a frame-by-frame account, making the persistence/continuity dis-
tinction serve as an interface between low-level event calculus dynamics and later pattern-level
analyses.

7.9   Process view: becoming as functorial evolution (bridge to process calculi)
Event calculus is one way to reason about change; a complementary way is to treat the world (or
mind) as a process indexed by proto-time. In this second lens, “becoming” is not primarily a list
of event-occurrences but a rule that assigns, to each experienced position in an order, a structured
state together with coherent transition maps. The emphasis is on how successive situations hang
together (compositionally), rather than on how a theory entails that a fluent holds.
Definition 74 (Becoming as a time-indexed process (functorial sketch)). Let (T, <) be a proto-
time. Consider the thin category T whose objects are elements of T and with a unique morphism
t1 → t2 iff t1 < t2 . A process over T is a functor
                                            S : T → Sys

                                                 146
into a chosen category of system states Sys (e.g. sets, measurable spaces, or V -enriched structures).
In particular, the functoriality condition forces compatibility with the proto-temporal order: if t1 <
t2 < t3 , then the induced maps satisfy S(t1 → t3 ) = S(t2 → t3 ) ◦ S(t1 → t2 ), so that multi-step
becoming factors into successive becomings without ambiguity.
Remark 287 (Notation and categorical intuition). A thin category is a category with at most one
morphism between any two objects; here the existence of a morphism t1 → t2 encodes exactly the
relation t1 < t2 . A functor S assigns to each timepoint t an object S(t) (a “state”) in Sys, and
to each precedence t1 < t2 a morphism S(t1 ) → S(t2 ) (an “evolution map”). Thus, time becomes
a parameter indexing structure-preserving transformation, rather than a numerical axis labeling
states. Equivalently, one can regard T as the categorical packaging of the proto-time order and S
as a representation of that order inside Sys.
    This is a canonical formalization of Process (Hyperseed-Concept 140) and clarifies how proto-
time supports process calculi: the order supplies composable arrows, and the functor turns them
into composable state transitions. From this viewpoint, the “laws of motion” (broadly construed)
are precisely the chosen morphisms in Sys that witness admissible change; changing Sys changes
what counts as a lawlike update (deterministic function, stochastic kernel, simulation relation,
refinement map, etc.).
Remark 288. This functorial viewpoint is the categorical form of “becoming”: morphisms represent
allowed transformations along the experienced order. It also makes explicit what is often only
implicit in informal talk about time: the content is not merely that there are states at moments, but
that there are coherent translations between them that respect the proto-temporal composition. In
later sections, this will interact with pattern webs and mind-world correspondence by replacing Sys
with a category of pattern-flow structures and by admitting approximate morphisms. Concretely,
“approximate” can be implemented by moving to an enriched or metric setting in which morphisms
carry a notion of distortion (or error budget), so that becoming can be stable under coarse-graining,
attention limits, and perceptual noise.
Remark 289 (Why include both event calculus and functorial process views?). Event calculus em-
phasizes logical entailment about discrete events and fluents; the functorial view emphasizes struc-
tured evolution and compositionality. They are complementary lenses on the same phenomenon:
one can often derive an event calculus from a process model by extracting predicates from states, and
conversely one can build a process model from an event calculus by taking time contexts as states.
Keeping both views available supports later synthesis with pattern-based cognition and with the
more explicitly process-ontological themes that trace back to Peircean and Whiteheadian traditions
[14, 15]. The bridge to process calculi is particularly transparent in the functorial picture: many
calculi distinguish between (i) the space of configurations and (ii) the step relation or transition
system, and the functor packages exactly this distinction while enforcing associativity of successive
steps via categorical composition. When proto-time is taken as a partial order (rather than a to-
tal one), the same construction supports branching and concurrency: incomparable elements of T
represent independent or unordered developments, while comparable elements represent precedence
constraints, aligning the categorical skeleton with causal or dependency structure rather than with
a single global clock.


8    Effort, resistance, and simplicity
Outline
• Represent “effort” as a resource/cost structure suitable for compositional reasoning.

                                                 147
• Model resistance/submission and opening/closing as (directed) changes to a system’s distinction
  policy.

• Define observer-relative simplicity in terms of effort minimization and (dually) weakness maxi-
  mization.

• Define compositional simplicity as a least-fixed-point/dynamic-programming object over a com-
  bination system.

• Connect these notions to generalized Kolmogorov complexity and to structural (grammar-like)
  complexity.

    To reduce ambiguity, the word “effort” will be treated as a typed magnitude rather than an
informal proxy for time, energy, or difficulty. In particular, the goal is to support reasoning of the
form: (a) a task can be achieved by alternative constructions, (b) each construction incurs effort, (c)
effort accumulates along chains of sub-operations, and (d) “simplicity” is the selection of low-effort
constructions relative to a given system/observer. This subsection is therefore preparatory: it fixes
the algebraic shape of the quantity that later sections will propagate through patterns, habits, and
predictive correspondence.
    The five bullet points above should be read as a progression from local to global structure.
First we choose a representation of effort that supports addition (doing things in sequence) and
comparison/minimization (choosing among alternatives). Then we interpret certain phenomeno-
logical notions—opening/closing and resistance/submission—as structured transformations whose
costs can be measured in the same effort space. Finally, we define two notions of simplicity: one
that is observer-relative (“simple for this system”) and one that is compositional (“stable under
building wholes from parts”), and we relate both to established complexity measures.

Summary and Hyperseed concepts covered
Hyperseed treats effort as primitive and observer-relative: what is “simple” is what a particu-
lar system can do, represent, or predict with low effort (Hyperseed-Concept 100). To make this
mathematically usable, we represent effort via a cost quantale and use it to define (i) simplic-
ity as minimum representational effort (Hyperseed-Concept 169), and (ii) compositional simplicity
as a stability property under building wholes from parts (Hyperseed-Concept 82). We then for-
malize opening/closing (Hyperseed-Concepts 125, 72) as relaxing/tightening distinction policies
(Hyperseed-Concept 98) and resistance/submission (Hyperseed-Concepts 158, 183) as the effort
gradient associated with such changes.
    More concretely, a cost quantale is used because it simultaneously provides (i) an order express-
ing “no more effort than,” (ii) an operation expressing sequential composition of efforts, and (iii)
a notion of “taking the best available option” as an infimum/meet (or, dually, “taking the worst”
as a supremum/join, depending on conventions). This avoids committing to effort being numeric;
it could be vector-valued (time, risk, attention), partially ordered (incomparable trade-offs), or
even extended with an “impossible” element representing infeasible constructions. The essential
requirement is that effort can be propagated through a composite description and then optimized
over the space of descriptions.
    The phrase “minimum representational effort” should be read as a design principle that converts
a descriptive problem into an optimization problem. Given a target object (a percept, prediction,
explanation, or action plan), and a family of available representational strategies (codes, models,
grammars, decompositions), the simplicity of the target for the observer is identified with the


                                                 148
least effort among those strategies. This makes simplicity explicitly dependent on the observer’s
repertoire: an object can be simple for one system (because it has an efficient internal code) and
complex for another (because it lacks the relevant decomposition).
    The “distinction policy” viewpoint is intended to make opening/closing precise. A distinction
policy is a rule (implicit or explicit) for which differences in the world are treated as relevant,
and which are collapsed as irrelevant. Opening corresponds to a directed change that admits
more distinctions (finer discrimination, increased sensitivity, more degrees of freedom in represen-
tation), while closing corresponds to a directed change that forbids distinctions (coarser discrim-
ination, compression, or ignoring degrees of freedom). Because these changes alter what can be
represented at all, they naturally induce changes in feasible effort: certain representations become
available/unavailable, and the costs of existing representations may change.
    Within this frame, resistance/submission is not introduced as a separate primitive but as the
effort landscape associated with changing the policy. Resistance expresses the additional effort
required to move in a certain direction in policy-space (for example, to open when a system is
currently closed, or to close when it is currently open), while submission expresses the relative
ease of moving with the local gradient (the direction that decreases effort or increases weakness,
depending on the dual convention). Thus “resistance” is not merely a psychological label; it is
a measurable asymmetry in how effort changes under directed transformations of the system’s
discrimination and control structure.
    The dual phrase “weakness maximization” is included to emphasize that effort minimization
can be equivalently presented as maximizing what a system cannot (or does not need to) do. On the
effort-minimizing view, a simple representation is one that requires little work. On the weakness-
maximizing dual view, a simple representation is one that intentionally leaves many distinctions
unresolved while still being adequate for the task, thereby preserving slack and avoiding commit-
ment. This duality will matter later when discussing robustness: sometimes a system becomes
more capable by refusing to overfit distinctions, i.e. by choosing policies that remain weak in the
right directions.
    Finally, compositional simplicity is treated as a least-fixed-point/dynamic-programming object
because “building wholes from parts” introduces recursion and shared substructure. If a system can
construct complex objects by combining simpler ones, then the effort to represent an object is not
just a property of the object in isolation but depends on the best decomposition into sub-objects,
the costs of the combination operations, and the reuse of previously constructed components. A
fixed-point characterization captures the stable assignment of minimal effort to each constructible
object under these combination rules, and it aligns with standard dynamic-programming logic:
compute the cost of a whole by minimizing over ways of assembling it from cheaper parts.
    The link to generalized Kolmogorov complexity is then conceptual rather than merely analogical.
In classical Kolmogorov complexity, simplicity is the length of the shortest program producing a
string, relative to a universal machine. Here, “program length” is replaced by the observer’s effort
quantale, and “universal machine” is replaced by the observer’s available representational operations
and distinction policy. Structural (grammar-like) complexity enters when representations are not
flat codes but compositional descriptions (grammars, rules, factor graphs, rewrite systems), in
which case the least-effort description typically reflects reusable structure rather than mere shortest
encoding.

Remark 290. Philosophically, this section attempts to treat “effort” not as a metaphor but as
a formally composable magnitude: something one can add along a chain of operations, minimize
over alternatives, and propagate through a system as a constraint. This makes effort play a role
analogous to “energy” in physics, but interpreted as an experiential-cognitive primitive rather than


                                                 149
a physical conserved quantity. The intended application is that later layers (patterns, habits, mind-
world correspondence) can talk about simplicity and resistance without silently switching between
incompatible notions of cost.

Remark 291. The intended level of generality is deliberately higher than “effort equals time” or
“effort equals number of steps.” Some observers have parallelism, caching, or learned shortcuts;
others face bottlenecks such as attention, working memory, or sensorimotor precision. A quantale-
based treatment is meant to keep these possibilities open while still enforcing the minimum structure
needed for compositional proofs: monotonicity (more demanding tasks should not cost less), com-
positionality (doing two things should cost at least doing each), and optimizability (alternatives
can be compared). This is also what makes it possible to talk about “effort gradients” for resis-
tance/submission without presupposing differentiability or even numeric effort.

Hyperseed concepts covered.

• Effort.

• Resistance/submission; opening/closing.

• Simplicity; compositional simplicity.

• (Generalized) Kolmogorov complexity; structural complexity.

• Minimum representational effort (as a design principle).

8.1   Effort as a cost structure
Hyperseed begins from the experiential primitive “effort” and then builds a derived notion of
simplicity. In a mathematical reconstruction, it is useful to represent effort using a compositional
algebra that supports: (i) sequential composition of acts/inferences/operations, (ii) choice among
alternatives, and (iii) taking minima over competing decompositions.
    One may view (iii) as the formal expression of “search over plans”: a single high-level act can
often be realized by many different decompositions into subacts, and effort should select the best
available decomposition by taking an infimum over a (possibly infinite) family of candidates. The
framework below is deliberately permissive about cardinality: in many realistic settings (e.g. con-
tinuous control, approximate inference, or anytime algorithms) the relevant set of decompositions
is naturally infinite, so the availability of arbitrary infima is not merely a technical luxury but the
algebraic counterpart of “optimize over all available implementations.”
    A standard choice (also used implicitly in shortest-path and dynamic programming) is the
Lawvere cost quantale.

Definition 75 (Effort quantale). Let

                                      E := ([0, ∞], ≥, inf, +, 0),

where the order is reversed (so that a ≤E b means a ≥ b as real numbers), the join in the quantale
order is inf (ordinary minimum), and the monoidal product is + (sequential composition of costs).
Then E is a commutative quantale: + distributes over arbitrary infima.

    It is sometimes helpful to keep in mind why [0, ∞] (with ∞ included) is used rather than [0, ∞).
Allowing ∞ provides a canonical value for “impossible” or “unavailable” processes within a context,


                                                  150
and it ensures that arbitrary infima always exist in the underlying complete lattice structure. This
aligns the formalism with optimization practice: if an operation cannot be performed under the
current constraints, it can be assigned effort ∞, and taking minima over alternatives then correctly
ignores it whenever a finite alternative exists.

Remark 292. Notation unpacking. The tuple ([0, ∞], ≥, inf, +, 0) should be read as follows:
the underlying set is the extended nonnegative reals [0, ∞]; the order relation used for the quantale
is the reversed real order (so “smaller effort” becomes “larger element” in the quantale order); the
quantale join (least upper bound in the quantale order) is inf in the usual real order; the monoidal
operation is + with unit 0. Saying “+ distributes over arbitrary infima” is exactly the familiar
identity
                                      a + inf bi = inf (a + bi ),
                                           i          i
which is what makes dynamic programming algebraically natural.

    One can also read the distributivity law operationally: if one has a fixed prefix act of cost a
and then must choose an optimal continuation among many options with costs bi , the optimal
total cost is obtained by adding a once and then optimizing the remainder, rather than re-solving
the whole problem from scratch for each candidate continuation. This is precisely the algebraic
skeleton behind Bellman-style optimal substructure.

Remark 293. Intuition. The reversed order is a small but important conceptual maneuver: we
want “better” to mean “easier,” i.e. lower cost. But many later constructions (especially those
expressed in quantale language, including weakness; Hyperseed-Concepts 202, 143) are more natu-
rally written as monotone statements in an order where “better” corresponds to “larger.” So we flip
the order once and then keep monotonicity statements in their natural direction; this is consonant
with the quantale-based treatment of weakness in [3] (and also with the broader Hyperseed ontology
presentation [1]).

   A related perspective (useful later, though not required here) is that E is the canonical “cost
domain” used in Lawvere’s approach to generalized metric spaces and enriched categories: addition
plays the role of path concatenation, and infimum plays the role of taking the best path among
many. This connection is one reason the same algebra reappears across shortest-path problems,
program semantics, and compositional models of planning.

Remark 294. Examples. If a system can solve a task by either: (1) doing method A costing
3 units, or (2) doing method B costing 5 units, then “choosing among alternatives” corresponds
to inf(3, 5) = 3. If it must do two steps in sequence costing 3 and 5, then the sequential effort is
3 + 5 = 8. Thus, even before one speaks of “minds,” this algebra captures the basic grammar of
optimization.

    It is also worth emphasizing that the “alternative set” over which inf is taken need not be
limited to two options. For instance, if a process can be implemented by selecting an integer
parameter k (say, the number of refinement iterations) and the effort scales as f (k), then the
best available implementation corresponds to inf k∈N f (k). If the infimum is not achieved by any
finite k (a common situation in asymptotic approximations), the formalism still cleanly represents
“arbitrarily close” improvements, which is often the right abstraction when one separates idealized
capability from finite-resource constraints.

Remark 295. We use the reversed order so that “better” (lower cost) corresponds to “larger”
in the quantale order. This makes formulas with inf and + align with the algebra of optimality:

                                                151
choosing among alternatives corresponds to taking inf, and composing steps corresponds to adding
costs.
Definition 76 (Effort of a process). Let P be a set of processes available to an observer in a fixed
context C. An effort assignment is a map
                                            Eff C : P → [0, ∞]
satisfying (as modeling assumptions):
• (Sequential subadditivity) Eff C (p; q) ≤ Eff C (p) + Eff C (q) whenever p; q denotes running p then q,
• (Choice) if p can be implemented by choosing between p1 and p2 , then Eff C (p) = min(Eff C (p1 ), Eff C (p2 )).
     The definition intentionally separates two layers: the abstract quantale E, which specifies the
algebra of combining and comparing costs, and the concrete map Eff C , which instantiates that
algebra for a particular observer and context. In categorical language (not required for later sections,
but conceptually clarifying), Eff C behaves like a lax monoidal measure of sequential composition:
it respects the monoidal operation + up to an inequality rather than on-the-nose equality, reflecting
that real implementations can reuse intermediate results, amortize setup costs, or exploit structure.
Remark 296. Intuition. An effort assignment is an observer-indexed bookkeeping device: it says,
within context C, how costly it is for the observer to execute certain operations. The inequalities
are deliberately weak. Sequential subadditivity says that doing two things in sequence should not cost
more than paying for each separately (because one can always execute them in the naive way). In real
systems there may be synergies (the combined act costs less than the sum) or frictions (overheads
not modeled here); the subadditivity axiom allows synergies and leaves room to represent frictions
elsewhere (e.g. via tC later).
    One can also interpret context dependence explicitly: the same “nominal” process p may have
very different effort in different contexts C because the observer’s available tools, cached state,
permissions, training, or environmental affordances differ. This is part of why the effort assignment
is not treated as an intrinsic property of p alone. For example, access to a GPU, a precomputed
index, or a specialized library can change Eff C (p) by orders of magnitude without changing the
abstract specification of p.
Remark 297. Examples. If p is “load a dataset” and q is “train a model,” then p; q is the
sequential procedure. If training reuses cached preprocessing from loading, then Eff C (p; q) may be
strictly less than Eff C (p) + Eff C (q). For “choice,” if p is “sort a list” and p1 is quicksort while p2 is
mergesort, then the observer may treat Eff C (p) as the cheaper of the two implementations available
in that context.
    A further example of frictions (not captured by subadditivity alone) is a fixed setup cost:
suppose running any nontrivial process incurs a one-time initialization overhead (allocating mem-
ory, starting a service, warming a cache). Then one may have Eff C (p; q) ≈ Eff C (p) + Eff C (q) −
(shared setup), which is synergy-like, but in other regimes one may see the opposite effect if the en-
vironment forces repeated setup (e.g. sandboxing, rate limits), motivating later context parameters
that explicitly model such overheads.
Remark 298. Usefulness. These axioms are the minimal interface needed to make later defini-
tions (simplicity as an infimum; compositional simplicity as a least fixed point) behave the way one
expects of optimization problems. They permit a clean separation between (i) the algebraic form of
“effort reasoning” and (ii) the empirical or architectural details of what an observer can actually
do, as emphasized in [19].

                                                    152
     In particular, because “choice” is modeled by a minimum and sequential composition is modeled
(at the quantale level) by addition, later notions of simplicity can be defined as the cost of the
cheapest description, explanation, or program that achieves a target. The present section therefore
fixes the cost calculus that makes such infimum-based definitions well-typed and compositional:
one can substitute equivalent subprocedures, refine a plan by expanding a step into substeps, and
still reason algebraically about the resulting effort.

8.2     Distinctions as policies; opening and closing
Hyperseed’s account of simplicity is inseparable from the idea that an observer may or may not
make certain distinctions. We model this using a distinction policy, conveniently represented by an
indistinction relation (the pairs the observer treats as the same for the task at hand). In particular,
the policy is meant to be task-relative: the same underlying observer may adopt different policies
for different contexts C, and even within a fixed C may move along a spectrum from very fine to
very coarse discrimination.
Definition 77 (Indistinction policy). Fix a finite universe X (of entities, states, events, or features
relevant in context C). An indistinction policy is a subset H ⊆ X × X, interpreted as:
      (x, y) ∈ H   means “the observer does not (currently) distinguish x from y in context C.”
Write HC ⊆ P(X × X) for the set of admissible policies for context C.
Remark 299. Scope and admissibility. The set HC is left abstract on purpose: in some appli-
cations, not every relation should be allowed. For example, an engineered sensor might be required
to treat indistinction symmetrically, or a legal/organizational setting might impose that indistinc-
tion respects certain categories (e.g. cannot collapse “approved” with “unapproved”). Conversely,
allowing HC to include non-equivalence relations makes it possible to represent partial, asymmet-
ric, or temporarily inconsistent discrimination patterns that occur under time pressure, noise, or
conflicting heuristics.
Remark 300. Intuition. An indistinction policy is the observer’s current answer to the question:
“Which differences matter here?” (Hyperseed-Concept 96) and, more sharply, “Which distinctions
will I actually enforce?” (Hyperseed-Concept 98). Representing it as a subset H ⊆ X × X empha-
sizes that the policy is a relation, not necessarily an equivalence relation. We are not assuming
symmetry, transitivity, or reflexivity; an observer may be inconsistent or paraconsistent about what
it merges, and later sections allow more graded/quantale-valued versions.
Remark 301. Extremes and calibration. Two boundary cases help calibrate the interpretation.
If H = ∅, then no pairs are explicitly treated as indistinct, corresponding to an idealized stance of
“distinguish everything from everything” (maximal discrimination, typically high effort). If H =
X × X, then every pair is treated as indistinct, corresponding to “everything is the same for this
task” (maximal collapse, typically low effort but also low discriminatory power). Most realistic
policies sit between these extremes, and the framework is designed to let later sections quantify the
cost/benefit of moving within this lattice of relations.
Remark 302. Examples. If X is a set of colors and the observer cannot distinguish nearby
shades, then H contains pairs of shades it treats as the same for the present task. If X is a set of
world-states and the observer ignores microphysical details, then H contains pairs of microstates
that are collapsed into one macrostate. In the most classical special case, H could be the graph
of an equivalence relation corresponding to a partition (coarse-graining), matching the probabilistic
coarse-graining discussion in Section 10.2.

                                                 153
Remark 303. Relation to representation maps. It is often helpful to think of a policy as being
implemented by some representation or measurement map π : X → R into a smaller set of reports
R, where (x, y) ∈ H whenever π(x) = π(y). This produces an equivalence relation (the kernel of π),
but the present definition is broader: it also covers situations where the observer’s “same/different”
judgments depend on direction, history, or limited local comparisons (e.g. x is treated as indistinct
from y for one subroutine but not vice versa). Keeping H as an arbitrary relation allows these cases
to be discussed without forcing a premature commitment to partitions.

Remark 304. Usefulness. Making the policy explicit allows later constructions to talk about
changing what is distinguished: opening and closing are then simply inclusion relations. This is a
way to treat “attention,” “granularity,” and “resolution” as first-class mathematical objects rather
than informal modifiers (cf. Hyperseed-Concept 60).

Remark 305. Order-theoretic viewpoint. Because policies are subsets of X × X, they inherit
the inclusion partial order. This gives a simple, compositional notion of “more indiscriminating”
versus “more discriminating” without requiring a numeric measure. Later, numeric notions of
effort or simplicity can be layered on top of this order (e.g. by assigning costs to relations or
to their generators), but the inclusion order is the minimal structural scaffold needed to compare
policies.

Definition 78 (Opening and closing). Given two policies H, H 0 ∈ HC :

• The transition H → H 0 is an opening (relaxation of distinctions) if H ⊆ H 0 .

• The transition H → H 0 is a closing (tightening of distinctions) if H 0 ⊆ H.

Remark 306. Intuition. Opening means: “I will now treat more pairs as indistinct,” i.e. I will
collapse more distinctions (Hyperseed-Concept 125). Closing means: “I will now treat fewer pairs
as indistinct,” i.e. I will enforce more distinctions (Hyperseed-Concept 72). It is useful to note the
direction: H ⊆ H 0 is an opening because H 0 is a bigger set of collapsed pairs.

Remark 307. Monotonic consequences. Under any reasonable downstream use of H (e.g.
defining which states are treated as interchangeable, or which features are ignored), opening is
monotone in the sense that anything permissible under H remains permissible under H 0 when
H ⊆ H 0 . Closing is the reverse move: it may invalidate previous simplifications by reintroducing
distinctions that must now be tracked, measured, stored, or acted upon. This monotonicity is what
makes openings/closings suitable as “policy moves” in later optimization and dynamical-control
discussions.

Remark 308. Examples. If X is the set of pixel configurations and the observer switches from
“full image” to “only average brightness,” the new policy collapses many more pairs of images and
is thus an opening. Conversely, switching from “only average brightness” to “average brightness
plus edge map” is a closing: fewer pairs remain indistinct.

Remark 309. Sequential changes. Openings and closings compose in the expected way along in-
clusion chains. For instance, H0 ⊆ H1 ⊆ H2 corresponds to successively coarsening discrimination,
while H2 ⊇ H1 ⊇ H0 corresponds to successively refining it. If a system alternates between opening
and closing, the resulting path may not be monotone; such non-monotone trajectories are precisely
what one expects when attention is reallocated over time (e.g. zooming out to gain tractability, then
zooming in on a salient subproblem).



                                                 154
Remark 310. Why needed. The opening/closing distinction is the bridge from phenomenological
vocabulary to optimization: it provides the partial order along which effort and weakness can be
compared. In later sections, opening/closing also becomes a dynamical control lever: a system
can spend effort to close (gain precision) or open (gain tractability), echoing the tradeoff themes
emphasized in [9].

Remark 311. Opening increases the set of collapsed distinctions (more pairs treated as “the
same”); closing decreases it. In Hyperseed terms: opening generally reduces representational ef-
fort (but may reduce control/predictive sharpness), whereas closing generally increases effort (but
may increase control/predictive sharpness).

Remark 312. Link to resistance and simplicity. Within this section’s theme (effort, resis-
tance, and simplicity), the policy language allows a clean separation between (i) what the world
presents (the complexity of X and its dynamics) and (ii) what the observer commits to tracking
(the chosen H). Resistance can then be modeled as the cost of maintaining a closing against pres-
sures to open (e.g. noise, limited bandwidth, competing tasks), while simplicity can be treated as the
availability of effective openings that do not destroy task performance. This sets up later formal-
izations in which simplicity is not merely “small description length,” but “small description length
relative to a tolerated indistinction policy.”

8.3   Effort of distinctions; resistance and submission
To connect policies to effort, we assume the observer incurs effort to maintain or compute distinc-
tions. This can be modeled in many ways; for this section we only require the directionality to
match the intended interpretation. Concretely, the partial order by inclusion on HC is read as
an “at least as discriminating as” relation: H ⊆ H 0 means that H keeps (at least) all the con-
straints/distinctions that H 0 keeps, so H 0 is a coarsening (an opening) of H. In many realizations
one can think of H as a partition, a σ-algebra, a hypothesis class, or a set of admissible histories;
in each case, enlarging H corresponds to allowing more states to be treated as equivalent, hence
reducing the informational or computational burden of maintaining sharp boundaries.

Definition 79 (Policy effort and marginal effort). A policy effort functional for context C is a
map
                                    Eff C : HC → [0, ∞]
that is antitone with respect to inclusion:

                               H ⊆ H0      =⇒     Eff C (H) ≥ Eff C (H 0 ).

Define the marginal effort of changing policy from H to H 0 as

                         ∆Eff C (H → H 0 ) := max 0, Eff C (H 0 ) − Eff C (H) .
                                                                             


Remark 313. Domain/codomain choices. Allowing Eff C to take values in [0, ∞] (rather than
only [0, ∞)) makes it possible to represent policies that are, in context C, effectively unrealizable for
the observer (e.g. a discrimination requiring unattainable sensor resolution or unbounded computa-
tion). No further regularity (continuity, convexity, additivity, etc.) is assumed here: the framework
is designed so that later sections can specialize Eff C according to the application.

Remark 314. Notation and conventions. The symbol Eff C has been used above as an effort
assignment on processes; here it is specialized to an effort assignment on policies H ∈ HC . This

                                                  155
is intentional: the policy is itself something the observer must implement (by allocating computa-
tion, attention, measurement, memory, etc.). Also note that max(0, ·) makes ∆Eff C a one-sided
“increase only” measure; it is a minimal operational proxy for resistance rather than a full signed
gradient. A signed analogue Eff C (H 0 ) − Eff C (H) could be introduced if one wanted to track both
“relief ” (negative changes) and “load” (positive changes), but for resistance the positive part is the
invariant needed.

Remark 315. Intuition. Antitonicity expresses the central phenomenological claim that fine-
grained discrimination is costly: if you collapse more distinctions (opening), you should not pay
more effort. The model is deliberately permissive: it does not insist that opening strictly decreases
effort, only that it does not increase it. Equivalently, if one reads ⊆ as a refinement order, then Eff C
is monotone with respect to “refinement makes things harder”: adding constraints cannot make the
observer’s implementation problem easier.

Remark 316. Examples. If H represents “distinguish 100 categories” and H 0 represents “dis-
tinguish only 10 categories,” then H ⊆ H 0 and Eff C (H) ≥ Eff C (H 0 ) says that maintaining 100
categories requires at least as much effort as maintaining 10. If closing from H 0 to H demands
extra memory or sensory precision, then ∆Eff C (H 0 → H) quantifies the added cost. A concrete
toy family is Eff C (H) = log |Π(H)| when H induces a finite partition Π(H) (or, more generally,
a description-length/MDL-type functional); then coarsening reduces the number of cells and does
not increase Eff C . Another common choice in probabilistic settings is to let Eff C (H) track the
expected coding or inference cost of operating with policy H under a context-dependent distribution;
antitonicity then expresses that enforcing additional distinctions cannot reduce expected operational
load.

Remark 317. Usefulness. This is the smallest assumption needed to define “resistance” without
psychologizing it. It also prepares the ground for more elaborate, history-dependent models of resis-
tance (habits) where opening can become costly because the system has invested in a high-resolution
policy and must now “unlearn” it. In particular, the present definition isolates an “instantaneous”
effort requirement associated to a policy as such; later, additional state variables can encode sunk
costs, commitments, or stabilizing feedbacks that make effort depend on the trajectory by which H
was reached.

Remark 318. Context dependence. The index C is essential: the same abstract policy H can
have different effort in different environments, embodiments, or task regimes (e.g. a classification
with 100 categories may be easy with a fast lookup table but hard if the categories must be inferred
from raw sensory streams). Formally, nothing forces Eff C and Eff C 0 to be comparable across con-
texts; the intended reading is that effort is observer-and-situation indexed, and comparisons are
meaningful only within a fixed C unless an explicit identification is provided.

Remark 319. If H → H 0 is an opening (H ⊆ H 0 ), antitonicity implies Eff C (H 0 ) ≤ Eff C (H),
hence ∆Eff C (H → H 0 ) = 0: opening does not require additional effort in this minimal model (it
releases constraints). If H → H 0 is a closing (H 0 ⊆ H), then ∆Eff C (H → H 0 ) measures the added
effort required to enforce more distinctions. A richer model (used later when habits are introduced
in Section 12) adds “habit penalties” so that opening may also be resisted. Note that no path-
additivity is assumed: even with a fixed Eff C , one need not have ∆Eff C (H → H 00 ) = ∆Eff C (H →
H 0 ) + ∆Eff C (H 0 → H 00 ); this absence of a required triangle law is deliberate, because resistance
will later be allowed to depend on intermediate reorganizations and nonlocal reparameterizations of
policy.


                                                  156