# 4 Core sanity theorems

Definition 5 (Negation). Define the involution

                                       ¬(v + , v − ) := (v − , v + ).

Remark 52 (Intuition, example, and why involution matters). Negation swaps positive and neg-
ative evidence: what was counted as support is now counted as opposition and vice versa. For
example, ¬(1, 0) = (0, 1) and ¬(0.8, 0.3) = (0.3, 0.8). This is an involution: applying it twice
returns the original value, ¬(¬v) = v.
    This operation is useful because it cleanly separates the representation of evidence from any
particular choice of connectives. It also makes anti-resonance propagation (Definition 22) formally
simple: one can propagate “the contrary” without inventing a new evidence calculus each time.

Definition 6 (Evidence-style conjunction and disjunction). Define

      v ∧ w := min(v + , w+ ), max(v − , w− ) ,   v ∨ w := max(v + , w+ ), min(v − , w− ) .
                                                                                        


Remark 53 (Intuition via constraints and two quick examples). The connective v ∧ w behaves like
an “and” for positive evidence and like an “or” for negative evidence: to support A ∧ B you must
support both (hence min), but to oppose A ∧ B it suffices to oppose either (hence max). Dually,
v ∨ w takes the easiest support (max) but the hardest opposition (min).
    Example: if v = (0.9, 0.1) and w = (0.4, 0.8) then

                             v ∧ w = (0.4, 0.8),         v ∨ w = (0.9, 0.1).

So the conjunction inherits the weaker support and the stronger opposition; the disjunction inherits
the stronger support and the weaker opposition. This is useful because it respects the intuition that
a single strong refutation can undermine a conjunction, while a single strong support can sustain a
disjunction.

Remark 54 (Interpretation). Under these connectives, supporting A ∧ B requires supporting both
(hence min on positive evidence), while refuting A ∧ B requires refuting either (hence max on
negative evidence). Dually, supporting A ∨ B requires supporting either (max), while refuting A ∨ B
requires refuting both (min). This is one standard “evidence pair” paraconsistent semantics; other
monotone choices are possible.
    It may help to keep the intended reading explicit: a value v = (v + , v − ) records independent
degrees of positive and negative evidence, so v + and v − need not sum to 1 and may simultaneously
be large (a conflicted state), or simultaneously be small (an uninformed state). With that in mind,
the ∧/∨ clauses above are just the order-theoretically simplest way to implement “need both” versus
“need either” for support/refutation, using the lattice operations min and max on each evidence
coordinate.
    In particular, if A is strongly supported but also strongly opposed, and similarly for B, then
A ∧ B remains strongly supported only insofar as both supports remain high (hence the min), while
it becomes strongly opposed as soon as either conjunct attracts strong opposition (hence the max).
The dual intuition for ∨ is analogous: disjunction is easy to support (any disjunct suffices) but hard
to refute (both must be refuted). These asymmetries are exactly what lets the semantics tolerate
inconsistency without collapsing into triviality.

Definition 7 (Implication (one convenient choice)). Define implication by

                                        v → w := (¬v) ∨ w.


                                                    54
Remark 55 (What this implication expresses and why we do not overcommit to it). The definition
v → w := (¬v) ∨ w is the familiar material-implication pattern translated into the evidence-pair
setting: “if v then w” is treated as “either not-v or w.” For example, if v = (1, 0) (strongly
supported) and w = (0, 1) (strongly opposed), then v → w becomes maximally conflicted, reflecting
the idea that a supported antecedent with an opposed consequent is problematic.
    One should also read this connective operationally: increasing evidence against v (i.e. increasing
the negative coordinate of v, which becomes positive evidence for ¬v) makes v → w easier to support,
while increasing evidence for w also makes v → w easier to support, since it is a disjunction.
Conversely, to refute v → w one must refute both ¬v and w, meaning (intuitively) one must have
strong support for v together with strong opposition to w; this matches the classical idea that an
implication fails precisely when the antecedent holds but the consequent does not, while still allowing
the paraconsistent possibility that additional counterevidence coexists.
    We include implication mainly as a bridge to conventional logical reading. Much of the later
theory leans more on monotone aggregation and composition (quantale joins/products and enriched-
category inequalities) than on any particular internal logic. This restraint is intentional: Hyperseed
aims to model cognition where inference is often heuristic, resource-bounded, and context-sensitive,
so algebraic monotonicity often does more work than a single, universal implication connective
[19, 20].
    Accordingly, nothing in the sequel depends on material implication validating all familiar proof
