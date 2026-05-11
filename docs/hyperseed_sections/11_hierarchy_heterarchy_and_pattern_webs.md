# 11 Hierarchy, heterarchy, and pattern webs

In Hyperseed terms, ignorance is “not enough distinction-making power or data,” whereas conflict
is “incompatible distinction-making pressures that are both locally supported.” Later (Section 12)
we will connect conflict to resonance/dissonance dynamics. It is often useful to treat these as
empirically and behaviorally different regimes: ignorance tends to invite exploration or refinement
of sensing (seek more data or sharper distinctions), whereas conflict tends to invite adjudication
(seek error sources, reconcile models, or split contexts so that incompatible pressures are not forced
into the same representational frame).
Remark 440. When comparing observers O1 and O2 , two further distinctions are helpful. First, if
ΣO1 ⊆ ΣO2 and PO2 is given, then PO2 restricts to a probability measure on ΣO1 ; this corresponds to
“forgetting” distinctions while keeping coherent odds on the coarser questions. Second, even when
ΣO1 = ΣO2 , different PO (or different EO ) can represent differences in priors, training histories,
or sensor reliabilities: the observer-indexing is therefore not only about what can be asked, but
also about how uncertainty is distributed over what can be asked. These two axes (expressivity
via ΣO and credence via PO and EO ) will matter later when we separate changes in “world-model
resolution” from changes in “belief within a fixed resolution.”

10.3    Shannon information, coding, and divergence
Assume X is finite and ΣO = 2X (or that we have reduced to the finite set of blocks of a partition).
Write pO (x) := PO ({x}).
Remark 441. Notation/conventions. Because X P          is finite, a probability measure PO is equiv-
alent to its point-mass function pO : X → [0, 1] with x∈X pO (x) = 1. The expression pO (x) :=
PO ({x}) is this identification. When we write H(X) later, we mean the Shannon entropy of the
distribution of the random variable X, i.e. the entropy of p(x) on its finite support.
Definition 120 (Entropy and surprise). The surprisal of an outcome x is

                                           sO (x) := − log pO (x),

where log denotes the natural logarithm. The Shannon entropy of PO (in nats) is
                                  X                     X
                      H(PO ) :=       pO (x) sO (x) = −   pO (x) log pO (x).
                                     x∈X                       x∈X

Define also the entropy in bits as
                                                            H(PO )
                                           Hbits (PO ) :=          .
                                                             log 2
Remark 442. Intuition. Surprisal sO (x) is high when x was deemed unlikely by O; entropy
H(PO ) is the average surprisal under the observer’s own expectations. One may read this as the
expected amount of conceptual work needed to accommodate an observation, provided that “work”
is measured in logarithmic units.
   Examples. If pO is uniform on |X| = N , then H(PO ) = log N (maximal uncertainty). If pO
concentrates on one point, entropy is 0 (no uncertainty). A biased coin with p(heads) = 0.9 has
lower entropy than a fair coin, because the observer is rarely surprised.
   Usefulness in this document. Entropy is a bridge from belief to description length: if an
observer believes outcomes are distributed according to p, then optimal codes have expected length
about Hbits (p). This will later be tied to effort-based simplicity (Section 8) and pattern intensity
(Section 9), and it parallels the algorithmic viewpoint on description length emphasized in [16].

                                                    202
Definition 121 (Cross-entropy and KL divergence). Given two distributions p and q on X with
q(x) > 0 whenever p(x) > 0, the cross-entropy and Kullback–Leibler divergence are
                               X                                               X                p(x)
                H(p, q) := −         p(x) log q(x),         DKL (pkq) :=             p(x) log        .
                                                                                                q(x)
                               x∈X                                             x∈X

Remark 443. Notation/conventions. The condition q(x) > 0 whenever p(x) > 0 ensures
log p(x)
    q(x) is well-defined wherever it is weighted by p(x). DKL (pkq) is not symmetric in (p, q) and is
not a metric; it is an information-theoretic divergence.
    Intuition. Cross-entropy H(p, q) is the expected code length (in nats) if the world is distributed
as p but you encode using a code optimized for q. KL divergence is the penalty for that mismatch:
DKL (pkq) = H(p, q) − H(p).
    Usefulness. Later, when we define fidelity and effability, we effectively compare a target item
x with a reconstructed distribution q = decO (d). KL divergence is a canonical way to measure such
mismatches; we do not enforce it as the unique notion of error here, but the reader should recognize
it as a standard candidate.

Proposition 11 (Entropy as optimal expected code length). Let p be a distribution on a finite
alphabet X. Among all prefix-free binary codes with codeword lengths `(x) ∈ N, the optimal expected
length                                             X
                                     L∗ (p) := inf    p(x) `(x)
                                                      `
                                                          x∈X

obeys
                                     Hbits (p) ≤ L∗ (p) < Hbits (p) + 1.

Remark 444. What the proposition says (plainly). If an observer believes outcomes follow
p, then there exists an essentially optimal way to encode outcomes in binary so that the average
number of bits used is about the entropy of p. One cannot beat Hbits (p) on average (lower bound),
but one can get within 1 bit of it with an explicit construction (upper bound).
    Why it matters. This is the classical theorem that makes entropy operational: it is not merely
a numerical ornament on a probability distribution; it is the best achievable average compression
rate under an ideal coding scheme. In the Hyperseed framing, this is one key bridge from belief
to effort: shorter codes mean less representational work, and longer codes mean more (cf. the
effort/simplicity lens in Section 8 and the coding/description lens in [16]).
    Connection to later sections. Patterns (Section 9) are defined by compressive re-description;
the inequality above is one of the classical reasons compression and probability models are insep-
arable. When we later speak of observer-relative “simplicity” or “weakness” as an optimization
principle, this proposition is a basic exemplar of how such minima arise.
                                                                             P −`(x)
Proof.P(Lower bound.) For any prefix-free code, Kraft’s inequality gives        x2      ≤ 1. Let
K := x 2−`(x) and define q(x) := 2−`(x) /K. Then q is a probability distribution, and
                                                          X                p(x)
                                 0 ≤ DKL (pkq) =                p(x) log        .
                                                           x
                                                                           q(x)

Rearranging yields
                X                    X                                 X
             −     p(x) log p(x) ≤ −   p(x) log q(x) = log K + (log 2)   p(x)`(x).
                  x                        x                                             x


                                                      203
                                                         P
Since K ≤P1 we have log K ≤ 0, hence H(p) ≤ (log 2) x p(x)`(x). Dividing by log 2 gives
Hbits (p) ≤ x p(x)`(x). Taking an infimum over codes proves the lower bound.
   (Upper bound.) Define candidate lengths by

                                     `(x) := d− log2 p(x)e ∈ N.

Then 2−`(x) ≤ 2log2 p(x) = p(x), hence
                                         P −`(x)       P
                                            x2      ≤     x p(x) = 1. By Kraft’s inequality, there
exists a prefix-free binary code whose codeword lengths are exactly these `(x) (for instance, via a
Shannon–Fano construction, or by building a binary tree whose leaf depths match `).
    For this code,
                      X              X                        
                         p(x)`(x) ≤      p(x) − log2 p(x) + 1 = Hbits (p) + 1.
                      x               x

Taking an infimum over all codes yields L∗ (p) ≤ Hbits (p) + 1, and since the bound is strict at
the level of L∗ (p) (because an integer-length constraint cannot in general achieve the real-valued
optimum exactly), we obtain L∗ (p) < Hbits (p) + 1 as stated.

Remark 445. On the +1 slack. The additive 1 bit arises from the integrality of `(x) and the
ceiling operation. If one allows idealized non-integer code lengths (or, operationally, block coding
over long sequences and arithmetic coding), the achievable average length can be made arbitrarily
close to Hbits (p). Equivalently: the entropy is the fundamental rate, while the +1 term is a single-
symbol overhead due to discretizing lengths.
    KL divergence as a coding penalty. The proof of the lower bound already contains a more
