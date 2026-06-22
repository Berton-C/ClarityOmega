# |- and Atomspace Persistence: RESOLVED (no bug) + the verified workflow

**Status:** RESOLVED. The "marshalling bug" was never a bug. After two corrections
(documented below, because the error pattern is the lesson), the substrate behavior
is fully understood: `|-` computes but does not persist; only `add-atom` commits;
the boundary throw is a correct refusal of a non-string. No code fix is needed -- the
resolution is a usage workflow.
**Updated:** 2026-06-13 (supersedes earlier versions of this doc that claimed first a
marshalling bug, then a |- side-effect deposit -- both wrong; see section 0).
**Companion reference:** `NAL_and_the_Marshal_Boundary_Reference.md` (the durable
how-it-works guide). Point new threads there; this is the investigation record.

---

## 0. Two corrections, because the error pattern IS the lesson

This document was wrong twice, in opposite directions, before landing on the truth.
Recording both because the meta-lesson is more valuable than the conclusion.

**Wrong v1: "marshalling bug, fix the throw."** Claimed `|-` results were discarded
by a defect at the eval-result py-call boundary; proposed disambiguating Origin 1 vs
2 and stringifying with `repr`/`string-safe`. FALSE: the boundary refusing a compound
term is crash-safe-by-design (per `string_safe_encode_decode_asymmetry.md`), not a
defect. Calling it a bug was the first frame error.

**Wrong v2: "|- deposits to the atomspace as a side effect."** Over-corrected to claim
the derivation persists automatically and only the display fails. FALSE, killed by a
clean test: premises A->B and B->C both committed, `(|- ...)` computed A->C at 0.81,
`match` for A->C returned EMPTY. Premises present, derivation computed, nothing stored.
The "premises must be committed" rescue was tested and also failed -- premises WERE
committed.

**The truth (verified):** `|-` is a calculator, not a writer. It computes correct
derivations and stores nothing. Persistence is explicit `(add-atom space value)` and
nothing else. The boundary throw is correct (compound is not displayable text). All
three earlier claims -- "bug," "side-effect deposit," "type_error is cosmetic" -- were
frame errors caught by testing the specific claim directly.

## 1. The resolution: the verified workflow (from Patrick's NACE docs)

```
[1] (add-atom &self premise1)       ;; commit premises explicitly
    (add-atom &self premise2)
[2] (|- premise1 premise2)          ;; compute derived truth values (stores NOTHING)
[3] (add-atom &self derived-result) ;; commit the derivation explicitly
```

`|-` computes; you read the value; you choose to `add-atom` it. The deposit is never
automatic. This is the canonical pattern from `knowledge.metta` / `spaces.metta` in
the NACE docs -- the substrate's own authoritative source, not an inference of ours.

There is NO marshalling fix to build. The earlier Origin-1-vs-2 disambiguation and the
`repr`/`string-safe` proposal are MOOT -- they lived inside the mistaken "the throw is
a defect" frame.

## 2. The verified facts (do not re-litigate)

- `|-` computes correct NAL derivations (multiplicative-confidence deduction; plus
  lower-confidence abductive inverses). Confirmed many times.
- `|-` does NOT persist. Computation is not commitment. (Clean test, section 0.)
- `add-atom` is the only commit path. Direct eval does not persist either.
- Within a process life, add-atom'd atoms persist and `match` finds them (10 of 12
  sampled found on first match). Across a rebuild, `&self` dies by design; only
  ChromaDB `remember`s survive.
- The type_error/domain_error is a COMPUTATION OUTPUT shown through the display path,
  not a masked hit and not a formatting artifact. Clean result = present; clean `[]` =
  absent; error = a computed value being displayed.
- The boundary refusing a raw compound is correct (crash-safe by design).

## 3. The load-bearing discipline this produced

**`add-atom` in multi-command blocks silently partially-fails.** At least 2 of ~60
network atoms never committed, with no error -- consistent with Repair-1's documented
silent-goal-failure physics (a failing `let*` binding killed invisibly; per-directive
`findall` absorbs it).

RULE: never trust "I added N." Confirm "match finds N" in a SEPARATE command, count,
re-add misses. A built network is not real until match-count == intended. Prefer
small batches / per-atom commits for load-bearing state.

This is the night's durable lesson and it generalizes beyond `|-`: verify the
load-bearing substrate claim with a clean test before building on it. "It threw" is
not "broken"; "it computed" is not "persisted"; "I added N" is not "N exist."

## 4. The one question still worth asking Patrick (genuinely open)

A single `|-` call computes BOTH a forward deduction and a reverse abduction at lower
confidence. Now that we know `|-` stores NEITHER (you `add-atom` what you want to
keep), the earlier "forward persists, reverse doesn't" asymmetry was an ARTIFACT of
the false deposit premise -- there is likely nothing to explain there.

The remaining real question is narrower and architectural, for when knowledge-base
design matters: when you DO `add-atom` a derived result, should both the forward
deduction (belief) and the reverse abduction (conjecture) be committed, or is it
sound practice to commit only the deduction and treat abductions as provisional? That
is a NARS knowledge-hygiene question, not a substrate-behavior question -- worth
Patrick's view when building the knowledge architecture, not blocking anything now.

## 5. Cross-references

- `NAL_and_the_Marshal_Boundary_Reference.md` -- the durable how-it-works guide
  (the verified workflow, the Janus boundary physics, the add-atom silent-failure
  discipline, reading match results correctly). Point new threads there.
- `string_safe_encode_decode_asymmetry.md` -- why the boundary is crash-safe by
  design (the constraint that made "stringify across the boundary" wrong).
- Repair-1 substrate physics -- the silent-goal-failure mechanism that explains the
  multi-command add-atom miss rate.
