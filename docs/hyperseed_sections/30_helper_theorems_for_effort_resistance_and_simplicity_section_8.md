# 30 Helper theorems for effort, resistance, and simplicity (Section 8)

both components large represent a state of inconsistent information (in the paraconsistent sense)
rather than a collapse of the framework. The componentwise operations are chosen so that common
evidential patterns have direct algebraic expressions: ⊕ merges alternative arguments by retaining
the strongest available pro and con components, while ⊗ models the idea that support (and counter-
support) can be propagated along compositional patterns such as chains of “before” comparisons.
Optional coherence constraints (Def. 57) can then be seen as enforcing minimal compatibility
conditions between direct and composed evidence (for example, requiring that direct evidence for
t1 < t3 not be weaker than what is obtained by composing evidence for t1 < t2 and t2 < t3 ), while
still permitting the presence of both support and objection in the same comparison.

Why the remaining definitions are grouped here. The later notions referenced above
(Past/Future sets and ∼, becoming via Dist and NDVar/Becoming, the event-calculus operators,
TimeCtx and TemporalSimilarity, regularity predicates, and the functorial process view) are all
ways of turning proto-time plus graded evidence into derived structures that behave like temporal
semantics. The point of this section is not to reintroduce those constructions, but to collect helper
theorems that show they respect the underlying order/evidence architecture: closure properties
under ⊕ and ⊗, invariance under quotienting by ∼, and the stability of becoming- and event-level
predicates under the similarity/regularity constraints. Establishing these routine facts once lets
later sections focus on modeling choices rather than re-proving basic algebraic and order-theoretic
properties.

29.1    Strict proto-time order: basic derived rules
Lemma 20 (Asymmetry from strictness). If (T, <) is a strict partial order, then for all t1 , t2 ∈ T ,
                                          t1 < t2 → ¬(t2 < t1 ).
Remark 1610. Intuitively, this lemma says that if “t1 is strictly before t2 ,” then t2 cannot be
strictly before t1 . In ordinary temporal language this is almost tautological, but it is worth isolating
because it is exactly where the strict nature of < matters: asymmetry is derived from irreflexivity
plus transitivity.
    More explicitly, recall that a strict partial order is, by definition, a relation that is (i) irreflexive
(¬(t < t) for all t) and (ii) transitive (if t1 < t2 and t2 < t3 then t1 < t3 ). The point of
the lemma is that one does not need to add asymmetry as an independent axiom: it is already
forced by (i)–(ii). This matters later because we will treat < as the base “proto” structure and
layer additional semantic/evidential notions on top; keeping the base assumptions minimal prevents
accidental circularity when richer principles are introduced.
    This result functions as the minimal sanity check on proto-time (Hyperseed-Concept 142):
it rules out the simplest temporal contradiction inside the underlying order, even before we add
graded/paraconsistent evidence. Later results on cycles and linear extensions reuse the same idea
in increasingly global forms.
    A useful reformulation is that the binary relation < defines an orientation on pairs: once t1 < t2
holds, the opposite orientation is ruled out. In particular, even if < is not total (so that some pairs
are incomparable), whenever comparability does occur it is one-way only; this is the precise sense
in which strictness provides a minimal directional constraint.
Sketch. Assume t1 < t2 and t2 < t1 . By transitivity, t1 < t1 , contradicting irreflexivity.

Remark 1611. Proof sketch (strategy). Suppose both directions hold; then compose them to obtain
a self-loop, which strictness forbids.

                                                    616
    Key step. The only real move is applying transitivity to the pair of inequalities; irreflexivity
then closes the door. One may picture t1 < t2 as an arrow t1 → t2 in a directed graph: having also
t2 → t1 forces a 2-cycle, hence a loop.
    Geometric intuition. In a strict order, time cannot “bend back” onto itself at a point; if it did,
the point would be both before and after itself, collapsing the meaning of “before” (Hyperseed-Concept
63).
    It is also worth noting what the lemma does not assert: it does not say that either t1 < t2
or t2 < t1 must hold. Thus, the absence of symmetry is compatible with branching or partially
ordered temporal structures, where two moments may be incomparable (neither earlier nor later in
the proto-time sense), even though any asserted ordering must be coherent.

Lemma 21 (No directed cycles). If (T, <) is a strict partial order, there is no finite cycle t0 <
t1 < · · · < tn−1 < t0 for any n ≥ 1.

Remark 1612. This lemma globalizes Lemma 20: not only are 2-cycles forbidden, but any finite
directed cycle is. In graph terms, the directed graph of the relation < is a DAG.
    Two boundary cases are worth keeping in view. When n = 1, the “cycle” would read t0 < t0 ,
which is excluded exactly by irreflexivity; so Lemma 21 may be seen as extending irreflexivity from
length-1 loops to all finite loops. When n = 2, the cycle is precisely the configuration ruled out
by Lemma 20. For n ≥ 3, the lemma says that one cannot return to a starting point by stepping
strictly forward finitely many times.
    The importance is practical as well as conceptual. Many constructions—linear extensions, topo-
logical sorts, inductive proofs over time—silently presuppose acyclicity. Here we see that acyclicity
is not an extra axiom but a theorem of strictness, which will be exploited immediately in Lemma 22
and Theorem 27.
    From the standpoint of later “becoming”-style talk, acyclicity is the minimal condition under
which iterative “advance” operations are guaranteed not to revisit a prior state in finitely many
steps. This provides a clean separation: any apparent temporal looping must come from additional
structure (e.g. evidential layers) rather than from the underlying proto-time relation itself.

Sketch. By repeated transitivity, the cycle implies t0 < t0 , contradicting irreflexivity.

Remark 1613. Proof sketch (strategy). Collapse the whole cycle into a single inequality t0 < t0
by composing along the chain.
    Key step. “Repeated transitivity” is simply iterated application of transitivity to the successive
links t0 < t1 , t1 < t2 , . . . , tn−1 < t0 .
    Visual intuition. Any directed cycle is a closed directed path; transitivity lets us treat a path as
a single arrow. But a closed path becomes a self-arrow, which strictness excludes.
    For readers who prefer a fully explicit symbolic form: apply transitivity to t0 < t1 and t1 < t2
to get t0 < t2 ; then combine this with t2 < t3 to get t0 < t3 ; continue until reaching t0 < tn−1 ,
and finally combine with tn−1 < t0 to conclude t0 < t0 . The proof uses no finiteness of T , only the
finiteness of the alleged cycle.

Lemma 22 (Minimal and maximal elements exist in the finite case). If T is finite and (T, <) is
a strict partial order, then T has at least one minimal element (no predecessor) and at least one
maximal element (no successor).

Remark 1614. In a finite proto-time, there must be at least one “earliest” point (a minimal
element) and at least one “latest” point (a maximal element), though there may be many of each.



                                                  617
This does not mean time is linear; it means only that in any finite acyclic directed graph there is
a source and a sink.
    Concretely, “minimal” here means: t ∈ T such that there is no s ∈ T with s < t; “maximal”
