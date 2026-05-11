# 1 Introduction

Note on AI Co-Authoring and Co-Utilization .

   • This document was primarily written by LLMs, though in a process of repeated prompting,
     sweeps across the whole document by scripts running prompts, and so forth. There was also
     human editing here and there when it was an easier way to fix things than doing prompting.
     Every part of the document was human-reviewed at one or more stages in the document
     creation process, but it can’t be claimed that every part has been carefully reviewed in the
     final form – there may still be glitches!

   • This is not a product envisioned as the subject of frequent leisure reading. It does contain a
     significant number of ideas, insights and conclusions that will be of interest to humans oriented
     toward philosophical and conceptual foundations of science, AI, and so forth; however, these
     are not usually presented here in the most delightfully consumable fashion, although effort
     has been made to include nontechnical explanations along with formalism.

   • A primary use-case for this document is envisioned as: Ingestion by AI systems, which may
     more fully formalized the material given here, and then leverage this more formalized ver-
     sion for practical guidance of automated uncertain reasoning in commonsense and scientific
     domains. The brief companion document Hyperseed: A Scrutability-Style Core Ontology and
     a Practical Inference-Control Scaffold for Probabilistic Logic Networks outlines some ideas
     on how this might be done, along with some associated theoretical work elaborating ”what
     makes a good ontology,” and some ideas on how AIs may evolve even better and more useful
     ontologies using Hyperseed as, well, a seed.


Contents
1 Introduction                                                                                        2
  1.1 Use of Hyperseed for Guiding AI Reasoning . . . . . . . . . . . . . . . . . . . . . . .         6

2 Hyperseed at a glance: concept inventory and dependency DAG                                          7
  2.1 Purpose and reading conventions . . . . . . . . . . . . . . . . . . . . . . . . . . . . .        7
  2.2 Layered view: the Hyperseed “semantic stack” . . . . . . . . . . . . . . . . . . . . .           9
  2.3 Concept inventory by module . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       11
  2.4 Dependency DAG: definition and interpretation . . . . . . . . . . . . . . . . . . . . .         15
  2.5 High-level DAG (module graph) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       17
  2.6 Key concept-level dependencies (selected adjacency list) . . . . . . . . . . . . . . . .        19
  2.7 Mathematical load-bearing walls . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       25
  2.8 Where observer-relativity and paraconsistency enter . . . . . . . . . . . . . . . . . .         27
  2.9 How this DAG drives the rest of the paper . . . . . . . . . . . . . . . . . . . . . . . .       29

3 Minimal formal core                                                                                 30
  3.1 Design requirements and core data types . . . . . . . . . . . . . . . . . . . . . . . . .       32
  3.2 Paraconsistent p-bit values . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   35
  3.3 Quantales as aggregation and composition domains . . . . . . . . . . . . . . . . . . .          37
  3.4 A canonical p-bit quantale . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    39
  3.5 V -valued relations and quantale composition . . . . . . . . . . . . . . . . . . . . . .        41
  3.6 V -enriched categories and approximate morphisms . . . . . . . . . . . . . . . . . . .          43
  3.7 Quantale weakness as “failed distinctions” . . . . . . . . . . . . . . . . . . . . . . . .      46
  3.8 Interpretation map: from Hyperseed talk to core objects . . . . . . . . . . . . . . . .         48

                                                   2
    3.9   Resonance derived from paraconsistency . . . . . . . . . . . . . . . . . . . . . . . . . 50

4 Core sanity theorems                                                                               54

