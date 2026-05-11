# 7 Order, time, and becoming

semantic values. In particular, one may later impose optional structural conditions (symmetry,
reflexivity, transitivity up to evidence, etc.) when modeling a specific domain, but the present
definition stays neutral: it merely provides a slot in which such constraints can be stated explicitly
rather than smuggled in as informal assumptions.
                                                                                                    
Definition 39 (Context-induced evaluations on occasions). Given a context c = Xc , Πc , δc , ιc ,
define the induced evaluators on occasions by

                  δcE (o, o0 ) := δc Πc (o), Πc (o0 ) , ιEc (o, o0 ) := ιc Πc (o), Πc (o0 ) ,
                                                                                          

for o, o0 ∈ Ob(E).

Remark 178 (What the presentation map is doing). The map Πc : Ob(E) → Xc expresses the
idea that a context does not have direct access to “raw occasions as such,” but only to a quotient-
like presentation into context-level entities. This is intentionally weaker than requiring that Πc be
invariant under all identifications in E: an admissible identification f : o → o0 in the occasion
space need not be one that the context can or will recognize, and contexts may collapse distinctions
that E retains (or refine them by remembering additional tags in Xc ). In concrete models, one may
nevertheless choose to impose compatibility conditions of the form “if o and o0 are connected in
E, then Πc (o) and Πc (o0 ) are judged highly interchangeable,” but such requirements are part of a
modeling choice rather than part of the primitive ontology.

Remark 179 (Example patterns for contexts). Typical sources of context-dependence fit neatly
into the tuple c: (a) Resolution/attention: Xc contains only the coarse entities available at a given
resolution, with Πc forgetting fine-grained differences between occasions; (b) Coordinate/viewpoint
choice: Πc factors out transformations the context treats as irrelevant, while δc may still register
residual differences important for the task; (c) Memory and identity-tracking: Xc may include
persistent labels (“the cup from earlier”), so that Πc encodes a policy for binding new occasions
to existing labels, and ιc describes when substituting one label for another preserves predicted con-
sequences. These examples illustrate why separating Πc (what is presented) from δc , ιc (how it is
evaluated) is useful: the same coarse-graining can be paired with different evaluators depending on
goals and background commitments.

Remark 180. A simple example is a vision context in which Xc is a set of tracked objects on
a screen, Πc maps pixel-level occasions to object IDs, δc scores how different two tracks are, and
ιc scores whether they can be swapped without changing the task outcome (e.g. two identical chess
pawns in symmetric positions might be interchangeable for some purposes). Concretely, one can
think of the underlying occasion space as a stream of low-level sensor events (frames, patches, key-
points, or other “glimpses”), while Πc performs the role of a context-dependent binding/association
rule that declares which of those low-level events count as evidence about which putative object. In
that setting, δc is not required to be a metric in the strict mathematical sense; it is simply whatever
evaluation the context treats as “difference-relevant,” possibly combining appearance, trajectory,
and role features into a paraconsistent value. Likewise, ιc is best read as an invariance or sym-
metry score: it records whether exchanging two hypothesized entities preserves whatever objective
or downstream action policy defines “the same outcome” for the current task. This allows the for-
malism to express both perceptual distinctions (two tracks are strongly non-identical) and practical
equivalences (two tracks are distinct but functionally interchangeable), which need not coincide once
observer goals are made explicit. The definition is useful because later notions (weakness/simplicity,
patterns, resonance) require a stable place to anchor “who is distinguishing what, and under what
rules” [5]. In particular, once later constructions quantify over repeated occasions, compressibility,

                                                 103
or alignment across contexts, it becomes important that the act of “counting as the same thing” has
been made an explicit, indexable datum rather than an implicit assumption. In Hyperseed terms,
this is the structural backbone for Hyperseed-Concept 86 and Hyperseed-Concept 124.

Remark 181 (Observer-relativity as explicit data). In this reconstruction, observer-relativity is
not a philosophical afterthought; it is built in as explicit context-indexing. Different contexts can: (i)
carve the same occasion space E into different entity sets Xc ; (ii) disagree paraconsistently about
whether two entities are distinct or interchangeable. The point of allowing (ii) is not merely to
permit “uncertainty,” but to permit structured coexistence of competing discriminations: a context
may accumulate simultaneous evidence that two tracks are the same (e.g. perfect appearance match)
and that they are not (e.g. mutually exclusive trajectories), without collapsing into triviality. This
also clarifies that observer-relativity here includes both representational choices (what the observer
treats as an entity at all) and normative choices (what differences are treated as relevant to a task,
and what differences are ignored as symmetries). On this view, two contexts may share the same
raw stream E yet implement different “grain sizes” by choosing different Xc and different binding
maps Πc , leading them to construct different object inventories from the same experiential substrate.
This is the formal home for Hyperseed’s claim that much of “ontology” is bookkeeping about which
distinctions are made by which observers, and at what grain.

Remark 182 (Notation clarification: V and p-bit-valued evaluations). The codomain V is the value
space for paraconsistent evidence, intended to be the p-bit quantale (typically [0, 1]2 with a chosen
order and monoidal product; cf. Section 3.4). When we write δc (x, y) ∈ V we mean that δc (x, y) has
(at least) two coordinates, often read as (positive-evidence, negative-evidence). Intuitively, this lets
the model represent “evidence for difference” and “evidence against difference” (or, depending on
the chosen polarity, “evidence for sameness” and “evidence against sameness”) side by side, rather
than forcing a single scalar that must trade one off against the other. Componentwise comparisons,
multiplication-like combination ⊗, and join-like aggregation ⊕ then provide a disciplined calculus
for combining experiential judgments. For example, if two independent cues both support distinct-
ness, ⊗ can be used to accumulate that support; if two alternative cues provide competing routes
to the same judgment, ⊕ can be used to aggregate them without prematurely discarding minority
evidence. The need for this richer codomain shows up immediately when contexts are allowed to dis-
agree or when binding is ambiguous: the system must be able to carry forward incompatible partial
assessments until later constraints (task loss, additional observations, or higher-level regularities)
resolve or compartmentalize them.

6.2   Difference and distinction
Hyperseed distinguishes difference from distinction. Difference is directed: one occasion diverges
from another. Distinction is symmetric: two occasions mutually diverge. In practice, the separation
is useful because many cognitive and operational comparisons have an intrinsic “reference” (what
is being compared to), even when ordinary language uses a symmetric phrasing. The context
parameter c is intended to hold fixed the aspect, task, or perspective relative to which divergence
is evaluated (e.g. perceptual modality, feature set, goal constraints, or a representational code), so
that directedness is not conflated with merely changing evaluative criteria.

Definition 40 (Difference as a directed evaluation). Given a context c, define the directed differ-
ence evaluator
                                  Diff c (x → y) := δc (x, y) ∈ V.



                                                   104
The positive channel Diff c (x → y)+ is evidence that x diverges from y. The negative channel
Diff c (x → y)− is evidence that x does not diverge from y (e.g. x is absorbed into, explained by, or
indistinguishable-from y along the relevant aspect).

     It is worth emphasizing that Diff c is not assumed to be a metric, a distance, or even a preorder; it
is simply an evaluator returning a p-bit-style evidential value. Accordingly, nothing in the definition
forces Diff c (x → y)+ and Diff c (x → y)− to be complements, and (in paraconsistent regimes) they
may both be high, representing simultaneously strong reasons for divergence and strong reasons for
non-divergence under different sub-aspects aggregated into the same context c. Conversely, they
may both be low, representing insufficient evidence either way.

Remark 183 (Intuition and examples for directed difference). The directedness in Diff c (x →
y) matters whenever “x differs from y” is not symmetric in the lived or operational sense. For
instance, a coarse prototype y may “explain” a fine-grained observation x better than x explains
y. In perception, a noisy instance may be well-absorbed into a clean template (low divergence of x
from y) even though the template does not fit the instance in reverse (higher divergence of y from
x) if the evaluators are aspect-sensitive.
    This definition is useful because it isolates the smallest unit in which “otherness” can appear: a
directed contrast. It corresponds naturally to Hyperseed-Concept 96 and provides the raw material
out of which symmetry (distinction), grouping (relations), and ultimately patterns are built [5]. A
further way to read the direction x → y is as “evaluate x using y as the comparator or explanatory
basis”: if y is a model, type, or hypothesis and x is a datum, then Diff c (x → y)+ expresses the degree
to which the datum resists assimilation to the model, while Diff c (x → y)− expresses the degree to
which it is successfully covered by the model. This interpretation also clarifies why the negative
channel is phrased as “does not diverge” rather than “is identical”: absorption and explainability
are often weaker (and more context-dependent) than identity.

Remark 184 (Self-comparison and neutral cases). Although many applications will set Diff c (x →
x)+ to be small and Diff c (x → x)− to be large (reflecting the expectation that an occasion does not di-
verge from itself ), the formalism does not require this. Allowing nontrivial self-difference can model
temporal or perspectival drift (an “occasion” treated as a process with internal variation), sensor
noise (a self-sample may not reproduce exactly), or representation mismatch (different encodings of
“the same” occasion). When a context c is too coarse or too uncertain to decide, Diff c (x → y) may
be near-indeterminate in both channels, which is precisely the situation later “weakness” notions
are designed to register rather than forcibly resolve.

Definition 41 (Distinction as mutual difference). Define the (symmetric) distinction evaluator by

                             Distc (x, y) := Diff c (x → y) ⊗ Diff c (y → x),

where ⊗ is the p-bit product from Section 3.4. Thus evidence that x and y are mutually distinct
compounds multiplicatively (and likewise for evidence against mutual distinctness).

    Because ⊗ combines evidential values, Distc is best read as “joint support for two directed
claims” rather than as an averaged similarity score. In particular, if either direction strongly fails
(e.g. Diff c (x → y)+ is very low because x is thoroughly absorbed into y in context c), then the
compounded support for mutual distinctness will typically be reduced. When ⊗ is commutative (as
in standard p-bit constructions), Distc (x, y) = Distc (y, x) holds automatically, aligning the formal
object with the intended symmetric reading.



                                                   105
Remark 185 (Intuition and examples for distinction). The move from difference to distinction is
the move from “x contrasts with y in this direction” to “x and y stand apart from each other.” If one
thinks geometrically, Diff c (x → y) is like a directed arrow recording mismatch; taking Distc (x, y)
amounts to requiring mismatch in both directions and combining the two pieces of evidence via
⊗. In a crisp (non-paraconsistent) setting, one could imagine Diff c (x → y) as a Boolean; then
Distc (x, y) reduces to conjunction.
    The definition is necessary because later measures of weakness and simplicity depend on how
