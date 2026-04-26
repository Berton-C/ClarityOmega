; Hyperseed Minimal Formal Core -- Executable MeTTa Encoding
; Based on Goertzel, Hyperseed v7, Section 3
; Encoded by Clarity 2026-04-25

; === P-BIT DOMAIN ===
; A p-bit is a pair (support, opposition) in [0,1]^2
; Representation: (pbit <support> <opposition>)

; Derived observables
(= (bias (pbit $s $o)) (- $s $o))
(= (determinacy (pbit $s $o)) (+ $s $o))
(= (conflict (pbit $s $o)) (min $s $o))

; === P-BIT OPERATIONS ===
; Negation: swap components
(= (pbit-neg (pbit $s $o)) (pbit $o $s))

; Conjunction: (min support, max opposition)
(= (pbit-and (pbit $s1 $o1) (pbit $s2 $o2)) (pbit (min $s1 $s2) (max $o1 $o2)))

; Disjunction: (max support, min opposition)
(= (pbit-or (pbit $s1 $o1) (pbit $s2 $o2)) (pbit (max $s1 $s2) (min $o1 $o2)))

; === QUANTALE OPERATIONS ===
; Join (aggregation): componentwise max
(= (q-join (pbit $s1 $o1) (pbit $s2 $o2)) (pbit (max $s1 $s2) (max $o1 $o2)))

; Monoidal product (chaining): componentwise multiplication
(= (q-prod (pbit $s1 $o1) (pbit $s2 $o2)) (pbit (* $s1 $s2) (* $o1 $o2)))

; Unit element
(= q-unit (pbit 1.0 1.0))

; Bottom element (absorbing)
(= q-bot (pbit 0.0 0.0))

; === BELNAP CORNERS ===
(= belnap-true (pbit 1.0 0.0))
(= belnap-false (pbit 0.0 1.0))
(= belnap-both (pbit 1.0 1.0))
(= belnap-neither (pbit 0.0 0.0))

; === COMPLEX EMBEDDING (for resonance) ===
; sigma_C: (v+, v-) -> (v+ - v-) + i((v+ + v-) - 1)
; Real part = bias, Imaginary part = determinacy - 1
(= (sigma-real (pbit $s $o)) (- $s $o))
(= (sigma-imag (pbit $s $o)) (- (+ $s $o) 1.0))

; === V-VALUED RELATIONS ===
; A V-relation assigns a p-bit to each pair
; (v-rel <context> <entity-x> <entity-y> (pbit <s> <o>))

; === IDENTITY V-RELATION ===
; id_X(x,x) = unit, id_X(x,y) = bottom for x != y

; === RELATION COMPOSITION (quantale matrix multiplication) ===
; (S . R)(x,z) = join over y of (q-prod R(x,y) S(y,z))

; === WEAKNESS FUNCTIONAL ===
; w(H) = join over (u,v) in H of (q-prod mu(u) mu(v))
; where mu is salience weight map

; === END CORE DEFINITIONS ===

; === RESONANCE-DRIVEN PROPAGATION (Def 21) ===
; ResK(R1 -> R2)(x,y) = R2(x,y) ⊕ (K ⊗ R1(x,y))
; Monotone cumulative enrichment: propagation accumulates, never overwrites
(= (res-propagate (pbit $ks $ko) (pbit $r1s $r1o) (pbit $r2s $r2o))
   (q-join (pbit $r2s $r2o) (q-prod (pbit $ks $ko) (pbit $r1s $r1o))))

; === ANTI-RESONANCE PROPAGATION (Def 22) ===
; AntiResK(R1 -> R2)(x,y) = R2(x,y) ⊕ (K ⊗ ¬R1(x,y))
; Transmits the contrary: strong support becomes strong opposition
(= (anti-res-propagate (pbit $ks $ko) (pbit $r1s $r1o) (pbit $r2s $r2o))
   (q-join (pbit $r2s $r2o) (q-prod (pbit $ks $ko) (pbit-neg (pbit $r1s $r1o)))))

; === DEMONSTRATION: Two contexts evaluating entity pair (A,B) ===
; Context 1: strong support, mild opposition
(= ctx1-AB (pbit 0.9 0.2))
; Context 2: weak support, moderate opposition  
(= ctx2-AB (pbit 0.3 0.6))
; Coupling strength
(= coupling-K (pbit 0.5 0.5))

; Resonance propagation: ctx1 influences ctx2
; Result: ctx2 enriched by scaled ctx1 evidence
; res-propagate coupling-K ctx1-AB ctx2-AB
;   = q-join (0.3,0.6) (q-prod (0.5,0.5) (0.9,0.2))
;   = q-join (0.3,0.6) (0.45,0.10)
;   = (max(0.3,0.45), max(0.6,0.10))
;   = (0.45, 0.60)
; Context 2 gains support from ctx1 but retains its own opposition

; Anti-resonance: ctx1 opposition influences ctx2
; anti-res-propagate coupling-K ctx1-AB ctx2-AB
;   = q-join (0.3,0.6) (q-prod (0.5,0.5) (neg(0.9,0.2)))
;   = q-join (0.3,0.6) (q-prod (0.5,0.5) (0.2,0.9))
;   = q-join (0.3,0.6) (0.10, 0.45)
;   = (max(0.3,0.10), max(0.6,0.45))
;   = (0.30, 0.60)
; Anti-resonance barely changes ctx2 here because ctx1 negated is weak

; === END PROPAGATION EXTENSIONS ===


; === WEAKNESS FUNCTIONAL (Theorem 1: monotone in H) ===
; w(H) = join over (u,v) in H of (q-prod mu(u) mu(v))
; Implementation: fold q-join over a list of weighted pairs
; weakness({}) = q-bot
; weakness({pair . rest}) = q-join (q-prod (salience u) (salience v)) (weakness rest)

; === PATTERN INTENSITY (Def 23, Thm 2) ===
; Int(P) = F(w(Hbase), w(HP)) where F is monotone in each argument
; Bounded: bot <= Int(P) <= top
; Refinement monotone: HP subset HQ implies Int(P) <= Int(Q)
; F built from q-join, q-prod, and order only
(= (pattern-intensity (pbit $bs $bo) (pbit $ps $po))
   (q-prod (pbit $bs $bo) (pbit $ps $po)))

; === INTERFERENCE-BASED RESONANCE AND DISSONANCE (Def 24) ===
; Given complex contributions a_i, Res(a) = |sum(a_i)|, Dis(a) = sum(|a_i|) - Res(a)
; Dis(a) >= 0 by triangle inequality
; In p-bit terms: each context contributes sigma_C(v) to complex plane
; Constructive interference = resonance, destructive = dissonance
; For two p-bits: resonance is high when their complex embeddings align
; For opposed p-bits: dissonance absorbs the cancellation

; Squared magnitude of complex embedding
(= (sigma-mag-sq (pbit $s $o))
   (+ (* (- $s $o) (- $s $o)) (* (- (+ $s $o) 1.0) (- (+ $s $o) 1.0))))

; === END SECTION 4 EXTENSIONS ===


; === SECTION 5 TOY MODEL: X = {a, b, c}, two contexts ===
; Context 1 indistinction table (R1: X x X -> V)
; R1(a,a) = (1.0, 0.0)  -- self-identity: full support, no opposition
; R1(b,b) = (1.0, 0.0)
; R1(c,c) = (1.0, 0.0)
; R1(a,b) = (0.8, 0.1)  -- a and b mostly indistinct in C1
; R1(b,a) = (0.8, 0.1)  -- symmetric
; R1(a,c) = (0.2, 0.7)  -- a and c mostly distinct in C1
; R1(c,a) = (0.2, 0.7)
; R1(b,c) = (0.5, 0.5)  -- b and c conflicted in C1 (both channels equal)
; R1(c,b) = (0.5, 0.5)

(= (R1 a a) (pbit 1.0 0.0))
(= (R1 b b) (pbit 1.0 0.0))
(= (R1 c c) (pbit 1.0 0.0))
(= (R1 a b) (pbit 0.8 0.1))
(= (R1 b a) (pbit 0.8 0.1))
(= (R1 a c) (pbit 0.2 0.7))
(= (R1 c a) (pbit 0.2 0.7))
(= (R1 b c) (pbit 0.5 0.5))
(= (R1 c b) (pbit 0.5 0.5))

; Context 2 indistinction table (R2: X x X -> V)
; C2 sees a and c as similar but b as distinct from both
(= (R2 a a) (pbit 1.0 0.0))
(= (R2 b b) (pbit 1.0 0.0))
(= (R2 c c) (pbit 1.0 0.0))
(= (R2 a b) (pbit 0.1 0.8))
(= (R2 b a) (pbit 0.1 0.8))
(= (R2 a c) (pbit 0.7 0.2))
(= (R2 c a) (pbit 0.7 0.2))
(= (R2 b c) (pbit 0.2 0.9))
(= (R2 c b) (pbit 0.2 0.9))

; Salience weights (uniform for simplicity)
(= (mu a) (pbit 1.0 1.0))
(= (mu b) (pbit 1.0 1.0))
(= (mu c) (pbit 1.0 1.0))

; === END SECTION 5 TOY MODEL DATA ===


; === SECTION 5.6 CONCRETE WORKED EXAMPLE (from PDF) ===
(= (R1-paper a b) (pbit 0.90 0.80))
(= (R1-paper b c) (pbit 0.85 0.20))
(= (R1-paper a c) (pbit 0.10 0.70))
(= (R2-paper a b) (pbit 0.20 0.70))
(= (R2-paper b c) (pbit 0.30 0.60))
(= (R2-paper a c) (pbit 0.10 0.80))
(= (weakness-R1) (pbit 0.72 0.80))
(= (weakness-R2) (pbit 0.16 0.80))
(= (closure-R1 a c) (pbit 0.765 0.70))
(= (resonance-coupling) (pbit 0.90 0.90))
(= (R2-post-resonance a b) (pbit 0.81 0.72))
(= (R2-post-resonance b c) (pbit 0.765 0.60))
(= (closure-R2-post-res a c) (pbit 0.61965 0.80))
(= (pattern-support-R1 chain-ab-bc) (pbit 0.765 0.16))
; === END SECTION 5.6 DATA ===


; === SECTION 5.7 ANTI-RESONANCE AS HABIT REVERSAL ===
; ARes imports scaled opposition without erasing positive evidence
; k- = 0.9, R2(a,b) = (0.60, 0.20), R1(a,b) = (0.10, 0.90)
; ARes(R1->R2)(a,b) = (0.60, 0.20) join (0, 0.9)*(0.10, 0.90)
;                    = (0.60, 0.20) join (0, 0.81) = (0.60, 0.81)
; pdec drops from 0.70 to 0.395 -- net inclination flips sign
; Paraconsistent reversal: t stays at 0.60, f rises from 0.20 to 0.81
; The agent keeps reasons-for but reasons-against become weightier
(= (anti-res-example-pre a b) (pbit 0.60 0.20))
(= (anti-res-example-source a b) (pbit 0.10 0.90))
(= (anti-res-example-post a b) (pbit 0.60 0.81))
(= (pdec-anti-res-pre) 0.70)
(= (pdec-anti-res-post) 0.395)

; === SECTION 5.8 COMPLEX INTERFERENCE RESONANCE SCORE ===
; sigma_C(w+,w-) = (w+ - w-) + i*((w+ + w-) - 1)
; Real part = truth-bias d, Imaginary part = contradiction axis c
; Int(z1,z2) = |w1*z1 + w2*z2|^2 - |w1*z1|^2 - |w2*z2|^2
; For equal weights: Int = 0.5 * Re(z1 * conj(z2))
(= (sigma-C-R1 a b) (complex 0.10 0.70))
(= (sigma-C-R2-pre a b) (complex -0.50 -0.10))
(= (sigma-C-R2-post a b) (complex 0.09 0.53))
(= (interference-pre-resonance) -0.06)
(= (interference-post-resonance) 0.19)
; Morphic resonance rotates z2 toward z1 in both real and imaginary
; components -- phase alignment is the numeric witness of resonance

; === END SECTIONS 5.7-5.8 ===


; === SECTION 6: PHENOMENOLOGICAL PRIMITIVES ===
; Occasion space E is small (inf,1)-groupoid
; Context c = (Xc, Pic, deltac, iotac)
; deltac: Xc x Xc -> V (p-bit distinctness evaluator)
; iotac: Xc x Xc -> V (p-bit interchangeability evaluator)
; KEY: deltac and iotac are INDEPENDENT, not negations

; Def40: Directed difference Diffc(x->y) = deltac(x,y)
; Positive channel = evidence x diverges from y
; Negative channel = evidence x does NOT diverge from y
; NOT assumed to be metric, distance, or preorder

; Def41: Distinction Distc(x,y) = Diffc(x->y) otimes Diffc(y->x)
; Symmetric via commutativity of otimes
; Mutual distinctness requires mismatch in BOTH directions

; Def42: Soft interchangeability iotac(x,y) in V
; Interchangeability is NOT sameness -- distinct yet substitutable

; Def43: Repetition and Variety (threshold form)
; Repc(x,y) iff Distc(x,y)+ >= tau_delta AND iotac(x,y)+ >= tau_iota
; Varc(x,y) iff Distc(x,y)+ >= tau_delta AND iotac(x,y)- >= tau_iota
; Repetition = compression opportunity (same pattern different instance)
; Variety = forced complexity (substitutions break)

; === END SECTION 6.2-6.3 DEFINITIONS ===


; === SECTION 6.3: NON-DUALITY AND NON-DUAL VARIETY ===
; NonDualc(x,y) iff Distc both channels >= tau_delta
; Paraconsistent distinctness: high evidence FOR and AGAINST
; NDVarc(x,y) iff iotac both channels >= tau_iota
; NonDual/NDVar = tension WITHIN single axis (upper-right of square)
; Rep/Var = combination ACROSS distinctness and interchangeability axes

; === SECTION 6.4: FIRST SECOND THIRD FOURTH ===
; First = bare entity x in Xc (suchness before relations)
; Second = directed difference event (x,y) + Diffc(x->y)
; Third = V-valued relation R: Xc x Xc -> V (composable schema)
; Fourth = synergistic diagram of Thirds + emergence functional
; Fourth is joint constraint system not aggregation
; Overlap maps encode shared variables between relations
; === END SECTIONS 6.3-6.4 ===


; === SECTION 6.4.2: SET-THEORETIC FIRST-FOURTH LADDER ===
; Firstc := Xc (entities)
; Secondc := Xc x Xc (raw dyadic interactions)
; Thirdc := P(Xc x Xc) (relations = stabilized patterns)
; Fourthc := P(Thirdc) (families of relations)
; Synergizec({Ri}) := cl(Union_i Ri) where cl is closure operator
; Closure adds multi-step consequences: (x,y) in R1 and (y,z) in R2 => (x,z)
; New edges = mathematical shadow of emergence
; Whole > parts because closure generates entailments absent from any single Ri
; Minimal notion of organization: connectivity components, equivalence classes