means: there is no u ∈ T with t < u. In the directed-graph picture (with an arrow s → t whenever
s < t), a minimal element is a vertex of indegree 0 and a maximal element is a vertex of outdegree
0. The lemma therefore states a familiar graph-theoretic fact about finite DAGs, restated in order-
theoretic language suited to proto-time.
    This lemma is the engine behind linearization (Theorem 27): the standard topological sorting
argument repeatedly removes a minimal element and continues. Philosophically, it exhibits a mild
form of “temporal directionality” without imposing a single global present: direction emerges from
the impossibility of cycles.
    It is also useful to compare this finite result with the stronger (and non-equivalent) notion
of well-foundedness in the infinite case. Finiteness guarantees that one cannot keep moving to
predecessors forever; in infinite structures, the existence of minimal elements can fail unless one
assumes additional well-foundedness conditions. The present lemma thus isolates exactly what
finiteness buys us, without building in stronger assumptions than needed.
Sketch. If there were no minimal element, start at any t0 and choose t1 < t0 , then t2 < t1 , etc.
Finiteness forces a repeated element, yielding a cycle, contradicting Lemma 21. The maximal case
is dual.

Remark 1615. Proof sketch (strategy). Assume the opposite and build an infinite descending (or
ascending) chain by always stepping to a predecessor (or successor); finiteness forces repetition,
hence a cycle.
    Key step. The pigeonhole principle turns an infinite walk in a finite set into a repeated vertex;
strictness turns the repeat into a contradiction via Lemma 21.
    Geometric intuition. Think of repeatedly walking “backward in time.” If you can always take
one more step, then in a finite universe you eventually revisit a moment, implying time has looped.
    The “dual” maximal-element argument can be read either by reversing all inequalities or, equiv-
alently, by applying the same reasoning to the opposite relation > (which is also a strict partial
order whenever < is). This symmetry clarifies why the finite DAG picture yields both a source and
a sink rather than only one of them.

29.2    Graded/paraconsistent temporal evidence: useful inequalities
Lemma 23 (Path lower bound under transitive support). Assume the optional transitive support
constraint (Def. 57.2): B(t0 , t2 ) ≥ B(t0 , t1 ) ⊗ B(t1 , t2 ). Then for any chain t0 , t1 , . . . , tn ∈ T ,
                                                       n
                                                       O
                                       B(t0 , tn ) ≥          B(ti−1 , ti ).
                                                        i=1
                                                              Qn
In particular, on the positive channel, B + (t0 , tn ) ≥        i=1 B
                                                                        + (t                                     2
                                                                               i−1 , ti ) in the canonical [0, 1] quan-
tale.
Remark 1616. This lemma states a very general principle: if evidence for “before” composes
transitively, then the evidence for a long-range ordering is at least as strong as the cumulative
composition of the short-range evidences along any chosen chain. In the canonical quantale, “com-
position” on the positive channel is multiplication, so support decays (unless values are 1).
    The usefulness is algorithmic and epistemic. Algorithmically, it provides a guaranteed lower
bound when one infers distant temporal relations from local ones. Epistemically, it mirrors a sober

                                                       618
Russellian caution: chained inferences should not become more certain merely because they are
longer. In paraconsistent settings [23, 24], one may carry positive and negative channels in parallel;
this lemma is about the monotone accumulation of support (not the resolution of conflict).
Sketch. Induct on n. The case n = 2 is Def. 57.2. The inductive step composes B(t0 , tn ) ≥
B(t0 , tn−1 ) ⊗ B(tn−1 , tn ) and applies the hypothesis to B(t0 , tn−1 ).

Remark 1617. Proof sketch (strategy). Reduce an n-step chain to an (n − 1)-step chain plus one
final step, then apply induction.
    Key step. The transitive-support axiom (Def. 57.2) is exactly the n = 2 case; everything else is
bookkeeping of repeated composition via associativity of ⊗ (implicit in the quantale structure).
    Visual intuition. Picture a path t0 → t1 → · · · → tn with each arrow labeled by a strength.
Transitive support says the direct arrow t0 → tn must be at least as strong as the composed label of
the path.
Lemma 24 (Two-step threshold propagation). Assume transitive support (Def. 57.2) and the
canonical [0, 1]2 tensor. If B + (t1 , t2 ) ≥ α and B + (t2 , t3 ) ≥ β, then

                                                  B + (t1 , t3 ) ≥ αβ.

Equivalently, if B + (t1 , t2 ) ≥ τ and B + (t2 , t3 ) ≥ τ , then B + (t1 , t3 ) ≥ τ 2 .
Remark 1618. This is the concrete numerical form of Lemma 23 for a chain of length 2. The
statement is almost pedagogical: if each of two links has at least some reliability, the inferred two-
step relation has at least the product reliability.
    Its conceptual role is to make explicit how thresholds behave under inference. If one chooses a
single threshold τ for “strong evidence,” then chaining two strong evidences yields a weaker lower
bound τ 2 . This warns us that thresholding is not invariant under composition: in long chains, one
may need renormalization, alternative t-norms, or different proof policies.
Sketch. Take the positive component of Lemma 23 for n = 2.

Remark 1619. Proof sketch (strategy). Specialize the general chain bound to n = 2 and read off
the positive coordinate.
    Key step. In the canonical [0, 1]2 quantale, ⊗ is componentwise multiplication, so the composed
positive evidence is αβ.
    Intuition. Each step is a filter on certainty; two filters in series multiply their pass-through.
Lemma 25 (No positive-evidence 2-cycles under transitive+irreflexive support). Assume transitive
support (Def. 57.2), irreflexive support B + (t, t) = 0 (Def. 57.3), and the canonical [0, 1]2 tensor.
Then for all t1 , t2 ∈ T ,
                                     B + (t1 , t2 ) · B + (t2 , t1 ) = 0.
So it is impossible to have strictly positive evidence for both directions simultaneously.
Remark 1620. This lemma translates the strict-order intuition “no two-way arrows” into the
evidence layer. Under transitive support, a 2-cycle would yield evidence for a self-loop; irreflexive
support forbids any positive self-loop, so at least one direction of the 2-cycle must have zero positive
evidence.
    The significance is methodological: it separates two notions of inconsistency. One may have
paraconsistent evidence (positive and negative simultaneously) without having positive evidence for
both temporal directions. The latter would be a particularly strong kind of incoherence, and this
lemma shows how to preclude it with simple constraints.

                                                          619
Sketch. Apply transitive support to the length-2 loop t1 → t2 → t1 : B + (t1 , t1 ) ≥ B + (t1 , t2 ) ·
B + (t2 , t1 ). But B + (t1 , t1 ) = 0, hence the product must be 0.

Remark 1621. Proof sketch (strategy). Turn the two-way evidence into evidence for a self-loop
via transitivity, then use irreflexivity to force the product to vanish.
    Key step. The inequality B + (t1 , t1 ) ≥ B + (t1 , t2 ) · B + (t2 , t1 ) is the transitive-support axiom
applied to t0 = t1 , t1 = t2 , t2 = t1 .
    Graph intuition. If both arrows t1 → t2 and t2 → t1 had positive weight, then the round trip