general statement: if a prefix-free code induces an implicit distribution q(x) ∝ 2−`(x) , then the
expected length satisfies
                       X                             1                 1
                          p(x)`(x) = Hbits (p) +         DKL (pkq) −       log K,
                        x
                                                   log 2             log 2
            P −`(x)
with K =       x2        ≤ 1. Thus, mismatch between the “true” p and the code-implied q shows
up as a nonnegative penalty term (the KL divergence), mirroring the earlier identity H(p, q) =
H(p) + DKL (pkq) in coding form.
    Observer-relativity. In the present document, it is often pO (the observer’s model) rather
than an objective distribution that matters. The same theorem applies with p replaced by pO : if the
observer’s beliefs are wrong, the code that is optimal under pO need not be optimal under the world’s
distribution, but it is still optimal relative to the observer’s own representational commitments.
Remark 446 (Why this matters for Hyperseed). In Hyperseed, “simplicity” is grounded in repre-
sentational effort. The proposition formalizes one standard bridge: a probability model induces an
optimal expected description length. Later sections connect description length to weakness and to
pattern intensity.
Additional detail on the “one checks” step. The feasibility claim for `(x) = d− log2 p(x)e
is the concrete place where discretization (integer lengths) meets the continuous ideal − log2 p(x).
Since `(x) ≥ − log2 p(x), we have

                                   2−`(x) ≤ 2−(− log2 p(x)) = p(x),
               P −`(x)      P
and therefore    x2       ≤   x p(x) = 1. This is exactly Kraft’s inequality for a binary prefix
code, so the length assignment is not merely formal: it is realizable by an actual prefix-free set of
codewords (equivalently, by a pruned binary tree whose leaves occur at depths `(x)).

                                                 204
Where the strict inequality comes from. For any real number r, the ceiling satisfies dre < r+1.
Applying this pointwise to r = − log2 p(x) gives `(x) < − log2 p(x) + 1, hence
   X               X                        X                       X
       p(x)`(x) <     p(x) − log2 p(x) + 1 =       p(x) − log2 p(x) +      p(x) = Hbits (p) + 1,
       x             x                               x                        x

making explicit that the sole source of slack is integer rounding. In particular, when all probabilities
are dyadic (i.e. p(x) = 2−kx for integers kx ), the ideal lengths are already integers and the rounding
loss vanishes, so the upper bound can meet Hbits (p) exactly.
More explicit link between coding and DKL . Given any prefix lengths `(x) satisfying           P Kraft,
the unnormalized weights 2−`(x) form a sub-probability mass function; normalizing by Z := x 2−`(x) ≤
1 yields
                                                      2−`(x)
                                             q(x) =          .
                                                        Z
Then `(x) = − log2 q(x) − log2 Z, so taking expectation under p gives
                                Ep [`(X)] = Ep [− log2 q(X)] − log2 Z.
Because Z ≤ 1, we have − log2 Z ≥ 0, so Ep [`(X)] ≥ Ep [− log2 q(X)]. Finally,
                                                X               p(x)
               Ep [− log2 q(X)] − Hbits (p) =       p(x) log2        = DKL (pkq)   (in bits),
                                                x
                                                                q(x)

so DKL (pkq) ≥ 0 implies Ep [`(X)] ≥ Hbits (p). This makes concrete the interpretation that a code
induces a model q, and the penalty for using the “wrong” model is precisely a KL divergence term.
Units and interpretation. The notation Hbits (p) emphasizes that the logarithm base is 2, so
entropy is measured in bits and code lengths are measured in binary digits. If one instead uses
natural logarithms, the same statements hold with lengths measured in nats and with the conversion
factor log2 t = (log t)/(log 2) accounting for the change of units.
Tightness and algorithmic realizations. The +1 in the upper bound is a worst-case guarantee
for single-symbol (one-shot) coding with integer lengths. In practice, Huffman coding achieves
an expected length within 1 bit of the entropy and is optimal among prefix codes for a fixed
alphabet. Moreover, by coding blocks of n symbols from the product distribution p⊗n , the per-
symbol overhead can be driven to 0 as n → ∞, reflecting that the discreteness penalty is not
fundamental but a finite-length artifact.
Further connection to the Hyperseed framing. In settings where a system maintains an
internal predictive distribution q while the world follows p, the expected description length under q
decomposes into Hbits (p) plus a mismatch cost DKL (pkq). Thus, “simplicity” (short expected code
length) can be read simultaneously as (i) compressibility of observations under the true law and (ii)
adequacy of the internal model. This dual view is often useful when later notions (e.g. weakness,
pattern intensity) depend not only on how much structure is present in p but also on how well an
agent-like representation aligns with it.

10.4       Mutual and interaction information
Let (X, Y ) be a pair of random variables on finite sets with joint distribution p(x, y). In this finite
setting all entropies and divergences below are well-defined (possibly taking value +∞ only if one
allows zero-probability events in ways that make the KL divergence diverge), and I(X; Y ) can be
read as an average quantity over outcomes rather than a pointwise guarantee about any particular
sample.

                                                    205
Definition 122 (Mutual information). The mutual information between X and Y is
                               I(X; Y ) := H(X) + H(Y ) − H(X, Y ).
Equivalently, I(X; Y ) = DKL (p(x, y)kp(x)p(y)). In particular, I(X; Y ) ≥ 0, with equality if and
only if p(x, y) = p(x)p(y) (independence).
Remark 447. Intuition. Mutual information measures how much knowing X reduces uncertainty
about Y (and symmetrically, knowing Y reduces uncertainty about X). The KL expression says: it
is the divergence between the true joint distribution and the distribution you would get if you falsely
assumed X and Y were independent. Equivalently, it is the expected log-likelihood ratio
                                                                    
                                                           p(X, Y )
                                I(X; Y ) = E(X,Y )∼p log               ,
                                                         p(X)p(Y )
so it quantifies the average extent to which joint observations look “surprising” relative to an inde-
pendence model. A useful identity that often clarifies the “uncertainty reduction” reading is
                        I(X; Y ) = H(Y ) − H(Y | X) = H(X) − H(X | Y ),
so it is literally the drop in entropy of one variable after conditioning on the other. From this,
one sees immediately the bounds 0 ≤ I(X; Y ) ≤ min{H(X), H(Y )}: no channel can convey more
information about Y than the total uncertainty that was present in Y to begin with.
    Example. If Y = X (perfect copying), mutual information equals H(X): observing Y tells
you everything about X. If X and Y are independent, then I(X; Y ) = 0. More generally, if Y is
a noisy copy of X through some stochastic channel, then I(X; Y ) decreases as noise increases; in
this sense it is a quantitative measure of “fidelity” that is independent of any particular decoding
rule.
    Usefulness. In a Hyperseed setting, I(X; Y ) is a clean numerical proxy for “how many distinc-
tions about Y are made available by access to X,” i.e. how one representational channel supports
another. This will reappear when discussing pattern webs and dependency-like relations between
representational units (Sections 11 and 12). A further practical reason it is favored is its invari-
ance under bijective reparameterizations of X or Y : relabeling symbols does not change I(X; Y ),
so it depends on the structure of dependence rather than the names of states.
    Chain rules and conditioning. For later use it is convenient to recall the chain rule
                                I(X; Y, Z) = I(X; Y ) + I(X; Z | Y ),
which formalizes the idea that information provided by a compound representation (Y, Z) decomposes
into the part already provided by Y plus the additional part provided by Z once Y is known. Here
I(X; Z | Y ) is the conditional mutual information, defined by
                I(X; Z | Y ) = H(X | Y ) − H(X | Y, Z) = H(Z | Y ) − H(Z | X, Y ),
