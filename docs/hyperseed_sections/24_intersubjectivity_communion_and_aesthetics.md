# 24 Intersubjectivity, Communion, and Aesthetics

whose value Aff(a, e) represents (paraconsistent) evidence that performing a using the artifact tends
to produce effect e within the relevant context.

Remark 1284. The use of tokens emphasizes that A and E are modeling choices rather than
metaphysical primitives. An action token may be low-level (a torque command), mid-level (a ges-
ture), or high-level (“compile and run test suite”); similarly an effect token may be a raw state
transition, a perceptual event, or a constraint satisfaction statement (“object is aligned”). The ap-
propriate granularity depends on O and on the explanatory task: for fine motor control one might
refine A to continuous commands, whereas for social or institutional tools one might coarsen A to
normative or procedural actions (“submit form”) and let E encode institutional state changes (“re-
quest accepted”). This flexibility is also what lets the same mathematical object cover both embodied
tools (hammers) and informational tools (calculators, software libraries) without forcing a single
privileged ontology of actions and effects.

Remark 1285. Intuitively, Aff(a, e) is an “action-to-effect” interface description: it says what the
artifact makes easy, difficult, reliable, unreliable, encouraged, or resisted. The codomain V = [0, 1]2
is the p-bit evidence space used throughout Hyperseed: the first coordinate is positive evidence
and the second is negative evidence. Thus an affordance can be simultaneously supported and
undermined by experience, reflecting the common situation that a tool can work well in some contexts
and fail (or be dangerous) in others. This is one instance of Hyperseed-Concept 86 interacting with
Hyperseed-Concept 191.
    A simple example is a lever used to lift a weight: an action token might be “apply downward
force at distance d from fulcrum,” and an effect token might be “weight rises by ∆h.” One expects
strong positive evidence for that action-effect pair in ordinary mechanical contexts, but one may also
have nontrivial negative evidence (slippage, breakage, user error). Another example is a password
manager: an action token might be “request credentials for site s,” and an effect token might be
“credentials filled into browser form”; again, positive evidence may coexist with negative evidence
when the environment is hostile or the tool is misconfigured. Formally, the point of Aff is that it
allows us to treat a tool as a morphism-like object mediating between an action vocabulary and an
effect vocabulary, which is exactly what later sections will need when tools become participants in
social and intersubjective systems.

Remark 1286. The “morphism-like” phrasing is meant operationally: Aff behaves like an interface
that can be compared, composed, and substituted. For example, if one tool T1 maps actions to an
effect token that is itself an action token for another tool T2 (e.g. “produce a tightened screw” as a
precondition for “mount a circuit board”), then one can model multi-tool workflows by composing
their affordance profiles at the level of shared intermediate tokens. Even when such strict token
matching is unavailable, coarse-graining and refinement mappings between token sets can be used to
relate affordance profiles across levels of description (e.g. translating a family of low-level controller
actions into a higher-level macro-action).

Remark 1287. The paraconsistent encoding in V = [0, 1]2 can also be read as separating two
kinds of observations: evidence for the claim “a tends to produce e” and evidence against it. This
separation is useful when the world is nonstationary or heterogeneous: repeated success in one
subcontext does not erase repeated failure in another, and both should remain available for context-
sensitive inference. In practice, one can interpret Aff(a, e) as a summary of experience under O
(counts, weighted frequencies, model-based estimates), and later decision procedures can condition
on additional context variables or aspects to resolve when the positive versus negative component
should dominate.


                                                   509
Remark 1288. The affordance profile is a compact interface between the (agent-relative) action
vocabulary and the (context-relative) effect vocabulary. In practice, Aff can be learned from inter-
action data, derived from physics models, or constructed compositionally from sub-artifacts.
Remark 1289. Learning Aff from interaction data can be understood as estimating a structured
action–effect relation under partial observability. For instance, given logs of attempted actions and
observed outcomes, one may update positive evidence when e is observed after a, and update negative
evidence when e fails to occur or when an incompatible effect occurs. When the relevant effects occur
with delay, one can either expand E to include temporally extended tokens (e.g. “achieved within
τ ”) or treat Aff as summarizing an induced policy-conditional transition model over an appropriate
time window. This keeps the definition agnostic about the details of time, memory, and credit
assignment, while still letting later sections talk about tools in a uniform vocabulary.
Definition 381 (Tool). A tool (relative to an agent class and an observer/context O) is an entity
T in a reality-system together with an affordance profile Aff T that is:
(a) usable: there exists a nontrivial subset AT ⊆ A and effects ET ⊆ E such that Aff T (a, e) has
    substantial positive evidence for some (a, e) ∈ AT × ET ; and

(b) purpose-supporting: for some objective functional (Section 18), the availability of T strictly
    increases expected objective achievement for typical users in the class, via the induced action-
    effect couplings.
Remark 1290. The “nontrivial” qualifier in the usability clause is intended to rule out degenerate
cases where AT or ET contains only vacuous tokens (e.g. an action that is never available to the
agent, or an effect that is always true regardless of action). Intuitively, a tool must open up at least
some meaningful region of action–effect space that was previously absent or less reliable. Depending
on the application, “substantial positive evidence” can be instantiated as a threshold on the positive
coordinate of Aff T (a, e), a gap between positive and negative evidence, or a downstream decision-
theoretic criterion tied to improved control.
Remark 1291. The purpose-supporting clause is deliberately phrased in terms of expected objec-
tive achievement to allow tools that are beneficial in aggregate despite occasional failures, and to
allow tools that shift risk profiles rather than deterministically guaranteeing outcomes. The reference
to “typical users” acknowledges that toolhood is relative not only to O but also to a distribution over
user skills, training, and embodiment: a lathe may be purpose-supporting for a trained machinist
but not for a novice; a user interface may be purpose-supporting for sighted users and not for blind
users unless paired with assistive technology. This connects directly to the motivating theme that
tools are part of embodied computation: their effective affordances depend on bodily and cognitive
properties of the agent class.
Remark 1292. The usability clause prevents “tools” from including arbitrary inert objects whose
action-effect links are too weak to matter; the purpose-supporting clause prevents us from calling
every causal mediator a tool (e.g. a random obstacle) unless it helps with some objective. In plainer
language: a tool is something that makes some intended outcomes easier or more reliably achievable
for some class of agents, relative to an observer/context.
    Examples: a hammer is a tool because it supports the objective “join two pieces of wood” by
increasing the probability of the effect “nail is driven” for actions in a natural user action set.
A microscope is a tool because it supports objectives that require fine perceptual distinctions by
reliably producing effects like “image reveals small-scale structure,” thus interacting with Hyperseed-
Concept 134 and Hyperseed-Concept 98. The usefulness of this definition is that it makes “toolhood”

                                                  510
a property that can be discussed in the same formal vocabulary as tasks and values: it becomes
possible to compare tools by their affordance maps and by the induced changes in expected objective
achievement.
Remark 1293. This framing also clarifies why “tool” is not synonymous with “technology” or
“artifact.” An entity may be technologically sophisticated yet fail the purpose-supporting clause
for a given objective functional (e.g. a complicated gadget that distracts rather than helps), and
conversely a simple artifact (a wedge, a string) may be a powerful tool relative to an agent class
and objective. Moreover, a single physical object can implement multiple tools depending on which
affordance profile is salient: a smartphone can be a camera, a map, a payment instrument, or a
distraction source, each corresponding to different subsets of A and E and different induced changes
in objective achievement.
Remark 1294 (Tools as patterns that extend agency). Earlier sections treated agency as closed-
loop control (Section 14) and tasks as externally specified objective-achievement problems (Sec-
tion 21). A tool is then an engineered pattern-system that enlarges the agent’s effective action set
(or reduces the effort of actions) by adding new reliable couplings from actions to effects.
Remark 1295. In this sense, tools can be seen as externalized “affordance morphisms” that restruc-
ture the agent’s reachable set in state space: they do not merely add raw power, but reparameterize
control. A steering wheel converts small hand rotations into large changes in vehicle trajectory;
a search engine converts short text queries into high-probability access to relevant information; a
musical instrument converts constrained gestures into complex acoustic effects. In each case, what
matters for agency is the induced mapping from a feasible action alphabet to a task-relevant effect
alphabet, not the internal mechanism by which the artifact accomplishes the transformation.
Remark 1296. Note the deliberate observer-relativity: “tool” is not asserted as an intrinsic
essence, but as a role an entity plays in a coupled system of agent, objective functional, and con-
text. This is consistent with Hyperseed’s general stance that many ontological tags are relative to
an observer/context and a modeling purpose [1].
Remark 1297. Observer-relativity also helps separate two questions that can otherwise be con-
flated: (i) whether an entity can mediate certain action–effect couplings (a descriptive claim about
the reality-system under O), and (ii) whether those couplings are counted as the entity’s affordances
in a given modeling task (a choice of A, E, and the relevant aspect of context). For example, a rock
affords “smash” in a coarse-grained model of improvised tools, but in a fine-grained safety-critical
model its negative evidence for controlled, repeatable effects may dominate, changing whether it is
treated as a tool for the objective at hand. This explicit separation is one reason the affordance pro-
file representation remains useful when the discussion later shifts to social tools (protocols, norms,
institutions) whose “actions” and “effects” are themselves observer- and context-mediated.

