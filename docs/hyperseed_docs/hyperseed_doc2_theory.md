# hyperseed-theory

Hyperseed: A Scrutability-Style Core Ontology
                 and a Practical Inference-Control Scaffold
                     for Probabilistic Logic Networks
                                              Ben Goertzel

                                             March 3, 2026


                                                 Abstract
         A recurring aspiration in philosophy, linguistics, and cognitive science is that a wide range
     of concepts—and perhaps a wide range of truths—can be reconstructed from a compact base
     vocabulary together with principled inferential bridges. Classical versions include Carnap’s con-
     structional systems and Wierzbicka’s Natural Semantic Metalanguage; Chalmers’ Constructing
     the World reframes the ambition using scrutability: given a compact base and ideal reasoning,
     many truths are conditionally (and sometimes a priori) scrutable from that base.
         We argue that Hyperseed—a formal ontology presented as a semantic stack for mind, expe-
     rience, and reality—can serve as a workable, engineering-relevant variant of a scrutability base,
     and that Probabilistic Logic Networks (PLN), embedded within the OpenCog Hyperon architec-
     ture, provide a concrete mechanism for building approximate intensional reductions of real-world
     concepts into Hyperseed terms. Beyond philosophical alignment, the same reductions yield an
     operational payoff: they can guide PLN inference control via estimates of marginal informa-
     tion gain per unit cost. We outline three complementary control templates (backward chaining,
     forward chaining, and bidirectional geodesic search) and discuss how domain-anchoring and
     embodiment links connect Hyperseed abstractions to concrete sensorimotor or domain-specific
     inference.
         Finally, we argue that representing a core ontology explicitly—rather than only implicitly via
     learned representations—increases a system’s capacity for transparent self-understanding and
     deliberate self-modification, an advantage that becomes increasingly relevant in AGI regimes
     where reflective control and corrigibility-like properties matter. And we explain how one may
     treat the current version of Hyperseed as an initial condition for ongoing automated ontology
     learning, in which an AI system progressively shapes for itself an ontology suitable for optimizing
     its own operations.


Contents
1 Introduction                                                                                             2
  1.1 Core ontologies: the philosophical and linguistic background . . . . . . . . . . . . . .             2
  1.2 Why core ontologies still matter for AI . . . . . . . . . . . . . . . . . . . . . . . . . .          3
  1.3 Hyperseed, Hyperon, and PLN . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .              3
  1.4 Thesis and plan of the paper . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           3
  1.5 Automated ontology learning as meta-inference control . . . . . . . . . . . . . . . . .              4

2 PLN-Based Approximate Intensional Reduction to Hyperseed
  as a Concrete Variant of Chalmers-Style Scrutability                                                     5


                                                     1
    2.1    Motivation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    5
    2.2    An AI-friendly “scrutability” relation . . . . . . . . . . . . . . . . . . . . . . . . . . .    5
    2.3    Intensional reductions as property profiles . . . . . . . . . . . . . . . . . . . . . . . .     6
    2.4    Theorems linking reduction quality to information and complexity . . . . . . . . . .            7
    2.5    How these results fulfill a close variant of Chalmers’ desiderata . . . . . . . . . . . .       8

3 Using Hyperseed to Guide PLN Inference Control                                                   9
  3.1 Hyperseed-guided backward chaining . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
  3.2 Hyperseed-guided forward chaining . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
  3.3 Bidirectional geodesic search . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

4 Structural Conditions for Exponential Speedup in Ontology-Guided Inference                              14
  4.1 Inference as tree search: the two-level picture . . . . . . . . . . . . . . . . . . . . . .         14
  4.2 Stochastic structural conditions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        14
  4.3 Main theorem: stochastic two-level ontological inference efficiency . . . . . . . . . . .           15
  4.4 Graph-theoretic characterization: ontological separation and treewidth . . . . . . . .              16
  4.5 Diagnostic program . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        18

5 Illustrative Examples                                                                         19
  5.1 Illustrative example I: integrative educational diagnosis . . . . . . . . . . . . . . . . 19
  5.2 Illustrative example II: cross-domain creative reasoning . . . . . . . . . . . . . . . . 20

6 Why an Explicit Core Ontology is Valuable for AGI                                                       21

7 Automated Ontology Learning: Growing and Refining the Scrutability Scaffold 22
  7.1 Ontology learning as optimization over definitional theories . . . . . . . . . . . . . . 23
  7.2 Route A: growing an ontology from scratch from inference histories . . . . . . . . . . 24
  7.3 Route B: incremental refinement of a given ontology (e.g. Hyperseed) . . . . . . . . . 25
  7.4 Remarks on richer logics and mechanization . . . . . . . . . . . . . . . . . . . . . . . 27

8 Discussion: Practicalities, Limitations, and Research Directions                                        27
  8.1 Operational meaning of “approximate reduction” . . . . . . . . . . . . . . . . . . . .              27
  8.2 Inference control is where the philosophy pays rent . . . . . . . . . . . . . . . . . . .           27
  8.3 Embodiment and domain anchoring are not optional . . . . . . . . . . . . . . . . . .                27
  8.4 Three complementary learning loops . . . . . . . . . . . . . . . . . . . . . . . . . . .            28

9 Conclusion                                                                                              28


1     Introduction
1.1       Core ontologies: the philosophical and linguistic background
The idea of defining a compact base vocabulary from which broader conceptual ontologies can
be systematically reconstructed has a long lineage. Carnap’s Aufbau [1] sought constructional
systems built from primitive relations; Wierzbicka’s Natural Semantic Metalanguage [2] argues for
a cross-linguistic inventory of semantic primes; and Chalmers’ Constructing the World [5] reframes
the ambition in terms of scrutability bases and ideal reasoning. Computational resources such as
WordNet [3] and FrameNet [4] reflect aspects of these philosophical traditions, though with greatly
restricted representational scope.


                                                      2
    Despite their diversity, these efforts share two key motifs. First, the base vocabulary need not
be tiny, but it should be compact in a principled sense. Second, the process of grounding concepts in
combinations of core elements must not be trivialized—it is not, in general, as simple as representing
a number by its prime factors. For AI, the crucial question is whether such a base can be made
operational: can it guide inference, learning, and self-understanding rather than merely serving as
a philosophical curiosity?

1.2   Why core ontologies still matter for AI
It might seem that the whole approach of ontology-based knowledge representation is a historical
atavism, given the success of approaches such as transformer neural networks. Modern AI systems
routinely learn powerful latent representations that behave as if they contain an ontology: there
are stable clusters, latent factors, and compositional features that guide prediction and action.
However, these implicit ontologies are encoded in weights, distributed vectors, or opaque activation
patterns and are therefore not directly available for explicit reasoning, explanation, or deliberate
revision. This makes it difficult for a system to use its own conceptual structure as an object of
inference and self-modification.
    Classical symbolic AI and knowledge-graph systems have long emphasized explicit ontologies,
but their weakness has typically been brittleness, inability to cope with uncertainty, and poor scal-
ability. Probabilistic and nonmonotonic logic frameworks, including Probabilistic Logic Networks
(PLN) [7], were developed in part to close this gap: retain explicit conceptual structure while al-
lowing uncertain evidence, graded inference, and practical heuristics for search control. Modern
infrastructures such as OpenCog Hyperon [6] provide scalable execution of such frameworks against
sizeable knowledge bases, yet scalable inference control remains a challenge. An appropriately con-
structed ontology can address this challenge by supplying a structured basis for inference-control
heuristics—but only if the ontology is broad, deep, and rich enough to support the full subtleties
of practical reasoning across a flexible variety of domains.

1.3   Hyperseed, Hyperon, and PLN
The Hyperseed ontology [8] is a collection of over 200 formally defined concepts, together with the-
orems relating them and establishing their properties. It is organized as a semantic stack spanning
mind, experience, and reality, and it includes illustrative theoretical material on topics such as AI
ethics and the nature of scientific theory. Crucially, Hyperseed is intended to be operational: it
should change what a reasoning system does, not only what it says.
    Our proposed approach to leveraging Hyperseed for AGI inference sits within the broader Hy-
peron initiative [6]—an AGI-oriented framework that treats a knowledge base as a living, incremen-
tally updated structure (a distributed “atomspace” / knowledge store) coupled to multiple inference
and learning processes. PLN is Hyperon’s uncertain inference engine: it provides a collection of
inference rules and truth-value semantics intended to support reasoning with partial, noisy, and
conflicting evidence while remaining compositional and scalable. Because PLN inference is com-
binatorially explosive, practical use requires inference control: heuristics and learned policies that
decide which rules to apply and which premises to use, under resource budgets.

1.4   Thesis and plan of the paper
We position Hyperseed simultaneously in three roles that are often kept separate:




                                                  3
      • Philosophical role (scrutability / reduction). Hyperseed serves as an expressive base-
        language in which other concepts can be approximately expressed. PLN provides uncertain,
        intensional inference for constructing approximate analyses, using (among other things) the
        Hyperseed principle that “information” is observer-indexed bookkeeping grounded in distinc-
        tions and probabilistic belief.1

      • Engineering role (inference control). Hyperseed supplies structure for estimating which
        inference steps are likely to matter next. Inference control is attention-allocation in the
        reasoning substrate: the management of limited resources2 bounded by effort budgets.3 We
        sketch three control templates—backward, forward, and geodesic—in which Hyperseed guides
        expected marginal information gain per unit cost and interfaces naturally with association-
        spreading mechanisms and learned rule-selection priors.

      • AGI / meta-cognitive role (self-understanding and self-modification). A system
        whose core ontology is explicit in its deliberative language can reason about, critique, and
        revise the way its experience is organized. When the ontology is only implicit, the system may
        still have one, but using it for transparent self-understanding and deliberate self-modification
        becomes substantially harder.

    Our central claim is that PLN-based approximate reduction to Hyperseed, implemented in the
