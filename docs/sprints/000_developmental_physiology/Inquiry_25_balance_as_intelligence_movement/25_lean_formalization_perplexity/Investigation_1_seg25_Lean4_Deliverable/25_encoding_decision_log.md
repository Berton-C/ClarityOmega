# 25 — Encoding Decision Log

## Investigation 25: Balance-as-Intelligence Movement — Lean 4 hardening

Schema per `25i_Lean4_Encoding_Decision_Log_and_Gap_Report_Contract.md` §1. This log is a separate record from the gap report and from prose commentary, as §0 of `25i` requires.

---

### DECISION-01

**25f SECTION:** §0, §4 (the boxed `𝔅_K=(D_K,Ω_K,I_K,W_K,C^{Soul}_K)` object and `Movement K K'` typing).
**MATHEMATICAL PHRASE:** "`Movement` must be cut-indexed or carry typed source/target cuts... a preferred shape is dependent `Movement (K K' : Cut)`" (25g §2); every further primitive `25g §2–§17` demands (`Relation`, `Distinction`, `Mode`, `Adm24`, energetics, ReadApp components, PNS/SNS witnesses, ...).
**LEAN REPRESENTATION:** every one of these primitive types/relations is bundled as a field of a single `structure Sig`, and every definition/theorem in `Core.lean` takes an explicit `(S : Sig)` argument instead of free-standing `variable {K K'} {Movement} ...` binders.
**WHY THIS REPRESENTATION:** free-standing `variable {K K' : Cut}` binders mixed with several mutually-dependent relation variables caused unresolvable metavariables under `leanprover/lean4:v4.33.0-rc2`'s elaborator. Bundling into one record parameter is a standard "locale"-style pattern for large abstract developments and sidesteps the metavariable failure entirely.
**ALTERNATIVES CONSIDERED:** (a) free-standing section `variable`s (rejected — elaboration failure); (b) a type class instead of a plain structure argument (rejected — type classes would make `Sig` implicit and ambiguous once M1/M2/M3 all instantiate it in the same file, risking accidental instance mixing across models); (c) five separate smaller bundles by concern (rejected — 25g §23 clause 3 requires "all three finite models use one unchanged semantics," which is easiest to state and check as one shared `Sig` type).
**DOES IT STRENGTHEN 25f? no.** Every field is exactly the primitive 25g asks for, under an explicit parameter instead of an implicit section variable — no mathematical content changes.
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? yes.** All three models instantiate the identical `Sig` record type; nothing about bundling vs. free variables is visible in any theorem statement.
**RATIFICATION REQUIRED? no.** Pure Lean-engineering choice.

---

### DECISION-02

**25f SECTION:** §7, §8 (`Rel_K(m):R_K^{mat}\to V`, `Prec_K(m):Δ_K^{mat}\to V`).
**MATHEMATICAL PHRASE:** the universal profile carrier `V`.
**LEAN REPRESENTATION:** `V := Standing`, a three-valued inductive (`full`/`partialStanding`/`absent`), with `MeetsFloor s := (s = Standing.full)`.
**WHY THIS REPRESENTATION:** 25f §23 explicitly lists the exact carrier `V` as provisional/deferred — no ratified richer structure exists to encode. A concrete three-point lattice is the minimal carrier that can (a) express a genuine "floor" (something strictly weaker than the maximum), and (b) support the non-compensation theorems (T05/T06), since nothing but `= full` is ever inspected by any theorem.
**ALTERNATIVES CONSIDERED:** (a) `V := Nat` or `V := ℝ`-style ordered scalar (rejected — 25g §7/§8 explicitly forbid encoding Relatedness/Precision as a scalar); (b) `V := Bool` (rejected — 25i §5 explicitly warns against "R/A/P as three floats" but also against collapsing standing to a plain boolean, which would erase the `partialStanding` distinction that 25f's prose implies exists); (c) an abstract opaque `V : Type` field of `Sig` with only an `IsFloorMet : V → Prop` predicate (considered seriously — would be maximally faithful to "provisional," but would make every finite-model proof depend on an unconstrained abstract predicate, weakening the finite models' concreteness with no compensating benefit, since the theorems never need more than the three-point structure).
**DOES IT STRENGTHEN 25f? no** — any ordered/richer `V` would still validate every theorem below verbatim, since nothing but `= full` is ever inspected.
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? yes.**
**RATIFICATION REQUIRED? yes** — logged in the gap report as GAP-02, since the *exact* carrier is genuinely undetermined by 25f and a future ratification could pick a different (e.g. richer ordered) `V` without changing any theorem here, but the choice is still a concrete stand-in that should be acknowledged, not silently treated as canon.

