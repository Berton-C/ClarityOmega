# 15 Attention and cognitive synergy

Remark 635. In examples like kiss(Ben) or get(ball), the event type may implicitly carry
arguments (participants, objects, locations). One can regard E as a set of fully instantiated predicates
(ground atoms), or as a set of predicate schemas paired with a domain of entities. Nothing below
depends on this choice, as long as the notation A@t picks out a well-formed token claim that can
be supported or opposed by the observer’s evidence.

Remark 636. This definition is useful because it cleanly separates (i) the syntax of events (what we
are talking about), (ii) the temporal indexing (when we are talking about it), and (iii) the evidence
semantics (how strongly we support or deny the token). That separation will let us define prediction
and control without assuming an underlying classical truth assignment.

   Hyperseed is explicitly comfortable with borderline, context-dependent, and even inconsistent
boundaries. We therefore allow paraconsistent evidence about event occurrences.

Definition 175 (Paraconsistent occurrence evidence). Fix an observer/context O. A paraconsis-
tent occurrence assignment is a map
                                                            +         −
                    EO : E × T → [0, 1]2 ,     EO (A@t) = (EO (A@t), EO (A@t)),
        +                                                         −
where EO   is the degree of positive evidence for occurrence and EO is the degree of negative evidence
                                                                             +           −
for occurrence. No consistency constraint is imposed; it may happen that EO    (A@t)+EO    (A@t) > 1.
                             +         −
Remark 637. The pair (EO       (A@t), EO (A@t)) is the p-bit-style encoding of evidence: the first
coordinate is support for occurrence, the second is support for non-occurrence. The subscript O
emphasizes that this is observer-indexed evidence, not an observer-independent fact (Hyperseed-
Concept ?? is treated elsewhere).

Remark 638. A useful way to read (p, q) ∈ [0, 1]2 is as answering two distinct questions that need
not be complements: “How much do I have reasons for A@t?” (measured by p) and “How much
do I have reasons against A@t?” (measured by q). Paraconsistency enters precisely by refusing the
classical identification of “reasons against” with “lack of reasons for,” thereby allowing the agent
to represent conflict, ambiguity, or model mismatch without forcing an immediate resolution.

Remark 639. As a toy example, suppose a microphone picks up a sound that is somewhat like
                                                    +
a door slam. An audio classifier might assign EO       = 0.7 for A =door-slam at time t, while a
                                                                  −                 +    −
concurrent vision module that sees no door movement assigns EO      = 0.6. Then EO    + EO = 1.3 > 1,
which records a genuinely conflicted evidential state. This is especially useful when modeling agents
that must act under contradictory cues rather than wait for idealized consistency.

Definition 176 (Derived evidence diagnostics (consistency, conflict, and indeterminacy)). Given
a token A@t with evidence (p, q) = EO (A@t), define:

      conf O (A@t) := min(p, q),      gapO (A@t) := 1 − max(p, q),        balO (A@t) := |p − q|.

Remark 640. The quantity conf O (A@t) measures conflict: it is large only when both occurrence
and non-occurrence are substantially supported. The quantity gapO (A@t) measures indeterminacy
(or evidential “silence”): it is large when neither side is strongly supported. Finally, balO (A@t)
measures how decisive the net evidence is, regardless of whether the decisiveness arises from consis-
tent support (large p with small q) or consistent refutation (small p with large q). These diagnostics
are optional but often clarify which kind of uncertainty is present: “both” (conflict) versus “neither”
(gap).

                                                  286
Remark 641. This definition is necessary for later sections where “self/other” boundaries and
other high-level partitions can be simultaneously supported and resisted (Section 16). It also aligns
with the broader paraconsistent stance that contradiction need not entail collapse of inference, but
may instead be treated as structured information [23, 24].

    To speak about attraction, we want a scalar “plausibility” derived from a p-bit. Many choices
are possible; the following is algebraically convenient and reduces to ordinary probabilities in the
consistent case.

Definition 177 (Plausibility projection). Define π : [0, 1]2 → [0, 1] by
                                                      1+p−q
                                         π(p, q) :=         .
                                                        2
We call π(EO (A@t)) the plausibility of A@t for O.

Remark 642. The symbol π here is a projection from two-dimensional evidence to a single scalar
in [0, 1]. If p is positive evidence and q is negative evidence, then p − q is a signed net tendency
toward occurrence; the affine transformation (1+(p−q))/2 merely rescales this net tendency so that
0 corresponds to “strongly implausible,” 1 corresponds to “strongly plausible,” and 1/2 corresponds
to a neutral balance.

Remark 643. The mapping π has a few immediate properties that motivate its later use as an
“attraction proxy.” First, it is monotone in the intended directions: increasing p (holding q fixed)
increases plausibility, and increasing q decreases it. Second, it is symmetric around the neutral
point: swapping p and q sends π(p, q) to 1 − π(p, q), expressing that “more reasons against” mirrors
“more reasons for.” Third, in a consistent probabilistic special case where the observer’s evidence
is such that q = 1 − p, one obtains π(p, 1 − p) = p, so π reduces to the familiar single probability
parameter.

Remark 644. It is also worth emphasizing what π does not do: it does not distinguish between
high-conflict and low-information states when they have the same net difference p − q. For example,
(p, q) = (1, 0) and (p, q) = (0.6, 0) both yield high plausibility, while (0.9, 0.9) and (0.1, 0.1) both
yield π = 1/2. This is intentional at this stage: attraction-oriented dynamics later will often be
driven by a one-dimensional “direction” (toward/away), while diagnostics such as conf O (A@t) and
gapO (A@t) can be carried alongside π when it matters to distinguish “conflicted” from “uninfor-
mative” neutrality.

Remark 645. Alternative scalarizations are possible (e.g., using p alone, using p/(p + q) when
p + q > 0, or using a nonlinear squashing of p − q). The choice of π is a minimal linear map
that preserves the qualitative ordering induced by net evidence while keeping values in [0, 1], which
makes it convenient for coupling to later definitions that resemble probabilistic prediction or utility-
like attraction scores without presupposing classical semantics.

Remark 646. For example, π(1, 0) = 1, π(0, 1) = 0, and π(0.7, 0.6) = 1+0.1   2   = 0.55, reflecting that
the token is only slightly more plausible than not. This scalarization is useful because attraction is
defined as a difference of conditional plausibilities, and differences are most straightforwardly taken
in a totally ordered set like [0, 1].
                                                                               −
Remark 647 (Consistent case). If the evidence is consistent in the sense that EO (A@t) = 1 −
  +                            +
EO (A@t), then π(EO (A@t)) = EO (A@t). Thus the projection π exactly recovers the “usual”
probability-like degree.

                                                  287
Remark 648. The consistent case remark shows that we are not abandoning classical probabilistic
intuition (Hyperseed-Concept 139); rather, we are extending it so that classical probability appears
as the special case where positive and negative streams are perfectly complementary. This is a
common pattern in foundational work: one seeks a conservative extension whose additional degrees
of freedom encode epistemic subtleties rather than metaphysical extravagance.

14.3     Prediction and attraction
14.3.1    Conditionals
To define attraction we need conditionals. We deliberately stay lightweight and treat conditionals
as something computed by the observer’s modeling machinery (statistical estimation, simulation,
logical inference, or combinations).

Definition 178 (Predictive conditional operator). Fix a lag window ∆ (e.g. a set of allowed lags,
or an interval [δmin , δmax ]). A predictive conditional operator for O is a map

                    CondO,∆ : E × E → [0, 1]2 ,         (A, B) 7→ CondO,∆ (B | A),

where CondO,∆ (B | A) is intended to represent evidence about “B occurs at some time t0 with t ≺ t0
and t0 − t ∈ ∆, given that A occurs at t.”

Remark 649. Notation unpacking: CondO,∆ (B | A) is a p-bit-valued object in [0, 1]2 , not a single
probability. The vertical bar “|” is read “given,” and ∆ specifies what counts as an acceptable
temporal separation between the antecedent token time t and the consequent token time t0 . The
strict order t ≺ t0 (derived from ) encodes temporal direction.

Remark 650. Intuitively, CondO,∆ is the observer’s forecasting interface: it answers the question,
“if A happens, how much evidence do I have that B will happen soon after (within the window ∆)?”
A simple example is: A =press(button), B =light(on), and ∆ = {1} in discrete time. Then
CondO,∆ (B | A) captures the learned (or inferred) reliability of the button-to-light connection.

Remark 651. This definition is useful because it remains neutral about how the observer computes
conditionals: from frequencies, from simulation, from mechanistic modeling, or from logical rules.
This neutrality matters for Hyperseed because minds may contain multiple inference processes whose
outputs must be fused (Section 15 discusses such multi-process regimes; see also [19] for a broader
cognitive-systems perspective).

Remark 652 (Empirical instance). In a finite dataset of event tokens, one may estimate CondO,∆ (B |
A) from relative frequencies of co-occurrence of A@t and B@t0 with t0 − t ∈ ∆, separately for pos-
itive and negative evidence streams. We use the abstract operator CondO,∆ so the formalism can
also cover more structured inference.

14.3.2    Attraction
Definition 179 (Attraction). For event types A, B ∈ E and lag window ∆, define the attraction
                                                                        
                AttO,∆ (A, B) := π CondO,∆ (B | A) − π CondO,∆ (B | ¬A) .

This is a real number in [−1, 1].



                                                  288
Remark 653. Attraction is the simplest formal embodiment of the “difference that makes a differ-
ence.” If AttO,∆ (A, B) is positive, then (in the observer’s model) A makes B more plausible than
it would be under ¬A; if it is negative, A suppresses B relative to the ¬A baseline. This is the
formal heart of Hyperseed’s PredictiveAttraction notion (Hyperseed-Concept ??).

