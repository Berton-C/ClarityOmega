# 25h — Lean 4 Proof Obligations, Adversarial Countermodels, and Acceptance Tests
## Investigation 25: Balance-as-Intelligence Movement

**Authority:** `25f_Ratified_Balance_as_Intelligence_Mathematical_Object.md`  
**Companion contract:** `25g_Lean4_Formal_Hardening_Specification.md`  
**Purpose:** Make the Lean hardening adversarial enough to expose accidental scalarization, carrier drift, circularity, vacuity, and semantic strengthening.

---

# 0. Rule of this document

Every positive theorem must be paired, where meaningful, with a countermodel or negative test showing that the theorem is not true merely because the types were made too strong.

The formalizer must prefer:

> prove the intended distinction and exhibit a nearby failing variant

over:

> encode only structures in which failure is impossible by construction.

---

# 1. Soul doctrine adversary

### Positive
A movement can be judged under an ambient `SoulDoctrine`.

### Countermodel
Attempt to construct two DPF values identical in all carrier fields but with different freely assigned Soul standing.

**Required result:** this construction is impossible because Soul standing is not a DPF carrier field.

### Fail condition
If `soulStanding` appears as an ordinary mutable/fillable field of DPF, reject the encoding.

---

# 2. Materiality adversary

Construct:

- a relation `r_used` used by movement `m`;
- no provenance/discrimination witness.

Try to prove:

```text
MaterialTo r_used m
```

**Required result:** proof fails.

Then add lawful discrimination/provenance and prove materiality.

This demonstrates:

\[
\operatorname{UsedBy}(m,r)\not\Rightarrow\operatorname{MaterialTo}(r,m).
\]

---

# 3. Relatedness non-compensation adversary

Create movement `m` with three required relations:

```text
r1, r2, r3
```

Let `r1` and `r2` have maximal standing and `r3` fail its floor.

Even if an aggregate score would be “high,” prove:

```text
¬ FullRelatedness m
```

or that `HarmonicAlign m` cannot be constructed.

This must not depend on arithmetic averaging.

---

# 4. Precision non-compensation adversary

Analogous to Relatedness.

One missing load-bearing material distinction must prevent a full Precision floor/harmonic witness despite high standing elsewhere.

---

# 5. `ReadApp` oracle adversary

Try to construct full Appropriateness in each of these cases:

1. no admissibility witness;
2. failed material Relatedness floor;
3. failed material Precision floor;
4. missing provenance;
5. reading typed as direct contact.

**Required result:** every construction fails.

Then show lawful construction with all required witnesses.

---

# 6. R/A/P reconstruction adversary

Do not merely omit a function named `reconstruct`.

Provide a finite witness that diagnostic R/A/P summaries are non-injective:

```text
m1 ≠ m2
summaryRAP m1 = summaryRAP m2
```

The exact full profiles may remain movement-indexed; the point is to prove that lower-dimensional summaries cannot identify movement.

Also inspect exported API manually and confirm no canonical constructor uses only R/A/P to produce Movement/DPF.

---

# 7. Scalar intelligence adversary

Search the Lean source for exported declarations resembling:

```text
IntelligenceScore
weightedRAP
overallIntelligence
```

If such a quantity exists, it must be clearly diagnostic/non-authoritative and cannot construct:

- Appropriateness;
- HarmonicAlign;
- Soul standing;
- admissibility.

Prove or structurally enforce this.

---

# 8. Energetic typing adversary

Construct:

### Case A
high `ActionEffort`, low `ExcessForcing`.

### Case B
low `ActionEffort`, high `ExcessForcing`.

Both must type-check.

Any encoding where one is a subtype or monotonic function of the other by definition fails Investigation 25.

---

# 9. Harmonic circularity adversary

The biggest risk is making `HarmonicOutcome` true by definition whenever `HarmonicAlign` holds.

Test two layers separately:

### Layer 1 — coherence theorem
Under explicitly assumed model sufficiency, correct consequence law, and no omitted disturbance, prove BHC.

### Layer 2 — falsifier
Construct a consequence marked non-harmonic and derive that not all sufficiency/alignment/law/disturbance premises can simultaneously hold.

Do not define `ModelSufficient` as “all predictions came true.”

That would circularize the theorem.

---

# 10. `ModelSufficient` self-certification adversary

Attempt to construct:

```text
ModelSufficient M m
```