23.3    Machines as internally patterned tool-systems
Hyperseed distinguishes machines from generic tools by emphasizing that the causal interactions
among parts of a machine form a pattern in the machine’s overall behavior. Put differently, a
machine is not merely used by an agent to produce an effect; it is also a system whose internal
use-relations (parts acting on parts) are engineered so that the whole has a robust, repeatable mode
of operation.
Definition 382 (Machine). A machine is an engineered physical system M (Definition 383) that
can be decomposed into components (Mi )i∈I such that:

                                                 511
(a) each component Mi is (typically) a tool for acting on other components; and
(b) the internal causal interaction structure among the components induces a stable input-output
    behavior of the whole M that exhibits nontrivial patterns (Section 9) with high intensity relative
    to the decomposition baseline.
Remark 1298. In ordinary speech, a machine is often “a tool with moving parts.” The formal
definition refines this: a machine is a network of tools acting on each other in such a way that the
composite behavior is stable and patterned. The phrase “patterns with high intensity” appeals to the
earlier formalization of pattern and emergence [5]; the idea is that the overall behavior is not merely
a bag of componentwise behaviors, but a structured regularity that survives perturbation and supports
prediction and control (Hyperseed-Concept 130 and Hyperseed-Concept ??). In particular, “relative
to the decomposition baseline” indicates that the relevant comparison is not against an arbitrary
null model, but against what one would expect if the components were only weakly coordinated (e.g.,
if they acted largely independently, or if their couplings were randomly rewired while keeping the
same parts). On this view, a system qualifies as a machine not merely because it is complicated,
but because its couplings constrain the accessible behaviors into a smaller, more regular family: the
whole exhibits a characteristic repertoire of operation that can be recognized, reproduced, and relied
upon.
    Examples: a mechanical clock decomposes into gears, springs, and escapement components that
constrain each other; the high-intensity pattern is periodic motion and reliable timekeeping. A
modern CPU decomposes into logic gates and subsystems; the high-intensity pattern is reliable
execution of instruction semantics under a clocked discipline. One may also view a bicycle as a
machine in this sense: its components (frame, chain, sprockets, bearings, brakes) are individually
tools that act on each other to yield a stable input-output relation between rider-applied forces and
predictable motion/steering/braking, with the “pattern” being the constrained dynamics that make
riding learnable and controllable rather than chaotic. These examples underscore that the “input”
and “output” of a machine need not be purely informational; they may be forces, motions, material
transformations, or other embodied variables, so long as the system as a whole implements a stable
mapping (possibly stochastic, but with reproducible statistics) from relevant operating conditions to
outcomes.
    This definition is useful because it lets us connect machines to compositional semantics: if the
components are tools and their couplings are stable, then one can treat the machine as a higher-
level tool whose affordance profile is itself constructed from lower-level affordances. The same idea
supports hierarchical abstraction: once the higher-level tool behavior is stable, it can be “black-boxed”
for many purposes, allowing agents to plan using the machine’s macroscopic affordances without
explicitly simulating all internal component interactions.
Remark 1299. Clause (a) uses “typically” to allow that some components may function primarily
as supports, constraints, or media (e.g., a chassis, casing, lubrication, or shielding) rather than as
direct actuators on other parts. Nevertheless, even these components often participate causally by
setting boundary conditions, maintaining tolerances, or channeling energy and information, so that
their presence is part of what makes the overall pattern stable. In this sense, the decomposition
(Mi )i∈I is not required to be unique: different granularities (coarser modules vs. finer subparts)
may each reveal patterned interactions, and the definition only requires that there exists some de-
composition at which the machine-like character is made explicit.
Remark 1300 (Machines induce internal “interaction languages”). When a family of machines
shares standardized components and couplings, one gets an internal “language” of parts and com-
positions (gears and shafts, logic gates, instruction sets, network protocols). Formally, this can be

                                                  512
treated as a subcategory of realizable processes whose morphisms are precisely the allowed compo-
nent compositions. The “language” metaphor is apt because the standards function like a syntax
(which parts may connect, in what orientations, under what tolerances) together with an operational
semantics (what behaviors result when they are connected in permitted ways). In mature machine
families, this interaction language is often explicitly documented as interface specifications (e.g.,
bolt patterns and torque specs, voltage levels and timing constraints, ISA and ABI conventions),
which makes the induced patterns portable across instances: one can reason about the behavior of
a class of compositions without re-deriving everything from first principles.

Remark 1301. This “interaction language” viewpoint is also a bridge to social coordination: once
a machine family stabilizes, communities can build training, documentation, and division of labor
around it. In that sense, machines become social artifacts that mediate collective competence,
anticipating the culture-level constructions of Section 22 (Hyperseed-Concept 91 and Hyperseed-
Concept 171). The point is not merely that people use machines, but that the stabilized internal
language of a machine family reshapes how labor is decomposed: roles emerge that correspond to
modular boundaries (designer vs. fabricator vs. operator vs. maintainer), and competence becomes
partly a matter of fluency in the relevant interaction language. This also clarifies why machines are
closely linked to computation and embodiment: they provide reliable, repeatable causal structure that
can be embedded into workflows, plans, and protocols, so that abstract procedures (including symbolic
ones) can be physically realized with predictable behavior across time, contexts, and operators.

23.4    Engineered artifacts
Hyperseed uses “engineered” as a broad ontological tag: created via purposeful, goal-oriented ac-
tivity of one or more intelligent minds. In particular, the term is meant to track origin and causal
history (how a thing came to be in the modeled reality-system), rather than merely its present-day
use or its aesthetic resemblance to human-made objects. The tag is intentionally permissive: it cov-
ers cases where design is explicit and centralized (a blueprint and a factory), as well as cases where
design is implicit, distributed, or only partially articulated (e.g., incremental improvement across
generations of makers, or selection among variants produced by a mixed intentional/accidental
process).

Definition 383 (Engineered). An entity E is engineered (relative to an observer/context O) if
there exists:

• an agent (or agent collective) A as in Section 21, with goal/valuation structure as in Section 18;
  and

• a nontrivial interval of time (Section 7)

such that E arises as a consequence of a goal-oriented design-and-construction process within O’s
modeled reality-system. In this observer-relative framing, the requirement that the process occur
“within O’s modeled reality-system” is doing substantive work: it excludes hypothetical external
designers that the observer does not model, while including indirect and mediated causal routes (e.g.,
a committee designs a standard, which reshapes incentives, which in turn leads many independent
actors to build compatible artifacts). The “nontrivial interval” clause is also intended to rule out
degenerate cases where E would be treated as engineered only by stipulating an instantaneous act
of creation; engineering here is tied to temporally extended activity such as iteration, refinement,
procurement, testing, coordination, or maintenance, any of which may be the bottleneck that makes
the outcome non-accidental relative to the goals of A.

                                                 513
Remark 1302. Intuitively, “engineered” names a causal pedigree: the artifact exists because some
mind (or coalition of minds) pursued a goal and successfully constrained reality to instantiate a
pattern. This is not restricted to industrial engineering; it includes language artifacts (alphabets,
grammars), institutional artifacts (contracts, courts), and computational artifacts (code and proto-
cols), depending on what the observer/context counts as part of the modeled reality-system. This is
Hyperseed-Concept ?? stated in the same observer-relative style as the rest of the ontology [1]. A
useful consequence of this broad scope is that “engineered” can apply to abstracta and semi-abstracta
insofar as they have realized implementations and stabilizing causal roles in the world the observer
models (e.g., a legal procedure instantiated by documents, officials, and sanction mechanisms; or a
protocol instantiated by software, hardware, and operator practices). Conversely, mere use does not
suffice: a naturally occurring stone used as a hammer is not, by that fact alone, engineered; but a
stone intentionally shaped or selected and curated through an organized process for hammering may
be engineered, depending on the causal history the observer ascribes.
    A simple example is a screwdriver: it is engineered because it arises from an iterative process
