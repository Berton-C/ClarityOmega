# 22 Society, culture, and collective mind systems

Remark 1147. In plain terms: if you know how to act in the abstract task T 0 , and you have
an exact interface F telling you how to view T as T 0 , then you can act in T with exactly the
same expected value. This is the formal skeleton of “solving a new problem by translating it into
a known one”. It connects directly to the later breadth and intellectuality definitions: a large part
of what makes an agent appear generally intelligent is not raw skill on each task, but the ability
to locate such interfaces quickly (Hyperseed-Concept 192, ??). In particular, the interface supplies
both an observation coding (what the agent is allowed to treat as the “same situation”) and an
action decoding (how an abstract decision is realized as a concrete intervention). When such a
translation is exact, there is no room for performance loss: the agent is not merely approximating
T by T 0 but inhabiting T 0 as an isomorphic informational perspective on T .

Proof. Define the encoded history map (·)          c : H → H 0 by applying fO to each observation in the
history and leaving action slots as abstract placeholders. More explicitly, if a history in T has the
form h = (o0 , a0 , o1 , a1 , . . . , ot ), then b
                                                 h = (fO (o0 ), 0 , fO (o1 ), 1 , . . . , fO (ot )), where each i
denotes an “action position” to be filled by an abstract action from A0 when π 0 is executed. This
separation emphasizes that π 0 is evaluated only on the information it expects in T 0 , namely its own
past abstract actions and the coded observations. At history h ∈ H with current observation o,
sample a0 ∼ π 0 (b h) and execute a = fA (o, a0 ) in T . This defines a policy π on T by the composite
procedure h 7→ b    h 7→ a0 7→ a; under the usual measurability assumptions on fO , fA , this induced
π is a valid stochastic policy. By construction, the resulting encoded observation process matches
the T 0 dynamics, and the step evaluation matches exactly; therefore the induced trajectory value
distribution matches, hence the expected p-bit value matches. Concretely, one can couple the two
rollouts so that at every time t the coded observation in the T -run equals the observation in the
T 0 -run, and the abstract action sampled by π 0 in T 0 is the same abstract action used (via fA ) to
generate the concrete action in T . The reduction axioms are precisely what make this coupling
consistent across time: the transition law for fO (ot+1 ) given the past agrees with the T 0 transition
law given (b h, a0 ), and the evaluation functional applied to (ot , at , ot+1 ) agrees with the evaluation
in T 0 applied to the corresponding coded transition. Under this coupling, the per-trajectory p-bit
values coincide almost surely, so taking expectations over the common randomness yields equality
of expected p-bit.

Proof sketch. One defines π by “running π 0 on the encoded history” and decoding its chosen abstract
action back into a concrete one. The reduction axioms guarantee that (i) the encoded observation
stream has the same law as in T 0 , and (ii) each step’s evaluation agrees under encoding. Therefore
trajectory values, and hence their expectations, coincide. Equivalently, the map F behaves like a
semantics-preserving compiler from T -interaction traces to T 0 -interaction traces: the agent com-
putes in the T 0 -space while the environment evolves in T , and the axioms ensure these two views
remain synchronized.                                                                              

Remark 1148. The proof works because the reduction conditions are exactly the two places where a
mismatch could enter: in the stochastic evolution of observations or in the evaluation of transitions.
Visually, one can imagine an agent living in T while wearing “glasses” that apply fO to every
observation; the world seen through the glasses behaves like T 0 , and the decoded actions ensure
the world is acted upon in the correct way to maintain the illusion. Said differently, the agent’s
internal state need not represent T directly: it can represent the coded process, plan there, and rely
on the decoder to realize those plans faithfully in T . If either condition failed, transfer could break
in a sharply identifiable way: the agent might see a process that no longer follows the assumed T 0
dynamics (model mismatch), or it might be optimizing the wrong objective because coded transitions
are evaluated differently (reward/value mismatch).

                                                       456
Remark 1149 (Where groupoids enter). If two tasks reduce to each other, they are equivalent
objects in Task; the invertible reductions form a groupoid of task equivalences. In later sections,
more flexible (approximate) morphisms can be handled by V -enrichment and higher-categorical
structure, but the strict case above already captures the core transfer idea. Here “groupoid” means
that every morphism regarded as an equivalence has an inverse and that these equivalences compose:
if T → T 0 and T 0 → T 00 are invertible reductions, then their composite is an invertible reduction
T → T 00 , with identities given by the trivial “do nothing” interface. From the agent’s perspective,
equivalence identifies tasks that differ only by a change of representation: any optimal (or more
generally any) policy can be transported across the equivalence without changing its induced value
distribution. This categorical viewpoint separates questions of capability (what can be solved up to
equivalence) from questions of search (how quickly an agent can find the relevant reduction).

21.4    Competence, intellectuality, and intelligence measures
We now define task competence and several derived quantities that capture Hyperseed’s distinction
between narrow and general intelligence.

Definition 322 (Agent as a policy-producing process). Fix an interface (O, A). An agent Ag is
any procedure that, when coupled to a task T on (O, A), produces a policy πAg,T : H → ∆(A). (We
make the internal state explicit in Section 21.5.)

Remark 1150. This definition intentionally abstracts away implementation details: it treats an
agent as a policy factory whose output depends on the task it is placed in. The point is to allow
many realizations (neural, symbolic, hybrid, social) under a single rubric (Hyperseed-Concept 111,
106, 80). Only later do we constrain the internal structure to express persistent agency.
    As an example, a table-lookup procedure that maps each history to a fixed action is an agent in
this sense (though not an interesting one); a reinforcement learning system that updates its policy
as it interacts is also an agent.

Remark 1151. A few clarifications help avoid category errors later. First, the dependence πAg,T on
T is meant to include whatever coupling information is available when the agent is “placed in” the
task: the task’s observation and action semantics, any provided training corpus or simulator access,
the interaction protocol, and (when relevant) the agent’s own randomization. Second, writing πAg,T :
H → ∆(A) keeps open whether Ag is deterministic or stochastic: a deterministic agent yields point-
mass distributions in ∆(A), whereas an exploratory learner yields non-degenerate distributions.
Finally, the interface (O, A) matters: the same underlying decision-maker may induce very different
policies depending on how information is represented in O or which interventions are available in
A; later comparisons should therefore be understood as being made within a fixed interface unless
explicitly stated otherwise.

Definition 323 (Task competence). Given agent Ag and task T , define the competence
                                                        
                          Comp(Ag; T ) := pl JT (πAg,T ) ∈ [0, 1].

Remark 1152. Competence is the scalarized “how well did it do” number, obtained by first com-
puting the p-bit policy value JT (π) and then projecting to [0, 1] by pl. It is thus a derived quantity,
suitable for aggregation and comparison, not the foundational notion of value itself.
    In the simplest non-paraconsistent case where r always has the form (u, 1−u) for a real u ∈ [0, 1],
the projection pl recovers u (up to an affine reparameterization). But in the general case, competence
is merely a pragmatic summary of conflicted evidence.

                                                  457
Remark 1153. Because competence is defined via a projection pl, it should be read as an ordi-
nally meaningful score unless further structure on pl is imposed: the same underlying p-bit value
can map to different numerical scales depending on how cautious or optimistic pl is about in-
consistency. In particular, if two tasks T and T 0 have very different reward-generating processes
(different noise models, different degrees of inconsistency, or different ranges before scalarization),
then Comp(Ag; T ) and Comp(Ag; T 0 ) are comparable only to the extent that JT and JT 0 have been
normalized in a commensurate way. This is one reason the present section treats competence as a
measurement layer on top of the task semantics rather than as a fundamental axiom of preference.

Definition 324 (Capability profile). For a task set T , the capability profile of Ag is the function

                           κAg : T → [0, 1],     κAg (T ) := Comp(Ag; T ).

Remark 1154. The capability profile κAg is a map from the ecology of tasks to measured perfor-
mance. It is conceptually useful because it reframes intelligence as a landscape rather than a point:
an agent may be strong in one region of T and weak in another, and questions about generalization
become questions about the geometry of this function (Hyperseed-Concept ??, 118).
    For instance, a chess engine may have κ near 1 on tasks involving legal chess positions and near
0 on tasks involving language understanding.

Remark 1155. The capability profile viewpoint also makes explicit what is sometimes implicit
in informal discussions of “intelligence tests”: any scalar score is necessarily an aggregation over
(explicit or latent) sub-tasks. In this paper’s terms, an “intelligence measure” corresponds to (i) a
chosen task set T , (ii) a way of sampling or weighting tasks (often a distribution D), and (iii) a
rule for collapsing the resulting function κAg (or learning curves derived from it) to one or a few
summary numbers. Put differently, κAg is the object that carries the most information; the various
aggregates introduced below intentionally discard information in order to gain interpretability and
comparability.

Definition 325 (Breadth at tolerance ε). Let D be a probability distribution on T . For ε ∈ [0, 1],
define the breadth (at tolerance ε) by
                                                                         
                          Brε (Ag; T , D) := D {T ∈ T : κAg (T ) ≥ 1 − ε} .

Remark 1156. Breadth Brε is the probability (under D) that the agent performs within ε of the top
score 1. Thus, as ε increases, the set inside D(·) expands, and breadth increases. This parameter
lets one tune how strict a notion of “competent” is.
    In the language of Hyperseed concepts, breadth formalizes one axis of General Intelligence
(Hyperseed-Concept ??) by explicitly quantifying how much of a task environment lies within reach
at a given tolerance.

Remark 1157. Note that breadth is not purely a property of the agent: it is a property of the triple
(Ag, T , D). Changing D can change breadth dramatically, even when T is held fixed: a distribution
that concentrates mass on a familiar subdomain can make a narrow specialist appear broad, while
a distribution that emphasizes rare corner cases can make a generally capable system look brittle.
For this reason, D should be interpreted as encoding an intended deployment ecology (what tasks
are likely to matter), not merely as a mathematical convenience. One can also view ε as absorbing
some of the normalization uncertainty of pl: if scalarization is slightly miscalibrated, reporting Brε
across a range of ε can be more robust than selecting a single hard threshold.



                                                 458
Remark 1158 (General vs narrow intelligence). A “general” agent has large breadth over a
large/diverse task environment; a “narrow” agent may have near-perfect competence on a small
region of T but low breadth overall. This makes the general/narrow distinction precise without
committing to a single canonical task set.
Remark 1159. The breadth-based distinction also makes visible an important tradeoff: because
breadth counts the mass of tasks above a competence threshold, it does not reward being superlative
on a narrow slice beyond crossing that threshold. In settings where extreme performance on a small
class of tasks is valuable (e.g. competitive games, highly standardized pipelines), a narrow agent can
be preferable even if it is not “general” by this definition. Conversely, in open-ended environments,
breadth aligns with the intuition that robustness across heterogeneous situations is central. Thus
“general” and “narrow” here are descriptive labels relative to an environment, not moral judgments
about which system is better in all contexts.
Definition 326 (Intellectuality as rapid transfer). To make “intellectuality” capture transfer speed,
assume the agent has a notion of interaction budget n ∈ N and produces a budget-indexed policy
 (n)
πAg,T (e.g. after n episodes, n samples, or n inference steps). Define the learning-curve competence
                                                              (n) 
                                  Comp(n) (Ag; T ) := pl JT (πAg,T ) .

Given a task distribution D, define the intellectuality curve

                           Int(n) (Ag; T , D) := ET ∼D Comp(n) (Ag; T ) .
                                                                      


An agent is “more intellectual” (relative to (T , D)) if it achieves high Int(n) for smaller n.
Remark 1160. This definition aims to isolate something like “grasp” rather than “polish.” Two
agents may eventually reach similar competence given enough interaction, but the more intellectual
one climbs its learning curves quickly across typical tasks in the environment. This is closely aligned
with the transfer-learning emphasis in AGI literature (Hyperseed-Concept ??, 192; cf. [19, 7]).
Remark 1161. Several modeling choices are bundled into the budget parameter n. In an episodic
RL setting, n might count episodes of online interaction; in a supervised or self-supervised setting, it
might count labeled examples or tokens; in a planning setting, it might count forward-model calls or
wall-clock compute devoted to inference. The abstraction is intentional: the core idea is to compare
rates of improvement, but one must take care to compare like with like when interpreting Int(n)
empirically. In particular, if one agent is allowed to amortize learning across tasks (meta-learning)
                                             (n)
