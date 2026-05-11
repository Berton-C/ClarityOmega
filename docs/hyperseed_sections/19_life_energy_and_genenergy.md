# 19 Life, energy, and genenergy

Remark 997. Implicit goals (Hyperseed-Concept ??) live in the dynamics rather than in the dis-
course: the agent behaves as if it were optimizing or constraining something, even if it cannot
articulate it. This matches both everyday psychology (habits, avoidance patterns) and machine
learning practice (policies trained end-to-end without symbolic specification). In Hyperseed terms,
this is also a bridge from the habit dynamics layer to the goal layer.
Remark 998. A simple example is “avoid embarrassment” in a person who never explicitly adopts
that phrase as a goal, yet repeatedly chooses actions that lower predicted social woe. Another
example is a learned controller that repeatedly chooses low-resistance actions even when no explicit
“minimize effort” rule is represented. The usefulness is that it lets the formalism describe goal-
directedness as a spectrum rather than a binary property.
Remark 999 (Hyperseed intent). This matches the everyday distinction: a person may have an
implicit goal of avoiding embarrassment without ever having stated it as a goal. Similarly, many
learned systems optimize a reward function (implicit goal) without explicit symbolic commitments.

18.4.3   Reward as a derived (optional) scalar
Hyperseed often speaks in terms of goals/values rather than rewards. Still, rewards are conve-
nient for algorithms, so we define them as derived. In particular, the intent is that the underlying
evaluative object remains the structured, potentially conflicting evidence (and any associated con-
straints), while the scalar is an interface layer for decision procedures that require a single number.
This also clarifies a methodological point in this section: “reward” is not treated as metaphysically
primitive, but as a deliberately lossy projection that can be turned on or off depending on the
reasoning context.
Definition 257 (Paraconsistent reward from evaluative evidence). Fix weights λd ≥ 0 for d ∈ D
and a resistance weight β ≥ 0. Define a scalar reward proxy:
                                X                              
                   rO (s, a) :=   λd JO (s, a; d) − WO (s, a; d) − β RO (s, a).
                                d∈D

    It is sometimes helpful to read the expression as a sequence of modeling choices: (i) treat each
dimension d as producing two-sided evaluative evidence, (ii) convert that two-sided evidence into
a signed “net” quantity via (J − W ), (iii) trade off dimensions by nonnegative weights, and (iv)
subtract an additional term capturing friction, cost, or internal opposition via RO . Nothing in the
definition requires that the units of (J − W ) match those of RO ; rather, the choice of β (and the
scale of the λd ) is what makes the overall scalar comparable across actions. In applications, λd and
β can be treated as hyperparameters to be elicited, learned, or tuned, with the important caveat
that tuning changes the induced trade-offs and can therefore change which conflicts get “smoothed
over” by the scalarization.
Remark 1000. The intuition is utilitarian in form but not in metaphysics: rO is a computational
convenience, a single number extracted from a richer evaluative structure. The difference (J − W )
is a simple way to turn two-sided evidence into a signed quantity, while βRO penalizes resistance.
This relates to Reward and Reward Maximization (Hyperseed-Concepts 160, 161), while preserving
the prior commitment that the vector structure is primary.
   A further implication of calling rO “derived” is that two agents (or two subsystems) may share
the same underlying (J, W, R) structure yet adopt different scalarizations for different tasks. For
example, a fast planner might use a coarse scalar proxy for search, while a slower reflective process

                                                 387
revisits the same candidate actions using the unsummed vector evidence to surface tensions and
failure modes that scalarization can conceal. This is one way to reconcile the convenience of scalar
interfaces with the broader aim of keeping value conflict legible.
Remark 1001. A simple example: if D = {truth, comfort} with λtruth = λcomfort = 1 and β = 0.5,
then rO (s, a) rewards actions with net positive evidence on each dimension while also preferring
lower-resistance options. The usefulness is that this makes contact with standard planning and
reinforcement learning interfaces (cf. broader AGI algorithmic discussions in [19]), without forcing
the entire theory to be reward-centric.
    In that example, note that the scalar can increase either by raising J (more supporting evidence),
lowering W (less opposing evidence), or lowering R (less resistance). These are not interchangeable
changes in the underlying representation: increasing J is not the same as decreasing W , even
if both increase (J − W ), and the distinction remains available to any procedure that inspects
the full evidence structure rather than only the scalar. This is precisely the sense in which the
scalar is optional: it can be used for action selection while leaving the evidence geometry intact for
explanation, auditing, and conflict management.
Remark 1002 (Reward maximization vs goal seeking). Reward maximization uses the scalar rO .
Goal seeking treats some constraints as hard or lexicographic (e.g. “do not violate compassion below
a threshold”) and uses rO only within the feasible set. Hyperseed’s conceptual preference is typically
the latter: keep conflicts visible, and use scalars carefully.
    A useful way to formalize the remark is to view goal seeking as a two-stage procedure: first
restrict to a feasible region defined by constraints on (some functions of) (J, W, R), and only then
optimize a scalar proxy on that region. This helps separate “non-negotiables” (hard constraints,
thresholds, or lexicographic priorities) from “trade-off” dimensions where scalarization is accept-
able. It also clarifies how resistance can be treated: in some contexts RO is a soft cost (hence the
βRO term), while in other contexts it can itself induce feasibility constraints (e.g. “avoid actions
that trigger extreme internal conflict”), again illustrating that rO is not the sole decision object.
Proposition 27 (Scalarization implies Pareto optimality when used monotonically). Fix a finite
set of actions A at state s and suppose we define a score
                                 X                               
                    Score(a) :=     λd JO (s, a; d) − WO (s, a; d) − β RO (s, a),
                                 d∈D

with λd > 0 for all d and β ≥ 0. If an action a? maximizes Score, then a? is Pareto-undominated
with respect to the componentwise order
                                                    
                          JO (s, a; d), −WO (s, a; d)  and − RO (s, a).
                                                       d∈D