of designing and manufacturing an object that reliably couples twisting actions to screw-rotation
effects. A more subtle example is a musical notation system: it is engineered (in this sense) because
it is a designed symbol technology enabling new patterns of reproduction and coordination across
time. The usefulness of explicitly labeling engineered entities is that later arguments about society,
culture, and collective minds can treat engineered artifacts as stabilizers of cross-agent coupling,
rather than as incidental background [19]. Note that these examples also illustrate that engineering
can be multi-layered: a screwdriver depends on engineered metallurgical practices and measurement
conventions, while notation depends on engineered inscriptions, pedagogy, and social norms. In such
cases, engineering is not a single event but a scaffold of interlocking engineered subsystems whose
combined effect is to make certain actions easy, reliable, and interoperable across agents.

Remark 1303. In borderline cases, it can be helpful to distinguish engineered entities from enti-
ties that are merely selected or filtered by agents without being constructed in detail. For example,
breeding and domestication involve goal-oriented selection operating through natural reproduction;
whether a domesticated organism counts as engineered relative to O depends on whether O models
the selective process as an intentional design-and-construction process (often distributed over time
and across many agents). Similarly, artifacts produced by autonomous systems (e.g., code emitted
by a learned model) can be engineered relative to O if O models the upstream training, prompting,
evaluation, and deployment pipeline as a goal-oriented process attributable to an agent collective.
These clarifications preserve the intent that “engineered” is about goal-directed constraint of out-
comes, even when the fine details of the resulting pattern are not explicitly specified by any single
mind at any single moment.

Remark 1304. In the quantale-weakness framing, one can treat engineering as constrained search
over candidate artifacts whose realized affordances reduce effort (Section 8) while meeting goal
constraints. We develop this viewpoint explicitly in Section 26. One can also interpret this as a shift
in the feasible action-set available to agents: an engineered artifact is not merely an object, but a
transformation of the coupling between intentions and outcomes, often by making some transitions
in the agent–environment system more reliable, cheaper, or more reversible. On this view, the
“constraints” include not only physical laws and resource limits, but also institutional compatibility
conditions, coordination costs, and cognitive limits of the agents that must adopt the artifact for it
to function as intended.

Remark 1305. The “constrained search” phrasing foreshadows the wu-wei formalism: one may
view successful engineering as finding low-effort geodesic-like trajectories in a space of designs,

                                                 514
where effort is not merely physical exertion but also cognitive and organizational cost [21]. This
links engineered artifacts to Hyperseed-Concept 100 and Hyperseed-Concept 207. In practical terms,
this emphasizes that many engineered artifacts are engineered interfaces: they compress complicated
causal structure into a small set of stable handles (buttons, APIs, rituals, forms) that let agents
achieve goals without re-solving the underlying problem each time. Accordingly, “engineering” in
this sense includes the creation of standards and abstractions whose primary function is to reduce
coordination effort by making agent expectations align.

23.5    Computers and programs as emulation machines
Hyperseed defines a computer (relative to a group of minds) as a machine that can, with modest
effort, be made to emulate a large variety of other machines; and defines a program as a set of
signals telling the computer what other machine to emulate.
    We formalize this by separating syntax, semantics, and realization.
Remark 1306. The phrase “relative to a group of minds” is meant to foreground that programma-
bility is partly an interface notion: what counts as “modest effort” depends on a user class’s tools,
training, and available infrastructure, and what counts as a “large variety” depends on which behav-
iors are distinguishable and valuable to that class. For example, to an embedded-systems engineer,
changing a firmware image may be modest; to a lay user, even installing a compiler toolchain may
not be. Likewise, two machines might be physically capable of the same reconfigurations, but differ
greatly in the effort required to exploit them (documentation, debugging support, safety constraints,
access to I/O), which is why the definition is intentionally not purely extensional.
Definition 384 (Abstract process semantics). Let Abs be a category (or V -enriched category) of
abstract processes. Objects are abstract state spaces, types, or contexts; morphisms are abstract
transitions/processes. We write f : A → B for an abstract process from A to B.
Remark 1307. The notation Abs indicates a category: its objects are “types of states” and its
morphisms are the processes that carry states of one type to states of another. One may keep in
mind standard examples: (i) sets and functions, (ii) measurable spaces and stochastic kernels, (iii)
state machines and their transition relations, or (iv) typed terms modulo equivalence in a lambda
calculus. The abstractness here is methodological: we want to speak about a process f independently
of any particular physical substrate that might implement it. This is a mathematical expression of
Hyperseed-Concept 51 and Hyperseed-Concept 140 (and, more specifically, Hyperseed-Concept 141).
    The definition is useful because it gives a precise target for implementation: when we later say
a physical system realizes f , the claim is that the physical dynamics, suitably encoded/decoded,
approximate this morphism in Abs.
    The parenthetical “(or V -enriched category)” is included to accommodate quantitative structure
that is common in engineering uses of computation. For instance, one may want hom-objects to
carry probabilities, costs, resource bounds, or metrics of approximation error. In such settings, the
statement that a physical system “approximately realizes” a morphism can be made internal to the
enrichment (e.g. an order capturing refinement, or a metric capturing simulation distance), rather
than treated as an informal afterthought.
Definition 385 (Program language and semantics). A programming language is a syntactic cat-
egory Syn together with a semantics functor
                                         J·K : Syn → Abs.
A program is a morphism p : A → B in Syn; its intended behavior is the abstract process JpK :
JAK → JBK.

                                                515
Remark 1308. The brackets J·K denote the interpretation map from syntax to semantics: given a
piece of code (a morphism in Syn), it produces an abstract process (a morphism in Abs). Calling
J·K a functor is the formal way of insisting that semantics respects composition: interpreting “do p
then q” should equal “interpret p, interpret q, then compose.” This is the semantic counterpart of
the engineering fact that wiring subroutines together yields a composite behavior.
    As examples: Syn could be a category generated by flowcharts or by typed lambda terms; Abs
could be a category of partial functions or of probabilistic state transformers. This definition is useful
because it cleanly separates three levels that are often conflated: the symbolic artifact (program
text), the mathematical object it denotes (abstract process), and the physical evolution that enacts
it (realization below). This separation is also congenial to algorithmic-information viewpoints in
which programs function as descriptions of processes [16], while remaining compatible with richer
semantic theories.
    It is often helpful (though not required here) to think of Syn as providing the compositional
interface available to a programmer: the primitives and composition rules that are exposed for as-
sembling behaviors. Dually, Abs provides the space of meanings in which one can state correctness
claims. On this view, different semantics functors J·K correspond to different intended interpreta-
tions of the same surface syntax (e.g. operational vs denotational semantics, or a resource-aware
semantics), and the functoriality condition is what makes correctness proofs scale from primitives
to composites.

Definition 386 (Computer as an emulation machine). A computer is a machine C equipped with:

(a) a set (or category) of admissible programs SynC (the “program signals” the user can provide);
    and

(b) an execution mechanism that, for many p ∈ SynC , yields a physical realization of JpK (Defi-
    nition 388 below);

such that the family {JpK : p ∈ SynC } spans (approximately) a large variety of machine behaviors
within the relevant engineering domain, and reconfiguration (from p to p0 ) has modest effort cost
for the relevant user class.

Remark 1309. The clause “set (or category) of admissible programs” allows SynC to carry ad-
ditional structure beyond mere membership. For instance, one may want to talk about transla-
tions/compilers between sublanguages, program equivalences, or program composition as an internal
operation, in which case it is natural to model programs as morphisms in a category rather than
as elements of a set. Likewise, the phrase “program signals” is intentionally broad: for different
machines these may be voltages on pins, bitstrings in memory, punched cards, network packets,
or even physical rewiring that selects among a finite library of behaviors, so long as the resulting
reconfiguration is systematic and cheap relative to rebuilding.

Remark 1310. In plain language: a computer is a machine whose behavior can be widely varied by
supplying different symbolically representable “recipes,” and doing so is cheap compared to rebuilding
the machine. This captures the practical heart of programmability: the user moves in a space of
behaviors by manipulating signs rather than metal. In Hyperseed terms, the computer is a tool
(indeed, a machine) whose affordance profile is unusually broad and compositional, and whose use
is mediated by a stable syntax/semantics interface (Hyperseed-Concept 80).
    A simple example is a microcontroller that can emulate many small control circuits by changing
firmware. A more expansive example is a general-purpose CPU that can approximate a huge range
of behaviors by interpreting different programs as different abstract processes. The definition is

                                                   516
useful because it avoids privileging any single formal model of computation: what matters is not a
particular axiomatization but an empirically grounded emulation capacity relative to a user class
and engineering domain, in the same spirit as Hyperseed’s operational approach to intelligence [19].
    The qualifier “(approximately)” is doing real work: physical computers are constrained by finite
