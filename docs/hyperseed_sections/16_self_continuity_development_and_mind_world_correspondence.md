# 16 Self, continuity, development, and mind-world correspondence

The definitions above are intentionally abstract: Hyperseed is compatible with many concrete
attention mechanisms. One common form is “soft” allocation by expected value-of-information or
expected control benefit. In particular, we can separate (i) a mechanism that scores candidate foci
(e.g., patterns) for their relevance to control, from (ii) a mechanism that turns those scores into a
bounded allocation that respects the need to diversify across multiple competing opportunities for
improvement.

Definition 197 (Priority scores from predictive attraction). Let G be a set of goal conditions
(Section 18). For each pattern p ∈ P assume there is an associated event type Ap meaning “pattern
p is currently active/salient” (Section 14). Define a priority score at time t by

                                   Priot (p) := max AttO,∆ (Ap , G) ,
                                                 G∈G

where AttO,∆ is the attraction operator from Section 14.3.

Remark 758. This definition is the promised “differential” idea in miniature: a pattern is prior-
itized if its presence makes a significant difference to what the system expects about its goals. The
absolute value allows both positive and negative attraction to matter: either “this pattern tends to
bring about the goal” or “this pattern tends to prevent the goal” can warrant attention, because both
can guide effective control.

Remark 759. The use of maxG∈G encodes a conservative, goal-sensitive criterion: a pattern is
high-priority if it substantially affects at least one goal condition, even if it is irrelevant to others.
Alternative aggregations are possible (e.g., expectation under a goal-importance distribution, or a
weighted sum), but the max operator cleanly captures the idea of “whatever is most at stake right
now” without committing to a particular utility encoding beyond the existence of G.

Remark 760. One may read Priot (p) as a bridge between prediction/control (Section 14) and
resource allocation: it converts the attraction relation into a scalar that can be traded off against
entropy-regularization or other concentration penalties. This is a typical move in architectures
emphasizing cognitive synergy and integrated attention allocation [19].

Remark 761. To connect the pattern-level priority score back to the update-action view, one may
imagine that many update actions u ∈ U are pattern-indexed (e.g., “update intensity of p”, “refine
distinction involving p”, “retrieve memories associated with p”). In that case, Priot (p) induces a
natural family of heuristics for scoring update actions: an action is valuable insofar as it is expected
to reduce uncertainty, sharpen distinctions, or improve control predictions for high-priority patterns.
This is one concrete route from attraction-based semantics to implementable attention scheduling.

Proposition 23 (Entropy-regularized attention allocation). Fix β > 0 and suppose P is finite.
Among all distributions α ∈ ∆(P), the maximizers of
                                     X                        1X
                           J(α) :=         α(p) Priot (p) −      α(p) log α(p)
                                                              β
                                     p∈P                       p∈P

are exactly the softmax distributions

                                                   exp(β Priot (p))
                                     α∗ (p) = P                        .
                                                  q∈P exp(β Priot (q))




                                                     311
                                                                                           P
Remark 762. A standard proof uses Lagrange multipliers: optimize J(α) subject to              p α(p) = 1
and α(p) ≥ 0. Differentiating yields
                                               1
                                 Priot (p) −     (1 + log α(p)) + λ = 0,
                                               β
so α(p) ∝ exp(β Priot (p)), and normalization gives the stated form. The entropy term is strictly
concave in α (on the simplex interior), so the optimizer is unique when all α(p) > 0.
Remark 763. This proposition says: if you want to allocate attention to maximize expected pri-
ority, but you also penalize excessively peaky allocations using Shannon entropy, then the optimal
allocation has the familiar exponential form. In other words, “soft attention” is not an arbitrary
heuristic; it is the exact optimizer of a simple and interpretable objective.
Remark 764. The parameter β plays the role of an inverse temperature. As β → ∞, the entropy
penalty vanishes and α∗ concentrates on patterns with maximal Priot (p), yielding a nearly greedy
attentional focus; as β → 0+ , the entropy term dominates and α∗ tends toward a uniform allocation
over P, representing highly diffuse or exploratory attention. Thus, β provides a compact handle on
the sharpness of attentional selection, independent of the underlying semantics of priority.
Remark 765. The result matters here because it gives a canonical mathematical mechanism for
turning attraction scores into a distribution αt that can be compared to the earlier focus defini-
tion. It therefore makes contact between the qualitative Hyperseed narrative about attention and a
quantitative optimization principle common in both cognitive modeling and machine learning. In
particular, it turns an ordinal ranking of patterns (what is more or less attractive) into a cardi-
nal allocation rule (how much attention each pattern receives), which is necessary if attention is
later treated as a measurable bottleneck. The same mechanism also clarifies what it means for at-
tention to be “bounded”: the entropy term encodes a soft resource constraint that penalizes overly
concentrated allocations unless the priorities justify them.
Remark 766. The connection to the rest of the document is direct: predictive attraction (Sec-
tion 14.3) feeds Priot , which feeds an attention distribution αt , which then gates which patterns
and knowledge types can participate in cognitive synergy (Section 15.6). This makes αt a control-
like interface between evaluation and participation: it is computed from internal scores, but it has
externally visible consequences for which inference steps, memory retrievals, and action propos-
als are even available to be composed. Seen this way, Priot plays the role of an energy landscape
over patterns, while αt is the induced sampling or allocation policy used by downstream cognitive
processes.
Proof. This is the standard Lagrange-multiplier calculation
                                                         P      for maximizing a linear functional with
an entropy regularizer under the simplex constraint p α(p) = 1. Differentiating the Lagrangian
yields Priot (p) − β1 (1 + log α(p)) = λ for all p, which implies α(p) ∝ exp(β Priot (p)). To make the
                                                                             P                   1
dependence explicit,
                   P one may start from an objective of the form J(α)P = p α(p) Priot (p) + β H(α)
with H(α) = − p α(p) log α(p), and impose α(p) ≥ 0 with                 p α(p) = 1. The stationarity
condition above holds on the interior (where α(p) > 0); at the optimum one indeed gets strictly
positive weights whenever β is finite and the priorities are finite, so the interior calculation is self-
consistent. Solving the first-order condition gives α(p) = exp(β(Priot (p) − λ) − 1), and the scalar
λ is fixed by the normalization constraint, yielding the familiar normalized softmax form.

Remark 767. At a high level, the proof works because the objective J(α) is strictly concave in α
on the interior of the simplex: a linear term plus (negative) entropy. Strict concavity guarantees a

                                                    312
unique optimum (up to degeneracies when priorities tie), and the first-order condition characterizes
it. Equivalently, one can view theP optimization as minimizing a Kullback–Leibler divergence to a
Gibbs distribution: maximizing p α(p)Priot (p) + β1 H(α) is the same as minimizing KL(α k πβ )
where πβ (p) ∝ exp(β Priot (p)). This perspective makes clear why the solution has full support for
finite β (no pattern is given exactly zero attention unless forced by infinite negative priority), and
why ties in Priot can yield symmetry-induced degeneracies only in the limiting cases where the
objective effectively becomes linear.
                                                              P
Proof sketch. Introduce a Lagrange multiplier λ to enforce p α(p) = 1. Taking derivatives with
respect to each coordinate α(p) yields an equation of the form log α(p) = β(Priot (p) − λ) − 1.
Exponentiating gives an P  unnormalized exponential distribution, and the normalization constant
is the partition function q exp(β Priot (q)). In other words, the multiplier λ is nothing but (a
shifted version of) the log-partition function that ensures the simplex constraint is satisfied, and it
couples all coordinates of α through a single global normalization. The same algebra also shows the
invariance under shifting priorities by a constant: replacing Priot (p) by Priot (p) + c multiplies all
unnormalized weights by eβc , which cancels after normalization, so only relative priority differences
matter.                                                                                              
Remark 768. Geometrically, one may picture the simplex ∆(P) as a polytope and the entropy
term as a barrier that discourages sliding onto its faces. As β → ∞, the barrier weakens and
the optimum approaches a hard argmax (full focus on the best pattern). As β → 0, the barrier
dominates and the optimum approaches uniform attention. Thus β is a temperature-like knob
interpolating between exploration and exploitation, but now phrased as an internal allocation of
genenergy. A complementary interpretation is that β sets the sensitivity of allocation to priority
gaps: for moderate β, small differences in Priot produce gently varying weights, while for large β
the distribution becomes sharply peaked and effectively implements winner-take-most selection. This
matters for cognitive synergy because it controls how many distinct pattern types can remain active
enough to interact; overly large β risks premature single-pattern lock-in, whereas overly small β
disperses genenergy so widely that no pattern is sufficiently amplified to contribute strongly.
Remark 769. Proposition 23 does not claim Hyperseed requires softmax attention. It only shows
one clean way to connect the earlier notion of predictive attraction to a concrete bounded-resource
allocation rule. More broadly, the proposition functions as an existence proof that “attraction →
gated participation” can be implemented by a principled optimization criterion, rather than by an
ad hoc mapping. Alternative mechanisms (e.g., sparsemax/entmax variants, thresholded mixtures,
or constraint-based allocations) could be substituted if they better match the desired phenomenology,
but the softmax case provides a simple baseline with a clear control parameter and well-understood
limiting behavior.