t1 → t1 would inherit positive weight; irreflexive support declares that no round trip is allowed to
count as “forward in time.”

Lemma 26 (Conflict detection from anti-symmetry-as-evidence). Assume the optional constraint
(Def. 57.1): B + (t1 , t2 ) ≤ B − (t2 , t1 ). Then any strong positive evidence for t1 < t2 forces at least
as-strong negative evidence for t2 < t1 . If additionally B + (t2 , t1 ) is also strong, then (t1 , t2 ) is
paraconsistently ordered: both directions have strong positive and strong negative evidence.

Remark 1622. The axiom B + (t1 , t2 ) ≤ B − (t2 , t1 ) can be read as a disciplined bookkeeping rule:
support for one direction counts as (counter-)evidence against the reverse direction. Under this
discipline, strong belief that t1 is before t2 automatically implies strong disbelief that t2 is before t1 .
    The second sentence isolates a characteristic paraconsistent phenomenon (Hyperseed-Concept
198 in the general style, and paraconsistent valuation as in [23, 24]): one may still end up with
strong B + (t1 , t2 ) and strong B + (t2 , t1 ) simultaneously, in which case the bookkeeping forces strong
negative evidence in both directions too. This is not “resolved” here; rather, it is detected and made
explicit, so later mechanisms can decide how to act on it.

Sketch. Immediate from Def. 57.1 and symmetry of the statement under swapping indices.

Remark 1623. Proof sketch (strategy). Unpack the constraint and apply it directly.
   Key step. The condition is already pointwise: for each ordered pair it gives an inequality relating
+ in one direction to − in the reverse.
   Intuition. The lemma is less a “derivation” than a clarifying rephrasing: it tells you what Def.
57.1 means operationally.

Remark 1624. To make the phrase “strong” fully concrete, one may read it relative to any chosen
strength threshold θ (often with θ near the top of the scale in use). In that case the first conclusion
can be restated as the monotonic implication

                                   B + (t1 , t2 ) ≥ θ =⇒ B − (t2 , t1 ) ≥ θ,

which is exactly what the inequality B + (t1 , t2 ) ≤ B − (t2 , t1 ) guarantees. No additional algebra is
needed: the inequality transfers lower bounds on B + (t1 , t2 ) into the same lower bounds on B − (t2 , t1 ).
   In the same thresholded reading, the “paraconsistently ordered” situation described in the lemma
can be written as the joint satisfaction of four strong-evidence conditions,

             B + (t1 , t2 ) ≥ θ,   B − (t1 , t2 ) ≥ θ,         B + (t2 , t1 ) ≥ θ,   B − (t2 , t1 ) ≥ θ,

where the two negative terms arise from the two positive terms by applying Def. 57.1 once to
(t1 , t2 ) and once to (t2 , t1 ). Thus the bookkeeping constraint functions as a conflict amplifier in the
following precise sense: if the data source or aggregation procedure supplies strong support in both
directions, then the constraint necessarily yields strong opposition in both directions as well, making
the inconsistency explicit rather than latent.

                                                         620
Remark 1625. The name “anti-symmetry-as-evidence” is intended to highlight the distinction
between (i) enforcing classical antisymmetry of an order, which would prohibit t1 < t2 and t2 < t1
from both holding, and (ii) enforcing a relation between evidence values for opposite directions.
Def. 57.1 is of type (ii): it does not directly forbid having strong B + (t1 , t2 ) and strong B + (t2 , t1 ) at
the same time, but it ensures that such a situation cannot occur without simultaneously producing
correspondingly strong B − values. In other words, the constraint does not remove paraconsistency;
it makes its presence measurable in the B ± fields, which is the relevant output for later decision
policies.

Further detail (optional). Fix t1 , t2 and assume Def. 57.1, i.e. B + (t1 , t2 ) ≤ B − (t2 , t1 ). If B + (t1 , t2 )
is strong (e.g. ≥ θ for a chosen θ), then by transitivity of ≤ we have θ ≤ B + (t1 , t2 ) ≤ B − (t2 , t1 ),
hence B − (t2 , t1 ) is strong. If, in addition, B + (t2 , t1 ) is strong, then applying the same constraint
with indices swapped gives B + (t2 , t1 ) ≤ B − (t1 , t2 ), so B − (t1 , t2 ) is also strong. This yields the four
strong-evidence statements described in the lemma’s final sentence.

29.3     Linearization and quotient-by-indistinguishability
Lemma 27 (∼ is an equivalence relation). Let ∼ be defined by equality of Past/Future sets (Def.
59). Then ∼ is reflexive, symmetric, and transitive.

Remark 1626. The relation ∼ collapses time points that are observationally indistinguishable with
respect to the order structure: two points are equivalent if they have the same Past-set and the same
Future-set. This is a structural instance of an equivalence relation (Hyperseed-Concept ??) arising
from an invariance principle: if nothing in the order-theoretic neighborhood distinguishes t from s,
we treat them as the same “abstract time.”
    This quotienting move is philosophically suggestive: it echoes the idea that time is partially
constituted by relations (Whitehead’s process-relational stance [15]), and technically it prepares the
ground for a clean strict order on the quotient (Theorem 26).

Sketch. Reflexive/symmetric are immediate from set equality. For transitivity, if Past(t)=Past(s)
and Past(s)=Past(r), then Past(t)=Past(r), and similarly for Future.

Remark 1627. Proof sketch (strategy). Use the standard fact that equality is an equivalence
relation, applied separately to Past and Future.
    Key step. Transitivity is inherited from transitivity of equality: if two sets are equal to a third,
they are equal to each other.
    Intuition. This is the formal stamp that “indistinguishable” behaves the way one expects: it
partitions T into classes.

Lemma 28 (Indistinguishable points are incomparable). If t ∼ s and t 6= s, then neither t < s
nor s < t.

Remark 1628. This lemma asserts that if two distinct points have identical Past/Future pro-
files, then the order cannot place one before the other. If it did, that very fact would change the
Past/Future profile and hence destroy indistinguishability.
     The result matters because it ensures the quotient T /∼ is not hiding genuine order information:
when we collapse t and s, we are not collapsing a real before/after distinction (Hyperseed-Concept
98); rather, we are collapsing redundancy in the representation of proto-time (Hyperseed-Concept
142).



                                                       621
Sketch. If t < s, then t ∈ P ast(s) but t ∈
                                          / P ast(t) (irreflexivity), contradicting Past(t)=Past(s).
The case s < t is symmetric.

Remark 1629. Proof sketch (strategy). Show that comparability forces an asymmetry in the Past
sets.
    Key step. Irreflexivity is crucial: t ∈
                                          / P ast(t), but if t < s then t ∈ P ast(s). Thus Past(t) 6=Past(s).
    Visual intuition. If t were before s, then t would cast a “shadow into the past” of s that is absent
from the past of itself.

Lemma 29 (Quotient map is order-preserving and order-reflecting). Let q : T → T /∼ be q(t) = [t]
and let the quotient order be as in Def. 59. Then for all t1 , t2 ∈ T ,

                                         t1 < t2 ⇐⇒ [t1 ] < [t2 ].

