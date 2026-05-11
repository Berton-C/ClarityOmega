# 25 Reality-systems, cosmos, multiverse, and eurycosm

by arbitrary suprema, and with monoidal product + distributing over suprema. We will not need
the full quantale structure here, but it is convenient to keep the “quantale habit” so intensity and
weakness can be treated uniformly later. Concretely, the choice of + reflects the idea that (when
appropriate independence assumptions hold) the combined salience of distinct supported patterns can
be accumulated, while the order ≤ supports the comparison of alternative descriptions by dominance
of intensity. Allowing ∞ is a technical convenience: it can represent “effectively unignorable”
regularities within I (for instance, hard constraints induced by the environment or by institutional
enforcement), and it guarantees the existence of suprema for arbitrarily large families of intensities
when such joins are useful for analysis.
Definition 393 (Minds, communities, and supported patterns). Let Mind be a set (or groupoid) of
minds. Fix a (finite) community C ⊆ Mind and a time interval I. For each nonempty subset U ⊆ C,
let PatU (I) denote the set of patterns whose realization is supported across exactly the minds in U
(e.g. shared attention, synchronized appraisal cycles, coordinated linguistic constructions, mutually
constrained expectations, shared affective dynamics). We write Pat{m} (I) as Patm (I) for singleton
supports.
    The phrase “supported across exactly the minds in U ” is intended to separate (i) patterns that
are purely idiosyncratic to a single mind from (ii) patterns that are genuinely sustained by interac-
tion, mutual modeling, or common constraints within a subcommunity. Here “exactly” should be
read as a modeling choice rather than a metaphysical claim: in practice one may treat PatU (I) as
consisting of patterns for which U is the minimal support set in C (with the understanding that a
pattern instantiated by all of U may also be compatible with, or embedded in, larger-U 0 patterns).
Nothing in what follows depends on having a unique minimal support; the only essential point is
that we can distinguish patterns by how broadly in the community they are realized.
    When Mind is taken as a groupoid rather than a set, the intention is that there may be structure-
preserving identifications between minds (e.g. treating two roles as equivalent in a certain analysis,
or quotienting by a notion of observational indistinguishability), and that pattern support can
be considered up to such identifications. This flexibility is useful later when we want to discuss
institutional roles, replaceability, and anonymity in large-scale intersubjective systems.
Definition 394 (Community intensity data). A community intensity datum on (C, I) is a family
of functions
                         w = { wU : PatU (I) → VI | ∅ =
                                                      6 U ⊆C}
assigning an intensity to each supported pattern.
    Intuitively, w encodes not only what patterns occur but how strongly they matter to the
community-level dynamics on I. One may read wU (p) as a community-relative measure of how
much predictive compression is gained by tracking the pattern p as a regularity jointly carried by
the minds in U (as opposed to treating the constituents of p as unrelated fluctuations). Because
VI is additive, it is natural—when appropriate—to consider aggregated quantities such as the total
intensity of all patterns supported on a given U ,
                                                   M
                                     W (U ) :=        wU (p),
                                                p∈PatU (I)

whenever the relevant sum is well-defined (or replaced by a supremum, depending on the modeling
choice). Such aggregated views will later make it easy to state conditions like “most of the action
is dyadic” or “the community has a strong global mode,” without committing to a particular
enumeration of patterns.

                                                 531
Definition 395 (Intersubjective reality-system). Fix (C, I) and a community intensity datum w.
An intersubjective reality-system for C on I is a triple
                                                             
                                      RC,I = EC,I , LC,I , w

where:

   • EC,I is a set of entities-as-modeled-in-community (tokens for persons, objects, shared symbols,
     joint goals, norms, roles, etc., as represented across the community);

   • LC,I is a set of weighted links encoding predictive and causal relationships between entities and
     between minds’ representations of entities. Formally, one may take LC,I to be a VI -weighted
     directed hypergraph or simplicial set on EC,I ;

   • w assigns intensities to patterns supported on subcommunities U ⊆ C.

We say RC,I is intersubjective (rather than merely a disjoint union of individual realities) if LC,I
contains nontrivial cross-mind links of significant weight and w assigns non-negligible total intensity
to patterns supported on |U | ≥ 2.

     The three components play complementary roles. The entity set EC,I is not meant to be a
list of mind-independent objects, but rather the community’s working ontology on I: the handles
that appear in joint descriptions, coordination, and expectation management. Thus “the same”
external object may correspond to different community-entities across different communities (or
time intervals), and conversely a single community-entity (e.g. a role like “referee” or a symbol like
a brand) may be realized by many different individuals or physical tokens while remaining stable
at the level of communal modeling.
     The link structure LC,I is where predictive and causal organization is recorded. Treating LC,I
as a weighted directed hypergraph emphasizes that relations in social cognition are often many-
to-one or many-to-many (e.g. several cues jointly predict an interpretation; multiple people jointly
enforce a norm; a shared goal shapes several downstream actions). The VI -weight on a link can
be interpreted as the strength, reliability, or relevance of the predictive/causal dependency during
I, in the same broad sense of salience used for pattern intensity. Links may connect not only
“external” entities but also representations (e.g. “Alice believes Bob intends X” linking an Alice-
representation node to a Bob-intention node), which is why cross-mind links are a natural place to
represent higher-order social inference and mutual modeling.
     The condition for being genuinely intersubjective is deliberately qualitative (“significant weight”,
“non-negligible total intensity”) because the intended use is comparative and context-sensitive. In
some settings, a small number of high-weight cross-mind links (e.g. a rigid command structure)
can dominate; in others, a diffuse field of moderate-weight mutual expectations (e.g. conversational
turn-taking or politeness norms) can be the primary stabilizer. The formalism permits either ex-
treme, and the role of w is precisely to let the analyst say where, within C, the realized regularities
actually live.

Remark 1334. This definition is intentionally permissive: “intersubjective reality” is not a single
kind of object. It ranges from dyadic conversations to large-scale institutions, markets, scientific
communities, and cultures. What unifies these is the presence of significant cross-mind predic-
tion/causation and significant cross-mind patterns.

   A useful way to read the permissiveness is that RC,I is a pattern system indexed by community
support rather than a single monolithic graph: it can represent simultaneously (i) individual-level

                                                  532
regularities (|U | = 1), (ii) small-group synchronizations (|U | = 2, 3), and (iii) whole-community
stabilizers (U = C). For example, in a conversation between two participants a, b ∈ C, one expects
substantial intensity on patterns in Pat{a,b} (I) such as turn-taking rhythms, accommodation of
vocabulary, and mutual repair strategies, together with cross-mind links in LC,I encoding rapid
reciprocal prediction (e.g. “a’s utterance predicts b’s next move”). In an institution, by contrast,
one expects prominent entities in EC,I corresponding to roles and norms, and high-intensity patterns
supported on larger subcommunities (sometimes approaching U = C), such as shared compliance
expectations or shared symbol grounding.
    Finally, note that nothing requires PatU (I) to be explicitly enumerated in applications. One
can treat it as an abstract carrier for whatever pattern-extraction procedure is used (statistical,
ethnographic, mechanistic, or hybrid), with w serving as the interface between such extraction and
the higher-level statements made about intersubjective structure.

24.4    Intersubjective communion as cross-mind intensity dominance
Hyperseed’s definition of intersubjective communion can be treated as a comparative statement:
cross-mind patterns become more intense than within-mind patterns. In this framing, communion
is not a primitive “togetherness” predicate but a measurable dominance relation: the community-
level phenomenology is taken to be explained by whether jointly-supported structure outweighs the
structure that remains private to each individual mind. The intent is that Wcross and Win serve as
coarse but tractable aggregates of “how much pattern-intensity is being carried” by intersubjective
versus merely intrasubjective organization, relative to a fixed community C, an index set I (e.g.
times, contexts, or interaction windows), and a chosen intensity datum w.

Definition 396 (Within-mind and cross-mind total intensity). Fix (C, I) and a community inten-
sity datum w. Define the within-mind total intensity and cross-mind total intensity by:
                                              X      X
                             Win (C, I; w) :=              w{m} (p),
                                                   m∈C p∈Patm (I)
                                                   X       X
                             Wcross (C, I; w) :=                     wU (p).
                                                   U ⊆C p∈PatU (I)
                                                   |U |≥2

(We assume these sums are finite; if not, replace sums by suitable suprema or integrals.)

    It is useful to keep in mind the intended separation of roles: Win aggregates intensities of
patterns whose supporting set is a singleton {m} (so they are, by construction, “owned” by one
mind), whereas Wcross aggregates patterns supported by some coalition U of size at least 2. The
indexing by U permits graded forms of intersubjectivity: a pattern supported by a dyad, a triad, or
the whole community can be assigned intensities at the corresponding support level(s), depending
on how PatU (I) and wU are specified. In applications, one often ensures that patterns are support-
tagged (so that the same abstract content appearing with different support sets is treated as distinct
pattern tokens), which makes the above sums unambiguous even when there is conceptual overlap
between “the same” pattern instantiated at different levels of support.
    The parenthetical finiteness clause also carries conceptual content: the theory only needs enough
regularity to compare within-mind and cross-mind aggregates. If the pattern collections are infinite
(for example, if PatU (I) is generated by a continuous-time process), replacing sums with integrals
makes the comparison sensitive to the choice of measure; replacing sums with suprema yields
a “peak-dominance” reading rather than a “total-mass” reading. The present section uses the


                                                   533
summation presentation because it most directly matches the interpretation of Win and Wcross as
total intensity budgets.
Definition 397 (Communion predicate and communion margin). We say the community C exhibits
intersubjective communion on I (relative to w) if
                    Comm(C, I; w)     holds, i.e.    Wcross (C, I; w) > Win (C, I; w).
Define the communion margin by
                          ∆Comm (C, I; w) := Wcross (C, I; w) − Win (C, I; w).
    The strict inequality in Comm is intended to encode a genuine dominance rather than a tie: if