Remark 1003 (Intuition and role in the section). The proposition says: if you insist on collapsing
multiple value dimensions (and resistance) into one scalar by a strictly monotone linear combina-
tion, then any scalar maximizer cannot be obviously worse than another available action across
all dimensions at once. In other words, scalarization cannot accidentally pick an option that is
dominated on every criterion that the scalar score rewards.
Remark 1004. This result matters because Hyperseed repeatedly warns against premature scalar
collapse, yet also acknowledges the practical convenience of scalar rewards. The proposition is a
small sanity bridge between these stances: it shows that a monotone scalar proxy at least respects
the minimal Pareto boundary of the richer evaluative geometry.

                                                 388
    A small but practically relevant nuance is why the proposition assumes a finite action set. With
infinite (or continuous) action spaces, one typically needs additional regularity to guarantee that
a maximizer exists (e.g. compactness of the feasible action set and continuity of Score, or else
replacing “maximizes” with “is optimal” in the sense of a supremum). The Pareto-undominance
conclusion is fundamentally about any maximizer that does exist: once an argmax is well-defined,
the same dominance contradiction goes through. Thus the finiteness assumption is best read as a
convenient sufficient condition for existence rather than a conceptual limitation of the monotonicity
idea.

Proof. Assume for contradiction that a? is dominated by some a such that for every d, JO (s, a; d) ≥
JO (s, a? ; d) and WO (s, a; d) ≤ WO (s, a? ; d), with strict inequality for at least one dimension or
strictly smaller resistance. Then each term λd (J − W ) is at least as large for a as for a? , and strictly
larger for at least one d. Also −βRO (s, a) is at least as large as −βRO (s, a? ) (and strictly larger if
resistance strictly decreases and β > 0). Hence Score(a) > Score(a? ), contradicting maximality of
a? .

Proof sketch. The proof is a direct monotonicity argument. Dominance means every coordinate
that contributes positively to Score is at least as favorable for a as for a? , and at least one is strictly
more favorable. Because the weights λd are strictly positive (and β ≥ 0), the strict improvement
survives summation, contradicting the assumption that a? maximizes the scalar score.                      

Remark 1005. The key step is that dominance is expressed in the same direction as the scalar
score: increasing J and decreasing W weakly increases each weighted term, and decreasing resistance
weakly increases the −βR term. This is why strict positivity of λd is important: it prevents an
improved dimension from being “invisible” to the scalar. Geometrically, the argument says that a
linear functional with positive coefficients cannot be maximized in the interior of a region that is
strictly dominated in every outward direction.

    One can also read the strict positivity requirement as a warning about “dropping” dimensions
during scalarization. If some λd = 0, then improvements in that dimension do not affect the
scalar score at all, and the scalar maximizer can be dominated with respect to the full vector order
that includes that dimension. In that sense, λd > 0 encodes a minimal respect condition: every
dimension declared relevant to the Pareto comparison must have at least some influence on the
scalar proxy. Similarly, if β = 0, then resistance is ignored by the scalar; the proposition still
holds for the reduced vector order that omits −RO , but it no longer guarantees undominance once
resistance is added back as an additional coordinate.

Remark 1006. The proposition does not claim scalar rewards are sufficient; it only states a sanity
property: if you do collapse to a scalar in a strictly monotone way, you do not accidentally pick a
dominated option. The paraconsistent structure still matters because the (J, W ) values can encode
conflict and incomplete evidence.

    A further limitation is that Pareto-undominance is only a minimal rationality property. Many
Pareto-undominated actions can still be mutually incomparable, and the scalarization picks one
according to a particular trade-off surface determined by (λ, β). Hyperseed’s emphasis on keep-
ing conflicts visible is partly a reminder that, when the underlying evidence is paraconsistent or
incomplete, the set of Pareto-undominated actions can be large, and the choice among them may
require additional deliberative structure (e.g. constraints, lexicographic rules, or context-sensitive
priorities) rather than a single fixed scalar.



                                                    389
18.5    Resonance as coordination signal for value conflict
A core Hyperseed motivation is that action can be “coherent” even when values conflict. We
formalize coherence using the resonance mapping from Section 3.9. In this subsection, “coherent”
is meant in the dynamical/behavioral sense: the agent can stably select and execute a policy whose
internal motivational components are sufficiently aligned to sustain follow-through, even if the agent
cannot produce a single propositional description that renders all value-claims jointly satisfiable.

Remark 1007. The philosophical point is subtle: coherence is not the same as consistency. An
agent may coherently act under conflict by aligning many partial tendencies into a single trajec-
tory, even if those tendencies cannot be made mutually noncontradictory at the representational
level. Resonance (Hyperseed-Concept 159) is a formal proxy for this kind of alignment; dissonance
(Hyperseed-Concept 97) is a proxy for cancellation and internal struggle.

    One practical reason to separate coherence from consistency is that real agents often face in-
commensurable desiderata (e.g., loyalty vs. fairness, exploration vs. safety, short-term relief vs.
long-term health). In such settings, insisting on representational consistency can force an artifi-
cial collapse of plural values into a single scalar, whereas the resonance framing aims to preserve
plurality while still yielding actionable structure.

Definition 258 (Complex value signal for a dimension). For each dimension d and option (s, a),
define the complex signal                                  
                            zO (s, a; d) := σC EO (s, a; d) ∈ C,
where σC is the logic-to-complex map introduced in the core.

Remark 1008. Here σC is the previously defined embedding of p-bit evidence into the complex
plane, used to make “interference” and “phase alignment” algebraically explicit (Section 3.9). The
intuition is that each value dimension contributes a complex phasor, and the overall alignment of
these phasors measures how coordinated the value system is under the contemplated option.

    It is helpful to keep two roles of zO (s, a; d) conceptually distinct: its magnitude corresponds
to the strength or confidence of the dimension-specific evaluation under (s, a), while its argument
(phase) corresponds to the “direction” of the evaluation (broadly, pro vs. con, or endorsement vs.
veto, depending on how σC was set up). This separation is exactly what makes it possible for
strong but opposing evaluations to cancel, rather than being forced into an arbitrary compromise.

Remark 1009. A toy example: if two dimensions yield complex signals of similar argument
(phase), their sum has larger magnitude; if they yield signals with opposite phase, they partially
cancel. This gives a clean mathematical image of “my values pull in the same direction” versus
“my values fight each other.”

   Note that cancellation can occur even when each individual dimension is “certain” (large magni-
tude): high-confidence opposition yields large destructive interference. Conversely, weak or ambigu-
ous evaluations (small magnitude phasors) contribute little to either alignment or conflict, which
matches the intuition that faint preferences should not dominate the global coordination signal.