precision, noise, timing jitter, component tolerances, and resource limits, so their realizations typ-
ically match JpK only up to an error model and within an operating regime. This is why emulation
here should be read in an engineering sense: the machine is a reliable stand-in for the target be-
havior under specified assumptions (e.g. clock bounds, numeric ranges, memory availability), not
a metaphysical identity. In particular, the same abstract process may admit many realizations
(different chips, different microarchitectures, different compilation strategies), and the point of the
syntax/semantics interface is to make these interchangeable for the relevant users.
    It is also worth distinguishing the present use of “emulate” from everyday “simulate.” A simu-
lation may reproduce aspects of a target system for purposes of prediction while remaining embedded
in a larger computational context (e.g. a weather model run inside a program that also handles I/O
and visualization). By contrast, the emulation perspective emphasizes behavioral substitution: sup-
plying p configures C so that, from the perspective of a designated interface, the resulting physical
behavior can play the same role as the emulated machine’s behavior.
Remark 1311 (Curry–Howard and typed semantics (optional)). If one chooses Syn to be a typed
lambda calculus (or related proof calculus), then J·K expresses a Curry–Howard style correspondence
between proofs and programs. In that setting, “computer programs are physical realizations of math-
ematical constructions” becomes a literal statement: proof terms (syntactic objects) are realized as
physical signal-configurations that drive a machine to enact the corresponding semantic morphisms.
    This optional perspective is also a reminder that the choice of Abs can encode more than input–
output behavior: it can encode invariants, specifications, or logical propositions that the program
is meant to witness. Then correctness can be phrased as a claim that execution realizes not only
a function-like mapping but also a structured piece of meaning (e.g. a proof-relevant morphism),
which is particularly useful when connecting “program” to “procedure” and “tool use” in embodied
contexts.
Remark 1312. The Curry–Howard remark emphasizes a broader methodological moral: the bound-
ary between “mathematics” and “mechanism” is in part a boundary between description languages
and the physical realizations that make those descriptions causally effective. This resonates with
Hyperseed-Concept 107 and Hyperseed-Concept 136, without requiring any particular foundational
stance.

23.6    Physical realizations of abstract processes
Hyperseed describes a physical realization as a case where a physical process P and an abstract
process A have strong intensional similarity, but one is physical and the other abstract. We express
this as a realizability structure: encodings/decodings plus dynamics.
Definition 387 (Physical process category). Fix a physical reality-system Rphys for an embodied
mind (Section 25). Let Phys be a category whose objects are physical substrates (bodies, tools, ma-
chines, laboratory setups) and whose morphisms are physically realizable processes (possibly stochas-
tic, possibly context-dependent).
Remark 1313. The category Phys is deliberately broad: it is not restricted to deterministic New-
tonian mechanics, but may include stochasticity, noise, measurement back-action, and context-
dependence. This is important for Hyperseed because the observer/context O is always present in

                                                 517
the modeling: what counts as a morphism is what the observer regards as a realizable transformation
in the reality-system [1]. The point is not to deny physics, but to represent physics as a structured
family of allowed transformations inside a reality-system (Hyperseed-Concept 135).
    A concrete example: an object of Phys might be a particular circuit board; a morphism might
be “apply voltage profile u(t) for t ∈ [0, T ],” resulting in a physical state transition. This definition
is useful because it provides the codomain in which implementations live: abstract morphisms are
realized by (structured) physical morphisms.
Definition 388 (Physical realization / implementation). Let f : A → B be an abstract process in
Abs. A physical realization of f is a tuple
                                          R = (P, enc, dec, φ)
where:
• P is a physical substrate (an object of Phys),
• enc : A → State(P ) is an encoding of abstract inputs into physical states,
• dec : State(P ) → B is a decoding of physical states into abstract outputs, and
• φ : State(P ) → State(P ) is (a model of ) the relevant physical dynamics of P induced by the
  realization setting (including any control signals regarded as part of the realization),
such that dec ◦ φ ◦ enc approximates f in the intended sense.
Remark 1314. The notation State(P ) is used informally for the state space associated to the
substrate P (for instance, a set of microstates, a manifold of configurations, or a space of probability
distributions over configurations, depending on modeling choices). The functions enc and dec are
the formal representation of what engineers call “representation” or “interface”: how abstract inputs
are written into the physical medium, and how physical outcomes are read back as abstract outputs
(Hyperseed-Concept 157 and Hyperseed-Concept 136). The map φ is the effective dynamics of the
substrate during execution; it may itself depend on context and control, but that dependence is
treated as part of the realization setting.
    A simple example is an adder circuit realizing the abstract function f : {0, 1}2 → {0, 1} given
by XOR. Here P is a gate-level circuit, enc maps bits to voltage levels, φ is the electrical evolution
over a short time window, and dec maps the output voltage back to a bit. The definition is useful
because it makes explicit where approximation can enter: errors can come from imperfect encodings,
noisy dynamics, or lossy decoding, and these can be measured and managed.
Remark 1315 (Quantale- / p-bit-valued correctness scores). In realistic settings, realization quality
is empirical and observer-relative. A convenient representation is a score
                                       Score(R, f ) ∈ V = [0, 1]2 ,
where the positive component measures evidence that the realized behavior matches f and the neg-
ative component measures evidence of mismatch. This score can be obtained by tests, formal veri-
fication, physical modeling, or mixtures.
Remark 1316. The p-bit-valued score again encodes the possibility of conflict: one may simulta-
neously possess strong evidence of correctness on a test suite and strong evidence of failure in edge
cases. This is not a defect but a faithful representation of engineering knowledge, which is often
paraconsistent in practice even when not acknowledged as such. It also connects implementation
to the broader Hyperseed value layer: correctness, safety, and reliability are themselves evaluated
through evidence-bearing processes rather than assumed as absolute, context-free facts.

                                                   518
   One of the main reasons to state physical realizations explicitly is to guarantee that “wiring
tools together” corresponds to composition of abstract processes.

Proposition 36 (Compositionality of realizations (lax functoriality)). Let f : A → B and g : B →
C be abstract processes. Suppose Rf = (Pf , encf , decf , φf ) realizes f and Rg = (Pg , encg , decg , φg )
realizes g. Assume the interface is compatible in the sense that the output of Rf can be fed as
input to Rg (e.g. encg accepts the decoded outputs of Rf , or there is a fixed adaptor with negligible
additional error). Then there exists a composite realization Rg◦f of g ◦ f on the composite substrate
Pf . Pg (“run Pf then Pg ”) such that

                        Score(Rg◦f , g ◦ f ) ≥ Score(Rg , g) ⊗ Score(Rf , f ),

where ⊗ is the chosen monoidal product on V (Section 3.4). In particular, the direction of the
inequality emphasizes that we are claiming only a guaranteed lower bound on end-to-end correctness
evidence: even if the composite system has additional sources of error, the combined stage-level
evidence still yields a conservative certificate in the order on V.

Remark 1317. Informally, the proposition says: if you have a physical implementation of f and a
physical implementation of g, and you can connect them so that the output of the first is a valid input
to the second, then you can implement the composite computation g ◦f by running the first and then
the second. Moreover, a conservative lower bound on the composite correctness evidence is given
by combining the stage-level correctness evidence using the same evidence-aggregation operation ⊗
used elsewhere in the p-bit quantale.
    This matters because much of engineering (and much of cognition) proceeds by composition:
we build systems out of subsystems. Hyperseed needs a formulation of this compositionality that
is compatible with paraconsistent, evidence-based correctness rather than requiring idealized per-
fect correctness. This proposition is also the implementation-analogue of the categorical principle
that semantics should respect composition (as in the functor J·K above). One can read Pf . Pg as
an abstract model of a pipeline: a temporally ordered coupling (not necessarily a mere product of
substrates) in which the physical degrees of freedom used to represent the intermediate value are
transferred, re-encoded, or otherwise adapted so that the second stage can consume them. The
point is not that the intermediate representation must be identical across stages, but that the real-
ization data includes whatever interface mechanism makes it meaningfully the “same value” for the
purposes of the overall abstract computation.

Proof. Define the composite substrate to execute φf on Pf and then φg on Pg . Define the composite
encoding as encf , and the composite decoding as decg , with the intermediate adaptor given by
the compatibility assumption. Concretely, the composite realization packages (i) the first-stage
preparation of a physical state from an abstract input via encf , (ii) evolution by φf on Pf , (iii) an
interface map that turns the relevant output degrees of freedom of Pf into admissible input degrees
of freedom for Pg (which may include copying, buffering, re-timing, transduction, or re-encoding),
and finally (iv) evolution by φg on Pg followed by readout via decg . This makes explicit that
the intermediate “wire” is itself part of the physical story: the claim only goes through when the
adaptor is treated as realization structure rather than an implicit idealization.
    Under the interpretation of ⊗ as multiplicative aggregation of evidence, independent positive
