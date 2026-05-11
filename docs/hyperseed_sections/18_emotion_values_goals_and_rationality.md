# 18 Emotion, values, goals, and rationality

• content that exists in local modules but is not globally broadcast.

We model this using a workspace closure operator. The intended separation is thus not between
two different ontological kinds of content, but between two regimes of functional connectivity:
some information remains encapsulated (local), whereas some is placed into a format that can be
consumed by many downstream processes (global).

Definition 231 (Workspace operator). A workspace operator is a monotone map

                                            W : VLOb → VLOb

intended to represent the effect of “global broadcasting” and “cross-module stabilization”: given an
integrated evidence state E, the workspace produces a refined state W (E) in which globally accessible
propositions may be mutually reinforced, disambiguated, or inhibited.

Remark 912. Notation check: VLOb denotes the set of all functions E : LOb → V, i.e. all evidence
states over the language. Thus W is an operator on evidence states. Monotonicity means: if E ≤ E 0
pointwise (every proposition has no less evidence in E 0 ), then W (E) ≤ W (E 0 ).
    Intuitively, W stands in for whatever mechanisms make some contents “globally present”: re-
current stabilization, cross-checking, binding, report preparation, etc. A very simple example is a
workspace rule that enforces a single implication “ϕ implies ψ”: it could map a state E to a new
state W (E) that increases E + (ψ) whenever E + (ϕ) is high. More generally, one can think of W as
encoding a family of (possibly soft) constraints among propositions in LOb that only become effective
once information is broadcast into a shared arena: consistency pressures, binding constraints (e.g.
linking a feature to an object), winner-take-most competitions, or normalization steps that reduce
ambiguity by distributing support across mutually exclusive hypotheses.
    The definition is useful because it packages all such cross-module interactions into one map, so
that consciousness can be analyzed as a property of the map’s fixed points rather than as a mysterious
extra ingredient. In particular, the map-based view allows one to ask structural questions about
the workspace independently of any specific module architecture: e.g. whether W tends to sharpen
evidence into stable patterns, whether it admits multiple distinct stable states (supporting a notion
of multistability), and how sensitive stable states are to small changes in the integrated input.
    It is also useful to note that this is deliberately stated at the level of a single-step operator. In ap-
plications, one may imagine iterating W (or iterating W interleaved with renewed integration) until
changes become negligible, and then treating the resulting stabilized state as the workspace-resolved
outcome. The fixed-point formulation below captures the equilibrium notion without committing to
any particular implementation of the iterative dynamics.

Remark 913 (What monotonicity means here). Monotonicity is the minimal sanity constraint:
if all modules provide at least as much positive/negative evidence for every proposition, then the
workspace should not reduce evidence. More sophisticated models may introduce inhibitory com-
petition via additional state variables, but the present reconstruction stays deliberately lightweight.
In this lightweight setting, inhibition is modeled (when needed) not by literally decreasing evidence
when inputs increase, but by how the workspace may preferentially increase some propositions more
than others in response to the same increment of input, thereby changing comparative salience while
preserving the basic “more in, no less out” ordering. This keeps the formalism compatible with the
idea that the workspace is a stabilizing broadcast mechanism rather than an adversarial filter that
destroys information.



                                                    358
Definition 232 (Conscious content as a fixed point). An evidence state E is workspace-stable if
W (E) = E. We define a conscious evidence state to be a workspace-stable state that is reachable
from module integration, i.e. of the form
                                
               E = W Γa (E• ) for some module collection E• and attention a.

Remark 914. The fixed-point condition W (E) = E is the formal avatar of “closure”: once the
content is broadcast and mutually adjusted, it does not immediately change under the same broad-
casting dynamics. In other words, a conscious evidence state is not merely a momentary aggregate,
but a self-consistent global posture of the system’s representational economy. This aligns with
the Hyperseed emphasis that consciousness is stabilized accessibility, not a raw data dump. The
additional reachability condition (being of the form W (Γa (E• )) for some inputs) prevents the def-
inition from treating every abstract fixed point of W as conscious: it ties workspace-stable states
to those that can actually be produced from the system’s modules under some attention allocation.
Conceptually, this separates “mathematical equilibria” from “attainable equilibria,” mirroring the
architectural idea that conscious contents arise from the interaction between what modules deliver
and what the workspace can stabilize and broadcast.
    Finally, note that the definition leaves open whether conscious states are unique: different atten-
tional settings a, or different module bundles E• (e.g. reflecting different sensory inputs or internal
memory retrievals), may lead to different workspace-stable outcomes. This provides a clean place to
later discuss phenomena like context dependence, priming, and multistable perception as differences
in which reachable fixed point (or approximate fixed point) is selected.
Remark 915. As an example, suppose W enforces that “if pain is present then I am aware of
pain” by boosting a proposition I(pain) whenever pain is supported (we implement this more explic-
itly below with introspection). One can think of this as a minimal “linking rule” from first-order
content to a matching higher-order access claim: W does not create pain evidence ex nihilo, but
it ensures that, once pain has become salient enough to enter the workspace dynamics, the corre-
sponding access marker is also made available for downstream use (e.g., for verbal report, control,
or memory routing). Then a workspace-stable state cannot have strong pain evidence but zero ev-
idence for awareness of pain; closure forces a consistency relation at the level of access. In this
sense, workspace closure behaves like an access-level coherence condition: it suppresses configura-
tions in which the system would be poised to act as if pain is present while simultaneously lacking
any globally available representation that it is aware of pain. This is intentionally weaker than
an identity claim between pain and awareness-of-pain; it is merely a constraint on which evidence
profiles can be stable once W has done its organizing work. The definition is useful because it lets us
separate two questions: (i) what modules compute and attention selects (Γa ), and (ii) what becomes
globally organized and reportable (W ). Equivalently, Γa concerns the formation and prioritization
of candidate contents, whereas W concerns the system-level integration that turns some of those
contents into accessible, mutually supporting commitments that can guide centralized decision and
communication.
Remark 916 (Conscious vs unconscious). Given a workspace-stable state E, one can define (for
a chosen threshold θ ∈ (0, 1)) the conscious proposition set

                                 Conθ (E) := {ϕ ∈ LOb : E + (ϕ) ≥ θ}

and treat the complement as “unconscious” at that moment. Formally, Conθ (E) is monotone in
the expected direction: if θ0 > θ then Conθ0 (E) ⊆ Conθ (E), so raising the bar yields a stricter notion
of what counts as conscious. This allows one to model “degrees” of access without changing the

                                                  359
underlying evidence state: the same E can support a thin conscious set (high θ) or a thick one (low
θ), depending on how demanding we want the operational criterion to be. This is not meant as a
metaphysical claim; it is a modeling move that operationalizes the conscious/unconscious boundary
in observer-relative terms. In particular, the threshold is a tool for linking the graded internal
quantities E + (ϕ) to binary behavioral predicates (e.g., “reportable now” or “available for deliberate
choice”) that often appear in experiments and in ordinary descriptions.

Remark 917. The thresholding move is deliberately pragmatic: it turns graded evidence into a
crisp set that can be used to define reports, action conditions, or “what is currently in mind”. It
also makes explicit that the model is not committed to a sharp boundary in the mechanism itself:
the sharpness is introduced by the analyst as a way to interface a continuous internal description
with discrete explanatory targets such as yes/no report, categorical memory encoding, or rule-based
action selection. Different observers or modeling contexts may choose different θ, reflecting dif-
ferent granularities of introspective access and different criteria for “present to experience.” For
example, a coarse-grained behavioral readout may justify a higher θ (only very strong evidence
counts as conscious), while a fine-grained phenomenological or neural readout may justify a lower
θ (allowing weak but systematic availability to count). This observer-relativity is not a bug: it is
consistent with the broader Hyperseed stance that many ontological boundaries are context-indexed
constructions rather than absolute partitions. In that spirit, the model can also accommodate in-
termediate categories (e.g., “fringe” or “preconscious” contents) by considering multiple thresholds
or by tracking how close E + (ϕ) is to θ, without changing the underlying definition of workspace
stability.

17.3     Reflective consciousness as higher-order representational closure
Hyperseed distinguishes ordinary consciousness from reflective consciousness. The simplest way to
capture the difference is:

• ordinary consciousness: workspace-stable integration of world/body/internal content;

• reflective consciousness: workspace-stable integration that includes meta-content about the agent’s
  own representations and attention.

Remark 918. This contrast parallels a familiar philosophical distinction between merely having
experiences and also taking oneself to be having them. But the present reconstruction refuses to
treat this as an unanalysable “light” added on top of cognition. Instead, reflective consciousness
is characterized by adding a further layer of representational tokens and requiring that the global
workspace stabilize including those tokens. In Hyperseed terms, reflective consciousness is a par-
ticular kind of stable self-reference enabled by paraconsistency rather than forbidden by it (compare
Hyperseed-Concept 84 and 166).

17.3.1    Adding a reflective layer
Introduce a syntactic operator I(·) producing “introspective” propositions. For each ϕ ∈ LOb , I(ϕ)
is read as “Ob is aware of ϕ” (or “ϕ is present to experience”).

Definition 233 (Reflective language extension). Define the reflective extension of the language by

                                  Lref
                                   Ob := LOb ∪ {I(ϕ) : ϕ ∈ LOb }.

An evidence state on Lref              ref
                      Ob is a map E : LOb → V.


                                                 360
Remark 919. Intuitively, Lref Ob doubles the vocabulary: for every base proposition ϕ we include a
corresponding meta-proposition saying “ϕ is in awareness”. This is not claimed to be psychologi-
cally exhaustive; it is a minimal representational hook that lets the model distinguish between (i) a
proposition being supported somewhere in the system and (ii) that proposition being accessible as
experienced content. In Russellian terms, we introduce a new set of propositions that talk about
the status of propositions, thus allowing the theory to make “aboutness of aboutness” explicit.
    A simple example: if ϕ is “there is an apple” then I(ϕ) is “I am aware that there is an apple”
or “the apple is present to experience.” The definition is useful because it makes reflective con-
sciousness an ordinary fixed-point/stability question in an enlarged evidence space, rather than a
sui generis phenomenon.

Definition 234 (Introspection operator). An introspection operator is a monotone map
                                                         ref
                                         Int : VLOb → VLOb

that assigns evidence to introspective propositions based on base evidence. A minimal choice is:

                               Int(E) I(ϕ) := E + (ϕ), 1 − E + (ϕ) ,
                                                                   


but more realistic choices incorporate attention (Section ??) and coherence (resonance, Section 3.9).

Remark 920. The minimal choice says: “awareness of ϕ tracks positive support for ϕ.” It is
intentionally crude, but it has two virtues: it is monotone, and it makes introspective support
computable from the same evidence quantities already present. More elaborate Int can (and in
realistic modeling should) depend on attention and workspace organization: one may have high
E + (ϕ) in a local module but low evidence for I(ϕ) if attention is elsewhere.
    For example, let ϕ be “background music is playing.” A perception module may support ϕ
strongly, yet if the system is deeply focused on a math problem, attention to that stream is low and
introspective awareness of the music may be absent. The usefulness of Int is that it gives a formal
bridge from first-order content to meta-content, enabling a precise statement of reflective closure
and self-reference in a paraconsistent setting [23, 24].