Definition 259 (Weighted resonance magnitude). Fix weights wd ≥ 0 and define the total complex
signal                                      X
                               ZO (s, a) :=   wd zO (s, a; d).
                                                d∈D



                                                 390
Define the resonance magnitude
                                          κO (s, a) := |ZO (s, a)|.
Optionally define an interference term (as in Section 3.9) by
                                                        X
                            IO (s, a) := |ZO (s, a)|2 −   |wd zO (s, a; d)|2 .
                                                             d∈D

    The nonnegativity constraint wd ≥ 0 ensures that weights encode relative salience or priority
without inverting a dimension’s meaning; sign flips are instead represented through the phase of
zO . In applications, wd can be used to encode long-run commitments (stable importance weights)
while allowing the evidence-to-phase map σC to reflect context-sensitive endorsement or rejection.

Remark 1010. The magnitude κO (s, a) is a scalar summary of alignment; it is large when many
weighted dimensions agree in “direction” (as encoded by the complex phases induced by σC ). The
interference term IO (s, a) measures whether the whole is more or less than the sum of squared parts;
negative values correspond to destructive interference, a particularly crisp signature of internal
conflict.

    Because IO is defined using squared magnitudes, it admits a familiar geometric reading: expand-
ing |ZO |2 yields cross-terms that are proportional to pairwise phase agreement between dimensions.
Thus IO can be interpreted as aggregating pairwise “coordination” contributions, making it useful
when one wants to diagnose which sets of dimensions are jointly supportive versus mutually can-
celling (though such diagnosis requires looking beyond the scalar and into the underlying phasors).

Remark 1011 (Interpretation). • Large κO indicates that the dimension-signals line up in phase
 (coherent “yes” or coherent “no” structure).

• Negative interference IO < 0 corresponds to cancellation between dimensions: this is one clean
  formal proxy for internal value conflict.
   This gives a mathematically explicit handle on Hyperseed’s qualitative talk of resonance/dissonance.

    Importantly, κO alone does not claim that the option is “good” in a single-dimensional sense;
rather, it measures the degree of coordinated support among the dimensions as encoded. An option
can have high resonance because many dimensions coherently reject it (a coordinated “no”), which
is still useful information for an agent that needs to avoid self-undermining action: coordination
can be coordination toward refusal as well as toward pursuit.

Definition 260 (Resonant feasible choice rule). Let APareto (s) ⊆ A be the Pareto-undominated set
at s (under pref across D). Define a resonant choice as any maximizer of
                                                                    
                           a? ∈ arg max        κO (s, a) − βRO (s, a) ,
                                       a∈APareto (s)

with β ≥ 0.

    The Pareto filter plays a normative role: it prevents resonance from favoring an option that is
strictly worse on all dimensions (which could otherwise happen if the mapping σC induces phases
that accidentally align even for uniformly dominated actions). In this sense, resonance is used as a
coordination tie-breaker among options that are already defensible from a pluralistic standpoint.




                                                       391
Remark 1012. The rule has a clear two-stage meaning. First, eliminate actions that are un-
ambiguously worse in the Pareto sense. Second, among the survivors, prefer options whose value
dimensions mutually reinforce (high resonance) and do not demand excessive resistance. The use-
fulness is that it preserves pluralism of values while still producing a practical decision rule. It
also mirrors a theme that recurs in Hyperseed: do not resolve conflict by denial; resolve it by
coordination.

    The parameter β controls the tradeoff between “internal alignment” and “effortfulness” (as
measured by RO ). At β = 0, the rule reduces to selecting the most internally coordinated option
among the Pareto-undominated set; as β increases, the agent increasingly favors options that are
easier to execute or that require less overcoming of aversion, fatigue, or constraint. This makes
the rule suitable both for idealized deliberation (small β) and for bounded, resource-aware choice
(larger β).
    This rule is intentionally conservative: it does not erase value conflicts; it selects among already-
undominated options using coherence and effort. In particular, it treats conflict as a first-class
signal: destructive interference lowers κO (and can render IO negative), thereby disfavoring options
that would likely produce vacillation, paralysis, or regret due to internal cancellation, even when
no single dimension can decisively veto the action.

18.6    Individuation, self-transcendence, and open-ended intelligence
Hyperseed treats individuation and self-transcendence as key drivers of open-ended growth. Here
we formalize them as meta-values: dimensions in D that regulate how the value system itself evolves.
Concretely, calling these dimensions “meta-values” means that they do not merely score external
world-states, but also score candidate updates to the agent’s self-model and evaluative vocabulary:
a change to D, to its internal organization, or to the policies that consult it can itself be treated as
an object of evaluation in EO,t .

Definition 261 (Individuation and self-transcendence as meta-values). Assume individuation, self transcendence ∈
D.

• High evaluation on individuation favors options that preserve coherence and continuity of the
  self-model (Section ??) and reduce destructive self-fragmentation.

• High evaluation on self transcendence favors options that expand the representational and moti-
  vational space, including revising or enlarging D itself.

Remark 1013. A useful operational reading is that individuation implicitly penalizes updates that
increase internal inconsistency, unresolvable goal-conflict, or identity discontinuities across proto-
time, while self transcendence implicitly rewards updates that increase model class capacity, perspective-
taking, and the ability to represent previously inexpressible goals. In this sense, these two dimensions
can be understood as providing a principled “regularizer” and “expander” for value learning: one
controls brittleness and fragmentation, the other controls stagnation and premature closure.

Remark 1014. These two dimensions capture a constructive tension. Individuation (Hyperseed-
Concept ??) protects the integrity of the self as a temporally extended pattern (Hyperseed-Concept
166); self-transcendence (Hyperseed-Concept 167) prevents that integrity from ossifying into a closed
world. In Russellian terms, individuation provides logical discipline, while self-transcendence sup-
plies the imaginative expansion that keeps the logical system from mistaking its axioms for the
cosmos.


                                                  392