---

### DECISION-03

**25f SECTION:** §17 ("staleness, forward movement, or the capacity to pivot is ... unavailable").
**MATHEMATICAL PHRASE:** the threshold-crossing condition for `Stuck`.
**LEAN REPRESENTATION:** `Stuck S τ := SNSLike S τ ∧ (StaleForwardMotion τ ∨ PivotUnavailable τ)` — disjunctive reading.
**WHY THIS REPRESENTATION:** the surface grammar of 25f §17 ("X, Y, or Z is unavailable") most naturally reads as "at least one of X/Y/Z," i.e. disjunction; this is the reading that makes `Stuck` easiest to *reach* (any one witness suffices) while still requiring the independent `SNSLike` conjunct.
**ALTERNATIVES CONSIDERED:** conjunctive reading (`StaleForwardMotion ∧ PivotUnavailable`) — would make `Stuck` strictly harder to establish and is an equally grammatically defensible parse of "or" in informal mathematical prose (informal "or" sometimes means "and/or" ambiguously).
**DOES IT STRENGTHEN 25f? possibly** — the disjunctive reading makes `Stuck` easier to satisfy than the conjunctive reading would, which is a genuine, non-cosmetic semantic fork.
**DOES IT WEAKEN 25f? no**, relative to the conjunctive alternative, but this is exactly the point: the two readings are not equivalent, so a real choice was made.
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? unknown** — `T_adv15_tStuck`'s witness trajectory happens to satisfy both `StaleForwardMotion` and `PivotUnavailable` simultaneously, so the disjunctive vs. conjunctive choice is not distinguished by any trajectory actually constructed in this package. A future finite model with staleness-but-pivot-available (or vice versa) would distinguish them.
**RATIFICATION REQUIRED? yes** — logged as GAP-09.

---

### DECISION-04