5 Toy model: finite universe, p-bit quantale, and morphic resonance demo                             62
  5.1 Finite universe and two contexts . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     64
  5.2 From relations to weakness: “failed distinctions” . . . . . . . . . . . . . . . . . . . .      66
  5.3 Patterns as finite constraints and pattern support . . . . . . . . . . . . . . . . . . . .     68
  5.4 Emergence via compositional closure . . . . . . . . . . . . . . . . . . . . . . . . . . .      70
  5.5 Miledorphic resonance and anti-resonance as cross-context coupling . . . . . . . . . .         73
  5.6 A concrete nontrivial instance reaching morphic resonance . . . . . . . . . . . . . . .        75
  5.7 Anti-resonance as habit reversal (tiny numeric demo) . . . . . . . . . . . . . . . . . .       78
  5.8 A tiny resonance score demo via paraconsistent interference . . . . . . . . . . . . . .        79


I   Systematic reconstruction of Hyperseed concepts                                                  81

6 Phenomenological primitives                                                                      81
  6.1 Occasions and contexts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 83
  6.2 Difference and distinction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 86
  6.3 Repetition, variety, non-duality, and non-dual variety . . . . . . . . . . . . . . . . . . 88
  6.4 First, Second, Third, Fourth . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 91
      6.4.1 A minimal inductive ladder . . . . . . . . . . . . . . . . . . . . . . . . . . . . 92
      6.4.2 A concrete set-theoretic model (optional) . . . . . . . . . . . . . . . . . . . . 95
  6.5 Presentational immediacy and intensity . . . . . . . . . . . . . . . . . . . . . . . . . 96
  6.6 Abstract and concrete . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 98
      6.6.1 Abstraction as quotienting of distinctions . . . . . . . . . . . . . . . . . . . . 98
      6.6.2 Concreteness as resistance to quotienting . . . . . . . . . . . . . . . . . . . . 101
  6.7 Non-duality as a bridge between perspectives . . . . . . . . . . . . . . . . . . . . . . 102

7 Order, time, and becoming                                                                       103
  7.1 After/before as strict partial order . . . . . . . . . . . . . . . . . . . . . . . . . . . . 105
  7.2 Proto-time as observer-relative ordering . . . . . . . . . . . . . . . . . . . . . . . . . 107
  7.3 Graded and paraconsistent temporal ordering . . . . . . . . . . . . . . . . . . . . . . 109
  7.4 Linear time axes as serializations and quotients . . . . . . . . . . . . . . . . . . . . . 111
  7.5 Becoming as boundary non-duality . . . . . . . . . . . . . . . . . . . . . . . . . . . . 115
  7.6 A paraconsistent, quantale-valued event calculus . . . . . . . . . . . . . . . . . . . . 119
      7.6.1 Signature and intended semantics . . . . . . . . . . . . . . . . . . . . . . . . . 119
      7.6.2 Monotone rule evaluation over a quantale . . . . . . . . . . . . . . . . . . . . 120
      7.6.3 Clipping and inertia (paraconsistent sketch) . . . . . . . . . . . . . . . . . . . 122
  7.7 Time contexts and temporal similarity . . . . . . . . . . . . . . . . . . . . . . . . . . 124
  7.8 Persistent, continuous, increasing, decreasing . . . . . . . . . . . . . . . . . . . . . . 126
  7.9 Process view: becoming as functorial evolution (bridge to process calculi) . . . . . . 128

8 Effort, resistance, and simplicity                                                                129
  8.1 Effort as a cost structure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 132
  8.2 Distinctions as policies; opening and closing . . . . . . . . . . . . . . . . . . . . . . . 135
  8.3 Effort of distinctions; resistance and submission . . . . . . . . . . . . . . . . . . . . . 137
  8.4 Simplicity as minimum representational effort . . . . . . . . . . . . . . . . . . . . . . 139

                                                   3
   8.5   Simplicity as weakness: the dual perspective . . . . . . . . . . . . . . . . . . . . . . . 140
   8.6   Minimum representational effort as constrained weakness maximization . . . . . . . 142
   8.7   Compositional simplicity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 146
   8.8   Generalized Kolmogorov complexity and structural complexity . . . . . . . . . . . . 151
   8.9   Discussion: how this feeds later Hyperseed layers . . . . . . . . . . . . . . . . . . . . 155