Remark 1015. One way to see the tension is to treat the self-model as a hypothesis that must
remain predictive enough to coordinate action over time, while also remaining revisable enough
to accommodate new evidence and new possibilities. Overemphasizing individuation risks “iden-
tity lock-in” (a self-model that refuses to update even when it systematically mispredicts), whereas
overemphasizing self-transcendence risks “identity diffusion” (a self-model that updates so freely
that long-horizon commitments and responsibility become unstable). The intended regime is nei-
ther rigidity nor dissolution but a dynamic equilibrium in which continuity is maintained through
intelligible, narratively compressible change.

Remark 1016. A simple example: in creative work, individuation may favor maintaining a co-
herent long-term project identity, while self-transcendence may favor learning a radically new tool
or exploring a new domain that reshapes the project. The usefulness of making these explicit di-
mensions is that “growth” can be formalized as a controlled revision of the value basis rather than
as an unstructured drift.

Remark 1017. The same structure applies outside creative work. In moral development, individ-
uation can favor keeping faith with prior commitments and relationships (so that change does not
become betrayal-by-forgetting), while self-transcendence can favor encountering unfamiliar perspec-
tives that force a refinement of what those commitments mean. In epistemic terms, individuation
supports calibration and internal consistency; self-transcendence supports the discovery of new la-
tent variables, new abstractions, and new ethical patient-classes that were previously absent from
D.

Definition 262 (Open-ended intelligence as stable-yet-revisable value dynamics). Let Dt be the set
of active value dimensions at proto-time t and EO,t the corresponding evaluative field. An observer
exhibits open-ended intelligence on an interval if:

1. ( stability) there exist nontrivial dimensions in Dt that remain stable for substantial sub-intervals
   (values do not dissolve into noise);

2. ( revisability) there exist times t < t0 such that Dt0 6= Dt (the value vocabulary can grow or
   reorganize);

3. ( coherence under revision) revisions do not make action selection trivial; i.e. the agent retains
   a non-degenerate Pareto set and nontrivial resonance structure.

Remark 1018. Condition (1) can be read as requiring that some evaluative commitments persist
long enough to support planning, learning, and accountability, while condition (2) requires that the
system can escape local optima in value space rather than merely optimizing within a fixed objective.
Condition (3) then rules out a degenerate “anything goes” regime: if revisions create a situation
where almost all options are mutually incomparable (or all options become equally optimal), then
the value system no longer provides actionable guidance. The non-degenerate Pareto requirement
is thus not an aesthetic preference but a functional criterion ensuring that evaluation continues to
constrain behavior in informative ways.

Remark 1019. It is also helpful to distinguish revisability at three granularities: (i) parame-
ter revision (reweighting dimensions or changing trade-off curves), (ii) structural revision (split-
ting/merging dimensions, introducing new latent factors, changing the geometry of D), and (iii)
semantic revision (changing what a dimension tracks via new world-model concepts). The definition
above permits all three, provided that stability and non-degeneracy are maintained somewhere in
the system so that the agent remains a coherent decision-maker throughout the revision process.

                                                  393
Definition 263 (Value-basis revision operator (one formalization)). Let Rev be a (possibly stochas-
tic) operator such that
                           (Dt+1 , EO,t+1 ) = Rev(Dt , EO,t , Mt , Ht ),
where Mt denotes the agent’s current world/self-model state and Ht denotes relevant history (expe-
rience, reflection, social input). We say Rev is individuation-respecting if it places high weight on
preserving identity-continuity constraints (e.g. bounded discontinuity of self-representations across
steps), and self-transcendence-capable if it assigns nonzero probability (or admissibility) to expan-
sions and reorganizations of Dt when such changes improve expressive adequacy or reduce systematic
blind spots.
Remark 1020. This operator view makes explicit that “meta-values” can be implemented as pref-
erences over updates rather than only over outcomes. For example, individuation-respecting revi-
sion can be modeled by continuity penalties (e.g. bounding divergences between successive self-model
encodings), while self-transcendence-capable revision can be modeled by allowing hypothesis-class
expansion steps (e.g. adding a new dimension when prediction error or moral uncertainty remains
persistently high). Importantly, these are not merely engineering conveniences: they correspond to
the normative intuition that growth should be both intelligible (continuous enough to remain “me”)
and exploratory (open enough to become more than prior limitations).
Remark 1021. This definition makes “open-ended intelligence” (Hyperseed-Concept 127) a prop-
erty of value dynamics, not only of problem-solving performance. The agent must be stable enough
to be itself, yet plastic enough to become otherwise; and the plasticity must not collapse decision-
making into incoherence. This connects to the broader AGI view that intelligence is partly the
ability to manage changing task and value regimes without losing functional unity [19].
Remark 1022. The “stable-yet-revisable” requirement is closely related to the exploration–exploitation
balance, but lifted to the level of normative representation. Exploitation corresponds to acting co-
herently under a relatively stable Dt ; exploration corresponds not only to trying new actions but
to considering new criteria for action. On this reading, self-transcendence is a driver of norma-
tive exploration (search over value bases), while individuation is a driver of normative exploitation
(consolidation and integration so that the expanded basis yields a unified self ).
Remark 1023. A simple example is an agent that begins with Dt = {safety, comfort}, later adds
truth, and later refines belonging into separate dimensions for “local community” and “global com-
mons.” Revisability is not mere addition: it can involve splitting, merging, or reweighting dimen-
sions. The usefulness of the non-degeneracy condition is that it blocks a pathological case where
everything becomes incomparable and the Pareto set becomes uninformative.
Remark 1024. A complementary pathological case is the opposite extreme: revisions that collapse
the evaluative field so that almost everything becomes tied (e.g. by flattening all distinctions or by
introducing an overriding dimension that trivializes the rest). Both extremes destroy guidance: per-
vasive incomparability yields paralysis, while pervasive ties yield arbitrariness. The point of requiring
a nontrivial resonance structure is to ensure that the system retains patterned sensitivities—some
options systematically “fit” the current integrated value basis better than others, in a way that can
be learned, explained, and used for planning.
Remark 1025 (Open-ended benefit). Open-ended benefit is the same idea applied normatively:
value evolution is not only open-ended, but tends to expand the feasible set of futures in which
multiple agents can realize joy and reduce woe. Formally, this is captured by including compassion
and non-destructive coordination constraints in the revision rule for Dt .

                                                  394