principles (e.g. unrestricted modus ponens under inconsistency), and alternative paraconsistent
implications could be substituted if one wishes to enforce different inferential behavior. The point
of Definition 7 is thus representational convenience: it supplies a recognizable “if–then” connective
that interacts predictably with ¬ and ∨ in the evidence-pair algebra, without claiming to be the
unique or cognitively privileged notion of implication.

   For the toy model and much of the later ontology, we will rely more heavily on monotone
aggregation (quantale joins and monoidal products) than on any particular choice of implication;
the above is included mainly to provide a familiar logical vocabulary when needed.

3.3   Quantales as aggregation and composition domains
                                                                             W
Definition 8 (Commutative quantale). A commutative quantale is a tuple (V, ≤, , ⊗, e) such
that:
                                          W
1. (V, ≤) is a complete lattice with joins S for all S ⊆ V ;

2. (V, ⊗, e) is a commutative monoid;

3. ⊗ distributes over arbitrary joins:
                           _  _                       _       _
                       a⊗       bi = (a ⊗ bi ),           bi ⊗ a = (bi ⊗ a).
                              i         i                 i             i


Remark 56 (Basic consequences worth W    keeping in mind). Because (V,W ≤) is a complete lattice, it
in
V  particular has a bottom element  ⊥ :=   ∅ and  a top element  > :=   V , and it also has all meets
   S (as joins in the opposite order). The distributivity axiom implies that, for each fixed a ∈ V ,
the map (−) 7→ a ⊗ (−) preserves arbitrary joins; similarly (−) 7→ (−) ⊗ a preserves arbitrary joins.
In particular, ⊗ is monotone in each argument:

                      b ≤ c =⇒ a ⊗ b ≤ a ⊗ c,          b ≤ c =⇒ b ⊗ a ≤ c ⊗ a.

                                                  55
This monotonicity is the order-theoretic statement that “adding evidence cannot reduce a composed
influence.” It is the minimal property needed to make repeated update steps behave predictably when
we later iterate propagation operators.
    A useful special case of join-preservation is the interaction with ⊥:
                                       _  _
                          a⊗⊥=a⊗            ∅ =      ∅ = ⊥,      ⊥ ⊗ a = ⊥,

so ⊥ acts as an absorbing element for composition. Intuitively, “impossible/absent influence” re-
mains impossible/absent under chaining.

Remark 57 (Notation and intuition for quantales). The symbols are meant  W to be read in an order-
theoretic way. The relation ≤ is an information/strength ordering;           is the join (least upper
bound), i.e. the operation of aggregating many pieces of evidence into the weakest upper bound that
dominates them. The operation ⊗ is the monoidal product, interpreted as a form of sequential or
conjunctive composition. The element e is the unit for ⊗.
    A quantale
             W can be thought of as “logic with arithmetic”: it allows you to accumulate many
influences ( ) and also to chain influences (⊗) in a way that interacts well with accumulation
(distributivity). This is precisely what we need for Hyperseed’s graded and compositional notions of
distinction, weakness, and pattern propagation [3].
    The commutativity assumption is not strictly necessary in all quantale applications, but it
matches the intended reading here where the combination of two influences is not sensitive to their
left/right ordering at the level of scalar weights. Later, directionality will be represented in the
relational structure (source/target of a link) rather than in the scalar itself, so a commutative ⊗
keeps the scalar calculus simple while still supporting non-symmetric networks.

Remark 58 (Simple examples and why quantales are useful here). Example 1: The Boolean
quantale ({0, 1}, ≤, ∨, ∧, 1)Wyields ordinary relational composition and crisp distinctions. Example
2: The unit interval with = max and ⊗ = · yields fuzzy relational composition. Our later choice
V = [0, 1]2 is a paraconsistent generalization of this.
    To connect these examples to the way Hyperseed will use them: if one represents a pattern-
propagation relation as a V -valued adjacency matrix, then the “two-step influence” from x to z
through intermediate
            W          nodes y is computed by composing along y using ⊗ and then aggregating over
all y using . In the Boolean case this recovers existential path composition; in the fuzzy case it re-
covers the standard max-product or sup-product style composition. The quantale axioms are exactly
what ensures that this matrix-style multiplication is associative, so that multi-step propagation does
not depend on arbitrary parenthesization.
    Quantales serve Hyperseed as a disciplined replacement for informal phrases like “combine these