9 Patterns, emergence, properties, and blending                                                     157
  9.1 Setup: entities, contexts, descriptions, and effort . . . . . . . . . . . . . . . . . . . . 159
  9.2 Combination, inheritance, and association as pattern-level notions . . . . . . . . . . 162
  9.3 Patterns and pattern intensity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 163
       9.3.1 Patterns as compressive descriptions . . . . . . . . . . . . . . . . . . . . . . . 164
       9.3.2 Patterns as compositional factorization . . . . . . . . . . . . . . . . . . . . . 164
       9.3.3 Pattern intensity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 165
  9.4 Properties as fuzzy sets of patterns . . . . . . . . . . . . . . . . . . . . . . . . . . . . 167
       9.4.1 Inheritance and association via properties . . . . . . . . . . . . . . . . . . . . 168
  9.5 Emergence . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 169
  9.6 Blends . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 171
       9.6.1 Categorical blend construction (pushout intuition) . . . . . . . . . . . . . . . 172
  9.7 Lifting from instances to groups . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 173
  9.8 Combinatorial-categorical patterns . . . . . . . . . . . . . . . . . . . . . . . . . . . . 174
  9.9 Combination systems, interpreters, and combinational dynamical causal models . . . 175
  9.10 Specific entities as temporally coherent patterns . . . . . . . . . . . . . . . . . . . . . 177
  9.11 Worked micro-example (optional but useful) . . . . . . . . . . . . . . . . . . . . . . . 178

10 Information, uncertainty, and ineffability                                                      179
   10.1 Motivation: information as observer-indexed bookkeeping . . . . . . . . . . . . . . . 179
   10.2 Observer-indexed probability spaces . . . . . . . . . . . . . . . . . . . . . . . . . . . 181
   10.3 Shannon information, coding, and divergence . . . . . . . . . . . . . . . . . . . . . . 183
   10.4 Mutual and interaction information . . . . . . . . . . . . . . . . . . . . . . . . . . . . 187
   10.5 Logical entropy and graphtropy from distinction structure . . . . . . . . . . . . . . . 189
   10.6 Uncertainty and ineffability as observer-relative modalities . . . . . . . . . . . . . . . 194
   10.7 Potential infinity and infinitesimals as “limit objects” . . . . . . . . . . . . . . . . . 198
   10.8 Section wrap-up . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201

11 Hierarchy, heterarchy, and pattern webs                                                          202
   11.1 Motivation: why Hyperseed needs both hierarchies and webs . . . . . . . . . . . . . 202
   11.2 Hierarchy as observer-assessed order . . . . . . . . . . . . . . . . . . . . . . . . . . . 204
   11.3 Systemic hierarchy via models of a dynamical system . . . . . . . . . . . . . . . . . . 207
   11.4 Subpattern hierarchy: patterns within patterns . . . . . . . . . . . . . . . . . . . . . 209
   11.5 Heterarchy: multi-path structure and loops . . . . . . . . . . . . . . . . . . . . . . . 211
   11.6 Pattern webs from pattern profiles and pattern-based distances . . . . . . . . . . . . 213
   11.7 Pattern webs as free V -categories . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 216
   11.8 Multi-resolution transforms and weakness . . . . . . . . . . . . . . . . . . . . . . . . 218
   11.9 Section wrap-up . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 220




                                                   4
12 Habits, self-weaving webs, and morphic resonance                                                221
   12.1 From Hyperseed’s probability phrasing to V -valued dynamics . . . . . . . . . . . . . 223
   12.2 Pattern webs as V -relations and habit update operators . . . . . . . . . . . . . . . . 226
   12.3 Self-weaving webs and autocatalytic closure . . . . . . . . . . . . . . . . . . . . . . . 231
   12.4 Morphic resonance and morphic anti-resonance as cross-context coupling . . . . . . . 234
   12.5 Stability, amplification, and decay . . . . . . . . . . . . . . . . . . . . . . . . . . . . 238
   12.6 A worked micro-example reaching self-weaving and morphic resonance . . . . . . . . 242
   12.7 Notes and bridges to later sections . . . . . . . . . . . . . . . . . . . . . . . . . . . . 245

