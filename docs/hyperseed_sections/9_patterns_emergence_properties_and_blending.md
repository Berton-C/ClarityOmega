# 9 Patterns, emergence, properties, and blending

Definition 80 (Resistance and submission (minimal operationalization)). For a directed policy
change H → H 0 in context C:
• Resistance is identified with ∆Eff C (H → H 0 ).

• Submission (in this minimal operationalization) occurs when the system follows a policy update
  that does not increase required effort, i.e. when ∆Eff C (H → H 0 ) = 0.
Remark 320. Intuition. Resistance (Hyperseed-Concept 158) is treated here as the “extra effort
demanded” by a change, and submission (Hyperseed-Concept 183) as the special case where no
extra effort is demanded. This minimal reading is intentionally behavioristic: it does not claim to
capture the whole phenomenology of resistance, only an invariant that can be transported into later
mathematics. In particular, it separates (i) the direction of a policy update in the lattice/order of
distinctions from (ii) the load required to implement that update for a given observer in context C.
Remark 321. Examples. If a system is asked to refine its model (closing) and this requires
additional computation, memory, or sensing, then ∆Eff C > 0 and the change is resisted in this
operational sense. If it is asked to simplify (opening) and this reduces constraints, then ∆Eff C = 0
and the change is “submitted to” without additional load. In later dynamical models, opening may
also incur cost because simplifying can break internal commitments (learned habits), leading to
nonzero resistance even for openings. One can also interpret ∆Eff C (H → H 0 ) as an activation
barrier: the policy H 0 might be globally “simpler” than H in a static sense, yet transitioning to it
can still be difficult if the model is extended to include switching/rewiring costs not captured by the
static Eff C alone.
Remark 322. Why this definition matters. One can view this as a precise analogue of a
thermodynamic gradient: forcing a system into a more constrained configuration costs work, and
that “work” is what resistance measures. This resonates with the “least-effort” orientation in [21]
while staying purely formal and observer-indexed. The analogy is structural rather than literal: Eff C
is not assumed to be physical energy, but it plays the same mathematical role of a potential whose
increases quantify the minimal additional “input” required to sustain tighter constraints.
Remark 323. Hyperseed’s phenomenological language distinguishes several kinds of resistance/submission
(somatic, cognitive, affective, spiritual). The formalization above is deliberately thin: it isolates a
single load-bearing invariant that will matter throughout the ontology: tightening distinctions is
effort-consuming. Later sections add dynamical structure to represent different “channels” of resis-
tance. The point of starting thin is that the ontology can then refine (rather than revise) the concept:
richer models may decompose Eff C into multiple terms (e.g. sensing vs. inference vs. memory), but
antitonicity and the resulting operational meaning of ∆Eff C remain stable.

8.4   Simplicity as minimum representational effort
Hyperseed’s simplicity is observer-relative and task-relative: an object is simple for an observer
if it can be handled (represented, predicted, manipulated) with low effort. This framing treats
“simplicity” not as an intrinsic geometric or syntactic attribute of x, but as a property of the best
interface an observer can construct between x and the demands of context C. In particular, what
counts as “handling” can vary: the same x may be easy to store but hard to simulate, easy to
predict but hard to control, etc., and these differences are absorbed into the choice of admissible
representations and the effort functional.
     We therefore define simplicity as an infimum over representations. The use of an infimum
(rather than, say, an arbitrary chosen representation) emphasizes that simplicity is an optimal

                                                 157
notion: sC (x) records the best achievable effort among all admissible representational strategies
in C. It also allows that the “best” representation may be approached only in the limit (e.g., by
increasingly refined approximations), which is often the realistic case in continuous or resource-
bounded settings.

Definition 81 (Representations and representational effort). Fix a context C and a domain of
items XC (entities, states, experiences, or patterns). Let RC (x) denote the set of admissible repre-
sentations of x ∈ XC . Assume an effort assignment Eff C on representations. Define the (subjec-
tive) simplicity of x in context C by

                                 sC (x) := inf{Eff C (r) : r ∈ RC (x)}.

Remark 324. Notation unpacking. Here RC (x) is a set (possibly large) of alternative repre-
sentations r that “stand for” x in context C. The functional Eff C (r) measures the cost of using
representation r (storage, computation, inference, sensing, etc.). The infimum inf is taken in the
ordinary real order: sC (x) is the best (least costly) representation effort available. When RC (x) is
rich, it is helpful to read “r ∈ RC (x)” as encoding both an encoding language (what forms rep-
resentations may take) and a set of acceptability constraints (what counts as representing x well
enough for the purposes of C).

Remark 325. Intuition. This definition turns “simplicity” into a controlled form of compression:
x is simple if there exists a cheap way to represent it. The philosophy is close in spirit to algorith-
mic information theory—the object is “simple” if it has a short description—but we have replaced
“short” with a general observer-dependent effort measure. This observer-relativity is central in Hy-
perseed (Hyperseed-Concept 169) and aligns with the broader pattern/emergence approach in [5].
One can also view sC (x) as a generalized “minimum description length” objective in which descrip-
tion length, compute time, energy, bandwidth, or even required sensor acuity may all contribute to
effort, depending on what the context regards as scarce.

Remark 326. Examples. A circle is simple for a context that has the concept “circle” and can
store “center + radius” cheaply; it may be complex for a context that can only store point clouds.
A large integer like 10100 is simple for a context that allows exponent notation, and less simple for
a context that requires explicit decimal expansion. Similarly, a periodic signal may be simple for a
context that admits Fourier representations (a few coefficients) but complex for a context restricted
to raw time-series samples; conversely, a sharply localized transient may be cheaper as a sparse
time-domain description than as a global frequency expansion.

Remark 327. Why useful. By making simplicity an infimum, we obtain a quantity that behaves
well under optimization and can be compared across tasks once adequacy constraints are imposed.
This is also the mathematical doorway through which patterns will enter in Section 9: a pattern
is, roughly, a representation whose effort is much smaller than some baseline. In practice, this
invites a two-part modeling stance: first choose what counts as an admissible representation (the
hypothesis class, the interface, the “vocabulary”), then measure the best achievable effort within
that class. Changing RC (x) (e.g., by adding a new representational primitive) can strictly decrease
sC (x), formalizing the idea that learning new concepts can make previously complex items simple.

Remark 328. Low sC (x) means “x is simple for C.” Different contexts yield different simplicity
orderings. This formalizes the Hyperseed claim that simplicity is not an absolute property of the
world but is indexed by an observer’s capacities and goals. In particular, if two contexts C and
C 0 differ only by resource budgets (time, memory, precision), then sC (x) can be interpreted as a

                                                  158
context-indexed “resource complexity” of x. Also note that, depending on conventions, it is natural
to allow sC (x) = +∞ when no admissible representation exists (e.g., RC (x) = ∅ or all candidates
have unbounded effort), which captures the possibility that some items are effectively unhandleable
in a given context.

8.5   Simplicity as weakness: the dual perspective
Section 3.7 defined a quantale-valued weakness w(H) for an indistinction policy H: weakness
increases as more (and/or more important) distinctions are collapsed (Hyperseed-Concepts 202, 143;
see also [3, 2] for related motivation). This provides an algebraic dual to effort-based simplicity. In
particular, it lets us speak about “being simpler” either in an operational sense (less work is required
to maintain fine-grained distinctions) or in a semantic/informational sense (fewer distinctions are
being asserted at all). The point of introducing w is that the latter can be aggregated and compared
even when an explicit effort model is unavailable or context-dependent.
    The key relation is monotonic: opening decreases effort and increases weakness, while closing
increases effort and decreases weakness. Here “opening” is the order-theoretic operation of enlarging
H by adding more pairs declared indistinct, i.e. moving upward in the inclusion order on HC ;
“closing” is the reverse movement. Because both w and Eff C are defined as order-respecting
maps (but in opposite directions), this monotonicity is not an extra axiom: it is the compatibility
condition that makes the two notions of simplicity track the same qualitative phenomenon. We
record the abstract monotonic facts as a sanity theorem, to be used later.

Theorem 7 (Effort–weakness monotonicity). Fix a context C with admissible indistinction policies
HC . Assume:

1. w : HC → V is monotone with respect to inclusion (as in Theorem 1 specialized to C),

2. Eff C : HC → [0, ∞] is antitone with respect to inclusion (Definition 79).

Then for any H ⊆ H 0 in HC we have

                          w(H) ≤ w(H 0 )      and       Eff C (H) ≥ Eff C (H 0 ).

