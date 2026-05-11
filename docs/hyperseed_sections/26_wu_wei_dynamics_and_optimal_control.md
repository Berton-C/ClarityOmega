# 26 Wu Wei dynamics and optimal control

The finite case adds a computational intuition: iterating F from a seed set is like repeatedly expand-
ing to the mutually predictive neighborhood until no new nodes appear. Visually, one is “growing”
a subgraph until it becomes closed under the relevant in- and out-neighborhood operators.
Remark 1386. In the finite case, the bound of |U| steps is a worst-case guarantee; in typical sparse
predictive graphs convergence can be much faster because each application of F only adds tokens
supported by the existing predictive structure. Conversely, if one begins from a large R0 , iteration
may also remove tokens depending on the exact definition of F (e.g. if F enforces mutuality rather
than one-way reachability), so the intuitive picture is not only “expansion” but “pruning toward
stability.” This clarifies why the fixed-point condition is aptly described as stabilization: it is the
point at which neither expansion nor pruning changes the set.
Remark 1387. The reference to Scott-continuity is not essential for the existence of fixed points
(which is already guaranteed by Knaster–Tarski) but becomes relevant if one wants the iterative
procedure to converge by taking countable limits rather than transfinite stages. In applications
where U is effectively enumerable and F has suitable continuity properties, this can justify practical
approximation schemes: compute F n (R0 ) for increasing n and interpret the limit (when it stabilizes)
as the induced reality-system.
Proof sketch. Show the ambient space 2U is a complete lattice. Verify F is monotone (Lemma 5).
Invoke Knaster–Tarski to obtain existence of lfp(F ) and gfp(F ) and completeness of the fixed-point
set. For finite U, use the fact that a strictly increasing chain of subsets cannot exceed length |U|,
so iteration stabilizes.                                                                           
Remark 1388. The sketch can be operationalized as follows: one chooses an explicit representa-
tion for U (tokens), an explicit rule for the predictive relation →θ at the chosen threshold, and then
defines F as the induced closure (or mutuality) operator. At that point, the abstract order-theoretic
argument guarantees that the resulting computation is not chasing a mirage: there really are stabi-
lized sets to be found, even if one later adds additional criteria for preferring one fixed point over
another.
Remark 1389 (“Stabilized pattern complex”). Interpreting →θ as a weighted directed graph, a
reality-system is a subgraph that is closed under taking one-step predictive in- and out-neighborhoods.
If we refine F to use multi-step reachability rather than one-step edges, fixed points coincide more
closely with unions of strongly connected components. Either way, the fixed-point condition captures
the intended circularity: reality is attributed to collections of entities that mutually support predictive
coherence.
Remark 1390. The phrase “pattern complex” is meant to stress that membership in R is not an
intrinsic label attached to a token in isolation, but a property of a configuration of tokens linked
by reliable predictive constraints. Graph-theoretically, the closure requirement ensures that once a
token is admitted, the local predictive dependencies that sustain it (incoming support) and that it
sustains (outgoing support) are also represented within the same subgraph, at least to the degree
enforced by F . This turns “being real relative to R” into a coherence notion: reality is the stable
core of a mutual-modeling relation rather than a primitive unary predicate.
Remark 1391. When F is strengthened from one-step to multi-step conditions, the strong connec-
tivity analogy helps explain why reality-systems tend to behave like “modules” of inference: within
a strongly connected predictive module, information can circulate and reinforce itself, supporting
robust counterfactual and temporal predictions. At the same time, the threshold θ controls whether
weak long-range links suffice to merge modules into larger fixed points or whether they remain
separate, yielding multiple coexisting stabilized pattern complexes inside the same U.

                                                   557
25.3    Physical reality and body as an interface-mediated reality-system
Hyperseed defines physical reality (relative to an embodied mind) as a reality-system containing the
body, with the additional property that the mind’s causal impact on that reality is mostly mediated
through the body-channel. We formalize this by adding a factorization condition on causal/process
morphisms.

Definition 420 (Embodied mind and body). Let M be a mind modeled as a dynamical subsystem
with internal states Mind, percept tokens Percepts, and action tokens Acts. A body for M is a
pattern-system B together with a distinguished interface map

                                       ι : (Percepts, Acts) −→ B                                     (9)

such that there is a highly significant mutual causal relationship between M and B. (In enriched
categorical terms: the coupling morphisms M ↔ B have large weight and are stable under refine-
ment.)

Remark 1392. The typing of ι encodes a simple but crucial idea: percepts and actions are not
free-floating; they are anchored in some structured subsystem B that mediates between inner and
outer. Here Mind, Percepts, and Acts are names for state/token sets internal to the model of M ; B
is a pattern-system (in the sense developed earlier, cf. [5]) that carries stable regularities over time.
The parenthetical enriched-categorical phrasing points to the earlier “weights” (weakness/residuals)
that quantify coupling strength (Hyperseed-Concept 202, 143; see [3, 2]).

Remark 1393. A concrete example is an animal body: Percepts may include retinotopic arrays and
proprioceptive signals, while Acts includes muscle activations. Then ι maps these tokens to bodily
subsystems (eyes, joints, muscles) whose dynamics couple to the environment. For a software
agent, B could be a robot platform, a server interface, or even a stable toolchain. The definition
is necessary because later notions of “physical reality” depend on which causal paths are privileged,
and those privileges are expressed by factorization through B.

Definition 421 (Physical reality). A physical reality for an embodied mind M is a reality-system
R such that:

(a) the body B is largely contained in R (i.e. B ⊆ R as a pattern-subsystem);

(b) most percepts and actions of M are perceptions/actions of entities in R;

(c) body-channel mediation: for any action-effect morphism f : M → R there exist morphisms
    g : M → B and h : B → R with
                                         f ≈ h ◦ g,                                    (10)
     where “≈” denotes approximation in the enrichment (e.g. bounded residual weakness or
     bounded prediction-error increase when replacing f by h ◦ g).

Remark 1394. Clause (c) is the formal core: the mind’s effective influence on R must (up to
controlled error) factor through the body. In symbols, f : M → R is any causal/process morphism
capturing an action-to-effect link; then g : M → B is the “issue a bodily action” component, and
h : B → R is the downstream physical influence of the body on the larger reality-system. The
approximation relation ≈ is where the enrichment matters: one may measure the deviation between
f and h ◦ g by weakness residuals, by increased prediction loss, or by any compatible metric-like
structure supplied by the formal core.

                                                  558
Remark 1395. An example: if M is you, B includes your vocal tract and hands, and R includes
your room, then speaking to move air molecules and thereby alter another person’s beliefs is still
mediated through B. By contrast, if one posits a mind that can directly alter far-away objects
without any intervening bodily channel, then (in this framework) its “physicalness” relative to that
R would be lower. This provides a mathematically expressible sense in which “physical reality and
body” (Hyperseed-Concept 135) are intertwined.

Remark 1396 (Degree of “physicalness”). One can define a graded physicalness score by measuring
how well action-effect morphisms factor through B. For example, if the enrichment provides a
distance d, define                                                
                          phys(M, R; B) := 1 − sup inf d f, h ◦ g .                        (11)
                                                  f :M →R g,h

If M can significantly impact R without using the body-channel, this score decreases.

Remark 1397 (Laws of physics). Within this ontology, the “laws of physics” relative to a physical
reality R are simply a system of effective hypotheses (models) for predicting and explaining what
happens in R. Formally, this can be cast as selecting a model class HR that minimizes predic-
tion error subject to simplicity/weakness constraints (a Minimum Description Length or weakness-
regularized choice).