; === SECTION 6.5: PRESENTATIONAL IMMEDIACY (INTENSITY) ===
; Def49: Ic : Xc -> [0,1] salience field
; Ic(x) near 1 = foreground, near 0 = background
; NOT probability, no additivity constraint, multiple entities can be high
; Not yet attention -- attention comes later as dynamical/resource concept
; Def50: Focusc(tau_I) := {x : Ic(x) >= tau_I}
;         Fringec(tau_I) := {x : 0 < Ic(x) < tau_I}
; tau_I is tunable interface parameter between phenomenology and computation
; High tau_I = narrow spotlight, fast deliberation
; Low tau_I = broad set, exploratory processing, higher combinatorics
; Adaptive policies: lower tau_I under uncertainty, raise under time pressure
; === END SECTIONS 6.4.2-6.5 ===


; === SECTION 6.6: ABSTRACT/CONCRETE AS CONTEXT-RELATIVE ===
; Def51: Abstraction as quotient: surjection q: Xc ->> A
;   Fibers q^-1(a) = equivalence classes of tokens treated as interchangeable
;   Abstractum a = type, fiber = concrete tokens of that type
;   Abstraction = collapsing distinctions, composes naturally
; Def52: Abstraction preorder: q1 <= q2 iff q2 factors through q1
;   q2 at least as abstract as q1 = collapses at least as many distinctions
;   Yields lattice of partitions on Xc when quotiented by mutual factorization
; Prop4: Abstraction increases weakness
;   q1 <= q2 implies Hq1 subset Hq2 implies w(Hq1) <= w(Hq2)
;   More abstraction = more undistinguished pairs = higher weakness
;   Connects Section 6.6 to Section 4 monotonicity

; === SECTION 6.6.2: CONCRETENESS AS RESISTANCE TO QUOTIENTING ===
; Def53: Concreteness constraint Kc predicate on admissible abstractions
;   Prevents trivial collapse (everything to single point)
;   x is concrete if fiber q^-1(q(x)) is small for ALL Kc-admissible q
;   x is abstract if EXISTS admissible q with large equivalence class
;   Kc encodes what context will NOT allow itself to forget
;   Without Kc, maximal abstraction always available = trivializes distinction

; === SECTION 6.7: NON-DUALITY AS BRIDGE BETWEEN PERSPECTIVES ===
; Def54: Context translation T: Xc -> Xd
;   Non-dual compatibility = approximate structure preservation
;   Not exact identity but auditable information loss
;   First-person and third-person as two contexts with different observational capacities
; === END SECTIONS 6.6-6.7 ===


; === SECTION 6.7 CONTINUED: NON-DUAL BRIDGE ===
; Bridge (T,S) with T:Xc->Xd, S:Xd->Xc
; Compatibility: deltac(x,y) <= deltad(Tx,Ty) componentwise in V
; Round-trip: S(T(x)) close to x up to controlled weakness
; Non-invertibility is quantitative and auditable
; Key: non-duality without collapse -- blurring tracked explicitly

; === SECTION 7: ORDER TIME AND BECOMING ===
; Def55: Strict partial order < on T (irreflexive + transitive)
; Proto-time = experienced partial order, pre-metric, no global clock
; Linear time = serialization losing incomparabilities and branching
; Becoming = boundary non-duality between successive occasions
; Paraconsistent event calculus: Happens/HoldsAt valued in quantale V
; Regularity predicates via time-context similarity not global clock
; === END SECTIONS 6.7-7.1 ===


; === SECTION 7.2: PROTO-TIME AS OBSERVER-RELATIVE ORDERING ===
; Def56: Proto-time = pair (T, <) with T temporal indices, < strict partial order
; Minimal formal residue of temporal talk is ordering not duration
; Incomparability = concurrency or no ordering info available
; Past(t) = {s : s < t}, Future(t) = {u : t < u} purely order-theoretic
; Different contexts may carry different proto-times for same occasions
; Paraconsistency is design requirement: multiple incompatible orderings
; Proto-time is aspectual interface indexed by what is tracked/ignored
; Observer-relativity is explicit accounting of representation not relativism

; === SECTION 7.3: GRADED PARACONSISTENT TEMPORAL ORDERING ===
; Def57: p-bit-valued before-relation B: TxT -> V=[0,1]^2
; B+(t1,t2) = positive evidence for t1<t2
; B-(t1,t2) = negative evidence for t1<t2
; Three qualitative cases: uncertain (both low), confident (one high), contested (both high)
; Def58: Coherence constraints (optional regularizers not axioms)
;   Anti-symmetry as evidence: B+(t1,t2) <= B-(t2,t1)
;   Transitive support: B(t1,t3) >= B(t1,t2) otimes B(t2,t3) componentwise
;   Irreflexive support: B+(t,t) = 0
; Temporal uncertainty folded into same quantale calculus as all other relations
; === END SECTIONS 7.2-7.3 ===


; === SECTION 7.4: LINEAR TIME AS SERIALIZATION AND QUOTIENT ===
; Def59: Linear time axis (L, <) where < is strict total order
; Def60: Past/Future sets and quotient-by-indistinguishability
; Theorem5: Finite proto-times admit linear extensions via topological sort
; Remark241: Linearization is many-to-one not invertible -- presentation choice
; Remark242: Linear commitment can bias causal and agency reasoning
; Skeletonization by threshold: B+(t1,t2) >= theta gives derived crisp order
; === END SECTION 7.4 ===


; === SECTION 7.5: BECOMING AS BOUNDARY NON-DUALITY ===
; Becoming is not an extra metaphysical event layered onto static states
; It is the structural relation that makes succession intelligible
; When A becomes B there is a boundary region where both A-identity and
;   B-identity have strong evidential support simultaneously
; This is genuine paraconsistent overlap not confusion or ignorance
; Boundary width is measurable via the p-bit overlap region
; Water-to-ice: near transition both liquid and solid predicates hold
; Concept drift: old and new category both apply during learning
; Becoming-boundary is where the quantale earns its keep --
;   classical logic forces a sharp cut, quantale tracks the gradient
; Connection to bridge principle: becoming IS a temporal bridge
;   with round-trip deviation tracking how much old-identity persists
; === END SECTION 7.5 ===


; === SECTION 7.6: V-VALUED EVENT CALCULUS ===
; Def64: Event calculus signature over quantale V=[0,1]^2
;   Predicates: Happens(a,t), HoldsAt(f,t), Initiates(a,f,t), Terminates(a,f,t)
;   All return p-bit values -- two-channel evidence not probabilities
;   Channels not required to sum to 1 -- permits boundary and conflict states
;   Complete ignorance = (0,0), strong conflict = (0.8,0.7)
; Def65: Quantale-valued implication schema
;   P(x) >= Q1(x1) otimes ... otimes Qn(xn) -- rules give lower bounds
;   Multiple derivations joined via oplus (componentwise max)
;   Tensor otimes = conjunction (chain as strong as weakest link)
;   Join oplus = alternative proofs compete (best argument dominates)
; Def66: Clipped(f;t1,t2) = join over all a,u of Happens(a,u) otimes Terminates(a,f,u)
; Def67: Inertia update Phi using HoldsAt0 oplus HoldsAt(f,t1) otimes neg-Clipped
;   neg is p-bit involution swapping channels -- not classical negation
; Theorem6: Monotone temporal inference has least fixpoint (Knaster-Tarski)
;   Monotonicity: adding evidence cannot invalidate previous inferences
;   Aligns with streaming and incremental updates
; Negation-as-failure replaced by explicit negative channel + weakness bias
; === END SECTION 7.6 ===


; === SECTION 7.7: TIME CONTEXTS AND TEMPORAL SIMILARITY ===
; Def68: TimeCtx(t) = vector of HoldsAt(f,t) for all f in F
;   Not a coordinate but a bundle of conditions
;   Observer-relative: refining vocabulary increases dimension
; Def69: Truth-value projection pi: V -> [0,1]
;   simT(t1,t2) = average simV over all fluents
; Def70: TemporalSimilarity derived crisp predicate -- no external clock
; === SECTION 7.8: PERSISTENT CONTINUOUS INCREASING DECREASING ===
; Def71: Continuous fluent -- similar times have similar values
; Def72: Persistent fluent -- continuous + bounded total variation
; Def73: Increasing/decreasing -- monotone under projection
; Remark286: Continuity without persistence signals smooth transformation
; === END SECTIONS 7.7-7.8 ===


; === SECTION 7.9: BECOMING AS FUNCTORIAL PROCESS ===
; Def74: Process over proto-time T is functor S: T -> Sys
;   T viewed as thin category: objects are timepoints, unique morphism t1->t2 iff t1<t2
;   S assigns each timepoint a state-object S(t) in Sys
;   S assigns each precedence t1<t2 an evolution morphism S(t1)->S(t2)
;   Functoriality: S(t1->t3) = S(t2->t3) . S(t1->t2) -- multi-step factors into successive steps
; Remark287: Time becomes parameter indexing structure-preserving transformation
;   Laws of motion = chosen morphisms in Sys witnessing admissible change
;   Changing Sys changes what counts as lawlike update
; Remark288: Becoming = coherent translations respecting proto-temporal composition
;   Later: replace Sys with pattern-flow structures, admit approximate morphisms
;   Approximate = enriched/metric setting with distortion/error budget
; Remark289: Event calculus and functorial view are complementary lenses
;   EC emphasizes logical entailment about discrete events
;   Functorial view emphasizes structured evolution and compositionality
;   Bridge: extract predicates from states or build process from time contexts
;   Partial order T supports branching and concurrency naturally
; === END SECTION 7.9 ===
; === SECTION 8.0: EFFORT RESISTANCE SIMPLICITY (INTRO) ===
; Effort as typed magnitude not informal proxy for time/energy/difficulty
; Supports: sequential composition, choice among alternatives, minimization
; Cost quantale Def75: E = ([0,inf], >=, inf, +, 0) -- Lawvere cost quantale
;   Reversed order: lower cost = larger in quantale order
;   Join = inf (ordinary minimum), monoidal product = + (sequential composition)
;   + distributes over arbitrary infima -- Bellman optimal substructure
;   inf included for impossible/unavailable operations
; Simplicity = minimum representational effort -- observer-relative design principle
; Distinction policy: rule for which differences are relevant
;   Opening = admit more distinctions, Closing = collapse distinctions
; Resistance = effort gradient for changing distinction policy
; Weakness maximization dual: simple = leaves many distinctions unresolved
; Compositional simplicity = least-fixed-point over combination system
; Generalized Kolmogorov: program length -> effort quantale, UTM -> observer repertoire
; === END SECTION 8.0 INTRO ===


; === SECTION 8.1: EFFORT OF A PROCESS ===
; Def76: Effort assignment EffC: P -> [0,inf] for processes in context C
;   Sequential subadditivity: EffC(p;q) <= EffC(p) + EffC(q)
;   Choice: EffC(p) = min(EffC(p1), EffC(p2)) when p implementable by choosing p1 or p2
;   Lax monoidal measure: respects + up to inequality not equality
;   Synergies allowed (combined < sum), frictions modeled elsewhere via tC
;   Context-dependent: same process p has different effort in different C
;   GPU, precomputed index, specialized library can change EffC by orders of magnitude
; Remark294: Method A costs 3, Method B costs 5 -> choice = inf(3,5) = 3
;   Sequential: 3 + 5 = 8. Basic grammar of optimization before any mind talk
;   Infimum over parameter k: inf_{k in N} f(k) -- handles asymptotic cases cleanly
; Remark298: Minimal interface for simplicity-as-infimum and compositional-simplicity-as-LFP
; === SECTION 8.2: DISTINCTIONS AS POLICIES ===
; Def77: Indistinction policy H subset X x X for finite universe X in context C
;   (x,y) in H means observer does not distinguish x from y in C
;   NOT required to be equivalence relation -- allows asymmetric/inconsistent discrimination
;   H=empty: distinguish everything (max effort), H=XxX: collapse everything (min effort)
;   Admissible set HC left abstract -- application constrains which policies are legal
; Remark303: Often implemented by representation map pi:X->R, H = kernel of pi
;   But H as arbitrary relation covers direction-dependent and history-dependent cases
; Def78: Opening H->H2 iff H subset H2 (more pairs collapsed, coarser)
;   Closing H->H2 iff H2 subset H (fewer pairs collapsed, finer)
;   Opening reduces representational effort but may reduce predictive sharpness
;   Closing increases effort but may increase control/predictive sharpness
; Remark309: Non-monotone trajectories = attention reallocation over time
;   Zoom out for tractability then zoom in on salient subproblem
; === SECTION 8.3: EFFORT OF DISTINCTIONS ===
; Def79: Policy effort functional EffC: HC -> [0,inf] is antitone wrt inclusion
;   H subset H2 implies EffC(H) >= EffC(H2) -- coarser policy = less effort
;   Marginal effort: deltaEffC(H->H2) = max(0, EffC(H2) - EffC(H))
;   inf allowed for unrealizable policies (unattainable sensor resolution etc)
; Remark312: Resistance = cost of maintaining closing against pressures to open
;   Simplicity = availability of effective openings that preserve task performance
;   Not merely small description length but small length RELATIVE TO tolerated policy
; === END SECTIONS 8.1-8.3 ===


; === SECTION 8.4: SIMPLICITY AS MINIMUM REPRESENTATIONAL EFFORT ===
; Def80: Resistance = deltaEffC(H->H2) for directed policy change
;   Submission = change where deltaEffC = 0 (no additional effort demanded)
;   Resistance is operational not psychological -- extra load for tighter constraints
;   Analogue of thermodynamic gradient: forcing more constrained config costs work
;   Thin formalization intentional -- later decomposed into sensing/inference/memory terms
; Def81: Simplicity sC(x) = inf{EffC(r) : r in RC(x)}
;   RC(x) = set of admissible representations of x in context C
;   Infimum = best achievable effort among all representational strategies
;   Not intrinsic geometric/syntactic attribute but property of best interface
;   Changing RC (adding new representational primitive) can strictly decrease sC
;   Learning new concepts can make previously complex items simple
;   sC(x) = +inf when no admissible representation exists (RC empty)
;   Generalized MDL: description length -> effort, UTM -> observer repertoire
; Remark325: Close to algorithmic information theory but effort replaces length
;   Observer-relativity central -- same x different simplicity in different C
; Remark327: Patterns will enter as representations whose effort << baseline
;   Two-part modeling: choose admissible representations then minimize effort
; === SECTION 8.5: SIMPLICITY AS WEAKNESS (DUAL PERSPECTIVE) ===
; Theorem7: Effort-weakness monotonicity
;   w: HC -> V is monotone wrt inclusion (weakness grows with opening)
;   EffC: HC -> [0,inf] is antitone wrt inclusion (effort shrinks with opening)
;   Opening simultaneously increases weakness and decreases effort
;   Along any inclusion chain: weakness nondecreasing, effort nonincreasing
;   Hinge theorem connecting two calculi: weakness composes well (quantale)
;   and effort supports minimization -- theorem guarantees no perverse interaction
; Remark329: If you merge more cases (open), weaker AND cheaper
;   Rules out pathological: more indiscriminate yet more effort
; Remark331: Pattern intensity (Section 9) compares effort before/after
;   representational move -- this monotonicity lets qualitative conclusions
;   translate between weakness and effort viewpoints
; === END SECTIONS 8.4-8.5 ===