influences” or “propagate this pattern.” They guarantee that iterative updates behave monotonically
and that multi-step compositions can be reassociated without ambiguity (associativity of relational
composition ultimately rests on the distributivity axiom). This becomes essential once we discuss
resonance-driven propagation and habit reinforcement, where repeated composition is the rule rather
than the exception (Hyperseed-Concept 189; Hyperseed-Concept 188).
    The paraconsistent choice V = [0, 1]2 can be read as tracking two graded channels (e.g. support
and counter-support) simultaneously. In that setting, ≤ will typically be chosen so that moving
“up”Wcorresponds to having at least as much support and at least as much counter-support, and the
join    becomes a pointwise “take the strongest available components.” What matters at this stage
is that quantales give a single abstract interface: regardless of whether we are in a crisp, fuzzy, or
paraconsistent regime, the same definitions of aggregation and chaining apply.


                                                 56
     Quantales are a natural “glue” structure for Hyperseed because they simultaneously support:
(i) graded aggregation (joins); (ii) sequential or conjunctive composition (monoidal product); and
(iii) order-theoretic monotonicity (needed for observer-relativity and refinement arguments).
     Operationally, items (i)–(iii) are the minimum
                                             W      needed to speak about networks where many par-
tial influences converge on a node (hence ), where influences can traverse multiple links (hence ⊗),
and where strengthening local information cannot create a global weakening (hence monotonicity).
This is why the quantale layer sits in the “minimal formal core”: it pins down the algebraic laws
that make later propagation operators well-defined, compositional, and stable under iteration.

3.4    A canonical p-bit quantale
Definition 9 (Canonical commutative p-bit quantale). Let V := ([0, 1]2 , ≤, ⊕, ⊗, e) where:
• (a+ , a− ) ≤ (b+ , b− ) iff a+ ≤ b+ and a− ≤ b− (componentwise order),

• (a+ , a− ) ⊕ (b+ , b− ) := (max(a+ , b+ ), max(a− , b− )) (join),

• (a+ , a− ) ⊗ (b+ , b− ) := (a+ b+ , a− b− ) (monoidal product),

• e := (1, 1) (unit).
Then V is a commutative quantale.
Remark 59 (Why this is a quantale (explicit properties)). The statement that V is a commutative
quantale unfolds into three routine facts: (i) ([0, 1]2 , ≤) is a complete lattice; (ii) (V, ⊗, e) is a
commutative monoid; and (iii) ⊗ distributes over arbitrary joins in each argument.
                                                                          −
   For (i), completeness is componentwise: given any family {(a+                          2
                                                                     i , ai )}i∈I ⊆ [0, 1] , its join is
                                 _                                
                                           −                     −
                                   (a+i , ai ) =   sup a+
                                                        i , sup ai ,
                                     i∈I               i∈I      i∈I


and its meet is defined analogously with infima; these exist because [0, 1] is complete. For finite
joins, this recovers ⊕ as the componentwise maximum.
    For (ii), associativity and commutativity of ⊗ follow from associativity and commutativity of
multiplication in [0, 1] applied componentwise, and e = (1, 1) is a two-sided unit since a± · 1 = a± .
                                                     −
    For (iii), fix (b+ , b− ) and a family {(a+ i , ai )}i∈I . Then
_                                                                                      _
            −       + −                               − −                             − −             −     + −
    (a+                                + +                              + +
                                                                                               (a+
                                                                                                                  
       i , ai )  ⊗(b , b  ) =    (sup ai )b , (sup  a i )b    =  sup (a i b ), sup (a i b ) =    i , ai )⊗(b , b ) ,
                                 i             i                 i          i
 i∈I                                                                                      i∈I

using that multiplication by a fixed b± ∈ [0, 1] preserves suprema in [0, 1] (it is monotone and Scott-
continuous on the complete lattice [0, 1]). The same argument applies in the other argument, hence
⊗ preserves arbitrary joins separately, as required for a quantale.
Remark 60 (How to read ⊕ and ⊗ in this specific quantale). The operation ⊕ takes componentwise
maxima: it is an “evidence accumulation” operator. If one source gives evidence (0.7, 0.2) and
another gives (0.5, 0.9), then the aggregate is (0.7, 0.9): we keep the strongest support and the
strongest opposition, because both may matter in a paraconsistent setting.
    This reading also highlights that ⊕ is idempotent and commutative: aggregating the same piece