Remark 654. A concrete example: let A =water(plant) and B =plant(healthy) within a two-
week lag window ∆. If the model estimates π(Cond(B | A)) = 0.8 but π(Cond(B | ¬A)) = 0.5, then
attraction is 0.3: watering provides a substantial differential lift. Conversely, if a healthy plant is
likely anyway due to rain (0.75 without watering), then even a high absolute conditional (0.8) yields
low attraction (0.05), signaling weak control leverage.

Remark 655. The definition is necessary because control and planning should be built on leverage,
not on mere correlation: if B happens regardless, then A is not a good handle on the world.
Attraction is the low-level quantity that will later be mixed with temporal precedence and simplicity
bias to yield a causal notion (Section 14.5).

Proposition 22 (Basic properties of attraction). For all A, B and ∆:

(a) (Boundedness.) AttO,∆ (A, B) ∈ [−1, 1].

(b) (Negation antisymmetry.) AttO,∆ (¬A, B) = −AttO,∆ (A, B).

(c) (Independence gives zero.) If π(CondO,∆ (B | A)) = π(CondO,∆ (B | ¬A)) then AttO,∆ (A, B) =
    0.

Remark 656. This proposition says that attraction behaves like a signed, normalized measure of
differential predictive influence: it cannot exceed 1 in magnitude, flipping the antecedent to its
negation flips the sign, and if the antecedent makes no difference to the consequent (in the projected
conditional plausibility), attraction vanishes. These are not deep theorems; rather, they are sanity
checks that the formal definition matches the intended conceptual role.

Remark 657. The connection to later material is direct: control strength will be defined using
causal implication, and causal implication will incorporate predictive attraction. Thus, verifying
simple algebraic properties here prevents later definitions from inheriting unintended asymmetries
or scale problems.

Proof. (a) Each term is in [0, 1], hence their difference lies in [−1, 1]. (b) Swap A and ¬A in the
definition. (c) Immediate.

Proof sketch. All three items follow by reading the definition literally. The key observation is that
the projection π maps into [0, 1], so subtraction yields a quantity in [−1, 1], and exchanging A with
¬A simply swaps the minuend and subtrahend, reversing the sign. In slightly more detail: for any
conditional object Cond(· | ·) in the definition, the scalarization π(Cond(· | ·)) is by construction a
real number between 0 and 1. Therefore, any expression of the form π(Cond(B | A)) − π(Cond(B |
¬A)) is automatically bounded below by 0 − 1 = −1 and above by 1 − 0 = 1. Moreover, the
“antisymmetry under negation” is not a separate theorem but a one-line algebraic check:
                                                                                             
        π(Cond(B | ¬A)) − π(Cond(B | ¬¬A)) = − π(Cond(B | A)) − π(Cond(B | ¬A)) ,

using only ¬¬A = A and commutativity of subtraction in the sense of swapping operands.               



                                                 289
Remark 658. The proof works because the definition of attraction is intentionally built from very
rigid pieces: a bounded scalarization followed by subtraction. The “negation antisymmetry” is not
a mysterious logical fact; it is an algebraic symmetry that we engineered into the definition so that
“doing A” and “not doing A” are treated as complementary alternatives. Note that this design
also forces a clear interpretation of the sign: positive attraction means that, after projection, B is
more plausible conditional on A than conditional on ¬A; negative attraction means the opposite;
and attraction near 0 means that A carries little differential information about B compared to its
negation, even if both one-sided conditionals are individually high.
Remark 659 (Why attraction matters). Suppose B is a goal condition and A is an action. Even
if π(Cond(B | A)) is large, taking action A is not very useful if π(Cond(B | ¬A)) is equally large.
Attraction measures the differential predictive value of A for B. This is the basic reason attraction
is closer to the intuitive notion of a “handle” or “lever”: it discounts baseline prevalence of B that
would be present regardless of whether A occurs. In particular, if B is already near-certain in the
background circumstances (so both conditionals project close to 1), then attraction correctly reports
that A adds little, whereas a raw conditional may misleadingly suggest that A is strongly associated
with B.

14.3.3   Predictive implication and predictive attraction
Hyperseed distinguishes ordinary implication from predictive implication (implication plus a tem-
poral precedence constraint). In the present lightweight setting, we simply make this temporal
aspect explicit via ∆. Operationally, ∆ should be read as a fixed prediction horizon: we are
not merely asking whether B is compatible with A, but whether B is expected to occur after A
within a specified window, so that the resulting quantity is tied to forecasting and (later) to action
evaluation.
Definition 180 (Predictive implication and predictive attraction). Define the predictive implica-
tion strength as                                              
                        PImpO,∆ (A, B) := π CondO,∆ (B | A) ∈ [0, 1].
Define the predictive attraction as
                      PAttO,∆ (A, B) := PImpO,∆ (A, B) − PImpO,∆ (¬A, B).
Remark 660. Here PImpO,∆ (A, B) is the one-sided, probability-like strength of the forward con-
ditional “A predicts B within ∆” (after projection). It is intentionally not yet causal: it does not
require that A precedes B typically in the stronger sense, nor that there be any intensional connec-
tion. Predictive attraction PAtt then restores the differential stance by contrasting A against ¬A.
One can also view PImp as a score assigned to the ordered pair (A, B), whereas PAtt is a score
assigned to the contrast between two rival predictors, A and ¬A, holding B fixed. This contrastive
structure is what makes PAtt more stable as a decision signal in settings where the background rate
of B fluctuates across contexts.
Remark 661. Example: if a smoke detector rings (A) then a person wakes up (B) with high
conditional plausibility, say PImp = 0.9. But if the person would wake anyway because of a loud
storm even without the detector (PImp(¬A, B) = 0.85), then PAtt = 0.05. The model is saying:
the detector is a good predictor but a weak lever. This distinction becomes crucial once we interpret
A as an action or intervention candidate in control. The same arithmetic also clarifies the limiting
cases: if PImp(¬A, B) ≈ 0, then PAtt ≈ PImp(A, B) and the action-like reading of A becomes
more credible; if PImp(A, B) ≈ PImp(¬A, B), then PAtt ≈ 0 and A provides little incremental
predictive advantage even if the absolute prediction is strong.

                                                 290
Remark 662 (Relationship to attraction). With the above definitions, PAttO,∆ (A, B) = AttO,∆ (A, B).
We keep both notations because (i) the ontology uses both; and (ii) in richer formalisms one may
separate “mere conditional dependence” from “dependence with a specific temporal semantics.” In
particular, future refinements may encode the ∆-constraint in the conditional object itself (e.g., as
an event construction) rather than as an external parameter, at which point it can become useful
to reserve Att for an atemporal notion and PAtt for the explicitly forward-looking notion used in
prediction and control.

Remark 663. This duplication of notation is philosophically telling: in the minimal formalism,
the concepts coincide; in richer settings, they may come apart. It is often fruitful in foundational
work to keep two names for what is presently the same quantity, if one expects later refinements to
split the notion along different conceptual joints (as happens below when we separate extensional
from intensional predictive attraction). Concretely, one expects such a split once the formalism
distinguishes (a) extensional regularities in observed sequences and (b) intensional linkages that
support counterfactual and interventional reasoning. The present section keeps the arithmetic sim-
ple, but the duplicated naming convention acts as a reminder that the surrounding interpretation
can change even when the underlying number happens to be computed by the same formula at this
stage.

Remark 664 (Range and interpretive calibration). Because PImpO,∆ (A, B) ∈ [0, 1] by definition,
it follows immediately that PAttO,∆ (A, B) ∈ [−1, 1]. The endpoints have a clear meaning: PAtt = 1
occurs only when PImp(A, B) = 1 and PImp(¬A, B) = 0, i.e., A perfectly predicts B within ∆ and
¬A perfectly predicts ¬B within the same horizon (after projection); PAtt = −1 reverses these
roles. Intermediate values can be read as a signed “margin” of predictive advantage, and the sign
convention is fixed so that PAtt > 0 favors A over ¬A as a predictor for B.

Remark 665 (Dependence on the projection π). The role of π is to force a common numeric
scale for comparison, independent of the internal representation of CondO,∆ (B | A). This makes
the subtraction in PAtt well-typed and ensures boundedness, but it also means that the qualitative
behavior of PImp and PAtt is sensitive to how π treats uncertainty, indeterminacy, or graded
evidence. Accordingly, later sections can change the empirical behavior of predictive attraction
either by changing the conditional object Cond or by changing the projection π, without changing
the surrounding algebraic facts used above.

14.4    Sequential and parallel temporal composition
Hyperseed emphasizes that predictive dependence concepts should compose along time. In the
original ontology this is expressed using operators such as SequentialAND, SimultaneousAND, and
SimultaneousOR. Here we sketch one clean way to realize this using the quantale and enriched-
category machinery from Section 3.4.

Remark 666. The guiding intuition is that a mind rarely reasons about isolated one-step predic-
tions. It reasons about chains (if I do this, then that happens, then something else becomes possible)
and about bundles (multiple conditions jointly supporting a later outcome). Quantales provide a
compact algebraic language for this kind of composition: a tensor ⊗ aggregates along a sequence,
and a join ⊕ aggregates across alternatives. This style is consonant with the pattern-web ma-
chinery used earlier (Sections 9 and 12) and foreshadows later planning/optimal-control principles
(Section 26; see [21]).



                                                 291
14.4.1   Sequential composition as quantale multiplication
Let E be viewed as a set of “states” or “event-conditions” and suppose the observer has a p-bit-
valued predictive relation

                    RO,∆ : E × E → [0, 1]2 ,     RO,∆ (A, B) := CondO,∆ (B | A).