13 Mind, representation, and perception                                                             246
   13.1 Systems, minds, and recognition processes . . . . . . . . . . . . . . . . . . . . . . . . 247
   13.2 Contexts and aspects . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 249
   13.3 Registration, sensory systems, and perception . . . . . . . . . . . . . . . . . . . . . . 251
   13.4 Representation as reference plus pattern inheritance . . . . . . . . . . . . . . . . . . 254
   13.5 Semiotic modes: icon, index, symbol . . . . . . . . . . . . . . . . . . . . . . . . . . . 257
   13.6 Soggy predicates and paraconsistent truth . . . . . . . . . . . . . . . . . . . . . . . . 259
   13.7 Micro-example: registering and representing a pattern . . . . . . . . . . . . . . . . . 262
   13.8 What this buys us for later sections . . . . . . . . . . . . . . . . . . . . . . . . . . . 263

14 Prediction, attraction, causality, and control                                                    264
   14.1 From patterns to forecasts and interventions . . . . . . . . . . . . . . . . . . . . . . . 264
   14.2 Event types, timelines, and paraconsistent occurrence data . . . . . . . . . . . . . . 266
   14.3 Prediction and attraction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 269
        14.3.1 Conditionals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 269
        14.3.2 Attraction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 270
        14.3.3 Predictive implication and predictive attraction . . . . . . . . . . . . . . . . . 271
   14.4 Sequential and parallel temporal composition . . . . . . . . . . . . . . . . . . . . . . 273
        14.4.1 Sequential composition as quantale multiplication . . . . . . . . . . . . . . . 273
        14.4.2 A tiny worked schematic . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 274
   14.5 Causality as attraction plus temporal precedence plus simplicity bias . . . . . . . . . 274
        14.5.1 Extensional and intensional predictive attraction . . . . . . . . . . . . . . . . 275
        14.5.2 Causal implication and simple causal implication . . . . . . . . . . . . . . . . 277
        14.5.3 Weakness-biased causal model selection . . . . . . . . . . . . . . . . . . . . . 279
   14.6 Control, control hierarchies, and perceptual hierarchies . . . . . . . . . . . . . . . . . 281
   14.7 Planning and optimal control: integration hooks . . . . . . . . . . . . . . . . . . . . 284
        14.7.1 Event calculus hook . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 284
        14.7.2 Wu Wei preview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 285

15 Attention and cognitive synergy                                                                 286
   15.1 From control to attention . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 286
   15.2 Genenergy budgets and attention measures . . . . . . . . . . . . . . . . . . . . . . . 287
        15.2.1 Attention to a pattern class . . . . . . . . . . . . . . . . . . . . . . . . . . . . 288
        15.2.2 Attentional focus and self-reflective attention . . . . . . . . . . . . . . . . . . 289
   15.3 Attention as a bounded control policy . . . . . . . . . . . . . . . . . . . . . . . . . . 290
   15.4 Varieties of knowledge as typed pattern structures . . . . . . . . . . . . . . . . . . . 295
        15.4.1 Declarative knowledge . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 296
        15.4.2 Procedural knowledge . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 296
        15.4.3 Sensory knowledge . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 297


                                                   5
        15.4.4 Attentional knowledge . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 298
        15.4.5 Intentional knowledge . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 299
   15.5 Cognitive synergy as cross-type weakness improvement . . . . . . . . . . . . . . . . . 300
        15.5.1 Usefulness of a learning algorithm for a knowledge type . . . . . . . . . . . . 300
        15.5.2 Explanations, weakness, and contrivance cost . . . . . . . . . . . . . . . . . . 301
        15.5.3 Synergy as strict subadditivity of contrivance . . . . . . . . . . . . . . . . . . 303
        15.5.4 A sufficient condition: monoidal compositionality of weakness . . . . . . . . . 303
        15.5.5 When does synergy become strict? . . . . . . . . . . . . . . . . . . . . . . . . 305
        15.5.6 A criterion for “synergy increases effective intelligence” . . . . . . . . . . . . 307
   15.6 Attention as the gating mechanism for synergy . . . . . . . . . . . . . . . . . . . . . 309