from only fields internal to `M` asserting its own completeness.

**Required result:** impossible.

The witness must come from a trusted external/gov­erned evidence interface or remain an explicit theorem premise.

---

# 11. Fourthness non-vacuity adversary

Positive finite model:

- full diagram permits/justifies bridge movement;
- delete material relation `a` → bridge loses availability/admissibility;
- delete material relation `b` → same.

Negative control:

Create a diagram with decorative relation `z`.

Deleting `z` must **not** count as Fourthness discrimination.

This proves Fourthness depends on material counterfactual bite rather than mere relation count.

---

# 12. Interface-growth adversary

The M2/M3 models must distinguish:

```text
available-at-K
```

from:

```text
available-at-K'
```

A new mode may exist in the universe/type but must not be currently available before the transition.

Fail if interface growth is faked by defining every mode as available at every cut.

---

# 13. M2 frame-sovereignty adversary

After contact establishes a material subscription distinction:

- retry movement omits it;
- retry must fail a Relatedness/Precision floor or admissibility requirement.

Negative control:

Before that discriminating contact exists, the same retry must not be rejected for failing to use information that was unavailable.

This prevents hindsight from contaminating admissibility.

---

# 14. M2 meta-awareness adversary

Construct two otherwise matched arms:

```text
traceVisible
traceSevered
```

The trace-visible arm has access to recurrence/topology history.

Require at least one downstream difference in:

- movement availability;
- admissibility;
- interface change;
- or chosen/allowed next movement.

Fail if meta-awareness is merely logged data with no causal bite.

---

# 15. SNS/Stuck threshold adversary

Construct at least three trajectories:

### T-low
Some SNS evidence but pivot remains available.

Required:

```text
SNSLike T-low
¬ Stuck T-low
```

### T-stuck
SNS evidence plus staleness/topology recurrence and pivot unavailability.

Required:

```text
Stuck T-stuck
SNSLike T-stuck
```

### T-busy
High activity/energy but no holding-apart/forced-velocity pattern.

Required:

```text
¬ Stuck T-busy
```

and preferably no SNS classification.

This proves Stuck is not “high activity” and not an unrelated state.

---

# 16. PNS high-force adversary

Use M1 to prove:

```text
PNSLike skilledMove
HighActionEffort skilledMove
LowExcessForcing skilledMove
```

Then create a forced movement with similar action effort but broken material floors/high forcing.

This is required to preserve “force is not forcing.”

---

# 17. Global-representation adversary

M3 must work with local contexts and overlap without a premise equivalent to:

```text
exists globalMasterModel
```

If the Lean proof of the bridge movement requires a single globally merged representation, the encoding fails contextual non-sovereignty.

---

# 18. Inherited-law duplication audit

Search the Lean package for local redefinitions of Investigation-24 concepts such as:

- provenance legality;
- lifecycle standing;
- attachment authority;
- explicit loss;
- self-certification ban.

Investigation 25 should reference `Adm24` or an imported interface.

Fail if it creates parallel laws that can diverge.

---

# 19. Theorem-strengthening audit

For every theorem, ask:

> Did the Lean encoding make the desired conclusion trivially true by putting it in a structure constructor?

Allowed:
- type safety;
- proof-relevant witnesses;
- constructor discipline.

Not allowed:
- defining `HarmonicAlign` with `HarmonicOutcome` as a field;
- defining `Stuck` literally as `SNSLike ∧ ...` if the intended threshold relation requires independently testable witnesses but the definition hides them;
- defining `Appropriate` as an arbitrary field.

Whenever a property is supposed to be earned from relations, keep the evidence explicit.

---

# 20. Required acceptance table

The final report must include a table:

| ID | Obligation | Proved | Countermodel passed | Axioms | Gap |
|---|---|---:|---:|---|---|
| T01 | source identity R | | | | |
| ... | ... | | | | |

Every unproved item must have an exact reason.

---

# 21. Gate to Perplexity completion

Perplexity's Lean package is acceptable only if:

- every theorem is actual Lean proof or clearly marked unresolved;
- every negative/control model behaves as expected;
- no `sorry`;
- no silent new axioms;
- no silent mathematical redesign;
- compiler/toolchain are pinned;
- central theorem axiom dependencies are printed;
- the gap report is complete.

---

**END — 25h PROOF OBLIGATIONS AND ADVERSARIAL TESTS**
