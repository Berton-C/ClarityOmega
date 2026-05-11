# 5 Toy model: finite universe, p-bit quantale, and morphic resonance demo

V = [0, 1] with ≤ the usual order, e = 1, and ⊗ a t-norm (often multiplication), then C(A, B) can
be read as a graded confidence/support. If one instead wishes to model cost or distance, a standard
choice is the Lawvere quantale V = ([0, ∞], ≥, +, 0) (note the reversed order), in which case the
same inequality becomes the triangle inequality for extended pseudo-metrics: going via B cannot
be cheaper than going directly. These examples underline that the “same” formalism can encode
either support-like or cost-like readings by a systematic choice of order and tensor.

Remark 76 (What “thin form” means and how to picture it). In an ordinary category, C(A, B)
is a set of morphisms. In the thin enriched form used here, we collapse that set to a single graded
value: C(A, B) ∈ V measures “how well A leads to B” (as support, feasibility, similarity, etc.). This
is closer to a preorder than to a category with many arrows, but it is often exactly what is needed
for resource-sensitive modeling: we care about degree of accessibility more than about enumerating
all witnesses.
    Example: objects could be contexts, models, or descriptions; then C(A, B) might encode the
degree to which B can be obtained from A by a translation or refinement step. The axioms then
say: each object can reach itself at least as well as the unit e, and going from A to B and then B to
C cannot yield better support than a direct A to C value (a quantitative triangle-like law). This is
a convenient formal home for Hyperseed’s many “approximate correspondence” claims (Hyperseed-
Concept 112).
    Equivalently, one can read a thin V -category as a V -valued preorder: it records, for every
ordered pair (A, B), a single “strength” of the statement “A is at most as informative as B” (or “A
can be transformed into B”) in a way that is reflexive and transitive in the enriched sense. This
perspective is often helpful when translating informal monotonicity claims into lemmas, because
one can appeal directly to enriched reflexivity/transitivity rather than to the existence of explicit
witnessing arrows.

Remark 77 (How to read the axioms). These axioms say: identity evidence is maximal (or at least
not worse than e), and chaining two correspondences yields a correspondence that is (weakly) no
stronger than the direct one. The direction of the inequalities depends on whether one models “cost”
(where smaller is better) or “support” (where larger is better). Here we model graded support, so
composition multiplies support and is bounded above by direct support.
    It is often useful to keep two derived intuitions in mind. First, the enriched composition law is a
submultiplicativity constraint: whatever proxy for “evidence” C(A, B) represents, indirect evidence
obtained by composing steps cannot systematically dominate direct evidence. Second, the axiom is
robust under coarse-graining: if one later refines the modeling to track multiple pathways explicitly,
taking a join/supremum over pathways typically yields a thin hom-value that still satisfies the same
inequality because ⊗ distributes over joins in a quantale.

Definition 14 (V -functor (thin form)). A V -functor F : C → D between V -enriched categories is
a function on objects such that
                                   C(A, B) ≤ D(F (A), F (B))
for all objects A, B.

Remark 78 (Intuition: structure preservation up to monotone improvement). A V -functor sends
each object in C to an object in D and guarantees that any accessibility/support present in C is
not lost under translation. In other words, if A supports reaching B to degree C(A, B), then F (A)
supports reaching F (B) at least as strongly in D.
   Example: C might be a category of world-states and D a category of internal representations.
Then F models a representational mapping that does not reduce the system’s ability to track certain

                                                  62
transitions. This is one rigorous way to capture “approximate morphism” talk in cognitive modeling
[19], while retaining the flexibility that F need not be invertible or information-preserving in the
classical sense.
    In practice, many mappings of interest are not strictly structure-preserving but are lax or ap-
proximate in the sense that they preserve lower bounds on support rather than exact values. The
thin V -functor inequality is exactly such a laxness condition: it asks only that the image corre-
spondence in D be at least as permissive (in the ≤-order sense) as the original correspondence.
This matches the modeling stance in which internal representations may “fill in” or “smooth over”
distinctions present in the world while still enabling reliable downstream composition of inferences.

Why enrichment is enough for “approximate morphisms.” In later sections we will rep-
resent many Hyperseed correspondences as either: (i) V -functors (structure-preserving maps), or
(ii) V -relations/modules (structure-preserving correspondences that need not be functional). Both
are stable under composition and admit quantitative comparison.
     Concretely, “admit quantitative comparison” can be read pointwise: given two candidate corre-
spondences of the same type, one can often define an ordering by saying that one is no worse than the
other exactly when it assigns everywhere-greater (support-like) hom-values (or everywhere-lower
costs, in the dual convention). This makes it possible to phrase optimization or “best available
translation” problems entirely inside the enrichment order, without prematurely committing to a
particular algorithmic realization.
Remark 79 (Why this suffices for a large portion of Hyperseed’s needs). One might worry that
a “thin” enriched category cannot express all the nuance of internal representations, which often
involve many distinct mechanisms. But much of Hyperseed’s ontology, at least at the scaffold
level, asks questions of the form: “to what degree does structure A constrain or entail structure
B?” For this, a single graded hom-value is often the right abstraction: it forgets implementation
details while preserving compositional inequality laws, which are the main invariants needed to prove
monotonicity and stability results later.
    This choice is also methodologically Russellian: replace metaphysical speculation with a cal-
culus of relations whose algebraic laws are explicit. When more expressivity is required (multiple
arrows, higher morphisms, transformations between transformations), the enriched perspective re-
mains compatible with refinement rather than needing replacement.
    A further pragmatic benefit is that thin enrichment cleanly separates two concerns that are often
conflated in informal discussions: (a) the existence of a pathway from A to B, and (b) the quality or
reliability of that pathway. In a thin V -category the former is encoded by whether C(A, B) is above
a chosen threshold, while the latter is encoded by its precise value; proofs can then be parameterized
by the threshold without changing the underlying formal statements.
Remark 80 (Optional higher-categorical extension). Nothing in this section requires higher cate-
gories. However, some Hyperseed themes (e.g. perspective shifts, equivalence up to reparameteriza-
tion, and self-reference) are naturally expressed using groupoids and (∞, 1)-categorical equivalence.
Where needed later, one may treat “entities” as objects of an (∞, 1)-groupoid and treat observer
translations as higher morphisms. The present section provides the 1-categorical “spine” on which
that extension can be built.
    Even in the presence of higher structure, thin enrichment remains useful as a decategorified
“shadow”: one can map a higher groupoid of transformations to a V -valued accessibility relation by
assigning to each pair (A, B) an aggregate strength of all higher paths from A to B (e.g. a supremum
over witnesses, a probability, or a robust similarity score). Thus the enriched spine is not merely a
preliminary simplification but also a stable interface between qualitative and quantitative layers.

                                                 63
3.7   Quantale weakness as “failed distinctions”
We now formalize the simplest quantitative proxy for Hyperseed’s simplicity/generalization idea:
an observer is “simpler” (or more general) when it collapses more distinctions [3, 2]. Hyperseed-
Concept 202; Hyperseed-Concept 143; Hyperseed-Concept 169.
    The key move in this subsection is to represent “what the observer does not (or chooses not
to) discriminate” as a relation on X, and then to aggregate the “importance” of the collapsed
pairs using the ambient quantale structure. This keeps the formal core small while still allow-
ing different downstream readings (perceptual limitations, abstraction, compression, or deliberate
coarse-graining).

Definition 15 (Salience/importance weights). Let X be a set and let µ : X → V be a weight map.
Intuitively, µ(x) encodes how much the observer cares about distinguishing x (or how much “mass”
x has for aggregation).

Remark 81 (Intuition and examples for µ). The weight map µ is a formal admission that not all
entities matter equally. Two observers may agree on which pairs are indistinct yet differ on the
consequences because one treats certain entities as salient and others as negligible. This aligns with
Hyperseed’s emphasis on attention and salience (Hyperseed-Concept 60).
    Example 1: In a perception task, µ(x) might reflect how often x occurs or how costly it is to