Remark 1630. This lemma says the quotient is faithful to the original strict order: it neither
invents new strict order relations nor loses old ones. Order-preserving (t1 < t2 ⇒ [t1 ] < [t2 ]) is
expected; order-reflecting is the deeper assurance that if two equivalence classes are ordered, then
their representatives really were ordered.
     This is the technical heart of treating T /∼ as an “abstracted” proto-time. In Hyperseed language,
it is a disciplined abstraction (Hyperseed-Concept 51) that respects temporal structure (Hyperseed-
Concept 142), a theme that also appears elsewhere in the system as abstraction-by-quotient.

Sketch. (→) If t1 < t2 , then by definition [t1 ] < [t2 ]. (⇐) If [t1 ] < [t2 ], there exist representatives
s1 ∼ t1 and s2 ∼ t2 with s1 < s2 . If t1 were not < t2 , Past/Future equalities plus the existence
of a comparable representative force a contradiction (same kind of reasoning used to show well-
definedness in Lemma 1).

Remark 1631. Proof sketch (strategy). The forward direction is definitional. The reverse direc-
tion argues that comparability is a class property: if some representatives are comparable, then all
representatives must align, because ∼ fixes Past/Future structure.
    Key step. The Past/Future invariants prevent a situation in which s1 < s2 but t1 and t2 are
not ordered: if s1 is in the Past of s2 , then (via equality of Past/Future sets within each class) the
corresponding membership relations must transfer to t1 and t2 .
    Intuition. Equivalence classes are meant to be “structural positions” in the order. If one repre-
sentative sits before another, the whole class sits before the other class; otherwise, the classes would
not be positions but merely bags of points.

Theorem 26 (Quotient order is strict (helper restatement of Lemma 1)). The relation < on T /∼
defined in Def. 59 is well-defined and makes (T /∼, <) a strict partial order.

Remark 1632. This theorem assures that the quotient construction yields a genuine proto-time
again: it is not merely a set of classes, but a set of classes equipped with a strict partial order.
“Well-defined” is the subtle point: we must not let the ordering depend on which representative
of a class one picks. It connects directly to Lemmas 27–29: the equivalence relation gives the
partition, incomparability protects against collapsing real order, and order-reflection preserves the
semantics of before/after. Taken together, they justify the quotient as an abstraction step in the
sense of Hyperseed (Hyperseed-Concept 51). In particular, the quotient does not “invent” new
temporal distinctions: it merely re-expresses the original proto-time in a coarser vocabulary where
indistinguishable points are treated as a single abstract point, while all genuine <-constraints remain
detectable at the level of equivalence classes.


                                                    622
Sketch. Well-definedness: comparability of one representative is incompatible with incomparability
of another when Past/Future sets are equal; strictness descends because any cycle in the quotient
would lift to a cycle in T . (This is the proof idea of Lemma 1.) More explicitly, if the quotient
order is defined by [t1 ] < [t2 ] iff there exist representatives t01 ∈ [t1 ], t02 ∈ [t2 ] with t01 < t02 , then
Past/Future equality is used to show that whenever one such witnessing pair exists, every choice
of representatives remains compatible with < in the sense that the opposite inequality cannot be
witnessed without contradicting incomparability preservation. For strictness, if [t0 ] < [t1 ] < · · · <
[tk ] = [t0 ] were a directed cycle among classes, choosing witnesses for each step produces a directed
cycle in T , contradicting Lemma 21.

Remark 1633. Proof sketch (strategy). For well-definedness, show that if [t1 ] < [t2 ] holds via
some representatives, it cannot fail via others. For strictness, transfer irreflexivity/transitivity (or
equivalently, acyclicity) from T to the quotient.
    Key steps. (i) Past/Future equality makes “being before” a class invariant. (ii) Any directed
cycle among classes would choose representatives to yield a directed cycle in T , contradicting
Lemma 21. Concretely, (i) is used in the contrapositive form: if two elements have identical
Past/Future sets, then there is no third point that can distinguish them by being before one but
not the other; this blocks the possibility that swapping representatives could flip a strict inequality
into a non-inequality. Step (ii) is the familiar “lift a cycle” maneuver: since each edge in the
quotient is witnessed by at least one edge in T , a cyclic chain of class-edges forces a cyclic chain
of element-edges.
    Intuition. Quotienting is safe here because the equivalence relation was designed from the order
itself; it forgets only redundancy, not structure. Put differently: proto-time is the primary structure,
and the quotient is a controlled compression of that structure, justified exactly because the defining
indistinguishability criterion is stated in terms of observable order-theoretic behavior (Past/Future),
rather than in terms of an external labeling.

Theorem 27 (Finite proto-times admit linear extensions (helper restatement of Theorem 5)). If
(T, <) is a finite proto-time, there exists a strict total order ≺ on T such that t1 < t2 → t1 ≺ t2 .

Remark 1634. A linear extension is a way of telling a complete story from a partial order: it
imposes a total order ≺ that respects all the constraints of <. When proto-time represents a web
of “must-be-before” constraints, a linear extension is a choice of one consistent timeline compatible
with them.
    This is important because many algorithms (simulation, scheduling, event calculus iteration) are
most naturally run over a linear order. The theorem says that for finite proto-times this is always
possible: one may add arbitrary tie-breaks among incomparable points without creating contradic-
tions. The proof relies on Lemma 22 and is the standard topological sorting argument. Equivalently,
one may view (T, <) as a finite acyclic directed graph and produce ≺ by repeatedly selecting a node
with no incoming edges; the finiteness assumption ensures the process terminates, while acyclicity
ensures one can always continue. Note that the construction generally produces many possible ≺,
reflecting the underdetermination present in the original proto-time.

Sketch. Induct on |T | using existence of a minimal element (Lemma 22), place it first, and extend
the remainder inductively (standard topological sort proof). More explicitly, choose a <-minimal
m ∈ T , define ≺ to start with m, restrict < to T \ {m} (which remains a finite proto-time), apply
the induction hypothesis to obtain a linear extension ≺0 on the remainder, and then concatenate
m with ≺0 . Minimality of m ensures no constraint t < m is violated, and the induction hypothesis
ensures all constraints internal to T \ {m} are respected.


                                                      623
Remark 1635. Proof sketch (strategy). Repeatedly peel off a minimal element and put it next in
the total order.
    Key step. Lemma 22 guarantees there is always at least one minimal element to peel off until
the set is empty. Induction then assembles these choices into a strict total order. The strictness
of ≺ is automatic because the construction never places two distinct elements in the same position,
and transitivity follows from the fact that each stage appends a well-ordered remainder.
    Intuition. In a finite acyclic dependency graph, there is always something you can do first;
do it, remove it, and repeat. When there are several minimal choices at some stage, each choice
corresponds to a different but equally valid “completion” of the partial temporal information encoded
by <.

Lemma 30 (Soundness of linearization; incomparability is not preserved). Let ≺ be a linear ex-
tension of (T, <). Then:
                             t1 < t2 → t1 ≺ t2 (soundness),
but in general,
                                 t1 ≺ t2 6→ t1 < t2    (not complete).