15.4    Varieties of knowledge as typed pattern structures
Hyperseed treats “knowledge” as a family resemblance notion: multiple distinct types of stored
content play different roles in prediction and control. The ontology offers a pragmatic classification
for human-like minds; we formalize it as a family of typed stores. In this framing, a “store” is
not merely a container of propositions, but a structured substrate whose items behave like typed
pattern constraints: each type comes with characteristic generalization behavior, characteristic
forms of evidence, and characteristic ways it can be brought to bear on ongoing perception/action
loops.
Definition 198 (Knowledge type). A knowledge type T for a system S consists of:

                                                 313
(a) a carrier set (or space) KT of knowledge items;

(b) a semantics map SemT : KT → S that interprets items as constraints on patterns, processes,
    or goals;

(c) an update operator (or family of operators) UpdT specifying how items are learned, revised, or
    forgotten;

(d) an interface specifying which other types it can exchange information with.

Remark 770. One can make the “update operator” more explicit as a rule family of the form

                                      UpdT : KT × ET → KT ,

where ET denotes the space of admissible evidential inputs for type T (e.g. sensory episodes, coun-
terexamples, rewards, demonstrations, proofs, or internal audit signals). What matters for the
present section is that different knowledge types have different ET and different invariants under
update (for example, exemplar memories may be capacity-limited while declarative stores may be
consistency-limited only by attention and time).

Remark 771. The point of calling these “types” is not to reify a metaphysical taxonomy, but to
mark distinct update dynamics and distinct failure modes. A knowledge item is not only something
that can be true or false; it is something that can be learned, revised, forgotten, communicated, and
used for control. These verbs differ across types, and this difference is precisely what makes cross-
type synergy possible [19].

Remark 772. The “interface” component (d) is where cognitive synergy becomes operational: it
specifies what queries a store can answer, what messages it can accept, and what it can emit to other
stores. Concretely, an interface may include (i) a set of accessors (e.g. retrieve-by-key, retrieve-by-
similarity, retrieve-by-goal), (ii) a set of translators into other representational formats, and (iii)
gating conditions (e.g. only export high-confidence items, or only import items when attention flags
a relevant context boundary). In practice, interfaces are also where resource constraints show up:
two knowledge types may be semantically compatible but interface-incompatible because translation
is too expensive under current genenergy/attention budgets.

Remark 773. One can view SemT as a disciplined way of saying “what does this store constrain?”
For declarative knowledge it constrains beliefs about events; for procedural knowledge it constrains
the space of policies; for attentional knowledge it constrains how the system searches its own com-
putations. In each case the semantics map ties a symbolic or stored item back to patterns and
processes (Hyperseed-Concept 157; Hyperseed-Concept ??). A useful way to read SemT is as a
bridge from a compact stored token to a (possibly large) set of permitted pattern instantiations: the
token is small, but its denotation is a constraint over the system’s pattern space.

15.4.1   Declarative knowledge
Definition 199 (Declarative knowledge). Declarative knowledge is a store of pattern beliefs, often
(but not necessarily) linguistically expressible. Formally, let L be a language for talking about
events/patterns. A declarative state is a valuation

                                       Kdec : L → V = [0, 1]2 ,

assigning each formula a p-bit degree of positive/negative evidence (Section 3.2).

                                                 314
Remark 774. Although L can be taken as a linguistic/propositional language, nothing in the
definition requires natural language; L may equally be a structured pattern description language
(e.g. relational templates over perceived entities, temporal claims, or causal sketches). The essential
ingredient is that formulas in L are the kind of objects that can be queried by other subsystems (e.g.
planning, explanation, counterfactual reasoning), and that their evidence values can be updated by
a mix of perception, testimony, and internal consistency checks.

Remark 775. Intuitively, Kdec (ϕ) is the system’s present evidential stance toward the claim ϕ:
not merely “how likely,” but “how supported” and “how refuted,” separately. This is a natural fit
for observer-relative and potentially inconsistent boundaries, where one can have both substantial
evidence for and against the same proposition without collapse (Hyperseed-Concept 65; see also
paraconsistent motivations in [23, 24]).

Remark 776. Update for declarative knowledge typically consists of accumulating or discounting
evidence while preserving the separation between positive and negative support. For example, a sin-
gle observation may increase the first coordinate without decreasing the second, while a debunking
argument may increase the second coordinate without forcing the first to vanish. This is relevant to
attention because conflict (high support and high refutation) is a natural trigger for targeted infor-
mation gathering: attention can treat such formulas as “open loops” whose resolution is valuable
but not always urgent.

Remark 777. A simple example is a vague predicate like “the room is quiet.” A system might
store Kdec (quiet) = (0.7, 0.4), reflecting positive evidence from a low sound meter and negative
evidence from intermittent noise. The usefulness is that later inference can proceed without forcing
premature consistency; attention can then decide whether to spend genenergy resolving the conflict
or to act under it.

15.4.2   Procedural knowledge
Definition 200 (Procedural knowledge). Procedural knowledge consists of “if in context C, doing
procedure π tends to achieve goal G.” Let C be a set of contexts and G a set of goals. Let Π be a
set of procedures (policies, programs, controllers). A procedural knowledge item is a triple (C, π, G)
together with an evidence value ProcEvd(C, π, G) ∈ V.

Remark 778. Here “context” C should be read broadly: it may denote an external situation (terrain
type, social setting), an internal state (fatigue, low battery), or a conjunction of both, and it may
be crisp or fuzzy depending on the system’s perceptual and conceptual granularity. In particular,
procedural knowledge can be indexed by attentionally constructed contexts: the system may only
carve out a context boundary (and thus create a stable key C) once attention has repeatedly found
that a certain cluster of features predicts procedure success/failure.

Remark 779. Procedural knowledge is “knowing how” rather than “knowing that.” The evidence
value ProcEvd(C, π, G) plays the same paraconsistent role as in declarative knowledge, but now
attached to a claim about the efficacy of a procedure. This lets a system represent, for instance,
that a policy often works but has known failure modes, without reducing everything to a single
success probability (Hyperseed-Concept ??; Hyperseed-Concept ??).

Remark 780. Procedural update is typically driven by rollouts, trial-and-error, imitation, and
counterfactual evaluation: a single attempted execution of π under an estimated C contributes
evidence to ProcEvd(C, π, G), while diagnosis of why an attempt failed can refine the context key


                                                 315
(the system may split C into subcontexts where the procedure behaves differently). This is one of
the primary points of interaction with attention: attention determines which trials to run, which
failures to analyze deeply, and which context splits are worth the representational complexity.
Remark 781. As an example, C might be “slippery ground,” π might be “walk slowly,” and G
might be “reach destination without falling.” The system may have positive evidence from past
successes and negative evidence from rare but salient failures. Such items feed directly into control
selection (Section 14) and can be prioritized by attention when a context boundary becomes active.

15.4.3   Sensory knowledge
Definition 201 (Sensory knowledge). Sensory knowledge is memory enabling discrimination: after
sensing an item s, the system can later distinguish a copy/recurrence of s from similar non-copies.
Formally, let S be a stimulus space and let d be a similarity (pseudo)metric. A sensory memory
state is a finite set of stored exemplars {sj } together with an embedding φ : S → Y such that
discrimination is performed by thresholding distances dY (φ(s), φ(sj )).
Remark 782. This definition abstracts over many implementations (template matching, nearest-
neighbor retrieval, metric learning, associative memories) by highlighting the functional role: a
discrimination operator induced by storing exemplars and comparing them in an internal space.
The finiteness of {sj } is not merely technical: it encodes the idea that sensory memory is usually
capacity-limited, so forgetting (or prototype compression) is a normal and often desirable update
dynamic.
Remark 783. This definition captures the bare bones of recognition by similarity: store a few
exemplars, map stimuli into an internal space Y , and then declare “match” when the embedded
distance is small. The pseudo-metric d allows the usual flexibility: different stimuli may be deemed
zero-distance by the system because it cannot or does not care to distinguish them at the current
resolution.
Remark 784. The embedding φ can be fixed, learned, or attention-modulated. In particular, at-
tentional control can act by temporarily changing the effective metric (or the threshold) so that, for
the current task, some distinctions are sharpened while others are collapsed. This gives one route to
cognitive synergy between sensory and declarative/procedural stores: declarative hypotheses can cue
which sensory dimensions should matter, and procedural demands can cue which discriminations
are worth allocating representational capacity to.
Remark 785. A simple example is face recognition: S is the space of face images, Y is an em-
bedding space learned by a neural network, and the exemplars {sj } are stored reference faces. The
utility of formalizing sensory knowledge this way is that it makes explicit where genenergy is spent:
improving φ, storing more exemplars, or changing thresholds are all internal update actions (Sec-
tion 15.3).
Remark 786. The same schematic separation also clarifies what can be held fixed while something
else is adapted. For instance, if φ is treated as stable (a “frozen” encoder), then sensory improve-
ment must occur via exemplar management (adding, pruning, reweighting, or clustering {sj }) and
via decision rules (thresholds, rejection options, abstention policies). Conversely, if exemplar mem-
ory is constrained, genenergy can be redirected toward learning a more invariant φ so that fewer
exemplars suffice. Making these tradeoffs explicit is useful when diagnosing failure: poor recog-
nition might come from an inadequate embedding, from stale exemplars, or from a miscalibrated
acceptance criterion, and these correspond to distinct internal actions and costs.

                                                 316