and it is always nonnegative as well.
Definition 123 (Interaction information). For three random variables (X, Y, Z), the interaction
information is
                             I(X; Y ; Z) := I(X; Y ) − I(X; Y | Z).
This quantity may be positive or negative, reflecting synergy or redundancy. It can also be written
symmetrically in entropies as
       I(X; Y ; Z) = H(X) + H(Y ) + H(Z) − H(X, Y ) − H(X, Z) − H(Y, Z) + H(X, Y, Z),
so it is invariant under permutation of X, Y, Z despite being defined using I(X; Y | Z).

                                                 206
Remark 448. Intuition. Interaction information asks whether the relationship between X and
Y becomes more or less informative once Z is known. If Z explains away the dependence between
X and Y , the quantity tends to be negative (redundancy). If Z unlocks a dependence that is not
visible marginally, it may be positive (synergy). One way to read the sign is:

                          I(X; Y ; Z) > 0   ⇐⇒     I(X; Y | Z) < I(X; Y ),

so conditioning on Z reduces the apparent X–Y association (suggesting that what X and Y “share”
is, in part, already present in Z), whereas

                          I(X; Y ; Z) < 0   ⇐⇒     I(X; Y | Z) > I(X; Y ),

so learning Z reveals dependence between X and Y that was not apparent marginally. The possibility
of negative values is not a paradox: it does not contradict nonnegativity of mutual information,
because interaction information is a difference of two nonnegative quantities.
    Example. In the classical XOR example, X and Y are independent fair bits and Z = X ⊕ Y .
Then I(X; Y ) = 0 but conditioning on Z makes X and Y perfectly dependent, leading to a positive
interaction information: information is present only in the triad. Conversely, if Z is a common
cause that copies into both X and Y (e.g. X = Z and Y = Z), then I(X; Y ) is large but I(X; Y |
Z) = 0, yielding negative interaction information: the apparent X–Y dependence is explained
by the shared variable. These two extremes motivate the informal language of “synergy” versus
“redundancy,” while also hinting that any single scalar can only be a coarse summary of multi-way
dependence.
    Usefulness. Hyperseed frequently emphasizes that cognition is not purely additive: wholes can
carry relations not present in parts. Interaction information is one standard quantitative hint of
such non-additivity, and it resonates with emergence-style notions introduced later in the pattern
section (Section 9). It is also a warning label against naive “Venn diagram” interpretations of in-
formation: although the symmetric entropy formula resembles inclusion–exclusion, the sign changes
show that multivariate dependence does not behave like ordinary set overlap.

Remark 449 (Observer-relative “second law” reading). Entropy-like quantities depend on which
variables are being tracked. If O changes its representational partition (coarse-grains or refines),
then the induced random variables change and so do H and I. Thus, statements that resemble a
“second law” (monotone entropy increase under typical dynamics) should always be read as: for
the chosen coarse variables, under the chosen effective dynamics, typical trajectories move toward
larger macro-uncertainty. This matches Hyperseed’s perspectivism: “the same world” can have
different entropic arrows at different resolutions. A concrete way to see this is that coarse-graining
typically reduces the maximum achievable mutual information between a microscopic state and a
macro-description: when distinctions are merged, there is (by design) less that can be learned from
the coarse variable about fine structure. Dually, refining a partition can create apparent information
flows that were previously invisible, simply because the representational vocabulary has changed.

Remark 450. This remark is a formal caution against turning a contextual regularity into a
metaphysical absolute. The second law (Hyperseed-Concept 164) is robust in physics, but its infor-
mational analogs are always indexed by (i) what we count as a macrostate and (ii) what we treat
as the effective dynamics. Hyperseed’s insistence on observer-indexing is, in this sense, a reminder
that entropy is a measure of description as much as a measure of disorder. In particular, when
one says “entropy increases,” what is usually meant is that the distribution over the tracked vari-
ables spreads out under the chosen dynamics and constraints; but changing the tracked variables

                                                 207
changes the sample space, the constraint set, and the induced notion of “spread.” The same under-
lying micro-dynamics can therefore support multiple, seemingly competing, informational narratives
depending on which distinctions are treated as salient.

10.5    Logical entropy and graphtropy from distinction structure
Logical entropy (also called “Gini impurity” in some applied contexts) measures the probability
that two independent draws fall into different “distinction classes.” In Hyperseed terms, it measures
the fraction of distinctions that are actually made.

Definition 124 (Logical entropy of a partition). Let π = {B1 , . . . , Bk } be a partition of X. Given
a distribution p on X, define the block masses
                                               X
                                         pi :=     p(x).
                                                 x∈Bi

The logical entropy of (π, p) is
                                                         k
                                                         X
                                        h(π, p) := 1 −         p2i .
                                                         i=1

Remark 451. Intuition. Where Shannon entropy measures expected code length under optimal
compression, logical entropy measures expected distinguishability under the partition π. It does
not ask: “How many bits to encode?” but rather: “How often do two random observations fall
into different blocks?” This makes it an especially direct companion to Hyperseed’s primitive of
distinction (Hyperseed-Concept 98) and aligns with Ellerman’s development of logical entropy [17].
P Example.      If π is the discrete partition into singletons, then pi = p(x) and h(π, p) = 1 −
       2
 x p(x) . If π is the trivial one-block partition, then h(π, p) = 0 (no distinctions are made).
    Why useful. Logical entropy is quadratic in p, hence behaves differently from Shannon entropy
under fine-graining; in many cognitive settings, quadratic forms correspond naturally to “pairwise
comparison” processes (e.g. sampling two items and checking whether they are treated as the same).
Graphtropy will generalize this beyond partitions, preserving this pairwise-comparison intuition.

Remark 452. The quantity i p2i is the probability that two iid draws fall in the same block. Hence
                               P
h(π, p) is the probability that two iid draws fall in different blocks, i.e. that the partition makes a
distinction between them.

Definition 125 (Distinction graphs and graphtropy). Let G be a (possibly directed) graph on
vertex set X. We interpret an edge x → y as “O does not distinguish x from y” (an indistinction).
Let ιG (x, y) ∈ [0, 1] be a weight encoding degree of indistinction, with ιG (x, y) = 1 meaning “fully
indistinct” and ιG (x, y) = 0 meaning “fully distinct.” Given a probability distribution p on X,
define the graphtropy as
                                               XX
                               GT(G, p) := 1 −          p(x)p(y) ιG (x, y).
                                               x∈X y∈X

Remark 453. Notation/conventions. ιG : X ×X → [0, 1] is an indistinction   P Pweight rather than
an adjacency matrix in the usual graph-theoretic sense. The double sum x y p(x)p(y) ιG (x, y)
is an expectation over two independent draws X1 , X2 ∼ p of the indistinction degree ιG (X1 , X2 ).
    Intuition. Graphtropy asks: if I sample two items according to p, how indistinguishable are
they on average? Then it flips the answer by taking 1−, so that higher graphtropy means “more

                                                 208
expected distinction”. This makes graphtropy a direct numerical shadow of an observer’s distinction
structure, even when that structure is graded, context-dependent, and not transitive.
    Examples. PIf ιG (x, y) = 1[x = y] (only identical items are treated as indistinct), then
GT(G, p) = 1 − x p(x)2 . If ιG (x, y) = 1 for all pairs (everything indistinct), then GT(G, p) = 0.
    Why useful. Partitions (equivalence relations) are often too rigid for cognitive modeling.