If we interpret RO,∆ (A, B) as an “edge weight” from A to B, then sequential composition of two
predictive steps corresponds to relational composition, with the quantale tensor as the multiplicative
aggregator.
Remark 667. Notation unpacking: RO,∆ is a V -valued relation (here V = [0, 1]2 with p-bit op-
erations), so RO,∆ (A, B) is the edge weight from A to B. The symbol ⊗ is the quantale tensor
(multiplicative aggregation along a path), and ⊕ is the quantale join (additive aggregation across
alternative intermediate nodes). This is the same algebraic pattern used in enriched-category com-
position, but here read operationally as “compose predictions across time.”
Definition 181 (Two-step predictive composition). Define the composite relation
                                           M
                  (RO,∆ ◦ RO,∆0 )(A, C) :=     RO,∆ (A, B) ⊗ RO,∆0 (B, C),
                                                B∈E

where ⊗ and ⊕ are the tensor and join of the p-bit quantale (Section 3.4).
Remark 668. This is the familiar “sum over intermediates, multiply along edges” pattern, gen-
eralized from classical probability or weighted automata to the p-bit quantale setting. One may
visualize E as nodes in a directed graph of event-types; then (R ◦ R0 )(A, C) aggregates the strength
of all two-step paths A → B → C.
Remark 669. A simple example: if A predicts B strongly and B predicts C strongly, then the
tensor R(A, B) ⊗ R0 (B, C) yields a strong composite for that B. If there are multiple plausible
bridges B, the join ⊕ allows them to compete/cooperate depending on the quantale’s join. This
definition is useful because it makes explicit what is often left informal in planning discussions: the
semantics of chaining predictions is not automatic; it is a chosen algebra.
Remark 670 (Reading). The join ⊕ aggregates over intermediate events B (“there exists a rea-
sonably good bridge”), while the tensor ⊗ aggregates evidence across a temporal chain (“both steps
work”). This is the algebraic content behind the informal operator SequentialAND.

14.4.2   A tiny worked schematic
Consider an action sequence (cf. the ontology’s example):

    Teacher says fetch → I get the ball → I bring the ball → I get a reward.

If each arrow has a predictive implication strength (in [0, 1] after projection π), then the overall
sequence can be given a composite strength by multiplying along the chain (tensor) and joining
over alternative intermediate paths. Predictive attraction then compares the “do the sequence”
case with the “do not do the sequence” case, exactly as in the single-step definition.
Remark 671. Even this schematic illustrates an important philosophical point: “the plan works”
is not a primitive fact but a compositional judgment assembled from local predictive regularities.
The Hyperseed approach tries to keep such judgments graded and evidence-sensitive, so that a plan
may be adopted with appropriate humility rather than with binary certainty.

                                                 292
14.5     Causality as attraction plus temporal precedence plus simplicity bias
The ontology proposes that causality is not captured by extensional dependence alone. Rather,
causal judgments combine: (i) a temporal precedence constraint; (ii) a surprising extensional de-
pendence (predictive attraction); (iii) an intensional (property-level) connection; and (iv) a sim-
plicity/weakness bias.
    These four ingredients are meant to be read as jointly necessary for the ordinary, practice-guided
use of “cause” in modeling and intervention. Temporal precedence rules out purely symmetric
associations as candidates for causal direction; predictive attraction encodes the idea that causes
provide leverage beyond background expectations; intensional linkage encodes the idea that the
dependence should be mediated by comparatively stable properties rather than arbitrary labels;
and the simplicity/weakness bias resolves underdetermination by preferring causal stories that
introduce as little representational “force” as possible.
Remark 672. Temporal precedence here is a constraint on admissible directionality rather than a
full dynamical model: it says that if A is judged a cause of B at resolution ∆, then the dependence
must be expressible with A occurring “before” B in the observer’s discretization. This keeps the
causal notion compatible with the predictive setup (which is indexed by ∆) while allowing that
different observers—or the same observer at different time scales—may legitimately report different
causal relations when the ordering becomes ambiguous at coarse granularity.
Remark 673. The simplicity/weakness bias is not merely aesthetic. It functions as a regularizer
on causal attribution: among multiple hypotheses that fit extensional predictive facts equally well,
prefer the one that commits to weaker predicates, fewer special cases, and less brittle boundary
drawing. In the Hyperseed framing, this is the same pressure that, in other contexts, selects simpler
patterns as better compressive descriptions, but here it is applied to causal predicates and their
associated intervention rules.
Remark 674. This cluster deliberately echoes several long-standing tensions in philosophy of sci-
ence: Humean regularity (extensional dependence) is not enough for the lived concept of cause; yet
pure metaphysical necessity is too heavy a tool for scientific practice. Hyperseed’s compromise is
operational: define causality as a structured kind of predictive leverage, constrained by time and
guided by an Occam-like preference for weak distinctions (Hyperseed-Concept 202, and in the quan-
tale form, Hyperseed-Concept 143). For related discussions of weakness as a central organizing
principle, see [2, 3].

14.5.1    Extensional and intensional predictive attraction
Definition 182 (Extensional predictive attraction). The extensional predictive attraction is the
predictive attraction computed on the level of occurrence of event types:

                                  PAttext
                                      O,∆ (A, B) := PAttO,∆ (A, B).

Remark 675. Calling this “extensional” emphasizes that it looks only at the surface fact of whether
A and B occur, not at what internal structure A and B may have as patterns or bundles of proper-
ties. In many empirical settings, extensional attraction is the easiest to estimate directly from time
series data, and so it often serves as the first approximation to causal influence.
Remark 676. One can also read PAttext     O,∆ (A, B) as a statistic of type-level tokens: it aggregates
over the observer’s instances of A and asks whether B is enriched in the future of those instances
relative to an appropriate baseline. In this sense it is closer to population-level causal evidence than

                                                  293
to a single mechanistic explanation; it answers “does A carry predictive leverage about B?” rather
than “through which internal channel does A bring about B?”
Remark 677. Example: if we take A =take(aspirin) and B =headache(reduces), extensional
attraction asks only whether the aspirin-token tends to be followed by a reduction-token, compared
to the baseline where aspirin is not taken.
Remark 678. The same example also illustrates why extensional attraction alone is not the full
causal story: the observed dependence might be mediated by confounders represented (or not repre-
sented) by O, by selection effects in when aspirin is taken, or by hidden structure within the event
types (dose, timing, severity). The role of the intensional layer below is to make explicit some of
the within-type structure that can stabilize causal attribution across contexts.
   To define the intensional counterpart we use the property machinery from Section 9. Recall that
the property set of an entity/event is the fuzzy set of patterns in it, weighted by pattern intensity
(Hyperseed-Concept 130).
Definition 183 (Property events). Fix a finite “property basis” P (patterns-as-properties) and
a map PropO : E → [0, 1]P . For p ∈ P we write p ∈O A for the derived “property event type”
“pattern/property p is present in A” and set

                                π(p ∈O A) := PropO (A)(p) ∈ [0, 1].

Remark 679. Notation unpacking: P is a set of properties (implemented as patterns), and PropO (A)
is a function P → [0, 1] assigning each property p an intensity for event type A. The expression
p ∈O A is not literal set membership but a derived event type whose plausibility is defined to be
PropO (A)(p). The subscript O again signals observer-relative representation.
Remark 680. The requirement that P be finite is a pragmatic restriction that matches how an
observer/model typically operates: causal claims are made in a bounded vocabulary of features,
measurements, or patterns. Technically, finiteness ensures that the averaging constructions below
are unproblematic, while conceptually it emphasizes that intensionality is always relative to a chosen
representational basis (which may be expanded when the observer learns new patterns).
Remark 681. Intuitively, this turns “A has property p” into something that can be fed back into
the same predictive machinery used for ordinary events. For example, if A is fire(burning) and
p is the pattern/property hot, then π(p ∈O A) is the degree to which the observer’s representation
of the event-type includes hotness. This is useful because it lets us ask not only whether A predicts
B, but whether the properties characteristic of A predict the properties characteristic of B.
Remark 682. In particular, property events let the same observer represent two different “internal
decompositions” of the same extensional event type. For instance, the event type take(aspirin)
may include properties such as dose(large) or dose(small) with different intensities in different
subpopulations or contexts. If those properties have different downstream predictive signatures, the
intensional analysis can distinguish them even when the extensional event label is the same.
Remark 683. The purpose of introducing property events is theoretical: it provides a bridge between
the “pattern as compressive description” view (Section 9) and causal judgments, by allowing causal
dependence to be sensitive to intensional structure rather than only to extensional co-occurrence.
This is one way to formalize the thought that causation should reflect not merely what happens, but
something about why it happens, insofar as “why” is accessible to the observer’s representational
vocabulary.

                                                 294
Remark 684. A further benefit is robustness under redescriptions: if two event types are extention-
ally similar but differ in property profile, then extensional attraction may be unstable across shifts in
data collection or coding, while intensional attraction can remain informative provided P captures
the stable aspects of the phenomenon. Conversely, if P omits the relevant mechanistic properties,
then the intensional score will collapse back toward an extensional proxy, which is appropriate: the
observer cannot legitimately claim a structured causal story without the representational capacity
to express it.

Definition 184 (Intensional predictive attraction). Define the intensional predictive attraction by
averaging predictive attraction over properties:
                                        XX
                     PAttint
                          O,∆ (A, B) :=          wp,q PAttO,∆ (p ∈O A, q ∈O B),
                                         p∈P q∈P

where wp,q ≥ 0 are weights that may be chosen, for example, proportional to PropO (A)(p) PropO (B)(q)
and normalized to sum to 1.