Hyperon framework, can fulfill a close, workable variant of the desiderata articulated in Chalmers’
Constructing the World [5]. In the sections that follow, we make this idea formally precise (Sec-
tion 2), spell out how Hyperseed can guide PLN inference control in several complementary ways
(Section 3), identify structural conditions under which ontology-guided inference achieves exponen-
tial speedup and illustrate the theory with two worked examples (Section 4), and then argue that
making a core ontology explicit is valuable from an AGI perspective (Section 6).

1.5      Automated ontology learning as meta-inference control
Finally, extending the above ideas, we consider the merging of dynamic ontology-formation into
the learning process of the AI system using the ontology.
    To frame this concept, start with our central premise that an ontology is not merely a naming
scheme but an inference-control scaffold: by choosing a base vocabulary B (scrutability primitives)
and a definitional/bridge theory ∆, we induce reduction profiles and graph-structured relevance
relations that shape which inference steps are considered promising under bounded resources. Once
we have explicit, quantitative criteria for evaluating this role (e.g. scrutability-based reduction
quality, separator/leakage diagnostics, and cost-normalized efficiency measures such as OER), it
becomes natural to treat ontology design itself as a learnable optimization problem rather than a
purely manual craft.
    In this perspective, automated ontology learning is a meta-level learning loop that searches over
ontologies O = (B, ∆) using inference histories as training data. The system runs tasks, records
which conceptual reductions and relevance cues actually improved search efficiency, and then pro-
poses ontology edits that would have made those successful traces shorter, more stable, or more
reusable. Two complementary routes are especially natural here: (A) growing an ontology from
  1
    Hyperseed-Concept 98 (Information as Distinction) and Hyperseed-Concept 139 (Probabilistic Belief ) in [8].
These two concepts recur frequently below; subsequent footnote references use abbreviated forms.
  2
    Hyperseed-Concept 60 (Attention) in [8].
  3
    Hyperseed-Concept 100 (Genenergy / Effort) in [8].




                                                      4
scratch by inventing new intermediate concepts that compress frequent proof fragments or cre-
ate better separators in the relevance graph; and (B) incrementally refining a given scaffold (e.g.
Hyperseed) by targeted edits such as adding mediator concepts, splitting or merging overloaded
predicates, and learning/repairing bridge axioms that anchor abstract concepts to domain pred-
icates. In both cases, concepts are treated as logical definitions (not just taxonomy nodes), and
candidate edits are accepted only when they improve the same gain-per-cost signals used for ordi-
nary inference control, after accounting for the added representational/maintenance complexity of
the ontology itself.
    Section 7 sketches concrete algorithms for both routes, including trace-mining candidate con-
cept definitions, replay-based scoring of ontology edits, and conservative budgeted selection of
additions/repairs. This meta-loop completes the paper’s methodological arc: the same formal
quantities that guide which inference steps to take can also guide which conceptual scaffold the
system should build for taking them.


2        PLN-Based Approximate Intensional Reduction to Hyperseed
         as a Concrete Variant of Chalmers-Style Scrutability
2.1        Motivation
Chalmers [5] argues (in the spirit of Carnap, Russell, and Leibniz) that there is a compact collection
of relatively “primitive” expressions (a scrutability base) from which all truths are, in an appropriate
sense, scrutable. Hyperseed is compatible with this spirit: it is explicitly introduced as an ontology
and “core scaffolding” intended to express other concepts, while not claiming to be a final list of
semantic primes. Instead, it aims to guide reasoning and enable deep reconstruction via a semantic
stack.
    The present section makes the Carnap/Chalmers aspiration algorithmically concrete by:

    1. treating a chosen subset of Hyperseed’s ontology as a compact base vocabulary in the Chalmers
       sense;

    2. representing real-world concepts intensionally via properties-with-degrees;

    3. using PLN to build and refine approximate reductions of arbitrary concepts to Hyperseed
       concepts; and

    4. controlling this reduction/inference process using an information-theoretic notion of inten-
       sional inheritance.

2.2        An AI-friendly “scrutability” relation
Chalmers’ scrutability relations capture an epistemic notion, often framed in terms of a-priority.
In deployed AI systems—and especially in multi-source knowledge graphs—one must work with
uncertainty, partial observability, and continual revision.4 We therefore introduce a probabilistic
surrogate that keeps the spirit of the Chalmers project while matching the realities of PLN-style
inference.

    4
        Hyperseed-Concept 139 (Probabilistic Belief ) and the associated concept Belief System in [8].




                                                             5
Definition 1 (Hyperseed base vocabulary). Let H denote the set of Hyperseed ontology predi-
cates/relations currently in use by a reasoning system, organized into a small number of semanti-
cally coherent families (e.g. patterns, processes, representations, beliefs). A Hyperseed base vocab-
ulary is a chosen subset B ⊆ H intended to be “compact” in the Chalmers sense (few families, no
trivial encodings), but still expressive enough to guide reductions and inferences.

Definition 2 (Probabilistic scrutability from a base). Fix a probability model P5 over a space of
“cases” Ω (these may be world-histories, situations, or epistemic scenarios indexed by a context).6
For any propositions S and base-description D, let S(ω) ∈ {0, 1} denote the truth value of S in
case ω.
    We say that S is -scrutable from the base vocabulary B (relative to a class of allowed inference
rules R, e.g. PLN rules) if there exists a formula/derivation ΦB ∈ Form(B, R) such that
                                                                  
                                             P ΦB (ω) 6= S(ω) ≤ .

When  = 0 we call this exact scrutability; otherwise it is approximate scrutability.

Comment. This definition is deliberately close to Chalmers’ while relaxing (i) strict a-priority
and (ii) strict definitional equivalence. It is designed so that improving the reduction ΦB directly
yields improved inference-control heuristics in an uncertain reasoner.

2.3    Intensional reductions as property profiles
The key gap between a philosophical scrutability thesis and a deployable AI mechanism is that
real concepts rarely admit crisp necessary-and-sufficient definitions. A workable substitute is to
represent a concept by a profile of weighted properties: a structured intension rather than an
extensional set of instances.

Definition 3 (Intensional property-profile concept). A concept W is represented by a finite multiset
of properties
                             Prop(W ) := {(W1 , e1 ), . . . , (Wm , em )}
where each Wj is a predicate (often drawn from H) and each ej ∈ [0, 1] is a degree indicating the
probability/extent to which Wj applies when W applies.7

Definition 4 (Hyperseed reduction profile). Given a base vocabulary B ⊆ H, a Hyperseed reduc-
tion profile of a concept W is any profile PropB (W ) of the form

                            PropB (W ) := {(F1 , d1 ), . . . , (Fk , dk )},     Fi ∈ B,

intended to approximate Prop(W ) well enough that W becomes -scrutable from B (Definition 2)
for suitably small .
   5
     Hyperseed-Concept (Probability) in [8].
   6
     Cf. the Hyperseed concept Contexts and Aspects in [8].
   7
     This “properties-with-degrees” form is intended as an abstract interface. In PLN, the ej may be realized as truth
values, strength/confidence pairs, or other uncertain annotations.




                                                          6
2.4      Theorems linking reduction quality to information and complexity
To use reductions as an inference-control heuristic, we need a scalar notion of how much a candidate
base concept F actually helps us understand W . Information theory provides exactly this: the
mutual information I(F ; W ) is the expected reduction in uncertainty about W gained by learning
F .8
Theorem 1 (Mutual information equals expected uncertainty reduction). Let F and W be Bernoulli
random variables representing the propositions “x is F ” and “x is W ” under some case distribution
on Ω. Let H(·) denote Shannon entropy. Then

                                       I(F ; W ) = H(W ) − H(W | F ),

so I(F ; W ) is exactly the expected reduction (in bits) in uncertainty about W obtained by knowing
F.
Proof. This is immediate from the definition of mutual information:

                      I(F ; W ) := H(W ) − H(W | F ) = H(F ) + H(W ) − H(F, W ).



    If we may pick only k Hyperseed primitives to form a reduction profile, a natural criterion is
to choose those that jointly maximize information about W , thereby minimizing residual uncer-
tainty. This connects directly to a practical PLN control strategy: route attention toward the base
predicates that maximize expected information gain.
Corollary 1 (Best k-primitive reduction as an information objective). Let S = {F1 , . . . , Fk } ⊆ B
be a set of base predicates. Then

                                   I(W ; S) = H(W ) − H(W | F1 , . . . , Fk ).

In particular, minimizing the residual uncertainty H(W | F1 , . . . , Fk ) is equivalent to maximizing
I(W ; S).
Proof. Apply Theorem 1 with F replaced by the joint variable (F1 , . . . , Fk ).

    Chalmers emphasizes that a compact base must avoid trivializing mechanisms (e.g. encoding
all truths into a single number). In an AI reduction framework, a direct way to prevent this
is to penalize description complexity of primitives. Algorithmic information theory makes the
point precise: a primitive that “encodes everything” must itself be very complex and is therefore
disfavored by a minimum-description-length objective.
Theorem 2 (Complexity-regularized reduction discourages trivial encodings). Let K(·) denote
prefix Kolmogorov complexity, and let K(W | F ) denote conditional complexity. Define the MDL-
style score
                               L(F → W ) := K(F ) + K(W | F ).
Then for any F ,
                                         L(F → W ) ≥ K(W ) − O(1).
Consequently, any “trivializing” primitive Ftriv that makes K(W | Ftriv ) = O(1) must satisfy
K(Ftriv ) ≥ K(W ) − O(1), hence cannot reduce the total description length below the inherent
complexity of W .
  8
      Hyperseed-Concept (Mutual Information) in [8].


                                                       7
Proof. A standard coding inequality for Kolmogorov complexity gives

                                    K(W ) ≤ K(F ) + K(W | F ) + O(1),