A mind can treat x as indistinct from y in one direction but not the other (asymmetry), and
can treat x ≈ y and y ≈ z without treating x ≈ z (non-transitivity). Graphtropy keeps the core
idea—distinction measured by pairwise sampling—without demanding equivalence-relation structure
(Hyperseed-Concept ??).
Remark 454 (Fuzzy and asymmetric cases). If ιG is crisp and symmetric and transitive (an equiv-
alence relation), then G encodes a partition and graphtropy reduces to logical entropy. If ιG is fuzzy
and/or asymmetric, then graphtropy measures “expected distinguishability” without requiring a par-
tition. This extra generality is important for modeling minds, which often treat “x indistinguishable
from y” as context-sensitive, graded, and non-transitive.
Proposition 12 (Reduction to logical entropy). Let π be a partition of X, and define ιπ (x, y) = 1
iff x and y lie in the same block, and 0 otherwise. Let Gπ be the induced indistinction graph. Then

                                          GT(Gπ , p) = h(π, p).

Remark 455. What the proposition says. Graphtropy is not a competing definition but a
strict generalization: in the special case where indistinction really is a partition (crisp equivalence
classes), graphtropy collapses exactly to logical entropy.
     Why it matters. This justifies graphtropy as a conservative extension. We gain the ability to
represent graded/non-transitive indistinction without losing compatibility with classical partition-
based measures such as logical entropy [17].
     Connection to the rest of the document. Earlier we treated distinctions as policies (Sec-
tion 8); graphtropy is a canonical way to turn such a policy into a scalar measure of how “finely”
the observer is carving X under a distribution p. This scalar will later be useful when comparing
distinction regimes in the definition of effability and in discussions of resolution changes.
Proof. Two iid draws (X1 , X2 ) from p fall in the same block with probability i p2i , which equals
                                                                                     P
P
   x,y p(x)p(y) ιπ (x, y). Here ιπ (x, y) is the (0–1) indistinction indicator for the partition π, so the
right-hand side is simply the probability (under independent sampling) of the event “X1 and X2
land in the same block”: independence gives Pr[X1 = x, X2 = y] = p(x)p(y), and the indicator
ιπ (x, y) selects exactly those pairs (x, y) that are in a common block. Equivalently, one may write
         X                        XX X                      X X            X         X
             p(x)p(y) ιπ (x, y) =                p(x)p(y) =            p(x)        p(y) =       p2i ,
        x,y                      i   x∈Bi y∈Bi             i      x∈Bi       y∈Bi           i

which makes explicit how the pairwise sum “collapses” onto block masses. Taking 1− of both sides
yields the claim.

Remark 456. Proof sketch. Compute the same probability in two ways: (i) by summing block
masses squared, and (ii) by summing over pairs (x, y) with an indicator that they lie in the same
block. Since graphtropy is defined as 1− that pairwise indistinction probability, it matches logical
entropy.
    Key step. The identity x,y p(x)p(y) ιπ (x, y) = i p2i is simply the law of total probability
                               P                      P
applied to blocks: it groups the pairwise sum by which block both elements fall into. Another way

                                                   209
to say this is that the indicator ιπ is block-constant in the sense that it is 1 exactly on the union of
the Cartesian products Bi × Bi , and 0 off that union; summing against p(x)p(y) therefore sums the
total p ⊗ p-mass of those diagonal block rectangles.
    Visual intuition. Imagine drawing two balls from an urn labeled by blocks. The chance that
both draws land in the same block is the sum over blocks of (chance of landing in that block)2 . If one
instead thinks in terms of ordered pairs, the same probability is obtained by summing the probability
of each ordered pair (x, y) and then discarding (via ιπ ) all pairs that straddle two different blocks;
graphtropy/logical entropy is precisely the complement of this “pair-collision” event.
Proposition 13 (Monotonicity under loss of distinction). Let G and G0 be two indistinction graphs
on X with weights satisfying ιG (x, y) ≤ ιG0 (x, y) for all x, y. Then for every distribution p,

                                       GT(G, p) ≥ GT(G0 , p).

In particular, adding more indistinction edges (or strengthening indistinction weights) cannot in-
crease graphtropy.
Remark 457. What the proposition says. If an observer becomes less discriminating (treats
more pairs as indistinct, or treats them as more strongly indistinct), then the expected distinguisha-
bility cannot go up.
     Why it matters. This is the formal monotonicity property one expects from any sensible
“distinction content” measure. It lets us reason order-theoretically about resolution changes: coars-
ening is an order move, and graphtropy moves monotonically with it. This will be echoed later
when effability is shown to be monotone in the indistinction regime. Concretely, if G0 is obtained
from G by declaring additional pairs (x, y) to be indistinct (changing ιG (x, y) from 0 toward 1)
or by increasing their indistinction weight in a fuzzy model, then G0 represents a genuine loss of
discriminative power, and GT registers that loss by decreasing (or staying equal) for every p.
     Connection. Notice the parallel between this proposition and Proposition 14 below: both say
that making fewer demands on distinctions expands what is achievable/expressible. In both cases,
the underlying mechanism is order preservation: increasing indistinction enlarges the set of “identi-
fied” pairs, which increases the expected indistinction and thereby reduces the complement quantity
(graphtropy) that counts distinctions.
Proof. Immediate from
                    P the definition of GT(G, p) as 1− a weighted average of ιG . More explicitly,
if GT(G, p) = 1 − x,y p(x)p(y)ιG (x, y) (or the corresponding normalized variant used in the
surrounding text), then pointwise ιG ≤ ιG0 implies
                          X                        X
                             p(x)p(y)ιG (x, y) ≤     p(x)p(y)ιG0 (x, y),
                            x,y                         x,y

and subtracting from 1 reverses nothing (it is an order-preserving affine transformation), yielding
GT(G, p) ≥ GT(G0 , p).

Remark 458. Proof sketch. The quantity subtracted from 1 is an expectation of ιG (X1 , X2 ) under
independent sampling from p. If ιG ≤ ιG0 pointwise, then the expectation under G is no larger than
under G0 , hence 1− that expectation is no smaller. Said differently, GT(G, p) is the expectation of
the complementary “distinction indicator” 1 − ιG (X1 , X2 ), and if ιG increases pointwise then 1 − ιG
decreases pointwise, so its expectation cannot increase.
    Geometric intuition. Think of ιG as a “blur kernel” over X × X. Increasing blur reduces
contrast; graphtropy measures contrast, so it decreases. In the crisp (0–1) case, adding indistinction

                                                  210
edges literally increases the region in X × X on which the kernel equals 1, so the p ⊗ p-mass of
indistinct pairs grows and the complementary mass of distinct pairs shrinks.

Theorem 10 (Shannon entropy lower-bounds quadratic/logical distinguishability). Let p be a
distribution on a finite set X and define
                                      X
                            S2 (p) :=    p(x)2 , H2 (p) := − log S2 (p).
                                           x∈X

Then
                                       H(p) ≥ H2 (p) = − log S2 (p).
If π is a partition of X and pi are the block masses, then
                                X                     X
                      H(π) := −     pi log pi ≥ − log   p2i = − log(1 − h(π, p)).
                                   i                            i

Remark 459. What the theorem says (plainly). Shannon entropy is always at P                    least the
order-2 Rényi entropy H2 (sometimes called “collision entropy” because it depends on             p(x)2 ,
the collision probability). So if an observer’s belief distribution is highly uncertain in the Shannon
(coding) sense, then it is also uncertain in this quadratic (pairwise-collision) sense.
    Why this is important here. Logical entropy and graphtropy are built from quadratic pairwise