Remark 685. The weights wp,q implement a choice about what it means for a property-level linkage
to be “about” A and B. Taking wp,q ∝ PropO (A)(p)PropO (B)(q) focuses the average on properties
that are actually present in the two event types, while still allowing rare but highly diagnostic
properties to matter if their associated PAtt terms are large. Other weighting schemes are possible
(e.g. emphasizing only properties of A, or penalizing very common q to reduce trivial predictability),
and can be understood as different observer policies for extracting mechanistically meaningful signal
from the same raw dependence statistics.

Remark 686. This definition says: look at all property pairs (p, q), measure how much the presence
of p in A predicts the presence of q in B (differentially, via PAtt), and then average these numbers
with weights wp,q emphasizing the properties actually salient in A and B. The result is a single
scalar capturing structured, property-level predictive linkage.

Remark 687. When P contains a very coarse property corresponding to the event’s own occurrence
(or a near-indicator pattern that tracks it), the intensional construction can recover the extensional
one as a special case: the average places most of its mass on the indicator-like property pair and
PAttint                           ext
     O,∆ (A, B) approaches PAttO,∆ (A, B). This provides a consistency check: intensional attrac-
tion refines extensional attraction rather than replacing it with an unrelated quantity.

Remark 688. A simple schematic example: let A be strike(match) and B be fire(ignites).
If properties like friction and heat are strongly present in A, and properties like heat and light
are present in B, then property-level attractions such as PAtt(friction ∈O A, heat ∈O B) and
PAtt(heat ∈O A, light ∈O B) should be positive, raising PAttint (A, B).

Remark 689. In that match example, the intensional score is closer to what one informally calls
a mechanism: it does not merely say that the labels strike(match) and fire(ignites) are statis-
tically associated, but that specific properties characteristic of striking (e.g. friction) are linked to
specific properties characteristic of igniting (e.g. heat). This is also where the simplicity/weakness
bias interacts with intensionality: if two candidate causal explanations fit the extensional data, the
preferred one is the one whose property linkages can be expressed with fewer and weaker distinguish-
ing properties (for example, a small, stable set of features rather than a highly conjunctive, brittle
property list).



                                                   295
Remark 690. This notion is useful because it can distinguish between (i) brute co-occurrence and
(ii) co-occurrence mediated by shared structure in the observer’s vocabulary of patterns-as-properties.
In complex systems, many correlations are accidental; intensional attraction is one principled way
to bias causal inference toward correlations that align with stable internal descriptions (cf. [5] on
hierarchical/ heterarchical pattern structure).
Remark 691. A further intuition is that “shared structure” should be understood as invariance un-
der reasonable changes of presentation: if the observer refines, factorizes, or re-encodes a situation
using roughly equivalent internal predicates, genuinely causal linkages should remain expressible with
similar property-level dependencies. By contrast, accidental correlations often disappear under such
re-descriptions because they do not correspond to a stable pattern-level relation in the observer’s
representational scheme.
Remark 692 (Interpretation). PAttint is high when the properties of A (as patterns) tend to
predict the properties of B. This captures the intuitive idea that a causal connection is not merely
a statistical regularity, but reflects a structured relationship between what A is like and what B is
like.
Remark 693. In particular, PAttint is meant to be sensitive to “mechanism-shaped” features: even
if A and B co-occur frequently, intensional attraction should increase only when the mapping from
salient attributes of A to salient attributes of B is compressible in the observer’s property language
(e.g. the same few properties of A explain many properties of B). This helps separate mere proxy
variables from variables that participate in a coherent descriptive pipeline.

14.5.2   Causal implication and simple causal implication
Definition 185 (Causal implication). Fix a lag window ∆ and a mixing parameter λ ∈ [0, 1].
Define the causal implication strength
         CImpO,∆ (A, B) := λ σ(PAttext                            int
                                                                             
                                      O,∆ (A, B)) + (1 − λ) σ(PAttO,∆ (A, B)) · 1[A ≺ B],

where 1[A ≺ B] is an indicator that A typically precedes B in the relevant context, and σ : [−1, 1] →
[0, 1] is the affine rescaling σ(x) = (1 + x)/2.
     Define also the strong (product) variant
                CImp×                   ext               int
                    O,∆ (A, B) := σ(PAttO,∆ (A, B)) σ(PAttO,∆ (A, B)) 1[A ≺ B].

Remark 694. One can read λ not only as “trust in statistics” versus “trust in structure,” but also
as a tuning between two kinds of robustness: extensional attraction can be robust to vocabulary drift
(it depends less on how properties are named) but brittle under distribution shift, whereas intensional
attraction can be robust across contexts where the same mechanism holds but brittle under changes
in the observer’s property set. The mixture is therefore an explicitly observer-relative compromise.
Remark 695. Notation unpacking: σ converts a signed attraction in [−1, 1] into a [0, 1] score,
so that negative attraction maps below 1/2 and positive attraction maps above 1/2. The indicator
1[A ≺ B] enforces temporal direction: even a strong predictive linkage does not count as causal
implication if A does not typically precede B in the observer’s time-ordering.
Remark 696. The affine rescaling is chosen so that a “neutral” attraction of 0 maps to 1/2, which
functions as a convenient baseline when combining multiple sources of evidence. In particular, the
product variant then has the interpretation that a neutral score in either extensional or intensional
attraction yields a mid-level contribution, while strongly negative attraction in either channel pushes
the overall score downward even when the other channel is strong.

                                                 296
Remark 697. Intuitively, CImpO,∆ (A, B) is a compromise between two ideas of cause: “A makes B
happen (extensional leverage)” and “A is connected to B through properties the observer recognizes
(intensional structure).” The parameter λ expresses how much the observer (or modeling choice)
trusts extensional statistics versus property-level structure.

Remark 698. The two variants also correspond to different stances on “defeaters.” In the sum
form, a strongly mechanistic-looking intensional linkage can partially rescue a weak extensional
signal (e.g. when the available samples are sparse), and conversely strong extensional predictability
can partially rescue an immature vocabulary. In the product form, either channel can act as a
defeater: if the observer cannot express a stable property-level relation, or if extensional evidence
is strongly negative, then causal implication is suppressed.

Remark 699. A simple example: in a world where barometers correlate with storms, extensional
attraction PAttext (barometer(low), storm) may be high. But the intensional attraction might be
low if the properties of barometer(low) do not structurally connect to the properties of storms in
the observer’s mechanistic vocabulary. The mixing/product choices then control whether barometer
readings are treated as causes or merely predictors.

Remark 700. The same distinction shows up in “common cause” settings: a hidden atmospheric-
pressure variable may generate both barometer(low) and storm, producing high extensional attrac-
tion, while a mechanistic vocabulary that explicitly represents pressure as an intermediate property
could raise intensional attraction for pressure(low)→storm and reduce it for barometer(low)→storm.
Thus, intensional attraction can be interpreted as a bias toward models that expose plausible inter-
mediates in the observer’s descriptive hierarchy.

Remark 701 (Temporal precedence as a statistic). One may implement A ≺ B in many ways, e.g.
as a thresholded statistic computed from the same occurrence data used for CondO,∆ : conditional
on co-occurrence of A and B within a broad window, the median (or mean) lag lag(A, B) is positive.
The ontology treats precedence as context-relative (observer-relative time and event boundaries), so
this indicator should be understood as relative to O.

Remark 702. The role of the lag window ∆ is to encode a causal timescale hypothesis: if ∆
is too small, genuine delayed effects will be missed; if it is too large, unrelated events may be
treated as eligible for precedence tests, washing out directionality. In practice, one can treat ∆
as a hyperparameter and evaluate sensitivity of CImpO,∆ to its choice, which is itself a kind of
“simplicity” consideration (prefer time-scale assumptions that do not require fine-tuning).

Remark 703 (Sum vs product). The “sum” form aligns with the ontology’s SimpleCausalImplication
intuition (a weighted average of extensional and intensional aspects), while the “product” form
aligns with the ontology’s CausalImplication intuition (both aspects must be simultaneously strong).

Remark 704. In a decision-theoretic reading, the sum form behaves more like an expected-evidence
aggregator (useful for ranking many candidate causes when evidence is heterogeneous), while the
product form behaves more like a conjunction of tests (useful when one wants high precision and is
willing to sacrifice recall). This difference matters when causal implication is later used for control:
permissive attribution can increase exploratory interventions, whereas severe attribution can reduce
spurious control attempts.

Remark 705. The product form is, in a sense, more severe: it demands that extensional and
intensional evidence cohere. The sum form is more permissive: it allows a cause to be inferred
from strong extensional leverage even if the property vocabulary is impoverished, or from strong

                                                  297
intensional coherence even if the raw statistics are noisy. This mirrors a practical tradeoff in
scientific reasoning between mechanistic understanding and purely statistical prediction (cf. [20]
for a related philosophy of science stance).
Remark 706. Edge cases help clarify interpretation: if 1[A ≺ B] = 0 then both scores are 0,
making the temporal ordering a hard gate rather than a soft preference. If λ = 1 then CImpO,∆
reduces to a purely extensional, precedence-gated score; if λ = 0 it reduces to a purely intensional,
precedence-gated score. Thus the definition contains, as limiting cases, both a Granger-like “pre-
diction with time-order” notion and a more structural “mechanism in the observer’s vocabulary”
notion.