Remark 1398. The last parenthetical points to a convergence of ideas: Minimum Description
Length is a way of expressing that models should be predictive yet parsimonious, often formalized
using description lengths related to algorithmic information [16]. Hyperseed’s weakness-regularized
variants reinterpret this parsimony as a representational/effort constraint (Hyperseed-Concept 82,
202), anticipating the Wu Wei control formalism developed later [21].

25.4    Algebraically asymmetric physical reality
Hyperseed stresses an algebraic asymmetry between physical reality (often low-dimensional and
“vector-space-like”) and mental/intersubjective realities (typically weaker, more topological, and
only approximately projectable into low-dimensional coordinates). We can express this without
committing to a particular physical theory by treating “algebraic structure” as additional opera-
tions/axioms on the state space. In particular, the asymmetry is not meant to assert that mental
reality is “vague” in every respect, but that the kinds of structure that make physical systems rigid
(e.g. smoothness, metrics, conservation laws, differential constraints, compatibility conditions) are
not, in general, fully present in intersubjective representations. Thus “algebraic weakness” here is
a statement about recoverability of structure: the mental/intersubjective level typically underde-
termines many physically distinct realizations.

Definition 422 (Structure strength and forgetful maps). Let Rphys be a category (or enriched
category) of models of physical reality, whose objects carry some strong algebraic structure (e.g.
smooth manifold, metric space, vector bundle, etc.). Let Rment be a category of models of mental
and intersubjective reality (e.g. topological or relational pattern spaces). An algebraic asymmetry
is the presence of a structure-forgetting functor

                                        U : Rphys −→ Rment                                      (12)

that is not (even approximately) invertible on the images relevant to a given community of minds.
In this case we say that mental reality is algebraically weaker than physical reality.



                                                559
Remark 1399. The phrase “category (or enriched category)” allows one to treat morphisms as
carrying graded costs, probabilities, or fidelities when needed. For example, in an enriched setting
one can measure how well a mental representation matches an underlying physical state, rather
than treating representation as all-or-nothing. This is useful for articulating the “approximately
projectable” clause: minds may track some physical degrees of freedom with high fidelity while
collapsing or ignoring others.
Remark 1400. The functor U is called “forgetful” because it discards structure: it takes an ob-
ject with rich operations/axioms (say, a differentiable manifold with metric) and remembers only
whatever mental/intersubjective representation retains (say, adjacency relations, coarse regions, or
pattern links). The non-invertibility condition encodes the asymmetry: from the weaker description
alone one generally cannot reconstruct the full physical structure. This is the categorical way to
articulate the Hyperseed-Concept 55.
Remark 1401. One can make the non-invertibility intuition more concrete by considering the
fibers of U . For an object m ∈ Ob(Rment ), the preimage (informally) U −1 (m) consists of all
physically structured objects that “look like” m under the forgetting process. Algebraic asymmetry
asserts that these fibers are typically large: many distinct physical configurations collapse to the
same mental/intersubjective pattern. The inability to choose a canonical element of the fiber (even
approximately, for the relevant class of observers) is exactly the sense in which U fails to be invertible
where it matters.
Remark 1402. A simple example is the ordinary map/territory gap: the same topological graph of
“places connected by roads” can be embedded in many different geometries with different distances
and curvatures. If mental reality records mostly graph-like relations, then lifting it to a physical
geometry requires extra choices. This is useful because it explains, without mysticism, why physical
reality feels “hard” or “constraining”: the constraint is precisely the missing information needed to
select one physical refinement among many mental descriptions that collapse under U .
Remark 1403. The same pattern appears in familiar mathematical forgetful functors. For in-
stance, forgetting a metric yields a topological space; forgetting a topology yields a set; forgetting
a smooth structure yields a topological manifold; forgetting phase information yields an intensity
pattern. In each case, the weaker object retains certain invariants (e.g. continuity properties, adja-
cency relations, cardinality, qualitative connectivity), but it does not determine the stronger object
without additional data. The point of stating this categorically is that one can swap in different
notions of “physical” and “mental” models while keeping the same asymmetry schema.
Remark 1404 (Why asymmetry “feels like constraint”). If U discards operations/constraints
present in physical reality, then many distinct physical states become indistinguishable in the weaker
mental description. From the mind’s perspective, trying to realize a mentally-specified pattern phys-
ically requires choosing (or discovering) additional structure to lift it back into Rphys . This lifting
typically incurs effort and may be impossible, producing the phenomenology that physical reality
“constrains” mind.
Remark 1405. The “may be impossible” clause has two distinct readings that can coexist. First,
there may be no object in Rphys that maps (even approximately) to the desired m under U , meaning
the mental pattern is not physically instantiable in that reality-system. Second, there may be many
such objects, but the agent may lack access to the additional structure needed to select and stabilize
one. In either case, the mental specification underdetermines the physical implementation, and
that underdetermination shows up phenomenologically as friction, failed attempts, or the need for
iterative refinement.

                                                   560
Proposition 41 (Free lift as a source of effort). Suppose U has a left adjoint F (a “free” structure-
adding functor), so F a U . Then any mental description m ∈ Ob(Rment ) has a canonical lift F (m)
into physical-structured form. If a mind’s goal pattern is specified in Rment , then realizing it physi-
cally requires at least the “free” lift plus additional constraint satisfaction (selecting a morphism out
of F (m) compatible with the actual physical reality-system). This separates conceptual feasibility
from physical realizability.
Remark 1406. Intuitively, an adjunction F a U formalizes the idea of “adding structure in the
cheapest possible way.” The proposition says that even the cheapest lift F (m) already introduces
commitments not present in m, and that making the lifted structure actually occur in a given
physical reality-system is an additional step. This is important because it lets us speak rigorously
about effort: effort is not only about searching a space of possibilities, but about bridging a categorical
gap between levels of structure.
Remark 1407. The word “free” should be read in the technical sense, not as implying physical ease.
In many settings, F (m) is a large object: it can represent the space of all minimally constrained
implementations of m consistent with the algebraic axioms of Rphys . As a result, the agent’s labor
is not removed by having F ; rather, the adjunction clarifies what kind of labor is required: selecting,
constraining, and stabilizing a specific physical realization within the degrees of freedom left open
by F (m).
Proof. An adjunction F a U provides, for each m, a unit map ηm : m → U (F (m)) that is universal
among maps from m into U -images. Thus F (m) is the least additional structure needed to represent
m in the physical category. Any further realization must factor through F (m) and so must satisfy
additional physical constraints not present in the mental description.

Remark 1408. The key step is the universality of the unit ηm . It ensures that every attempt to
interpret the mental description m as something physically structured must pass through F (m), so
the free lift acts as a bottleneck: it is the common interface between the weak and strong worlds.
Geometrically, one may picture F (m) as the “bundle of all minimal physical implementations” of a
mental specification, and “physical realizability” as the further act of selecting a section compatible
with the actual physics. The proof works because adjunctions are precisely the machinery that
captures “best approximation” across categories.
Remark 1409. There is also a useful dynamical reading. The composite T := U ◦ F is a monad
on Rment , meaning it is an endofunctor that takes a mental description and returns its “freely
physically-coherent” enrichment as seen back in the mental category. In this language, iterating T
can be interpreted as repeatedly applying a coherence-imposing closure: the agent refines a pattern
until it becomes stable under the constraints implicitly imported from Rphys . This does not add
a new assumption beyond F a U ; it only spells out a standard categorical consequence that often
matches how agents learn to respect physical constraints through repeated feedback.
Proof sketch. Use the unit ηm : m → U (F (m)) provided by F a U . By the adjunction’s universal
property, any map from m into an underlying physical object factors uniquely through ηm , showing
that F (m) is the canonical minimal-structure lift. Realizing m physically then necessarily involves
(at least) choosing and satisfying additional constraints beyond those encoded in m.              