expressions. This theorem links the coding-theoretic world (Shannon) to the distinction/pairwise
world (logical entropy/graphtropy). It is, in effect, a compatibility guarantee: the different notions
of “uncertainty” discussed in this section are not unrelated numbers but are constrained by in-
equalities. In particular, whenever one uses S2 (p) (or its complement 1 − S2 (p)) as a proxy for
uncertainty/heterogeneity, the theorem bounds how far that proxy can drift from Shannon’s coding
interpretation.
    Connection to earlier/later material. Earlier we motivated information as observer-
indexed; this theorem remains valid under that indexing, because it is a statement about any finite
distribution pO the observer might hold. Later, in pattern and habit sections, we will move between
coding-like and distinction-like quantities; having such monotone bridges makes those translations
principled rather than merely metaphorical. One can also view this as a special case of a more
general monotonicity phenomenon for Rényi entropies: as the order α increases, Hα decreases, so
H = H1 sits above H2 ; the present proof gives a direct inequality tailored to the quadratic quantity
that appears in graphtropy.

Proof. Define r(x) := p(x)2 /S2 (p), which is a probability distribution on X. Nonnegativity of KL
divergence gives
                                                   X           p(x)
                                 0 ≤ DKL (pkr) =      p(x) log      .
                                                    x
                                                               r(x)

Substituting r(x) = p(x)2 /S2 (p) yields
                                   X                      p(x)        X          S2 (p)
                     DKL (pkr) =           p(x) log        2
                                                                    =   p(x) log        .
                                       x
                                                       p(x) /S2 (p)   x
                                                                                 p(x)

Hence                                        X
                        0 ≤ log S2 (p) −             p(x) log p(x) = log S2 (p) + H(p),
                                                 x



                                                          211
which rearranges to H(p) ≥ − log S2 (p) = H2 (p). The partition statement follows by applying the
same argument to the block distribution (pi ). Note that no special cases are needed for p(x) = 0 (or
pi = 0): the conventional interpretation 0 log 0 := 0 makes all displayed sums well-defined, and KL
divergence remains nonnegative as long as r(x) > 0 whenever p(x) > 0, which holds here because
r(x) ∝ p(x)2 .

Remark 460. Proof sketch. Construct an auxiliary distribution r proportional       to p2 , P
                                                                                           then apply
                                                                         p log p and log p2 .
                                                                       P
the universal inequality DKL (pkr) ≥ 0 to derive an inequality between
    Key step. The choice r(x) ∝ p(x)2 is not arbitrary: it is exactly the distribution that
turns log S2 (p) into a normalization constant inside the KL divergence. Once that substitution
is made, the inequality becomes algebraic. One can also read the algebra as comparing the aver-
age of − log p(x) under p (which is H(p)) to the log of an L2 -type quantity S2 (p); the KL step
is what guarantees the comparison has the correct direction for all p (not just for nearly uniform
distributions).
    Visual intuition. Shannon entropy is sensitive to the entire distribution shape, while S2 (p)
is dominated by larger probabilities (since it squares them). The inequality H ≥ H2 expresses that
if a distribution is “peaky,” its S2 becomes large (so H2 becomes small), and Shannon entropy
cannot bePlarger 2than that quadratic constraint allows. In the common “collision” interpretation,
S2 (p) = x p(x) is the probability that two independent draws from p coincide; thus H2 = − log S2
measures how difficult it is (in bits) to force a collision. Under this reading, H ≥ H2 says that
the coding-theoretic uncertainty H cannot undercut the collision-based notion of spread captured by
H2 , and it becomes tight (up to support effects) when the distribution is close to uniform over its
effective support.

Remark 461 (Hyperseed reading). The theorem says: if an observer’s distribution is spread out
enough to have large Shannon entropy, then it must also have a large “quadratic spread,” hence a
large logical entropy/graphtropy. In other words, uncertainty in the coding sense lower-bounds the
expected rate at which distinctions are encountered. Equivalently, when the observer is forced (by
high Shannon uncertainty) to distribute probability mass broadly, the probability that two indepen-
dent samples fall into the same indistinction class drops, so the complement quantity (logical entropy
/ graphtropy) rises. This is one way to connect the “uncertainty” modality (coding/inference spread)
to the “distinction” modality (how often the observer can separate states): the former constrains
the latter because concentrated mass simultaneously increases collision probability and reduces the
expected number of effective distinctions available to the observer.

10.6    Uncertainty and ineffability as observer-relative modalities
Hyperseed uses “ineffable” in a practical sense: something may exist and matter to a mind, yet
remain resistant to being stably and communicably represented. We formalize this by combining
(i) a cost model for representations and (ii) a fidelity predicate that depends on the observer’s
distinctions. The key point is that both ingredients are explicitly indexed by the observer/context
O, so “ineffability” is not an absolute metaphysical label but a relative statement about what can
be encoded given a representational interface and a limited budget.

Definition 126 (Observer representational resources). An observer/context O is equipped with:

• a description space (language) DO ;

• a cost/effort function σO : DO → [0, ∞);


                                                 212
• a decoding map decO : DO → ∆(X), where ∆(X) is the set of probability distributions on X.

Given d ∈ DO , the distribution decO (d) is interpreted as the observer’s best reconstruction of the
target in X from description d.

Remark 462. Notation/conventions. DO is a set of descriptions (strings, programs, structured
messages, etc.). σO (d) is the effort/cost of using description d; it plays the same formal role as
description length or resource use, but we do not insist it be literal bit-length. ∆(X) denotes the
simplex of probability distributions on X.
    Intuition. A description d is not required to point to a single x ∈ X; instead it may decode to
a distribution, reflecting that a finite description can determine only a region of possibilities. This
is a deliberately observer-friendly model: what the observer can say need not uniquely identify what
the world is.
    Example. If X is a set of images and DO is a natural-language vocabulary, then decO (d) is
the distribution over images compatible with the phrase d (e.g. “a red apple on a table”). If X is
microstates and DO is macroscopic parameters, then decO (d) is a macrocanonical distribution over
microstates.
    Why useful. This definition provides the scaffold needed to define effability/ineffability as a
resource-bounded property, aligning with Hyperseed’s emphasis that what can be expressed depends
on effort and available representational moves (Hyperseed-Concept 100, Hyperseed-Concept ??).
    Further clarification. The map decO can be read in several compatible ways: (a) as a con-
ventional semantics map (a description denotes a set/region of states, represented here by a distri-
bution), (b) as Bayesian posterior inference given a message d, or (c) as a lossy decompressor in a
coding system. Allowing decO (d) to be a distribution rather than a point makes room for ambigu-
ity, underspecification, and context-dependence, which are precisely the regimes where ineffability is
most natural to discuss. Similarly, the cost σO may measure time, energy, cognitive effort, social
negotiation cost, or any other constrained resource, so that “saying more precisely” is not free.

Definition 127 (Fidelity relative to a distinction structure). Fix an indistinction weight function
ιG on X. Given a target x ∈ X and a reconstructed distribution q ∈ ∆(X), define the distinction
error                                        X
                              ErrG (x, q) :=     q(y) (1 − ιG (x, y)).
                                                y∈X

Define the corresponding distinction fidelity
                                                             X
                          FidG (x, q) := 1 − ErrG (x, q) =         q(y) ιG (x, y).
                                                             y∈X

Remark 463. Intuition. FidG (x, q) is the expected indistinction between the true target x and
a random draw y ∼ q. So fidelity is high when q puts most of its mass on states y that the
observer would treat as indistinct from x. This makes fidelity explicitly dependent on the observer’s
distinction policy.
    Example. If ιG is induced by a partition into categories (say, “cat” vs. “dog”), then fidelity
measures whether your reconstruction distribution stays within the correct category. A description
might be “good enough” even if it cannot identify the exact microstate, as long as it lands in the
right coarse class.
    Why useful. This is the technical move that makes ineffability meaningful rather than mys-
tical: we can say precisely which aspects of x the observer fails to capture, because the failure is

                                                  213