14.5.3   Weakness-biased causal model selection
Causal attribution is also biased by simplicity. In the Hyperseed formal core, simplicity is tracked by
weakness (Section 3.7): all else equal, prefer explanations that make fewer special-case distinctions
(Hyperseed-Concept 169, Hyperseed-Concept 202).
Remark 707. This is an explicitly Russellian move: when two descriptions fit the appearances
equally well, prefer the one that posits fewer independent discriminations. In Hyperseed, this pref-
erence is not only a methodological maxim but is formalized via quantale weakness measures [3, 2].
The result is that causal inference becomes a kind of model selection under a simplicity prior, rather
than a mere reading-off of correlations.
Remark 708. Here “fewer special-case distinctions” can be read operationally as: fewer con-
ditional branches, fewer context-specific parameters, fewer ad hoc predicates, or fewer exception
clauses required to maintain predictive adequacy across the contexts recognized by O. Importantly,
weakness is not merely “small cardinality” of S; it concerns the complexity of the description of
the explanation, so that a slightly larger parent set may still be weaker if it enables a more uniform
rule.
Definition 186 (Weak causal parent selection (schematic)). Fix a target event type B. Let C be a
finite set of candidate causes. A causal parent set is a subset S ⊆ C. Define a score

            Score(S → B) := Fit(S → B)                               +η Weak(S → B) ,
                            |    {z  }                                  |    {z   }
                               predictive adequacy                       simplicity/weakness

where η > 0 is a tradeoff parameter. A weak causal explanation for B is a parent set S ∗ maximizing
this score.
Remark 709. The separation into Fit and Weak is intended to parallel standard regularization:
Fit rewards predictive performance (e.g. likelihood, reduction in uncertainty, or improvement in
CondO,∆ -style predictability when conditioned on S), while Weak acts like a simplicity prior (e.g.
a penalty for representational complexity, or a reward for compressibility). The hyperparameter
η therefore controls how readily the observer trades marginal predictive gains for a simpler causal
story.
Remark 710. Although presented schematically, this parent-selection view connects back to CImpO,∆ :
one can treat CImp (or CImp× ) as a primitive pairwise signal used to generate C (screening can-
didates), and then use weakness-biased selection to choose a multivariate explanation that resolves
redundancy among candidates (e.g. when several correlated Ai compete as apparent causes of the
same B). In that role, weakness functions as a bias toward selecting upstream or more “explanato-
rily central” parents when multiple nearly equivalent predictors exist.

                                                     298
Remark 711. This definition is deliberately schematic: it isolates the form of the causal selection
rule without committing to a particular Fit or Weak. Conceptually, it says that causality is not a
single number but an optimization: we search for a set of antecedents that both predict B and do
so without excessive complexity. In particular, the definition is meant to be read as a regularized
model-selection principle: among many candidate antecedent-sets S that could be placed “before” B
in the relevant sequence, we prefer those that score well under Fit while paying an explicit penalty
(or softness constraint) measured by Weak. This keeps the notion of “cause” distinct from mere
association, since high association achieved only by ad hoc, highly brittle conditions is treated as
less causal under the same observational data. The temporal-precedence component is encoded by
restricting attention to candidates that occur in the antecedent portion of Seq(S) relative to B, so
that the optimization is not over arbitrary correlates but over prospective parents in the temporal
(or otherwise directed) ordering.
Remark 712. A simple example (in outline): suppose B is alarm(rings), and the candidate
causes C include smoke, steam, and dust. A high-fit but overly specific rule might include a long
conjunction of rare conditions; a weaker (simpler) rule might treat smoke as the primary parent
because it captures most of the predictive signal with fewer special cases. The parameter η governs
how aggressively the observer prefers such simplicity. One can view this as preferring a small, stable
explanatory “core” over an arbitrarily detailed exception list: e.g. a contrived rule like (smoke AND
weekday AND sensor A AND NOT window open AND ...) may fit a limited dataset extremely well
while generalizing poorly, whereas smoke alone may capture most of the predictive mass across
contexts. In this toy scenario, steam might be a frequent correlate in kitchens (thus sometimes
predictive) but also a common benign source of false alarms, and dust might correlate with sensor
noise in certain rooms; the weakness term is intended to suppress treating such context-fragile
correlates as “the cause” unless the added distinctions genuinely buy enough predictive performance
to justify the added complexity. The role of η is then analogous to a regularization strength: small
η permits richly contextual causes when the fit gain is large, while large η pushes toward more
parsimonious parent-sets even at some cost in fit.
Remark 713. This is useful for the broader theory because it harmonizes with later “Wu Wei”
optimization: the same weakness bias that prefers simple causal stories can also prefer minimally
contrived control policies (Section 26; Hyperseed-Concept 206, 207; see [21]). It also connects to
general tradeoff-theorem thinking about balancing dependency, fit, and complexity [9]. In other
words, the same mathematical knob that discourages baroque explanatory structure also discourages
baroque interventions: both “overfitted explanations” and “overengineered controls” can be seen
as solutions that achieve a target outcome only by relying on an excessive number of finely tuned
distinctions. When the observer (or agent) is constrained to prefer weaker descriptions, it tends to
select causal parents that are robust across contexts, and likewise tends to select policies that succeed
without requiring a long list of special-case contingencies. This is precisely the sense in which a
shared simplicity/weakness bias can provide a unifying regularity principle across prediction (which
antecedents matter?), causality (which antecedents count as parents?), and control (which actions
achieve outcomes without contrivance?), making the later Wu Wei criteria appear less as a separate
doctrine and more as the control-theoretic face of the same selection rule.
Remark 714 (What “Fit” and “Weak” may be). There are many concrete instantiations. For
example, Fit may be the projected predictive implication π(Cond(B | Seq(S))) or a negative log-
loss; and Weak may be a quantale weakness of the distinctions needed to state the conditional “B
depends on S” (e.g. a description-length proxy or a partition-based weakness of contexts). The
point is the structure: causality is not “just statistics” but statistics plus an Occam-like bias. Con-
cretely, Fit can be read as any score that rewards accurate forecasting of B from the antecedent

                                                  299
sequence, including likelihood-based criteria, proper scoring rules, or information-theoretic depen-
dence measures so long as they increase when S makes B more predictable in the intended sense.
Likewise, Weak is intentionally permissive: it may be instantiated as an MDL-style codelength of
the rule, a complexity of the partition of contexts required to make the rule true, a penalty on the
number of conjuncts/clauses, or a more semantic notion of “how many distinctions the observer
must track” to use the conditional reliably. The quantale phrasing is meant to allow weakness to
compose and compare across heterogeneous kinds of distinctions (e.g. temporal, contextual, and rep-
resentational), rather than restricting it to a single numeric proxy. Under any such instantiation,
the selection principle can be read as: choose parents that are predictive and that can be stated and
applied with a small, reusable inventory of distinctions, thereby building temporal precedence and
simplicity directly into the operational meaning of “cause.”

14.6    Control, control hierarchies, and perceptual hierarchies
Hyperseed’s slogan is: control is systematic causation. We formalize this by treating control as
causal implication where the antecedent is an intervention/action variable (Hyperseed-Concept
87). In this framing, “systematic” emphasizes repeatability across relevant contexts: a controller
is not defined by a single lucky coincidence but by a stable mapping from doable antecedents
to downstream consequences. The use of causal implication rather than mere co-occurrence is
meant to exclude cases where A and G happen to correlate due to a common cause, and to favor
cases where actively setting or instantiating A would (in the model) make G more likely. The
context parameter O and lag window ∆ are therefore not incidental bookkeeping: they encode what
background conditions are held fixed and what temporal scope is treated as the “effect horizon” of
action.
Definition 187 (Actions, goals, and control strength). Let A ⊆ E be a designated set of action
event types. Let G ∈ E be a goal condition (or a conjunction/disjunction of such). For A ∈ A
define the control strength of A over G as

                                CtrlO,∆ (A → G) := CImpO,∆ (A, G).

Remark 715. The formal move is simple: we do not invent a new scalar for control; we reuse
causal implication, restricted to antecedents interpreted as actions or interventions. Philosophically,
this encodes the idea that agency is not an extra substance added to the world, but an organizational
stance toward certain event types as doable (actions) and certain event types as desirable (goals).
A technical advantage of this reuse is that any refinements already built into causal implication
(e.g. sensitivity to temporal precedence, background context O, and windowing by ∆) carry over
automatically to control: what counts as “the same action” and what counts as “achieving the goal”
are evaluated inside the same event-type and context machinery.
Remark 716. Example: if A =turn(key) and G =engine(starts), then Ctrl(A → G) is high
precisely when turning the key differentially raises the plausibility of starting the engine, does so
with temporal precedence, and (optionally) aligns with intensional property connections. This is
useful because it makes control a graded quantity, allowing partial control and contested control (e.g.
conflicting evidence about whether the key mechanism is functional). A further benefit of grading
is comparative evaluation: if {Ai } are alternative actions, then control strengths Ctrl(Ai → G)
provide a principled way to rank actions by their expected goal-directed causal leverage under the
same context and lag assumptions. In that sense, the definition is compatible with (but does not
itself impose) decision-theoretic selection rules such as choosing an A that maximizes control subject
to costs or constraints.

                                                 300