misclassify it. Example 2: In an internal cognitive model, µ(x) might encode how emotionally
charged or goal-relevant an item is, which will later connect to values and emotion (Hyperseed-
Concept ??; Hyperseed-Concept ??). The usefulness is that weakness and pattern measures become
sensitive not only to how many distinctions are lost, but to which ones.
    Operationally, µ is the hook by which context enters the otherwise combinatorial object H ⊆
X × X: changing attention, goals, or risk tolerance can be modeled simply by changing µ, without
changing X itself. In particular, assigning µ(x) = ⊥ (or the least element of V ) can be read as
declaring x negligible for the present analysis,Lsince such elements will not contribute to weakness
after multiplication by ⊗ and aggregation by .

Definition 16 (Crisp failed-distinction set). A failed-distinction set is a subset H ⊆ X × X whose
elements are the pairs an observer treats as indistinguishable (in a given context and for a given
purpose).

Remark 82 (Intuition: a formal shadow of “cannot tell apart”). A failed-distinction set H records
where the observer’s discriminative power collapses: (u, v) ∈ H means that, for the relevant purpose,
u and v are treated as the same. If one were modeling classical equivalence, one might demand
reflexivity, symmetry, and transitivity. Here we do not impose those axioms: in cognitive reality,
indistinction can be asymmetric or context-fragmented, and transitivity can fail under noise or
shifting attention (Hyperseed-Concept ??; Hyperseed-Concept 195).
    Example: If X consists of similar visual stimuli, H may contain (u, v) when the system confuses
u for v. The usefulness of keeping H separate from a fully axiomatized equivalence relation is that
it allows us to measure weakness and then later study what closure operations (e.g. compositional
propagation) do to H as a form of emergence (Hyperseed-Concept ??).
    Note also that H is allowed to include or exclude diagonal pairs (u, u). If (u, u) ∈ H is permitted,
it can be interpreted as “self-collapse” in the sense that the observer does not maintain a stable
distinction of u from itself across time or internal state (e.g. due to temporal aliasing); if it is
excluded, then weakness is driven purely by cross-entity confusions. The formalism itself does not
force either convention; one can choose the modeling stance appropriate to the domain.


                                                  64
Definition 17 (Weakness of a failed-distinction set). Given (X, µ) and H ⊆ X × X, define the
weakness of H by                            M
                                w(H) :=          µ(u) ⊗ µ(v).
                                              (u,v)∈H
                                                                                      L
Remark 83 (Notation unpacking, intuition, and a tiny example). The symbol                 denotes the
join/supremum in the quantale V (in the canonical p-bit quantale, this is componentwise max). The
product ⊗ is the quantale monoidal product (in the canonical case, componentwise multiplication).
Thus each indistinct pair contributes a combined weight µ(u) ⊗ µ(v), and w(H) aggregates all such
contributions.
    Example (canonical p-bit quantale): if µ(u) = (0.9, 0.9) and µ(v) = (0.5, 0.5) then µ(u) ⊗
µ(v) = (0.45, 0.45). If H contains several pairs, then w(H) keeps the maximum positive component
and maximum negative component among the pair-weights. This is a minimal but robust way to
say: “weakness is at least as large as the most significant collapsed distinction.” The definition
is useful because it creates a monotone scalar-like measure (in V ) that can be compared across
observers/contexts and will later interface with pattern intensity and effort tradeoffs [3].
    A useful basic property, immediate from the definition and the order structure of V , is mono-
tonicity in H: if H ⊆ H 0 then every join-summand for H is also present for H 0 , hence w(H) ≤
w(H 0 ). In words, declaring additional pairs as indistinct cannot reduce weakness. Likewise, if
µ ≤ µ0 pointwise (meaning µ(x) ≤ µ0 (x) for all x), then w µ (H) ≤ w µ0 (H), expressing that increas-
ing salience can only increase (or preserve) measured weakness.                         L
    When V has a top element > and ⊗ is order-preserving, one can also read w(H) ≤ (u,v)∈H > =
> as a trivial upper bound, and w(∅) = ⊥ as the base case: an observer that collapses no tracked
distinctions (in the current context) has minimal weakness.

Remark 84 (Fuzzy failed distinctions). One can generalize H from a crisp set to a V -valued
relation H : X × X → V and define
                                     M
                         w(H) :=           H(u, v) ⊗ µ(u) ⊗ µ(v),
                                       (u,v)∈X×X

which reduces to Definition 17 when H is {e, ⊥}-valued. The crisp form is sufficient for the sanity
theorem in Section 4 and for minimal exposition.
    In this fuzzy reading, H(u, v) can be interpreted as a graded degree of indistinguishability or