25.5    Signals and observer-indexed universes
Hyperseed defines a “universe” relative to a system and a signal class. Intuitively: what counts
as “in the universe” depends on what kinds of signal exchanges the system believes are possible.

                                                   561
This usage is intentionally operational: it tracks what is reachable for interaction (in the sense of
potential bidirectional coordination, observation, or control), rather than what is “out there” in a
mind-independent inventory.
Definition 423 (Signals and signal classes). Let S be a category (or enriched category) whose
objects are systems/entities. A signal from A to B is a pair of patterns (ptx , prx ) (transmission,
receipt) together with a causal interpretation that the transmission pattern is causal for the receipt
pattern. A signal class C is a specified family of signals (morphisms) in S. Because these are
observer-indexed, we allow a mind M to assign a p-bit evidence value EM (s) ∈ [0, 1]2 to the
proposition “signal s is usable.”
Remark 1410. The category S supplies the ambient “systems and interactions” universe in which
we talk about signaling. A signal s : A → B is not merely a physical disturbance; it is a disturbance
together with an interpretation that it transmits information in a usable way. The pair (ptx , prx )
emphasizes that the same underlying process may be encoded one way at the transmitter and decoded
another way at the receiver; this matches the earlier emphasis that “pattern” is observer-relative
[5]. Allowing EM (s) ∈ [0, 1]2 makes the epistemic status of “usability” paraconsistent: a mind can
have simultaneous evidence for and against the usability of a purported channel [23, 24].
Remark 1411. It is helpful to separate three layers that are bundled in ordinary language: (i) a dy-
namical coupling in the substrate (some causal influence from A toward B), (ii) a coding/decoding
convention that makes that coupling function as information transfer, and (iii) a pragmatic con-
straint that the transfer is reliable enough (or controllable enough) to count as usable for the mind’s
current purposes. The definition of “signal” packages (i) and (ii) into a morphism-like object,
while the evidence value EM (s) records (iii) in a way that can accommodate ambiguity, adversarial
environments, deception, and internal uncertainty.
Remark 1412. When S is taken as an enriched category, the enrichment can encode graded
notions of interaction (e.g. costs, capacities, fidelities, probabilities, or resource bounds). In that
case, “a specified family of signals” may mean “morphisms satisfying a constraint in the enriching
structure” (for example, only channels above a minimum capacity, or only interactions within a
given energy budget). The present development does not require fixing an enrichment, but it is
useful to keep in mind that many physically relevant restrictions on communication are naturally
expressed in enriched-categorical terms.
Remark 1413. Example: in an embodied physical cosmos, C might be electromagnetic signals
detectable by the body’s sensors (light, radio) or mechanical signals (sound, touch). In a so-
cial/intersubjective cosmos, C might include linguistic utterances and symbolic artifacts. The defi-
nition is useful because it makes “what exists for me” depend on the reachability structure induced by
which signals are taken seriously, which is exactly the sort of observer-relativity Hyperseed intends.
Remark 1414. The same underlying interaction may fall into different signal classes depending
on the mind’s model. For instance, the same acoustic wave can be treated as “noise” (excluded
from C), as a generic mechanical disturbance (included in a broad C), or as a linguistic utter-
ance with semantic content (included in a narrower but more structured C that presupposes shared
conventions). In this way, choosing C captures not only physical modality but also interpretive
commitment.
Definition 424 (Observable universe relative to a signal class). Fix a system S (typically including
a mind and its current reality-system model) and a signal class C. For a threshold η ∈ (0, 1), define
the observable universe of S relative to C as
                                                                                +
           UnivC,η (S) := {X ∈ Ob(S) : ∃ a finite C-signal path S       X with EM ≥ η}.           (13)

                                                 562
In words: X is in the universe if S believes it can (now or eventually) send/receive a C-class signal
to/from X.
Remark 1415. Here Ob(S) denotes the objects of the category S. The notation S         X indicates
                                                                                           +
a finite composable chain of signals in the class C from S to X. The condition “with EM       ≥ η”
means that along the relevant path(s), the mind’s positive evidence component for usability exceeds
the chosen threshold. (One may similarly incorporate negative evidence, for instance by requiring
high positive and low negative evidence, but the present definition keeps the reachability notion
uncluttered.)
                                                       +       −                        +
Remark 1416. Concretely, if EM (s) = (EM                 (s), EM (s)) ∈ [0, 1]2 , then EM  refers to the first
coordinate, interpreted as evidence-for-usability. The definition leaves implicit how evidence is
aggregated across a multi-step path; the intended minimal reading is existential: there exists at least
one finite path s1 , . . . , sn of C-signals for which each step is usable to degree ≥ η (or, more generally,
for which the mind judges the path as a whole to clear the threshold under its preferred aggregation
rule). This keeps the reachability predicate flexible enough to model different epistemic policies (e.g.
                                              +
“weakest-link” aggregation via mini EM          (si ) versus Bayesian-like compounding), without changing
the surrounding categorical picture.
Remark 1417. The phrase “now or eventually” is meant to include mediated reachability: S may
not directly signal to X, but may be able to do so via relays, intermediaries, or composed protocols.
The use of a finite path matches the operational idea that interaction proceeds through finitely many
steps that the mind can in principle represent as a procedure, even if the intermediate systems are
not themselves salient in ordinary description.
Remark 1418. As an example, if C is “radio transmission” and S is an Earth-based civiliza-
tion, then UnivC,η (S) includes objects that are radio-reachable in principle (satellites, nearby space-
craft), but excludes galaxies beyond any plausible ability to send/receive radio signals at the required
strength. Changing C changes the universe: if C expands to include hypothetical faster-than-light
signals, the universe expands accordingly. This formalizes Hyperseed’s distinction between cos-
mos/universe talk and absolute ontology (Hyperseed-Concept 89).
Remark 1419. The threshold η plays a normative role: it encodes how demanding the system
is about what counts as a usable channel. A cautious scientific instrument may require a high η
(only high-confidence channels are admitted), whereas an exploratory or imaginative cognition may
use a lower η (allowing tenuous, speculative, or weakly supported channels to count as potential
links). Thus UnivC,η (S) is sensitive not only to physics and infrastructure, but also to epistemic
temperament and context.
Proposition 42 (Monotonicity in signal class). If C ⊆ C 0 then UnivC,η (S) ⊆ UnivC 0 ,η (S).
Remark 1420. This proposition states the obvious but important structural fact: allowing more
kinds of signals cannot reduce what you can reach. It mirrors Lemma 5 at a different level: both
are monotonicity principles ensuring that subsequent closure/fixed-point constructions behave well.
Proof. Any C-signal path is also a C 0 -signal path. Thus reachability using C implies reachability
using C 0 .

Remark 1421. The proof is immediate because the definition of universe membership is existential:
it suffices that there exists a path of allowed signals. Enlarging the allowed set preserves existing
paths. Visually, if one adds more edge-types to a graph, the set of vertices reachable from a fixed
start vertex can only increase.

                                                     563
Remark 1422. Operationally, this monotonicity is a sanity check for model revision: if a mind
updates its reality-system model by admitting a previously disallowed channel type into C (e.g. it
learns a new protocol, discovers a new sensor modality, or accepts testimony it previously dis-
counted), then previously reachable entities remain reachable, while additional entities may become
reachable. This aligns the formalism with ordinary learning dynamics.