Remark 717. Although the definition is written for a single antecedent A, many control situations
are sequential: a policy is a temporally extended pattern of actions. One can model such cases
by letting A denote a composite event type (e.g. a short action script within ∆) or by applying
the definition to intermediate subgoals G1 , G2 , . . . that are chained together. This keeps the basic
notion of control strength intact while allowing hierarchical decomposition of complex tasks into
locally controllable steps.
Definition 188 (System-level control). Let U and V be groupings of event types (subsystems,
modules, or coarse variables). We say U controls V (in context O with lag window ∆) if there exist
A ∈ U ∩ A and B ∈ V such that CtrlO,∆ (A → B) exceeds a chosen threshold.
Remark 718. This lifts control from individual event types to coarse subsystems: “U controls V”
means that something in U, construed as an action, exerts sufficiently strong causal implication
toward something in V. The threshold is a modeling choice, reflecting how strict we wish to be
in calling a relation “control” rather than “influence.” Because the definition uses an existential
quantifier, it captures the minimal claim that some action-like degree of freedom in U can steer some
event type in V; stronger notions (sometimes useful in engineering) would replace “there exists”
with requirements like “for many B ∈ V” or would aggregate via maxA∈U ∩A maxB∈V Ctrl(A → B)
to define a graded inter-module control strength.
Remark 719. Example: let U be motor-command events and V be arm-position events. Then
system-level control holds if there exists a motor command that reliably steers the arm. In more
abstract cognitive systems, U might be an executive module and V a memory module; the definition
then captures the idea that executive actions can gate or modulate memory states. This kind of
modular control analysis is widely used in cognitive architectures (cf. [19]). In both examples, the
window ∆ implicitly distinguishes fast, direct effects (a command changes position within tens of
milliseconds) from slower, mediated effects (a command changes posture after a sequence of reflex
loops). Choosing ∆ therefore selects what counts as “the controlled variable” at the scale of interest.
Remark 720 (Asymmetry and bidirectionality). Nothing forces control to be symmetric. One
may have U controlling V without V controlling U. Bidirectional control corresponds to feedback
coupling. In feedback-coupled systems, bidirectionality is common: U may act on V while V supplies
observations or error signals that modulate subsequent actions in U. The present definition is
deliberately agnostic about stability and optimality: it identifies the presence of causal leverage,
not whether the resulting closed-loop dynamics converge, oscillate, or diverge. Those dynamical
questions can be layered on top by analyzing control strengths across multiple lags or across recurrent
cycles.
Definition 189 (Control hierarchy). A control hierarchy is a partial order (M, <) on a family
of modules M such that M1 < M2 is aligned with “M1 has (potentially asymmetric) control over
M2 .”
Remark 721. The term “hierarchy” is used in the order-theoretic sense: < is a partial order, so it
need not compare every pair of modules. This accommodates heterarchical organization (Hyperseed-
Concept ??) where some modules are incomparable or form local loops, while still capturing a global
tendency for some modules to sit “above” others in the sense of exerting more control (Hyperseed-
Concept 88). Operationally, one can imagine estimating pairwise system-level control relations
(possibly at different thresholds or different ∆) and then taking the transitive closure to obtain an
ordering over modules. When mutual control is pervasive, it is often useful to treat strongly mutually
controlling clusters as equivalence classes, so that the partial order applies between clusters rather
than insisting on antisymmetry between tightly coupled components.

                                                 301
Remark 722. A simple example is a two-level robot controller: a high-level planner module Mplan
chooses goals and sequences, and a low-level motor module Mmotor executes them. Then Mplan <
Mmotor . In biological or cognitive settings, such a clean order may not exist globally; using a partial
order rather than a total order respects this. One also frequently encounters multi-level cases where
Mplan controls not the motor plant directly but the parameters of lower controllers (gains, setpoints,
task constraints), while lower controllers control moment-to-moment actuator outputs. The partial-
order notion is intended to cover both “direct command” and “parameter-setting” as varieties of
control, so long as they show up as strong causal implication from action-like events in the higher
module to state changes in the lower one.

Remark 723. This definition is useful because it gives a formal handle on a pervasive explana-
tory motif: many systems are organized so that some processes constrain or parameterize others.
Later sections revisit this motif under attention allocation and cognitive synergy, where control of
resource flow is as important as control of external actions. A further motif is abstraction: higher
modules often act over coarser variables and longer time horizons, while lower modules act over
finer variables and shorter time horizons. The parameters (O, ∆) can be chosen to reflect this scale
separation, so that “higher controls lower” is not merely a metaphor but corresponds to measurable
differences in what kinds of event types are treated as actions, what kinds of event types are treated
as goals, and over what temporal windows the causal implications are evaluated.

Definition 190 (Perceptual hierarchy). A perceptual hierarchy is a control hierarchy in which
the relevant control events are instances of pattern recognition (Section 13): controlling a module
consists in selecting, stabilizing, or transforming the patterns it registers.

Remark 724. This definition treats perception as a special case of control: higher levels “control”
lower levels by constraining what patterns are recognized, amplified, or suppressed. It thereby links
representation (Section 13) with action: to perceive is to enact a selection among possible organi-
zations of the incoming stream (Hyperseed-Concept 133). Concretely, “control” here can be realized
by mechanisms such as attentional gating, adaptive thresholding, top-down priming, or predictive
templates that bias which hypotheses the lower module considers. On this view, a higher perceptual
level does not merely read a fixed set of features; it can actively shape the feature space and the
salience landscape, thereby changing what the lower level will count as a match on subsequent inputs.
This is especially clear in ambiguous stimuli, where stabilizing one interpretation over another is
itself a form of goal-directed regulation of internal state, even if no overt motor action is taken.

Remark 725. Example: in vision, a high-level hypothesis like face-present can bias lower-level
feature detectors to stabilize edge/texture patterns consistent with a face; conversely, ambiguous
low-level features may fail to stabilize any high-level pattern. In the present formalism, such biasing
is represented abstractly as control relations among modules whose event types include recognition
events. This is consonant with active-perception and predictive-processing intuitions, while not
committing to a particular neural implementation.
    The point of phrasing this as a control relation is that the “top–down” influence is treated as
a directional constraint on which downstream events are made more (or less) likely to occur in a
stable way, rather than as a mere correlation. In particular, a recognition event at a higher layer
functions as a context-setting signal: it changes which lower-level event sequences are admissible
(or evidentially supported) as the system settles into an interpretation. Conversely, persistent
instability at the lower layer can be read as a failure to supply sufficient evidential support for any
higher-level recognition event to become dominant, which explains why the overall percept remains
indeterminate in ambiguous stimuli.


                                                  302
Remark 726 (Perception as action). In this view, perception is not passive “taking in data” but an
active control process that modulates which patterns become salient and how they are organized. This
aligns naturally with predictive-processing and active-inference perspectives, but remains agnostic
about particular neuroscience.
    More concretely, the “action” here need not be overt motor behavior; it can also be internal
action in the space of hypotheses, such as adjusting attention, gain, precision, or other modulatory
knobs that determine which prediction errors are amplified and which are attenuated. The formal
upshot is that perceptual outcomes are treated as controlled equilibria: what is perceived is what-
ever interpretation the system can stably maintain under its current control policy and evidential
constraints, rather than a direct readout of raw sensory input.

14.7     Planning and optimal control: integration hooks
14.7.1    Event calculus hook
The Event Calculus represents temporally extended domains using predicates such as Happens(a, t),
Initiates(a, f, t), Terminates(a, f, t), and HoldsAt(f, t). In a Hyperseed-style uncertain setting, one
can attach p-bit evidence values to these predicates and treat planning as search for action sequences
whose composed predictive implication toward the goal is high. The sequential composition oper-
ator from Section 14.4 is designed to match the temporal compositionality required by planning.
     The intended reading is that each of these predicates can be treated as an evidential claim rather
than a Boolean fact: an agent may have partial support that an action occurred, mixed support that
it initiates a fluent, or even contradictory support due to noisy sensing, conflicting reports, or model
mismatch. Planning then becomes an evidential optimization problem: instead of searching for a
single logically consistent narrative, one searches for trajectories whose chained, time-respecting
implications make the goal fluent more strongly supported at the relevant horizon. The sequential
operator is the mechanism that turns per-step evidential implications into an aggregate multi-step
assessment while respecting temporal order (i.e. earlier actions can only influence later holds).

Remark 727. This paragraph is an interface point rather than a full development: it says that
one may take a classical event/process calculus (Hyperseed-Concept ??) and replace its crisp truth
values with p-bit evidence values, thereby allowing plans to be assessed under contradictory and
incomplete information. The quantale-composition rule then supplies an algebra for aggregating
multi-step plan reliability without leaving the evidential domain.
    In particular, the “interface” claim is that existing symbolic planning infrastructure can be re-
used at the level of syntax and temporal structure (events, fluents, and their persistence), while
the semantics of entailment is softened into evidential support. This makes it possible to speak
meaningfully about plans that are good enough even when no plan can be proven correct in the
classical sense, and it clarifies how plan refinement can proceed: one improves a plan either by
strengthening the evidential links between steps (better predictive implication) or by inserting actions
whose main role is epistemic, i.e. to reduce contradiction and increase the stability of later inferences
about HoldsAt(f, t).

14.7.2    Wu Wei preview
Section 26 introduces Wu Wei dynamics: a bias toward minimal contrivance, i.e. achieving goals
via the weakest (least special-case) control policies that still work. In the present terms, Wu Wei is
a global optimization principle layered on top of the local notions of attraction/causality/control.
Roughly: among plans that achieve high projected predictive implication toward the goal, prefer


                                                  303
those that maximize weakness (simplicity) and minimize experienced effort (Section 8) (Hyperseed-
Concept 206, Hyperseed-Concept 100; see [21]).
    The integration hook to optimal control is that “weakness” plays a role analogous to regular-
ization or complexity penalties: it biases the solution set toward policies that are robust under
model error and that do not rely on brittle coincidences in the environment. Meanwhile “effort”
functions like a cost functional over control signals, including both overt energy expenditure and
internal computational or attentional load. The resulting preference ordering is thus not merely
about whether a goal can be reached, but about whether it can be reached in a way that remains
stable under the agent’s limited resources and imperfect knowledge.
Remark 728. The philosophical tenor here is that of “least action,” but translated from physics to
agency: do not seek maximal domination of the world, but maximal alignment with the world’s own
tendencies, so that small interventions suffice. Formally, this becomes a multi-objective optimization
over (i) plan success (predictive implication), (ii) simplicity/weakness, and (iii) effort. This is also
where control theory (in the engineering sense) and weakness theory (in the Hyperseed sense) meet.
    One can also read this as a constraint on control hierarchies: higher layers should prefer to set