**25f SECTION:** §24 (evidence-already-earned examples), 25h §2–§10/§15–§16 (model-agnostic adversaries).
**MATHEMATICAL PHRASE:** n/a (a packaging choice, not a mathematical-content choice).
**LEAN REPRESENTATION:** M1 hosts not only its own §18-required content (skilled/forced-high-high contrast) but also several 25h adversarial countermodels that are not specific to any one finite interpretation (materiality, Relatedness/Precision non-compensation, `ReadApp` oracle, R/A/P non-injectivity, energetic typing, BHC/`ModelSufficient`, SNS/Stuck threshold) — rather than building eight separate throwaway `Sig` instances, one per adversary.
**WHY THIS REPRESENTATION:** these adversaries test properties of the *shared* `Sig`/`Core.lean` machinery, not properties unique to a particular model's narrative; reusing one sufficiently rich model keeps the amount of finite-model boilerplate proportional to the task while still giving each adversary a genuine, independently checkable witness inside a real instantiated `Sig`.
**ALTERNATIVES CONSIDERED:** one dedicated minimal `Sig` per adversary (rejected — would multiply the file by roughly 8x with no proof-strength benefit, since each such `Sig` would just be M1's relevant fragment in isolation).
**DOES IT STRENGTHEN 25f? no.**
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? n/a** (packaging choice; does not change what is proved, only where it lives).
**RATIFICATION REQUIRED? no.**

---

### DECISION-05

**25f SECTION:** §15–§17 (PNS-like, SNS-like, Stuck).
**MATHEMATICAL PHRASE:** "PNS-like organization" / "SNS-like organization" as properties of a movement's *trajectory* through cuts.
**LEAN REPRESENTATION:** `PNSLike`, `SNSLike`, `Stuck` are all predicates on `Sig.Trajectory`, a type distinct from `Sig.Movement K K'`, not on `Movement` itself.
**WHY THIS REPRESENTATION:** 25f's prose describes PNS/SNS/Stuck as properties of an *ongoing* pattern across (potentially many) movements/cuts, not a single movement's one-shot admissibility — a single `Movement K K'` is a single edge, whereas "holding apart + forced velocity" (§16) and "staleness of forward motion" (§17) are properties that only make sense of a path/history. Introducing `Trajectory` as its own primitive type (rather than overloading `Movement`) keeps this distinction visible in the type system itself.
**ALTERNATIVES CONSIDERED:** defining PNS/SNS/Stuck directly on `Movement K K'` (rejected — would conflate single-edge admissibility with path-level organization, and 25f §15's nine witnesses read naturally as trajectory properties, e.g. "self-weaving plasticity" is not meaningful for one atomic movement).
**DOES IT STRENGTHEN 25f? no.**
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? yes** — all three models declare a `Trajectory` type independently of `Movement`.
**RATIFICATION REQUIRED? no** — this is the only representation that keeps 25g §16's "structured predicates over movement/trajectory evidence" and §17's threshold language coherent without inventing new ontology beyond what §15–17 already name.

---

### DECISION-06

**25f SECTION:** n/a (packaging/tooling deviation from `25j`'s required file list, not a 25f mathematical clause).
**MATHEMATICAL PHRASE:** n/a.
**LEAN REPRESENTATION:** the project uses `lakefile.toml` instead of the `lakefile.lean` named in the `25j` handoff prompt's required package layout.
**WHY THIS REPRESENTATION:** `lakefile.toml` is Lake's declarative TOML configuration format, functionally equivalent to a `lakefile.lean` for this project's needs (three `lean_lib` targets plus one `lean_exe`, no custom build steps or dependency-fetching logic that would require Lean-level scripting). TOML was used because it is less error-prone for a static target list and avoids a class of Lean-level lakefile elaboration issues encountered in earlier iterations of this exact toolchain.
**ALTERNATIVES CONSIDERED:** rewriting as `lakefile.lean` (would work equivalently for this project's simple target list; not done because no functional gap was found and 25j's own preamble treats the file list as a required *shape*, and `lakefile.toml` occupies the identical structural role).
**DOES IT STRENGTHEN 25f? no.**
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? n/a.**
**RATIFICATION REQUIRED? no** — but logged here as an explicit, non-hidden deviation from the literal `25j` file list per the handoff prompt's own instruction to document any such discrepancy rather than silently substitute.

---

### DECISION-07

**25f SECTION:** §13/§17 via 25h §13 (M2 frame-sovereignty adversary, hindsight fairness).
**MATHEMATICAL PHRASE:** "before that discriminating contact exists, the same retry must not be rejected for failing to use information that was unavailable" (25h §13 negative control).
**LEAN REPRESENTATION:** `Distinction K0` and `Distinction K2` in M2 are empty types (zero constructors); only `Distinction K1` has the single constructor `subscription`.
**WHY THIS REPRESENTATION:** making the *absence* of the discriminating distinction a type-level fact (rather than merely a `Prop`-level "this distinction is not required yet") is the strongest available way to prevent hindsight from contaminating admissibility: `retryBefore`'s `AllPrecFloors` obligation is discharged by `fun d => nomatch d`, i.e. it is not merely unpenalized by a chosen definition, it is *impossible to state a floor obligation about a distinction that does not exist at that cut*.
**ALTERNATIVES CONSIDERED:** a single `Distinction : Type` (not cut-indexed) with a Prop-valued "was available at this cut" predicate deciding whether `RequiredDist` can be `True` (rejected — this is exactly the weaker, Prop-level version that 25i §4's strengthening warning would flag as risking a hidden convenience: it would make the negative control pass only because of how a predicate happened to be *defined*, rather than because the type itself has no witness to omit).
**DOES IT STRENGTHEN 25f? no** — this is a faithful reading of 25f's cut-indexed `Δ_K` (25f §8: `Δ_K^{mat}`, a *per-cut* material distinction set), not an addition to it.
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? unknown** — M1's `Distinction` is not cut-empty anywhere (all three of `d1,d2,d3` live at the single cut `K` M1 uses), and M3's `Distinction` is empty at *every* cut (M3 targets relations, not distinctions), so this specific "empty at K0/K2, inhabited only at K1" pattern is unique to M2; whether a hypothetical M4 would need the same pattern is unknown.
**RATIFICATION REQUIRED? no** — this is a direct, non-strengthening instantiation of 25f §8's existing cut-indexing, not a new assumption.

---

### DECISION-08

**25f SECTION:** §17 (via 25h §17, global-representation adversary).
**MATHEMATICAL PHRASE:** M3 "must work with local contexts and overlap without a premise equivalent to `exists globalMasterModel`."
**LEAN REPRESENTATION:** `M3.WorldModel := Empty`.
**WHY THIS REPRESENTATION:** rather than merely *not constructing* a global model witness in the M3 proofs (which would leave open the possibility that one could be constructed, just wasn't), making `WorldModel` literally uninhabited in M3's `Sig` instance proves the stronger, cleaner claim: no global master model can exist *even in principle* in this model, and the bridge movement (`bridgeMove`) is still fully `Adm25`-admissible without ever touching `WorldModel`. This is the most adversarially strong available demonstration of contextual non-sovereignty.
**ALTERNATIVES CONSIDERED:** `WorldModel := Unit` with no proof ever invoking it (rejected — weaker: leaves it merely unused rather than provably unusable, which is a real difference an adversarial reviewer could challenge); `WorldModel` as some inhabited type with an explicit non-merging axiom (rejected — would require inventing new axiomatic content, which 25g/25h forbid without ratification).
**DOES IT STRENGTHEN 25f? no** — 25f itself never posits a `globalMasterModel`; this encoding *removes* a possible smuggled premise, it does not add one.
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? no** — M1 and M2 both use `WorldModel := Unit`/inhabited types (M1's BHC theorems genuinely need `goodModel`/`badModel` values), so this is a deliberate, model-specific divergence, logged rather than silently applied everywhere.
**RATIFICATION REQUIRED? no** — this is a strictly *conservative* encoding relative to 25f/25h's own requirement, not a new assumption.

---

### DECISION-09

**25f SECTION:** §18 (via 25g §17 / 25h §12, interface-growth adversary).
**MATHEMATICAL PHRASE:** "a new mode may exist in the universe/type but must not be currently available before the transition... do not fake interface growth by defining every mode as available at every cut."
**LEAN REPRESENTATION:** in both M2 and M3, `AvailableAt {K} (_ : Mode K) : Prop` is defined by an explicit `match K with | ... => False | ... => True` on the cut itself, rather than returning `True` unconditionally or via any path that could accidentally default to `True` everywhere.
**WHY THIS REPRESENTATION:** matching on the cut is the only way to make the "not available before, available after" asymmetry a checkable fact rather than an assumed one — `T20_interface_growth_not_faked`/`T23_interface_growth_not_faked` explicitly prove `¬ AvailableAt (mode at the pre-transition cut)`, which would be false (and hence unprovable) if `AvailableAt` returned `True` unconditionally.
**ALTERNATIVES CONSIDERED:** a `Sig`-level opaque `AvailableAt` field left as a hypothesis in every theorem needing it (rejected — would push the "not faked" burden onto every caller instead of proving it once per model, and 25h §12 explicitly requires a fail-if-faked check, which is best enforced structurally at definition site).
**DOES IT STRENGTHEN 25f? no.**
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? yes** — M2's and M3's `AvailableAt` are structurally identical in shape (match-on-cut, `False` pre-transition / `True` post-transition), differing only in cut names; M1 does not exercise `AvailableAt` non-trivially (`M1.AvailableAt := fun _ => True`, since M1's adversarial focus is energetics/floors, not interface growth — logged as GAP-11, since this makes M1's `AvailableAt` field vacuous by omission rather than by a proved fact).
**RATIFICATION REQUIRED? no.**

---

### DECISION-10

**25f SECTION:** §4.2/§11 (Fourthness/overlap) via 25h §11 (Fourthness non-vacuity adversary).
**MATHEMATICAL PHRASE:** "Fourthness depends on material counterfactual bite rather than mere relation count" — the negative-control requirement that deleting a *decorative* relation must not count as Fourthness discrimination.
**LEAN REPRESENTATION:** M3's `Relation LA` has three constructors, `a`/`b` (material: `RequiredRel = True`, `DiscriminatesRel = True`) and `z` (decorative: `RequiredRel = False`, `DiscriminatesRel = False`), with four `LA → Bridge` movements exercising all four combinations (full diagram; missing `a`; missing `b`; missing `z`).
**WHY THIS REPRESENTATION:** the material/decorative split must be encoded at the level of the *required-ness* predicate (`RequiredRel`), not merely by informal naming, since `RelFloor`'s non-compensation (T05) is specifically gated on `RequiredRel` — this is what makes `m3_missingZ_not_penalized` a genuine, non-trivial proof (that deleting `z`'s standing does not break `AllRelFloors`) rather than a renamed tautology.
**ALTERNATIVES CONSIDERED:** counting relations (`|Relation LA| ≥ n`) as a Fourthness proxy (explicitly forbidden by 25i §5: "Fourthness as `relations.length ≥ 3`"); a single boolean `isDecorative` field on `Relation` inspected ad hoc (rejected — `RequiredRel`/`DiscriminatesRel` already exist as the canonical 25g-mandated predicates for exactly this purpose, so introducing a parallel boolean would duplicate law rather than reuse it, risking the two diverging).
**DOES IT STRENGTHEN 25f? no.**
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? no** — M1 has no decorative/material relation split (all of M1's required relations are uniformly `True`); this split is specific to M3's Fourthness narrative.
**RATIFICATION REQUIRED? no.**

---

### DECISION-11

**25f SECTION:** n/a (25g §19 required theorem-inventory naming, not a 25f mathematical clause).
**MATHEMATICAL PHRASE:** `T12 high_action_low_force_consistent` (25g §19's required theorem-family name).
**LEAN REPRESENTATION:** no Lean declaration in the package is named `T12` or `high_action_low_force_consistent`; the *mathematical content* 25g §19 asks for — a movement exhibiting simultaneously high `ActionEffort` and low `ExcessForcing` — is proved by `M1.T18_energetic_case_A_skilled` (part of the T18 `M1_acceptance` family) instead.
**WHY THIS REPRESENTATION:** T18 (`M1_acceptance`, 25g §18) already required constructing exactly this witness as part of M1's acceptance obligations ("high `ActionEffort`, low `ExcessForcing`, `HarmonicAlign`... for a skilled movement"), so the content of T12 was proved once, under T18's declaration name, rather than duplicated under a second name with an identical proof term.
**ALTERNATIVES CONSIDERED:** adding a second declaration `T12_high_action_low_force_consistent := T18_energetic_case_A_skilled.1` as a pure alias (considered, not done — would satisfy the letter of the naming inventory at the cost of a redundant declaration with no new content; noted here instead so the correspondence is explicit and auditable).
**DOES IT STRENGTHEN 25f? no.**
**DOES IT WEAKEN 25f? no.**
**IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? n/a** (naming/organizational choice only).
**RATIFICATION REQUIRED? no** — logged in the build/axiom report's acceptance table as a naming deviation with content fully discharged, per 25i §6's rule that mechanical/organizational issues are not mathematical gaps unless they force a semantic choice (this one does not).

---

## Mechanical Lean-engineering fixes

(Per `25i` §6: listed separately from the decision log proper — these are compiler/elaborator issues, not semantic choices, but recorded here with exact diffs since no dedicated section exists elsewhere in this file set for them; the same list also appears as build notes in `25_build_and_axiom_report.md`.)

**MECHANICAL-01 — bare-constructor auto-bound-implicit.**
Symptom: referencing bare `Movement` constructor names (e.g. `skilled`, `matUsedOnly`) inside a theorem's *type* caused Lean 4's auto-bound-implicit feature to silently reinterpret the unresolved lowercase identifier as a fresh implicit variable rather than raising a name-resolution error, producing a cascade of spurious "expected type must not contain free variables" / type-mismatch errors.
Fix: `open Movement` (and, in M2, additionally `open Distinction Mode`) at the top of each model namespace, so bare constructor names resolve as ordinary terms.
```diff
 namespace M1
 ...
+open Movement
 
 theorem m1_materiality_used_not_material :
```

**MECHANICAL-02 — structure-projection reducibility for `rfl`/`decide`.**
Symptom: `rfl`/`decide`-based proofs about `sig.someField` failed to reduce because the `sig`/`doctrine` `def`s were not transparent enough for the elaborator's definitional-unfolding at default transparency.
Fix: mark every model's top-level `sig`/`doctrine` definitions `@[reducible]`.
```diff
-def sig : Sig where
+@[reducible] def sig : Sig where
   ...
-def doctrine : sig.SoulDoctrine := ()
+@[reducible] def doctrine : sig.SoulDoctrine := ()
```
Applied proactively to `sig2`/`doctrine2` (M2) and `sig3`/`doctrine3` (M3) from first draft.

**MECHANICAL-03 — `unfold` single-pass vs. `simp only` fixed-point.**
Symptom: a single `unfold` call on nested `Sig`-projected definitions (e.g. `SNSLike`, `Stuck`, their constituent `HoldingApart`/`ForcedVelocity`/etc.) unfolds only one layer, leaving deeper definitional layers opaque to the subsequent `decide`.
Fix: use `simp only [<all constituent lemma/def names>]` (a fixed-point rewriter) immediately before `decide` in the M1 SNS/Stuck threshold theorems (`T_adv15_tLow`/`T_adv15_tStuck`/`T_adv15_tBusy`), rather than `unfold`.

**MECHANICAL-04 — `Decidable` instance synthesis failure on non-reducible `Prop`-valued helper `def`s.**
Symptom: `by decide` failed with "failed to synthesize `Decidable P`"/"`Decidable ¬P`" on goals built from plain `Prop`-valued helper `def`s (e.g. `AvailableAt`, `RequiredRel`) even though the underlying `Sig` instance was already `@[reducible]` — because typeclass/instance-transparency search does not unfold ordinary `def`s the way `rfl`/kernel-reduction does. Root cause is the same underlying transparency issue as MECHANICAL-02, but manifesting through the `decide` tactic's instance search rather than through `rfl`.
Fix: replace `by decide` with direct term-mode proofs that force defeq-checking at default transparency via type ascription, e.g.:
```diff
-theorem T20_interface_growth_not_faked : ¬ AvailableAt (Mode.modeAt (K := Cut.K0)) := by decide
+theorem T20_interface_growth_not_faked : ¬ AvailableAt (Mode.modeAt (K := Cut.K0)) := fun h => h
```
and, for eliminating a hypothesis whose stated type reduces to `False`:
```diff
-  | .z, hreq => exact absurd hreq (by decide)
+  | .z, hreq => exact (hreq : False).elim
```
Plain equality-typed goals over concrete inductive types (e.g. `Standing.absent ≠ Standing.full`) are unaffected by this bug — `DecidableEq` instances for concrete inductives resolve via ordinary instance search regardless of how the compared terms were produced, so `by decide` remains correct and is kept for those.

**MECHANICAL-05 — "ambiguous namespace" warning on `open Relation`.**
Symptom: `open Relation Mode` inside M3's namespace produced an "ambiguous namespace" warning, because Lean 4 core already declares a top-level `Relation` namespace (`Relation.ReflTransGen`, etc.).
Fix: simply omit the `open` for `Relation` — every constructor reference in M3 was already either fully qualified (`Relation.a`) or used bare dot-notation (`.a`/`.b`/`.z`), which resolves via expected-type elaboration without needing an explicit `open` at all.
```diff
-open Relation Mode
```
(no replacement needed; the line is deleted, not replaced)

**MECHANICAL-06 — equation-compiler `match` sugar vs. explicit `fun`/`match`.**
Symptom: functions of apparent shape `∀ {K K' : Cut}, Movement K K' → ... := | pat => ...` (equation-compiler sugar) triggered a genuine elaborator bug whenever the `Cut` inductive's own constructors share names with the implicit binder names (`K`, `K'`) — the anonymous-constructor `.ctor` notation in match arms was resolved against `Cut` instead of `Movement`/`Relation`/etc., producing spurious `unknownIdentifier` errors.
Fix: write every such function as `{K K' : Cut} (m : Movement K K') ... := match m ... with | pat => ...` (explicit `fun`/`match`) instead of equation-compiler sugar, throughout `Models.lean`.