while another is reset between tasks, then πAg,T corresponds to different experimental protocols, and
the resulting intellectuality curves answer different questions about transfer. Relatedly, one can treat
Int(n) as a curve-valued statistic (rather than a single number): comparisons such as “dominates
for all n” or “achieves a given competence level with smaller n” often retain more information than
collapsing the curve to, say, its area under the curve, even though such collapses can be useful in
applications.
Remark 1162. A simple example: if T is a family of maze-navigation tasks differing only by a
relabeling of wall textures, then an agent that quickly discovers the invariant structure (geometry of
free space) will have a much higher Int(n) for small n than an agent that relearns each maze from
scratch. In particular, the texture relabeling changes superficial perceptual features while preserving
the transition-relevant latent variables; high small-n performance therefore witnesses an ability to
extract task symmetries and reuse a compact representation across instances rather than amortizing
a separate model per instance.

                                                  459
Remark 1163 (Connection to reductions). Reductions in Section 21.3 provide a concrete mecha-
nism for high intellectuality: if the agent can identify (or learn) a reduction from a new task to an
already-solved one, it can lift an existing policy with little additional data, improving small-n perfor-
mance. Concretely, a reduction specifies how to translate observations, actions, and rewards of the
new task into those of an old task; when such a mapping is available, the agent’s “effective sample
size” needed to achieve competent behavior can drop sharply because the remaining uncertainty is
limited to estimating the reduction rather than learning the entire control problem end-to-end.

21.5    Agents as persistent perception-action loops
We now pin down the core Hyperseed meaning of “agent”: persistent closed-loop control. The key
point is that the formal object called an agent is defined independently of any particular task; tasks
enter only when we couple the agent to a task dynamics, producing an overall stochastic process.
Definition 327 (Agent as a controlled transducer). Fix (O, A). An agent is a tuple
                                           Ag = (S, s0 , U, G),
where S is a (finite or measurable) internal state space, s0 ∈ S is an initial state, U : S × O → S
is an update map, and G : S → ∆(A) is an action map. Here ∆(A) denotes the set of probability
measures over A (or probability mass functions when A is finite), so G allows randomized policies
as a first-class case. Given a history ht = (o0 , a0 , . . . , ot ), the agent state is generated by
                                  st+1 := U (st , ot ),   at ∼ G(st ).
Thus, the dependence of actions on the full history ht is mediated entirely through the sufficient
internal state st , which is why S can be read as the agent’s “memory” or “belief ” variable.
Remark 1164. This is the mathematical core of agency as process rather than as a static mapping.
The internal state S is what allows persistence: the agent at time t is not merely a response to
ot but the continuation of an internal trajectory s0 , s1 , . . .. The update U represents perception
and internal processing; the map G represents action selection (Hyperseed-Concept 87, 140, 151).
In this view, “learning” can be modeled either by enlarging S to include parameters and letting
U update them online, or by treating U and G as already-optimized maps obtained offline; the
definition itself is agnostic to where the maps come from.
    A trivial example is a reactive agent with S = O and U (s, o) = o, so the internal state simply
caches the latest observation. In that case the action distribution at time t is conditionally inde-
pendent of the earlier past given ot , matching the usual notion of a memoryless policy. A more
interesting example is a Bayesian filter in which S is a space of belief states, U is a belief update,
and G selects actions based on expected value or plausibility; this matches the integration of epis-
temic dynamics and control emphasized earlier (Sections 20 and 14). In partially observed settings,
st can be interpreted as an information state that renders optimal control Markovian in st even
when the raw observation process is not Markov.
Remark 1165. Definition 327 is deliberately minimal: it is a controlled Mealy-machine style model.
Belief states (Section 20) and attention policies (Section 15) can be realized by taking S large enough
to include those variables. Likewise, internal randomness (e.g. exploration noise, randomized tie-
breaking, or stochastic computation) is captured by the fact that G(s) is a distribution rather than
a single action, and one may also represent randomized internal computation by adding a private
random seed to S. When G(s) is a Dirac measure for each s, the agent is deterministic at the action-
selection level, and all stochasticity in the closed-loop system comes only from the task kernel P
(and from any stochasticity one later chooses to place into U ).

                                                    460
Definition 328 (Closed-loop coupling to a task). Coupling Ag = (S, s0 , U, G) to a task T =
(O, A, P, r, γ) yields a Markov process on S × O with transition kernel
                                            X
                      P (s, o) → (s0 , o0 ) =  G(s)(a) 1[s0 = U (s, o)] P (o, a)(o0 ).
                                            a∈A

Equivalently, given the current pair (st , ot ), we sample at ∼ G(st ), set st+1 = U (st , ot ), and then
sample ot+1 ∼ P (ot , at ); the displayed kernel is simply the one-step marginal of this generative
description.

Remark 1166. The indicator 1[s0 = U (s, o)] enforces the deterministic state update: among all
s0 ∈ S, only the one equal to U (s, o) is possible. The sum over a ∈ A averages over the randomized
action choice a ∼ G(s). Finally, P (o, a)(o0 ) is the probability that the task emits observation o0 after
seeing (o, a). Because the resulting chain is Markov on S × O, standard tools (occupancy measures,
stationary distributions when they exist, mixing and recurrence conditions, etc.) become available
for analyzing long-run performance and the effect of memory capacity encoded by S.
    This kernel makes concrete the idea that “agent + environment” is a single dynamical system.
It is also the place where one can later insert richer causal or mechanistic structure: e.g. if U is
stochastic, the indicator would be replaced by an internal transition kernel. Similarly, if the task is
written in a more latent-state form (e.g. an MDP on hidden states with an observation channel), the
above coupling remains valid after folding the latent state into an augmented observation variable,
or by extending the product space beyond S × O.

Remark 1167 (Agency vs mere dynamics). Any physical system has dynamics, but an “agent” in
Hyperseed is a system for which (i) actions are computationally selected as a function of internal
state, and (ii) internal state is updated as a function of perception, yielding an ongoing feedback
loop. This is the minimal mathematical form of persistent agency. The requirement that action
is selected as a function of internal state is what distinguishes closed-loop control from open-loop
replay of a fixed action sequence; conversely, the requirement that internal state is updated as a
function of perception distinguishes adaptive interaction from a self-contained dynamical system
that never conditionally responds to its input stream.

21.6    Autonomy, intent, and stimulate/inhibit primitives
Hyperseed distinguishes agency from autonomy, and uses “intent” plus the action polarities “stim-
ulate”/“inhibit” as conceptual primitives for action semantics.
    In this framing, agency is primarily about the presence of an action-selection loop (the system
chooses actions as a function of its state and incoming information), while autonomy concerns
where the system’s effective objectives come from and how they change over time. The definitions
below make this separation explicit by introducing intent as an explicit state component, and then
defining autonomy in terms of whether that intent can be endogenously formed and updated rather
than being fully imposed by the task interface.

Definition 329 (Intent variable). Let G be a set of goal-tokens (which may encode explicit goals,
subgoals, or self-generated questions). An intent-augmented agent is an agent Ag whose internal
state factors as S = Se × G and whose action map depends on the current intent:

                                            G(s̃, g) ∈ ∆(A).

We interpret gt ∈ G as the agent’s intent at time t.


                                                   461
Remark 1168. The factorization S = Se × G makes explicit a distinction that is often only implicit
in control models: there is a “how am I doing” state s̃ and a “what am I trying to do” state g.
Here G is intentionally token-level: it may represent explicit symbolic goals, implicit drives, active
questions, or socially supplied objectives (Hyperseed-Concept ??, ??, 144).
    As a toy example, G = {eat, hide} could encode two competing intents, and G(s̃, g) may put high
probability on different actions depending on whether the agent is in “eat” mode or “hide” mode,
even if the observation stream is the same.

Remark 1169. The object G(s̃, g) ∈ ∆(A) can be read as a policy conditioned on an explicit
“goal-token” variable: it returns a distribution over actions rather than a single action so that both
deliberate stochasticity (e.g. exploration) and unresolved internal conflict can be modeled without
adding extra structure. When G is finite and relatively small, this resembles a mixture-of-policies
view; when G is large (e.g. language-like), g functions more like a latent program pointer or a
compact description of the currently active objective.
    Although we call g an “intent,” nothing in the definition requires g to be linguistically reportable
or consciously accessible. The main requirement is functional: g is a state component that mediates
action choice in a way that is not reducible to s̃ alone.

Definition 330 (Autonomous agent (operational)). An intent-augmented agent is autonomous if
it contains an internal goal-formation mechanism: there exists a (possibly stochastic) update rule

                                          Φ : Se × O → ∆(G)

such that the intent is updated by sampling gt+1 ∼ Φ(s̃t , ot ), and such that Φ is not a fixed external
script of the task alone (i.e. it depends nontrivially on the agent’s internal state and value structure;
cf. Section 18).

Remark 1170. Operationally, autonomy is the refusal of the agent’s goal dynamics to be reducible
to the task’s input alone. The update Φ(s̃, o) is permitted to depend on the observation o—autonomy
does not mean blindness to circumstance—but it must also depend on internal organization and
value, so that the agent’s intent trajectory is genuinely self-involving (Hyperseed-Concept 119, 110;
cf. [10] for a related use of fixed-point ideas to analyze self-modifying goal systems).
    A simple non-autonomous case is Φ(s̃, o) = δψ(o) for some externally imposed map ψ, forcing
intent to be a deterministic function of observation. A more autonomous case is when s̃ contains
long-term commitments or identity-like variables, and Φ expresses how those commitments bias goal
selection.

Remark 1171. The clause “not a fixed external script of the task alone” is meant to rule out
trivial relabelings where the environment or supervisor effectively chooses g step-by-step, leaving the
agent to merely execute a conditioned controller. In particular, even if Φ is learned from data, it is
still non-autonomous in this sense if, at run time, its dependence on s̃ is vacuous or inert and all
variation in gt+1 is driven by externally provided signals. Conversely, Φ may be highly reactive to
o and still count as autonomous if that reactivity is mediated by persistent internal structure (e.g.
personal constraints, commitments, or preferences encoded in s̃) rather than by a one-to-one task
script.
     It is often useful to view Φ as a controller over controllers: G maps (s̃, g) to actions, while Φ
maps (s̃, o) to an updated distribution over goal-tokens. This makes room for hierarchical organi-
zation in which g selects a mode, skill, or subpolicy, and Φ implements deliberation, self-querying,
or goal arbitration.


                                                  462
Remark 1172 (Degree of autonomy). Definition 330 is binary, but one can define a degree of
autonomy by measuring how sensitive gt+1 is to internal variables vs external task signals (e.g.
mutual information or causal influence measures). Hyperseed’s “self-determined goal formation”
can thus be treated quantitatively.

Remark 1173. One concrete quantitative proxy is to compare (i) the influence of s̃t on gt+1
holding ot fixed versus (ii) the influence of ot on gt+1 holding s̃t fixed, using either information-
theoretic terms (e.g. I(gt+1 ; s̃t | ot )) or interventionist ones (e.g. average causal effect under do-
interventions on components of s̃t ). Such measures do not replace the conceptual definition, but
they make the intended contrast operational in empirical or simulated settings where one can perturb
internal memory, value parameters, or identity variables and observe resulting changes in the intent
trajectory.

Definition 331 (Action effects and stimulate/inhibit). Fix a claim set L (Section 20) and let β
be the agent’s belief state. Assume that executing an action a in observation context o produces an
effect increment
                                            a,o : L → V,
so that a belief update step has the form β ← β ⊕ a,o (possibly followed by closure). For a claim
ϕ ∈ L:

• a stimulates ϕ at o if +          −
                          a,o (ϕ) > a,o (ϕ);

• a inhibits ϕ at o if −          +
                        a,o (ϕ) > a,o (ϕ);

• a is neutral on ϕ at o if the two are equal.

Remark 1174. Here a,o (ϕ) = (+              −
                                    a,o (ϕ), a,o (ϕ)) is the evidence increment, contributed by doing
a in context o, toward affirming or denying ϕ. The update β ← β ⊕ a,o uses ⊕ as evidence
accumulation, which matches earlier paraconsistent belief dynamics (Section 20).
    The stimulate/inhibit distinction (Hyperseed-Concept 179, ??) should be read as an action se-
mantics primitive: actions are meaningful insofar as they tilt the evidential balance of claims. For
example, if ϕ is “I am safe,” then taking cover may stimulate ϕ (more positive than negative
increment), while stepping into traffic may inhibit it.

Remark 1175. Because a,o is indexed by both a and o, stimulate/inhibit is inherently context-
dependent: the same motor primitive can stimulate ϕ in one situation and inhibit it in another.
This matches ordinary action descriptions (“running” can stimulate “I am safe” when escaping
danger, but inhibit it when running onto a freeway). It also highlights that stimulate and inhibit
are not properties of actions in isolation, but of action-context pairs relative to a claim language L
and an evidence scale V.
    The strict inequalities in Definition 331 encode a simple polarity test. In applications where