Remark 1026. The phrase “expand the feasible set of futures” can be read in a multi-objective
sense: revisions should (in expectation and subject to uncertainty) increase the set of attainable
trajectories that score well across a plurality of agents’ evaluative fields, while avoiding expansions
that are achieved by exploitation, coercion, or irreversible harm. This is stronger than simple
“innovation” or “growth” because it adds constraints on the means of expansion (non-destructive
coordination) and on the distribution of its benefits (compassion).

Remark 1027. Open-ended benefit (Hyperseed-Concept 126) adds a social and ethical tilt: it asks
that the expansion of possibilities not be purchased by narrowing others’ possibilities. In multi-agent
settings, this is naturally connected to compassion and to collective coordination effects, echoing
broader Hyperseed arguments about prosocial efficiency [6].

Remark 1028. In practice, “compassion and non-destructive coordination constraints” can be in-
terpreted as admissibility conditions on Rev: certain updates to Dt (or to the weights and semantics
of its dimensions) are disallowed if they systematically increase incentives for domination, decep-
tion, or zero-sum lock-in. This makes open-ended benefit a criterion not only on chosen actions
but on the long-run shape of the evolving value system: it favors meta-stable attractors in which
agents remain mutually legible and able to negotiate, rather than drifting toward value regimes that
externalize costs onto others or render cooperation impossible.

18.7    Rationality: coherence between belief, value, and action under constraints
Hyperseed uses “rationality” broadly: not merely logical consistency, but action selection that
respects evidence, values, and resource limits. In particular, the term is intended to cover both
(i) epistemic discipline (how strongly different outcomes are supported by the belief model) and
(ii) practical discipline (how choices are filtered and ranked when multiple value-criteria and costs
compete). This usage intentionally departs from the common identification of rationality with either
deductive closure or with unconstrained expected-utility maximization, since the present framework
makes room for conflict, incompleteness, and bounded computation as first-class structural features.

Remark 1029. In this setting, rationality (Hyperseed-Concept 148) is not the classical ideal of a
perfectly consistent belief set with a total utility function. It is instead a form of coherence under
limitation: coherence across paraconsistent belief evidence, paraconsistent value evidence, and the
resistances imposed by finite resources. This is consonant with the general Hyperseed ethos that
weakness is fundamental rather than accidental [3, 2]. A useful way to read “coherence” here is
as a family resemblance between internal components: beliefs constrain which futures are treated as
live, values constrain which futures are treated as desirable, and resistances constrain which futures
are treated as reachable without collapse. The relevant notion of “consistency” is therefore not
global consistency of all attitudes at once, but local compatibility sufficient to support stable action
selection.

Definition 264 (Rational decision criterion (minimal version)). Fix state s. A choice rule πO (· | s)
is (Hyperseed-minimally) rational if it satisfies:

1. Non-explosion under value conflict: if two actions have incomparable value-vectors (due to
   paraconsistency), the rule still returns a nonempty admissible set (or distribution) rather than
   degenerating into arbitrary choice over all actions.

2. Dominance respect: if a Pareto-dominates a0 (under pref across all d and has no greater
   resistance), then πO does not prefer a0 over a.


                                                  395
3. Resource sensitivity: ceteris paribus, if two actions have equal value evidence, the rule prefers
   smaller resistance RO (s, ·).
4. Belief/value/action coherence: if the observer’s belief model assigns negligible plausibility
   to an outcome, the value attached to that outcome does not dominate action selection unless
   explicitly designated as a faith-commitment (Section 20).
    The four clauses are intentionally framed as failure-avoidance constraints: they do not dic-
tate a unique optimizer, but they rule out characteristic ways a decision procedure can become
pathological when paraconsistency and bounded resources are treated as normal. They can also be
read as “guardrails” for many different concrete implementations (e.g., rule-based filters, scalariza-
tions, satisficing schemes, or distributions over an admissible set), provided those implementations
preserve the stated invariants.
Remark 1030. These criteria separate three kinds of failure. The first is explosion (everything
becomes permissible) under conflict—the evaluative analogue of logical explosion. The second is
dominated choice (choosing something plainly worse). The third is resource blindness (preferring
an equally good but harder path). The fourth is wishful incoherence (acting as if an implausible
outcome were assured). Together, they provide a minimal floor, not a full theory of rationality.
It is worth emphasizing that “plainly worse” in the second item is defined relative to the agent’s
own current value-ordering and resistance structure, not relative to any external metric. In this
way, the minimal criterion stays neutral about substantive ethics while still forbidding internal
self-undermining moves such as paying strictly more resistance for strictly less-supported value
outcomes.
Remark 1031. A simple example of criterion (4): an agent may value “winning the lottery,” but
if its belief model makes the probability effectively negligible, then “buy lottery tickets and quit my
job” should not be selected unless the agent elevates that goal to a special status (faith-commitment).
This links the present section to the epistemic layer (Section 20), where belief systems and com-
mitments are treated as structured and resource-sensitive. More generally, this criterion blocks a
common failure mode in multi-criteria settings: a high value attached to a near-impossible out-
come can otherwise swamp moderate values attached to plausible outcomes, producing policies that
are “optimistic” in a purely formal sense but behaviorally brittle. The “faith-commitment” escape
hatch is included to represent deliberate, explicitly endorsed departures from evidential proportion-
ality (e.g., vows, sacred values, or identity-defining goals), rather than allowing such departures to
enter implicitly through numerical instabilities or unchecked aggregation.
Remark 1032. A simple example of criterion (2): suppose a and a0 are two actions and, for every
value-dimension d, the evidence-weighted preference ranks a at least as good as a0 (and strictly
better for at least one d), while also satisfying RO (s, a) ≤ RO (s, a0 ). Then preferring a0 amounts to
accepting strictly less of what one already endorses while paying no less resistance. The minimal
criterion does not require choosing a uniquely (there may be ties or incomparable alternatives), but
it disallows elevating a0 above a when a0 is dominated in this strong sense.
Remark 1033. Criterion (1) can be viewed as the decision-theoretic analogue of paraconsistent
non-triviality: a system that tolerates conflicting value evidence must still avoid the collapse in
which every action becomes equally admissible simply because some values disagree. Practically,
this often amounts to requiring that incomparability yields a frontier (a set of candidates) rather
than a uniform indifference over all actions. In implementations that return a distribution, “non-
explosion” can be operationalized by ensuring the support of the distribution remains within an
admissible subset rather than spreading mass arbitrarily across clearly inferior or irrelevant options.

                                                  396