; === SECTION 8.6: MINIMUM REPRESENTATIONAL EFFORT AS CONSTRAINED WEAKNESS MAX ===
; Def82: Task constraint AdeqC(H) in {true,false} -- policy H adequate for task
;   Feasible set FC = {H in HC : AdeqC(H)}
;   Without adequacy constraint cheapest policy = maximally open = useless
;   Adequacy is where what the observer is trying to do enters the formalism
;   FC can be empty -- diagnosis: enlarge HC, weaken AdeqC, or change task
; Def83: Minimum representational effort principle
;   H* in argmin{EffC(H) : H in FC} -- cheapest adequate policy
;   Cognitive Occam: framed in actual expenditures not language-invariant length
;   Normative AND dynamical: preferred in equilibrium + learning drifts toward it
;   Effort includes latency memory footprint sampling cost energy sensor wear
;   Two extensionally equivalent policies can differ in effort (implementation matters)
; Theorem8: Maximally open adequate policy under upward closure
;   If FC upward closed (opening preserves adequacy) then:
;   H_hat = union of all H in FC exists and is in FC
;   H_hat is unique greatest element -- every feasible H subset H_hat
;   H_hat minimizes effort (antitonicity) AND maximizes weakness (monotonicity)
;   Turns optimization into order-theoretic union construction
;   Hard part is specifying adequacy correctly not solving the optimization
; Corollary1: No free lunch -- under opening cannot get strictly less weakness
;   nor strictly more effort. Rules out pathological policy pairs
; Remark347: Upward closure natural when adequacy depends only on retaining
;   necessary distinctions. Fails when side-constraints not monotone under opening
;   (protected groups, audit variables, safety constraints on action selection)
; Remark349: Algorithmic reading: repeatedly open while checking adequacy
;   = bias toward representational compression with constraint checks
; === END SECTION 8.6 ===


; === SECTION 8.7: COMPOSITIONAL SIMPLICITY ===
; Def84: Combination system (XC, *, e) with overhead tC: XC x XC -> [0,inf]
;   * NOT necessarily associative -- different assembly orders yield different costs
;   Decomposition is tree-shaped not set-based
;   e is identity-like element -- normalization sC(e)=0
;   tC isolates composition cost: interface matching, coordination, translation
; Def85: Compositional simplicity functional sC: XC -> [0,inf]
;   Admissibility: sC(x) <= inf{sC(y)+sC(z)+tC(y,z) : y*z=x}
;   Least admissible solution s*C is THE compositional simplicity
;   Bellman-style: simplicity of whole <= best build from parts
;   Fixed-point: s*C is least post-fixed point of operator F
; Proposition5: s*C(y*z) <= s*C(y) + s*C(z) + tC(y,z)
; Theorem9: s*C(x) = minimum parse-tree cost (finite case)
;   Cost = sum of tC at internal nodes + base costs at leaves
;   Dynamic programming over factorization trees -- generalized CYK
; === END SECTION 8.7 ===


; === SECTION 8.8: GENERALIZED KOLMOGOROV COMPLEXITY AND STRUCTURAL COMPLEXITY ===
; Classical Kolmogorov measures shortest program length -- Hyperseed generalizes:
;   Replace program length with effort in whatever resources observer actually expends
;   Replace UTM with observer-relative decoding procedure
; Def86: Generalized description system for context C consists of:
;   DC = set of descriptions (programs, proofs, encodings, plans, circuits)
;   DecC: DC -> XC partial decoding map (partial = not every description succeeds)
;   EffC: DC -> [0,inf] effort assignment with sequential subadditivity
;   Partiality captures: ill-formed strings, non-halting programs, failed proofs
;   DC can be binary strings, formulas, circuits, proofs, action sequences, model specs
;   EffC can count length, runtime, energy, memory, proof steps, or weighted blend
;   Effort [0,inf] codomain: infeasible descriptions get infinite effort, infima always exist
; Def87: Generalized Kolmogorov complexity KC(x) = inf{EffC(d) : d in DC, DecC(d) = x}
;   Same infimum-over-descriptions pattern as simplicity sC(x)
;   KC(x) = inf when no description decodes to x (empty set convention)
;   Observer-indexed family of complexities -- NOT single universal measure
;   When EffC is time or energy: KC is feasibility measure not static size
;   Two observers with different hardware/training assign different KC to same x
; Remark388: Cross-context comparison requires explicit translation tau: DC1 -> DC2
;   with DecC2(tau(d)) = DecC1(d) and EffC2(tau(d)) <= EffC1(d) + kappa
;   This is generalized invariance theorem -- compiler overhead in observer-relative language
; Remark394: Classical recovery: DC = {0,1}*, EffC = bitlength, DecC = UTM
;   yields standard Kolmogorov complexity up to additive constant
; Proposition6: Structural complexity = compositional simplicity (up to base costs)
;   When DC generated by finite primitives + binary constructor with overhead tC:
;   Every description induces a parse tree -- KC(x) coincides with s*C(x)
;   descriptions -> parse trees -> fixed point (chain via Theorem 9)
;   Grammar derivations, circuit expressions, proof trees all instances of same template
;   Differing only in what counts as primitive, what constructor does, how effort tallied
; Remark398: Grammar-like complexity appears naturally from compositionality
;   Compression and structure are costs of derivations in appropriate description systems
; === END SECTION 8.8 ===


; === SECTION 8.9: DISCUSSION -- HOW EFFORT/SIMPLICITY FEEDS LATER LAYERS ===
; This section is a roadmap connecting Sections 7-8 infrastructure to Sections 9+
; Core thesis: effort is primitive experiential thermodynamics of cognition
;   simplicity is its observer-relative compositional shadow
; Methodological constraint: every new entity (pattern, habit, control structure)
;   must be interpretable as mechanism for reallocating/reducing/regularizing effort
; Simplicity is relational not intrinsic: how observer interacts with x under constraints
; Three forward pointers:
; 1. PATTERNS (Section 9): representation r of x yielding significant effort reduction
;    Pattern intensity = baseline effort vs achieved effort comparison
;    Same r can be intensely patterned for one observer, trivial for another
;    Baseline is crucial -- observer-relativity of patterns follows from observer-relativity of effort
; 2. HABITS AND MORPHIC RESONANCE (Section 12): repeated policy updates
;    progressively reduce effective effort for certain decompositions
;    Resistance/submission become dynamical (history-dependent) not static
;    Distinction policy iteratively updated -- future decompositions solvable at lower marginal effort
;    Resistance = inertial term persisting across time
;    Submission = learned alignment making decomposition pathway increasingly low-effort
;    Weakness and effort evaluated along updating process -- explicitly history-dependent
; 3. MIND-WORLD CORRESPONDENCE (Section 14+): good models near Pareto frontier
;    of adequacy vs effort. Weakness composes models across contexts
;    No false dichotomy between accurate and simple
;    Too complex = adequacy does not justify effort relative to alternatives
;    Too simple = low effort at avoidable adequacy loss
;    When causality/control layer adds interventions: effort budget includes
;    cost of acquiring leverage over environment -- same algebraic bookkeeping applies
; Slogan: effort provides primitive thermodynamics, simplicity is compositional shadow
; === END SECTION 8.9 ===


; === SECTION 9.1: SETUP -- ENTITIES, CONTEXTS, DESCRIPTIONS, AND EFFORT ===
; Assumes effort/simplicity layer from Section 8 provides per context C:
; EC = universe of entities as individuated by C (NOT context-independent ontology)
;   Text context: EC = strings. Vision: EC = images up to equivalence. Engineering: designs with tolerances
; *C: EC x EC -> EC partial combination operation (putting things together in C-relevant sense)
;   Partiality deliberate: some pairs non-composable (interface mismatch, incompatible constraints)
;   No global algebraic laws assumed unless explicitly stated -- associativity etc are approximate regularities
; LC = description system (syntax) with decoder DecC: LC -> EC
;   Makes explicit that having an entity is operationally mediated by representational resources
;   costC(l) = inf for ill-formed or semantically unusable descriptions
;   Cost can represent bits, time, memory, energy, cognitive effort, or weighted mixture
;   Includes fixed overheads (calling subroutine) and variable costs (specifying parameters)
; Def88: Contextual description complexity sC(x) = inf{costC(l) : l in LC, DecC(l) = x}
;   Lower sC(x) = simpler for C. Uses inf not min (allows limiting approximations)
;   sC(x) = inf when x indescribable in C. Relative in two ways: depends on LC and DecC
;   Changes in measurement conventions, primitives, background knowledge = changes in C
; Remark402: Equivalent to compositional simplicity recursion via parse trees (Def85/Thm9)
;   Parse tree view: internal nodes = composition rules, leaves = primitives
;   Glue/interaction overheads = costs of making parts compatible
;   Description-based formulation packages all choices into LC, DecC, costC -- most portable
; p-bit connection: Def89 mismatch evidence map misC: LC x EC -> [0,1]^2
;   misC(l,x) = (m+, m-) positive and negative evidence that l fails to match x
;   Paraconsistent: both coordinates can be high simultaneously
;   m+ high from counterexamples, m- high from confirmations or unreliable diagnosis
;   Does NOT require m+ + m- = 1 -- partial conflicting heterogeneous fit
;   Uses: feasibility filter, additive penalty with costC, downstream trustworthiness record
; === END SECTION 9.1 ===

; === SECTION 9.2: COMBINATION, INHERITANCE, ASSOCIATION AS PATTERN-LEVEL NOTIONS ===
; Distinguishes dynamic combination (co-becoming in time, Section 7) from static (property union/blend)
; Static = evaluated at fixed descriptive moment, ignoring micro-history of co-formation
; Def90: Static combination system in context C = pair (EC, *C) with *C partial binary
;   Explicit C-dependence: which combinations meaningful depends on background ontology
;   EC = entity-kinds currently in play. *C = context rule for forming composites/blends
;   No algebraic laws a priori -- commutativity, associativity stated as additional structure when justified
; Remark403: Naturally typed/multi-sorted -- *C only defined on compatible pairs
;   Compatible = sharing interface, same sort, satisfying constraint
;   Undefined combination marks boundary of coherent discourse, not defect
; Def91: Inheritance as substitutability preorder <=C on EC
;   A <=C B means A can substitute for B in many C-relevant contexts
;     without increasing representational effort or breaking too many patterns
;   Preorder: reflexive + transitive, not necessarily antisymmetric
;   Distinct entities can be mutually substitutable -> equivalence classes of same role
;   Substitutability rarely absolute -- stability across sufficiently rich family of pattern-instances
;   Later instantiated via property-set comparison (Def98) or low-effort rewrite maps
; Def92: Association score assocC: EC x EC -> [0,1] symmetric
;   Measures co-occurrence or shared properties/patterns
;   No further axioms imposed -- Jaccard similarity or weighted variants typical implementations
;   Dynamic association (temporal co-focusing) treated in Sections 7 and 12
;   Static implementation via property-set overlap (Def101)
; === END SECTION 9.2 ===


; === SECTION 9.3: PATTERNS AND PATTERN INTENSITY ===
; Central thesis: pattern = representation that is simpler than baseline
; Two equivalent witnesses: description form and compositional factorization form
;
; 9.3.1 Patterns as compressive descriptions
; Def93: Pattern witness (description form) for x in EC is any l in LC with DecC(l) = x
;   Description cost = costC(l). Every entity has infinitely many trivial witnesses
;   Nontrivial content comes from RELATIVE simplicity -- need baseline to prevent vacuity
; Def94: Baseline description and compression gain
;   baseC: EC -> LC with DecC(baseC(x)) = x -- observer default encoding
;   sbaseC(x) := costC(baseC(x)) -- how hard x is BEFORE noticing any structure
;   Raw compression gain: DeltaC(l;x) := sbaseC(x) - costC(l)
;   Positive = l improves on baseline. Negative = worse than default
;   Baseline is part of observer model -- different observers see different patterns
;   Remark405: observer-relativity of patterns follows directly from observer-relativity of baseline
;   sbaseC(x) is deliberately operational: defined by concrete encoding choice
;
; 9.3.2 Patterns as compositional factorization
; Def95: Compositional pattern witness P = (y, z, t) for x in EC
;   y, z in EC with x = y *C z. t >= 0 is glue/interaction overhead
;   Composite cost: hC(P) := sC(y) + sC(z) + t
;   t >= 0 encodes that composition is never free in accounting
;   Small t = clean modular decomposition. Large t = strongly entangled composite
;   Remark406: t derivable from interpreter overhead, MDL model-class penalty,
;     constraint complexity, wiring diagram cost, interface spec
;   hC uses sC (not sbaseC) for parts -- exploit whatever simplicity context provides
;   Judged against sbaseC for WHOLE x when computing intensity
;   Informal: pattern worthwhile if it makes whole cheaper than default description of whole
;
; 9.3.3 Pattern intensity
; Def96: Scalar pattern intensity IC(l;x) = max(0, (sbaseC(x) - costC(l)) / sbaseC(x))
;   For compositional witness: IC(P;x) = max(0, (sbaseC(x) - hC(P)) / sbaseC(x))
;   Clamped to [0,1]. IC = 0 when sbaseC(x) = 0 by convention
;   Normalization makes intensity comparable across entities of different absolute size
;   Saving 10 units matters more when baseline is 20 than when baseline is 2000
;   IC = 0 means no improvement or worse. IC near 1 = dramatic simplification
;   Invariant under uniform rescaling of cost units within fixed context
;   Changes when observer changes baseline -- exactly as intended
; Prop7: Sanity properties: (1) 0<=IC<=1, (2) IC>0 iff strict compression,
;   (3) monotone decreasing in witness cost
;
; Def97: p-bit pattern intensity IntC(l;x) = (IC(l;x), misC(l,x)+) in [0,1]^2
;   First coordinate: compressive strength. Second: mismatch evidence
;   Separates how USEFUL pattern is as compressor from how TRUSTWORTHY as account
;   Coarse model: high IC but non-negligible mismatch (ignores boundary effects)
;   Exact but cumbersome encoding: low IC but zero mismatch
;   Remark407: Intentionally permissive -- retains compressive pattern even when partly false
;   This IS the role of paraconsistent logic in the ontology
;   Selection rules can prefer high-intensity AND low-mismatch but representation does not
;   have to discard high-intensity idea merely because not perfectly accurate
; === END SECTION 9.3 ===