evidence for correctness multiplies across stages, and (at minimum) the resulting composite score
is bounded below by the product of the stage scores. This is the standard “pipeline” principle of
implementation: correctness does not improve by composition, but a reliable stage chained after
a reliable stage remains reliably correct in the aggregated-evidence sense. Formally, what is used


                                                   519
here is that ⊗ is monotone in each argument with respect to the order on V: if a realization of the
composite can be analyzed as first satisfying f to some degree and then satisfying g to some degree
(with compatibility ensuring that the second analysis is applicable to the first stage’s outputs), then
combining the two pieces of evidence via ⊗ yields an evidence value that is no stronger than any
additional, possibly more complex end-to-end analysis, hence the inequality as a lower bound. The
“independence” language should be read in the conservative sense appropriate to paraconsistent
evidence: we are not assuming that errors are uncorrelated in a probabilistic model, only that the
evidence calculus represented by ⊗ is designed to aggregate stage-level support without introducing
unjustified strengthening. In practical terms, even when the stages share failure modes (for example,
both depend on a common power supply, clock, or calibration procedure), the proposition still
serves as a template for what one may safely claim given only the two stage scores and an interface
condition.

Proof sketch. The strategy is to build the composite realization by literally running the first physical
process and then the second, using the interface-compatibility assumption to connect the two runs.
The inequality then follows from the intended semantics of ⊗ as an evidence aggregator: stage-level
evidence is combined to yield a conservative bound on end-to-end evidence. Intuitively, one can
think of Rg◦f as a “program” for the laboratory or machine shop: prepare according to encf , run
the first device, translate its output into the input format of the second device, run the second
device, and finally read out using decg .                                                             

Remark 1318. The key step is conceptual rather than technical: we treat encodings/decodings as
part of the realization structure, so the “wiring” between stages is not a handwave but an explicit
adaptor condition. Once that is granted, the remaining content is the monotonicity and aggrega-
tive meaning of ⊗ in V. Geometrically one may picture each stage as a noisy channel between
abstract spaces; composing two channels yields another noisy channel whose reliability is (at best)
the product-like combination of the reliabilities of the components. A helpful concrete picture is
a sensing-and-control loop: f might be a sensor pipeline mapping a physical quantity to a digital
estimate, and g a control law mapping that estimate to an actuator command; the composite g ◦ f
is the overall perception-to-action transform. Even if the sensor and controller are each only par-
tially correct in the paraconsistent evidence sense, chaining them yields an overall system with an
evidence score that is at least the ⊗-combination of the two, provided the estimate produced by the
sensing stage is indeed in the admissible input class for the control stage (units, ranges, timing,
and representation all count as part of this admissibility).

Remark 1319. Proposition 36 is intentionally weak: it asserts only a monotone lower bound
on composite correctness evidence. This matches engineering reality: composition can introduce
new failure modes, but one can still obtain a conservative guarantee by multiplying (or otherwise
aggregating) stage-level guarantees. The weakness is also a feature for Hyperseed’s intended use:
it allows modular reasoning in the presence of inconsistency, where one may have strong evidence
for some aspects of each stage and counterevidence for others, and still wish to propagate whatever
support is available without collapsing into triviality. In particular, the proposition does not claim
that Score(Rg◦f , g ◦ f ) equals Score(Rg , g) ⊗ Score(Rf , f ), nor that the bound is tight; it merely
guarantees that the evidential calculus respects the basic operational fact that running two verified-
enough stages in sequence yields a verified-enough composite, in the sense captured by the order on
V.




                                                  520
23.7    Embodiment and the body-channel
Hyperseed defines a physical reality (for an embodied mind) as a reality-system containing the
body where the mind’s causal impact on that reality is mostly mediated through the body-channel.
We represent this using factorization constraints on causal influence. This framing is deliberately
structural: rather than stipulating what “matter” or “the physical” is in itself, it specifies which
parts of a mind–world interaction graph are treated as primary for modeling, prediction, and
intervention.

Definition 389 (Body as a coupled pattern-system). Let M be a mind-level pattern web (Sec-
tions 13–17). A body for M is a physical substrate B such that:

(a) there is strong mutual causal coupling between M and B (modeled as bidirectional channels
    for perception and action), and

(b) B is largely contained in a designated physical reality-system Rphys .

Remark 1320. Intuitively, this definition says that a body is not merely “owned” by a mind, but
coupled to it: the mind changes because the body is sensed, and the body changes because the mind
acts. The bidirectionality clause is what distinguishes a body from a mere instrument occasionally
used: the coupling is persistent and forms a significant part of the mind’s ongoing dynamics. This is
the formal doorway into Hyperseed-Concept 135 and Hyperseed-Concept ?? (the latter being implicit
in the ontology even when not singled out as a separate primitive).
    Examples: for a human mind-model M , B may be the organism’s nervous system and muscu-
loskeletal system as represented in a physical reality-system. For a robot controller M , B may be
the sensor-actuator suite plus onboard compute substrate. The usefulness of the definition is that
it makes “having a body” a structural property that can be used in later causal and cosmological
definitions: a physical reality-system is then the one in which this body is situated and through
which most causal influence flows.
    Two clarifications are often useful in applications. First, “strong mutual causal coupling” is
not intended as a binary predicate but as a dominance claim: relative to the observer’s modeling
granularity, there are sustained causal pathways B → M (perception, interoception) and M → B
(action, regulation) that explain a large fraction of M ’s state transitions and a large fraction of
B’s state transitions on the timescales of interest. Second, the boundary of B may be context-
dependent: prostheses, implants, or tightly integrated tools can be treated either as part of B or
as external artifacts depending on whether their coupling to M is persistent, high-bandwidth, and
governed by the same closed-loop dynamics that ordinarily characterize sensorimotor control.

Definition 390 (Body-channel mediation (factorization form)). Fix a physical reality-system Rphys
and an embodied mind (M, B). We say that M ’s causal impact on Rphys is mostly mediated
through the body if, for most effects e in Rphys that are attributable to M (relative to observer O),
the corresponding influence morphism factors as
                                         Act       Phys
                                   M −−−−→ B −−−−→ Rphys ,

up to the chosen approximation notion in the process formalism (Section 3). In particular, “most”
and “attributable” are to be read as observer-indexed judgments about explanatory and predictive
relevance: O selects a causal model, a notion of intervention/counterfactual dependence, and a
tolerance under which small residual channels may be ignored without materially changing forecasts
or control policies.


                                                521
Remark 1321. The factorization diagram is the mathematical version of the everyday claim that,
in physical reality, minds act through bodies. The arrow labeled Act stands for the mind-to-body
channel (motor control, endocrine control, etc.), and the arrow labeled Phys stands for body-to-
world causal propagation. The qualifier “mostly” is essential: it permits exceptions (e.g. indirect
influence via other agents or artifacts) while asserting that the body-channel carries most of the
causal mass relevant for prediction and control.
    This is useful because it provides a criterion for when a reality-system should be called “physical”
relative to a mind: if there are large, reliable mind-to-world influence channels that do not factor
through the body, then the modeling stance changes (as the next remark states). In short, physicality
is treated operationally via channel structure rather than metaphysically.
    Although the definition is stated in terms of impact (an M → Rphys direction), the same model-
ing posture typically comes with a complementary perception-side regularity: for most observations
o in M that are about Rphys , the relevant information flow factors as

                                             Sens         Per
                                     Rphys −−−−→ B −−−→ M,

again up to approximation. This makes explicit why B functions as an interface: it is simultaneously
the dominant actuator path outward and the dominant sensor path inward, yielding a closed loop
whose stability and bandwidth strongly constrain the kinds of policies and representations that are
feasible for M in Rphys .

Remark 1322. If a mind can reliably influence a reality-system without using the body-channel,
then (in the Hyperseed sense) that reality-system is less “physical” relative to that mind. The
point here is not metaphysical; it is a modeling decision about which channels carry most causal
mass for the observer’s predictions. Concretely, if the observer must posit persistent high-bandwidth
morphisms M → R that bypass B in order to explain regularities (e.g. dependable “direct” effects
of intention on distant states), then it becomes misleading to treat R as a standard physical reality-
system for that mind, because the dominant control affordances would not be organized around
embodied action.