Wcross = Win , then the community is at a boundary where neither intrasubjective nor intersubjec-
tive structure clearly governs the overall intensity accounting. In many empirical or computational
settings, one may introduce a tolerance parameter τ > 0 and require Wcross ≥ Win + τ to obtain ro-
bustness to estimation noise; the margin ∆Comm already provides the quantity one would threshold
in such a variant.
    It is also sometimes convenient to separate Wcross by coalition size:
                                                  |C|
                                                  X   X        X
                             Wcross (C, I; w) =                         wU (p),
                                                  k=2 U ⊆C p∈PatU (I)
                                                      |U |=k

so that one can distinguish dyadic resonance from broadly shared patterns. On this view, ∆Comm
measures not only whether intersubjectivity dominates, but also (when decomposed) how it dominates—
e.g. by many small coalitions or by a smaller number of large, community-wide supports.
Remark 1335. One can normalize ∆Comm to obtain a bounded score, e.g. ∆Comm /(Wcross +Win +ε).
We keep the unnormalized margin because (a) it composes additively in the simplest way, and (b)
it keeps clear the ontology-level meaning: a literal dominance of cross-supported pattern intensity.
    A further reason the unnormalized margin can be informative is that it retains sensitivity to
the scale of the interaction: two communities might have the same normalized score while differing
drastically in absolute cross-mind intensity, which may matter if one aims to connect communion to
downstream effects (e.g. behavioral coordination, communication bandwidth, or aesthetic salience).
At the same time, the reader should note an elementary invariance: if one scales all intensities by
a common factor λ > 0 (i.e. replaces w by λw pointwise), then both Win and Wcross scale by λ,
and hence Comm(C, I; w) is unchanged while ∆Comm scales by λ. Thus the predicate captures a
comparative dominance, while the margin captures a dominance magnitude.
    For intuition, consider the smallest nontrivial case C = {m1 , m2 }. Then
                X                     X                                   X
     Win =             w{m1 } (p) +          w{m2 } (p),   Wcross =               w{m1 ,m2 } (p),
            p∈Patm1 (I)            p∈Patm2 (I)                            p∈Pat{m1 ,m2 } (I)

so communion says that the dyad’s jointly-supported intensity outweighs the sum of their private
intensities. This makes explicit the conceptual reading: the dyad is “more constituted” by what is
mutually supported than by what remains individually supported.
Proposition 38 (Monotonicity of communion under adding cross-supported patterns). Fix (C, I)
and a community intensity datum w. If w0 differs from w only by increasing some cross-mind inten-
sities (i.e. wU0 (p) ≥ wU (p) for all |U | ≥ 2, and w{m}
                                                     0   = w{m} for singletons), then ∆Comm (C, I; w0 ) ≥
∆Comm (C, I; w). In particular, if Comm(C, I; w) holds, then Comm(C, I; w0 ) holds.

                                                    534
Proof. Immediate from Definition 396 and Definition 397: only Wcross can increase, while Win is
unchanged.

    This proposition formalizes a minimal adequacy condition for the notion of communion: strength-
ening jointly-supported pattern intensity (without changing private pattern intensity) cannot make
the community less communal under the dominance criterion. Equivalently, the only way to de-
crease ∆Comm is to decrease cross-mind intensity or to increase within-mind intensity; the definition
thereby cleanly separates “what adds to togetherness” from “what adds to privateness” at the level
of intensity bookkeeping. When ∆Comm is used as a target quantity for optimization or learning,
Proposition 38 ensures that any update rule that monotonically increases cross-supported weights
(holding singleton weights fixed) is guaranteed to be non-worsening with respect to the communion
margin.

24.5    Explicit intersubjective communion via self-model recognition
Hyperseed distinguishes implicit communion (cross-mind patterns dominate) from explicit commu-
nion, where the participants’ self-models recognize the communion as such. To formalize “recog-
nize” we use a simple paraconsistent truth-value space. This keeps the ontology compatible with
simultaneously holding (or partially holding) seemingly incompatible self-reports, commitments,
and interpretations. In particular, “recognition” here is treated as a kind of endorsement state
internal to each participant: one can endorse that communion is occurring while also endorsing (to
some extent) that it is not occurring, or that it is unsafe, or that one is uncertain what to call the
experience. This is common in real reports (e.g. “I feel connected, but I also feel guarded”), and it
is precisely the kind of case where a classical truth assignment would force premature resolution.

Definition 398 (Uncertain paraconsistent truth values). Let

                                            B := [0, 1] × [0, 1].

An element b = (t, f ) ∈ B is read as “degree of truth” t and “degree of falsity” f . Define negation,
conjunction, and disjunction by

                                      ¬(t, f ) := (f, t),
                           (t1 , f1 ) ∧ (t2 , f2 ) := (min{t1 , t2 }, max{f1 , f2 }),
                           (t1 , f1 ) ∨ (t2 , f2 ) := (max{t1 , t2 }, min{f1 , f2 }).

Fix a designation threshold τ ∈ (0, 1]. We say b = (t, f ) is designated (accepted/endorsed) if t ≥ τ .

    The intended reading is that t tracks the strength with which the self-model supports a propo-
sition, while f tracks the strength with which the self-model supports its denial. Nothing in the
definition enforces t + f = 1, so the framework permits both incompleteness (low t and low f ) and
inconsistency (high t and high f ). The connective definitions make this interpretation operational:
conjunction preserves the weaker truth-support (via min) while accumulating falsity-support (via
max), whereas disjunction preserves the stronger truth-support (via max) while reducing falsity-
support (via min). Negation simply swaps the two degrees, reflecting that support for ¬ϕ is
measured by support-for-falsity of ϕ in the same self-model.
    The designation threshold τ isolates the specific notion of “counts as endorsed” needed for
explicit communion. For instance, taking τ = 1 yields a strict reading: only full truth-support
counts as recognition. Taking τ < 1 permits graded recognition: partial endorsement suffices,
which can be appropriate when self-model access is noisy, introspective reports are hesitant, or

                                                     535
participants are linguistically misaligned but still clearly signaling a “yes” in practice. Importantly,
designation depends only on t; thus a proposition may be designated even when f is simultaneously
large, capturing the case “I endorse that communion is occurring, even though part of me also rejects
that description.”

Remark 1336. This is a continuous generalization of the familiar four-valued Belnap-Dunn bilat-
tice. The key property for our purposes is: contradictions do not entail triviality.

    Concretely, the familiar four corners embed as (1, 0) (true only), (0, 1) (false only), (1, 1) (both
true and false), and (0, 0) (neither), with the continuous interior representing intermediate mixtures.
The paraconsistent motivation is practical rather than purely philosophical: if a participant’s self-
model includes both “we are in communion” and “we are not in communion” (or “this is safe”
and “this is unsafe”) at nonzero strength, then we do not want the formalism to collapse into
a state where every proposition becomes equally endorsable. Instead, we want to preserve the
informational content of ambivalence and keep explicit-communion criteria well-defined.

Definition 399 (Self-model valuation). Fix a mind m ∈ C. Let Lm be the (informal) language of
propositions expressible in m’s self-model on I (e.g. “we are in communion now”, “I feel connected”,
“I feel threatened”, etc.). A self-model valuation is a map

                                            vm : Lm → B.

    The point of allowing Lm to be informal is to avoid overcommitting to a particular cognitive
architecture. Different minds may carve the space of self-descriptions differently, may have different
granularity of introspective access, and may attach different connotations to the same surface
sentence. What matters for the present definition is only that each mind can represent (in some
way) a proposition playing the role of “the community is currently in communion on I,” and
that the valuation records the mind’s endorsement and rejection degrees for such propositions. In
settings where the self-model is partly implicit or sub-symbolic, vm can be viewed as an idealization
of an accessible report channel (e.g. a confidence score, a felt-sense rating, or a post-hoc linguistic
report) rather than a literal internal data structure.

Definition 400 (Explicit communion). Fix (C, I), intensity datum w, and self-model valuations
vm for m ∈ C. Assume there is a proposition symbol CommNowC,I available in each Lm meaning
“the community C is currently in communion on I” (as represented by m). We say explicit
intersubjective communion holds if:

  1. Comm(C, I; w) holds (implicit communion), and

  2. for every m ∈ C, the value vm (CommNowC,I ) is designated.

We denote this by ExplComm(C, I; w, {vm }).

    Clause (2) is intentionally phrased as a universal condition over participants: explicit commu-
nion is not merely that “someone notices,” nor that “on average the group notices,” but that each
member’s self-model contains sufficient endorsement of the communion proposition. Because desig-
nation ignores the falsity coordinate, this allows explicit communion even when some members are
conflicted, defensive, or simultaneously carrying counter-interpretations, provided the endorsement
of CommNowC,I clears the agreed threshold τ . For example, if τ = 0.7, then a participant with

                                    vm (CommNowC,I ) = (0.8, 0.8)


                                                  536
still counts as explicitly recognizing communion (designated), even though they are also strongly
pulled toward denying it; this models “yes, and no” states without forcing a resolution. Conversely,
a participant with
                                     vm (CommNowC,I ) = (0.6, 0.0)
would not count as recognizing it at τ = 0.7, even though they are not actively rejecting it; this
models hesitant or unclear acknowledgement.
    The explicitness criterion can also be read as a coordination condition on meta-representation:
implicit communion concerns the dominance of cross-supported patterns in the system dynamics,
whereas explicit communion adds that each self-model has tracked and endorsed that very fact.
In that sense, the additional structure in ExplComm is not merely epistemic; it is part of the
phenomenon being defined, since Hyperseed distinguishes communion that is lived but unrecog-
nized from communion that is jointly identified and thus available for deliberate action, narrative
stabilization, and norm formation.

Remark 1337. Explicit communion is a joint condition: it is possible that Comm holds but some
participants do not endorse (or do not have access to) the proposition CommNowC,I in their self-
models. Conversely, a group can self-report communion while cross-supported patterns do not dom-
inate, in which case ExplComm fails due to the first clause.

    A further subtlety is that “do not have access” can occur even when a participant is behaviorally