In particular, if t1 and t2 are incomparable in <, ≺ still forces exactly one of t1 ≺ t2 or t2 ≺ t1 .

Remark 1636. This lemma is a cautionary counterpart to Theorem 27. A linear extension is
sound with respect to <: it never violates the original constraints. But it is not complete: it
introduces additional comparabilities that were not present in the proto-time. Incomparable events
become artificially ordered.
    The point is conceptual as much as technical. Linearization is an interpretive act: it selects a
narrative from a partial structure. Hyperseeds stance is to keep proto-time primary and treat any ≺
as a derived convenience, not as ontology itself (Hyperseed-Concept 142). This distinction prevents
one from mistaking a bookkeeping choice for a metaphysical fact. A simple example is a proto-time
with two events a, b such that neither a < b nor b < a; any linear extension must pick either a ≺ b
or b ≺ a, but that choice encodes no additional constraint in the underlying model. Accordingly, any
subsequent reasoning that depends on the newly introduced order (e.g., treating a ≺ b as evidence
that a “really” precedes b in proto-time) is methodologically unsound unless it is explicitly stated as
a convention or an extra assumption.

Sketch. Soundness is the definition of linear extension. Non-completeness holds because a total
order must compare incomparable pairs, introducing an arbitrary choice that does not imply <.
Formally, if t1 and t2 are incomparable under <, then t1 < t2 is false and t2 < t1 is false, but
totality of ≺ forces exactly one of t1 ≺ t2 or t2 ≺ t1 ; hence either way one obtains an instance of
t1 ≺ t2 (or its reverse) that does not correspond to a <-fact. This shows that ≺ may strictly extend
< by adding relations not entailed by the proto-time.

Remark 1637. Proof sketch (strategy). The first implication is immediate from the definition;
the second is forced by the nature of total orders.
    Key step. Totality means every pair is comparable under ≺, so ≺ contains at least one of (t1 , t2 )
or (t2 , t1 ) even when < contains neither. Thus, while < embeds into ≺ (soundness), the embedding
is typically proper: ≺ contains additional ordering information not justified by proto-time alone.
    Intuition. Linearization is like choosing an ordering of chapters in a book built from partially
ordered notes: it respects the dependency constraints but still chooses an order where none was man-
dated. The extra order is best understood as a convenient serialization for execution or exposition,
not as a discovery of hidden temporal structure.


                                                 624
29.4    Becoming as boundary non-duality: operational lemmas
Lemma 31 (Necessary paraconsistent boundary condition). If x becomes y along (T, <) (Def. 62),
then there exists a neighborhood U ⊆ T near the transition such that for all u ∈ U ,

                                        Dist(u; x, y) ≥ (θ, θ)

for the chosen NDVar threshold θ (Def. 61).

Remark 1638. The core idea of becoming (Hyperseed-Concept 62) here is neither simple replace-
ment nor mere succession. Rather, it is characterized by a boundary region in which x and y are
held together in a kind of structured ambiguity: strong evidence both for and against their dis-
tinction, formalized via NDVar (Hyperseed-Concept 120) and ultimately via a paraconsistent Dist
valuation.
    This lemma extracts the operational test that any implementation must satisfy: if the theory
declares “x becomes y,” then there must exist some time neighborhood where Dist is simultaneously
high in both channels. This is the minimal trace of Whiteheadian transition (process and becoming
[15]) rendered in quantale-valued evidence.

Sketch. Immediate: boundary non-duality (Def. 62.2) is NDVar at each u near the transition, and
NDVar is Dist(u; x, y) ≥ (θ, θ) by Def. 61.

Remark 1639. Proof sketch (strategy). Unpack the definitions: Def. 62 reduces becoming to
boundary NDVar; Def. 61 reduces NDVar to a threshold on Dist.
   Key step. The inequality Dist(u; x, y) ≥ (θ, θ) is simply the bundled form of “both positive and
negative components are at least θ.”
   Intuition. Becoming must leave a signature: a zone where the system is compelled to treat x and
y as both distinct and not-distinct (Hyperseed-Concept 121), rather than switching instantaneously.

Remark 1640. Further operational reading. The neighborhood U in Lemma 31 should be under-
stood as an interval of indeterminacy around the transition locus, not necessarily symmetric and
not necessarily unique. In applications where T carries additional structure (e.g. a topology or
a metric), “near the transition” can be instantiated as a small open interval, a finite window in
discrete time, or any other admissible neighborhood notion used by Def. 62. The lemma itself only
needs the minimal neighborhood concept already assumed in the definition of becoming.
    Why the inequality is two-channel. Since Dist(t; x, y) is paraconsistent, the condition Dist(u; x, y) ≥
(θ, θ) does not mean “maximal confusion”; it means that both (i) evidence for distinction and (ii)
evidence against distinction cross the same operational floor. This is exactly the boundary-style sig-
nal: the system is pulled in incompatible directions strongly enough that a classical crisp predicate
(distinct vs. identical) cannot be consistently applied in that region.
    Threshold dependence. For fixed Dist, the choice of θ tunes how demanding the test is. Increas-
ing θ makes becoming harder to certify, shrinking the set of times counted as boundary; decreasing
θ enlarges it. Thus the lemma is best read as a relative statement: given the θ that defines NDVar
(Def. 61), becoming forces a θ-robust paraconsistent band to exist around the transition.

Remark 1641. Implementation note (minimal check). In a computational or empirical setting,
Lemma 31 can be used as a necessary diagnostic: sample or estimate Dist(t; x, y) on a candidate
transition window and verify that there exists a contiguous set of times on which both components
exceed θ. Failure of this diagnostic rules out becoming regardless of any higher-level narrative about
x and y.


                                                 625
Lemma 32 (Non-becoming tests). Fix (T, <) and Dist.

  1. If there is no t ∈ T with Dist(t; x, y) ≥ (θ, θ), then x does not become y.

  2. If Dist(t; x, y) ≥ (θ, θ) for all t ∈ T , then x does not become y (because Def. 62.3 cannot be
     satisfied).

Remark 1642. This lemma gives two complementary failure modes for becoming. The first is the
obvious one: if x and y are never in the required non-dual-variety relation, then there is no boundary
region and hence no becoming. The second is subtler: if x and y are in NDVar everywhere, then
the boundary ceases to be a boundary—there is no “outside” where the system recovers ordinary
distinguishability.
    Operationally, these tests matter because they prevent over-ascription. Without them, one might
call everything a becoming, either by never checking for the boundary signature or by allowing a
perpetual blur to count as transition. The formalism insists that becoming is a localized phenomenon:
neither absent everywhere nor present everywhere.

Sketch. (1) Contrapositive of Lemma 31. (2) Def. 62 requires a boundary region U where NDVar
holds, but also that away from U the pair is more distinguishable (not strongly paraconsistent). If
NDVar holds everywhere, the ”outside” clause fails.

Remark 1643. Proof sketch (strategy). Part (1) is direct contrapositive reasoning; part (2) checks
the “boundary vs. outside” clause in the definition of becoming.
    Key step. The distinction between “there exists a neighborhood U ” and “outside U something