Remark 1323. This factorization stance also prepares later social and communion discussions:
many causal influences in society do not run directly through one’s own body but through artifacts,
institutions, and other agents. Separating “body-channel” influence from “artifact-mediated” in-
fluence lets one speak precisely about extended agency and collective mind systems without losing
the embodied anchor. In particular, it allows a clean distinction between (i) amplification of em-
bodied action (where Act still initiates the relevant causal chain, even if subsequent propagation is
mediated by machines and institutions) and (ii) putative non-embodied channels (which would re-
quire a different ontological placement in the causal web). This becomes important when describing
delegation, coordination, and the emergence of higher-level agents whose effective “bodies” may be
distributed across many human bodies and technical substrates.

23.8    Algebraic asymmetry of physical reality
Hyperseed emphasizes that physical reality tends to have a relatively rigid, low-dimensional (vector-
space-like) structure, while mental and intersubjective realities tend to have weaker algebraic struc-
ture (often best treated topologically), and that the latter can only approximately be projected
into the former. This “rigidity” is meant in the sense that physical descriptions typically come with
many simultaneously interacting constraints (e.g. compositional laws, conservation principles, and
dynamical compatibility conditions), whereas mental and social descriptions often preserve only

                                                    522
those aspects that remain stable under coarse changes of implementation (e.g. continuity rather
than linearity, reachability rather than exact trajectories, or preference/ordering rather than precise
quantities).
    A minimal formalization uses a “forgetful” map from stronger structure to weaker structure.
Concretely, one can treat “physical structure” and “mental/intersubjective structure” as different
signatures of operations and relations together with axioms, where the mental signature is obtained
from the physical signature by dropping some operations, equations, or distinguished predicates.
In that common situation, the corresponding forgetful functor is not an additional assumption but
a standard construction: every model of the richer theory canonically determines a model of the
poorer theory by restriction of structure.
Definition 391 (Algebraic asymmetry (structure implication form)). Let Algphys be an algebraic
theory capturing salient physical structure (e.g. vector-space operations, linear dynamics, conser-
vation laws) and let Algmind be a weaker theory capturing salient mental/intersubjective structure
(e.g. topology, partial order, or merely the quantale-enriched relational structure).
    We say that a community’s physical and mental realities exhibit algebraic asymmetry if:
(a) there is a canonical forgetful functor

                                     U : Alg(Algphys ) → Alg(Algmind )

     that maps each physically structured system to its underlying mental/intersubjective structure;
     but
(b) there is no functorial inverse that assigns to each mental/intersubjective system a unique phys-
    ically structured system realizing it (at best, one has approximations, constraints, or choices).
Remark 1324. The definition says, in effect, that physical structure is (for the relevant commu-
nity) more constraining than mental/intersubjective structure. There is a systematic way to forget
some structure (go from richer algebra to poorer algebra), but there is no systematic way to recon-
struct the richer structure uniquely from the poorer. This is Hyperseed-Concept 55 expressed in
standard mathematical language (forgetful functors and non-invertibility).
    A guiding example is that many different vector spaces can share the same underlying set, and
many different norms can induce the same coarse topology; the “mental” structure (say, topology
or order) typically underdetermines the “physical” structure (say, linear operations and conserved
quantities). The usefulness of the definition is that it provides a clean formal lever for later claims
about implementation and projection: mental contents may be realized physically only by selecting
among many physically distinct instantiations, and that selection is constrained by effort, resources,
and context. In particular, the “no inverse” clause should be read as a non-uniqueness claim: even
when a realization exists, it generally does not exist canonically (i.e. in a way that is natural with
respect to morphisms in Alg(Algmind )), and so any reconstruction procedure necessarily imports
additional conventions, priors, or external constraints.
Remark 1325. It is worth separating three notions that can otherwise be conflated: (i) existence of
some right-inverse on objects (each mental structure is realizable by at least one physical structure),
(ii) existence of a section S with U ◦ S = id (a consistent choice of a realization for each mental ob-
ject), and (iii) existence of a functorial section (the chosen realizations respect structure-preserving
maps between mental systems). The definition rules out (iii), which is the categorical form of “no
systematic unique reconstruction.” In many settings (especially when mental descriptions ignore
metrics, coordinates, or conserved quantities), one may have (i) for broad classes of cases, occa-
sionally (ii) after imposing extra choices, but typically not (iii) without adding additional structure

                                                  523
to Algmind that effectively re-introduces the missing physical constraints. This captures the sense in
which embodiment and implementation require extra degrees of freedom beyond what is present in
the mental description alone.
Remark 1326 (The simplest motivating example). A real vector space canonically determines a
topological space (via the metric induced by a norm), but an arbitrary topological space does not
determine a vector space structure. This is an archetype for Hyperseed’s claim: physical structure
typically implies (and constrains) mental/intersubjective structure, whereas mental structure only
partially constrains physical structure and often requires approximation to be physically instantiated.
One can sharpen the same point with even simpler forgetful functors: a group canonically determines
a set, but a set does not canonically determine a group; a smooth manifold canonically determines a
topological space, but a topological space does not canonically determine a smooth structure. These
examples emphasize that “forgetting” is often a many-to-one collapse of possibilities: the fibers
of U over a given mental object can be large, reflecting many distinct physical implementations
compatible with the same mental/intersubjective description.
Remark 1327. The community-relative phrasing is material: what counts as “salient physical
structure” depends on the community’s instrumentation, embodiment, and practical invariants. A
community that can only measure coarse macroscopic variables may treat distinct microphysical
configurations as physically irrelevant, thereby shifting the boundary between Algphys and Algmind .
In that sense, algebraic asymmetry is compatible with multiple nested layers of description: one
may have a chain of forgetful functors from microphysics to macrophysics to phenomenology, each
step discarding structure and enlarging the space of admissible realizations.
Proposition 37 (Asymmetry and weakness). If mental/intersubjective structure is modeled as a
coarse-graining (a controlled collapse of distinctions) of physical structure, then the passage from
physical to mental reality increases quantale weakness (Section 3.7) relative to the finest-grained
physical observer.
Remark 1328. In plain terms, the proposition says: if we go from a fine-grained physical descrip-
tion to a coarser mental/intersubjective description by identifying distinctions, then we become
“weaker” in the sense that more states are treated as undistinguished. This is not a pejorative
claim; it is a structural one. It links the philosophical idea of coarse-grained experience to the
formal order-theoretic notion of weakness developed earlier [3, 2]. The connection to the preced-
ing definition is that the forgetful passage U is a structured way of discarding discriminations:
when operations/observables are forgotten, the induced semantics can merge previously separable
possibilities, thereby enlarging the indistinguishability relation that defines weakness.
Proof. Coarse-graining identifies (or partially identifies) physical states that were previously dis-
tinct. In the weakness formalism, this corresponds to adding undistinguished pairs. By Theorem 1,
adding undistinguished pairs monotonically increases weakness. More explicitly, if the finest-grained
physical observer induces an undistinguished relation ∼phys on a state space, and the coarse-grained
mental/intersubjective observer induces ∼mind , then coarse-graining means ∼phys ⊆∼mind (at mini-
mum, every pair that was already indistinguishable remains so, while some formerly distinguishable
pairs become indistinguishable). The monotonicity theorem applies to this inclusion.

Proof sketch. The proof reduces the statement to monotonicity: coarse-graining is exactly the
act of declaring previously distinct states to be undistinguished, and weakness was defined so that
enlarging the undistinguished relation increases weakness. Equivalently, coarse-graining is an order-
preserving map in the direction that collapses distinctions, and weakness is ordered so that more
collapse corresponds to greater weakness.                                                          

                                                 524
Remark 1329. The key step is the identification of “coarse-graining” with “adding undistinguished
pairs.” Once this is made explicit, the result is essentially a corollary of how weakness is ordered. A
visual intuition is to imagine a high-resolution image being pixelated: multiple microstates collapse
into one macrostate, and the observer loses discriminative power. In Hyperseed terms, this loss is
not merely epistemic; it shapes what patterns can be represented and what control can be exerted,
because both depend on distinctions. A further intuition, aligned with the functorial language above,
is that the collapse induced by U can be understood as pushing forward along an “observation”
that identifies states whenever the remaining (mental/intersubjective) invariants agree; since fewer
invariants are tracked, more pairs agree, and the indistinguishability relation expands.