Proof sketch. Universe membership is witnessed by a finite path using signals in C. If C ⊆ C 0 , the
same path is valid in C 0 , so reachability (and hence membership) is preserved.                  

Proposition 43 (Monotonicity in threshold). If η ≤ η 0 then UnivC,η0 (S) ⊆ UnivC,η (S).

Proof. If X ∈ UnivC,η0 (S) then there exists a finite C-signal path S       X whose positive evidence
           +                                                       +
satisfies EM ≥ η 0 . Since η ≤ η 0 , the same path also satisfies EM ≥ η, hence X ∈ UnivC,η (S).

Remark 1423. This captures the dual way in which the “observer-indexed universe” can grow:
either by broadening C (new modalities of interaction) or by lowering η (relaxing standards of
usability). Conversely, a stricter evidential policy (raising η) can shrink the operational universe
even if the underlying substrate and signal class remain unchanged.

Remark 1424 (Cosmos vs universe). We use cosmos informally for a privileged or stabilized
universe notion, often induced by a canonical signal class (e.g. “physical” signals mediated through
the body-channel for embodied minds). Different minds or different coupling regimes may induce
different cosmos notions.

Remark 1425. In this terminology, a “cosmos” is typically what remains after a process of con-
vergence: shared measurement conventions, stable instrumentation, and negotiated intersubjective
standards produce a relatively fixed C and an implicit threshold policy η. By contrast, “universe”
here is deliberately parameterized, so that shifts in embodiment, interface, language-game, or trust
policy are represented as explicit parameter changes rather than as contradictions about what exists.

25.6    Multiverse and guidable multiverse
In Hyperseed, a multiverse is not introduced as a purely metaphysical postulate. Rather, it is
an observer-relative construct: a multiverse is a class of possible universes such that (from the
observer’s perspective) stochastic events determine which universe the observer will inhabit after
the event. In this sense, “universe” should be read as a structured world-hypothesis or world-
state at the level of description available to the observer’s modeling interface, rather than as a
commitment to a specific cosmological ontology. The same underlying reality-system may admit
many such universe-descriptions depending on which signal classes are available and which variables
the observer can stably track.

Definition 425 (Stochastic events relative to an observer). Fix an observer O. An event e is
stochastic relative to O if O cannot predict its outcome. An event class is stochastic relative to O
if O cannot predict the outcome of any particular event in the class, but can predict some features
of the outcome distribution over many instances.

Remark 1426. This definition is epistemic rather than metaphysical: “stochastic” means “un-
predictable to the observer,” not “uncaused.” One may read this in a Peircean spirit: chance is
a name for a limit of habit, a region where regularities have not yet been formed or recognized
(cf. the emphasis on habit and Thirdness in [14]). In Hyperseed’s operational language, the mind
lacks a model that reduces prediction error for the outcomes of e. A practical consequence is that

                                                564
“stochastic” depends on the observer’s representational capacity, data access, and computational
limits; it can therefore change when the observer learns, upgrades instrumentation, or acquires a
new signal class.

Remark 1427. Example: a fair coin flip is stochastic relative to a typical human observer. But
the same physical process may be non-stochastic relative to an idealized observer with complete
microstate information and unlimited computation (if one adopts a deterministic underlying model).
The definition is useful because it lets multiverse talk arise naturally from limits of prediction
and control, rather than requiring an ontological proclamation that “all possibilities exist.” More
generally, what matters is not whether the microphysics is deterministic, but whether the observer
can compress the relevant causal details into a predictive habit at the scale of interaction; when the
required compression is unavailable, the observer is forced into a distributional (rather than point)
forecast.

Definition 426 (Multiverse (controlled Markov form)). Fix an observer O and a base universe U0
(itself observer- and signal-class-indexed). A multiverse associated with (U0 , O) is:

(a) a set (or measurable space) U of candidate universes consistent with O’s model class;

(b) a transition kernel P (· | U, e) giving a distribution over next universes after a stochastic event
    e occurring while in universe U .

Thus, the observer’s universe evolves as a stochastic process on U.

Remark 1428. The kernel P (· | U, e) is a Markov-style update rule on the space of universes: given
that the observer is currently in universe U and event e occurs, the observer assigns a distribution
over which universe comes next. The measurable-space option is included because U may be infinite
or continuous in realistic modeling. The point is not that universes are literally “jumped between”
in a physical sense, but that the observer’s self-location among competing world-hypotheses changes
stochastically as unpredictable events unfold. This formalizes Hyperseed-Concept 116 in a way
compatible with decision/control extensions. One can also read U as an information-state (e.g., a
hypothesis index, a parameter setting, or a latent regime label), in which case P (· | U, e) expresses
how surprises and updates move the observer among regimes.

Remark 1429. A simple example is Bayesian model selection over a hypothesis class of “which un-
derlying dynamics governs my environment.” After a surprising observation, probability mass shifts
among hypotheses, which can be read as transitioning among “universes” in U. The definition is
useful because it makes multiverse structure available wherever there is irreducible uncertainty and
competing world-models, including mundane settings like partial observability and nonstationarity.
In this Bayesian reading, the “state” of the multiverse can equivalently be taken as a belief distribu-
tion over U; the present definition instead treats the realized (self-located) universe as the stochastic
variable and keeps the belief implicit in O’s kernel assignment. Both viewpoints are compatible: the
former emphasizes inference dynamics, while the latter emphasizes experienced branch-selection.

Remark 1430. The “event” label e may be instantiated at different granularities. At one extreme,
e can be a single measurement or observation; at the other, e can stand for an extended episode
whose internal microstructure is not modeled by O. The Markov form should then be read as a
modeling commitment that whatever details of the past matter for predicting the next universe are
encoded in the current U (as represented by O), which is exactly the usual sufficiency intuition
behind state variables in stochastic process modeling.


                                                  565
Definition 427 (Guidable multiverse). Let S1 and S2 be two signal classes and let O be an observer.
A guidable multiverse (relative to S1 , S2 , O) is a multiverse U defined using S1 -reachability such
that, in universe U as modeled by O, signals in class S2 can systematically influence which element
of U the observer will be in after a transition. Formally, this means there is an action set A
(implementing S2 signals) and a controlled transition kernel

                                              P (· | U, a)                                        (14)

on U.

Remark 1431. The only new ingredient is control: a ∈ A indexes interventions available to the
observer (or to an agent coupled to the observer) and the kernel P (· | U, a) replaces the purely
event-driven kernel. This is the same structural move that turns an uncontrolled Markov chain
into a Markov decision process. The definition is useful because it makes room for the Hyperseed
idea that broader or subtler signal classes could enlarge not only what is reachable, but what is
steerable. In particular, if S2 is weak or noisy, then distinct actions may induce nearly identical
kernels P (· | U, a), making the multiverse effectively unguidable at the level of U even if many
universes are in principle possible.

Remark 1432. Example: in ordinary life, S1 might be “sensory signals that define my everyday
physical universe,” while S2 might be “actions I can take using tools and institutions.” Then P (· |
U, a) encodes how my choices alter which future regimes (“universes” in the hypothesis/experience
space) become actual for me. This connects to Hyperseed’s general emphasis on action as selec-
tion among futures, later formalized variationally in Wu Wei dynamics [21]. In a more explicitly
                              R can introduce a policy π(a | U ) and consider the induced (uncon-
decision-theoretic register, one
trolled) kernel Pπ (· | U ) = A P (· | U, a) π(da | U ), which makes clear that guidance is realized
through a choice rule that couples the observer’s current universe-description to action selection.