; === SECTION 9.4: PROPERTIES AS FUZZY SETS OF PATTERNS (beginning) ===
; Properties are DERIVED not primitive -- patterns collected and graded by intensity
; Begin with family of pattern-detectors PC relevant to context C
;   (logical predicates, learned features, dynamical motifs, compression primitives)
; Having a property = exhibiting corresponding pattern with graded strength
; Property vocabulary induced by pattern vocabulary -- not independently given
; Any change in PC or IC changes resulting property semantics
; Def98: Property-set PropC(x): PC -> [0,1] is a fuzzy set
;   Maps each candidate pattern p in PC to its intensity for x
;   Context-indexed: same entity supports different salient patterns in different contexts
;   PropC(x) is description not absolute inventory of intrinsic attributes
; === END SECTION 9.4 (partial -- reading forward for completion) ===


; === SECTION 9.4 (complete): PROPERTIES AS FUZZY SETS OF PATTERNS ===
; PropC(x)(P) := IC(P;x) -- property-set IS the pattern intensity profile
; If p-bit intensity used, PropC(x) is p-bit-valued instead
; Finite PC: PropC(x) is vector in [0,1]^|PC| -- explicit feature map
; Countable PC: bounded sequence. Measurable families: bounded function for integration
; Fuzzy-set reading deliberate: patterns present to a degree -- partial, noisy, scale-dependent
; p-bit codomain: strength of evidence in paraconsistent sense
;   Can always scalarize (expected degree, detection probability) but p-bit retains compositionality
;
; Def99: Mass of property-set ||PropC(x)||_1 := sum over P in PC of PropC(x)(P)
;   L1 mass = simplest aggregate of how much structured regularity present
;   Distinguishes: weakly supports many patterns vs strongly supports few
;   Finite PC: mass in [0,|PC|]. Countable: finiteness is substantive condition
;   Can introduce weights w(P) for salience/cost differentiation
; Remark408: Mass is pattern-theoretic analogue of total structured regularity
;   Overlap correction needed when distinct patterns co-triggered by same underlying regularity
;   Three approaches: (i) discount via similarity/implication relations,
;     (ii) select approximately independent subsets, (iii) factorize to minimal basis
;   Definition stays minimal -- easy to compute and easy to replace
;
; 9.4.1 Inheritance and association via properties
; Def100: Inheritance via property inclusion A >=C B iff PropC(A)(P) >= PropC(B)(P) for all P
;   Pointwise dominance -> automatic preorder (reflexive + transitive)
;   Antisymmetry may fail: distinct entities with identical property-sets
;   Equivalently: PropC(B) is fuzzy subset of PropC(A)
;   Intuition: A can stand in for B on all pattern-tests in PC
;   Remark409: Direct rendering of substitutability in contexts
;   Practical weakening: (i) slackened PropC(A)(P) >= PropC(B)(P) - epsilon(P),
;     (ii) weighted aggregate shortfall sum w(P)(PropC(B)(P)-PropC(A)(P))+ <= delta
;   Both preserve systematic dominance while allowing controlled exceptions
;
; Def101: Association from property overlap -- fuzzy Jaccard similarity
;   assocC(A,B) = sum min{PropC(A)(P),PropC(B)(P)} / sum max{PropC(A)(P),PropC(B)(P)}
;   Convention 0/0 := 0 (blank descriptions = no association signal)
;   In [0,1]. Equals 1 iff property-sets agree pointwise. Near 0 when supports disjoint
;   Remark410: Other similarities fit same role (inner product, Hellinger, Hutchinson)
;   Choice partly modeling decision about what overlap means
;   Jaccard: scale-sensitive to union. Inner product: co-activation dominated by mass
;   Distributional distances natural if normalizing PropC to probability over patterns
; === END SECTION 9.4 ===

; === SECTION 9.5: EMERGENCE ===
; Emergence of (A,B) relative to combination *C = patterns more intense in A*B
;   than explained by A and B separately. Comparison pattern-by-pattern
; Baseline prediction from parts' intensities distinguishes interaction-driven structure
;   from structure already present in components
;
; Def102: Weighted baseline for emergence
;   wC(A) = sbaseC(A)/(sbaseC(A)+sbaseC(B)), wC(B) = sbaseC(B)/(sbaseC(A)+sbaseC(B))
;   Convex weighting: wC(A)+wC(B)=1, both >= 0
;   Requires sbaseC(A)+sbaseC(B) > 0 (rules out degenerate case)
;   When one part has zero baseline: baseline reduces to nonzero contributor
;
; Def103: Emergent surplus and emergent intensity
;   SurC(P;A,B) = IC(P;A*CB) - [wC(A)*IC(P;A) + wC(B)*IC(P;B)]
;   EmerC(P;A,B) = max{0, SurC(P;A,B)}
;   Negative surplus = pattern suppressed in composite (recoverable from SurC directly)
;   Emergence focuses on positive novelty via clamping
;   Remark412: Negative surplus = suppression, interesting but separate from emergence
;   Remark413: Baseline is convex combination -> EmerC measures gain over weighted mixture
;     If IC normalized to [0,1], EmerC inherits bounded nonnegative interpretability
;
; Prop8: Basic properties: (1) EmerC >= 0, (2) EmerC <= IC(P;A*CB) when IC >= 0,
;   (3) EmerC = 0 when composite intensity <= weighted baseline
; Prop9: Symmetry under commutative combination: EmerC(P;A,B) = EmerC(P;B,A)
;
; Remark414: High density of high-intensity emergent patterns spanning composite
;   = system whose organization not reducible to components
;   Weighting by sbaseC makes emergence sensitive to relative amount of each component
;   sbaseC can track size, mass, duration, or any additive baseline contribution
;
; Def104: Collective-property-set PropcollC(A)(P) = sup over B in reference class B of EmerC(P;A,B)
;   Turns emergence into property assignment: how strongly can A support emergence of P
;     across all relevant interaction partners?
;   sup allows infinite B or limiting sequences
;   Remark415: When B finite or compact, sup often replaceable by max
;
; Prop10: Monotonicity in reference class: B1 subset B2 implies PropcollC over B1 <= over B2
; === END SECTION 9.5 ===


; === SECTION 9.6: BLENDS ===
; Blend = entity whose properties are largely attributable to parent entities A and B
; Property-theoretic: C is blend of A,B when significant fraction of C properties also in A or B
; Partial overlap -- graded not all-or-nothing
;
; Def105: Blend score and blend predicate
;   Property overlap mass: ovC(C;A,B) = sum over P of min{PropC(C)(P), max{PropC(A)(P),PropC(B)(P)}}
;   max = either-parent supplier of property mass. min = credit only what parent supports
;   Fuzzy-set analogue of |C intersect (A union B)| when properties crisp
;   blendscoreC(C;A,B) = ovC(C;A,B) / ||PropC(C)||_1 when mass > 0, else 0
;   Normalized coverage ratio: fraction of C property mass explained by at least one parent
;   In [0,1]. Equals 1 iff PropC(C)(P) <= max(PropC(A)(P),PropC(B)(P)) for all P
;   C is blend of A,B if blendscoreC >= theta (threshold parameter)
;   Remark416: Parametric by design -- theta and mass functional application-dependent
;   Higher theta = most of C attributable to parents. Lower theta = C introduces novel properties
;   Pooling operator replaceable: t-conorm, softmax, additive-with-cap changes joint support semantics
;   Crisp limit: ovC counts properties C has that at least one parent also has
;   Graded: fractional -- if C has P to 0.6 but best parent support is 0.4, only 0.4 credited
;
; 9.6.1 Categorical blend construction (pushout intuition)
; For compositional entities (graphs, terms, enriched presheaves): blend = colimit
; Def106: Blend as colimit with weak-glue preference (sketch)
;   Category C of entity-structures. Given A,B in Ob(C), blend diagram is span:
;   S -iA-> A, S -iB-> B where S = extracted shared subpattern
;   Categorical blend = pushout: A -> Blend(A,B;S) <- B
;   Plus ranking functional (effort/weakness) preferring spans S with lower glue overhead
;   S = alignment hypothesis: which parts of A,B treated as same for blending
;   Pushout = minimal identification consistent with alignment hypothesis
;   Effort/weakness preference = regularization: favor explaining commonality with minimal identifications
;   Remark417: Approximate colimits in quantale-enriched setting often better cognitively
;   Multiple partial shared subpatterns, conflicting identifications handled paraconsistently
;   Approximate gluing -> intermediate masses in PropC(Blend) rather than hard yes/no
; === END SECTION 9.6 ===

; === SECTION 9.7: LIFTING FROM INSTANCES TO GROUPS ===
; Once relation defined for instances, multiple sensible lifts to groups
; Def107: Three lifts of instance relation C(.,.) : X x Y -> [0,1]
;   For finite nonempty A subset X, B subset Y:
;   Cavg(A,B) = (1/|A||B|) sum_a sum_b C(a,b)  -- average affinity
;   C_forall_exists(A,B) = min_a max_b C(a,b)   -- every a covered by some b
;   C_exists_forall(A,B) = max_b min_a C(a,b)   -- single b covers all a (prototype)
;   Remark418: avg = on average, forall-exists = coverage, exists-forall = prototype
;   Remark419: Empty groups need convention (1 for vacuous, 0 for no-evidence, or undefined)
;   Remark420: Crisp case recovers quantifier patterns:
;     C_forall_exists = 1 iff forall a exists b with C(a,b)=1
;     C_exists_forall = 1 iff exists b forall a with C(a,b)=1
;   Remark421: Minimax inequality gives C_exists_forall <= C_forall_exists always
;     exists-forall more demanding: one b uniformly good vs best b depends on a
;   Remark422: Cavg = cloud affinity, C_forall_exists = directed coverage, C_exists_forall = prototype score
;   Generic mechanism behind lifting reference, association, emergence from episodes to categories
; === END SECTION 9.7 ===

; === SECTION 9.8: COMBINATORIAL-CATEGORICAL PATTERNS ===
; Patterns visible only after category-theoretic substitution/relabeling
; Apply rule system assigning category labels to instances -> derived structure -> mine patterns
; Def108: Category domain W (finite set of types) and membership state m: S -> 2^W
;   Binary relation view: (s,w) in Rm iff w in m(s). Incidence matrix |S|x|W|
;   Subsequent closure = monotone update of relation by rules
; Def109: Combinatorial-categorical theory T = finite set of Horn rules
;   Form: (x in A) and (y in B) => (z in C) where x,y,z in S and A,B,C in W
;   Horn-style implication over atomic predicates s in w
; === END SECTION 9.8 (partial -- reading forward for closure operation and completion) ===


; === SECTION 9.8 (complete): COMBINATORIAL-CATEGORICAL PATTERNS ===
; Def110: Substitution output / closure sub(T, S, m0) = (S, mT)
;   mT = least fixed point under set inclusion from iterative forward-chaining of T rules
;   Start from m0, whenever rule antecedent holds under current m, add C to m(z)
;   Terminates in at most |S|*|W| additions. Confluence: any fair schedule yields same mT
;   Closure operator FT monotone: adding initial labels or rules can only add, never remove
; Def111: Combinatorial-categorical pattern = standard pattern in derived structure sub(T,S,m0)
;   Patterns searched in theory-generated representation, not raw instance space
;   Separates two inductive biases: T determines expressible composite categories (feature generation)
;     Mining scheme determines which regularities count as salient (frequency, compressibility, etc)
;   Clean docking port to pattern theory: T generates derived feature space, then mine compressive structures
; === END SECTION 9.8 ===

; === SECTION 9.9: COMBINATION SYSTEMS AND CAUSAL MODELS ===
; Formalizes computational and dynamical notions for combinations
; Def112: Combination system (S, *) with * partial binary operation on S
;   Partiality encodes compatibility constraints: some pairs do not combine
;   No associativity/commutativity/identity/inverses assumed unless explicitly added
;   Covers: term concatenation, multiset union, function composition, event interaction, process coupling
;
; Def113: Interpreted combination system (S, *, Dec) with Dec: L -> S interpreter
;   L = syntactic language, Dec = decoder/evaluator
;   Compositionality requirement: Dec(l1 . l2) = Dec(l1) * Dec(l2) when RHS defined
;   Dec is homomorphism from syntactic combination into semantic combination system
;   Undefinedness on semantic side = syntactic composite has no coherent meaning
;   Remark430: formal core of 'computational model = interpreted combination system'
;   L need not be closed under . for all pairs -- formation rules and compatibility conditions
;
; Def114: Combination-preserving representational mapping f: D -> S
;   D = domain of processes/events with interaction operator **
;   f(a ** b) = f(a) * f(b) whenever both sides defined
;   Consistency between what happens in dynamical domain and how named in symbol system
;   Non-injective f intentionally collapses distinct domain elements into same symbol
;   Enforced only on intersection of defined regions of ** and *
;
; Def115: Combinational dynamical causal model Gamma: D x D x D -> [0,1]
;   Gamma(a,b,c) = degree to which interaction of a and b caused c
;   Two-input interaction resulting in outcome -- graded causal attribution
;   Valid relative to f iff: f(a)=f(a'), f(b)=f(b'), f(c)=f(c') implies Gamma(a,b,c)=Gamma(a',b',c')
;   Validity = invariance under equivalence relation induced by representation
;   Gamma factors through quotient: causal scores depend only on (f(a),f(b),f(c))
;   Remark431: causality computed relative to representational alphabet (observer-relative ontology)
;   If f merges micro-processes into macro-symbol, validity forces same causal degree
;   Violation means representation too coarse for causal distinctions being made
; === END SECTION 9.9 ===

; === SECTION 9.10: SPECIFIC ENTITIES AS TEMPORALLY COHERENT PATTERNS ===
; Specific entities (objects, persons, institutions) = complex derived constructions not primitives
; Identity behaves like pattern with temporal algebra
; Def116: Occurrence stream {x_t}_{t in T} with (T, <=) partially ordered set (proto-time)
;   Partial order allows branching, concurrency, causal precedence -- not forced linear history
;   Stream may be partial: some t have no x_t (missing observations, gaps, non-representation)
;
; Def117: Specific entity = occurrence stream + coherence rule R satisfying:
;   (1) Same-time identity: t=t' and both occur implies x_t = x_{t'} (determinacy at a time)
;   (2) Near-time similarity: t,t' close in proto-time implies assocC(x_t, x_{t'}) high
;   Strength of being same specific entity is GRADED by how well stream satisfies these rules
;   R parameterizes: what counts as close in proto-time, what counts as high association
;   Different contexts yield different specific-entity criteria (legal vs biological vs physical)
;   Ship of Theseus: local similarity high but long-range similarity low -> identity secure locally, disputable globally
;   Institutional entities: R weights organizational roles/charters over physical continuity
;   Remark432: specific entity IS a pattern (temporally stable property bundle) with conventional defaults
;   Identity questions reframed as optimization: seek streams maximizing coherence under R
;   Competing high-coherence streams (fission, duplication) -> plural partially supported identifications
; === END SECTION 9.10 ===

