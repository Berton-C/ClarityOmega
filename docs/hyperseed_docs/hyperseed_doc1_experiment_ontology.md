# Experiment-ontology

Representing Scientific Experiments in MeTTa:
    SUMO/EXPO Structure with Hyperseed Epistemic Annotations

                                               Ben Goertzel

                                            February 25, 2026


                                                  Abstract
          We propose a representation for scientific experiments—especially computational ones—as
      structured symbolic objects in MeTTa. The representation has two layers: an ontological layer,
      drawn from EXPO (Ontology of Scientific Experiments, built on the SUMO upper ontology),
      that records what an experiment is (goals, design, factors, actions, results, errors); and an epis-
      temic layer, inspired by Hyperseed’s p-bit evidence semantics, that records what an experiment
      does to a belief system—which claims it supports or undermines, and with what strength and
      caveats.
          The combined representation is designed to make experiments uniformly representable across
      domains so they can be searched, compared, and composed; to make results machine-actionable
      by encoding tables as typed measurement objects; and to enable reasoning about validity, re-
      producibility, and domain transfer by attaching explicit evidence states to claims. A detailed
      worked example, formalizing a regime-classification methodology paper in quantitative finance,
      is provided in Appendix A.


1     Introduction
Scientific progress depends on experiments, but modern scientific practice depends just as much on
managing them: storing, comparing, reproducing, integrating with prior work, and reasoning about
what they imply and what they fail to establish. In many fields this management has become a
scaling bottleneck: the volume of reports, datasets, pipelines, and partial replications exceeds any
human (or committee) capacity for reliable synthesis.
    This paper proposes a representation that is simultaneously ontological (recording the struc-
ture of an experiment in a reusable schema), epistemic (recording what the experiment does to
a belief system, in a way that tolerates conflict and supports incremental updating), and compu-
tational (designed so that logic-based inference engines—including PLN-like systems—can exploit
the structure to draw nontrivial inferences across experimental records, datasets, and semantically
parsed text).

1.1   Why a logical representation rather than YAML?
A well-designed configuration schema (YAML, JSON, etc.) can record experiment metadata and
results effectively, and for many workflows it suffices. A purely syntactic schema, however, is
not by itself a strong substrate for reasoning. The approach here is justified only insofar as the
representation supports capabilities that are hard to obtain from a configuration format alone:



                                                      1
    • Constraint-aware normalization. Two experiments can be automatically recognized as
      “the same experiment up to irrelevant renaming” or “variants differing only in factor X,”
      because factors, factor-levels, and targets are explicit first-class objects.

    • Inference over validity and comparability. Threats to validity (leakage, confounding, in-
      complete data, faulty comparisons) can be represented as objects that participate in inference
      rules, so that downstream conclusions inherit appropriate caveats.

    • Cross-source integration. Semantic parsing can turn prose claims into candidate proposi-
      tions; dataset ingestion can turn tables into measurement objects; the system can link both
      into a unified graph where inference bridges text, data, and experimental design.

    • Epistemic aggregation under conflict. Multiple experiments may support and oppose
      the same claim. The representation stores both without forcing premature collapse, en-
      abling downstream AI components to reconcile, segment by context, or propose discriminating
      follow-up experiments.

    • Search by meaning, not by string. One can query for “all experiments estimating X
      under regime Y with window size T and dictionary capacity D” rather than relying on
      keyword matching.


2     EXPO: The Ontological Backbone
EXPO (Ontology of Scientific Experiments), anchored to the SUMO upper ontology, is an interme-
diate ontology layer designed to capture experiment concepts that are common across domains. It
provides a reusable vocabulary in which goals, factors, target variables, actions, results, conclusions,
and errors are explicit and comparable.
    EXPO plays two roles in our representation:

    1. Canonical structure. It supplies the stable “shape” of an experiment record—what parts
       exist and how they relate.

    2. Interoperability. It provides a shared semantic scaffold so that experiments in different
       domains can still be aligned at the level of design and results.

Modeling style. EXPO treats an experiment as an object with (at least) three conceptual levels:
a physical/world level (the field of study), a model level (the experimental model or domain model),
and a design level (parameters, target variables, actions). Experiments are assembled from a small
set of core relations inherited from SUMO conventions—instance, subclass, part, attribute,
and role—together with experiment-specific parts: ExperimentalDesign, ExperimentalModel,
ExperimentalGoal, ExperimentalResults, ExperimentalConclusion, and so on. The design
and model are elaborated through Factor, FactorLevel, TargetVariable, ModelAssumption,
ResearchHypothesis, NullHypothesis, and AlternativeHypothesis.


3     Hyperseed Epistemics as an Overlay on EXPO
EXPO records what an experiment is; our aim is also to make experiment records usable objects
for automated reasoning—aggregating evidence across studies, representing and analyzing conflicts,



                                                   2
connecting claims to parsed text and structured data, and proposing discriminating follow-up ex-
periments. To this end we add an epistemic layer inspired by Hyperseed, a formal-logic-based
ontology that aims to formalize a coherent conceptual account of the physical and mental worlds,
and the knowledge and reasoning of cognitive agents therein.
    Hyperseed provides a compact, mathematically grounded treatment of epistemics that comple-
ments EXPO’s structural descriptions. The central idea is to represent knowledge as an evidence
state over a claim language rather than as a brittle set of Boolean assertions. In the simplest useful
instance, evidence values live in V = [0, 1]2 : a “p-bit” recording separate degrees of positive and
negative support. These assemble into evidence states E : L → V over a proposition language L.
    This representation is directly suited to experiment corpora, where evidence is routinely incom-
plete, context-dependent, and sometimes contradictory across laboratories, datasets, and evaluation
protocols. With p-bit evidence states, conflict does not force collapse: strong support and strong
counter-support can coexist explicitly, allowing downstream reasoning to remain nontrivial.

Division of labor. The two layers have a clean separation of concerns: EXPO provides the
structural object—a record with explicit factors, target variables, actions, and measurement tables—
while Hyperseed provides the belief-update interpretation: the experiment induces an evidence
increment on a chosen claim language (e.g. performance, robustness, causal effect), and these
increments can be aggregated across experiments.
    Concretely, for each derived claim c we attach a p-bit E(c) = (E + (c), E − (c)) ∈ [0, 1]2 , where
E (c) summarizes positive support and E − (c) summarizes counter-support (including threats to
  +

validity, suspected leakage, untested assumptions, or replication failures). This enables meta-
reasoning operations such as aggregating evidence across experiments without erasing disagreement,
propagating caveats through derived conclusions, identifying “controversial” claims with simulta-
neously high E + and E − , and proposing follow-up experiments that most reduce uncertainty or
resolve conflicts.

Relation to PLN-style inference. PLN-style inference benefits from explicit structure: typed
predicates, explicit factor levels, measurement semantics, and explicit uncertainty representations.
EXPO supplies the first three; Hyperseed supplies the fourth in a lightweight but mathematically
disciplined form that supports principled aggregation and closure reasoning. In this sense Hyperseed
is not a competing ontology but an epistemic semantics that makes EXPO experiment records more
actionable for automated inference.