aligned with the communion: they may enact the pattern without categorizing it as communion,
or they may lack the linguistic/conceptual resources to form CommNowC,I as a stable self-model
proposition. The definition treats this as a failure of explicitness (by assumption, the symbol
exists, but the valuation may fail to designate it), which matches the intended distinction between
tacit participation and self-conscious recognition. At the same time, the paraconsistent setting
prevents such cases from forcing a binary verdict about the participant’s entire self-model: the
model can represent partial endorsement, partial denial, and partial indeterminacy simultaneously,
and explicit communion depends only on whether the endorsement passes the chosen threshold.

24.6    Spiritual experience as communion with a broader-scope mind
Hyperseed treats spiritual experience as a special case of communion: communion between a mind
M and another mind that is experienced as broader in scope. In this framing, “spiritual” does not
name a separate ontological substance; it names a particular relational configuration within the
general communion machinery, namely one in which the partner mind is comparatively broader (in
a sense made checkable below) over the interval of interest.

Definition 401 (Scope of a mind on an interval). Fix a mind m and an interval I. Assume
we have: (i) a multiset of patterns Patm (I), (ii) intensities w{m} on these patterns, and (iii) a
complexity/cost function κ : Patm (I) → [0, ∞) measuring pattern depth (e.g. description length
in some fixed representational language, or effort to represent/maintain the pattern). Define the
scope as
                     Scope(m, I) := α · Hm (I) + (1 − α) · Dm (I), α ∈ [0, 1],
where
                          X                                                  w{m} (p)
         Hm (I) := −                πm (p) log(πm (p) + ε),   πm (p) := P                       ,
                       p∈Patm (I)                                       q∈Patm (I) w{m} (q) + ε




                                                     537
and                                               X
                                   Dm (I) :=                πm (p) κ(p).
                                               p∈Patm (I)

Here ε > 0 is a small numerical stabilizer.

Remark 1338. Hm measures diversity of salient patterns (breadth), while Dm measures average
depth. Any other combination of diversity and depth consistent with the intended semantics could
be used. The ontology only requires that “broader scope” be a mathematically checkable comparative.

Remark 1339. The normalization πm makes Hm and Dm depend on relative saliencies rather
than the absolute scale of w{m} ; in particular, if w{m} is multiplied by a positive constant, πm
is unchanged (up to the ε term), so scope is driven by how attention/importance is distributed
across patterns. The multiset language allows multiple tokenings of the “same” schematic pattern
to be treated as distinct when the representational system of m distinguishes them (e.g. repeated
motifs, recurring affective complexes), while still permitting coarse-graining by choosing Patm (I)
appropriately.

Remark 1340. The parameter α interpolates between two limiting readings: when α = 1, scope
reduces to diversity of salient patterns (a purely breadth-like notion), and when α = 0, scope reduces
to average depth under κ (a purely depth-like notion). The choice of log base in Hm only rescales
the contribution of the entropy term and can be absorbed into α (or into a rescaling of κ), so the
operational content is the comparative ordering of scopes across minds/intervals rather than any
absolute unit. The stabilizer ε can be taken small enough that it does not affect comparisons except
in degenerate cases (e.g. extremely sparse or near-zero intensity mass), where it serves to keep the
expressions well-defined.

Definition 402 (Spiritual communion). Let m, n be minds and consider C = {m, n}. We say m
has a spiritual experience with n on I if:

  1. Comm({m, n}, I; w) holds, and

  2. Scope(n, I) ≥ Scope(m, I) + δ for some fixed δ > 0,

where the second condition expresses that n is broader-scope than m.

Remark 1341. The threshold δ encodes that “broader” is intended as a robust rather than hairline
comparative: it rules out labeling as spiritual those cases where m and n have essentially the same
breadth/depth profile on I up to negligible fluctuations. In applications, δ may be treated as a
context-dependent parameter (e.g. varying by domain, by the granularity of Pat, or by the scaling
of κ), but the logical role remains the same: it implements a margin that makes the broader-scope
relation stable under small modeling perturbations (choice of pattern vocabulary, noise in w, etc.).

Remark 1342. The definition is deliberately stated in terms of Scope(n, I), not merely m’s belief
about it. This yields a structural notion that can, in principle, be assessed from a third-person model
of both pattern systems. At the same time, many episodes described as spiritual involve an appear-
ance of vastness or encompassment that may or may not match the external comparative; if desired,
one can represent this by adding an epistemic layer in which m maintains an estimate Scope \ m (n, I)
and the phenomenology tracks Scopem (n, I) − Scopem (m, I), while the present definition tracks the
                                 \               \
underlying relational configuration.



                                                  538
Remark 1343. The “broader-scope mind” n may be (i) a collective mind of a group including m,
(ii) a mind of another individual, animal, ecosystem-scale process, etc., or (iii) an unusual mind-
model accessed in altered states. The ontology does not decide which of these is metaphysically
correct; it only supplies a structural criterion for when the experience is of the relevant kind.
Remark 1344. In case (i), the scope inequality can be read as a formal version of a familiar
intuition: groups can sustain a richer or deeper joint pattern repertoire than any single member
on the same interval (e.g. via division of cognitive labor, distributed memory, or complementary
perspectives). In case (ii), the inequality can represent the phenomenology of encountering an agent
whose lived world is experienced as “larger” (more varied or more structurally articulated). In case
(iii), the scope inequality can model episodes where m relates to an internally generated partner n
(a god-form, archetype, “nature,” “the universe”) that carries a broader pattern economy than m’s
ordinary self-model, even if the ontological status of n is left open by design.
Definition 403 (Entheogen as a communion-shifting intervention). Fix an embodied mind m with
body Bm and suppose interventions on Bm can change m’s pattern system. An entheogen (or more
generally an entheogenic procedure) is an intervention E on Bm such that, for a relevant class of
intervals I and relevant classes of partner minds n, the induced change in intensity data w 7→ wE
tends to increase
                      ∆Comm ({m, n}, I; wE ) and/or vm (CommNow{m,n},I )
toward designation.
Remark 1345. This definition intentionally avoids committing to a single mechanism. Entheogens
may act by changing attention dynamics, relaxing self-model rigidity, increasing cross-subsystem
coupling, altering predictive priors, etc. All of these show up as changes in w and/or in the
valuation maps vm .
Remark 1346. The “and/or” is important: some interventions primarily change the structural
conditions for communion (as measured by ∆Comm ), while others primarily change whether m counts
an already-present relation as salient, valuable, or real (as measured by vm (CommNow{m,n},I )). The
phrase “toward designation” is meant to cover thresholded decision rules commonly used elsewhere
in the ontology: even if ∆Comm is continuous, communion-as-designated may require crossing a
context-specific cutoff, and entheogens are characterized here by their tendency to push the system
across that boundary for a nontrivial class of (I, n) rather than by guaranteeing communion in every
instance.

24.7   Emotion and compassion as mind-body-and-community patterns
Hyperseed treats emotions as dynamical patterns spanning large portions of mind and body over
time. Compassion is treated as an emotion whose content and dynamics are essentially intersub-
jective. In this framing, an “emotion” is not primarily a propositional judgment, nor merely an
isolated bodily sensation, but a coordinated regime that recruits perception, appraisal, action-
readiness, autonomic regulation, and attention into a temporally extended configuration. Likewise,
“intersubjective” does not mean that an emotion must be publicly expressed or linguistically re-
ported; it means that some of the constitutive structure of the episode depends on, tracks, or
anticipates patterns that are jointly realized across more than one mind (e.g. co-regulation, mutual
attention, joint action, or reciprocity constraints).
Definition 404 (Emotion episode). Fix an embodied mind m with body Bm and interval I. Let
Sm (t) denote the (modeled) mind-state at time t ∈ I and SBm (t) the body-state. An emotion episode
is a pattern e ∈ Patm (I) such that:

                                                539
  1. e is supported on both mind and body degrees of freedom (not purely cognitive, not purely
     somatic),

  2. e has nontrivial temporal extent (persists across a subinterval J ⊆ I),

  3. e organizes (constrains) a large fraction of the system’s active patterns during J.

    Concretely, condition (1) is meant to exclude both “cold” belief updates that do not recruit
bodily regulation and also purely reflexive physiological events that do not enter the mind-level
organization of attention and action; the episode must be realized as a coupled mind–body pattern.
Condition (2) distinguishes an episode from instantaneous perturbations (e.g. a momentary startle
spike) by requiring persistence on a subinterval with internal temporal structure, allowing onset,
maintenance, and decay phases. Condition (3) captures the familiar phenomenology that emotions
are global organizers: they bias perception, reshape salience, modulate memory access, and gate
policy selection, rather than remaining local to a single representational module. The membership
e ∈ Patm (I) is intended to emphasize that episodes are identified as patterns at the level of the
whole embodied system across time, not as single-state labels; in particular, two distinct micro-
realizations can count as the “same” episode-type if they share the relevant organizing constraints
at the pattern level.

Definition 405 (Compassion episode). Fix a community C containing m and another mind m0 6=
m. A compassion episode in m toward m0 on I is an emotion episode e ∈ Patm (I) such that:

  1. e is causally and predictively coupled to cross-mind patterns supported on {m, m0 } (i.e. in-
     tersubjective content),

  2. e carries positive valence in m’s valuation scheme and includes patterns representing m0 as
     included in m’s concern-set (“love inclusive of the other mind”).

    The coupling requirement in (1) is intended to be stronger than mere causal dependence on a
perceptual stimulus: the compassion episode must participate in a dynamical loop in which m tracks
and forecasts relevant aspects of m0 (e.g. affect, needs, intentions, vulnerability), and where that
tracking is itself stabilized or corrected by cross-mind interaction. In particular, the “predictive”
clause allows compassion to be constituted partly by anticipatory organization (e.g. preparing
supportive actions, maintaining readiness to coordinate, sustaining attention to m0 ), rather than
requiring that all relevant information about m0 be presently observed. The concern-set clause in
(2) is meant to mark the difference between benevolent attention and neutral monitoring: m0 is
represented as a beneficiary of m’s protective, affiliative, or helping dispositions, so that action
selection is biased toward outcomes favorable to m0 (subject to m’s broader constraints). Nothing
in the definition requires that m0 reciprocate, that m0 be aware of m’s state, or that the episode be
socially successful; it only requires that the episode in m be constituted by intersubjective coupling
and inclusive valuation directed toward m0 .