23.9     Two tiny examples
23.9.1    A tool that reduces effort via mechanical advantage
Let a task be “raise a weight” within a physical reality-system. Model the relevant effort scalar
as E ∈ [0, 1] where larger means more effort. Let Ebare = 0.9 be the effort without a tool, and
let a lever tool T yield ET = 0.3 for the same achieved effect in the same context. One can
read the choice of [0, 1] here as a normalization convention: it fixes units only up to monotone
rescaling, but it is enough to express ordinal comparisons (this action is easier than that action)
and threshold claims (an agent can afford at most E ≤  in a given episode). The phrase “same
achieved effect” is also doing work: the comparison is not between different goals, but between
different means to the same end, so that the effort change can be attributed to the tool rather than
to a change in objective. In many environments the effort would be context-dependent (terrain,
grip, fatigue, precision requirements), and the toy scalar E should be read as already incorporating
those background conditions into a single budget-like quantity.
Remark 1330. This is the archetypal case where the affordance profile changes the mapping from
action to effect by changing the required resource expenditure: the lever increases the space of
achievable effects for a bounded agent because actions that were previously too costly become feasible.
This illustrates why Hyperseed keeps effort (Section 8) close to the ontology of tools: tools are not
merely causal mediators but resource transformers (Hyperseed-Concept 100 and Hyperseed-Concept
191).
    In Hyperseed terms: the lever is a tool because it is purposefully manipulable toward the ob-
jective, and it extends agency by lowering effort for the same outcome. In the quantale-weakness
perspective, lowering effort typically enables the agent to maintain finer distinctions elsewhere (at-
tention, memory, control), indirectly reducing global weakness. Equally importantly, the reduction
Ebare 7→ ET can be understood as a change in the effective action space: even if the bare body
can in principle generate the required force, the lever may move the task from “barely possible” to
“reliably repeatable” under noise, limited precision, and finite time. This motivates treating tools
not just as add-ons but as parts of an extended sensorimotor loop, where the tool shifts which
policies are stable under perturbations and which plans remain within budget. On this reading,
mechanical advantage is just one especially transparent instance of a more general pattern: an
external artifact can reshape the effort landscape so that the same target state becomes reachable
by a broader set of trajectories.

23.9.2    A program as a physical realization of an abstract construction
Let Syn contain a program p whose semantics JpK is an abstract process f : A → B (e.g. a parsing
algorithm, a planning operator, or a proof normalization map). Running p on a computer C yields

                                                 525
a physical realization R = (P, enc, dec, φ) of f in the sense of Definition 388. Here P can be read
as the relevant physical state space (register contents, memory configurations, I/O buffers, and
possibly environmental degrees of freedom that the computation couples to), enc and dec specify
how abstract inputs and outputs are represented at that physical level, and φ names the concrete
evolution (often a time-indexed dynamics induced by the machine executing the compiled form of
p). Even in this simple packaging, the role of representation becomes explicit: a program does not
act on A and B directly, but on their encodings, and the “same” abstract function can be realized
by different choices of code, data layout, and hardware, yielding different resource profiles.

Remark 1331. The example highlights the three-layer separation: program (a syntactic object),
meaning (an abstract morphism), and execution (a physical evolution plus an interface). In prac-
tice, many confusions about computation come from sliding between these layers without noticing.
The formalism forces us to keep track of where a claim lives: is it about denotation (JpK), or about
implementation quality (Score(R, f )), or about resource usage (effort, time, energy) of the physical
substrate? This is precisely why Hyperseed-Concept 80 is placed alongside Hyperseed-Concept 136.

   This makes precise (at a minimal level) the slogan:

     Computer programs are physical realizations of mathematical constructions.

The slogan becomes more structured if Syn is taken to be a proof calculus (Curry–Howard), but
the basic point already holds at the level of “syntax → semantics → physical realization.” The
additional structure in R is what allows one to distinguish correctness from mere intention: JpK = f
is an abstract statement about denotation, while the realized process may approximate, fail, or only
probabilistically track f because φ is embedded in a noisy, finite-precision substrate. Moreover, two
realizations can agree extensionally on f yet differ significantly in embodied properties (latency,
energy draw, heat dissipation, fault tolerance), which are invisible if one collapses everything into
the abstract morphism alone. In Hyperseed terms, this is exactly the point at which computation
becomes part of embodiment: the interface maps abstract types into physical carriers, and the
carrier dynamics determines which abstract constructions are feasible under an agent’s resource
constraints. This also clarifies why “running the same program” can be an underspecified claim:
without fixing enc, dec, and the operational context of φ, one has not fixed the realized process
that the world actually instantiates.

23.10    What this section contributed to the overall reconstruction
This section mapped the Hyperseed nodes tools, machines, engineered, computers and programs,
physical realizations, and physical reality/body with algebraic asymmetry into the paper’s core math-
ematical vocabulary. In particular, it translated what can look like informal engineering talk (de-
vices, implementations, programs, bodies) into a small number of reusable structural moves: cou-
pling, emulation, factorization through channels, and order-theoretic coarse-graining. This matters
because it makes later claims about “shared worlds” and “scaling” provably sensitive to the con-
straints and degrees of freedom that artifacts and bodies impose, rather than treating them as
externalities.

• Tools and machines become physical pattern-systems whose affordances can be represented as
  p-bit-valued couplings from actions to effects. Concretely, one can treat an action-set (or action-
  algebra) A and an effect-set E as interfaces, and model the tool as a constrained relation or
  channel A      E whose entries live in p-bit, so that “what the tool lets you do” is captured by
  a structured map rather than a verbal description. On this reading, a tool is not merely an

                                                526
  object but an input–output regularity stabilized in the world, and the coupling encodes both
  possibilities and impossibilities as first-class data.

• Computers and programs become emulation machines plus syntax/semantics layers, with physi-
  cal realization connecting semantics to physics. Here the central explanatory move is to separate
  (i) the physical machine as an emulator (a pattern-system capable of reliably realizing a family
  of state transitions), from (ii) a syntactic layer (descriptions, code, symbols) and (iii) a semantic
  layer (what those symbols are taken to denote or implement), and then to insist that a realization
  map is what makes the semantics causally efficacious. This is precisely what lets later sections
  speak about “the same program” across different substrates without erasing embodiment: same-
  ness is routed through emulation and realization, not assumed as a primitive identity.

• Embodiment becomes a factorization constraint on causal impact through a body-channel. In-
  stead of treating an agent’s influence as a direct action on the external world, the reconstruction
  forces a decomposition in which the agent’s internal degrees of freedom can only affect distal
  variables via a mediating interface (the body), i.e., via a channel that both enables and limits
  control. This makes constraints such as bandwidth, locality, actuation delay, and sensor noise
  part of the formal story: what an agent can bring about is restricted to what can pass through
  that body-channel and be amplified by the surrounding physics.

• Algebraic asymmetry becomes a formal “strong structure forgets to weak structure” relation,
  with coarse-graining captured by monotone increases in weakness. The point of phrasing this
  as an asymmetry is that there is typically an easy, structure-forgetting map from a richer de-
  scription to a poorer one, while reconstruction in the opposite direction is underdetermined or
  impossible without extra information. By encoding this as a monotone order (“more weak” =
  “less structured”), the framework gains a disciplined way to talk about abstraction layers (e.g.,
  physical → computational → semantic) and about why certain equivalences are stable under
  forgetting while others are not.

Remark 1332. From a broader perspective, these constructions place “engineering” inside the
same conceptual frame as “pattern” and “agency”: engineered artifacts are patterns stabilized by
goal-directed processes, and computers are machines whose stable patterns include a semantics-
respecting reconfiguration mechanism. Put differently, an engineered object is a pattern whose
persistence is not merely accidental but maintained (historically and/or presently) by optimization,
selection, or design, and this maintenance can be tracked using the same coupling-and-channel
vocabulary used elsewhere in the reconstruction. Moreover, emphasizing semantics-respecting re-
configuration highlights what distinguishes general-purpose computation from mere dynamics: the
machine is organized so that changes in symbolic descriptions (programs) systematically correspond
to changes in realized behavior, with the realization map doing the work of tying symbols to physical
transitions. This is why these notions are not merely ancillary but central to the later discussion
of intersubjective communion and cosmological scaling: communities build shared realities partly by
building shared artifacts [1, 19]. The shared artifact, on this view, is a coordination device precisely
because it induces shared couplings: multiple agents can reliably predict how actions propagate to
effects through the artifact, and this predictability is a precondition for stable joint practice.

    These constructions are used in the next sections to formalize intersubjective communion and
cosmological scaling in a way that keeps the engineering/implementation dimension explicit. In-
tersubjective communion can then be treated not only as alignment of beliefs or symbols, but also
as alignment of accessible channels and realizations (e.g., agreeing on what a sign, tool, or protocol


                                                  527
does because the underlying couplings are shared and repeatedly testable). Cosmological scaling,
likewise, can be discussed in terms of how such couplings, emulators, and body-channels compose
and persist across increasing spatial, temporal, and energetic scales, rather than being idealized
away as if agency operated on an unbounded, implementation-free substrate.