Remark 1433 (Interpretation). A guidable multiverse is simply a multiverse equipped with con-
trollable degrees of freedom. In conventional physical modeling, “guidance” is limited by the causal
structure of the physical reality-system. Hyperseed allows (as a conceptual possibility) that broader
signal classes may exist, which would make the multiverse “more guidable” relative to a mind. One
concrete way to interpret “more guidable” (still at the level of modeling, not metaphysics) is that
different actions a induce more distinguishable outcome distributions over U (e.g., larger separations
between P (· | U, a) across a), thereby increasing the set of achievable transitions and decreasing the
entropy of the next-universe distribution under well-chosen interventions.

Remark 1434. The guidable multiverse definition deliberately remains neutral about whether the
observer has direct access to U (full observability) or only to signals generated by U (partial ob-
servability). In the latter case, U may be treated as latent and the effective control problem lives on
a belief state over U, but the intuitive claim remains: certain signal classes (S2 ) can act as han-
dles that reshape which world-hypothesis becomes experientially realized next. This preserves the
Hyperseed motif that expansion of signal classes is simultaneously an expansion of both epistemic
discrimination and practical steering capacity.

25.7    The Yverse as a recursive limit of multiverse towers
Hyperseed introduces the Yverse as the limit of iterating the “multi” construction:

                       universe → multiverse → multimultiverse → · · ·


                                                 566
In this view, signals that appear random at one level may become predictable at a higher level, and
in the limit a signal may be paraconsistently both random and predictable. The name “Yverse”
references the Y-combinator from combinatory logic, which makes its argument recursive. One
can read the informal “→ · · · ” not merely as an unending sequence, but as a prompt to replace
indefinite iteration with a stabilization principle: rather than asking for the tower at stage n, one
asks for a description that is already closed under the “make it multi” operation. This is the
sense in which the Yverse is a recursive limit: it is characterized by an equation rather than by an
external indexing set of stages.
Remark 1435. The “random vs. predictable” slogan can be understood in a coarse-graining sense:
at a given level of description, a signal may be effectively unpredictable because relevant hidden
variables are not represented. A higher-level description may add latent structure (e.g. by turning
a single-world description into a distribution over refinements), making the same signal condi-
tionally predictable relative to the expanded information state. In the limit, if the description is
self-referentially closed under such expansions, it becomes coherent (in a paraconsistent sense) to
treat the signal as both “random” (under a projection or forgetting map back down to a lower level)
and “predictable” (under the enriched viewpoint that retains the higher-order structure).
Definition 428 (Abstract multi-operator). Let D be a complete lattice of “world-descriptions”
(these may encode universes, multiverses, and higher-level constructions). A multi-operator is a
monotone map
                                         Multi : D → D                                      (15)
that sends a description to the corresponding “multi” description.
Remark 1436. The lattice D is an abstract container for levels of description: an element might
be a single universe model, a probability distribution over universe models, a distribution over
such distributions, and so on. The order structure (making D a complete lattice) is what permits
fixed-point reasoning: it provides suprema/infima needed by general theorems. Monotonicity of
Multi means that refining a description cannot yield a strictly coarser multi-level description; it
is the analog, at the “tower of worlds” level, of the earlier monotonicity lemmas. It is often
helpful to read the order ≤ on D epistemically: d1 ≤ d2 may mean “d2 contains at least as much
information/constraint as d1 ,” or “d2 is at least as strong a theory as d1 .” Under such readings,
monotonicity of Multi expresses the idea that adding constraints at the base level should not reduce
the constraints (or information) available after passing to the multi-level wrapper.
Remark 1437. A concrete mental picture is to let D be a powerset lattice of admissible meta-
descriptions, or a lattice of theories ordered by entailment/strength. Then Multi wraps a descrip-
tion into a “distribution over refinements” object. The definition is useful because it isolates the
recursion in a single operator, making the Yverse a fixed point rather than an indefinitely postponed
iteration. Another concrete picture (compatible with the same formalism) is to treat elements of
D as state spaces with semantics: a description might specify both (i) a space of possible world-
histories and (ii) an interpretation map telling us which signals are observable. Then Multi can
be understood as lifting a description to a meta-space in which the previous space appears as one
component among many alternatives, together with a weighting or selection mechanism. The for-
mal abstraction deliberately does not commit to whether this lifting is probabilistic, possibilistic, or
logical; it only commits to the order-theoretic property needed for fixed-point existence.
Definition 429 (Yverse as a fixed point). A Yverse is a fixed point Y ∈ D of Multi:

                                            Y = Multi(Y ).                                         (16)

                                                  567
When multiple fixed points exist, one may select Y := lfp(Multi) (the least fixed point) or Y :=
gfp(Multi) (the greatest fixed point) depending on the intended semantics.
Remark 1438. The equation Y = Multi(Y ) is the formal signature of self-reference: the Yverse is
a world-description that, when “multiversed,” yields itself. Philosophically, this is the point where
classical insistence on well-founded constructions begins to strain: the object is defined by its own
image. Hyperseed treats this not as a defect but as a clue that paraconsistent and/or non-well-
founded semantics may be appropriate when discussing ultimate “wider world” notions (Hyperseed-
Concept 209). In analogy with the Y-combinator, the role of Multi is that of a functional F for
which one seeks a fixed point satisfying Y = F (Y ). The combinatory-logic analogy is not meant to
collapse set-theoretic and computational fixed points, but to highlight a shared structural theme: self-
application is not an anomaly to be eliminated, but a generative mechanism that produces objects
characterized by closure or invariance under a transformation.
Remark 1439. One may think of lfp(Multi) as the most conservative fixed point: the smallest
self-consistent Yverse description compatible with the multi-operator. Conversely, the greatest fixed
point can be read as the most expansive closure under “multi.” The availability of both mirrors
familiar least/greatest fixed point choices in semantics (induction vs. coinduction), which in turn
mirrors Hyperseed’s willingness to keep multiple, potentially tensioned, but useful perspectives in
play. In semantic terms, least fixed points are typically associated with “generated” structures (what
must be true if one starts from nothing and repeatedly closes under the operator), whereas greatest
fixed points are associated with “allowed” structures (what can be true if one permits any consistent
completion that remains closed under the operator). Under a “tower of worlds” interpretation,
these correspond to two different attitudes: building up the multi-tower from a minimal base ver-
sus admitting any sufficiently rich background and requiring only that it be stable under further
multiversing.
Remark 1440. When D has a least element ⊥ and greatest element > (as every complete lattice
does), one may form the ascending chain

                                 ⊥ ≤ Multi(⊥) ≤ Multi2 (⊥) ≤ · · ·                                 (17)

and the descending chain
                                > ≥ Multi(>) ≥ Multi2 (>) ≥ · · · ,                                (18)
            n
where Multi denotes n-fold iteration. In many familiar settings these chains stabilize at lfp(Multi)
and gfp(Multi) respectively; in full generality, one can require transfinite iteration and take suprema/infima
at limit ordinals. This makes precise the earlier informal idea of “iterating the multi construction
and taking a limit,” with the lattice operations providing the needed notion of limit.
Proposition 44 (Existence of Yverse fixed points). If Multi is monotone on a complete lattice D,
then fixed points exist and the set of fixed points forms a complete lattice.
Remark 1441. This proposition says that the Yverse is not a merely aspirational infinity: under
the same minimal hypotheses used earlier (complete lattice + monotone operator), fixed points exist
by purely mathematical necessity. In the narrative of the paper, this repeats the structural motif of
Section 25.2: wherever Hyperseed defines something by a stabilization condition, it also provides
the monotonicity needed to guarantee existence. This is a recurring theme in the broader Hyperseed
program [1]. A further useful consequence (often taken as part of the Knaster–Tarski package) is
that least and greatest fixed points admit order-theoretic characterizations:
                    ^                                             _
      lfp(Multi) =    {d ∈ D : Multi(d) ≤ d},      gfp(Multi) =      {d ∈ D : d ≤ Multi(d)}.    (19)

                                                  568