4     Design Requirements
We want experiment records that satisfy:
    1. Within-domain uniformity: similar experiments in a domain should map to the same
       schema.
    2. Cross-domain compatibility: different domains share top-level experiment structure and
       common measurement primitives.
    3. Reasoning affordances: the representation should support consistency checks (missing
       components, incompatible units, contradictory claims), comparative queries (find experiments
       with the same factor levels or similar results), downstream reasoning (derive conclusions from
       result measurements), and epistemic updating (new experiments add support or counter-
       support to existing claims).

                                                  3
5     A Practical EXPO-to-MeTTa Mapping
5.1   Core idea
Each experiment is represented as a MeTTa object graph whose nodes are instances of EXPO
(and domain-extension) classes and whose edges are SUMO/EXPO relations (instance, part,
attribute, role, etc.).

5.2   Type signatures (informal)
Even without a full dependent type system, structure can be enforced by conventions. The following
classes form the core vocabulary:

; --- EXPO classes ---
expo:ScientificExperiment
expo:ComputationalExperiment
expo:ExperimentalDesign
expo:ExperimentalModel
expo:ExperimentalGoal
expo:ExperimentalResults
expo:ExperimentalConclusion
expo:Factor
expo:FactorLevel
expo:TargetVariable
expo:ResearchHypothesis
expo:ModelAssumption

; --- Extended measurement/epistemic classes ---
exmeta:Dataset
exmeta:MeasurementTable
exmeta:MeasurementRow
exmeta:Measurement
exmeta:Claim
exmeta:EvidenceState          ; Hyperseed-style epistemic object

5.3   Canonical relations
; Membership
(instance <individual> <class>)

; Composition / structure
(part <part> <whole>)

; Attributes and roles
(attribute <entity> <attribute>)
(role <role-holder> <role-in-context>)

; Experiment-specific links
(hasFactor        <experiment-or-model> <factor>)


                                                4
(hasFactorLevel   <factor> <factorLevel>)
(hasTargetVariable <experiment-or-model> <targetVariable>)
(hasAssumption    <experiment-or-model> <assumption>)
(hasHypothesis    <experiment> <hypothesis>)
(hasResults       <experiment> <results>)
(hasConclusion    <experiment> <conclusion>)


6     Representing Results as Structured Measurement Objects
6.1   Why not just store a CSV?
Raw tabular storage lacks explicit column semantics (metric identity), units and aggregation rules,
provenance linking each number to a method and dataset, and machine-checkable compatibility
across experiments. Structured measurement objects supply all four.

6.2   A reusable measurement schema
Result tables are represented as MeasurementTables containing MeasurementRows, each row holding
multiple Measurement objects:

(instance table7 exmeta:MeasurementTable)
(part table7 exp1)
(tableTitle table7 "Crypto: daily regime statistics")
(tableHasRow table7 row7.R0)
(tableHasRow table7 row7.R1)
...

(instance row7.R0 exmeta:MeasurementRow)
(rowContext row7.R0 (regime R0) (asset_pool crypto12) (freq daily))
(rowHasMeasurement row7.R0 m7.R0.n_days)
(rowHasMeasurement row7.R0 m7.R0.sigma_d)
(rowHasMeasurement row7.R0 m7.R0.absret)
(rowHasMeasurement row7.R0 m7.R0.persistence)

(instance m7.R0.sigma_d exmeta:Measurement)
(measureMetric m7.R0.sigma_d exfin:DailyVolatility)
(measureValue m7.R0.sigma_d 3.23)
(measureUnit   m7.R0.sigma_d "pct_per_day")

    A measurement can optionally include an uncertainty object:
(measureValue       m8.R5.llc_lambda 0.883)
(measureUncertainty m8.R5.llc_lambda (stderr 0.078))


7     Epistemic Annotations for Experiment Claims
7.1   Claims versus measurements
Measurements are data objects—numbers together with their meaning, units, and provenance.
Claims are propositions derived from measurement sets, possibly under additional modeling as-

                                                5
sumptions. We therefore maintain three distinct object types: Measurement objects, Claim
objects (logical propositions that can be supported or refuted), and EvidenceState objects (epis-
temic annotations attached to claims).

7.2    Evidence states as p-bits
Each claim receives an evidence pair (p, n) with p, n ∈ [0, 1], where p is the degree of positive
support and n is the degree of counter-evidence. Both can be nonzero simultaneously, enabling
paraconsistent accumulation of conflicting results.

7.3    Computing (p, n) in practice
A simple (and replaceable) recipe:
    1. Convert effect sizes and uncertainties into a support score—for example, via a sigmoid of
       (estimate / standard error).
    2. Convert known threats to validity (data leakage, non-stationarity, untested assumptions) into
       negative support.
    3. Track provenance: record which measurements and assumptions contributed.
An illustrative encoding:
(instance claim.crypto.R5.compressible exmeta:Claim)
(claimText claim.crypto.R5.compressible
  "In crypto, Complex Trend (R5) is compressible (positive LLC).")

(instance ev.claim.crypto.R5.compressible exmeta:EvidenceState)
(evidencePair ev.claim.crypto.R5.compressible (p 0.98) (n 0.05))
(supportedBy claim.crypto.R5.compressible m8.R5.llc_lambda)
(supportedBy claim.crypto.R5.compressible m8.R5.llc_stderr)
(evidenceOf ev.claim.crypto.R5.compressible claim.crypto.R5.compressible)


8     Worked Example: Compression-Based Regime Classification
Appendix A presents a complete, step-by-step formalization of a regime-classification methodology
paper in quantitative finance (Goertzel, 2026). The paper proposes a compression-based approach
to classifying financial time-series into six regimes (three complexity levels crossed with two trend
levels) and evaluates it on 12 cryptocurrency and 14 FX/commodity instruments.
    The formalization demonstrates the following key aspects of the representation:

Experiment skeleton. The paper is registered as an EXPO ComputationalExperiment with
explicit goals (computing regime posteriors; investigating cross-asset stability), four research hy-
potheses, and a full parts hierarchy (design, model, results, conclusions).

Explicit factor enumeration. Every experimental “knob” is declared as a Factor with typed
FactorLevels: asset universes (two pools), sampling frequency, symbolization parameters (5×3×3
= 45-symbol encoder), the six-regime taxonomy (complexity × trend axes with pooled-tercile and
median thresholds), LZ78 dictionary capacity, posterior sharpening parameter β, EM refinement
passes, classification window size, and LLC regression windows.

                                                  6
Measurement tables. Fourteen result tables from the paper are encoded as MeasurementTable
objects with explicit metrics, units, and provenance—including EM convergence diagnostics, label
distributions, per-instrument regime distributions and confidence scores, daily regime statistics
(volatility, returns, persistence), LLC estimates with standard errors, cross-asset comparisons, and
regime-conditional trading parameter suggestions.