of evidence twice does not inflate it, and order of aggregation does not matter. Moreover, since ⊕
is the join induced by ≤, the inequality (a+ , a− ) ≤ (a+ , a− ) ⊕ (b+ , b− ) expresses that aggregation is
information-increasing in each coordinate.

                                                      57
    The operation ⊗ multiplies components: it is a “co-occurrence” or “chaining” operator. If
two independent stages each preserve positive evidence at rates a+ and b+ , then the two-stage
preservation is a+ b+ (and similarly for negative evidence). This multiplicativity is computation-
ally convenient and aligns with common probabilistic intuitions without reducing evidence-pairs to
ordinary probabilities.
    Algebraically, ⊗ is monotone in each argument with respect to ≤: if (a+ , a− ) ≤ (a0+ , a0− ) then
(a+ , a− ) ⊗ (b+ , b− ) ≤ (a0+ , a0− ) ⊗ (b+ , b− ), because multiplication by b± ∈ [0, 1] preserves order.
Intuitively, strengthening either the positive or negative component cannot weaken the chained out-
come.

Remark 61 (Bottom and top). The least element is ⊥ = (0, 0) and the greatest element is > =
(1, 1) = e. Intuitively, ⊥ represents “no evidence either way”, while > represents “maximal evidence
on both sides”. This is acceptable (and sometimes desirable) in paraconsistent settings; if one wants
> to mean “maximally true” instead, one may instead work with a different ordering (e.g. a truth
order vs. a knowledge order). For the present paper, the componentwise order is treated as an
information aggregation order.
    Concretely, with the information aggregation (knowledge) order, (a+ , a− ) ≤ (b+ , b− ) means that
b contains at least as much supporting evidence and at least as much opposing evidence as a. Under
this interpretation, increasing either coordinate represents adding information rather than resolving
a truth-value; hence it is consistent for > to carry maximal values in both coordinates.

Remark 62 (A concrete example and why e = (1, 1) is not a paradox). It may look strange that the
monoidal unit e carries maximal evidence in both components. But e is not intended to represent
“the proposition that is perfectly true.” It represents “no loss under composition”: composing with
e should not attenuate either positive or negative evidence. In that sense, e plays the role of a
neutral element for information-flow, not a metaphysical truth.
    This choice is particularly appropriate when the lattice order is read as “having at least as much
information” (knowledge order). Under that reading, (1, 1) is indeed the most informative point: it
contains maximal positive and maximal negative evidence simultaneously. This echoes the bilattice
tradition that separates truth-order from knowledge-order [23].
    A small numerical check may help: for any (a+ , a− ) we have (a+ , a− ) ⊗ (1, 1) = (a+ , a− ),
whereas (a+ , a− ) ⊕ (1, 1) = (1, 1). Thus e is neutral for chaining (⊗) but absorbing for aggregation
(⊕), exactly as one expects when ⊕ is a join operation and e happens to coincide with the top
element in the chosen order.

