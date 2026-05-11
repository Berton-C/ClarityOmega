# 14 Prediction, attraction, causality, and control

a seed and the web’s closure can be the weave. One may also view the example as separating two
kinds of “cause”: an external cause (the morphic field term) that changes what is locally available
to the system, and an internal cause (the reinforcement web) that determines what the system can
build from whatever is available. The two-step structure matters: without the morphic injection, p
would remain low in positive evidence in C2 , and the edge p → q would not generate a substantial
increase in q; without the internal web, the morphic injection would remain a local change to p
without generating additional downstream organization.

12.7    Notes and bridges to later sections
Where attention and effort enter. The update operators above are “structural.” In Hy-
perseed, attention (Hyperseed-Concept 60) and effort (Hyperseed-Concept 100) modulate which
pattern classes are tracked and which reinforcement links are strengthened. Formally, attention
can be implemented as a time-varying reweighting of A and ut (and even of the pattern class P
itself) driven by resource constraints from Section 8. Concretely, one may treat attention as a
gating field wt that rescales the effective adjacency and reinforcement updates (e.g., A 7→ wt A
and ut 7→ wt ut with appropriate normalization), so that limited processing budget is expressed
directly as selective amplification/suppression of candidate pattern links. On this view, “effort”
can be modeled not only as a scalar budget but also as a constraint on the allowable complexity
of the currently tracked subweb (e.g., limiting the number of active nodes/edges, the depth of
multi-step propagation, or the entropy of the attention weights), thereby coupling computational
cost to the dynamics of habit-formation. This makes explicit how the same structural operator
can yield markedly different learning trajectories under different resource regimes: under scarcity,
updates become sparse and conservative; under abundance, they become denser and can support
rapid structural reconfiguration. This perspective aligns with the general cognitive-systems view
that attention is a resource-allocation operator acting on inference/learning dynamics (see, e.g.,
[19]).

Relation to resonance/dissonance (Section 3.9). Section 3.9 sketches a logic-to-complex
mapping and an interference-based resonance score. In the present section, morphic resonance is
implemented as a coupling kernel K`0 →` that transports pattern support across contexts. One can
combine these views by: (i) using paraconsistent interference scores to adaptively learn K; and/or
(ii) interpreting high interference-coherence as a signal that two contexts share a near-morphism
between their pattern webs, warranting stronger morphic coupling. In more operational terms,
K`0 →` may be taken as a (row-)stochastic or otherwise mass-preserving operator so that “transport”
can be read literally as redistribution of support, with constraints (e.g., positivity, bounded norm,
or decay with contextual distance) preventing spurious amplification. Likewise, when interference is
used as a learning signal, it can be used either to increase coupling for coherent overlaps (resonance)
or to decrease coupling when overlaps are systematically contradictory (dissonance), yielding a
unified knob that can implement both attraction and repulsion between webs depending on the
sign/structure of the paraconsistent evidence. The near-morphism interpretation can be made
explicit by asking whether there exists a structure-respecting map that approximately preserves
key relational signatures (connectivity motifs, implication-like edges, or compositional paths) from
one web to the other; high coherence then indicates that such a map is available with low distortion,
making cross-context transfer reliable rather than merely associative. This is one natural meeting
point between paraconsistent evidence dynamics and resonance-style measures [24].




                                                 264
Reality-systems and beyond. In later sections (reality-systems, intersubjective reality, eu-
rycosm), the same coupled-web formalism can be re-used with L indexing different reality-systems
and K encoding cross-system transduction pathways. This provides a mathematically explicit
“port” for discussing morphic resonance in settings where “spatial separation” is generalized to sepa-
ration across representational, social, or cosmological contexts (Hyperseed-Concept 149, Hyperseed-
Concept ??, Hyperseed-Concept ??; see also [18]). Here it is helpful to read “transduction” broadly:
K can stand for translation between symbol systems, alignment between agents internal models,
propagation through communication networks, or coupling across scales (e.g., individual → group
→ institution) when L is organized hierarchically. In such cases, constraints on K can encode
empirical or normative limitations (bandwidth limits, trust/credibility filters, institutional fric-
tion), making the same mathematics serve both descriptive and prescriptive roles: describing how
habits and meanings spread, and prescribing how to shape coupling to improve coordination or
reduce pathological contagion. This framing also anticipates later uses where one distinguishes
“within-system” stabilization (habit consolidation inside a reality-system) from “between-system”
transfer (morphic resonance across reality-systems), since the two can be tuned independently by
the intra-web reinforcement rules versus the inter-web kernel K.


13     Mind, representation, and perception
This section introduces the representational layer of Hyperseed [1]. The preceding sections provide
(i) an observer-relative notion of distinction/weakness, (ii) patterns as simplicity-improving re-
presentations, and (iii) dynamical operators (habits and morphic resonance) that move pattern
support across contexts. Here we focus on how a system becomes a mind by supporting registration
of patterns, representation of what is registered, and the beginnings of closed-loop organization
(with control treated formally in Section 14).

Remark 583. Conceptually, this section is the hinge between the “static” side of the formalism
(distinctions, weakness, and patterns) and the “active” side (prediction, control, and attention). A
mind, in the Hyperseed sense, is not merely a container of data; it is a system that can stabilize
some internal stand-ins for what it encounters, and then use these stand-ins to guide future behavior.
This framing aligns with the emphasis in [19] on internal representational dynamics as the substrate
for flexible cognition.

13.1    Systems, minds, and recognition processes
Hyperseed uses “system” in the autopoietic sense: not every arbitrary distinguished collection
counts as a system; a system must have internal coherence and internal production. For this paper,
it is useful to model “system” at two complementary levels: (i) a process level (how state evolves)
and (ii) a pattern level (what compressive regularities are stably present).

Definition 157 (Process and system). A process is a triple (T, Σ, δ) where:

• T is a proto-time index (a poset, interpreted as a partial order of “before/after”),

• Σ is a (possibly structured) state space,

• δ : T → (Σ → Σ) assigns to each t ∈ T a state-update map.

A system is a finite directed multigraph S = (P, E) whose nodes p ∈ P are processes and whose
edges encode production dependencies: (p → q) ∈ E means that the evolving state of p supplies

                                                 265
part of the input (or constraint) for the evolution of q. We say S is inter-producing if every node
lies on a directed cycle.
Remark 584. A few notational clarifications help anchor this definition. The symbol T denotes
a partially ordered set (poset): one should read t  t0 as “t is no later than t0 ” in the system’s
proto-time (Hyperseed-Concept 142). The state space Σ is the mathematical home of instantaneous
configurations, and δ(t) : Σ → Σ is the time-indexed update map (so the state at t advances
according to δ(t)). Thus, the composite object (T, Σ, δ) is a minimalist process in the style of
dynamical systems theory, but allowing partial time order fits well with later branching-time and
context machinery.
    The shift from a single process to a system S = (P, E) is a shift from “one evolving thing” to
“many evolving things with dependencies.” A directed multigraph allows multiple edges between
the same pair of processes, which is useful when a module can depend on another in several distinct
ways. The inter-producing condition (every node lies on a directed cycle) is a concise way of
insisting on mutuality: nothing in the system is purely a passive input; every component is also
(perhaps indirectly) sustained by others. This resonates with process-ontological intuitions in the
background of Hyperseed (compare [15]) and with Hyperseed’s emphasis on self-maintaining webs
(Hyperseed-Concept 168).
Remark 585. The “inter-producing” condition is a minimal formal proxy for the informal Hyper-
seed idea that systems are coherent sets of inter-producing processes. In Section 12 we strengthen
this idea using autocatalytic closure properties expressed on pattern webs.
Definition 158 (Mind). A mind is a system M = (P, E) equipped with additional structure:
1. A distinguished registration interface (a “sensory” subgraph) Sin ⊆ M.
2. A representation space R (objects, tokens, or states that can stand in for other entities).
3. A reference relation Ref C ⊆ R × U for each context/aspect C, where U denotes the ambient
   universe of entities under discussion.
4. An update rule that turns registrations into representational changes (e.g. rt+1 = Update(rt , Regt )
   for some internal state rt ∈ R).
The remaining sections refine these components and give semantics in terms of patterns, weakness,
and paraconsistent evidence.
Remark 586. This definition should be read as a deliberately spare “constitution” rather than a
detailed psychology. A mind is, first, a system in the sense above: an interdependent complex of
processes. But it becomes a mind by having (i) a privileged gateway where the world impresses
itself upon the system (registration; Hyperseed-Concept 153), (ii) an internal realm of stand-ins
(representation; Hyperseed-Concept 157), and (iii) a relation Ref C that ties stand-ins to what they
are about (reference; Hyperseed-Concept 152). The context index C matters philosophically: it
encodes the Russellian insistence that meaning is not floating in a void; it is always meaning under
some way of taking the world, i.e. under some partition of distinctions (Hyperseed-Concept 86).
    A simple example: let U contain physical objects, and let R contain internal feature vectors or