Epistemic annotations. Five principal claims are extracted and annotated with p-bit evidence
states: that crypto inhabits all six regimes with high balance (p = 0.93, n = 0.10); that Complex
Trend is uniquely compressible in crypto (p = 0.98, n = 0.05); that no FX/commodity regime is
compressible under the current estimator (p = 0.90, n = 0.12); that cross-asset structure differs
materially (p = 0.92, n = 0.10); and that trading-strategy estimates are indicative only, lacking full
backtest validation (p = 0.95, n = 0.05).


9     How This Enables Search, Analysis, and Reasoning
Once multiple experiments are represented in this framework, MeTTa/PLN-style reasoning can
exploit the structure in several ways:

     • Search by factor level. Find all experiments using a 45-symbol encoder and a 200-bar
       classification window.

     • Cross-domain outcome comparison. Treat tables uniformly as measurement objects and
       aggregate metrics across domains.

     • Contradiction detection. If two experiments make incompatible claims about the same
       proposition, their evidence states can be combined without explosion (paraconsistent evidence
       pairs).

     • Guided inference. Rules can map result patterns to suggested actions—for example, if
       regime persistence is high, then regime-conditional parameterization is likely more stable.

Illustrative query patterns (informal MeTTa):

; Find experiments with evaluation window 200
(match &kb (hasFactorLevel F.window_eval L.window.200) ...)

; Find all claims about compressibility in regime R5
(match &kb (claimText $c $t) (supportedBy $c table8.crypto.llc) ...)


10      Conclusion
EXPO provides a clean, reusable ontology skeleton for experiments—goals, hypotheses, factors,
design, results, conclusions—while Hyperseed-style epistemics supply a lightweight but principled
layer for representing degrees of support and counter-support for claims derived from experiment
measurements.
    The worked example in Appendix A demonstrates concretely how to enumerate the full factor
set of a computational finance experiment, encode result tables as structured measurement objects
with explicit metrics and provenance, and attach epistemic evidence states to the main conclusions


                                                  7
so that future experiments can update them incrementally. The combination yields experiment
records that are not merely archival but serve as active substrates for search, comparison, conflict
detection, and automated inference.


A     Worked Example: Compression-Based Regime Classification in
      Finance
This appendix presents a complete formalization of a regime-classification methodology paper (Go-
ertzel, 2026) in the EXPO + Hyperseed representation described in the main text.

A.1    Experiment identification (EXPO administrative layer)
The paper is registered as an EXPO ScientificExperiment (specifically a ComputationalExperiment)
comprising two closely related study runs: Run A on 12 crypto assets (hourly, pooled training and
evaluation) and Run B on 14 FX/commodity instruments (hourly, identical pipeline).

; Experiment root
(instance exp.goertzel.2026.regime_methodology expo:ScientificExperiment)
(instance exp.goertzel.2026.regime_methodology expo:ComputationalExperiment)