Remark 1034. Criterion (3) is deliberately stated as ceteris paribus because resistance is not an
overriding value in the framework; it is a constraint-sensitive bias. When value evidence does not
distinguish two actions (or distinguishes them only within a tolerance or uncertainty band), lower
resistance functions as a tie-breaker that preserves operability and avoids gratuitous expenditure of
time, energy, risk, or attention. This also connects to bounded rationality: limited resources are
not merely external constraints but part of the internal structure that makes planning stable over
time.

Theorem 17 (Nonemptiness of resonant feasible choice in the finite case). Assume A is finite.
Then the Pareto-undominated set APareto (s) is nonempty, and the resonant feasible choice rule
admits at least one maximizer.

Remark 1035 (Intuition and connection). The theorem says that once we refuse to collapse ev-
erything into a single scalar, we do not thereby doom ourselves to indecision—at least not in the
finite-action case. There is always at least one undominated option, and once we restrict to the
undominated set, any real-valued selection criterion (here κO − βRO ) attains a maximum. This
provides a minimal existence guarantee for the decision scaffolds introduced above. One can also
read this as a structural robustness statement: pluralism (many dimensions) and paraconsistency
(incomplete or conflicting comparisons) can enlarge the set of admissible actions, but they do not
force the admissible set to be empty. The nonemptiness of APareto (s) ensures that “refusing to
scalarize” is not the same thing as “refusing to decide.”

Remark 1036. This result is not surprising to order theorists, but it is conceptually important in
the present document because it reassures us that paraconsistency and pluralism do not automati-
cally destroy operability. It complements Proposition 27: scalarization respects Pareto boundaries,
and Pareto boundaries exist (in the finite case), so one can move between scalar and vector view-
points without falling into emptiness. In particular, the pairing of (i) an undominated-set filter
and (ii) a subsequent scalar tie-breaker is a common pattern in practice: the first stage protects
against dominated choices and some forms of value-conflict explosion, while the second stage yields
a concrete selection when the frontier contains multiple elements.

Proof. In any finite partially ordered set, there exists at least one minimal element. Apply this to
the strict dominance relation (or equivalently to the complement of being dominated) to obtain
a Pareto-undominated action. Thus APareto (s) 6= ∅. Because APareto (s) is finite, the function
a 7→ κO (s, a) − βRO (s, a) achieves a maximum on it, so a maximizer exists. A slightly more explicit
phrasing of the first step is: if every action were dominated by some other action, one could iterate
the dominance relation indefinitely, constructing an infinite chain in a finite set, which is impossible;
hence at least one action is not dominated.

Proof sketch. The strategy is purely finitary. First, in a finite set you cannot have an infinite
descending chain of “strictly dominated by” relations, so at least one action is not strictly dominated
by any other (Pareto-undominated). Second, any real-valued function on a finite set attains a
maximum, so the resonance-minus-resistance criterion yields at least one maximizer once restricted
to the undominated set. The same schematic argument recurs throughout bounded frameworks:
finiteness (or compactness, in continuous variants) is what turns “there are candidates” into “there
is a best candidate” for a chosen scoring functional.                                                 

Remark 1037. The key step is recognizing Pareto-undominated actions as minimal elements in an
appropriate order (or, dually, as maximal elements under the reverse order). Geometrically, if you
plot all actions as points in a multi-criteria space, the Pareto set is the “frontier” that is not strictly

                                                   397
overshadowed by any other point. Finite sets always have such a frontier. In paraconsistent settings,
the geometry should be interpreted with care: incomparability can arise not only from tradeoffs
between dimensions but also from genuinely unresolved or conflicting evidence about ordering within
a dimension. Nevertheless, the “frontier” metaphor continues to serve as an intuition pump: the
decision procedure first avoids points that are clearly worse by the agent’s own lights, and then
expends additional structure (e.g., κO − βRO ) only within the remaining boundary.
Remark 1038. This theorem is deliberately simple, but it encodes a practical sanity check: once
we refuse to collapse values into a single scalar, we must still guarantee that action selection does
not become undefined. In later sections where action spaces may be large, continuous, or gener-
ated on the fly, this finitary sanity check can be treated as a baseline to be approximated: one
seeks either finite candidate sets (via search and pruning) or conditions such as compactness and
upper-semicontinuity that play the same role as finiteness in ensuring the existence of undominated
elements and maximizers.

18.8     Ethics: categorical imperative, cultural morality, and evil
Hyperseed treats ethics as a real phenomenon (not a mere epiphenomenal story) but also as
observer-relative and socially embedded. We therefore model ethics as constraints and evaluation
dimensions that are (i) representable, (ii) revisable, and (iii) partly shared across agents.
Remark 1039. This subsection treats ethical notions as part of the same formal fabric as predic-
tion, value, and action. The intent is not to settle meta-ethics, but to show that ethical constraints
can be made computationally explicit without pretending that they are infallible. In Hyperseed terms,
ethics is a species of socially stabilized evaluative pattern (Hyperseed-Concepts 197, 170, 91).

18.8.1    Maxims and universalization
Definition 265 (Maxim). A maxim is a rule m mapping a representable context description to an
action choice:
                                      m : CO → A,
where CO is the set of contexts that O can represent (Section 13).
Remark 1040. A maxim is a compact representation of policy, but at the level of reasons rather
than reflex. It says: “in contexts of type c, do action a.” This corresponds to the Hyperseed
emphasis that ethics must be expressible in the same representational medium as other knowledge,
if it is to be debated, taught, revised, or enforced (Hyperseed-Concept 71).
Remark 1041. A simple example is: “When I borrow something, I return it promptly.” Here
CO includes the representable condition “I borrowed item x from person y,” and m selects the
corresponding return action. The usefulness is that maxims can be fed into universalization tests
and compared across agents as explicit social artifacts.
Definition 266 (Universalization operator). Let W denote the modeled world dynamics (as in
Section 14), including other agents. Define Univ(m) as the counterfactual world in which all
relevant agents adopt maxim m whenever m applies. This induces a predicted outcome distribution
over histories, denoted PO (· | Univ(m)).
Remark 1042. Universalization turns a first-person rule into a third-person dynamical hypothesis:
what happens if everyone follows it? Technically, Univ(m) is not a single history but a modified
policy regime inside the world model W, which then induces a distribution PO (· | Univ(m)) over
possible histories (because the world may be stochastic or partially known).

                                                 398
