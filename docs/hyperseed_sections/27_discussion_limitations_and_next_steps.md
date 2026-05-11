# 27 Discussion, limitations, and next steps

• Effort to move: changing internal (or external) state has a kinetic/transport cost.
• Effort to resist: maintaining a trajectory that diverges from a reference (“natural”) dynamics
  has an informational/forcing cost.
Wu wei then means: among all ways of achieving the intended result, follow the path that minimizes
these costs, subject to constraints.
Hyperseed concepts covered here. Wu wei; wu wei dynamics; fluid flow and optimal control;
minimum representational effort as the bias shaping the flow.
   To make the phrase “geometry induced by weakness” concrete, it is useful to imagine that
the agent’s state (or belief-state) lives on a manifold (or simply a high-dimensional space) x ∈ X ,
and that “weakness” supplies a local notion of difficulty for representing, predicting, or enacting
changes around x. Mathematically, this can be encoded as a position-dependent metric (or, more
generally, a convex local norm) gx (·, ·) that determines which directions are “easy” and which are
“hard” given the agent’s limited descriptive resources. In such a setting, the effort-to-move term
naturally takes the form of a kinetic energy measured in this metric,
                                               Z T
                                                    1
                                Emove [x(·)] ≡        hẋ(t), ẋ(t)igx(t) dt,
                                                 0  2
so that a geodesic under g is precisely a path that changes state in the least effortful way relative to
the agent’s representational constraints. This is the sense in which wu wei is not “doing nothing,”
but rather “moving along directions that are already cheap,” i.e., moving in the grain of what the
system can express without strain.
    The effort-to-resist term can be framed in parallel by introducing a reference dynamics (the
“passive unfolding”) and measuring how strongly a controlled trajectory must depart from it. For
example, one may posit a baseline dynamics ẋ = f (x) (or a stochastic baseline, if noise is essential
to the model), and represent deliberate intervention via an additive control u,

                                   ẋ(t) = f (x(t)) + B(x(t)) u(t).

In this case, “minimal forcing” means not merely that u is small in magnitude, but that it is small
in the right units: the units are again dictated by weakness, via a cost or norm that penalizes
interventions that are informationally expensive for the agent to specify or sustain. A canonical
form is                                            Z T
                                                       1
                            Eresist [u(·), x(·)] ≡       hu(t), u(t)iRx(t) dt,
                                                    0 2
where Rx can be interpreted as an inverse “control authority” or, equivalently, as a local resistance
tensor (so large Rx means forcing is costly). In probabilistic terms, and especially when one
works with stochastic reference dynamics, this same idea can be expressed as an informational
divergence between the controlled and uncontrolled path measures; then “gentle reweighting” can
be taken literally as changing the likelihood of trajectories without inventing fundamentally alien
ones, which aligns with the remark above that effective agency can appear as a modest tilt of what
would have happened anyway.
    Finally, the phrase “subject to constraints” should be read broadly: constraints may encode
reaching a target set, matching terminal conditions, satisfying safety bounds, or (in the valuation
language of earlier sections) tracking a potential-like objective derived from resonance-weighted
evidence. In the variational picture, these constraints enter as boundary conditions or as Lagrange-
multiplier terms that shape the Euler–Lagrange equations (or, in control language, the Hamilton–
Jacobi–Bellman conditions). The resulting wu wei trajectory is thus the one that (i) respects what

                                                  576
the agent can represent and execute with low complexity (weakness), (ii) remains close to the
reference unfolding unless deviation is genuinely needed (minimal forcing), and (iii) still attains the
intended outcome via the least costly reconfiguration of the flow.

26.1    Wu wei as minimal-forcing control relative to a passive dynamics
We start with a discrete-time, finite-state formulation that makes the “minimal forcing” idea ex-
plicit. In this setting, “control” does not mean selecting an arbitrary action in a separate action
set; instead, the agent’s decision is directly a choice of next-state distribution P (· | x), and the
central question becomes how much this chosen distribution departs from a baseline P0 (· | x).
Definition 435 (Passive and controlled dynamics). Let X be a finite state space. A passive (or
unforced) dynamics is a Markov kernel

                                   P0 (· | x) ∈ ∆(X)      (x ∈ X),