16 Self, continuity, development, and mind-world correspondence                                 311
   16.1 Self/other boundary as a paraconsistent, observer-relative cut . . . . . . . . . . . . . 312
   16.2 Approximate morphisms of quantale-weighted networks . . . . . . . . . . . . . . . . 315
   16.3 Self-continuity as approximate self-morphism across time . . . . . . . . . . . . . . . 318
   16.4 Development as continuity plus expanding capability . . . . . . . . . . . . . . . . . . 322
   16.5 Mind–world correspondence via pattern-flow morphisms . . . . . . . . . . . . . . . . 325
   16.6 Space as a structure on which correspondences are defined . . . . . . . . . . . . . . . 329

17 Consciousness, reflective will, and autonomy                                                     334
   17.1 Orientation: what gets formalized here . . . . . . . . . . . . . . . . . . . . . . . . . . 334
   17.2 A minimal interface: evidence states, workspace closure, and access . . . . . . . . . . 335
        17.2.1 Languages and evidence states . . . . . . . . . . . . . . . . . . . . . . . . . . 335
        17.2.2 Subsystem reports and attention-weighted integration . . . . . . . . . . . . . 336
        17.2.3 Global accessibility and workspace closure . . . . . . . . . . . . . . . . . . . . 339
   17.3 Reflective consciousness as higher-order representational closure . . . . . . . . . . . . 341
        17.3.1 Adding a reflective layer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 342
        17.3.2 Reflective workspace closure and a fixed-point existence theorem . . . . . . . 343
   17.4 Resonance and coherence as stability selectors . . . . . . . . . . . . . . . . . . . . . . 346
        17.4.1 Coherence scores from paraconsistent evidence . . . . . . . . . . . . . . . . . 346
        17.4.2 Reflective consciousness as coherence-weighted closure . . . . . . . . . . . . . 347
   17.5 Reflective will as meta-control on self-model dynamics . . . . . . . . . . . . . . . . . 349
        17.5.1 Will as choice of an intervention on the update operator . . . . . . . . . . . . 349
        17.5.2 Reflective will as meta-selection . . . . . . . . . . . . . . . . . . . . . . . . . . 350
   17.6 Autonomy and the reflective self as fixed points and higher morphisms . . . . . . . . 351
        17.6.1 Autonomy as viability under self-directed closure . . . . . . . . . . . . . . . . 351
        17.6.2 Reflective self as a stabilized self-representation . . . . . . . . . . . . . . . . . 352
   17.7 States of consciousness as parameter regimes . . . . . . . . . . . . . . . . . . . . . . 353
        17.7.1 Canonical regimes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 353
   17.8 Intuition and reason as dual inference channels . . . . . . . . . . . . . . . . . . . . . 355
   17.9 Closing remarks and link to values/ethics . . . . . . . . . . . . . . . . . . . . . . . . 357

18 Emotion, values, goals, and rationality                                                          358
   18.1 Orientation: why “emotion” belongs in the formal stack . . . . . . . . . . . . . . . . 358
   18.2 Paraconsistent evaluative evidence and affective projections . . . . . . . . . . . . . . 360
        18.2.1 Evaluation fields . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 360
        18.2.2 Joy/woe and pleasure/pain . . . . . . . . . . . . . . . . . . . . . . . . . . . . 362
        18.2.3 Aggregating across value dimensions without collapsing conflicts . . . . . . . 363


                                                   6