; Admin info
(title exp.goertzel.2026.regime_methodology
  "Compression-Based Regime Classification for Financial Time Series:
   Methodology, Cross-Asset Results, and Trading Applications")
(author exp.goertzel.2026.regime_methodology "Ben Goertzel")
(date   exp.goertzel.2026.regime_methodology "2026-02")

; Parts
(instance design.goertzel.2026 expo:ExperimentalDesign)
(instance model.goertzel.2026   expo:ExperimentalModel)
(instance results.goertzel.2026 expo:ExperimentalResults)
(instance concl.goertzel.2026   expo:ExperimentalConclusion)

(part design.goertzel.2026 exp.goertzel.2026.regime_methodology)
(part model.goertzel.2026   exp.goertzel.2026.regime_methodology)
(part results.goertzel.2026 exp.goertzel.2026.regime_methodology)
(part concl.goertzel.2026   exp.goertzel.2026.regime_methodology)

A.2    Goals and hypotheses
Two EXPO-aligned goals are recorded—a ComputeGoal (compute regime posteriors from price
data) and an InvestigateGoal (investigate whether regimes are stable and interpretable across
asset classes)—together with four research hypotheses:

(instance goal.compute expo:ComputeGoal)
(instance goal.investigate expo:InvestigateGoal)
(part goal.compute exp.goertzel.2026.regime_methodology)
(part goal.investigate exp.goertzel.2026.regime_methodology)


                                                 8
(instance H.tech.posteriors expo:ResearchHypothesis)
(text H.tech.posteriors
  "Compression ratios approximate evidence / free-energy well enough
   to compute regime posteriors.")

(instance H.emp.crypto.balance expo:ResearchHypothesis)
(text H.emp.crypto.balance
  "Crypto markets occupy all six regimes with substantial balance
   and high confidence.")

(instance H.emp.crossasset.structure expo:ResearchHypothesis)
(text H.emp.crossasset.structure
  "FX majors, EM FX, and commodities occupy different regions of
   the same regime taxonomy.")

(instance H.emp.compressible.R5 expo:ResearchHypothesis)
(text H.emp.compressible.R5
  "Complex Trend (R5) is uniquely compressible in crypto
   (positive LLC).")

(hasHypothesis exp.goertzel.2026.regime_methodology H.tech.posteriors)
(hasHypothesis exp.goertzel.2026.regime_methodology H.emp.crypto.balance)
(hasHypothesis exp.goertzel.2026.regime_methodology H.emp.crossasset.structure)
(hasHypothesis exp.goertzel.2026.regime_methodology H.emp.compressible.R5)

A.3     Full factor set
Each experimental knob is declared as a Factor with one or more FactorLevels. The enumeration
below covers both domain factors and algorithmic factors.

A.3.1    Domain and dataset factors
; Factor: asset universe (run A: crypto)
(instance F.assets.crypto12 expo:Factor)
(label F.assets.crypto12 "Asset universe (crypto vs USD)")
(hasFactor model.goertzel.2026 F.assets.crypto12)

(instance L.assets.crypto12 expo:FactorLevel)
(value L.assets.crypto12
  (BTC-USD ETH-USD ADA-USD SOL-USD BNB-USD DOGE-USD
   FET-USD XRP-USD NEAR-USD AR-USD INJ-USD GRT-USD))
(hasFactorLevel F.assets.crypto12 L.assets.crypto12)

; Factor: asset universe (run B: FX/commodity)
(instance F.assets.fxcomm14 expo:Factor)
(label F.assets.fxcomm14 "Asset universe (FX and commodities)")
(hasFactor model.goertzel.2026 F.assets.fxcomm14)


                                             9
(instance L.assets.fxcomm14 expo:FactorLevel)
(value L.assets.fxcomm14
  (EURUSD GBPUSD USDJPY AUDUSD USDCHF USDCAD
   USDTRY USDZAR USDMXN GC=F CL=F NG=F SI=F HG=F))
(hasFactorLevel F.assets.fxcomm14 L.assets.fxcomm14)

; Factor: data frequency
(instance F.freq expo:Factor)
(label F.freq "Sampling frequency")
(hasFactor model.goertzel.2026 F.freq)
(instance L.freq.hourly expo:FactorLevel)
(value L.freq.hourly "1h")
(hasFactorLevel F.freq L.freq.hourly)

; Factor: daily aggregation rule
(instance F.daily_agg expo:Factor)
(label F.daily_agg "Hourly -> daily regime aggregation")
(hasFactor model.goertzel.2026 F.daily_agg)
(instance L.daily_agg.mode expo:FactorLevel)
(value L.daily_agg.mode "daily label = mode(hourly labels)")
(hasFactorLevel F.daily_agg L.daily_agg.mode)

; Factor: confidence threshold for daily statistics
(instance F.conf_thresh_daily expo:Factor)
(label F.conf_thresh_daily "Confidence filter for daily regime statistics")
(hasFactor model.goertzel.2026 F.conf_thresh_daily)
(instance L.conf_gt_0p6 expo:FactorLevel)
(value L.conf_gt_0p6 0.6)
(hasFactorLevel F.conf_thresh_daily L.conf_gt_0p6)

A.3.2   Feature extraction factors (11 features)
(instance F.features11 expo:Factor)
(label F.features11 "Feature set for regime classification")
(hasFactor model.goertzel.2026 F.features11)

(instance L.feat.ret expo:FactorLevel)
(value L.feat.ret (name ret) (window none)
  (def "log return clipped at +/- 5*sigma_hat_168"))

(instance L.feat.rvol6 expo:FactorLevel)
(value L.feat.rvol6 (name rvol_6h) (window 6)
  (def "std(r_t-6:t) * sqrt(8760)"))

(instance L.feat.rvol24 expo:FactorLevel)
(value L.feat.rvol24 (name rvol_24h) (window 24)
  (def "std(r_t-24:t) * sqrt(8760)"))


                                          10
(instance L.feat.rvol168 expo:FactorLevel)
(value L.feat.rvol168 (name rvol_168h) (window 168)
  (def "std(r_t-168:t) * sqrt(8760)"))

(instance L.feat.volratio expo:FactorLevel)
(value L.feat.volratio (name vol_ratio) (window none)
  (def "rvol_6h / rvol_168h"))

(instance L.feat.autocorr1 expo:FactorLevel)
(value L.feat.autocorr1 (name autocorr_1) (window 24)
  (def "rolling lag-1 autocorrelation"))

(instance L.feat.autocorr5 expo:FactorLevel)
(value L.feat.autocorr5 (name autocorr_5) (window 48)
  (def "rolling lag-5 autocorrelation"))

(instance L.feat.volofvol expo:FactorLevel)
(value L.feat.volofvol (name vol_of_vol) (window 24)
  (def "std(rvol_6h over last 24 bars)"))

(instance L.feat.dirpersist expo:FactorLevel)
(value L.feat.dirpersist (name dir_persist) (window 12)
  (def "fraction of consecutive same-sign returns"))

(instance L.feat.absret6 expo:FactorLevel)
(value L.feat.absret6 (name abs_ret_6h) (window 6)
  (def "rolling mean of |r_t|"))

(instance L.feat.cumdisp24 expo:FactorLevel)
(value L.feat.cumdisp24 (name cum_disp_24h) (window 24)
  (def "absolute 24-bar cumulative return"))

(hasFactorLevel F.features11 L.feat.ret)
(hasFactorLevel F.features11 L.feat.rvol6)
(hasFactorLevel F.features11 L.feat.rvol24)
(hasFactorLevel F.features11 L.feat.rvol168)
(hasFactorLevel F.features11 L.feat.volratio)
(hasFactorLevel F.features11 L.feat.autocorr1)
(hasFactorLevel F.features11 L.feat.autocorr5)
(hasFactorLevel F.features11 L.feat.volofvol)
(hasFactorLevel F.features11 L.feat.dirpersist)
(hasFactorLevel F.features11 L.feat.absret6)
(hasFactorLevel F.features11 L.feat.cumdisp24)

A.3.3   Symbolic encoding factors
(instance F.symbolization expo:Factor)


                                         11
(label F.symbolization "Symbolic encoder specification")
(hasFactor model.goertzel.2026 F.symbolization)

(instance L.sym.ret_bins expo:FactorLevel)
(value L.sym.ret_bins
  (dimension return_magnitude) (feature ret) (bins 5)
  (boundaries "quantiles at 10th, 30th, 70th, 90th percentile"))

(instance L.sym.vol_bins expo:FactorLevel)
(value L.sym.vol_bins
  (dimension volatility_ratio) (feature vol_ratio) (bins 3)
  (boundaries "quantiles at 33rd, 67th percentile"))

(instance L.sym.ac_bins expo:FactorLevel)
(value L.sym.ac_bins
  (dimension autocorr_sign) (feature autocorr_1) (bins 3)
  (boundaries "thresholds at -0.10, +0.10"))

(instance L.sym.combine expo:FactorLevel)
(value L.sym.combine
  (formula "sym(t) = ret_bin(t)*9 + vol_bin(t)*3 + ac_bin(t)")
  (alphabet_size 45)
  (boundary_fit "fit on pooled training data across instruments"))

(hasFactorLevel F.symbolization L.sym.ret_bins)
(hasFactorLevel F.symbolization L.sym.vol_bins)
(hasFactorLevel F.symbolization L.sym.ac_bins)
(hasFactorLevel F.symbolization L.sym.combine)

A.3.4   Regime taxonomy factors
(instance F.regime_taxonomy expo:Factor)
(label F.regime_taxonomy "Six-regime taxonomy: 3 complexity x 2 trend")
(hasFactor model.goertzel.2026 F.regime_taxonomy)

(instance L.axis1_complexity expo:FactorLevel)
(value L.axis1_complexity
  (axis complexity)
  (feature H24_symbol_entropy) (window 24)
  (split "pooled terciles (33rd, 67th) across training instruments")
  (levels (Simple Structural Complex)))

(instance L.axis2_trend expo:FactorLevel)
(value L.axis2_trend
  (axis trend)
  (feature TrendScore)
  (DirPersist_window 12) (CumDisp_window 24)
  (split "pooled median of TrendScore")


                                       12
 (levels (NonTrend Trend)))

(instance L.regime_id_map expo:FactorLevel)
(value L.regime_id_map
  (complexity_level {0,1,2}) (trend_level {0,1})
  (id_formula "ID = 2*complexity_level + trend_level")
  (regime_names
    (R0 "Simple NonTrend") (R1 "Simple Trend")
    (R2 "Struct NonTrend") (R3 "Struct Trend")
    (R4 "Complex NonTrend") (R5 "Complex Trend")))

(hasFactorLevel F.regime_taxonomy L.axis1_complexity)
(hasFactorLevel F.regime_taxonomy L.axis2_trend)
(hasFactorLevel F.regime_taxonomy L.regime_id_map)

; Thresholds differ by dataset pool
(instance F.axis_thresholds.crypto expo:Factor)
(label F.axis_thresholds.crypto "Crypto grid thresholds")
(hasFactor model.goertzel.2026 F.axis_thresholds.crypto)
(instance L.crypto.entropy_bounds expo:FactorLevel)
(value L.crypto.entropy_bounds (H24_bounds 3.0902 3.5179))
(instance L.crypto.trend_boundary expo:FactorLevel)
(value L.crypto.trend_boundary (TrendScore_boundary 0.0190))
(hasFactorLevel F.axis_thresholds.crypto L.crypto.entropy_bounds)
(hasFactorLevel F.axis_thresholds.crypto L.crypto.trend_boundary)

(instance F.axis_thresholds.fxcomm expo:Factor)
(label F.axis_thresholds.fxcomm "FX/Commodity grid thresholds")
(hasFactor model.goertzel.2026 F.axis_thresholds.fxcomm)
(instance L.fxcomm.entropy_bounds expo:FactorLevel)
(value L.fxcomm.entropy_bounds (H24_bounds 3.0425 3.4550))
(instance L.fxcomm.trend_boundary expo:FactorLevel)
(value L.fxcomm.trend_boundary (TrendScore_boundary 0.0263))
(hasFactorLevel F.axis_thresholds.fxcomm L.fxcomm.entropy_bounds)
(hasFactorLevel F.axis_thresholds.fxcomm L.fxcomm.trend_boundary)

A.3.5   Dictionary, posterior, EM, and evaluation-window factors
(instance F.dict_capacity expo:Factor)
(label F.dict_capacity "Per-regime LZ78 dictionary max size")
(hasFactor model.goertzel.2026 F.dict_capacity)
(instance L.dict.D2051 expo:FactorLevel)
(value L.dict.D2051 2051)
(hasFactorLevel F.dict_capacity L.dict.D2051)

(instance F.posterior expo:Factor)
(label F.posterior "Posterior over regimes from compression ratios")
(hasFactor model.goertzel.2026 F.posterior)


                                         13
(instance L.posterior.beta200 expo:FactorLevel)
(value L.posterior.beta200 (beta 200) (prior "uniform pi(r)=1/6"))
(hasFactorLevel F.posterior L.posterior.beta200)

(instance F.window_eval expo:Factor)
(label F.window_eval "Classification window size (bars)")
(hasFactor model.goertzel.2026 F.window_eval)
(instance L.window.200 expo:FactorLevel)
(value L.window.200 200)
(hasFactorLevel F.window_eval L.window.200)

(instance F.em_passes expo:Factor)
(label F.em_passes "Number of EM refinement passes")
(hasFactor model.goertzel.2026 F.em_passes)
(instance L.em.2 expo:FactorLevel)
(value L.em.2 2)
(hasFactorLevel F.em_passes L.em.2)

(instance F.llc_windows expo:Factor)
(label F.llc_windows "LLC regression window sizes (bars)")
(hasFactor model.goertzel.2026 F.llc_windows)
(instance L.llc.windows expo:FactorLevel)
(value L.llc.windows (60 120 200 300))
(hasFactorLevel F.llc_windows L.llc.windows)

A.4     Measurement tables
The paper’s key result tables are encoded below as MeTTa measurement objects.

A.4.1    Table 3: EM convergence diagnostics
(instance table3.crypto.EMdiag exmeta:MeasurementTable)
(part table3.crypto.EMdiag results.goertzel.2026)
(tableTitle table3.crypto.EMdiag
  "EM convergence diagnostics (crypto pooled, hourly)")

(instance row3.p0 exmeta:MeasurementRow)
(rowContext row3.p0 (pass 0) (note "grid_init"))
(rowHasMeasurement row3.p0 m3.p0.balance)
(rowHasMeasurement row3.p0 m3.p0.confidence)
(measureMetric m3.p0.balance exfin:RegimeBalance)
(measureValue m3.p0.balance 0.369)
(measureUnit   m3.p0.balance "unitless")
(measureMetric m3.p0.confidence exfin:MeanConfidence)
(measureValue m3.p0.confidence 0.930)
(measureUnit   m3.p0.confidence "unitless")
(tableHasRow table3.crypto.EMdiag row3.p0)



                                             14
(instance row3.p1 exmeta:MeasurementRow)
(rowContext row3.p1 (pass 1))
(measureMetric m3.p1.balance exfin:RegimeBalance)
(measureValue m3.p1.balance 0.399)
(measureUnit   m3.p1.balance "unitless")
(measureMetric m3.p1.confidence exfin:MeanConfidence)
(measureValue m3.p1.confidence 0.942)
(measureUnit   m3.p1.confidence "unitless")
(measureMetric m3.p1.labels_changed exfin:LabelsChangedFraction)
(measureValue m3.p1.labels_changed 0.757)
(measureUnit   m3.p1.labels_changed "fraction")
(tableHasRow table3.crypto.EMdiag row3.p1)

(instance row3.p2 exmeta:MeasurementRow)
(rowContext row3.p2 (pass 2))
(measureMetric m3.p2.balance exfin:RegimeBalance)
(measureValue m3.p2.balance 0.405)
(measureUnit   m3.p2.balance "unitless")
(measureMetric m3.p2.confidence exfin:MeanConfidence)
(measureValue m3.p2.confidence 0.938)
(measureUnit   m3.p2.confidence "unitless")
(measureMetric m3.p2.labels_changed exfin:LabelsChangedFraction)
(measureValue m3.p2.labels_changed 0.568)
(measureUnit   m3.p2.labels_changed "fraction")
(tableHasRow table3.crypto.EMdiag row3.p2)

(instance row3.p3 exmeta:MeasurementRow)
(rowContext row3.p3 (pass 3) (note "overfit"))
(measureMetric m3.p3.balance exfin:RegimeBalance)
(measureValue m3.p3.balance 0.318)
(measureUnit   m3.p3.balance "unitless")
(measureMetric m3.p3.confidence exfin:MeanConfidence)
(measureValue m3.p3.confidence 0.940)
(measureUnit   m3.p3.confidence "unitless")
(measureMetric m3.p3.labels_changed exfin:LabelsChangedFraction)
(measureValue m3.p3.labels_changed 0.463)
(measureUnit   m3.p3.labels_changed "fraction")
(tableHasRow table3.crypto.EMdiag row3.p3)

A.4.2   Table 4: Implementation constants
(instance table4.constants exmeta:MeasurementTable)
(part table4.constants results.goertzel.2026)
(tableTitle table4.constants "Implementation constants")

(constant K_regimes 6)
(constant alphabet_size 45)
(constant dict_capacity 2051)


                                        15
(constant beta 200)
(constant eval_window_bars 200)
(constant em_passes 2)
(constant llc_windows (60 120 200 300))

A.4.3   Table 5: Label distribution (crypto pooled)
(instance table5.crypto.labeldist exmeta:MeasurementTable)
(part table5.crypto.labeldist results.goertzel.2026)
(tableTitle table5.crypto.labeldist
  "Crypto: final EM pass label distribution (pooled)")

(rowLabelDist table5.crypto.labeldist
  (R0 "Simple NonTrend" (segments 633) (symbols 117081)))
(rowLabelDist table5.crypto.labeldist
  (R1 "Simple Trend"    (segments 1023) (symbols 49294)))
(rowLabelDist table5.crypto.labeldist
  (R2 "Struct NonTrend" (segments 895) (symbols 50539)))
(rowLabelDist table5.crypto.labeldist
  (R3 "Struct Trend"    (segments 1149) (symbols 73933)))
(rowLabelDist table5.crypto.labeldist
  (R4 "Complex NonTrend"(segments 993) (symbols 49871)))
(rowLabelDist table5.crypto.labeldist
  (R5 "Complex Trend"   (segments 791) (symbols 50746)))

A.4.4   Table 6: Crypto regime distribution and confidence
(instance table6.crypto.regime_by_inst exmeta:MeasurementTable)
(part table6.crypto.regime_by_inst results.goertzel.2026)
(tableTitle table6.crypto.regime_by_inst
  "Crypto: regime distribution and confidence by instrument (selected)")

(regimeDistCrypto table6.crypto.regime_by_inst
  (BTC-USD (R0 27.6) (R1 15.9) (R2 15.3) (R3 14.1) (R4 13.7) (R5 13.4) (Conf 0.92)))
(regimeDistCrypto table6.crypto.regime_by_inst
  (ETH-USD (R0 27.5) (R1 15.7) (R2 14.8) (R3 14.6) (R4 14.1) (R5 13.3) (Conf 0.91)))
(regimeDistCrypto table6.crypto.regime_by_inst
  (ADA-USD (R0 22.5) (R1 17.5) (R2 14.7) (R3 14.3) (R4 15.2) (R5 15.8) (Conf 0.90)))
(regimeDistCrypto table6.crypto.regime_by_inst
  (SOL-USD (R0 15.5) (R1 21.1) (R2 16.5) (R3 15.3) (R4 17.0) (R5 14.7) (Conf 0.90)))
(regimeDistCrypto table6.crypto.regime_by_inst
  (FET-USD (R0 6.5) (R1 23.3) (R2 13.0) (R3 25.3) (R4 9.6) (R5 22.3) (Conf 0.93)))
(regimeDistCrypto table6.crypto.regime_by_inst
  (XRP-USD (R0 42.6) (R1 9.5) (R2 18.1) (R3 4.0) (R4 19.0) (R5 6.8) (Conf 0.93)))
(regimeDistCrypto table6.crypto.regime_by_inst
  (DOGE-USD (R0 25.1) (R1 17.0) (R2 15.2) (R3 13.9) (R4 14.9) (R5 13.9) (Conf 0.91)))
(regimeDistCrypto table6.crypto.regime_by_inst
  (NEAR-USD (R0 12.8) (R1 22.9) (R2 16.5) (R3 18.3) (R4 12.8) (R5 16.8) (Conf 0.90)))


                                          16
(summary table6.crypto.regime_by_inst
  (note "Selected instruments shown; all 12 were classified.")
  (mean_confidence_all_instruments 0.921)
  (regime_balance_overall 0.4734))

A.4.5   Table 7: Crypto daily regime statistics
(instance table7.crypto.daily_stats exmeta:MeasurementTable)
(part table7.crypto.daily_stats results.goertzel.2026)
(tableTitle table7.crypto.daily_stats
  "Crypto: daily regime statistics (all instruments, confidence > 0.6)")

(dailyRegimeStats table7.crypto.daily_stats
  (R0 "Simple NonTrend" (n_days 5343) (sigma_d_pct 3.23)
   (E_absret_pct 2.18) (persistence 0.912)))
(dailyRegimeStats table7.crypto.daily_stats
  (R1 "Simple Trend"    (n_days 3156) (sigma_d_pct 5.82)
   (E_absret_pct 4.19) (persistence 0.778)))
(dailyRegimeStats table7.crypto.daily_stats
  (R2 "Struct NonTrend" (n_days 2968) (sigma_d_pct 4.93)
   (E_absret_pct 3.48) (persistence 0.780)))
(dailyRegimeStats table7.crypto.daily_stats
  (R3 "Struct Trend"    (n_days 2670) (sigma_d_pct 6.38)
   (E_absret_pct 4.61) (persistence 0.790)))
(dailyRegimeStats table7.crypto.daily_stats
  (R4 "Complex NonTrend"(n_days 2673) (sigma_d_pct 4.48)
   (E_absret_pct 3.10) (persistence 0.762)))
(dailyRegimeStats table7.crypto.daily_stats
  (R5 "Complex Trend"   (n_days 2501) (sigma_d_pct 8.27)
   (E_absret_pct 5.52) (persistence 0.808)))

A.4.6   Table 8: Crypto LLC estimates
(instance table8.crypto.llc exmeta:MeasurementTable)
(part table8.crypto.llc results.goertzel.2026)
(tableTitle table8.crypto.llc
  "Crypto: LLC estimates from multi-scale regression")

(llcEstimate table8.crypto.llc
  (R0 "Simple NonTrend" (lambda -6.851) (stderr 0.462) (tier "incompressible")))
(llcEstimate table8.crypto.llc
  (R1 "Simple Trend"     (lambda -11.768) (stderr 0.174) (tier "incompressible")))
(llcEstimate table8.crypto.llc
  (R2 "Struct NonTrend" (lambda -0.793) (stderr 0.237) (tier "incompressible")))
(llcEstimate table8.crypto.llc
  (R3 "Struct Trend"     (lambda -9.916) (stderr 0.051) (tier "incompressible")))
(llcEstimate table8.crypto.llc


                                          17
  (R4 "Complex NonTrend" (lambda -16.769) (stderr 0.262) (tier "incompressible")))
(llcEstimate table8.crypto.llc
  (R5 "Complex Trend"    (lambda 0.883)   (stderr 0.078) (tier "compressible")))

A.4.7   Tables 9–10: FX/Commodity configuration and cross-asset regime distribution
(instance table9.fxcomm.config exmeta:MeasurementTable)
(part table9.fxcomm.config results.goertzel.2026)
(tableTitle table9.fxcomm.config
  "FX/Commodity classifier configuration (matches crypto pipeline)")

(config table9.fxcomm.config
  (alphabet_size 45) (dict_size 2051) (beta 200.0)
  (em_passes 2) (eval_window_bars 200)
  (entropy_bounds 3.0425 3.4550) (trend_boundary 0.0263))

(instance table10.fxcomm.by_class exmeta:MeasurementTable)
(part table10.fxcomm.by_class results.goertzel.2026)
(tableTitle table10.fxcomm.by_class
  "Regime distribution by asset class (hourly bars)")

(regimeDistByClass table10.fxcomm.by_class
  (FX_major   (R0 40.7) (R1 26.2) (R2 0.1) (R3 31.5) (R4 0.8) (R5 0.7) (Conf 0.92)))
(regimeDistByClass table10.fxcomm.by_class
  (FX_em      (R0 26.4) (R1 22.3) (R2 1.9) (R3 33.5) (R4 10.8) (R5 5.1) (Conf 0.91)))
(regimeDistByClass table10.fxcomm.by_class
  (Commodity (R0 1.1) (R1 3.4) (R2 53.5) (R3 3.2) (R4 16.4) (R5 22.5) (Conf 0.94)))

A.4.8   Table 11: Per-instrument FX/Commodity regime distribution
(instance table11.fxcomm.by_inst exmeta:MeasurementTable)
(part table11.fxcomm.by_inst results.goertzel.2026)
(tableTitle table11.fxcomm.by_inst
  "FX/Commodity: per-instrument regime distribution and confidence")

(regimeDistFxComm table11.fxcomm.by_inst
  (EURUSD fx_major (R0 37.1) (R1 19.9) (R2 0.0) (R3 43.0)
   (R4 0.0) (R5 0.0) (Bal 0.000) (Conf 0.91)))
(regimeDistFxComm table11.fxcomm.by_inst
  (GBPUSD fx_major (R0 36.9) (R1 31.1) (R2 0.0) (R3 32.0)
   (R4 0.0) (R5 0.0) (Bal 0.000) (Conf 0.90)))
(regimeDistFxComm table11.fxcomm.by_inst
  (USDJPY fx_major (R0 32.1) (R1 32.2) (R2 0.5) (R3 29.8)
   (R4 2.7) (R5 2.7) (Bal 0.017) (Conf 0.91)))
(regimeDistFxComm table11.fxcomm.by_inst
  (AUDUSD fx_major (R0 37.0) (R1 32.4) (R2 0.1) (R3 28.5)
   (R4 0.7) (R5 1.4) (Bal 0.001) (Conf 0.96)))
(regimeDistFxComm table11.fxcomm.by_inst


                                        18
  (USDCHF fx_major (R0 44.7) (R1 28.3) (R2 0.2) (R3 25.3)
   (R4 1.5) (R5 0.0) (Bal 0.000) (Conf 0.89)))
(regimeDistFxComm table11.fxcomm.by_inst
  (USDCAD fx_major (R0 56.0) (R1 13.4) (R2 0.0) (R3 30.6)
   (R4 0.0) (R5 0.0) (Bal 0.000) (Conf 0.91)))

(regimeDistFxComm table11.fxcomm.by_inst
  (USDTRY fx_em (R0 40.1) (R1 8.4) (R2 0.0) (R3 46.0)
   (R4 0.7) (R5 4.8) (Bal 0.000) (Conf 0.92)))
(regimeDistFxComm table11.fxcomm.by_inst
  (USDZAR fx_em (R0 18.1) (R1 24.9) (R2 1.7) (R3 28.8)
   (R4 23.6) (R5 2.9) (Bal 0.060) (Conf 0.91)))
(regimeDistFxComm table11.fxcomm.by_inst
  (USDMXN fx_em (R0 21.0) (R1 33.7) (R2 4.1) (R3 25.6)
   (R4 8.2) (R5 7.5) (Bal 0.121) (Conf 0.90)))

(regimeDistFxComm table11.fxcomm.by_inst
  (Gold   commodity (R0 5.3) (R1 16.9) (R2 18.4) (R3 15.8)
   (R4 32.2) (R5 11.3) (Bal 0.165) (Conf 0.92)))
(regimeDistFxComm table11.fxcomm.by_inst
  (Crude commodity (R0 0.0) (R1 0.0) (R2 64.5) (R3 0.0)
   (R4 10.6) (R5 24.8) (Bal 0.000) (Conf 0.93)))
(regimeDistFxComm table11.fxcomm.by_inst
  (NatGas commodity (R0 0.0) (R1 0.0) (R2 79.0) (R3 0.0)
   (R4 0.0) (R5 21.0) (Bal 0.000) (Conf 0.96)))
(regimeDistFxComm table11.fxcomm.by_inst
  (Silver commodity (R0 0.0) (R1 0.0) (R2 69.5) (R3 0.0)
   (R4 6.9) (R5 23.6) (Bal 0.000) (Conf 0.93)))
(regimeDistFxComm table11.fxcomm.by_inst
  (Copper commodity (R0 0.0) (R1 0.0) (R2 36.7) (R3 0.0)
   (R4 31.9) (R5 31.4) (Bal 0.000) (Conf 0.98)))

A.4.9   Table 12: Volatility, mean return, and skewness by regime and asset class
(instance table12.fxcomm.vol_mu_skew exmeta:MeasurementTable)
(part table12.fxcomm.vol_mu_skew results.goertzel.2026)
(tableTitle table12.fxcomm.vol_mu_skew
  "FX/Commodity: annualized volatility, mean return (bps/bar),
   skewness by regime and asset class (hourly)")

(volMuSkew table12.fxcomm.vol_mu_skew
  (R0
    (FX_major (n 41000) (vol_pct 9.0) (mu_bps -0.0) (skew -0.29))
    (FX_em    (n 13000) (vol_pct 10.5) (mu_bps 0.1) (skew 0.54))
    (Commodity(n   714) (vol_pct 15.2) (mu_bps 0.9) (skew -0.41))))
(volMuSkew table12.fxcomm.vol_mu_skew
  (R1
    (FX_major (n 27000) (vol_pct 10.1) (mu_bps 0.0) (skew -0.29))


                                         19
    (FX_em    (n 11000) (vol_pct 13.5) (mu_bps 0.0) (skew 0.11))
    (Commodity(n 2300) (vol_pct 16.8) (mu_bps 0.7) (skew 0.50))))
(volMuSkew table12.fxcomm.vol_mu_skew
  (R2
    (FX_major (n   130) (vol_pct 16.9) (mu_bps 0.8) (skew 3.43))
    (FX_em    (n   986) (vol_pct 20.5) (mu_bps -0.0) (skew 0.07))
    (Commodity(n 36000) (vol_pct 69.5) (mu_bps 0.1) (skew -3.73))))
(volMuSkew table12.fxcomm.vol_mu_skew
  (R3
    (FX_major (n 32000) (vol_pct 9.1) (mu_bps 0.1) (skew -0.57))
    (FX_em    (n 17000) (vol_pct 13.4) (mu_bps 0.2) (skew 3.23))
    (Commodity(n 2100) (vol_pct 16.7) (mu_bps 0.6) (skew 0.43))))
(volMuSkew table12.fxcomm.vol_mu_skew
  (R4
    (FX_major (n   826) (vol_pct 21.5) (mu_bps 0.5) (skew 1.12))
    (FX_em    (n 5500) (vol_pct 17.3) (mu_bps 0.0) (skew 0.17))
    (Commodity(n 11000) (vol_pct 27.9) (mu_bps 0.6) (skew -2.66))))
(volMuSkew table12.fxcomm.vol_mu_skew
  (R5
    (FX_major (n   697) (vol_pct 12.1) (mu_bps 0.9) (skew 0.17))
    (FX_em    (n 2600) (vol_pct 19.1) (mu_bps -0.2) (skew 1.62))
    (Commodity(n 15000) (vol_pct 50.1) (mu_bps 0.7) (skew 2.58))))

A.4.10   Table 13: FX/Commodity LLC estimates
(instance table13.fxcomm.llc exmeta:MeasurementTable)
(part table13.fxcomm.llc results.goertzel.2026)
(tableTitle table13.fxcomm.llc
  "FX/Commodity: LLC estimates from multi-scale regression")

(llcEstimate table13.fxcomm.llc
  (R0 "Simple NonTrend" (lambda -3.080) (stderr 0.094) (tier "incompressible")))
(llcEstimate table13.fxcomm.llc
  (R1 "Simple Trend"     (lambda -11.724) (stderr 0.218) (tier "incompressible")))
(llcEstimate table13.fxcomm.llc
  (R2 "Struct NonTrend" (lambda -10.686) (stderr 0.150) (tier "incompressible")))
(llcEstimate table13.fxcomm.llc
  (R3 "Struct Trend"     (lambda -3.517) (stderr 0.027) (tier "incompressible")))
(llcEstimate table13.fxcomm.llc
  (R4 "Complex NonTrend" (lambda -3.719) (stderr 0.097) (tier "incompressible")))
(llcEstimate table13.fxcomm.llc
  (R5 "Complex Trend"    (lambda -3.209) (stderr 0.734) (tier "incompressible")))

A.4.11   Table 14: Summary comparison across asset classes
(instance table14.summary exmeta:MeasurementTable)
(part table14.summary results.goertzel.2026)
(tableTitle table14.summary "Summary comparison across asset classes")


                                        20
(summaryComparison table14.summary
  (Crypto   (regime_balance 0.473) (active_regimes "6/6")
            (vol_ratio_maxmin 2.6) (mean_confidence 0.921)
            (compressible_regimes 1) (R0_persistence 0.912))
  (FX_major (regime_balance "<0.02") (active_regimes "3/6")
            (vol_ratio_maxmin 2.4)   (mean_confidence 0.913)
            (compressible_regimes 0))
  (Commodity(regime_balance "<0.01") (active_regimes "3/6")
            (vol_ratio_maxmin 4.6)   (mean_confidence 0.944)
            (compressible_regimes 0)))

A.4.12   Table 17: Regime-conditional trading parameters
The paper provides a regime-conditional parameter table for market-making (spreads, gamma, max
position). These can be represented either as ExperimentalResults (if treated as study outputs)
or as ExperimentalConclusion / Recommendation objects with low epistemic confidence, since
they have not been validated by full backtesting.

(instance table17.mm_params exmeta:MeasurementTable)
(part table17.mm_params results.goertzel.2026)
(tableTitle table17.mm_params
  "MM parameter suggestions by regime (calibrated from crypto data)")

(mmParams table17.mm_params
  (R0 "Simple NonTrend" (spread_bps 814) (gamma 5.0) (max_pos 0.55)
   (action "Quote normally")))
(mmParams table17.mm_params
  (R1 "Simple Trend"     (spread_bps 1580) (gamma 5.0) (max_pos 0.30)
   (action "Reduce position, skew quotes")))
(mmParams table17.mm_params
  (R2 "Struct NonTrend" (spread_bps 1082) (gamma 5.0) (max_pos 0.43)
   (action "Quote with care")))
(mmParams table17.mm_params
  (R3 "Struct Trend"     (spread_bps 1698) (gamma 5.0) (max_pos 0.28)
   (action "Widen or sit out")))
(mmParams table17.mm_params
  (R4 "Complex NonTrend" (spread_bps 1296) (gamma 5.0) (max_pos 0.35)
   (action "Wide spreads, accept fills")))
(mmParams table17.mm_params
  (R5 "Complex Trend"    (spread_bps 1805) (gamma 5.0) (max_pos 0.23)
   (action "Widest spreads, min position")))

A.5   Epistemic annotations on principal claims
Claims are created from the measurement tables above and annotated with p-bit evidence states.

; Claim: Crypto uses all 6 regimes with high balance
(instance claim.crypto.all6 exmeta:Claim)

                                              21
(claimText claim.crypto.all6
  "Crypto inhabits all six regimes with high balance and
   high mean confidence.")
(supportedBy claim.crypto.all6 table6.crypto.regime_by_inst)
(supportedBy claim.crypto.all6 table5.crypto.labeldist)
(supportedBy claim.crypto.all6
  (summary table6.crypto.regime_by_inst (regime_balance_overall 0.4734)))

(instance ev.claim.crypto.all6 exmeta:EvidenceState)
(evidencePair ev.claim.crypto.all6 (p 0.93) (n 0.10))
(evidenceOf ev.claim.crypto.all6 claim.crypto.all6)

; Claim: Complex Trend is compressible in crypto (positive LLC)
(instance claim.crypto.R5.compressible exmeta:Claim)
(claimText claim.crypto.R5.compressible
  "Crypto Complex Trend (R5) is compressible: LLC is positive.")
(supportedBy claim.crypto.R5.compressible table8.crypto.llc)

(instance ev.claim.crypto.R5.compressible exmeta:EvidenceState)
(evidencePair ev.claim.crypto.R5.compressible (p 0.98) (n 0.05))
(evidenceOf ev.claim.crypto.R5.compressible claim.crypto.R5.compressible)

; Claim: No FX/commodity regime is compressible
(instance claim.fxcomm.none_compressible exmeta:Claim)
(claimText claim.fxcomm.none_compressible
  "FX/commodity LLC estimates are negative across regimes
   under this finite-dictionary estimator.")
(supportedBy claim.fxcomm.none_compressible table13.fxcomm.llc)

(instance ev.claim.fxcomm.none_compressible exmeta:EvidenceState)
(evidencePair ev.claim.fxcomm.none_compressible (p 0.90) (n 0.12))
(evidenceOf ev.claim.fxcomm.none_compressible
  claim.fxcomm.none_compressible)

; Claim: Cross-asset structure differs
(instance claim.crossasset.different_structure exmeta:Claim)
(claimText claim.crossasset.different_structure
  "Asset classes occupy different regions of regime space
   (distributions differ).")
(supportedBy claim.crossasset.different_structure
  table10.fxcomm.by_class)
(supportedBy claim.crossasset.different_structure
  table11.fxcomm.by_inst)

(instance ev.claim.crossasset.different_structure exmeta:EvidenceState)
(evidencePair ev.claim.crossasset.different_structure (p 0.92) (n 0.10))
(evidenceOf ev.claim.crossasset.different_structure
  claim.crossasset.different_structure)

                                       22
; Claim: Trading strategy estimates are indicative only
(instance claim.strategies.indicative_only exmeta:Claim)
(claimText claim.strategies.indicative_only
  "Strategy Sharpe/capacity numbers are indicative and
   not validated by full backtests.")

(instance ev.claim.strategies.indicative_only exmeta:EvidenceState)
(evidencePair ev.claim.strategies.indicative_only (p 0.95) (n 0.05))
(evidenceOf ev.claim.strategies.indicative_only
  claim.strategies.indicative_only)




                                       23