Remark 1347. The ontology does not insist on a single scalar “valence”. All that is required is
that there is a valuation component (possibly multi-dimensional) that can distinguish benevolent
inclusion from aversive exclusion, and that compassion corresponds to inclusion along that axis.

   This remark allows the model to accommodate cases where affective tone, motivational direction,
and normative appraisal dissociate (for example, compassion that is experienced as painful or heavy
while remaining prosocial and inclusive). It also permits valuation schemes in which “positive” is
not hedonically pleasant but instead reflects a structured preference for relationship-preserving,

                                                 540
other-regarding, or harm-avoiding outcomes. Accordingly, the “axis” of inclusion can be realized
by a family of coordinated valuation components (e.g. attachment, affiliation, care, fairness) so long
as they jointly implement the inclusion/exclusion distinction relevant to compassion.

Proposition 39 (Communion-bias of compassion). Suppose a mind m has a compassion episode
toward m0 on I as in Definition 405. Then, for the dyadic community {m, m0 }, the cross-supported
intensity Wcross is bounded below by the total intensity of those cross-supported patterns coupled to
the compassion episode. In particular, compassion in this sense cannot occur in a purely individual
reality-system with Wcross = 0.

    Intuitively, the proposition formalizes a “communion bias”: if compassion is constitutively
intersubjective, then it necessarily allocates nonzero pattern-intensity to structures that are not
realizable within a single isolated mind. The bound is stated in terms of cross-supported patterns
coupled to the episode to emphasize that not all interpersonal structure in {m, m0 } need be relevant,
only that the compassion episode cannot be constituted without some positive share of cross-mind
organization. This is compatible with compassion also recruiting many purely intra-mind patterns
in m (e.g. autobiographical memory, private imagery, internal deliberation), while still requiring
that a nontrivial component of the episode’s dynamics is anchored in patterns supported on the
dyad.

Proof. By Definition 405, the compassion episode is causally and predictively coupled to cross-
supported patterns on {m, m0 }, hence at least one such pattern has positive intensity, so Wcross > 0
and is bounded below by the sum of intensities of these coupled patterns.

    The proof uses only the minimal content of the definition: coupling entails the existence of at
least one cross-supported pattern participating in the episode’s causal/predictive structure, and the
intensity formalism assigns a nonzero contribution to any such participating pattern. The inequality
is therefore a bookkeeping statement about how the total cross-supported intensity cannot fall
below the portion that is actually recruited by the compassion episode. Under a strict isolation
assumption (no cross-supported patterns at all, i.e. Wcross = 0), the definitional coupling condition
cannot be satisfied, so compassion-as-defined is ruled out in that regime.

24.8     Aesthetics and beauty as paraconsistent “surprising fulfillment”
Hyperseed proposes: (i) aesthetic experience is the experience of beauty, (ii) art is whatever has
significant aesthetic effect for a class of experiencers, and (iii) beauty involves an experience that
is both fulfilling-of-expectations and surprising, and whose internal representation behaves like an
open-endedly intelligent mental subnetwork.
    We now encode these claims in a form compatible with the earlier quantale/pattern formalism.

24.8.1    Fulfillment and surprise as distinct evaluators
Definition 406 (Predictive fulfillment and compression surprise). Fix a mind m and an encoun-
tered stimulus/artifact/event B over interval I. Assume m maintains:

   • a predictive model Πm assigning likelihoods to observations of B,

   • an internal coding/compression scheme with code-length functional Lm (·) on representations
     of B.



                                                 541
Define:
                                                                   
                       Fulm (B; I) := exp −λ · E[− log Πm (obs(B))] ∈ (0, 1],
                      Surm (B; I) := max{0, Lold      new
                                             m (B) − Lm (B)} ∈ [0, ∞),

where λ > 0 is a scaling parameter and “old/new” refer to before/after updating m’s internal codes
after the encounter with B.

Remark 1348. With these definitions, fulfillment and surprise are not forced to be complements.
A stimulus can be broadly predictable (high Ful) while still yielding nontrivial compression gain
(high Sur), which is a precise mathematical reading of “surprising fulfillment”.

24.8.2    Beauty as a paraconsistent conjunction
Hyperseed explicitly notes a tension (even a contradiction) between fulfillment and surprise. A
convenient way to keep that tension in the formalism without collapsing reasoning is to use a
paraconsistent logic.

Definition 407 (Beauty proposition and valuation). Fix a mind m and stimulus B on I. Let
Ful(B) and Sur(B) be proposition symbols in m’s self-model language Lm . Define a valuation vm
on these by mapping to B (Definition 398) as:

                 vm (Ful(B)) := (min{1, Fulm (B; I)}, 1 − min{1, Fulm (B; I)}),
                                                                                
                                          Surm (B;I)                Surm (B;I)
                 vm (Sur(B)) := min{1, Sur m (B;I)+1
                                                     }, 1 − min{1, Surm (B;I)+1 }  .

Define the beauty proposition by

                                   Beaut(B) := Ful(B) ∧ Sur(B),

with ∧ interpreted as paraconsistent conjunction on B.

Theorem 21 (Non-explosion for “surprising fulfillment”). In the paraconsistent semantics of Def-
inition 398, there exist valuations v and propositions P, Q such that P and ¬P are both designated,
but Q is not designated. Hence contradictions do not entail triviality.

Proof. Let τ = 1 (designation means t = 1). Choose v(P ) = (1, 1) and v(Q) = (0, 0). Then
v(¬P ) = ¬(1, 1) = (1, 1), so both P and ¬P are designated. But v(Q) has truth degree 0, so Q is
not designated.

Remark 1349. This formalizes the intended use: one can explicitly represent the tension between
“fulfills expectations” and “is surprising” (including by adding additional rules that may generate
contradictions), yet still reason nontrivially about other matters.

24.8.3    Beauty and open-endedly intelligent subnetworks
Hyperseed’s definition of beauty includes that the internal representation of the beautiful object
“behaves as an open-endedly intelligent mental subnetwork.” We capture this with a minimal,
ontology-compatible criterion: the representation should contribute to both individuation and self-
transcendence while maintaining self-continuity.



                                                542
Definition 408 (Individuation gain, transcendence gain, self-continuity). Fix a mind m and an
encounter with B on I. Assume we have numeric functionals:

                GI (m, B; I) ∈ [0, ∞),   GT (m, B; I) ∈ [0, ∞),    SelfC(m; I) ∈ [0, 1],

interpreted respectively as individuation gain, self-transcendence gain, and self-continuity during I.
Assume monotonicity constraints consistent with Hyperseed’s intent:

  1. GI is nondecreasing in Fulm (B; I) (fulfillment supports individuation),

  2. GT is nondecreasing in Surm (B; I) and in SelfC(m; I) (surprise with continuity supports self-
     transcendence).

Definition 409 (Aesthetic subnetwork is OEI-active). Let Repm (B; I) denote the induced pat-
tern subweb/subnetwork in m representing B during I. We say Repm (B; I) is OEI-active if both
GI (m, B; I) > 0 and GT (m, B; I) > 0.

Theorem 22 (Beauty implies OEI-activity under mild thresholds). Fix thresholds θF ∈ (0, 1],
θS > 0, and θC ∈ (0, 1]. Assume:

  1. Fulm (B; I) ≥ θF implies GI (m, B; I) > 0,

  2. Surm (B; I) ≥ θS and SelfC(m; I) ≥ θC imply GT (m, B; I) > 0.

Then if m undergoes a beauty episode with B on I in the sense that Beaut(B) is designated and
SelfC(m; I) ≥ θC , it follows that Repm (B; I) is OEI-active.

Proof. If Beaut(B) = Ful(B) ∧ Sur(B) is designated, then both Ful(B) and Sur(B) have designated
truth components, hence Fulm (B; I) ≥ θF and (after rescaling) Surm (B; I) ≥ θS for suitable corre-
sponding numeric thresholds. By assumptions (1) and (2) and SelfC(m; I) ≥ θC , we get GI > 0 and
GT > 0. Thus Repm (B; I) is OEI-active by Definition 409. In other words, the designated status of
Beaut(B) forces both constituents—fulfillment and surprise—to be present to a model-dependent
but nontrivial degree (captured by θF , θS ), and the OEI-activity condition is triggered precisely
because the growth terms GI , GT are required to be strictly positive rather than merely nonneg-
ative. The “after rescaling” clause is included to emphasize that Surm (·) may be measured on a
different natural scale than Fulm (·) (e.g. entropic novelty versus reward-like satisfaction), yet the
designatedness constraint can still be pushed down to a single inequality by choosing a monotone
calibration map and an appropriate θS .

Remark 1350. This theorem is intentionally a “sanity theorem”: it shows that the ontology can
formalize Hyperseed’s claim that beauty is tied to open-ended intelligence (individuation + self-
transcendence) without requiring a single reductionist scalar. Stronger results can be obtained once
specific models of GI , GT , SelfC are chosen. In particular, the point is not that Beaut equals any one
quantitative score, but that the logical structure of beauty-as-“surprising fulfillment” can be made to
entail (via thresholding) the activation of a representation subnetwork with both individuative and
transcendent growth directions. Accordingly, the theorem isolates the minimal commitments needed
for the implication Beaut(B) ⇒ “OEI-active representation”: designatedness of the conjunction,
and positivity of the growth terms under adequate self-coherence.




                                                  543
24.9    Archetypes, art, and religion as communion technologies
Hyperseed treats archetypes as patterns that occur surprisingly often across a collection of systems
but with diverse instantiations, and treats art as something with strong aesthetic effect. A natural
ontology-level synthesis is: artifacts and rituals are pattern carriers that can induce cross-mind
patterns, thus facilitating communion. Here “pattern carrier” is intended broadly: it includes
not only static objects (images, texts, buildings) but also repeatable procedures (chants, dances,
liturgies) whose execution can synchronize attention, affect, and interpretation across a group.
The central technical idea is that such carriers can be analyzed in the same language as other
representational substrates, by tracking how they change cross-supported intensities and thereby
shift communion margins.
Definition 410 (Archetype as a cross-context pattern template). Fix a class of systems (minds,
texts, cultures, etc.) indexed by J. An archetype is a template τ together with an instantiation
map sending each j ∈ J to a (possibly empty) set of instantiations Instj (τ ), such that:
  1. τ has high support across J (many j have Instj (τ ) 6= ∅), and

  2. the typical instantiations are diverse (not near-copies), and

  3. the support is “surprising” relative to the description complexity of τ (e.g. high occurrence
     despite nontrivial κ(τ )).