confusion: ⊥ means “fully distinguished” and larger values mean “more collapsed.” The algebraic
form then says that weakness is obtained by combining (via ⊗) three factors: how much the observer
fails to distinguish the pair, and how salient each endpoint is. The crisp case corresponds to the
indicator-like choice                          (
                                                 e (u, v) ∈ H,
                                     H(u, v) =
                                                 ⊥ (u, v) ∈
                                                          / H,
so that only the designated indistinct pairs contribute to the join.

Remark 85 (Why weakness formalizes “simplicity” rather than merely “error”). It is tempting to
read H as a set of mistakes, but in Hyperseed the collapse of distinctions is not always a failure;
it is often a strategy of generalization. A system with limited resources may deliberately treat
many cases as “the same” to gain compression and transfer. The weakness functional captures this
tradeoff by measuring the extent of such collapse, without presuming it is bad. In later sections,
effort and description-length considerations will supply the missing normative layer, connecting to
algorithmic compression intuitions [16].

                                                   65
    This is also why the definition is phrased purely in terms of indistinction and salience, rather
than in terms of an externally provided “ground truth”: the same H may be advantageous or
disastrous depending on which downstream tasks are prioritized (encoded, here, primarily through
µ and later through explicit utility/effort structure).

Interpretive link to Hyperseed simplicity. Hyperseed treats simplicity as observer-relative
and grounded in the distinctions an observer can afford to make. The weakness w(H) is a direct
algebraic instantiation: larger failed-distinction sets (or heavier collapsed pairs) produce larger
weakness. Later, effort and description length will provide additional structure on top of this.
    Because w(H) lives in the same quantale V used elsewhere in the minimal formal core, it can
be compared, combined, or bounded using the same operations as other quantities (e.g. pattern
intensities). This is one reason to prefer a quantale-valued measure rather than a single real number:
the ordering and aggregation structure needed for later composition is already present at the type
level.

3.8   Interpretation map: from Hyperseed talk to core objects
The formal core is intended to be a “dictionary” rather than a full metaphysics [1]. In particular,
the role of the mapping below is to make each piece of Hyperseed vocabulary point to a typed
mathematical placeholder with a clear domain of definition (e.g. elements, relations, functionals)
and with explicit rules for how it composes with the rest of the framework. This helps keep later
constructions invariant under changes of philosophical reading: one may reinterpret the words, but
the algebra of the surrogates stays fixed. A convenient minimal mapping is:

• Entity / occasion token          element x ∈ XC in a context C. Hyperseed-Concept 124. Here XC
  is not assumed to be a set of mind-independent “things”; it is simply the carrier of whatever items
  are available to be related inside the chosen standpoint C, so its intended meaning is operational
  rather than metaphysical.

• Context / aspect / observer package C with XC and V -relations and valuations. Hyperseed-
  Concept 86. Concretely, C functions as the minimal bookkeeping device that fixes (i) what counts
  as an admissible token, (ii) what graded comparisons or constraints between tokens can be stated,
  and (iii) which valuation scheme interprets those graded statements in the chosen evidence struc-
  ture V .

• Distinction / indistinction       a designated V -relation RC : XC × XC → V (read as evidence-
  for/evidence-against “same for purpose P ”), plus thresholded crisp projections if needed. Hyperseed-
  Concept 98; Hyperseed-Concept ??. The point is that “distinguishability” is represented as
  graded rather than all-or-nothing: RC (x, y) records how strongly C supports treating x and y as
  the same (or as different, depending on the chosen polarity) relative to a purpose parameter P
  that may be implicit in C’s choice of relation. When later arguments require a classical equiv-
  alence relation, one can recover it by selecting a threshold in V and projecting RC to a crisp
  predicate, thereby making explicit exactly where discretization enters.

• Simplicity / generalization       weakness w(H) of an induced failed-distinction relation H.
  Hyperseed-Concept 169; Hyperseed-Concept 202; Hyperseed-Concept 143. Intuitively, H sum-
  marizes where a proposed distinction does not hold (or holds only weakly), and the functional
  w(H) turns that summary into a scalar-like comparison value inside the ambient order of V (or
  an associated preorder). Reading “simplicity” as “ability to ignore differences without breaking


                                                 66
  too much,” greater weakness corresponds to more aggressive generalization: the formalism makes
  that tradeoff measurable so that later optimization principles can compare different candidate
  abstractions.
• Approximate morphism / correspondence                 a V -relation (module) or V -functor between
  enriched structures. Hyperseed-Concept 112. This treats “correspondence” as something that
  may be many-to-many and degree-valued rather than a strict function: a module captures soft
  matching between carriers, while a V -functor captures structure preservation at the enriched
  level (so that similarity, entailment, or reachability relations are transported coherently). The
  choice between them is therefore not merely technical: it encodes whether the intended alignment
  is functional, relational, or compositional.
• Pattern support         a constraint family on V -relations (or a subobject in an enriched cat-
  egory), ranked by weakness/intensity (developed later). Hyperseed-Concept 130; Hyperseed-
  Concept 132. In this dictionary, a “pattern” is not a primitive shape but a condition that
  admissible relations (or admissible objects) satisfy; support is then the degree to which the con-
  dition is met under the valuation scheme. The weakness/intensity ranking is included so that
  “pattern is present” becomes a comparative statement (which patterns are stronger, more stable,
  or more informative) rather than a binary label.
• Resonance / coupling         a functional of paraconsistent valuations (Section 3.9) used to modu-
  late cross-context propagation operators. Hyperseed-Concept 159; Hyperseed-Concept 115. The
  intent is that resonance is not itself another relation on XC , but a higher-level aggregator acting
  on valuations (which may contain inconsistent or incomplete evidence) and returning a control
  parameter that gates how strongly information, constraints, or alignments are allowed to flow
  between contexts. Framed this way, “coupling” becomes something that can be tuned, composed,
  and compared, rather than a purely qualitative metaphor.

Remark 86 (Why a dictionary is philosophically honest). Hyperseed’s ambition is ontological,
but a mathematical reconstruction can remain neutral about ultimate metaphysics while still being
precise about inference rules and composition laws. The dictionary approach acknowledges, in a
Whiteheadian spirit [15], that much of what we call “reality” in practice is a stabilized network of
relations and transformations between standpoints. What matters for theoremhood is not whether
a term is metaphysically primitive, but whether its formal surrogate behaves coherently under the
operations the theory demands.
    This mapping is also a safeguard: when later sections speak in richer language (pattern, habit,
resonance, mindplex), we can always ask, “what is the corresponding object here, and what oper-
ations does it support?” The core thus acts as a semantic spine that keeps the later conceptual
elaborations from drifting into purely metaphorical territory.
    A further virtue is methodological: disagreements about interpretation can be localized. If two
readings of “context” lead to the same algebraic interface (carriers, V -relations, valuations, and
their induced operators), then the subsequent theorems apply to both; if they lead to different inter-
faces, the point of divergence is made explicit and can be analyzed as a change of axioms rather
than as a purely verbal dispute.
    This dictionary will be refined repeatedly in the systematic reconstruction part of the paper
(Part II). In particular, later sections will add explicit assumptions on V (e.g. whether it is a
quantale, bilattice, or other ordered algebra), clarify how valuations interact with composition of
V -relations, and specify which additional structure on contexts is required to make cross-context
propagation and comparison theorems well-posed.

                                                 67
3.9   Resonance derived from paraconsistency
Hyperseed uses “resonance” as a primitive-seeming word for coherent coupling. Hyperseed-Concept 159.
To make it mathematically explicit while keeping the paraconsistent structure visible, we embed
p-bit values into the complex plane [24]. This also sets the stage for later discussion of morphic
resonance (Hyperseed-Concept 115) and related speculative inspirations [13].

Definition 18 (Logic-to-complex map). Define σC : V → C by

                           σC (v + , v − ) := (v + − v − ) + i (v + + v − ) − 1 .
                                                                               


Remark 87 (Notation unpacking and intuition). Here C is the complex plane, and i is the imag-
inary unit. The map σC takes an evidence-pair (v + , v − ) and produces a complex number whose
real part is the evidence bias v + − v − and whose imaginary part is the total evidence (v + + v − )
recentered so that v + + v − = 1 maps to imaginary part 0.
    Intuitively, this is a way of turning paraconsistent structure into a phase-like object: different
kinds of certainty and conflict point in different directions. Once evidence lives in C, we can use the
geometry of angles and inner products to speak of alignment, opposition, and interference—concepts
that mirror the phenomenology of resonance more closely than scalar similarities do.

Remark 88 (Geometric meaning). The real part is the bias toward positive vs negative evidence.
The imaginary part measures over- vs under-determination relative to the midpoint v + + v − = 1:

• (1, 0) 7→ 1 + 0i (“true” axis),

• (0, 1) 7→ −1 + 0i (“false” axis),

• (1, 1) 7→ 0 + 1i (“both” axis),

• (0, 0) 7→ 0 − 1i (“neither” axis).

Thus the four Belnap corners become the four cardinal directions in C.

Remark 89 (Two simple examples and why complex geometry helps). Example 1: (0.9, 0.1) maps
to 0.8+i(0.0), strongly positive and determinate. Example 2: (0.9, 0.9) maps to 0+i(0.8), indicating
maximal conflict without bias. In the plane, these points are orthogonal directions: a bias-driven
certainty is geometrically distinct from a conflict-driven certainty.
    This matters because many cognitive couplings are sensitive to kind of certainty, not just
amount. Two contexts can both be “highly committed” while one is committed via consensus and the
other via internal contradiction; the embedding keeps these apart so that resonance can distinguish
alignment from mere magnitude.

Definition 19 (Local resonance kernel). For v, w ∈ V with σC (v) 6= 0 and σC (w) 6= 0, define the
normalized alignment                                      
                                          < σC (v)σC (w)
                           align(v, w) :=                   ∈ [−1, 1].
                                          |σC (v)| |σC (w)|
If either σC (v) = 0 or σC (w) = 0, set align(v, w) := 0.

Remark 90 (Notation unpacking: <, (·), and | · |). The symbol <(·) denotes the real part of a
complex number. The bar z denotes complex conjugation, which reflects z across the real axis.
The absolute value |z| denotes the complex modulus (Euclidean norm). Thus <(σC (v)σC (w)) is the


                                                    68
standard real inner product on R2 written in complex notation, and the denominator normalizes by
lengths to yield a cosine similarity.
    So align(v, w) is literally the cosine of the angle between the two embedded evidence vectors.
In geometric language: resonance is alignment of directions; anti-resonance is pointing in opposite
directions; orthogonality is non-coupling.

Remark 91 (Reading align). align(v, w) = 1 indicates perfect alignment in the complex embedding
(maximal “resonance”), align(v, w) = −1 indicates perfect opposition (maximal “anti-resonance”),
and values near 0 indicate weak coupling or orthogonality (e.g. true vs both).

Remark 92 (Why define alignment locally before aggregating). Resonance in practice is rarely
a single comparison; it is an emergent property of many coupled judgments across a network
(Hyperseed-Concept 131; Hyperseed-Concept 132). The local kernel align(v, w) gives the primi-
tive comparison from which larger interference measures can be built. By keeping the primitive
symmetric and normalized, we avoid arbitrary scale artifacts when later summing many terms.
    In the paraconsistent resonance perspective [24], such kernels are the atoms of a broader in-
terference calculus: coherent coupling corresponds to constructive interference of many phase-like
contributions.

    Many resonance phenomena involve aggregation over many coupled evaluations. The following
interference functional is one simple way to obtain a scalar coupling score that increases under
coherent alignment.

Definition 20 (Interference-based resonance for a family). Let z1 , . . . , zn ∈ Cd and weights α1 , . . . , αn ∈
R≥0 . Define
                                n
                                X                             n
                                                              X
                        ztot :=    α k zk ,   I := kztot k2 −     kαk zk k2 .
                                     k=1                                   k=1
                                                                                                         2 when nonzero)
                                                                                         P
