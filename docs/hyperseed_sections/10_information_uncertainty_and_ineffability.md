# 10 Information, uncertainty, and ineffability

Definition 88 (Contextual description complexity). For x ∈ EC , define

                          sC (x) := inf{costC (`) : ` ∈ LC , DecC (`) = x}.

We interpret lower sC (x) as “simpler for C” (less representational effort).

    The use of inf (rather than min) accommodates description languages with arbitrarily fine
approximations or parameterizations: one may be able to describe x increasingly cheaply while
approaching it in a limiting sense, or there may be no single cheapest description even though
costs can be driven down to a greatest lower bound. In many discrete settings (finite strings, finite
programs with integer-valued costs), the infimum is attained and sC (x) is a true minimum. If there
is no ` with DecC (`) = x, the set in the infimum is empty and one may take sC (x) = ∞, expressing
that x is indescribable (or not individuated) within the representational resources of context C.
    It is also useful to keep in mind that sC is relative in two ways: it depends on what counts as a
description (the choice of LC ) and on how descriptions are interpreted (the choice of DecC ). Thus,
changes in measurement conventions, available primitives, background knowledge, or permissible
abstractions are all legitimately represented as changes in C (and hence changes in sC ).

Remark 402. One can equivalently define sC via compositional simplicity recursion (as in Hy-
perseed’s informal definition) by choosing a grammar for building entities and taking sC (x) to
be the least total effort of any parse tree yielding x, including glue/interaction overheads. The
description-based definition above is the most portable because it separates (i) the space of possible
representations from (ii) the evaluator/decoder.

    Concretely, the “parse tree” viewpoint treats a description as an explicit construction plan:
internal nodes correspond to applications of combination rules (often modeled by ∗C or by a family
of typed composition operators), while leaves correspond to primitives (atomic symbols, stored
concepts, measurements, or retrieved exemplars). In that view, glue/interaction overheads capture
the costs of making parts compatible: specifying alignment, resolving interfaces, setting boundary
conditions, or adding correction terms needed for the composite to decode to the intended entity.
The description-based formulation packages all of these choices into LC , DecC , and costC , which
is why it can be transported across domains even when the natural “parts” and “composition”
operations differ dramatically.
    To connect to the formal core (Section 3), it is often useful to allow the system to store not only
scalar costs but also p-bit-valued evidence about whether a putative description actually matches
its target. This is optional, but it is exactly where paraconsistency becomes practically relevant:
many cognitively useful “patterns” are compressive but partly wrong.
    One motivation is that, in practice, an observer often deploys short descriptions that intention-
ally ignore exceptions (e.g., “birds fly”, “objects are rigid”, “noise is Gaussian”). Such descriptions
can be excellent compression devices (low cost) even when they conflict with some data (nonzero
mismatch). Separating “how cheap is the description?” from “how well does it fit?” allows us to
model the common situation where a representation is preferred because it is simple and informa-
tive, not because it is perfectly accurate.

Definition 89 (p-bit-valued mismatch evidence). Fix a context C. A mismatch evidence map is
any function
                                  misC : LC × EC → [0, 1]2
where misC (`, x) = (m+ , m− ) is interpreted as (positive, negative) evidence that ` fails to match x
in context C.


                                                 179
    The two coordinates in misC (`, x) = (m+ , m− ) are intended to support paraconsistent situa-
tions in which evidence can accumulate on both sides: m+ can be high because there are clear
counterexamples to the description, while m− can simultaneously be high because there are strong
confirmations (or because the context provides reasons the mismatch diagnosis is unreliable). In
particular, the framework does not require that “evidence for mismatch” and “evidence against
mismatch” sum to 1; allowing both to be nontrivial is what lets the system represent partial,
conflicting, or heterogeneous fit in a controlled way.
    Operationally, one can use misC in several (compatible) ways without fixing a single choice here:
as a feasibility filter (only accept descriptions with m+ below a threshold), as an additive penalty
term combined with costC (trading off simplicity and mismatch), or as a record used downstream to
decide which aspects of a description are trustworthy. In applications where a single scalar is desired,
one may derive a mismatch score from the pair (e.g., by a context-dependent aggregation), but
keeping the pair explicit preserves information about conflict and uncertainty that would otherwise
be collapsed.

9.2   Combination, inheritance, and association as pattern-level notions
Hyperseed distinguishes dynamic combination (co-becoming in time) from static combination (prop-
erty union/blend). The present section focuses on the static side (the dynamic side is reconstructed
via proto-time and event/process calculi in Section 7). In particular, “static” should be read as
“evaluated at a fixed descriptive moment”: we intentionally ignore the micro-history of how a com-
pound came about, and only keep the resulting blend of relevant traits. This separation is method-
ological: the same pair of entities may admit both a temporally detailed story of co-formation
(dynamic combination) and a temporally collapsed account in which only the resulting pattern
profile matters (static combination).

Definition 90 (Static combination in a context). A static combination system in context C is a
pair (EC , ∗C ) where ∗C is a partial binary operation on EC . We write A ∗C B when the combination
is defined.

    The explicit dependence on C is essential: which combinations are meaningful, admissible, or
even nameable depends on the background ontology and the representational resources assumed in
that context. Thus EC should be read as “the entity-kinds currently in play,” and ∗C as the rule by
which the context permits us to form composites/blends at the static (property-level) description
scale. The partiality of ∗C is not merely a technical convenience: it encodes the idea that some pairs
do not have a well-formed blend in the chosen descriptive scheme, or that a purported blend would
require introducing new entity-types not available in EC . No algebraic laws (such as commutativity
or associativity) are assumed a priori; when such laws hold in a given application, they should be
stated as additional structure on (EC , ∗C ) rather than taken for granted.

Remark 403. Many important cases are naturally typed or multi-sorted: ∗C is only defined on
compatible pairs. This is not a defect; it is exactly what makes combination systems suitable as
ontologies.

   Concretely, “compatible” may mean sharing an interface (e.g. two modules with matching
ports), belonging to the same sort (e.g. two color swatches that can be mixed), or satisfying a
constraint (e.g. two roles that can co-occupy a narrative position without contradiction). In such
cases one can think of ∗C as implicitly carrying a typing judgment: only when the judgment suc-
ceeds do we get a combined entity in EC . When combination is undefined, that is informative: it


                                                  180
marks a boundary of what the context treats as a coherent object of discourse, rather than forcing
an artificial “junk” element to stand for incoherence.
    Inheritance and association are also most naturally defined using patterns and properties, but we
give early “pre-definitions” now (and tighten them after properties are defined). The intent is that
these notions operate at the level of pattern-roles (how an entity behaves in typical constructions)
rather than at the level of internal constitution: inheritance concerns what can stand in for what,
while association concerns what tends to co-appear or co-fit within the same descriptive frame.
Definition 91 (Inheritance as substitutability (preorder form)). Fix a context C. A relation C
on EC is an inheritance preorder if A C B means “A can substitute for B in many C-relevant
contexts without increasing representational effort or breaking too many patterns.”
    The phrase “preorder form” signals that, in typical instantiations, C is intended to be at least
reflexive and transitive (while not necessarily antisymmetric): distinct entities may be mutually
substitutable at the granularity that C cares about, yielding equivalence classes of “effectively the
same role”. The qualifier “many C-relevant contexts” is also deliberate: substitutability is rarely
absolute, so C should be understood as summarizing a stability of use across a sufficiently rich
family of pattern-instances judged important in C. Likewise, “representational effort” is meant to
capture the cost of accommodating the substitute (e.g. extra clauses, exceptions, or ad hoc repairs),
so inheritance becomes a notion tied to the economy of pattern-description rather than mere set
inclusion.
Remark 404. Later we instantiate C by comparing property-sets (Definition 98) or by requiring
existence of low-effort rewrite maps in a combination system.
    In property-set terms, the guiding picture is that A C B holds when A carries (most of)
the properties that make B usable in the patterns of interest, possibly together with additional
properties that do not interfere too often. In rewrite-map terms, the idea is that there is a systematic
way to translate occurrences of B into occurrences of A with small overhead, so that pattern-
instances remain largely valid after substitution. Both readings emphasize that inheritance is not
simply a static taxonomic claim, but a claim about preservation of pattern-function under controlled
replacement.
Definition 92 (Association (static version)). A (static) association score in context C is a sym-
metric map
                                   assocC : EC × EC → [0, 1]
intended to measure “how much A and B tend to occur together” or “how many properties/patterns
they share.”
     The symmetry requirement reflects the intended reading as co-occurrence or overlap rather than
directional implication. No further axioms are imposed here: depending on the application, one
might want assocC (A, A) = 1, or monotonicity with respect to inheritance, or triangle-type con-
straints, but these should be added only when justified by the chosen construction. The codomain
[0, 1] should be interpreted as a normalization convention: association is meant to be compara-
ble across pairs in the same context, even when raw counts or unnormalized overlaps would be
scale-dependent. When association is later implemented via property-sets, typical examples in-
clude normalized overlap coefficients (such as Jaccard similarity) or weighted variants in which
some properties contribute more heavily because they anchor more central patterns in C.
     Dynamic notions of association (via short chains of becoming, or temporal co-focusing) are
treated in Sections 7 and 12. Here we will implement association in terms of overlap between

                                                  181
property-sets (Definition 101). This implementation is meant to make explicit the bridge between
“co-occurs” and “co-describes”: if two entities share many of the properties that matter to the
context, then they will tend to appear together in pattern-instances and will also be easy to group,
compare, or blend without introducing exceptional-case bookkeeping.

9.3     Patterns and pattern intensity
We now formalize Hyperseed’s key operational definition:

        A pattern is a representation as something simpler.

    There are two complementary ways to say this rigorously: (i) the description-theoretic way
(a code ` for x with lower effort than baseline), and (ii) the compositional way (a factorization
of x into simpler components with bounded glue cost). In practice, these two views are often
intertranslatable: a compositional factorization can be encoded as a structured description (e.g.
a parse tree), while a good description typically implies some latent factorization (e.g. reuse of
subroutines, shared parameters, or repeated motifs). The point of stating both is that different
applications make different primitives more natural: for a string, a description is immediate; for a
physical or semantic object, an explicit “parts + interaction” picture can be the clearer witness.

9.3.1     Patterns as compressive descriptions
Definition 93 (Pattern witness (description form)). Fix a context C. A pattern witness for x ∈ EC
is any ` ∈ LC with DecC (`) = x. Its description cost is costC (`).

    The role of LC , DecC , and costC is to make explicit what counts as an admissible representation
and what “effort” means for the observer in context C. For example, costC might be literal bit-
length, runtime, description length under a grammar, MDL-style codelength (data plus model), or
an experimentally grounded cognitive effort proxy. Allowing such flexibility is essential later when
the same underlying entity is judged by different observers or under different resource constraints.
    In this raw form, every entity has infinitely many “patterns” (by trivial re-encoding). The
nontrivial content comes from relative simplicity. Concretely, without a reference point, one can
always define a baroque coding language in which a particular x has a one-token name, thereby
making it “simple” by fiat. The baseline mechanism below is what prevents such vacuity: it forces
simplicity to be measured relative to a fixed default scheme rather than an adversarially chosen
code.

Definition 94 (Baseline description and compression gain). Fix a context C. Choose a baseline
description scheme for entities, represented by a function baseC : EC → LC with DecC (baseC (x)) =
x. Define the baseline cost
                                    sbase
                                     C (x) := costC (baseC (x)).

Given any witness ` of x, define the (raw) compression gain

                                   ∆C (`; x) := sbase
                                                 C (x) − costC (`).

    The quantity ∆C (`; x) is positive exactly when ` improves on the baseline, and negative when `
is a worse-than-default way to represent x. Keeping ∆C in “absolute units” (whatever units costC
uses) is convenient for aggregating costs across compositions; later, the normalized intensity IC will
rescale this gain into a unit interval.


                                                 182
Remark 405. The baseline is part of the observer model: different observers have different “de-
fault” ways of representing the same thing, so they will see different patterns. This is not optional;
it is Hyperseed’s observer-relativity made explicit. A useful way to read sbase
                                                                              C (x) is “how hard x is
before I notice any structure”; then a pattern witness is precisely a certificate that the observer can
exploit some structure to do better.

   It is often helpful to distinguish the baseline cost sbase
                                                          C (x) from any other intrinsic or task-
dependent simplicity measure sC (x) used elsewhere in the paper. Here, the baseline is deliberately
operational: it is defined by a concrete encoding choice baseC , so that “compression” is not merely
metaphorical but literally an improvement over what the observer would otherwise do by default.

9.3.2   Patterns as compositional factorization
To mirror Hyperseed’s (y, z)-pattern picture, we represent patterns as explicit decompositions.
Intuitively, x = y ∗C z asserts that x can be assembled from parts y and z using the context’s
composition operator, while t accounts for the additional coordination or interaction cost not al-
ready paid for by describing y and z separately. This makes the notion of a “pattern” align with
common scientific and engineering practice: a system is understood by specifying components plus
a (hopefully small) interaction law.

Definition 95 (Compositional pattern witness). Fix a context C. A compositional pattern witness
for x ∈ EC is a tuple
                                        P = (y, z, t)
such that y, z ∈ EC , x = y ∗C z, and t ∈ R≥0 is an explicit glue/interaction overhead intended to
upper bound the extra effort needed to assemble the composite from its parts in context C.
   Define the composite cost
                                    hC (P ) := sC (y) + sC (z) + t.

    The requirement t ≥ 0 encodes the idea that composition is never “free” in the accounting:
even when the parts are known, there is at least the bookkeeping cost of specifying how they are
combined. At the same time, by allowing t to vary by witness, this framework can represent both
clean modular decompositions (small t) and strongly entangled composites (large t), which will
later be relevant for distinguishing mere aggregation from genuine emergent interaction.

Remark 406. If one has a direct syntactic representation ` for the composite (e.g. a parse tree),
t can be derived from the overhead terms in the interpreter; in algorithmic settings t is often a
“model class” penalty (e.g. number of parameters, constraint complexity). In MDL terms, one may
think of sC (y) + sC (z) as the cost of stating the components, and t as the cost of stating the linking
hypothesis (alignment, coupling constants, wiring diagram, interface spec, etc.).

    Note that hC (P ) is written using sC (y) and sC (z) rather than sbase          base
                                                                        C (y) and sC (z). This is
intentional: a compositional witness is meant to exploit whatever simplicity notion sC the context
provides for parts, while still being judged against the baseline for the whole x when we compute
intensity. This matches the informal picture “a pattern is worthwhile if it makes the whole cheaper
than my default way of describing the whole,” even if the parts themselves are described using
specialized (non-baseline) codes.




                                                  183
9.3.3   Pattern intensity
Hyperseed defines pattern intensity as normalized improvement over baseline (in the compositional
case, improvement of hC over the baseline sC (x)). We adopt that, with two small refinements: (i)
we clamp at 0 so that “non-patterns” have intensity 0, and (ii) we optionally add a p-bit negative
component to record mismatch evidence.
     The normalization by sbase
                             C (x) makes intensity comparable across entities of different absolute
sizes: saving 10 units of cost is a bigger deal when the baseline is 20 than when it is 2000. Clamping
at 0 ensures that “actively worse” representations do not create misleading negative intensities;
instead, they simply fail to count as patterns under the intensity measure, while their costs can
still be tracked separately if needed.

Definition 96 (Scalar pattern intensity). Fix C and x ∈ EC with sbase
                                                                   C (x) > 0. For any description
witness ` of x, define the scalar intensity

                                              sbase
                                                                
                                               C (x) − costC (`)
                          IC (`; x) := max 0,                      ∈ [0, 1].
                                                    sbase
                                                     C (x)

For any compositional witness P = (y, z, t) of x, define

                                               sbase
                                                               
                                                C (x) − hC (P )
                        IC (P ; x) := max 0,                      ∈ [0, 1].
                                                     sbase
                                                      C (x)

If sbase
    C (x) = 0, set IC (·; x) = 0 by convention.

   As a quick calibration: if costC (`) = sbase
                                             C (x), then IC (`; x) = 0 (no improvement); if costC (`) =
1 base                       1                        base
 s
2 C    (x), then IC (`; x) = 2 ; and if cost C (`) ≥ sC (x), the clamping forces IC (`; x) = 0 rather
than a negative value. Thus, intensities near 1 correspond to dramatic simplifications relative to
baseline, and intensities near 0 correspond to either negligible simplification or none at all.

Proposition 7 (Basic sanity properties of intensity). Fix C and x.

1. 0 ≤ IC (P ; x) ≤ 1 for all witnesses P of x.

2. IC (P ; x) > 0 if and only if hC (P ) < sbase
                                            C (x) (strict compression).

3. If P and Q are witnesses of x with hC (P ) ≤ hC (Q), then IC (P ; x) ≥ IC (Q; x).

Proof. All items follow directly from Definition 96: the ratio lies in (−∞, 1], clamping yields [0, 1],
and the map u 7→ max{0, (s − u)/s} is monotone decreasing in u for fixed s > 0.

    One additional consequence (used implicitly later) is that intensity is invariant under uniform
rescaling of cost units within   a fixed context: if all costs are multiplied by a positive constant, the
ratio sbase
                              base
        C   (x) −  cost C (`) /sC (x) is unchanged. What does change intensity is any shift in what
the observer treats as baseline, which is exactly as intended: intensity measures improvement over
what the observer would have done by default.
    Now incorporate paraconsistency: the positive component measures compressive strength, while
the negative component records evidence of mismatch (“strong but wrong”). This lets us represent
the common situation in which a hypothesis yields a compact description but only approximately fits
the data (or fits in one regime while failing in another), without forcing the entire representational
apparatus to collapse into triviality.


                                                  184
Definition 97 (p-bit pattern intensity). Fix C and assume a mismatch map misC (Definition 89).
For any description witness ` of x, define a p-bit intensity
                          IntC (`; x) := IC (`; x), misC (`, x)+ ∈ [0, 1]2 ,
                                                                

where misC (`, x)+ is the positive-evidence component that ` mismatches x. (Alternative conventions
are reasonable; the only requirement for later sections is monotonicity in compression-gain and
mismatch evidence.)
    This two-coordinate view separates two axes that are often conflated: how useful the pattern
is as a compressor versus how trustworthy it is as an account of x. For instance, a coarse model
might yield high IC (`; x) by exploiting a strong regularity, yet still incur non-negligible mismatch
evidence because it ignores boundary effects or rare events; conversely, an exact but cumbersome
encoding may have low intensity while having essentially zero mismatch evidence.
Remark 407. This construction is intentionally permissive: it lets a system retain a compressive
pattern even when it is partially false, without forcing triviality. That is precisely the role of
paraconsistent logic in the ontology. Operationally, later selection rules can prefer patterns that
are simultaneously high-intensity and low-mismatch, but the representation itself does not have to
discard a high-intensity idea merely because it is not perfectly accurate.

9.4   Properties as fuzzy sets of patterns
Hyperseed’s property notion is derived: properties are patterns, collected and graded by intensity.
Concretely, one begins with whatever family of pattern-detectors PC is deemed relevant to a context
C (logical predicates, learned features, dynamical motifs, compression primitives, etc.), and then
treats an object’s “having a property” as nothing more (and nothing less) than exhibiting the
corresponding pattern with some graded strength. In this sense, the property vocabulary is not
primitive: it is induced by the pattern vocabulary, and any change in PC (or in the intensity
functional IC ) changes the resulting property semantics. It is also important that C is explicit: the
same entity may support very different salient patterns in different contexts, so PropC (x) should
be read as a context-indexed description rather than an absolute inventory of intrinsic attributes.
Definition 98 (Property-set). Fix a context C and a space of candidate patterns PC . The property-
set of x ∈ EC is the fuzzy set
                      PropC (x) : PC → [0, 1],      PropC (x)(P ) := IC (P ; x).
If one uses p-bit intensity (Definition 97), then PropC (x) is p-bit-valued instead.
     This is an explicit “feature map” induced by patterns: it sends an entity x to a membership
function on PC . If PC is finite, then PropC (x) can be viewed as a vector in [0, 1]|PC | ; if PC is
countable, as a bounded sequence; and if one generalizes further (e.g. measurable pattern families),
as a bounded function suitable for integration against weights. The fuzzy-set reading is deliberate:
a pattern P is not simply “present” or “absent,” but can be present to a degree, matching the idea
that real-world regularities are often partial, noisy, or scale-dependent.
     When p-bit-valued intensities are used, the codomain changes but the role does not: PropC (x)(P )
still represents the strength of evidence (in the particular p-bit sense) that x supports P . One can
always recover an [0, 1]-valued proxy (for instance, by mapping a p-bit value to an expected degree,
a probability of detection, or another application-specific scalarization), but keeping p-bit values
can be useful when one wants intensities that compose more naturally under operations introduced
elsewhere.

                                                 185
Definition 99 (Mass of a property-set (one simple choice)). Assume PC is finite or countable.
Define the mass of the property-set as
                                               X
                               kPropC (x)k1 :=   PropC (x)(P ).
                                                   P ∈PC

    This L1 -style mass is the simplest aggregate notion of “how many patterns are present, counting
multiplicity by intensity.” In particular, it distinguishes the case where x weakly supports many
patterns from the case where it strongly supports only a few, while still remaining additive over the
pattern index. For a finite PC , the mass is automatically finite and lies in [0, |PC |]; for a countably
infinite PC , finiteness becomes a substantive condition and can be enforced by choosing PC so
that only finitely or summably many patterns havePnon-negligible intensity on typical entities, or
by introducing weights w(P ) ≥ 0 and considering P w(P )PropC (x)(P ) when different patterns
carry different saliencies or costs.

Remark 408. This mass is a pattern-theoretic analogue of “how much structured regularity” is
present. More sophisticated variants can correct for overlap between patterns (see the “structural
complexity” discussion in Section 8).

    A useful way to interpret the overlap issue is that two distinct patterns P, Q ∈ PC may be
systematically co-triggered by the same underlying regularity, so summing their intensities can
double-count evidence. Correcting for this can be done by (i) discounting redundancy via sim-
ilarity/implication relations among patterns, (ii) selecting approximately independent subsets of
patterns, or (iii) passing from a raw pattern-family to a factorized or minimal basis (when such
a notion is available). The present definition intentionally stays minimal: it supplies a baseline
quantity that is easy to compute and easy to replace.

9.4.1   Inheritance and association via properties
We can now instantiate inheritance and association in a canonical way. The guiding idea is that
once entities are represented by their pattern-intensity profiles, standard set-theoretic relations
and similarities can be lifted to the fuzzy setting, yielding orderings (for “is-a”-like relations) and
symmetric scores (for “related-to”-like relations) directly from the same data.

Definition 100 (Inheritance via property inclusion). Fix C. Define an inheritance preorder on
EC by
              A C B ⇐⇒ PropC (A)(P ) ≥ PropC (B)(P ) for all P ∈ PC .

    Because the condition is pointwise in P , C is automatically reflexive and transitive, hence
a preorder (antisymmetry may fail if two distinct entities have identical property-sets on PC ).
Equivalently, A C B means that PropC (B) is a fuzzy subset of PropC (A) under the usual product
order on [0, 1]PC . This matches the intuition that A can stand in for B with respect to all pattern-
tests in PC : any pattern that manifests in B manifests no less in A.

Remark 409. This reads: “A inherits from B” when every pattern/property that characterizes
B is present (at least as strongly) in A. This is a direct mathematical rendering of Hyperseed’s
“substitutability in contexts.” In applications, one usually weakens the ∀P requirement to a weighted
or thresholded version.




                                                  186
   Two common weakenings, both compatible with the same conceptual picture, are: (i) a slack-
ened inclusion condition such as PropC (A)(P ) ≥ PropC (B)(P ) − ε(P ) for pattern-dependent tol-
erances ε(P ) ≥ 0 (useful when intensities are noisy), and (ii) a weighted aggregate condition such
as                        X                                         
                              w(P ) PropC (B)(P ) − PropC (A)(P ) + ≤ δ,
                         P ∈PC
where (t)+ := max{t, 0} measures shortfall of A relative to B and w(P ) encodes salience. These
variants preserve the idea that inheritance is driven by systematic dominance of property intensity,
while allowing controlled exceptions or trading off minor deficits against major matches.
Definition 101 (Association from property overlap). Fix C. Define the (symmetric) association
score                             P
                                    P ∈PC min{PropC (A)(P ), PropC (B)(P )}
                 assocC (A, B) := P
                                   P ∈PC max{PropC (A)(P ), PropC (B)(P )}
with the convention 0/0 := 0.
    This ratio lies in [0, 1] whenever the denominator is nonzero. It equals 1 precisely when the
two property-sets agree pointwise (on all patterns that appear in at least one of them), and it
approaches 0 when their supports (in the fuzzy sense) are largely disjoint. The 0/0 := 0 convention
corresponds to treating two entities with identically zero intensity on every candidate pattern (i.e.
indistinguishable “blank” descriptions relative to PC ) as having no meaningful association signal
under this particular score; alternative conventions are possible, but the present one keeps the score
conservative in the absence of evidence.
Remark 410. This is a fuzzy Jaccard similarity. Other similarity measures (inner product,
Hellinger distance, Hutchinson metric on induced measures) fit the same role; the later “pattern
web” construction (Section 11) can be built from any reasonable choice.
    The choice of similarity is partly a modeling decision about what “overlap” should mean. Jac-
card emphasizes shared intensity relative to total exhibited intensity, hence it is naturally scale-
sensitive to the union of properties; inner-product-based scores emphasize co-activation but can be
dominated by overall mass; and distributional distances (e.g. Hellinger) become particularly natural
if one normalizes PropC (x) to a probability distribution over patterns when kPropC (x)k1 > 0. All
of these remain instances of the same general recipe: represent entities by graded pattern profiles,
then apply a similarity/divergence on those profiles to obtain an association primitive suitable for
building higher level relational structure.

9.5   Emergence
Hyperseed defines emergence of (A, B) (relative to a combination operation ∗) as the collection of
patterns that become more intense in A ∗ B than is explained by A and B separately. Intuitively,
the comparison is made pattern-by-pattern: a candidate pattern P is deemed emergent when
its measured intensity in the composite exceeds an explicit baseline prediction formed from the
intensities of P in each part. The role of the baseline is to distinguish genuinely “interaction-
driven” structure from structure that is already present in A or in B alone and would therefore be
expected to appear in the composite even without additional organization.
Definition 102 (Weighted baseline for emergence). Fix C and A, B ∈ EC with sbase   base
                                                                            C (A)+sC (B) >
0. Define weights
                                  sbase
                                   C (A)                                  sbase
                                                                           C (B)
                wC (A) :=                     ,         wC (B) :=                     .
                            sC (A) + sbase
                             base
                                        C (B)                       sC (A) + sbase
                                                                     base
                                                                                C (B)


                                                  187
Remark 411. Definition 102 produces a convex weighting in the sense that wC (A), wC (B) ≥ 0
and wC (A) + wC (B) = 1. The condition sbase             base
                                             C (A) + sC (B) > 0 rules out the degenerate case
in which neither entity contributes any baseline “mass” for constructing a meaningful prediction.
When sbase               base
       C (A) = 0 and sC (B) > 0 (or vice versa), the baseline reduces to the nonzero contributor,
so emergence is measured relative to the part that carries the entire baseline weight in context C.

Definition 103 (Emergent intensity and emergent set). Fix C and assume A ∗C B is defined. For
a pattern candidate P ∈ PC , define the emergent surplus
                                                                                       
             SurC (P ; A, B) := IC (P ; A ∗C B) − wC (A) IC (P ; A) + wC (B) IC (P ; B) .

Define the emergent intensity

                             EmerC (P ; A, B) := max{0, SurC (P ; A, B)}.

The emergence of (A, B) is the fuzzy set P 7→ EmerC (P ; A, B), or the crisp set {P : EmerC (P ; A, B) >
0} if desired.

Remark 412. The surplus SurC (P ; A, B) is permitted to be negative: this corresponds to a pattern
candidate whose intensity is suppressed in the composite relative to the weighted baseline. Defini-
tion 103 focuses the notion of emergence on “positive novelty” by clamping negative surplus to 0
via max{0, ·}. In settings where suppression is also of interest, one can still recover it directly from
SurC (P ; A, B) without altering the present definition.

Remark 413. Because the baseline term is a convex combination of IC (P ; A) and IC (P ; B), the
quantity EmerC (P ; A, B) measures a relative gain over what would be expected if the composite
carried forward only a weighted mixture of the parts’ pattern intensities. In particular, if IC (P ; ·)
is normalized (for example, IC (P ; X) ∈ [0, 1] for all X ∈ EC ), then EmerC (P ; A, B) inherits
corresponding interpretability as a bounded, nonnegative degree of emergence. The definition itself
does not require a particular normalization, but it does require that IC (P ; X) be comparable across
X ∈ {A, B, A ∗C B} within the same context C.

Proposition 8 (Basic properties of emergent intensity). Fix C and assume A ∗C B is defined.
Then for every P ∈ PC :

  1. EmerC (P ; A, B) ≥ 0.

  2. If IC (P ; X) ≥ 0 for all X ∈ {A, B, A ∗C B}, then

                                     EmerC (P ; A, B) ≤ IC (P ; A ∗C B).

  3. EmerC (P ; A, B) = 0 whenever IC (P ; A ∗C B) ≤ wC (A) IC (P ; A) + wC (B) IC (P ; B).

Proof. (1) holds by definition since EmerC is the maximum of 0 and a real number. For (2), the
baseline term wC (A) IC (P ; A) + wC (B) IC (P ; B) is nonnegative under the stated assumption, so

                 SurC (P ; A, B) = IC (P ; A ∗C B) − (nonnegative) ≤ IC (P ; A ∗C B),

and clamping cannot increase the quantity beyond IC (P ; A ∗C B). Statement (3) is immediate from
the definition of SurC and the clamping in EmerC .



                                                  188
Proposition 9 (Symmetry of emergence under commutative combination). Fix C and assume ∗C
is commutative and A ∗C B is defined. Then for every P ∈ PC ,

                                   EmerC (P ; A, B) = EmerC (P ; B, A).

Proof. If ∗C is commutative, then A ∗C B = B ∗C A, hence IC (P ; A ∗C B) = IC (P ; B ∗C A). The
weights in Definition 102 satisfy wC (A) and wC (B) swap under exchanging A and B, so the baseline
term swaps accordingly. Therefore the surplus and its clamped version agree.

Remark 414. Emergence is the formal bridge from “patterns in parts” to “integration”. A high
density of high-intensity emergent patterns spanning a composite corresponds to the Hyperseed in-
tuition of a system whose organization is not reducible to its components. The weighting by sbase
                                                                                             C (·)
makes this bridge sensitive to the relative “amount” of each component in the context: in many
applications sbase
               C   can be chosen to track size, mass, duration, or any other baseline contribution
that would make a simple additive expectation reasonable before accounting for interactions.

Definition 104 (Collective-property-set). Fix C. Given an entity A ∈ EC and a reference class
B ⊆ EC of “other entities” relevant to A, define the collective-property-set of A relative to B as

                               Propcoll
                                   C (A)(P ) := sup EmerC (P ; A, B).
                                                   B∈B

Remark 415. Definition 104 turns emergence into a property assignment for A by asking: across
all relevant interaction partners B ∈ B, how strongly can A support the emergence of pattern P ?
The use of sup (rather than max) allows B to be infinite or to admit limiting sequences of partners
for which the emergent intensity approaches, but does not necessarily attain, its least upper bound.
When B is finite (or compact under suitable regularity assumptions on EmerC ), the supremum can
often be replaced by a maximum.

Proposition 10 (Monotonicity in the reference class). Fix C and A ∈ EC . If B1 ⊆ B2 ⊆ EC , then
for all P ∈ PC ,
                         Propcoll                    coll
                              C (A; B1 )(P ) ≤ PropC (A; B2 )(P ),

where Propcoll
          C (A; B)(P ) denotes the right-hand side of Definition 104 with the chosen reference
class B.

Proof. If B1 ⊆ B2 , then the set of values {EmerC (P ; A, B) : B ∈ B1 } is a subset of {EmerC (P ; A, B) :
B ∈ B2 }, hence its supremum cannot exceed the supremum over the larger set.

9.6   Blends
Hyperseed’s blend concept is property-theoretic: C is a blend of A and B when a significant
fraction of C’s properties are also properties of A or B. Here “properties” are understood in
the same weighted sense used throughout the property semantics: PropC (X)(P ) assigns (possibly
graded) salience, strength, or evidential mass to the claim that X has property P in context C, so
overlap can be partial rather than all-or-nothing.

Definition 105 (Blend score and blend predicate). Fix C and choose a threshold θ ∈ (0, 1]. Define
the property overlap mass of C with (A, B) as
                          X       n                                                 o
        ovC (C; A, B) :=      min PropC (C)(P ), max PropC (A)(P ), PropC (B)(P ) .
                           P ∈PC


                                                   189
Define the blend score
                                    (             
                                     ovC (C; A, B) kPropC (C)k1 ,     kPropC (C)k1 > 0,
           blendscoreC (C; A, B) :=
                                     0,                               kPropC (C)k1 = 0.

We say C is a blend of A and B (in context C) if blendscoreC (C; A, B) ≥ θ.
    The use of max(PropC (A)(P ), PropC (B)(P )) treats the sources A and B as an “either-parent”
supplier of property mass for P , while the outer min{·, ·} enforces that only as much of C’s mass on
P can be credited as is supported by at least one parent. Thus ovC is a fuzzy-set analogue of |C ∩
(A ∪ B)| when properties are crisp indicators, and blendscoreC becomes a normalized coverage ratio
for how much of C can be explained as inherited from A or B at the property level. In particular,
whenever kPropC (C)k1 > 0 one has 0 ≤ blendscoreC (C; A, B) ≤ 1, with blendscoreC (C; A, B) = 1
precisely when, for every P ∈ PC , PropC (C)(P ) ≤ max(PropC (A)(P ), PropC (B)(P )).
    Because the normalization uses kPropC (C)k1 , the score measures the fraction of C’s own as-
serted property mass that is supported by A or B; properties that are salient for A or B but not
salient for C do not inflate the score. This keeps the predicate focused on explaining C rather than
on measuring generic similarity between A and B. The special case kPropC (C)k1 = 0 corresponds
to a context where C has no active property mass (e.g. missing data, a fully uncommitted repre-
sentation, or an explicitly “null” property profile), in which case the conservative convention sets
the score to 0.
Remark 416. This definition is intentionally parametric: the threshold θ and the mass functional
can be chosen based on application. In cognitive modeling, blends are typically context-sensitive;
the present definition makes that explicit. A higher θ demands that most of what is asserted about
C be attributable to at least one parent, whereas a lower θ allows C to introduce more novel or
emergent properties not present in A or B. Likewise, replacing max by another pooling operator
(e.g. a t-conorm, a softmax, or an additive rule with a cap) changes whether joint support from
both parents can strengthen the accounting for a property.
    For intuition, consider the crisp/unweighted limit where PropC (X)(P ) ∈ {0, 1} and kPropC (C)k1 =
|{P : PropC (C)(P ) = 1}|. Then ovC (C; A, B) counts the number of properties that C has and
that at least one of A or B also has, and blendscoreC (C; A, B) is the fraction of C’s properties
covered by A ∪ B. In the graded case, the same picture holds but with fractional contributions: if
C partially satisfies P to degree 0.6 while the stronger parent support is 0.4, then only 0.4 counts
as overlap and the remaining 0.2 of C’s mass on P is treated as not inherited from either parent.

9.6.1   Categorical blend construction (pushout intuition)
A more structural notion of blend is useful when entities are themselves compositional objects (e.g.
graphs, terms, enriched presheaves). In that case, a blend is naturally modeled by a colimit that
glues two objects along a shared substructure, with a weakness/effort bias to prefer minimal glue.
This captures the common cognitive intuition that blending reuses a matched subpattern and then
merges the remaining structure around it, rather than arbitrarily combining the entirety of A and
B.
Definition 106 (Blend as colimit with weak-glue preference (sketch)). Fix a category (or enriched
category) C of entity-structures appropriate to the domain. Given A, B ∈ Ob(C), a blend diagram
is a span
                                          iA            iB
                                       S −→   A,     S −→  B

                                                190
where S is an extracted “shared subpattern.” A categorical blend is a choice of pushout (or more
generally colimit)
                             i     i
                          A ←A− S −→
                                   B
                                     B             A → Blend(A, B; S) ← B,
together with a ranking functional (effort/weakness) that prefers spans S yielding lower glue over-
head.

    Operationally, S represents the alignment hypothesis: it specifies which parts of A and B are
to be treated as “the same” for the purpose of blending, and the pushout performs the minimal
identification consistent with that hypothesis. The effort/weakness preference then plays a role
analogous to regularization: among many possible spans S (and many possible ways to extract
them from data), one favors those that explain the perceived commonality while introducing as few
identifications, coercions, or ad hoc repairs as possible. In concrete categories (e.g. graphs), the
glue overhead can be understood as the size or complexity of the interface S relative to A and B,
the number of forced identifications, or the amount of additional structure required to make the
span commute in the chosen modeling formalism.

Remark 417. In practice, one rarely needs literal pushouts; approximate colimits in a quantale-
enriched setting often match cognition better (multiple partial shared subpatterns, conflicting iden-
tifications, etc.). Paraconsistency enters here in a controlled way: one can glue while retain-
ing evidence against some identifications. From the property-theoretic perspective, such “approx-
imate gluing” corresponds to allowing the blend to inherit some properties strongly while keeping
other candidate inheritances tentative or contested, which then manifests as intermediate masses
in PropC (Blend(·)) rather than hard yes/no attributions.

9.7   Lifting from instances to groups
Hyperseed notes that once a relation is defined for instances, there are multiple sensible ways to lift
it to groupings of instances. We formalize three common lifts (average-like, ∀∃-like, and ∃∀-like) in
a form that generalizes well.

Definition 107 (Three lifts of an instance relation). Let C(·, ·) : X × Y → [0, 1] be any graded
instance-level relation. For finite nonempty A ⊆ X and B ⊆ Y , define:
                                                    1 XX
                                 Cavg (A, B) :=          C(a, b),
                                                  |A||B|
                                                          a∈A b∈B
                                 C∀∃ (A, B) := min max C(a, b),
                                                  a∈A   b∈B
                                 C∃∀ (A, B) := max min C(a, b).
                                                  b∈B    a∈A

Remark 418. These correspond (respectively) to “on average”, “for most a there exists some
b”, and “there exists some b that works for most a”, in a graded sense. The same pattern works
in quantale-valued settings by replacing (min, max) with meet/join and the average with a chosen
aggregation functional.

Remark 419. The nonemptiness of A, B ensures each lift is well-defined without additional con-
ventions. In applications where empty groups may arise (e.g., sparse clustering outputs), one can
extend the definitions by selecting neutral elements (e.g., 1 for “vacuously true” lifts, 0 for “no
evidence”) or by explicitly carrying an “undefined” value; the present formalization keeps the core
algebra clean.

                                                   191
Remark 420. When C is crisp, i.e. C(a, b) ∈ {0, 1}, the second and third lifts reduce to familiar
quantifier patterns:

C∀∃ (A, B) = 1 ⇐⇒ ∀a ∈ A ∃b ∈ B : C(a, b) = 1,         C∃∀ (A, B) = 1 ⇐⇒ ∃b ∈ B ∀a ∈ A : C(a, b) = 1.

Thus, in the Boolean case, C∀∃ behaves like an “every a can be matched” score, while C∃∀ behaves
like a “single prototype b covers all a” score.

Remark 421. Basic bounds and order-theoretic behavior are immediate from the definitions. Writ-
ing
             Cmin (A, B) := min C(a, b),        Cmax (A, B) := max C(a, b),
                               a∈A, b∈B                            a∈A, b∈B

one always has Cmin (A, B) ≤ C∀∃ (A, B) ≤ Cmax (A, B) and Cmin (A, B) ≤ C∃∀ (A, B) ≤ Cmax (A, B),
and the minimax inequality gives

                                      C∃∀ (A, B) ≤ C∀∃ (A, B).

In particular, C∃∀ is the more “demanding” lift: it asks for one element of B that uniformly scores
well against all of A, whereas C∀∃ allows the best witness in B to depend on a.

Remark 422. If C is interpreted as a similarity or compatibility, then Cavg measures overall
affinity between two clouds, C∀∃ measures whether each point in A is well-covered by some point
in B (a directed “coverage” score), and C∃∀ measures whether B contains a single representative
that fits all of A (a directed “prototype” score). These readings often align with empirical choices
in clustering, retrieval, and exemplar-based modeling.

    This is the generic mechanism behind lifting reference, association, and even emergence-like
relations from episodes to categories.

9.8   Combinatorial-categorical patterns
Hyperseed introduces “combinatorial-categorical patterns” as patterns that become visible only
after running a category-theoretic substitution/relabeling process. We formalize this as: apply
a rule system that assigns category labels to instances, producing a derived structure in which
ordinary patterns can be mined.

Definition 108 (Category domain and membership state). Fix a finite set of categories (types)
W . A membership state on a set of instances S is a map

                                           m : S → 2W .

Remark 423. Equivalently, a membership state can be seen as a binary relation Rm ⊆ S × W via
(s, w) ∈ Rm ⇔ w ∈ m(s), or as a |S| × |W | incidence matrix. This viewpoint makes the subsequent
closure operation look like a monotone update of a relation by rules.

Definition 109 (Combinatorial-categorical theory). Fix a set of instances S and a category domain
W . A combinatorial-categorical theory T is a finite set of rules of the form

                                (x ∈ A) ∧ (y ∈ B) =⇒ (z ∈ C),

where x, y, z ∈ S and A, B, C ∈ W .


                                                192
Remark 424. Syntactically, these are Horn-style implication rules over the atomic predicates “s ∈
w” (read: the instance s has category label w). The restriction to conjunctions in the antecedent
ensures that the associated operator on membership states is monotone under set inclusion, which
is what makes least-fixed-point semantics natural and robust.
Definition 110 (Substitution output / closure). Given an initial membership state m0 : S → 2W
and a theory T , define the closure mT as the least fixed point (under set inclusion) obtained by
repeatedly applying the rules of T : start from m0 and whenever a rule’s antecedent holds under the
current m, add C to m(z). Let
                                       sub(T, S, m0 ) := (S, mT )
denote the resulting labeled structure.
Remark 425. Because S and W are finite and rules only add labels, the iterative forward-chaining
process must terminate after at most |S|·|W | successful additions, independent of rule order. More-
over, the least-fixed-point characterization implies confluence: any fair rule-application schedule
yields the same mT , so sub(T, S, m0 ) is well-defined without committing to an operational order.
Remark 426. It is often useful to name the associated closure operator explicitly: define FT on
membership states by adding, for each rule (x ∈ A) ∧ (y ∈ B) ⇒ (z ∈ C), the label C to z whenever
A ∈ m(x) and B ∈ m(y). Then mT is the least fixed point of FT above m0 (i.e. the least m ⊇ m0
with FT (m) = m). This makes clear that sub is monotone in m0 and in T (adding initial labels or
rules can only add, never remove, derived labels).
Definition 111 (Combinatorial-categorical pattern). Fix a context C and assume a pattern mining
scheme has been defined on labeled structures. A pattern candidate P is a combinatorial-categorical
pattern in S relative to T and m0 if P is a (standard) pattern in the derived structure sub(T, S, m0 ).
Remark 427. Concretely, one can take the “labeled structure” to be the multiset {mT (s) : s ∈
S} and apply any off-the-shelf pattern formalism (frequent itemsets, association rules, MDL-based
codes, subgraph motifs after encoding mT as a bipartite graph, etc.). The key is that patterns are
not searched for in the raw instance space, but in the feature space induced by closure under T .
Remark 428. This construction cleanly separates two kinds of inductive bias. The theory T de-
termines which composite categories are even expressible (a kind of “feature generation”), while the
mining scheme determines which regularities count as salient (frequency, compressibility, predictive
utility, etc.). In this sense, “combinatorial-categorical patterns” are ordinary patterns, but in a
theory-generated representation.
Remark 429. This is a clean formal docking port to “pattern theory” constructions: T gener-
ates a derived feature space (categories as features), after which one mines compressive structures
(patterns) over that space.

9.9   Combination systems, interpreters, and combinational dynamical causal
      models
We now formalize the computational and dynamical notions Hyperseed attaches to combinations.
The intent of this subsection is to keep the algebraic structure minimal (a set equipped with a
not-necessarily-total binary operation), while still being expressive enough to cover common cases
such as term concatenation, multiset union, function composition, event interaction, and process
coupling. In particular, the partiality of the operator is used to encode compatibility constraints:
some pairs of objects simply do not combine (or are not allowed to combine) under the rules of a
given model.

                                                 193
Definition 112 (Combination system). A combination system is a pair (S, ∗) where S is a set
and ∗ : S × S * S is a partial binary operation.
    The use of a partial operation ∗ : S × S * S means that there may exist x, y ∈ S for which x ∗ y
is undefined. This can be read either operationally (the system refuses to execute that composition)
or semantically (there is no meaningful composite object in the chosen ontology). No associativity,
commutativity, identity, or inverses are assumed unless explicitly added later; this allows the same
template to describe both highly structured algebraic settings and ad hoc gluing rules that arise in
modeling and representation.
Definition 113 (Interpreted combination system). An interpreted combination system is a triple
(S, ∗, Dec) where (S, ∗) is a combination system, L is a syntactic language of expressions, and Dec :
L → S is an interpreter such that whenever `1 · `2 denotes a syntactic composition corresponding
to ∗, one has
                                   Dec(`1 · `2 ) = Dec(`1 ) ∗ Dec(`2 )
whenever the right-hand side is defined.
   Here L may be thought of as a grammar-generated set of expressions, while · is the syntactic
constructor for putting two expressions together in whatever way is appropriate (concatenation,
application, pairing, sequencing, etc.). The condition

                                   Dec(`1 · `2 ) = Dec(`1 ) ∗ Dec(`2 )

is a compositionality requirement: decoding a composite expression agrees with composing the
decoded parts, whenever that semantic composition exists. Equivalently, Dec behaves like a ho-
momorphism from the syntactic combination (where defined as a constructor) into the semantic
combination system (where defined as a partial operation), and undefinedness on the semantic side
signals that the syntactic composite has no coherent meaning under the intended interpretation.
Remark 430. This is the formal core of “a computational model is an interpreted combination
system”: syntax plus an evaluation map into semantic objects equipped with composition.
    One can also view (S, ∗) as the model’s semantic workspace, and Dec as the mechanism that
embeds symbolic expressions into that workspace. The definition deliberately does not constrain L
to be closed under · for all pairs: even at the syntactic level there may be formation rules, and at
the semantic level there may be compatibility conditions. When L is closed under · but ∗ is partial,
then some well-formed syntactic composites may decode to undefined semantic composites, which
captures the common situation where an expression is grammatical but ill-typed or semantically
incoherent.
    Next, a combination-preserving representational mapping allows a system to talk about a dy-
namical domain using a symbolic combination system. The central idea is that the same com-
binational structure appears on two sides: in the world-domain of processes/events and in the
representational-domain of symbols. A map that preserves combination is the minimal require-
ment for symbols to track how interactions in the domain assemble into larger composite processes.
Definition 114 (Combination-preserving representational mapping). Let (D, ∗∗) be a domain of
processes or events with a (possibly partial) interaction/combination operator ∗∗. Let (S, ∗) be a
combination system of symbols. A map f : D → S is combination-preserving if

                                        f (a ∗ ∗b) = f (a) ∗ f (b)

whenever a ∗ ∗b and f (a) ∗ f (b) are defined.

                                                   194
    This condition can be read as a consistency constraint between what happens in the dynamical
domain and how we name it in the symbol system. Because both ∗∗ and ∗ may be partial, the
definition only enforces equality on the intersection of their defined regions: if an interaction a ∗ ∗b
exists and the corresponding symbolic combination f (a) ∗ f (b) is also meaningful, then the symbol
for the interaction must agree with the combination of the symbols. In modeling terms, this is
precisely the requirement that representation respect the compositional granularity of the domain.
When f is not injective, it intentionally collapses distinct domain elements into the same symbol; the
later validity condition for causal attribution is designed to ensure that causal claims are invariant
under such representational collapse.
    Finally, Hyperseed’s “combinational dynamical causal model” is a graded causal attribution for
triples. The triple (a, b, c) is intended to capture a two-input interaction resulting in (or contributing
to) an outcome. The range [0, 1] supports soft or probabilistic attributions, and it is compatible
with both deterministic and statistical readings depending on how Γ is instantiated.

Definition 115 (Combinational dynamical causal model). Let (D, ∗∗) be a dynamical process
domain. A combinational dynamical causal model is a function

                                              Γ : D × D × D → [0, 1]

where Γ(a, b, c) is interpreted as the degree to which “interaction of a and b caused c.”
    Given a combination-preserving representational mapping f : D → S into a symbol system
(S, ∗), we say Γ is valid relative to f if

                 f (a) = f (a0 ), f (b) = f (b0 ), f (c) = f (c0 )   =⇒   Γ(a, b, c) = Γ(a0 , b0 , c0 )

for all a, b, c, a0 , b0 , c0 ∈ D.

    The valid relative to f condition can be understood as invariance under the equivalence relation
induced by the representation. If we define x ∼f y to mean f (x) = f (y), then validity requires
Γ to be constant on ∼f -equivalence classes in each argument simultaneously. Equivalently, Γ
factors through the quotient induced by f : there exists a well-defined function Γ    e on the level of
symbols/classes such that Γ(a, b, c) depends only on (f (a), f (b), f (c)). This makes explicit that the
causal scores are not absolute facts about D alone, but are constrained to be compatible with the
descriptive alphabet provided by f .

Remark 431. Validity means the causal model “respects the symbols”: it does not distinguish pro-
cesses that the representation identifies. This is the causal analogue of observer-relativity: causality
is computed relative to a representational alphabet (and thus relative to an ontology).

    In particular, if f merges multiple micro-level processes into a single macro-symbol (e.g., many
distinct trajectories mapped to one coarse label), then validity forces Γ to assign the same causal
degree to any two triples that are indistinguishable at that macro level. This ensures that causal
attributions are stable under re-description: once an ontology has decided what counts as the
same process, the causal model cannot re-introduce distinctions that the ontology has explicitly
discarded. Conversely, if a proposed Γ violates validity, then either the representation f is too
coarse for the causal distinctions being made, or the causal model is implicitly using additional
latent features not present in (S, ∗).




                                                          195
9.10    Specific entities as temporally coherent patterns
Hyperseed treats “specific entities” (ordinary objects, persons, institutions) as complex derived
constructions rather than primitives. The key observation is that specific-entity identity behaves
like a pattern with a temporal algebra. In particular, what is being modeled is not an additional
metaphysical glue beyond the entities already available in EC , but a rule-governed way of tracking
a coherent thread through time-slices: the stream provides the candidate trajectory, while the
coherence rule R fixes which kinds of variation count as “the same” within the intended resolution
of the context C. This makes explicit that persistence is always relative to (i) the granularity of
proto-time, (ii) the measurement/description vocabulary encoded by the properties used in assocC ,
and (iii) the tolerance encoded by R.

Definition 116 (Occurrence stream). Fix a context C with proto-time ordering (Section 7). An
occurrence stream is a family {xt }t∈T of entities xt ∈ EC indexed by times (or time-slices) t in a
partially ordered set (T, ≤).

    The choice of (T, ≤) as a partially ordered set, rather than assuming a total order, is intentional:
it allows proto-time to represent branching, concurrency, or causal precedence structures (e.g.
distributed records, parallel sub-processes, or partially ordered observations), without forcing a
single linear history. In this setting, an occurrence stream may be partial : for some t ∈ T there
need not be an xt at all, reflecting missing observations, gaps in memory, or times at which the
entity is simply not represented in EC . The phrase “if . . . both occur” in the coherence conditions
is meant to accommodate such partiality.

Definition 117 (Specific entity (pattern-theoretic criterion)). A specific entity in context C is
specified by an occurrence stream {xt }t∈T together with a coherence rule R such that:

1. (Same-time identity) If t = t0 and both xt and xt0 occur, then they are identified: xt = xt0 .

2. (Near-time similarity) If t and t0 are close in proto-time, then the association assocC (xt , xt0 ) is
   high (Definition 101), or equivalently the property-sets overlap strongly.

The strength of “being the same specific entity” is graded by how well the stream satisfies these
rules.

    Condition (1) should be read as a determinacy constraint internal to the representation: within
a fixed time-slice, the stream does not bifurcate into multiple candidates that are simultaneously
treated as distinct occurrences of the same tracked entity. This is a minimal consistency requirement
for a tracking convention, and it separates questions of “co-reference at a time” from questions of
persistence across time. Condition (2) provides the persistence signal: if proto-time steps are
small, then large discontinuities in properties are penalized (low assocC ), while small variations are
tolerated. The coherence rule R can be taken to parameterize what counts as “close” in proto-
time (e.g. adjacent steps, bounded distance in the order, or neighborhood relations induced by the
context) and what counts as “high” association (e.g. a threshold, a soft score, or a weighted overlap
depending on which properties are privileged in C). Thus, even when the same underlying object is
being discussed informally, different contexts C (legal, biological, physical, social) can yield different
specific-entity criteria because they select different property vocabularies and tolerances.
    The graded reading in the final sentence is crucial: rather than producing a binary verdict, the
framework supports degrees of identity driven by the quality of temporal coherence. For example,
a heavily repaired artifact (a “Ship of Theseus” trajectory) can yield a stream where local simi-
larity remains high even though long-range similarity between distant times is low; the framework

                                                   196
then naturally supports the common phenomenon that identity feels secure locally but disputable
globally. Likewise, institutional entities (companies, governments) are often stable under large
personnel changes, so R in such contexts would weight organizational roles, charters, or registries
more than physical continuity; by contrast, for biological organisms R would privilege different
properties (e.g. bodily continuity, metabolic functioning).

Remark 432. This captures the intended Hyperseed idea: “specific entity” is a pattern (a tempo-
rally stable bundle of properties) with conventional default rules, but those rules can be violated in
exotic scenarios (yielding graded/ambiguous identity rather than forcing contradiction).

    A further consequence is that identity questions can be reframed as optimization or inference
problems: given a set of candidate occurrences in EC at various times, one seeks streams that maxi-
mize coherence under R (high near-time association, minimal violations of same-time determinacy),
possibly subject to additional constraints coming from the context. This aligns the informal prac-
tice of “tracking an object/person” with a precise, context-sensitive criterion: the best-supported
stream is the one that forms the most temporally coherent pattern. In cases with competing high-
coherence streams (e.g. fission, duplication, imperfect records), the model predicts plural partially
supported identifications rather than a forced all-or-nothing answer.

9.11    Worked micro-example (optional but useful)
Example 9 (A minimal pattern and emergent pattern). Let C be a context with a combination
operator ∗ and baseline costs sbase                        base
                               C . Suppose x = y ∗ z and sC (x) = 10, sC (y) = 3, sC (z) = 4, and
glue overhead t = 1. Then hC (P ) = 3 + 4 + 1 = 8 so
                                                          
                                                    10 − 8
                                IC (P ; x) = max 0,          = 0.2.
                                                      10

Thus (y, z, t) is a pattern in x of intensity 0.2. Here hC (P ) is the hypothesized cost of “explaining”
or “reconstructing” x via the structured description provided by the pattern P (namely, reuse y and
z and pay the additional glue overhead t to combine them in the appropriate way). The baseline
sbase
 C (x) is the cost of representing x without exploiting any special structure, so the numerator 10−8
measures the absolute savings attributable to recognizing P inside x. Dividing by 10 normalizes this
savings, making the resulting intensity scale-free relative to the baseline size of x in context C. The
outer max{0, ·} enforces that an alleged pattern cannot have negative intensity: if the hypothesized
description is no cheaper than baseline (i.e., if hC (P ) ≥ sbase C (x)), then the correct conclusion
is simply that P provides no compression advantage in x (intensity 0) rather than treating it as
“anti-pattern” evidence.
    Now suppose also that A∗C B exists and a pattern P has intensities IC (P ; A) = 0.1, IC (P ; B) =
0.1, but IC (P ; A ∗C B) = 0.5. If sbase         base
                                     C (A) = sC (B) then wC (A) = wC (B) = 1/2 and

                          SurC (P ; A, B) = 0.5 − (0.5 · 0.1 + 0.5 · 0.1) = 0.4,

so P is emergent in A ∗C B with emergent intensity 0.4. The point of this second computation
is that emergence is assessed relative to what one would “expect” from the parts when combined,
where that expectation is a weighted average of part-wise intensities. In this symmetric case, equal
baseline sizes lead to equal weights, so the predicted intensity absent interaction effects is just
the simple average of 0.1 and 0.1, namely 0.1. The surplus SurC (P ; A, B) = 0.4 quantifies the
genuinely interaction-dependent gain: the pattern becomes much more detectable (or much more
cost-saving) in the composite than one would anticipate from its weak presence in each component

                                                   197
alone. Equivalently, this example isolates a situation where the combined object A ∗C B supports a
strong structural shortcut described by P that is not available, or not salient enough to be valuable,
when considering A and B in isolation.

Remark 433. This example is numerically trivial, but it is exactly the formal shape of the Hy-
perseed definitions. In later sections, the toy resonance model (Section 5) and the habit dynamics
(Section 12) will turn these static notions into time-evolving structures. One should read the num-
bers here as placeholders for whatever cost model is supplied by the context C: for instance, costs
may encode description length, energy, inference effort, or any other resource that the agent tracks.
Likewise, the “glue overhead” t is the minimal place where contextual idiosyncrasy can enter: even
if y and z are individually cheap, composing them may require additional bookkeeping, alignment,
interface matching, or constraints to be satisfied, all of which are abstracted into t. The emer-
gent calculation is also intentionally schematic: it highlights that emergence is not merely “having
high intensity,” but rather “having higher intensity than predicted from the parts under the chosen
weighting scheme.” Consequently, changing sbase C    (and hence the weights wC ) can change the quan-
titative emergent intensity, reflecting the fact that what counts as “surprising” depends on how the
context measures and compares the relative contribution of the components.


10     Information, uncertainty, and ineffability
10.1    Motivation: information as observer-indexed bookkeeping
Hyperseed treats distinction as primitive and observer-relative (Hyperseed-Concept 98). As soon as
we take this stance seriously, “information” and “uncertainty” can no longer be treated as absolute
scalars attached to a world-state; they must be indexed by a context (or observer) (Hyperseed-
Concept ??, Hyperseed-Concept 195; see also [1]). This section provides a small formal layer that
lets us: (i) speak about probabilistic belief (Hyperseed-Concept 139); (ii) relate classical Shannon
information to distinction-based measures (logical entropy and graphtropy) (Hyperseed-Concept
105, Hyperseed-Concept ??; [17]); (iii) make “ineffability” precise as a representational limitation
(Hyperseed-Concept ??); and (iv) clarify what “potential infinity” and “infinitesimals” can mean
in a resource-sensitive ontology (Hyperseed-Concept ??, Hyperseed-Concept ??).
     Throughout, let X denote a (typically finite) set of “world items” (entities, events, situations)
and let O denote an observer/context. The basic data carried by O are: (a) a family of distinctions
it can make about X; and (b) a belief state over those distinctions.
     In this framing, X should be read as a domain of discourse relative to a modeling task: it
might be a set of perceptual episodes, candidate hypotheses, experimental outcomes, or coarse-
grained situations that are treated “as if” they were atomic for current purposes. The parenthetical
“typically finite” is not merely a convenience: in Hyperseed the finiteness (or boundedness) of X
often stands in for resource limits on attention, memory, time, and representational capacity, while
still allowing limits to be taken when discussing “potential” infinities.
     Item (a) can be made concrete in multiple equivalent ways, depending on which mathematical
lens is most appropriate. For example, a distinction-making capacity can be encoded as a partition
of X into equivalence classes (items that O cannot tell apart), or as a set of binary questions of
the form “does x have property P ?”, or (more generally) as a σ-algebra of subsets of X specifying
which events are measurable for O. Each representation emphasizes a different intuition: partitions
emphasize indistinguishability, question-sets emphasize interrogability, and σ-algebras emphasize
closure properties needed for consistent probability assignments. In particular, once distinctions
are taken as primary, it becomes natural to treat two items x, y ∈ X as observationally equivalent


                                                 198
for O when no available distinction separates them; the “world-state” relative to O is then more
faithfully represented by the cell of a partition (or, dually, by the truth-values of all questions in
the algebra) than by a bare element of X.
    Item (b) is then the observer’s weighting over the distinguishable alternatives. Operationally,
one may think of O as assigning probabilities to the events it can express (e.g., to the cells of a par-
tition, or to measurable subsets), which is why a probability measure naturally appears alongside
the distinction structure. This is intentionally broad: it includes Bayesian degrees of belief, empir-
ical frequencies within a data stream, and hybrid or imprecise credal assignments, so long as they
respect the representational constraints imposed by (a). The key point is that probabilities are not
assigned to an unstructured “reality” but to recognizable possibilities—hence even a numerically
identical probability vector may correspond to different informational situations if the underlying
distinctions differ.

Remark 434. The philosophical point is modest but consequential: an “information measure” is
never purely a property of the world; it is a property of a world as carved by some scheme of
recognition, and as weighted by some state of belief. Russell would say that the definitions below are
not metaphysical proclamations about Being, but carefully chosen bookkeeping devices; Peirce would
add that this bookkeeping is itself a habit of interpretation, hence belongs as much to the interpreter
as to the interpreted. Formally, the bookkeeping will appear as (i) a σ-algebra encoding what can
be asked, and (ii) a probability measure encoding how strongly the observer leans toward different
answers.

    A useful way to read the remark is as a constraint on what it could even mean to compare
information across observers. If two contexts O1 , O2 carve X differently, then an expression like
“O1 has more information than O2 ” is not automatically well-defined until one specifies a transla-
tion between their distinction structures (e.g., refinement/coarsening maps between partitions, or
homomorphisms between σ-algebras). When such a translation exists, many familiar monotonicity
intuitions reappear (finer distinctions can support lower uncertainty, higher potential information
gain), but these become theorems about relationships between algebras/partitions rather than
metaphysical claims about a single observer-independent quantity.
    This observer-indexed bookkeeping also motivates why distinction-based measures (logical en-
tropy, graphtropy) are not merely alternative “formulas” for the same idea. Shannon entropy
presumes a fixed alphabet of outcomes and measures expected code length relative to that al-
phabet; logical entropy directly counts (in expectation) how often two draws fall into different
distinguishability classes, making the role of distinctions explicit. Graphtropy generalizes the same
intuition from partitions to graphs of indistinguishability or comparability relations on X, which
is often closer to how real cognitive and computational systems represent “can/cannot tell apart”
in a graded or relational manner. Thus, the formal layer introduced here is meant to keep the
distinction structure visible, so that later statements about uncertainty reduction, learning, and
ineffability remain tethered to what the observer can actually represent.
    Finally, the promised link to ineffability can be previewed already at this introductory stage:
something is “ineffable for O” not because it is mystical, but because it cannot be stably encoded
within O’s distinction system and the associated algebra of questions. On this view, ineffability
is an internal, structural limitation: there may be facts about X that exist in some richer meta-
description, yet are not measurable (or not finitely describable) in the σ-algebra available to O, or
cannot be assigned coherent probabilities without extending O’s representational resources. This
is also where resource-sensitive readings of infinity and infinitesimals enter: what looks like an
“infinitary” refinement may be treated as a limit of finite refinements that an observer can only ever


                                                  199
approximate, and “infinitesimal” differences may correspond to distinctions that are in principle
definable but in practice unresolvable at the observer’s current granularity.

10.2    Observer-indexed probability spaces
Definition 118 (Observable events). Fix an observer/context O. An event observable to O is a
predicate on X whose truth value is determined at the resolution of O. Formally, we model the
collection of O-observable events as a sigma-algebra ΣO ⊆ 2X . A probability model for O is a
probability measure
                                        PO : ΣO → [0, 1].
The triple (X, ΣO , PO ) is the observer-indexed probability space.

Remark 435. Notation/conventions. Here 2X denotes the power set of X (all subsets of X);
ΣO ⊆ 2X is a σ-algebra, meaning it is closed under complements and countable unions (in the finite
case, this reduces to closure under complements and finite unions). The probability measure PO
assigns to each observable event A ∈ ΣO a number in [0, 1] with PO (X) = 1 and countable additivity
on disjoint unions. It is also standard that PO (∅) = 0 and that (by additivity) PO (Ac ) = 1 − PO (A)
whenever A ∈ ΣO ; these identities emphasize that PO is defined only on the observer’s event-
language ΣO rather than on arbitrary subsets of X. When X is large or continuous, the restriction
to ΣO is not only philosophical but technically necessary: many subsets of X are not measurably well-
behaved, and σ-algebras are precisely the minimal structure needed to make probability assignments
coherent.
    Intuition. ΣO is the mathematical shadow of the observer’s question-set: it lists precisely
which yes/no questions about X are meaningful at O’s resolution. If A ∈     / ΣO , it is not that A is
false; it is that A is not a well-formed observable event for O. Once the observer has a question-set,
PO encodes the observer’s uncertainty over answers. In this sense, an “observer” O can be read
broadly: a physical sensor suite, an agent with finite memory and categories, a modeling choice
about which variables are tracked, or even a scientific community that has stabilized a repertoire of
admissible experimental distinctions.
    Example. Let X be the set of microstates of a gas. A coarse observer might only measure
temperature and pressure, so ΣO is generated by macroscopic equivalence classes (microstates with
the same macro-observables). A finer observer might distinguish many more subsets, having a much
larger ΣO . This is the formal version of saying: different observers inhabit different informational
worlds even when they speak about the same underlying X. Equivalently, one can think of the coarse
observer as having access only to a map fO : X → YO of microstates into macrostates, so that ΣO
is the pullback of the power set (or Borel σ-algebra) on YO ; in that view, PO is the pushforward of
whatever uncertainty the observer implicitly has over X into the observer’s accessible variables.

Remark 436 (Coarse-graining as “loss of distinction”). If ΣO is generated by a partition πO of X,
then the observer does not represent individual elements of X but only the block in πO that contains
them. The move from 2X to ΣO is a formal encoding of “failure to make distinctions.” In particular,
any two microstates x, x0 ∈ X that lie in the same block of πO are observationally interchangeable
for O: no event in ΣO can separate them. This makes explicit that “coarse-graining” is not merely
a lossy summary of a distribution, but a restriction on the very predicates that can be formed and
evaluated.

Remark 437. A partition-induced σ-algebra is the simplest case, and it corresponds to crisp in-
distinction: O treats two items as the same iff they fall in the same block. Later we generalize


                                                 200
this to graded and even asymmetric indistinction (via indistinction graphs), which is closer to how
cognition behaves in practice (cf. the pattern-based picture in [5]). In the Hyperseed vocabulary this
is an instance of treating distinctions as primary structure (Hyperseed-Concept 98). It is useful
to note that “finer” and “coarser” observers can be compared directly at the level of σ-algebras:
if ΣO1 ⊆ ΣO2 , then O2 can express every question O1 can (and possibly more), so O2 is infor-
mationally at least as fine as O1 . This inclusion relation is a precise, order-theoretic version of
“one observer refines another,” and it will later support principled ways to relate models across
levels (e.g. restricting a finer model to a coarser question-set, or lifting a coarse belief to a family
of compatible fine beliefs).

Definition 119 (Paraconsistent evidence annotations). To connect to the paraconsistent core (Sec-
tion 3), we may annotate events with a p-bit evidence value
                                     +       −
                          EO (A) = (EO (A), EO (A)) ∈ [0, 1]2       (A ∈ ΣO ),
        +                                          −
where EO  (A) is degree of positive evidence and EO  (A) is degree of negative evidence. No consistency
                                             +         −
constraint is imposed: it is allowed that EO   (A) + EO  (A) > 1. In particular, EO is not assumed to
                                                      −               +
be a probability measure, nor is it assumed that EO (A) equals EO       (Ac ); the point is to retain two
channels of support that need not be reducible to a single additive calculus.

Remark 438. Intuition. Ordinary probability tries to compress all epistemic nuance into one
scalar PO (A). Paraconsistent annotation instead records two partially independent intensities: rea-
                                                +        −
sons for A and reasons against A. Allowing EO     (A)+EO   (A) > 1 is not a bug but a formal admission
that real epistemic agents can be pulled strongly in incompatible directions at once (e.g. contradic-
tory testimonies, model mismatch, sensor conflict). This connects directly to paraconsistent logics
such as Constructible Duality Logic [23] and to resonance-style dynamics studied in [24]. One can
       ±
read EO   operationally as aggregating heterogeneous sources that are not forced to “cancel” into a
net score; the annotation thereby separates amount of support from degree of resolution, and it
allows an agent to represent “I have strong reasons on both sides” without collapsing that state into
a near-1/2 probability. At a technical level, this is a way of preserving informational structure that
would otherwise be lost under a single-number summary.
    Examples. If EO (A) = (0.9, 0.1) the observer has strong support for A with little counter-
pressure. If EO (A) = (0.9, 0.9) the observer has a deep conflict: A is simultaneously strongly
supported and strongly opposed, reflecting a state closer to dissonance than ignorance. If EO (A) =
(0.1, 0.1), by contrast, the agent has little evidence either way; this can be interpreted as genuine
informational poverty rather than a balanced clash of considerations.
    Usefulness. This annotation is not meant to replace probability, but to complement it when the
observer’s representational regime allows mutually incompatible local inferences. Later, when habit
dynamics and resonance/dissonance are modeled as update rules on graded supports (Section 12),
the possibility of conflict becomes structurally central. In particular, keeping PO alongside EO allows
one to distinguish (i) the agent’s betting-odds or action-guiding summary from (ii) the internal
tension profile that may drive future reorganization of distinctions, attention, or model class.

Remark 439 (Two kinds of “uncertainty”). The pair (PO , EO ) supports two distinct phenomena:

• Ignorance: probabilities near 1/2 and/or low total evidence.

• Conflict: simultaneous strong positive and strong negative evidence.



                                                  201