15.4.4    Attentional knowledge
Hyperseed highlights a specific meta-knowledge type: learned regularities of attention shift.
Definition 202 (Attentional knowledge). Let X be a set of “attention targets” (pattern classes,
module clusters, or questions). Attentional knowledge consists of regularities of the form: “when
attention is on X, it often shifts to Y , and this shift is associated with goal success.” Formally, an
attentional knowledge state may be represented as a family of kernels
                             Katt (Y | X, G) ∈ V,       X, Y ∈ X , G ∈ G,
encoding (paraconsistent) evidence that shifting focus from X to Y tends to support G.
Remark 787. This is knowledge about the system’s own search procedure: it stores which transi-
tions of attentional focus have historically been fruitful. The notation Katt (Y | X, G) is deliberately
reminiscent of a conditional probability kernel, but valued in V = [0, 1]2 to permit mixed evidence.
The targets X can be pattern sets, modules, or even explicit questions (Hyperseed-Concept ??).
Remark 788. Interpreting Katt as a kernel emphasizes that it can be many-to-many and con-
textually gated by goals: from the same X there may be several productive next foci Y , and the
ranking can depend strongly on G. The paraconsistent valuation V = [0, 1]2 can be read as sepa-
rately tracking evidence-for and evidence-against a shift, so that the system may represent both (i)
that a transition is often helpful in some regimes, and (ii) that it is also often harmful or distracting
in others, without collapsing this tension into a single scalar. This matters for attention control,
since overly aggressive “always shift to Y ” habits are a common pathology in bounded systems.
Remark 789. One can also regard Katt as an internal, learned “operator selection” map: X names
a current representational neighborhood (e.g., a memory store, a perception stream, a planning mod-
ule), and Y names which neighborhood to query next. In this reading, attentional targets are not
only semantic objects but also interfaces to computational resources, so the kernel summarizes regu-
larities about which interface-switches pay off under which goals. This makes attentional knowledge
a natural site for genenergy expenditure: updating Katt changes how future computation is allocated
even when the underlying declarative beliefs remain unchanged.
Remark 790. A simple example: when debugging code (target X), shifting attention to “construct
a minimal reproducible example” (target Y ) often supports the goal G of fixing the bug. The system
may not be able to justify why this works declaratively, yet it can learn the attentional transition
as a useful habit. This is one of the clearest loci where cognitive synergy manifests in practice: the
system uses one knowledge type (attentional) to orchestrate updates in others.
Remark 791. In that debugging example, the shift X → Y is valuable partly because it changes the
data distribution seen by other subsystems: a minimal reproducible example compresses the search
space, reduces confounds, and yields cleaner counterfactual tests. Thus attentional knowledge can be
viewed as knowledge about which transformations of the agent’s own input streams make downstream
learning or inference cheaper. This perspective also clarifies why attentional habits can remain
useful even when they are not explicitly articulated: the relevant regularity may be procedural and
distributed across modules rather than available as a compact declarative rule.

15.4.5    Intentional knowledge
Definition 203 (Intentional knowledge). Intentional knowledge captures goal specialization: “when
pursuing goal G in context C, it is appropriate to switch to a specialized goal G1 .” Formally,
represent intentional knowledge as a relation
                             Kint (G1 | G, C) ∈ V,      G, G1 ∈ G, C ∈ C.

                                                  317
Remark 792. This is knowledge about the internal goal topology of the agent: how abstract goals
refine into more concrete subgoals when contexts shift. It is not merely planning, but a learned
mapping of which refinements tend to be appropriate. In Hyperseed terms, it is a pattern of goal-
development (Hyperseed-Concept 95; Hyperseed-Concept ??).
Remark 793. The emphasis on topology is meant literally: the agent’s goal system can be treated
as a graph (or hypergraph) where edges correspond to refinement, decomposition, or constraint addi-
tion. Then Kint (G1 | G, C) plays a role analogous to a context-sensitive adjacency relation, encoding
which outgoing refinements are supported or discouraged by experience. Because it is V-valued, the
representation can capture that a refinement is plausible yet risky, or that it is appropriate only
when further conditions (not yet represented in C) hold. This allows the agent to maintain multiple
candidate specializations without premature commitment.
Remark 794. An example: for a general goal G = “be healthy,” and context C = “winter,”
a specialized goal might be G1 = “get vitamin D.” The system may have mixed evidence about
the appropriateness of this specialization depending on other latent factors, hence the p-bit-valued
relation. Formalizing Kint is useful because it provides a precise target for attentional update actions:
one can spend genenergy revising not only beliefs and policies but also the mapping from goals to
subgoals.
Remark 795. The “appropriate to switch” phrasing is intentionally compatible with several control
regimes. In a strict regime, Kint may be used to replace G by G1 (commitment); in a softer regime, it
may spawn G1 as a concurrent subgoal (branching); and in a reflective regime, it may be treated as a
prompt for information gathering (e.g., attend to whether latent conditions hold before specializing).
These distinctions matter operationally because they correspond to different resource commitments
and different ways of recovering from a poor specialization.
Remark 796 (Why multiple knowledge types). Different types have different update dynamics and
different failure modes. Procedural knowledge can be robust without being explainable; declarative
knowledge can be communicable without being actionable; attentional knowledge can guide search
even when the system cannot articulate why the guidance works. This plurality is one of Hyperseed’s
motivations for cognitive synergy.
Remark 797. The failure-mode differences are not merely philosophical; they induce different
diagnostics and different interventions. When procedural knowledge fails, the symptom may be
brittle performance under distribution shift; when declarative knowledge fails, the symptom may be
contradiction or confabulation under questioning; when attentional knowledge fails, the symptom
may be wasted compute on unproductive loci even if the necessary facts are present somewhere in
memory. Treating these as distinct knowledge types supports targeted repair: e.g., revise a kernel
like Katt to change where the system looks, rather than trying to directly patch the content it will
eventually retrieve or infer.
Remark 798. In the Hyperseed framing, the plurality is not a defect but a structural response to
finitude: because a bounded system cannot maintain one perfect, unified representational format, it
maintains several partially overlapping ones. Synergy is then the disciplined practice of translating
between them, so that the weaknesses of one type are compensated by the strengths of another
(Hyperseed-Concept ??; [19]).
Remark 799. On this view, cognitive synergy is implemented by concrete cross-type couplings:
attentional knowledge decides which declarative store to consult; declarative knowledge can propose
new attention targets (e.g., a hypothesis suggests a test); procedural knowledge can supply fast

                                                  318
heuristics that seed deliberate reasoning; and intentional knowledge can reshape the very criteria by
which attention shifts are judged successful. The point of explicitly typing these structures (kernels
over X , relations over G ×C, etc.) is to make such couplings engineerable: each type exposes specific
“handles” for internal update actions, and genenergy can be budgeted among them rather than being
spent implicitly and opaquely.

15.5     Cognitive synergy as cross-type weakness improvement
Hyperseed’s term cognitive synergy names a ubiquitous architectural fact: complex cognition typ-
ically requires frequent exchange of intermediate products between distinct knowledge processes
(not merely “final answers”). We now give a weakness-based formalization. In particular, the
guiding hypothesis is that many of the practical benefits of “integrated cognition” can be expressed
as improved explanation quality at lower contrivance when multiple knowledge types are allowed to
interact, i.e. when one representational mode can supply constraints, priors, candidate structures,
or abstractions to another.

Remark 800. The motivating intuition is that “the whole is more than the sum of its parts”
becomes operational when translations between representational modes yield new compressions. This
is the same spirit in which pattern discovery is a compression phenomenon (Section 9; [5]), but now
lifted to an architectural level: the compression is enabled by cross-type interaction rather than by a
single homogeneous inference engine (Hyperseed-Concept 73). One may read “translation” broadly:
it can be an explicit encoder/decoder, a shared latent space, a symbolic labeling of subsymbolic states,
a compilation of rules into a policy prior, or any other mechanism by which structure found in one
knowledge store reduces the search burden in another.

15.5.1    Usefulness of a learning algorithm for a knowledge type
Definition 204 (Learning algorithms indexed by knowledge type). For each knowledge type T ,
let Alg(T ) denote a family of learning/update algorithms appropriate to T (e.g. logical inference
for declarative, reinforcement learning for procedural, metric learning for sensory). An algorithm
A ∈ Alg(T ) induces an update map UpdT,A : KT → KT .

Remark 801. This definition is a modest piece of type discipline: it says that not every learning
method is appropriate for every store. One does not typically update a sensory embedding φ by
syllogistic inference, nor update a logical theory by gradient descent—though hybrid methods exist.
By making Alg(T ) explicit, we can later speak precisely about cross-type communication: outputs of
one type become inputs to algorithms of another. A convenient side effect is that it lets us talk about
where an intervention occurs: an update that changes Kdec but leaves Kproc fixed is a different kind
of cognitive act than one that changes both, even if both ultimately serve the same downstream goal.

Remark 802. A simple example is: T = proc, Alg(T ) includes Q-learning, and UpdT,A takes
a table of action values and updates it after an episode. For T = dec, Alg(T ) might include a
paraconsistent inference procedure (Section 3.2). The usefulness of writing UpdT,A is that it lets us
treat learning steps as internal update actions in the sense of Section 15.3. It also makes iteration
                                   (n)
explicit: repeated application UpdT,A := UpdT,A ◦ · · · ◦ UpdT,A is the formal proxy for “training for
                                         |          {z         }
                                                  n times
n steps” or “performing n rounds of inference,” and so properties like convergence, brittleness, or
sensitivity to initialization can be attached to the map rather than left implicit.



                                                  319