A bounded resonance score may be obtained by normalizing I (e.g. by                         k kαk zk k
and applying any monotone squashing map into [0, 1].

Remark 93 (Intuition: constructive vs. destructive      interference). The quantity kztot k2 measures
the squared magnitude of the vector sum, while k kαk zk k2 measures the sum of squared magnitudes
                                                P
if there were no cross-terms. Their difference I is exactly the contribution of pairwise cross-terms:
it is positive when vectors tend to align (constructive interference) and negative when they tend to
cancel (destructive interference).
     More explicitly (for the usual inner product on Cd ), expanding the square gives
                           P             2       P            2
                                                                      P                     
                               k αk zk       =   k kαk zk k       +   i6=j < hαi zi , αj zj i ,

so I aggregates the (real parts of the) pairwise alignments hzi , zj i after scaling by αi , αj . In partic-
ular, I is sensitive not just to magnitudes but to relative directions/phases, which is exactly what
one wants from a numerical proxy for “resonance” versus “anti-resonance.”
    Example (scalar case d = 1): if z1 = z2 = 1 and α1 = α2 = 1, then ztot = 2 so I = 4 − (1 + 1) =
2 > 0. If z1 = 1 and z2 = −1, then ztot = 0 so I = 0 − (1 + 1) = −2 < 0. This makes I a natural
numerical surrogate for resonance/anti-resonance at the aggregate level.
    In intermediate situations I can be close to 0 even when individual terms are strong, meaning
that the aggregate is “balanced” by competing contributions; this is the quantitative sense in which
interference captures the difference between mere presence of strong components and their ability
to jointly amplify a shared direction.

                                                         69
Remark 94 (Why we allow zk ∈ Cd ). The extra dimension d allows us to embed multiple aspects of
evaluation simultaneously—for example, multiple propositions, multiple relational edges, or multiple
features of a pattern. This is a small but important generalization: resonance in rich systems is
seldom one-dimensional. The formalism here is kept minimal, but it anticipates later constructions
where patterns and contexts are multi-aspect objects (Hyperseed-Concept 86; Hyperseed-Concept 79).
    Allowing C (rather than restricting to R) is useful even if one ultimately interprets relation-
strengths as real-valued: complex phases provide a compact way to encode contextual “orientation”
or timing/ordering effects, so that two strong components can either reinforce (similar phase) or
suppress (opposite phase) without changing their magnitudes. In particular, the same magnitude
data kzk k can yield different aggregate behavior depending on relative phases, which mirrors the idea
that the same local evidence can support different global outcomes depending on context alignment.

Resonance as a driver of propagation. To connect resonance to later morphic-resonance
dynamics, we introduce the abstract form of a resonance-driven update rule.
   The point of isolating an abstract operator at this stage is that it factors “what is being propa-
gated” (the V -relation) from “how propagation composes” (the quantale algebra), so later sections
can swap in different concrete semantics for V without changing the propagation skeleton.
Definition 21 (Resonance-driven propagation operator (abstract form)). Let R1 , R2 : X × X → V
be V -relations in two contexts (or two subsystems). Let K ∈ V be a coupling strength. Define
                                                                          
                        ResK (R1 → R2 )(x, y) := R2 (x, y) ⊕ K ⊗ R1 (x, y) .

Remark 95 (Intuition and a minimal example of an update). This update says: the new relation-
value in context 2 is the old value, plus (in the quantale join sense) a contribution from context
1 scaled by coupling strength K. In the canonical p-bit quantale, ⊕ is componentwise max, so
this means the update can only increase evidence components: resonance propagation accumulates
rather than overwrites.
    Conceptually, K plays the role of a gain or transmissibility parameter: when K is low, even
strong structure in R1 has limited influence on R2 ; when K is high, R2 rapidly inherits (in the join
sense) the strongest components present in R1 . Because the update is pointwise in (x, y), this is the
minimal “local” propagation law; later dynamics can make K depend on (x, y) or on higher-order
pattern statistics.
    Example: if R2 (x, y) = (0.2, 0.1), K = (0.5, 0.5), and R1 (x, y) = (0.9, 0.8), then

                                     K ⊗ R1 (x, y) = (0.45, 0.4),

so ResK (R1 → R2 )(x, y) = (max(0.2, 0.45), max(0.1, 0.4)) = (0.45, 0.4). This captures the intu-
ition that strongly resonant structure in one context can “pull” another context toward similar
evaluations, without requiring them to become consistent or to erase prior opposition (Hyperseed-
Concept 159; Hyperseed-Concept 86).
    Note also that the form R2 ⊕ (· · · ) makes the prior state of context 2 explicit: propagation is
not a replacement map R2 7→ K ⊗ R1 , but a cumulative enrichment map. This is the algebraic
analogue of treating contexts as memory-bearing substrates rather than as ephemeral registers.
Remark 96 (Why this is the right minimal form). The operator ResK is:
• monotone in R1 , R2 , and K;

• explicitly paraconsistent: it can increase positive evidence without erasing negative evidence (and
  vice versa);

                                                 70
• compositional: repeated application composes via the quantale product.

Section 5 instantiates this operator numerically and shows how it reaches a “morphic resonance”
style update.
    The compositionality point can be read operationally as a semigroup law for propagation strength:
applying ResK1 and then ResK2 yields an effect equivalent to a single step whose effective contribution
from R1 is scaled by a combination of K1 and K2 as dictated by ⊗ and ⊕ (with the precise normal
form depending on distributivity properties available in the chosen V ). This is one reason to phrase
the update at the quantale level: the algebra already knows how to combine influences.

Remark 97 (Why monotonicity is a feature, not a limitation). One might object that real learning
sometimes decreases beliefs. That is correct; but the monotone operator here is intentionally the
minimal propagation primitive. Decrease and revision will later enter via additional dynamics:
decay, inhibition, competition between patterns, and anti-resonance mechanisms. In other words,
we first isolate a clean “transmission” law and then layer conflict-resolution and forgetting on top,
which is closer to how dynamical systems are often built in cognitive modeling [19].
    Technically, monotonicity is also what makes iterated updates well-behaved: one can form in-
creasing chains R2  ResK (R1 → R2 )  ResK (R1 → ResK (R1 → R2 ))  · · · and then study their
convergence or fixed points using standard order-theoretic tools when V supports them. This is
helpful later when “habit” is modeled as a stabilized relation-value under repeated exposure.

Definition 22 (Anti-resonance propagation (minimal choice)). Define the anti-resonance operator
by propagating negated evidence:
                                                                           
                  AntiResK (R1 → R2 )(x, y) := R2 (x, y) ⊕ K ⊗ (¬R1 (x, y)) .

Remark 98 (Intuition: transmitting the contrary and modeling habit reversal). Anti-resonance
propagation uses the same algebra as resonance but flips the incoming evidence via ¬. If R1 (x, y)
strongly supports a match, then ¬R1 (x, y) strongly supports a mismatch, and vice versa. The
resulting update tends to induce opposition or reversal in the target relation-values.
    Because ¬ is applied before the same ⊗-scaling and ⊕-accumulation, this operator is not a
different propagation mechanism but a different polarity of what is being transmitted. In paracon-
sistent settings (such as p-bit), this is crucial: transmitting the contrary does not require removing
the original support already present in R2 , so the target context can legitimately accumulate mixed
evidence and thereby represent tension, ambiguity, or internal conflict rather than being forced into
a prematurely consistent state.
    This gives a minimal formal hook for Hyperseed’s idea that some couplings do not reinforce but
rather destabilize or invert habits (Hyperseed-Concept 188; Hyperseed-Concept 114). The operator
is intentionally simple; later sections can refine it by making K depend on interference scores,
context similarity, or resource constraints.
    In particular, one can anticipate variants where K is large precisely when the interference
indicator I is strongly negative (net cancellation), so that anti-resonant channels become more
active when signals are out of phase; the present definition isolates the algebraic core needed for
such couplings without committing to a specific functional dependence.

Remark 99 (Toward “morphic” resonance). In Hyperseed terms, morphic resonance will arise
when resonance-driven propagation interacts with (i) repeated exposure over proto-time, (ii) rein-
forcement/decay (habit-taking and habit-reversal operators), and (iii) a pattern web structure that
makes some relation-values self-supporting. Those dynamical ingredients are added in Sections 5
and 12.

                                                  71
    From the perspective of the present minimal core, the key transition to “morphic” behavior is the
emergence of feedback loops: once propagated relation-values in one context begin to act as sources
for further propagation (possibly back into the original context, or into overlapping subcontexts), the
system can amplify particular relational regularities and thereby exhibit the characteristic persistence
associated with habits. The same feedback architecture can also sustain stable paraconsistent states
(simultaneous support and opposition), which is one reason the update primitives above are designed
to be compatible with non-classical evidence aggregation from the outset.


4    Core sanity theorems
Outline
    • Prove monotonicity properties that justify interpreting w(H) as “weakness.”

    • Prove basic boundedness/consistency properties for pattern intensity and resonance.

    • State minimal categorical coherence properties needed later (functoriality, enrichment laws).

Summary and Hyperseed concepts covered
These theorems are intentionally simple. They exist to ensure that the chosen core definitions be-
have in the expected direction: more collapsed distinctions means greater weakness, and resonance
behaves monotonically under coherent aggregation.

Hyperseed concepts covered.

    • Distinction; equivalence; simplicity/weakness; pattern intensity (as a later derived quantity).
      (Hyperseed-Concepts 98, ??, 169, 202, 143.)

    • Resonance/dissonance (as interference monotonicity). (Hyperseed-Concepts 159, 97.)

Standing notation. Fix a commutative quantale (V, ≤, ⊕, ⊗, e) and a set of entities X. Let µ :
X → V be an object-valuation. For a relation H ⊆ X × X interpreted as the set of undistinguished
pairs, recall the (quantale) weakness functional
                                              M
                                   w(H) =        µ(u) ⊗ µ(v).
                                              (u,v)∈H

(Here ⊕ is the quantale join/supremum.)

Remark 100. A brief decoding of the symbols may help fix the intended reading. A commutative
quantale is, in particular, a complete lattice (V, ≤) equipped with a commutative, associative “mul-
tiplication” ⊗ with unit e, such that ⊗ distributes over arbitrary joins ⊕. Thus ⊕ should be read as
a supremum (a generalized “maximum”), while ⊗ is the operation used to aggregate two pieces of
graded evidence or intensity. This is precisely the algebraic setting in which one can speak coherently
about combining local contributions and then taking their overall “best possible” aggregate; it is also
the basic technical vehicle for quantale-style weakness in the sense of [3] (see Hyperseed-Concept
143).
    The set X is the local universe of entities (occasion-tokens, perceived items, or internal states),
and µ : X → V assigns each entity a weight/importance in the evidence domain V . The relation


                                                  72
H ⊆ X × X collects pairs that an observer/context fails to distinguish (Hyperseed-Concept 98).
Then w(H) takes every undistinguished pair (u, v), scores it by the combined weight µ(u) ⊗ µ(v),
and aggregates all these scores via the join ⊕. Philosophically, this is a very Russellian move:
one takes an apparently qualitative notion (“weakness” as failure-to-separate) and pins it to a
monotone functional that can be reasoned about with lattice algebra, while leaving ample room for
the phenomenological interpretation (Hyperseed-Concepts 202, 169).
    It is also worth noting what information is, and is not, being retained. The functional w(H)
depends only on the set of undistinguished pairs, not on any additional structure (e.g. transitivity,
symmetry, or a metric-like notion of “how hard” a pair is to distinguish). Later sections may
impose additional axioms on H (for instance, taking H to be an equivalence relation, or the kernel
of an observation map), but the present sanity checks deliberately avoid such commitments: they
isolate the order-theoretic behavior that should hold for any coarsening of distinctions.
    Finally, the commutativity of ⊗ ensures that µ(u) ⊗ µ(v) does not depend on the ordering of the
pair. This matches the intended semantics when H is thought of as an undirected indistinction; if
one later studies directed or asymmetric indistinction (e.g. attentionally one-way confusions), then
one can still use the same formula, but should be explicit about whether H is closed under swapping
coordinates.
Theorem 1 (Weakness is monotone under adding undistinguished pairs). Let H, K ⊆ X × X with
H ⊆ K. Then w(H) ≤ w(K).
Remark 101. Intuitively, this theorem says: if you collapse more distinctions (i.e. you declare
more pairs to be “undistinguished”), then you cannot become less weak. This is exactly the di-
rection one expects if weakness is meant to proxy simplicity-as-coarsening: a coarser partition of
experience (more identifications, fewer discriminations) carries less articulated structure, hence rep-
resents a stronger “failure to distinguish” (Hyperseed-Concepts 98, 202; see also [2, 3] for related
motivations).
    This monotonicity is also a sanity check for later constructions. When patterns are modeled as
constraints that reduce the space of distinctions in a controlled way (Hyperseed-Concepts 130, ??),
we will repeatedly compare “baseline” and “pattern-induced” indistinction relations. The present
theorem guarantees that these comparisons can be made in the order-theoretic language of V without
logical surprises.
    One can also read the result contrapositively: if some intervention (a new measurement, a refined
conceptual scheme, an additional sensor) strictly decreases the computed weakness value, then it
must have eliminated at least one undistinguished pair of nontrivial weight. Thus w behaves like a
coarse “certificate” that refinement has occurred, even when one does not track which distinctions
were recovered.
Proof. Since H ⊆ K, every term µ(u) ⊗ µ(v) included in the join for w(H) also appears in the join
for w(K). Because ⊕ is a join (supremum) and hence monotone in each argument, adding more
terms cannot decrease the result.

Remark 102. Proof sketch. The strategy is to reduce everything to the elementary fact that
a supremum cannot go down when you enlarge the set you take the supremum over. Here the set
being “enlarged” is the collection of pair-scores µ(u) ⊗ µ(v) indexed by (u, v) ∈ H versus (u, v) ∈ K.
    Spelled out in lattice-theoretic terms, define two indexed families in V :
          A = {µ(u) ⊗ µ(v) | (u, v) ∈ H},    B = {µ(u) ⊗ µ(v) | (u, v) ∈ K}.
                                      L           L           L
Then
L HL  ⊆ K implies A ⊆ B, and w(H) =     A, w(K) =    B. Since     is the least upper bound,
  A ≤   B follows from A ⊆ B alone, with no need for any further algebraic properties of ⊗

                                                  73
beyond well-typedness. In particular, commutativity of ⊗ is conceptually natural but not used by
this specific monotonicity argument.
    This is one reason quantales are a convenient ambient structure: they provide (i) enough com-
pleteness so that arbitrary joins exist, and (ii) an order in which “more evidence aggregated” is
reflected
L         as “larger value.” Even in the degenerate case H = ∅, the same reasoning applies:
   (u,v)∈∅ · · ) is the join of the empty subset of V , hence equals the bottom element of the lattice
          (·
(often denoted ⊥), so monotonicity includes the base case ⊥ = w(∅) ≤ w(K) for all K.
    A useful mental model is the Boolean quantale V = {0, 1} with ⊕ = ∨ and ⊗ = ∧. If µ(x) = 1
for all x, then w(H) = 1 iff H is nonempty, and the theorem becomes the trivial statement that if
H ⊆ K and H is nonempty then K is nonempty. More informative is the fuzzy/probabilistic-like
setting V = [0, 1] with ⊕ = max and (for instance) ⊗ = ·; then w(H) returns the maximum pairwise
combined salience among the undistinguished pairs, so adding more undistinguished pairs can only
maintain or increase that maximum.
    In later applications, one often considers K = H ∪ H 0 where H 0 is the new set of collapsed
distinctions introduced by an additional pattern or aggregation step. The theorem then reads w(H) ≤
w(H ∪H 0 ), making explicit that pattern-driven coarsening can be tracked purely by order comparison
in V .

Proposition 1 (Weakness is monotone in each argument under unions). For any H, K ⊆ X × X
one has
                   w(H) ≤ w(H ∪ K)        and    w(K) ≤ w(H ∪ K).

Proof. Both inclusions H ⊆ H ∪ K and K ⊆ H ∪ K hold, so the claim follows immediately from
Theorem 1.

Remark 103. This simple corollary is often the operational form of monotonicity: “adding an
additional source of indistinction” is mathematically modeled by taking a union of relations. In
contexts where multiple pattern constraints contribute independently to collapse of distinctions, the
inequality above ensures that combining constraints by union can only increase (or leave unchanged)
the overall weakness score.
    If one later introduces a directed family of relations (Hi )i∈I with Hi ⊆ Hj for i ≤ j (successive
coarsenings), then repeated application yields a chain

                                      w(Hi ) ≤ w(Hj )   (i ≤ j),

so the weakness values themselves form an increasing net in the complete lattice V . This observation
is frequently used implicitly when taking limits of refinement/coarsening procedures, or when
    The key step is not computational but conceptual: interpreting w(H) W     literally as a join over
a family makes monotonicity immediate. In particular, if w(H) = { φ(e) | e ∈ H } for some
assignment φ into V , then enlarging H simply enlarges the index set of the join, and completeness
of the lattice ensures that taking the join over a larger family cannot decrease the value. One may
visualize H as a set of edges in a graph on X (edges mark “undistinguished” pairs). Adding edges
increases the pool of candidate weights, and a join/supremum can only stay the same or increase.
Equivalently, H ⊆ H 0 implies every upper bound of {φ(e) | e ∈ H 0 } is also an upper bound of
{φ(e) | e ∈ H}, so the least such upper bound (the supremum) satisfies w(H) ≤ w(H 0 ). This is
exactly the sense in which “monotonicity is baked into the definition”: no further algebraic identities
are required beyond the order-theoretic behavior of joins.

Definition 23 (One possible pattern-intensity functional (placeholder)). [TODO: Replace with
the final definition used in the paper.] A pattern intensity functional is a map Int : P → V

                                                  74
from a space of candidate patterns P to the quantale V that increases when a pattern yields a more
compressive (weaker/simpler) description of data relative to a baseline. Concretely, the intended
reading is that V plays the role of a graded evidence/score domain: larger elements represent “more
intensity” (however that is instantiated later), and the order ≤ is the sole structure used to compare
intensities across patterns. The definition does not require P to carry additional structure (such
as a lattice order), but later uses typically equip P with a refinement preorder so that monotonicity
statements become meaningful.
Remark 104. This definition is deliberately schematic: it identifies what a pattern-intensity must
do (be a graded score in V ) without committing to a single formula. Intuitively, P is the space of
“possible regularities” one might impose on data (Hyperseed-Concept 130), and Int(P ) measures
how much structural economy the pattern P buys you compared to not using it (Hyperseed-Concepts
169, 82). In particular, “baseline” is meant to capture whatever reference situation corresponds to
“no pattern” (or a default pattern family), so that intensity can be interpreted as a relative rather
than absolute score. In compression language, one imagines that a stronger pattern allows a shorter
description; in the weakness language, one imagines that a stronger pattern organizes indistinction
in a way that can be exploited for prediction or representation (cf. the pattern/emergence viewpoint
in [5]). The quantale viewpoint is that whatever concrete coding length or predictive advantage is
used, it is ultimately funneled into an ordered structure where joins, tensors, and monotone maps
preserve the comparisons one cares about.
    A simple toy example (consistent with later sections) is: let P specify that certain pairs in X ×X
must be treated as indistinct (or, conversely, must be distinguished), inducing a relation HP of
undistinguished pairs. Then Int(P ) can be a monotone function of w(HP ) relative to some baseline
Hbase . For instance, one may take F (a, b) = b (pure weakness-as-intensity), or F (a, b) = a ⊗ b
(combining baseline and pattern weakness multiplicatively/tensorially), or F (a, b) = b ⊕ a (a join-
style aggregation); the theorem below is formulated to cover such choices as long as monotonicity
is preserved. The point of keeping the definition abstract here is methodological: the later theory
wants theorems that depend only on quantale-algebraic monotonicity, not on the idiosyncrasies of
one specific intensity formula. In particular, by avoiding a fixed numeric encoding at this stage,
one can later change the enrichment base V (e.g. to Boolean truth values, costs, probabilities, or
degrees of evidence) without having to redo the monotonicity proofs from scratch.
Theorem 2 (Pattern intensity is bounded and respects refinement). Assume the intensity func-
tional Int is defined in the form
                                                                
                                  Int(P ) = F w(Hbase ), w(HP )

for some map F : V × V → V that is monotone in each argument and is constructed using only the
quantale operations ⊕, ⊗ and the order ≤. Then:
  1. ( Boundedness) Int(P ) lies between the least and greatest elements of V . Equivalently, writing
     ⊥ and > for the bottom and top of the underlying complete lattice, one has ⊥ ≤ Int(P ) ≤ >
     for every P ∈ P.
  2. ( Refinement monotonicity) If P refines Q in the sense that HP ⊆ HQ (i.e. P leaves weakly
     fewer pairs undistinguished than Q), then Int(P ) ≤ Int(Q). In words: moving to a finer
     pattern (fewer declared indistinguishabilities) cannot increase the weakness-based ingredient,
     so any monotone intensity aggregator cannot increase either.
Remark 105. In plain language, this theorem is saying two unsurprising but indispensable things.
First, the intensity score never “escapes” the universe of discourse: it is always some element of the

                                                 75
evidence lattice V , hence automatically confined between bottom and top. This is not a deep estimate
but a type discipline: once the codomain is V and V is a complete lattice, every term built from V -
operations has a well-defined place in the global order. Second, the ordering of patterns by refinement
is respected by the intensity score: when one pattern P is “sharper” than another Q (it collapses
fewer distinctions, i.e. it declares fewer pairs undistinguished), then the corresponding weakness-
based ingredient w(HP ) is smaller, and this order propagates through any monotone aggregator F .
Note that the subset condition HP ⊆ HQ is oriented so that refinement corresponds to removing
edges from the “undistinguished graph”: fewer edges means more distinctions are enforced.
    This connects directly back to Theorem 1: refinement monotonicity is not a new phenomenon
but a consequence of the same lattice-theoretic discipline. In later sections, this is what allows
one to treat “pattern selection” as a legitimate optimization or comparison problem, rather than
as a collection of metaphors (Hyperseed-Concepts 130, ??, 169; compare [5]). In particular, once
refinement induces an order on patterns, one can speak coherently about maximizing intensity,
computing Pareto frontiers under multiple scores, or proving existence of optima using completeness
properties (when they apply), all without leaving the order-enriched setting.

Proof. Because V is a complete lattice, it has a least element (bottom) and a greatest element
(top). Any expression built from ⊕ and ⊗ on elements of V evaluates to an element of V , hence is
automatically bounded between bottom and top. More explicitly, for any v ∈ V one has ⊥ ≤ v ≤ >
by definition of ⊥ and >, and therefore the same holds for v = Int(P ) regardless of how F is
parenthesized or composed, provided its values lie in V .
    For refinement monotonicity: if HP ⊆ HQ , then by Theorem 1 we have w(HP ) ≤ w(HQ ).
Monotonicity of F in its second argument (and the fact that w(Hbase ) is fixed across P, Q) yields
Int(P ) ≤ Int(Q). If one also varies the baseline across comparisons, then monotonicity in the first
argument would be needed as well; the present statement isolates the typical situation where the
baseline is held constant and only the pattern-induced relation changes.

Remark 106. Proof sketch. The proof separates into two independent observations. Boundedness
is immediate once one remembers that V is a complete lattice: there is simply nowhere else for
Int(P ) to land. Refinement monotonicity is a one-line reduction: HP ⊆ HQ implies w(HP ) ≤
w(HQ ) by Theorem 1, and monotonicity of F propagates the inequality to Int. In many concrete
instantiations, F will be built as a composition of monotone primitives (e.g. F (a, b) = (a ⊗ b) ⊕ a),
and the statement “constructed using only ⊕, ⊗ and ≤” is precisely what guarantees monotonicity
is preserved under such compositions.
    The key step is the use of structural monotonicity rather than any specific numeric property.
This is a recurring theme of the reconstruction: rather than rely on special arithmetic facts, we aim
to work in the generality of order, join, and tensor, so that the same argument can later be trans-
ported to other enrichment bases via change-of-quantale results (cf. Proposition 2 below). One can
also read this as a robustness claim: as long as the semantics of “combining evidence” is expressed
by monotone quantale operations, refinement comparisons of patterns will behave predictably across
models.

Definition 24 (Interference-based resonance and dissonance (sanity model)). Let I be a finite
index set and let a = (ai )i∈I be a finite family of complex-valued contributions ai ∈ C. Define the
resonance and dissonance by

                                    X                       X
                       Res(a) =           ai ,   Dis(a) =         |ai | − Res(a).
                                    i∈I                     i∈I



                                                  76
Intuitively, Res(a) measures coherent constructive interference, while Dis(a) measures the destructive-
interference gap relative to perfect alignment.
                                                                                     P        P
Remark 107. A few immediate sanity checks are worth keeping in view. Because | i ai | ≤ i |ai |
by the triangle inequality, Dis(a) ≥ 0 always, so dissonance is a nonnegative defect term measuring
the strictness
         P      of that inequality. At the extremes,P if |I| = 1 then Res(a) = |ai | and Dis(a) = 0,
while if i ai = 0 then Res(a) = 0 and Dis(a) = i |ai | (complete cancellation). Both Res and Dis
are also permutation-invariant in I (they depend only on the multiset of contributions), reflecting
that the model is agnostic to any ordering of “inputs.”
    It is also useful to note the scaling behavior: for any c ∈ C one has
                                                                 
                         Res (cai )i = |c| Res(a),     Dis (cai )i = |c| Dis(a),

so the model separates a global strength factor |c| from the internal alignment structure of the phases.

Remark 108. Here the notation is meant to be read with the ordinary geometry of the complex
                        P a = (ai )i∈I is a collection of “phasors” (vectors) in C, |z| denotes the
plane in mind. The family
complex
      P  modulus,   and   i∈I ai is their vector sum. Thus Res(a) is the length of the resultant vector,
while i |ai | is the sum of the lengths. The quantity Dis(a) is exactly the shortfall between these
two, i.e. how much cancellation occurs because the ai point in different directions.
    In particular, Dis(a) can be viewed as a quantitative proxy for “phase dispersion”: holding
 P magnitudes |ai | fixed, any increase in disagreement among arguments arg(ai ) tends to reduce
the
| i ai | and thereby increases Dis(a). For two contributions a1 , a2 6= 0 with relative angle ϕ =
arg(a2 ) − arg(a1 ), one has the explicit formula
                       p
             Res(a) = |a1 |2 + |a2 |2 + 2|a1 ||a2 | cos ϕ,  Dis(a) = |a1 | + |a2 | − Res(a),

so dissonance increases monotonically as cos ϕ decreases (i.e. as the vectors rotate away from one
another toward opposition).
    This interference model is intentionally modest: it supplies a mathematically sharp proxy for
the phenomenological language of resonance/dissonance (Hyperseed-Concepts 159, 97) without yet
importing the full paraconsistent-to-complex embedding discussed elsewhere in the document. It is
also aligned with the broader theme that “coherence” is a kind of constructive alignment and that
“conflict” is measured by cancellation; related developments coupling paraconsistent structure to
resonance-style propagation appear in [24].

Theorem 3 (Resonance is invariant under global phase and increases under coherent alignment).
Let a = (ai )i∈I be as in Definition 24.

  1. ( Uniform phase rotation invariance) For any real θ,

                      Res (eiθ ai )i∈I = Res(a),     Dis (eiθ ai )i∈I = Dis(a).
                                                                    


  2. ( Coherent-alignment monotonicity) For any real θ, define the aligned family a(θ) = (|ai |eiθ )i∈I .
     Then                                  X
                    Res(a) ≤ Res a(θ) =                  0 ≤ Dis a(θ) ≤ Dis(a).
                                                                      
                                              |ai |,
                                                i∈I
                           P
      Moreover, Res(a) =      i |ai | iff all nonzero ai share a common phase.




                                                  77
Remark 109. A useful way to read the statement is that Res depends only on relative phases
and magnitudes. Part (1) says that there is no distinguished “absolute reference direction” in the
complex plane: rotating the entire configuration rigidly cannot affect either the resultant length or
the cancellation defect. Part (2) identifies an extremal configuration at fixed magnitudes: among
all families with the same |ai |, the maximum possible resultant is achieved exactly by placing every
vector on the same ray (common phase), and the dissonance is then forced to vanish.
    The inequalities also clarify an interpretive asymmetry: alignment can only help resonance
(never hurt it), while misalignment can only increase dissonance (never decrease it), as long as
magnitudes are held fixed. In later applications, this gives a clean monotonicity principle: any
mechanism that reduces relative phase disagreement (or, more abstractly, reduces mutual contra-
diction among contributing terms) must move the model in the direction of larger Res and smaller
Dis.

Remark 110. This theorem formalizes two pieces of intuition that often remain implicit when
one speaks of “resonance.” First, resonance is not about absolute phase but about relative phase:
rotating every contribution by the same angle changes nothing. Second, resonance is maximized
when all contributions are aligned, in which case the resultant amplitude equals the sum of the
individual amplitudes and dissonance vanishes.
    The result is important mainly because it validates a particular direction of explanation used
later: if a coupling mechanism tends to align phases (or, more abstractly, tends to bring separate
evaluative contributions into mutual agreement), then resonance increases and dissonance decreases.
This is precisely the sort of monotone behavior one wants when resonance is used as a driver for
cross-context pattern propagation (Hyperseed-Concepts 131, 159, 168) rather than as a merely poetic
label.

Proof. (1) We have

                                       X              X      X
                      Res (eiθ ai )i =   eiθ ai = eiθ
                                    
                                                        ai =   ai = Res(a).
                                        i                    i      i

Also |eiθ ai | = |ai |, so the sum of magnitudes is unchanged, hence Dis is unchanged as well. Equiv-
alently, multiplying by eiθ is an isometry of C ∼ = R2 , so it preserves all Euclidean lengths appearing
in the definitions.
    (2) By the triangle inequality,
                                             X         X
                                                ai ≤        |ai |.
                                             i           i
                iθ   eiθ                                                                    ≤ Res(a(θ) ) =
     P                     P                                      P
But
P      i |ai |e   =       i |a
                             Pi |, whose   magnitude   is exactly   i |ai |. Thus Res(a)
                                                                                  P
   i |ai |. Since Dis(a) =      i |ai | − Res(a), increasing Res (with the same     i |ai |) decreases Dis,
and Dis(a(θ) ) = 0. One can also read this as: at fixed magnitudes, the maximal possible resultant
is achieved by placing every term so that its contribution to the projection along the common
direction is positive and maximal.
     Equality in the triangle inequality holds iff all nonzero summands have the same argument, i.e.
the ai are all nonnegative real multiples of a common eiθ .

Remark 111. Proof sketch. Part (1) uses the fact that multiplying a complex number by eiθ rotates
it without changing its length, and that absolute value is invariant under such rotations. Part (2)
is essentially the triangle inequality: the magnitude of a sum cannot exceed the sum of magnitudes,
with equality exactly when all vectors point the same way.

                                                    78
    The key step is recognizing that “alignment” can be expressed by replacing each ai with a vector
of the same length but common phase. Geometrically, one may picture the ai as arrows in the plane;
the resonant case is when the arrows lie on top of each other, so their endpoint-to-endpoint addition
is maximal, and the dissonant case is when they partially cancel. In this sense, Dis(a) is not an
additional primitive but a bookkeeping device that records precisely “how far” the configuration is
from saturating the triangle inequality, which is why it behaves well under the sanity checks above
(nonnegativity, vanishing in the fully aligned case, and maximality under total cancellation).
Proposition 2 (Minimal  L categorical coherence for weakness:Ljoin-homomorphism and change of
base). With w(H) =        (u,v)∈H µ(u) ⊗ µ(v) as above (where       denotes the arbitrary join in the
complete lattice V , so the definition makes sense for finite or infinite H):
  1. ( Complete join preservation) For any family of relations {Hj }j∈J ,
                                      
                                 [           M
                             w     Hj  =       w(Hj ),      w(∅) = ⊥V ,
                                   j∈J          j∈J

      where ⊥V is the least element of the lattice V . In particular, overlaps among the Hj do not
      affect the result: if a given pair (u, v) appears in more
                                                           L than one Hj , it contributes the same
      element µ(u) ⊗ µ(v) multiple times, but because         is a join (hence idempotent), repeated
      contributions do not change the supremum.
  2. ( Functoriality under quantale homomorphisms) If φ : V → W is a (commutative) quantale
     homomorphism (preserving ⊕, ⊗, e), and if µW := φ◦µ : X → W , then for every H ⊆ X ×X,
                                                
                                       φ wV (H) = wW (H),
      i.e. computing weakness commutes with change of enrichment base. Equivalently, the assign-
      ment H 7→ w(H) is natural with respect to strict change-of-base maps φ that preserve the
      operations used in the definition of w (joins and tensor), so that the same relational evidence
      is merely re-expressed in W rather than altered.
Remark 112. This proposition is the small categorical spine hidden inside an apparently elemen-
tary functional. Item (1) says that w behaves like a homomorphism from unions of relations to joins
in V : the weakness of “either H1 or H2 or · · · ” is the join of their weaknesses. This is exactly
what one wants if weakness is to be compatible with compositional constructions that build complex
indistinction relations by taking unions (for example, when forming closures or aggregating evidence
across subcontexts). Stated in slightly more algebraic terms, (1) says that w : P(X × X) → V is a
complete join-semilattice morphism when P(X × X) is ordered by inclusion and equipped with joins
given by unions: it preserves arbitrary joins and therefore is automatically monotone (if H ⊆ K
then w(H) ≤ w(K)), which matches the intuition that adding more indistinguishability pairs cannot
decrease the overall weakness.
    Item (2) is a “change of base” principle: if one maps the quantale V into another quantale W in
a structure-preserving way (via φ), then one can compute weakness either before or after applying φ
and get the same answer. This is the order-enriched analogue of functoriality, and it is what allows
later sections to shift between different evidence domains (e.g. probability-like versus possibilistic-
like) while keeping the formal meaning of weakness stable (cf. the quantale-oriented development
in [3]). Concretely, the point is that w(H) is built from µ using only two constructors: taking
tensor-products µ(u) ⊗ µ(v) and then taking their join; a quantale homomorphism preserves exactly
these constructors, so it cannot “see” any difference between “compute-then-map” and “map-then-
compute.”

                                                  79
Proof. (1) Expand definitions and use that ⊕ is the join in V :
                  
              [             M                    M M                        M
           w Hj  =              µ(u) ⊗ µ(v) =               µ(u) ⊗ µ(v) =   w(Hj ).
               j             (u,v)∈∪j Hj                  j   (u,v)∈Hj             j


Also, the empty join is ⊥V , so w(∅) =S⊥V . A slightly more explicit way to read the middle equality
is that taking the join over the set j Hj is the same as taking the join over the disjoint union
of indexing data {(j, (u, v)) | (u, v) ∈ Hj } and then observing that repetitions do not matter for
suprema: if the same pair (u, v) is indexed multiple times, its contribution is duplicated but the
join remains unchanged.
    (2) Using preservation of joins and tensor by φ:
                                     
                 M                         M                      M
φ wV (H) = φ           µ(u) ⊗ µ(v) =           φ(µ(u)⊗µ(v)) =         φ(µ(u))⊗φ(µ(v)) = wW (H).
                   (u,v)∈H                 (u,v)∈H                       (u,v)∈H

Here the second equality is exactly the “arbitrary-join preservation” part of being a quantale
homomorphism, while the third equality is multiplicativity with respect to ⊗; together they ensure
that φ commutes with the syntactic formation of w from µ. In particular, no special finiteness
assumptions on H are needed: the argument applies uniformly to infinite joins because quantales
are, by definition, complete join-semilattices with ⊗ distributing over arbitrary joins, and φ is
assumed to respect this structure.

Remark 113. Proof sketch. For (1), the proof strategy is to “flatten” the indexing: taking the join
over a union of sets is the same as taking a join over each set and then joining those results. This
is the lattice-theoretic content of complete additivity with respect to unions. For (2), the strategy
is to push φ through the defining expression for w using the fact that a quantale homomorphism
preserves the operations used to build that expression. One can also view both statements as “no-
surprises” coherence conditions: w is assembled from universal constructions (joins) and monoidal
structure (tensor), so it must respect the canonical ways of rearranging those constructions.
    The crucial steps
                   L are exactly where the quantale axioms enter: preservation of arbitrary joins
(to move φ past ) and preservation of tensor (to rewrite φ(µ(u) ⊗ µ(v)) as φ(µ(u)) ⊗ φ(µ(v))).
Visually, one can think of (2) as asserting that “measuring weakness” is invariant under a consistent
change of measuring instrument: applying a monotone, structure-respecting regraduation of the
evidence scale does not alter the computed weakness, aside from expressing it in the new units. For
example, if V encodes evidence in one scale (say, additive costs) and W encodes it in another (say,
a normalized or clipped cost domain), then a homomorphism φ that preserves the relevant joins and
combinations ensures that the computed weakness is transported faithfully; what changes is only the
codomain in which the resulting bound is reported.


5    Toy model: finite universe, p-bit quantale, and morphic reso-
     nance demo
Outline
• Fix a small finite universe X and two contexts C1 , C2 .

• Represent each context’s “indistinction judgments” by a V -valued relation Ri : X × X → V .


                                                     80