Intuitively, (1) captures the “recurrence” aspect of archetypes, (2) rules out trivial replication effects
(e.g. a single meme copied verbatim), and (3) is the anti-tautology constraint ensuring that τ
is neither so vague that it matches anything nor so simple that high frequency is automatically
expected. Depending on application, “diverse” can be operationalized via a distance on instantiations
(semantic, structural, stylistic), and “surprising” can be operationalized via deviation from a null
model on J in which occurrences are generated independently of τ ’s internal structure.
Remark 1351. A useful way to read Definition 410 is as a three-way tension: increasing κ(τ )
typically decreases baseline occurrence under simple generative priors, so an archetype is precisely
a template whose empirical support remains high despite that penalty. This aligns the informal
“archetypal” notion (recurring forms that feel deeper than coincidence) with a quantitative perspec-
tive in which recurrence is evaluated against compressibility and expected frequency.
Definition 411 (Art as an intersubjective pattern carrier). Fix a class of experiencers X ⊆ Mind.
An art object A (relative to X ) is any entity such that, for many m ∈ X , encountering A induces
a designated beauty proposition Beaut(A) in m’s valuation. Equivalently, it induces a high rate
of beauty episodes in the population X . Because Beaut(·) lives in a paraconsistent setting, this
criterion allows that some experiencers may also (simultaneously) assign non-designated or even
conflicting evaluations to A without preventing A from counting as an art object relative to X , so
long as the designated-beauty response is sufficiently widespread. The explicit relativization to X is
meant to capture the familiar phenomenon that what functions as art for one community may not
function as art for another, not merely due to preference but due to differences in learned perceptual
and interpretive repertoires.
Definition 412 (Communion capacity of an artifact). Fix a community C and interval I, and let
A be an artifact jointly attended to by the community on I. Define the communion capacity of A
for (C, I) as the expected change in communion margin:
                                         h                                   i
                     ΓComm (A; C, I) := E ∆Comm (C, I; wA ) − ∆Comm (C, I; w) ,

                                                   544
where w is the baseline intensity datum and wA is the datum after (or during) joint participation in
A, and the expectation is over relevant internal stochasticity and contextual variation. The quan-
tity ΓComm is therefore an intervention effect: it isolates the marginal contribution of adding joint
participation in A to the community’s dynamics, holding fixed (in expectation) other sources of fluc-
tuation. In particular, ΓComm (A; C, I) may be negative for artifacts that fragment interpretation or
intensify within-mind idiosyncrasy more than cross-mind alignment, so the sign of ΓComm functions
as a formal separator between communion-promoting and communion-eroding interventions.

Proposition 40 (Broadly beautiful artifacts tend to have positive communion capacity). Assume:

  1. Joint attention to an artifact A creates at least one cross-supported pattern (a shared repre-
     sentation, shared affective response, shared narrative token, etc.) with intensity increasing in
     the number of participants who undergo a beauty episode with A.

  2. Within-mind intensities are not increased by joint attention to A faster than cross-mind in-
     tensities (i.e. the dominant new patterns created by joint participation are cross-supported).

Then for communities drawn from a population in which A is an art object (Definition 411), we
have ΓComm (A; C, I) > 0 for a substantial measure of (C, I). The “substantial measure” clause
is meant to exclude degenerate cases (e.g. communities of size one, or intervals too short for any
shared pattern to form) while not requiring universality across all possible C and I; it is enough
that the positive effect persists across a non-negligible region of typical group compositions and
engagement durations.

Proof. Under assumption (1), the probability that multiple members of C undergo beauty episodes
with A implies creation of cross-supported patterns with positive intensity, increasing Wcross . As-
sumption (2) ensures the within-mind total does not outgrow the cross-supported total under this
intervention. Therefore ∆Comm increases in expectation, giving ΓComm (A; C, I) > 0. More explic-
itly, when A is an art object for the ambient population, draws of (C, I) from that population have
a nontrivial chance that several members of C will instantiate designated Beaut(A) during I; by (1)
this increases at least one cross-supported component of the intensity datum, so wA differs from
w by adding (or amplifying) cross-linked structure. Condition (2) prevents this amplification from
being offset by a larger (or faster) growth in purely within-mind intensities, so the net effect on the
communion margin remains positive on average under the stated expectation.

Remark 1352. This proposition is the formal core of a qualitative Hyperseed theme: art and
ritual can function as reliable methods for inducing communion, hence as social technologies for
shaping intersubjective realities. In this framing, the reliability is not mystical but statistical: if an
artifact robustly elicits designated beauty episodes across a class of experiencers, then joint exposure
predictably increases the weight of cross-supported patterns (shared interpretations, shared affect,
shared narrative anchors), which is exactly the structural move required for communion as measured
by ∆Comm . This also clarifies why the same artifact can fail to produce communion in some settings:
if the induced increments concentrate in within-mind idiosyncratic elaborations rather than in shared
tokens, assumption (2) can fail and ΓComm can be small or negative.

24.10    Religion, ritual, and state-dependent science
Hyperseed treats religion as a system of cultural beliefs and social roles associated with spiritu-
ality within a society, and treats “state-dependent science” as science relative to observation-sets
accepted broadly within a community while they are in particular states of consciousness. In this


                                                   545
framing, “religion” is not reduced to propositional doctrine alone; it also includes institutional roles,
pedagogies, calendars, and shared interpretive practices that shape how spiritual episodes are rec-
ognized, narrated, and transmitted. Likewise, “state-dependent” is meant in a precise epistemic
sense: it marks a restriction of the evidential interface (what counts as an observation) and of the
community’s background constraints (what counts as a permissible inference) to those intervals in
which the relevant state predicate is satisfied. The intent is not to grant automatic authority to any
such state, but to make explicit that many communities already operate with tacit state-conditions
(e.g. prayer, meditation, fasting, liturgical participation) that filter both experience and evaluation.
    The ontology-level reading is that:

   • Religions are persistent, socially stabilized pattern systems that (among other things) scaffold
     repeated access to spiritual communion (Definition 402), making such episodes more frequent
     and more explicit (Definition 400). This includes stabilizing a repertoire of symbols, narra-
     tives, and practices that lower the activation threshold for communion-relevant patterns and
     provide socially shared “handles” for interpreting them. In particular, the persistence of a
     religion can be understood as a kind of cultural memory that preserves the conditions under
     which communion has been historically attainable, even when individuals’ private access is
     intermittent.

   • Rituals are repeated procedures that reliably increase cross-supported pattern intensity, thereby
     tending to push a community toward Comm and sometimes ExplComm. Here “procedure” is
     meant broadly: bodily synchrony, chanting, call-and-response, incense, architectural acous-
     tics, and coordinated attention can all function as controllable parameters that increase mu-
     tual predictability and shared salience. On the present ontology, a ritual’s efficacy is therefore
     not primarily a matter of private belief, but of interlocking supports that raise the intensity
     of patterns that are jointly tracked, jointly enacted, and jointly reinforced.

   • State-dependent science is an epistemic practice internal to an intersubjective reality-system
     that is conditioned on particular community states; formally, it is ordinary science carried
     out on a restricted subdomain of intervals I satisfying a state predicate Σ(I). The restriction
     to Σ(I) should be read as a domain restriction rather than a suspension of ordinary epistemic
     norms: within the selected intervals one still compares models, checks predictiveness, and ne-
     gotiates intersubjective agreement, but one does so using the observation-sets and inferential
     affordances that are actually available in those states. In this sense, the proposal parallels
     familiar cases where instruments or training open new observation channels, except that the
     “instrument” is partly constituted by communal state and practice.

Definition 413 (State-dependent science schema). Fix a community C and a state predicate Σ
selecting intervals I (e.g. “oceanic state”, “I-Thou state”, “high compassion resonance”). A state-
dependent science for (C, Σ) is a family of model-building procedures that, restricted to intervals
I with Σ(I), produces predictive/causal models of observation-sets that are accepted broadly by
members of C in those states.

    The schema is intentionally permissive about what counts as a “model-building procedure.”
In some cases the procedures may look like familiar experimental cycles (induction, controlled
variation, replication, and error analysis), while in others they may be closer to disciplined phe-
nomenological reporting with structured elicitation protocols and inter-rater calibration. The key
constraints are (i) the restriction to Σ-intervals is explicit, (ii) the outputs are not merely idiosyn-
cratic but admit communal uptake, and (iii) there is some articulated sense in which the resulting


                                                  546
models succeed or fail relative to the observation-sets available under Σ. In particular, the ac-
ceptance clause is meant to exclude purely private revelation from counting as “science” in this
narrow technical sense, unless it is embedded in practices that render its contents intersubjectively
assessable within C.

Remark 1353. This definition is intentionally schematic; it exists to locate the concept inside the
ontology. Filling it out requires specifying: the observation algebra, the acceptance criterion, and
how altered states modify the available observation channels and inference biases.

    A useful way to read “observation algebra” in this setting is as the community’s formal or in-
formal account of which experiential discriminations are admissible as stable observables under Σ,
and which combinations, comparisons, and transformations of those observables preserve meaning.
For example, a tradition might treat certain affective contours, attentional unifications, or rela-
tional gestalts as reliably reportable only after training; that training then functions analogously to
calibration in laboratory practice. Similarly, altered-state inference biases need not be understood
only as sources of error; they may also function as structured priors that are appropriate to the
restricted domain (though they can mislead when exported outside it). On the present view, the
main methodological risk is equivocation between domains: treating claims stabilized under Σ as
if they were validated over all intervals, or conversely dismissing Σ-restricted regularities simply
because they do not appear in the complement domain.