where ∆(X) is the probability simplex on X. A controlled dynamics is a kernel P (· | x) ∈ ∆(X)
that the agent may choose. A (stationary) policy is a map π that assigns to each state x a controlled
kernel Pπ (· | x).
Remark 1469. Intuitively, P0 (· | x) is “what the world (and agent) tend to do” when currently
at x, before we impose any task-specific steering. Saying that P0 (· | x) ∈ ∆(X) simply means it is
a probability distribution over next states: for each fixed x, the numbers P0 (x0 | x) are nonnegative
and sum to 1 as x0 ranges over X. A controlled kernel P (· | x) is another such distribution,
representing the agent’s choice of how to bias the next step from x.
Remark 1470. It is worth emphasizing what is not assumed here: we do not posit an explicit action
space A with transition law P (· | x, a). One may recover that standard viewpoint by taking P (· | x)
to be the marginal transition kernel induced by choosing an action (or a randomized action) at x.
However, the present formulation is more direct for wu wei because it foregrounds the comparison
between an “effortless” flow P0 and any “steered” flow P .
Remark 1471. A simple example is a random walk on a small graph whose nodes are X. The
passive kernel P0 (x0 | x) could put equal probability on each neighbor of x (a “default exploration”).
A controlled kernel P (· | x) might, at some states, assign higher probability to neighbors leading
toward a goal region. The definition is useful because it isolates the central wu wei contrast: instead
of choosing arbitrary dynamics from scratch, we measure how far the controlled choice departs from
the passive baseline.
Remark 1472. In graph terms, P0 encodes the geometry and friction of the environment: which
moves are “easy” (high passive probability) and which are “unnatural” (low or zero passive proba-
bility). This becomes important later because the KL penalty makes it extremely expensive (indeed
impossible at finite cost) to assign positive probability to transitions that are impossible under the
passive flow, so the passive dynamics functions as a feasibility scaffold as well as an effort prior.
Definition 436 (Forcing cost as divergence from the passive flow). Fix a scale parameter λ > 0.
The forcing cost at state x for using a controlled kernel P (· | x) is
                                                                            
                          Forceλ (P k P0 )(x) := λ KL P (· | x) k P0 (· | x) .             (26)

We interpret this as resistance/effort: it is zero when we “go with the flow” (P = P0 ) and grows
as we push the dynamics away from its natural tendencies.

                                                 577
Remark 1473. Here KL(·k·) denotes the Kullback–Leibler divergence: for two distributions P, Q ∈
∆(X) with P absolutely continuous with respect to Q,
                                                   X                     P (x0 )
                                    KL(P kQ) =             P (x0 ) log           .
                                                                         Q(x0 )
                                                   x0 ∈X

It is always ≥ 0 and is 0 exactly when P = Q. The parameter λ is a unit/scale parameter that
determines how expensive it is to deviate from the passive flow: large λ means “forcing is costly,”
so wu wei strongly prefers near-passive behavior; small λ makes deviation cheap. This KL-based
penalty is a standard information-geometric way to quantify effort-to-resist [16, 21].

Remark 1474. Two additional facts about KL(P kQ) matter for the wu wei reading. First, it is
asymmetric: steering away from P0 is penalized according to how surprising the controlled flow
would look to an observer who expects P0 . Second, the absolute continuity condition (P must not
put mass outside the support of P0 ) formalizes a kind of “non-violent” constraint: one cannot, at
finite forcing cost, demand transitions that the passive dynamics regards as impossible. In many
physical settings this corresponds to respecting hard constraints (walls, forbidden moves), while still
allowing soft steering among feasible moves.

Remark 1475. As a concrete example, suppose from a state x the passive kernel assigns P0 (· |
x) = (1/2, 1/2) on two successors. If the controller changes this to (3/4, 1/4), the forcing cost is
positive but moderate; if it changes to (1, 0), the forcing cost becomes larger (and in fact infinite if
P0 assigns zero mass where P assigns positive mass). This captures the wu wei intuition that “hard
commitment” is a kind of strain when it contradicts what the passive dynamics naturally supports.

Remark 1476. The dependence on λ can also be read in this example: the same change from
(1/2, 1/2) to (3/4, 1/4) is interpreted as “mild effort” when λ is small and as “significant effort”
when λ is large. Thus λ mediates a tradeoff between task achievement and non-interference: it
acts like a temperature parameter, where high temperature (small λ) permits sharper tilting of
probabilities, while low temperature (large λ) keeps the controlled kernel close to the passive one.