many distinctions a context fails to make. Distinction provides the symmetric “edge” concept needed
for graphs, equivalence-like closures, and entropy-like measures such as graphtropy (cf. Hyperseed-
Concept 98 and Hyperseed-Concept ??). One can also view Distc as the minimal symmetry-
enforcing operation applied to raw directed evaluations: rather than attempting to symmetrize by
averaging or by taking a maximum, ⊗ encodes the idea that mutual distinctness is supported only
to the extent that both directed divergences are supported together. This choice aligns with later
graph-theoretic constructions, where an undirected edge typically represents a mutual relation that
should not be present if either directed justification for separating the nodes is missing.
Remark 186 (Paraconsistent readings of mutuality). Since values live in V, mutuality can itself be
conflicted: it is possible to have substantial evidence that x and y are distinct and, simultaneously,
substantial evidence that they are not distinct (for example, two stimuli may differ in shape but be
functionally interchangeable for the current task). Under Distc (x, y) = Diff c (x → y)⊗Diff c (y → x),
such conflicts can arise either from conflicts already present in one direction or from an interplay
between directions (e.g. one direction supports divergence while the other direction supports non-
divergence). This is not treated as a defect but as a faithful representation of contexts in which
“making a distinction” is itself unstable, multi-aspect, or sensitive to what is taken as explanans
versus explanandum.
Remark 187 (Thresholding). To obtain a crisp “made distinction” relation (useful for counting,
graphs, and later definitions of graphtropy), choose thresholds τδ , τι ∈ (0, 1). One may then declare:
                                  x #c y    ⇐⇒      Distc (x, y)+ ≥ τδ .
Hyperseed frequently reasons at both levels: a fuzzy background of graded distinctions together with
crisp distinctions induced by task needs. In applications, τδ governs the willingness to treat weak
positive evidence as sufficient to “separate” two occasions, and adjusting it changes graph density
in the induced crisp distinction graph. The additional parameter τι is naturally available for dual
thresholding of the negative channel (e.g. to assert a crisp “indistinguishable” or “identified” relation
when Distc (x, y)− is large), allowing a context to support both separation and identification decisions
with explicit, independent criteria when required by downstream constructions.
Remark 188 (Notation clarification: channels and threshold parameters). When we write Distc (x, y)+
we mean the positive-evidence coordinate of the p-bit value Distc (x, y) ∈ V; similarly for − . The
thresholds τδ , τι are real numbers in (0, 1) used to turn graded evidence into crisp relations when
needed. It is often helpful to keep in mind the typing discipline implicit here: Diff c and Distc return
objects of the same evidential type V, while channel extraction (−)+ and (−)− maps those objects
to ordinary reals (or whatever ground scale V uses for each coordinate), which is why comparing to
numerical thresholds is well-formed.

6.3   Repetition, variety, non-duality, and non-dual variety
Beyond difference/distinction, Hyperseed elevates four additional pairwise experiential categories
to the primitive level. In the present reconstruction, these are defined by combining (i) distinctness

                                                  106
information and (ii) interchangeability information, both potentially paraconsistent. In particular,
the intent is that a context may track not only “are these two presented as different?” but also
“can one stand in for the other without loss for the currently salient purpose?”; the latter is a
practical/operational relation rather than a purely perceptual one. Because both axes are evaluated
with potentially incomplete and competing cues, it is important that the formalism can represent
mixed evidence without forcing an immediate resolution.
Definition 42 (Soft interchangeability). Given c, interpret ιc (x, y) ∈ V as a paraconsistent evalu-
ation of interchangeability. We will often use its two channels as shorthand:

        ιc (x, y)+ (evidence interchangeable),      ιc (x, y)− (evidence not interchangeable).

Remark 189 (Intuition and examples for interchangeability). Interchangeability is not sameness.
Two items can be distinct and yet substitutable for a purpose: two identical screws in a machine,
two equivalent lemmas in a proof, or two tokens of a symbol-type. Conversely, two items can be
nearly indistinguishable in raw perception and yet not interchangeable because of hidden constraints
(one is a live wire, the other insulated). The paraconsistent reading allows both kinds of evidence
to be present, which is often how real systems behave under partial information [23, 24].
    Formally, ιc gives us a second axis beyond distinctness. This is useful because Hyperseed’s later
notions of pattern and emergence rely not only on detecting difference, but on discovering stable
substitutions and invariances across contexts (Hyperseed-Concept 59 and Hyperseed-Concept 130).
    Interchangeability should also be read as explicitly context-indexed: ιc (x, y) can change when
the operative goal, constraints, or “interface” changes. For example, two objects may be inter-
changeable with respect to mass distribution (balancing a scale) but not interchangeable with
respect to provenance (authenticity, ownership, legal responsibility). Nothing in the primitive re-
quires ιc to be an equivalence relation: symmetry and transitivity may hold in some contexts (e.g.
standardized parts) but can fail in others (e.g. substitutability under resource limits, one-way em-
ulation, or asymmetric access rights). The paraconsistent two-channel representation is therefore
meant to cover both well-behaved “mathematical” substitution and the more brittle substitutions
encountered in empirical systems.
Definition 43 (Repetition and variety (threshold form)). Fix thresholds τδ , τι ∈ (0, 1). For x 6= y
in Xc define:

                      Repc (x, y)   ⇐⇒     Distc (x, y)+ ≥ τδ and ιc (x, y)+ ≥ τι ,
                      Varc (x, y)   ⇐⇒     Distc (x, y)+ ≥ τδ and ιc (x, y)− ≥ τι .

Intuitively, a repetition is a pair that is experienced as distinct yet context-substitutable; a variety
is distinct and non-substitutable.
Remark 190 (Intuition and examples for repetition and variety). A repetition is the lived form
of “same pattern, different instance.” Two distinct footsteps in sand may be distinct events (Dist+   c
high) but interchangeable as tokens of one gait (ι+ c high). A variety is the contrary: the distinction
matters. Two keys on a keyboard are distinct and not interchangeable if one is “Enter” and the
other is “Escape” for the current task.
    These notions are useful because they separate mere multiplicity from structured multiplicity.
Repetition is where compression begins: if many distinct things are interchangeable, a context can
represent them with less descriptive effort, feeding directly into simplicity/weakness reasoning [3, 2].
Variety, by contrast, is where complexity is forced upon the system because substitutions break. This
corresponds to Hyperseed-Concept 155 and Hyperseed-Concept 199.

                                                  107
     It is worth emphasizing that the threshold presentation is a “crisping” of inherently graded
judgments. The parameters τδ and τι should be understood as knobs for when evidence becomes
actionable for a context: in some regimes one may require near-certainty before treating two items
as substitutable, while in others weak evidence may suffice. Because both Distc and ιc have two
channels, these thresholds can be used to carve out robust regions of decision even when the
complementary channel is non-negligible; for instance, a system may classify Repc (x, y) based on
ιc (x, y)+ being high, while still retaining “residual” ιc (x, y)− as a warning that substitution is not
unconditional. This separation between stored evidence (the p-bit valuation) and downstream cat-
egorization (thresholding) is part of what allows Hyperseed to represent pragmatic choice without
losing contradictory or minority cues.

Definition 44 (Non-duality and non-dual variety (threshold form)). Fix thresholds τδ , τι ∈ (0, 1).
For x 6= y in Xc define:

                 NonDualc (x, y)    ⇐⇒      Distc (x, y)+ ≥ τδ and Distc (x, y)− ≥ τδ ,
                   NDVarc (x, y)    ⇐⇒      ιc (x, y)+ ≥ τι and ιc (x, y)− ≥ τι .

Thus non-duality is “distinct and not-distinct” (paraconsistent distinctness), while non-dual variety
is “interchangeable and not interchangeable” (paraconsistent substitutability).

Remark 191 (Intuition and examples for non-duality and non-dual variety). Non-duality here
is not a metaphysical decree that all things are identical; it is a disciplined way of representing a
familiar phenomenological tension: the same pair can be simultaneously experienced as separate and
as not-separate. In perceptual bistability (e.g. ambiguous figures), one may have strong evidence
for two incompatible parsings. In social cognition, one may experience another person as “other”
and yet as “part of me/us”; the formal point is that both channels can be high without forcing
contradiction to trivialize the system [24].
    Non-dual variety likewise captures cases where substitution is both licensed and prohibited de-
pending on which constraints are salient. For example, two roles in an organization may be inter-
changeable in a reporting chart but not interchangeable for legal responsibility. These definitions
are useful because they prevent an overly classical ontology from erasing precisely the regimes where
experience is richest: the zones where evidence does not settle into a single polarity (Hyperseed-
Concept 121 and Hyperseed-Concept 120).

   Non-dual variety can also arise in technical settings where multiple compatibility layers coexist.
Two software modules may be interchangeable at the level of an interface (they implement the
same signature, so ι+
                    c is high) yet not interchangeable at the level of non-functional constraints
(performance, security policy, licensing, nondeterminism), yielding substantial ι−
                                                                                 c as well. Similarly,
in mathematics two proof steps might be interchangeable from the perspective of entailment, but
not interchangeable from the perspective of constructive content, proof length, or allowed axioms;
what counts as “salient” is again context-indexed, so it is natural that the evidence channels can
both be high before a downstream agent commits to a choice.

Remark 192 (Non-duality as paraconsistency rather than collapse). A common mathematical
temptation is to interpret “not-distinct” as strict equality. Hyperseed explicitly resists this: non-
duality is not the claim that x = y as symbols, but that experience supplies simultaneous evidence
for and against the distinction. The p-bit semantics makes this precise: non-duality is simply a
region of the square [0, 1]2 where both channels are large. No logical explosion occurs because the
logic is paraconsistent.


                                                  108
    The four primitives discussed in this subsection should not be read as mutually exclusive, nor as
exhausting all possible evidence states. Because the underlying evidence is stored in two-channel
form, it is possible (and often realistic) that Repc (x, y) holds while ιc (x, y)− is also nontrivial
(a “normally safe” substitution with known caveats), or that Varc (x, y) holds while ιc (x, y)+ is
also nontrivial (items are usually not substitutable, yet there are emergency procedures or partial
substitutions). Likewise, non-duality in distinctness can co-occur with either repetition or variety
judgments: one can have strong evidence for both distinction and non-distinction while also having
a fairly settled stance on interchangeability (or vice versa). In this sense, NonDualc and NDVarc
track tensions within a single evidence axis, whereas Repc and Varc combine information across
the distinctness and interchangeability axes.
    A useful geometric picture is to treat each p-bit-valued predicate as placing the pair (x, y) at a