because a shortest description of F together with a shortest conditional program for W given F
yields a description of W . Rearranging yields the claimed lower bound on L(F → W ). The final
claim follows by substituting Ftriv and using K(W | Ftriv ) = O(1).

    Classical ontologies (including many linked-ontology systems) often use extensional “is-a” (sub-
set) relationships. For a unified reduction framework, it is valuable to recover this as a special case
of the richer intensional machinery, ensuring that linking Hyperseed to existing ontologies does not
require different conceptual equipment.

Theorem 3 (Extensional inheritance as a special case of intensional inheritance). Assume that the
properties in an intensional profile correspond to singleton elements and degrees are in {0, 1}, so that
each concept corresponds to a set of instances. Then intensional inheritance reduces to extensional
inheritance (a probabilistic subset/overlap relationship): knowing x ∈ F informs x ∈ W exactly via
set overlap, and the information-based inheritance score is determined by these overlaps.

Proof. Under the stated assumptions, each concept corresponds to a subset of instances; let |F | = n,
|W | = m, and |F ∩ W | = k under a uniform prior on instances. Then

                                                        |F ∩ W |  k
                                         P(W | F ) =             = ,
                                                          |F |    n

which is precisely the extensional overlap/subset signal. The mutual-information formulation then
collapses to this set-based dependence because the only dependencies between F and W are via
instance overlap.

2.5      How these results fulfill a close variant of Chalmers’ desiderata
We now summarize, point by point, how PLN-based approximate reduction to Hyperseed realizes
a workable cousin of the Chalmers program:

  1. A compact base vocabulary. Hyperseed’s ontology is explicitly positioned as core scaf-
     folding for expressing other concepts, organized into a semantic stack of concept families.
     Taking B ⊆ H (Definition 1) corresponds directly to choosing a compact set of expression
     families.

  2. Intensional, not merely extensional, reduction. Reduction profiles (Definitions 3–
     4) treat a concept by its structured meaning-properties (intension) rather than only by its
     extension. This aligns with the Hyperseed commitments to Representation and Mind-World
     Correspondence.9

  3. Approximation and refinement rather than brittle definitions. Approximate scrutabil-
     ity (Definition 2) is designed so that successive refinements of a reduction profile can strictly
     decrease  by increasing the mutual information captured (Corollary 1).

  4. Avoiding trivializing mechanisms. Theorem 2 makes precise why “encode everything
     into one primitive” is disfavored by a complexity-regularized reduction objective.
  9
      Hyperseed concepts Representation and Mind-World Correspondence in [8].


                                                        8
     5. Compatibility with existing ontologies. Theorem 3 guarantees that extensional inheri-
        tance is recovered as a special case, providing a principled route to link Hyperseed to external
        ontologies while still using an intensional, information-theoretic reduction score to guide in-
        ference.
     6. Direct inference-control heuristic. Given a query about W , prioritize PLN inference
        steps that condition on base predicates F ∈ B with highest estimated I(F ; W ), since this
        yields maximal expected uncertainty reduction (Theorem 1) per inference step.

Bottom line. Chalmers’ project can be read as claiming that, in an idealized epistemic setting,
meanings and truths can be systematically recovered from a compact base. Hyperseed provides a
candidate ontology-level base of concept families; PLN provides uncertainty-aware inference; and
intensional inheritance provides a mathematically grounded metric for constructing and refining
reductions. Together these deliver a detailed, workable realization of a close variant of the Chalmers
desiderata.


3         Using Hyperseed to Guide PLN Inference Control
PLN inference is powerful but combinatorially explosive: at any moment there are many possible
rule instances to apply and many possible premises to combine, and naive search rapidly wastes
resources. Hyperseed offers a way to turn the knowledge base into a control surface: it provides a
structured notion of semantic proximity, abstraction level, and cross-domain resonance that can be
used to estimate which candidate inference actions are likely to yield progress.
    From a Hyperseed perspective, inference control is a special case of attention allocation: the
system must allocate limited genenergy across many possible operations.10 The most direct quan-
titative idea is:

           Prefer inference steps with high expected marginal information gain (about what we
           care about) per unit effort cost.

The GTGI-inspired machinery makes this analogy crisp: we can treat an inference episode as
a context with an associated resource-consumption distribution, and interpret “good inference
control” as maximizing a competence-per-resource functional in the spirit of efficient pragmatic
general intelligence, specialized to the “environment” constituted by the current knowledge base,
rule set, and query.11
    Practically, the heuristics split into two partly separable problems:

         • Rule selection: which inference rule schema (and high-level instantiation pattern) to try
           next—often best learned from prior inference trajectories.
         • Premise selection: given a rule schema, which candidate premises to bind into it—often
           best guided by relevance signals and association-spreading dynamics (attention as resource
           allocation).

    Below we present three control templates—backward chaining, forward chaining, and a bidirec-
tional geodesic methodology—each designed so that Hyperseed can plug in as a guide to expected
marginal information gain.
    10
   Hyperseed-Concept 60 (Attention) and Hyperseed-Concept 100 (Genenergy / Effort).
    11
   Hyperseed-Concept 214 (Context), Hyperseed-Concept 216 (Resource-Consumption Distribution),      and
Hyperseed-Concept 217 (Efficient Pragmatic General Intelligence).


                                                    9
3.1       Hyperseed-guided backward chaining
Backward chaining begins from a target conclusion and works upstream toward premises. In PLN
this means: given a query Q, select a rule that could derive (or strengthen) Q, then select subgoals
whose satisfaction would enable that rule instance, and iterate.
    Hyperseed enters in two places: (i) it supplies semantic decompositions of Q into nearby/related
concepts, suggesting plausible intermediate subgoals; and (ii) it helps estimate which subgoals
are likely to be informative about Q relative to the current belief state, i.e., which ones reduce
uncertainty in distinctions relevant to Q.12

Technical sketch. Let B denote the current belief state (a set of PLN truth-valued expressions),
and let Q denote the current query. Consider a candidate backward step a that replaces Q by
a multiset of subgoals {G1 , . . . , Gm } together with a planned rule instance schema σ such that
σ(G1 , . . . , Gm ) ⇒ Q.
   Define a scoring functional
                                                                              
                                                     E ∆IHS (B, Q | a)
                                 Score← (a; B, Q) :=                   ,                                       (1)
                                                         Cost(a)
where:
       • IHS is any Hyperseed-indexed information/relevance functional—for example, entropy reduc-
         tion over a Hyperseed-induced partition of conceptual space, or a Hyperseed graph-distance-
         weighted estimate of uncertainty reduction. This reflects the “observer-indexed bookkeeping”
         stance used throughout Hyperseed: distinctions drive what counts as information, and beliefs
         weight those distinctions.13
       • Cost(a) is an effort/genenergy estimate14 —e.g. CPU time, memory bandwidth, or proof-
         search expansion budget.
       • The expectation is taken over uncertain bindings and uncertain premise truth-values (PLN-
         style).
       The control policy is: choose a maximizing Score← (a; B, Q), subject to budget constraints.

Implementation notes. In practice the pieces in (1) are best estimated by different mechanisms
at different granularities:
       • Rule selection as probabilistic program generation. Maintain a learned prior over rule
         schemas and macro-patterns of chaining, drawn from saved inference histories. Hyperseed
         can index and condition this prior by ontological type, abstraction level, and analogy class.15
       • Premise selection via association-spreading (ECAN-like). Given a rule schema, select
         premises by spreading activation from the current query and/or subgoals through the knowl-
         edge graph. Hyperseed provides the high-level semantic scaffolding for what edges exist and
         how activation should decay across them. This is attention allocation in the literal Hyperseed
         sense, bounded by resource budgets.16
  12
     Subgoal informativeness is assessed via Hyperseed-Concept 139 (Probabilistic Belief ) and Hyperseed-Concept 98
(Information as Distinction).
  13
     Hyperseed-Concept 98 (Information as Distinction) and Hyperseed-Concept 139 (Probabilistic Belief ).
  14
     Hyperseed-Concept 100 (Genenergy / Effort).
  15
     Cognitive synergy heuristics align here with Hyperseed-Concept 73 (Cognitive Synergy).
  16
     Hyperseed-Concept 60 (Attention) and Hyperseed-Concept 100 (Genenergy / Effort).


                                                        10
3.2     Hyperseed-guided forward chaining
Forward chaining begins from what is currently believed and pushes consequences outward: pick a
rule and a set of supported premises, derive a conclusion, and continue. It is essential for continual
inference in embodied or domain-focused systems, since it can opportunistically derive useful results
before a particular query arrives and can update the belief state as new percepts arrive.
    Hyperseed helps forward chaining avoid degenerating into pointless closure computation by
biasing inference toward concept regions and abstraction levels likely to be useful for the system’s
active goals. In GTGI terms, the environment and goals define a context, and forward inference
tries to increase expected goal-achievement per unit resource.17

Technical sketch. Let B be the current belief state and let G be a set of currently active
goals/queries (possibly empty). A candidate forward step a is a rule instance σ(P1 , . . . , Pk ) ⇒ C
applied to premises Pi ∈ B, yielding a new conclusion C added to B with an updated truth value.
   Define                                                         
                                                 E ∆UHS (B, G | a)
                            Score→ (a; B, G) :=                      ,                             (2)
                                                       Cost(a)
where UHS is a Hyperseed-indexed utility functional measuring expected future usefulness of adding
C to the belief state, relative to active goals G and/or expected goal distributions (observer-indexed
distinctions weighted by probabilistic belief).18
    Common specializations include:

      • Goal-directed: UHS measures expected increase in support for members of G (or decrease in
        their uncertainty).

      • Curiosity / coverage: UHS measures expected increase in conceptual breadth/coverage in a
        Hyperseed-induced partition of conceptual space—naturally resource-sensitive via genenergy
        budgeting.19