different happens” is what blocks the degenerate case where NDVar is ubiquitous.
    Intuition. A boundary is meaningful only if it separates regions with different character; other-
wise it is just uniform fog.

Remark 1644. Clarifying the two failure modes. Items (1) and (2) exclude opposite extremes:

   • In (1), Dist never reaches the paraconsistent threshold in both channels simultaneously, so
     there is no candidate region in which x and y can be held in the structured ambiguity required
     by boundary non-duality. Even if Dist occasionally makes x and y look similar (e.g. one
     channel high), the defining feature of NDVar is the joint lower bound.

   • In (2), the condition holds everywhere, so NDVar becomes the background state rather than a
     transition signature. The intended reading of Def. 62.3 is that becoming is witnessed not only
     by a boundary band but also by a recovery of “ordinary” discriminability away from that band.
     If there is no such recovery, then the situation is better described as persistent non-duality (a
     standing ambiguity) rather than becoming (a bounded passage).

These tests therefore delineate a middle regime: becoming is compatible with NDVar holding for
some times (enough to form a neighborhood) but not for all times.

Remark 1645. Discrete vs. continuous time. When T is discrete (e.g. T = Z or a finite sequence
of frames), a “neighborhood” U can be instantiated as a finite block of indices around a transition
index. Lemma 32(1) then becomes a simple scan for any index with Dist(t; x, y) ≥ (θ, θ), while
Lemma 32(2) becomes a check for the degenerate case where every index satisfies the NDVar in-
equality. When T is continuous, the same logic applies, but the existence of U is naturally read as
the presence of an interval (possibly small) on which the inequality persists.



                                                 626
Remark 1646. Robustness under strengthening the outside clause. The exclusion in Lemma 32(2)
is intentionally weak: it does not require specifying how much more distinguishable x and y must
become outside U , only that Def. 62.3 fails if NDVar holds everywhere. In settings where one
strengthens Def. 62.3 (for example, by requiring Dist(t; x, y) 6≥ (θ, θ) on a nontrivial set outside
U , or by requiring a quantitative drop in at least one component), the same failure mode remains:
ubiquitous NDVar leaves no room for any strengthened “outside” behavior either.

29.5    Quantale-valued event calculus: monotonicity and inertia rules
Lemma 33 (Rule contributions are lower bounds; multiple proofs join). For a quantale-valued
Horn rule (Def. 64),
                             P (x̄) ⇐ Q1 (x̄1 ) ∧ · · · ∧ Qn (x̄n ),
the semantics enforces the pointwise lower bound

                               JP (x̄)K ≥ JQ1 (x̄1 )K ⊗ · · · ⊗ JQn (x̄n )K.

If multiple rules/instantiations derive the same head, the resulting head value is at least the ⊕-join
(componentwise max in [0, 1]2 ) of all contributions.

Remark 1647. This lemma clarifies how quantale-valued inference behaves: each rule instance
contributes a lower bound on the heads truth-value. Conjunction in the body corresponds to ⊗
(so evidence composes), and multiple independent derivations aggregate via ⊕ (so the strongest
derivation in each channel dominates, in the canonical model).
    The importance is that it makes explicit the proof-theoretic meaning of the quantale connectives.
One can read ⊕ as “alternative reasons” and ⊗ as “joint reasons,” which aligns with the broader
goal of implementing a graded, potentially paraconsistent event calculus (Hyperseed-Concept ??)
using algebraic semantics [23, 24].

Sketch. This is exactly Def. 64: conjunction maps to ⊗ and alternative derivations aggregate by
⊕.

Remark 1648. Proof sketch (strategy). This is definitional: interpret the rule under the chosen
semantics.
    Key step. The only “work” is remembering which connective maps to which quantale operation.
    Intuition. A rule is not a claim that the head equals the bodys value; rather, it guarantees at
least that much support. Additional rules can only add more support (via ⊕), never subtract it.

Remark 1649. A useful way to read the displayed inequality is as a semantic analogue of modus
ponens for graded proofs: whenever the body holds to some degree (in the quantale order), the
head must hold to at least the corresponding combined degree. In particular, if V = [0, 1]2 with
the pointwise order, the inequality means that each coordinate of JP (x̄)K is bounded below by the
corresponding coordinate of the ⊗-product of the body coordinates. This coordinatewise reading
is what makes the “componentwise max” description of ⊕ operationally transparent: independent
derivations can improve one channel without harming the other.
    Note also that the lemma is phrased as a lower bound rather than an equality because the canon-
ical model is designed to be proof-accumulative: the semantics must admit additional support for
P (x̄) coming from other rules, from facts, or from later iterations in a fixpoint construction. Thus
the inequality is the correct algebraic statement of “sound rule application” in a setting where mul-
tiple sources of evidence may coexist.


                                                   627
Lemma 34 (Monotonicity of proof accumulation). Assume all rules are built using only ⊕, ⊗, and
monotone operations on V (as in Theorem 6). Then increasing any premise value (in the pointwise
order on assignments) cannot decrease any derived head value.
Remark 1650. Monotonicity is the quiet structural condition that makes fixpoint semantics pos-
sible. It says: if you strengthen the premises (in either evidence channel), you cannot end up with
weaker conclusions. This is the algebraic analogue of the ordinary Horn-clause property that adding
facts does not invalidate derivations.
    This lemma is the hinge connecting local rule evaluation to global least-fixpoint constructions
(Theorem 28). Without monotonicity, iterative semantics may oscillate or depend on evaluation
order. With it, one may safely “accumulate proofs” as a growing approximation.
Sketch. ⊕ and ⊗ are monotone in each argument; joins over index sets preserve monotonicity. Thus
each rule contribution is monotone, and the aggregate is monotone.

Remark 1651. Proof sketch (strategy). Reduce the claim to the monotonicity of the constructors
used to build rule bodies and aggregation.
    Key step. The pointwise order on V (·) means monotonicity is checked coordinatewise at each
ground atom/time; ⊕ and ⊗ preserve inequalities coordinatewise.
    Intuition. If inference is built only from operations that never reverse inequalities, then inference
itself never reverses them.
Remark 1652. Concretely, if ν ≤ ν 0 are two assignments of values in V to ground atoms (so
ν(A) ≤ ν 0 (A) for every atom A), then for any fixed rule instance, the body evaluation under ν is
≤ the body evaluation under ν 0 because it is computed by composing monotone operations (iterated
⊗ and any other admissible monotone connectives). Applying the lemma repeatedly over all rule
instances shows that a single “round” of consequence generation defines a monotone operator on
the complete lattice of assignments, which is the exact hypothesis needed to justify least fixpoints
(and hence canonical minimal models) by standard order-theoretic arguments.
    This also explains why non-monotone connectives (for example, a classical negation interpreted
as order-reversing) are excluded from the rule building blocks in this fragment: they would break the
monotone-operator property and thereby undermine the intended “accumulate and join” reading of
proofs.
Lemma 35 (Clipped lower bound and monotonicity). Define Clipped as in Def. 65:
                                 M
        Clipped(f ; t1 , t2 ) :=         Happens(a, u) ⊗ T erminates(a, f, u).
                                  a∈A, u∈T : t1 <u<t2