point in [0, 1]2 (one coordinate for positive evidence and one for negative evidence). Thresholding
then selects regions: NonDualc (x, y) corresponds to the “upper-right” region of the distinctness
square, while NDVarc (x, y) corresponds to the upper-right region of the interchangeability square.
By contrast, Repc (x, y) and Varc (x, y) are defined by combining one channel from the distinctness
square (the positive channel) with one channel from the interchangeability square (positive or
negative, respectively). This helps clarify why non-dual categories are not simply “in between”
repetition and variety: they represent high-confidence conflict rather than low-confidence ambiguity.
    Finally, there is a classical limit worth keeping in view. If, for a given context, the evidence
is nearly consistent in the sense that Distc (x, y)− is typically small whenever Distc (x, y)+ is large
(and similarly for ιc ), then NonDualc and NDVarc will be rare, and the remaining categories behave
more like classical dichotomies: distinct pairs separate into mostly interchangeable repetitions
and mostly non-interchangeable varieties. Hyperseed retains the non-classical regimes not because
they are always present, but because they become decisive precisely in settings involving partial
observability, layered constraints, or competing interpretations—the same settings where pattern
discovery and emergent structure are most informative.

6.4   First, Second, Third, Fourth
Hyperseed uses the numerical-metaphysical categories First, Second, Third (Peirce) and extends
them with Fourth (synergy, Jungian “mandalic” structure). The key point for a rigorous ontology is
that these are not mystical numerology; they are structural levels obtained by iterating a small set
of constructions. Concretely, the intent is that each higher “number” is not an extra ingredient but
a disciplined closure step on what came before: Firsts are carriers, Seconds are directed contrasts
between carriers, Thirds are reusable organizations of such contrasts, and Fourths are higher-order
organizations of multiple Thirds whose joint behavior is not reducible to separate consideration of
each Third in isolation. This “iterated construction” view is what will allow later sections to treat
phenomenological language as shorthand for precise mathematical objects and maps between them,
rather than as a separate interpretive layer.
Remark 193. Peirce’s categories are often presented as metaphysics [14], but they are equally well
read as an austere typology of how relations enter experience: firstness as suchness, secondness as
reaction, thirdness as mediation/law. Hyperseed’s maneuver is to make this typology operational: we
identify canonical mathematical carriers for each level, so that later theorems can depend on them
without importing any particular spiritual vocabulary [1]. A further benefit of making the carriers
explicit is that one can compare different contexts c by comparing their associated carrier-sets Xc
and the maps between them; in other words, the Peircean ladder becomes compatible with ordinary
mathematical practices of translating structures across domains (e.g. from perceptual contexts to
linguistic contexts) without presuming that the underlying “stuff ” is the same.

                                                 109
6.4.1   A minimal inductive ladder
The ladder below is “minimal” in the sense that each step adds only as much structure as needed to
express the corresponding Peircean intuition. In particular, nothing forces Diff c , V , or Synergizec
to have any special form beyond what is required for subsequent constructions; the framework is
designed so that one may instantiate them with metrics, divergences, logical orderings, probabilistic
scores, or other application-specific choices as long as they fit the declared types.

Definition 45 (Firsts). For a context c, a First is an entity x ∈ Xc considered without relating it
to anything else. Operationally, it is the unit of description before any distinctions are made.

Remark 194 (Intuition and examples for Firsts). A First is the bare “this-such” prior to compar-
ison: a tone as heard before labeling it as higher than another, a patch of red before classifying it
as stop-sign, a number-symbol “17” before embedding it into arithmetic structure. In formal terms,
it is just an element of Xc , but the point is methodological: we allow ourselves to speak of entities
even when no relational judgments have yet been asserted about them.
     This is useful because it separates existence-in-a-context from structure-in-a-context. Many later
constructions (weakness, abstraction, patterns) talk about how relations over Xc behave; identifying
Firsts as the carriers of later relations keeps the levels clean (Hyperseed-Concept ??). It is also
helpful to read Xc as a typed carrier: the context c fixes what counts as an admissible “atom of
discourse” at all (pixels, tokens, hypotheses, actions, etc.), and the subsequent ladder then describes
increasingly structured ways of speaking about those admissible atoms, rather than silently changing
the underlying domain midstream.

Definition 46 (Seconds). For a context c, a Second is a directed difference event, i.e. an ordered
pair (x, y) ∈ Xc × Xc together with its directed difference evaluation Diff c (x → y). Seconds are the
smallest units at which “reaction” or “opposition” can be represented.

Remark 195 (Intuition and examples for Seconds). A Second is what appears when a First meets
resistance: “this is not that,” “I cannot substitute this for that,” “this pushes back.” The ordered
pair (x, y) records directionality: x can fail to fit y even if y fits x in some aspect-sensitive sense.
In a predictive setting, one may read a Second as the primitive discrepancy between a model state
and an observation.
    The definition is useful because it makes explicit the granularity at which “difference” lives: not
as a global property of a system but as a local, typed datum that can later be aggregated into Thirds
(relations) and Fourths (synergistic webs). This aligns with Hyperseed-Concept 163 and Hyperseed-
Concept 163. One can think of Diff c (x → y) as an annotation on the arrow x → y: depending on
the application, it may be a real-valued cost, an element of an ordered evidence lattice, a probability
of mismatch, or a logical witness of incompatibility. The only commitment at this stage is that the
evaluation is part of the Second, so that later operations have access to both the fact of pairing
(x, y) and the strength/character of the directed contrast.

Definition 47 (Thirds). For a context c, a Third is a grouping of Seconds. Concretely, we model
a Third as a (possibly fuzzy) relation

                                          R : Xc × Xc → V,

where V is a commutative quantale as in Section 3.4. In the simplest crisp case, a Third is just a
subset R ⊆ Xc × Xc .



                                                  110
Remark 196 (Intuition and examples for Thirds). If Seconds are individual dyadic events, then a
Third is a policy, a rule, or a stable pattern of such events: “whenever x is of type A and y is of type
B, treat them as distinct,” or “these pairs are usually interchangeable.” In the crisp case, a Third
is literally a set of ordered pairs; in the V -valued case it is a graded and potentially paraconsistent
assignment of evidence to each pair.
     The usefulness is twofold. First, Thirds are composable: relations can be combined, closed,
propagated, and compared—all operations that become central in later discussions of patterns and
emergence [5]. Second, Thirds are where weakness/simplicity naturally lives: weakness measures
are aggregations over relations of which distinctions are left unmade [3, 2] (Hyperseed-Concept 190
and Hyperseed-Concept 132). It is worth emphasizing why the codomain V is taken to be a quantale:
it supports a join operation (for pooling/merging evidence across sources) and a monoidal product
(for chaining/propagating relational strength), so that one can later model both “either of these
reasons supports the relation” and “these reasons compose along a path” in a uniform algebraic
language.

Remark 197 (Relation-as-Third). This choice is deliberately aligned with the observation that
“a relation is a set of ordered pairs grouped together.” The mathematical point is that the move
from Second to Third is the move from isolated dyadic differences to a reusable schema of dyadic
differences. This becomes the backbone for later constructions: patterns, rules, causal links, and
interpretive frames all live at the level of Thirds. Equivalently, Seconds correspond to tokens of
interaction, while Thirds correspond to types (or stable regularities) extracted from many such
tokens; this token/type distinction is one of the simplest ways to see how “lawlike mediation” can
be implemented without positing any additional metaphysical substance beyond the data of directed
contrasts and their organization.

Definition 48 (Fourths). A Fourth is a higher-order grouping that joins multiple interconnected
Thirds into a larger web in a way that can create emergent “whole is greater than the parts” behavior.
   Formally, let Thic denote a chosen class of Thirds (e.g. V -valued relations on Xc with finite
support). A Fourth is specified by a finite diagram D in Thic (a network of relations together with
chosen overlap maps), together with a chosen composite/colimit-like operation

                                        Synergizec (D) ∈ Thic .

The degree of Fourthness (synergy) of D is then measured by an emergence functional (defined
precisely in Section 9) comparing the “intensity” of Synergizec (D) to the intensities of the individual
relations in D.

    A diagram D should be read as more than a mere set of Thirds: the overlap maps encode how the
component relations are intended to share variables, subdomains, or intermediate identifications,
i.e. where one relation’s “output” becomes another relation’s “input” or constraint. In concrete
applications, Synergizec (D) may be instantiated as a closure operation, a pushout/pullback-like
construction, an inference step that propagates constraints across the network, or any other prin-
cipled mechanism that produces a new Third capturing what is jointly implied by the entire con-
figuration. This is also the sense in which the Jungian “mandalic” image is meant: not a claim
about symbolism, but a reminder that Fourths are characterized by global coherence arising from
a structured interlocking of multiple mediations rather than from any single dyadic interaction or
single law taken alone.

Remark 198 (Intuition and examples for Fourths). A Fourth is where “mere aggregation” becomes
“organization.” Said differently, a Fourth is not just “many Thirds at once” but a joint constraint

                                                  111
system in which the participating Thirds co-determine what counts as admissible structure. If each
Third is a relational lens (a rulebook, constraint-set, or association pattern), then a Fourth is a
structured conjunction of lenses whose interaction yields consequences none had in isolation. In
particular, the interaction is not merely logical conjunction at the level of predicates; it includes a
chosen mode of interaction (a way the lenses compose, interfere, reinforce, or propagate along each
other).
    In a toy model, take two relations R1 and R2 and close them under a composition rule; the
closure may entail new pairwise links, and those entailments are precisely the mathematical shadow
of “emergence.” Concretely, if R1 and R2 are viewed as permitted transitions, then closing under
composition asserts that multi-step transitions are also permitted, producing new edges (x, z) from
paths (x, y) ∈ R1 and (y, z) ∈ R2 . Even when R1 and R2 are each individually sparse or locally
meaningful, their combined closure can produce global connectivity patterns, equivalence classes, or
invariants that were not readable from either relation alone.
    This definition is useful because it is flexible while still principled: by making a Fourth a diagram