24.11    Summary and forward links
We have given:

   • a community pattern-system definition of intersubjective reality (Definition 395);

   • a quantitative criterion for intersubjective communion via cross-supported pattern dominance
     (Definition 397);

   • a formalization of explicit communion via self-model recognition using uncertain paraconsis-
     tent truth values (Definition 400);

   • a scope-based definition of spiritual communion and an intervention-based definition of en-
     theogen (Definitions 401–403);

   • emotion and compassion as mind-body-and-community patterns (Definitions 404–405);

   • beauty as paraconsistent conjunction of fulfillment and surprise and a non-explosion theorem
     explaining why this is coherent (Theorem 21);

   • a minimal theorem linking beauty episodes to OEI-activity of the representing subnetwork
     (Theorem 22);

   • archetypes, art, and ritual as cross-mind pattern carriers with positive communion capacity
     (Definitions 410–412, Proposition 40);

   • a schema locating religion and state-dependent science as persistent community-level pattern
     practices (Definition 413).

    Taken together, these items supply a single “ladder” from ontology to practice. At the base, in-
tersubjective reality is treated as neither a private mental construction nor an observer-independent


                                                 547
substrate, but as what is stabilized when multiple agents participate in and reinforce a shared pat-
tern system. The communion criteria then provide a way to distinguish mere agreement (e.g.,
coincidental similarity of reports) from structural coupling in which patterns become mutually
sustaining across minds and media.
    The progression from intersubjective communion to explicit communion clarifies the role of
reflexivity: explicit communion is not only that agents co-enact compatible patterns, but that their
self-models (and their models of others) register this co-enactment under truth values that may be
incomplete or even locally inconsistent. The use of uncertain paraconsistent valuations is thus not
a stylistic choice but a technical mechanism for allowing realistic cognitive states—where agents
can partially endorse and partially reject the same proposition—without trivializing the overall
inferential system.
    The scope-based definition of spiritual communion and the intervention-based definition of en-
theogen can be read as a controlled extension of the communion framework to cases where (i) the
relevant pattern web extends beyond ordinary interpersonal exchange (scope enlargement), and (ii)
there exist interventions that systematically alter the salience, accessibility, or binding of patterns
in w and in the agent valuations. This framing makes it possible to compare “spiritual” episodes
to other kinds of high-scope communal episodes (scientific, artistic, political) using the same un-
derlying vocabulary while still marking where special interventions or altered state dynamics are
doing explanatory work.
    Emotion and compassion enter as patterns precisely because they mediate between internal
valuation updates and outwardly observable coordination. In this setting, emotions are not merely
“inner feelings” but structured, learnable, and socially conditioned pattern complexes that affect
attention, memory, and action selection; compassion is then a special case with characteristic
coupling properties (e.g., tendencies to align the welfare-related evaluations of self and other),
which makes it directly relevant to communion as a stabilizing or destabilizing force depending on
context.
    The aesthetic items connect evaluation to coherence under contradiction. Defining beauty as
a paraconsistent conjunction of fulfillment and surprise formalizes an everyday phenomenology—
that the beautiful often both “fits” and “exceeds” expectation—while the non-explosion theorem
guarantees that allowing such conjunctions does not collapse the logic into triviality. The OEI link
then supplies a minimal dynamical bridge: beauty episodes are not only definitional artifacts of a
valuation scheme, but correlate with identifiable activity of the representing subnetwork, which is
the sort of claim needed for later empirical contact (e.g., computational or neurocognitive modeling).
    Archetypes, art, and ritual are positioned as portable pattern carriers that can propagate and
synchronize across individuals, timescales, and media. Their “communion capacity” is the key
functional notion: it identifies when a carrier does not merely transmit content but tends to increase
cross-support among participants’ patterns (including affective and normative patterns), thereby
enhancing the conditions under which communion predicates are satisfied. Finally, the schema for
religion and state-dependent science frames both as persistent community-level pattern practices:
each involves stabilized methods of generating, selecting, legitimating, and teaching patterns, and
each can be analyzed in terms of the same underlying machinery while differing in their typical
interventions, scopes, and validation dynamics.
    In later sections, these constructions can be specialized by: (i) choosing concrete pattern lan-
guages and complexity measures (linking to weakness/MDL formalisms), (ii) choosing explicit dy-
namical models for how artifacts and rituals modify w and the valuations vm , and (iii) connecting
repeated communal practice to habit formation (morphic resonance) as a long-run stabilizer of
intersubjective pattern webs.
    Concretely, item (i) determines what counts as a “pattern” in the first place and how compet-

                                                 548
ing descriptions are penalized or preferred; this is where the abstract pattern-system talk acquires
operational bite, since the same empirical stream can admit multiple encodings with different com-
plexity profiles. The MDL/weakness link is especially important here because it yields a principled
way to trade off expressivity and generalization, making intersubjective stabilization a matter of
converging on pattern sets that are jointly compressive under shared constraints.
     Item (ii) then fixes the time-evolution story: the definitions above specify relational and logical
conditions, but dynamical models specify mechanisms by which those conditions arise, persist, or
fail. In particular, modeling how artifacts and rituals modify w and the valuations vm makes
it possible to distinguish (a) mere informational transmission from (b) systematic reweighting of
saliences, priorities, and inferential pathways. This also clarifies how the same ritual form can have
different communion outcomes depending on parameter regimes (e.g., strength of coupling, noise
levels, or the degree of paraconsistent tolerance in participants’ valuation dynamics).
     Item (iii) provides the long-horizon glue: repeated practice does not only reinforce explicit
beliefs but also trains priors, attentional habits, and default interpretive moves, thereby shaping
the background conditions under which future communion is more or less likely. Casting this
as habit formation (morphic resonance) supplies a way to model persistence at the community
timescale without requiring that every episode of communion be re-constructed from scratch; in-
stead, stabilized pattern webs can be treated as attractors that new participants enter and that
existing participants revisit, with the possibility of drift, bifurcation, or sudden reconfiguration
under strong interventions.


25     Reality-systems, cosmos, multiverse, and eurycosm
This section scales Hyperseed’s observer-relative ontology outward. Earlier sections developed
the formal core (paraconsistent evidence, quantale weakness, and compositional model/process
structure) and used it to formalize patterns, habits, and resonance (cf. [1, 5, 3]). Here we use the
same primitives to define:
(i) empirical reality as predictive usefulness to a mind over an interval;
(ii) reality-systems as stabilized networks of mutually predictive entities/patterns;
(iii) physical reality and body as a particular reality-system with a privileged sensorimotor interface;
(iv) cosmos/universe as an observer- and signal-class-indexed reachability notion;
(v) multiverse and guidable multiverse as (controlled) stochastic evolution on universes;
(vi) the Yverse as a recursive limit of multiverse towers (best treated paraconsistently);
(vii) the eurycosm and near eurycosm as the “wider world” beyond any single well-defined mind
or universe; and
(viii) optional speculative anchors: the anthropic principle and big-bounce cosmology.
     To motivate the ordering of (i)–(viii), it is helpful to view the constructs as successive closures
of the same operational loop: a mind conditions on evidence, makes predictions, and adjusts its
internal models/processes; “reality” is then whichever parts of this loop remain stable enough to
support compression and counterfactual reliability across time. In this sense, the section does
not introduce new metaphysical primitives so much as new scales at which the same inferential
machinery is applied: from short-horizon usefulness (empirical reality) to long-horizon mutual
stabilization (reality-systems), then to reachability under constraints (cosmos/universe), then to
stochastic families of such reachability structures (multiverse towers), and finally to limiting con-
structions intended to capture what remains when no single observer-indexed universe is taken as
final (Yverse, eurycosm).
     A practical reading is that each definition below will be paired with an “operational test” of the


                                                  549
form: what evidence is admissible, what predictions are counted, what closure operator is being
used, and what is treated as a fixed point or attractor. This makes the terminology functional:
for instance, whether some entity belongs to a reality-system is not a binary metaphysical decree,
but a question about whether it participates in sufficiently strong mutual predictability with other
entities (relative to the mind, the time interval, and the permitted evidence transformations).

Remark 1354. Conceptually, the aim is to keep the metaphysical vocabulary honest by tethering
it to explicit operations: conditioning, prediction, closure, reachability, and fixed points. One may
read this as a Russell-style attempt to replace vague nouns (“the real,” “the universe”) by precise
relations between a mind and its prospective experience, without thereby denying that there can be
a world that exceeds any one mind. In Hyperseed’s idiom, the exceeding is captured not by a single
absolute set, but by a family of observer-indexed constructions and their limits.

    The emphasis on reachability and fixed points is not accidental: many of the objects named in
this section can be presented as solutions to recursive equations (e.g., “the smallest closed structure
containing what the mind can stably track,” or “the maximal set of states reachable given a class
of signals and updates”). When the recursion is well-founded and convergent, classical set-based
reasoning can suffice; when the recursion is open-ended (as in multiverse towers or the Yverse),
paraconsistent treatment is advocated so that one can work with partially specified limits without
trivializing the theory in the presence of inevitable self-reference and boundary ambiguities.
Hyperseed concepts covered here. Empirical reality / reality-systems (??, 149); physical
reality and body (135); algebraically asymmetric physical reality (55); cosmos/eurycosmos (89,
??); universe, multiverse, guidable multiverse, Yverse (116, 209); eurycosm and near -eurycosm
(??); anthropic principle (57); big bounce (66).
    For orientation, “signal-class-indexed” in (iv) anticipates that a mind’s accessible universe may
depend not only on its internal inferential capacities but also on which channels of interaction
are counted as legitimate interventions or observations (e.g., a restricted sensor suite versus an
augmented one, or a narrower versus richer class of admissible measurements). Likewise, the
“privileged sensorimotor interface” in (iii) should be read as a structural asymmetry: the body is
not merely another predicted object, but the particular interface through which prediction errors
arrive and actions are issued, thereby shaping the update dynamics that define empirical reality
and reality-systems in the first place.
    Finally, the “optional speculative anchors” in (viii) are included as interpretive touchpoints