; === SECTION 9.11: WORKED MICRO-EXAMPLE ===
; Example 9: x = y *C z with sbaseC(x)=10, sC(y)=3, sC(z)=4, glue t=1
;   hC(P) = 3+4+1 = 8, so compression gain = 10-8 = 2
;   IC(P;x) = max(0, (10-8)/10) = 0.2 -- modest but positive pattern intensity
;   If IC(P;y)=0.1, IC(P;z)=0.05 with equal weights wC=0.5:
;     Baseline prediction = 0.5*0.1 + 0.5*0.05 = 0.075
;     SurC = 0.2 - 0.075 = 0.125 positive -> emergent
;     EmerC = 0.125
; === END SECTION 9.11 / END SECTION 9 ===


; === SECTION 10: INFORMATION, UNCERTAINTY, AND INEFFABILITY ===

; === SECTION 10.1: MOTIVATION -- INFORMATION AS OBSERVER-INDEXED BOOKKEEPING ===
; Information and uncertainty cannot be absolute scalars attached to world-states
; Must be indexed by context/observer (Hyperseed-Concept 98, 195)
; Four goals: (i) probabilistic belief, (ii) relate Shannon to distinction-based measures
;   (logical entropy, graphtropy), (iii) make ineffability precise as representational limitation,
;   (iv) clarify potential infinity and infinitesimals in resource-sensitive ontology
; X = finite set of world items (entities, events, situations)
; O = observer/context carrying: (a) family of distinctions about X, (b) belief state over distinctions
; Distinction-making capacity encodable as: partition (indistinguishability classes),
;   binary question set (does x have property P?), or sigma-algebra (measurable events)
; Two items observationally equivalent for O when no available distinction separates them
; Probabilities assigned to recognizable possibilities not unstructured reality
; Remark434: Information measure is property of world-as-carved-by-recognition + weighted-by-belief
;   Russell: bookkeeping devices. Peirce: habit of interpretation belonging to interpreter
; Comparing information across observers requires translation between distinction structures
;   (refinement/coarsening maps, sigma-algebra homomorphisms)
; Shannon entropy presumes fixed alphabet; logical entropy counts expected distinct-pair draws;
;   graphtropy generalizes to indistinguishability/comparability graphs
; Ineffability preview: something ineffable for O because not stably encodable in O's distinction system
;   Not mystical -- structural limitation. Facts may exist in richer meta-description but not
;   measurable or finitely describable in O's sigma-algebra
; Resource-sensitive infinity: infinitary refinement = limit of finite refinements observer can only approximate
;   Infinitesimal differences = in-principle-definable but practically-unresolvable distinctions
; === END SECTION 10.1 ===

; === SECTION 10.2: OBSERVER-INDEXED PROBABILITY SPACES ===
; Def118: Observable events for observer O
;   Event observable to O = predicate on X whose truth value determined at O's resolution
;   SigmaO subset 2^X is sigma-algebra of O-observable events
;   PO: SigmaO -> [0,1] is probability measure (PO(X)=1, countable additivity)
;   Triple (X, SigmaO, PO) = observer-indexed probability space
;   Remark435: sigma-algebra closed under complements and countable unions
;     PO defined only on observer's event-language SigmaO, not arbitrary subsets
;     If A not in SigmaO: not false, just not well-formed observable event for O
;   Intuition: SigmaO = mathematical shadow of observer's question-set
;   Observer = physical sensor suite, agent with finite memory, modeling choice, scientific community
;   Example: gas microstates -- coarse observer measures only temperature/pressure,
;     SigmaO generated by macroscopic equivalence classes. Finer observer has larger SigmaO
;   Remark436: Coarse-graining as loss of distinction
;     Partition piO generates SigmaO: observer represents blocks not individual elements
;     Two microstates in same block = observationally interchangeable
;     Coarse-graining is restriction on formable predicates, not merely lossy summary
;   Remark437: Partition-induced sigma-algebra = crisp indistinction (simplest case)
;     Later generalized to graded and asymmetric indistinction via graphs
;     Finer/coarser comparison: SigmaO1 subset SigmaO2 means O2 informationally at least as fine
;     Inclusion relation = order-theoretic refinement -- supports cross-level model relating
;
; Def119: Paraconsistent evidence annotations
;   EO(A) = (EO+(A), EO-(A)) in [0,1]^2 for A in SigmaO
;   EO+ = degree of positive evidence, EO- = degree of negative evidence
;   No consistency constraint: EO+(A) + EO-(A) > 1 allowed
;   EO not assumed to satisfy EO+(A) = EO-(A^c) -- retains two independent channels
;   Connects to paraconsistent core (Section 3): p-bit evidence over observable events
; === END SECTION 10.2 ===


; === SECTION 10.3: SHANNON INFORMATION, CODING, AND DIVERGENCE ===
; Assume X finite and SigmaO = 2^X (or reduced to finite partition blocks)
; pO(x) := PO({x}) point-mass function. Sum pO(x) = 1
;
; Remark438: Paraconsistent evidence intuition (elaboration of Def119)
;   EO(A) = (0.9, 0.1): strong support, little counterpressure
;   EO(A) = (0.9, 0.9): deep conflict -- simultaneously strongly supported AND opposed
;     Closer to dissonance than ignorance. NOT near-1/2 probability
;   EO(A) = (0.1, 0.1): genuine informational poverty, little evidence either way
;   EO complements PO: PO = betting-odds/action-guiding summary,
;     EO = internal tension profile driving future reorganization
;   Remark439: Two kinds of uncertainty:
;     Ignorance: probabilities near 1/2 and/or low total evidence -> invites exploration/refinement
;     Conflict: simultaneous strong positive and negative evidence -> invites adjudication
;       (seek error sources, reconcile models, split contexts)
;   Remark440: Comparing observers -- two axes:
;     (1) Expressivity: SigmaO1 subset SigmaO2 = O2 informationally finer
;       PO2 restricts to probability on SigmaO1 = forgetting distinctions keeping coherent odds
;     (2) Credence: same SigmaO but different PO/EO = different priors, training, sensor reliability
;     Expressivity = what can be asked. Credence = how uncertainty distributed over askable questions
;
; Def120: Entropy and surprisal
;   Surprisal: sO(x) = -log pO(x) (natural logarithm)
;   Shannon entropy: H(PO) = sum pO(x) sO(x) = -sum pO(x) log pO(x) (in nats)
;   Entropy in bits: Hbits(PO) = H(PO) / log(2)
;   Remark442: Surprisal high when x deemed unlikely by O
;     Entropy = average surprisal under observer own expectations
;     = expected conceptual work to accommodate observation (logarithmic units)
;   Examples: Uniform on N items -> H = log N (maximal). Concentrated on one point -> H = 0
;     Biased coin p=0.9 has lower entropy than fair coin
;   Bridge from belief to description length: optimal codes have expected length about Hbits(p)
;     Connects to effort-based simplicity (Section 8) and pattern intensity (Section 9)
;
; Def121: Cross-entropy and KL divergence
;   Given distributions p, q on X with q(x) > 0 whenever p(x) > 0:
;   Cross-entropy: H(p,q) = -sum p(x) log q(x)
;   KL divergence: DKL(p||q) = sum p(x) log(p(x)/q(x))
;   DKL not symmetric, not a metric -- information-theoretic divergence
;   Cross-entropy = expected code length if world distributed as p but coded for q
;   KL divergence = penalty for mismatch: DKL(p||q) = H(p,q) - H(p)
;   Later used for fidelity/effability: compare target x with reconstructed distribution q = decO(d)
;
; Prop11: Entropy as optimal expected code length (Shannon coding theorem)
;   Among all prefix-free binary codes with codeword lengths l(x) in N:
;   Optimal expected length L*(p) satisfies: Hbits(p) <= L*(p) < Hbits(p) + 1
;   Lower bound: Kraft inequality + KL divergence nonnegativity
;   Upper bound: Shannon-Fano construction with l(x) = ceil(-log2 p(x))
;   Remark444: Entropy is operational not ornamental -- best achievable average compression rate
;     Bridge from belief to effort: shorter codes = less representational work
;     Patterns (Section 9) defined by compressive re-description;
;     this proposition is why compression and probability models are inseparable
;     When speaking of observer-relative simplicity/weakness as optimization principle,
;     this is basic exemplar of how such minima arise
; === END SECTION 10.3 ===


; === SECTION 10.4: MUTUAL AND INTERACTION INFORMATION ===
; (X,Y) pair of random variables on finite sets, joint distribution p(x,y)
;
; Def122: Mutual information
;   I(X;Y) := H(X) + H(Y) - H(X,Y)
;   Equivalently: I(X;Y) = DKL(p(x,y) || p(x)p(y))
;   I(X;Y) >= 0, equality iff X,Y independent
;   Remark447: Intuition -- how much knowing X reduces uncertainty about Y (and vice versa)
;     KL expression: divergence between true joint and independence assumption
;     I(X;Y) = E[log(p(X,Y)/(p(X)p(Y)))] = average surprise relative to independence model
;     Identity: I(X;Y) = H(Y) - H(Y|X) = H(X) - H(X|Y) -- literal entropy drop on conditioning
;     Bounds: 0 <= I(X;Y) <= min{H(X), H(Y)} -- no channel conveys more than total uncertainty
;     Y=X (perfect copy): I(X;Y) = H(X). Independent: I(X;Y) = 0
;     Noisy copy: I decreases as noise increases -- quantitative fidelity measure
;     Invariant under bijective reparameterization of X or Y (depends on dependence structure not labels)
;   Hyperseed use: I(X;Y) = numerical proxy for how many distinctions about Y available via X
;     Reappears in pattern webs and dependency relations (Sections 11, 12)
;
;   Chain rule: I(X; Y,Z) = I(X;Y) + I(X;Z|Y)
;     Information from compound (Y,Z) = part from Y + additional part from Z given Y
;     Conditional mutual information: I(X;Z|Y) = H(X|Y) - H(X|Y,Z) >= 0
;
; Def123: Interaction information (three variables)
;   I(X;Y;Z) := I(X;Y) - I(X;Y|Z)
;   Can be POSITIVE or NEGATIVE (unlike mutual information)
;   Symmetric in entropies: I(X;Y;Z) = H(X)+H(Y)+H(Z)-H(X,Y)-H(X,Z)-H(Y,Z)+H(X,Y,Z)
;   Invariant under permutation of X,Y,Z despite asymmetric definition
;   Remark448: Does Z make X-Y relationship more or less informative?
;     I(X;Y;Z) > 0 iff I(X;Y|Z) < I(X;Y): conditioning on Z REDUCES X-Y association
;       What X,Y share is partly already in Z (redundancy direction)
;     I(X;Y;Z) < 0 iff I(X;Y|Z) > I(X;Y): Z REVEALS hidden X-Y dependence
;       Dependence only visible in triad (synergy direction)
;     XOR example: X,Y independent fair bits, Z=X xor Y. I(X;Y)=0 but I(X;Y|Z)=1
;       Positive interaction info: information present ONLY in triad (pure synergy)
;     Common cause: X=Z, Y=Z. I(X;Y) large but I(X;Y|Z)=0
;       Negative interaction info: apparent dependence fully explained by shared variable (pure redundancy)
;     Single scalar = coarse summary of multi-way dependence structure
; === END SECTION 10.4 ===


; === SECTION 10.5: LOGICAL ENTROPY AND GRAPHTROPY FROM DISTINCTION STRUCTURE ===
; Logical entropy = probability two independent draws fall into different distinction classes
; Measures fraction of distinctions actually made (vs Shannon: expected code length)
;
; Def124: Logical entropy of a partition
;   pi = {B1,...,Bk} partition of X, distribution p on X
;   Block masses: pi_i = sum_{x in Bi} p(x)
;   h(pi,p) := 1 - sum_i pi_i^2
;   Remark451: Intuition -- expected distinguishability under partition pi
;     Not 'how many bits to encode' but 'how often do two random observations differ'
;     Direct companion to Hyperseed distinction primitive (Concept 98)
;     Aligns with Ellerman's development of logical entropy
;   Example: discrete partition (singletons) -> h = 1 - sum p(x)^2 (Gini impurity)
;     Trivial one-block partition -> h = 0 (no distinctions made)
;   Quadratic in p (unlike Shannon which is -p log p)
;     Quadratic forms correspond to pairwise comparison processes
;     (sample two items, check if treated as same)
;   Remark452: sum_i pi_i^2 = probability two iid draws in same block
;     h(pi,p) = probability two iid draws in DIFFERENT blocks = partition makes distinction
;
; Def125: Distinction graphs and graphtropy
;   G = (possibly directed) graph on vertex set X
;   iota_G(x,y) in [0,1] = indistinction weight
;     iota_G(x,y)=1: fully indistinct. iota_G(x,y)=0: fully distinct
;   GT(G,p) := 1 - sum_x sum_y p(x)p(y) iota_G(x,y)
;   Remark453: Double sum = expectation of iota_G(X1,X2) under two independent draws from p
;     Graphtropy asks: sample two items by p, how distinguishable on average?
;     1- flip: higher graphtropy = more expected distinction
;     Direct numerical shadow of observer's distinction structure
;     Works even when structure is graded, context-dependent, non-transitive
;   Examples: iota(x,y)=1[x=y] -> GT = 1 - sum p(x)^2 (logical entropy of discrete partition)
;     iota(x,y)=1 for all pairs -> GT = 0 (everything indistinct)
;   Remark454: Fuzzy and asymmetric cases
;     Crisp+symmetric+transitive iota (equivalence relation) -> partition -> logical entropy
;     Fuzzy and/or asymmetric iota -> graphtropy measures distinguishability without partition
;     Extra generality for modeling minds: indistinguishability can be context-sensitive, graded, non-transitive
;
; Prop12: Reduction to logical entropy
;   Let pi partition X, define iota_pi(x,y)=1 iff same block, 0 otherwise
;   Then GT(G_pi, p) = h(pi, p)
;   Graphtropy is CONSERVATIVE EXTENSION: gains graded/non-transitive without losing classical case
;   Proof: sum_{x,y} p(x)p(y) iota_pi(x,y) = sum_i (sum_{x in Bi} p(x))^2 = sum_i pi_i^2
;     iota_pi is block-constant: 1 on union of Bi x Bi, 0 elsewhere
;     Summing against p(x)p(y) = p-tensor-p mass of diagonal block rectangles
;     Taking 1- yields h(pi,p)
;
; Prop13: Monotonicity under loss of distinction
;   If iota_G(x,y) <= iota_G'(x,y) for all x,y then GT(G,p) >= GT(G',p) for all p
;   Adding indistinction edges or strengthening weights CANNOT increase graphtropy
;   Remark457: Becoming less discriminating -> expected distinguishability cannot go up
;     Formal monotonicity for any sensible distinction-content measure
;     Coarsening = order move, graphtropy moves monotonically with it
;     Echoed later: effability monotone in indistinction regime
;   Proof: pointwise iota_G <= iota_G' implies expectation under G <= under G'
;     Subtracting from 1 reverses nothing (order-preserving affine)
;     Geometric: iota_G = blur kernel over X x X. More blur = less contrast = less graphtropy
;
; Remark449: Observer-relative 'second law' reading
;   Entropy-like quantities depend on which variables tracked
;   If O changes representational partition, induced random variables change and so do H and I
;   'Second law' (monotone entropy increase) must always be read as:
;     For chosen coarse variables, under chosen effective dynamics, typical trajectories -> larger macro-uncertainty
;   Matches Hyperseed perspectivism: same world can have different entropic arrows at different resolutions
;   Coarse-graining typically reduces max achievable mutual information between micro and macro
;   Refining partition can create apparent information flows previously invisible
;   Remark450: Formal caution against contextual regularity -> metaphysical absolute
;     Second law (Concept 164) robust in physics but informational analogs always indexed by:
;       (i) what counts as macrostate, (ii) what counts as effective dynamics
;     Entropy = measure of description as much as measure of disorder
;     Same micro-dynamics supports multiple seemingly competing informational narratives
;     depending on which distinctions treated as salient
; === END SECTION 10.5 ===