measured by the observer’s own indistinction structure. It also anticipates the later use of graded
relations/quantales to represent cognition (Sections 11 and 12).
     Basic properties. When ιG (x, y) ∈ [0, 1] for all x, y, one has ErrG (x, q) ∈ [0, 1] and FidG (x, q) ∈
[0, 1]. Moreover, FidG (x, q) is linear in q, so mixing reconstructions mixes fidelities in the obvious
way. At the extremes: if ιG (x, y) = 1x=y (perfect distinction of microstates), then FidG (x, q) = q(x)
is just the probability that q hits the correct state exactly; if ιG (x, y) ≡ 1 (no distinctions at all),
then FidG (x, q) ≡ 1 and everything is trivially “perfectly faithful” in this coarse sense.

Remark 464. If ιG encodes a partition, then FidG (x, q) is exactly the probability mass that q
assigns to the block of x. Thus FidG measures whether the reconstruction lands in the “right
distinction class.” For fuzzy ιG , it becomes a graded correctness criterion. In particular, when
ιG is derived from a weighted graph (or similarity kernel), FidG (x, q) can be read as the expected
similarity between x and a q-sample, so the same formalism covers both crisp categorization and
graded perceptual similarity.

Definition 128 ((, K)-effability and ineffability). Fix thresholds  ∈ (0, 1) and K ∈ (0, ∞). An
element x ∈ X is (, K)-effable for O (relative to G) if there exists a description d ∈ DO such that
                                                                
                          σO (d) ≤ K and FidG x, decO (d) ≥ 1 − .

Otherwise x is (, K)-ineffable for O (relative to G). We write Eff O (, K; G) ⊆ X and Ineff O (, K; G) :=
X \ Eff O (, K; G).

Remark 465. Intuition. Effability is a two-threshold notion:

• K limits how much representational effort the observer may spend;

•  limits how much distinction error the observer is willing to tolerate.

An item is ineffable if every description cheap enough fails the fidelity test.
   Examples. A detailed inner sensation might be ineffable for an observer with a coarse language
(small DO ) or small budget K. A high-dimensional physical state may be ineffable relative to a
coarse distinction structure G if the observer demands fine fidelity (tiny ) but lacks resources.
    Monotonicity and limiting cases. Holding O and G fixed, Eff O (, K; G) is monotone in-
creasing in both parameters: if K 0 ≥ K, then any description feasible under K is feasible under K 0 ,
and if 0 ≥ , then any reconstruction meeting the stricter fidelity target 1 −  also meets the weaker
target 1 − 0 . Thus ineffability is most stringent at small K and small , matching the informal idea
that “hard to say” can mean either “too expensive to say precisely” or “no available description hits
the demanded granularity.” At the opposite extreme, if DO contains arbitrarily long descriptions
and decO can represent point masses δx (perfectly specific reconstructions), then every x becomes
(, K)-effable for sufficiently large K and sufficiently small ; the interesting regime is where either
the language cannot express such pinpoint reconstructions or the budget K forbids them.
    Relation to lossy coding. Formally, the condition FidG (x, decO (d)) ≥ 1 −  parallels a
distortion constraint in rate–distortion theory, with (1−ιG ) acting as an observer-relative distortion
measure. The novelty here is that distortion is not imposed externally but induced by the observer’s
distinction structure, so “what counts as an acceptable lossy description” is itself observer-relative.


Remark 466. Why this is useful. This definition separates three sources of “ineffability” that
are often conflated: (i) lack of resources (small K), (ii) lack of expressive language (restricted DO

                                                  214
and decO ), and (iii) demanding too fine a notion of correctness (too discriminating an ιG or too
small ). In Hyperseed terms, it makes ineffability a modality indexed by effort and distinction
regime, rather than an absolute metaphysical boundary (Hyperseed-Concept ??). Equivalently, the
question “is x ineffable?” is replaced by the operational question “for which budgets K, tolerances ,
and regimes G does x fall outside the reachable set of reconstructions?”. This shift matters because
it lets one diagnose which knob (capacity, vocabulary/decoding, or resolution) is responsible for the
failure, rather than treating all failures as the same phenomenon. It also clarifies that “ineffability”
can arise even in a fully deterministic world: it is about limits of mediation and evaluation, not
about indeterminacy in the target.
Proposition 14 (Monotonicity in resources and resolution). If K 0 ≥ K then Eff O (, K; G) ⊆
Eff O (, K 0 ; G). If G0 is coarser than G in the sense that ιG (x, y) ≤ ιG0 (x, y) for all x, y (more
indistinction), then
                                      Eff O (, K; G) ⊆ Eff O (, K; G0 ).
Remark 467. What the proposition says. Two monotonicities hold:
• More resource budget (K 0 ≥ K) cannot make previously sayable things unsayable.
• Coarser resolution (more indistinction) cannot make previously acceptable reconstructions unac-
  ceptable.
Here “resource budget” is whatever complexity/cost measure is encoded in the definition of Eff O (, K; G)
(e.g., description length, time, energy, sample size, or any composite bound), so the first mono-
tonicity is a statement about feasibility under constraint relaxation. Likewise, “coarser” is not an
informal metaphor but the pointwise order ιG ≤ ιG0 , which guarantees that every pair (x, y) is
judged at least as “similar” (or at least as “indistinct”) in G0 as it was in G.
    Why it matters. This is the minimal sanity condition for an effability notion: adding capac-
ity should not reduce what you can express, and relaxing your standards of distinction should not
reduce what you can count as successfully expressed. It also gives a clean formal handle on devel-
opmental/cultural claims: as a community gains representational resources or shifts its distinction
regime, the boundary between effable and ineffable moves monotonically. In particular, if one thinks
of  as a tolerance parameter for “good enough” reconstruction, then this proposition isolates two
other monotone directions (in K and in G) that move the boundary without changing . This is
useful when comparing observers: two agents can agree on  but still differ radically in effability
because they differ in budget K or in the similarity structure ιG they implicitly apply.
    Connection. Compare with Proposition 13: graphtropy decreases under coarsening, while ef-
fability increases under coarsening. Together they express a trade: fewer distinctions encountered
means more targets count as representable. One can read this as a duality between (i) the “com-
plexity of the world as cut” (how many distinctions are treated as real) and (ii) the “complexity of a
message needed to succeed” (how hard it is to meet the fidelity test). When G is made coarser, the
observer is, in effect, permitted to ignore more microstructure, so many different underlying states
can share a single acceptable description.
Proof. The first inclusion is immediate: any description of cost at most K is also of cost at most K 0 .
Concretely, if d ∈ DO is feasible under K (i.e., it belongs to the allowed-cost subset of descriptions),
then it remains feasible under any larger bound K 0 , and the corresponding decoded reconstruction
decO (d) does not change; only the admissible set of d expands. For the second, if ιG ≤ ιG0 then for
any q ∈ ∆(X) we have
                                  X                    X
                   FidG0 (x, q) =    q(y) ιG0 (x, y) ≥    q(y) ιG (x, y) = FidG (x, q).
                                  y                     y


                                                  215
A coarser G0 makes the fidelity test easier to satisfy, so the effable set can only expand. Equivalently,
for each fixed x and each candidate reconstruction q, the set of regimes under which q is -acceptable
is upward closed in the pointwise order on ι; taking an existential quantifier over descriptions
preserves this monotonicity.

Remark 468. Proof sketch. The first part is pure set inclusion under a relaxed constraint:
enlarging the allowed-cost set enlarges the feasible descriptions. The second part is an inequality
under a pointwise domination ιG ≤ ιG0 , which transfers directly through the expectation defining
fidelity. What is doing the work is that FidG (x, q) depends on G only through ιG (x, ·), so comparing
regimes reduces to comparing two functions pointwise and then averaging.
    Key step. Fidelity is linear in ιG (it is an average of ιG (x, y) under q), so pointwise ordering