rather than as load-bearing axioms: they indicate how Hyperseed-style definitions might interface
with familiar cosmological and selection-effect discussions without presupposing that any single
cosmological narrative exhausts the eurycosm. In particular, the near eurycosm is intended to name
those aspects of the “wider world” that remain robust across a broad range of observer-indexed
constructions, even when the full eurycosm is treated only via partial, limit-like characterizations.

25.1    Empirical reality as predictive usefulness
Hyperseed characterizes “empirically real” in explicitly operational terms: roughly, something is
empirically real to a mind over a time interval insofar as perceiving it improves that mind’s predic-
tions about its future. To formalize this, we separate (a) entities/patterns that may be perceived
and (b) the prediction task induced by the mind’s ongoing coupling to its environment. This framing
treats “reality” as a role played inside an inferential control-loop: what matters is whether incor-
porating a candidate distinction measurably improves forward-looking performance, not whether
the distinction is metaphysically primitive or phenomenologically forceful.


                                                 550
Definition 414 (Entities and perceptions). Fix a mind (or observer) M and an interval of (proto-
)time I. Let U be a set of entities, situations, or patterns that M may treat as objects of perception.
We represent “perceiving x ∈ U” over the interval I by an observation token obsI (x).

Remark 1355. The notation here is deliberately spare. The set U is not assumed to be “the set of
all things that exist”; it is merely the repertoire of candidate distinctions available to the mind M
in the context at hand. Likewise obsI (x) is a token standing for the event “M has (somehow) taken
in x during I,” not a claim that x is thereby known with certainty. The proto-time interval I is
the minimal temporal scaffolding needed to speak of “future observations”; it matches the Hyperseed
emphasis that time may be mind- and process-relative (see Hyperseed-Concept 142).

Remark 1356. A useful way to read obsI (x) is as an interface variable rather than a raw datum:
it stands for whatever internal representation M actually makes available to its predictor. Thus,
two minds may share the same external stimulus while having different x-tokens (different feature
sets, categorizations, or attention policies), and consequently different empirical realness scores for
“the same” ostensible thing. This observer-indexing is not a bug in the framework; it is the intended
mechanism by which Hyperseed makes “empirical reality” a property of mind–world coupling rather
than a view-from-nowhere.

Remark 1357. A simple example is to let U contain items like “the traffic light is red,” “the stove
is hot,” “my colleague looks annoyed,” or “this symbol-string has the form of a proof.” Then obsI (x)
is an abstract placeholder for whichever perceptual/interpretive process produces that classification.
The definition is useful because it lets us discuss reality in terms of what changes in the mind’s
predictive situation when such a token is available, without taking a stand on whether the token
came from a retina, a dream, a telescope, or a theorem-prover.

Definition 415 (Observer-indexed prediction loss). Let FI denote a space of future observation
streams relevant to M on the next interval (e.g. I + ). A predictor for M is a map ΠM that assigns
to each current informational state a predictive distribution over FI . Let L be a bounded loss
function comparing predicted to realized futures. Define the expected prediction error of ΠM on I
by                                                              
                                 ErrI (ΠM ) := E L(ΠM , future) .                              (1)
If M conditions on perceiving x, write ΠM | obsI (x) and ErrI (ΠM | obsI (x)).

Remark 1358. The symbol FI is a space of possible “next-step” futures as M encodes them: e.g.,
strings of sensor readings, sequences of internal thoughts, or higher-level events. The predictor
ΠM is left abstract on purpose: it may be Bayesian, neural, symbolic, hybrid, or something else.
The expectation E[·] is taken with respect to the distribution over futures that actually governs
M ’s coupling to the world (whatever that means in the model). Boundedness of L is a technical
convenience ensuring the expectation exists and that normalizations below behave well.

Remark 1359. The phrase “current informational state” can be understood broadly to include:
memory traces, latent beliefs, currently attended features, and any background context that persists
through I. In this sense, conditioning on obsI (x) does not assert that x is the only input to
prediction; it isolates the marginal contribution of having x available on top of whatever else M
already carries. One can therefore interpret ErrI (ΠM ) − ErrI (ΠM | obsI (x)) as an operational proxy
for “how much x helps, given the rest of M .”

Remark 1360. As an example, suppose L is log loss and ΠM outputs a probability distribution over
the next sensory frame; then ErrI (ΠM ) is a cross-entropy-like quantity measuring how surprised M

                                                 551
is, on average, by what happens next. Conditioning on obsI (x) corresponds to giving the predictor
access to a feature x (“I see smoke”), and the resulting change in error formalizes the pragmatic
sense in which perceiving x makes the world more navigable. This is precisely the Hyperseed-Concept
?? cast in a predictive mold.

Remark 1361. In the special (idealized) case where ΠM is the Bayes-optimal predictor for M ’s true
generative coupling and L is log loss, the expected reduction in loss from conditioning on x admits
an information-theoretic reading: it coincides with an expected log-likelihood ratio and is closely
related to the mutual information between obsI (x) and the next-step future in FI . This highlights an
intended interpretation of “empirically real” as “carries compressive, future-relevant information for
this mind,” while still allowing non-log-loss settings where other operational desiderata (calibration,
squared error, asymmetric costs, safety margins) matter more than pure information gain.

Definition 416 (Empirical realness score). Fix a small constant δ > 0. The empirical realness of
x ∈ U to mind M on interval I (relative to predictor ΠM and loss L) is

                                           ErrI (ΠM ) − ErrI (ΠM | obsI (x))
                             ρM,I (x) :=                                     .                      (2)
                                                    ErrI (ΠM ) + δ

Thus ρM,I (x) is high when conditioning on x yields a large relative reduction in prediction loss.

Remark 1362. The fraction defining ρM,I (x) is a normalized error reduction. The numerator is the
improvement in expected predictive performance when x is perceived; the denominator ErrI (ΠM ) + δ
prevents division by zero and makes the score scale-comparable across regimes where overall predic-
tion is easy or hard. In particular, ρM,I (x) can be negative: an observation token that systematically
misleads the predictor (say, due to illusion, biased interpretation, or adversarial manipulation) will
increase error rather than decrease it.

Remark 1363. Because L is bounded, ρM,I (x) is also controlled in magnitude (though not neces-
sarily confined to [−1, 1] under this particular normalization). Concretely, if 0 ≤ L ≤ Lmax , then
0 ≤ ErrI (ΠM ) ≤ Lmax and the numerator lies in [−Lmax , Lmax ], giving the crude bound

                                    Lmax                        Lmax
                           −                  ≤ ρM,I (x) ≤                .                         (3)
                               ErrI (ΠM ) + δ              ErrI (ΠM ) + δ

This makes explicit the role of δ as more than a division-by-zero patch: it also prevents extreme
blow-ups when ErrI (ΠM ) is very small (i.e., when the mind is already in an easy-to-predict regime).
In applications, δ may be chosen to reflect a minimum meaningful scale of predictive error (a noise
floor) below which additional “improvement” should not count as large empirical realness.

Remark 1364. The score ρM,I (x) is explicitly relative to a predictor ΠM . This is intentional: if
M uses a systematically mis-specified predictor, then even perfectly reliable cues may fail to improve
its forecasts, yielding low measured realness in practice. In that sense, empirical realness here is not
only about the environment; it is also about the competence and inductive biases of the mind. This
matches the Hyperseed stance that “world” and “knower” cannot be fully separated when reality is
cashed out operationally.

Remark 1365. Two instructive examples:

(a) If x is “the kettle is whistling” and the future includes “steam will appear,” then conditioning
    on x can sharply reduce error, giving ρM,I (x) > 0.


                                                    552
(b) If x is “I am certain this random sequence has a hidden message” but this belief leads to
    consistently wrong anticipations, then ρM,I (x) may be < 0 even though the experience feels
    compelling.
This illustrates why Hyperseed refuses to identify the real with the merely vivid: empirical realness
is tied to the predictive economy of the mind-world coupling, not to a phenomenological intensity
taken in isolation (cf. Hyperseed-Concept ??).
Remark 1366. The time-indexing by I matters. Some tokens x can be locally predictive (high
ρM,I (x)) while degrading longer-horizon performance if they incentivize brittle policies or overfit-
ting to short-lived regularities. Conversely, some distinctions may appear useless on a single step but
become empirically real over extended horizons (e.g., slow variables, latent traits, stable causal mech-
anisms). A natural extension is therefore to consider multi-interval aggregates such as ρM,[I1 :IT ] (x)
defined by replacing ErrI with an averaged or discounted error across a sequence of proto-time steps,
which better captures the pragmatic persistence often associated with “real objects.”
Remark 1367. Finally, nothing in the setup restricts x to being atomic. In many cognitive and
scientific settings, empirical traction comes from bundles of cues (joint features, models, or hy-
potheses) that are only predictive together. One may therefore treat x as a structured object (e.g., a
tuple, a submodel, or a learned representation) or generalize the conditioning event to a set S ⊆ U
by writing ΠM | obsI (S) for “M has access to all tokens in S on I,” enabling a notion of incremen-
tal realness (marginal contribution) and synergy (non-additive gains) within the same operational
framework.
Remark 1368 (Paraconsistent evidence). The scalar ρM,I (x) measures predictive utility, not logi-
cal certainty. If one wishes, one may lift ρ to a p-bit value by tracking (i) evidence that conditioning
on x improves prediction and (ii) evidence that conditioning on x worsens or destabilizes predic-
tion. This is compatible with Hyperseed’s tolerance for borderline and inconsistent boundaries, and
connects naturally to paraconsistent valuation frameworks such as Constructible Duality Logic [23]
and resonance-based paraconsistent semantics [24].

25.2    Reality-systems as stabilized mutually predictive pattern complexes
Hyperseed motivates “reality” as a property of systems of entities rather than isolated objects.
The circularity in the slogan “x is real if perceiving it helps predict real things” is not a bug; it
indicates a fixed-point structure. We now package this via a closure operator on subsets of U.
Definition 417 (Predictive adjacency at threshold). Fix M, I and a threshold θ ∈ (0, 1). Define a
directed relation →θ on U by setting

                                   x →θ y    iff   ρM,I (x → y) ≥ θ,                                (4)