Definition 205 (Usefulness). Fix a goal set G and a success predicate Succ(G). An algorithm
A ∈ Alg(T ) is useful for knowledge type T if, across the contexts of interest, repeatedly applying
UpdT,A tends (in expectation) to increase the probability of achieving some goals in G. Equivalently,
“invoking A to learn T -knowledge” forms a valuable pattern in the system’s activity (Section 9).

Remark 803. The definition says: a learning algorithm is not judged by elegance but by teleology—
by whether it improves goal achievement in the contexts that matter. This is a deliberately pragmatic
stance in the spirit of Hyperseed’s observer-relative epistemology (Hyperseed-Concept ??; Hyperseed-
Concept 160). Here “contexts of interest” can be understood as a (possibly implicit) distribution
over task situations, sensory histories, internal states, and resource constraints; the expectation is
taken with respect to that distribution together with any stochasticity in the algorithm or environ-
ment. This framing also makes room for bounded rationality: an algorithm may be “useful” because
it improves timely success under limited compute, even if an idealized unbounded method would
eventually do better.

Remark 804. As an example, a memory consolidation method might be “useful” if it increases
the probability of later successful recognition or planning, even if it occasionally strengthens some
false declarative beliefs. The paraconsistent setting makes room for such tradeoffs: usefulness is an
expected-value criterion rather than a demand for global consistency. In the same vein, a heuristic
that increases success on a target regime while slightly degrading performance on rare corner cases
can still qualify as useful—and such regime-dependence will later be important when we discuss
synergy, since cross-type information flow often acts as a mechanism for shifting the system toward
the regimes where its individual methods are strongest.

15.5.2   Explanations, weakness, and contrivance cost
We measure the “simplicity” or “generality” of an explanatory construct by a scalar weakness. This
is a specialization of the quantale weakness ideas from Section 3.7. Intuitively, “weak” explanations
are permissive (they rule out fewer possibilities), while “strong” ones are more committal (they
encode many fine distinctions); contrivance cost is then the currency in which committal structure
is paid for.

Definition 206 (Explanations and weakness). Fix a behavior (or dataset) b. Let E(b) be a set of
candidate explanations of b (models, hypotheses, plans, proofs, causal graphs, etc.). Assume each
explanation E ∈ E(b) comes with:

(a) an adequacy score Fit(E) ∈ [0, 1] (how well it predicts/explains/controls b);

(b) a weakness Weak(E) ∈ (0, 1] (how few distinctions it makes; larger is weaker).

Define the contrivance cost (description-length proxy)

                                Con(E) := − log Weak(E) ∈ [0, ∞).

Remark 805. Weakness is a formal proxy for a familiar epistemic virtue: an explanation that
makes fewer distinctions is, other things equal, more general and less brittle. In the Hyperseed
development, weakness is not mere vagueness; it is a structured notion built to live in quantale
settings where composition and partial order matter (Hyperseed-Concept 202; Hyperseed-Concept
??; [3, 2]). At a purely scalar level, one can read Weak(E) as measuring “how large a set of worlds”
(or latent configurations) remain compatible with E; then larger Weak(E) corresponds to a coarser
partition of possibilities, hence fewer encoded distinctions.

                                                 320
Remark 806. A simple example: suppose b is a dataset generated by a linear relation plus noise. A
linear model may have high Weak(E) (few degrees of freedom, fewer distinctions) and decent Fit(E),
while a high-degree polynomial can achieve higher fit but lower weakness (more contrivance). The
cost Con(E) = − log Weak(E) then behaves like a description length in the spirit of algorithmic
information theory [16]. One may also view this as a minimal-description-length style tradeoff:
among explanations with comparable adequacy, those with larger weakness (smaller Con) are pre-
ferred because they are less likely to be overfit to incidental structure in b.
Remark 807. The usefulness of Con is that it makes the Russellian demand for clarity operational:
to explain is to compress, and to compress is to pay for distinctions. The logarithm converts
multiplicative weakness comparisons into additive costs, which is exactly the currency in which
tradeoffs and budgets are most naturally expressed. Because Weak(E) ∈ (0, 1], the sign convention
ensures Con(E) ≥ 0 and assigns infinite penalty only to the limiting case of Weak(E) → 0, i.e. to
explanations so highly contrived that they are maximally distinction-heavy. The choice of logarithm
base merely selects units (e.g. natural nats versus bits with log2 ), and the additive form is what
matters for comparing composite explanations built from multiple sub-structures.
Remark 808. It is often helpful to interpret the pair (Fit(E), Con(E)) as defining a Pareto-style
frontier: improving fit typically requires paying additional contrivance, while reducing contrivance
may reduce fit. In that light, “weakness improvement” refers to moving to an explanation E 0 with
comparable (or higher) adequacy but lower cost, e.g. Fit(E 0 ) ≥ Fit(E) and Con(E 0 ) < Con(E).
This is the axis along which cross-type interaction will be cast as synergistic: a translation from
one representational mode to another can supply constraints or latent variables that let the second
mode reach the same adequacy with fewer ad hoc distinctions.
Remark 809. The use of − log is optional but convenient: multiplicative weakness becomes additive
cost. Any monotone transform would serve similarly.
Definition 207 (Best achievable contrivance under a fit threshold). Fix τ ∈ (0, 1]. For a col-
lection of knowledge types T (e.g. a subset of the full architecture), let ET (b) be the explanations
constructible using only those types. Define

                       Con∗ (T ; τ ) := inf{Con(E) : E ∈ ET (b), Fit(E) ≥ τ }.

Equivalently, Con∗ (T ; τ ) is the minimal contrivance needed to reach fit τ using the knowledge in T .
Remark 810. The quantity Con∗ (T ; τ ) is a performance frontier: it asks for the least contrived
(most weak/general) explanation that still meets an adequacy demand τ . The infimum allows that
the best tradeoff might be approached by a sequence of explanations even if not attained exactly,
which is important when the space of explanations is large or continuous.
Remark 811. In practice, one may think of τ as a required success rate, prediction accuracy, or
control competence. Then Con∗ (T ; τ ) is the minimal “model complexity” that the architecture frag-
ment T must deploy to achieve that competence. This creates a clean interface to later “intelligence
under budget” notions (Section 21).

15.5.3   Synergy as strict subadditivity of contrivance
Definition 208 (Cognitive synergy between knowledge sets). Let T1 , T2 be two disjoint sets of
knowledge types and fix τ ∈ (0, 1]. We say there is cognitive synergy at level τ between T1 and T2
if
                          Con∗ (T1 ∪ T2 ; τ ) < Con∗ (T1 ; τ ) + Con∗ (T2 ; τ ).

                                                 321
The synergy gain is the positive part
                                                                                       
                Σ(T1 , T2 ; τ ) := Con∗ (T1 ; τ ) + Con∗ (T2 ; τ ) − Con∗ (T1 ∪ T2 ; τ ) .
                                                                                       +

Remark 812. In plain terms: synergy means that letting the two knowledge sets interact yields
an explanation meeting the same adequacy threshold with strictly less contrivance than one could
achieve by using each set in isolation and then “adding” the results. The positive-part operator
(·)+ ensures Σ is always nonnegative, so it behaves like a measurable gain rather than a signed
difference.
Remark 813. A simple example is a system where declarative knowledge supplies a compact causal
rule that lets procedural learning drastically reduce exploration. Separately, each subsystem must
encode many exceptions; together, one subsystem supplies a compression that the other can exploit,
lowering the overall contrivance needed for fit. This is precisely the kind of architectural phenomenon
discussed under the name “cognitive synergy” in [19] (Hyperseed-Concept 73).
Remark 814. The definition captures Hyperseed’s informal criterion: exchanging intermediate
representations is useful when it enables a less contrived (weaker, more general) explanation to
achieve the same level of adequacy.

15.5.4    A sufficient condition: monoidal compositionality of weakness
The simplest theorem states that if weakness is compositional across independent subsystems, then
combining subsystems cannot be worse (in contrivance cost) than treating them separately.
Definition 209 (Multiplicative weakness model). Assume that when two explanations E1 , E2 are
combined (e.g. run in parallel, or glued along an interface) to form E1 ⊗E2 , their weakness satisfies

                                Weak(E1 ⊗ E2 ) ≥ Weak(E1 ) Weak(E2 ).

Remark 815. This condition says that composing explanations does not force additional distinc-
tions beyond those already made by the parts. Since weakness is larger when fewer distinctions
are made, the inequality Weak(E1 ⊗ E2 ) ≥ Weak(E1 )Weak(E2 ) asserts that the composed system
is at least as “weak” as the multiplicative baseline. This is a natural monoidal-style assumption
consistent with the quantale flavor of weakness developed earlier [3] (Hyperseed-Concept ??).
Remark 816. A concrete example is when E1 and E2 explain disjoint aspects of the data b and
are glued without sharing parameters. Then the combined description length is roughly additive,
corresponding to multiplicative weakness. The reason to formalize this is not because independence
always holds, but because it gives a clean baseline against which emergent (strict) synergy can later
be measured.
Proposition 24 (Subadditivity of contrivance under multiplicative weakness). If Weak(E1 ⊗E2 ) ≥
Weak(E1 )Weak(E2 ) for all composable E1 , E2 , then for all disjoint knowledge sets T1 , T2 and all τ ,

                            Con∗ (T1 ∪ T2 ; τ ) ≤ Con∗ (T1 ; τ ) + Con∗ (T2 ; τ ).