Here the meet ranges over pre-fixed points and the join ranges over post-fixed points. This connects
the fixed-point selection question to a semantics question: choosing the least fixed point amounts to
intersecting all descriptions that are “closed downward” under multiversing, whereas choosing the
greatest fixed point amounts to uniting all descriptions that can be extended in a way preserved by
multiversing.

Proof. This is again Knaster–Tarski.

Remark 1442. The proof deliberately does not add detail because it is identical in structure to
Theorem 23: Knaster–Tarski applies to any monotone operator on a complete lattice. The visual
intuition is again closure under iteration, except that the objects being iterated are now themselves
“world towers.” One may imagine repeatedly applying Multi and taking a limit in the lattice order;
fixed points are precisely where the process stabilizes. It is also worth noting what is not assumed:
no continuity, no contractiveness, and no metric or topological structure is required. The cost of
this generality is that the fixed point need not be reached in finitely many steps or even in countably
many steps by naive iteration; the benefit is that the existence of a stabilized “recursive limit” does
not depend on a particular implementation of multiversing, only on its monotone behavior with
respect to refinement/strength.

Proof sketch. Invoke Knaster–Tarski on the complete lattice D and the monotone endomap Multi.
Conclude existence of least and greatest fixed points and completeness of the fixed-point set. 

Remark 1443 (Why paraconsistent logic helps). If the “multi” tower diverges or leads to self-
referential definitions, classical well-founded reasoning may fail. Paraconsistent logic and non-
well-founded set-like constructions (used elsewhere in Hyperseed to model self-reference) provide
principled semantics in which such recursive limits can be discussed without trivialization [23, 24].
Concretely, if one tries to force a strict stratification in which level n+1 must be built only from
level n, then the equation Y = Multi(Y ) appears illicit, because the right-hand side mentions Y
“from above.” Paraconsistent and non-well-founded approaches relax the demand that definitions be
grounded in a well-founded hierarchy, allowing circularity while controlling explosion (the principle
that from a contradiction everything follows). This aligns with the intended reading of the Yverse
as a stable closure of the multiverse-building act itself, rather than as a final object obtained only
after completing an impossible traversal of all stages.

25.8    Eurycosm and near eurycosm
Hyperseed’s eurycosm (“wider world”) is the scope of distinctions, entities, and experiences beyond
any single well-defined mind or physical universe. The intent is to capture, in one term, the idea
that what is “out there” may not be exhausted by any one internally coherent physics, ontology,
or observer-interface; different observers and different admissible channels of interaction can carve
the wider world into different operational “worlds” that may partially overlap, partially disagree,
or be mutually incommensurable. The near eurycosm relative to a given mind is the portion of the
eurycosm that the mind can at least partially comprehend. In particular, “comprehend” here does
not require full simulation or perfect prediction; it can mean any stable representational handle,
such as a compressive model, a useful analogy, or a reliable decision-relevant summary. Universe,
multiverse, and Yverse are then different ways of conceptualizing aspects of the eurycosm. One can
think of these as different lenses: “universe” emphasizes a single consistent context, “multiverse”
emphasizes families of related contexts, and “Yverse” emphasizes structures that remain meaningful
across diverse contexts (e.g. cross-context invariants and correspondences).


                                                 569