Definition 437 (Task cost and total objective). Let q : X → R be a bounded state cost (negative
reward). Given initial state distribution ρ0 ∈ ∆(X) and horizon T ∈ N, define
                                      −1
                                    hTX                                              i
                                                                          
                      JT (π) := E          q(xt ) + Forceλ (Pπ k P0 )(xt ) + qT (xT ) ,            (27)
                                     t=0

where x0 ∼ ρ0 , xt+1 ∼ Pπ (· | xt ), and qT is a terminal cost. A wu wei policy for this problem is
any minimizer
                                         π ∗ ∈ arg min JT (π).
                                                      π

Remark 1477. The assumption that q is bounded ensures, in particular, that the task part of
the objective does not by itself create divergences in the finite-horizon expectation. Any remaining
possibility of infinite cost typically comes from the forcing term (via support mismatch), which
is conceptually appropriate: if one tries to “force” transitions not permitted by P0 , the penalty
becomes prohibitive. The terminal cost qT is included to model goals that are evaluated at the end
of the horizon (e.g., “be in a target set at time T ”), and it also supports dynamic-programming
formulations where boundary conditions are naturally expressed at t = T .



                                                     578
Remark 1478. The objective JT (π) combines two desiderata in a single expectation E[·] over
trajectories: (i) we want to avoid high-cost states (small q if thinking in rewards, or small negative
reward if thinking in costs), and (ii) we want to avoid “fighting” the passive dynamics, quantified
by Forceλ . The random variables x0 , x1 , . . . , xT are generated by first drawing x0 from the initial
distribution ρ0 and then propagating forward according to the controlled kernel selected by π at each
visited state.

Remark 1479. Although the policy is defined as stationary (state-dependent but not time-dependent),
the finite-horizon criterion still makes sense: one may either restrict attention to stationary poli-
cies for conceptual simplicity, or later allow nonstationary πt when emphasizing optimality for each
remaining time-to-go. In linearly-solvable and KL-regularized control, the stationary restriction is
often adopted because the optimal kernels can be expressed as statewise tilts of P0 (· | x) by func-
tions of successor-state “desirability,” and these tilts have a consistent form across time in the
time-homogeneous case.

Remark 1480. A simple example is navigation with stochastic drift: q(x) is large in dangerous
regions and small near the target; P0 models wind/current drift; Pπ models the effect of steering. A
wu wei policy is then one that reaches the target while (in expectation) expending minimal forcing
against the drift. This definition is necessary for the later claims about “exponential tilting” and
“linear solvability”: the KL-regularized form is exactly what makes the optimization admit closed-
form local solutions and linear recursions.

Remark 1481. It is also useful to notice that the forcing cost is state-local while the task cost is
trajectory-coupled through the state evolution. This is precisely the structure that allows one to
write Bellman-style recursions: the immediate cost at xt is q(xt ) + λ KL(Pπ (· | xt )kP0 (· | xt )), and
the future cost depends on the chosen next-state distribution. When one minimizes over P (· | x), the
KL term acts as a convex regularizer, leading (under standard assumptions) to a unique minimizing
controlled kernel at each state given an appropriate value-to-go function.

Remark 1482 (Where weakness enters). The forcing term is an information-geometric penalty.
To connect it to the paper’s weakness theme, interpret P0 as the dynamics induced by a weak
model (a maximally general representation that makes few distinctions), while Pπ is the refined,
task-specific dynamics requiring extra distinctions. Minimizing KL(Pπ kP0 ) is then a precise form
of minimum representational effort: do not add distinctions unless they buy real task value.

Remark 1483. This connection can be made even more explicit by reading a controlled kernel
Pπ (· | x) as an “annotated” version of the passive kernel: it reallocates probability mass among
successor states, thereby encoding which distinctions among successors are behaviorally relevant. If
the weak model P0 already concentrates on a small set of plausible next states, then steering within
that set can be cheap, while insisting on a qualitatively different move (outside the passive support)
corresponds to introducing a distinction the weak model does not even represent. In this sense,
wu wei control implements a disciplined refinement of the weak baseline: it intervenes only to the
extent that intervention is justified by the task cost.

Remark 1484. This remark is pointing at Hyperseed-Concept 143 and Hyperseed-Concept 202. In
the weakness-centered view [3, 2], a “strong” model draws sharper boundaries and therefore supports
more specialized, more brittle interventions. The wu wei objective says: sharpen boundaries only
where the task truly compels it, and otherwise remain close to the weak/default dynamics. Thus
what looks like an external control regularizer can also be read as an internal epistemic ethic:
avoid gratuitous distinctions. One can also read this as a warning about self-induced overfitting

                                                  579