In particular, the synergy gain Σ(T1 , T2 ; τ ) is well-defined and nonnegative.
Remark 817. The proposition says that, under the multiplicative weakness model, there is never
a penalty (in minimal contrivance) for allowing two disjoint knowledge sets to be used together.
Even if they do not yield strict synergy, they can at least be composed without worsening the best
achievable tradeoff.

                                                     322
Remark 818. This result is important mainly as a sanity check: it ensures that the synergy gain
defined earlier behaves as a nonnegative quantity under a natural compositionality assumption. It
thereby connects the architectural idea of cross-type interaction to the algebraic idea that weakness
behaves well under composition (a theme running through the weakness/pattern layers of the docu-
ment). In particular, the inequality can be read as saying that “having access to more explanation
types” cannot make the best achievable contrivance frontier worse, provided that the architecture
admits a way of juxtaposing explanations without destroying their adequacy. This is the minimal
monotonicity one expects from any notion of joint modeling capacity: if it were violated, then
the definitions of Weak, Con, and the admissible explanation classes would be misaligned with the
intended semantics of “adding representational degrees of freedom.”
Remark 819. The link to later sections is that attention (as a gating mechanism) determines
whether compositions like E1 ⊗ E2 are actually realized in time. The inequality here is about repre-
sentational possibility; Section 15.6 is about resource-mediated actuality. Said differently, Proposi-
tion 24 is “offline”: it assumes the agent is permitted to form the composite explanation and then
measures what cost is achievable in principle. Attention introduces an “online” constraint: even if
E1 and E2 exist and can be composed, the system may fail to instantiate E1 ⊗ E2 because the gating
policy does not co-activate the relevant pathways, or because partial activation yields an effectively
degraded fit that falls below τ .
Proof. Let ε > 0. Choose explanations E1 ∈ ET1 (b) and E2 ∈ ET2 (b) with Fit(Ei ) ≥ τ and
Con(Ei ) ≤ Con∗ (Ti ; τ ) + ε. (Here we use that Con∗ (Ti ; τ ) is an infimum: for any ε > 0 there exists
an admissible explanation whose contrivance lies within ε of the optimum.) Combine them to form
E := E1 ⊗ E2 . Assuming the combination preserves fit at level τ (e.g. the two parts address
disjoint aspects of b), we have E ∈ ET1 ∪T2 (b). The “disjoint aspects” condition is one sufficient
way to guarantee that the joint explanation does not introduce interference; more generally, any
architectural condition ensuring that the composite retains Fit ≥ τ is enough for the argument.
Then

                 Con(E) = − log Weak(E) ≤ − log(Weak(E1 )Weak(E2 ))
                          = Con(E1 ) + Con(E2 ) ≤ Con∗ (T1 ; τ ) + Con∗ (T2 ; τ ) + 2ε.

The first inequality is exactly where the multiplicative weakness hypothesis enters; it is also where
one implicitly uses that the relevant weakness quantities lie in (0, 1] so that − log is well-defined
and order-reversing in the expected way. Taking the infimum over admissible E and then letting
ε → 0 yields the inequality. Equivalently, the construction shows that for each ε one can exhibit a
feasible joint explanation whose cost is within 2ε of the sum of the separate optima, which forces
the joint optimum not to exceed that sum in the limit.

Remark 820. The proof is a standard ε-approximation argument: one takes nearly optimal ex-
planations from each side, composes them, and then uses the multiplicative weakness hypothesis to
show the cost of the composite is no more than the sum of the costs. The passage to the infimum
and the limit ε → 0 then yields the stated inequality for the optimal frontiers. Conceptually, this is
the same pattern as “subadditivity” arguments in coding and complexity: once a candidate compos-
ite description is written down, optimality can only improve upon it, never worsen relative to that
explicit construction.
Proof sketch. Pick E1 and E2 within ε of their respective optima. Form the composite E = E1 ⊗E2 .
Multiplicative weakness turns into additive cost because of the − log. This gives an upper bound
on Con∗ (T1 ∪ T2 ; τ ), and letting ε → 0 removes slack. One can interpret the “slack” as coming

                                                  323
solely from the choice of near-optimal witnesses rather than exact minimizers; no special convexity
or continuity assumptions are required beyond the basic ability to approximate an infimum.       
Remark 821. The key step is exactly why the logarithm was chosen: it converts the structural
hypothesis about weakness under composition into the familiar subadditivity inequality for costs.
Visually, if one thinks of weakness as a kind of “volume” of indistinction, then composing inde-
pendent explanations multiplies volumes; contrivance cost is then the negative log-volume, hence
additive. This is also the sense in which “independence” (or sufficiently weak interaction) is the
baseline case: when the two explanations do not share compressive structure, one expects multipli-
cation of volumes and hence mere additivity of costs, leaving no room for strict gains.

15.5.5   When does synergy become strict?
Proposition 24 only guarantees “no penalty” for combining knowledge types. Hyperseed’s intended
phenomenon is stronger: strict improvement, driven by cross-type emergent patterns (Section 9).
The strict case corresponds to the presence of shared structure that is representable once in the
joint space but would have to be redundantly encoded (or simulated) in each type-specific space if
one enforced modularity.
Definition 210 (Cross-type emergent compression). Let T1 , T2 be disjoint knowledge sets. We say
there is a cross-type emergent compression pattern for b if there exists an explanation E ∈ ET1 ∪T2 (b)
with Fit(E) ≥ τ such that for every decomposition E ≈ E1 ⊗ E2 with Ei ∈ ETi (b) and Fit(Ei ) ≥ τ ,
one has
                                  Con(E) < Con(E1 ) + Con(E2 ).
In this formulation, the strict inequality is uniform over all admissible factorizations: it is not
enough that some particular split is inefficient; rather, every attempt to realize the same explanatory
content via separate type-restricted components incurs additional contrivance.
Remark 822. This definition formalizes the intuitive notion of emergence as irreducible compres-
sion: the joint explanation achieves a description-length advantage that cannot be recovered by any
attempt to factor it into separate explanations for the two subsystems. The approximate equality
E ≈ E1 ⊗ E2 is intentionally informal: it stands for any decomposition notion appropriate to the
architecture (e.g. separable parameterizations, modular pipelines, or independent subgraphs). The
intent is that E ≈ E1 ⊗ E2 should range over all “reasonable” ways of enforcing a two-part modular
interpretation; the strict inequality then says that the best such modular account still fails to match
the compression achieved by a genuinely cross-type representation.
Remark 823. A simple example is when a shared latent variable simultaneously explains sensory
regularities and guides procedural choices; representing it once in a cross-type structure is less
contrived than duplicating its effect separately in each module. In pattern language, the latent
variable is an emergent pattern spanning multiple representational strata [5] (Hyperseed-Concept
??). One can also view this as a coordination advantage: a single latent factor couples prediction
and control constraints, so that the same degrees of freedom satisfy both simultaneously, whereas
separate modules must “rediscover” compatible structure through additional parameters or ad hoc
interface conventions.
Remark 824. The usefulness of naming emergent compression explicitly is that it makes “synergy”
empirically testable in principle: one can compare minimal contrivance frontiers under enforced
modularization versus allowed interaction, and ask whether a strict gap appears. Operationally,
this suggests experimental protocols where the architecture is trained under different constraints

                                                 324
(e.g. blocked cross-attention, frozen communication channels, or enforced factorizations) and the
resulting best-achievable Con∗ curves are compared at matched fit thresholds.

Proposition 25 (Emergent compression implies positive synergy). If there exists a cross-type
emergent compression pattern for b at level τ , then Σ(T1 , T2 ; τ ) > 0.

Remark 825. The proposition says that the emergent compression condition is not merely poetic:
it entails a strict inequality at the level of the optimal contrivance frontiers. Thus, emergence (as
defined) is a sufficient condition for positive synergy gain. In other words, an explicit witness E
whose cost beats every separable decomposition forces the joint optimum to beat the sum of separate
optima by at least some nonzero margin (potentially small, but strictly positive in the sense of the
inequality).

Remark 826. This connects tightly to the definition of Σ: the synergy gain is exactly the amount
by which the joint optimum beats the sum of the separate optima. Emergent compression provides
a witness E that beats every separable decomposition, hence it beats the optimal separable costs in
particular. Concretely, if one denotes by Csep the infimum of Con(E1 )+Con(E2 ) over all admissible
(E1 , E2 ) with Fit ≥ τ , then emergent compression asserts Con(E) < Csep , while Proposition 24
ensures the joint optimum is at most Csep ; together these force a strict improvement and hence
Σ > 0.

Proof. Let E witness emergent compression. By definition, Con(E) < Con(E1 ) + Con(E2 ) for
any admissible decomposition. Taking infima over admissible E1 and E2 implies Con(E) <
Con∗ (T1 ; τ ) + Con∗ (T2 ; τ ). Since Con∗ (T1 ∪ T2 ; τ ) ≤ Con(E), we obtain strict subadditivity and
hence a positive synergy gain.
    To unpack the two inequality steps: the emergent witness E is itself a jointly-constructed
explanation drawn from the hypothesis class available when T1 and T2 are allowed to interact,
so it is a feasible candidate in the joint optimization defining Con∗ (T1 ∪ T2 ; τ ). Meanwhile, each
admissible decomposition corresponds to a pair of feasible candidates for the separate optimizations
defining Con∗ (T1 ; τ ) and Con∗ (T2 ; τ ), so their infima provide a lower envelope over all separable
ways of reaching fit threshold τ . The strictness is crucial: because Con(E) is strictly below every
decomposed cost, it is strictly below the best decomposed cost as well.