V is noisy or coarse, one may also introduce a tolerance (e.g. treat differences below a threshold
as neutral), but the conceptual role remains the same: to classify action effects by which side of a
claim they support.

Remark 1176. This formalizes stimulate/inhibit as primitive polarities of action meaning. The
same definition applies if ϕ is a pattern-claim, a goal-claim, a self-model claim, or a social claim.
In later sections, a,o can be derived from mechanistic models (neural, symbolic, or hybrid) or from
learned causal predictors (Section 14).



                                                  463
Remark 1177. The evidence-increment view also makes room for multi-claim tradeoffs: a single
action a can simultaneously stimulate some claims and inhibit others. For instance, in a social
setting, speaking up might stimulate a claim like “my preference is expressed” while inhibiting “the
group perceives me as agreeable.” In this sense, stimulate/inhibit is not itself a utility theory; it is
a semantics layer that describes how actions push on a structured set of propositions, leaving later
machinery (e.g. value aggregation, intent selection, or constraint handling) to determine which
claims are prioritized under a given g.
    Finally, note that nothing requires a,o to be purely epistemic (“evidence about what is true”)
as opposed to dispositional (“evidence about what will be true”). When ϕ is a future-oriented claim
(e.g. “I will be safe in the next minute”), a,o can be interpreted as action-conditioned predictive
support, which aligns stimulate/inhibit with causal control models while preserving the common
representational interface of claim-level updates.

21.7    Engineered artifacts as externalized agency
Hyperseed uses “engineered” as an ontological category: a pattern (tool, machine, institution,
protocol, etc.) brought into existence by intelligent action. In this sense an engineered artifact can
be read as externalized agency: a stabilized structure in the world that continues to implement
(or make easier to implement) an agent’s goals even when the agent is not actively intervening at
every moment. The point of treating “engineered” as a category is to capture not only material
objects but also non-material but causally efficacious patterns (e.g., conventions, standards, and
procedures) whose existence is reflected in reliable regularities and constraints on future trajectories.

Definition 332 (Engineered pattern / artifact). Let ϕY ∈ L be the claim “artifact/pattern Y
exists (in the relevant sense).” We say Y is engineered by agent Ag over an interval [t0 , t1 ] if:

(a) ( Emergence) βt+0 (ϕY ) is low and βt+1 (ϕY ) is high;

(b) ( Intent alignment) there exists an intent token g active for a nontrivial fraction of times
    in [t0 , t1 ] such that g entails (via the agent’s internal rules) a positive commitment to ϕY
    (Section 20);

(c) ( Causal dependence) actions taken by Ag in [t0 , t1 ] are causally implicated in the increase of
    β + (ϕY ) in the sense of the causal/control notions of Section 14.

If there exists some interval [t0 , t1 ] for which these hold, we call Y engineered.

    The formulation intentionally uses the same representational substrate L and the same eviden-
tial/credal quantity βt+ (·) that appear elsewhere, so that “coming into existence” is not treated as a
primitive metaphysical event but as a transition that can be tracked within an agent/world-model
interface. The parenthetical “in the relevant sense” is doing work: for a physical artifact it may
mean spatiotemporal existence in an environment model, whereas for an institution or protocol it
may mean existence as a socially instantiated pattern (e.g., a stable equilibrium of expectations)
that the model can detect and reliably predict around.

Remark 1178. The three conditions separate three ideas that are often conflated. Condition (a)
is an epistemic/emergence criterion (Hyperseed-Concept ??): the world-model moves from “Y is
not (evidentially) there” to “Y is there.” Condition (b) asserts that the emergence is not accidental
relative to the agent: it sits within the agent’s intent dynamics (Hyperseed-Concept ??). Condition
(c) requires that the agent’s actions actually matter, so that “engineering” is not mere wishful
thinking.

                                                  464
    A simple example: if Y is “a bridge across the river,” then engineering requires that the bridge
comes to exist, that building-a-bridge was an active intent, and that the agent’s actions contributed
causally to the bridge’s existence. This definition is designed to interface smoothly with the later
refinement into tools, machines, and programs (Section 23; Hyperseed-Concept 191, 106, 80). In
particular, (b) is what distinguishes engineering from mere lucky correlation (e.g., the bridge ap-
pearing because another party built it while Ag merely hoped for it), while (c) is what distinguishes
engineering from mere endorsement (e.g., sincerely wanting a bridge and announcing that desire,
but having no causal handle on the construction process).

Remark 1179. Definition 332 makes “engineered” neither purely physical nor purely intentional: it
requires both an intentional commitment and a causal pathway from action to existence. Section 23
will refine this into tools/machines/programs and their realization semantics.

Remark 1180. Several boundary cases are worth making explicit because they motivate the par-
ticular choice of criteria. First, the “low”/“high” requirements in (a) are deliberately qualitative:
in applications one can pick thresholds, but the conceptual role is to demand a robust shift in sup-
port for ϕY , not a transient blip; this helps exclude cases where Y is merely hypothesized and then
discarded. Second, (b) requires an intent token g to be active for a nontrivial fraction of [t0 , t1 ] so
that momentary whim or post-hoc rationalization does not automatically count as engineering; the
intent must play a sustained role in the policy dynamics. Third, the “causally implicated” phrasing
in (c) is meant to cover indirect and distributed control: engineering a protocol or institution may
proceed by writing documents, persuading others, or building coordination scaffolding, none of which
is a direct physical construction step, yet each can provide the relevant control pathway under the
notions of Section 14.

Remark 1181. The definition also accommodates multi-agent and social artifacts by allowing Ag
to be read as an individual or a suitably defined collective agent. For example, for Y = “a ratified
constitution” the emergence criterion (a) tracks the transition from nonexistence to existence of
the constitutional regime in the relevant model; (b) corresponds to the presence of an active intent
(e.g., “establish a constitutional order”) in the collective decision process; and (c) is satisfied when
the coalition’s actions (drafting, negotiating, voting, enforcement) are causally responsible for the
increase in support for ϕY . Conversely, the definition is designed to exclude cases of mere discovery:
learning that a natural resource deposit exists may raise β + (ϕY ) dramatically, but unless Y is defined
as a newly instantiated pattern (e.g., “an operating mine” rather than “a mineral deposit”), (b)
and (c) will not align in the right way for engineering.

21.8    Intelligence, weakness minimization, and transfer by invariance
Hyperseed repeatedly links intelligence and simplicity: the intelligent system finds the weakest
representation that preserves what matters for control and value. We now formalize one clean
version of this principle: when a task is invariant under some coarse-graining, an agent loses
nothing by failing to distinguish within the coarse-graining. Said differently, when a task “factors
through” a representation map q, then planning can be performed entirely at the level of Q without
sacrificing achievable return.

Definition 333 (Task quotient / abstraction). Let T = (O, A, P, r, γ) be a task and let q : O → Q
be a surjection onto a finite set Q. Define the pushforward kernel q∗ : ∆(O) → ∆(Q) by (q∗ ν)(B) =
ν(q −1 (B)). We say q is a task abstraction if for all o1 , o2 ∈ O with q(o1 ) = q(o2 ) and all a ∈ A:

(a) ( Lumpable dynamics) q∗ (P (o1 , a)) = q∗ (P (o2 , a));

                                                  465
(b) ( Evaluation invariance) for all o+ ∈ O,

                                         r(o1 , a, o+ ) = r(o2 , a, o+ ).

    The pushforward q∗ is the standard way to express “what distribution on abstract states is
induced by a distribution on concrete observations”: sampling o+ ∼ ν and then mapping to q(o+ )
yields a random variable on Q whose law is exactly q∗ ν. The surjectivity requirement means every
abstract label corresponds to at least one concrete observation (no “dead” abstract states), and the
finiteness of Q keeps measurability issues out of the foreground; conceptually the same definition
extends to measurable Q by replacing subsets B ⊆ Q with measurable sets.
Remark 1182. The map q : O → Q is a coarse-graining: it groups fine observations into abstract
classes. Condition (a) is a standard “lumpability” requirement: from the perspective of the abstract
label q(o), it does not matter which representative o in the fiber was actually seen, because the
distribution of the next abstract label is the same. Condition (b) says the immediate evaluation
likewise ignores the within-fiber distinctions.
    Intuitively, a task abstraction is an invariance: the task simply does not depend on certain
details. This is the formal place where Hyperseed’s simplicity/weakness thesis becomes visible:
ignoring irrelevant distinctions can be free (Hyperseed-Concept 202, 143, 169; cf. [3, 2]). One may
also read this as an operational cousin of compression ideas: if the environment is invariant under
identifying certain observations, then a shorter description (in the sense of algorithmic information)
can suffice for control (cf. [16]).
    A useful way to internalize the two conditions is via “what the agent can affect and what the
agent is scored on.” Lumpability says that, after taking action a, the distribution of future abstract
observations depends only on the current abstract observation. Evaluation invariance says that the
instantaneous score attached to a transition (o, a, o+ ) depends on o only through its abstract class;
in particular, if two observations are identified by q, then they are interchangeable as far as one-step
evaluation is concerned. Together these conditions ensure that the entire value computation (not
just one-step statistics) can be performed on Q.
Theorem 19 (Invariant tasks admit quotient-optimal policies). Let q : O → Q be a task abstraction
for T = (O, A, P, r, γ). Then:
(a) There exists a reduced task TQ = (Q, A, PQ , rQ , γ) such that q induces a reduction T → TQ in
    the sense of Definition 321.

(b) Any policy πQ for TQ lifts to a policy π for T with identical p-bit value: JT (π) = JTQ (πQ ).
Consequently, an agent that represents observations only up to q (i.e. fails to distinguish within
fibers of q) is not disadvantaged on task T .
Remark 1183. In ordinary language, the theorem says: if the world does not care about some
distinctions, then you do not need to care about them either—at least not for the sake of maximizing
task value. The surprise (if any) is not that simplification can help, but that under exact invariance
it can be made rigorously lossless: there exists an abstracted task whose optimal behavior is exactly
as good as optimal behavior in the original task.
    This result connects the earlier categorical transfer machinery with the weakness/simplicity
theme: the abstraction q becomes a specific reduction morphism T → TQ , so the value-preservation
of lifted policies is an instance of Proposition 34. Thus, “simplicity helps generalization” here is
not a slogan but a factorization through a task morphism (Hyperseed-Concept 192, 202).

                                                   466
    One concrete way to read part (b) is that a policy for the quotient task can be executed on
the original task by composing with q: the agent first maps its observation o to an abstract label
q(o) and then samples an action from πQ (· | q(o)). The equality JT (π) = JTQ (πQ ) asserts that this
“act only on the abstraction” strategy is exactly value-preserving, not merely approximately good.
In particular, the optimal value functions coincide under the same identification: the best return
achievable by any history-independent policy on O is the same as the best return achievable by a
history-independent policy on Q, because any optimal πQ  ? can be lifted back to O without loss.


Proof. Define PQ : Q × A → ∆(Q) by PQ (q(o), a) := q∗ (P (o, a)). This is well-defined by lumpable
dynamics. Define rQ (q(o), a, q(o+ )) := r(o, a, o+ ); this is well-defined by evaluation invariance.
Then (q, idA ) yields a reduction T → TQ (take fO = q and fA (o, a) = a). The lifting statement is
a special case of Proposition 34.

    To make the “well-definedness” point completely explicit: if q(o1 ) = q(o2 ), then condition (a)
implies q∗ (P (o1 , a)) = q∗ (P (o2 , a)), so the expression PQ (q(o), a) depends only on q(o) and not on
the chosen representative o. Likewise, if q(o+,1 ) = q(o+,2 ), then by condition (b) (applied with fixed
o and a) the value r(o, a, o+,1 ) equals r(o, a, o+,2 ), so writing rQ (q(o), a, q(o+ )) is unambiguous as
a function of abstract next-observation. Under these definitions, the lifted policy referred to in (b)
can be taken concretely as π(· | o) := πQ (· | q(o)), which matches the idea that the agent “forgets”
all within-fiber distinctions before acting.
Proof sketch. Construct the quotient task by pushing the original dynamics forward along q and
defining the quotient reward by the invariance condition. The abstraction axioms guarantee these
definitions do not depend on which representative o of an abstract state q(o) is chosen. Once
this quotient task is built, the map q is immediately a reduction, so value-preserving policy lifting
follows from the general transfer-by-reduction proposition.                                             