broad, low-commitment goals or biases that allow lower layers to exploit existing attractors in the
environment, rather than micromanaging every degree of freedom. In that sense, Wu Wei is not a
rejection of control but a discipline of control: intervene at the level where a small informational
or policy change yields a large shift in downstream trajectories, and avoid interventions that must
be continually “propped up” against the system’s natural dynamics.

Hyperseed concepts covered
• Attraction, PredictiveImplication, PredictiveAttraction; sequential temporal operators (Sequen-
  tialAND, SimultaneousAND, SimultaneousOR) at a formal level.

• Cause, CausalImplication, SimpleCausalImplication; extensional vs intensional predictive attrac-
  tion; temporal precedence; weakness/simplicity bias.

• Control, asymmetric/symmetric control; Control Hierarchy; Perceptual Hierarchy.

• Planning hook (Event Calculus) and connection to later Wu Wei optimal control.


15     Attention and cognitive synergy
15.1    From control to attention
Section 14 introduced prediction, attraction, and control. For bounded systems, however, “control”
is always exercised through a bottleneck: only a small fraction of the system’s internal processes
can be actively updated at any moment. This bottleneck can be read quite literally as a limit on
concurrently maintainable state, updatable parameters, searchable hypotheses, or executable action
plans—and, more abstractly, as the simple fact that any physical mechanism has finite throughput.
Hyperseed calls the structured management of this bottleneck attention. In other words, attention
is not an optional add-on to control; it is the mechanism by which control becomes realizable under
finite capacity.
    Informally, attention is not (only) a spotlight on sensory data. It is the system’s allocation
of its limited resources (time, energy, computation, bandwidth) across the recognition, inference,
simulation, and action processes that operate on patterns. This includes not only which patterns
are processed, but also how deeply they are processed: e.g., whether a hypothesis is merely queued,

                                                  304
weakly checked, or iteratively refined until it becomes a stable, reusable chunk in the system’s
pattern inventory. When the allocation becomes highly concentrated, the system has an attentional
focus. When the system’s self-model lies inside the focus, it has self-reflective attention, a key
ingredient in Hyperseed’s later notion of reflective consciousness (Section 17). Equivalently, self-
reflective attention can be viewed as the case where the system treats parts of its own modeling-
and-control loop as objects of ongoing inference and revision, rather than as fixed machinery.
    A useful way to read the above is that attention defines an attentional policy over internal
processes: it determines which inference chains get additional compute, which simulations get
extended time horizons, which sensors are sampled at higher fidelity, and which candidate actions
are evaluated with higher resolution. Since these choices affect what the system learns and what
it can do next, attention couples short-term performance to long-term capability: the system that
repeatedly allocates effort to the same limited set of patterns may become very efficient there, but
risks neglecting alternative explanations or actions. This trade-off between exploitation (deepening
a current focus) and exploration (shifting focus to new patterns) will reappear later when we discuss
synergy across processes and the conditions under which collections of patterns become mutually
supportive rather than mutually distracting.

Remark 729. The guiding idea is that agency is never merely about possessing a good model; it
is also about deciding which parts of the model to refine now. This is a resource-theoretic thought
in the style of bounded rationality, but expressed in the native Hyperseed vocabulary of patterns
and genenergy. In this sense, attention is the operative bridge between the “can in principle” of
prediction/control and the “can right now” of a finite mechanism [19, 1]. One concrete implication
is that even an accurate generative model may fail to yield effective control if the system cannot
reliably route effort to the model components that matter for the present context (e.g., the causal
variables relevant to a current goal, or the uncertainty sources that dominate expected loss).

Remark 730. When we later refer to the Hyperseed core-concept set, the notions of attention
and focus here should be read alongside Hyperseed-Concept 60 and the more general resource/effort
notions (Hyperseed-Concept 100) that implicitly underwrite the formal budget constraints below. In
particular, “effort” can be interpreted as the accounting unit that allows different internal activities
(updating beliefs, running simulations, searching memories, selecting actions) to be compared and
traded off within a single bounded budget, even when their concrete computational substrates differ.

Remark 731. It is also helpful to distinguish the target of attention (which patterns or processes
are selected) from the mode of attention (how selection is enforced). In engineered systems this
mode might look like explicit scheduling, priority queues, or dynamic resource allocation; in bio-
logical systems it may appear as gating, inhibition, or neuromodulatory gain control. Hyperseed
abstracts away from these implementations and treats attention primarily as the functional role of
reliably concentrating limited genenergy on the pattern-transformations most relevant to the current
trajectory of inference and action.

15.2    Genenergy budgets and attention measures
Hyperseed measures attention in terms of “genenergy”: any fungible resource that gates what the
system can do (metabolic energy, compute cycles, working memory bandwidth, time-on-task, etc.).
Section 19 gives a broader treatment of energy/genenergy; here we only need a minimal accounting
formalism.

Definition 191 (System, modules, and genenergy flow). A system S is assumed to have:


                                                  305
(a) a finite set of modules M = {1, . . . , n} (subsystems/process bundles);

(b) a finite (or countable) set of patterns P (Section 9);

(c) an association map Assoc : M → 2P indicating which patterns each module is currently
    “about” (recognizes, maintains, manipulates);

(d) a time index set T (Section 7);

(e) a genenergy expenditure function

                                 g : T × M → [0, ∞),              (t, i) 7→ gt (i),

     where gt (i) is the amount of genenergy spent by module i during the interval around t.
The total genenergy spent at time t is
                                                  X
                                          Gt :=         gt (i).
                                                  i∈M

Remark 732. Intuitively, the definition separates what the system is (a collection of modules
that can spend resources) from what the system is about (the patterns those modules are currently
tracking or manipulating). The association map Assoc is intentionally coarse: it is not a semantic
truth-condition, only a bookkeeping relation indicating which patterns are in the working ambit of
which processes (Hyperseed-Concept 59; Hyperseed-Concept 130).
Remark 733. A simple example is a toy architecture with three modules: vision (i = 1), planning
(i = 2), and motor control (i = 3). At time t, we might have gt (1) = 5, gt (2) = 2, gt (3) = 1,
so Gt = 8. Even in this minimal case, attention is already present as the uneven allocation of
genenergy across modules (Hyperseed-Concept ??).
Remark 734. The notation gt (i) follows a standard convention: g is the underlying function, while
the subscript t indicates we freeze time and view gt as a function of the module index i. Similarly,
Gt is the scalar total expenditure at time t. This small notational discipline matters later, when we
push forward module-level allocations to pattern-level distributions.
Remark 735. Nothing in the definitions requires genenergy to be conserved or fixed across time.
If Gt = 0 we interpret S as effectively inactive at time t.

15.2.1   Attention to a pattern class
Hyperseed defines attention to a class of patterns as genenergy spent on processes associated with
those patterns. To avoid double-counting when modules touch multiple patterns, we distribute
each module’s expenditure over its associated pattern set.
Definition 192 (Pattern-level attention). Assume each module i comes with a nonnegative weight-
ing                                               X
                               wi : P → [0, 1],       wi (p) = 1,
                                                        p∈P

with wi (p) = 0 unless p ∈ Assoc(i). Define the attention mass on pattern p at time t by
                                                 X
                                    Attnt (p) :=     gt (i) wi (p).
                                                  i∈M


                                                  306
For a class of patterns X ⊆ P define
                                                          X
                                      Attnt (X) :=              Attnt (p).
                                                          p∈X

When Gt > 0, define the normalized attention distribution
                                            Attnt (p)           X
                                αt (p) :=             ,               αt (p) = 1.
                                              Gt
                                                                p∈P

Remark 736. The intent is to get a clean quantitative proxy for the intuitive claim “pattern p is
in the spotlight.” Each module spends genenergy, and each module spreads its expenditure over the
patterns it is currently engaging. The weights wi (p) can be read as a soft assignment: how much of
module i’s work is effectively “about” p rather than something else.
Remark 737. A concrete example: suppose a planning module i is simultaneously considering two
candidate subgoals, represented by patterns p1 and p2 . One might set wi (p1 ) = 0.7, wi (p2 ) = 0.3.
Then if gt (i) = 10, this module contributes 7 units of attention mass to p1 and 3 to p2 . Summing
across modules yields a global pattern-level allocation.
Remark 738. The distribution αt ∈ ∆(P) is the normalized version of attention mass. Here ∆(P)
denotes the probability simplex on P: the set of functions α : P → [0, 1] summing to 1. We use
probabilistic notation not because attention is always stochastic, but because normalization turns
“share of resources” into a form that can be compared across times and systems, and connected to
entropy-like concentration measures.
Remark 739 (Module-level vs pattern-level). One can also work directly with the module allocation
vector α̂t (i) := gt (i)/Gt . The pattern-level distribution αt is a pushforward of α̂t along the weights
wi .
Remark 740. The pushforward comment can be read categorically: α̂t lives on modules, while αt
lives on patterns; the weights wi implement a (time-dependent) stochastic map from modules to
patterns. In the philosophical idiom, this is how the system’s internal economy of effort becomes a
distribution over what is present to its cognition (Hyperseed-Concept ??).

15.2.2    Attentional focus and self-reflective attention
Hyperseed’s notion of attentional focus is a concentration condition: a relatively small subset of
the system absorbs a relatively large fraction of genenergy. In this section we treat the attention
weights αt (p) as an abstract accounting device for how much of the system’s limited update capacity
is effectively routed through
                            P pattern p at time t. In particular, one can read αt as a probability