of agency: if the controller commits to distinctions not demanded by the objective, it pays an
avoidable “maintenance cost” in the form of higher sensitivity to mismatch between model and
world. In that sense, the KL penalty is not merely a numerical convenience but a formal way to
encode the preference that intervention should be locally justified by task-relevant gradients rather
than by the availability of controllable degrees of freedom.

26.2    A one-step wu wei principle: exponential tilting
The forcing regularizer has a canonical optimization consequence: optimal control is achieved by
tilting the passive dynamics by an exponential of negative cost. Equivalently, the controller chooses
the least-informative (closest-to-passive) distribution that still achieves an improved expected cost,
where “least informative” is measured in the KL geometry induced by the passive kernel. This is the
same variational template that appears in maximum-entropy inference: an energy term (expected
cost) plus an entropic or divergence-based regularizer yields a Gibbs/Boltzmann form.

Proposition 45 (Gibbs form for minimal forcing). Fix a state x ∈ X, a passive distribution
P0 (· | x) with full support, and an immediate cost function c : X → R. Consider the one-step
optimization problem
                                 n                                                 o
                          min     Ex0 ∼P (·|x) [c(x0 )] + λ KL P (· | x)kP0 (· | x) .    (28)
                      P (·|x)∈∆(X)

Then the unique minimizer is

                  P0 (x0 | x) exp −c(x0 )/λ
                                              
                                                                   X
   P ∗ (x0 | x) =
                                                                                               
                                                  with    Z(x) =         P0 (y | x) exp −c(y)/λ .   (29)
                              Z(x)
                                                                   y∈X

Remark 1485. In plain terms, the proposition says: if you pay a cost both for “going to expensive
next states” and for “departing from the default distribution,” then the optimal way to choose your
next-state distribution is to take the default P0 (· | x) and reweight it by an exponential preference
for low cost. The normalization constant Z(x) (often called a partition function) is just what
makes the reweighted numbers sum to 1 again. It is useful to notice that the exponential weight
is relative: what matters is not the absolute scale of c but its scale compared to λ. For example,
adding a constant to c(·) does not change the minimizer, because it factors out of the numerator
and is cancelled by the same factor in Z(x); only cost differences across next states affect the tilt.

Remark 1486. A further quantitative reading is that −λ log Z(x) is a “soft minimum” of c under
the passive distribution. Indeed, Z(x) is a log-sum-exp moment of −c/λ under P0 (· | x), so log Z(x)
plays the role of a cumulant-generating function and interpolates between averaging and minimizing
as λ varies. This is one of the reasons λ is often called a temperature: high temperature smooths
preferences and low temperature sharpens them. In control terms, this makes explicit how the wu
wei regularizer controls the curvature (and therefore brittleness) of the effective objective landscape
over actions/policies.

Remark 1487. This is important because it is one of the rare places in control theory where a
constrained optimization over the whole simplex yields an explicit, closed-form answer. It connects
directly to later results in this section: the multi-step “linear desirability recursion” is essentially
this one-step tilt applied repeatedly inside dynamic programming. It also connects to the broader
Hyperseed theme that “soft” (quantitative, graded) commitments are often the right formalization
of non-forcing behavior. A second reason it matters is methodological: having an explicit optimizer


                                                   580
makes it possible to reason about limits (λ → 0 and λ → ∞), sensitivity (how P ∗ changes as c
changes), and compositionality (how local tilts combine across time) without appealing to generic
existence theorems or black-box numerical solvers.

Remark 1488. One can also explicitly write the optimal objective value by substituting P ∗ back
into the functional. A standard calculation yields
                                  n                      o
                           min      EP [c] + λ KL(P kP0 ) = −λ log Z(x),
                         P (·|x)∈∆(X)

so the partition function is not merely a normalization device: it is the quantity that summarizes
the best achievable cost–forcing tradeoff at state x. This identity is the one-step version of the “free
energy” variational principle, and it is the algebraic reason that log-partition functions recur when
one passes from one-step control to multi-step value functions.

Proof. The objective is strictly convex in P because KL(·kP0 ) is strictly convex P on the simplex
when P0 has full support. Introduce a Lagrange multiplier α for the constraint x0 P (x0 | x) = 1.
Differentiating the Lagrangian with respect to P (x0 | x) and setting to zero yields

                         c(x0 ) + λ log(P (x0 | x)/P0 (x0 | x)) + 1 + α = 0.
                                                                   


