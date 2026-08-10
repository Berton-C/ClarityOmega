# WMK Canonical Kernel — verified build

This is a self-contained Lean 4 project containing the fixed, compiling version
of `0h_WMK_Canonical_Hardened.lean`.

## What's in here

- `WmkCheck/Kernel.lean` — your kernel file, with 5 small fixes applied (see
  `kernel_fixes.diff` alongside this zip, or the summary report, for exactly
  what changed and why).
- `WmkCheck/VerificationTests.lean` — `#print axioms` / `#check` / `#eval`
  checks that confirm the headline theorems hold with no `sorry` and no
  unexpected axioms.
- `lakefile.toml`, `lean-toolchain`, `lake-manifest.json` — pinned build
  configuration (Lean `v4.33.0-rc2`, `batteries` as the `Std` dependency).

## How to build it yourself

1. Install `elan` (the Lean version manager), if you don't have it:
   ```
   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
   ```
2. From this folder, run:
   ```
   lake update   # fetches the pinned batteries dependency
   lake build    # compiles the kernel + verification tests
   ```
   `lake build` will print the `#print axioms` / `#check` / `#eval` output
   from `VerificationTests.lean` as `info:` lines.
3. For day-to-day editing, install the "lean4" extension in VS Code and open
   this folder — you'll get inline red-underline error feedback as you type,
   which is much faster than round-tripping through `lake build`.

## Notes

- The toolchain is pinned to a specific Lean release candidate
  (`v4.33.0-rc2`) because that's what `batteries` currently requires at HEAD.
  If you later see the toolchain drift on `lake update`, that's expected —
  Lean and its libraries move together.
- 15 cosmetic linter warnings remain (unused existential-binder names, and
  three `def`s that could be `theorem`s since they produce `Prop`s). None of
  these affect correctness; they're style suggestions only.