Embodiment and domain anchoring. For an embodied AI system (or any system specialized
to a domain), Hyperseed-guided forward inference depends critically on background inference links
connecting Hyperseed concepts to sensorimotor primitives, task affordances, domain ontologies,
instrumentation vocabularies, and so on. These links can be hand-built, learned, or imported (e.g.
via mappings from external ontologies); once present, they function as bridges allowing PLN to
translate abstract Hyperseed-level inferences into concrete, actionable domain conclusions.
    A simple but important monotonicity observation is:

Proposition 1 (Adding sound Hyperseed–domain bridges cannot reduce attainable inference per-
formance). Fix a PLN rule set and a resource budget. Suppose we extend a knowledge base B to
B 0 := B ∪ ∆ by adding a set ∆ of sound bridge axioms/rules connecting Hyperseed concepts to do-
main or embodiment concepts. If the inference controller is allowed to ignore any added axiom/rule
and the evaluation of goal-achievement is monotone in the available set of admissible proof paths,
then the maximum achievable expected goal-achievement using B 0 is at least that using B (for the
same resource budget).
 17
    Hyperseed-Concept 214 (Context) and Hyperseed-Concept 217 (Efficient Pragmatic General Intelligence).
 18
    Hyperseed-Concept 98 (Information as Distinction) and Hyperseed-Concept 139 (Probabilistic Belief ).
 19
    Hyperseed-Concept 100 (Genenergy / Effort).




                                                     11
Proof sketch. Any inference trajectory available in B is still available in B 0 (simply never use the
added bridges). By the assumed monotonicity of evaluation with respect to the available proof-
path set, the optimum over the larger admissible set cannot be smaller than the optimum over the
subset.

   The point is not that bridges automatically help; it is that, under sane control assumptions,
adding correct bridges expands the reachable conceptual territory without forcing degradation.
The real engineering work is making the controller prefer bridges when they offer good expected
marginal gain per unit cost.20

3.3    Bidirectional geodesic search
Forward and backward chaining are asymmetric: one pushes from what is known, the other pulls
from what is wanted. In complex inference problems, either extreme can thrash: forward chaining
can diffuse effort into irrelevant consequences, and backward chaining can generate subgoals that
are hard to ground in available premises. A natural alternative is to work both ends at once,
attempting to connect them in the middle.
    Geodesic inference control provides a principled picture of this bidirectional strategy: view
inference as searching for a least-effort path between an initial distribution (premises/priors) and
a goal distribution (desired conclusions/queries), with effort measured in a resource-sensitive way.
The Schrödinger-bridge view yields a canonical form of intermediate guidance: weight intermediate
states by a product of a forward factor (reachability from the past) and a backward factor (usefulness
toward the future). This directly motivates bidirectional chaining: grow frontiers from both ends
and prefer steps that improve the product per unit effort.

Technical sketch. Let X be a space of candidate intermediate inference states (e.g. partial
proofs, partial bindings, or subgoal sets). Let ρinit be an initial distribution over X induced by
the current premises, and let ρgoal encode what “being close to the goal” means (e.g. states that
already entail the query with high support). A geodesic controller maintains two frontiers:

    • a forward frontier grown from ρinit (premise-side reachability),

    • a backward frontier grown from ρgoal (goal-side pull).

    Introduce two potentials φ := log f and ψ := log g, where heuristically:

    • f (x, t) measures how easily the forward process can reach x by time t,

    • g(x, t) measures how easily x can continue to the goal by time t.

    A generic step-selection score is then

                               Scoregeo (step s) := ∆(φ + ψ) − λ ∆Cost(s),                                       (3)

where λ > 0 trades off benefit against effort cost.
   A minimal pseudocode sketch:
  20
     I.e., the controller must treat bridge-use as an attention-allocation decision—Hyperseed-Concept 60 (Attention)—
subject to genenergy budgets—Hyperseed-Concept 100 (Genenergy / Effort).




                                                         12
init forward frontier F with rho_init
init backward frontier B with rho_goal
while budget not exhausted:
  choose a side to expand (to keep step-costs roughly equal)
  for each candidate step s from chosen frontier node x:
    estimate phi(x_next), psi(x_next)    # from f,g surrogates
    score[s] = (phi+psi at x_next) - (phi+psi at x) - lambda*cost(s)
  take top-K steps, update frontier estimates
  attempt to splice a forward and backward partial path that meet/unify
return best spliced paths found

Approximating the forward and backward factors. In practice f and g are estimated by
statistical and structural surrogates:

   • local message passing when the inference constraints factorize (factor-graph style),

   • short-horizon Monte Carlo “meet” probabilities between frontiers,

   • amortized predictors trained from prior inference runs (learned φ, ψ).

Hyperseed enters here by (i) defining which semantic factorization is appropriate (ontology-induced
structure), and (ii) shaping the features used by learned predictors (ontological type, abstraction
depth, archetype adjacency, etc.).

Why the product guidance is principled. A key conceptual reason to prefer bidirectional
geodesic guidance over ad hoc mixtures is that the product f · g is the canonical time-symmetric
way to weight intermediate states between boundaries:

Proposition 2 (Time-symmetric intermediate weighting has product form). In a Schrödinger-
bridge (least-effort) interpolation between boundary distributions, the time-t intermediate weighting
that remains consistent under arbitrary subdivision of the interval is (up to normalization) the
product of a forward factor f (·, t) and a backward factor g(·, t):

                                        ρ(x, t) ∝ f (x, t) g(x, t).

Proof sketch. Schrödinger-bridge theory yields a unique bridge marginal at intermediate time t
determined by the boundary data and the reference dynamics. This bridge marginal factorizes into
a forward and backward solution of the corresponding scaling equations; the factorization implies
time symmetry, and the uniqueness implies interval consistency. The product form is therefore not
an arbitrary heuristic but the canonical intermediate weighting induced by the boundary-value,
least-effort formulation.

   From the Hyperseed perspective, the significance is that the controller implements a resource-
sensitive attention policy that is structurally compatible with two-ended guidance: it avoids both
pure diffusion (forward-only) and pure fantasy (backward-only), and it naturally fits the cognitive-
synergy theme because different subsystems can specialize in estimating different parts of the
guidance signal.21
  21
     Hyperseed-Concept 73 (Cognitive Synergy), Hyperseed-Concept 60 (Attention), and Hyperseed-Concept 100
(Genenergy / Effort).



                                                    13
4     Structural Conditions for Exponential Speedup in Ontology-
      Guided Inference
The preceding sections established that Hyperseed can serve as a scrutability-style base (Section 2)
and that its structure can guide PLN inference control (Section 3). The theorems presented so far,
however, are essentially foundational identities and monotonicity arguments: they show that the
framework is coherent and that adding ontological structure cannot hurt, but they do not explain
when it provides a dramatic advantage. A natural question remains: under what conditions does
ontology-guided inference achieve exponentially better performance than unguided search, and how
can one empirically verify that those conditions hold?
    This section answers both questions. We introduce stochastic structural conditions on the
relationship between the Hyperseed base and the broader concept space, prove that these condi-
tions imply exponential search-cost reduction, characterize the conditions graph-theoretically via
an approximate separator / ontological treewidth framework, and describe a diagnostic program
for empirically measuring whether the conditions hold in a deployed system. We then illustrate the
theory with two worked examples.

4.1    Inference as tree search: the two-level picture
PLN inference can be modeled as exploring a search tree T of depth D and per-node branching
factor up to b. At each internal node v (representing a partial inference state), the system chooses
among Ch(v) candidate next steps (rule instantiations and premise bindings). The value function
J ∗ (v) = maxw∈Ch(v) [g(v, w) + J ∗ (w)] satisfies the Bellman equation, where g(v, w) is the net gain
of a single inference step. Exhaustive search costs O(bD ).
     Each inference state v admits a Hyperseed projection πB (v) ∈ Rn (its reduction profile with
respect to the ontological base B, |B| = n  N ). The central question is whether πB (v) is
informative enough to guide search.
     The realistic picture is a two-phase decision at each node:
    1. Ontological triage (cheap). Use πB to partition Ch(v) into ontological clusters—groups
       of children that look similar from the abstract-ontological standpoint—rank the clusters by
       projected value, and discard clusters that are clearly unpromising.
    2. Concrete discrimination (moderate cost). Within each surviving cluster, use domain-
       specific data and local reasoning to identify the best child.
The total cost per level is (number of surviving clusters) × (cost to resolve each cluster), iterated
over D depth levels.
    This two-level structure reflects an important asymmetry. An abstract ontology like Hyperseed
can distinguish types of inference actions (e.g. “morphological comparison” vs. “chemical analysis”
for an animal-classification query) but cannot distinguish specific instances within a type (e.g.
“compare ear length” vs. “compare tail shape”). The former is ontological triage; the latter is
concrete discrimination requiring domain data.

4.2    Stochastic structural conditions
In any realistic deployment the system faces a distribution D of inference problems. We state
conditions under the node-visit distribution µ: the distribution over nodes actually encountered by
the guided controller during inference on ω ∼ D. This is important—conditions need not hold at
nodes the controller never visits.

                                                 14
    At each visited node v, the Hyperseed clustering yields K(v) clusters, q(v) of which survive
triage, with per-cluster concrete-resolution costs ck (v).

Definition 5 (Stochastic Ontological Cluster Separation, SOCS(β̄, τ )). For each cluster Ck (v)
let Vkmax (v) = maxw∈Ck [g(v, w) + J ∗ (w)] and let V̂k (v) be its Hyperseed-projected value estimate.
Define the local OCS failure event:

                                         ∃ j, k : V̂j > V̂k + 3β̄ but Vjmax ≤ Vkmax .
                                        
                           Fail(v) =