Remark 827. The proof is a direct “witness to strictness” argument. The emergent compression
hypothesis is already quantified over all decompositions; taking infima simply extracts the best pos-
sible decomposed costs and preserves strict inequality. The final step uses that the joint optimum is
no worse than any particular joint explanation.
    Equivalently, one can view the argument as comparing two feasible regions: (i) the joint feasible
set in which hypotheses may couple degrees of freedom across T1 and T2 , and (ii) the restricted
feasible set in which hypotheses must factor into components sourced separately. Emergent com-
pression asserts that the restricted feasible set cannot realize the low-contrivance point achieved by
E. The infimum operation then formalizes “best possible under the restriction” without changing
the direction (or strictness) of the comparison.

Proof sketch. Use the emergent E to show it beats every decomposable pair (E1 , E2 ). Therefore it
beats the best decomposable pair, i.e. the sum of the separate optima. Since the joint optimum is
at most the cost of E, the joint optimum is strictly less than the sum, giving Σ > 0.
   In other words, E is a certificate that “interaction helps”: once you exhibit a single joint
construction whose contrivance lies below the entire separable baseline, you immediately obtain a
nonzero gap between the joint optimum and the best separable performance.                       

                                                 325
Remark 828. Visually, if one plots the best-achievable contrivance as a function of enforced mod-
ularization constraints, emergent compression says the unconstrained curve dips below the sum of
the constrained minima. This is a precise sense in which interaction creates a new “path of least
contrivance” through hypothesis space.
    The same picture can be read as a “regularization relief ” effect: the constraint that hypotheses
must split across representational types can force each side to pay separate description length for
structure that, in a coupled representation, is shared or reused. The dip corresponds to a regime
where shared latent structure is expressible only when cross-type coupling is allowed.

15.5.6    A criterion for “synergy increases effective intelligence”
This paper later defines intelligence in terms of tasks (Section 21). For present purposes we state
a local criterion that connects synergy to solvable task sets under resource limits.
Definition 211 (Budgeted solvability criterion). Fix a fit threshold τ and a contrivance budget B.
A task/dataset b is solvable by knowledge set T at budget B if Con∗ (T ; τ ) ≤ B.
   Note that this definition is intentionally one-sided: it declares solvability whenever there exists
some explanation meeting the fit threshold with contrivance at most B, i.e. it uses the minimal
contrivance Con∗ as a summary of the most efficient available strategy within T .
Remark 829. This is the simplest possible “resource-bounded competence” definition: competence
is meeting fit τ , and resource use is contrivance cost. The budget B should be understood as an
abstract proxy for the system’s available representational and computational resources, mirroring
the genenergy budgeting earlier in the section (Hyperseed-Concept ??).
    In particular, B can be interpreted as fixing a “feasible complexity band” of hypotheses: if the
system’s architecture or training regime can only realize hypotheses up to contrivance B, then any
task whose best achievable contrivance exceeds B is effectively out of reach, even if it is learnable
with unbounded resources.
Remark 830. A concrete reading is: if B is small, only very weak (highly general, low-description-
length) explanations are permitted. If the task requires a very contrived explanation, then it is
not solvable at that budget even if solvable in principle. This provides a clean interface between
architectural synergy and “effective intelligence” under scarcity [9].
    This criterion also makes the “capabilities under scaling” story explicit: increasing B expands
the solvable set monotonically, but architectural synergy can shift the required budget for a given
task downward by reducing Con∗ . In that sense, synergy acts like an efficiency gain in how the
system allocates limited representational capacity to meet the same fit level.
Proposition 26 (Synergy expands the solvable set relative to non-synergistic partitions). Let
T1 , T2 be disjoint knowledge sets and suppose Σ(T1 , T2 ; τ ) > 0 for a given task/dataset b. Define the
“partition-limited” contrivance level
                           Conpart (T1 , T2 ; τ ) := Con∗ (T1 ; τ ) + Con∗ (T2 ; τ ),
which corresponds to architectures in which the two knowledge sets may each build an explanation,
but only in a separable (non-emergent) way. Then there exists a budget B such that b is solvable by
T1 ∪ T2 at budget B, but is not solvable by any separable partition-limited architecture at budget B.
    The disjointness assumption is meant to rule out double-counting the same representational
resources: if T1 and T2 overlapped heavily, then the sum Con∗ (T1 ; τ ) + Con∗ (T2 ; τ ) could overstate
the true cost of a separable design by charging twice for shared structure. Under disjointness, the
comparison to a strictly synergistic joint solution is cleanly attributable to cross-type interaction
rather than to bookkeeping artifacts.

                                                     326
Remark 831. The statement translates synergy into an operational advantage: there is a range of
budgets for which the synergistic architecture succeeds while any architecture forced to keep the two
knowledge sets separable must fail. This is exactly the kind of “capability gap” one expects when
intermediate results can be exchanged across representational types rather than only combined at
the end.
    Concretely, a separable architecture must “pay” separately for whatever structure is required
to reach fit τ from within each knowledge set, whereas a synergistic one may express a single
joint hypothesis whose parts co-adapt and share explanatory burden. The proposition isolates this
advantage as a strict separation in feasible budgets, not merely as a mild reduction in cost at high
budgets.
Remark 832. The result connects back to the earlier subadditivity propositions: if synergy is strict,
then the joint contrivance frontier lies below the separable one. The proposition simply chooses a
budget in the strict gap. This is a small but principled instance of a more general tradeoff theme in
the Hyperseed line of work: architectural constraints translate into provable capability limits under
budgets [9].
    One can also read the result as a robustness statement about evaluation under resource limits:
if a benchmark is run at a fixed budget B lying in the gap, then observed success/failure becomes
diagnostic of whether the system is exploiting cross-type coupling, rather than merely having a larger
raw budget.
Proof. Let C12 := Con∗ (T1 ∪ T2 ; τ ) and Cpart := Conpart (T1 , T2 ; τ ). Positive synergy means C12 <
Cpart . Choose any budget B satisfying C12 ≤ B < Cpart . Then b is solvable by T1 ∪ T2 at budget
B by definition. On the other hand, any architecture restricted to separable explanations built
independently from T1 and T2 requires contrivance at least Cpart , hence cannot meet the same fit
threshold within budget B.
    Existence of such a B follows immediately from strict inequality: there is at least one real value
between C12 and Cpart (for example, B = 21 (C12 + Cpart ) when both quantities are finite). If Con∗
is defined via an infimum rather than a minimum, the use of “≤ B” in the solvability criterion is
important: even if the optimal contrivance is not attained, any B above the infimum still permits
arbitrarily close feasible solutions, while the strict lower bound B < Cpart continues to exclude all
separable architectures at that budget.

Remark 833. The proof is essentially interval arithmetic: strict inequality C12 < Cpart implies
there exists a nonempty open interval of budgets between them. Picking any B in that interval
creates a regime where joint explanations are affordable but separable ones are not.
    This also clarifies why the result is framed as an existence statement: it does not claim that
every budget benefits from synergy, only that whenever there is a strict cost gap, one can select a
budget that lands inside that gap and thereby forces an observable difference in solvability.
Proof sketch. Let the synergistic optimum cost be C12 and the best separable cost be Cpart . Since
C12 < Cpart , choose B between them. Then the synergistic system meets the budget while every
separable system exceeds it.
    In the language of decision thresholds, B is chosen so that it accepts the joint model class but
rejects the separable model class, turning a quantitative synergy gain into a qualitative difference
in whether the task can be solved under the imposed resource constraint.                          
Remark 834. Geometrically, one can picture two thresholds on the number line: synergy moves
the required budget leftward. One threshold corresponds to the minimum budget at which the task
becomes solvable when types are allowed to interact emergently, while the other corresponds to the

                                                 327
minimum budget when the types are forced to contribute in isolation. In this picture, “leftward”
does not mean that the task becomes easier in an absolute sense; it means the architecture makes
better use of the same scarce computational currency by enabling multi-type regularities to be cap-
tured earlier. The “intelligence increase” is then not mystical; it is the existence of tasks that cross
from impossible to possible when the architecture permits cross-type emergent compression patterns
(Hyperseed-Concept ?? provides a related intuition about gains from moving between representa-
tional levels). In particular, the shift can be interpreted as a reduction in contrivance: fewer ad hoc
special cases are required because structure discovered in one type can constrain search or learning
in another.

Remark 835. Proposition 26 isolates a simple operational implication: synergy can make a task
solvable under a budget that would be insufficient for any architecture that forces the two knowledge
sets to contribute only in a separable (non-emergent) way. This is one clean sense in which synergy
can increase effective intelligence. Equivalently, if one thinks of a system designer choosing an
architecture under a fixed resource envelope, synergy expands the set of tasks that can be completed
without increasing the envelope. The “separable” constraint is important here: it rules out the
possibility that partial results in one type reshape the hypothesis space, loss landscape, or action
space explored by the other type, and thus rules out precisely the kind of cross-type compression that
yields strict subadditivity.

15.6    Attention as the gating mechanism for synergy
Cognitive synergy requires frequent exchange of intermediate results. In bounded systems, such
exchange competes for attention. Thus attention is the architectural “gate” that decides whether
potential synergy is realized. One can read this as an opportunity-cost claim: every unit of attention
devoted to translation and cross-type integration is a unit not devoted to within-type refinement,
and so the system must continuously trade off short-horizon progress against longer-horizon integra-
tive gains. Conversely, if attention never “pays” for communication, then even a richly multimodal
or multi-algorithmic architecture behaves like a set of loosely coupled modules with minimal mutual
constraint.