Thus opening simultaneously increases weakness and decreases effort. Equivalently, along any in-
clusion chain
                                      H0 ⊆ H1 ⊆ · · · ⊆ Hn ,
                    n                                                           n
the sequence w(Hi ) i=0 is nondecreasing in the quantale order, while Eff C (Hi ) i=0 is nonincreas-
ing in the usual order on [0, ∞].

Remark 329. What this says, in plain language. If you merge more cases together (open
the policy), then you become “weaker” in the precise quantale sense (you assert fewer distinctions),
and you also do not have to spend more effort maintaining distinctions. This theorem is not deep;
its value is that it makes the duality between two kinds of “simplicity talk” explicit and checkable.
In particular, it rules out the pathological possibility that a policy could be simultaneously “more
indiscriminate” (collapsing distinctions) and yet require strictly more effort to implement, or vice
versa, at least at the level of the abstract order-theoretic interface.

Remark 330. Why it matters. Later sections will compose policies across subsystems and
contexts. Weakness is designed to compose well (quantale aggregation), while effort is designed to
support minimization. This theorem is the hinge connecting those two calculi: it guarantees that


                                                  159
one is not optimizing a quantity that behaves perversely with respect to the other. A typical use
is: if a construction (composition, relaxation, marginalization) is known to correspond to opening
in HC , then one immediately gets a one-line comparison statement for both w and Eff C without
unpacking their internal definitions in that particular setting.

Remark 331. Connection to the rest of the document. In Section 9, pattern intensity is
defined by comparing effort (or weakness) before and after a representational move. In that setting,
one often wants to reason with whichever quantity composes more conveniently; the monotonic
relation here lets one translate qualitative conclusions across the two viewpoints. For example, if
a representational move is shown (by construction) to only ever open the operative policy, then it
cannot increase effort; if instead it is shown to strictly close the policy, then it cannot decrease weak-
ness. These translations are intentionally “direction-only”: they preserve the sign of comparisons
even when the magnitudes live in different codomains (V versus [0, ∞]).

Proof. The weakness inequality is exactly monotonicity of w under adding undistinguished pairs.
The effort inequality is the assumed antitonicity of Eff C . One can also view the statement as the
conjunction of two functoriality properties: w is order-preserving and Eff C is order-reversing on
the poset (HC , ⊆).

Proof sketch. The argument is purely definitional: “opening” means H ⊆ H 0 . Monotonicity of
weakness turns inclusion into w(H) ≤ w(H 0 ), while antitonicity of effort turns the same inclusion
into Eff C (H) ≥ Eff C (H 0 ). There is no hidden construction; the point is to record that the intended
phenomenological directionality has been built into the formalism. A useful way to remember the
variance is: weakness measures what you give up by collapsing distinctions, so it grows when you
add collapses; effort measures what you must supply to maintain distinctions, so it shrinks when
you stop maintaining them.                                                                             

Remark 332. A useful image is to imagine a knob controlling perceptual or conceptual resolu-
tion. Turning the knob toward coarser resolution corresponds to opening: more things look the
same. Weakness increases (more indistinction), and effort decreases (less computation/attention).
Turning the knob toward finer resolution corresponds to closing: more things must be told apart,
which costs effort. At the extremes, the fully open end of the knob corresponds to a maximally in-
discriminate policy (everything relevant is treated as the same), which should intuitively have high
weakness and low effort; the fully closed end corresponds to a maximally discriminating policy (no
additional identifications beyond those forced by admissibility), which should have low weakness and
high effort. The theorem does not assume such extrema exist in HC , but whenever they do, the
inequalities specialize to immediate upper/lower bounds.

Remark 333. Order conventions and interpretability. The inequality w(H) ≤ w(H 0 ) is
taken in the intrinsic order of the quantale V . In many concrete quantales used for aggregation
(e.g. ([0, ∞], ≥, +, 0) with the reverse order, or a powerset quantale ordered by inclusion), it is worth
checking once which direction corresponds to “more severe” weakness. The present statement fixes
that convention by insisting that opening corresponds to increasing weakness in the chosen order;
all later comparisons inherit this convention. Similarly, the effort inequality uses the standard order
on [0, ∞], so “decreases effort” always means “numerically no larger.”

Corollary 1 (No free lunch in both directions). If H ⊆ H 0 and w(H 0 ) < w(H) (strictly, in the order
of V ), then such a pair cannot occur under the stated assumptions; likewise, if Eff C (H 0 ) > Eff C (H),
then H ⊆ H 0 cannot hold. In other words, under opening one cannot simultaneously get strictly
less weakness, nor strictly more effort.

                                                   160
8.6   Minimum representational effort as constrained weakness maximization
In applications, an observer typically cannot open indefinitely: too much collapsing of distinctions
destroys predictive power and control. Hyperseed’s “minimum representational effort” principle is
therefore a constrained minimization: among all policies/representations that are adequate for a
task, prefer those requiring the least effort (cf. [2, 19] for related design principles). In particular,
the “constraint” is not an incidental add-on: it is the mathematical device that prevents the trivial
solution “represent nothing” (or “distinguish nothing”) from being optimal.

Definition 82 (Task constraint and feasible policy set). Let a task constraint in context C be a
predicate AdeqC (H) ∈ {true, false} meaning: “policy H is adequate for the task (prediction/control
objective)”. Define the feasible set

                                    FC := {H ∈ HC : AdeqC (H)}.

Remark 334. Intuition. The predicate AdeqC (H) is where “what the observer is trying to do”
enters. Without it, the cheapest policy would typically be the maximally open one (collapse every-
thing), which is useless for prediction/control. Adequacy formalizes the idea that some distinctions
are not optional because the task depends on them (Hyperseed-Concept 186).

Remark 335. Examples. If the task is to predict whether a system will fail, then collapsing
distinctions that separate failure states from non-failure states makes the policy inadequate. If the
task is image classification among a small set of labels, then distinctions within each label class may
be safely collapsed without harming adequacy.

Remark 336. Why needed. This definition isolates a general optimization shape that will recur
in more elaborate guises (Pareto frontiers, tradeoff theorems, multi-objective feasibility). It is the
formal core of what the Hyperseed overview treats as “do not spend representational effort unless
you must” [1].

Remark 337. Well-posedness. The feasible set FC can be empty if the task is impossible under
the observer’s available policy class HC (or if the adequacy predicate is too strict). In that case
the principle in Definition 83 becomes a diagnosis: either enlarge HC (more expressive policies),
weaken/relax AdeqC (approximate adequacy, probabilistic success, slack constraints), or change the
task/context C. This mirrors practical learning systems where “no model fits” is handled by revising
the hypothesis class or by moving from hard constraints to soft penalties.

Definition 83 (Minimum representational effort principle). An observer in context C satisfies
minimum representational effort if it preferentially selects

                                       H ∗ ∈ arg min Eff C (H).
                                                 H∈FC

Remark 338. Intuition. Among all adequate policies, choose the one that costs the least effort to
maintain/compute. This is a cognitive analogue of an Occam-style constraint, but framed in terms
of the observer’s actual expenditures rather than a language-invariant notion of description length.

Remark 339. Example. Suppose two policies are adequate for a classification task: one distin-
guishes 1,000 fine-grained categories and then maps them to labels, while the other distinguishes
only the labels directly. The minimum representational effort principle picks the latter, provided
both are adequate for the actual objective.


                                                  161
Remark 340. Usefulness. This principle provides a normative and (later) dynamical bias: it
tells us which policies are preferred in equilibrium, and it suggests learning dynamics that drift
toward lower effort subject to constraints. Such dynamics are central in cognitive architectures that
explicitly manage resource tradeoffs [19].

Remark 341. This is a formalization of a central Hyperseed slogan: “simplicity is what costs less
effort.” Note that “adequacy” may itself be paraconsistent, fuzzy, or multi-objective; the definition
above only assumes we can describe a feasible region.

Remark 342. Effort as an internal cost functional. The point of writing Eff C (H) rather than
a syntactic complexity measure is that effort can include costs that are not captured by descriptions
alone: latency, memory footprint, sampling cost, training instability, energy expenditure, or (in
embodied settings) sensor/actuator wear. Thus two extensionally equivalent policies (same input–
output behavior) may differ in effort because they are implemented differently in the observer. This
is also why the context subscript C matters: what is “cheap” depends on available hardware, priors,
and interaction regime.

    Under mild closure assumptions, minimum-effort selection is equivalent to selecting the maxi-