Solving gives P (x0 | x) ∝ P0 (x0 | x) exp(−c(x0 )/λ), with the proportionality constant fixed by nor-
malization. Strict convexity implies uniqueness. Because P0 (· | x) has full support, the stationarity
condition is valid at an interior point of the simplex and the optimizer does not need to place exact
zeros in order to be feasible; instead, it can trade off small probabilities continuously against the
KL penalty. This interiority is what makes the Euler–Lagrange (first-order) condition sufficient
here, rather than merely necessary.

Remark 1489. A useful way to read the proof is: KL divergence is the “right” strictly convex
barrier on the simplex that makes the calculus work cleanly. The Lagrange multiplier step encodes
the single essential constraint (probabilities sum to 1), and the derivative calculation produces a
logarithm, which is why the solution comes out exponential. The full-support assumption on P0
ensures the logarithm is well-defined and enforces uniqueness. Another way to say the same thing
is that KL(P kP0 ) supplies a Legendre-type duality between log-partition functions and moment con-
straints: exponential families are the natural coordinates in which the tradeoff between expected cost
and informational deviation becomes linear. This is why the same mathematical move appears in
both “soft” control and in maximum-entropy inference: the optimizer lives in an exponential family
anchored at the reference measure P0 (· | x).

Proof sketch. The strategy is to minimize a strictly convex functional on a compact convex set
(the simplex), so there is a unique minimizer characterized by first-order optimality. One writes
the Lagrangian with a normalization constraint and solves the resulting stationarity condition,
which yields an exponential reweighting of the passive distribution. In particular, the stationarity
condition forces log P to differ from log P0 by an affine function of c, and exponentiating converts
that affine relation into multiplicative reweighting.                                             

Remark 1490. Geometrically (in information geometry), this minimizer can be viewed as the
closest distribution to P0 (in KL sense) among those that achieve the desired reduction in expected
cost. The “tilt” is not an arbitrary trick: it is the canonical way to trade off expectation constraints
against divergence penalties, and it recurs throughout variational formulations of inference and
control [21]. More precisely, the level sets of expected cost are affine slices of the simplex, while

                                                  581
the KL divergence supplies a strictly convex “distance-like” function; the optimizer is therefore the
unique point where a KL ball around P0 first becomes tangent to a cost level set. This tangency
picture also makes the role of λ intuitive: increasing λ inflates the effective penalty on moving away
from P0 , so the tangency occurs closer to P0 .

Remark 1491 (Interpretation). The passive kernel supplies a default motion. The exponen-
tial tilt supplies a soft bias toward lower-cost next states. As λ → ∞ the policy approaches the
passive dynamics (high acceptance / low forcing). As λ → 0 the policy concentrates on argmin
states (high forcing, potentially brittle). Wu wei is not “do nothing” but rather “bias gently unless
strongly necessary.” A further operational reading is that λ governs how much evidence (in the
form of expected-cost improvement) is required to justify deviating from the default. Large λ de-
mands strong, persistent cost advantages before it will significantly reallocate probability mass, while
small λ makes the controller “decisive” in the sense of rapidly collapsing onto whichever next state
currently looks best. In applications, this means that wu wei regularization can be used to tune not
only average performance but also mode of failure: softer tilts tend to fail gracefully (by remaining
near baseline behavior under uncertainty), whereas harder tilts can fail catastrophically if the cost
model is misspecified.

26.3    Multi-step wu wei control and linear solvability
The same structure persists over many steps and yields a particularly clean dynamic programming
recursion.

Definition 438 (Finite-horizon value function). Define the optimal cost-to-go
                                   −1
                                 hTX                                                       i
                                                                       
               Vt (x) := inf E          q(xs ) + Forceλ (Pπ k P0 )(xs ) + qT (xT )   xt = x .      (30)
                         π
                                  s=t

Set VT (x) := qT (x).

Remark 1492. The value function Vt (x) is the standard dynamic programming object: it com-
presses all future consequences of optimal behavior from time t onward, given that we are currently
at state x. The conditioning “ xt = x” means we evaluate the expected future cost assuming the
current state is fixed to x. This definition is useful because it allows the global trajectory optimiza-
tion problem to be solved recursively (Bellman’s principle), and it is precisely this recursion that
becomes linear after a change of variables.