where ρM,I (x → y) is a chosen score measuring how much conditioning on obsI (x) improves predic-
tion of observation tokens associated with y. (Concrete choices include conditional loss reduction
restricted to features belonging to y.)
Remark 1369. The symbol →θ is a thresholded “predicts” relation: x →θ y means that, at the
selected confidence level θ, access to x makes y more predictable. The auxiliary score ρM,I (x → y)
is intentionally underspecified; it should be read as a directed version of the earlier ρM,I (x) that
focuses on the part of the future stream attributable to y. In a feature-based setting, one may take
y to denote a subset of coordinates of the future observation stream and compute loss reduction on
those coordinates only.

                                                   553
Remark 1370. A simple example: let U include weather-relevant tokens, and suppose x is “dark
clouds” and y is “rain within 10 minutes.” Then x →θ y holds for a fairly high θ in many climates.
By contrast, if x is “I had a particular dream” and y is “rain within 10 minutes,” the relation may
fail for typical observers, even if some observers attribute meaning to the dream. The definition
is useful because it turns “seems to go with” into a directed graph that can be closed and iterated,
preparing the ground for fixed-point constructions of reality-systems (Hyperseed-Concept 149).
Definition 418 (Forward/backward predictive closure). For R ⊆ U, define

                            Pred→ (R) := {y ∈ U : ∃x ∈ R s.t. x →θ y},                           (5)
                                 ←
                            Pred (R) := {y ∈ U : ∃x ∈ R s.t. y →θ x}.                            (6)

Define the mutual predictive closure operator

                                  F (R) := Pred→ (R) ∩ Pred← (R).                                (7)

Remark 1371. The operators Pred→ and Pred← are the one-step out- and in-neighborhood oper-
ators in the directed graph given by →θ . Thus:
• Pred→ (R) collects what R predicts;

• Pred← (R) collects what predicts R; and

• F (R) keeps only those nodes that stand in both relations to R.
The intersection is where the circularity enters: a candidate real set should not merely emit predic-
tions, nor merely be predicted; it should participate in a mutually supporting web.
Remark 1372. As a toy example, suppose U = {a, b, c, d} with edges a → b, b → a, b → c, c → b,
and d isolated. Then the mutually predictive closure of {a} yields {a, b} (and may further expand
to include c depending on the thresholded edges), while d never enters any nontrivial fixed point.
This makes vivid the intended metaphysical moral: isolated tokens that do not participate in stable
mutual prediction are, by this operational criterion, not part of a well-formed reality-system.
Lemma 5 (Monotonicity). The operator F : 2U → 2U is monotone: if R ⊆ R0 then F (R) ⊆ F (R0 ).
Remark 1373. Intuitively, monotonicity says: if you start with more candidate “real” items (a
larger seed set), then the set of things that are mutually predictively adjacent to it cannot shrink.
This is a minimal sanity condition for any closure-like operator and is precisely what we need to
invoke general fixed-point theorems later. In the logic of the development, this lemma is the hinge
connecting the empirical/predictive notions above to lattice-theoretic existence results below.
Proof. If R ⊆ R0 , then any witness x ∈ R for membership in Pred→ (R) or Pred← (R) is also in R0 .
Thus Pred→ (R) ⊆ Pred→ (R0 ) and Pred← (R) ⊆ Pred← (R0 ), hence their intersection is monotone.

Remark 1374. At a high level, the proof uses only the existential nature of the definitions: mem-
bership in Pred→ (R) is witnessed by the existence of some x ∈ R with an edge x →θ y. If R grows
to R0 , every old witness remains available, so the image can only expand. Geometrically, enlarging
a set of nodes in a directed graph cannot reduce its one-step neighborhoods.
Proof sketch. Unpack the definitions: both Pred→ and Pred← are built from an ∃x ∈ R condition.
Replacing R by a superset R0 preserves all witnesses, so each of the two neighborhood operators is
monotone, hence so is their intersection.                                                       

                                                554
Definition 419 (Reality-system (fixed-point form)). A reality-system for mind M on interval I
(at threshold θ) is a nonempty set R ⊆ U such that

                                             F (R) = R.                                            (8)

Elements of R are then “real relative to R” in the sense that they are both predicted by and predictive
of the rest of R (at least along some edges at the chosen threshold).
Remark 1375. The definition is intentionally parameterized by M , I, and θ to make explicit that
“what counts as mutually predictive” can depend on the observer, the temporal or contextual window,
and the granularity at which predictive links are deemed strong enough to count. In particular,
changing θ changes the edge set of →θ and therefore changes the fixed points of F ; one can view
θ as controlling the tradeoff between permissive “reality-systems” (low θ, many weak links) and
conservative ones (high θ, only robust links survive).
Remark 1376. The fixed-point condition can also be read as a closure principle: R contains exactly
those tokens that survive the operator F when applied to R itself. Equivalently, if one starts from
R and applies the “mutual predictability filter” encoded by F , nothing is gained and nothing is lost.
This makes F (R) = R a formal way to say that R is self-maintaining under the inferential norms
induced by →θ (for the chosen mind and interval).
Remark 1377. The fixed-point equation F (R) = R is the formal expression of the earlier circular
slogan. Rather than attempting to define “the real” by a one-directional reduction (from world
to mind or from mind to world), we define it as a stabilized relation between tokens inside a
predictive web. The requirement that R be nonempty prevents the trivial solution in which nothing
is real because nothing predicts anything.
Remark 1378. Nonemptiness also forces “reality” to pick out at least one informationally anchored
token, which matters when →θ is sparse or when the mind is in a regime where predictive links
degrade (e.g. noise, novelty, or adversarial inputs). Without the nonemptiness clause, the empty
set would always be a fixed point for many natural choices of F , and the theory would risk collapsing
into the claim that vacuity is always an available “reality-system”. The clause therefore functions
like a minimal coherence constraint: there must be at least some token(s) that participate in the
mutual-support structure.
Remark 1379. A practical example: in ordinary perception, the set R might include “solid ob-
jects,” “my hand,” “gravity,” “sound sources,” and so on, because these tokens support a dense
network of mutual predictability (touch predicts proprioception; object permanence predicts future
visual input; etc.). In a scientific sub-community, R might also include theoretical entities (fields,
genes, curvature) insofar as conditioning on them improves predictions of experimental outcomes.
This is a conceptual bridge to Hyperseed’s view of science as observer- and community-relative
model selection [20].
Remark 1380. This example can be sharpened by observing that the same underlying sensory
stream can support different stabilized sets depending on which auxiliary tokens the community
treats as eligible members of U (measurement conventions, inferential schemas, instrument readouts,
and mathematical constructs). On this view, disagreements about “what exists” often reduce to
disagreements about which tokens belong in the shared candidate universe and which predictive
relations clear the threshold θ under the community’s modeling practices. The fixed-point framing
makes those dependencies explicit without implying that reality is arbitrary: fixed points are still
constrained by the actual pattern of predictive relations.

                                                 555
Theorem 23 (Existence of minimal and maximal reality-systems). For any mind M and interval I,
the monotone operator F has a complete lattice of fixed points (ordered by inclusion). In particular
there exist:

(a) a least fixed point lfp(F ) (possibly empty),

(b) a greatest fixed point gfp(F ) (possibly all of U), and

(c) for any seed set R0 ⊆ U, a least fixed point containing R0 given by iterating F from R0 until
    convergence.

Remark 1381. The “least” and “greatest” qualifiers are with respect to inclusion, so lfp(F ) is
the smallest reality-system (if any) that satisfies the fixed-point constraint, while gfp(F ) is the
largest stabilized predictive web compatible with F . Interpreting fixed points as possible “worlds-as-
modeled,” the theorem guarantees both an extremal minimal commitment (take as real only what
must be in any fixed point) and an extremal maximal commitment (take as real everything that can
be stably included without breaking mutual predictive closure). This is useful later when comparing
conservative and expansive ontologies inside the same formal framework.

Remark 1382. Part (c) can be read as a procedure for “ontological bootstrapping”: begin with some
tokens treated as nonnegotiable (e.g. immediate experiences, measurement outcomes, or postulated
primitives), then repeatedly close under the mutual predictability operator until the process stops
changing the set. The resulting fixed point is the smallest stabilized reality-system that honors the
initial commitments R0 . This provides a clean way to formalize how different starting assumptions
can lead to different self-consistent stabilized webs even when F is held fixed.

Remark 1383. In plain terms, the theorem says that once we define “mutual predictive closure”
in a monotone way, reality-systems exist automatically: there is always a smallest self-consistent
predictive web and a largest one, and any initial guess can be iteratively refined to a stabilized
web. This is important because it shows that the fixed-point approach is not merely poetic; it is
supported by general order-theoretic machinery (Knaster–Tarski) rather than by ad hoc assumptions.
It also connects directly with later uses of fixed points in Hyperseed to study self-stabilizing systems,
including goal systems of self-modifying agents [10].

Remark 1384. The lattice-of-fixed-points perspective also highlights that reality-systems need not
be unique: there can be many distinct fixed points, partially ordered by inclusion. When multiple
fixed points exist, the formalism separates two questions: (i) which stabilized webs are possible
under the predictive relations encoded by F , and (ii) which one(s) are selected by a particular
mind or community, perhaps via pragmatic criteria (compression, robustness, intervention success)
not contained in the bare fixed-point equation. Thus, the existence theorem supplies the space of
candidates, while selection principles (if any) determine where within that lattice an actual observer
tends to land.

Proof. The powerset 2U is a complete lattice under inclusion. By Lemma 5, F is monotone, so
the Knaster–Tarski theorem implies that the set of fixed points of F is a complete lattice and that
least/greatest fixed points exist. If U is finite, then the ascending chain R0 ⊆ F (R0 ) ⊆ F 2 (R0 ) ⊆ · · ·
stabilizes in at most |U| steps at the least fixed point above R0 . In the infinite case, one may use
transfinite iteration or (under mild continuity assumptions) Scott-continuous fixed-point theory.

Remark 1385. The proof is a direct application of a general theorem: monotone endomaps on
complete lattices have fixed points, and in fact their fixed points themselves form a complete lattice.

                                                    556