Remark 1043. This is useful because it connects ethical reasoning to the prediction machinery
of the earlier sections. Ethics becomes a kind of counterfactual forecasting problem: evaluate the
world you would get if the maxim were generalized. The paraconsistent machinery allows that
the forecast can contain mixed evidence (e.g. universal lying might increase short-term safety but
destroy long-term trust), rather than forcing a single verdict.

Definition 267 (Categorical imperative test (paraconsistent)). Fix a set Deth ⊆ D of ethical
dimensions (typically including compassion and possibly truth, nonviolence, etc.). Define the uni-
versalized ethical evaluation
                               univ
                                                                        
                              EO    (m; d) := Eω∼PO (·|Univ(m)) EO (ω; d) ,

where EO (ω; d) is the p-bit evidence that the realized history ω promotes/opposes d (obtained by ag-
gregating stepwise evidence across the history using ⊕, ⊗). We say m passes a threshold categorical
imperative if
                      univ                            univ
                                                                
                  J EO     (m; d) ≥ τd and W EO            (m; d) ≤ ηd    ∀d ∈ Deth ,

for fixed thresholds τd , ηd ∈ [0, 1].

Remark 1044. This test is a direct formalization of the Kantian structure: evaluate a maxim by
universalizing it. The novelty here is not the moral slogan but the computational interface: the
output is a paraconsistent p-bit expectation for each ethical dimension, and the pass/fail decision
is thresholded. This aligns with Categorical Imperative (Hyperseed-Concept 71) and also with the
Hyperseed idea that ethical rules are operational constraints in a world-model, not metaphysical
axioms.

Remark 1045. A simple example: suppose m is “lie when it is convenient.” In a sufficiently
realistic model W, Univ(m) may predict that communication reliability collapses, undermining co-
ordination and producing large expected woe on belonging and truth. The usefulness of the formalism
is that such effects can be represented as predicted histories and aggregated evidence, rather than
asserted by fiat.

Remark 1046. This is a formal analogue of “act only on maxims you can will as universal law”:
universalization is explicit, and paraconsistency is allowed (there can be both-for and both-against
evidence). The test does not claim metaphysical finality; it is a computationally meaningful con-
straint an agent can actually evaluate approximately.

18.8.2    Cultural morality
Definition 268 (Cultural morality as shared value field). Let G be a group/community. A cultural
morality for G is a family of value dimension weights and thresholds
                                          (G)   (G)   (G) 
                                         λd , τd , ηd         d∈D

together with shared maxims M(G) such that:

• members of G tend to evaluate actions using these weights/thresholds (perhaps implicitly);

• maxims in M(G) have high social resonance (Section 12 and Section 18.5), meaning they are
  reinforced by communication and imitation.


                                                399
Remark 1047. This definition makes cultural morality (Hyperseed-Concept 92) into a partially
shared parameterization of evaluation: the community supplies default weights and thresholds, plus
a repertoire of endorsed maxims. The emphasis on resonance connects morality to habit formation
and social reinforcement: moral rules are stabilized because they are repeated, communicated, and
                                                                                   (G)
emotionally rewarded, not merely because they are “known.” In particular, the λd encode which
                                                                                                 (G)
dimensions are treated as salient or overriding (“what matters most”), while thresholds such as τd
      (G)
and ηd encode where the community draws lines between acceptable and unacceptable (or between
normal and exceptional) trade-offs within those dimensions.

Remark 1048. One should not read “shared” as “perfectly uniform.” A cultural morality can be
realized as a distribution over individuals clustered around community defaults, with disagreement
arising from variance around (λ, τ, η) as well as from different interpretations of which real-world
                                                                         (G) (G) (G)
situations instantiate a maxim. Formally, this means that even if (λd , τd , ηd ) are treated as
community-level parameters, the modeling stance can still accommodate subgroups, role-based moral
specializations (e.g. professional roles), and context-conditional parameter shifts without abandoning
the notion of a cultural field.

Remark 1049. A simple example is a professional culture (e.g. scientific practice) where truth has
high weight and where maxims like “report negative results” have high resonance. The usefulness
is that one can model moral disagreement as parameter mismatch (different λ, τ, η or different
M(G) ), and one can study cultural evolution as dynamics on these parameters. In such a setting,
changes in institutional incentives or communication channels can be represented as interventions
that alter resonance (which maxims are repeated and rewarded) even when explicit endorsement
remains stable, thereby yielding divergence between “stated morality” and the effective evaluative
field.

Remark 1050. Cultural morality is not assumed to be correct; it is modeled as a socially stabilized
pattern in evaluative fields. This matches Hyperseed’s stance that morality is both real (behaviorally
and experientially) and historically contingent. The point of the definition is therefore descriptive
and explanatory: it provides state variables with which to represent moral learning, acculturation,
conformity pressures, and conflict between communities, rather than presupposing a final criterion
of ethical truth.

18.8.3   Evil
Definition 269 (Evil as a persistent anti-compassion pattern). Fix an observer O modeling a
multi-agent setting. An action policy π is evil relative to (O, Deth ) if, over a substantial interval,
it exhibits:

1. persistent high expected woe imposed on others, i.e. large W in the compassion and related ethical
   dimensions under universalized or repeated application; and

2. a tendency to maintain or increase the resistance/constraint load of others (increasing their R
   in typical contexts), thereby reducing their feasible action sets.

Remark 1051. The definition treats evil (Hyperseed-Concept ??) as neither a single act nor a
metaphysical substance, but as a stable pattern across time: repeated production of others’ woe,
coupled with constriction of others’ agency. The second clause is important because it captures a
structural feature of domination: not only harm, but the engineering of a world in which alternatives
are hard or impossible for the victims. The qualifier “over a substantial interval” is meant to exclude

                                                 400