symbolic tokens. A camera-like subsystem can serve as Sin . Then Ref C (r, u) may mean “token r
currently refers to object u as seen in visual context C.” The update rule is the bridge from mere
causal impact to sustained internal content. This is why Hyperseed treats registration as weaker
than perception: the update rule can fail, be blocked, or be too noisy to stabilize representation. The
general program is consonant with the cognitive-systems stance of [19], while remaining compatible
with the pattern/emergence framing in [5].

                                                 266
Definition 159 (Pattern recognition process). Fix a context/aspect C and a set of candidate
patterns PC . Assume each system-state S at time t determines a (possibly fuzzy) intensity map
IntS,t : PC → V into the quantale V from Section 3. A process Y is a pattern recognition process
aimed at an entity X (in aspect C) if there exists a nonempty set PX,C ⊆ PC such that for each
P ∈ PX,C :

1. (alignment) IntY,t (P ) ≤ IntX,t (P ) for all relevant t, and

2. (learning) IntY,t (P ) is nondecreasing in t (w.r.t. the order on V ), with strict increase for at
   least one P at least once.

Remark 587. Here PC is the repertoire of patterns that the context C makes available (Hyperseed-
Concept 130). The quantale V supplies a graded scale of “how much a pattern is present”: the order
≤ on V is the comparison of intensities, and the monoidal structure (introduced in the formal core)
is what ultimately makes these intensities compositional. The notation IntS,t (P ) is the intensity of
pattern P in the system-state S at time t; one may picture it as the system’s current “degree of
embodiment” of P .
    Intuitively, Y recognizes X when Y comes to mirror (some of ) X’s patterns, and to do so ever
more stably. Condition (alignment) prevents us from calling arbitrary growth in Y a recognition of
X; it must be growth in patterns that are genuinely patterns of X. Condition (learning) demands
a temporal direction: recognition is not a static coincidence but a historical acquisition. A toy
example: if X is a melody and P ranges over rhythmic/melodic motifs, then a listener-process Y
recognizes X as it internalizes these motifs (its IntY,t (P ) rises), while remaining within what is
actually present in the melody (alignment).
    This concept is useful because it makes recognition expressible without presupposing crisp symbols
or propositional truth: recognition is framed in the same graded pattern vocabulary as the rest of the
theory. That uniformity becomes crucial once we allow paraconsistent evidence, habit dynamics,
and cross-context resonance (Hyperseed-Concept 151).
    A further point of the quantale-valued formulation is that “presence” need not be probabilistic or
frequency-like: depending on the chosen V , intensities can encode salience, constraint-satisfaction,
degree of activation, similarity, or any other orderable evidence measure that supports the re-
quired compositional operations. In particular, allowing IntS,t to be fuzzy means that Y can par-
tially recognize X—e.g. strongly for some motifs and weakly for others—without forcing a binary
recognized/not-recognized cut. The set PX,C can be read as the (aspect-relative) collection of pat-
terns through which X is “trackable” by Y in the given context; different choices of C can therefore
yield different recognition relations even between the same X and Y .
    The clause “for all relevant t” is intentionally flexible: in applications one may take t to range
over a training episode, over a window in which X is presented, or over a period of interaction
in a shared environment. Nothing in the definition requires t to be discrete; the monotonicity
condition in (learning) can be interpreted for continuous time (as an order-preserving map along the
temporal order) as readily as for stepwise updates. Likewise, (learning) allows plateaus: IntY,t (P )
may stabilize once Y has acquired the pattern, but the requirement of at least one strict increase
rules out the degenerate case where Y merely happens to match X without any acquisition at all.

Remark 588. Definition 159 formalizes a core Hyperseed intuition: recognition means that, through
interaction, the recognizer comes to contain more of the same patterns that are present in what it
recognizes. When combined with habit dynamics (Section 12), this becomes an explicit model of
perceptual learning. In that combined picture, the monotone rise of IntY,t (P ) can be understood
as the trace left by repeated successful engagements with P —a memory-like accumulation that need


                                                   267
not be explicit or symbolic. The alignment condition then plays the role of an external constraint:
it ties the direction of learning to the target entity X rather than to arbitrary self-amplification
within Y , and it permits a clean distinction between “becoming more patterned” and “becoming
more patterned in the way that matches X.” The nonemptiness of PX,C similarly enforces that
recognition is about at least one concrete pattern channel in the specified aspect, making explicit that
recognition is always selective and aspect-relative rather than an undifferentiated global relation.
Remark 589. It can be helpful to view PX,C as encoding what counts as “evidence about X” for
the recognizer in context C: if P ∈     / PX,C , then even large values of IntY,t (P ) do not contribute
to recognition of X in that aspect. This separation makes room for familiar phenomena such
as confounds and misattribution: Y may increase intensity on patterns that are predictive in its
environment but are not actually patterns of X, in which case (alignment) fails and the process is
better described as learning a surrogate. Conversely, the definition allows recognition to be partial
and distributed: Y need not match X on all patterns in PC , only on some nonempty subset, and only
to the extent measured in V . In settings where one wants to model over-shooting or hallucination
(i.e. IntY,t (P ) > IntX,t (P ) for some P ), one can treat such departures as a distinct kind of process
rather than folding them into recognition; the present definition deliberately marks that boundary
by requiring alignment.

13.2    Contexts and aspects
Hyperseed treats most predicates as context-dependent. For representation, this context depen-
dence is not optional: what a token represents is always “a representation of B in some aspect
C.”
Definition 160 (Context and aspect extraction). Let Ctx be a (small) poset of contexts with order
C  D meaning “D refines C” (makes at least as many distinctions). An aspect extraction family
is a family of maps
                               aspC : U → UC       (C ∈ Ctx)
with the property that if C  D then there is a canonical “forgetful” map πD→C : UD → UC
satisfying aspC = πD→C ◦ aspD . We write X|C := aspC (X) for the aspect of X in context C.
Remark 590. The notation is doing quiet but important work. The poset Ctx is a bookkeeping
device for “ways of carving reality”: C  D means that D is at least as discriminating as C
(Hyperseed-Concept 86). The map aspC is a projection that forgets everything about X that C is
not sensitive to. The codomain UC is the universe as viewed through C: one may think of it as
equivalence classes, coarse descriptors, or structured observations, depending on the application.
    A simple example is geometric: let U be the set of 3D objects, and let C be “silhouette shape”
while D is “full 3D mesh.” Then D refines C, and πD→C maps a 3D mesh to its silhouette de-
scriptor; extracting the silhouette directly from the object or extracting the mesh and then forgetting
down to silhouette yield the same result. Another example is linguistic: C might keep only “part of
speech,” while D keeps full syntactic parse; again, D refines C.
    This definition is necessary because reference and representation will be indexed by C, and
without a disciplined notion of aspect we risk equivocation: a token can be a faithful representation in
one aspect (e.g. location) while being wildly unfaithful in another (e.g. color). Hyperseed’s insistence
that meaning is aspect-relative makes this explicit and prevents category mistakes.
Remark 591. The condition aspC = πD→C ◦aspD says that refining context and then forgetting back
down is equivalent to extracting the coarse aspect directly. This formalizes the idea that “aspects”
are stable observer-relative projections.

                                                  268
Remark 592. It is helpful to view the family {UC }C∈Ctx as a system of compatible “views” of U,
where refinement introduces additional structure but never contradicts coarser views. Concretely,
if C  D  E, then one typically expects the forgetful maps to compose coherently, i.e. πE→C =
πD→C ◦πE→D , so that there is a unique way to forget from a very fine context down to a very coarse
one. This kind of coherence is often implicit when one says the map πD→C is “canonical,” and it
mirrors the informal idea that there is not more than one principled way to discard distinctions.

Remark 593. The adjective “small” for Ctx is primarily a set-theoretic convenience: it ensures
that the indexing of contexts does not introduce size issues when later constructions quantify over
contexts, form products over families of contexts, or speak of “all” contexts relevant to an agent.
Intuitively, it corresponds to the modest claim that the agent’s repertoire of ways-of-carving is
enumerable within the theory, rather than a proper class of all imaginable measurements.

Remark 594. In many applications, each aspC may be understood as inducing an equivalence
relation on U: two entities X, Y ∈ U are C-equivalent if X|C = Y |C. Under this reading, UC can
be taken (up to isomorphism) as the quotient of U by C-equivalence, and πD→C expresses that D-
equivalence refines C-equivalence when C  D. This can clarify the slogan that a context “forgets
distinctions”: it identifies many fine-grained states as the same coarse state.