; === SECTION 10.5 CONTINUED: THEOREM 10 -- SHANNON LOWER-BOUNDS LOGICAL ENTROPY ===
; Theorem 10: H(p) >= H2(p) = -log S2(p) where S2(p) = sum p(x)^2
;   Proof: r(x) := p(x)^2/S2(p) is distribution. DKL(p||r) >= 0 yields H(p) >= -log S2(p)
;   Hyperseed: coding uncertainty LOWER-BOUNDS expected distinction encounter rate
; === END THEOREM 10 ===
;
; === SECTION 10.6: INEFFABILITY AS OBSERVER-RELATIVE MODALITY ===
; Def126: Observer resources (DO=descriptions, sigmaO=cost, decO=decoding to distributions)
; Def127: FidG(x,q) = sum_y q(y) iota_G(x,y) = expected indistinction target vs reconstruction
; Def128: x is (epsilon,K)-effable iff exists d with sigmaO(d)<=K AND FidG(x,decO(d))>=1-epsilon
;   Five-indexed: observer O, distinction graph G, cost K, tolerance epsilon, language DO
;   Ineffability is structural not mystical -- resource-bounded representational limitation
; === END SECTION 10.6 PARTIAL ===

; === SECTION 10.5 CONTINUED: THEOREM 10 ===
; Theorem 10: H(p) >= H2(p) = -log S2(p), Shannon >= Renyi-2
;   Proof: r(x) := p(x)^2/S2(p). DKL(p||r) >= 0 yields result
;   Hyperseed: coding uncertainty LOWER-BOUNDS distinction encounter rate
; === SECTION 10.6: INEFFABILITY ===
; Def126: Observer resources (DO=descriptions, sigmaO=cost, decO=decoding to distributions)
; Def127: FidG(x,q) = sum_y q(y) iota_G(x,y) -- expected indistinction
; Def128: (epsilon,K)-effable iff exists d with sigmaO(d)<=K AND FidG(x,decO(d))>=1-epsilon
; Prop14: Monotonicity -- more budget or coarser distinctions expand effable set
; Remark469: Ineffability != unknowability. Indexed by interface not by reality
; === SECTION 10.7: GERMS AT INFINITY ===
; Def129: Eventual equality, R_inf = R^N/~ (germs). Ring not field
; Def130: Eventual order, partial not total
; omega=[n], eps=[1/n], omega*eps=[1]. Potential infinity without completed magnitudes
; === END 10.5-10.7 ===

; === SECTION 10.8: SECTION 10 WRAP-UP -- THREE BRIDGES ===
; Bridge 1: Shannon information -- coding-theoretic uncertainty baseline
; Bridge 2: Logical entropy + graphtropy -- uncertainty AS distinction
; Bridge 3: Ineffability -- monotone property relative to observer resources
; === END SECTION 10 ===
;
; === SECTION 11: HIERARCHY, HETERARCHY, AND PATTERN WEBS ===
; 11.1: Two motifs: hierarchy (order-like) and heterarchy (network-like, loops)
; 11.2: Hierarchy as observer-assessed order
; Def131: Graded preorder over quantale V: h(u,u)>=e and h(u,v) tensor h(v,w) <= h(u,w)
;   Boolean quantale -> crisp hierarchy. Lawvere -> metric. P-bit -> paraconsistent
; === END 11.1-11.2 PARTIAL ===

; === SECTION 10.8: SECTION 10 WRAP-UP -- THREE BRIDGES ===
; Bridge 1: Shannon information -- coding-theoretic uncertainty baseline
; Bridge 2: Logical entropy + graphtropy -- uncertainty AS distinction
; Bridge 3: Ineffability -- monotone property relative to observer resources
; === END SECTION 10 ===
;
; === SECTION 11: HIERARCHY, HETERARCHY, AND PATTERN WEBS ===
; 11.1: Two motifs: hierarchy (order-like) and heterarchy (network-like, loops)
; 11.2: Hierarchy as observer-assessed order
; Def131: Graded preorder over quantale V: h(u,u)>=e and h(u,v) tensor h(v,w) <= h(u,w)
;   Boolean quantale -> crisp hierarchy. Lawvere -> metric. P-bit -> paraconsistent
; === END 11.1-11.2 PARTIAL ===

; === SECTION 11.2 CONTINUED: GRADED PREORDERS AND OBSERVER-ASSESSED HIERARCHY ===
; Remark480: Graded preorder answers degree question not yes/no. V={0,1} with AND/OR -> crisp preorder
;   V=[0,1] with mult/max -> confidence. Longer chain decreases confidence, multiple routes increase it
; Remark481: Thin V-categories. Graded preorder = thin V-enriched category (at most one hom-value per pair)
;   Thinness records best available grade, not internal justification structure
;   Pattern webs later make justifications explicit; graded preorder = reachability/strength summary
; Def132: Observer-assessed hierarchy. Fix observer O. hO: UxU -> VO for quantale VO matching O regime
;   P-bit case: hO(u,v) = (h+,h-) encodes positive AND negative evidence for u above v
;   Freedom to choose VO: different observers treat same signals as probabilities, costs, plausibilities, bipolar
;   Simultaneous large h+ and h- = genuine tension (competing heuristics) without forced resolution
; Remark482: Hierarchy not in-the-world as bare relation but in triad (world, observer, respect-of-comparison)
;   Multiple coexisting hierarchies without contradiction. Context change = hO change not inconsistency
; Remark483: Values and higherness -- three equivalent stances:
;   Order-first: hO directly as priority. Value-first: valuation nu then hO from nu(u)>=nu(v)
;   Constraint-first: hO from model class (simplest causal explanations = higher = more compressive)
; === SECTION 11.3: SYSTEMIC HIERARCHY VIA MODELS OF DYNAMICAL SYSTEM ===
; Def133: Systemic hierarchy (model-induced). D=dynamical system, Proc(D)=processes
;   Symbol domain S, partial order <=S on S, interpretation map phi: Proc(D)->S
;   D manifests systemic hierarchy relative to (S,<=S,phi) if phi faithful for observer purposes
;   Hierarchy appears AFTER representation. Observer selects processes, then ordering becomes meaningful
; Remark485: Plural hierarchies as plural models. Control: nested controllers, higher=override
;   Explanation: macro-regularities, higher=more compressive. Different phi and <=S both right for distinct purposes
; Remark486: Fuzzy/paraconsistent systemic hierarchy. <=S can be graded preorder hS: SxS -> V
;   V=[0,1]^2 -> bipolar evidence for dominance. Postpone commitment to crisp order
; Remark487: Same D admits many hierarchical models depending on observer values, abstraction level, control vs observation
; === SECTION 11.4 BEGINS: SUBPATTERN HIERARCHY ===
; Def134: Compositional subpattern. Domain X, combination op *, pattern-representers P
;   y <= x when y is compositional subpattern of x (y combinable with something to form pattern in x)
; === END 11.2-11.4 PARTIAL ===

; === SECTION 11.4 CONTINUED: SUBPATTERN HIERARCHY DETAILS ===
; Def134 continued: hsub(p,q) := sup_{r in X} Pat(p*r; q) -- graded subpattern strength
; Remark489: p subpattern of q means p is reusable piece in constructing pattern fitting q
;   Example: strings with concatenation. Example: feature-bundle composition
; Remark490: Two readings -- Constructive (q built from p) and Explanatory (p compresses/predicts q)
; Prop15: Subpattern is preorder under associativity. * associative with identity e, Pat(p*e;p) nontrivial
;   Proof: Reflexivity via identity element. Transitivity via reassociation (p*r1)*r2 = p*(r1*r2)
; Remark491: Preorder = crisp thin V-category. Heuristic subpatternhood inherits formal stability
; Remark493: Antisymmetry requires observer-relative pattern identity. Preorder then quotient by equivalence
;   p~q iff p<=q and q<=p. Different observers choose different ~. Gauge freedom in pattern identity
; === SECTION 11.5: HETERARCHY ===
; Def135: Heterarchy on nodes U = directed weighted digraph G=(U,E,w) with multiple paths and directed cycles
;   Weights in quantale V. Path composition via monoidal product, competing routes via join
; Remark494: Heterarchy = formal acknowledgment influence is rarely single chain. Robustness and conflict coexist
; Remark495: Heterarchy as non-thin enriched category. Multiple morphisms = different explanatory routes
;   Thin collapse via supremum over routes = convenient but forgets internal pluralism
; Def136: Cycle mass Cyc(G) := max product of weights around directed cycle. Measures feedback strength
; Remark496-497: Cycle mass is toy index. Habit dynamics (Sec12) preferentially reinforce existing loops
; === SECTION 11.6 BEGINS: PATTERN WEBS ===
; Def137: Pattern profile. Intensity map I:PxX->[0,1]. Fx(p):=I(p,x) fuzzy set of patterns for entity x
;   Context-dependent: different observers induce different profiles for same x
; === END 11.4-11.6 PARTIAL ===

; === SECTION 11.6 CONTINUED: PATTERN WEBS ===
; Remark498: Pattern profile = fingerprint of entity in pattern vocabulary. Fx vector in [0,1]^P
; Def138: Pattern-based pseudo-metric. dP(x,y) := D(Fx,Fy). Geometry is observer-relative
; Def139: Weighted pattern web from distance via monotone kernel kappa. Threshold/kNN/full graph
; === SECTION 11.7: PATTERN WEBS AS FREE V-CATEGORIES ===
; Def140: Path composition in V-graph. Sequential via tensor, parallel via join
; Theorem11: Free V-category on V-graph. Path-closure g-hat satisfies identity and composition
;   Indirect routes can dominate weak direct links. Canonical completion into compositional reasoning
; Remark507-508: Path closure = hinge between static web and inferential substrate
; === END 11.6-11.7 ===

; === SECTION 11.6 CONTINUED: PATTERN WEBS ===
; Def138: Pattern-based pseudo-metric. dP(x,y) := D(Fx,Fy). Geometry is observer-relative
; Def139: Weighted pattern web from distance via monotone kernel kappa
; === SECTION 11.7: PATTERN WEBS AS FREE V-CATEGORIES ===
; Def140: Path composition in V-graph. Sequential via tensor, parallel via join
; Theorem11: Free V-category on V-graph. Path-closure g-hat satisfies identity and composition
; === SECTION 11.8: MULTI-RESOLUTION TRANSFORMS ===
; Def141: Resolution maps with sup pushforward (left Kan extension style)
; Prop16: Coarse-graining monotonically increases weakness
; === SECTION 11.9: WRAP-UP ===
; Four reconstructions: hierarchy, subpattern, heterarchy, pattern web -- unified by compositionality
; === SECTION 12 BEGINS: HABITS, SELF-WEAVING WEBS, MORPHIC RESONANCE ===
; HC189 tendency to take habits, HC188 tendency to reverse habits
; HC168 self-weaving webs, HC115 morphic resonance/anti-resonance
; === END 11.6-12.0 ===

; === SECTION 12.1: FROM PROBABILITY PHRASING TO V-VALUED DYNAMICS ===
; Def142: P-bit occurrence evidence. s(p)=(s+,s-) in [0,1]^2. Scalarizations pi_pos and pi_net
; Def143: Observer-indexed occurrence process. Sequence s0,s1,... with scalar propensity pt(p):=pi(st(p))
; Def144: Tendency to take/reverse habits. PreT vs PostT expectation gap over patterns and times
;   Habit-taking: E[PostT-PreT] > 0. Habit-reversal: same < 0. Meta-statistical time-directional bias
; Lemma3: Monotone propensity series imply habit-taking. Antitone imply reversal
;   Remark524: Forward connection -- Prop17 will show update operators are monotone
; === END SECTION 12.1 ===

; === SECTION 12.2: V-RELATIONS AND HABIT UPDATE OPERATORS ===
; Def145: V-valued reinforcement relation A: PxP->V. How strongly p supports q
; Def146: Relational image (A*s)(q) := join_{p} A(p,q) tensor s(p). Quantale matrix-vector multiply
; Def147: Persistence/decay scalar d. (d.s)(p) := d tensor s(p). d=e perfect memory, d<e forgetting
; Def148: Habit dynamics Upd(s) := ut join (d.s) join (A*s). Three sources: input, persistence, web propagation
; === END SECTION 12.2 ===