mally open adequate policy, hence the maximally weak adequate policy. Here “mild” is primarily
the assumption that adequacy is monotone with respect to opening, i.e., once the task can be done,
discarding additional distinctions that the task does not use will not break adequacy.

Theorem 8 (Maximally open adequate policy under upward closure). Assume FC is upward
closed under opening:
                        H ∈ FC and H ⊆ H 0 =⇒ H 0 ∈ FC .
Let                                                [
                                           H
                                           b :=          H.
                                                  H∈FC

Then:
   b ∈ FC ,
1. H

2. for all H ∈ FC , we have H ⊆ H,
                                b

                              b minimizes effort over FC ,
3. if Eff C is antitone, then H
                          b maximizes weakness over FC .
4. if w is monotone, then H

Remark 343. What this says, in plain language. If adequacy is preserved when you open
further (collapse extra distinctions that the task does not need), then there is a single “most open”
adequate policy: take the union of all adequate policies. This most open adequate policy is automat-
ically the least-effort one (because effort decreases under opening) and the most weak one (because
weakness increases under opening).

Remark 344. Why it is important. The theorem turns an optimization problem (minimize
effort subject to adequacy) into a purely order-theoretic construction (take a union). This is con-
ceptually valuable: it says that, in the upward-closed regime, the hard part is not optimization but
specifying adequacy correctly. It also foreshadows later fixed-point reasoning about stable policies
and goal systems (cf. [10] for a related fixed-point style in a different layer).



                                                  162
Remark 345. Connection to weakness. This theorem makes precise the slogan “minimum
effort equals maximum weakness subject to task constraints,” at least when FC is upward closed.
This is one of the main reasons weakness is useful: it can be maximized compositionally across
contexts, while effort is minimized.

Remark 346. Proof sketch (unpacking the order-theoretic steps). Item (2) holds by con-
struction: every H ∈ FC is a subset of the union of all such H. For item (1), pick any H0 ∈ FC
(when FC 6= ∅); then H0 ⊆ H,     b and by upward closure H    b ∈ FC . For item (3), antitonicity of
                     0                   0
Eff C means H ⊆ H implies Eff C (H ) ≤ Eff C (H), so combining H ⊆ H        b with antitonicity gives
Eff C (H) ≤ Eff C (H) for all feasible H. Item (4) is analogous: monotonicity of weakness means
       b
H ⊆ H 0 implies w(H) ≤ w(H 0 ), hence w(H) ≤ w(H)      b for all feasible H. The content is therefore
not a delicate inequality, but the existence of a greatest element (a maximal opening) in the feasible
set once it is upward closed.

Remark 347. When upward closure is reasonable (and when it can fail). Upward closure
is natural for tasks whose adequacy depends only on retaining certain necessary distinctions: if
a policy is adequate, then merging additional states that are irrelevant to the objective will keep
it adequate. It can fail for tasks where the representation itself must satisfy side-constraints that
are not monotone under opening (e.g., “must separately track two protected groups” or “must
retain a diagnostic variable for auditing”), or where opening changes action selection in a way that
violates a safety constraint even if prediction remains acceptable. In such cases, FC need not have
a single maximally open element, and minimum-effort selection may involve genuine optimization
over incomparable feasible policies rather than the union construction.

Remark 348. Interpretation in common representational formalisms. If policies corre-
spond to partitions (or σ-algebras) over a state space, “opening” corresponds to coarsening the
partition (forgetting distinctions). The union Hb then corresponds to the coarsest partition that is
still adequate: it merges every pair of states that can be merged without breaking the task. This
matches the informal idea of “keep exactly the distinctions the task forces you to keep” and discard
the rest.

Remark 349. Algorithmic reading. Although Theorem 8 is stated extensionally (via a union
over all feasible policies), it suggests an intensional procedure: repeatedly open (merge distinctions)
while checking adequacy, stopping only when any further opening would violate AdeqC . In learning
settings, this corresponds to a bias toward representational compression with constraint checks (or
constraint penalties), which is a common pattern in resource-bounded inference and control.

Proof. (1) Upward closure implies that since each H ∈ FC satisfies H ⊆ H,      b we have H  b ∈ FC . To
make the inclusion H   S ⊆ H explicit, recall that H is defined as the union of the feasible policies
                             b                        b
(in particular, H = G∈FC G), so every element of a given H ∈ FC is, by definition of union, an
                   b
element of H. b Thus H  b is an upper bound for FC in the inclusion order, and upward closure then
upgrades this pointwise upper-boundedness into feasibility of the upper bound itself.
     (2) Trivial from the definition of union. More concretely, if some relation/distinction/permission
         b then x ∈ H for at least one feasible H, and conversely any x ∈ H for a feasible H must
x is in H,
lie in H;
        b this is the sense in which H b aggregates all the “openings” present in any adequate policy.
     (3) If H ⊆ H and Eff C is antitone, then Eff C (H) ≥ Eff C (H)
                  b                                                 b for all H ∈ FC , so Hb is an effort
minimizer. Here antitone means that moving upward in (HC , ⊆) cannot increase effort: whenever
H ⊆ H 0 , one has Eff C (H) ≥ Eff C (H 0 ). Since every feasible H is below H,
                                                                            b the inequality specializes
to show that H achieves effort no larger than any other feasible candidate, i.e. it is a minimizer
                 b


                                                  163
over the feasible set. In particular, Hb is not merely locally improving along a chain; it is globally
extremal because it is a (feasible) top element among all feasible policies under inclusion.
    (4) If w is monotone and H ⊆ H   b then w(H) ≤ w(H)  b for all feasible H, hence H b is a weakness
maximizer. Monotonicity means weakness is aligned with openness: enlarging H (collapsing more
distinctions) cannot decrease w. Thus, because H  b contains every feasible H, it achieves weakness at
                                                     b realizes the maximum of w over FC provided
least as large as any feasible policy. Equivalently, H
FC is nonempty, and the argument shows that this maximum is witnessed by the same union object
that witnesses minimal effort under antitonicity.

Proof sketch. The strategy is to build a candidate policy that is “at least as open as any adequate
one,” namely the union H. b Intuitively, Hb is constructed by taking every permission/identification
that appears in some adequate policy and allowing it simultaneously; it is therefore the least restric-
tive object that still stays within the closure assumptions. Upward closure guarantees adequacy
is preserved when moving upward in the inclusion order, so H    b remains feasible. This step is the
only place where closure is used: without it, the union could overshoot the feasible region even if
each constituent policy is feasible. Then antitonicity/monotonicity convert the inclusion compar-
isons H ⊆ H b into the desired extremal properties for effort and weakness. In other words, once
H is known to be a feasible upper bound, order-respecting objective functions automatically turn
 b
that upper bound into an optimizer: antitone objectives favor higher elements, while monotone
objectives reward higher elements.                                                                   
Remark 350. A visual way to think of this is to picture the poset (HC , ⊆) as a landscape of
policies. The feasible region FC is a subset of this landscape. Upward closure means FC is a
“cone” pointing upward: once you are feasible, moving upward (opening) stays feasible. The union
Hb is then the apex of this cone. In order-theoretic terms, H
                                                            b functions as a greatest element (or at
least a canonical maximal element) of FC with respect to ⊆, because every feasible H lies below it.
This is why the optimization statements become essentially immediate: if the objective is compatible
with the order (antitone for effort, monotone for weakness), then an extremum is attained at such
an apex.
Remark 351. The upward-closure assumption formalizes a natural regime: if a policy is already
adequate, then collapsing additional distinctions that the task does not depend on remains adequate.
This corresponds to the intuition that adequacy depends only on preserving distinctions that matter
for C; any extra granularity is gratuitous and can be removed without harming performance. Later
sections refine this using pattern-intensity and emergence: adequacy can fail under excessive opening
because emergent patterns may disappear. In that refined regime, H    b may cease to be feasible, so
the existence of a single “most open adequate” policy is no longer guaranteed, and the extremal
argument must be replaced by a constrained optimum that balances these competing effects.

8.7   Compositional simplicity
Hyperseed insists that simplicity must be compositional to support a serious theory of pattern. We
formalize compositional simplicity in a way that is compatible with the effort-quantale viewpoint
and later categorical constructions.
Remark 352. Why “compositional” is a substantive constraint. A non-compositional
simplicity score can always be defined by fiat (e.g. “declare the objects we like to be simple”).
Requiring a recursive upper bound in terms of parts forces simplicity to be witnessable by an explicit
construction history, and thereby makes simplicity sensitive to the structure induced by the context
C (available building blocks, allowable compositions, and their overheads).

                                                 164
Definition 84 (Combination system and overhead). A combination system is a tuple (XC , ∗, e)
where:

• XC is a set of items in context C,

• ∗ : XC × XC → XC is a (not necessarily associative) combination operation,

• e ∈ XC is an identity-like element (when applicable).

An overhead is a function tC : XC × XC → [0, ∞] representing the extra effort needed to “glue” y
and z into y ∗ z.

Remark 353. On non-associativity. Allowing ∗ to be non-associative is not a technicality:
in many realistic contexts, (y ∗ z) ∗ w and y ∗ (z ∗ w) represent different assembly orders with
different intermediate artifacts and different integration burdens. The framework therefore treats a
decomposition as implicitly tree-shaped rather than simply set- or multiset-based, and later “parse
tree” viewpoints make this explicit.

Remark 354. On the role of e. The element e is included to support contexts where there is a
natural “do nothing” or “empty” item (empty string, empty program module, empty diagram, etc.).
When a true unit does not exist or is not meaningful, one can still include a distinguished baseline
element for which sC (e) = 0 expresses a normalization convention. This normalization prevents
degenerate admissible solutions obtained by shifting all costs down by a constant.

Remark 355. Intuition. A combination system abstracts the idea that complex items can be
built from simpler ones. The overhead tC (y, z) isolates the cost of composition itself: bookkeeping,
interface matching, coordination, translation between formats, etc. In cognitive terms, even if you
can represent y and z cheaply, combining them may require additional work (aligning contexts,
resolving conflicts, finding a common schema).

Remark 356. Examples. If ∗ is concatenation of strings, tC might be 0 (gluing is free). If ∗
is merging two knowledge graphs, tC may be substantial because entity alignment is nontrivial. If
∗ is composing two programs, tC can represent integration overhead such as type conversions or
interface code.

Remark 357. Usefulness. By making overhead explicit, we can distinguish “intrinsic simplicity”
of parts from “integration simplicity” of wholes. This becomes important when discussing emergence
and pattern: sometimes a whole is simple not because its parts are simple, but because there is a
low-overhead way to organize them.

Remark 358. Overhead as a contextual parameter. In practice, tC is often where the context
C enters most strongly. For example, the same pair of modules (y, z) may have small overhead in a
shared ecosystem (common protocols, shared ontologies) and large overhead across ecosystems. Thus
compositional simplicity is not intended to be an intrinsic property of an abstract object alone, but
of an object as situated in a particular representational and operational environment.

Definition 85 (Compositional simplicity functional). Let (XC , ∗, e) be a combination system with
overhead tC . A function sC : XC → [0, ∞] is compositionally admissible if:

1. sC (e) = 0,




                                                165
2. for all x ∈ XC ,                                                          
                               sC (x) ≤ inf       sC (y) + sC (z) + tC (y, z) ,
                                        y,z∈XC
                                         y∗z=x

   with the understanding that inf ∅ = ∞.
Define the compositional simplicity s∗C to be the least (pointwise) function satisfying these con-
straints.
Remark 359. Why an inequality (rather than equality). The admissibility condition requires
that sC (x) not exceed the best available two-part construction cost. This leaves room for x to be even
simpler for reasons not captured by binary decomposition alone (e.g. if x is deemed primitive, or
if x has a special direct representation not modeled as ∗-composition). Taking the least admissible
solution s∗C then eliminates arbitrary slack: any simplicity that cannot be justified by the recursive
constraints is removed.
Remark 360. The “no decomposition” case. If x cannot be expressed as y ∗ z for any pair
(y, z), then the right-hand side is inf ∅ = ∞, and the inequality becomes sC (x) ≤ ∞, i.e. imposes no
upper bound. This is deliberate: whether such an x should have finite simplicity is determined by
the global least-solution requirement, not by forcing every item to decompose. Consequently, items
can be treated as primitives in a given system (finite or infinite cost depending on what is consistent
with the rest of the constraints).
Remark 361. Notation unpacking. The set under the infimum is the set of all pairs (y, z)
that decompose x via the operation ∗. For each such decomposition, we assign a candidate cost
sC (y)+sC (z)+tC (y, z). Then we take the best (minimum) cost among decompositions, via inf. If x
has no decomposition at all (empty set), we set inf ∅ = ∞, meaning “cannot be built compositionally
(within this system)”.
Remark 362. Intuition. This is a Bellman-style optimality condition: the simplicity of a whole
should be no more than the best way to build it from parts, paying the simplicity of parts plus
integration overhead. Taking the least solution s∗C says we are not allowed to assign arbitrary low
costs; we want the smallest costs consistent with the recursive constraints. In effect, s∗C is “the cost
of the cheapest parse” of x.
Remark 363. Fixed-point viewpoint (effort-quantale compatibility). Define an operator F
on functions s : XC → [0, ∞] by setting F (s)(e) = 0 and, for x 6= e,
                                                                      
                            F (s)(x) = inf s(y) + s(z) + tC (y, z) ,
                                         y,z∈XC
                                          y∗z=x

interpreting inf ∅ = ∞ as above. Then compositionally admissible s are precisely (pointwise) post-
fixed points of F (i.e. s ≤ F (s)), and s∗C is the least post-fixed point. This framing matches the
quantale intuition: [0, ∞] with + and ≤ supports monotone recursion, and inf plays the role of
taking best achievable effort among alternatives.
Remark 364. On existence and computability. Because [0, ∞] is complete under arbitrary
infima, one can construct the least admissible solution by taking the pointwise infimum over all
admissible functions, or (under mild finiteness/well-foundedness assumptions on decomposition) by
iterative improvement reminiscent of dynamic programming. When there are cycles of decomposi-
tions, s∗C still exists as a least consistent assignment, but it may take the value ∞ on elements that
cannot be finitely justified without circularity.

                                                   166
Remark 365. Examples. If items are arithmetic expressions and ∗ combines subexpressions,
s∗C (x) measures the minimal cost of a derivation tree of x. If items are designs built from com-
ponents, it measures the cheapest assembly plan accounting for component simplicity and assembly
overhead.

Remark 366. Further example (segmentation). If XC is a set of strings, ∗ is concatenation,
and tC ≡ 0, then s∗C can be read as the best achievable cost under all binary segmentations of a
string into substrings. Different binary parenthesizations correspond to different parse trees, but
because tC = 0 and concatenation is associative, the best cost is effectively governed by the best
segmentation into primitive or previously-simplified pieces.

Remark 367. Why needed. Hyperseed’s pattern theory requires not just that some objects are
simple, but that simplicity behaves predictably under composition. Otherwise “pattern intensity”
would not be stable when patterns are nested or combined. Compositional simplicity is one way to
enforce this stability, and it aligns with the hierarchical/heterarchical pattern-web perspective in [5].

Remark 368. The recursion above is the effort-quantale analogue of the informal Hyperseed sketch
(see the motivating discussion around compositional simplicity in the Hyperseed overview). The
“least” solution corresponds to the best achievable decomposition costs, i.e. dynamic programming
over all factorization trees.

Remark 369. Binary vs. multiway composition. Only binary composition is built into the
definition, but multiway composition is implicitly covered by iterating ∗ along a tree. The overhead
function tC then determines how integration costs accumulate across intermediate stages, which
is precisely why parenthesization can matter when ∗ is non-associative or when overheads depend
strongly on the intermediate artifacts.

Proposition 5 (Immediate subadditivity bound). For any y, z ∈ XC we have

                                s∗C (y ∗ z) ≤ s∗C (y) + s∗C (z) + tC (y, z).

Remark 370. What this says, intuitively. Even if there might exist a cleverer way to build
y ∗ z than “build y, build z, glue them,” the naive plan is always available. Therefore the optimal
cost of y ∗ z cannot exceed the cost of that naive plan. This is the compositional counterpart of the
basic subadditivity property of effort.

Remark 371. Connection. This proposition is a one-step corollary of the defining inequality of
compositional admissibility. It is also the local inequality that later becomes global when we interpret
s∗C (x) as the minimum over parse trees in Theorem 9.

Remark 372. When the bound is informative. If tC (y, z) is small (or zero), the proposition
says that simplicity is nearly subadditive under composition, so building larger structures from
simple parts does not incur disproportionate penalty. If tC (y, z) is large, then even very simple
parts can yield a complex whole, capturing the common phenomenon that “integration dominates
implementation.”

Proof. In the definition of s∗C (y ∗ z), the infimum is taken over all decompositions of y ∗ z. One ad-
missible decomposition is precisely (y, z), hence the infimum is bounded above by the corresponding
cost.




                                                   167
Proof sketch. The proof simply points to one specific candidate decomposition inside the infimum
defining s∗C (y ∗ z). An infimum over many candidates is always less than or equal to any particular
candidate. Concretely, the defining inequality for s∗C (x) (as the least solution of the compositional
recursion) considers all pairs (y, z) with y ∗ z = x; selecting the specific pair that actually wit-
nesses the composition y ∗ z gives an admissible term in that infimum, hence an immediate upper
bound. This is the same one-line argument that underlies subadditivity bounds for shortest-path
or dynamic-programming value functions: “evaluate at a specific action” bounds the optimum. 
Remark 373. A geometric metaphor is useful: think of all decompositions of x as offering dif-
ferent “routes” to construct x, each with a cost. The simplicity s∗C (x) is the cost of the cheapest
route. The particular route “split into y and z” provides an upper bound on the cheapest route,
because it is one of the routes under consideration. Equivalently, if one imagines a landscape of
candidate constructions, then s∗C (x) is the lower envelope of their costs, and any explicitly described
construction gives a point on that landscape. This perspective also clarifies why such bounds are
often easy to produce: it is typically simpler to describe one feasible construction than to certify
optimality among all constructions.
Theorem 9 (Compositional simplicity equals minimum parse-tree cost (finite case)). Assume XC
is finite, and for each x ∈ XC the set of decompositions

                              Dec(x) := {(y, z) ∈ XC × XC : y ∗ z = x}

is finite. Assume also tC (y, z) ≥ 0 for all (y, z) and s∗C (e) = 0. Define the cost of a full binary
parse tree T evaluating to x by summing tC over internal nodes and 0 on leaves labeled by e (or by
primitive atoms assigned fixed base costs, if desired). Then s∗C (x) equals the minimum cost among
all such parse trees for x. Moreover, in this finite setting the minimum is attained by at least one
parse tree (so the statement is not only an “infimum equals infimum” claim, but an actual minimum
over a finite search space of well-formed derivations).
Remark 374. Plain-language meaning. In the finite case, s∗C (x) is exactly what you would
compute by enumerating all ways of parenthesizing/decomposing x into binary combinations, adding
up the overhead at each combination, and taking the cheapest total. So the abstract least-solution
definition really does coincide with the familiar notion of “minimum derivation cost” from parsing
and dynamic programming. In particular, the recursion for s∗C can be read as the usual dynamic-
programming recurrence: the best way to build x is to choose a last split (y, z) that yields x and pay
the best costs for y and z plus the overhead tC (y, z).
Remark 375. Why it matters. This theorem justifies calling s∗C “compositional simplicity”
rather than an arbitrary fixed-point artifact. It says the definition matches an operational proce-
dure: build x by a tree of compositions and pay overhead at each internal node. This is the form
in which simplicity will interface with grammar-like structural complexity (Hyperseed-Concept 181)
and, later, with pattern hierarchies. It also means that many standard intuitions about parsers
carry over: sharing subcomputations, reusing repeated substructures, and excluding impossible de-
compositions correspond to pruning the parse-tree search and thus computing s∗C efficiently when
the finite assumptions hold.
Remark 376. Connection to later sections. Pattern recognition often constructs candidate
explanations via hierarchical decompositions. The parse-tree interpretation implies that if patterns
supply cheap decompositions of observations, then they also supply low compositional simplicity.
This will be used implicitly when emergence is defined by comparing pattern intensities under com-
bination in Section 9. A useful way to keep the linkage in mind is: patterns propose “good splits”

                                                  168
(low tC and/or low child costs), and the theorem formalizes that repeatedly choosing such splits
corresponds exactly to building a low-cost derivation tree.

Proof. Because XC is finite and each Dec(x) is finite, the recursion defining s∗C reduces to a finite
system of Bellman-style optimality equations over a finite directed hypergraph. Standard dynamic-
programming arguments imply that the least fixed point assigns each x the minimum cost among
all finite derivations (parse trees) that construct x from e using ∗, with per-node cost tC . One
convenient way to make this precise is to define the Bellman operator B on functions f : XC → [0, ∞]
by                                                                          
                            (Bf )(x) =     inf     f (y) + f (z) + tC (y, z) ,
                                        (y,z)∈Dec(x)

together with the boundary condition f (e) = 0 (and any chosen base costs for other primitives, if
the variant with primitives is used). In the finite nonnegative-cost setting, iterating B from the
pointwise-zero (or pointwise-minimum admissible) function produces a monotone nondecreasing
sequence that stabilizes at the least fixed point, and that limit coincides with the minimum over
all finite parse trees because each application of B corresponds to adding one more internal-node
layer to a partial derivation.

Proof sketch. The high-level strategy is: (i) view the decomposition relation y ∗ z = x as a
finite hypergraph of production rules; (ii) interpret the defining inequality for s∗C as the Bellman
optimality condition for that hypergraph; (iii) invoke the standard fact that, in finite nonnegative-
cost settings, the least fixed point of the Bellman operator yields the minimum cost over all finite
derivations, i.e. parse trees. If one wants a slightly more operational phrasing, step (iii) can be
seen as: dynamic programming on a finite acyclic-or-nonnegative-cost graph cannot benefit from
infinite unfolding, so optimal values are witnessed by finite trees, and the least solution is exactly
the one computed by taking minima over all finite unfoldings.                                       

Remark 377. The key step is the identification of “least solution of recursive inequalities” with
“minimum over trees.” Nonnegativity of tC prevents pathological negative-cost cycles, and finiteness
ensures the relevant minima are achieved among finitely many candidate derivations. The “directed
hypergraph” phrasing is simply the combinatorial shadow of the binary constructor: each equation
x = y∗z is a hyperedge from (y, z) to x. It may also help to note that the hypergraph viewpoint cleanly
separates syntax (which decompositions are allowed, i.e. which hyperedges exist) from weights (the
overheads tC ), and s∗C is exactly the induced shortest-derivation-cost function in that weighted
hypergraph.

Remark 378. A visual intuition is to imagine building x by repeatedly merging pieces. Each merge
has an overhead cost. A parse tree records the history of merges. The theorem says: among all
possible merge histories that end at x, the least fixed point s∗C (x) picks the cheapest. In this picture,
internal nodes correspond to merge operations, leaves correspond to the simplest available building
blocks (here normalized so that e has zero cost), and the total cost is additive along the merge
history, mirroring how many compositional systems accumulate “effort” across steps.

Remark 379. The theorem is stated in a minimal form to emphasize the intended interpretation.
In the full development one typically assigns base costs to a set of primitives and allows leaves to
be any primitive, not only e; the same proof pattern applies. The only substantive change in that
extension is that the base-cost function contributes an additional leaf term in the tree-cost sum,
while the internal-node contributions remain exactly the overheads tC .



                                                   169
8.8   Generalized Kolmogorov complexity and structural complexity
Classical Kolmogorov complexity measures the length of the shortest program that outputs an
object (Hyperseed-Concept ??; see [16]). Hyperseed’s observer-relative simplicity suggests a more
general construct: replace “program length” by effort measured in whatever resources the observer
actually expends.
Remark 380. A small but important shift. In the classical setting, the observer fixes (implic-
itly) a reference machine and a bitlength measure; both are taken as background structure. Here,
the context C makes that background structure explicit: the observer not only chooses a decoding
procedure, but also chooses which objects count as admissible descriptions and which expenditures
count as cost. This makes it possible to speak about complexity in settings where “programs” are not
the natural currency (e.g. physical actions, laboratory protocols, or interactive strategies), without
losing the essential “best available redescription” character of Kolmogorov-style definitions.
Definition 86 (Generalized description systems). A generalized description system for context C
consists of:
• a set of descriptions (programs, proofs, encodings) DC ,

• a partial decoding map DecC : DC * XC ,

• an effort assignment Eff C : DC → [0, ∞] satisfying Eff C (d1 d2 ) ≤ Eff C (d1 ) + Eff C (d2 ) for a
  suitable concatenation/combination operation on descriptions.
Remark 381. Notation unpacking. The arrow * denotes a partial function: not every de-
scription must decode successfully. The expression d1 d2 denotes a chosen notion of concatena-
tion/combination of descriptions (for instance, string concatenation, program composition, proof
concatenation). The inequality Eff C (d1 d2 ) ≤ Eff C (d1 ) + Eff C (d2 ) is the same sequential subaddi-
tivity idea as before, now applied to description objects.
Remark 382. What “partial” buys you. Allowing DecC to be partial captures several common
situations: ill-formed strings, programs that do not halt, proofs that fail to check, circuits with un-
defined behavior under the chosen simulator, or sensory-motor policies that fail to reach a terminal
state. Formally, partiality lets DC include a broad space of candidates while keeping DecC as the
filter that determines which candidates are meaningful for the observer. This mirrors the classical
use of partial computable functions (universal machines) but does not restrict DecC to that regime.
Remark 383. Effort as a resource preorder. The codomain [0, ∞] is chosen so that infeasible
descriptions can be assigned infinite effort, and so that infima of effort sets always exist (possibly as
∞). The subadditivity condition is deliberately weak: it says only that performing two description-
steps in sequence should not cost more than paying for each step separately. In many concrete
models one expects an additional fixed overhead (e.g. for glue code, delimiters, or interface adapta-
tion), and this can be incorporated either by modifying the combination operation or by absorbing
the overhead into the definition of Eff C (as is done later via tC in compositional systems).
Remark 384. Intuition. A description system is a general “language + interpreter + cost”
triple. Kolmogorov complexity chooses a specific universal programming language and uses bitlength
as cost; we instead allow any description language that an observer in context C can actually use,
and any cost model that tracks the observer’s real expenditures. This is one way to reconcile the
philosophical power of algorithmic information with the Hyperseed insistence on observer-relativity
[1].

                                                  170
Remark 385. Examples. DC could be: binary strings interpreted by a fixed machine; formulas
decoded by a parser; circuits decoded by a simulator; or proofs decoded by a proof checker. Effort
could count length, runtime, energy, memory, or a weighted blend (Hyperseed-Concept 100).

Remark 386. Two clarifying example patterns. If DC is a set of plans (action sequences)
and DecC maps each plan to its realized outcome in an environment model, then KC (x) becomes the
least action-cost required to produce x. If DC consists of probabilistic model specifications together
with random seeds, and DecC is “run the sampler and return its sample,” then effort can represent
expected compute and KC (x) becomes a best-effort generative route to x (where the partiality can
encode non-termination or rejection conditions). These are not classical program-length settings,
but they still instantiate the same abstract “search for cheapest description that yields x” template.

Remark 387. Why needed. Later, when patterns are defined as effort-reducing redescriptions,
we need the notion of “description” to be context-dependent: the patterns available to a symbolic
reasoner differ from those available to a sensory-motor controller. Generalized description systems
are the formal slot where that dependence lives.

Remark 388. On comparability across contexts. Because KC depends on DC , DecC , and
Eff C , values KC1 (x) and KC2 (x) are not automatically commensurate. This is a feature rather
than a bug: Hyperseed uses C precisely to record which tools, priors, and resource-accounting con-
ventions the observer is using. When cross-context comparisons are needed, they must be mediated
by explicit translations between description systems (e.g. an embedding of DC1 into DC2 with con-
trolled overhead), which is the generalized analogue of the classical invariance discussion around
universal machines [16].

Definition 87 (Generalized Kolmogorov complexity). Given a generalized description system,
define
                      KC (x) := inf{Eff C (d) : d ∈ DC , DecC (d) = x}.

Remark 389. Well-definedness and edge cases. If there is no description d with DecC (d) = x,
then the set inside the infimum is empty and, by the usual convention, KC (x) = ∞. If there are
descriptions achieving arbitrarily low effort without attaining a minimum (e.g. due to a limiting
process in Eff C ), the infimum still exists even though no optimal description exists. Thus KC should
be read as an “optimal achievable bound” rather than a guarantee of an attained optimum.

Remark 390. Intuition. This is the same infimum-over-descriptions pattern as the simplicity
definition sC (x), but with an explicit decoding map. It is therefore best read not as a single universal
complexity, but as an observer-indexed family of complexities KC .

Remark 391. Examples. If x is an image and DC contains generative-model parameters plus a
decoder that renders images, then KC (x) measures the cheapest generative explanation of x available
to C. If x is a theorem statement and DC consists of proofs in a formal system, then KC (x)
measures the cheapest proof effort to derive x (relative to that system).

Remark 392. Interpreting “cheapest” in non-length models. When Eff C is time or energy,
KC (x) is not a static measure of description size but of description feasibility. In such cases
KC (x) is naturally paired with a specific execution model (the DecC dynamics) and may depend
sensitively on implementation details (e.g. hardware assumptions, parallelism, or available caches).
This dependence is exactly what is wanted in observer-relative analysis: two observers with different
hardware, training, or libraries can legitimately assign different complexities to the same x.


                                                  171
Remark 393. Usefulness. This definition provides a rigorous bridge between the classical “short-
est program” perspective [16] and the Hyperseed “least effort” perspective. It allows later claims
about simplicity/patterns to be interpreted either as compression statements or as resource-allocation
statements, depending on the chosen Eff C .

Remark 394. If DC = {0, 1}∗ , Eff C (d) = |d| is bitlength, and DecC is a universal Turing machine,
then KC reduces (up to an additive constant) to classical Kolmogorov complexity. If Eff C counts
time, energy, memory, proof steps, or a weighted blend, one obtains different observer-relative
complexity notions.

Remark 395. Relationship to classical invariance (informal). The “additive constant”
caveat in the classical case comes from comparing two universal machines via compiler overhead.
In the generalized setting, analogous comparison statements require explicit assumptions: a trans-
lation τ : DC1 → DC2 such that DecC2 (τ (d)) = DecC1 (d) and Eff C2 (τ (d)) ≤ Eff C1 (d) + κ (or a
multiplicative/affine variant). When such a translation exists, one can transport upper bounds on
KC1 (x) into upper bounds on KC2 (x) with controlled overhead, which is the operational content of
invariance in this observer-relative language.

Proposition 6 (Structural complexity as compositional complexity). Suppose DC is generated by
a finite set of primitives and a binary constructor corresponding to ∗ (with overhead tC ) so that
every description induces a parse tree whose yield is x ∈ XC . Then the generalized complexity
KC (x) coincides with a compositional simplicity functional of the form s∗C (x) (up to fixed base costs
for primitives).

Remark 396. Plain-language meaning. When your description language is essentially “build
objects by repeatedly combining primitives,” then the cheapest description is the cheapest parse tree.
So structural complexity (Hyperseed-Concept 181) is not a separate mystery: it is compositional
simplicity under a particular choice of description system.

Remark 397. Proof idea (informal). Under the hypothesis, any d ∈ DC corresponds to a
finite parse tree whose leaves are primitives and whose internal nodes are applications of the binary
constructor. If Eff C assigns each primitive a fixed base cost and each constructor application the
overhead tC (possibly plus child costs), then Eff C (d) is (up to constants) the same as the recursively
defined compositional cost of the induced tree. Taking the infimum over all d yielding x is therefore
the same optimization as taking the infimum over all ∗-parse trees yielding x, which is exactly
what s∗C (x) encodes. The “up to fixed base costs” clause accounts for the choice of primitive-cost
normalization, which shifts all complexities by a bounded amount when the primitive set is finite.

Remark 398. Why it matters. This proposition explains why grammar-like notions of complexity
appear naturally once one takes compositionality seriously. It also clarifies how the later pattern
layer can speak simultaneously about “compression” and “structure”: both are costs of derivations
in appropriate description systems [5].

Remark 399. Connection to grammars and circuits. When primitives are terminals and
the constructor corresponds to applying production rules, parse trees are exactly derivations in a
grammar, and KC (x) becomes a least-derivation-cost measure. When primitives are gates and the
constructor corresponds to wiring subcircuits, parse trees become circuit expressions, and KC (x)
becomes a size/energy/time cost of realizing the circuit that yields x. These familiar “structural”
complexity measures are therefore instances of the same generalized template, differing only in what
counts as a primitive, what the constructor does, and how effort is tallied.


                                                  172
Remark 400. Connection to Theorem 9. The proposition reduces an infimum over descrip-
tions to a minimum over parse trees, and Theorem 9 identifies that minimum with the least fixed
point s∗C . So the chain is: descriptions → parse trees → fixed point. More explicitly, the descrip-
tion language can be viewed as a syntactic presentation of the same compositional data encoded
by a derivation/parse tree: the leaves specify which primitives are used, and each internal node
records one application of the binary constructor (together with any side-information required by
the combination system). The key point is that the objective being optimized (effort) is structural:
it depends only on the multiset of leaves (base costs) and the pattern of internal nodes (overhead),
so it is invariant under switching between these two representations.

Proof. Each description corresponds to a finite parse tree in the combination system, whose effort
is the sum of base costs and overhead costs. Taking the infimum over descriptions is therefore
equivalent to taking the minimum over parse trees. By Theorem 9, this is exactly the compositional
simplicity s∗C (x) (with the appropriate base-cost initialization). To make the equivalence precise,
note that the decoding map from descriptions to objects factors through the induced tree: once
a description is parsed, it determines (i) the primitive labels at the leaves and (ii) the recursive
bracketing specifying how the binary constructor is applied. Conversely, given any finite labeled
parse tree that evaluates to x under the combination rules, one can encode it as a description by
writing down the corresponding parenthesized expression (together with the same primitive labels),
so the two optimization domains are coextensive up to the chosen encoding/decoding conventions.
Moreover, because effort is defined additively—a leaf contributes its base cost and each internal
node contributes the constructor overhead for that particular combination step—the effort assigned
to a description coincides with the effort assigned to its tree. Under this identification, optimizing
over descriptions or over trees is the same optimization problem, and Theorem 9 supplies the value
of that optimum as the least fixed point s∗C with the stated initialization.

Proof sketch. The proof strategy is a change of variables. Instead of optimizing over descriptions
directly, we optimize over their induced parse trees. Because the description language is generated
by primitives and a binary constructor, descriptions and parse trees carry the same information up
to the chosen decoding. Effort additivity over constructors becomes summation of overhead along
internal nodes, so the best description is the cheapest tree, which Theorem 9 already characterizes as
s∗C . In other words, the apparent “infimum over strings” is not an additional analytic complication
here: the strings are merely a linearization of a finite tree-shaped derivation. Once we switch to
the tree view, the cost decomposition aligns directly with the dynamic-programming/fixed-point
viewpoint: the cost of a node is the overhead for combining its two children plus the costs already
assigned to those children, so the global optimum is obtained by choosing, at each object, the
cheapest available decomposition into subobjects. This is exactly the recursion captured by the
operator whose least fixed point is s∗C .                                                           

Remark 401. One can think of this as a Russellian move: replace an informal notion (“struc-
ture”) by an explicit construction (“a derivation tree in a generating grammar”) and then observe
that the resulting measure of complexity is just the optimization problem already solved by the com-
positional simplicity fixed point. From this perspective, “structural complexity” is not an extra
ingredient beyond the grammar/combination system: it is the minimal cost of a witness that x can
be generated by the primitives via the constructor. The move is useful because it separates (a) the
representational choices (how we write down derivations as descriptions) from (b) the invariant
content (which derivations exist and what costs they accrue), and it is the latter that the fixed-point
characterization computes.



                                                 173
8.9   Discussion: how this feeds later Hyperseed layers
This section provides the minimal mathematical “landing zone” for several later constructs: In
particular, the goal is to make the informal notions of “trying,” “difficulty,” and “having a good way
to see something” available in a form that can be transported into later layers without reintroducing
hidden anthropomorphic assumptions. The emphasis on relative effort (relative to a baseline,
relative to an observer, relative to an available policy class) is deliberate: later Hyperseed layers will
repeatedly compare systems that differ in representational resources, history, or control authority,
and the present setup makes those comparisons explicit rather than tacit. One may also read this
section as fixing a common currency for subsequent tradeoffs: whenever a later construct is said to
be “simpler,” “more natural,” or “more learnable,” the intended operational meaning is that some
decomposition or control objective can be achieved with systematically reduced effort, possibly
after a change of representation.

• Patterns (Section 9). A pattern will be a representation r of x that yields a significant
  reduction in effort relative to a baseline. Pattern intensity will compare baseline effort to achieved
  effort (or dually compare baseline weakness to achieved weakness). This links the present material
  to the theory of pattern and emergence in [5]. In this sense, a “pattern” is not merely a regularity
  in x, but a useful regularity: it is evidenced by an improved effort profile when the agent adopts
  (or is given) the representation r. The baseline is crucial: the same r may be intensely patterned
  for one observer (who lacks alternative efficient decompositions) and nearly trivial for another
  (who already possesses a better policy or representation class), which is exactly the observer-
  relativity that later emergence arguments rely upon. When later sections speak of the “strength”
  or “salience” of a pattern, the intent is that such terms can be cashed out in the effort/weakness
  comparison induced by substituting r into a fixed task family, rather than by appealing only to
  descriptive compression in the abstract.

• Habits and morphic resonance (Section 12). Habit formation will be modeled as repeated
  updates to a distinction policy (or to the representations supported by a policy) that progressively
  reduce effective effort for certain decompositions. Resistance/submission will become dynamical
  (history-dependent) rather than purely static. (For the broader ontological framing of habit and
  resonance, see [13] alongside the Hyperseed presentation [1].) The core addition in the habit layer
  is that “effort” is not treated as fixed by the current task alone: instead, the system carries a
  trajectory of learned biases, cached distinctions, and preferred decompositions that change what
  is easy to do next. Formally, this means that whatever object plays the role of a distinction
  policy is iteratively updated so that future instances of a decomposition problem are solvable
  at lower marginal effort, e.g. by reusing internal structure rather than reconstructing it from
  scratch. In this frame, “resistance” to a proposed decomposition can be read as an induced cost
  that persists across time (a kind of inertial term), while “submission” corresponds to a learned
  alignment in which the same decomposition pathway becomes increasingly low-effort. This is
  also where the present algebraic notions become temporally textured: weakness and effort will
  be evaluated not only at a single time slice, but along an updating process, making the relevant
  quantities explicitly history-dependent.

• Mind-world correspondence (Section 14 and onward). “Good models” are those that
  achieve task adequacy with low effort, i.e. they lie near the Pareto frontier of adequacy vs
  effort. Weakness provides an algebraic handle for composing such models across contexts, as
  emphasized in [3]. The Pareto framing is meant to prevent a false dichotomy between “accurate”
  and “simple”: in later sections, adequacy (predictive, explanatory, or control success) and effort


                                                   174
    (cognitive/work cost under a policy) will be treated as jointly constrained objectives. On this
    view, a model that is “too complex” is not rejected for having many parts per se, but because its
    achieved adequacy does not justify its effort relative to available alternatives; conversely, a model
    that is “too simple” is one whose low effort comes at an avoidable adequacy loss. Weakness
    enters as a compositional bridge: when moving between contexts or composing submodels, one
    wants to track how far the composed construction is from an ideal of effortless adequacy, and
    weakness provides a way to express and bound that deviation without re-deriving everything
    from first principles each time. This is especially important when the later causality/control
    layer introduces interventions and control authority: the “effort” budget then includes not only
    internal computation but also the cost of acquiring leverage over the environment, and the same
    algebraic bookkeeping is intended to remain applicable.

    In short: effort provides the primitive experiential “thermodynamics” of cognition, and sim-
plicity is its observer-relative, compositional shadow. Read this as a methodological constraint as
well as a slogan: whenever later layers introduce new entities (patterns, habits, control structures),
they should be interpretable as mechanisms for reallocating, reducing, or regularizing effort across
tasks and contexts. Correspondingly, “simplicity” is not an intrinsic label attached to an object x
in isolation, but a relational statement about how an observer can interact with x under some rep-
resentational and policy constraints, and about how such interactions compose when x is embedded
into larger constructions.


9     Patterns, emergence, properties, and blending
Outline
• Fix a general “description-and-decoding” setup in a context C: entities, a combination operation,
  a description language, and a cost/effort functional.

• Define pattern as a compressive re-description (a representation-as-something-simpler), and de-
  fine pattern intensity as normalized compression gain (optionally p-bit-valued to allow “strong
  but wrong” patterns).

• Define properties as fuzzy sets of patterns (membership = intensity), and define specific entities
  as temporally coherent bundles of patterns (identity-as-a-derived-pattern).

• Define emergence for a combination A∗B as patterns whose intensity in A∗B exceeds a weighted
  combination of their intensities in A and B.

• Formalize combination, inheritance, association, and lifting from instances to groups as operations
  on pattern/property structures (with quantale-style aggregation as a unifying tool).

• Define blends in property-set terms (large overlap of properties), and present a categorical blend
  construction (pushout/colimit with weakness/effort ranking).

• Define combinatorial-categorical patterns (patterns that appear after category-theoretic substi-
  tutions), and define combination systems, interpreted combination systems, and combinational
  dynamical causal models.




                                                   175
Summary and Hyperseed concepts covered
Hyperseed’s “pattern layer” is the pivot from phenomenological primitives and effort/simplicity
to structured cognition. The core move is operational: a pattern in x is a way to represent x
as something simpler (lower effort / lower description cost) in a given observer/context. Once
pattern intensity is available, one can define properties (as fuzzy sets of patterns), emergence (as
patterns whose intensity is amplified by combination), and blending (as property overlap). This sec-
tion also supplies formal counterparts of Hyperseed’s auxiliary constructs that are needed to make
patterns interact with computation and dynamics: combination systems, interpreters, substitution-
lifted (combinatorial-categorical) patterns, and combination-preserving representations of dynami-
cal causality.
     The intended reading is that the “observer/context” C fixes not only what counts as a valid
description, but also what resources are salient: the same underlying entity can exhibit different
patterns under different description languages, different decoders, different noise models, or different
effort functionals. In particular, the cost/effort functional should be understood broadly: it may be
a code length, a runtime/space budget, an energy expenditure, a statistical risk, or any proxy for
what the context treats as “simplicity.” This is what makes patterns comparable and “intensity”
meaningful: intensity is not an intrinsic property of the entity alone, but a context-indexed degree
of compressive advantage.
     The phrase “representation-as-something-simpler” is meant to cover both exact and lossy re-
descriptions. An exact pattern corresponds to a shorter description that still decodes to the same
target (up to the equivalence notion induced by the decoder), whereas a lossy pattern permits a
controlled mismatch when the context does not distinguish the difference. Allowing p-bit-valued
intensity is a way to explicitly represent the case where a description is highly compressive yet
systematically incorrect: such a pattern can be strong as a proposal while being wrong as a recon-
struction, which becomes important when modeling biased or partial observers, adversarial settings,
or situations where the decoder is itself fallible. In that sense, intensity is not merely “how present
a pattern is,” but how much the pattern functions as an economical explanatory handle within the
context.
     Defining properties as fuzzy sets of patterns makes the ontology “pattern-first” rather than
“predicate-first.” A property is not an atomic label attached to entities; it is a distribution of
pattern intensities, so that property membership is graded and decomposable. This supports a
notion of similarity as overlap of property-sets (equivalently, similarity of pattern profiles), and it
also supports compositional updates: changing context C changes which patterns are cheap, thereby
changing property membership without requiring a separate re-axiomatization of predicates. The
notion of a “collective-property-set” then captures the idea that a group or aggregate can carry
properties that are not merely pointwise averages of its members’ properties, but are properties
arising from aggregation of pattern evidence under the chosen combination operator.
     Similarly, defining specific entities as temporally coherent bundles of patterns makes identity a
derived, dynamical construct. What persists through time is not a metaphysically primitive “thing,”
but a stable configuration of patterns whose intensities remain coherent under a temporal update
rule (the temporal coherence algebra). This lets the framework treat tracking, object permanence,
and re-identification as instances of pattern maintenance under resource constraints, rather than
as separate primitives. It also clarifies why boundaries of entities can be context-sensitive: what
counts as “the same” entity can depend on which patterns are cheap enough to enforce over time.
     The emergence criterion for A ∗ B is intended to separate three cases: (i) mere inheritance of
patterns already intense in A or B, (ii) dilution or interference where intensities decrease upon
combination, and (iii) genuinely emergent amplification where the combined object supports a


                                                  176
pattern more strongly than expected from its parts. The weighted comparison baseline makes this
precise without forcing linearity: the weights can encode asymmetry of contributions, attention, or
relevance, and the aggregation can be tuned to match the semantics of the combination operator ∗.
In particular, emergence here is not a mysterious ontological surplus; it is a detectable departure
in pattern intensity relative to a specified compositional expectation.
    The operations listed (combination, inheritance, association, and lifting) are included to make
pattern/property structures usable as algebraic objects rather than mere annotations. Quantale-
style aggregation is singled out because it provides a unified way to combine graded evidence
(intensities), compose relational links (associations), and transport structure between levels (from
instances to groups) while preserving monotonicity and resource-sensitivity. This is the sense in
which the pattern layer serves as infrastructure: it supplies the algebra needed to manipulate
intensional content in a way that is stable under composition and aggregation.
    Blending is presented in two complementary ways: as a high-overlap relation on property-sets
and as a categorical construction. The property-overlap view captures an intuitively geometric
notion of conceptual mixture: two entities (or two concepts) blend when they share a large portion
of their salient properties, with “large” measured relative to the chosen intensity aggregation and
any relevance weighting. The categorical pushout/colimit view then captures the constructive side:
a blend is not only a comparison between two sources but an explicit amalgam built by identifying
shared structure. The mention of weakness/effort ranking indicates that there may be multiple
candidate pushouts or colimits, and the framework chooses among them by preferring lower-effort
identifications, thereby keeping the construction aligned with the underlying description-cost se-
mantics.
    Finally, combinatorial-categorical patterns, interpreted combination systems, and combinational
dynamical causal models are included to connect patterns to computation and dynamics. The key
point is that new patterns can become visible only after a systematic change of representation
(a substitution or functorial re-encoding), so the framework must account for patterns that are
invariant or salient under such transformations. A combination system provides the abstract algebra
of how entities compose; an interpreted combination system adds a semantics that links abstract
compositions to concrete decoded entities and their costs; and a combinational dynamical causal
model adds time and causality in a way that is compatible with combination. Together, these
notions ensure that patterns are not merely descriptive snapshots but can be propagated, compared,
and preserved under dynamical evolution and under the computational processes that implement
decoding and substitution.

Hyperseed concepts covered.
• Pattern; pattern intensity.

• Emergence.

• Property; property-set; collective-property-set.

• Specific entity (as a derived pattern with a temporal coherence algebra).

• Blend.

• Combination; inheritance; association; lifting from instances to groups.

• Combinatorial-categorical pattern.

• Combination system; interpreted combination system.

                                                177
• Combinational dynamical causal model.

9.1   Setup: entities, contexts, descriptions, and effort
We assume the effort/simplicity layer from Section 8 provides, for each context (or observer-relative
aspect) C, a universe of entities EC together with:

• a (possibly partial) combination operation

                                         ∗ C : EC × E C * EC ,

  intended to model “putting things together” in the sense relevant to C;

• a description system (syntax) LC and an interpreter/decoder

                                             DecC : LC → EC ,

  intended to model how the observer encodes/constructs entities; and

• an effort or description cost functional

                                      costC : LC → R≥0 ∪ {∞}.

    Here “context” should be read broadly: C may represent a sensory modality, a measurement
apparatus, a scientific modeling stance, a downstream task, or a cognitive “view” that determines
which distinctions are salient. Accordingly, EC is not assumed to be a context-independent ontology;
rather, it is the space of entities as individuated by C. For example, for a text-processing context
C, EC might be strings; for a vision context, EC might be images up to some equivalence; and for
an engineering context, EC might be structured designs equipped with tolerances.
    The partiality of ∗C is deliberate: some pairs of entities may be non-composable (e.g., their
interfaces do not match, their physical constraints are incompatible, or the context has no rule for
combining them). No global algebraic laws (associativity, commutativity, identities) are assumed
unless explicitly stated later; different applications may impose such laws, or may instead treat them
as approximate regularities that can themselves be learned or encoded by descriptions. Intuitively,
x ∗C y captures the context-specific notion of composing x and y (e.g., concatenation of strings,
overlaying images, wiring components, forming a conjunction of properties, or bundling features
into a composite representation).
    The role of LC is to make explicit that “having an entity” is operationally mediated by rep-
resentational resources. The map DecC then specifies how a description ` is interpreted as an
entity. Although written as a total function, one can fold ill-formedness or decoding failure into
this framework by allowing costC (`) = ∞ for descriptions that are syntactically valid but semanti-
cally unusable in C, or by treating LC as already restricted to well-formed, decodable descriptions.
The cost functional costC can represent many things (bits, time, memory, energy, cognitive effort,
or a weighted mixture), and it may incorporate both fixed overheads (e.g., calling a subroutine, in-
voking a concept) and variable costs (e.g., specifying parameters at a given precision). Allowing ∞
is important: it makes room for hard constraints (some descriptions are forbidden or unattainable),
and it ensures the infimum below behaves sensibly even when some candidates are inadmissible.
    The (contextual) simplicity/complexity of an entity is then the minimal effort required to de-
scribe it:


                                                  178