Remark 1184. The decisive steps are the two “well-definedness” checks. Lumpability ensures that
PQ depends only on the abstract class q(o), and evaluation invariance ensures rQ is consistent across
a fiber. Geometrically, one can imagine collapsing the observation space O by gluing together points
in the same fiber; the theorem states that, when the task’s dynamics and evaluation are constant
along these fibers, the glued space supports an induced task with the same achievable values.

    This quotient construction is closely related to familiar notions of MDP homomorphism and
bisimulation-style aggregation: the abstract state q(o) is sufficient for predicting the next abstract
state distribution and the reward. In those literatures, one often states the condition as “the
abstract process is Markov” plus “rewards respect the partition,” which is exactly what (a) and
(b) ensure here. The present framing emphasizes the transfer consequence: invariance is not only
a modeling nicety but a certificate that a weaker representation is guaranteed to be adequate for
control.

Remark 1185 (Weakness reading). If an observer uses the abstraction q, it collapses distinctions
among o1 , o2 with q(o1 ) = q(o2 ). This increases weakness (Section 3.7) relative to a fully discrimi-
nating observer. The theorem states that this “failure to distinguish” can be free for control on tasks
that do not depend on the finer distinctions. This is a precise sense in which simplicity supports
generalization and transfer.

21.9    Micro-example: a task family with transfer by coarse-grained structure
Example 18 (Two-cluster task family on a four-element universe). Let O = {1, 2, 3, 4} and A =
{L, R}. Let q : O → Q = {α, β} be the partition map with q(1) = q(2) = α and q(3) = q(4) =

                                                   467
β. Equivalently, q identifies two equivalence classes (fibers) {1, 2} and {3, 4}, so that any two
observations in the same fiber are treated as the same “kind” of input at the abstract level.
   Consider a family of tasks {Tθ } parameterized by a label θ ∈ {0, 1} meaning “which cluster