of ι implies ordering of fidelities. In particular, no additional regularity assumptions (convexity,
continuity, etc.) are needed: the argument is purely order-theoretic.
    Intuition. If you blur your distinctions, you become easier to satisfy: many reconstructions
that were previously “wrong in the details” become “close enough” in the new regime. Conversely,
sharpening distinctions (moving from G0 to a finer G) can render previously adequate summaries
inadequate, not because the agent “lost” expressive power, but because the scoring rule became
stricter.

Remark 469 (Ineffability versus unknowability). Ineffability is not the same as (absolute) un-
knowability. Even if x is ineffable to O at some (, K), it may become effable after: (i) increasing
resources (larger K); (ii) changing the representational language DO ; or (iii) changing the distinc-
tion regime (a different G). Hyperseed’s point is that such changes are common in development
and culture: a concept can become sayable once a community learns to carve the world differently.
Said differently, ineffability here is indexed by an interface: a particular coding/decoding practice
together with a particular way of scoring similarity. Under that interpretation, an “ineffable” x is
often better described as “not currently compressible into the observer’s available description forms
without exceeding the tolerated error”. This also prevents a common equivocation: a fact may be
perfectly learnable in principle (there exists some richer observer O0 or some larger K for which it
is effable) while being practically unsayable for a given agent in a given context.

Remark 470. In Peircean terms, ineffability is not a statement about the absence of a Third
(law/representation), but about the current poverty of mediating habits available to the agent or
community. In Whiteheadian terms, it is a limitation in the available forms of “prehension” and
their integration, not a denial that the occasion exists (cf. [14, 15] for the broader metaphysical
framing). The present formalism simply makes those philosophical diagnoses testable against pa-
rameters: one can ask whether the obstacle is primarily one of habit/mediation (modeled by DO
and decO ), one of effort (modeled by K), or one of discriminatory stance (modeled by G and ).
On that reading, a “new concept” in a community can be seen as simultaneously (a) an expansion
of DO (new symbols, new grammars, new practices of description) and (b) a reconfiguration of ιG
(new similarities taken as salient), either of which can move items from the ineffable to the effable
region without changing the underlying target space.

10.7    Potential infinity and infinitesimals as “limit objects”
Hyperseed frequently speaks about “potentially infinite” or “potentially infinitesimal” quantities.
Rather than invoke full nonstandard analysis, it is often enough to work with a constructive surro-
gate: germs of sequences at infinity. In this subsection, “limit object” should be read in an informal
operational sense: we take a potentially unbounded or potentially refining process (a sequence),

                                                  216
and then identify processes that differ only by a finite amount of “startup behavior.” What remains
is a stable tail-pattern that functions like an idealized object for asymptotic reasoning.

Definition 129 (Eventual equality and germs). Let RN be the set of real sequences. Define an
equivalence relation ∼ on RN by

                               a∼b       ⇐⇒     ∃N ∈ N ∀n ≥ N : an = bn .

The quotient
                                               R∞ := RN / ∼
is called the set of germs at infinity. We write [a] for the germ of the sequence a. Addition and
multiplication are defined pointwise on representatives.

Remark 471. Well-definedness and algebra. Because ∼ is compatible with pointwise addition
and multiplication (if two pairs of sequences agree eventually, then so do their pointwise sums and
products), the operations “defined pointwise on representatives” do not depend on which represen-
tative of a germ one chooses. Thus R∞ is naturally a commutative ring. It is not a field in general:
a germ can fail to have a multiplicative inverse, e.g. if a representative has infinitely many zero
terms (so that no pointwise reciprocal sequence exists beyond any finite stage).
    Embedding of standard reals. There is a canonical map R ,→ R∞ sending a real number c
to the germ of the constant sequence (c, c, c, . . . ). This makes it precise to compare a germ to an
ordinary real “benchmark” without leaving the germ language. In what follows, inequalities such as
ε <∞ c implicitly use this embedding.
    Notation/conventions. RN is the set of sequences (a0 , a1 , a2 , . . . ) with real entries. The
relation a ∼ b means “a and b are eventually the same,” i.e. they may differ at finitely many initial
indices but coincide from some point onward. [a] denotes the equivalence class (germ) of a.
    Intuition. A germ forgets finite beginnings and remembers only tail behavior. This captures the
idea of “potential” processes: what matters is not having an actually completed infinity, but having
a rule whose behavior stabilizes beyond any finite horizon. Equivalently, a germ is a bookkeeping
device for statements of the form “for all sufficiently large n,” which will recur whenever one reasons
about limits, asymptotics, or tolerances.
    Examples. The sequences (0, 1, 2, 3, . . . ) and (5, 1, 2, 3, . . . ) define the same germ: they differ
only at the first entry. The sequences (1, 1, 1, . . . ) and (1, 1, 1, 0, 1, 1, . . . ) do not define the same
germ if they differ infinitely often. Similarly, the sequences (n) and (n+1000) define the same germ
difference as a constant shift: [n + 1000] = [n] + [1000], so the “potential infinity” is insensitive to
finite offsets in starting point.
    Why this is useful. Resource-sensitive ontology often wants to say “can be made arbitrarily
large” or “arbitrarily small” without committing to completed infinities. Germs provide a minimal
algebraic language for such talk, compatible with an operational view of approximation. They also
separate two kinds of information that often get conflated: the finite transient behavior of a process
(which can be idiosyncratic or context-specific) and its eventual regime (which is what asymptotic
comparison and “limit” talk typically tracks).

Definition 130 (Eventual order). For germs [a], [b] ∈ R∞ define

                            [a] ≤∞ [b]    ⇐⇒      ∃N ∈ N ∀n ≥ N : an ≤ bn .

This is a partial order compatible with addition and multiplication by nonnegative germs.


                                                     217
Remark 472. Basic properties. The relation ≤∞ is reflexive and transitive, and it is anti-
symmetric in the sense appropriate for a quotient: if [a] ≤∞ [b] and [b] ≤∞ [a], then an = bn
eventually, hence [a] = [b]. It is generally not a total order: there may be incomparable germs
whose representatives cross infinitely often.
     Intuition. [a] ≤∞ [b] means: after some finite stage, an never exceeds bn . So the order
compares asymptotic tail behavior and ignores finitely many initial anomalies. This is exactly the
quantifier pattern used in many “limit” arguments: the tail is constrained uniformly beyond some
cutoff.
     Example. If an = n and bn = n2 , then [a] ≤∞ [b] since eventually n ≤ n2 . But [a] ≤∞ [c]
and [c] ≤∞ [a] can both fail if the sequences oscillate forever. For instance, if cn = (−1)n n, then
neither [c] ≤∞ [0] nor [0] ≤∞ [c] holds: the sign keeps flipping, so no single tail bound of one by
the other stabilizes.
     Why useful. The eventual order lets us define “infinitely large” and “infinitesimal” ele-
ments as order-theoretic comparisons with constants, matching Hyperseed’s use of potential in-
finity/infinitesimals (Hyperseed-Concept ??, Hyperseed-Concept ??). Concretely, a germ x is “(po-
tentially) infinite” if it eventually exceeds every constant, and it is “(potentially) infinitesimal” if
it is eventually positive yet eventually below every fixed positive constant.
Example 10 (A potentially infinite and a potentially infinitesimal element). Let ω := [n] where
n 7→ n. Then ω dominates every standard constant: for any c ∈ R, eventually n > c. Let ε := [1/n].
Then ε is positive but smaller than any fixed positive constant in the eventual order.
Remark 473. This example is the operational core: ω stands for an unbounded growth process,
while ε stands for a decay process that can be made smaller than any fixed tolerance by going far
enough along the sequence. Neither requires a completed infinite magnitude; both require only the
ability to continue the process as needed. In particular, the germ formalism explicitly tolerates the
fact that real computations have “initial conditions”: changing finitely many initial values of n or
1/n does not change the potential object.
    A useful consistency check is that these two limit objects interact as expected under multiplica-