Then for any particular witness (a, u) with t1 < u < t2 ,
                     Clipped(f ; t1 , t2 ) ≥ Happens(a, u) ⊗ T erminates(a, f, u).
Moreover, Clipped is monotone in each of Happens and T erminates.
Remark 1653. The operator Clipped expresses the idea that a fluent f might fail to persist from
t1 to t2 because some terminating action happened in between. Quantale-valuedly, we aggregate
all such potential terminating witnesses by a big ⊕. The lemma says two things: any particular
terminating witness contributes a guaranteed lower bound, and strengthening either the evidence for
actions happening or for their terminating effects can only increase the clippedness.
    This is a typical pattern in the algebraic event calculus (Hyperseed-Concept ??): existential
search over possible witnesses becomes a join over an index set, and the order-theoretic properties
(lower bounds, monotonicity) become immediate consequences of the quantale operations.

                                                   628
Sketch. The witness inequality holds because Clipped is a ⊕-join over a set that includes that term.
Monotonicity follows from monotonicity of ⊗ and ⊕.

Remark 1654. Proof sketch (strategy). Use the universal property of joins: a join is above each
joined element.
    Key step. The specific pair (a, u) is among the indices being joined, so its term is bounded above
by the join.
    Intuition. “Clipped” means “there exists evidence of a terminator”; ⊕ is the algebraic stand-in
for that existential.

Remark 1655. It is often helpful to separate two layers in the definition of Clipped: (i) for each
candidate witness (a, u), the conjunction “Happens(a, u) and T erminates(a, f, u)” is evaluated by
⊗, producing a single combined piece of evidence that f is terminated in the open interval (t1 , t2 );
and (ii) these candidate pieces of evidence are pooled by ⊕ across all intermediate times and actions.
The first layer corresponds to requiring both an occurrence and an appropriate effect; the second
corresponds to allowing any intervening terminator to suffice.
    In particular, in the [0, 1]2 setting, if one coordinate tracks positive support and the other tracks
negative support (or, more generally, two independent evidential channels), then Clipped can in-
crease in either coordinate as soon as there is a single witness whose combined ⊗-value increases
in that coordinate. This coordinatewise behavior is precisely what is needed later when inertia is
formulated as a rule with a condition like “ not clipped”: the clippedness score provides a graded ob-
struction to persistence that can be compared and combined monotonically in the subsequent fixpoint
computation.

Lemma 36 (One-step inertia propagation bound). Let Φ be the inertia update operator (Def. 66):
                                              M
    (ΦHoldsAt)(f, t2 ) := HoldsAt0 (f, t2 ) ⊕    HoldsAt(f, t1 ) ⊗ ¬Clipped(f ; t1 , t2 ).
                                                     t1 <t2

Then for any t1 < t2 ,

                     (ΦHoldsAt)(f, t2 ) ≥ HoldsAt(f, t1 ) ⊗ ¬Clipped(f ; t1 , t2 ).

Remark 1656. This lemma isolates a single contribution to inertia: if f held at some earlier time
t1 , and there is strong evidence that it was not clipped between t1 and t2 , then the update Φ ensures
that f holds at t2 with at least the composed strength. It is the quantale-valued analogue of the
familiar persistence axiom.
     The reason to spell this out is practical: in implementations, one often wants interpretable
justifications for why a fluent holds. This inequality tells you exactly which term in the big join
witnesses that justification.

Remark 1657. Two order-theoretic facts are being used implicitly here and will        L reappear through-
out: (i) in any join-semilattice, a join dominates each of its summands, i.e. i xi ≥ xj for every
j; and (ii) ⊕ itself is a join-like operation, so for any a, b one has a ⊕ b ≥ b (and also a ⊕ b ≥ a).
In particular, even if HoldsAt0 (f, t2 ) is weak (or ⊥), the joined inertia support still lower-bounds
the total update.
      Note also that the term HoldsAt(f, t1 ) ⊗ ¬Clipped(f ; t1 , t2 ) is a single causal path from past to
present: it composes (i) the degree to which f held at t1 with (ii) the degree to which the interval
[t1 , t2 ] is free of terminating events for f . The lemma says that Φ never discards such a candidate
path; it can only keep it or be strengthened by other paths via ⊕.


                                                   629
Sketch. Immediate: the right-hand term is one of the joined summands in Def. 66.

Remark 1658. Proof sketch (strategy). Again use the fact that a join dominates each summand.
    Key step. The index t1 is included in the join over all t1 < t2 , so its corresponding term provides
a lower bound.
    Intuition. Inertia is modeled as “take the best surviving support from the past”; any particular
past-support path is a candidate, and the operator keeps at least the best one via ⊕.

Remark 1659. For readers who want the inequality written as an explicit chain, one may unpack
Def. 66 as follows. Let
                             M
                        S :=   HoldsAt(f, t) ⊗ ¬Clipped(f ; t, t2 ).
                                  t<t2

Then (ΦHoldsAt)(f, t2 ) = HoldsAt0 (f, t2 ) ⊕ S ≥ S by join-domination, and S ≥ HoldsAt(f, t1 ) ⊗
¬Clipped(f ; t1 , t2 ) because t1 is one of the indices in the join defining S. Chaining these inequalities
yields the claimed bound.
    Operationally, the lemma can be read as a local certificate: to justify a lower bound on (ΦHoldsAt)(f, t2 ),
it suffices to exhibit one earlier witness time t1 together with the corresponding unclipped evidence,
without needing to inspect the other summands.

Theorem 28 (Least fixpoint semantics for monotone temporal inference (helper restatement of
Theorem 6)). Assume T is finite and all event-calculus rules use only ⊕, ⊗, and monotone op-
erations on V . Then the induced immediate-consequence operator (e.g. Φ) is monotone on the
complete lattice (V F ×T , ≤) and hence has a least fixpoint.

Remark 1660. This theorem provides the semantic foundation for the quantale-valued event cal-
culus: the meaning of the theory is given by the least stable assignment of truth-values to all
fluent-time pairs that satisfies the rules. That least fixpoint corresponds to “nothing is believed
unless forced by the rules,” generalized to graded/paraconsistent belief.
    The result is important because it replaces ad hoc procedural evaluation with an order-theoretic
guarantee: iterating the immediate-consequence operator from the bottom converges (in finitely
many steps when T is finite) to a canonical model. This style of reasoning via fixed points is a
recurring tool in analyzing self-referential or self-updating systems (see also [10] for related fixed-
point analyses in agent goal dynamics), and it sits naturally within the process view (Hyperseed-
Concept 140) where “what holds” is stabilized by iterated update.

Remark 1661. A useful way to read the statement is to separate (a) the domain and (b) the
operator. The domain V F ×T is the space of all functions assigning each fluent-time pair (f, t) a
value in V ; the order is pointwise: X ≤ Y iff X(f, t) ≤ Y (f, t) for all (f, t). Completeness then
follows from the fact that arbitrary joins and meets can be taken pointwise, e.g.
                   M               M               ^              ^
                        Xi (f, t) =      Xi (f, t),       Xi (f, t) =    Xi (f, t),
                     i∈I             i∈I                i∈I             i∈I