Remark 1493. As an example, if T = 1 then V0 (x) is exactly the one-step objective minimized
in Proposition 45 (up to the addition of the immediate q(x) term and terminal cost). For larger
horizons, Vt stitches together many such one-step optimizations, with the crucial twist that the
“immediate cost” in the tilt becomes the next-step value Vt+1 .

Theorem 24 (Linear recursion in desirability variables). Assume P0 (· | x) has full support for all
x. Define the desirability variables
                                                        
                                 zt (x) := exp −Vt (x)/λ ∈ (0, ∞).                            (31)

Then the Bellman optimality equations are equivalent to the linear recursion
                                              X
                        zt (x) = exp −q(x)/λ        P0 (x0 | x) zt+1 (x0 ).                        (32)
                                                       x0 ∈X


                                                      582
Moreover, the optimal controlled kernel at time t is
                                                  P0 (x0 | x) zt+1 (x0 )
                                 Pt∗ (x0 | x) = P                         .                       (33)
                                                  y∈X P0 (y | x) zt+1 (y)
Remark 1494. The theorem says that, for this particular KL-regularized control problem, dynamic
programming becomes almost suspiciously simple: if one exponentiates (with scale λ) the negative
value function, the nonlinear Bellman minimization turns into a linear update of the transformed
quantity zt . In other words, the “difficulty” of optimal control has been moved into a change of
variables, after which the recursion resembles a passive expectation under P0 .
Remark 1495. This result matters because linear recursions are algorithmically and conceptually
easier than nonlinear ones: they admit superposition, can be estimated by sampling, and connect
directly to spectral methods. Within this section, it is the multi-step counterpart of Proposition 45;
within the larger Hyperseed development, it supports the claim that “minimal forcing” yields a kind
of computational grace: one does not merely suffer less, one often computes more cleanly. This
“linear solvability” viewpoint is also part of the motivation for connecting wu wei to “geodesics”
and “fluid flow” later [21].
Proof. Start from the Bellman equation
                                         n                                     o
                      Vt (x) = q(x) + min λ KL(P kP0 )(x) + Ex0 ∼P [Vt+1 (x0 )]
                                       P (·|x)

Apply Proposition 45 with c(x0 ) := Vt+1 (x0 ). The minimizing kernel satisfies Pt∗ (x0 | x) ∝ P0 (x0 |
x) exp(−Vt+1 (x0 )/λ) = P0 (x0 | x) zt+1 (x0 ). The minimal value of the inner optimization is
                     X                                          X                       
            −λ log        P0 (x0 | x) exp(−Vt+1 (x0 )/λ) = −λ log    P0 (x0 | x) zt+1 (x0 ) .
                     x0                                                  x0
Thus                                                 X                          
                             Vt (x) = q(x) − λ log         P0 (x0 | x) zt+1 (x0 ) .
                                                      x0
Exponentiating −Vt /λ gives the stated linear recursion.
Remark 1496. The proof is essentially “plug Proposition 45 into Bellman recursion.” The key
move is recognizing that the Bellman minimization over P (· | x) has exactly the same KL-regularized
form as the one-step problem, with Vt+1 playing the role of the one-step cost. Once this is seen,
everything becomes algebra: the minimizer is an exponential tilt, the minimized value is a log-
partition term, and exponentiating cancels the logarithm and produces linearity.
Proof sketch. One first writes Bellman’s equation for Vt and notices that the inner minimization is
the one-step KL-regularized optimization from Proposition 45. The minimizer is therefore a Gibbs
tilt by exp(−Vt+1 /λ), and the minimized objective becomes a negative log of a passive expectation.
Finally, defining zt = exp(−Vt /λ) converts the log-sum-exp into a linear sum.                   
Remark 1497. A visual intuition is to imagine a “field” over states whose height is Vt (x); expo-
nentiating turns steep cliffs into near-zero desirabilities. Then the update for zt says: propagate
desirability backward by averaging future desirability under the passive dynamics, while discounting
by immediate state cost. This is the sense in which wu wei control can look like “letting passive
trajectories vote,” rather than issuing a single deterministic command.
Remark 1498 (Wu wei as “path integral control”). The recursion for zt expresses desirability as
a passive expectation of exponentiated negative cost. This makes explicit a wu wei reading: instead
of forcing a single hard plan, we compute a soft “desirability field” and let the passive dynamics
flow through it. Algorithmically, this often yields efficient estimation by Monte Carlo sampling.

                                                     583