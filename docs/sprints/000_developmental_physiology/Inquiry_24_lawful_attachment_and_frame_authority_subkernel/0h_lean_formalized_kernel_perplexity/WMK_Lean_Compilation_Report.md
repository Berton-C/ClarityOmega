# WMK Canonical Kernel — Lean Compilation Report

## Bottom line

`0h_WMK_Canonical_Hardened.lean` now compiles cleanly under Lean 4
(`v4.33.0-rc2`) with the `batteries` library (the current name for `Std`).
5 small, surgical fixes were needed — none of them touch the mathematical
content of your kernel. Every theorem in the file, including the finite
"Mattermost" model and the central `authoritative_implies_governing_package`
theorem, is now a genuine, kernel-checked proof with **no `sorry` anywhere**.

## The 5 fixes

| # | Location | Issue | Fix |
|---|----------|-------|-----|
| 1 | `ContactSeal`/`ContactRecord`/`Provenance.contact`/`mmSeal` | The field name `seal` collides with a keyword introduced in recent Lean versions | Renamed the field to `sealF` everywhere it's used (4 sites) |
| 2 | `mmBefore_irrefl` and friends (`by decide`) | `mmBefore` is a plain `def`, so typeclass search couldn't find a `Decidable` instance for it | Added one instance: `instance mmBefore.decidable ... := by unfold mmBefore; infer_instance` |
| 3 | `availability_has_semantic_witness`, `mmRecovery`, `MattermostModelWitness.recovery` | `AvailabilityTransition`'s `Event` type parameter only appears in the structure's own field, never in any of its arguments, so Lean can't infer it | Added an explicit `(Event := ...)` annotation at all 3 use sites |
| 4 | `mmNotSelfGenerated` | `induction h` isn't allowed when the target index (`e12`) isn't a bare variable | Switched to `cases h`, which is smart enough to recognize the `formation`/`assembly` base cases are impossible outright and only leaves the `step` case |
| 5 | `mmStuck.sameEffect` | The `simp` call left one case (`a ∈ []`) unresolved | Swapped `List.mem_singleton` for `List.not_mem_nil, or_false`, which correctly collapses the final disjunct |

Full unified diff: see `kernel_fixes.diff`.

15 purely cosmetic linter warnings remain (unused existential-binder names in
a couple of `∃` proofs, and 3 `def`s that could be `theorem`s since they
produce `Prop`s). These don't affect correctness and are safe to ignore or
silence.

## Test results (ran against the real Lean kernel, not just a syntax check)

I added `WmkCheck/VerificationTests.lean`, which asks the Lean kernel to
double-check what's already proved, rather than just trusting that "it
compiled":

**Axiom audit** (`#print axioms`) — confirms nothing is secretly resting on
`sorry` or an unexpected classical axiom:

| Theorem | Axioms it depends on |
|---|---|
| `mattermostModelAccepted` | `propext` only |
| `authoritative_implies_governing_package` (your central 0h theorem) | **none** — fully constructive |
| `mmModelSatisfiesCentralAuthorityTheorem` | `propext` only |
| `availability_has_semantic_witness` | **none** |
| `mmRecoveryHasSemanticWitness` | **none** |
| `history_conservative` | **none** |
| `anchor_conservative` | **none** |
| `no_sequential_recommit` | **none** |
| `mmNotSelfGenerated` | `propext` only |

`propext` (propositional extensionality) is one of Lean's three built-in
trusted axioms — completely standard, not a red flag. Nothing depends on
`sorryAx` (which would mean an unproved hole) or `Classical.choice`.

**Concrete evaluation checks** (`#eval`) on the finite Mattermost model,
confirming the decidable facts your theorems claim actually hold:

- `decide (mmBefore e6 e9) = true` — matches your `e6_before_e9` theorem
- `decide (mmBefore e6 e8) = false` and `decide (mmBefore e8 e6) = false` —
  matches your `e6_e8_incomparable` theorem (the two events are genuinely
  incomparable in your partial order)

**Existence check** (`#check`): `mattermostModel : MattermostModelWitness`
type-checks directly — the concrete model instance is accepted by the
kernel, not just the abstract theorem about it.

## What you're getting

- `0h_WMK_Canonical_Hardened_FIXED.lean` — your corrected kernel file, ready
  to drop back into your own project.
- `kernel_fixes.diff` — exact line-by-line diff of the 5 fixes.
- `wmk_lean_project.zip` — a complete, self-contained Lean project (kernel +
  verification tests + pinned `lakefile.toml`/`lean-toolchain`/manifest) that
  I rebuilt from scratch from the zipped copy to confirm it reproduces
  cleanly on a fresh checkout. Unzip it, run `lake update && lake build`,
  and you'll see the same axiom/eval output shown above.