Remark 921. It is also important that I(·) is treated here as a representational operator rather
than a factive epistemic one: I(ϕ) is not read as “ϕ is true and known to be true,” but as “ϕ is
tokened in a way that is globally available as experience.” This matches the intended use in global-
workspace-style models, where what matters for consciousness is accessibility and stabilization, not
guaranteed veridicality. Accordingly, I(ϕ) can be present even when ϕ is false, and (conversely) ϕ
can be well-supported in a peripheral subsystem without I(ϕ) being supported.

Remark 922 (Paraconsistent self-reference). Nothing prevents the model from supporting evidence
for both I(ϕ) and I(¬ϕ) simultaneously. This is a direct formal analog of “I am aware of conflicting
impressions” without collapse into triviality.

17.3.2   Reflective workspace closure and a fixed-point existence theorem
Let W ref be a workspace operator on the reflective language:
                                                 ref      ref
                                       W ref : VLOb → VLOb .

Combine module integration, introspection, and workspace closure into a single update map.


                                                361
Definition 235 (Reflective update map). Fix attention a and module evidence E• on LOb . Define
the reflective update map
                                    F := W ref ◦ Int ◦ Γa ,
                   ref
with codomain VLOb .
Remark 923. The intended reading of the composition is operational: Γa performs attention-
weighted integration of first-order contents into a candidate workspace state; Int then generates
(or updates) the corresponding introspective tokens I(ϕ); finally, W ref imposes the global-workspace
constraint on the extended state in which first-order and meta-level tokens co-determine stability.
On this picture, reflective consciousness is not a separate process added after ordinary integration,
but a closure condition for a larger state space in which awareness-claims are among the stabilized
representations.
                                                                                                       ref
Definition 236 (Reflective closure / reflective consciousness state). An evidence state E ∗ ∈ VLOb
is reflectively closed (with respect to F ) if it is a fixed point:

                                             F (E ∗ ) = E ∗ .

When such a fixed point is reached (or approximately reached under iterative dynamics), the model
treats the agent as being reflectively conscious in the sense that the workspace has stabilized over
both object-level content and the corresponding introspective/meta-content.
Remark 924. This definition makes the higher-order aspect precise: what is stabilized is not
only ϕ-tokens about the world/body/internal state, but also I(ϕ)-tokens about what is present. In
particular, the model distinguishes (a) stable first-order representations without stable I(·) support
(a formal analog of “processing without reportable experience”) from (b) stable joint support for
ϕ and I(ϕ) (a formal analog of reportable, globally accessible experience). Because the workspace
operates over Lref
                Ob , the availability of meta-content can feed back into which first-order propositions
remain stable, capturing the intuitive idea that “noticing” something can itself reorganize what is
experienced.
Theorem 15 (Fixed-point existence under monotonicity). Assume Γa , Int, and W ref are monotone
with respect to the pointwise order on evidence states (inherited from the order on V). Then the
reflective update map
                                       F = W ref ◦ Int ◦ Γa
                                                  ref
is monotone, hence (on the complete lattice VLOb ) admits at least one fixed point. Moreover, F has
a least fixed point and a greatest fixed point.
Remark 925. The theorem expresses the “closure” idea in a mathematically standard way: if the
dynamics are order-preserving, then reflective stabilization is guaranteed in the sense of fixed-point
existence (even when the contents stabilized may be paraconsistent). Interpretively, the least fixed
point can be read as the minimal reflectively closed workspace compatible with the update rules, while
larger fixed points represent richer stabilized profiles of both object-level and introspective tokens. In
applications, one typically studies the iteration Et+1 := F (Et ) and asks when (and in what sense)
it converges, using the fixed points as attractors or equilibrium candidates for reflectively conscious
episodes.
Remark 926. This is the formal “assembly line” of reflective consciousness in one equation. Start-
ing from distributed module reports, Γa builds an integrated base evidence state; then Int adds meta-
evidence about what is present to awareness; then W ref applies the global stabilization/broadcasting

                                                   362
dynamics in the enlarged language. The composition order matters: it reflects a modeling judgment
that introspective tokens are built from base content (and its attention-mediated integration) and
then are themselves subject to workspace-level reinforcement, inhibition, and coherence constraints.
     A minimal example is: a sensory module yields evidence for ϕ; attention is high; introspection
adds I(ϕ); the reflective workspace then may propagate this to further tokens like “I am attending
to ϕ” (if included in the language) or may suppress contradictions. The usefulness of the definition
is that it makes reflective consciousness amenable to standard order-theoretic tools: we can ask
when F (or a variant) has fixed points and how they are selected. Moreover, reading the pipeline
left-to-right helps separate three distinct roles that are often run together in informal discussions:
(i) integration of first-order contents (modeled by Γa ), (ii) re-representation of those contents as
available-to-awareness (modeled by Int), and (iii) global constraint satisfaction and propagation
over the resulting mixed vocabulary (modeled by W ref ). In particular, the model does not assume
that introspection is infallible or “transparent”: since we work in an evidence lattice, Int can add
graded support and/or graded counterevidence for reflective propositions, allowing misintrospection,
uncertainty about one’s own states, or even simultaneous partial evidence for and against I(ϕ)
without trivialization.
                                                                        ref
    To speak about fixed points we consider the complete lattice VLOb with pointwise order. Con-
                           ref
cretely, an element of VLOb assigns to each sentence ψ ∈ Lref    Ob a pair of values in V = [0, 1]
                                                                                                  2

(e.g. degrees of support and counter-support), and the pointwise order compares such assignments
proposition-by-proposition. This is the natural setting for treating reflective updates as global
operators on entire evidence profiles, rather than as isolated updates to single tokens.

Theorem 16 (Existence of reflective conscious fixed points). Assume W ref and Int are monotone
and Lref                                    Lref
     Ob is finite (or more generally that V
                                             Ob is a complete lattice). Then the operator


                                                                 ref
                                     c := W ref ◦ Int
                                     W            c     on   VLOb

admits at least one fixed point, where Int
                                         c is any monotone extension of introspection that can read
reflective propositions as input (e.g. by ignoring them or by treating them as additional signals). In
particular, Wc has a least fixed point and a greatest fixed point.

Remark 927. In plain language, the theorem says: if your reflective workspace update rule is
monotone, then “reflectively stable” global states are guaranteed to exist. This is important because
self-reference is often thought to invite paradox; in classical logic, naive self-reference can indeed
be explosive. Here, by working in an ordered paraconsistent evidence lattice and using monotone
closure, we obtain an existence guarantee rather than a contradiction. This theorem thus connects
directly to the Hyperseed theme that “weak” (non-explosive) forms of self-reference are not only
possible but structurally natural in bounded cognitive systems [2, 3]. A useful way to read the
monotonicity requirement is as a “no retraction of evidence by fiat” constraint: when the input
state is informationally larger (more support and/or more counterevidence, in the lattice order),
the output is not allowed to become informationally smaller. This captures, at an abstract level,
the idea that the workspace dynamics are a kind of closure or propagation process rather than a
capricious rewrite rule; it is precisely this closure-like behavior that makes fixed-point existence the
default expectation rather than a delicate special case.
    The result also connects forward: later, when we talk about reflective will and autonomy as fixed
points of meta-control maps, we again rely on the idea that monotone self-modification dynamics
can have stable regimes; compare the use of fixed-point theorems to analyze stability of self-modifying
goal systems [10]. In that later application, the presence of multiple fixed points should be interpreted

                                                  363
as a formal analogue of multiple admissible “self-stabilizing” agent regimes (e.g. different coherent
reflective stances), with least/greatest fixed points providing extremal anchors among them.
                   ref
Proof. The set VLOb is a complete lattice under pointwise order because V = [0, 1]2 is a complete
lattice under componentwise order and products of complete lattices are complete. By monotonicity,
Tarski’s fixed point theorem applies, yielding existence of least and greatest fixed points of W
                                                                                               c . One
may also note that the “finite language” hypothesis is a convenient sufficient condition: if Lref Ob is
finite, then the product lattice is automatically complete, so no additional set-theoretic assumptions
are needed to ensure existence of arbitrary joins and meets.

Remark 928. Proof sketch. The strategy is purely order-theoretic: build a big ordered space of
possible reflective evidence states, check that it has enough completeness (all joins/meets exist), and
then invoke the general fixed-point principle that monotone maps on complete lattices must have
fixed points. No special properties of the particular p-bit operations are needed beyond completeness
and monotonicity. This robustness is part of the point: the existence claim is intended to survive a
wide range of choices for how evidence is aggregated, so long as those choices respect the underlying
order.
                                      ref
     The key step is recognizing VLOb as a product lattice: each proposition contributes a copy of
[0, 1]2 , and the product of complete lattices is complete. Once this is in place, Tarski’s theorem does
the heavy lifting. If one wants a visual intuition, imagine iterating W    c from the “least evidence”
state and watching evidence accumulate monotonically until it can no longer increase; this limiting
state is the least fixed point. Dually, iterating downward from the top element yields the greatest
fixed point. In many cognitive readings, the least fixed point can be interpreted as the minimally
committed reflective stabilization compatible with the dynamics (only what is forced by closure),
whereas the greatest fixed point represents a maximally saturated stabilization (everything that can
be maintained without violating the order constraints). Nothing in the theorem requires that the fixed
point be unique; rather, the lattice-theoretic framework anticipates the possibility of multiple stable
reflective equilibria, which can be selected among by additional constraints (e.g. cost, simplicity, or
policy-level preferences) not encoded in monotonicity alone.

Remark 929 (Interpretation). Theorem 16 is a small but useful “sanity anchor”: it ensures that
if one models reflective consciousness as a closure process on a paraconsistent evidence lattice, then
reflective conscious states exist as fixed points. This matches the Hyperseed intuition that reflective
awareness is a stabilized regime of self-referential modeling rather than a one-shot predicate. It
also clarifies what kind of mathematical object a “reflective conscious state” is in this setup: not
a single privileged sentence, but a whole valuation over an enriched language that includes both
world-directed claims and (possibly fallible) claims about what is present to awareness. Finally,
the extremal fixed points provided by Tarski offer canonical reference states even when empirically
plausible dynamics admit many equilibria; they supply baseline targets for subsequent questions
about selection, robustness under perturbation, and the effect of adding further reflective operators
to Lref
     Ob .


17.4    Resonance and coherence as stability selectors
In Hyperseed, resonance functions both as: (i) a dynamical amplifier (habit reinforcement, morphic
resonance; Section 12); and (ii) an experiential signature of coherence vs conflict (motivational
resonance; see also the core construction in Section 3.9).
    Here we use resonance as a selector among the fixed points guaranteed by Theorem 16. Con-
cretely, the existence of multiple fixed points can be read as the formal analogue of multiple in-

                                                  364
ternally stable “interpretations” or “self-consistent closures” of the same evidential situation; reso-
nance is then the additional principle that ranks (or biases trajectories toward) some closures rather
than others. In other words, the closure theorem supplies possibility (stable self-maps exist), while
resonance supplies preference (some stable self-maps are lived as coherent, others as fragmented or
tense).