so the Knaster–Tarski theorem applies as soon as monotonicity of the immediate-consequence map
is established.
    The finiteness of T is used for the computational reading (finite convergence of iteration). Ex-
istence of lfp itself does not require T finite; it is guaranteed by Knaster–Tarski on any complete
lattice. What finiteness buys is that the ascending chain produced by Kleene iteration from ⊥ cannot
increase indefinitely through distinct time-slices without eventually stabilizing in the finite product.

                                                  630
Sketch. V F ×T is a complete lattice under pointwise order. Each rule contribution is monotone
(Lemma 34), hence the overall operator is monotone. Apply Knaster–Tarski to obtain a least
fixpoint.

Remark 1662. Proof sketch (strategy). Prove the operator is monotone; then invoke the Knaster–
Tarski theorem, which guarantees least and greatest fixpoints for monotone maps on complete lat-
tices.
     Key steps. (i) Completeness of V F ×T comes from taking joins/meets pointwise. (ii) Monotonic-
ity is inherited from the rule constructors by Lemma 34. (iii) Knaster–Tarski supplies existence of
lfp.
     Intuition. The lattice is the space of all possible temporal valuations; the operator is “one round
of reasoning.” A least fixpoint is the smallest valuation that survives another round unchanged: the
minimal stable story consistent with the rules.

Remark 1663. For later use, it is often convenient to recall the equivalent characterization of the
least fixpoint:                       ^
                           lfp(Φ) = {X ∈ V F ×T | Φ(X) ≤ X},
i.e. the meet of all pre-fixpoints. This emphasizes why the semantics is conservative: any valuation
                                                                                            L
that is stable (or over-approximates stability) must lie above lfp(Φ). Dually, gfp(Φ) =        {X |
X ≤ Φ(X)} exists as well, but the event-calculus reading typically privileges lfp as the “minimal
commitment” model.
     When implementing the iteration from bottom, one typically starts from the pointwise least ele-
ment ⊥ ∈ V F ×T (assigning ⊥ everywhere) and forms the chain ⊥ ≤ Φ(⊥) ≤ Φ2 (⊥) ≤ · · · . Mono-
tonicity ensures this is ascending, and any stage in the sequence provides an under-approximation
to lfp(Φ), which is useful when one wants progressively refined bounds on HoldsAt(f, t).

29.6    Time contexts, similarity, and regularity predicates
Lemma 37 (Basic properties of similarity and TemporalSimilarity). Let π : V → [0, 1] be monotone
and define simV (v, w) = 1 − |π(v) − π(w)| (Def. 68). Let simT be the average over fluents (Def.
68) and TemporalSimilarity be the threshold predicate (Def. 69). Then:

  1. simV (v, w) = simV (w, v) and 0 ≤ simV (v, w) ≤ 1, with simV (v, v) = 1.

  2. simT (t1 , t2 ) = simT (t2 , t1 ) and 0 ≤ simT (t1 , t2 ) ≤ 1, with simT (t, t) = 1.

  3. TemporalSimilarity is symmetric, and is reflexive whenever the threshold τ ≤ 1.

  4. If τ1 ≤ τ2 then TemporalSimilarityτ2 (t1 , t2 ) → TemporalSimilarityτ1 (t1 , t2 ).

Remark 1664. The map π : V → [0, 1] is a chosen projection from p-bit values to a single scalar—
for instance, one might take π(v) = v + to measure “support” alone, or something more nuanced.
Similarity simV (v, w) is then the simplest possible metric-like notion: values are similar when their
projected scalars are close. The time similarity simT averages this across all fluents, producing
a single number in [0, 1] that summarizes how alike two timepoints look in the given time context
(Def. 67).
    The lemma collects basic sanity properties: symmetry, boundedness, reflexivity, and monotonic-
ity in the threshold. These are not deep, but they are the kinds of properties one needs later when
building higher-level reasoning about regularity (Hyperseed-Concept ??) and when interpreting tem-
poral clustering or compression as abstraction.

                                                     631
Sketch. (1) Absolute value is symmetric and bounded; (2) averages preserve symmetry and bounds;
(3) follows from (1–2); (4) is threshold monotonicity.

Remark 1665. Proof sketch (strategy). Reduce everything to elementary properties of | · | and of
averaging.
    Key steps. (i) |π(v) − π(w)| = |π(w) − π(v)| gives symmetry. (ii) Since π(v) ∈ [0, 1], the
difference lies in [−1, 1], so 1 − | · | lies in [0, 1]. (iii) Averaging preserves inequalities and range.
(iv) Threshold predicates are monotone by definition.
    Intuition. Similarity is engineered to behave like a sane resemblance score; the lemma verifies
it does so.

Lemma 38 (Continuity gives a projection-difference bound). If a fluent f is continuous (Def. 70)
with parameter η ∈ (0, 1], then for any t1 , t2 ,

          T emporalSimilarity(t1 , t2 ) → |π(HoldsAt(f, t1 )) − π(HoldsAt(f, t2 ))| ≤ 1 − η.

Remark 1666. Here “continuity” is a regularity condition on a fluent: whenever two times are
deemed similar enough (TemporalSimilarity holds), the fluents value cannot change too much (after
projection by π). The lemma simply rewrites this in the more familiar form of an upper bound on
a difference.
    This matters because it turns a similarity-based condition into an inequality that can be composed
with other numerical reasoning. In effect, it lets one treat TemporalSimilarity as a kind of control
on variation, linking the qualitative predicate to quantitative bounds.

Sketch. Def. 70 gives simV (HoldsAt(f, t1 ), HoldsAt(f, t2 )) ≥ η. By Def. 68, simV = 1 − |π(·) −
π(·)|, so 1 − |∆| ≥ η, i.e. |∆| ≤ 1 − η.

Remark 1667. Proof sketch (strategy). Substitute the definition of simV and rearrange.
    Key step. The transformation from 1 − |∆| ≥ η to |∆| ≤ 1 − η is purely algebraic, but it is the
step that makes the condition operational.
    Intuition. “High similarity” means “small distance,” because similarity was defined as 1 −
distance.

Lemma 39 (Increasing and decreasing imply constancy). Fix (T, <) and projection π (Def. 72).
If f is both increasing and decreasing, then for all t1 < t2 ,

                               π(HoldsAt(f, t1 )) = π(HoldsAt(f, t2 )).

So π(HoldsAt(f, t)) is constant along each <-chain.

Remark 1668. This lemma is an order-theoretic truism with a useful interpretive punch: a quan-
tity that never goes down and never goes up is constant. Here the quantity is the projected fluent
value along the proto-time order.
    Its role is to show how qualitative monotonicity constraints collapse degrees of freedom. In a
system where fluents represent properties evolving through time, imposing both monotone directions
forces stasis (at least in π), which can be used either as a diagnostic (your constraints are too
strong) or as a characterization (the fluent is invariant).

Sketch. Increasing gives π(t1 ) ≤ π(t2 ), decreasing gives π(t1 ) ≥ π(t2 ); hence equality.




                                                   632