We require:

 (a) Prv∼µ [Fail(v)] ≤ τ        (low failure rate).

 (b) Ev∼µ [β(v)] ≤ β̄        (controlled average tolerance), where β(v) is the smallest β for which OCS
     holds at v.

   This condition says: the ontological projection usually ranks clusters correctly, but is allowed to
be confused at a τ -fraction of nodes and to have tolerance up to β̄ on average. It does not require
the projection to rank children within a cluster—that is what concrete reasoning handles.

Definition 6 (Stochastic Cluster Tractability, SCT(q̄, c̄, σq , σc )). Under µ:
                                               hP                       i               hP                   i
       E[q(v)] ≤ q̄,       Var[q(v)] ≤ σq2 ,   E    k retained ck (v)       ≤ c̄,   Var      k retained ck (v)   ≤ σc2 .

    Note that cluster sizes do not appear as a separate condition; they are folded into ck (v). A large
cluster that is easy to resolve (concrete features are very discriminating) is fine. A small cluster
that is expensive to resolve is also fine if it is atypical. What matters is the total cost distribution.

Definition 7 (Projection Efficiency, PE(p(n))). Computing V̂k for all K(v) clusters at node v costs
at most K(v) · p(n) operations, where p is polynomial in the Hyperseed base size n.

4.3   Main theorem: stochastic two-level ontological inference efficiency
Theorem 4 (Stochastic Two-Level Ontological Inference Efficiency). Let D be a distribution over
inference problems with trees of depth at most D and per-node branching factor at most b. Assume
SOCS(β̄, τ ), SCT(q̄, c̄, σq , σc ), and PE(p(n)). Consider the two-level guided controller AH+C that
at each node performs ontological triage (retaining clusters within 3β̄ of the top projected value)
followed by concrete discrimination within each retained cluster.
(a) Expected regret (greedy controller). If the controller commits greedily to the best-estimated
child at each level,
                         Eω∼D J ∗ (s0 ) − J A (s0 ) ≤ D 6β̄ + Rmax τ
                                                                   

where Rmax bounds single-step gain.
(b) High-probability regret. With probability ≥ 1 − δ:
                                                                                 q                
                       ∗           A
                   J (s0 ) − J (s0 ) ≤ D 6β̄ + Rmax τ + O Rmax D ln(1/δ) .


(c) Expected computational cost.
                                                                                    
                                       E[Cost(AH+C )] ≤ D K̄ p(n) + c̄

                                                          15
where K̄ = E[K(v)].
(d) Exponential speedup. The expected speedup over exhaustive search is

                                                 bD
                                                            ,
                                            D(K̄ p(n) + c̄)

which is exponential in D whenever the per-node guided cost K̄ p(n) + c̄ is bounded.
(e) Exact optimality (multi-path variant). If the controller recurses on all q(v) surviving
cluster-winners at each level, it finds the exactly optimal path with probability ≥ 1 − τ D. The
                                              D , where q
expected number of nodes explored is at most qeff                     2
                                                          eff = q̄ + σq /q̄ accounts for variance across
                                         D
levels. The expected speedup is (b/qeff ) .

Proof. Part (a). At each level `, let w`∗ be the truly optimal child and w̃` the controller’s selection.
Single-level regret R` splits into two cases.
    Case 1: no OCS failure (probability ≥ 1 − τ ). The cluster containing w`∗ is retained: if it were
excluded, some other cluster would be confidently ranked above it, yielding V̂j > V̂k∗ + 3β̄ with
Vjmax ≤ Vkmax
            ∗  , contradicting SOCS. All retained cluster-winners have projected values within 3β̄ of
each other (by the retention threshold), so their true max-values differ by at most 6β̄ (accounting
for β̄ tolerance in both directions). Thus R` ≤ 6β(v` ), and E[R` · 1[no fail]] ≤ 6β̄.
    Case 2: OCS failure (probability ≤ τ ). R` ≤ Rmax , so E[R` · 1[fail]] ≤ Rmax τ .
    Summing: ` E[R` ] ≤ D(6β̄ + Rmax τ ).
                 P

Part (b). The failurep indicators 1[fail at v` ] are Bernoulli with parameterP≤ τ . Their sum F
satisfies Pr[F > Dτ + D ln(1/δ)/2] ≤ δ by Hoeffding’s inequality. Similarly, ` β(v` ) concentrates
around Dβ̄. A union bound gives the stated high-probability bound.
Part (c). Per level the controller computes cluster projections (K(v) · p(n)) and resolves retained
          P
clusters ( k ret. ck (v)). Expectations under µ give the bound.
Part (d). Ratio of bD to the Part (c) bound.
Part (e). At each level the optimal child is among the q(v) survivors (when OCS does not fail);
the failure probability over D levels is ≤ τ D by a union bound. For the node count, if q(v` ) are
independent across levels then E[ ` q(v` )] = q̄ D ; under positive correlations the bound inflates to
                                       Q
 D with q
qeff                   2                          2      2   2
           eff = q̄ + σq /q̄ (via the identity E[q ] = q̄ + σq and a product-moment inequality).

Remark 1. The Ontological Efficiency Ratio OER = log q̄/ log b is the key summary statistic. The
exponential speedup factor is b(1−OER)·D . OER = 0 means perfect discrimination (only one cluster
survives); OER = 1 means no discrimination at all.

4.4   Graph-theoretic characterization: ontological separation and treewidth
The preceding theorem assumes SOCS. A natural follow-up question is: what structural property
of the concept graph causes SOCS to hold? The answer is that the Hyperseed base acts as an
approximate separator—a “thin waist” through which most long-range conceptual dependencies
flow.

Definition 8 (Concept relevance graph). Let C = {C1 , . . . , CN } be the working concept space. The
concept relevance graph Gη = (C, E, w) has edge weights w(i, j) = I(Ci ; Cj ) (mutual information
under the system’s belief distribution), thresholded at η > 0.


                                                   16
Definition 9 (Approximate Ontological Separation, AOS(, s)). B is an (, s)-approximate sepa-
rator if, upon removing B from Gη :

  1. the residual graph Gη [C \B] decomposes into connected components R1 , . . . , RL of size at most
     s;

  2. the leakage—total weight of edges between distinct residual components—satisfies Leak(B) :=
       i∈Ra , j∈Rb , a6=b w(i, j) ≤  Wtotal , where Wtotal =
     P                                                        P
                                                               (i,j)∈E w(i, j).

    Condition 1 says that without the ontological scaffold the concept space fragments into small
domain-specific islands. Condition 2 says that cross-island information flow bypassing the ontology
is a small fraction  of the total.
    The separator property implies an approximate conditional-independence structure:

Proposition 3 (Separation implies approximate Markov blanket). If B satisfies AOS(, s) and P
satisfies the local Markov property with respect to Gη , then for all a 6= b,

                                                        Leak(B)
                                                                   
                               I(Ra ; Rb | B) ≤ O                       = O( Wtotal /η).
                                                           η
Proof sketch. Under the local Markov property, exact graph separation implies exact conditional
independence. Leakage edges contribute residual conditional dependence bounded, via the data
processing inequality applied per edge, by the total leakage weight divided by the threshold η.

    This approximate Markov blanket property is what makes SOCS hold: the Hyperseed projec-
tion captures most of the inter-regional dependence structure, so it can correctly rank clusters of
inference actions that exploit different concept regions.

Definition 10 (Ontological treewidth). twB (Gη ) is the treewidth of the residual graph Gη [C \ B].

Theorem 5 (Separation implies SOCS; treewidth controls concrete cost). Let Gη be the concept
relevance graph with Hyperseed base B satisfying AOS(, s), and let t = twB (Gη ). Suppose P
satisfies the local Markov property and the inference value function decomposes additively over
concept-footprint contributions:

                         g(v, w) + J ∗ (w) = φB (w) +
                                                                      X
                                                                                  φa (w) + ξ(w)
                                                                 a:Ra ∩F (w)6=∅

where φB depends only on πB (w), each φa depends on local state within Ra , and ξ captures cross-
component leakage. Then:
                    √
(i) E[|ξ|2 ]1/2 ≤ O(  k∇C J ∗ k), where k∇C J ∗ k is a Lipschitz constant of the value function.
(ii) SOCS(β̄, τ ) holds with
                                                                                                        !
               √
                           ∗
                                                                                  k∇C J ∗ k2
      β̄ ≤ O         k∇C J k + Eµ [max range(φa )] ,               τ ≤O                                    .
                                       a                                 (typical inter-cluster gap)2

(iii) Concrete-resolution cost within a residual component Ra satisfies c(Ra ) ≤ O(|Ra | · exp(t)).
When t = O(log N ) (logarithmic ontological treewidth), this cost is polynomial in N .




                                                            17
Proof sketch. (i) For an inference step with footprint spanning components Ra , Rb , the leakage
term ξ arises because P(Ra , Rb | B) is not exactly factored. By Proposition 3 and Pinsker’s
                                                  √
inequality the total-variation distance is O( ); the value perturbation is bounded by k∇C J ∗ k
times this distance.
                                              (k)
     (ii) The projected value V̂k estimates φB . From the additive decomposition, inter-cluster value
                                              (j)   (k)
discrepancy equals the ontological gap (φB − φB ) plus concrete and leakage residuals bounded
                                                                       √
by maxa range(φa ) + range(ξ). The leakage contribution to β̄ is O(  k∇J ∗ k) from part (i). For
τ : ranking failures occur when residuals exceed the inter-cluster ontological gap; by Chebyshev the
failure probability is O(k∇J ∗ k2 /gap2 ).
     (iii) Standard results in graphical-model inference: exact inference in a model with treewidth
t costs O(nvars · dt+1 ), where d is the per-variable domain size.