plus a chosen universal-like composition, we ensure that Fourthness is not a vague adjective but a
reproducible construction. The “diagram” component specifies which Thirds are present and how
they overlap or are glued; the “composition” component specifies how information is allowed to flow
across that overlap. As a result, Fourthness can be tested by checking whether the composite object
supports new entailments, new conserved quantities, or new effective rules that are stable under the
chosen composition.
    It directly anticipates later pattern/emergence formalisms (Hyperseed-Concept ?? and Hyperseed-
Concept ??) and aligns with Hyperseed’s emphasis on synergy as a core engine of intelligence [19].
In that framing, Fourthness is the minimal formal layer at which “synergy” becomes something we
can compute, compare across contexts, and reason about via functorial or closure properties rather
than by informal appeal to holism.
Remark 199 (Why the definition is “diagram + composition”). Hyperseed’s description of Fourth-
ness emphasizes embedding a local network of relations into a broader web. This emphasis is
important: the same local Third can behave very differently when placed inside different ambient
relational environments, because the ambient links provide additional paths of inference, constraint
propagation, or coordination. In category theory, “a local network of composable pieces plus an
embedding into a larger web” is naturally represented by a diagram and a universal construction
(colimit, pushout, Kan extension, etc.). The diagram records the local pieces and their interface
maps, while the universal construction enforces that the resulting composite is the most general ob-
ject compatible with those interfaces (or, depending on direction, the best approximation living in
a target category). This is precisely the categorical way to ensure that the composite object depends
on the parts only through their specified relationships, rather than through arbitrary presentation
artifacts.
    We keep the definition abstract here because different applications suggest different concrete
choices of diagram shape and composition law. For example, when relations represent constraints, a
colimit-like construction captures gluing constraints together; when relations represent observations,
a Kan extension-like construction can express how local observations induce global predictions; and
when relations represent rewrites or proofs, closure under a proof calculus implements the intended
notion of inferential completion. The intended invariance is: if two diagrams are isomorphic (or
equivalent up to the relevant notion of equivalence in context), their synergized outputs should be
correspondingly equivalent, so that Fourthness behaves stably under re-indexing and re-description.
Remark 200 (Notation clarification: Thic and D). The symbol Thic is not a new axiom but a
placeholder for “whatever collection of Thirds we are willing to manipulate in context c” (e.g. finite-

                                                  112
support relations, measurable relations, etc.). The point of leaving Thic schematic is that Fourthness
should not depend on a single privileged substrate: one can instantiate Thirds as binary relations,
weighted relations, stochastic kernels, logical theories, constraint graphs, or other relational objects,
provided the context supplies a sensible notion of combination. In practice, the context c encodes
what counts as an entity, what counts as a relation over entities, and what operations (composition,
closure, saturation) are admissible or computable.
    A “finite diagram D in Thic ” means a finite indexing shape (a small finite category) together
with an assignment of an object of Thic to each node and overlap maps along arrows. Here “fi-
nite” is primarily a technical convenience: it guarantees that the specified pattern of interaction is
bounded and can be treated as a discrete schema, which is particularly relevant for computational
implementations and for avoiding size issues. The “overlap maps” should be read as interface con-
straints: they specify how one Third is to be matched against another (e.g. shared variables, shared
subrelations, restriction maps, or inclusion of a common substructure).
    The operation Synergizec is then a chosen way to combine the diagram into a single Third. It
is useful to think of Synergizec as a context-dependent “completion” or “fusion” operator: it takes
multiple partial lenses and returns a single lens that reflects what is jointly implied once they are
allowed to interact by the chosen rule. Depending on the application, Synergizec may be idempotent
(a closure operator), may be monotone with respect to refinement of diagrams, and may satisfy
naturality properties under change of context, but these are additional structure one may impose
later rather than assumptions built into the notation.

6.4.2   A concrete set-theoretic model (optional)
Example 8 (Set-theoretic First–Fourth ladder). Fix a context c with entity set Xc . Define

                               Firstc := Xc ,
                            Secondc := Xc × Xc ,
                              Thirdc := P(Xc × Xc ),
                             Fourthc := P(Thirdc ) (families of relations).

This ladder is intentionally coarse-grained: it treats a Third as a plain subset of pairs, so that the
only built-in structure is membership. Even so, it already separates (i) entities, (ii) raw dyadic
interactions, (iii) stabilized patterns of interaction (relations), and (iv) ensembles of such patterns.
    A “synergy” operator might map a family of relations {Ri } to their closure under a composition