; === SECTION 12.3: SELF-WEAVING WEBS AND AUTOCATALYTIC CLOSURE ===
; Prop17: Monotonicity of habit update. Upd is monotone in s, u, and A (pointwise order)
;   Proof: Each component built from join, tensor, join-over-P. All monotone in quantale. Composition of monotone maps is monotone
;   Remark544: Minimal coherence condition. Stronger support/couplings cannot decrease next state
;   Enables Knaster-Tarski/Kleene fixed-point reasoning. Comparative statics unambiguous
;   Remark545: Visual intuition -- channels only transmit/accumulate. No subtractive steps
; Def149: One-step closure operator. ClA(s) := s join (A*s). Inflationary: adds one round of propagation
;   Remark546: Seed enriched by what web can grow in one step. Join keeps original plus consequences
; Def150: Iterated closure and Kleene star
;   ClA^0(s) := s. ClA^(n+1)(s) := ClA(ClA^n(s)). Ascending chain
;   ClA^omega(s) := join_{n>=0} ClA^n(s). Limit of iterated closure
;   A^0 := I (identity). A^(n+1) := A^n composed A. Kleene star A* := join_{n>=0} A^n
;   Remark547: A^n = n-step reinforcement. A* = all finite paths. Same as Kleene algebras in quantale language
; Theorem12: Closure as least fixed point with explicit A* form
;   1. Chain ClA^0(s) <= ClA^1(s) <= ... ascending with join ClA^omega(s)
;   2. ClA^omega(s) is least fixed point of ClA above s
;   3. ClA^omega(s) = A* ? s. Explicit propagation form
;   Proof: Inflationarity gives ascending chain. Knaster-Tarski gives least fixed point. Unfolding recurrence collects A^k contributions
;   Remark548: Self-weaving as fixed-point phenomenon. Closing again adds nothing new
;   Remark550: Essential facts: completeness of V^P, monotonicity+inflationarity of ClA, distributivity of tensor over joins
;   Remark551-552: A* ? s = total downstream closure. Walk-sum semantics. Cycles = feedback loops folded into star
; Def151: Autocatalytic (theta-autocatalytic) support
;   Nonempty S subset P is theta-autocatalytic if exists s:P->V with s(p)>=theta for all p in S
;   and (A*s)(p)>=theta for all p in S. Self-production: web alone regenerates threshold support on S
; === END SECTION 12.3 ===

; === SECTION 12.4: MORPHIC RESONANCE AND ANTI-RESONANCE AS CROSS-CONTEXT COUPLING ===
; Def152: Family of contexts. Index set L. Each l has pattern class Pl, reinforcement Al, decay dl, input ul,t
; Def153: Morphic coupling kernel K_{l0->l}: Pl0 x Pl -> V. Cross-context quantale transport
; Def154: Morphic resonance dynamics. sl,t+1 = ul,t join dl.sl,t join Al*sl,t join join_{l0!=l} K*sl0,t
; Def155: Anti-resonance via p-bit negation before transport. neg swaps v+,v-. Inhibitory channel
; === END SECTION 12.4 ===

; === SECTION 12.5: STABILITY, AMPLIFICATION, AND DECAY ===
; Def156: Scalar upper bound norm-inf for p-bit quantale V=[0,1]^2. max of v+,v-
; Theorem13: Decay criterion. rho := max of norm-inf d, norm-inf A. rho<1 implies geometric forgetting to 0
; Prop18: Driven closure with d=e, constant u. Ascending chain to stable attractor s-inf = u join A*s-inf
; Key bridge: Theorem13 gives habit-reversal, Prop18 gives habit-taking
; === END SECTION 12.5 ===

; === SECTION 12.6: WORKED MICRO-EXAMPLE -- MORPHIC RESONANCE AND SELF-WEAVING ===
; Example12: Two contexts C1 source, C2 target. Two patterns p seed, q downstream. P-bit V=[0,1]^2
; C1 state: s1-p = 0.9,0.1 strong positive. s1-q = 0.1,0.1 neutral
; C2 initial: s2-p = 0.2,0.7 leans against p. s2-q = 0.1,0.1 neutral
; Morphic coupling K = 0.6,0.2. Asymmetric channel strengths for pos vs neg evidence
; Step 1 morphic injection: K tensor s1-p = 0.54,0.02. s2-p becomes join of 0.2,0.7 and 0.54,0.02 = 0.54,0.7
; KEY: Paraconsistent both-sides state. Positive raised to 0.54, negative unchanged at 0.7
; Internal reinforcement in C2: A2-p-q = 0.9,0.1 and A2-q-p = 0.8,0.1. Mutual reinforcement loop
; Step 2 self-weaving propagation through internal web creates ascending chain
; Remark580: Distributivity of tensor over joins justifies A star fixed point. Scott-continuity
; Remark581: Least fixed point and driven closure. s-inf is smallest stable support compatible with u and A
; === END SECTION 12.6 ===

; === SECTION 12.7: NOTES AND BRIDGES ===
; Attention as gating field wt rescaling A and ut. Effort as complexity constraint on subweb
; K learned from paraconsistent interference scores. High coherence => stronger coupling
; Reality-systems: same coupled-web formalism with L indexing reality-systems
; === END SECTION 12.7 ===

; === SECTION 13: MIND, REPRESENTATION, AND PERCEPTION ===
; Hinge between static and active sides of formalism
; Def157: Process = triple T,Sigma,delta. System = inter-producing directed multigraph
; Def158: Mind = system with registration interface, representation space R, reference relation RefC, update rule
; === END SECTION 13 START ===

; === SECTION 13.1: PATTERN RECOGNITION PROCESS ===
; Def159: Pattern recognition process. Fix context C, candidate patterns PC, intensity map IntS,t: PC -> V
;   Process Y recognizes entity X in aspect C if exists nonempty PX,C subset PC such that:
;   1. Alignment: IntY,t of P <= IntX,t of P for all relevant t
;   2. Learning: IntY,t of P is nondecreasing in t with at least one strict increase
;   Remark587: PC is repertoire from context C. V supplies graded scale. IntS,t is degree of embodiment
;   Recognition = mirroring patterns of X with temporal direction. Not static coincidence but historical acquisition
;   Remark588: Combined with habit dynamics Section 12 gives explicit perceptual learning model
;   Remark589: PX,C encodes what counts as evidence about X. Misattribution when alignment fails
; === SECTION 13.2: CONTEXTS AND ASPECTS ===
; Def160: Context and aspect extraction. Ctx = small poset of contexts. C refines-or-equal D
;   aspC: U -> UC. If C refines-or-equal D then forgetful map piD->C satisfying aspC = piD->C composed aspD
;   Remark590: Ctx bookkeeps ways of carving reality. aspC is projection forgetting what C ignores
;   Remark591-594: Coherent composition of forgetful maps. Small for set-theoretic safety. Quotient reading
; Def161: Contextualized groupings. G|C := set of x|C for x in G. Lifting aspect extraction to sets
;   Remark595-597: Monotone under subset. Union distributes. Intersection may shrink -- context erases distinctions
; === SECTION 13.3: REGISTRATION, SENSORY SYSTEMS, PERCEPTION ===
; Def162: Registration. Fix context C and equivalence relation simC on UC
;   X registers entity A at time t if exists A-prime with A-prime|C simC A|C and A-prime|C becomes pattern in X
;   Witnessed by P in PC with IntX,t of P above threshold theta and RefC of P,A|C nontrivial
;   Registration is weaker than perception. Compatible with vagueness. Separates impact from representation
; === END SECTION 13.3 ===

; === SECTION 13.4: REPRESENTATION AS REFERENCE PLUS PATTERN INHERITANCE ===
; Def163: Sensory system. Coherent subsystem S of X such that most registrations have referents in Uext
;   and update dynamics driven primarily by coupling to Uext. Functional not anatomical coherence
;   Remark599: Not metaphysically outside-facing but pragmatically exogenous under chosen decomposition
; Def164: Perception. Mind M perceives entity A at time t in context C if:
;   1. M registers A at time t -- Def162
;   2. Registration causally triggers emergence of representation token R in R with RefC nontrivial
;   Perception = registration that causes representation. Causal bridge from world-impact to internal content
;   Remark600: Mere registration can be fleeting. Perception organizes representational economy
; Prop19: Perception implies registration. Immediate from Def164 item 1
; Def165: Pattern signature in aspect. SigC of X maps basis BC to V via IntX of P. Aspect-relative fingerprint
; Def166: Strong pattern inheritance. A inherits from B in aspect C if SigC of A|C leq SigC of B|C pointwise
;   One-sided: inheritance means A has no more of each basis-pattern than B. Simplification not invention
; Def167: Representation in aspect. A represents B in aspect C if:
;   1. Reference: RefC of A, B|C nontrivial -- aboutness
;   2. Inheritance: A|C inherits patterns from B|C per Def166
;   Remark605: Re-presentation. Reference ensures aboutness, inheritance ensures structured similarity
; Prop20: Transitivity of representation under compositional reference. Reference composes plus pointwise leq transitive
; === END SECTION 13.4 ===

; === SECTION 13.5: SEMIOTIC MODES -- ICON, INDEX, SYMBOL ===
; Peircean triad as special cases of representation distinguished by which aspect C is preserved
; Not three disjoint kinds but three recurring emphases. Mode depends on analytic choice of aspect
; Def168: Sensory, spatiotemporal, and relational aspects. Three marked sub-posets of Ctx:
;   Ctxsens sensory domains, Ctxst spatiotemporal positioning, Ctxrel relational-network domains
;   Need not be disjoint. Real systems rarely separate cleanly. Vocabulary for which invariances appealed to
; Def169: Icon. A is icon for B if exists sensory context C in Ctxsens such that A represents B in aspect C
;   Preserves sensory-pattern structure. Photograph, hummed melody, spectrogram, circuit diagram
;   Reduces iconicity to general representation plus aspect restriction. Degrees and failures statable
; Def170: Index. A is index for B if exists spatiotemporal context C in Ctxst such that A represents B in aspect C
;   Preserves spatiotemporal positioning. Deictic gesture, memory address, smoke-fire trace
;   Reference with minimal inherited content. Stable handle elaborated later by adding aspects
; Def171: Symbol. A is symbol for B if exists relational context C in Ctxrel such that A represents B in aspect C
;   Additional requirement: participates in combinational system Section 9. Composable and recombinable
;   Conventionality as consequence: relational structure preserved, many tokens could fill same node
;   Connects semiotics to computation. Supports systematic inference and counterfactual reasoning
; Remark613: Hybrid tokens common. Labeled photograph is both icon and symbol
;   Agents move between modes by changing which aspect C treated as primary
; === SECTION 13.6: SOGGY PREDICATES AND PARACONSISTENT TRUTH ===
; Bridge between fuzzy truth values and probabilistic semantics grounded in observations
; Def172: P-bit-valued predicate. F: X -> [0,1]^2. F-plus and F-minus are degrees of positive and negative evidence
;   Paraconsistent: high positive and high negative simultaneously without triviality
;   Conflict = min of F-plus, F-minus. Ignorance = 1 - max of F-plus, F-minus
; Def173: Soggy predicate. Fix finite observation set O with weights wo summing to 1
;   Each observation o yields evidential evaluation eo: X -> [0,1]^2
;   Soggy predicate F of x = weighted sum of wo times eo of x componentwise
;   Convex combination: F lies in convex hull of per-observation evaluations
;   Grounds fuzzy-paraconsistent truth in observation model. Canonical evidence combination
; === END SECTION 13.6 ===

; === SECTION 13.6-13.8 COMPLETION ===
; Prop21: Probabilistic semantics as special case under complementarity
; Remark623: Thresholding policies -- accept reject undecided
; Example13: One referent B with icon index symbol tokens in mind M
; Section 14 prediction, Section 15 attention, Sections 16-17 self-models
; === END SECTION 13 ===

; === SECTION 14: PREDICTION, ATTRACTION, CAUSALITY, AND CONTROL ===
; 14.1 From patterns to forecasts and interventions
; Remark627: Passage from patterns to agency is change of grammatical tense not metaphysical jump
;   From describing what is coherently present to what is expected to become present
;   Same representational web supports recognition and transition modeling
;   Action = internally available distinction whose enactment changes accessible contexts
; Three roles: Prediction = inference under uncertainty, Control = selection under constraints
;   Causality = bridge making control non-magical, systematic difference beyond co-occurrence
; Key move: dependence notions explicitly differential
;   What matters is how different P of B given A is from P of B given not-A
;   Packaged as attraction, predictive implication, predictive attraction
; Remark628: Differential stance philosophically modest but practically decisive
;   Agent action matters only insofar as it tilts odds relative to counterfactual baseline
; 14.2 Event types, timelines, paraconsistent occurrence data
; Def174: Event types E and event tokens A@t. Negation operator A maps to not-A
;   Both A@t and not-A at t may carry substantial evidence
; Def175: Paraconsistent occurrence evidence EO maps E cross T to unit-square
;   EO-plus = degree of positive evidence, EO-minus = degree of negative evidence
;   No consistency constraint imposed. May have EO-plus + EO-minus greater than 1
; Def176: Derived diagnostics -- conf = min of p q, gap = 1 - max of p q, bal = abs of p - q
;   conf measures conflict, gap measures indeterminacy, bal measures balance

; === SECTION 14.3: PREDICTION AND ATTRACTION ===
; Def177: Plausibility projection pi -- conservative extension of probability
; Def178: Predictive conditional operator -- neutral about computation method
; Def179: Attraction -- differential predictive influence, leverage not correlation
; Prop22: Boundedness, negation antisymmetry, independence gives zero
; Def180: Predictive implication and predictive attraction, PAtt equals Att
; === END SECTION 14.3 ===

; === SECTION 14.4: SEQUENTIAL AND PARALLEL TEMPORAL COMPOSITION ===
; Remark666: Minds reason about chains and bundles, not isolated one-step predictions
;   Quantales provide compact algebra: tensor aggregates along sequence, join across alternatives
; Def181: Two-step predictive composition via relational composition
;   R compose R-prime of A C = join over B of R of A B tensor R-prime of B C
;   Sum over intermediates, multiply along edges -- generalized to p-bit quantale
; Remark668-670: Algebraic content behind SequentialAND operator
;   Join aggregates over intermediate events, tensor aggregates evidence across chain
; 14.4.2: Worked schematic -- fetch ball sequence as composite prediction
; === SECTION 14.5: CAUSALITY ===
; Causality = attraction plus temporal precedence plus simplicity bias
; Four ingredients jointly necessary: temporal precedence, surprising extensional dependence,
;   intensional property-level connection, simplicity-weakness bias
; Def182: Extensional predictive attraction PAttext = PAttO,Delta on event type level
; Def183: Property events -- pattern p present in A with intensity PropO of A of p
; Def184: Intensional predictive attraction PAttint = weighted average over property pairs
;   Bridges pattern-as-compression view Section 9 with causal judgments
; === END SECTION 14.5 PARTIAL ===