should go left.” In T0 , the intended policy is “choose L on α and R on β.” In T1 , swap the actions.
Thus, for each θ, there is a natural optimal policy πθ : Q → A at the abstract level, and any
concrete policy π : O → A that factors through q (i.e., π = πθ ◦ q) realizes the same behavior on all
observations within a cluster.
   Define dynamics so that the observation is i.i.d. uniform on O each time-step (no state depen-
dence), and define a one-step evaluation
                             (
                              (1, 0) if a matches the cluster-action label of q(o) under θ,
            rθ (o, a, o+ ) =
                              (0, 1) otherwise.

The two-component reward can be read as a minimal “success/failure” signal (e.g., first coordinate
for “correct” and second for “incorrect”), and could be converted to a scalar reward by any fixed lin-
ear scalarization without changing the structural point of the example. Then q is a task abstraction
for each Tθ : reward depends only on q(o) and the observation law is constant on fibers. Concretely,
if q(o) = q(o0 ) then (i) the conditional distribution of observations (here simply uniform, hence
identical for all o) does not distinguish o from o0 , and (ii) the criterion for whether an action is
correct is identical for o and o0 under the same θ.
     An agent that learns the abstraction q once (a coarse pattern: “there are two kinds of observa-
tions”) can solve both tasks with only one bit of additional information (which θ holds), achieving
rapid transfer. In other words, after committing to the representation Q = {α, β}, the remaining
adaptation problem across the family {Tθ } is just to determine whether α 7→ L or α 7→ R, which is a
binary choice. An agent that insists on distinguishing all four observations has a larger hypothesis
space and can require more data to discover the same transferable structure. For example, without
using the quotient, a learner may treat the four mappings 1 7→ L/R, 2 7→ L/R, 3 7→ L/R, 4 7→ L/R
as independent degrees of freedom, even though the task family only varies along the single bit θ
once the clustering is recognized.
     In Hyperseed language: the transferable pattern is the two-cluster schema; intellectuality appears
as the speed with which the agent compresses experience into that schema and reuses it across
task contexts. From this perspective, “transfer” is precisely the reuse of the learned factorization
    q
O→ − Q → A across distinct values of θ, rather than relearning a fresh mapping O → A each time.

Remark 1186. This micro-example is intentionally austere, but it displays a genuine phenomenon:
the learnable invariant is not the particular mapping from {1, 2, 3, 4} to actions, but the partition
into two clusters (Hyperseed-Concept ??, 103). Put differently, the family {Tθ } shares the same
quotient structure q even though it disagrees about which abstract label should be assigned which
action. Once the agent has the right abstraction, the remaining uncertainty (the bit θ) is small and
can be resolved quickly, yielding high small-n intellectuality. This is a simple instance where “most”
of what must be learned is representational (discovering the right grouping), while the task-specific
learning reduces to a low-dimensional parameter fit.
    One can view this as a toy instance of a broader moral: discovering the right quotient is often the
true work of intelligence, while selecting the right action within the quotient is then routine. Here
the quotient can be seen explicitly as collapsing O by the equivalence relation o ∼ o0 iff q(o) = q(o0 ),
and the induced decision problem on Q is strictly smaller than the original one on O. This is also a
point of contact with compression-based views of learning, where discovering a shorter description
of the environment can reduce sample complexity (cf. [16]). In particular, once the agent encodes


                                                  468
the data using the two-symbol alphabet {α, β} rather than four unrelated symbols, fewer examples
are needed to justify a stable generalization across the full observation set, because each new data
point supports a whole cluster rather than a single element.

21.10    Ensembles, attention, and cognitive synergy as intelligence multipliers
Finally, we relate intelligence to attention and synergy (Section 15) in a minimal theorem: com-
bining monotone cognitive processes cannot reduce capability, and can strictly improve it when
different processes capture complementary transferable patterns. In this subsection, “cognitive
processes” can be read broadly: any subsystem that produces a belief state over a shared claim
language (e.g. a perceptual channel, a model-based predictor, a memory retriever, a theorem-prover,
or an attentional module that re-weights which claims are salient). The key structural move is that
combining such processes is modeled as an order-theoretic join on beliefs, while the downstream
control layer (action selection) is required to respect that order. This makes the non-degradation
statement essentially a monotonicity fact: more (ordered) evidence should not force fewer (good)
options.
Definition 334 (Monotone action selection from beliefs). Let β range over belief states L → V
with pointwise order. An action-selection map A(β) ∈ ∆(A) is monotone if β1 ≤ β2 implies A(β1 )
is no more restrictive than A(β2 ) (e.g. the set of actions above a fixed value threshold only grows).
In particular, one can interpret “no more restrictive” in several compatible ways depending on how
∆(A) is used: as inclusion of supports (actions assigned nonzero probability), as inclusion of an
“admissible” subset of A underlying a stochastic choice, or as monotonic expansion of the set of
actions exceeding a choice criterion computed from β. The requirement is intentionally permissive:
it does not force a unique policy, only that improving beliefs (in the ≤ sense) cannot invalidate
actions that were previously permissible under weaker belief.
Remark 1187. Pointwise order on belief states means β1 ≤ β2 iff for every claim ϕ, β1 (ϕ) ≤
β2 (ϕ) in the p-bit order. Monotonicity then encodes a rational constraint: adding evidence should
not arbitrarily forbid actions that were previously considered acceptable. This is a mild structural
assumption, compatible with many decision rules, including thresholding, softmax-like schemes,
and dominance filters. A useful way to read this is: if β2 strengthens β1 claim-by-claim, then
any action that was defensible given β1 should remain defensible given β2 (even if it is no longer
the most preferred). In practice, one can enforce such monotonicity by separating (i) a monotone
feasibility or admissibility stage from (ii) a tie-breaking or exploration stage; only the former needs
to be monotone for the proposition below to go through.
    Conceptually, monotonicity is a thin formal expression of a cognitive-synergy desideratum: when
additional cognitive processes contribute additional distinctions or evidence, the control layer should
be able to exploit them rather than being confused by them (Hyperseed-Concept 73, 60). This also
clarifies the role of attention: attentional focus can be viewed as a resource-allocation choice about
which claims are evaluated or refined, and the monotonicity requirement says that refining attention
(thereby increasing certain belief values) should not itself destroy previously available behavioral
options.
Proposition 35 (Parallel join of evidence cannot hurt under monotone control). Suppose two
cognitive subsystems produce belief states β (1) and β (2) over the same claim language, and the agent
combines them by β := β (1) ⊕ β (2) (pointwise join). If the downstream action-selection mechanism
is monotone in the belief state, then for any task T the combined system can achieve competence
at least as high as the better subsystem acting alone:
                      Comp(Ag⊕ ; T ) ≥ max{Comp(Ag1 ; T ), Comp(Ag2 ; T )}.

                                                 469
The implicit intuition is that Ag⊕ has access to at least the evidential basis of each subsystem, so it
can always choose to ignore whichever parts of the combined belief are unhelpful for a given decision
and reproduce the choices of the stronger subsystem. When Comp is evaluated via expected task
performance under the policy induced by A(β), the inequality should be read as an existence-style
guarantee: there exists a valid way for the combined agent to act (consistent with monotone control)
that attains at least the better subsystem’s competence, even if a particular learning or optimization
procedure may fail to find it.
Remark 1188. The proposition says, in effect, that “having two eyes cannot make you see worse,”
provided your action-selection respects the ordering of evidence. It is not claiming that naive en-
sembling always yields large gains; it is claiming a non-degradation property: if one subsystem was
already good, joining in additional evidence does not force you to throw away the good option. This
is one of the simplest rigorous footholds for the broader Hyperseed theme that cognitive synergy
can multiply intelligence (Hyperseed-Concept 73; cf. [19]). A further operational reading is that
the combined system can implement a gating or fallback strategy: if subsystem 1 is reliable on
a task family while subsystem 2 contributes sporadically, then the joined belief state can preserve
the reliable action set while occasionally unlocking additional high-value actions when subsystem 2
provides confirming evidence. This highlights why monotonicity is the right minimal assumption:
without it, a control rule could react pathologically to extra information by collapsing to a worse
action set, destroying the intended benefit of parallel cognition.
Proof. Pointwise, β (i) ≤ β (1) ⊕ β (2) for i = 1, 2. By monotonicity of action selection, any action
deemed feasible/good under β (i) remains feasible under the joined belief state. Therefore the
combined agent can simulate whichever subsystem attains the higher competence on T . To make
the simulation idea concrete, fix i ∈ {1, 2}. If under β (i) the control layer would select from
some admissible set (or distributional support) Si ⊆ A, monotonicity ensures that under β the
admissible set S satisfies Si ⊆ S in the relevant “no more restrictive” sense. Thus the combined
agent is permitted to choose exactly the same action (or sample from exactly the same distribution)
that Agi would, yielding the same task performance; taking the better of the two establishes the
stated lower bound.

Proof sketch. The join ⊕ is an upper bound, so each subsystem’s belief state is below the combined
belief state. Monotonicity ensures that moving upward in belief cannot eliminate the actions
available before. Hence the combined agent can always choose to behave exactly like the better
subsystem, ensuring competence at least as large as the maximum of the two. Equivalently, the
combined system has a “safe policy” option: default to the better-performing subsystem’s behavior,
and only deviate when the joined evidence expands (rather than shrinks) the set of admissible high-
quality actions.                                                                                 
Remark 1189. The proof is short because the algebra is doing the work: ⊕ is a join, so it is
literally the least upper bound, and monotonicity is exactly the condition needed to ensure upward
movement in belief does not remove options. If one wants a visual intuition, imagine two partial
maps of a landscape; taking their join is like overlaying them so that any marked safe path remains
marked safe. Strict improvement becomes possible when the joined belief state reveals an action
that neither subsystem, in isolation, had enough evidence to select. One simple sufficient condition
for strictness (in threshold-based controllers) is: there exists an action a? such that under each β (i)
its score lies just below the selection threshold, but under β (1) ⊕ β (2) it crosses the threshold due to
complementary evidence. This captures the intended “complementary transferable patterns” case:
each subsystem supplies a different piece of reusable structure, and only their combination yields a
decisive signal at the control interface.

                                                   470
Remark 1190 (Why this matters for Hyperseed). This proposition is a minimal mathematical
expression of “cognitive synergy” as an intelligence multiplier: multiple partial processes, each lim-
ited in what distinctions it can track, can be combined without loss, and with potential gain when
their pattern abstractions and transfer morphisms complement one another. Quantale weakness
then provides the bookkeeping for which distinctions are being collapsed and where new distinctions
are worth paying for. In particular, if weakness parameters encode which claims are represented
coarsely (or ignored) by a subsystem, then different subsystems may be weak in different places;
the join can partially undo those independent collapses without requiring either subsystem to bear
the full representational cost alone. This clarifies a concrete route by which attention-like mech-
anisms (allocating representational precision to a subset of claims) and ensemble-like mechanisms
(aggregating multiple such allocations) interact to yield a net capability increase.

21.11    GTGI-inspired quantitative measures of general intelligence
This subsection introduces a family of quantitative functionals intended as concrete instantiations of
General Intelligence (Hyperseed-Concept ??) in the style of GTGI. These functionals are phrased
in a policy–environment interaction formalism, but can be read as special cases of Hyperseed’s
broader “task environment” formalism (cf. the task-set/breadth machinery used to sharpen the
general/narrow distinction; see Hyperseed-Concept 118).

Basic interaction model. Fix countable sets of actions A and observations O, and a reward
set R ⊆ [0, 1] ∩ Q. A (stochastic) policy is a map

                                    π : (A × O × R)∗ → ∆(A),

and an (AIXI-style) environment is a map

                                µ : (A × O × R)∗ × A → ∆(O × R),

where ∆(S) denotes the set of probability distributions on S. Writing Eµ,π [·] for expectation over
trajectories induced by the interaction of π with µ, define the (undiscounted) expected total reward
                                                     "∞ #
                                                      X
                                        Vµπ := Eµ,π       rt .
                                                       t=1

Definition 335 (Reward-summable environment). An environment µ is reward-summable iff for
every policy π,                          "∞ #
                                          X
                                 π
                               Vµ = Eµ,π      rt ≤ 1.
                                                   t=1

(Glossary: Hyperseed-Concept 210.)

Definition 336 (Universal intelligence). Let E be a chosen set of reward-summable environments.
The universal intelligence of a policy π is
                                              X
                                      Υ(π) :=     2−K(µ) Vµπ ,
                                                µ∈E

where K(µ) is Kolmogorov complexity (Hyperseed-Concept ??) with respect to a fixed descrip-
tion/decoding scheme. (Glossary: Hyperseed-Concept 211.)

                                                 471
Definition 337 (GTGI goal function). A GTGI goal function is a map

                                             g : (A × O)∗ → R.

Given a trajectory prefix x1:t := (a1 , o1 , . . . , at , ot ) ∈ (A × O)∗ , the goal-induced reward at time t is

                                                rt := g(x1:t ).

(Glossary: Hyperseed-Concept 212.)

Definition 338 (Natural timescale indicator). Given a goal function g and environment µ, a
natural timescale indicator is a map

                                            τg,µ : N>0 → {0, 1},

where τg,µ (n) = 1 indicates that evaluating performance on g in µ over n steps is considered
meaningful, and τg,µ (n) = 0 indicates it is not. (Glossary: Hyperseed-Concept 213.)

Definition 339 (GTGI context). A GTGI context is a triple

                                                c = (µ, g, T ),

where µ is an environment, g is a goal function, and T = {t1 , . . . , t2 } is a finite time-interval of
discrete steps. Its length is |T | := t2 − t1 + 1.
    Given a policy π, the expected goal-achievement of π in context (µ, g, T ) is
                                               " t     #
                                                 X 2
                                 π
                               Vµ,g,T  := Eµ,π       rt , rt := g(x1:t ).
                                                  t=t1

(Glossary: Hyperseed-Concept 214.)

Definition 340 (Pragmatic general intelligence). Let E be a chosen class of environments, G a
chosen class of goal functions, and T a chosen class of finite time-intervals. Let ν be a probability
distribution on E, and let γ(·, µ) be a conditional probability distribution on G for each fixed µ ∈ E.
The pragmatic general intelligence of a policy π (relative to ν and γ) is
                                     XX X
                                                                           π
                          Π(π) :=                ν(µ) γ(g, µ) τg,µ (|T |) Vµ,g,T ,
                                       µ∈E g∈G T ∈T

whenever the sum is convergent. (Glossary: Hyperseed-Concept 215.)

Definition 341 (Resource-consumption distribution). Fix a discrete resource scale Q ⊆ R>0 (e.g.
time-steps, FLOPs, bytes). For each context (µ, g, T ), a resource-consumption distribution is a
probability distribution                          X
                           ηµ,g,T : Q → [0, 1],        ηµ,g,T (Q) = 1,
                                                            Q∈Q

where ηµ,g,T (Q) is the probability that Q units of computational resources are consumed by the
agent/policy while pursuing g in µ over T . (Glossary: Hyperseed-Concept 216.)




                                                      472
Definition 342 (Efficient pragmatic general intelligence). With the same E, G, T , ν, γ, τ as in Def-
inition 340, and with resource distributions ηµ,g,T as in Definition 341, the efficient pragmatic
general intelligence of π is
                              XX X X                                                                 π
                                                                                                    Vµ,g,T
                   eff
                 Π (π) :=                             ν(µ) γ(g, µ) τg,µ (|T |) ηµ,g,T (Q)                    ,
                                                                                                       Q
                              µ∈E g∈G T ∈T Q∈Q

whenever the sum is convergent. (Glossary: Hyperseed-Concept 217.)

Definition 343 (Intellectual breadth). Define the context-competence weight of π on (µ, g, T ) by
                                                            X                     π
                                                                                 Vµ,g,T
                               χConπ (µ, g, T ) :=                ηµ,g,T (Q)              .
                                                                                    Q
                                                           Q∈Q

Define a normalized distribution over contexts by

                                                 ν(µ) γ(g, µ) τg,µ (|T |) χConπ (µ, g, T )
                χPConπ (µ, g, T ) := P                                                                          ,
                                      µ0 ,g 0 ,T 0 ν(µ0 ) γ(g 0 , µ0 ) τg0 ,µ0 (|T 0 |) χConπ (µ0 , g 0 , T 0 )

assuming the denominator is finite and nonzero. The intellectual breadth of π is the Shannon
entropy of this distribution:
                                      X
                                        χPConπ (µ, g, T ) log χPConπ (µ, g, T ) ,
                                                                               
                        Bint (π) := −
                                         µ,g,T

with a fixed choice of log base (e.g. base 2). (Glossary: Hyperseed-Concept 218.)
                                                             π
    Intuitively, χConπ (µ, g, T ) aggregates performance Vµ,g,T  across an explicit “difficulty” or “com-
plexity” index Q ∈ Q, weighted by ηµ,g,T (Q). The factor 1/Q implements a conventional com-
plexity penalty: holding value fixed, competence concentrated on lower-complexity (easier) contexts
contributes more weight, while competence only at higher-complexity contexts is discounted. This
makes the induced distribution χPConπ sensitive not merely to raw reward, but to where (across
context families and difficulty) that reward is being obtained.
    The normalized quantity χPConπ (µ, g, T ) can be read as a posterior-like mass function over con-
texts, proportional to (i) prior plausibility of environments ν(µ), (ii) a coupling term γ(g, µ) indi-
cating which goals g are meaningfully posed in which environments µ, (iii) a length- or horizon-
weighting τg,µ (|T |) over task sets of size |T |, and (iv) the context-competence weight itself. Under
this interpretation, Bint (π) measures how widely the policy’s competence is spread across the space
of contexts after accounting for these priors/weights: high entropy corresponds to competence that
is distributed across many distinct (µ, g, T ) rather than concentrated on a small subset.
    The finiteness/nonzero assumption on the denominator is not only technical but conceptual: it
enforces that the weighted competence mass is normalizable, i.e. the choice of (ν, γ, τ, η) yields a
well-posed comparison across policies. In particular, if Q or the context index set is infinite, then
the decay of ηµ,g,T (Q) (and the interaction with 1/Q) governs whether χConπ is finite; similarly,
the tails of ν(µ) and τg,µ (|T |) govern whether the global sum is finite.
    Finally, the choice of log base only rescales Bint (π) (e.g. bits for base 2, nats for base e), so
comparisons of breadth across policies are invariant up to a constant factor. In applications, one
often pairs this entropy with a separate level term (e.g. average competence) to distinguish “broad
but weak” from “broad and strong” policies, although the present definition isolates breadth as
dispersion of competence mass.


                                                          473
Definition 344 (Multi-criterion driven general intelligence). Fix a feasible policy class Πadm and
a vector of objective functionals

                            J(π) := (J1 (π), . . . , Jk (π)) ∈ Rk ,       π ∈ Πadm ,

intended to represent multiple desiderata (e.g. efficiency Πeff , breadth Bint , and additional Hyperseed-
relevant criteria such as joy/growth/choice). Define Pareto dominance by π 0  π iff

                     (∀i ∈ {1, . . . , k}) Ji (π 0 ) ≥ Ji (π)   and   (∃j) Jj (π 0 ) > Jj (π).

The multi-criterion general intelligence set (Pareto front) is

                         Pareto(J) := {π ∈ Πadm : @π 0 ∈ Πadm with π 0  π}.

(Glossary: Hyperseed-Concept 219.)
    This definition makes explicit that “general intelligence” (as operationalized here) is not a single
scalar score but a family of trade-offs among multiple desiderata. Concretely, the feasible class Πadm
encodes admissibility constraints (e.g. computational budgets, safety constraints, embodiment limits,
permitted interventions, or epistemic limitations), so that the Pareto set is taken over policies that
are actually realizable under the system’s design and deployment assumptions.
    Each coordinate Ji (π) can be interpreted as a measurement functional induced by some bench-
mark family: for instance, an efficiency-like functional might quantify reward per unit time/compute;
a breadth-like functional can be instantiated by Bint (π); and additional coordinates can encode
desiderata that are not reducible to reward maximization (e.g. robustness, corrigibility, preference
learning quality, or more explicitly Hyperseed-aligned constructs such as joy/growth/choice). The
Pareto-front framing prevents premature scalarization: if two policies differ such that neither is
uniformly better across all criteria, both remain “optimal” in the multi-criterion sense.
    The strict inequality requirement in at least one coordinate ensures that Pareto dominance cap-
tures genuine improvement rather than equality. In practice, one may also consider ε-dominance
(to model measurement noise) or impose partial orders induced by constraints (e.g. treat some Ji
as hard constraints and others as objectives). These are refinements of the same core idea: multi-
criterion general intelligence is identified with non-dominated policies relative to a declared objective
vector, rather than with a unique maximizer of a single aggregated score.
    Because Pareto(J) is a set, it naturally supports subsequent selection principles (e.g. choose
among Pareto-optimal policies using a domain-specific preference over trade-offs, or choose policies
that remain Pareto-optimal under shifts in ν, γ, τ defining breadth). This separation of measure-
ment (the Ji ) from selection (how one picks a point on the front) is often crucial when aligning
agent behavior to pluralistic or evolving desiderata.

Hyperseed concepts covered
• Tasks; task sets; intellectuality as rapid transfer/generalization across tasks.

• General intelligence vs narrow intelligence (breadth and learning-curve measures).

• Agent as persistent perception-action loop; closed-loop coupling to a task.

• Autonomous agent via internal goal/intent formation and revision.

• Intent as an explicit variable shaping policy; autonomy as nontrivial internal intent dynamics.

• Stimulate/inhibit as action primitives defined by p-bit-valued effect increments on claims.

                                                        474
• Engineered as an ontological category for artifacts/patterns brought into existence by intent-
  aligned, causally efficacious intelligent action.

• Various formal criteria for measuring degres of general intelligence (and related quantities)

    The two definitions above provide a quantitative bridge from task-centric competence to agency-
level evaluation. The “intellectual breadth” measure turns competence across environments, goals,
and task-sets into an information-theoretic dispersion score, making it possible to distinguish a
policy that is competent in many context families from one that is competent in only a few.
The “multi-criterion” construction then places such breadth alongside other desiderata and treats
general intelligence as residing in the set of non-dominated feasible policies, rather than collapsing
all considerations into a single number.


22     Society, culture, and collective mind systems
22.1    From individual agents to social pattern webs
Previous sections treated a single observer/context as the primary bearer of distinctions, patterns,
beliefs, and action (Sections 9–21). Hyperseed then scales this picture to groups: societies, tribes,
cultures, and collective minds. The key methodological move is conservative:

• Keep the same core mathematics (paraconsistent p-bit evidence values and quantale-style com-
  position), but

• allow multiple agents to be coupled by communication and shared artifacts, so that patterns can
  span agents.

    Concretely, “scaling to groups” is not treated as changing the kind of object under study, but
as changing the boundary of the system whose pattern web we track. The individual case studies
a pattern web internal to one agent’s perceptual-cognitive-action loop; the social case studies a
pattern web distributed across many such loops, with additional coupling edges corresponding
to message passing, imitation, norm enforcement, and environment-mediated coordination. The
key consequence of keeping the same evidence and composition machinery is that all the usual
operations for combining, propagating, and constraining patterns (including accumulation of partial
evidence, composition of subroutines, and coexistence of incompatible commitments) remain valid,
but they now apply to a larger graph whose nodes may be multi-agent processes rather than intra-
agent ones.
    The phrase “patterns can span agents” should be read literally: some patterns are not located
in any single head, but are only well-defined at the level of interaction. For example, a question–
answer routine, a bargaining protocol, a classroom lecture, or a market price formation process
can be treated as a pattern whose realizations require at least two roles (and typically multiple
agents), with regularities that persist even as individual participants change. In the same spirit, a
shared artifact (a text, law, map, software repository, or ritual object) can be treated as a persistent
substructure in the overall pattern web, providing stable constraints and coordination points that
outlast particular communicative episodes.
Remark 1191. The philosophical point is that “sociality” is not introduced as an extra substance.
Rather, it is introduced as an additional layer of composition: we keep the individual-level formal-
ism, but we allow morphisms (influence, communication, artifact-mediated constraint) to connect
individual pattern webs into a larger web. This aligns with Hyperseed’s general stance that much

                                                  475
of mind is a matter of structured pattern dynamics rather than an ineffable residue; see also the
general Hyperseed ontology framing in [1].
    This compositional framing also makes it natural to treat social phenomena as having multiple
simultaneous “carriers”: (a) transient signals (spoken utterances, gestures, posts), (b) relatively
stable media (documents, institutions, codebases), and (c) embodied habits (skills, practices, and
dispositions). In the formalism, these carriers correspond to different kinds of coupling edges and
different persistence timescales, but they can still be integrated by the same evidence calculus: signals
supply short-lived evidence pulses, institutions provide long-lived constraints, and habits implement
default transitions that bias future pattern activation.
    In Hyperseed-Concept terms, what is being formalized here is chiefly Society (Hyperseed-Concept
170), Culture (Hyperseed-Concept 91), and the move from individual Pattern Web dynamics to
group-scale Pattern Web dynamics (Hyperseed-Concept 132), with explicit allowance for contradic-
tion via Value Paraconsistency (Hyperseed-Concept 198).
    The explicit role of paraconsistency becomes especially salient at the social scale: groups com-
monly exhibit stable patterns of behavior while holding mutually inconsistent narratives, norms,
or self-models. Rather than forcing premature consistency (which would erase important empiri-
cal structure), p-bit-valued evidence allows a society-level pattern web to encode, for example, that
a norm is publicly endorsed, privately doubted, and selectively enforced, without collapsing into
triviality. This supports modeling phenomena such as pluralism, taboo, propaganda, institutional
hypocrisy, and multi-layer norm systems as structured configurations of evidence and composition
rather than as exceptions to rational modeling.

    In this section we formalize: (i) societies and tribes as coupled multi-agent pattern webs; (ii)
communicative acts and communicative systems (speech acts and their physical realizations); (iii)
social roles as interaction templates (teacher, student, worker, colleague); (iv) culture as stabilized
intersubjective pattern web; and (v) collective mind systems, including mindplex and global brain.
    Item (i) focuses on the graph-theoretic and algebraic structure of coupling: agents are treated
as pattern-web-bearing subsystems, while social ties become morphisms that transmit constraints,
evidence, and action affordances. Importantly, coupling can be asymmetric (authority, expertise,
dependence), delayed (archives, reputation), or mediated (institutions, markets), and these variants
correspond to different composition pathways and update schedules in the distributed web.
    Item (ii) separates the illocutionary aspect of communication (what act is performed: asking,
promising, warning, asserting) from its physical realization (sound waves, ink, bits). This distinction
matters because the same physical channel can realize different speech acts depending on context,
and the same speech act can be realized across many channels; the formalism therefore treats
communicative acts as patterns that can be instantiated in multiple substrates, with evidence
accumulating both from content and from channel-dependent credibility cues.
    Item (iii) treats roles as reusable interface specifications for multi-agent patterns: a role con-
strains what inputs are expected, what outputs are permissible, and what transitions are typical.
Roles thus act as higher-level templates that compress social complexity: instead of modeling
each dyad from scratch, one models role-structured interactions and then binds agents to roles in
particular contexts, allowing rapid composition of large-scale social dynamics.
    Item (iv) characterizes culture as what remains invariant (or changes only slowly) when indi-
viduals enter and leave: a stabilized, intersubjective pattern web whose persistence is supported
by enculturation, shared artifacts, and institutional reinforcement. On this view, cultural “beliefs”
need not be located as propositional attitudes inside individuals; they can be seen as constraints on
what patterns are easy to activate, acceptable to express, or rewarded to enact in the social web.
    Item (v) extends the same apparatus to collective mind systems in which coordination and


                                                  476
shared artifact layers become sufficiently rich that group-level cognitive functions emerge: dis-
tributed attention (what the group monitors), distributed memory (archives and traditions), dis-
tributed planning (organizations and governance), and distributed self-modeling (public narratives
and metrics). The terms “mindplex” and “global brain” are treated here as endpoints on a spectrum
of integration: a mindplex emphasizes tightly coupled subcommunities (e.g., institutions or net-
works) whose interaction yields coherent higher-level dynamics, while the global brain emphasizes
planetwide information flow and coordination patterns spanning many such subsystems, without
presuming a single central controller.

22.2    Minimal social data: agents, coupling, and shared artifacts
We assume the general agent notion from Section 21: agents are persistent perception–action loops
interacting with an environment, and autonomous agents are those for which a significant fraction
of action has simplest-causal explanations internal to the agent.
    For social modeling we need, minimally, (a) a set of agents, (b) an interaction structure, and
(c) a way to represent communication and shared artifacts.
Remark 1192. The qualifier “minimally” is important: richer models often include internal state
spaces, explicit message contents, norms, payoffs, or learning rules. Here we separate what is
structural (who can affect whom, and what durable objects mediate coordination) from what is
dynamical (how agents update). The point of this subsection is to provide just enough scaffolding
that later sections can state fixed-point, stabilization, and propagation claims without committing
to a specific cognitive architecture.
Definition 345 (Interaction graph and coupling weights). Let A be a (finite or infinite) set of
agents. An interaction graph on A is a directed graph
                                    G = (A, E),           E ⊆ A × A,
where (i, j) ∈ E means agent i can directly influence agent j (by communication, direct action, or
mediated action that is “social” from the modeling perspective).
   A coupling weight is an assignment
                             K : E → [0, 1]    or    K : E → V = [0, 1]2 ,
depending on whether we want a scalar coupling or a paraconsistent (two-axis) coupling. We inter-
pret larger K(i, j) as higher bandwidth, trust, salience, or effectiveness of i’s influence on j.
Remark 1193. When A is infinite, the interaction graph is best thought of as a relation rather
than a finite data structure. In applications one may impose additional regularity (e.g. bounded
out-degree, locality constraints, or measurability assumptions) so that aggregate quantities (such as
total incoming coupling to an agent) are well-defined. Nothing in the present definition forces such
assumptions, but later analytic arguments may add them as needed.
Remark 1194. A directed edge (i, j) is not meant to imply a moral direction, but an operational
direction: there exists some channel (speech, coercion, imitation, infrastructural control, shared
tools, etc.) through which i can nontrivially alter j’s future internal state or external behavior. The
weight K(i, j) then compresses many concrete facts (bandwidth, reliability, attention, authority)
into a single scalar or p-bit-pair.
    As a simple example, in a small lab group one might take K(i, j) ≈ 0.8 for supervisor-to-
student instruction, but K(j, i) ≈ 0.3 for the reverse direction. In a peer group, one might have
K(i, j) ≈ K(j, i) ≈ 0.6 for many pairs. These are not “true” numbers; they are a modeling device
for the later fixed-point and stabilization arguments.

                                                    477
Remark 1195. In practice, K(i, j) may summarize multiple distinct channels (e.g. direct con-
versation, group chat, shared work products, or observation of third-party interactions). One can
interpret K(i, j) as an effective coupling after coarse-graining across channels and timescales. This
is useful when the model aims to capture macroscopic phenomena (consensus, polarization, insti-
tutional persistence) rather than the microstructure of individual conversations.
Remark 1196 (Why allow V-valued coupling?). If coupling is scalar, it can only say “more”
or “less” influence. If coupling is p-bit-valued, it can also represent ambivalent links: e.g. high
positive coupling (strong influence) together with high negative coupling (active resistance, distrust,
or adversarial framing). This matters in social settings where attention and belief updates can be
both attracted and repelled.
Remark 1197. Allowing V-valued coupling is also a mathematical way to treat “mixed valence”
social relations without forcing them into a single real axis. In many real societies, a source may
be simultaneously salient and distrusted; the recipient may attend closely in order to rebut, parody,
or guard against manipulation. Paraconsistency thus enters not only at the level of beliefs but at
the level of channels themselves, echoing Hyperseed’s broader stance that contradiction is often a
stable feature of complex adaptive systems rather than an immediate catastrophe; compare [3] for
related uses of resource-sensitive algebraic structure.
Remark 1198. One convenient reading of a p-bit-valued edge K(i, j) = (k + (i, j), k − (i, j)) is that
k + parameterizes how strongly j is pulled toward adopting or integrating i’s outputs, while k −
parameterizes how strongly j is pushed toward counter-signaling, discounting, or producing anti-
correlated outputs in response. This interpretation allows a single graph to represent settings in
which opposition is coupled (and thus structured) rather than merely absent interaction.
Remark 1199. Nothing requires the coupling to be static across time. One may generalize to
Kt (i, j) (discrete time) or K(i, j; t) (continuous time) to represent attention cycles, institutional
reconfigurations, or learning about trustworthiness. In such cases the interaction graph itself can
be time-varying, e.g. Et ⊆ A × A, with edges appearing or disappearing as agents enter or leave a
community, or as communication channels become available or are blocked.
Definition 346 (Shared artifacts). Let A be a set of artifacts (documents, tools, rituals, institu-
tions, machines, shared environments, shared memory stores, etc.). An access relation is a relation

                                            Acc ⊆ A × A,

where (i, a) ∈ Acc means agent i can read/use/modify artifact a (in the sense relevant to the model).
Optionally, we enrich access with weights κ(i, a) ∈ [0, 1] or κ(i, a) ∈ V to represent accessibility,
trust, and friction.
Remark 1200. The access relation is intentionally broad: “read” may mean perception (seeing a
public sign), “use” may mean executing a procedure embodied in a tool, and “modify” may mean
editing a document, changing an institutional policy, or physically altering an environment. In many
cases, access is asymmetric: some agents can modify an artifact that others can only observe, which
can be represented either by directional refinement (separate read/write relations) or by encoding
this asymmetry in κ(i, a).
Remark 1201. One may also view (A, A, Acc) as a bipartite graph and then “project” it to obtain
an induced agent–agent coupling via shared artifacts: two agents become effectively coupled if they
co-access or co-modify the same artifact. This makes explicit how environments and institutions
can generate social structure even when direct communication is sparse.

                                                 478
Remark 1202. Artifacts are the simplest route from ephemeral interaction to durable structure. An
utterance fades, but a written protocol, a code repository, a ritual, or an institution can persist and
thereby “store” patterns that many agents can later re-import into their own webs. In Hyperseed-
Concept terms, this is a core mechanism by which Culture (Hyperseed-Concept 91) acquires memory
beyond individual lifetimes.
    As an example, a shared calendar is an artifact: it constrains coordination by offering a per-
sistent representation of commitments. A library is an artifact: it stores a vast set of template
patterns and inference habits that can be repeatedly instantiated by different minds. Even a physical
tool can be an artifact in this sense; Section 23 treats this more explicitly via physical realizations
of abstract processes.

Remark 1203. The artifact view also clarifies how “the same” cultural object can be instantiated
in many media. A norm may exist as an explicit written rule, as a repeated ritual practice, and as a
set of implicit expectations encoded in many agents’ policies; modeling it as an artifact (or a small
constellation of artifacts) provides a common handle for these heterogeneous realizations. This will
matter later when distinguishing transient alignment (momentary coordination) from persistent
alignment (coordination maintained by externalized memory and enforcement).

   Artifacts are crucial in Hyperseed because they create durable cross-agent coupling: a belief,
pattern, or procedure can persist outside any one individual and propagate through time.

Remark 1204. This durability can be treated as a timescale separation: interactions among agents
may be fast and noisy, while artifact dynamics are slower and more inertial. Modeling artifacts
explicitly therefore supports explanations of social stability (and of abrupt regime shifts) that do not
rely on assuming stable individual psychology. In particular, once artifacts are present, a society
can exhibit path-dependence: early contingencies become “locked in” by persistent representations
that shape later learning and coordination.

22.3     Society as a coupled multi-agent system
Hyperseed’s informal definition emphasizes sustained close interaction and dependence. Our formal
definition keeps the spirit but stays minimal. In particular, the aim is to isolate a small set
of coupling primitives that can later be instantiated in many ways: communication, imitation,
exchange, instruction, coercion, care, and other recurrent channels of mutual influence. The guiding
idea is that “being a society” is less about any one mechanism (e.g. kinship, markets, or law) than
about the existence of persistent feedback loops among agents, mediated both directly (agent–agent
interaction) and indirectly (through durable shared structures).

Definition 347 (Society). A society is a tuple

                                     Soc := (A, G, K, A, Acc, D),

where:

• A is a set of agents;

• G = (A, E) is an interaction graph;

• K is a coupling weight on E;

• A is a set of shared artifacts;


                                                  479
• Acc ⊆ A × A is an access relation; and

• D is (optional) additional domain structure capturing the resource-flow and reproduction de-
  pendencies relevant to the society (metabolism, exchange, child rearing, maintenance of shared
  infrastructure, etc.).

Remark 1205. The tuple Soc is intentionally austere: it says that a society is (i) a population
of agents, (ii) a directed coupling structure among them, and (iii) a set of external structures
that agents can jointly read and write. In this sense it is closer to a “minimal ontology of social
coupling” than to a sociological theory. The formalism is designed to support later questions such
as: which patterns stabilize; which beliefs become shared; which roles emerge; and when the group
behaves in a mind-like fashion. One should read G and K as describing effective influence rather
than any single physical channel: an edge (i, j) ∈ E indicates that, in the relevant timescale,
agent i can affect agent j’s state or action selection in a repeatable way, while the weight K(i, j)
parameterizes the strength, rate, or reliability of that effect (depending on the modeling choice used
later). The “shared artifacts” A play the role of an external memory and coordination substrate:
they include objects like documents, codebases, signage, norms-as-inscriptions, ledgers, shared tools,
or institutions understood as stateful entities that persist beyond any single interaction. The access
relation Acc makes explicit that not all agents necessarily have symmetric visibility or control over
each artifact, allowing the same formalism to represent, for example, private vs. public channels,
credentialed systems, censorship, and asymmetric power to modify common resources.
    A simple example is a two-agent society with A = {1, 2}, E = {(1, 2), (2, 1)}, a symmetric
K(1, 2) = K(2, 1) = 0.7, and A containing a shared notebook. Even this toy case already permits
nontrivial cultural stabilization: repeated reinforcement through the notebook can induce long-lived
habits that neither agent would sustain alone. Here the notebook functions as a minimal “public
world”: each agent can offload intermediate results, commitments, and cues, and then later re-
import them as if they were environmental facts. This kind of indirect coupling is important because
it can create path dependence: once certain entries exist, they bias future behavior even if the
immediate interpersonal influence K is weakened or intermittent.

Remark 1206. This definition is also a convenient “socket” into which more specialized theories
can be plugged. For instance, if one wants to reason about prosocial coordination as efficiency gain,
one can enrich D with explicit resource-flow and bargaining constraints, connecting with arguments
like [6]. But the present section keeps D optional so the mathematics does not presuppose any
particular economics or evolutionary story. Concretely, D can be used to add whatever additional
state variables and constraints are needed to make “dependence” precise in a given application: en-
dowments, production functions, task graphs, consumption needs, enforcement mechanisms, spatial
structure, or demographic turnover. Leaving D optional is also a way to separate two questions
that are often conflated: (a) what makes interaction socially coupled at the level of information
and control (handled by G, K, A, Acc), and (b) what makes that coupling necessary or stable given
material constraints (often captured in D).

Remark 1207 (Where “metabolism and reproduction” enter). If one wants to explicitly encode Hy-
perseed’s biological emphasis, D can include a resource-flow network (who supplies what to whom),
plus reproduction/maintenance processes. For many cognitive and cultural applications, it is enough
to treat D as implicit and to work directly with G, K and the shared artifact layer. One can view
this as a modeling choice about the boundary between “social cognition” and “social ecology”: if the
focus is on belief dynamics, norm propagation, institutional memory, or collective decision-making,
then the informational coupling via G, K and the persistence provided by A may be the dominant


                                                 480
explanatory variables. By contrast, when studying collapse, resilience, demographic transitions, or
long-run selection pressures, making D explicit becomes important because it specifies the feasibility
constraints under which cultural patterns must reproduce.

Remark 1208 (Interpretation notes (noncommittal but operational)). The components of Soc
are intentionally typed only loosely at this stage. For example, K may be taken as a function
K : E → R≥0 , a stochastic matrix on A, a time-dependent weight Kt , or even a vector of modality-
specific couplings (communication, observation, sanction, etc.); later sections can choose the level
of structure appropriate to theorems being proved. Similarly, A may be instantiated as a set of
discrete objects, as a shared state space, or as a collection of writable variables with an update
semantics; the only essential requirement is that artifacts provide a medium through which effects
can persist and propagate beyond a single dyadic exchange.

22.4    Tribes as tightly intertwined sub-societies
Hyperseed treats a tribe as a society that is “very tightly intertwined” and typically small enough for
many direct interactions among members. We formalize this as a high-coupling, high-connectivity
regime.

Definition 348 (Strong-tie threshold graph). Fix a threshold τ ∈ (0, 1]. Given a society Soc =
(A, G, K, . . .) with scalar couplings K : E → [0, 1], define the strong-tie graph Gτ = (A, Eτ ) by

                                   Eτ := {(i, j) ∈ E : K(i, j) ≥ τ }.

If K is V-valued, one may threshold on a projection, e.g. the plausibility map π(p, q) = (1 + p − q)/2
(Section 14) or simply on the positive axis.

Remark 1209. Intuitively, Gτ discards the weak, occasional, or negligible interactions and keeps
only the links strong enough to function as reliable conduits for habit, language, norm, and belief
transfer. The threshold τ is not a metaphysical constant; it is a modeling knob that selects a
time-scale and a notion of “meaningful influence.”
    As a small example, if in a workplace K(i, j) measures average weekly effective communication,
then a high τ might isolate a close-knit team (a tribe-like substructure), while a low τ might recover
the whole organizational chart. In Hyperseed-Concept terms, this is a way to carve out a Tribe
(Hyperseed-Concept 194) as a high-coupling region inside a Society (Hyperseed-Concept 170).

Remark 1210. Depending on the modeling choice for G and K, the strong-tie graph Gτ may
be treated as undirected (mutual strong ties) or directed (asymmetric influence or attention). In
the directed case, “(strongly) connected” in later definitions can be interpreted as strong connec-
tivity when influence is genuinely directional, whereas in the undirected case it reduces to ordinary
graph connectivity. When K(i, j) is not symmetric, one can also consider symmetrizations such as
min{K(i, j), K(j, i)} (for mutuality) or max{K(i, j), K(j, i)} (for one-way influence) before thresh-
olding, depending on whether tribal cohesion is intended to require reciprocal contact.

Remark 1211. Varying τ induces a natural filtration of graphs: if τ1 ≤ τ2 then Eτ2 ⊆ Eτ1 . Thus,
as τ increases, strong-tie components can only split (or disappear), never merge. This monotonicity
supports a multi-scale reading of “tribal structure” in which higher τ reveals the most robust, re-
peatedly reinforced cores, while lower τ reveals looser coalitions that may still be socially meaningful
at a longer time-scale.

Definition 349 (Tribe). A tribe (relative to τ ) is a subset T ⊆ A such that:

                                                  481
(a) the induced strong-tie subgraph Gτ [T ] is (strongly) connected; and

(b) T satisfies a boundedness condition reflecting finite memory/interaction bandwidth, modeled
    either as an explicit size bound |T | ≤ N or as a density condition such as
                                           1       X
                                                     1[(i, j) ∈ Eτ ] ≥ δ,
                                    |T |(|T | − 1)
                                                 i6=j∈T

     for some δ close to 1.

Remark 1212. Condition (a) enforces that strong ties form a single influence-component rather
than a scattering of dyads. Condition (b) encodes the idea that tribes are not merely connected but
thickly connected (or at least bounded in size so that connectivity is experientially meaningful). The
two modeling options for (b) reflect two ways of cashing out bounded cognitive bandwidth: either
limit the number of close ties, or require that close ties be dense among the members.
    A canonical example is an extended family or small religious community where most members
interact directly and repeatedly. By contrast, an online fandom might be connected but not dense;
in that case it may be a society with many tribes rather than a tribe itself.

Remark 1213. The density expression in (b) is written in a directed-edge style (summing over
ordered pairs i 6= j). If one instead models Gτ as undirected, the analogous normalization uses
|T |(|T | − 1)/2 and the indicator for {i, j} ∈ Eτ ; the conceptual role of the condition is the same:
it approximates the claim that “nearly everyone in T is in frequent contact with nearly everyone
else.”    In empirical settings, one may also replace density by an average-degree constraint (e.g.
 1 P
|T |   i∈T degGτ [T ] (i) ≥ d) when ties are not expected to be fully meshed but are still expected to be
richly redundant.

Remark 1214. The size-bound option |T | ≤ N can be read as a formal proxy for conversational
and attentional limits (often discussed informally via “Dunbar-like” constraints), while the density
option can be read as a proxy for repeated joint context (shared routines, shared reference frames,
and repeated mutual updating). These are not competing metaphysical theses: they are alternative
handles on the same modeling intent, and they can also be combined when one wants “small and
dense” as the operational definition of tribal cohesion.

Remark 1215. In many real societies, tribes overlap: an agent may simultaneously belong to a
family unit, a work cell, and a religious circle. The present definition treats a tribe as a subset
T ⊆ A and does not require a partition of A; consequently, different tribes may intersect, and the
same agent may serve as a high-coupling “bridge” across multiple tribal contexts. When overlap is
common, one can interpret Gτ as supporting a cover of A by connected, bounded, high-density sets,
rather than a disjoint decomposition.

Remark 1216 (Why tribes matter for later sections). Tribal substructure is where morphic reso-
nance and cultural stabilization become most visible: high coupling and repeated interaction create
strong reinforcement dynamics. In the later “mindplex” discussion, tribes are a natural scale at
which notable coherence can arise.

Remark 1217. One practical reason to isolate tribes is that many dynamical claims (diffusion
of habits, norm formation, convergence of belief-like variables, stabilization of shared symbols)
have qualitatively different behavior on sparse-but-connected graphs versus dense, redundant graphs.
Dense strong-tie subgraphs support multiple independent paths of reinforcement, making them less


                                                  482
fragile to occasional edge failures, episodic disengagement, or the removal of a single highly con-
nected individual. In this sense, the density/size boundedness condition can be read as a robustness
surrogate: it aims to rule out “connected only through a single corridor” structures that behave
more like chains of acquaintance than like tightly intertwined sub-societies.

Remark 1218. Hyperseed’s mention of “morphic resonance” gestures at reinforcement across
time and across instances; the present section uses it only as an intuition, not as an extra axiom.
Where it is used as an explanatory frame, it is natural to connect it to [13] and to the formal
habit and resonance machinery earlier in the document. In Hyperseed-Concept terms, see Morphic
Resonance (Hyperseed-Concept 115) and Autocatalytic Sets (Hyperseed-Concept 61) for related
self-reinforcement imagery.

Remark 1219. Finally, the thresholding perspective makes contact with standard community-
detection intuitions without committing to a particular algorithm: tribes can be approximated by
connected components of Gτ (when boundedness is enforced by N ) or by searching for dense con-
nected subgraphs inside Gτ (when boundedness is enforced by δ). In applications, one may choose
τ by a measurement convention (e.g. “at least once per day”), by calibration to observed cohesion
(e.g. self-reported trust), or by stability across nearby thresholds (selecting tribes that persist over
a range of τ values as especially robust sub-societies).

22.5    Communicative acts and communicative systems
Hyperseed treats communication as an action by one complex interactive system aimed at effecting
a communicative act on another system, and emphasizes that communicative acts come in multiple
logical forms (speech acts) and multiple physical forms. In particular, the same abstract message
can be instantiated as spoken language, written text, gestures, signals embedded in artifacts, or
machine-to-machine protocol events; the formal layer below is deliberately indifferent to these
carrier modalities, treating them as different physical realizations of a shared state-transformer
schema.
    Our minimal formalization is built on the epistemic layer (Section 20). Fix a claim language L
and recall the p-bit domain V = [0, 1]2 . The purpose of reusing V here is to make “communication”
compatible with the same evidence geometry already used for learning, inference, and aggregation,
so that receiving testimony is treated as one more evidence-producing interaction rather than as a
separate logical primitive.

Remark 1220. Here L is simply a set of well-formed “claims” (propositions, statements, hy-
potheses) about which agents can store and exchange evidence. We do not assume L is complete,
consistent, or even closed under all classical connectives; the epistemic layer already allows para-
consistent inference and resource-sensitive closure. In communicative settings, this flexibility is
essential: natural-language discourse rarely presents itself as a tidy Boolean algebra, and social ac-
tors routinely trade in partially formalizable claims (e.g. vague predicates, defeasible generalizations,
or context-indexed statements) whose logical closure properties are not globally stable.

Definition 350 (Messages as paraconsistent evidence bundles). A message is a finitely supported
function
                                        m : L → V,
interpreted as “the sender is transmitting this bundle of positive/negative evidence about claims.”
Let Msg(L) denote the set of messages.



                                                  483
Remark 1221. “Finitely supported” means that m(ϕ) 6= (0, 0) for only finitely many claims ϕ.
This reflects the mundane constraint that each communicative act carries only bounded explicit
content, even if it triggers further inferences in the recipient. The codomain V = [0, 1]2 means that
each claim receives two independent coordinates: positive evidence and negative evidence, as in the
p-bit framework used throughout the epistemic and value layers. One can also regard a message
as the “public” part of a richer communicative event: prosody, timing, source identity, and shared
situational context are not encoded in m itself, but can be incorporated indirectly through how the
recipient chooses the coupling k (or through auxiliary state variables in more detailed models).
    As a toy example, if L contains claims {“it will rain”, “the bus is late”}, a message might assign
(0.8, 0.1) to “it will rain” and (0.0, 0.0) to everything else, thereby asserting rain with mild doubt,
and staying silent about the bus.

Definition 351 (Belief states and message assimilation). Let βj : L → V be agent j’s belief state.
Given a coupling value k ∈ [0, 1] (or k ∈ V), define the assimilated message k m by
                                           (
                                            (k, k) ⊗ m(ϕ) if k ∈ [0, 1],
                          (k m)(ϕ) :=
                                            k ⊗ m(ϕ)         if k ∈ V,

where ⊗ is the quantale product on V from Section 3. Define the belief update

                                         βj ← βj ⊕ (k    m),

where ⊕ is the componentwise join on V. Optionally, after receiving a message the agent applies
an inference closure (Section 20.5) to propagate implications.

Remark 1222. The operator            here is not a new primitive; it is just notation for “scale the
message by the coupling strength.” If k ∈ [0, 1], we embed it as (k, k) ∈ V so that the same ⊗
operation can be used uniformly. The update βj ← βj ⊕ (k m) then says: the recipient retains
their existing evidence and also joins in whatever evidence arrives through the channel, discounted
by coupling. Operationally, k can be read as a compressed stand-in for many social and cognitive
factors: trust in the sender, perceived expertise, attention allocation, channel noise, and incentives.
Allowing k ∈ V further permits asymmetric coupling—e.g. a recipient might treat the sender as
reliable for positive testimony but unreliable for denials, or conversely discount affirmations while
taking warnings seriously.
    A simple numerical example: if k = 0.5 and m(p) = (0.8, 0.2), then (k, k) ⊗ m(p) yields a down-
weighted evidence pair for p (depending on the exact ⊗ defined in the p-bit quantale). Joining
this into βj (p) accumulates evidence without requiring consistency. In richer settings one may also
consider claim-dependent coupling k(ϕ), or context-dependent coupling chosen as a function of the
act type α and conversational state; the present formalization keeps k uniform to isolate the core
mechanism.

Remark 1223 (Paraconsistency is the default at social scale). Even if each individual is internally
“mostly consistent” (in some approximate sense), the join of many individuals’ evidence streams
quickly yields conflicting evidence on many claims. Hyperseed’s paraconsistent stance therefore
becomes more natural, not less, as we scale up. The point is not merely that different agents disagree,
but that a single recipient typically integrates heterogeneous sources whose evidential standards and
error modes are not aligned, making some degree of contradiction an ordinary equilibrium condition
rather than a pathology.



                                                 484
Remark 1224. Conceptually, this is the same reason classical logic is a poor description of large
bodies of testimony: the world is large, observers are limited, and social incentives are mixed.
Hyperseed treats this not as an anomaly but as a structural property of any large coupled epistemic
system. The mathematical role of the p-bit domain is precisely to let contradiction be represented
without allowing it to collapse the entire inferential apparatus; compare the paraconsistent framing
in [24] for a different (but thematically related) use of non-classical structure. In communicative
terms, this means that “he said, she said” does not force the system into triviality; instead it yields
a state in which both positive and negative evidence coordinates can be simultaneously high, and
downstream decisions can explicitly condition on that mixed evidential profile.

Definition 352 (Communicative act types). A communicative act type is an intended state-
transformer that uses a message as a vehicle. We use the following Hyperseed-aligned types:

(a) Question: aims to elicit an answer (a message or action) or to provoke inquiry in the recipient.

(b) Response: aims to answer a question by transmitting evidence or constraints.

(c) Command: aims to cause the recipient to carry out some particular action.

(d) Statement: aims to cause the recipient to possess a certain belief (evidence update).

(e) Interjection: aims to cause the recipient to possess a belief about the sender’s emotional state
    or attitude (a value/affect update; Section 18).

Formally, an act is a triple (i, j, α, m) where i is sender, j is recipient, α is act type, and m
is message content. The act type determines which internal variables of j are targeted (beliefs,
goals, attention, affect), and how m is interpreted. In particular, the same evidence bundle may
be processed differently depending on whether it is treated as an answer to a standing question, a
freestanding assertion, or a socially binding directive; act types therefore function as a routing layer
that selects the relevant update operators and any associated normative or procedural constraints.

Remark 1225. This definition separates content (the evidence bundle m) from illocutionary force
(the act type α). That separation is useful because the same propositional content can be used as
a statement, a hint, a threat, or a question depending on context; conversely, the same act type
(question, command) can be realized with many different contents. In addition, it clarifies how
communicative success and communicative uptake can diverge: the sender may intend a command
while the recipient treats it as mere information, or the sender may pose a question whose primary
function is to shift attention rather than to obtain new evidence. This gap between intended and
realized state-transformation is one locus where social power, shared norms, and institutional roles
enter the model (e.g. by modulating k, by constraining admissible responses, or by altering which
state variables are allowed to be targeted by particular senders).

Definition 353 (Communicative systems as coupled message dynamics). A communicative system
over a population of agents A is given by (i) belief states {βi }i∈A , (ii) a set of admissible act types
(as above), and (iii) coupling parameters {kij }i,j∈A (with kij ∈ [0, 1] or kij ∈ V) specifying how
strongly j assimilates messages from i. A communicative episode can then be modeled as a finite
sequence of acts
                                (i1 , j1 , α1 , m1 ), . . . , (iT , jT , αT , mT ),
with each act inducing an update to the targeted state of the recipient (e.g. belief update via βjt ←
βjt ⊕ (kit jt mt ) in the case of statements).


                                                  485
Remark 1226. This system-level view makes explicit that “communication” is not only a dyadic
event but a networked process: repeated updates, feedback, and multi-party routing (broadcast, gos-
sip, institutional reporting) can be represented by composing these elementary acts. It also highlights
that coupling is typically directional (kij 6= kji ) and role-sensitive, and that stability phenomena
(e.g. convergence to shared high-positive evidence, polarization into incompatible evidence profiles,
or persistence of mixed evidence) are properties of the induced dynamics rather than of any single
message in isolation.

Remark 1227. As an example, “Close the window” is a command. “Could you close the window?”
is syntactically a question, but pragmatically often functions as a command; in a richer model, that
pragmatic mapping would live in the recipient-side update rules associated with α and the context
encoded in K and attention variables. In particular, the same surface form can map to different
illocutionary forces depending on relational context (e.g. power asymmetries, politeness conventions,
shared projects), local attentional state, and the agent’s estimate of channel costs (e.g. whether direct
imperatives are socially penalized). Formally, this means that the decoding and update stages may
depend not only on the message token but also on latent variables internal to the receiver (and, in
multi-turn settings, on dialogue state), so that the “meaning” relevant for state change is a function
of (m, βj , attentionj , K(i, j), . . . ) rather than of m alone.

Definition 354 (Communicative system). A communicative system on a society is a choice, for
each ordered pair (i, j) ∈ E, of:

• a message alphabet/space Msgij (often a subset of Msg(L));

• encoding/decoding maps (possibly stochastic) that implement the physical channel; and

• update rules on the recipient (belief update, goal update, attention update, etc.).

We write this data collectively as Com = (Msg, Enc, Dec, Upd). It is important that the choice is
made for each ordered pair (i, j): communication can be asymmetric in both capacity and interpre-
tation (e.g. agent i can reliably address j but not vice versa; or j treats i as authoritative while i
discounts j). The dependence on (i, j) also lets the model represent institutionally mediated chan-
nels (moderation, bureaucracy, publication) as special cases of edges with distinctive Enc/Dec and
with characteristic filtering or amplification in Upd. Finally, allowing Msgij to differ across edges
captures the fact that not all agents share the same vocabulary, protocol, or representational format,
even when they participate in the same society-wide network.

Remark 1228. The communicative system Com is where “language” and “media” enter the for-
malism, but in a way that keeps us honest: communication is not magic, it is a channel with an
encoding, a decoding, and a state-update. This is compatible with Shannon-style abstraction, but
the state being updated is paraconsistent and value-sensitive rather than a single probability distri-
bution. Put differently, Shannon theory idealizes the transmission of symbols; here we additionally
specify what receiving a symbol does to an agent’s cognitive state, and we do not assume that this
effect can be reduced to a single scalar belief. The separation into Enc, Dec, and Upd also forces an
explicit distinction between (i) channel errors (noise, loss, distortion), (ii) interpretive divergence
(the same token mapped to different internal content), and (iii) normative or strategic response (the
receiver may understand but decline to update, or may update attention/values without accepting
propositional content).
    As a simple example, Enc could be “serialize evidence pairs into a JSON packet” and Dec could
be “parse the packet,” while Upd could be the join-update βj ← βj ⊕ (k m). In face-to-face speech,


                                                  486
Enc/Dec are biophysical and socially trained processes, and Upd includes pragmatic inference and
attention modulation (Section ??; see also the broader cognitive-systems framing in [19]). Note that
even in the “JSON packet” case, the decoding stage typically includes a schema agreement (what
fields mean) and a trust calibration (how much weight to place on the packet), both of which can
be modeled either as part of Dec (mapping bytes to structured internal objects) or as part of Upd
(mapping structured objects to state change). Likewise, the weighting factor k can be interpreted
as folding into a single scalar multiple heterogeneous features such as channel reliability, source
credibility, alignment of incentives, and current cognitive load; making these components explicit
yields richer update operators without changing the overall architecture.
     A further consequence is that communication protocols (turn-taking rules, quoting, forwarding,
cryptographic signing, moderation queues) can be represented by enriching Enc/Dec and by letting
Upd depend on message metadata (timestamps, signatures, provenance, thread position). This
matters in collective settings because many social phenomena (rumor cascades, institutional trust,
polarization) are driven at least as much by these protocol-level variables as by the propositional
content transmitted.

Physical realizations. Hyperseed emphasizes that the same logical act types can be physically
realized in different ways. We therefore treat physical forms as implementations of Enc/Dec: the
same act type α (e.g. asserting p, requesting an action, signaling approval) may be instantiated as
a spoken utterance, a gesture, a written note, or a machine-readable command, with potentially
different error profiles and with different degrees of persistence and publicness. This perspective
also makes it natural to treat “translation” (between languages or modalities) as composition of
encoding/decoding maps, where translation quality becomes part of the effective noise model and
can be learned or institutionalized.

• gesture (iconic/indexical signaling),

• “Hmmmmm” (holistic, manipulative, multi-modal, musical, mimetic signaling),

• spoken language,

• written language,

• social language (used inside a society),

• natural language (evolved by use),

• constructed language (engineered, e.g. Lojban),

• programming language (communication with a machine; see Section 23).

We will not formalize each form separately; instead we treat them as different channel families
with different noise models, bandwidth, grounding constraints, and habit formation dynamics.
Here “bandwidth” includes not only raw symbol rate but also effective expressive capacity under
shared conventions; “grounding constraints” include the degree to which signals are anchored to
shared perception/action loops (e.g. pointing in a shared environment versus reference in a text-only
forum); and “habit formation dynamics” covers how repeated use of a channel changes both avail-
ability (ease of production) and interpretation (default pragmatic enrichments). This is also where
latency and synchronization enter: some channels support rapid repair (immediate clarification)
while others require asynchronous clarification, which alters the feasible structure of multi-step
coordination.

                                                487