Definition 430 (Eurycosm). Let Mind be a class of minds/observers and let SigClass be a class
of signal classes. The eurycosm is the (typically large) union of observer-indexed universes across
signal classes:                         [         [
                              Eury :=                    UnivC,η (M ).                         (20)
                                       M ∈Mind C∈SigClass

Here UnivC,η (M ) should be understood as the “universe” induced for observer M when M treats
signals of class C as admissible and reliable up to the tolerance parameter η (e.g. a coarse-graining
or error bar that determines which distinctions count as stable). This makes the union sensitive not
only to what channels are allowed but also to how finely the mind is able or willing to discriminate
structure within those channels. This definition is schematic; formally one may treat Eury as a
large category of contexts with morphisms given by admissible signals and cross-context pattern
correspondences. In that categorical picture, objects are contexts (observer-relative worlds), and
morphisms represent structured ways of carrying information, models, or identifications from one
context to another without insisting on literal identity of ontology.

Remark 1444. The formula for Eury should be read with a logician’s caution: it is not claiming
that all such unions form a small set. Rather, it expresses an organizing principle: the wider world
is what you get when you range over minds and over the classes of signals they treat as real. The
suggestion that Eury may be treated as a large category emphasizes that relations between contexts
(translations, analogies, correspondences of patterns) matter at least as much as the contexts them-
selves. This aligns with the euryphysics framing [18]. Concretely, depending on ones foundational
stance, Eury may be a proper class, or it may be internalized by working inside a Grothendieck
universe or a type-theoretic hierarchy; the mathematical bookkeeping is secondary to the intended
invariant: do not privilege one observer-context as the unique container of reality. The categor-
ical emphasis also helps separate two kinds of questions: questions about the internal laws of a
context (object-level structure) and questions about how patterns recognized in one context can be
transported or matched to patterns in another (morphism-level structure).

Remark 1445. A helpful example is to consider SigClass ranging from ordinary physical channels
to social-symbolic channels and to any hypothetical channels contemplated by a community. Then
Eury contains, in a single schematic envelope, the diverse “universes” induced by those different
signal regimes. The definition is necessary because Hyperseed wishes to speak about “beyond any
one universe” while retaining operational content: the beyond is not a mysterious elsewhere, but a
quantified range over observer-indexed reachability structures (Hyperseed-Concept ??). In practice,
SigClass can also include formal channels such as mathematical proof systems, computational exper-
iment, and mediated instrumentation; these are not “mere language” in this framing, but structured
ways of making distinctions and establishing constraints that can stabilize parts of the eurycosm for
a community of minds. On this view, “physical” and “social-symbolic” are not competing sub-
stances but different signal-mediated interfaces, each with its own notions of invariance, noise, and
admissible intervention.

Definition 431 (Near eurycosm). Fix a mind M . Let CompM (X) ∈ [0, ∞] be a complexity/effort
cost for M to represent or comprehend X (e.g. a weakness-regularized description length). For a
budget B, define the near eurycosm of M at budget B by

                         NearEuryB (M ) := {X ∈ Eury : CompM (X) ≤ B}.                          (21)

The parameter B is intentionally abstract: it may stand for compute, time, memory, training
data, attention, or any mixture of resources that constrain the minds modeling capacity. One

                                                570
natural consistency condition (not required but often convenient) is monotonicity: if B1 ≤ B2 then
NearEuryB1 (M ) ⊆ NearEuryB2 (M ), expressing that additional resources weakly expand what the
mind can stably grasp.

Remark 1446. The function CompM is where resource-boundedness enters explicitly. It may be
defined via description length (algorithmic complexity [16]), via weakness in the sense of quantale-
enriched representational limitation [3], or by any other effort-like cost compatible with the formal
core. The budget B turns that cost into a boundary: what the mind can grasp without exceeding its
representational and computational means. Depending on the application, CompM may include (i)
the cost to learn a representation from data, (ii) the cost to use the representation for inference
or action, and (iii) the cost to communicate the representation to other minds; these can diverge
sharply even when the underlying object X is the same. It is also useful to allow CompM (X) = ∞ for
objects that are, for that mind, effectively unrepresentable (for example, because no stable interface
exists within its available signal classes).

Remark 1447. Example: for a human mind M , parts of Eury corresponding to high-dimensional
microscopic dynamics may be outside NearEuryB (M ) for any realistic B, while coarse statistical
laws fall inside. For a rich-resource mind (Hyperseed-Concept 162) with the ability to simulate vast
portions of the cosmos (as discussed in [11]), the boundary may be dramatically farther out. The
definition is useful because it makes “the wider world that is in principle there” distinct from “the
portion of it that this mind can meaningfully engage.” This distinction also clarifies why scientific
progress can look like an outward motion of the near eurycosm: new instruments, mathematical
languages, and training regimes can decrease CompM (X) for previously inaccessible X, thereby
pulling additional structure into NearEuryB (M ) without changing Eury itself. Conversely, the same
underlying region of Eury may be “near” for one mind and “far” for another because CompM is
observer-relative: what is a direct percept for one agent can be an exotic hypothesis for another.

Remark 1448 (Operational meaning). The near eurycosm depends on the mind’s representational
resources. This makes “beyond our universe” precise in the same observer-relative style as the rest
of Hyperseed: it means “outside the portion of the wider world that the mind can currently model
with bounded effort.” Operationally, a claim that some phenomenon lies outside NearEuryB (M ) can
be read as a prediction about failure modes: the mind will lack stable compressions, will be forced
into brittle ad hoc models, or will be unable to maintain cross-context correspondences robustly
under noise and limited data. Likewise, bridging work (new signal channels, new representational
formalisms, or better translations between contexts) can be understood as constructing morphisms
that effectively lower CompM for relevant targets, thereby making parts of the wider world newly
actionable.

25.9    Anthropic principle as self-locating evidence
Hyperseed treats the anthropic principle as a straightforward statistical point: one’s own existence
is data, and should be conditioned on when reasoning about the universe. In this sense, “anthropic”
updates are not a special-purpose loophole in inference, but an ordinary application of Bayesian
reasoning in the presence of indexical (self-locating) information: not only do we learn facts about
the world, we also learn that we are located in a world-history compatible with our being here to
observe it.

Definition 432 (Anthropic conditioning). Let Θ be a parameter space of universe models (physical
constants, laws, initial conditions, etc.). Let π(θ) be a prior distribution over Θ. Let A be an


                                                 571
“anthropic” event such as “observers of type O exist.” The anthropic posterior is

                                      π(θ | A) ∝ π(θ) P(A | θ).                                  (22)

Remark 1449. The notation is standard Bayesian conditioning: π(θ) is a prior over models
θ ∈ Θ, and P(A | θ) is the probability that observers exist under model θ. The proportionality indi-
cates normalization by the marginal P(A). The definition is useful because it demystifies anthropic
arguments: they are, at their core, conditioning on self-location information.
Remark 1450. In many applications, P(A | θ) is understood as an “observer-weight” or “selection”
factor: models in which observers are common receive greater posterior support after conditioning
on the fact that an observer is making the inference. More explicitly, the omitted normalization
constant is                               Z
                                   P(A) =     π(θ) P(A | θ) dθ,                              (23)
                                              Θ
so that the posterior is a reweighted version of the prior in which the weight is precisely the model-
dependent chance (or frequency, or measure) of producing observers of the relevant kind.
Remark 1451. The event A can be defined at different levels of granularity depending on the
question. A coarse-grained choice is “there exists at least one observer somewhere in the universe,”
while a more fine-grained choice might be “there exists an observer with my evidence-state” (in-
cluding, for example, being in a galaxy of roughly the Milky Way’s age, observing a low-entropy
past, and so on). Hyperseed’s usage emphasizes that such choices are not arbitrary decorations:
they encode what information is actually being conditioned on, and therefore what hypotheses are
being compared.
Remark 1452. A simple example: if some models predict sterile universes with essentially zero
probability of observers, then conditioning on A will suppress those models regardless of their prior
weight. This aligns with Hyperseed’s insistence that epistemology is observer-indexed: what is
rational to believe depends on what kind of observer you are and that you are one at all (Hyperseed-
Concept 57).
Remark 1453. It is also useful to distinguish “possibility” from “probability” in P(A | θ). A
model might permit observers in principle but only in an exceedingly small region of its parameter-
realization space (or along an exceedingly narrow subset of histories), making P(A | θ) tiny. In
that case, anthropic conditioning treats the model as strongly disfavored, not because it is logically
inconsistent with observers, but because observers are atypical under it. This captures the intuition
that “compatible with our existence” is weaker than “makes our existence probable.”
Remark 1454 (Selection effects are not “explanations”). Anthropic conditioning does not explain
why a parameter choice is “likely” in some absolute sense. Rather, it formalizes a constraint on
what an observer should expect to see given that the observer exists. This is fully compatible with
Hyperseed’s emphasis on observer-relativity.
Remark 1455. In particular, anthropic conditioning separates two questions that are often con-
flated: (i) what the universe is like (encoded by θ), and (ii) what an observer should expect to see
given that they are sampling from the subset of world-histories containing observers. The latter is a
statement about conditional expectation, not about a teleological “purpose” of the universe. On this
reading, anthropic arguments do not compete with dynamical or microphysical explanations; they
specify how observational evidence is filtered by the fact that only certain worlds contain observers
capable of gathering that evidence.

                                                  572
Remark 1456. Finally, the anthropic event A is a minimal form of self-locating evidence, but
it is not the only one. One may also condition on additional indexical data such as “I am an
observer at a cosmic time when heavy elements are abundant” or “I find myself in a region with
a particular coarse-grained environment.” In Bayesian terms, these are further events E to be
conditioned on, leading to π(θ | A, E) ∝ π(θ)P(A, E | θ), which makes explicit that anthropic
reasoning is continuous with ordinary scientific updating: the only novelty is that some components
of E describe the observer’s location within the model rather than only the model itself.

25.10    Big bounce as two-ended boundary coupling (speculative)
Hyperseed suggests a “big bounce” picture as an optional speculative anchor: if the large-scale
cosmos is modeled by a least-contrivance (Wu Wei) principle between boundary conditions, then
one may ask where those boundary conditions come from. A big-bounce hypothesis replaces a strict
“beginning” and “end” with a coupled pair of boundaries, potentially allowing certain patterns to
“pass through” from a previous cycle.
    A further motivation for writing the hypothesis in a two-ended form is that, in many infer-
ential and variational settings, specifying both endpoints is a compact way to encode constraints
that would otherwise appear as time-dependent “forces” or finely tuned initial microstates. In cos-
mological language, this also echoes the idea that macroscopic regularities (including low-entropy
constraints or special smoothness conditions) may be more naturally stated as boundary informa-
tion than as ad hoc midstream interventions. In this register, the “bounce” is not only a geometric
picture (contraction followed by expansion) but also an informational coupling between terminal
and subsequent initial data.
Definition 433 (Two-ended cosmic boundary model). Let X be a space of coarse cosmic states
(or state distributions), and let T > 0 be a cosmic timescale. A two-ended model specifies boundary
data (µ0 , µT ) and selects a history distribution {µt }t∈[0,T ] by minimizing a contrivance functional
(e.g. a KL divergence relative to a reference dynamics), subject to these boundary constraints. This
is the same mathematical idiom used for Schrödinger bridges and Wu Wei dynamics.
Remark 1457. The objects µ0 and µT are boundary distributions on X , and {µt } is a path (in
distribution space) connecting them. The “contrivance functional” is meant to quantify how much
the selected history deviates from a reference, “natural” dynamics; KL divergence is a canonical
choice in Schrödinger bridge theory. Hyperseed uses this idiom to formalize Wu Wei as least forcing
[21]; the present definition merely transposes the same mathematics to a cosmic scale (Hyperseed-
Concept 66, 207).
Remark 1458. For readers who prefer a slightly more explicit bridge to standard formulations:
one common setup places a reference path measure P0 on trajectories (induced, for instance, by
a Markov kernel or stochastic differential equation regarded as “baseline physics” at the chosen
coarse-graining), and then selects a constrained path measure P whose time-marginals are {µt }.
The contrivance cost is then written as KL(P kP0 ), and the boundary conditions appear as marginal
constraints P (X0 ∈ ·) = µ0 and P (XT ∈ ·) = µT . In that language, the family {µt } is not merely
an arbitrary interpolation but the set of marginals of the least-contrived path ensemble consistent
with the endpoint information. This is one reason the two-ended specification is methodologically
attractive: it turns endpoint information into a well-posed selection principle over entire histories.
Remark 1459. A simple intuition is to imagine that instead of specifying an initial condition
and letting dynamics run, one specifies both an “initial-like” and “final-like” macroscopic condition
and asks for the least contrived interpolation. This resembles variational principles in physics and

                                                 573
control, and in Hyperseed’s philosophical register it resonates with the idea that “history” is a
selection among possible trajectories subject to constraints, rather than an inert given.
Remark 1460. At the level of interpretation, a two-ended formulation also helps separate three
notions that are often conflated: (i) microscopic time-reversal symmetry (a property of candidate
baseline dynamics), (ii) macroscopic arrow-of-time (a property of typical solutions under special
boundary conditions), and (iii) epistemic updating (how an observer infers histories given partial
data). In the present subsection, Hyperseed is not committing to a specific microphysical model of the
bounce; it is instead emphasizing that, whatever the microphysics, a coupled-boundary representation
can make explicit which part of the “arrow” is being attributed to boundary data rather than to
asymmetric dynamical laws.
Definition 434 (Bounce operator and cross-cycle morphic resonance). A bounce operator is a
map B sending the terminal boundary to the next-cycle initial boundary:

                                             µnext
                                              0    = B(µT ).                                     (24)

A simple way to express “two-sided morphic resonance” across the bounce is to let B depend on
pattern content:                                                     
                         B(µT ) := arg min KL(ν k µ? ) + λ Res(ν, µT ) ,                 (25)
                                         ν

where µ? is a reference prior for initial conditions and Res is a (bounded) resonance functional
favoring re-instantiation of patterns present in µT .
Remark 1461. In the displayed formula, arg minν (· · · ) selects the distribution ν (candidate next
initial condition) that trades off proximity to a baseline prior µ? (via KL divergence) against “res-
onant” similarity to the previous terminal condition µT (via Res). The scalar λ tunes the tradeoff.
This is intended as a formal placeholder showing that, if one wants to talk about cross-cycle pat-
tern carryover, one can do so in the same optimization and resonance language used elsewhere in
Hyperseed. The mention of “morphic resonance” connects to speculative proposals in the broader
literature [13] as well as Hyperseed’s own resonance formalism [5].
Remark 1462. The requirement that Res be bounded is not merely cosmetic: it is one simple
way to avoid trivializing the optimization by letting resonance dominate all other terms. More
generally, one can view Res as encoding a pattern statistic extracted from µT and compared to
a candidate ν. For instance, if patterns are represented by a feature map φ : X → Rd (coarse
observables, topological signatures, long-range mode amplitudes, algorithmic motifs, etc.), then a
resonance penalty/reward could depend on moment matching such as kEν [φ] − EµT [φ]k2 , or on a
kernel similarity between distributions. Writing B in this way makes explicit where the hypothesis
lives: in the choice of pattern representation and in the form/weight of the coupling.
Remark 1463. One should also distinguish the “bounce operator” B from the within-cycle refer-
ence dynamics used in the two-ended model. In the present idiom, B is not a time-step of ordinary
evolution on X ; it is an inter-cycle boundary map that may include coarse-graining, informa-
tion loss, or projection onto a family of admissible next-cycle initial macrostates. Put differently,
even if the within-cycle history is selected by least-contrivance relative to a baseline dynamics, the
cross-cycle linkage can still be nontrivial because it acts on boundary distributions rather than on
instantaneous microstates.
Remark 1464. One should notice the methodological point: even when Hyperseed permits spec-
ulative anchors, it seeks to express them as operators and functionals that could, in principle,

                                                  574
be constrained by evidence. This is the Dyson/Sagan virtue in a metaphysical setting: keep the
conjecture legible to calculation, so that disagreement can become quantitative rather than merely
rhetorical.

Remark 1465. In the same methodological spirit, the bounce-operator parametrization suggests at
least three distinct kinds of constraints one might imagine (even if only in principle): (i) constraints
on the “memory strength” λ (how much cross-cycle similarity is permitted without contradicting
observed decoherence or cosmological mixing), (ii) constraints on which observables can plausibly
remain informative across a bounce (encoded by the choice of φ or of the admissible class of Res),
and (iii) consistency constraints between within-cycle least-contrivance histories and cross-cycle
boundary maps (e.g. fixed-point or cycle-consistency relations such as µ0 ≈ B(µT ) for a stationary
cycling regime). These are not claims that such data are currently available; they clarify what, in
this formalization, would count as sharpening or refuting the hypothesis.

Remark 1466 (Status). This “big bounce” construction is included here as a formal placeholder:
it shows how to talk about cross-cycle pattern carryover using the same operators already developed
for resonance and least-effort path selection. Hyperseed explicitly notes that quantitative aspects of
such a phenomenon are unclear.

Taken together, these constructions place Hyperseed’s cosmological vocabulary inside the same
mathematical toolbox as its cognitive vocabulary. The next section (Wu Wei dynamics) uses the
variational viewpoint more directly, treating action and history selection as geodesic flow in a
weakness-shaped geometry [21].


26      Wu Wei dynamics and optimal control
Hyperseed uses the Taoist term wu wei as an ontological-computational slogan: effective action
with minimal forcing. The informal imagery is “like water” or “like a plant bending in the wind”:
adaptive, responsive, and skillful, without unnecessary struggle. Earlier sections of this paper
formalize (i) representational limits via weakness and (ii) conflicting valuation via paraconsistent
evidence and resonance. This section adds a third piece: control as variational flow in a geometry
induced by weakness.

Remark 1467. The philosophical gesture behind wu wei in Hyperseed is that agency need not
be identified with strain. One may act, and act effectively, while remaining close to a “passive”
unfolding of events—provided that the passive unfolding already embodies a rich store of learned
regularities and habits. In this sense, wu wei is an engineering principle as much as a contemplative
one: it says that a good controller should look, mathematically, like a gentle reweighting of what
would have happened anyway, rather than a continual override of the world and the agent’s own
default tendencies; compare [21].

Remark 1468. Conceptually, this section is primarily about Hyperseed-Concept 206 and Hyperseed-
Concept 207, and it also relies on Hyperseed-Concept ??, Hyperseed-Concept 100, Hyperseed-
Concept 158, and Hyperseed-Concept 202. The formal development below is meant to show how
these concepts can be grounded in standard (but remarkably elegant) variational principles, while
keeping faith with Hyperseed’s emphasis that “minimal forcing” is inseparable from “minimal rep-
resentational effort” [3, 2].

     The key move is to treat “effort” as having (at least) two components:


                                                  575