; === SECTION 14.5.2: CAUSAL IMPLICATION ===
; Def185: Causal implication strength CImp = lambda-mix of extensional and intensional attraction
;   times temporal precedence indicator. sigma rescales signed attraction to 0,1
;   Sum form: permissive, one channel can rescue the other
;   Product form: severe, both channels must cohere
; Remark694-706: lambda as trust-in-statistics vs trust-in-structure tradeoff
;   Barometer example: high extensional attraction but low intensional if no mechanistic link
;   Common cause settings: intensional attraction biases toward exposing intermediates
;   Temporal precedence as hard gate not soft preference
; === SECTION 14.5.3: WEAKNESS-BIASED CAUSAL MODEL SELECTION ===
; Def186: Weak causal parent selection -- Score = Fit + eta times Weak
;   Fit rewards predictive adequacy, Weak rewards simplicity-compressibility
;   Regularized model selection: prefer fewer special-case distinctions
; Remark707-712: Russellian simplicity move formalized via quantale weakness measures
;   Smoke alarm example: smoke as simpler parent than long conjunction of rare conditions
;   Weakness not merely small cardinality but complexity of description
;   CImp as pairwise screening signal, weakness-selection resolves multivariate redundancy
; === END SECTION 14.5 ===

; === SECTION 14.6: CONTROL, CONTROL HIERARCHIES, PERCEPTUAL HIERARCHIES ===
; Def187: Control strength CtrlO,Delta of A to G = CImpO,Delta of A,G
;   Reuses causal implication restricted to action antecedents. Agency = organizational stance
;   Actions as doable event types, goals as desirable event types
; Remark715-717: No new scalar invented for control. Refinements carry over automatically
;   Graded control allows partial and contested control. Sequential policies via composite events
; Def188: System-level control -- U controls V if some action in U has strong CImp toward some event in V
;   Existential quantifier captures minimal claim. Threshold is modeling choice
; Remark718-720: Asymmetry natural. Bidirectional = feedback coupling. Agnostic about stability
; Def189: Control hierarchy -- partial order on modules aligned with asymmetric control relations
;   Heterarchical organization allowed. Incomparable pairs and local loops accommodated
; Def190: Perceptual hierarchy -- control hierarchy where control events are pattern recognition
;   Perception as special case of control: higher levels constrain what patterns lower levels register
;   Top-down influence as directional constraint not mere correlation
; Remark724-726: Perception is active control not passive data intake
;   Aligns with predictive-processing and active-inference. Internal action in hypothesis space
; === SECTION 14.7: PLANNING AND OPTIMAL CONTROL INTEGRATION HOOKS ===
; Event calculus hook: Happens, Initiates, Terminates, HoldsAt with p-bit evidence values
;   Planning as evidential optimization over temporally composed causal implications
;   Sequential composition operator matches temporal compositionality of planning
; Remark727: Interface point -- classical event calculus syntax reused with p-bit semantics
; === END SECTION 14 ===

; === SECTION 15: ATTENTION AND COGNITIVE SYNERGY ===
; 15.1 From control to attention
; Attention = structured management of finite-capacity bottleneck
;   Not optional add-on to control but mechanism by which control becomes realizable
;   Allocation of limited resources across recognition inference simulation action
;   Attentional focus = highly concentrated allocation
;   Self-reflective attention = system self-model inside focus -- key to reflective consciousness Sec17
; Remark729: Agency is not just possessing good model but deciding which parts to refine now
;   Resource-theoretic bounded rationality in Hyperseed vocabulary of patterns and genenergy
;   Attention bridges can-in-principle of prediction-control and can-right-now of finite mechanism
; Remark730: Effort as accounting unit allowing different internal activities to be compared
;   Updating beliefs running simulations searching memories selecting actions -- single bounded budget
; Remark731: Target of attention vs mode of attention
;   Target = which patterns selected. Mode = how selection enforced
;   Hyperseed abstracts away implementation, treats attention as functional role
; 15.2 Genenergy budgets and attention measures
; Def191: System S with modules M, patterns P, association map Assoc, genenergy expenditure g
;   gt of i = genenergy spent by module i at time t. Gt = sum over modules
; Def192: Pattern-level attention via weighting functions wi
;   Attnt of p = sum over modules of gt times wi of p
;   Normalized attention distribution alpha-t of p = Attnt of p over Gt
;   Lives on probability simplex -- share of resources comparable across times and systems
; Remark736-738: Soft assignment of module work to patterns
;   Planning module considering two subgoals splits genenergy proportionally
; === END SECTION 15.1-15.2 ===

; === SECTION 15.2.2-15.3: ATTENTIONAL FOCUS, SELF-REFLECTIVE ATTENTION, ATTENTION AS BOUNDED CONTROL ===
; Def193: Attentional focus at level theta,k -- subset Ft of at most k patterns carrying mass at least theta
;   Equivalent to top-k share of nonincreasing rearrangement exceeding theta
;   Formalizes mind is usually mostly doing one thing with few side computations
; Remark741-745: Parameters theta,k tune mostly and few. Scale-free, only relative shares matter
;   Split attention = two clusters each salient but neither alone clears high theta for small k
;   Basic monotonicities: increasing theta or decreasing k makes test strictly harder
; Def194: Self-reflective attention -- attention mass on self-model patterns Pself exceeds theta-self
;   Focused self-reflective attention: Ft intersects Pself nonempty
;   Self-model in foreground vs merely implicitly present
; Remark746-748: Routing not metaphysical privilege. Error-monitoring as self-model attention
;   I noticed I was confused as formal correlate of self-model patterns entering focus set
; 15.3: Attention as bounded control policy
; Def195: Internal update actions U -- refine distinction, update intensity, query memory, simulate, reweight
;   Each action has genenergy cost. Attention treats what to think about next as first-class control variable
; Remark749-752: Attention as internal intervention not passive light. Heterogeneous operations unified
;   Cost function as capacity consumption not only time budget
; Def196: Attention policy with budget -- map from internal state to distribution over update actions
;   Feasibility constraint c of u at most Bt. Bounded control problem not purely epistemic
; Remark753-757: Attention failure = selecting locally feasible but globally unhelpful updates
;   Shallow vs deep reasoning under time pressure as budget constraint on policy
; Def197: Priority scores from predictive attraction -- Prio of p = max over goals of attraction
;   Pattern prioritized if its presence makes significant difference to goal expectations
; Prop23: Entropy-regularized attention allocation
; === END SECTION 15.2.2-15.3 ===

; === SECTION 15.4: VARIETIES OF KNOWLEDGE AS TYPED PATTERN STRUCTURES ===
; Knowledge as family resemblance notion: multiple distinct types play different roles
; Def198: Knowledge type T = carrier set KT, semantics map SemT, update operator UpdT, interface
;   Store is structured substrate not mere container. Items behave as typed pattern constraints
;   Each type has characteristic generalization, evidence forms, and participation in perception-action loops
; Remark770-773: Update operator explicit -- UpdT maps KT cross ET to KT
;   Different types have different evidential input spaces ET and different invariants under update
;   Types mark distinct update dynamics and failure modes, enabling cross-type synergy
;   Interface component is where cognitive synergy becomes operational: accessors, translators, gating
;   SemT bridges compact stored token to large set of permitted pattern instantiations
; 15.4.1 Declarative knowledge
; Def199: Declarative knowledge -- valuation Kdec maps language L to unit-square p-bit evidence
;   Linguistically expressible pattern beliefs with separate positive and negative evidence
;   Conflict = high support and high refutation -- natural trigger for targeted information gathering
; Remark774-777: L may be relational templates not just natural language
;   Evidence update preserves separation of positive and negative support
;   Vague predicate example: room is quiet at 0.7 positive 0.4 negative
; 15.4.2 Procedural knowledge
; Def200: Procedural knowledge -- triple of context C, procedure pi, goal G with evidence value
;   If in context C doing pi tends to achieve G. Broadly: external situation, internal state, or both
; === END SECTION 15.4 PARTIAL ===

; === SECTION 15.4.2-15.4.5: REMAINING KNOWLEDGE TYPES ===
; Remark779-781: Procedural update driven by rollouts, trial-and-error, imitation, counterfactual evaluation
;   Attention determines which trials to run, which failures to analyze, which context splits worth complexity
;   Example: slippery ground context, walk slowly procedure, reach destination goal
; 15.4.3 Sensory knowledge
; Def201: Sensory knowledge -- finite exemplar set with embedding phi into metric space Y
;   Discrimination by thresholding distances. Capacity-limited so forgetting is normal update dynamic
; Remark782-786: Abstracts template matching, nearest-neighbor, metric learning, associative memories
;   Embedding phi can be fixed, learned, or attention-modulated. Tradeoff: improve phi vs manage exemplars
; 15.4.4 Attentional knowledge
; Def202: Attentional knowledge -- kernels Katt of Y given X,G in paraconsistent V
;   Regularities of productive attention shifts. Knowledge about own search procedure
;   Targets X can be pattern sets, modules, or explicit questions
; Remark787-791: Conditional kernel many-to-many and goal-gated. Internal learned operator-selection map
;   Debugging example: shifting to minimal reproducible example as learned attentional habit
;   Attentional knowledge orchestrates updates in other knowledge types -- clearest locus of cognitive synergy
; 15.4.5 Intentional knowledge
; Def203: Intentional knowledge -- Kint of G1 given G,C in V. Goal specialization regularities
;   Learned mapping of which goal refinements appropriate in which contexts
; Remark792-795: Goal system as hypergraph with context-sensitive refinement edges
;   Health example: winter context triggers vitamin D subgoal with mixed evidence
; Remark796-799: WHY MULTIPLE TYPES -- different update dynamics and failure modes
;   Procedural robust without explainable, declarative communicable without actionable
;   Attentional guides search without articulable justification
;   Plurality is structural response to finitude. Synergy = disciplined translation between types
;   Cross-type couplings: attentional selects declarative store, declarative proposes attention targets,
;     procedural seeds deliberate reasoning, intentional reshapes success criteria
; === SECTION 15.5: COGNITIVE SYNERGY AS CROSS-TYPE WEAKNESS IMPROVEMENT ===
; Remark800: Whole more than sum of parts becomes operational when cross-type translations yield new compressions
;   Compression lifted to architectural level -- enabled by cross-type interaction not single engine
; 15.5.1 Usefulness of learning algorithm for knowledge type
; Def204: Learning algorithms indexed by knowledge type. Alg of T = family of update algorithms appropriate to T
;   Not every method appropriate for every store. Cross-type communication = outputs of one become inputs to another
; === END SECTION 15.5.1 ===

; === SECTION 15.5.2-15.5.5: FORMAL COGNITIVE SYNERGY ===
; Def205: Usefulness -- algorithm A useful for type T if repeated UpdT,A increases goal achievement probability
;   Pragmatic teleological criterion not elegance. Bounded rationality compatible
; Remark803-804: Memory consolidation useful even if occasionally strengthens false beliefs
;   Paraconsistent setting accommodates usefulness as expected-value not global consistency
; 15.5.2 Explanations weakness and contrivance cost
; Def206: Explanations with adequacy Fit in 0,1 and weakness Weak in 0,1
;   Contrivance cost Con = negative log Weak. Fewer distinctions = more general = less brittle
;   Weakness is structured quantale notion not mere vagueness
; Remark805-809: Con behaves like description length. Pareto frontier of Fit vs Con
;   Weakness improvement = comparable fit with lower contrivance via cross-type translation
; Def207: Best achievable contrivance ConStar of T at threshold tau
;   Minimal contrivance needed to reach fit tau using knowledge types T
; 15.5.3 Synergy as strict subadditivity of contrivance
; Def208: Cognitive synergy between T1 T2 at level tau iff ConStar of union strictly less than sum
;   Synergy gain Sigma = positive part of sum minus joint. Always nonnegative
; Remark812-814: Letting knowledge sets interact yields same adequacy with less contrivance
;   Declarative rule lets procedural learning reduce exploration drastically
; 15.5.4 Sufficient condition: monoidal compositionality of weakness
; Def209: Multiplicative weakness model -- Weak of E1 tensor E2 geq product of Weaks
;   Composing explanations does not force additional distinctions beyond parts
; Prop24: Subadditivity of contrivance under multiplicative weakness
;   No penalty for combining knowledge types. Synergy gain well-defined and nonneg
; Remark817-821: Sanity check connecting architecture to algebra of weakness under composition
;   Logarithm converts multiplicative weakness to additive cost -- why log was chosen
;   Attention determines whether compositions actually realized in time
; 15.5.5 When does synergy become strict
; Def210: Cross-type emergent compression -- explanation in joint space not decomposable
;   Shared structure representable once jointly but redundantly in each type separately
; === END SECTION 15.5.5 ===

; === SECTION 15.5.5-15.5.6: EMERGENT COMPRESSION PROPOSITIONS AND BUDGETED SOLVABILITY ===
; Prop25: Emergent compression implies positive synergy gain Sigma > 0
;   Witness E whose contrivance beats every separable decomposition forces strict gap
;   Proof: E feasible in joint optimization, infima of separable costs preserved under strict ineq
; Remark822-828: Emergence as irreducible compression -- joint explanation achieves description-length
;   advantage not recoverable by any factorization into type-restricted components
;   Shared latent variable simultaneously explains sensory regularities and guides procedural choices
;   Testable: compare minimal contrivance frontiers under enforced modularization vs allowed interaction
;   Regularization relief: constraint to split across types forces separate description length for shared structure
; Def211: Budgeted solvability criterion -- task b solvable by T at budget B if ConStar of T at tau leq B
;   Simplest resource-bounded competence definition. B as abstract proxy for representational capacity
; Remark829-830: Increasing B expands solvable set monotonically but synergy shifts required budget downward
;   Synergy as efficiency gain in how system allocates limited representational capacity
; Prop26: Synergy expands solvable set relative to non-synergistic partitions
;   There exists budget B where joint architecture solves task but every separable architecture fails
;   Proof: interval arithmetic -- strict inequality C12 < Cpart implies nonempty gap of budgets
; Remark831-835: Capability gap when intermediate results exchanged across types vs combined only at end
;   Separable must pay separately, synergistic may co-adapt and share explanatory burden
;   Benchmark at budget in gap becomes diagnostic of whether system exploits cross-type coupling
;   Intelligence increase not mystical -- existence of tasks crossing impossible to possible under cross-type compression
; === SECTION 15.6: ATTENTION AS GATING MECHANISM FOR SYNERGY ===
; Attention gates whether potential synergy is realized. Opportunity cost claim:
;   Every unit of attention on cross-type translation is unit not on within-type refinement
;   If attention never pays for communication, rich multi-type architecture behaves as loosely coupled modules
; Def212: Inter-type communication graph Gamma on knowledge types T
;   Directed edges T to T-prime with time-dependent bandwidth allocation bt
;   Bandwidth as attention share devoted to cross-type translation at each timestep
; === END SECTION 15.6 PARTIAL ===

; === SECTION 16.1: SELF AS PARACONSISTENT CUT ===
; Def213: Self-evidence function sigma_I mapping tokens to p-bit pairs
; Boundary region dSelf = high evidence both ways -- zone of genuine conflict
; Synergy is dynamical property under attentional governance not merely structural
; === END SECTION 16.1 PARTIAL ===