24      Intersubjectivity, Communion, and Aesthetics
24.1     Hyperseed concepts handled in this section
This section gives a mathematically grounded treatment of the following Hyperseed concepts:

     • intersubjective reality;

     • intersubjective communion and explicit intersubjective communion;

     • spiritual experience as communion with a broader-scope mind; psychedelics/entheogens;

     • emotion and compassion;

     • archetypes (as cross-context pattern templates);

     • aesthetics/art/beauty as “surprising fulfillment of expectations” and the role of paraconsistent
       logic;

     • religion and ritual as persistent social technologies for inducing and stabilizing communion;

     • (briefly) state-dependent science as a community-level epistemic practice conditioned on states
       of consciousness.

    To avoid ambiguity, the intent of the list above is not merely thematic but structural: each
item will be assigned an explicit representational role inside the same formal apparatus (patterns,
carriers, links, and state/observer parameters), so that claims about communion, archetypes, or
beauty can be expressed as statements about how patterns distribute and couple across minds and
artifacts. In particular, “intersubjective reality” is treated here as an object of analysis rather than
a vague backdrop: it is the specific pattern-structure that a community can jointly sustain, predict
within, and coordinate action around. Likewise, “communion” is treated as a dynamical regime of
that structure (a change in the balance between within-mind and cross-mind pattern dominance),
and “explicit communion” as the additional condition that some agents in the community represent
(possibly imperfectly) that regime within their self- and world-models.
    The inclusion of psychedelics/entheogens and “state-dependent science” signals that the relevant
variables are not only social (who is connected to whom) but also stateful : the same community
graph can instantiate different intersubjective realities under different distributions of attention,
affect, and altered states, because those states modulate which patterns become salient, which
links are strengthened, and which contradictions can be tolerated without collapse. Emotion and
compassion are included not as informal add-ons but because they function as pattern-selection
and coupling mechanisms: they bias which patterns are amplified, which others are suppressed,
and how quickly patterns propagate across interpersonal channels.




                                                  528
24.2    Motivation and placement in the formal development
Hyperseed treats minds as pattern-bearing systems, and treats communities of minds as giving
rise to intersubjective realities: reality-systems constituted by patterns distributed across multiple
minds, together with causal and predictive couplings between these minds.
    A key motivation for formalizing intersubjective realities is that many phenomena of interest
(language, norms, shared meanings, institutions, artistic canons, collective emotions, religious ex-
periences, and scientific paradigms) are neither well-captured by purely individualist models nor
by undifferentiated “group mind” metaphors. The proposed framework aims to model precisely
what is shared (patterns and their carriers), how it is shared (links with weights and directions),
and how it can remain stable even when it is not fully consistent from any single point of view. In
this sense, the formal objects introduced here are intended to be reusable building blocks for later
sections: once intersubjective reality is expressed as a pattern-structured object, one can compare
communities, track phase transitions in coordination, and study how artifacts and rituals act as
external memory and alignment mechanisms.
    The goal here is not to reduce intersubjectivity, communion, or beauty to a single scalar. Rather,
the goal is to place these notions inside a rigorous ontology in a way that is: (i) compositional (com-
munity structure matters), (ii) explicitly state- and observer-relative (different communities and
states of consciousness yield different regimes), and (iii) compatible with non-classical reasoning,
since Hyperseed’s core claims explicitly allow tensions and contradictions (e.g. the “surprising yet
fulfilling” character of beauty).
    Compositionality here means that the theory should distinguish, for example, a tightly con-
nected triad from a loosely coupled crowd, even if both have the same number of participants:
higher-order structure (clusters, bridges, hubs, and shared artifacts) changes what patterns can be
sustained and how quickly they synchronize. State- and observer-relativity means that the same
underlying environment can support multiple concurrently valid intersubjective realities, depending
on which patterns are accessible in a given state of consciousness and which measurements/queries
are being posed by which observers. Compatibility with non-classical reasoning is required because
many of the target phenomena are characterized by stable co-presence of apparently incompati-
ble descriptions: rituals can be “symbolic and real,” archetypes can be “abstract and concrete,”
and aesthetic experiences can be “unexpected yet exactly right.” A paraconsistent setting allows
such co-presence to be represented without trivializing inference, which is crucial if one wants a
mathematics that can model the phenomenology rather than explain it away.
    We proceed in three steps:
  1. Define an intersubjective reality for a community as a weighted pattern hypergraph with
     cross-mind predictive/causal links.

  2. Define communion as a dominance of cross-mind pattern intensity over within-mind pattern
     intensity, and define explicit communion via self-model recognition using paraconsistent truth
     values.

  3. Define aesthetic experience and beauty in a way that directly formalizes “surprising ful-
     fillment” and explains why a paraconsistent logic is a natural fit; then relate aesthetics to
     communion via shared pattern carriers (artifacts, rituals) and archetypes.
   Step (1) is meant to make “shared reality” operational: the hypergraph representation allows
patterns to be carried not only by individual minds but also by multi-agent configurations and by
external artifacts (texts, images, songs, places, symbols), with hyperedges encoding that certain
patterns are only instantiated or only predictive when several carriers jointly participate. The

                                                 529
weights on links and hyperedges will be interpreted as strengths of coupling, reliability of predic-
tion, and/or causal influence, so that the formalism can express both weak cultural resonance and
strong, high-fidelity synchrony. The “predictive/causal” language is intentionally inclusive: in some
contexts the relevant link is a learned model of another agent, while in other contexts it is a di-
rect causal pathway (speech, gaze-following, imitation, coordinated movement), and the framework
aims to support both without forcing an artificial reduction.
    Step (2) isolates communion as a regime change: instead of treating communion as an ineffable
binary property, it is treated as a measurable shift in where pattern-intensity resides (primarily
within individuals versus primarily across the interpersonal links and shared carriers). The “ex-
plicit” qualifier is then reserved for cases where at least some agents track, represent, or can report
the communion regime in their self-models, even if that representation is partial, conflicted, or
simultaneously affirmed and denied. The invocation of paraconsistent truth values at this step
reflects a common empirical feature of communion reports: agents may sincerely endorse both “I
remained myself” and “I dissolved into the group” without experiencing this as a failure of cogni-
tion. A logic that can register such dual attribution without collapse is thus not a decorative choice
but a way to keep the ontology faithful to the data the theory is supposed to cover.
    Step (3) ties aesthetics to inference and prediction: “surprising fulfillment of expectations” will
be made precise by distinguishing (a) a departure from locally expected patterns (surprise) and (b)
a higher-level coherence or resolution that nonetheless satisfies deeper constraints (fulfillment). The
paraconsistent connection arises because many aesthetic resolutions operate by sustaining tension
(two readings, two moods, two interpretations) while still yielding an integrated experience; the
formalism should therefore permit a controlled coexistence of incompatible pattern-attributions
that remains informative rather than degenerating into arbitrariness. Finally, the link back to
communion is not merely sociological: artworks, rituals, and archetypal narratives act as shared
pattern carriers that can entrain attention and expectation across multiple minds, thereby increas-
ing cross-mind pattern intensity and stabilizing communal regimes over time. This is also where
“religion and ritual” and the brief discussion of “state-dependent science” are placed: both can be
analyzed as repeatable protocols for shifting state variables (attention, affect, interpretive priors)
in a coordinated population, thereby selecting which intersubjective realities become accessible,
credible, and action-guiding under those conditions.

24.3    Intersubjective reality as a community pattern system
We assume (as in earlier sections) that “pattern” is an observer-relative regularity associated with
compression/effort, and that pattern intensity is a nonnegative quantity reflecting salience, coher-
ence, frequency, and/or causal relevance within a time interval. In particular, the same underlying
events may support different patterns for different observers, and the same nominal “kind” of pat-
tern (e.g. a linguistic convention) may register with different intensities depending on how stable it
is, how often it is instantiated, how much predictive power it contributes, or how costly it would be
(in description length or cognitive effort) to ignore it. The time interval I is included explicitly so
that both short-lived synchronizations (e.g. a fleeting shared glance) and longer-lived regularities
(e.g. a persistent norm) can be treated within one scheme by varying the temporal window over
which intensities are evaluated.

Definition 392 (Intensity quantale). Let VI = ([0, ∞], ≤, ⊕, 0) where ⊕ is addition with x ⊕ y :=
x + y and [0, ∞] is ordered by the usual ≤. We will use VI as the codomain of pattern-intensity
maps and as an aggregation monoid.

Remark 1333. VI is a commutative quantale if equipped with the complete lattice structure given

                                                 530