Remark 930. The existence theorem above is generous: a monotone closure map may have many
fixed points. Phenomenologically, however, consciousness is not an arbitrary fixed point; it has a
felt signature of coherence, dissonance, tension, and release (Hyperseed-Concept 159 and 97). The
role of resonance here is to provide a principled mechanism for preferring some stable closures over
others, echoing the broader Hyperseed account of pattern emergence and reinforcement (Hyperseed-
Concept ??, 130, and 115) [5, 13]. A useful way to think about this is as a two-stage constraint:
(a) a workspace dynamics imposes logical and evidential closure, producing a set of fixed points
compatible with monotonic updating; (b) a resonance criterion then acts like a Lyapunov-style or
energy-style selector that makes some fixed points attractors (or makes them more robust against
perturbation), while others remain merely mathematically admissible. This distinction mirrors the
everyday fact that many “interpretations” of oneself and the world are compatible with the available
evidence, yet only some are experienced as settling, integrated, or action-guiding.

17.4.1   Coherence scores from paraconsistent evidence
Assume we have a logic-to-complex mapping σC as in Section 3.9. For an evidence state E and a
chosen feature map Φ from propositions to vectors (e.g. by stacking σC (E(ϕ)) for a designated list
of propositions), define a coherence score. The key modeling move is that σC allows one to treat
paraconsistent structure as a signal in a continuous space, so that “coherence” can be computed,
compared, optimized, and coupled to dynamics, rather than remaining a purely qualitative label.

Definition 237 (Coherence functional). Let K ⊆ Lref   Ob be a finite set of propositions regarded as
the “currently relevant workspace contents” (this may depend on attention and task). Define

                               zE ∈ C|K| ,
                                                                  
                                               (zE )ϕ := σC E(ϕ) ,

and define the coherence functional
                                                  1 X
                                     Coh(E) :=        |(zE )ϕ |2 .
                                                 |K|
                                                     ϕ∈K

Remark 931. Notation check: K is a finite index set of propositions; |K| is its cardinality. The
vector zE has one complex coordinate for each ϕ ∈ K, obtained by applying σC to the p-bit value
E(ϕ). The modulus |(zE )ϕ | is the usual complex absolute value, and Coh(E) is the mean squared
magnitude over the chosen proposition set.
    Intuitively, this turns a structured paraconsistent evidence configuration into a single scalar that
can play the role of a “stability” or “coherence” signal. A simple example: if σC maps high net
support to large real magnitude, then a workspace state with many strongly supported propositions
yields high Coh(E). If instead σC maps tension to imaginary magnitude, then a state full of
conflicts also yields high Coh(E) (but in a different complex direction), allowing the modeler to
decide whether to favor or penalize tension, as in paraconsistent resonance constructions [24]. This
is useful because it provides an explicit numerical criterion to prefer one fixed point over another,
rather than appealing to an informal “coherence” notion.


                                                  365
    One can also unpack the contribution of each proposition: if (zE )ϕ = aϕ + ibϕ , then |(zE )ϕ |2 =
a2ϕ + b2ϕ . Thus the chosen σC implicitly defines which aspects of evidential state count as “large”:
pure support-dominant regimes correspond to aϕ dominating, while conflict/energy-dominant regimes
correspond to bϕ dominating. The squared magnitude is convenient because it is additive across co-
ordinates and insensitive to global phase conventions, but it is not the only possible choice; it is
simply a minimal functional that is (i) nonnegative, (ii) decomposable across propositions, and (iii)
compatible with treating σC as a feature embedding.

Remark 932 (Reading). Large |(zE )ϕ | corresponds (by design of σC ) to either strong net support
(real part) or strong paraconsistent tension/energy (imaginary part). Depending on modeling goals,
one can prefer net support, prefer “energized tension”, or penalize tension. The point is not the
specific formula but the existence of a principled bridge from p-bit evidence patterns to a continuous
stability/interaction signal. A further modeling degree of freedom lies in the choice of K: taking K
to be attention-weighted makes coherence explicitly state-dependent, while taking K to include self-
referential and meta-level propositions makes coherence sensitive to reflective consistency rather
than only object-level consistency. In this sense, Coh(E) can be read as a task- and attention-
conditioned “felt integrity” measure: it is not a global property of an agent’s total belief state, but of
the currently active workspace slice that is available for report, control, and reflective endorsement.

17.4.2    Reflective consciousness as coherence-weighted closure
A simple way to model “states of consciousness” is to treat the workspace operator W ref as de-
pending on parameters controlling:

• external coupling (how strongly sensory evidence anchors the workspace),

• internal coupling (how strongly association/imagination fills in content),

• reflective gain (how strongly introspection amplifies meta-content),

• and coherence preference (how strongly the workspace selects coherent states).

The last parameter is the locus at which resonance enters as a stability selector: it does not create
new logical consequences, but changes which closures become salient, persistent, or self-reinforcing
under iteration.

Definition 238 (Parametric reflective workspace family). A parametric reflective workspace family
is a family
                                                ref     ref
                                      Wλref : VLOb → VLOb
indexed by parameters λ = (λext , λint , λref , λcoh ), where each Wλref is monotone and can be inter-
preted as: external evidence anchoring (λext ), internal completion (λint ), introspection amplification
(λref ), and coherence selection (λcoh ).

Remark 933. Intuitively, λ is a “control panel” for the style of conscious closure. If λext is high,
the workspace behaves like a sober accountant tethered to registration (Hyperseed-Concept 153); if
λint is high, it behaves more like a novelist weaving completions and associations; if λref is high,
it tends to generate and amplify meta-content; if λcoh is high, it prefers states that score well
according to the chosen coherence criterion. This way of speaking is intentionally suggestive rather
than neuroscientific: it says that many qualitative shifts in “state” can be treated as parameter
changes, not as changes of metaphysical kind (Hyperseed-Concept 178). Moreover, the parameters


                                                   366
can be read as implementing different selection pressures on the set of fixed points: varying λext
and λint changes which propositions are likely to enter and persist in the workspace, varying λref
changes how strongly the system closes over meta-level descriptions of its own state, and varying
λcoh changes whether the dynamics tolerates patchwork tension or instead drives toward integrative
resolutions. In this sense, “reflective will” can be modeled as the agent’s capacity to modulate λ (in
particular λcoh and λref ) so that the eventual fixed point is not only reachable but also endorseable:
the closure is selected not merely because it is stable, but because it resonates with the agent’s
preferred mode of integration.

Remark 934 (Selector interpretation of fixed points). Given λ, Theorem 16 yields at least one
fixed point E ∗ ∈ Fix(Wλref ). When there are many, one can impose a resonance-based preference
by ranking fixed points via Coh(E ∗ ) (or via a variant that explicitly rewards support and penalizes
tension). Formally, one can treat the “selected” conscious closure as an element of

                               arg max Coh(E ∗ ) : E ∗ ∈ Fix(Wλref ) ,
                                       


when this set is nonempty and the modeling context licenses a maximization principle. Alterna-
tively (and more dynamically), one can view λcoh as shaping the iteration trajectory so that high-
coherence fixed points have larger basins of attraction, thereby capturing the phenomenological idea
that resonant configurations are easier to maintain and return to after perturbation, while dissonant
configurations are fragile or effortful to sustain.
                                                                                    1
Remark 935 (On the choice of normalization and workspace size). The factor |K|        makes Coh(E)
comparable across different workspace sizes, which is useful if K is attention-dependent and can
expand or contract. If one instead wants larger workspaces to have systematically larger coherence
signals (e.g. to model the felt “intensity” of a richly populated conscious scene), one can drop the
normalization or replace it with a softer scaling. Likewise, one can introduce proposition weights
wϕ to model salience:
                                                 1      X
                                Cohw (E) := P              wϕ |(zE )ϕ |2 ,
                                               ϕ∈K wϕ  ϕ∈K

without changing the basic role of coherence as a selector; such weights provide a direct handle on
how attention and motivational relevance modulate resonance.

Remark 936. As a concrete example, one could define Wλref to take a convex combination (in
the quantale sense) of “sensory anchoring” constraints and “associative completion” rules, with
weights controlled by λext and λint . In particular, one may read λext as strengthening the degree to
which external error-correction, cross-modal consistency, and stimulus-locked constraints dominate
the closure, and λint as strengthening the degree to which internally generated completions, priors,
and memory-driven predictions dominate it. The quantale-convex phrasing is meant to emphasize
that the combination need not be linear in a vector-space sense: the “mixture” can be expressed
through the underlying order and monoidal structure that governs how constraints compose and
how entailments accumulate. The definition is useful because it formalizes the claim that waking,
dreaming, hallucination, etc., can be understood as regimes of the same computational architec-
ture, tuned differently. On this view, what varies across regimes is not the presence or absence
of a workspace/closure mechanism, but which families of constraints are allowed to dominate the
selection of stable fixed points of the induced operator.

    This provides a clean formal slot for the Hyperseed claim that many distinct “states of con-
sciousness” are parameter regimes rather than separate ontological kinds. It also makes room for

                                                 367
intermediate and mixed cases (e.g. lucid dreaming, absorption, meditation, or drug-induced states)
as regions in a continuous parameter landscape rather than as discrete labels, since small changes
in λext and λint can shift which patterns become coherent enough to persist.

17.5     Reflective will as meta-control on self-model dynamics
Hyperseed uses “(reflective) will” to denote more than mere action selection: it is the capacity
to intentionally reshape the mind’s own internal dynamics (especially attention and self-model
updates). In particular, the relevant “internal dynamics” include not only which contents enter
a global workspace, but also which self-descriptions (e.g. “I am safe,” “I am failing,” “I am cu-
rious”) are repeatedly re-instantiated by the closure process, thereby becoming behaviorally and
phenomenologically dominant.

Remark 937. In ordinary engineering terms, “will” here is closer to meta-control than to control:
it is the selection of how control itself is carried out, including how attention is allocated and
how self-representations are stabilized. One can think of it as operating on the parameters and
operators that determine which internal signals are amplified, which are suppressed, and which are
treated as “authoritative” inputs to decision-making. This aligns with Hyperseed’s broader interest
in self-modifying agents and stability of internal goal/attention structures [10]. It also connects to
the concept of Weakness (Hyperseed-Concept 202) in the sense that the system must manage self-
reference and self-modification without collapsing into inconsistency or paralysis [2, 3]. In more
concrete terms, meta-control must include safeguards (implicit or explicit) that prevent runaway
self-editing (e.g. compulsive policy rewriting) while still allowing sufficient plasticity for learning
and recovery.

17.5.1    Will as choice of an intervention on the update operator
Let SOb be a state space of the observer (internal memory, body state, etc.). For example, SOb
may include latent variables corresponding to working memory contents, affective tone, estimated
uncertainty, and the current self-model, insofar as these are available to the system as inputs
to further updating. Let U be a set of interventions that can affect: (i) attention allocation a
(Section ??), (ii) the workspace parameters λ (Section 17.4), and/or (iii) the control policy used to
act in the world (Section 14). It is important that U ranges over internal as well as external-facing
interventions: the notion of “intervening” here is not restricted to motor outputs, but includes
changes to the internal routing and gain-control by which information becomes influential.

Definition 239 (Will operator). A will operator is a map

                                           Will : SOb → U

that selects an intervention u ∈ U based on the current internal state. Applying u induces an update
of the reflective closure operator, i.e. changes F = W ref ◦ Int ◦ Γa to a new operator Fu . One may
view u as selecting (or modulating) one or more components of the composite map—for instance,
by altering Γa through attention shifts, by altering Int through changes in how sensory evidence is
incorporated, or by altering W ref through changes in reflective stabilization strength.