Definition 161 (Contextualized groupings). For a grouping (collection) G ⊆ U and context C,
define the contextualization of G to C by

                                   G|C := { x|C : x ∈ G } ⊆ UC .

Remark 595. This is the natural lifting of aspect extraction from individuals to sets (Hyperseed-
Concept 103). Intuitively, if G is “the set of all cups on the table,” then G|C is that same set as
seen through context C—for example, perhaps as a set of silhouettes, or as a set of rough positions,
depending on what distinctions C preserves.
    The usefulness is pragmatic: later constructions (pattern webs, attention allocation, prediction)
often operate on collections rather than single entities. By contextualizing the collection, we can
compare group-level phenomena across contexts without pretending that the contexts share the same
granularity.

Remark 596. Note that the definition uses an ordinary set image, so distinct elements of G may
collapse to the same element of UC when context C is coarse. This is not a bug: it records the fact
that, relative to C, those distinct individuals are indistinguishable. When multiplicity matters (e.g.
“two identical-looking cups” vs. “one cup”), one may later choose to work with multisets, measures,
or probability distributions on UC rather than plain subsets, but the present definition captures the
minimal invariant needed for many aspect-relative comparisons.

Remark 597. Contextualization interacts with basic set operations in the expected monotone way.
If G ⊆ H then G|C ⊆ H|C, and if {Gi } is any family of groupings then
                                  [           [
                                       Gi |C = (Gi |C).
                                         i             i

In general, contextualization does not commute with intersections: (G∩H)|C may be strictly smaller
than (G|C) ∩ (H|C), because two different elements—one from G and one from H—may become
C-indistinguishable even if the original sets were disjoint. This is another manifestation of how
a context can erase distinctions, and it will be relevant whenever later arguments reason about
“overlap” between groupings in an aspect-relative way.

                                                 269
13.3    Registration, sensory systems, and perception
Registration is Hyperseed’s primitive “information intake” notion. It is weaker than perception:
perception requires that registration triggers an internal representation. In particular, registration
is meant to capture the minimal sense in which the system’s dynamics come to depend on some
aspect of the world, even when that dependence is too coarse, too unstable, or too weakly integrated
to count as content-bearing cognition. This makes registration suitable as a common substrate for
later distinctions: for instance, one can speak of registration that is accurate but nonconceptual,
registration that is noisy or ambiguous, and registration that is driven by internal couplings (as in
dreams) rather than exogenous causes (as in ordinary sensing).
Definition 162 (Registration). Fix a context C and an equivalence relation ∼C on UC (interpreted
as “indistinguishable in context C” for the registering system). A system X registers an entity A
at time t (in context C) if there exists A0 ∈ U such that A0 |C ∼C A|C and A0 |C becomes a pattern
in X by time t. Concretely, this can be witnessed by a pattern P ∈ PC such that

                       IntX,t (P ) 6≤ θ   and      Ref C (P, A|C) is nontrivial,

for some threshold θ ∈ V .
Remark 598. Registration (Hyperseed-Concept 153) is intentionally defined so that it can occur
without any rich internal model. The equivalence relation ∼C encodes what the system cannot
tell apart in context C (Hyperseed-Concept ??). Thus, registration is compatible with vagueness:
to register A is not necessarily to pin down A as a unique individual, but to have one’s internal
dynamics come to embody a pattern that is at least compatible with A under the system’s current
discriminations.
    A minimal example: let C be a low-resolution visual context in which many distinct objects
share the same coarse “blob” descriptor. Then ∼C identifies objects with the same blob. The system
registers a particular object A when a blob-pattern becomes salient in the system (IntX,t (P ) crosses
threshold) and is linked by reference to the extracted aspect A|C. Here the notation IntX,t (P ) 6≤ θ
means “the intensity is above threshold” in the quantale order; in a numeric quantale this would read
as the usual inequality “greater than θ,” but the order-theoretic phrasing accommodates nonstandard
evidence domains.
    This definition is useful because it separates (i) being impacted by the world from (ii) construct-
ing an internal token that stands for the world. That separation is needed for later distinctions
among mere sensation, perception, hallucination, and reflective awareness.
    Two further clarifications help fix the intended reading. First, the role of A0 is to accommodate
the fact that the system may only ever interact with (or encode) a surrogate that is equivalent to
A under the coarse-graining imposed by C and ∼C ; one should not read the definition as requiring
access to A “as it is in itself,” but only to some entity that is indistinguishable from A at the
resolution that matters for the registering system. Second, the “becomes a pattern in X by time
t” clause is temporal in a permissive way: it allows registration to be an event that takes time to
settle (e.g., integration over a short window, the closing of a feedback loop, or the accumulation of
evidence), rather than an instantaneous snapshot. In settings where t is discrete and updates are
synchronous, this can be read as “at or before the t-th update.”
    It is also useful to distinguish nontrivial reference from maximally specific reference. The
condition Ref C (P, A|C) nontrivial demands that the pattern is not merely active, but active as
about (or at least systematically linked to) the contextual aspect A|C. However, the definition does
not force the pattern to determine a unique referent beyond the equivalence class fixed by ∼C : the
same P may be compatible with many distinct A’s in U so long as their C-aspects are identified.

                                                 270
This is the intended locus of perceptual ambiguity at the level of registration (e.g., “something
moved” or “a sound occurred” without a stable object assignment).

Definition 163 (Sensory system). Let X be a system and let U ext ⊆ U denote those entities
considered “external” to X in a given modeling decomposition. A sensory system for X is a
coherent subsystem S ⊆ X such that:

1. most registrations produced by S have referents in U ext , and

2. the update dynamics of S are driven primarily by coupling to U ext (rather than by coupling
   internal to X).

Remark 599. The point is not that the sensory system is metaphysically “outside-facing,” but that,
under a chosen decomposition into “system” and “environment,” its causal drivers are predomi-
nantly exogenous. In robotics this might literally be sensors; in social cognition it might be language
interfaces; in introspective cognition it might even be sub-systems that “sense” other parts of the
mind. The definition thus accommodates both the ordinary case and the more Peircean/Whiteheadian
view that there are many layers of mutual prehension, some treated as external only by pragmatic
abstraction [14, 15].
     As an example, in a neural network model of an agent, an early vision stack could serve as S
if its inputs are mostly pixels from the environment and its learned features are mostly driven by
those pixels. The utility of naming S is that perception, attention, and control will later be analyzed
as transformations that begin at such interfaces and propagate inward.
     The qualifier “most” in item (1) is deliberate: many realistic sensory subsystems also generate
registrations whose immediate referents are internal variables (e.g., gain control states, prediction
error channels, or learned latent features) while still being primarily shaped by exogenous coupling.
Similarly, item (2) is intended to be robust under modeling choices: one may refine or coarsen the
system–environment boundary, and the definition only asks that, under the chosen decomposition,
the dominant causal influence on S comes from U ext . This keeps the notion compatible with settings
in which sensorimotor loops blur the boundary (e.g., active sensing where X moves to create infor-
mative inputs) while still allowing one to identify subsystems whose input channels are anchored
in the external world.
     It is also helpful to note that coherence of S is functional rather than anatomical: a sensory
system may be distributed (e.g., multiple modalities or parallel transducers) so long as it forms a
relatively unified interface from the standpoint of downstream processing (for instance, by supporting
stable patterns P ∈ PC that later stages can treat as evidence).

Definition 164 (Perception). A mind M perceives an entity A at time t (in context C) if:

1. M registers A at time t (Definition 162), and

2. this registration causally triggers the emergence of a representation token R ∈ R with Ref C (R, A|C)
   nontrivial.

In slogan form: perception is registration that causes representation.

Remark 600. Perception (Hyperseed-Concept 134) is the first place where the theory demands a
causal bridge from world-impact to internal content. Item (2) is what blocks a trivialization: mere
registration can be fleeting, local, and unintegrated, whereas perception is registration that organizes
the mind’s representational economy by producing a token R that can participate in later inference,
memory, and action.

                                                  271
    A simple example: a thermostat may “register” a temperature (its state changes in response
to heat), but unless it produces an internal token that stands for “it is hot” in a way that can be
recombined with other tokens, we would hesitate to call it perception in this framework. Conversely,
an agent that forms an explicit map entry or object-file when stimulated by A meets the condition.
This is why perception is the natural bridge to the prediction/control machinery of Section 14.
    The “causally triggers” clause is meant to exclude cases where a representation happens to co-
occur with a registration without being appropriately dependent on it. For instance, if R is generated
by a purely endogenous process and merely coincides with the time at which M registers A, then (2)
fails even if Ref C (R, A|C) is nontrivial. Conversely, if the registration initiates a cascade (possibly
mediated by attention, gating, or working memory) that yields R, then the perception condition is
satisfied even when the representation is delayed relative to the initial registration, so long as the
causal dependence is preserved.
    It is also important that (2) requires a representation token rather than merely a strengthened
pattern. Intuitively, a token R ∈ R is something the mind can reuse, store, compare, and bind into
larger structures; it is the kind of internal item that can later be evaluated for accuracy, recalled,
or used as a premise in reasoning. Thus, perception is not merely “strong sensation”: it is the
emergence of a content-bearing element whose reference to A|C is stabilized enough to enter the
mind’s representational repertoire.

Proposition 19 (Perception implies registration). If a mind M perceives A at time t in context
C, then M registers A at time t in context C.

Proof. Immediate from Definition 164, item (1), which requires that M registers A at time t in
context C as a precondition for perception.

Remark 601. Intuitively, this proposition says: if you genuinely perceived something (in the
present formal sense), then you must at least have been affected by it in the weaker registration
sense. The result is not surprising, but it is structurally important: it guarantees that perception is
a strengthening of registration rather than a separate notion that could drift away. This monotonic
relationship will be quietly used later when we model attention as selectively modulating the pipeline
from registration to representation.

Proof. Immediate from Definition 164, item (1).

Proof sketch. Unpack the definition of perception: registration is literally a required conjunct. 

Remark 602. The key step “item (1)” is doing all the work because perception was defined as a
two-part condition, with registration as the first part. One may think of this as a design choice: the
formalism encodes a conceptual hierarchy of notions (registration ⇒ perception) directly into the
logical form of the definitions.

13.4    Representation as reference plus pattern inheritance
Hyperseed defines representation as “re-presentation”: there must be a reference relation to what
is represented, and the representation must inherit (some of) the patterns of the represented entity.
We now formalize both components.

Definition 165 (Pattern signature in an aspect). Fix a context C and a finite pattern basis BC ⊆
PC . The pattern signature of an entity X in aspect C is the map

                          SigC (X) : BC → V,        SigC (X)(P ) := IntX (P ),

                                                  272
where IntX (P ) denotes the intensity of pattern P in X as defined in Section 9 (or its later refine-
ment).

Remark 603. The pattern signature is an “aspect-relative fingerprint” of an entity in terms of
a chosen basis BC (Hyperseed-Concept 141). Concretely, BC is a finite list of patterns we have
decided are salient for the present discussion; the signature SigC (X) then assigns each basis pattern
P an intensity value in V measuring how strongly P is present in X.
    A simple example: if C is a sensory context and BC is a set of visual features (edges, colors,
textures), then SigC (X) is analogous to a feature vector. If C is a relational context and BC is a
set of graph motifs, then SigC (X) is a profile of how much X exhibits those motifs. The definition
is useful because representation will be defined by comparing signatures: to represent is, in part, to
share patterns in a controlled (typically reduced) way. This directly reflects Hyperseed’s notion of
patterns as compressive regularities [5].

Definition 166 (Strong pattern inheritance). Let A, B ∈ U and context C be given. We say that
A inherits patterns from B in aspect C if

                           SigC (A|C)(P ) ≤ SigC (B|C)(P )      ∀P ∈ BC .

Equivalently, SigC (A|C) ≤ SigC (B|C) pointwise.

Remark 604. The inequality is intentionally one-sided: inheritance means “A has no more of
each basis-pattern than B does,” so A is (at most) as pattern-rich as B in the monitored directions.
In a numeric setting, if SigC were feature activations in [0, 1], then inheritance would say each
activation in A is bounded above by the corresponding activation in B.
    A toy example is projection: if B is a high-resolution image and A is a compressed thumbnail,
then the thumbnail inherits many coarse patterns (large-scale edges) but not the fine ones; in a
basis that monitors only coarse patterns, one expects SigC (A) ≤ SigC (B). The definition is useful
because it captures, in a single monotone condition, the intuition that a representation should be a
simplification: it may discard detail, but should not invent detail in the same aspect without further
explanation.

Definition 167 (Representation in an aspect). Let A, B ∈ U and context C be given. We say that
A represents B in aspect C if:

1. (reference) Ref C (A, B|C) is nontrivial, and

2. (inheritance) A|C inherits patterns from B|C in the sense of Definition 166.

Remark 605. This definition makes precise Hyperseed’s slogan that representation is “re-presentation”:
A presents again, in a cheaper form, something that is already present in B. The reference condition
ensures “aboutness” (Hyperseed-Concept 152), while inheritance ensures a structured similarity in
the chosen aspect (Hyperseed-Concept 157). Either condition alone is insufficient: mere similarity
without reference yields accidental resemblance, and mere reference without inherited patterns yields
a bare pointer with no internal content.
    As a simple example, a written name “Paris” may refer to Paris (reference), but in a sensory
context it inherits almost none of Paris’s sensory patterns; thus it is not an icon. In a relational
context, however, it can inherit relational patterns (linked to “France,” “capital-of,” etc.), hence it
can count as a symbol. The usefulness of the definition is that it lets us treat iconic, indexical, and
symbolic representation uniformly and then specialize by aspect.


                                                   273
Remark 606. The inheritance condition is deliberately “one-way”: representations are allowed
(and usually expected) to drop patterns. Dropping patterns is what makes a representation simpler
and cheaper to manipulate.

Proposition 20 (Transitivity of representation under compositional reference). Assume the ref-
erence relation composes in the following weak sense: if Ref C (A, B|C) and Ref C (B, C|C) are non-
trivial, then Ref C (A, C|C) is nontrivial. Then representation is transitive: if A represents B in
aspect C and B represents C in aspect C, then A represents C in aspect C.

Remark 607. In plain terms: if A stands for B, and B stands for C, then (under a mild assump-
tion on how reference chains behave) A stands for C. This is the familiar idea that representations
can be layered: a mental image can represent a drawing which represents an object; a symbol can
represent a definition which represents a concept; and so on. In particular, the “mild assumption”
is doing the standard compositional work one expects of any usable notion of reference: when one
token is used via another to pick out a target, the mediated link is still a bona fide instance of
reference rather than a mere accidental correlation. The point is not that every associative chain
composes (spurious co-occurrences should not), but that the chains that satisfy the definition’s ref-
erence clause are closed under concatenation.
    What may be slightly surprising is that we also get the inheritance part “for free” by order
transitivity: if each layer only drops patterns, then the composite also only drops patterns. Put
another way, if passing from C to B forgets (at most) some structure and passing from B to A
forgets (at most) some additional structure, then passing from C to A cannot have introduced any
new structure not already present in C; it can only have forgotten what the intermediate steps forgot.
This is the precise sense in which “pattern inheritance” behaves like information monotonicity along
a pipeline.
    This proposition connects the present section to later ones in two ways. First, prediction and
control will often operate on multi-step representational pipelines, so transitivity ensures that the
end-to-end token still counts as representing the target. Here one can think of a learned model
whose internal states represent latent variables that in turn represent environment-level quantities:
even if the agent only ever directly manipulates internal states, the claim guarantees that such
manipulation is still, in the defined sense, manipulation of a representation of the distal target.
Second, attention allocation may be described as choosing which representational chains to extend;
transitivity guarantees that extending a chain does not break representation, provided reference com-
poses. This matters because attention policies often introduce new intermediate codes (additional
“layers”), and we want a criterion under which adding such codes preserves representational status
rather than requiring a fresh justification from scratch at each extension.

Proof. By assumption, nontrivial reference composes. Here “nontrivial” rules out degenerate cases
in which everything is taken to refer to everything (or reference is satisfied vacuously); the intended
assumption is that whenever (A, B) and (B, C) meet the reference clause of Definition 167, then
so does (A, C). This isolates the reference-conjunct from any additional constraints coming from
inheritance and makes clear that the compositional step is a closure property of the reference
relation itself.
    For inheritance, if SigC (A|C) ≤ SigC (B|C) and SigC (B|C) ≤ SigC (C|C) pointwise, then by
transitivity of ≤ we have SigC (A|C) ≤ SigC (C|C) pointwise. The word “pointwise” is essential: it
means that for each coordinate (each pattern-dimension tracked by the signature), the inequality
holds separately, so inequalities can be chained coordinate by coordinate without any need for
aggregation or weighting. In particular, nothing like convexity, linearity, or an averaging argument
is required; the conclusion follows purely from the order structure on the codomain of SigC (· | C).

                                                 274
    Thus both the reference and inheritance conditions of Definition 167 hold for (A, C). Equiv-
alently, the composite map from C-relevant patterns to those preserved in A factors through B
but does not depend on which factorization is chosen: any intermediate layer that merely deletes
patterns cannot enable A to exceed C in signature strength.

Proof sketch. The proof separates the two conjuncts in the definition of representation. Reference
transitivity is assumed directly. Inheritance transitivity is obtained by chaining pointwise inequali-
ties of pattern signatures. One can regard this as a “two-channel” argument: the semantic channel
(reference) composes by hypothesis, while the structural channel (inheritance) composes because
it is expressed as an order constraint, and orders are designed to support such chaining.          

Remark 608. The key move is the pointwise ordering on signatures: it turns “inherits patterns”
into an ordinary order-theoretic statement. Once that translation is made, the proof becomes an
instance of the simplest Russellian principle: if a ≤ b and b ≤ c then a ≤ c. Visually, one can
picture signatures as vectors in a positive cone and inheritance as coordinatewise domination; then
domination is clearly transitive. In more concrete terms, if each coordinate tracks the salience,
presence, or strength of a given pattern relative to C, then “X inherits patterns from Y ” means X
does not score higher than Y on any such coordinate, i.e. X never claims to preserve a pattern more
strongly than its source. The positive-cone picture is helpful because it emphasizes that we are not
comparing vectors by length or angle (which could behave non-monotonically under composition),
but by the product order, for which transitivity is immediate.
    It is also worth noting what this does not require. The argument does not assume that any
layer is lossless, only that loss is monotone in the sense captured by ≤. Nor does it require that
signatures be complete descriptions of internal states; they only need to be the features relevant to
the inheritance clause. As long as inheritance is expressed as coordinatewise non-increase of these
features, any number of intermediate representational formats can be inserted without endangering
the inheritance relation from the initial target to the final token.

13.5    Semiotic modes: icon, index, symbol
Hyperseed adopts a simple Peircean triad [14]. All three modes are special cases of representation,
distinguished by which aspect C is being preserved. In this framing, the triad is not a claim that
there are three disjoint kinds of things “in the world,” but that there are three recurring emphases
in how a token functions as a representation: it may primarily preserve sensory patterning, spa-
tiotemporal placement, or relational constraints. Which mode is appropriate can therefore depend
on the analytic choice of aspect C (and thus on what the agent is treating as relevant structure)
rather than on the token alone.

Definition 168 (Sensory, spatiotemporal, and relational aspects). Assume the context poset Ctx
contains (at least) three marked sub-posets:

• Ctxsens (sensory domains),

• Ctxst (spatiotemporal positioning domains),

• Ctxrel (relational/network domains).

These need not be disjoint; a single context may mix multiple concerns.

Remark 609. This definition is a convenience: it declares three families of aspects that correspond,
roughly, to “how it looks/feels,” “where/when it is,” and “how it relates.” The sub-posets may

                                                 275
overlap because real representational systems rarely separate these cleanly: a perceptual token may
encode both sensory features and spatial location, and a symbol may have sensory typography. What
matters is that we can talk about emphasizing one family of patterns over another when classifying a
representational mode. This prepares the ground for the icon/index/symbol definitions (Hyperseed-
Concept ??, ??, 184).
    The role of the marked sub-posets is not to constrain what representations can exist, but to
provide a vocabulary for which invariances are being appealed to when we say “A represents B.”
For instance, a single token may preserve a sensory pattern (e.g. a silhouette) while also locating an
event (e.g. a timestamped recording); the present taxonomy says that these are different represen-
tational aspects, even if realized by the same artifact. In later applications, this separation allows
one to ask whether an inference step is justified by sensory similarity, by spatiotemporal anchoring,
or by relational constraints in a model.

Definition 169 (Icon). An entity A is an icon for an entity B if there exists a sensory context
C ∈ Ctxsens such that A represents B in aspect C.

Remark 610. An icon is, in effect, a representation that preserves sensory-pattern structure. A
photograph is the standard example: in an appropriate sensory context it inherits many of the visual
patterns of its referent (though often with distortions). Another example is a melody hummed from
memory: it can be iconic of the original tune insofar as auditory patterns are preserved.
    The definition is intentionally broad about what counts as “sensory.” Many scientific and tech-
nical representations function iconically once a suitable sensory context is fixed: a spectrogram can
be an icon of an acoustic event in a visual sensory context; a plot of a signal over time can be
iconically related to the underlying process insofar as shape, periodicity, and relative magnitude
are preserved. Even schematic diagrams (e.g. circuit diagrams) can be partially iconic if the rel-
evant sensory aspect is taken to be geometric adjacency or shape-based regularities, rather than
photorealism.
    The usefulness of the definition is that it reduces “iconicity” to the general representation notion
plus a restriction on aspect. This makes it possible to treat icons within the same mathematical ma-
chinery used for symbols, rather than as an unrelated primitive. In particular, the present viewpoint
allows degrees and failures of iconicity to be stated as failures to preserve specific sensory patterns
(e.g. loss of resolution, occlusion, aliasing), rather than as a vague departure from “resemblance.”

Definition 170 (Index). An entity A is an index for an entity B if there exists a spatiotemporal
context C ∈ Ctxst such that A represents B in aspect C.

Remark 611. An index preserves spatiotemporal positioning patterns: it is a pointer, a trace, or
a coordinate-like token. A deictic gesture “that” is indexical; a memory address in a computer is
indexical; smoke can be indexical of fire when treated in a spatiotemporal/causal-trace context.
    The spatiotemporal aspect may be literal (a GPS coordinate, a clock time, a bounding box in
an image) or implemented via a proxy that is treated as preserving location-like structure (e.g.
a database key that is stable under operations interpreted as “moving through” a record space).
What matters for the present classification is that the representation is used primarily to pick out
an occurrence or region by its placement within some ordering of space, time, or traceable causal
propagation, rather than to encode its detailed sensory qualities.
    Indices are theoretically useful because they allow reference with minimal inherited content. In
many control and prediction settings, what you need is not a rich description but a stable handle
to the relevant portion of the world. Indexicality supplies this handle in a form that can later be
elaborated into richer representation by adding further aspects. This also clarifies why indexical


                                                  276
tokens often appear in pipelines: an agent may first secure an index to “the object over there”
and only subsequently attach iconic features (appearance) or symbolic labels (category, name) once
additional processing becomes available.
Definition 171 (Symbol). An entity A is a symbol for an entity B if there exists a relational
context C ∈ Ctxrel such that A represents B in aspect C. In addition, symbolic representations
are assumed to participate in a combinational system (Section 9): symbols can be composed and
recombined, and their referents are constrained by their relationships to other symbols.
Remark 612. A symbol is a representation whose salient preserved structure is relational, not
sensory. The word “electron” does not look like an electron; it inherits its meaning from the web
of relations it bears to other symbols (laws, measurement terms, mathematical operators). The
additional requirement of participation in a combinational system captures this: symbols are not
isolated labels; they live in a grammar, calculus, or graph of constraints (Hyperseed-Concept 77).
    On this view, “conventionality” or “arbitrariness” is not a separate axiom but a common con-
sequence: if what is preserved is primarily relational structure, then many different tokens could
in principle occupy the same node in the relational web without changing the role they play. Con-
versely, if the relational neighborhood changes (e.g. the inferential rules governing a term), then the
symbol’s meaning shifts even if the token’s sensory form remains identical. This matches everyday
cases in which a symbol retains its typography while acquiring new use through altered definitions,
laws, or embedding discourse.
    This definition is valuable because it connects semiotics to computation. Once symbols are com-
binable, they support systematic inference and counterfactual reasoning; hence symbolic represen-
tation is a key substrate for the later sections on prediction, causality, and control. The move also
echoes Peirce’s emphasis on the triadic, law-like mediation characteristic of symbols [14] (compare
also Hyperseed-Concept 190). A further consequence is that symbolic systems typically admit ex-
plicit notions of well-formedness and equivalence (syntactic validity, derivability, rewriting), which
can be treated as additional relational constraints internal to Ctxrel .
Remark 613. These definitions deliberately leave room for hybrid tokens. For instance, a labeled
photograph may be both an icon (sensory similarity) and a symbol (networked relationship to other
labeled items).
    Hybridity is not an exception but a common mechanism of grounding and coordination: an index
may anchor a symbolic description to a particular event, while an icon may provide a perceptual
interface for symbolic manipulation (e.g. diagrammatic reasoning where visual similarity guides
steps that are nonetheless licensed by relational rules). In practice, agents often move between
modes by changing which aspect C they treat as primary: the same token can be read iconically
(attend to resemblance), indexically (attend to location or provenance), or symbolically (attend to
its role in a combinational system).

13.6    Soggy predicates and paraconsistent truth
Hyperseed’s “soggy predicates” are intended as a bridge between: (i) fuzzy truth values attached to
predicates, and (ii) probabilistic semantics grounded in (possibly hypothetical) collections of obser-
vations. We now define soggy predicates in a way that is compatible with the [0, 1]2 (paraconsistent)
evidence domain [23, 24].
Definition 172 (p-bit-valued predicate). Let X be a universe of discourse. A p-bit-valued predicate
on X is a function F : X → [0, 1]2 . We interpret F (x) = (F + (x), F − (x)) as degrees of positive
and negative evidence for the statement “x has property F .”

                                                 277
Remark 614. A p-bit-valued predicate replaces a single truth degree with a pair of evidential
degrees: how much evidence supports the predicate and how much evidence opposes it. The notation
F + (x) and F − (x) simply refers to the first and second components of F (x), respectively. This is a
natural fit for paraconsistent reasoning: one can simultaneously have high positive and high negative
evidence without collapsing into triviality (Hyperseed-Concept 198).
    A simple example: let X be a set of patients and F (x) encode evidence that patient x has a
disease. A lab test might contribute positive evidence while a conflicting scan contributes negative
evidence. Then F (x) can legitimately be (0.8, 0.7), reflecting serious conflict rather than forcing an
artificial resolution. This is useful later because habit dynamics, prediction, and control will often
propagate and transform such evidential pairs rather than crisp truths.

Remark 615. It is helpful to keep distinct (i) evidence and (ii) truth in the classical sense. In
a p-bit-valued predicate, the pair (F + (x), F − (x)) is not required to satisfy F − (x) = 1 − F + (x),
and therefore it is not a probability assignment or a fuzzy membership degree by default. Instead,
it records two potentially independent aggregates: “how much pushes toward acceptance” and “how
much pushes toward rejection.” This independence is precisely what allows explicit representation
of conflict, as well as “informational gaps” where both coordinates are small.
    A common derived reading (not assumed, but often useful as intuition) is to view

        conflict(x) := min(F + (x), F − (x)),     ignorance(x) := 1 − max(F + (x), F − (x)),

so that (1, 0) indicates maximal support with no opposition, (0, 1) indicates maximal opposition with
no support, (1, 1) indicates maximal conflict, and (0, 0) indicates maximal lack of evidence either
way. The framework itself only commits to the evidential pair; any downstream “decision rule”
(accept/reject/undetermined) can be layered on later, depending on the application.

Definition   173 (Soggy predicate). Fix a finite observation set O and weights wo ≥ 0 with
               Assume each observation o ∈ O yields an evidential evaluation eo : X → [0, 1]2 .
P
      w
  o∈O o   = 1.
Define the soggy predicate induced by (O, w, e) as
                                               X
                                      F (x) :=     wo eo (x),
                                                 o∈O

where the sum is taken componentwise in [0, 1]2 .

Remark 616. A soggy predicate (Hyperseed-Concept 172) is,P   mathematically, just an average of
evidential evaluations across an ensemble. The normalization o wo = 1 ensures F (x) remains in
[0, 1]2 when each eo (x) does. Componentwise summation means:
                                    X                       X
                                                    −
                          F + (x) =   wo e +
                                           o (x), F   (x) =   wo e −
                                                                   o (x).
                                    o                            o

Intuitively, each o ∈ O is a possible “way of looking” (an observation, measurement, or test), and
wo measures its importance or frequency.
    A simple example: let O be a set of diagnostic tests. Each test o yields a pair eo (x) of sup-
port/opposition for “x has condition F .” Then F (x) aggregates them. This is useful for two
reasons. First, it grounds fuzzy/paraconsistent truth in an observation model, which is important
for the later philosophy-of-science stance. Second, it provides a canonical way to combine hetero-
geneous evidence without prematurely forcing complementarity; this aligns with the paraconsistent
motivation emphasized in [23, 24].


                                                 278
Remark 617.   P Because the weights (wo )o∈O form a simplex (nonnegative and summing          to 1), the
                                                                                      2
map F (x) = o wo eo (x) is a convex combination of the points {eo (x)}o∈O ⊆ [0, 1] . Thus F (x) lies
in the convex hull of the per-observation evidential evaluations, and in particular cannot introduce
out-of-range evidence values. This convexity perspective is often the right mental model: “sogginess”
amounts to pooling an ensemble of perspectives without forcing them to agree.
    In the intended applications, O can be read either extensionally (a literal finite set of mea-
surements) or intensionally (a finite set of measurement types or contexts). Correspondingly, the
weights wo can be read as empirical frequencies, reliabilities, priors over contexts, or (in engineered
settings) design choices that allocate attention among sensors or sub-models.
Remark 618. Soggy predicates are “simple observation grounded” in the sense that F (x) is the
(weighted) average evidential assessment over an ensemble of observations. The ensemble O need
not be the mind’s actual observations; it may encode hypothesized observations, cultural priors, or
counterfactual experiments.
Remark 619. The finiteness of O is a convenience rather than a deep restriction: it ensures the
sum is elementary and avoids measure-theoretic overhead. Conceptually, one can regard (O, w)
as a finite probability space on “observation modes” and eo (x) as a random evidential evaluation;
then F (x) is the expectation of that random evaluation. This probabilistic reading is deliberately
weak: it treats weights as a bookkeeping device for aggregation, without requiring that the evidential
coordinates themselves be probabilities.
Proposition 21 (Probabilistic semantics as a special case). Suppose that for every observation
o and entity x the evidence is complementary, meaning e−                       +
                                                                o (x) = 1 − eo (x). Then the induced
                              −                +                       +
soggy predicate F satisfies F (x) = 1 − F (x) for all x. Thus F (x) can be read as an ordinary
fuzzy membership degree in [0, 1] and, if e+ o (x) are interpreted as per-observation probabilities, then
F + (x) is the expected probability of satisfaction.
Remark 620. This proposition says that the paraconsistent framework strictly generalizes the
familiar probabilistic (or fuzzy) one. If every observation insists that “negative evidence is exactly
one minus positive evidence,” then the two-coordinate representation collapses back down to a single
number, and soggy predicates become ordinary expectations. This is important because it reassures
us that we have not abandoned classical semantics; we have merely stopped assuming that the world
(or the observer) always provides perfectly complementary information.
    The result connects backward to the earlier probability-flavored phrasing of habits (Section 12.1)
and forward to prediction and control (Section 14), where one may sometimes choose to work in
the complementary subcase for convenience.
Remark 621. The complementarity assumption e−                   +
                                                     o (x) = 1−eo (x) can be understood as embedding
                                                   2
a single scalar evaluation into the square [0, 1] via the diagonal map p 7→ (p, 1 − p). Under
this embedding, the soggy construction commutes with averaging: averaging on the diagonal in
[0, 1]2 is the same as averaging in [0, 1] and then re-embedding. In this sense, soggy predicates are
“conservative” over ordinary fuzzy/probabilistic semantics: the extra coordinate does not change
anything when the data already lives on the diagonal, but it becomes available when the data departs
from complementarity.
     It is also worth noting what complementarity rules out: if two observations deliver eo1 (x) =
(0.9, 0.1) and eo2 (x) = (0.1, 0.9), then each observation is individually complementary, yet the
disagreement between observations is not represented as within-observation conflict; rather, it man-
ifests as uncertainty in the aggregate when averaged. By contrast, genuinely paraconsistent evidence
allows an individual observation mode (or model) to carry its own internal tension, e.g. (0.9, 0.8),
which is a different phenomenon than mere inter-observation disagreement.

                                                  279
Proof. Compute componentwise:
                    X              X                       X
          F − (x) =   wo e −
                           o (x) =   wo (1 − e+
                                              o (x)) = 1 −   wo e+            +
                                                                 o (x) = 1 − F (x).
                       o               o                        o




Proof sketch. Use the complementarity
                          P              assumption e−          +
                                                      o = 1 − eo inside the weighted sum, then pull
out the constant 1 using o wo = 1.                                                                
                                                                               P
Remark 622. The   P decisive step is the normalization of weights. Without o wo = 1, one would
obtain F − (x) = ( o wo ) − F + (x) instead. Geometrically, complementarity restricts evidence pairs
to the diagonal line v − = 1 − v + in the unit square; averaging preserves this line, so the soggy
predicate stays on the diagonal and can be identified with its first coordinate.

Remark 623. In later sections, it is sometimes useful to treat F as defining a family of classical
predicates by thresholding one or both coordinates, e.g. “accept F at level α” meaning F + (x) ≥ α
(support-based), or “reject F at level β” meaning F − (x) ≥ β (opposition-based), or a three-way
policy that separates accept/reject/undecided by simultaneously requiring high support and low oppo-
sition. The point of the soggy construction is that such policies can be formulated after aggregation,
once the evidential landscape is explicit, rather than being silently forced by an assumption of com-
plementarity at the outset.
    Moreover, because F is an affine combination of the eo , any downstream affine transformation
of evidence (for example, a linear calibration map applied to each observation mode) can be moved
inside the sum when convenient. This algebraic flexibility is part of why soggy predicates behave
well as building blocks for habit-updates and for compositional models of perception.

Remark 624. The point of the [0, 1]2 form is that complementary evidence is not required. A mind
may have strong positive and strong negative evidence simultaneously for the same predicate (con-
flict), or may have neither (lack of evidence). Soggy predicates simply average such evidence profiles
over an observation ensemble. In particular, the two coordinates can be read as independently ac-
cumulated support-for and support-against signals, rather than as probabilities that must sum to
one. This makes room for familiar cognitive situations: perceptual ambiguity (both channels low),
illusion or misinformation (high negative evidence against a claim that is nevertheless asserted),
and genuine inconsistency in a knowledge base (both channels high due to incompatible but salient
cues). Averaging over an ensemble should be understood as smoothing over time, viewpoints, or
sub-systems (e.g. different sensory modalities), so that a “stable” soggy predicate can coexist with
momentary spikes of conflict without forcing an immediate collapse to a single bivalent verdict.

13.7    Micro-example: registering and representing a pattern
We illustrate the chain

                           external pattern → registration → representation

on a minimal finite instance, aligned with the toy universe style of Section 5. The intent is to
separate (i) what is present in the external entity, (ii) what the sensory apparatus can extract in
a particular situation, and (iii) what the cognitive system subsequently stabilizes as a manipulable
internal item. Even in this minimal setting, the example shows that “representation” is not a single
relation but a family of context-indexed relations, each preserving different structural constraints.


                                                 280
Example 13 (Icon, index, and symbol for one referent). Let U contain an external entity B.
Assume a mind M has a sensory subsystem S that registers B in a sensory context Csens ∈ Ctxsens .
Registration produces a token ricon ∈ R whose sensory signature matches a subset of B’s sensory
signature, i.e. SigCsens (ricon ) ≤ SigCsens (B). Here the order ≤ can be read as “no more detailed than”
or “contained within” the external signature as constrained by the context (e.g. limited resolution,
occlusion, viewpoint, or modality). Thus, even when B has a rich sensory profile, the registered icon
may preserve only a small pattern family (edges but not texture; pitch but not timbre; silhouette but
not color), and the context index specifies which family is being compared. If Ref Csens (ricon , B|Csens )
is nontrivial, then ricon is an icon for B. Nontriviality can be taken to rule out purely accidental
resemblance or degenerate cases where the token fails to track B at all in that context (e.g. noise
that happens to match a feature).
    Now suppose the same registration also yields a spatiotemporal pointer token rindex ∈ R (e.g.
“the thing at location ` at time t”), with nontrivial reference in some Cst ∈ Ctxst . Then rindex
is an index for B. The index need not share sensory features with B; its fidelity is instead to
the coordinate structure of the spatiotemporal context (tracking, co-location constraints, persistence
conditions, and so on). This makes explicit how a mind can keep track of “that thing there” even
when the iconic channel is weak or corrupted, and conversely how an icon may be vivid without
being anchored to a stable pointer.
    Finally, suppose M maintains a relational knowledge graph in a context Crel ∈ Ctxrel . A new
node token rsym ∈ R is introduced into this graph and linked via learned relations (e.g. “is-a”, “part-
of ”, “causes”). If rsym represents B in Crel and participates in the graph’s combinational operations
(composition/inference rules), then rsym is a symbol for B. The emphasis on participation is
crucial: the symbol is not merely a label, but a handle that supports rule-governed recombination
(e.g. inheritance along “is-a”, constraint propagation along “part-of ”, or abductive links along
“causes”). In this sense the symbol preserves a pattern family that is primarily relational rather
than sensory or spatiotemporal, and its adequacy is tested by the success of downstream inferences
rather than by immediate resemblance.
    In this way, one referent B can simultaneously have iconic, indexical, and symbolic represen-
tations within the same mind, each preserving different pattern families. The three tokens may be
created together by a single episode, but nothing in the setup requires a one-to-one correspondence:
a single referent can spawn many icons (different viewpoints), many indices (different tracking
frames), and many symbols (different conceptual roles), and conversely a single token can some-
times serve multiple roles when contexts align.

Remark 625. This example highlights why the aspect index C is not decorative. The same ref-
erent B can generate three tokens with three different “fidelities,” each faithful in its own slice of
structure. The icon inherits sensory patterns; the index inherits spatiotemporal patterns; the symbol
inherits relational patterns and gains power from combinational constraints. In realistic cognitive
architectures, these modes interact: symbols can cue imagery, indices can anchor symbolic facts,
and icons can be annotated symbolically. The present formalism supports that interaction precisely
because all modes are instances of the same representation schema. More formally, the context
index indicates (i) which signature map is in play, (ii) which reference conditions count as non-
trivial tracking, and (iii) which transformations are licensed as “structure-preserving” within that
mode. Interactions across modes can then be modeled as context-bridging operations (e.g. an index-
to-symbol update that binds a pointer to a graph node, or a symbol-to-icon query that retrieves a
stored prototype), rather than as an informal mixing of incomparable representational types. This
also clarifies how conflict can arise and be managed: an icon may strongly support a property
while the symbol-graph entails its negation, yielding the kind of simultaneous positive and negative


                                                   281
evidence that motivates the soggy/paraconsistent treatment above, without forcing an immediate
collapse of either representational channel.

13.8    What this buys us for later sections
This section sets up the representational vocabulary needed for later parts of the paper: in particu-
lar, it provides a disciplined way to move between (a) causal interaction with the world, (b) internal
state that carries information across time, and (c) the system’s own graded assertions about what is
the case. The payoff is that later sections can rely on these distinctions without having to re-argue
them each time, and can state claims in a way that is stable under changes of implementation
details (e.g. the chosen evidence calculus).
• In Section 14, prediction and control can be defined over representations, with sensory registration
  providing the perception channel. This means that what gets predicted (and what gets steered) is
  not raw stimulation as such, but the system’s internal stand-ins that persist and can be compared,
  composed, and acted upon; registration then functions as the principled interface by which the
  environment constrains and corrects those stand-ins.

• In Section 15, attention can be modeled as selective updating of subsets of the representa-
  tion/predicate network. On this framing, “attention” is not a mysterious extra faculty but a
  policy over which representational tokens and which predicate-attachments are revised given
  new registrations; this makes it natural to treat attentional bottlenecks and synergy effects as
  properties of update locality, bandwidth, and coupling between subnets.

• In Sections 16 and 17, self models and reflective content will be formalized as representational
  fixed points and higher-order registrations (e.g. “M registers that M registers A”). The fixed-
  point language is intended to capture the way a stable “self” representation can be maintained
  even as particular subordinate representations change, while higher-order registration provides
  a uniform syntax for reflexive and meta-level content (for example, when the system not only
  registers A but also registers something about its own registering of A).
Remark 626. In philosophical terms, we have separated three layers that are often conflated: (i)
the world’s impact on a system (registration), (ii) the system’s stabilized internal stand-ins (rep-
resentation tokens), and (iii) the evidential grading of assertions about entities (soggy predicates).
This separation is what permits later sections to talk rigorously about agency: prediction and con-
trol operate on representations, attention shapes which representational subnets are updated, and
reflective consciousness can be treated as iterated registration/representation operating on the sys-
tem itself (Hyperseed-Concept 166, 85). A useful way to read (i)–(iii) is as a progression from
causal contact, to internal re-identification, to doxastic stance: registration is the “impression” or
incoming constraint, representation tokens are the stabilized carriers that allow re-use and cross-
context comparison, and soggy predicates express not just whether a claim is stated but how strongly
it is supported given the system’s currently available registrations and representational structure. In
particular, soggy predicates make room for the possibility that the same representation token can be
maintained while its evidential status shifts (e.g. strengthened, weakened, or put into tension by new
registrations), which will matter later when we discuss conflict, revision, and partial observability.
     Mathematically, the benefit is modularity: one may change the evidence domain (e.g. Boolean,
probabilistic, p-bit-paraconsistent) or change the context poset, while keeping the same definition-
shape of mind, perception, and representation. This is a recurring theme in the Hyperseed program
[1]. Concretely, the definitions are arranged so that (a) representation-management operations (e.g.
prediction, control, and selective update) depend primarily on the abstract interfaces provided by

                                                 282
the chosen evidence domain and context structure, and (b) the perception channel can be treated as
a morphism-like linkage from registrations into representational updates. As a result, later claims
can be phrased at a level where one can swap out, for instance, a crisp two-valued evidential seman-
tics for a graded or paraconsistent one, and still interpret the same formal roles for “perception,”
“belief-like grading,” and “self-referential registration” without rewriting the surrounding conceptual
architecture.


14     Prediction, attraction, causality, and control
14.1    From patterns to forecasts and interventions
Sections 9–13 built a scaffold in which an observer/context O (a mind, or a mind-plus-environment
slice) (i) makes distinctions, (ii) registers patterns, (iii) organizes those patterns into hierarchies/webs,
and (iv) maintains representations whose content is indexed by contexts and aspects.
    This scaffold is intentionally descriptive: it explains how a structured “world of patterns” can
be available to an observer, without yet committing to any particular stance on time, action, or
counterfactual dependence. In particular, the indexing-by-context machinery implies that what
counts as “the same” pattern may vary with aspect (what features are being attended to) and
with the surrounding representational commitments (what background regularities are currently
assumed). Forecasting and intervention add further structure: they require that the observer’s
stored patterns be usable not only as compressions of what has been registered, but also as guides
to what is likely, what is avoidable, and what is achievable under feasible actions.

Remark 627. In the Hyperseed framing, the passage from “patterns” to “agency” is not a meta-
physical jump but a change of grammatical tense: we move from describing what is coherently
present to describing what is expected to become present, and what may be made to become present
by action. This shift is precisely what brings prediction, control, and therefore causality into focus,
and it connects the pattern-oriented representational layer to the later resource-bounded attentional
layer (Section 15). See [1, 5] for the motivating ontology-level narrative.

    One can read this “tense shift” as adding a minimal temporal semantics to the representational
architecture: patterns are no longer merely relations among currently co-present distinctions, but
also constraints on transitions between contexts. In that sense, the same representational web
that supports recognition (“this looks like that”) is repurposed into a transition model (“from
here, that tends to follow”). Likewise, the same distinction-making that supports categorization
is repurposed into a space of candidate interventions: an “action” is, at minimum, an internally
available distinction whose enactment changes which subsequent contexts become accessible.
    This section adds the “forward arrow” needed for agency: prediction (how likely are future
patterns/events?) and control (how can actions steer future patterns/events?), as well as the
intermediate notion of causality (Hyperseed-Concept 70).
    A useful way to separate these three is by their roles, not their vocabulary. Prediction concerns
inference under uncertainty: given present context/aspects and available evidence, what distribu-
tion over future distinctions is warranted? Control concerns selection under constraints: given
possible actions and limited resources, which action policies best steer the distribution of future
contexts toward desired regions? Causality, in this framing, is the bridge that makes control non-
magical: it is the claim that some distinctions (candidate actions, conditions, or structural changes)
make a systematic difference to future patterns beyond mere co-occurrence, thereby licensing in-
tervention planning rather than passive extrapolation.


                                                   283
    Hyperseed’s key move here is to make the dependence notions explicitly differential. For decision
making, what matters is rarely P (B | A) by itself, but rather how different P (B | A) is from
P (B | ¬A). This is packaged in the notions of attraction, predictive implication, and predictive
attraction (Hyperseed-Concept ??).
    Concretely, a non-differential statement like “B is likely” can be true in a way that is irrelevant
to agency: B may be likely regardless of what the agent does, because of background regularities
that dominate the dynamics. Differential dependence, by contrast, asks whether A changes the
likelihood of B relative to a baseline, where the baseline is typically “not A” or “the default
policy” in the given context. This is why notions like attraction naturally support ranking and
prioritization: if two candidate actions both yield high P (B | A), but one of them yields only a tiny
improvement over P (B | ¬A), then that action carries less leverage and is typically less valuable
for control.
    It is also where the representational indexing by context matters operationally. The quantities
P (B | A) and P (B | ¬A) are only meaningful relative to a specified evidential context, including
which aspects are held fixed, which are allowed to vary, and which background conditions are
treated as stable. Thus, the “difference” being computed is not merely a numerical subtraction
but a context-sensitive comparison between two nearby worlds (or two nearby policy regimes) as
represented by O. When later sections introduce resource-bounded attention, this contextuality
becomes even more pronounced: an agent may only be able to approximate such differences using
compressed, aspect-limited summaries of the evidence.
    From the standpoint of interventions, it is often helpful to distinguish evidential conditioning
from interventional forcing: P (B | A) can be high because A is a symptom of hidden causes,
even if setting A would not increase B. Hyperseed’s “control” reading therefore implicitly invites
a distinction between “observing A” and “doing A”—the latter corresponding to an intervention
that breaks certain background dependencies. Even when the formalism is written in ordinary
conditional-probability terms, the intended use is counterfactual: the agent is comparing what
happens under a contemplated action to what would have happened without it, within the same
contextual slice.

Remark 628. The differential stance is philosophically modest but practically decisive: it acknowl-
edges that many future outcomes are overdetermined by background regularities, and that an agent’s
action matters only insofar as it tilts the odds relative to what would have happened otherwise. This
is also where ordinary probability talk (Hyperseed-Concept 139) becomes insufficient on its own: in
borderline, vague, or internally conflicted contexts, we often possess evidence both for and against
an event, and the difference between conditional propensities must be computed from that evidence
rather than assumed crisp at the outset. Paraconsistent treatments of evidence streams of this sort
are developed in various logical settings; see, e.g., [23, 24].

    A further pragmatic consequence is that differential notions can be estimated and improved
incrementally. An observer may begin with crude qualitative comparisons (“A seems to help B”)
and refine them into more stable graded relations (“A attracts B more strongly than A0 does”) as
additional evidence accumulates, aspects are reweighted, or confounders are represented explicitly.
In this sense, attraction-like quantities function as “handles” for learning and control: they are
directly tied to what changes when the agent changes something, and thus to the empirical signature
of agency within a pattern-based world-model.




                                                 284
14.2    Event types, timelines, and paraconsistent occurrence data
We assume the temporal scaffolding from Section 7: a (possibly branching, partially ordered)
timeline (T, ) for a given context/observer, where t  t0 means “t is not later than t0 as experi-
enced/represented by O.”

Remark 629. The notation (T, ) should be read as follows: T is a set of time indices, and  is a
partial order encoding the observer’s “before/after” structure (Hyperseed-Concept 142). The possi-
bility that  is not total allows branching and incomparability, which is useful when the observer’s
model has multiple consistent continuations or when retrospective reconstruction leaves some order
relations undecided.

Remark 630. It is helpful to keep three distinct readings of t ∈ T in mind, depending on the
application: (i) t may be a physical clock reading (as in sensor timestamps), (ii) t may be an
internal computational step or belief-state index (as in an agent’s recurrent update cycle), or (iii) t
may be a reconstructed “scene time” used to order remembered or narrated events. The partial order
 is deliberately flexible enough to cover all three cases while remaining agnostic about whether time
is continuous, discrete, or hybrid.

Remark 631. When  is partial, one can still speak about histories (or branches) as chains H ⊆ T
such that any two elements of H are -comparable. Many constructions later can be understood
as first restricting attention to a particular chain H (a single “possible continuation” as tracked
by O), and only then applying sequence-like reasoning. This is one way to connect branching time
intuitions with sequence-based prediction rules.

Definition 174 (Event types and event tokens). Let E be a set of event types (also called “event
predicates”), such as kiss(Ben) or get(ball). An event token is a pair (A, t) with A ∈ E and
t ∈ T . We write A@t for “event type A occurs at time t.” We assume the event language is closed
under a formal negation operator A 7→ ¬A, read as “not A”. Because boundaries may be vague or
inconsistent, it is allowed that both A@t and (¬A)@t carry substantial evidence.

Remark 632. Intuitively, an event type is a reusable description (a predicate schema), while an
event token is a particular alleged occurrence located at a particular time index. The notation A@t
is a compact “addressing” convention: it keeps the type A and the time t visible so we can talk
about temporal relations between occurrences.

Remark 633. The operator ¬ is treated here as syntactic negation: it simply forms a new event
type ¬A from A. In particular, we do not assume that ¬A exhausts all alternatives to A, or
that it behaves like a classical complement with respect to evidence. This matters in practice: for
many perceptual or social predicates, “not A” is not a well-delimited natural kind, and the observer
may have independent reasons to support both A and ¬A (e.g., due to incompatible measurement
channels or shifting criteria of application).

Remark 634. A simple example is: let A =get(ball) and let t be the moment a camera frame
shows a hand grasping a ball. Then A@t is the token claim “the ball is gotten at time t.” If the
camera view is occluded, one may simultaneously have evidence for A@t (a motion consistent with
grabbing) and for (¬A)@t (no clear visual confirmation). Allowing both is not a flaw here; it is a
way of keeping track of the epistemic situation without prematurely forcing a crisp boundary between
“occurs” and “does not occur.” This connects back to Hyperseed’s emphasis on distinction-making
as observer-relative (Sections 3 and 13).


                                                 285