Definition 212 (Inter-type communication graph). Let T be a set of knowledge types. Define a
directed graph Γ on T where an edge T → T 0 indicates that items in KT can be transformed into
inputs for Alg(T 0 ). Assign each edge a time-dependent bandwidth allocation bt (T → T 0 ) ≥ 0 with
                  0
P
   T,T 0 bt (T → T ) ≤ Bt . We interpret bt as the fraction of the attention budget devoted to cross-type
communication. In general bt may be sparse (concentrated on a few edges) or diffuse (spread over
many edges), and its temporal variation encodes when the system chooses to integrate versus when
it chooses to specialize. If desired, one can also interpret Γ as including only genuinely cross-type
edges (within-type processing handled separately), though allowing T = T 0 edges can be convenient
when one wants a uniform accounting of all attentional expenditures in a single graph formalism.

Remark 836. The graph Γ is a wiring diagram for cognitive synergy: it says which translations are
available. The scalar bt (T → T 0 ) then says which translations are being actively     exercised at time
t, under the same budget logic as earlier attention policies. The constraint T,T 0 bt (T → T 0 ) ≤ Bt
                                                                                 P
treats cross-type communication as something that consumes the same scarce currency as within-type
updates. It also makes explicit that “having a translator” is distinct from “running the translator
often enough”: the former is a structural capability (an edge exists), while the latter is an attentional
commitment (a nontrivial bt over time). In particular, a system can possess many potential cross-
type edges but still behave effectively unimodally if the policy allocates negligible bandwidth to them.


                                                  328
Remark 837. A simple example is a pipeline T = sens → T 0 = dec, where sensory embeddings
are converted into declarative propositions, or T = dec → T 0 = proc, where declarative constraints
shape action selection. If the corresponding bt values are near zero, the translations exist only
as dormant possibilities; if they are substantial, the system is actively weaving together types into
joint explanations [19, 7]. In realistic cases, the most synergy-rich subgraphs are often not simple
pipelines but feedback loops, e.g. sens → dec → proc → sens, where actions select new observations,
observations revise beliefs, and revised beliefs reshape policies. The directed nature of Γ matters
here: translation can be easier in one direction than the reverse (for example, procedural skill may
be difficult to verbalize), so high synergy may require asymmetric allocations bt (T → T 0 ) that reflect
these representational asymmetries.

Remark 838. This makes precise the intuitive claim that synergy is not merely a structural prop-
erty of an architecture, but a dynamical property of an architecture under attentional governance.
A system may have the representational machinery for cross-type emergence, yet fail to realize it
because attention is monopolized by short-term demands (Hyperseed-Concept ??). A complemen-
tary failure mode is oscillation without integration: attention repeatedly switches types but allocates
insufficient bandwidth for any translation to become reliable, yielding overhead without commen-
surate cross-type constraint. On the other hand, sustained attention to translation can bootstrap
itself: once intermediate results become easier to exchange (e.g. via learned interfaces, shared latent
variables, or cached abstractions), the effective cost of future communication drops, making synergy
more likely to persist.

Remark 839 (Two limiting regimes). If the cross-type bandwidths are near zero, then even if
synergy is latent (in principle), it will not be expressed. If the bandwidths are substantial, the system
can form and exploit cross-type emergent compression patterns, supporting the strict inequalities
in Section 15.5. Between these extremes lies a practically important intermediate regime: modest
bandwidth can be sufficient if the translated artifacts are high-leverage (e.g. a small number of
declarative constraints that sharply prune procedural search), while in other domains the same
modest bandwidth may be ineffective because useful intermediate products are numerous, noisy,
or require iterative back-and-forth refinement. In this sense, the “gate” metaphor should be read
quantitatively: the question is not only whether the gate is open, but how wide it is and for how
long.

Hyperseed concepts covered
• Attention; attentional focus; genenergy-based attention measure; self-reflective attention (Hyperseed-
  Concept 60; Hyperseed-Concept ??; Hyperseed-Concept ??).

• Varieties of knowledge: declarative, procedural, sensory, attentional, intentional (Hyperseed-
  Concept ??; Hyperseed-Concept 65; Hyperseed-Concept 157).

• Cognitive synergy: usefulness of learning algorithms by knowledge type; synergy as strict sub-
  additivity of contrivance/weakness; attention as the gating mechanism for synergy (Hyperseed-
  Concept 73; Hyperseed-Concept 202; Hyperseed-Concept ??).


16     Self, continuity, development, and mind-world correspondence
This section formalizes a cluster of Hyperseed notions that are often treated informally in cognitive
science and philosophy of mind: self/other boundaries, diachronic self-continuity, development,


                                                  329
and mind–world correspondence (world-model quality). Hyperseed’s distinctive move is to define
these notions in terms of pattern structure and its persistence, rather than in terms of a privileged
substance or an observer-independent identity relation [1, 5]. In the present reconstruction, “self”
is thus not a metaphysical atom but a repeatedly reconstituted cut through a web of relations, and
continuity is not an all-or-nothing identity but a degree of structural persistence. This cluster of
ideas connects directly to the Hyperseed core-concept set: Self vs. Other (Hyperseed-Concept 165),
Self-Continuity (Hyperseed-Concept 166), Development (Hyperseed-Concept 95), and Mind-World
Correspondence (Hyperseed-Concept 112).                                             W
    Throughout, fix an observer/context O and a commutative quantale (V, ≤, ⊗, , 1) as in Sec-
tion 3.

Remark 840 (Notation and conventions used throughout). Here V is the domain of “degrees”
(truth-like, evidence-like, or strength-like values), ≤ is its order (so u ≤ v means “u is no stronger
W v”), ⊗ is the monoidal product (interpretable as conjunction/combination of constraints), and
than
V is the join (supremum; interpretable as “best possible” or “least upper bound”). We will also use
   (the infimum/meet) when defining degrees via “for all” constraints. The element 1 is the unit
for ⊗ and typically plays the role of a maximal (or perfectly adequate) degree. Quantales (and their
“weakness”-flavored interpretations) are discussed more broadly in [3, 2].

    When we want explicit paraconsistency we take V to be the p-bit-valued quantale used in the
toy model (Section 5). Time is treated as an observer-indexed proto-time ordering (Section 7); we
write I, J for time intervals, and we treat a “time slice” as data aggregated over such an interval.
    The key representational objects are pattern webs and pattern-flow networks (Sections 9 and 12).
In this section we focus on morphisms between such networks: maps that preserve pattern-relational
structure up to controlled degradation. This emphasis on morphism and transport is aligned
with Hyperseed’s broader stance that cognition is best modeled by what can be carried along
transformations, rather than by what is statically possessed [7]. Pattern and Pattern Flow Networks
are treated as core notions (Hyperseed-Concepts 130 and 131).
    To situate the above commitments: fixing an observer/context O is not merely a notational
convenience, but a way to make explicit that the relevant pattern decompositions, degrees of fit,
and even the effective “time slices” are all relative to an information-gathering and information-
organizing standpoint. In particular, what counts as the “same” pattern across two intervals I and
J will typically be mediated by representational choices (feature sets, granularity, segmentation)
that are part of O; the formalism does not attempt to erase this dependence, but instead makes it
explicit and therefore comparable across contexts.W
    Likewise, the quantale of degrees (V, ≤, ⊗, , 1) is meant to carry the minimal algebra needed
to talk about approximate preservation and graded failure. In concrete applications one may in-
stantiate V as a unit interval [0, 1] with a t-norm, as a Boolean algebra, or as a more information-
structured object (e.g. the paraconsistent p-bit choice mentioned above). The point is that the
same definitions can be read as (i) graded truth of relational constraints, (ii) graded evidence for
relational constraints, or (iii) graded strength of pattern-couplings, provided that ⊗ plays the role of
“putting constraints together” and that joins/meets provide the appropriate extremal aggregations.
    The phrase “controlled degradation” will be made precise by requiring that morphisms between
pattern-flow networks preserve relations not necessarily exactly but to a specified degree in V.
Informally, such morphisms can be read as transports that (a) identify which parts of a network
correspond, (b) quantify how much relational structure survives the transport, and (c) localize
where structure is lost, distorted, or newly introduced. This is the technical hinge on which the
section turns: self/other boundaries, self-continuity, development, and mind–world correspondence


                                                  330
will each be cast as particular patterns of existence (or non-existence) of such structure-respecting
transports.
    With this in mind, the four headline notions can be previewed as follows (with full definitions
deferred to the subsequent subsections). A self/other boundary will be treated as a context-relative
partitioning of a pattern web into subnetworks whose internal transports are comparatively strong
and whose cross-boundary transports are comparatively weak (all measured in V). Diachronic
self-continuity will then be a degree of transportability from the “self”-designated subnetwork at
interval I to the corresponding subnetwork at interval J, where the degree tracks which relational
constraints remain satisfiable (or approximately so) over time. Development will be expressed not
as mere accumulation of states but as a structured sequence of network morphisms whose typical
effect is to expand or reorganize the space of patterns and flows available to O (for example, by
adding new stable motifs or by reweighting existing habit-like transitions). Finally, mind–world
correspondence will be expressed as the existence and quality of morphisms (or adjoint-like pairs of
morphisms) that align an internal pattern-flow network (the “model”) with an external or action-
embedded pattern-flow network (the “world as encountered”), again with degradation explicitly
represented rather than idealized away.
    The use of paraconsistent degrees (via p-bit) is especially relevant here because both self-models
