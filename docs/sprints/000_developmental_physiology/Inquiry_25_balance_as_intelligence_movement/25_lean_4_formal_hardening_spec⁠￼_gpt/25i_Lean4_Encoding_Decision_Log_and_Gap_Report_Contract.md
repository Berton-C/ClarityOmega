# 25i — Lean 4 Encoding Decision Log and Formalization Gap Report Contract
## Investigation 25

**Purpose:** Prevent implementation convenience from silently becoming project canon.

---

# 0. Required deliverables

The Lean formalizer must return two separate records:

1. **Encoding Decision Log**
2. **Formalization Gap Report**

They must not be merged into prose commentary.

---

# 1. Encoding Decision Log schema

For every nontrivial encoding choice record:

```text
DECISION-ID:
25f SECTION:
MATHEMATICAL PHRASE:
LEAN REPRESENTATION:
WHY THIS REPRESENTATION:
ALTERNATIVES CONSIDERED:
DOES IT STRENGTHEN 25f? yes/no
DOES IT WEAKEN 25f? yes/no
IS IT OBSERVATIONALLY EQUIVALENT IN M1-M3? yes/no/unknown
RATIFICATION REQUIRED? yes/no
```

Examples of choices that MUST be logged:

- dependent `Movement K K'` versus movement record with source/target fields;
- representation of material relations;
- profile carrier `V`;
- how `Adm24` is abstracted;
- whether `ReadApp` is inductive relation or partial/dependent function;
- definition of `FullyAppropriate`;
- representation of `NoDisqualifyingExcessForcing`;
- representation of participation-interface availability;
- how Stuck threshold is represented;
- how local contexts are represented in M3;
- how `ModelSufficient` is introduced;
- how provenance/generation kind prevent contact masquerade.

---

# 2. Formalization Gap Report schema

For every under-specification record:

```text
GAP-ID:
25f SECTION:
STATEMENT:
WHY LEAN CANNOT ENCODE IT UNIQUELY:
MINIMUM CHOICES:
CHOICE USED FOR TESTING (if any):
NEW ASSUMPTION REQUIRED?:
WOULD THAT ASSUMPTION BECOME CANON?:
AFFECTS M1/M2/M3?:
BLOCKS FORMAL HARDENING? yes/no
RECOMMENDED PROJECT RULING:
```

---

# 3. Gaps that are expected rather than hidden

The following are already explicitly provisional in 25f and SHOULD appear as gaps/abstract interfaces if Lean needs them:

- exact numeric metric for `E_force`;
- exact universal carrier `V`;
- exact semantic implementation of `ReadApp`;
- complete awareness/meta-awareness mathematics;
- complete Soul mathematics;
- physical-energy grounding maps.

Do not “solve” these silently.

---

# 4. Strengthening warning

The most dangerous formalization error is:

> proving the theorem by encoding a stronger premise than 25f ratified.

Examples:

- making `ModelSufficient` include `HarmonicOutcome`;
- making `Adm25` include the final Appropriateness reading rather than evidence for it;
- defining `MaterialTo` as membership in the movement;
- defining Stuck as a label with no threshold witnesses;
- making all future interface modes available at every cut;
- making Relatedness/Precision floors vacuous by requiring no material items.

Any such choice must be rejected or explicitly returned for ratification.

---

# 5. Weakening warning

Also reject formalizations that erase distinctions:

- Soul standing as ordinary data;
- all energy kinds as `Nat`;
- contact provenance as a string;
- R/A/P as three floats;
- `ReadApp` as arbitrary boolean;
- Fourthness as `relations.length ≥ 3`;
- Stuck as `SNSLike = true`.

The goal is not merely compilation.

The goal is faithful type structure.

---

# 6. Compiler-generated issues

Mechanical Lean issues such as:

- inference ambiguity;
- universe levels;
- decidability instances;
- reserved names;
- coercion syntax;
- termination;
- simplifier lemmas

do not count as mathematical gaps unless resolving them forces a semantic choice.

They should be listed separately as:

```text
MECHANICAL FIXES
```

with exact diffs.

---

# 7. Final disposition categories

Every gap must end in exactly one of:

```text
RESOLVED-MECHANICAL
RESOLVED-FAITHFUL-ENCODING
PROVISIONAL-ENCODING
REQUIRES-RATIFICATION
OUTSIDE-INVESTIGATION-25
BLOCKING-CONTRADICTION
```

This keeps proof engineering from blurring epistemic status.

---

# 8. Investigation-25 reopening rule

Investigation 25 is reopened only for:

- `REQUIRES-RATIFICATION` issues that materially affect the ratified object;
- `BLOCKING-CONTRADICTION`.

It is not reopened for ordinary Lean syntax or implementation convenience.

---

**END — 25i ENCODING/GAP CONTRACT**