Remark 938. Intuitively, Will is the system’s “choice of how to proceed,” not only in the world
but also in its own cognitive configuration. An example of u ∈ U might be: “shift attention from
rumination to sensory grounding,” which changes a and potentially increases λext . Another example
is: “engage deliberative mode,” which might increase the weight of explicit reasoning processes and

                                                 368
adjust workspace inhibition rules. A further example (in the same spirit) is: “reduce precision on
intrusive imagery,” which would down-weight certain internally generated candidates before they
are stabilized by closure, thereby reducing the chance that they become fixed-point contents.
    This definition is useful because it makes “will” something that has a clear causal footprint in
the formalism: it changes the operator whose fixed points are the conscious states. That is, will is
not a ghostly add-on; it is a map that selects an intervention that changes the dynamics of closure,
thereby changing what is stably present to experience and action. Equivalently, it lets us speak
precisely about cases where two agents (or two moments of the same agent) have similar sensory
inputs but systematically different stable experiences because the meta-selected operator Fu differs.
Remark 939 (Why this is “will” rather than “control”). Ordinary control (Section 14) chooses
actions in the world. Here the intervention may also choose: what the agent attends to, how reflec-
tive closure is computed, and how self-representations are stabilized. This corresponds closely to
Hyperseed’s use of “will” as control over inner dynamics. In particular, it distinguishes between (a)
selecting an action under a fixed cognitive pipeline and (b) selecting the pipeline (or its parameters)
under which subsequent actions and perceptions will be generated.

17.5.2   Reflective will as meta-selection
Reflective will occurs when the system can represent and modify the will operator itself. We capture
this by allowing interventions that change the policy class. This is the point at which the agent is
no longer only choosing within a given meta-control scheme, but is able to restructure the scheme
that generates such choices, thereby altering its own future degrees of freedom.
Definition 240 (Reflective will). Let Π be a space of possible will operators π : SOb → U . A
reflective will state is a pair (π, s) with π ∈ Π and s ∈ SOb . A reflective will update is a map

                                    RWill : Π × SOb → Π × SOb ,

which may change both the internal state and the will operator. In effect, RWill can be read as a
learning (or self-programming) dynamic on Π coupled to an ordinary state-update dynamic on SOb .
Remark 940. In plain language: a non-reflective will chooses what to do; a reflective will can
also choose how it will choose in the future. For example, an agent might adopt a new attentional
policy “when anxious, ground attention in breath”; this is a modification to the will operator itself,
not merely a single action. The pair (π, s) represents “the current chooser” together with the
current state it is choosing from. One can also interpret π as encoding commitments or self-
binding constraints (e.g. “do not deliberate about X after midnight,” or “when uncertain, consult
external evidence”), which then shape subsequent trajectories of Fu by restricting or biasing which
interventions are selected.
    This definition is necessary if we want to model long-term autonomy and development: an agent
that cannot revise its own will policy is confined to a fixed meta-level, whereas reflective agents can
enter regimes of self-training, self-regulation, and ethical self-binding. Order-theoretic and dynam-
ical tools then become applicable to questions of stability and drift, linking naturally to fixed-point
approaches to self-modifying systems [10]. It also makes it possible to distinguish benign adaptation
(slow improvement of π with respect to some internal viability criterion) from destabilizing meta-
dynamics (rapid churn in π that prevents coherent stabilization of goals, attention, or self-model
contents).
Remark 941 (Fixed point picture). A stable reflective will regime corresponds to a fixed point
(or slowly drifting orbit) of RWill. This is one of the cleanest mathematical ways to interpret the

                                                 369
Hyperseed idea that “reflective will” is a stabilized meta-level capability rather than a single act.
In such a regime, the agent’s meta-policy π is itself resilient under the pressures of short-term
perturbations in s (fatigue, affect, noise), and this resilience can be studied with the same stability
intuitions used elsewhere in the framework (e.g. as a selector for coherent, self-sustaining patterns).

17.6     Autonomy and the reflective self as fixed points and higher morphisms
Hyperseed’s “natural autonomy” is not maximal independence from world and society; it is the
capacity to maintain coherent self-directed dynamics while remaining coupled to larger systems.
The earlier sections already provide most of the needed machinery: self as boundary in a pattern
web (Section 16), control as attraction-sensitive intervention (Section 14), and habits/self-weaving
dynamics (Section 12).
   Here we package these ideas into a minimal autonomy criterion.
Remark 942. This notion of autonomy (Hyperseed-Concept 119) is intentionally non-romantic:
it is not “freedom from causation” but the ability to keep one’s dynamics within a viable region by
selecting interventions, including internal interventions. It is also explicitly relational: the viable
region depends on coupling to environment and society, and the self/other boundary (Hyperseed-
Concept 165) is itself observer-relative and potentially paraconsistent (Section 16).

17.6.1    Autonomy as viability under self-directed closure
We treat autonomy as viability of self-maintaining closure.
Definition 241 (Viable set and autonomy). Let Du : SOb → SOb denote the state update induced
by applying intervention u ∈ U (this includes both world actions and internal interventions). Let
V ⊆ SOb be a set of “viable” states (states where the mind remains functional, coherent enough,
and continuous enough; this is observer- and model-dependent). We say Ob has natural autonomy
relative to V if for every s ∈ V there exists an intervention u ∈ U such that Du (s) ∈ V.
Remark 943. Intuitively, V is the set of states in which the agent “still counts as itself and still
works”. The condition says: whenever the agent is in a viable state, it has at least one available
move that keeps it viable. This is a minimal viability-style autonomy notion, echoing how “life”
and “agency” are often made precise via invariance or controlled invariance of a viability region
(compare Section 19.2).
    A simple example: if SOb includes a resource variable (energy, attention capacity, etc.) and
V is defined by “resource above threshold,” then autonomy means the agent can always choose
some intervention that does not immediately exhaust the resource. The definition is useful because
it separates autonomy from omnipotence: autonomy is not “I can do anything,” but “I can keep
going in a coherent way,” which is closer to the lived phenomenon and to Hyperseed’s emphasis on
self-maintaining pattern-web dynamics.
Remark 944 (Connection to self-weaving). If V is defined in terms of persistence of a self-weaving
subweb (Section 12) plus a continuity constraint (Section 16), then “autonomy” is precisely the
ability to choose actions (internal and external) that keep the self-weaving process alive without
losing identity.

17.6.2    Reflective self as a stabilized self-representation
Hyperseed’s “reflective self” is not merely a self-model; it is a self-model that becomes a stable
reference point for reflective consciousness and reflective will.

                                                 370
Definition 242 (Self-model object and reflective self condition). Assume Lref   Ob includes special
propositions of the form Self(ψ) meaning “ψ is a property of me” (e.g. a pattern/property token
as in Section 9 applied to the self-boundary of Section 16). A workspace-stable evidence state E is
said to exhibit a reflective self if:
(a) (Self-presence) for a designated set Pself of self-properties, E + (Self(p)) is above threshold for
    many p ∈ Pself ;
(b) (Reflective access) for these p, the introspective propositions I(Self(p)) are also supported above
    threshold;
(c) (Stability) these supports persist under small perturbations of module evidence and attention.
Remark 945. This definition makes “having a self ” (as a representational fact) different from
“having a reflective self ” (as a stable, accessible, meta-accessible representational fact). Condition
(a) says that many self-attributions are present; condition (b) says they are not merely implicit but
are themselves available to awareness; condition (c) says the whole configuration is robust under
small changes. In informal terms: it is not enough that the system encodes a self-model somewhere;
it must be able to stand by it in the workspace and to know (in the formal introspective sense) that
it is standing by it.
     A simple example is a bodily self-property p = “this arm is mine.” In a reflective self regime,
one expects both Self(p) and I(Self(p)) to be supported, and not to vanish under minor sensory noise.
This definition is useful because it ties together three threads from earlier sections: self/other bound-
ary (Hyperseed-Concept 165), self-continuity (Hyperseed-Concept 166), and attention-mediated global
accessibility (Hyperseed-Concept 60). It also provides a place to connect with individual and collec-
tive “consciousness location” ideas in the broader Hyperseed program [4, 12].
Remark 946 (Higher morphism reading). In the enriched-categorical viewpoint, a stable reflective
self can be treated as a higher morphism (or a higher cell) relating:

(self-boundary as subobject of a pattern web)         →      (self-representation in the reflective workspace)   →   (meta

We avoid heavy (∞, 1)-categorical machinery here, but the conceptual alignment is direct.

17.7     States of consciousness as parameter regimes
Hyperseed lists a number of “states of consciousness” (ordinary waking consciousness, dreaming,
hallucinating, being, oceanic consciousness, creative inspiration, enlightenment, Vedantic strata).
In the present reconstruction, these can be modeled as regimes of the parameter vector λ =
(λext , λint , λref , λcoh ) together with the habit/resonance coupling strengths (Sections 12 and 3.9).
Remark 947. The modeling posture here is pluralist but disciplined: we do not deny the qualitative
diversity of states of consciousness (Hyperseed-Concept 178); rather, we claim that much of this
diversity can be represented as changes in coupling strengths and closure preferences inside a single
architecture. This is reminiscent of how, in physics, different phases of matter are not different
substances but different regimes of the same underlying constituents; here the “constituents” are
attention, evidence, workspace closure, and resonance.
Definition 243 (State-of-consciousness parameters). A state-of-consciousness parameter tuple is

                                 Λ := (λext , λint , λref , λcoh , ρhab , ρres ),

where:

                                                      371
• λext controls anchoring to current sensory registration (Section 13);

• λint controls internal completion/association (pattern web propagation; Section 11);

• λref controls introspection gain (Section 17.3);

• λcoh controls coherence preference (Section 17.4);

• ρhab controls habit reinforcement strength (Section 12);

• ρres controls resonance coupling strength (Sections 3.9 and 12).

Remark 948. Intuitively, Λ extends the earlier workspace parameters λ with two further knobs:
habit reinforcement and resonance coupling. If ρhab is high, recently active patterns are rapidly
entrenched (Hyperseed-Concept 155); if ρres is high, distant parts of the pattern web can synchronize
and amplify one another (Hyperseed-Concept 159). Thus Λ acts as a compact descriptor of how
“tight” or “loose” the system is in binding together contents and in reinforcing repeated flows.
    As an example, a dreaming-like regime might be described by low λext , high λint , and moderate-to-
high ρres (strong internal coupling) with weaker external anchoring. The usefulness of introducing
Λ is that it allows the narrative taxonomy of states to be replaced by a parameterized family of
operators, which is mathematically tractable and composable with the rest of the framework.

17.7.1   Canonical regimes
The following table is not intended as neuroscience; it is a compact map from Hyperseed vocabulary
to a minimal mathematical control panel.

• Ordinary waking consciousness. High λext ; moderate λint ; moderate λref ; λcoh tuned to
  prefer sensory-consistent closure. Habits and resonance are active but constrained by sensory
  feedback.

• Dreaming. Low λext ; high λint ; variable λref . Coherence preference may be lower, allowing
  more internally generated blends and narrative jumps. Habit dynamics may replay or reweight
  pattern-flow motifs (Section 12) without external error correction.

• Hallucinating. Low λext but strong internal propagation and high self-consistency pressure:
  high λint and high λcoh , with closure dominated by internally generated evidence. Paraconsis-
  tency becomes prominent: the system may carry simultaneous support for incompatible world
  propositions without collapse, while still experiencing strong presence.

• Being (non-conceptual presence). Moderate-to-low λint (less elaborative completion), mod-
  erate λext (or also low, depending on context), and high λcoh with coherence defined more by low
  tension than by high net propositional content. In this regime the workspace fixed point contains
  fewer explicit propositions but higher stability.

• Oceanic consciousness. This is naturally modeled by a reduction of self/other boundary sharp-
  ness (Section 16) together with high global coherence. Formally, this corresponds to: (i) fewer
  strongly supported self-boundary propositions; (ii) higher coupling between self-typed and world-
  typed pattern nodes; and (iii) a coherence preference that does not penalize loss of boundary
  distinctions. This connects back to Hyperseed’s non-duality motif (Section 6; Hyperseed-Concept
  121).


                                                 372
• Creative inspiration. A transient regime with increased resonance coupling ρres between nor-
  mally distant subwebs, enabling new blends (Section 9). Here ρres can be read as a control
  parameter governing the effective “conductance” of associative links across otherwise weakly
  communicating regions of the cognitive network, so that activation can percolate between con-
  texts that are usually conditionally independent. One can model this as a temporary increase in
  cross-context coupling in the habit/resonance kernel, leading to rapid emergence of high-intensity
  composite patterns [5]. Concretely, if the kernel K weights transitions between subweb states,
  then “inspiration” is a short-lived deformation K 7→ K + ∆K with ∆K concentrated on off-
  diagonal (cross-context) blocks, so that previously subthreshold combinations become reachable
  within a few update steps. Phenomenologically, this corresponds to the felt “suddenness” of a
  novel synthesis: the composite pattern is not built by slow local refinement alone, but by a burst
  of long-range binding that stabilizes once coherence constraints are satisfied.
• Enlightenment. Modeled here as a stable, low-effort, high-coherence regime in which: (i)
  reflective closure remains stable under perturbation; (ii) will/intervention choices tend to preserve
  viability with minimal contrivance (foreshadowing Wu Wei; Section 26; Hyperseed-Concept 206
  and 207) [21]; and (iii) self/other boundary is flexible without inducing disorganized conflict.
  Item (i) can be understood as a robustness property: small changes in incoming evidence, affect,
  or bodily state do not cause reflective propositions to oscillate or fragment, i.e. the closure
  operator returns to (or remains near) the same fixed point after bounded disturbance. Item (ii)
  emphasizes that “control” is not absent but becomes economical: interventions align with system
  dynamics so that fewer corrective moves are required to maintain constraints (e.g. viability, social
  coordination, or goal satisfaction), resembling a descent along a shallow energy landscape rather
  than repeated forcing against steep gradients. Item (iii) indicates that increased permeability
  of self/other modeling does not collapse into indiscriminate identification; instead, boundary
  flexibility is paired with sufficient coherence to avoid runaway contagion of competing action
  policies. In quantale terms: low “tension” components across the reflective proposition set while
  retaining functional coupling for control. More explicitly, if reflective propositions are combined
  via a monoidal product that aggregates commitments, then “tension” informally tracks the degree
  to which jointly held propositions require active suppression of incompatibilities; the enlightened
  regime corresponds to configurations where incompatibilities are either resolved (by re-framing)
  or rendered non-disruptive (by appropriate contextualization), while the coupling needed for
  action selection remains intact.
• Vedantic strata. A simple formal analogue is a hierarchy of reflective closures: LOb ⊂ Lref        Ob ⊂
  Lref,2
    Ob   ⊂ · · · , where Lref,k
                          Ob    adds propositions  about awareness-of-awareness    iterated k times. This
  mirrors the idea that certain reports distinguish (a) first-order contents, (b) awareness of those
  contents, and (c) awareness that one is aware, etc., with each level introducing new constraints
  on what counts as a stable self-description. Different strata correspond to stable fixed points at
  different k (or different gains λref ), with the paraconsistent setting allowing such iteration without
  trivial paradox. Operationally, λref can be interpreted as a weighting (or gain) on reflective update
  terms relative to first-order dynamics: higher λref makes meta-level propositions more influential
  in the closure computation, which can stabilize higher-order self-modeling when the network
  can sustain it. The reference to paraconsistency matters because awareness-of-awareness claims
  often generate self-referential structures; allowing controlled inconsistency prevents the entire
  reflective lattice from collapsing into triviality while still permitting meaningful fixed points that
  correspond to distinct phenomenological “strata”.

Remark 949. The point of these regime descriptions is not to legislate phenomenology but to show

                                                  373
that the formalism has enough expressive degrees of freedom to represent qualitative shifts without
adding new primitives. In this sense the regimes are parameterized views of one and the same
machinery: varying coupling, gain, noise, and boundary-regularization terms can move the system
between recognizable macrostates without changing the underlying ontology of operators, proposi-
tions, or update rules. In particular, the transition from waking to dreaming becomes intelligible as
a movement along the axis from externally anchored closure to internally generated completion; the
more “mystical” regimes become movements along the axes of self/other boundary softness and co-
herence preference, echoing Hyperseed’s process-oriented stance in which identity and boundary are
dynamically constructed (compare [15, 14] for metaphysical inspirations). One can also view these
axes as coordinates on a stability landscape: “waking” corresponds to closures strongly constrained
by sensory-anchored evidence and prediction-error correction, whereas “dreaming” corresponds to
closures where generative priors and internal completion dominate, with external correction weak-
ened. Likewise, changes in boundary softness can be modeled as shifts in how strongly the system
penalizes cross-agent (or cross-model) identification errors, and changes in coherence preference
can be modeled as shifts in how aggressively the system resolves or tolerates local inconsistency in
the reflective set.

17.8    Intuition and reason as dual inference channels
Hyperseed explicitly distinguishes intuition and reason, and treats both as essential. A minimal
way to integrate this into the present framework is to posit two update channels:

• Intuitive update: fast, low-cost propagation in pattern webs, strongly driven by resonance.

• Reasoned update: slower, higher-cost composition of explicit predictive/causal relations.

Remark 950. This distinction corresponds to two complementary modes of cognition: intuition
(Hyperseed-Concept ??) as quick pattern completion and resonance-driven association, and rea-
son (Hyperseed-Concept 150) as explicit manipulation of articulated relations (implications, causal
arrows, plans). The framework does not declare one mode superior; rather, it provides a math-
ematical place for their interaction, consistent with the Hyperseed emphasis on cognitive synergy
(Hyperseed-Concept 73) [19].

Definition 244 (Two-channel update sketch). Let E be the current reflective evidence state. De-
fine:
                           Eint := Uint (E),   Erea := Urea (E),
where Uint is a monotone operator that spreads support along pattern-web morphisms (Section 11)
and resonance couplings (Section 17.4), and Urea is a monotone operator that propagates support
along explicitly represented implications and attractions (Section 14), with explicit composition.
The combined update may be taken as

                              U (E) := W ref E ⊕ β ⊗ Eint ⊕ γ ⊗ Erea ,
                                                                    


with channel weights β, γ ∈ [0, 1].

Remark 951. Notation check: Uint and Urea are endomaps on the space of reflective evidence states
(they take an evidence state and output another). The scalars β, γ are embedded into V via β, γ,
and then used to weight the contributions of the two channels using the quantale tensor ⊗. The
join ⊕ combines the baseline state with the two channel-updated states, and finally W ref re-applies
reflective workspace stabilization.

                                                374
    Intuitively, this says: take the current state, add in a resonance-driven intuitive propagation and
a relation-driven reasoned propagation, each with its own strength, then stabilize globally. A concrete
toy example is: intuition quickly spreads support from “dark clouds” to “it will rain” via a learned
association, while reason slowly constructs support for “bring an umbrella” by chaining explicit
implications. The definition is useful because it gives a formal grammar for how two inference
modes can cooperate without requiring them to be reducible to one another.
Remark 952. The two-channel form also makes room for an important asymmetry often observed
in practice: the intuitive channel is typically broad (high fan-out in the pattern web) but shal-
low (limited explicit depth of justification), whereas the reasoned channel is typically narrower but
deeper (longer chains of explicit composition). In the present notation, this difference is not en-
coded by changing the carrier space of E, but by the structure of Uint versus Urea : the former is
dominated by resonance couplings and morphism-local propagation steps, while the latter is domi-
nated by explicit relational composition (e.g. repeated application of implications, causal links, or
plan operators). This helps clarify why “slower” does not merely mean “smaller γ”: it can also
mean that Urea itself is implemented as a multi-step computation whose intermediate results may
enter the workspace only after partial stabilization by W ref .
Remark 953. Although the definition presents a single combined update U (E), the same ingredi-
ents can be used to model alternating or interleaved schedules, which better match many cognitive
architectures. For example, one may consider a two-phase cycle
            1                                                               1                     1
      E (t+ 2 ) := W ref E (t) ⊕ β ⊗ Uint (E (t) ) , E (t+1) := W ref E (t+ 2 ) ⊕ γ ⊗ Urea (E (t+ 2 ) ) ,
                                                                                                      

so that intuition rapidly proposes candidate completions that are then subjected to explicit reasoning
on the next phase. This interleaving is still monotone at each step (assuming monotonicity of the
constituents), and it highlights that “interaction” can mean not only additive combination via ⊕ but
also sequential coupling through the shared workspace.
Remark 954. From the perspective of reflective will and autonomy, the weights β, γ can be under-
stood as coarse global controls over where computational effort is spent. A high-β regime privileges
fast associative completion (useful for time pressure and exploration), while a high-γ regime privi-
leges explicit justification and longer-horizon planning (useful for high-stakes deliberation). Nothing
in the formalism requires β and γ to be fixed constants; they may be taken as functions of the cur-
rent state (or of a separate control state) to represent attentional gating. For instance, one may
write β(E), γ(E) to indicate that the system shifts toward reason when the workspace contains unre-
solved conflicts, or shifts toward intuition when the workspace is sparse and requires rapid hypothesis
generation.
Remark 955. A further use of the two-channel grammar is to separate proposal from justifica-
tion without forcing either to be infallible. Intuition may propose a high-support candidate that is
later weakened by reason when explicit causal structure does not sustain it; conversely, reason may
construct a formally valid chain that remains low-impact in practice if it fails to resonate with the
currently active pattern web. In the combined update, these cases correspond to situations where
β ⊗ Eint dominates the join but is then attenuated by stabilization, or where γ ⊗ Erea introduces
structured support that nonetheless competes with other attractors already present in E. This is one
place where cognitive synergy becomes operational: the channels are allowed to disagree, and the
workspace provides the arena in which their contributions are reconciled into an actionable state.
Remark 956 (Why paraconsistency matters for intuition/reason). Intuition often produces “both-
leaning” states: simultaneous attraction toward incompatible interpretations. In a classical logic

                                                  375
semantics this would be immediately problematic; in the p-bit setting it is a first-class representa-
tional state that can later be refined by reason, by attention shifts, or by additional evidence.

Remark 957. The preceding point can be sharpened by noting that the intuitive channel may
increase support for multiple mutually incompatible hypotheses at once because resonance can be
triggered by shared features (e.g. similar surface cues) even when deeper causal models differ. Para-
consistent representation allows such “multi-attractor” activation to remain expressible in E long
enough for Urea to apply discriminating structure (explicit constraints, explanations, counterfactual
checks, or plan feasibility tests). In this sense, paraconsistency is not merely a tolerance of in-
consistency but a functional resource: it provides a stable intermediate regime in which the system
can entertain competing candidates without collapsing into triviality or prematurely committing to
a single narrative.

17.9    Closing remarks and link to values/ethics
This section has treated consciousness and reflective will as closure and meta-control phenomena.
In that framing, “closure” is the emergence of a globally available, self-consistent-enough (in the
paraconsistent sense) workspace configuration, while “meta-control” is the system’s capacity to act
on its own internal dynamics (e.g., to sustain, redirect, inhibit, or reconfigure processes that would
otherwise run automatically). Two crucial ingredients have been intentionally bracketed:

• valuation: what the system cares about (joy/woe, goals, values);

• ethical structure: how value conflicts and social constraints are represented and resolved.

Here, “valuation” is meant broadly: it includes affective salience (what feels good or bad), instru-
mental priorities (what advances goals), and more reflective endorsements (what the agent takes
itself to have reason to pursue), all of which can bias which content is amplified into the workspace
and which is ignored or suppressed. Likewise, “ethical structure” is not restricted to explicit moral
rules; it includes any internal representation of constraints that have a normative character for the
system (e.g., prohibitions, commitments, fairness-like considerations, role obligations, or coordina-
tion requirements in multi-agent settings), as well as the mechanisms by which such constraints
interact with other goals under conflict. In Hyperseed, these are not add-ons: they shape attention,
shape which fixed points are selected, and shape whether reflective will stabilizes into autonomy
or degenerates into fragmentation. More concretely, the same capacity for reflective iteration that
enables autonomy can also enable rumination, oscillation among incompatible commitments, or op-
portunistic switching, unless there are stable evaluative gradients and constraint-handling policies
that give reflective control a direction and a stopping condition. Accordingly, Section 18 extends
the same paraconsistent and resonance-enabled machinery to evaluation, motivation, and ratio-
nal/ethical decision. This extension matters because evaluation is not merely a label attached after
the fact; it enters into the dynamical loop that determines which representations couple resonantly,
which attractors are reachable, and which equilibria are robust under perturbation, learning, and
social feedback.

Remark 958. One way to read the logical arc is: this section supplies the stage (workspace closure
and its reflective iteration), while the next supplies the drama (what is attractive, what is aversive,
which conflicts matter, and which resolutions count as rational or ethical). The metaphor is inten-
tional: closure and reflective will specify a capacity for integration and self-modification, but they do
not by themselves specify why the system should integrate in one direction rather than another, nor
which internal tensions are to be treated as errors versus acceptable trade-offs. Without values, a

                                                  376
consciousness modeled as “just” a fixed point is underdetermined: many fixed points may exist, and
the system needs selection pressures to inhabit some rather than others. This underdetermination
appears both at the level of content (which interpretations, plans, or self-models can close) and at
the level of policy (which meta-control actions are deemed improvements), so valuation and norm-
like constraints function as discriminators over a landscape of possible closures. Hyperseed’s claim
is that affect and value are among the deepest such selectors, co-evolving with attention, habit, and
resonance [5, 24]. On this view, autonomy is not merely the persistence of a reflective fixed point,
but the stability of a reflective process under evaluative and normative pressures: it is the ability to
maintain coherent commitments over time while still revising them in response to evidence, conflict,
and social constraint.


18     Emotion, values, goals, and rationality
18.1    Orientation: why “emotion” belongs in the formal stack
Hyperseed treats effort and distinction as primitive and observer-relative. Once effort is taken
seriously as a first-class quantity (Sections 8–9), it becomes natural to treat many affective phe-
nomena as evaluative signals about (i) expected effort/resistance, (ii) expected coherence/resonance,
and (iii) expected alignment with values/goals. In this section we give a minimal, mathematically
explicit vocabulary for:

• joy/woe and pleasure/pain as scalar projections of paraconsistent evaluative evidence;

• emotion as structured (vector-valued, context-dependent) evaluation fields rather than a single
  utility number;

• values, feelings, and goals as stable patterns and constraints in these evaluation fields;

• implicit vs explicit goals as a representational distinction;

• value paraconsistency as an intended feature (conflict without explosion);

• rationality as coherence between belief, value, and action under resource constraints;

• ethics (categorical imperative, cultural morality, evil) as constraints on goal selection and action
  selection that can be stated in the same formal language.

    A key motivation for placing “emotion” inside the formal stack is that, in real agents, evaluation
is not an optional afterthought appended to belief: it is part of the control loop that determines
which distinctions are worth making, which inferences are worth paying for, and which actions are
worth attempting under limited time/energy. If the framework already assigns a formal status to
effort (as an accounting of cost, resistance, and compression difficulty), then it is consistent to treat
affective variables as the agent’s internal, dynamically updated estimates of that effort landscape,
coupled to its goal constraints. On this view, emotion is not primarily a noise source to be “filtered
out” from rationality, but a low-latency summary of how current perception and prediction interact
with constraints on action selection.
    The phrase “observer-relative” is doing additional work here: what counts as “effortful” or
“coherent” depends on the representational resources and habits of the observer (or subsystem)
doing the evaluation. Thus, the same external situation can induce different affective profiles in
different agents, or even in the same agent across time, without requiring that emotion be arbitrary;


                                                  377
it is lawful relative to the agent’s current distinctions, priors, and available control policies. This also
clarifies why a single scalar utility is often too coarse: distinct appraisal channels can simultaneously
register “high resistance,” “high resonance,” and “high value alignment,” yielding mixed feelings
that are not well-captured by total ordering.
     The three parenthesized components—expected effort/resistance, expected coherence/resonance,
and expected alignment with values/goals—should be read as separable but interacting coordinates
of evaluation. Expected effort/resistance tracks anticipated cost-to-execute (physical, computa-
tional, social) and cost-to-maintain (attention, working memory, ongoing commitment). Expected
coherence/resonance tracks how well a candidate interpretation/action integrates with existing
patterns (including narrative self-models, predictive models, and social models), and therefore how
stable it is under perturbation. Expected alignment tracks the degree to which a candidate is
compatible with constraints that the system treats as non-negotiable or priority-weighted (explicit
commitments, learned norms, or implicit drives). Later formalisms will allow these coordinates to
be aggregated, contrasted, or kept separate depending on the control regime.
     The formalisms here are intentionally lightweight: we aim for a scaffold that composes cleanly
with the formal core (Section 3), with the control/prediction machinery (Section 14), and with the
resonance construction (Section 3.9). In particular, we want definitions that remain meaningful
when the agent’s beliefs are incomplete, when its goals are partially articulated, and when its
evaluative evidence is internally conflicted. This motivates the use of paraconsistent structures:
an agent can have simultaneously supported and opposed evaluations of the same option (e.g.,
“approach” and “avoid”) without collapsing into triviality, and without requiring that the conflict
be immediately resolved before action is possible.
     Concretely, the intended picture is that an agent maintains a collection of context-indexed
evaluation fields over its state/action space (or over structured descriptions of situations), and
emotions are identifiable patterns in these fields as they change over time. Scalar quantities such as
pleasure/pain are then treated as projections or summaries extracted from a richer object, typically
for fast control decisions. This retains the practical role of simple affective labels while keeping the
underlying representation expressive enough to capture ambivalence, tradeoffs, and norm conflict.
Remark 959. At the level of philosophical posture, this section takes seriously the idea that “value”
is not a decorative gloss atop cognition, but a structural constraint on what a system can coherently
do. In Peircean terms, values function as a species of Thirdness—habits, norms, and generali-
ties shaping inference and action—while emotions are the time-local manifestations of how that
Thirdness collides with the recalcitrance of the world (Secondness) and the immediacy of felt quality
(Firstness) [14]. In a Whiteheadian accent, emotions are not opaque atoms but events in a process:
they are patterns in the ongoing concrescence of appraisal and action [15]. Put differently, the “for-
mal stack” is not meant to exclude phenomenology, but to provide a disciplined way to talk about
the constraints and transformations that make phenomenology actionable for an agent. A value,
in this posture, behaves like a general rule that can be instantiated across contexts; an emotion
behaves like the local error-signal (or opportunity-signal) generated when that general rule meets a
particular world-situation under resource bounds.
Remark 960. This section should be read alongside the Hyperseed core-concepts: Effort (Hyperseed-
Concept 100), Distinction (Hyperseed-Concept 98), Emotion (Hyperseed-Concept ??), Values (Eth-
ical) (Hyperseed-Concept 197), Goals: Explicit/Implicit (Hyperseed-Concepts ??, ??), Value Para-
consistency (Hyperseed-Concept 198), Rationality (Hyperseed-Concept 148), and Compassion/Evil
(Hyperseed-Concepts 81, ??). One way to keep the reading coherent is to treat “emotion” (as used
here) as the interface layer between (i) descriptive models of the world (belief/prediction), (ii) pre-
scriptive constraints (values/goals), and (iii) the cost model (effort). In that sense, the section is not

                                                   378
proposing a separate psychology module, but a unifying vocabulary that lets the same mathematics
speak about appraisal, commitment, conflict, and action choice.

18.2     Paraconsistent evaluative evidence and affective projections
18.2.1    Evaluation fields
Let S denote a set of (observer-relative) situations or states and A a set of actions. We also fix a
finite set D of value dimensions. Typical elements of D include:

comfort, safety, truth, beauty, competence, belonging, compassion, individuation, self transcendence.

Nothing in the math forces these labels; the point is that Hyperseed does not assume values are
reducible to one scalar.
Remark 961 (Notation and conventions). Here s ∈ S is a modeled situation (which may already
bundle a time-slice, an internal state-estimate, and relevant context), and a ∈ A is a candidate
intervention. The finite index set D is not assumed to be “the true list of human values”; it is the
observer’s current basis of evaluative distinctions. The choice to make D finite is pragmatic: it lets
us treat value as a vector of coordinates while still allowing the coordinates themselves to evolve
later (Section 18.6).
Remark 962 (Why S×A rather than S alone). The dependence of evaluation on (s, a) (rather than
on s alone) is essential: many values are primarily interventional rather than merely descriptive.
For example, a situation s may be high in safety as a snapshot, while a contemplated action a may
nonetheless be evaluated as strongly anti-safety because it increases risk; conversely, s may be low
in comfort but a may have high pro-comfort evidence due to expected relief. The field EO is thus
best read as attaching evaluation to counterfactuals (“what would happen if I do a in s”) rather
than to world-states in isolation.
Definition 245 (Paraconsistent evaluative field). Fix an observer/context O. A paraconsistent
evaluative field is a map
                                 EO : S × A × D → [0, 1]2 ,
where
                                                +             −
                                                                         
                                EO (s, a; d) = EO (s, a; d), EO (s, a; d)
encodes degree of evidence that action a in situation s promotes (resp. opposes) the value dimension
                                                                 +               −
d. No consistency constraint is imposed; it is allowed that EO     (s, a; d) + EO  (s, a; d) > 1.
                                                                     +     −
                                                                             
Remark 963 (Interpretation of the two channels). The pair EO           , EO    should be read as two sepa-
rately supported appraisals, not as a single net valence split into positive/negative parts. Concretely,
  +                                                                                                −
EO  may be driven by cues of opportunity, growth, alignment, or anticipated benefit, while EO         may
be driven by cues of threat, violation, loss, or anticipated harm. Allowing both to be simultaneously
high captures the common case where an option is “meaningful but dangerous,” “honest but socially
risky,” or “safe but stifling.” In this sense, the paraconsistent format is not merely tolerant of
conflict; it makes conflict representable without forcing an immediate resolution step.
Remark 964. Intuitively, EO is a kind of “moral/affective sensorium” that maps each contem-
plated option to a two-sided appraisal. The two coordinates are not probabilities; they are indepen-
dent evidence channels, so one may have strong reasons both for and against. This is the evaluative
analogue of the paraconsistent evidence states used earlier for beliefs, and it aligns with the general
Hyperseed stance that conflict is often data rather than error (Hyperseed-Concept 198).

                                                   379
Remark 965 (Sources and observer-relativity). The subscript O emphasizes that evaluative ev-
idence is indexed to an observer/context, which can include embodiment, developmental history,
culture, role, and current commitments. In particular, EO can legitimately encode information that
is not “in the world” as a neutral fact (e.g., attachment dynamics, trauma-conditioned threat de-
tection, social-norm priors), because these factors causally shape both experienced affect and action
guidance. This is not a concession to arbitrariness: it is an explicit modeling choice that makes
room for calibration, learning, negotiation among observers, and reflective updates of O itself.

Remark 966. A simple example is the choice “tell a difficult truth” in a social situation. Relative
to d = truth one may have high positive evidence and low negative evidence; relative to d = belonging
one may have both substantial positive evidence (authenticity builds trust) and substantial negative
evidence (risk of social rupture). The formalism records this without prematurely collapsing it into
a scalar utility. This is useful because later decision rules can treat some dimensions as constraints,
others as objectives, and can invoke resonance to measure coordination among them rather than
forcing a false unanimity.

Remark 967 (Value paraconsistency is the default, not an exception). Hyperseed explicitly expects
that real agents have value conflicts, self/other boundary ambiguities, and mixed evidence about
what is good or bad. The p-bit representation is a direct formalization of this stance: one can carry
“pro-d” and “anti-d” evidence simultaneously without collapsing the system into triviality.

Remark 968 (Incompleteness and neutrality). Paraconsistency should be distinguished from mere
uncertainty: it is possible (and common) that both channels are low, e.g. EO (s, a; d) ≈ (0, 0),
representing a kind of evaluative silence or irrelevance with respect to d. This matters because “no
strong evidence either way” is not equivalent to “moderate net endorsement”: downstream rules
can treat low-information dimensions differently (e.g. defer, seek more data, or discount) rather
than mistaking neutrality for agreement.

Remark 969. This stance resonates with the broader paraconsistent program used in Constructible
Duality Logic and related approaches: inconsistency is handled by design rather than by denial
[23]. In the Hyperseed context, this also connects to paraconsistent resonance constructions, where
structured interference is treated as informative rather than merely pathological [24].

18.2.2   Joy/woe and pleasure/pain
To connect to the phenomenological words, we need scalar projections of the p-bit.

Definition 246 (Joy/woe intensities as projections). Given a p-bit v = (v + , v − ) ∈ [0, 1]2 , define:

                J(v) := v +      (joy intensity),      W (v) := v −     (woe intensity).

Given an evaluative field EO , define:
                                                                                    
                  JO (s, a; d) := J EO (s, a; d) ,     WO (s, a; d) := W EO (s, a; d) .

Remark 970 (Why take projections rather than a single valence). The choice to define J(v) and
W (v) as direct coordinate projections (rather than, say, v + − v − or v + /(v + + v − )) is deliberate:
it preserves the possibility that joy and woe co-occur without being forced into a one-dimensional
tradeoff. A net-valence reduction would erase the distinction between (0.9, 0.9) and (0.9, 0.1) even
though they plausibly correspond to very different phenomenology and very different action-guidance
(the former signaling “high stakes” and the latter signaling “clear endorsement”).

                                                     380
Remark 971. The intuition is almost austere: joy and woe are taken here as readouts of the pos-
itive and negative channels of evidence. This does not claim that joy is merely “belief in goodness”;
rather, it asserts that whatever else joy and woe are, they can be operationally summarized (for de-
cision purposes) by two monotone coordinates that can coexist. This corresponds to the Hyperseed
core-concepts Joy and Woe (Hyperseed-Concepts ??, 204).

Remark 972 (Joy/woe as action-guiding signals). Under this projection, JO (s, a; d) can be read as
the strength of “pull” toward a along dimension d, while WO (s, a; d) is the strength of “push-back”
or inhibition along the same dimension. Importantly, neither signal by itself dictates choice: a high
JO can be overridden by high WO (e.g. morally tempting but dangerous actions), and a high WO
can coexist with a high JO when the agent faces a costly duty or a meaningful sacrifice. This sets
up later mechanisms in which regulation, prioritization, or resonance can decide how such tensions
are handled rather than assuming they must be eliminated at representation time.

Remark 973. As a concrete example, take v = (0.8, 0.7). Then J(v) = 0.8 and W (v) = 0.7:
the system has strong pull and strong repulsion simultaneously. Phenomenologically this resembles
ambivalence, dread-excitement, or “I want it and I fear it.” The usefulness is that such a state
need not be treated as an error to be eliminated; it becomes a stable input to downstream coherence
and choice mechanisms.

Remark 974 (Pleasure/pain). We treat pleasure as joy-dominant affect and pain as woe-dominant
affect, but we do not identify them with mere sensation. Instead, pleasure/pain are taken to be evalu-
ative and can attach to internal or external processes (physical, mental, social, spiritual). Formally,
pleasure and pain are scalar summaries of (JO , WO ) after aggregating across value dimensions and
time horizons.

Remark 975 (Aggregation across dimensions and horizons). The last sentence is intentionally
underspecified: different tasks call for different aggregators. One natural family is a weighted com-
bination across dimensions,
                              X                                   X
                 Joy(s, a) =      wd JO (s, a; d),    Woe(s, a) =     wd WO (s, a; d),
                             d∈D                                  d∈D

with context-dependent weights wd ≥ 0 (possibly normalized, possibly not), together with a temporal
pooling rule that can emphasize short-term impact, long-term impact, or risk-sensitive tails. The key
point is that whatever aggregation is used, it is applied after representing the two-channel evidence
per dimension, so that mixed or conflicting evidence remains visible until the stage where explicit
policy choices (e.g. prioritizing safety as a constraint) are permitted to matter.

Remark 976 (Why “pleasure/pain” are not identical to any single d ∈ D). Although comfort
is an obvious contributor, pleasure and pain as used here are not confined to the comfort axis: a
person can experience pleasure in truth-telling, competence, belonging, or self-transcendence, and
can experience pain in betrayal, shame, incoherence, or moral injury even in the absence of physical
discomfort. Treating pleasure/pain as aggregated evaluative summaries is therefore a way to model
how multiple value dimensions can jointly produce global affective tone, while still allowing finer-
grained analysis at the level of (s, a; d) when needed.

Remark 977. This remark aligns Pleasure and Pain (Hyperseed-Concepts 137, 129) with the idea
that affect is not just peripheral sensation but a control-relevant appraisal. One simple toy aggre-
gation is: average JO (s, a; d) and WO (s, a; d) over a chosen subset of d and over a short temporal
window, and then compare the two. Yet the formalism deliberately leaves the aggregation operator

                                                 381
open, because in real agents pleasure/pain is plastic, trained, and context-dependent. In particular,
the same underlying stream of two-sided evaluative evidence can be re-weighted by attention, habit-
uation, framing, or learned predictors of downstream outcomes, so that an “affective summary” is
best treated as an agent-relative readout rather than a fixed physical observable. Formally, one can
regard an aggregation operator as any map from a collection of per-dimension, time-indexed p-bits to
a single p-bit (or small tuple of p-bits) that is subsequently used for control; leaving this open allows
the theory to represent both hard-coded reflex-like aggregation and slowly learned, meta-cognitively
editable aggregation.

18.2.3    Aggregating across value dimensions without collapsing conflicts
Hyperseed wants aggregation, but not at the cost of erasing conflict. The simplest approach is: keep
the vector structure for decision constraints, and use a scalar only as a tie-breaker. Concretely, the
vector is used to define feasibility or dominance (so that certain tradeoffs are forbidden or at least
not silently normalized away), while any scalarization is invoked only after the space of options has
already been filtered to those that are acceptable under the explicit multi-dimensional constraints.
This separation mirrors common practical decision procedures: first rule out options that violate
non-negotiables, then optimize within what remains.
Definition 247 (Value-vector for an option). For fixed (s, a) define the value-vector:

                          EO (s, a) := EO (s, a; d) d∈D ∈ ([0, 1]2 )D .
                                                   

Remark 978. This is the precise mathematical expression of “values are plural.” Each coordinate
is itself paraconsistent, so EO (s, a) is a structured object: a vector of two-sided appraisals. A simple
example is D = {truth, comfort}, in which case EO (s, a) is just a pair of p-bits. The usefulness is
that we can express constraints like “must not strongly violate comfort” while still optimizing truth
among feasible options. More generally, the formalism supports heterogeneous dimensions whose
evidential sources differ: e.g. truth may be driven by predictive accuracy and calibration signals,
whereas comfort may be driven by affective forecasting and physiological proxies; keeping separate
coordinates prevents premature averaging from hiding which subsystem is “objecting.” This also
makes room for asymmetric policy rules, such as treating some dimensions as veto constraints (e.g.
“never exceed woe threshold on safety”) and others as objectives (e.g. “maximize joy on curiosity”),
without forcing all of them into a single commensurate scale.
Definition 248 (Preference order on p-bits). For evaluative purposes, define a partial order pref
on [0, 1]2 by
                   (v + , v − ) pref (u+ , u− ) ⇐⇒ v + ≤ u+ and v − ≥ u− .
Thus “better” means more positive evidence and less negative evidence.
Remark 979. The order pref is the simplest monotone notion of “at least as good” compatible
with two-sided evidence: you can improve by increasing the positive channel and/or decreasing the
negative channel. It is partial rather than total because many pairs are incomparable (one has more
joy but also more woe). This incomparability is not a technical nuisance; it is the formal reflection
of conflicted evaluation (Hyperseed-Concept 198). Note that pref makes explicit that “net” affect
is not the primitive object: a p-bit with high (v + , v − ) may represent a tempting but risky option,
whereas a p-bit with lower (u+ , u− ) may represent a dull but safe option; neither dominates the
other without an additional principle. In this sense, a later tie-breaker scalar (if used at all) is
properly interpreted as an extra policy commitment about how to resolve incomparabilities, not as
part of the evidence itself.

                                                  382
Example 15. Let v = (0.7, 0.2) and u = (0.8, 0.2). Then v pref u because u has at least as
much positive evidence and no more negative evidence. But v 0 = (0.9, 0.7) and u0 = (0.8, 0.2)
are incomparable: one is higher joy and higher woe, the other lower joy and lower woe. This is
a minimal formal model of ambivalence versus calm satisfaction. One can also view (0.9, 0.7) as
“high activation conflict” (strong pull and strong push), whereas (0.8, 0.2) is “cleanly positive”;
treating them as incomparable preserves the psychologically natural distinction between intensity
and valence-mixing, which would be lost under a single net score.
Definition 249 (Pareto dominance for value-vectors). For two options (s, a) and (s, a0 ) define:

             EO (s, a) Pareto EO (s, a0 )   ⇐⇒   EO (s, a; d) pref EO (s, a0 ; d) ∀d ∈ D.

An option is Pareto-undominated if there is no other option that strictly improves at least one
dimension and is no worse in all others (under pref ).
Remark 980. Pareto dominance is the canonical way to aggregate multiple objectives without
assigning tradeoff weights: it marks an option as “unambiguously worse” only when it is worse
(or equal) in every dimension and strictly worse in at least one. In a value setting, this has a
moral flavor: if one option is no worse on every value and strictly better on at least one, then
choosing the dominated option looks like pure irrationality or error. This connects directly to
the rationality conditions later (Hyperseed-Concept 148). Importantly, using Pareto-undominated
options as a first-stage filter does not require the agent to decide how to trade truth against com-
fort; it only requires the weaker commitment to avoid options that are jointly worse by the agent’s
own lights in every tracked dimension. When the undominated set is large (as is typical in high-
dimensional, conflict-laden settings), a tie-breaker can be applied afterwards—for example, by a
context-conditioned scalar functional T (EO (s, a)) that is allowed to depend on situational features,
learned norms, or risk sensitivity—but such a functional is then explicitly a second-stage policy
choice rather than a covert averaging that would hide the underlying conflict structure.
    This keeps value paraconsistency explicit: conflicts remain visible as non-comparabilities. It
also makes room for principled “refusal” or “deferral” behaviors: if all available actions are Pareto-
undominated yet each carries substantial woe on some dimension, the formalism can represent
the state as one of genuine normative tension rather than forcing a spurious numeric optimum.
Conversely, when a clear dominance relation exists, the model predicts stable agreement across a
wide class of tie-breakers, since any reasonable scalarization that is monotone in the sense of pref
will also avoid selecting Pareto-dominated actions.

18.3    Emotion as structured evaluation and resistance signals
Hyperseed’s notion of emotion is not merely an add-on to cognition; it is a control-relevant summary
of value and effort structure.
Remark 981. The guiding idea is that emotion compresses a large evaluative landscape into a small
set of control knobs: what to approach, what to avoid, what to endure, what to postpone. Formally,
we will keep the compression mild: rather than forcing a scalar utility, we package (i) predicted
value-evidence, (ii) predicted resistance/effort, and (iii) a coherence indicator. This should be read
as a mathematical scaffold for the Hyperseed concept Emotion (Hyperseed-Concept ??) rather than
as an attempt to exhaust phenomenology.
Definition 250 (Effort/resistance estimator). Let cO (s, a) ∈ V denote an observer-relative effort
cost (weakness/effort quantale value; cf. Section 3.7 and Section 8). Let ρ : V → [0, ∞) be any

                                                  383
monotone “readout” mapping from quantale cost to a nonnegative scalar (e.g. ρ could be a chosen
norm or a projection). Define the scalar resistance estimate:
                                                             
                                     RO (s, a) := ρ cO (s, a) .

Remark 982. Here V is the underlying quantale (or cost domain) used earlier to encode weak-
ness/effort; cO (s, a) is the cost object in that domain; and ρ is a chosen way to read it out as a
single nonnegative number so we can compare options by “how hard.” The monotonicity require-
ment on ρ is the only structural assumption: more cost in the quantale sense should not turn into
less scalar resistance. This ties the present section back to the weakness/effort program [3, 2] and
to the core notion Quantale Weakness (Hyperseed-Concept 143).

Remark 983. A simple example is when V = [0, ∞] with the usual order, and cO (s, a) is already
a scalar time/energy estimate; then ρ can be the identity. A more Hyperseed-flavored example is
when V encodes multi-resource cost (compute, attention, social risk) and ρ is a chosen projection
that fits the observer’s current strategic posture.

Definition 251 (Emotion as an evaluation-resistance pattern). Fix a time horizon H and let
E
bO (s, a; d) denote the predicted (future) value-evidence for d over horizon H if action a is taken at
s. An emotion token for O at (s, a) is a tuple
                                                                           
                           EmO (s, a) := E  b O (s, a), RO (s, a), κO (s, a) ,

where κO (s, a) is an optional coherence/resonance signal (defined below) indicating how aligned the
value evidence is across dimensions and timescales.

Remark 984. Intuitively, EmO (s, a) is what an agent “feels about” doing a from s, in a way that
is already poised to influence control: it includes (i) the forecasted evaluative consequences, (ii) the
forecasted effort/resistance, and (iii) whether the forecasted consequences harmonize or fight each
other. A simple example is “approach a difficult conversation”: high predicted truth and belonging
benefits, but also high resistance; and depending on the internal model, high or low coherence between
dimensions.

Remark 985. The usefulness is compositional. The prediction/control layer can be used to compute
E
bO ; the weakness/effort layer yields RO ; and the resonance layer yields κO . Emotion then becomes
a derived interface object that is compatible with the rest of the stack, rather than a new primitive.

Remark 986 (Why this matches the Hyperseed intent). • Joy/woe components live in E
                                                                                 b O.

• “Tension” and “relief ” can be modeled as changes in RO and/or changes in the coherence signal
  κO .

• Complex emotions correspond to characteristic patterns in the vector-valued evidence, rather than
  to single scalar utilities.

18.3.1   Compassion
Compassion is treated as a value dimension whose evaluation depends on modeled others.

Definition 252 (Compassion as other-referenced evaluation). Let A be a set of agents, with distin-
guished self agent self ∈ A. For each j ∈ A assume O carries an estimate of that agent’s joy/woe


                                                  384
for outcomes, encoded as p-bits EO→j (s, a; joy) and EO→j (s, a; woe). Define a compassion score (as
a p-bit) by
                                       M                                            
            EO (s, a; compassion) :=             EO→j (s, a; joy) ⊗ ¬EO→j (s, a; woe) ,
                                      j∈A\{self}

where ¬ is p-bit negation (swap evidence components) and ⊕, ⊗ are the aggregators fixed in the
core.

Remark 987. This definition treats compassion (Hyperseed-Concept 81) as intrinsically model-
based: it depends on how O represents other agents’ prospective joy and woe. In that sense it
links value theory to social cognition and to the self/other boundary formalism earlier (Hyperseed-
Concept 165). The algebraic structure—combine a model of others’ joy with the negation of others’
woe, then aggregate over others—makes explicit what is otherwise left as moral rhetoric.

Remark 988. A simple example: suppose there is one other agent j, and EO→j (s, a; joy) =
(0.6, 0.2) while EO→j (s, a; woe) = (0.4, 0.7). Then ¬EO→j (s, a; woe) = (0.7, 0.4), and the combined
term is EO→j (joy) ⊗ ¬EO→j (woe). The exact numeric result depends on the quantale operations,
but the intended qualitative reading is: compassion rises when we foresee others’ joy and do not
foresee their woe.

Remark 989. This definition is only a template: it says compassion is evaluated by modeling
others’ joy/woe and aggregating. Different observers may use different agent sets, weights, and
aggregators. The key point is structural: compassion is not a mysterious extra primitive; it is a
particular kind of evaluative dependence on other-modeled affect.

Remark 990. In multi-agent contexts, formal compassion also connects to arguments that prosocial
constraints can increase group-level efficiency and coordination capacity, rather than merely adding
moral overhead [6]. In Hyperseed terms, compassion can be seen as an ingredient in building high-
resonance cultural patterns that reduce collective resistance.

18.4     Values, feelings, goals, and reward
Hyperseed distinguishes between transient feelings and persistent values. Goals are commitments
that bind action selection to values.

18.4.1    Values as stable patterns; feelings as local evaluations
Definition 253 (Value as a stable evaluative pattern). A value dimension d ∈ D is said to be a
stable value for observer O over an interval of proto-time T if the induced evaluation function

                                         (s, a) 7→ EO (s, a; d)

is (approximately) invariant under the observer’s typical context changes in that interval (up to a
tolerance set by O’s weakness/effort limits).

Remark 991. The intuition is that a value is not a single episodic feeling; it is a pattern of ap-
praisal that persists across changing circumstances. “Truth matters” means: across many contexts,
actions predicted to support truth tend to receive stable positive evidence relative to that dimension.
This explicitly ties values to the broader Hyperseed idea that ontology is reconstructed in terms of
stable patterns (Hyperseed-Concept 130; cf. [5]).

                                                   385
Remark 992. A simple example: if d = compassion is stable for O over T , then even as the
specific people and situations vary, the mapping (s, a) 7→ EO (s, a; d) continues to privilege actions
that reduce others’ woe. The usefulness of this definition is that it gives a crisp criterion for when
we are justified in treating some evaluative coordinate as a relatively fixed constraint in planning,
rather than as noise.
Definition 254 (Feeling as time-local affective readout). A feeling token for O at time t is any
scalar or low-dimensional readout
                                                          
                                  FO (t) = Φ EmO (st , at ) ,

where Φ is a bounded map (e.g. combining joy/woe across a small subset of dimensions, plus
resistance).
Remark 993. Here Φ formalizes the act of compression: the mind cannot (and need not) repre-
sent the entire evaluative tensor at every moment, so it reads out a small summary. In common
terms, this includes things like “anxiety level,” “relief,” or “contentment.” The formal definition
is deliberately permissive: many different physiological and cognitive architectures may implement
different Φ. This corresponds to Feelings (Hyperseed-Concept ??) as time-local indicators rather
than enduring commitments.
                                         b R, κ) = P