transient accidents and short-lived coordination failures, and to emphasize that the pattern is robust
under feedback (e.g. the policy persists even after the harms are visible to the agent implementing
π or to the institutions sustaining it).
Remark 1052. The reference to “universalized or repeated application” connects the criterion to
a categorical-imperative-style stress test: if the policy were adopted as a general practice (or is
enacted repeatedly as a standing policy), does it systematically generate woe in compassion-relevant
dimensions? This does not require that O endorse Kantian ethics; rather, it uses universalization as
an operational probe for whether the harm is structurally tied to the policy rather than to an unusual
one-off context. In this sense, the formalism isolates a pattern-level property that is detectable even
when agents rationalize or localize responsibility.
Remark 1053. A simple example is a policy that repeatedly extracts resources from others while
imposing surveillance and dependency so that resistance becomes costly. In the formalism, this
shows up as persistently high woe-evidence in compassion-like dimensions and rising R for others’
typical actions. The usefulness is that it separates “accidental harm” from a self-maintaining harm
pattern, which better matches the ordinary (and political) notion of evil as systemically reproducing
injury. A further diagnostic implication is that even if the immediate W is episodically lowered
(e.g. through superficial welfare concessions), a policy can remain evil if it continues to ratchet
constraints and lock victims into narrowing feasible sets, thereby preserving the long-run capacity
to impose woe.
Remark 1054. This definition intentionally mixes affect (woe), ethics (compassion), and agency
(feasible sets / resistance). This mirrors the Hyperseed intuition: “evil” is not merely violating a
rule; it is creating a stable pattern of harm and constriction. It also clarifies why purely outcome-
based snapshots can be misleading: a momentary reduction in visible harm does not negate the
presence of an agency-constricting mechanism that predictably regenerates harm under ordinary
dynamics of compliance, enforcement, and retaliation.

18.9     Humility, grandiosity, ambition, and “humbition”
Hyperseed highlights a family of self-attitudes that matter for rational agency: humility, grandiosity,
ambition, and the proposed synthesis “humbition” (ambition with humility).
Remark 1055. These notions are included because self-calibration is a hidden hinge between eval-
uation and action. If an agent systematically overestimates its capability, it will select actions with
catastrophic resistance; if it underestimates itself, it will forgo feasible value. Hyperseed treats these
not merely as personality adjectives, but as parameters shaping rational decision under uncertainty
(Hyperseed-Concepts 148, 195).
Remark 1056. In particular, “self-attitude” is meant in a decision-theoretic sense: it determines
how internal self-model evidence is translated into action selection, planning depth, risk appetite,
and information-seeking. Two agents with identical outward goals and identical external observa-
tions can nevertheless diverge sharply in behavior if they map capability evidence to commitment
differently.

18.9.1    Capability p-bits and self-calibration
Definition 270 (Capability evidence). Let cap be a proposition meaning “I (or we) can successfully
execute plan Π in context c.” Represent evidence for/against this proposition by a p-bit
                                          +          −
                                                       (Π, c) ∈ [0, 1]2 .
                                                             
                            CO (Π, c) = CO  (Π, c), CO

                                                   401
Remark 1057. This is the capability analogue of the belief evidence states from Section 17.2: it
stores both pro- and anti-evidence for success. A simple example is Π being “lift a heavy object” and
c encoding fatigue state; one may have positive evidence from past successes and negative evidence
from current weakness signals. The usefulness is that humility/grandiosity can be expressed as how
one aggregates these two channels, rather than as a vague disposition.
                                            +         −
Remark 1058. Nothing here requires CO          and CO   to be complementary or to sum to 1; the rep-
resentation is explicitly compatible with mixed, conflicting, or incomplete evidence. This matters
because many real capability judgments are paraconsistent in practice: e.g. an agent may have
strong reasons to think a plan is doable (training, past performance) while simultaneously having
strong reasons to think it will fail (new constraints, time pressure, degraded resources). The role of
calibration is then not to pretend the conflict is absent, but to decide how conflict is action-relevant.

Remark 1059. The context variable c is intended to include both external situation features (en-
vironmental difficulty, adversarial load) and internal state features (attention, fatigue, coordination
quality). This makes capability evidence a function of state rather than a static trait, which is
important for distinguishing “I can do this in general” from “I can do this now, under these con-
straints.”

Definition 271 (Humility and grandiosity parameters). Fix a calibration parameter h ∈ [0, 1]
(humility). Define a calibrated confidence scalar
                                  +                     +                   −
                                                                                    
                Conf h (Π, c) := CO (Π, c) · (1 − h) + CO (Π, c) · h · 1 − CO (Π, c) .

Interpretation:

• Large h means negative evidence meaningfully suppresses confidence (humility).

• Small h means confidence tracks positive evidence while ignoring negative evidence (grandiosity
  tendency).

Remark 1060. The formula can be read as a convex interpolation between two attitudes toward
                                                          +
negative evidence. When h = 0, confidence is simply CO       : “if I see reasons to think I can, I
                                               +        −
proceed.” When h = 1, confidence becomes CO (1 − CO ): positive evidence is discounted when
substantial negative evidence is present. The usefulness is that the moral-psychological idea of
humility becomes a tunable parameter in a decision pipeline.

Remark 1061. Algebraically, one may note (without changing the intended interpretation) that
                                         +                 −
                                                                   
                        Conf h (Π, c) = CO (Π, c) 1 − h · CO (Π, c) ,

so humility h functions as a multiplicative “penalty sensitivity” to counterevidence. This makes
                                                                                 +              +
several monotonicity properties transparent: for fixed h, Conf h increases with CO ; for fixed CO , it
                  −                                             +   −          −
decreases with CO at a rate proportional to h; and for fixed (CO , CO ) with CO > 0, it decreases as
h increases. In other words, h is precisely the parameter controlling how costly warning signs are
to one’s felt feasibility.

Remark 1062. One motivation for keeping the two-channel form (rather than collapsing to a single
                                                                  +                             −
probability) is that it allows “high confidence under dispute”: CO   can remain high even when CO
is also high, and humility then determines how the dispute is resolved for purposes of commitment.
This provides a simple handle on phenomena like brittle overcommitment (low h despite substantial
  −                                                          +
CO  ) versus cautious non-commitment (high h even when CO      is strong).

                                                  402