distribution over P (hence p∈P αt (p) = 1), but the intended interpretation is budgetary: the mass
is a normalized proxy for “genenergy share” rather than a claim about any specific implementation.
Definition 193 (Attentional focus). Fix parameters θ ∈ (0, 1) (mass threshold) and k ∈ N (size
bound). We say S has an attentional focus at time t (at level (θ, k)) if there exists a subset Ft ⊆ P
with |Ft | ≤ k such that                       X
                                   αt (Ft ) :=    αt (p) ≥ θ.
                                                    p∈Ft

Equivalently, if αt↓ is the nonincreasing rearrangement of the weights (αt (p))p∈P , then focus holds
iff kj=1 αt↓ (j) ≥ θ.
   P


                                                     307
Remark 741. The definition formalizes an old introspective fact: at any moment, a mind is
usually “mostly doing one thing,” perhaps with a few side computations. The parameters (θ, k) let
us tune what we mean by “mostly” and “few.” The nonincreasing rearrangement αt↓ is simply the
list of attention weights sorted from largest to smallest; the criterion then says: the top k patterns
together carry at least θ fraction of the attention mass. It is also useful to keep in mind that the
set Ft is typically not unique: whenever there are ties among the largest weights, multiple choices
of Ft witness the same level of focus. Nothing in later arguments depends on a canonical choice;
only the existence of some small set with large mass matters.
Remark 742. A simple example: if P has 100 patterns and the top k = 5 patterns carry 85% of
the mass, then the system has focus at (θ, k) = (0.85, 5). Conversely, if attention is spread nearly
uniformly, then no small subset can reach a high threshold and focus fails. This aligns with the
intuition that “diffuse attention” is the absence of a narrow bottleneck. Note that this is sensitive to
how nonuniformity is distributed: e.g. two medium-sized clusters can each be salient without either
cluster alone clearing a large θ for small k, which matches the everyday phenomenon of “split
attention” (two active tasks) as distinct from either single-task focus or fully uniform diffusion.
Remark 743. The usefulness of this definition is pragmatic: it lets later sections talk about focus-
dependent phenomena (e.g. workspace access, self-reference, and stable control loops) without com-
mitting to a specific psychological or neural mechanism. It is thus a minimal mathematical hook
for Hyperseed-Concept 60. A further pragmatic benefit is that the condition is scale-free: only the
relative genenergy shares matter. This is helpful when comparing subsystems or agents whose ab-
solute compute budgets differ, since attentional bottlenecks are often about allocation rather than
total capacity.
Remark 744 (Basic monotonicities). The definition behaves monotonically in the expected way: if
focus holds at (θ, k), then it holds at (θ0 , k 0 ) for any θ0 ≤ θ and any k 0 ≥ k. Conversely, increasing
θ or decreasing k makes the test strictly harder. This lets one speak of “strong” focus (high θ with
small k) versus “weak” focus (lower θ and/or larger k) without changing the underlying concept.
Remark 745 (Canonical witnessing set via top-k). Given αt , one can always witness the maximal
attainable mass under a size bound k by choosing P Ft to be any set of k patterns achieving the k
largest weights (ties arbitrary). Then αt (Ft ) = kj=1 αt↓ (j), which shows that the “existence of Ft ”
phrasing and the rearrangement criterion are not merely equivalent but operationally the same test:
compute the top-k share and compare to θ.
Definition 194 (Self-model and self-reflective attention). Let Pself ⊆ P be the set of patterns that
constitute the system’s current self-model (Section 16). We say S has self-reflective attention at
time t if
                                          αt (Pself ) ≥ θself
for some chosen threshold θself ∈ (0, 1). More strongly, S has focused self-reflective attention at
time t if Ft can be chosen so that Ft ∩ Pself 6= ∅.
Remark 746. Here the point is not metaphysical privilege but routing: self-model patterns are
those whose update affects how the system predicts, controls, and narrates itself. When a significant
share of attention mass is allocated to Pself , the system is spending real resources on maintaining or
revising its self-description (Hyperseed-Concept ??; Hyperseed-Concept 165). The two thresholds θ
(general focus) and θself (self allocation) need not coincide: one may want to detect self-involvement
even when overall focus is weak (e.g. rumination spread across many self-related fragments), or
conversely require that self-related patterns occupy a significant fraction of a very tight focus set.

                                                   308
Remark 747. A typical example is a learning agent that allocates attention to error-monitoring
patterns such as “I am failing” or “my model is uncertain.” These are self-model patterns in the
present sense, and when they enter the focus set Ft , one gets a crisp formal correlate of the everyday
report “I noticed that I was confused.” This is a small but essential ingredient for the later con-
sciousness interface (Section 17) and resonates with empirical discussions of self-related processing
(Hyperseed-Concept 85). It is worth emphasizing that the stronger condition (intersection with Ft )
captures a difference between (i) dedicating some background mass to self-maintenance and (ii) hav-
ing self-model content be among the currently dominant patterns. The latter is the mathematically
clean version of the phenomenological distinction between “the self is in the foreground” and “the
self is merely implicitly present.”
Remark 748 (Focus is graded). The parameters (θ, k) provide a simple family of “focus tests.”
Other concentration measures can be used (entropy, Gini coefficient, top-k share), but the above
definition is adequate for connecting to later sections. In
                                                         Pkpractice, one may also care about temporal
                                                                ↓
aspects (how long a focus persists): a brief spike where j=1 αt (j) ≥ θ may have different functional
consequences than a sustained interval on which the inequality holds. Later when we discuss stable
control loops, it will be natural to consider not only instantaneous focus but also its persistence
under small perturbations of αt .

15.3    Attention as a bounded control policy
Attention is itself an action: it chooses which parts of the internal model are updated, refined, or
queried. Formally, we treat attention as a policy that selects a distribution over internal update
actions. This framing makes “what to think about next” a first-class control variable, rather than
a side-effect of perception or representation: the system can actively steer its own computational
trajectory by deciding which internal transformation to apply next.
Definition 195 (Internal update actions). Let U be a set of internal update actions. An element
u ∈ U may represent:
(a) refining a distinction (Section 3);
(b) updating a pattern intensity estimate (Section 9);
(c) querying memory or a submodule (Section 20);
(d) simulating a causal consequence (Section 14);
(e) reweighting or re-indexing representations (Section 13).
Assume each update action u has a genenergy cost c(u) ≥ 0.
Remark 749. The philosophical move here is to treat attention not as a passive “light” but as an
internal intervention: an update action u changes the system’s internal state, and thus changes
what future actions are possible. This matches the control-theoretic reading of attention used in
engineered AGI systems, where “choosing what to compute next” is itself a crucial policy decision
[19].
Remark 750. It is useful to emphasize that U can mix heterogeneous operations that live at different
algorithmic levels. For example, “refine a distinction” may change the representational vocabulary,
while “retrieve one memory” may only change the active context, and “simulate a consequence”
may instantiate a temporary forward model. Treating all of these as elements of a single action
set is a deliberate unification: the attention mechanism need not commit in advance to a single
computational paradigm, and can instead arbitrate among many possible internal moves.

                                                 309
Remark 751. Examples of u ∈ U include: running one step of a planner; performing a memory
retrieval; updating a Bayesian posterior; or running a short roll-out simulation. The cost c(u) is
deliberately abstract so it can stand in for time, energy, FLOPs, bandwidth, or any conserved-or-not
resource (Hyperseed-Concept 87; Hyperseed-Concept 100).

Remark 752. The cost function c(u) can also be interpreted as a capacity consumption measure:
two update actions may both be fast, but one may monopolize scarce working memory or interfere
with concurrent processes. In that sense, bounded attention is not only a time-budget story; it can
represent any constraint that forces internal computation to be selectively scheduled rather than
globally applied.

Definition 196 (Attention policy with budget). Fix a budget Bt ≥ 0 for time t. An attention
policy is a map
                                      πt : Ωt → ∆(U),
where Ωt is the system’s internal state space at time t and ∆(U) is the set of probability distributions
over U. A draw u ∼ πt (ω) is feasible if c(u) ≤ Bt .

Remark 753. One can equivalently define, for each (t, ω), a feasible subset

                                    Ut (ω) := {u ∈ U : c(u) ≤ Bt },

and view πt (ω) as a distribution supported on Ut (ω). This highlights that the budget may be context-
dependent in practice: the same nominal update action might be cheap in one internal configuration
(e.g., when a relevant cache is warm) and expensive in another (e.g., when a submodule must be
re-initialized).

Remark 754. The notation πt : Ωt → ∆(U) is standard in decision theory: given an internal
state ω ∈ Ωt , the policy πt returns a distribution over actions. The only twist is that actions here
are internal computations or updates rather than external motor moves. The feasibility condition
c(u) ≤ Bt makes the resource constraint explicit, so that attention is a bounded-control problem
rather than a purely epistemic one.

Remark 755. In this language, “attention failure” can be described without invoking any special
pathology: it is simply the selection (perhaps repeatedly) of update actions that are locally feasible but
globally unhelpful, e.g., over-investing in cheap but low-value computations, or repeatedly applying
an update rule that no longer improves internal predictions. Conversely, “skilled attention” is a
policy πt that reliably selects update actions whose downstream effects improve later decision quality
under budget constraints.

Remark 756. A simple example: if Bt is small, the policy may assign high probability only to
cheap actions like “retrieve one memory” rather than expensive ones like “run a long simulation.”
This gives a clean way to formalize attentional phenomena such as shallow vs. deep reasoning under
time pressure, without altering the underlying pattern semantics.

Remark 757. The budgeted-policy view also clarifies how attentional allocation can couple to
external action. If an external decision must be made imminently, Bt effectively shrinks, shifting πt
toward quick diagnostic updates; if the system is in a deliberative regime, Bt can expand, permitting
costly counterfactual simulation and deeper representational refinement. In both cases, the same
internal machinery can be used; only the feasible set and the policy’s trade-offs change.



                                                   310