Remark 994. A simple example is Φ(E,                 d∈D0 λd (J −W )−βR for a small subset D0 ⊆ D
active in the current attentional focus. The usefulness is that the theory can talk about feelings with-
out reifying them as primitives: they are observer-dependent readouts of deeper evaluative structure.
   This makes the common-sense relationship precise: feelings are local readouts; values are stable
patterns in evaluative fields.

18.4.2   Goals: explicit and implicit
Definition 255 (Explicit goal). An explicit goal for O is a representable constraint G on trajec-
tories or outcomes:
                                            G⊆Ω
where Ω is a space of outcomes or histories (as formalized in the prediction/control layer). Explic-
itness means O can name G in its representational language (Section 13).
Remark 995. The intuition is that an explicit goal is declarative: it lives in the agent’s repre-
sentational economy as something like “finish the proof,” “do not lie,” or “keep the system within
a safety envelope.” This corresponds to Goals: Explicit (Hyperseed-Concept ??). The set-theoretic
form G ⊆ Ω is standard in control theory: it lets us treat goals as constraints on whole trajectories
rather than one-step rewards.
Remark 996. A simple example is Ω being the set of finite-length action-observation histories up
to horizon H, and G being those histories in which a safety predicate never becomes false. The
usefulness is that such a goal can be used as a hard feasibility constraint, independent of how one
trades off other values within the safe region.
Definition 256 (Implicit goal). An implicit goal for O is any stable regularity in action selection
induced by EO and cO that need not be representable as a named constraint in O’s language.
Equivalently: an implicit goal is a goal implemented by policy/habit rather than by declarative
representation.

                                                  386