tion:
                              ω · ε = [n] · [1/n] = [ n · (1/n) ] = [1],
since n · (1/n) = 1 for all n ≥ 1, i.e. the product is eventually the constant 1. This illustrates how
the germ quotient encodes the idea that “after a finite warm-up,” scaling up and scaling down can
cancel in a stable way.
Lemma 2 (Infinitesimal property in the germ order). Let ε = [1/n] ∈ R∞ . Then 0 <∞ ε and for
every standard c > 0 we have ε <∞ c.
Remark 474. What the lemma says. The germ of 1/n behaves exactly as one informally
expects of an infinitesimal: it is eventually positive, yet eventually smaller than any fixed positive
real constant.
    Relation to “limit” language. In ordinary analysis one writes limn→∞ 1/n = 0. Here,
instead of collapsing 1/n to the value 0, we keep the whole tail-behavior as an object ε that remains
distinguishable from 0 but is dominated by every positive constant. This is precisely the kind of
“nonzero but negligible” quantity that potential-infinitesimal talk is aiming at.
    Why it matters. This provides a precise, lightweight sense in which we can talk about “arbi-
trarily weak couplings” or “arbitrarily small errors” inside a framework that treats infinity as po-
tential rather than completed. Such language is later useful when describing diminishing influences

                                                  218
across increasingly remote contexts (e.g. in resonance-style stories), where one wants “nonzero but
negligible” rather than exactly zero. In particular, the lemma justifies replacing a family of toler-
ance statements “for every c > 0 there exists a stage after which the error is < c” with a single
order-theoretic comparison against all constants.

Proof. For n ≥ 1, 1/n > 0, so ε >∞ 0. Given c > 0, choose N > 1/c. Then for all n ≥ N , 1/n < c,
so ε <∞ c.

Remark 475. Proof sketch. Both claims follow by choosing a sufficiently large index N . Posi-
tivity is immediate because all terms 1/n are positive; smallness follows because 1/n eventually falls
below any fixed threshold c.
    Key step. The eventual order bakes “there exists an N such that for all n ≥ N ” into the
definition, so asymptotic estimates translate directly into order relations. This is the same quantifier
structure that appears in ε–δ reasoning; germs package it into algebraic objects so that one can
reason about tails without constantly reintroducing quantifiers.
    Visual intuition. Plot 1/n against n; the curve descends toward 0. The lemma is simply the
statement that any horizontal line at height c > 0 is eventually above the curve.
    Interpretive note. Although ε is “smaller than any fixed constant,” it is not equal to 0 in
R∞ : the sequence 1/n is never eventually the zero sequence. This distinction is exactly what makes
ε a useful “limit object” rather than merely a limit value.

Remark 476 (Conceptual role). Germs provide a lightweight way to talk about “approaching infin-
ity” or “approaching zero” without assuming that a mind must represent completed infinite objects.
In this sense, a germ functions as a stable direction of refinement: it records what remains invariant
as one continues to sharpen a description (for example, by increasing resolution, adding measure-
ment time, or enlarging a comparison class), while refusing to reify the unattainable endpoint as
a finished entity. This is the intended “limit object” reading: not an actually-given limit, but a
disciplined placeholder for an indefinitely extensible process of approximation.
    In the ontology, this supports statements like: “the distinction granularity can be refined without
bound” (potential infinity) and “a coupling can be arbitrarily weak” (potential infinitesimal). Here
“without bound” should be read as a modal claim about available refinements (there is always a
further distinction regime available in principle), rather than as a claim that an infinite set of
distinctions is ever simultaneously present to an observer. Likewise, “arbitrarily weak” emphasizes
a comparative ordering of couplings under refinement: for any operational threshold fixed by an
observer, one can consider contexts in which the coupling falls below that threshold, even if no
absolute “zero-coupling” state is ever asserted.
    When we later discuss morphic resonance across increasingly remote contexts, it can be useful
to treat resonance strength as an infinitesimal germ rather than as exactly zero. This avoids a sharp
discontinuity between “no influence” and “some influence” that would otherwise be an artifact of
representational coarseness: the germ formalizes the idea that influence may persist in a way that is
systematically negligible for any fixed finite resource bound, yet not logically excluded. Equivalently,
the infinitesimal germ lets us separate two questions that are often conflated: whether a coupling
is detectable at a given resource level, and whether it is structurally present in the relational
organization being modeled.

10.8    Section wrap-up
This section supplied three bridges that will be used repeatedly later:


                                                  219
• Shannon information provides the standard coding-theoretic notion of uncertainty. In particular,
  it supplies a quantitative baseline for how many bits are required, on average, to resolve a choice
  among alternatives given an assumed probability model, and it supports the usual trade-offs
  between compression, prediction, and error.

• Logical entropy and graphtropy connect uncertainty to the Hyperseed primitive of distinction.
  This makes uncertainty explicitly about separations (which pairs are distinguished and which
  are not), so that information measures can be read directly as properties of a distinction graph
  or partition structure, rather than only as properties of symbol sequences.

• Ineffability becomes a monotone property relative to observer resources and distinction regimes.
  That is, an object or pattern may be perfectly effable for one observer (or one modeling interface)
  while remaining ineffable for another, and increasing resources or refining distinctions can only
  decrease ineffability in the sense that more becomes stably nameable and communicable.

With these in place, we can treat hierarchy and pattern webs (Section 11) and habit dynamics
(Section 12) as information-processing structures whose meaning depends explicitly on what is, and
is not, distinguished. This dependence is not merely epistemic but structural: changing a distinction
regime can change what counts as an entity, a relation, or a causal regularity in the model, thereby
shifting which compressions are valid and which predictions are well-posed. Conversely, by keeping
the distinction regime explicit, later sections can state claims about organization and dynamics in
a way that remains robust under changes of scale, granularity, or observational interface.


11     Hierarchy, heterarchy, and pattern webs
11.1    Motivation: why Hyperseed needs both hierarchies and webs
Patterns (Section 9) do not occur in isolation. Once an observer can represent “P is a pattern in
x” with some intensity, it can also represent relationships between patterns and between patterned
entities. This is not an optional embellishment: as soon as patterns are treated as reusable cognitive
objects, the observer must be able to compare them, compose them, and propagate information
from one to another. In particular, even a minimal pattern-recognizer tends to (a) reuse the same
patterns across many inputs and (b) relate those reused patterns via co-occurrence, entailment,
explanation, control, abstraction, and part–whole decomposition. Two structural motifs appear
immediately:

• Hierarchy: some entities are treated as “higher” than others (more valuable, more general, more
  controlling, more explanatory) and this induces an order-like structure.

• Heterarchy (web): most entities have multiple different paths of relationship to other entities,
  forming loops and multi-path dependence networks rather than trees.

The emphasis on “order-like” versus “network-like” is deliberate: in practice, the same pair of
patterns may be related in multiple ways at once (e.g. one pattern may be more general, while the
other is more predictive in a restricted domain), and the cognitive model must be able to represent
both the comparative directionality (who outranks whom, or who constrains whom) and the lateral
connectivity (who interacts with whom, possibly reciprocally). In this section, the word “hierarchy”
will be used broadly enough to include not only strict trees but also preorders and partial orders,
i.e. structures where many elements may be incomparable, and where “being higher” can mean
“being at least as good as” rather than “being the unique parent of.”

                                                 220