rule (e.g. relational composition, transitive closure, or closure under a proof calculus). For instance,
one may define                                                [ 
                                    Synergizec ({Ri }) := cl      Ri ,
                                                               i

where cl is a chosen closure operator (transitive closure, reflexive-transitive closure, or a domain-
specific saturation procedure). The key point is that the closure is not merely union: it adds whatever
the rulebook says must follow from jointly having those relations available.
    The resulting closure typically contains entailments that were not present in any single Ri . In
graph language, new edges appear because multi-edge paths become single-step consequences under
the closure rule; in logic language, new theorems appear because premises from different Ri can be
combined in a single derivation. This is the simplest rigorous picture behind “the whole is greater
than the parts.” It also exhibits a minimal notion of “organization”: the output relation can encode
higher-level regularities (e.g. connectivity components, reachability, or induced equivalences) that
effectively act like emergent macroscopic features of the system.

                                                  113
Remark 201 (Why include the set-theoretic model). The optional ladder is a sanity anchor: it
shows that the definitions do not require higher category theory to be meaningful. It also makes
explicit which step introduces which kind of structure: moving from Secondc to Thirdc is the shift
from individual interactions to patterns of interaction, while moving from Thirdc to Fourthc is the
shift from one pattern to interacting patterns. Even in this elementary setting, the conceptual point
survives: Fourthness corresponds to closure/interaction effects among multiple relations. Moreover,
one can already ask meaningful questions such as: when does synergizing preserve symmetry, when
does it generate equivalence relations, and when does it create long-range dependencies that were
absent from the input family?
    This is also the simplest place to test computational toy models before lifting to enriched or
higher-categorical settings [5]. For example, one can implement Synergizec as a saturation loop,
measure the growth of the closure as a function of input family size, and compare different closure
rules as different hypotheses about what kind of “synergy” a given domain supports. Such exper-
iments help distinguish effects that are artifacts of representation from effects that persist under
more abstract formulations.

6.5    Presentational immediacy and intensity
Hyperseed treats presentational immediacy as a primitive correlate of “raw consciousness”: some
occasions are foreground, others background, and this distinction is fuzzy. We model this fuzziness
as a context-indexed salience (intensity) field. In particular, the index c is meant to cover whatever
factors jointly determine “what it is like right now”: task demands, bodily state, sensory modality,
memory activation, and ongoing control state. Nothing in this subsection presumes that the salience
assignment is stable across time, agents, or tasks; it is explicitly permitted (and expected) that Ic
changes as the context changes.

Definition 49 (Presentational immediacy). A presentational immediacy function in context c is
a map
                                      Ic : Xc → [0, 1].
If Ic (x) is near 1, x is in the foreground of experience in c. If Ic (x) is near 0, x is in the background.

    The choice of codomain [0, 1] is a normalization convention rather than an ontological claim
that salience is intrinsically bounded. It allows comparisons within a context and makes later
constructions (e.g., thresholds, resource budgets, and weighted graphs) notationally simple. Im-
portantly, Ic is not intended to be a probability, and no additivity constraints are imposed; multiple
entities may simultaneously have high immediacy. Similarly, we do not require maxx∈Xc Ic (x) = 1
(although one may impose such a gauge-fixing in specific models), because contexts may differ in
overall “vividness” or saturation.

Remark 202 (Intuition and examples for presentational immediacy). The function Ic is the formal
shadow of the commonplace fact that experience has a figure/ground structure. While staring at a
page, the letters are foreground; the pressure of one’s feet is fringe; the hum of distant traffic may
be nearly absent. The map Ic : Xc → [0, 1] is intentionally modest: it asserts only that a context
can assign graded salience to its presented entities.
    This definition is useful because it provides a primitive quantity that later theories can explain
rather than assume. In later sections, intensity will be connected to effort, resource allocation, and
attention dynamics (Hyperseed-Concept 138 and Hyperseed-Concept 60; see also [19] for related
cognitive resource themes).


                                                    114
    A further virtue of treating immediacy as a field over Xc is that it can, in principle, be applied
uniformly across heterogeneous kinds of presented entities. For example, Xc may contain perceptual
items (a letter-shape), interoceptive signals (heart rate sensations), affective tones (unease), action
affordances (“turn the page”), and memory fragments (a recalled phrase). The same formalism
covers all of these without committing to a single representational format. This is one reason the
definition is kept at the level of a simple map rather than, say, a modality-specific vector or a
hand-built attentional structure.

Remark 203 (Foreground/background is not (yet) attention). Later (Section 8 and onward) we
will connect intensity to effort/energy expenditure and obtain attention as a dynamical/resource
concept. Here we keep intensity primitive: it is an observational datum about what is “present”
and with what degree.

    It is also useful to distinguish immediacy from related but nonidentical notions that often travel
under the same name in informal discussions. For instance, an item may be highly immediate
because it is perceptually intrusive (a loud bang), even if it is not selected for deliberate manipula-
tion or report; conversely, an item may be the target of deliberate control (a rehearsed intention)
while remaining phenomenologically “thin” compared to vivid sensory input. By separating (i) a
phenomenological grading Ic from (ii) later dynamical and computational mechanisms, Hyperseed
leaves room for models in which selection, report, working memory access, or executive control can
dissociate from subjective vividness.

Definition 50 (Focus and fringe). Given a threshold τI ∈ (0, 1), define the focus set

                                Focusc (τI ) := {x ∈ Xc : Ic (x) ≥ τI },

and the fringe set
                              Fringec (τI ) := {x ∈ Xc : 0 < Ic (x) < τI }.
These are coarse operationalizations of the fuzzy foreground/fringe distinction.

    Note that Fringec (τI ) explicitly excludes entities with Ic (x) = 0. This leaves open two common
interpretations, both compatible with the present formalism: either (i) Ic (x) = 0 designates entities
not presented at all in context c (outside the lived field), or (ii) it designates entities presented
so weakly that they are functionally negligible for the purposes at hand. Which interpretation
is appropriate can be fixed later when Xc and the mechanisms generating Ic are specified more
concretely.

Remark 204 (Intuition and examples for focus/fringe thresholding). The threshold τI is a prag-
matic bridge between graded phenomenology and discrete computation. For instance, a system may
allocate symbolic reasoning only to elements in Focusc (τI ) while allowing statistical/background
processes to operate on Fringec (τI ). Different tasks warrant different thresholds; this is one reason
Hyperseed keeps thresholding explicit rather than implicit.
    The definition is useful because many later constructions (graphs of salient entities, resource
budgets, bounded planning) require finite or crisp sets even when the underlying salience is contin-
uous. This is a standard move in cognitive architectures [19].

    In practice, one may treat τI as a tunable interface parameter between phenomenology and
computation. A high threshold yields a narrow “spotlight” that supports fast, low-branching
deliberation; a lower threshold yields a broad set that supports integrative or exploratory processing
at the cost of increased combinatorics. Because τI is explicit, the theory can later describe adaptive

                                                  115
policies (e.g., lowering τI under uncertainty, raising it under time pressure) without changing the
                                                                               (1)     (2)
underlying meaning of Ic . One can also define multiple thresholds (e.g., τI > τI ) to obtain
layered bands of salience, but the single-threshold version already captures the minimal coarse-
graining needed for many constructions.
    Finally, although the present definitions are pointwise, they are compatible with temporal re-
finements. If contexts are indexed by time (or contain a time parameter), then c and c0 at nearby
moments may induce fields Ic and Ic0 whose changes describe shifts of lived salience. Later dynam-
ical models can then constrain the rate or cost of such shifts (e.g., inertia in salience, hysteresis
under fatigue) while preserving the basic primitive notion introduced here.

6.6     Abstract and concrete
Hyperseed distinguishes abstract experiences (e.g. the number 17) from concrete experiences (e.g.
kicking a brick), while emphasizing that the same “content” may sometimes be experienced with
more concreteness under unusual states. For a rigorous ontology, we need a notion of abstract-
ness/concreteness that is: (i) context-relative, (ii) compatible with graded intensity, and (iii) com-
patible with the weakness/simplicity formalism. In particular, “abstract vs. concrete” here is not
treated as a property of an isolated symbol or proposition, but as a property of how some col-
lection of experienced tokens is organized within a context (what distinctions the context makes
salient, which equivalences it tolerates, and which discriminations it refuses to carry out). This
is why the definitions below are phrased in terms of maps out of Xc , rather than in terms of an
intrinsic “abstractness score” assigned to a content in isolation. The graded aspect (ii) will be
represented indirectly: one can move along chains in the abstraction preorder, or consider degrees
of refinement/coarsening, rather than requiring a single scalar that must fit every use-case.
Remark 205. This section’s definitions deliberately echo a long-standing mathematical habit: ab-
straction is quotienting. To abstract is to identify; to concretize is to refuse identification unless
constraints are satisfied. The point is not to reduce phenomenology to set theory, but to give a
clean interface between lived categories (abstract/concrete) and later formal tools (weakness, effort,
compression). See Hyperseed-Concept 51 and Hyperseed-Concept 83. A practical reading is: an
“abstract experience” is one in which many token-level variations are treated as irrelevant (and
therefore collapsed), whereas a “concrete experience” is one in which the system maintains, attends
to, or is compelled by distinctions among tokens that might otherwise be quotiented away. On this
view, unusual states can make the same nominal content feel more concrete by effectively refining
the relevant context c (enlarging Xc and/or making finer discriminations available), so that fewer
identifications are tolerated without experiential “error” or friction.

6.6.1    Abstraction as quotienting of distinctions
Definition 51 (Abstraction as a quotient). Let c be a context with entity set Xc . An abstraction
of c is a surjection
                                          q : Xc  A
to a set of abstracta A. The abstraction collapses distinctions by identifying elements of the same
fiber. Equivalently, q determines an equivalence relation
                                    x ∼q y   ⇐⇒        q(x) = q(y).
In this sense, the abstractum a ∈ A can be read as the “type” corresponding to the entire equivalence
class q −1 (a) ⊆ Xc of concrete tokens that are treated as interchangeable for the purposes of the
context.

                                                 116
Remark 206 (Intuition and examples for abstraction-as-quotient). The surjection q : Xc  A
says: “many concrete tokens map to one abstract type.” For example, take Xc as handwritten
glyphs and let A be the set of letters; then q sends each glyph to the letter it instantiates, collapsing
distinctions among different handwriting styles. Or let Xc be physical trajectories of balls and let
A be a coarse state descriptor (position rounded to a grid), collapsing micro-differences.
    This definition is useful because it expresses “collapsing distinctions” in a way that composes:
two abstractions can factor through one another, and the induced equivalence relations can be or-
dered. It connects directly to weakness: collapsing more distinctions increases undistinguished pairs,
hence increases weakness in the sense used elsewhere [3, 2] (Hyperseed-Concept ?? and Hyperseed-
Concept 202). One can also read q as a formalization of an invariance: the map forgets differences
along directions the context treats as irrelevant. In the glyph example, stylistic variation (stroke
thickness, slant) becomes an “ignored degree of freedom,” while in the trajectory example, micro-
physical perturbations become ignorable, leaving only a coarse descriptor. This aligns with the phe-
nomenological claim that abstraction often feels like “stability under variation”: what is preserved
by q is what the experience treats as the same.

Definition 52 (Abstraction preorder). Given abstractions qi : Xc  Ai , define

                           q1  q2   ⇐⇒      ∃ r : A1 → A2 with q2 = r ◦ q1 .

Thus q2 is at least as abstract as q1 when it factors through q1 (i.e. collapses at least as many
distinctions). Equivalently, q1  q2 means that every q1 -fiber is contained in a q2 -fiber, so the
partition of Xc induced by q2 is a coarsening of the partition induced by q1 .

Remark 207 (Intuition and examples for the abstraction preorder). The preorder  formalizes
“is no less abstract than.” If q2 = r ◦ q1 , then whatever identifications q1 makes, q2 makes them as
well (and possibly more). For instance, in image recognition one might first quotient by viewpoint
to get object identity (q1 ), and then quotient object identities by category to get “animal vs. vehicle”
(q2 ). Then q1  q2 because category forgets more.
     This is useful because it gives a rigorous notion of abstraction order without requiring a nu-
meric scale. Later, when we attach cost/effort to abstraction, the preorder provides the qualitative
backbone for those quantitative refinements. It is also useful that  is only a preorder: two different
surjections can induce the same equivalence relation (e.g. via different codomains Ai that merely
relabel classes), so antisymmetry need not hold at the level of functions even when the induced
partitions are identical. If desired, one can pass to equivalence classes of abstractions under mutual
factorization, yielding a partial order isomorphic to the lattice of partitions (or equivalently, of
equivalence relations) on Xc . This observation is conceptually helpful later when “graded concrete-
ness” is implemented by moving between finer and coarser partitions, rather than by changing the
underlying set of tokens.

Proposition 4 (Abstraction increases weakness). Assume a context c supplies an “undistinguished
pairs” relation Hc ⊆ Xc × Xc . If q1  q2 are abstractions and Hqi denotes the induced relation that
treats all ∼qi -equivalent pairs as undistinguished, then

                             Hq1 ⊆ Hq2        =⇒         w(Hq1 ) ≤ w(Hq2 ).

Remark 208 (What the proposition says, and why it matters). This proposition states that “more
abstraction” (in the sense of identifying more things) produces “more weakness” (in the sense of
leaving more pairs undistinguished), provided the induced undistinguished-pairs sets are nested.


                                                   117
Intuitively, if you agree to treat more pairs as the same, you have deliberately declined to make
distinctions; weakness is designed to increase exactly in that situation [3, 2].
    The result connects this section’s abstract/concrete interface to Section 4, where monotonic-
ity properties justify interpreting w(H) as a coherent weakness measure. Here we see a concrete
instantiation: quotienting creates inclusion of undistinguished-pair sets, and monotonicity of weak-
ness carries the inclusion to an inequality. Phenomenologically, this captures a common pattern: as
an experience becomes more abstract, it becomes “easier to satisfy” because fewer discriminations
are demanded; conversely, concrete experience imposes more specific constraints (more opportuni-
ties for mismatch), which corresponds to fewer undistinguished pairs and hence lower weakness.
Note that the antecedent Hq1 ⊆ Hq2 is presented explicitly to keep the statement modular: in some
formalisms Hqi may include both the base relation Hc and the identifications induced by qi , and the
inclusion condition is then the clean hypothesis under which monotonicity of w(·) applies without
committing to a particular construction of Hqi .

Proof. The factorization condition q1  q2 implies that ∼q2 is coarser than ∼q1 , hence any pair
identified by q1 is also identified by q2 , giving Hq1 ⊆ Hq2 . The conclusion then follows from
Theorem 1. More explicitly: if x ∼q1 y then q1 (x) = q1 (y), so q2 (x) = r(q1 (x)) = r(q1 (y)) =
q2 (y), hence x ∼q2 y; therefore every ∼q1 -identified pair is also ∼q2 -identified, which is exactly the
coarsening relationship needed to apply monotonicity of w to the induced undistinguished-pairs
relations.

Remark 209 (Concretization as refinement (informal)). Although the formal development here is
phrased in terms of abstraction maps q : Xc  A, the opposite motion—toward concreteness—can
be read as moving to a finer quotient (i.e. reversing ), or equivalently as refining the induced
partition of Xc so that fewer tokens are treated as interchangeable. In this sense, “concretizing”
does not require introducing a new primitive beyond the preorder: it can be modeled as selecting
an abstraction q 0 with q 0  q replaced by q  q 0 failing, i.e. by choosing q 0 that distinguishes more.
This dovetails with graded intensity (ii): to become “more concrete” is not necessarily to jump
categories, but to traverse a chain of refinements, each step adding discriminations that the context
now treats as salient.

Remark 210 (Proof sketch and commentary). Proof sketch. Factorization means that q2 cannot
distinguish anything that q1 already identifies, so the equivalence classes (fibers) of q2 are unions
of fibers of q1 . Equivalently, every identification made by q1 is preserved by q2 , because q2 only
has access to information that already passed through q1 . Hence the set of pairs declared equivalent
by q1 is contained in the set declared equivalent by q2 . In other words, ∼q2 is at least as coarse
as ∼q1 : it can collapse further, but it cannot “un-collapse” any pair that q1 has already merged.
Weakness is monotone under adding undistinguished pairs, so the inclusion yields the inequality.
This monotonicity can be read operationally: if a quotient is allowed to forget more distinctions
(i.e. it identifies more pairs), then it can only become weaker in the sense of losing discriminative
or task-relevant structure.                                                                        
     The key step is the passage from q2 = r ◦ q1 to “∼q2 is coarser than ∼q1 .” This is simply the
observation that if q1 (x) = q1 (y) then automatically q2 (x) = r(q1 (x)) = r(q1 (y)) = q2 (y). It is
sometimes helpful to rephrase this in terms of kernels: the relation ∼q is the kernel congruence of
q, and composition enlarges kernels, i.e. ker(q1 ) ⊆ ker(r ◦ q1 ). Geometrically, quotienting can be
pictured as merging points into blobs; factoring corresponds to merging blobs into larger blobs, so
the set of merged pairs can only grow. One can also view the map r as defining a partition of the
q1 -blobs, after which q2 assigns the same label to all blobs in each part of that partition.



                                                   118
6.6.2   Concreteness as resistance to quotienting
The previous definitions make “more abstract” precise as “collapses more distinctions.” In partic-
ular, abstraction is measured by how large a family of potentially different entities is treated as
interchangeable once mapped through q. To model concreteness we add a complementary notion:
some entities resist being safely quotiented away. Here “resist” is not metaphysical stubbornness
but a contextual fact: in some practices, merging certain items produces errors, surprises, or loss
of control. We represent this as a context-indexed constraint on admissible abstractions. The role
of the context index c is to keep track of which invariances are acceptable: the same physical entity
may be concrete for one task and abstract for another.
Definition 53 (Concreteness constraint). Let c be a context. A concreteness constraint is a pred-
icate Kc on abstractions q : Xc  A specifying which quotientings count as “benign”. The point
of treating Kc as a predicate (rather than a single privileged quotient) is that there may be many
acceptable ways to abstract, and concreteness is meant to be robust across that admissible family.
An entity x ∈ Xc is concrete (relative to c) if, for every admissible abstraction q in the sense of Kc ,
the fiber q −1 (q(x)) is “small” (i.e. x is not merged with many other entities without violating Kc ).
Here “small” is intentionally left schematic: depending on the application it may mean small car-
dinality, small measure, bounded diameter under a similarity metric, or small expected variability
in downstream predictions. Conversely, x is abstract if there exist admissible abstractions under
which x represents a large equivalence class. This existential clause captures the idea that an entity
can function as a representative or type when the context licenses aggressive identification, even if
other contexts would forbid it.
Remark 211 (Intuition and examples for concreteness constraints). A concreteness constraint Kc
encodes what a context will not allow itself to forget. Equivalently, Kc expresses which distinctions
are treated as non-negotiable because collapsing them would damage some capability the context aims
to preserve. For a robotic context, Kc might forbid quotienting that breaks sensorimotor prediction:
two objects cannot be identified if pushing one produces different outcomes than pushing the other.
More generally, any abstraction that would destroy controllability or introduce systematic prediction
error would be deemed non-benign. For a mathematical context, Kc might be looser: many concrete
instances can be safely quotiented into a single abstract structure if all proofs and computations of
interest are invariant under that quotient. For example, different presentations of the same group
may be quotiented together when the task concerns only group-theoretic properties, but not when the
task concerns a specific representation or algorithmic cost.
    This definition is useful because it prevents a degenerate triviality: without constraints, maxi-
mal abstraction is always possible. Indeed, the quotient map that sends all of Xc to a single point
is always available set-theoretically, but it is rarely benign relative to any nontrivial practice. By
making admissibility explicit, we keep the abstract/concrete distinction tethered to practice and
consequence. Later sections can propose specific quantitative forms of Kc based on effort or predic-
tive utility, connecting to Hyperseed-Concept 100 and Hyperseed-Concept ??. One can anticipate,
for instance, that Kc (q) might require that some loss functional (prediction loss, control loss, or
explanation loss) remain below a context-dependent threshold.
Remark 212 (Why a constraint is necessary). If we allowed arbitrary quotient maps, every entity
could be collapsed into a single point, making everything maximally abstract. This would trivialize
any attempt to compare abstractions, because there would always exist a strictly coarser quotient that
“wins” by collapsing more. Hyperseed’s distinction between abstract and concrete presupposes that
not all quotientings are experienced as legitimate. The predicate Kc stands in for whatever makes
a quotient “valid” in a context: sensorimotor coupling, causal consequences, pragmatic stakes, or

                                                  119
other constraints. In practice, Kc can be thought of as delimiting a feasible set of compressions:
compressions outside this set are experienced as errors, category mistakes, or harmful oversimplifi-
cations. Later sections will propose quantitative candidates for Kc in terms of effort and predictive
utility.

6.7    Non-duality as a bridge between perspectives
Hyperseed treats non-duality as primitive and also as an organizing constraint relating (at least)
first-person and third-person framings. We record one clean mathematical way to express “non-
duality without collapse” using the language of context translation. In particular, the aim is to
state a condition that is strong enough to prevent a translation from trivializing distinctions, while
still weak enough to permit genuine coarse-graining and abstraction (as is unavoidable when moving
between descriptive standpoints).
Remark 213. In philosophical terms, this is a proposal to treat “bridging perspectives” as a problem
in approximate structure-preservation rather than exact identity. One does not demand that first-
person and third-person descriptions coincide; one asks instead for translations that preserve what
must be preserved, blur what may be blurred, and make the extent of blurring legible as a parameter.
This resonates with process-oriented and sign-oriented metaphysics (Whitehead and Peirce) in which
relations and mediations are primary [15, 14]. It also anticipates later Hyperseed themes of mind–
world correspondence and self/other boundaries (Hyperseed-Concept 112 and Hyperseed-Concept
165). A further motivation is methodological: if one treats “first-person” and “third-person” as two
contexts with different observational capacities, then any realistic bridge must allow information
loss in at least one direction, yet should still provide an auditable account of what was preserved
and what was sacrificed.
Definition 54 (Context translation and non-dual compatibility). Let c, d be contexts. A translation
from c to d is a function T : Xc → Xd . We say that T is non-dually compatible with c and d if
for all x, y ∈ Xc we have
                                                                             
                        δc (x, y) ≤ δd T x, T y   and δc (x, y) ≤ δd T y, T x

(componentwise order on V), i.e. d does not erase distinctions that are strong in c. Dually, a
translation S : Xd → Xc is compatible if it does not create spurious distinctions.
    A non-dual bridge between c and d is a pair of translations (T, S) together with a witness that
the composites S ◦ T and T ◦ S act like identities only up to controlled weakness (to be made precise
using the quantale V and weakness ordering).
    One may read the compatibility inequalities as a minimal “no-forgetting” requirement: if δc (x, y)
certifies that x and y are distinguishable in context c (in whichever multivalued sense V encodes),
then translating to d should not make them less distinguishable. Because V is ordered componen-
twise, each component of δ (e.g. evidential strength, salience, modality-specific discriminability)
is protected separately; thus a translation is allowed to blur some components only insofar as the
order relation permits, and any such blurring is tracked at the level of V rather than hidden in
informal interpretation.
Remark 214 (Intuition and examples for translations and bridges). A translation T : Xc → Xd is a
recipe for re-expressing what c can talk about in the language of d. Non-dual compatibility demands
that if c has strong evidence that x and y diverge, then d must not flatten that divergence after
translation. In other words, T must not turn strong distinctions into weak ones. The symmetric-
looking condition with (T x, T y) and (T y, T x) ensures this protection of distinction in both directions,

                                                   120
matching the earlier emphasis on mutuality for distinctions. A useful way to think about this is that
even when δ is not literally symmetric (e.g. if it encodes directional evidential flow, or asymmetric
accessibility), the bridge should not depend on an arbitrary choice of ordering of the pair (x, y) when
deciding whether a distinction has been preserved.
    A simple example is mapping a fine-grained introspective context (many subtle feelings) into a
coarse behavioral context (few categories). A compatible translation cannot claim two feelings are
indistinct if, in the introspective context, the evidence for their distinctness is high. The notion
of a non-dual bridge then says: even if round-tripping x 7→ T x 7→ S(T x) does not return exactly
x, it returns something that is “the same up to controlled weakness,” making the loss of detail
explicit and measurable via weakness. This is the formal analogue of “non-duality without collapse”
(Hyperseed-Concept 121 and Hyperseed-Concept 143; see also [3]).
    A second example (closer to scientific practice) is translating from a richly parameterized dynam-
ical model to a low-dimensional summary statistic used for prediction or control. The translation to
the summary statistic is permitted to discard degrees of freedom, but it should not erase a distinc-
tion that the original model treats as robust. Conversely, the translation back from the statistic to a
representative dynamical state should not hallucinate fine distinctions unsupported by the statistic,
i.e. it should not “over-interpret” the coarse description as if it contained more information than
it does.
    In both examples, the “witness” for the bridge can be understood as a formal certificate of how
far S ◦ T and T ◦ S deviate from identity in the weakness order. Concretely (at an intuitive level),
one expects such a witness to amount to inequalities of the form “x is close to S(T x) up to an
allowed weakening” and likewise “u is close to T (Su) up to an allowed weakening,” where “close”
is expressed using δ and the allowed weakening is expressed using the quantale structure on V .
Thus, the bridge does not pretend that translations are invertible; it instead makes non-invertibility
quantitative and therefore discussable.

Remark 215. The point of this definition is not to force an equivalence between first-person and
third-person descriptions. Rather, it provides a formal knob: a bridge can preserve some distinctions
while allowing others to blur, and non-dual states are those where the blurring is substantial but non-
trivial structure remains. This prepares the ground for later sections where self/other boundaries,
intentionality, and “mind–world correspondence” are modeled as approximate morphisms rather
than strict identities. In particular, the framework makes room for the possibility that different
contexts are related by many admissible bridges, not a unique privileged one; the choice of bridge
can then be treated as part of the modeling assumptions, and the witness explicitly records the cost of
that choice in terms of weakness. This is one way to reconcile the phenomenological insistence that
perspectives are irreducible with the scientific insistence that perspectives can nonetheless constrain
one another.


7    Order, time, and becoming
Outline
• Formalize after/before as strict partial orders (and graded/paraconsistent refinements).

• Define proto-time as “time before physics-time”: any experienced partial order.

• Define linear time axes as serializations/quotients/approximations of proto-time.

• Define becoming as boundary non-duality between successive occasions/entities.


                                                 121
• Give a paraconsistent, quantale-valued event calculus as a canonical “time reasoning” layer.

• Define event regularity predicates: persistent, continuous, increasing, decreasing, via time-context
  similarity.

Summary and Hyperseed concepts covered
Hyperseed treats time as built from ordering. The most primitive ingredient is an experienced
after/before relation, i.e. a family of asymmetric distinctions whose transitive closure yields a
(strict) partial order. Any such partial order is a proto-time. A linear time axis is a special case
(or approximation) that serializes events; this can lose information when concurrency or branching
is present.
    The section then connects this ordering-first viewpoint to concrete temporal reasoning for-
malisms. We define a paraconsistent, quantale-valued event calculus in which predicates such as
Happens and HoldsAt take values in the p-bit quantale V from the formal core. Finally, we formalize
Hyperseed’s qualitative temporal predicates (persistence, continuity, increasingness, decreasingness)
using a notion of time-context and temporal similarity.

Hyperseed concepts covered.

• After / Before; A < B implies NOT(B < A); NOT(A < A); transitivity.

• Proto-Time; linear time axis (serialization); “information loss under linearization”.

• Becoming (boundary non-duality / non-dual variety).

• Event and process calculi; events; fluents; holds/initiate/terminate; “holds sometime in”.

• Persistent / continuous / increasing / decreasing (events or fluents).

• Time context; temporal similarity.

Remark 216 (Orientation and sources). The present formalization is an intentionally austere
extraction of the “ordering-first” stance on temporality used throughout the Hyperseed ontology [1].
The guiding thought is Russellian in its analytic economy: if we can explain “before/after” without
presupposing a global time coordinate, we obtain a foundation that can accommodate branching,
concurrency, subjective ordering, and inconsistent evidence. At the same time, the section keeps
open a Whiteheadian reading in which temporal structure is a derived regularity of processes rather
than a primitive container [15].

    The key methodological move is to treat “temporal talk” as downstream of a more basic relation
of order. Concretely, an agent (or a theory) may register multiple local discriminations of the form
“A is after B” without thereby committing to a single global clock or even to a total ordering. The
strictness assumptions in the bullet list can be read as idealizations: irreflexivity NOT(A < A) and
asymmetry A < B ⇒ NOT(B < A) express that “after” is not meant as mere difference, while
transitivity captures the compounding of experienced precedence. In practice, the motivating data
may be fragmentary, cyclic, or in tension (e.g. multiple observers, noisy sensors, retrospective
reconstruction), which is why the section explicitly anticipates graded/paraconsistent refinements
rather than insisting on classical consistency from the start.
    Calling any such partial order a proto-time is meant to separate two notions that are often
conflated: (i) having an ordering at all, and (ii) having a privileged metric parameter with uniform


                                                 122
units. Proto-time in this sense is compatible with incomparability (neither A < B nor B < A),
which operationally corresponds to concurrency, causal independence, or simply missing evidence.
It is also compatible with branching structures, where a single event is before two mutually in-
comparable events, capturing divergent possible continuations or genuinely parallel processes. This
emphasizes that proto-time is not merely “early physics” but rather “pre-metric order”—a notion
that can appear in phenomenology, computation traces, causal graphs, and narrative accounts.
    The phrase “linear time axis” is then treated as an additional construction on top of proto-time.
A serialization can be understood as selecting (or synthesizing) a total order that is consistent with
(some portion of) the partial order, for example by choosing a linear extension when one exists,
or by imposing tie-breaking conventions when it does not. A quotient/approximation perspective
is also useful: if many events are only distinguishable up to simultaneity or resolution limits, one
may collapse equivalence classes and order the classes instead. Either way, “information loss under
linearization” is not merely a philosophical slogan: incomparabilities and branching structure can
be erased when represented on a single axis, so that distinct proto-times may project to the same
linearized representation.
    The concept of becoming is positioned as a bridge between ordering and ontology: if we speak
of successive occasions/entities, the boundary between them is not treated as a hard cut but as a
non-dual interface in which “earlier” and “later” partially interpenetrate. In this framing, becoming
is not an extra event occurring in time; rather, it is the structural relation that makes a succession
intelligible as a succession of occasions at all. This is why becoming is stated as “boundary non-
duality”: it names the continuity of inheritance/transition even when the order relation itself is
strict.
    Finally, the event-calculus layer is introduced as a disciplined way to reason with proto-time
when evidence is inconsistent or graded. Interpreting Happens(e, t) and HoldsAt(f, t) as V -valued
predicates allows the theory to track not only whether an event happens or a fluent holds, but to
what extent and under what kind of logical status in p-bit. In particular, the quantale structure
supports aggregating temporal evidence (via its join/meet structure) and sequencing/composition
of supports (via its monoidal operation), which is essential when temporal claims are derived from
multiple partial observations. On this basis, regularity notions such as persistence and continuity
can be cast as constraints over families of contexts: a fluent is persistent when its V -valuation
remains stable across sufficiently similar neighboring contexts, continuous when changes are small
relative to a similarity threshold, and increasing/decreasing when there is a directional trend relative
to the proto-time order. The explicit use of time-context and temporal similarity is meant to keep
these predicates qualitative and robust, so that they remain meaningful even when no globally
consistent linear clock is available.

7.1    After/before as strict partial order
Hyperseed’s first move is to treat time as a special case of ordering. Mathematically, the minimal
clean object capturing this is a strict partial order. This choice deliberately separates the direction
of precedence from any further commitments about metric structure (how long something takes),
topology (continuity), or global synchrony (a single shared clock). In particular, it keeps open
whether time is discrete or continuous, whether it branches, and whether every pair of events
admits comparison.

Definition 55 (Strict partial order). A strict partial order on a set T is a binary relation < on T
such that:

1. (Irreflexive) for all t ∈ T , not(t < t),

                                                  123
2. (Transitive) for all t1 , t2 , t3 ∈ T , if t1 < t2 and t2 < t3 then t1 < t3 .
We say t1 is before t2 if t1 < t2 , and t2 is after t1 .
    It is often convenient (and conceptually clarifying) to note that a strict order < canonically
induces a non-strict companion relation ≤ by defining t1 ≤ t2 to mean “t1 < t2 or t1 = t2 .” This
does not add structure; it simply packages the option of equality explicitly. Conversely, starting
from a reflexive partial order ≤, one recovers a strict version by setting t1 < t2 iff t1 ≤ t2 and
t1 6= t2 . This standard conversion is useful later when one wants to talk about “no later than”
versus “strictly earlier” without changing the underlying conceptual commitments.
Remark 217 (Intuition, examples, and why this matters). The relation < is meant to capture only
the irreducible directional fact “this precedes that,” not necessarily measured duration. Irreflexivity
forbids loops of the form “an event is before itself,” and transitivity enforces that “before” composes:
if t1 is before t2 and t2 before t3 , then t1 must be before t3 . Together these clauses prevent directed
cycles, so the order can be read as an acyclic dependency structure (a “can-happen-before” relation).
     Two standard examples are: (i) T = N with the usual <; (ii) T = P(S) for a set S with A < B
defined as A ( B (strict inclusion). In the temporal reading, the second example is suggestive:
temporal precedence can behave like a refinement relation on information states. This strict-partial-
order abstraction is useful because it is the weakest structure that still lets us speak rigorously about
“past” and “future” without assuming that every pair of events is comparable. This aligns directly
with the Hyperseed notions After and Before (Hyperseed-Concepts 52 and 63).
     One can also visualize a strict partial order as a directed graph whose vertices are elements of T
and whose edges indicate immediate precedence; transitivity then says that reachability agrees with
<. In the finite case, a Hasse-style picture (showing only “cover” relations and omitting transitive
edges) makes the distinction between a chain (a totally ordered subset) and an antichain (a set of
pairwise incomparable elements) explicit. In temporal terms, a chain reads as a history-like thread
of definite succession, while an antichain reads as a simultaneous (or mutually unrelated) slice at
the resolution being modeled.
     A further reason this matters is that many familiar time models implicitly assume total order,
i.e. for all distinct t1 , t2 one has either t1 < t2 or t2 < t1 . A strict partial order drops exactly that
assumption. Thus it can represent branching futures, merging causal lines, and observer-dependent
coarse-grainings where the model refuses to invent an arbitrary order when the underlying situation
does not warrant one.
Remark 218 (Hyperseed’s asymmetry axiom). For strict partial orders, the Hyperseed clause
“A < B implies NOT(B < A)” follows from irreflexivity and transitivity: if A < B and B < A
then transitivity yields A < A, contradicting irreflexivity.
    It is worth emphasizing that this derivation uses only the internal logic of the relation <: the
contradiction is not empirical but formal. In particular, the step “A < B and B < A implies
A < A” is exactly the closure property transitivity provides, so asymmetry is not an additional
stipulation about time; it is a structural fact about any relation intended to behave like strict
precedence.
Remark 219 (Intuition: why asymmetry is not a separate axiom). One sometimes writes “asym-
metric” as a separate requirement for a strict order, but it is already latent in the two clauses given.
Philosophically, this is a small instance of a broader pattern in foundational work: what appears at
first as an additional metaphysical constraint can often be seen as a theorem of a simpler algebra
of relations. Here, the prohibition of self-precedence and the compositionality of precedence suffice.

                                                     124
    Another way to say the same thing is that strict partial orders are precisely those relations
whose “before” arrows cannot be followed around a directed cycle. If a theory of time wants to
allow closed timelike curves or other forms of cyclic dependence, then it is not (in that region)
a strict partial order; one would need a different primitive. Hyperseed’s choice here therefore
commits to acyclicity at the level of the basic After/Before relation, while leaving open many other
possibilities (density, branching, finiteness, etc.).

Remark 220 (Incomparability and concurrency). If neither t1 < t2 nor t2 < t1 holds, then t1 and
t2 are incomparable. In the time interpretation, incomparability represents concurrency, branching,
or the absence of a well-defined ordering relation at the observer’s grain.

   Given any t ∈ T , the strict order also induces the associated “past” and “future” sets

                     Past(t) = {s ∈ T : s < t},      Future(t) = {u ∈ T : t < u}.

These are purely order-theoretic constructions (no metric required). Incomparability between t1
and t2 can then be read as the failure of inclusion between their past/future profiles: neither event
lies in the other’s future, so the order records no precedence constraint between them. This gives
a precise sense in which partial ordering supports talk of “past” and “future” locally, even when a
global linear timeline is unavailable.

Remark 221 (Example: concurrency as a mathematical primitive). In a distributed system, two
messages may be causally unrelated: neither is provably earlier. A strict partial order captures this
directly by leaving the pair incomparable, rather than forcing a spurious choice. This is precisely
the sort of “information-preserving humility” that is lost when one insists prematurely on linear
time.

    In such settings, it is common to distinguish the causal order (the strict partial order that
must be respected) from any schedule or linearization that totally orders events for execution or
narration purposes. Mathematically, a schedule is a total order that extends the partial order:
whenever t1 < t2 causally, the schedule also places t1 before t2 . The key point is that many
different extensions may exist, and their differences correspond exactly to choices made among
incomparable events. Hyperseed’s use of strict partial orders therefore cleanly separates what is
forced by After/Before from what is merely conventional or perspective-dependent.

7.2   Proto-time as observer-relative ordering
Hyperseed’s term proto-time refers to “every partial ordering considered as a sort of time”. This can
be taken literally. In particular, the proposal is that the minimal formal residue of “temporal” talk
is not duration or a privileged coordinate, but an ordering relation that can support the distinctions
“earlier than”, “later than”, and “not (yet) comparable at the present resolution”. The emphasis
on partial (rather than total) order is crucial: it allows the formalism to treat indeterminacy,
concurrency, and limited access as first-class rather than as defects to be repaired.

Definition 56 (Proto-time). A proto-time is a pair (T, <) where T is a set of temporal indices
(e.g. occasions, events, or representations of them) and < is a strict partial order on T . In other
words, < is irreflexive (¬(t < t) for all t ∈ T ) and transitive (if t1 < t2 and t2 < t3 then t1 < t3 );
antisymmetry is automatic for a strict order in the sense that cycles are excluded by transitivity
and irreflexivity.



                                                  125
Remark 222 (Intuition and connection to experience). Proto-time is time “before clocks”: any
experienced ordering of episodes, perceptions, or internal updates qualifies, regardless of whether
it resembles a line. The set T is deliberately generic: it may be a set of occasions (Hyperseed-
Concept 124), a set of events in an event calculus, or a set of internal representational states.
The only essential ingredient is the precedence relation <, which records whatever the system takes
to be “after” and “before” at its current resolution. The point of using a strict order is that it
matches the phenomenological asymmetry of “before/after” without forcing an identity criterion
for simultaneous or indistinguishable episodes; where equality or “same time” is needed, it can be
supplied separately (e.g. via an equivalence relation or by quotienting), rather than being silently
baked into the time structure. Likewise, incomparability (¬(t1 < t2 ) and ¬(t2 < t1 )) need not mean
“simultaneous” in any physical sense: it can mean “no ordering information available”, “different
narrative threads”, or “the system declines to commit”.
    A simple example is a causal DAG whose vertices are events and whose edges represent di-
rect causal influence; the reachability relation induces a strict partial order. This illustrates how
proto-time can be extracted from constraints rather than posited as an ambient parameter: causa-
tion (or influence) supplies the arrows, and time is the induced ordering. Another example is the
“edit history” of a document with branching: commits form a partially ordered set under ancestor
relation. These are proto-times in exactly the present sense, and they make vivid why a linear
axis is often a lossy summary rather than the primitive. In both examples, a linear “timeline” can
be recovered only by adding choices (e.g. selecting a linear extension, choosing a topological sort,
or imposing additional tie-breaking conventions), and different choices may be equally compatible
with the underlying proto-time. This definition operationalizes the Hyperseed notion Proto-Time
(Hyperseed-Concept 142).

Remark 223 (Proto-time is local and aspectual). Different contexts/aspects (in Hyperseed’s sense)
may carry different proto-times. For instance, the same collection of occasions may admit a fine-
grained causal proto-time and a coarser narrative proto-time, or multiple incompatible orderings
inferred from different evidence. This is one of the places where paraconsistency is not an af-
terthought but a design requirement. Concretely, a system may maintain one ordering for senso-
rimotor updating, another for autobiographical memory, and yet another for planning, even when
these do not admit a single common refinement without introducing contradictions or arbitrarily
discarding constraints. The locality claim can also be read computationally: proto-time is indexed
by what is tracked and what is ignored, so changing resolution (e.g. by coarse-graining episodes into
“chunks”) can change T and thereby change which order-relations are expressible at all. In that
sense, proto-time functions as an aspectual interface: it describes the temporal commitments of an
aspect, not an absolute inventory of “all events”.

Remark 224 (Why “observer-relative” is not a concession but a method). To say proto-time is
context-indexed is not to deny a mind-independent world; it is to keep separate (i) the structure
realized by whatever generates events and (ii) the structure inferred or imposed by a bounded system
attempting to navigate them. Hyperseed repeatedly exploits this separation later when relating time
to effort-minimization and “least-effort paths” in inference or control [21]. The methodological pay-
off is that one can ask two different questions without conflating them: “What ordering constraints
does the world impose?” versus “Which ordering constraints does this agent (or aspect) represent,
and how costly is it to refine them?”. On this view, observer-relativity is not a relativism about
reality, but an explicit accounting of representation: a proto-time is the agent’s current ordering
model, which may be revised as evidence arrives, resources change, or goals shift. It also clarifies
why proto-time does not presuppose a metric, a topology, or a global “now”: those are additional


                                                126
structures that may be constructed when useful, but the base concept remains the ordering relation
that supports predictions, explanations, and control.

7.3    Graded and paraconsistent temporal ordering
Hyperseed also gestures at graded orderings (“how long or fast the flow feels”). A simple rigorous
way to do this within the formal core is to treat “before” as a p-bit-valued relation whose positive
component records support for “t1 is before t2 ” and whose negative component records support
against it. One can view this as replacing a single Boolean-valued edge in a temporal graph by a pair
of weights: a pro-weight and a con-weight, both of which may be nonzero. The point is not merely
to allow uncertainty (low support in both channels), but also to allow tension (simultaneously high
support and high counter-support) without collapsing into triviality.
Definition 57 (p-bit-valued before-relation). Let V = [0, 1]2 be the p-bit quantale from Section 3.4.
A p-bit-valued temporal evidence relation is a map

                        B : T × T → V,           B(t1 , t2 ) = (B + (t1 , t2 ), B − (t1 , t2 )).

Here B + (t1 , t2 ) is positive evidence for t1 < t2 , and B − (t1 , t2 ) is negative evidence.
Remark 225 (Order and entailment on V ). Since V is used as a codomain for evidential values,
inequalities such as B(t1 , t3 ) ≥ B(t1 , t2 ) ⊗ B(t2 , t3 ) presuppose a comparison relation on pairs. In
the basic p-bit setup, one typically orders V = [0, 1]2 componentwise:

                           (v + , v − ) ≤ (w+ , w− )   iff   v + ≤ w+ and v − ≤ w− .

Under this reading, “≥” means “has at least as much positive evidence and at least as much negative
evidence.” This is deliberately not a reduction to a single net score: increasing v − does not auto-
matically decrease v + , so the structure can represent both evidential accumulation and evidential
conflict as first-class phenomena rather than as noise to be normalized away.
Remark 226 (Notation unpacking). The symbol V = [0, 1]2 denotes ordered pairs (v + , v − ) of reals
in [0, 1]. We read v + as “support for” and v − as “support against” a proposition. Thus B + (t1 , t2 )
and B − (t1 , t2 ) are simply the two coordinate functions of B. This two-channel semantics is one
concrete paraconsistent option; related four-valued approaches appear in constructible duality logics
[23], and the use of such values as composable evidence is aligned with the general “paraconsistent
resonance” perspective [24]. A convenient mnemonic is that (1, 0) behaves like “confidently yes,”
(0, 1) like “confidently no,” (0, 0) like “no information,” and (1, 1) like “inconsistent but fully
activated,” with intermediate points capturing graded mixtures of these modes.
Remark 227 (Intuition, examples, and purpose). A crisp order says either “t1 < t2 ” or not; the
p-bit-valued relation says how strongly the system leans in each direction, and allows it to record
conflict explicitly. For example, a system may have sensory evidence suggesting that a stimulus
s1 preceded s2 (high B + ), while a higher-level narrative model suggests the opposite (high B − ). A
single classical truth value would force premature resolution; the p-bit pair preserves both pressures
so that later inference (e.g. transitive closure, inertia reasoning) can integrate them. In particular,
the representation supports at least three qualitatively different cases that a single probability-like
scalar conflates: (i) uncertain (both channels near 0), (ii) confident (one channel high, the other
low), and (iii) contested (both channels high).
    This graded form is useful because it connects time to the same algebra used for distinction,
weakness, and compositional aggregation elsewhere in the document [3]. In other words, temporal

                                                        127
uncertainty is not treated as an exceptional problem requiring a separate probabilistic apparatus; it
is folded into the same quantale-enriched calculus. From a modeling standpoint, this uniformity
matters: if temporal judgments are produced by the same pipelines that produce other relational
judgments (causal, spatial, conceptual), then having a common aggregation and comparison alge-
bra makes it possible to share learning rules, regularizers, and compositional mechanisms across
domains.

Definition 58 (Coherence constraints for temporal evidence (optional)). One may impose any of
the following (model-dependent) constraints:

1. (Anti-symmetry as evidence) B + (t1 , t2 ) ≤ B − (t2 , t1 ) for all t1 , t2 .

2. (Transitive support) B(t1 , t3 ) ≥ B(t1 , t2 ) ⊗ B(t2 , t3 ) where ⊗ is the quantale tensor (componen-
   twise multiplication).

3. (Irreflexive support) B + (t, t) = 0 for all t (while allowing B − (t, t) to encode strong evidence
   against t < t).

We emphasize that these are constraints on evidence, not metaphysical axioms.

Remark 228 (Componentwise reading of the constraints). It may be helpful to unpack clause (2)
in coordinates. If ⊗ is componentwise multiplication, then

                 B(t1 , t2 ) ⊗ B(t2 , t3 ) = B + (t1 , t2 )B + (t2 , t3 ), B − (t1 , t2 )B − (t2 , t3 ) .
                                                                                                       


With the componentwise order on V , the inequality B(t1 , t3 ) ≥ (· · · ) requires both

         B + (t1 , t3 ) ≥ B + (t1 , t2 )B + (t2 , t3 )   and    B − (t1 , t3 ) ≥ B − (t1 , t2 )B − (t2 , t3 ).

Thus transitivity is treated as a statement about how evidence propagates along a chain in each
channel, rather than as a demand that the sign of the final verdict must be classically consistent.
This makes it possible for a system to infer that a longer chain can inherit both support and
counter-support, which is often exactly what happens when different subsystems contribute competing
temporal cues.

Remark 229 (Intuition and examples for the evidence constraints). Clause (1) says: evidence
that t1 is before t2 should count as counter-evidence for t2 being before t1 . It is a soft version of
asymmetry, expressed in the vocabulary of evidence rather than in the vocabulary of facts. Clause
(2) says: if we have support for t1 < t2 and for t2 < t3 , then we should have at least the composed
support for t1 < t3 ; the tensor ⊗ (componentwise multiplication in the p-bit quantale) plays the
role of “and then,” i.e. accumulation of evidential strength along a chain. Clause (3) enforces that
the positive channel does not directly support self-precedence, while leaving room for the negative
channel to record explicit rejection of it.
    These constraints are useful when B is learned or estimated: they provide regularizers that
encourage temporal evidence to behave like an order without demanding perfect consistency. As a
concrete numerical illustration, if B + (t1 , t2 ) = 0.9 and B + (t2 , t3 ) = 0.8, then clause (2) requires
B + (t1 , t3 ) ≥ 0.72; similarly, if both negative evidences are 0.6, it requires B − (t1 , t3 ) ≥ 0.36. This
matches an intuitive “attenuation along a path” reading: longer compositions retain only what
survives repeated conjunction.




                                                         128