Remark 63 (Residuals (optional W    but often useful)). Many quantale-based constructions use the
(right) residual x ⇒ y := {z | x ⊗ z ≤ y} when it exists; in a quantale it always exists by
completeness. In the present [0, 1]2 instance, the residual is componentwise and can be written
explicitly using the usual residuum of multiplication on [0, 1]:
                                                                      (
                                                                       1,             a = 0,
      (a+ , a− ) ⇒ (b+ , b− ) = a+ ⇒× b+ , a− ⇒× b− ,
                                                     
                                                            a ⇒× b :=
                                                                       min{1, b/a}, a > 0.

This observation is not required for the basic development, but it clarifies that the canonical choice
supports implication-like operations (as adjoints to chaining) without leaving the p-bit domain.

Remark 64 (Other choices). The specific operations above are not mandatory. Any commutative
quantale compatible with the intended monotonicities can be substituted. The canonical choice is
used because it is simple, computable, and supports the toy model in Section 5.


                                                    58
    For example, one could replace componentwise multiplication by a different t-norm (and com-
ponentwise maximum by the corresponding join if one changes the underlying order), or keep the
componentwise order but use an alternative monoidal product reflecting a different notion of se-
quential combination. The key constraints are that ⊗ be associative, commutative, monotone, and
distribute over joins, so that the general quantale calculus remains available.

3.5   V -valued relations and quantale composition
Definition 10 (V -valued relations). Given a set X, a V -valued relation on X is a map

                                          R : X × X → V.

More generally, a V -valued relation from X to Y is a map R : X × Y → V .
Remark 65 (Basic special cases and why “relations” is the right word). When V = 2 = {⊥, >}
with ⊕ = ∨ and ⊗ = ∧, a V -valued relation R : X × Y → V is exactly an ordinary (crisp) relation:
R(x, y) = > means “related” and R(x, y) = ⊥ means “not related.” When V = [0, 1] with ⊕ = sup
and ⊗ a t-norm, one recovers standard fuzzy relations. The present setting keeps the same relational
syntax R(x, y) but allows richer evidence types, so that the same formalism can express classical,
fuzzy, and paraconsistent/bi-graded correspondences as instances.
Remark 66 (Intuition: relations as graded, possibly conflicting correspondences). A classical
relation says only whether (x, y) is related (yes/no). A V -valued relation assigns to each pair (x, y)
a value in V encoding graded evidence. When V = [0, 1]2 , this means we can simultaneously record
degrees of “x matches y” and “x does not match y,” without forcing a collapse. This directly
supports Hyperseed’s graded distinction/indistinction (Hyperseed-Concept 98).
    Example: If X is a set of perceived objects and Y is a set of internal symbols, then R(x, y) =
(0.8, 0.1) might mean the system mostly endorses interpreting object x as symbol y, with mild coun-
terevidence. In a conflicting case, R(x, y) = (0.8, 0.8) records a genuine ambiguity: strong reasons
to map and strong reasons not to map. Such relations are a natural substrate for representation and
correspondence (Hyperseed-Concept 157; Hyperseed-Concept 112) as discussed in cognitive-systems
settings [19].
Remark 67 (Terminology: evidence values live in a poset, not necessarily numbers). It is important
that V is used only through its order and its two operations. Even when one writes pairs such as
(0.8, 0.1), the formal reading is: R(x, y) is an element of an ordered structure in which one can
(i) combine pieces of evidence along a path using ⊗, and (ii) aggregate alternative paths using ⊕
(a join). Thus the same definitions apply when V is non-numeric (e.g. logical truth values, cost
semirings, or other complete lattices equipped with a compatible “multiplication”).
Definition 11 (Quantale “matrix” composition). Given R : X × Y → V and S : Y × Z → V ,
define their composite                     M
                          (S ◦ R)(x, z) :=    R(x, y) ⊗ S(y, z).
                                                y∈Y

When V is complete and ⊗ distributes over joins, this composition is associative.
Remark 68  L (Well-definedness for infinite Y and why completeness matters). For finite Y , the
expression y∈Y is just a finite join.
                                   L For general (possibly infinite) Y , the definition requires that
arbitrary joins exist in V so that    y∈Y (· · · ) is meaningful. This is exactly the “completeness”
condition in the quantale assumption, and it is the reason quantales (rather than merely monoids
or semirings) are the natural ambient algebra for relation-like composition over arbitrary sets.

                                                  59
                                                                        L
Remark 69 (Notation unpacking and a small example). The symbol y∈Y denotes the join (supre-
mum) over all intermediates y. It plays the role of “there exists a good intermediary” but in a graded
way: we aggregate the evidence contributed by each path x → y → z using ⊗, and then take the
best/most informative aggregate using ⊕.
    Example (finite Y ): if Y = {y1 , y2 } then
                                                                                
                  (S ◦ R)(x, z) = R(x, y1 ) ⊗ S(y1 , z) ⊕ R(x, y2 ) ⊗ S(y2 , z) .

This is literally matrix multiplication with (+, ·) replaced by (⊕, ⊗). The usefulness is that it
gives a principled notion of chaining approximate correspondences, essential for modeling multi-
step representation pipelines (e.g. perception → internal model → action), and it will later support
pattern-web propagation rules (Hyperseed-Concept 132).
Remark 70 (Associativity: what “⊗ distributes over joins” buys you). The associativity claim
can be seen by expanding both sides pointwise. Given R : X × Y → V , S : Y × Z → V , and
T : Z × W → V , one has
                                       M M                    
                   T ◦ (S ◦ R) (x, w) =        R(x, y) ⊗ S(y, z) ⊗ T (z, w),
                                           z∈Z y∈Y

and distributivity of ⊗ over joins allows one to rewrite this as
                                M M
                                         R(x, y) ⊗ S(y, z) ⊗ T (z, w).
                                z∈Z y∈Y

Similarly,                                M           M                   
                                
                     (T ◦ S) ◦ R (x, w) =   R(x, y) ⊗    S(y, z) ⊗ T (z, w) ,
                                           y∈Y             z∈Z

which also becomes              M M
                                          R(x, y) ⊗ S(y, z) ⊗ T (z, w).
                                y∈Y z∈Z

Since joins are associative/commutative up to the ambient order (and ⊗ is associative), these two
expressions coincide. Thus the “matrix” composition is not merely suggestive: it is genuinely
functorial under the standard quantale axioms.
Remark 71 (Interpretation as approximate correspondence). A V -relation R : X × Y → V can be
read as a graded, possibly inconsistent correspondence: R(x, y) is the amount of evidence that x in
X “matches” y in Y (or is “the same” for some purpose), with both positive and negative compo-
nents allowed. Composition then corresponds to chaining correspondences through an intermediate
representation.
Remark 72 (Reading ⊕ as aggregation of alternatives rather than averaging). The join ⊕ should
be read as an order-theoretic “best supported” (or “most informative”) combination of alternatives,
not as an arithmetic average. In particular, if one alternative path yields strictly stronger evidence
than another, the join simply retains the stronger one. This is one reason quantale composition is
well-suited to propagation of constraints or supports in a pattern web: multiple routes can contribute,
but the algebra specifies precisely how they compete or reinforce.
Definition 12 (Identity V -relation). For a set X, define idX : X × X → V by
                                                 (
                                                  e if x = y,
                                   idX (x, y) :=
                                                  ⊥ if x 6= y.

                                                  60
Remark 73 (Why this is the correct identity and what ⊥ does). The identity relation is meant
to say: an element matches itself with full compositional strength, and matches distinct elements
with none. Here ⊥ is the least element of V (in the p-bit quantale, ⊥ = (0, 0)), so it contributes no
evidence under joins and attenuates completely under products.
    A quick check in the finite case confirms the intuition: composing any R : X × Y → V with
idX on the left leaves R unchanged because only the x = y term contributes nontrivially. This
identity is essential because it lets us treat V -relations as morphisms in a bona fide category (so
that associativity and identity laws hold), which in turn is what makes later compositional arguments
about contexts and translations well-typed rather than metaphorical.

Remark 74 (Left and right unit laws pointwise). It is useful to keep in mind the explicit pointwise
verification. For R : X × Y → V and x ∈ X, y ∈ Y ,
                        M                                           M
     (R ◦ idX )(x, y) =    idX (x, x0 ) ⊗ R(x0 , y) = e ⊗ R(x, y) ⊕    ⊥ ⊗ R(x0 , y) = R(x, y),
                       x0 ∈X                                       x0 6=x

using ⊥ ⊗ v = ⊥ and ⊥ ⊕ v = v. Similarly idY ◦ R = R. These computations are routine but
conceptually important: they show that idX acts exactly like the diagonal matrix with e on the
diagonal and ⊥ elsewhere, matching the matrix analogy from Definition 11.

   With these definitions, sets and V -relations form a category (indeed, a standard quantaloid
construction when one varies X).

3.6   V -enriched categories and approximate morphisms
Hyperseed frequently talks as if there are “morphisms” between internal and external pattern
structures, but these morphisms are rarely exact. Quantale enrichment provides a uniform language
for this [7].
    A useful way to think about the role of the quantale (V, ≤, ⊗, e) is that it supplies a scale of
comparison (the order ≤) together with a compositional aggregator (the monoidal product ⊗) and
a baseline unit (the element
                        W    e). In many applications V is not merely a set of “weights”: it is chosen
so that arbitrary joins exist and ⊗ distributes over them, ensuring that “taking the best available
evidence” and “composing evidence” interact coherently. Although we assume commutativity here
for simplicity, many of the intended readings (e.g. asymmetric translation effort) can be modeled
in noncommutative quantales as well; the thin axioms below are written so that the directional
nature of C(A, B) is retained regardless.

Definition 13 (V -enriched category (thin form)). Let (V, ≤, ⊗, e) be a commutative quantale. A
V -enriched category C consists of:

• a class of objects Ob(C);

• for each A, B ∈ Ob(C), a hom-value C(A, B) ∈ V ;

such that for all A, B, C:

                             e ≤ C(A, A),   C(A, B) ⊗ C(B, C) ≤ C(A, C).

Remark 75 (Canonical choices of V ). Different choices of quantale recover familiar “approximate”
semantics. If V = 2 = {⊥ ≤ >} with ⊗ = ∧ and e = >, then a thin V -category is exactly a
preorder: C(A, B) = > means “A entails/reaches B” and the composition axiom is transitivity. If


                                                 61