and world-models are typically inconsistent in the weak sense: they contain partial, conflicting, and
context-shifting constraints that remain practically useful. In such cases, mind–world correspon-
dence is not well represented by a single global consistency requirement, but rather by a pattern of
locally strong correspondences coexisting with tolerated contradictions—a situation the quantale
semantics is designed to encode.

16.1    Self/other boundary as a paraconsistent, observer-relative cut
Hyperseed treats “self” as something constructed by a mind: a self is a distinguished subsystem
(often hierarchical) carved out of a broader coherence field. A crucial point is that the self/other
boundary is not always crisp; it can be fuzzy, context-dependent, and even genuinely inconsistent
(one may simultaneously experience something as “me” and “not-me”). This is the formal face
of Self vs. Other (Hyperseed-Concept 165) and of Non-Duality motifs (Hyperseed-Concept 121)
in an otherwise highly analytic framework; compare the paraconsistent stance motivating such
coexistence of opposites [23, 24]. In particular, “observer-relative” here should be read literally:
different observers (or the same observer under different modeling stances) can induce different
partitions of the same underlying dynamics, because the cut is made in representational space
rather than assumed to be a pre-given ontological seam in the world. The time-interval parameter
I likewise matters: self/other boundaries are treated as temporally situated practices, so that drift,
context-switching, and rapid oscillation can be expressed as changes in σI across I.
    We model this by attaching to each representational item a p-bit degree of self-membership. The
use of a two-component degree is intended to capture not only vagueness (weak evidence in either
direction) but also conflict (strong evidence in both directions), which is precisely the configuration
that classical single-valued membership functions cannot represent without forcing a premature
resolution.

Definition 213 (Self-evidence and self-groupings). Fix a time interval I. Let XI be the set of rep-
resentational tokens (entities, situations, pattern-nodes) used by the observer/model O to describe
the system under study on I. A self-evidence function is a map

                           σI : XI → [0, 1]2 ,    σI (x) = (σI+ (x), σI− (x)),


                                                 331
where σI+ (x) is the degree of evidence that “x is part of the self ” and σI− (x) is the degree of evidence
that “x is not part of the self.” No consistency constraint is imposed. Equivalently, σI may be
read as a graded, paraconsistent labeling of tokens by the observer O: the two coordinates are not
complements, and their joint values are informative precisely when they fail to sum to 1.
    Given thresholds θ+ , θ− ∈ [0, 1], the corresponding crisp self-grouping (induced by σI ) is

                         Self θ (I) := {x ∈ XI : σI+ (x) ≥ θ+ and σI− (x) ≤ θ− },

where θ = (θ+ , θ− ). The complementary crisp other-grouping is Otherθ (I) := XI \ Self θ (I). The
particular choice of θ is best understood as a downstream modeling decision (e.g. needed to define
an agent boundary for credit assignment, control, or responsibility), rather than as an intrinsic
parameter of the phenomenon.

Remark 841 (Threshold monotonicity and decision-sensitivity). For fixed σI , the map θ 7→
Self θ (I) behaves monotonically in the expected directions: increasing θ+ (demanding stronger posi-
tive evidence) can only shrink Self θ (I), while decreasing θ− (demanding weaker negative evidence)
can only shrink Self θ (I). Thus, varying θ interpolates between permissive and conservative self-
ascriptions without altering the underlying evidence profile encoded by σI . This makes explicit a
methodological separation between (i) evidence accumulation about self-relevance and (ii) the prac-
tical need to make a binary cut for a particular analytic task.

Remark 842 (Intuition and examples for self-evidence). Intuitively, σI (x) is not a statement of
fact about an object x but a statement about O’s boundary-making practice on interval I. The
pair (σI+ (x), σI− (x)) records that evidence can point both ways at once: this is the mathematical
counterpart of the phenomenological observation that some contents are experienced as “mine”
and “not mine” in different respects (or even simultaneously). One can also view (σI+ (x), σI− (x))
as distinguishing four qualitative regimes in a graded way: predominantly-self (high +, low −),
predominantly-other (low +, high −), mixed or conflicted (high +, high −), and unassigned/irrelevant
(low +, low −). The last regime is important in practice because many tokens in XI may simply not
participate in the self-model at all, even though they are present in the observer’s overall description
of the situation.
     A simple example is bodily sensation: let x = “pain in the arm.” One may have high σI+ (x)
because the pain is experienced as happening “to me,” while also having nontrivial σI− (x) because the
pain is experienced as an intrusive, alien event. Another example is a tool in skilled use (e.g. a tennis
racket): during fluent action one may assign it substantial positive self-evidence, while still retaining
negative evidence because it is not literally part of the body. The usefulness of this definition is that
it turns boundary vagueness into a manipulable object: thresholds θ yield crisp sets when needed for
downstream constructions, without erasing the underlying ambiguity. A further class of examples
arises in social and extended-cognition settings: a group “we” token, a conversational role, or an
institutional identity can carry high σI+ during coordination (the group-agent is treated as self-like)
while simultaneously carrying high σI− because the same observer recognizes non-identity at the
individual level; the model records this tension rather than forcing an all-or-nothing verdict.

Remark 843 (Boundary and non-duality). The boundary region between self and other is naturally
modeled as
                  ∂Self θ (I) := {x ∈ XI : σI+ (x) ≥ θ+ and σI− (x) ≥ θ− }.
Elements in ∂Self θ (I) carry substantial evidence in both directions. This is a simple formal rep-
resentation of the Hyperseed motif that experienced categories can be simultaneously distinct and


                                                   332
not-distinct. Note that ∂Self θ (I) is not a topological boundary but a decision-relative “zone of con-
flict”: it depends on θ, and it expresses the coexistence of incompatible self-ascriptions at the level
of representation rather than an ambiguity about where matter ends and begins.

Remark 844 (Further intuition: why model a boundary region?). The set ∂Self θ (I) is where
explanatory work tends to be needed: it marks tokens whose role in agency, responsibility, and
prediction is inherently unstable. In Russellian terms, it allows us to speak precisely about cases
where the “class” Self fails to be sharply defined, without thereby abandoning logical discipline. In
Peircean terms, it acknowledges that the sign-process by which the self is constituted may place the
same token under multiple interpretants (Hyperseed-Concepts 190 and 157); and in Whiteheadian
terms it treats the self-boundary as a process-dependent abstraction rather than a substance boundary
[14, 15]. Operationally, boundary-region tokens are also the ones for which small shifts in attention,
affect, or narrative framing can lead to large shifts in downstream attributions (e.g. “I did that”
versus “it happened to me”), which is precisely the kind of sensitivity that motivates keeping σI+
and σI− separate rather than forcing a single net score.

Remark 845 (Multiple selves and hierarchical self-models). In many systems it is natural to con-
sider multiple nested “selves” (e.g. bodily self, actional self, narrative self, social self ). Formally,
                                                      (k)
one may use a family of self-evidence functions σI : XI → [0, 1]2 indexed by a level k (or by a
                                                                                   (k+1),+        (k),+
context label). Nestedness can be encoded either by pointwise inequalities σI              (x) ≤ σI     (x)
                                                                             (k+1)            (k)
(stricter self at higher k) or by explicit inclusion of crisp groupings Self θ     (I) ⊆ Self θ (I). Con-
ceptually, this accommodates the possibility that “what counts as me” is not a single flat set but a
stratified construction: some tokens are self-like only at certain descriptive levels, and conflicts can
occur not only within a level (high + and high −) but also between levels (e.g. bodily self-evidence
positive while narrative self-evidence negative).

Remark 846 (Example: nested selves). As a concrete illustration, let k = 0 denote “bodily self ”
                                                                             (0),+
and k = 1 denote “narrative self.” A heartbeat token may have high σI              (it is bodily-me) but
       (1),+
low σI       (it is not typically part of the narrative-me), while a biographical memory may show
the reverse. The nestedness conditions formalize the idea that higher-level selves are often more
selective: they include fewer tokens, but possibly with greater stability across time. This multi-level
framing is also compatible with phenomenological taxonomies that sort experience into “locations”
or “modes” of selfhood [4, 12]. One can also treat social roles (e.g. “teacher in the classroom”) as
                                                                         (k)
a higher-level self that activates only on certain intervals I, making σI an explicitly context-gated
construction; in such cases, the same underlying token (say, a verbal utterance) may alternate
between being ascribed to the role-self and being experienced as alien or forced, naturally landing in
∂Self θ (I) during periods of role strain.

Where does σI come from? Hyperseed motivates selfhood via persistence of patterns over time
and via coherence (a mind often draws a boundary separating a mutually coherent group from
other entities). In this paper we treat σI as derived data, typically computed from: (i) persistence
statistics across time (Section 16.3); (ii) coherence/interaction weights within the pattern web
(Section 9); and (iii) control/agency signals (Sections 14 and 15). The formal point is that none of
these drivers need be consistent.

Remark 847 (Why self-evidence is placed “upstream” of identity). A tempting move in philos-
ophy is to posit an identity relation and then to explain experience by reference to that identity.
Hyperseed inverts this: boundary-making and persistence are primary, and “identity” is (at best) an


                                                   333