Interpretation. Theorem 5 explains why abstract ontological concepts are natural graph sep-
arators. Abstraction is precisely the cognitive operation of identifying structure shared across
domains. Shared structure manifests as hub nodes in the concept graph: “morphological pattern,”
“causal process,” “distinction,” “representation” mediate dependencies between otherwise disparate
domain-specific concept clusters. Remove these hubs and the graph fragments into domain islands.

4.5   Diagnostic program
All conditions are empirically testable from inference traces and the knowledge base.

Ontological Efficiency Ratio (OER). OER     [ = log q̄ˆ/ log b̄. This is the headline number: the
expected speedup is approximately b̄(1− \
                                        OER)·D .

OCS violation rate τ̂ . At each visited node, check whether the ontological cluster ranking agrees
with the true value ranking for cluster pairs whose gap exceeds 3β̄ˆ. If τ̂ > 0.05, the ontology has
systematic blind spots.

Distribution of surviving clusters q(v). Heavy tails indicate specific inference contexts where
the ontology provides little discrimination. Identifying these contexts indicates where ontological
enrichment would be most valuable.

Regret decomposition. Decompose observed regret into the two sources: (i) imprecision (non-
optimal selection among retained clusters, bounded by 6β̄ per level) and (ii) failure (OCS violations,
bounded by Rmax τ per level). Imprecision is benign and expected; failure indicates structural
problems.

Residual component analysis. Remove B from Gη and compute connected component sizes.
Large components are candidates for ontological enrichment. For each component, compute the
ratio of internal to boundary edges; low ratios indicate poor ontological mediation.

Marginal value of ontological expansion. Progressively add concepts to B and re-estimate
            [
OER. Plot OER(n)     as a function of |B| = n. The plateau point indicates the “natural complexity”
of the ontological base: beyond it, remaining variation is inherently concrete.



                                                 18
Cross-level correlation. Measure Corr(q(v` ), q(v`+1 )) across successive levels. High correlation
means some problems are systematically harder (the ontology is less useful for them); the Version A
search cost inflates above q̄ D .

Spectral coverage (a priori check). Compute the mutual-information matrix M and measure
how much spectral mass the B-columns capture: SC(B) = ni=1 σi (MB )2 / N         2
                                                                  P   P
                                                                       j=1 σj (M) . High
spectral coverage is necessary (but not sufficient) for small β̄.


5     Illustrative Examples
5.1   Illustrative example I: integrative educational diagnosis
To see how ontology-driven reasoning might work in practice, consider an example everyday sce-
nario: an AI tutoring system helping a struggling 15-year-old student. The surface presentation is
failing math/science grades, incomplete homework, increasing absenteeism. The reasoning task is
to diagnose what is actually going wrong and construct a coherent intervention.

The domains involved. This task spans six concept clusters: (i) academic/cognitive (prerequi-
site chains, working memory, reading comprehension), (ii) motivational /psychological (self-efficacy,
anxiety-avoidance cycles, learned helplessness), (iii) social/relational (peer dynamics, teacher rela-
tionships, family pressure), (iv) temporal/developmental (adolescent identity formation, how cur-
rent choices affect future options), (v) resource/practical (limited study time, competing demands),
and (vi) pedagogical (scaffolding, zone of proximal development, spaced repetition).
    Without ontological scaffolding, the system faces b ≈ 15–25 plausible interventions at each
decision point, each grounded in a different domain’s logic. Evaluating cross-domain interactions
(“Will drilling fractions help if anxiety makes her shut down during math?”) requires bridging
between clusters.

Hyperseed concepts as separators. The Hyperseed concept of distinction bridges the aca-
demic and motivational domains: the key diagnostic question—“Is the student failing because she
cannot do the math, or because she will not attempt it?”—is a distinction that is graded, observer-
relative, and evidence-based (probeable by offering scaffolded problems at varying difficulty and
observing engagement patterns). Without this bridge the system would need to independently
discover that the academic assessment question and the motivational assessment question are two
aspects of a single diagnostic distinction.
    Wu wei and effort bridge the resource and intervention domains: the best intervention is one
where the student’s own default tendencies are already partially aligned with the goal, requiring only
gentle steering. Drilling fractions against active anxiety means high forcing cost; first addressing
the anxiety aligns P0 with the learning task, making subsequent instruction low-forcing.
    Attention bridges the cognitive and scheduling domains: study time, emotional bandwidth, and
processing capacity are all instances of resource allocation under constraints—a single Hyperseed-
structured optimization rather than three separate domain-specific problems.
    Representation and resonance bridge the social and intervention domains: the student’s self-
concept (“I’m not a math person”) is a representation that is maintained by social resonance;
changing it requires feedback from trusted others that aligns with and gradually shifts her self-
model.



                                                 19
Efficiency analysis. With b ≈ 20 and q ≈ 3, OER ≈ 0.37—the same as the creativity example,
since both are cross-domain bridging tasks. Over D ≈ 5 major reasoning steps, the speedup is
20(1−0.37)×5 ≈ 104 .

Where the ontology helps less. For purely intra-domain questions—e.g. “What is the best way
to teach fraction addition to a 15-year-old who understands the concept but makes computational
errors?”—the OER would be close to 1: Hyperseed’s abstract concepts add little beyond what
the pedagogical domain’s internal structure provides. The theory predicts that Hyperseed-guided
inference shows its largest advantages for integrative, cross-domain reasoning, exactly the type of
reasoning most needed by a general intelligence.

Diagnostic implication. The residual component analysis (Subsection 4.5) would reveal which
domains are well-separated by Hyperseed and which need enrichment. In this example, the so-
cial/relational domain might show higher leakage  (some direct dependencies between peer influ-
ence and motivation that bypass Hyperseed), suggesting that additional ontological concepts in the
social layer would be valuable.

5.2   Illustrative example II: cross-domain creative reasoning
As a different sort of illustrative example, we consider a reasoning task that we actually carried out
as part of our own AI research: the construction of the Motivated Wu-Wei Creativity Hypothesis [9],
which argues that under resource constraints and repeated sociocultural interaction, AI systems
whose creative behavior is driven by internally grounded motivational dynamics will participate in
creative practice more efficiently than motivation-less prompting approaches.

Why the task is hard without ontological scaffolding. The argument bridges five dis-
tinct conceptual domains normally studied separately: (i) aesthetics / philosophy of art, (ii) KL-
regularized optimal control, (iii) motivational psychology (PSI theory), (iv) social/cultural theory,
and (v) generative AI. Without ontological structure, formalizing the initial informal intuition re-
quires searching across the full product space of formalisms from each domain; with branching
factor b ≈ 20 (plausible formalisms per step) and depth D ≈ 6 (major reasoning stages), the
unguided search space is ∼ 206 ≈ 6 × 107 candidate paths.

Hyperseed concepts as separators. In the concept relevance graph, the five domain clusters
are connected almost entirely through Hyperseed bridge concepts:
    Wu wei / minimal-forcing control mediates between the control-theory cluster and the aesthetics
cluster: the Hyperseed formalization of effort as transport cost plus KL-forcing cost directly yields
the paper’s core formal object J(π; α) = E[ t cα (xt )] + λ E[ t KL(Pπ kP0 )].
                                            P                 P

    Attention and genenergy/effort mediate between motivational psychology and control theory:
the insight that PSI-style modulators shape the passive dynamics P0 (so that a well-motivated
system pays low forcing cost) falls out directly from the Hyperseed framework.
    Resonance mediates between cultural theory and the control/AI clusters: social feedback be-
comes a signal that drives modulator recalibration, adjusting P0 and reducing future forcing cost
for culturally aligned creative behavior.
    Pattern, repetition, and distinction mediate between aesthetics and the formalization of inten-
tion: creative intention becomes “a temporally extended pattern of stable goal selection, coherent
modulator trajectories, and feedback-sensitive revisions that preserve project identity.”


                                                 20
Efficiency analysis. At each reasoning step, ontological triage reduces b ≈ 20 candidates to
q ≈ 2–3 (the ontologically indicated cluster plus one or two alternatives). Over D = 6 steps the
guided search explores ∼ 36 = 729 paths vs. ∼ 6 × 107 unguided—a speedup of roughly 105 , or
OER ≈ log 3/ log 20 ≈ 0.37.
    The concrete intra-cluster work remains: after wu wei identifies KL-regularized control as the
right cluster, the system still needs domain expertise to choose KL divergence over Wasserstein,
derive the exponential tilting theorem, etc. This is the Phase 2 concrete discrimination—bounded
by the cluster size, not the full branching factor.


6         Why an Explicit Core Ontology is Valuable for AGI
Many intelligent systems develop an implicit core ontology because the world and the body impose
regularities: sensors and actuators carve experience into stable dimensions, goals impose repeated
evaluation pressures, and social interaction channels stabilize shared categories. In modern machine
learning, this core ontology is often implicit in a learned representation: present, but not directly
available as an object of deliberation.
    Hyperseed makes a different bet: it is worthwhile to represent a core concept network explicitly
in a manipulable, logical/relational form and then use it as a scaffold for uncertain inference and
for self-modeling. The AGI-relevant claim is not that explicit ontologies are magically “better”
than learned representations; it is that explicitness changes what the system can intentionally do
with its own conceptual structure.
    In Hyperseed terms: attention is the deliberate allocation of limited resources.22 A system
that can bring its own ontological commitments into the focus of attention can devote resources to
understanding and revising them. A system whose ontological commitments are trapped in parts
of its mind that do not interface cleanly with deliberative reasoning may still adapt, but without
the same degree of transparent self-understanding and controlled self-modification.

A formal framing. Let L be the system’s deliberative representation language (the language
in which it formulates explicit hypotheses and plans). Let Θ be a space of internal parame-
ters/structures that determine behavior (which may include subsymbolic encodings). Let M be a
self-modification operator that proposes changes in Θ based on reasoning in L.

         • In an implicit-ontology regime, large parts of the system’s core conceptual commitments live
           in Θ but lack a faithful, manipulable representation in L.

         • In an explicit-ontology regime, there is a reasonably faithful mapping from a substantial subset
           of those commitments into L (e.g. via explicit Hyperseed nodes/relations), so that reasoning
           processes in L can refer to, critique, and revise them.

         This leads to a monotonicity-style advantage claim:

Proposition 4 (Explicit ontological access expands the reachable space of deliberate self-modifica-
tion). Assume: (i) the system’s self-modification proposals are generated by reasoning in L; (ii) the
system can only deliberately modify aspects of Θ that are representable (with usable fidelity) in L;
and (iii) the evaluation criterion for self-modification is monotone with respect to the set of available
deliberate modifications (the system may ignore any proposal). Then, holding everything else fixed,
moving from an implicit-ontology regime to an explicit-ontology regime (by adding an explicit core
    22
         Hyperseed-Concept 60 (Attention) and Hyperseed-Concept 100 (Genenergy / Effort).


                                                          21
ontology such as Hyperseed into L) weakly expands the set of reachable deliberate self-modifications
and therefore cannot decrease the optimum achievable value of the evaluation criterion under a fixed
resource budget.

Proof sketch. By assumption, the set of deliberate modifications available in the implicit regime
is a subset of those available in the explicit regime, because explicit representability in L is a
precondition for deliberate modification. Since the evaluation criterion is monotone in the available
choice set, the optimum over the larger set is at least the optimum over the subset.

Why this matters in practice. The formal claim is intentionally modest (a non-degradation
statement), but it points to two practical AGI advantages of explicit ontology:

         • Better self-understanding. The system can form explicit hypotheses about why it is
           confused, what distinctions it is failing to make, and what conceptual bridges it lacks—
           the same “distinction-first” thinking underlying Hyperseed’s treatment of information and
           probabilistic belief.23

         • More controllable self-modification. The system can propose and evaluate ontological
           revisions as explicit candidates—e.g. adding, removing, or restructuring concept links—with
           explicit resource/effort accounting.24 When the ontology is only implicit, analogous changes
           may still occur via learning, but they may be harder to steer using deliberative reasoning.

    In short: an explicit Hyperseed-like core ontology does not replace learning; it changes the inter-
face between learning, reasoning, and reflection. It makes the ontology-directedness of experience
explicit, and that explicitness supports more transparent attention allocation and more targeted
expenditure of genenergy toward conceptual revision.25


7         Automated Ontology Learning: Growing and Refining the Scrutabil-
          ity Scaffold
We have so far been treating Hyperseed ontology as a given, and looking at how to leverage it for
effective AGI-oriented reasoning. However, Hyperseed itself, in its current form, is best considered
a crude first approximation of what an AGI system’s ontology needs to be. Where things get really
interesting is when once considers using Hyperseed as an initial condition for automated ontology
learning.
    Of course, one can also do automated ontology learning from scratch, setting Hyperseed aside.
However, it seems likely that to do this really effectively might require dramatically more compute
time and diversity of system experience than incrementally updating a reasonable initially-provided
ontology such as Hyperseed.
    The preceding sections give a clear foundation for automated ontology learning, via treating
an ontology not only as a representational artifact but as an inference-control scaffold: a base
vocabulary B that induces reduction profiles (Definition 4), which in turn guide search via expected
marginal information gain per unit cost. The point is, once we can measure how well an ontology
supports this role—e.g. via the Ontological Efficiency Ratio (OER) and the associated diagnostics
    23
       Hyperseed-Concept 98 (Information as Distinction) and Hyperseed-Concept 139 (Probabilistic Belief ).
    24
       Hyperseed-Concept 100 (Genenergy / Effort).
    25
       Hyperseed-Concept 60 (Attention) and Hyperseed-Concept 100 (Genenergy / Effort).



                                                         22
(Subsection 4.5) built on Theorem 4 and the separator view (Definition 9, Theorem 5)—it becomes
natural to treat ontology design itself as a learnable optimization problem.
    In this spirit, we now sketch two complementary algorithmic routes to automated ontology
learning that fit the paper’s formal framing:

   • Route A (grow from scratch): induce a compact base and derived concept definitions
     from inference histories, treating concept invention as a compression and separation problem.

   • Route B (refine an existing ontology): start from a given scaffold (e.g. Hyperseed) and
     iteratively repair blind spots and add missing mediators, guided by the same OER/separation
     diagnostics.

   Both routes assume the ontology is more than a term hierarchy: it is a collection of concepts
specified by logical expressions (possibly in a higher-order, paraconsistent, or type-theoretic setting),
plus bridge axioms that connect abstract predicates to domain-anchored ones.

7.1   Ontology learning as optimization over definitional theories
Fix a background logic/language L used by the reasoner. (For PLN+Hyperon, L is the uncer-
tain logic supported by the Atomspace representation; for other implementations, L could be a
paraconsistent predicate logic or a typed logic.) We treat an ontology instance as a pair

                                              O = (B, ∆),

where B is the designated base vocabulary (the “scrutability primitives” used for profiles) and ∆
is a set of definitional and bridge constraints.
    A single learned concept C is represented not merely by a node label but by a definitional
schema in L, e.g.
                                          ∀x C(x) ↔ ϕC (x)
or (in an uncertain / non-brittle encoding) by a pair of implications with graded support,

                                 C(x) ⇒ ϕC (x),         ϕC (x) ⇒ C(x),

each carrying truth-value annotations appropriate to the reasoner. The intent is that ϕC uses
previously available symbols (and possibly second-order constructors) so that adding C constitutes
a genuine abstraction/compression rather than a trivializing encoding (cf. Theorem 2).

Data: inference histories and task episodes. Let D be a collection of reasoning episodes
(queries and tasks), and let H(O) denote the inference histories produced by running the system
under ontology O (including rule applications, premise bindings, costs, and derived conclusions).
These traces support:

   • estimating reduction-quality signals (mutual information and residual uncertainty; Section 2.4);

   • estimating control-quality signals (OER, τ̂ , q(v) tails, residual component structure; Subsec-
     tion 4.5);

   • proposing candidate abstractions by mining repeated proof fragments and repeated cross-
     domain bridge patterns.


                                                   23
A generic objective. We will not commit to a single scalar objective, but a representative loss
functional is
  L(O) = λscrut · ScrutLoss(D, O) + λctrl · OER(B)
                                            [      + λsep · Leak(B) + λcomp · Comp(O), (4)
where:
   • ScrutLoss measures how well target concepts become -scrutable from B (Definition 2 and
     Definition 4), e.g. via residual uncertainty or held-out prediction error of reduction profiles;

   • OER(B)
     [      is estimated from traces as in Subsection 4.5;
   • Leak(B) is the leakage term from AOS (Definition 9);
   • Comp(O) is an MDL-style proxy for “how much ontology we added,” approximating the
     complexity regularization principles in Theorem 2 (e.g. syntactic description length of ∆ plus
     |B| or proxy Kolmogorov complexity estimates).
The key engineering point is that ontology learning is driven by the same quantities that control
inference: information gain and effort, together with structural separation signals that predict
exponential speedup.

7.2   Route A: growing an ontology from scratch from inference histories
Route A assumes we do not begin with a curated base like Hyperseed, but instead start from a
minimal symbolic substrate and a stream of inference histories. The goal is to invent a compact
base B and definitional theory ∆ that make broad families of concepts increasingly scrutable and
make inference controllable.

A.1 Candidate-generation by compression of proof fragments. A practical way to invent
predicates is to mine repeated structure in inference traces. Two common trace-level motifs are:
   • Repeated conjunctive/relational motifs: the same small pattern of premises repeatedly
     appears as the “useful core” of a subproof. Introduce a new predicate C whose definition ϕC
     captures that motif, so later proofs can use C as a single handle.
   • Repeated bridge motifs: similar cross-domain moves repeatedly occur, but only after long
     detours. Introduce a mediator predicate M whose definition makes the bridge explicit, so the
     concept relevance graph becomes more nearly separated by a thin waist (AOS), reducing q̄
     and thus OER.
    In both cases, the candidate space of ϕC can be generated by a grammar of allowed constructors
in L (conjunction, implication chains, bounded quantification over roles/relations, higher-order
pattern constructors if available, etc.). Candidates are then filtered by whether they (i) occur
frequently enough to pay for their representational cost, and (ii) improve separation or mutual-
information coverage.

A.2 Base-set selection as separator learning. Even with many derived predicates available,
the designated base B matters because it is the feature set used for reduction profiles and for
cluster ranking. Using the concept relevance graph Gη (Definition 8), one can search for B that
approximately separates the graph (Definition 9) while keeping |B| small. Operationally, this is
                                                                                        [
guided by the diagnostic loop: progressively add candidate base predicates and watch OER(n)
plateau (Subsection 4.5).

                                                 24
A.3 Trace-driven learning loop (sketch). A minimal end-to-end Route A loop is:

# Route A: GrowOntologyFromScratch
initialize ontology O = (B, Delta) with a minimal seed vocabulary
repeat until budget exhausted:
  run reasoner on tasks D using O, collect inference traces H
  estimate diagnostics from H:
     OER_hat, tau_hat, residual_components, leakage_hat, etc.
  mine candidate concept definitions Phi from H:
     - frequent proof-fragment motifs
     - frequent cross-domain bridge motifs
  for each candidate definition phi in Phi:
     form edit e = "add new predicate C with definition C <-> phi"
     score[e] = predicted_improvement(OER_hat, leakage_hat, scrut_loss)
               - complexity_penalty(e)
  apply best-scoring edit(s) to O
  occasionally:
     - prune redundant concepts (low use / low MI gain)
     - re-select base set B to improve separator quality
return O

    This loop is deliberately conservative: it uses the same “pay rent” criterion as inference control
itself. A new concept is retained only if it reduces expected scrutability loss and/or improves
separator structure enough to decrease OER, after penalizing the additional descriptive complexity.

7.3   Route B: incremental refinement of a given ontology (e.g. Hyperseed)
Route B begins from an existing curated scaffold O0 = (B0 , ∆0 ) and treats ontology learning as
debugging and enrichment rather than open-ended invention. This setting is directly motivated by
the paper’s diagnostic program (Subsection 4.5), which already identifies where an ontology fails
as an inference-control scaffold.

B.1 Where to edit: using the diagnostic signals. The following signals naturally suggest
specific ontology edits:

   • High OCS violation rate τ̂ : systematic misranking indicates missing mediator concepts or
     missing bridge axioms in ∆ that would make the ontological projection πB track value-relevant
     structure more faithfully.

   • Heavy tails in q(v): there are inference contexts in which the ontology does not discriminate.
     These contexts indicate candidate areas for enrichment: add a small number of concepts whose
     definitions carve that context into better-separated subcases.

   • Large residual components under AOS: if removing B leaves large components, the
     ontology is not acting as a thin waist for those domains. Add concepts whose definitions are
     built from patterns common across those domains (abstractions), or add bridge axioms that
     force more dependencies to flow through existing ontology nodes.

   • Plateau behavior of OER(n):
                               d       if OER does not improve as |B| grows, the candidate ad-
     ditions are likely either redundant or overly concrete. This suggests changing the kind of

                                                 25
     abstraction being introduced (i.e. different grammar/operators for ϕC ), not merely adding
     more terms.

B.2 A small set of ontology edit operators. A practical refinement system can be built from
a small menu of local edit operators:

   • Add a new mediator concept: introduce C with a definition C ↔ ϕC intended to reduce
     leakage between two residual regions.

   • Split an overloaded concept: replace C by C1 , C2 with definitions that partition its typical
     uses, when traces show that a single predicate is used in two semantically distant ways that
     confuse control.

   • Merge redundant concepts: if C1 and C2 are nearly equivalent across traces (high mutual
     information / near-implication in both directions), merge to reduce complexity without losing
     control quality.

   • Repair bridges: add, remove, or re-weight bridge axioms linking abstract concepts to
     domain-anchored predicates, guided by whether those bridges actually reduce scrutability
     loss or improve control.

B.3 Trace-driven refinement loop (sketch). A minimal Route B loop is the same skeleton
as Route A but with a more targeted proposal step:

# Route B: RefineOntology
input: initial ontology O0 = (B0, Delta0)
O = O0
repeat until budget exhausted:
  run reasoner on tasks D using O, collect traces H
  compute diagnostics: OER_hat, tau_hat, q_tail, residual_components, etc.
  identify "bad contexts" where the ontology provides weak discrimination
  propose a small set of edits E:
     - add mediator concepts targeting largest residual components / highest leakage
     - split concepts implicated in high tau_hat contexts
     - repair or add bridge axioms where grounding fails
  for each edit e in E:
     estimate delta_score[e] on held-out traces or via fast surrogate evaluation
     score[e] = delta_score[e] - complexity_penalty(e)
  apply best-scoring edit(s), update base set B if needed
return O

    The key difference from Route A is that refinement is constrained by a strong prior structure
(the existing ontology), so edits should be local and justifiable in terms of the diagnostics. This
aligns with the engineering stance that an ontology should be legible and maintainable: growth
without repair discipline risks creating a large, fragile concept soup that does not function as a
clean separator.




                                                26
7.4    Remarks on richer logics and mechanization
Nothing in the above learning loops depends on a specific choice of L beyond three requirements:

    1. Evaluability: we must be able to evaluate candidate definitions (or at least estimate their
       predictive impact) on traces, so that mutual-information and scrutability-style objectives can
       be computed.

    2. Compositional cost: we must be able to assign an effort/complexity proxy to candidate
       formulas, so that trivializing encodings are disfavored in the spirit of Theorem 2.

    3. Operational linkage to control: the ontology must induce the projection πB used by
       inference control, so that improvements in separation and reduction quality translate into
       improvements in search behavior.

    Thus the same overall approach applies whether concepts are expressed in a higher-order pred-
icate logic, a paraconsistent logic with explicit support and counter-support channels, or a type-
theoretic setting in which concept definitions are types/terms rather than predicates. The unifying
theme is that an ontology is a learned, compression-oriented interface between raw domain detail
and the thin waist required for scalable inference control.


8     Discussion: Practicalities, Limitations, and Research Directions
The material above deliberately spans two genres: philosophy of concepts (scrutability and reduc-
tion) and engineering (inference control). This section sketches how the two constrain each other
once the system is built and deployed.

8.1    Operational meaning of “approximate reduction”
In a PLN+Hyperseed implementation, “reducing a concept W to Hyperseed” is not primarily a
claim about definitional equivalence. It is an algorithmic act: build a reduction profile (or multiple
competing profiles) that makes W more predictable, more compressible, and more inferentially
connected to the rest of the knowledge base. The reduction may improve over time, and multiple
reductions may coexist, indexed by contexts and aspects. This is the intended engineering analogue
of a scrutability-base program: not a final, perfect reduction, but a systematic process that yields
increasingly usable analyses.

8.2    Inference control is where the philosophy pays rent
In large uncertain reasoning systems, the primary bottleneck is rarely the availability of inference
rules; it is the combinatorial explosion of possible rule applications and premise bindings. The
Hyperseed-guided view suggests that a concept reduction profile is not merely explanatory; it is
a feature vector for control. Once an active query is embedded into Hyperseed space, the system
can prioritize steps that are (i) close in the ontology, (ii) high in expected information gain, and
(iii) low in estimated cost.

8.3    Embodiment and domain anchoring are not optional
A common failure mode of purely abstract ontologies is ungrounded inference: beautiful chains of
symbolic steps that do not connect to the world, the body, or the domain of concern. The bridging

                                                 27
proposition (Proposition 1) formalizes a minimal engineering stance: adding sound Hyperseed–
domain bridges can only help if the controller is allowed to ignore them and if evaluation is monotone
in available proof paths. The hard work is building bridges that are (i) correct enough, (ii) rich
enough to matter, and (iii) cheap enough to be used frequently under budget constraints.

8.4    Three complementary learning loops
The overall picture suggests three coupled learning loops:

    • Reduction learning: learn better Hyperseed reduction profiles for concepts as the system
      accumulates evidence and experience—a “semantic compression” loop.

    • Control learning: learn better priors over rule schemas and better relevance estimators for
      premise selection (including association-spreading dynamics)—an “attention allocation” loop.

    • Ontology learning: learn to revise the base vocabulary B and the definitional/bridge theory
      ∆ itself (concept invention, splitting/merging, and targeted bridge construction), using the
      trace-based diagnostics of Subsection 4.5 (OER, τ̂ , q(v) tails, residual component analysis)
      as direct optimization signals—a “scaffold revision” loop (see Section 7).

   The philosophical scrutability view gives a normative target for the reduction and learning
loops; the engineering constraints of inference control give a normative target for the control loop.


9     Conclusion
We have articulated a unified argument—philosophical in motivation and engineering in consequence—
for treating Hyperseed as a practical cousin of a Chalmers-style scrutability base, realized not by
crisp definitions but by uncertain, intensional reductions built and refined through PLN inference.
The core philosophical move is to replace brittle definitional reduction with probabilistic, profile-
based scrutability: concepts become increasingly scrutable from a compact base as their Hyperseed
reduction profiles improve and as the system learns which primitives provide the largest marginal
information gain.
    The core engineering move is to use those same reductions as inference-control scaffolding: back-
ward and forward chaining become tractable when guided by marginal information gain per unit
cost, and bidirectional geodesic search provides a principled way to merge premise-side reachability
with goal-side pull while maintaining explicit resource accounting and (in richer implementations)
evidence conservation.
    Finally, we argued for an AGI-oriented meta-point: making a core ontology explicit in a sys-
tem’s deliberative language expands the reachable space of deliberate self-understanding and self-
modification. Implicit ontologies will emerge in any sufficiently capable learning system, but explicit
ontologies make ontological commitments legible to the system itself, turning them into objects of
reflection and controlled revision. In the Hyperseed+PLN picture, this is not merely a philosoph-
ical preference; it is an architectural affordance that can be used to guide inference, learning, and
reflective cognition under bounded resources.


References
 [1] Rudolf Carnap. The Logical Structure of the World (Der logische Aufbau der Welt). Open
     Court, 1967 (original German edition 1928).

                                                 28
[2] Anna Wierzbicka. Semantics, Culture, and Cognition: Universal Human Concepts in Culture-
    Specific Configurations. Oxford University Press, 1992.

[3] George A. Miller. WordNet: A lexical database for English. Communications of the ACM,
    38(11):39–41, 1995.

[4] Charles J. Fillmore, Christopher R. Johnson, and Miriam R. L. Petruck. Background to
    FrameNet. International Journal of Lexicography, 16(3):235–250, 2003.

[5] David J. Chalmers. Constructing the World. Oxford University Press, 2012.

[6] Ben Goertzel et al. Hyperon: A metacognitive, neural-symbolic AGI framework (re-
    view/overview paper). arXiv preprint (exact identifier to be filled).

[7] Ben Goertzel, Matt Iklé, Izabela Goertzel, and Ari Heljakka. Probabilistic Logic Networks: A
    Comprehensive Framework for Uncertain Inference. Springer, 2008.

[8] Ben Goertzel. Hyperseed ontology: formal presentation and theoretical development. Unpub-
    lished manuscript, January 2026.

[9] Ben Goertzel and ChatGPT 5.2-Pro. Motivated wu-wei creativity: a Hyperseed argument for
    intention-coupled generative AI. Position paper, March 2026.




                                              29