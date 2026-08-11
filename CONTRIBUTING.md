# Contributing to ClarityOmega

Thanks for your interest. ClarityOmega is maintained by a single maintainer
(Berton), so this guide keeps the process small and predictable.

---

## Branches

| Branch | Purpose |
|---|---|
| `main` | The stable, usable version. Tagged releases are cut from here. |
| `v0.2.0-development` | Larger experimental work toward the next release. |

Small bug fixes, documentation improvements, and cleanup go to `main` through
pull requests. Larger or architecture-changing work goes to
`v0.2.0-development`.

---

## The fork and pull-request workflow

**1. Fork the repository** on GitHub, then clone your fork:

```bash
git clone https://github.com/<your-username>/ClarityOmega.git
cd ClarityOmega
git remote add upstream https://github.com/Berton-C/ClarityOmega.git
```

Here `upstream` means Berton's ClarityOmega. Note that the ClarityOmega
repository itself uses `upstream` for a different thing: Patrick Hammer's
`asi-alliance/OmegaClaw-Core`, from which ClarityOmega is forked.

**2. Synchronize your fork before starting work:**

```bash
git fetch upstream && git checkout main && git merge --ff-only upstream/main && git push origin main
```

`--ff-only` refuses to create a merge commit. If it fails, your `main` has
diverged; ask before resolving it.

**3. Create one small branch per change:**

```bash
git checkout -b fix/short-description
```

One concern per branch. A branch that fixes a typo and refactors a module is
two pull requests.

**4. Make the change and commit it:**

```bash
git add <specific files> && git commit -m "Short description of the change"
```

Stage specific paths. Avoid `git add .`, which sweeps in unrelated files.

**5. Push and open a pull request** against `main` of
`Berton-C/ClarityOmega`. Fill in the pull-request template.

**6. Review.** Berton reviews and decides whether to merge. Expect questions;
they are about understanding the change, not about your competence.

**7. Fixes that also matter for v0.2.0** are brought into
`v0.2.0-development` after merging to `main`.

---

## Conventions this project actually enforces

These come from hard experience and are not stylistic preferences.

- **No em dashes** anywhere in documents, code comments, or commit messages.
- **Verify before claiming.** Do not assert what the code does from memory or
  from a document. Read the live source in the current session. Where a
  document and the runtime disagree, the runtime wins.
- **Surgical commits.** One concern per commit; stage specific paths.
- **Reversible edits.** Scripts that modify tracked files follow the apply
  pattern: dry run by default, `--apply` to write, `--reverse --apply` to undo,
  byte-exact anchors matched exactly once, and a diff preview.
- **`loop.metta` stays hooks, not logic.** Runtime extensions land as a hook
  calling a named function defined in `soul/` or `src/helper.py`. This keeps
  merges from Patrick's upstream workable.
- **MeTTa first.** Control flow and reasoning live in MeTTa. Python exists for
  what MeTTa cannot do: LLM calls, I/O, ChromaDB, OS operations.
- **Never modify upstream code unnecessarily.** Defects in code inherited from
  OmegaClaw-Core are fixed in the fork and reported upstream where possible.

---

## What CI checks, and what it does not

Pull requests run hygiene checks only: MeTTa parenthesis balance, Python
syntax, absence of committed secrets, and `.env.example` staying in sync with
`docker-compose.yml`.

CI **cannot** verify agent behaviour. Soul evaluation and NAL reduction only
occur inside the live loop process. A green CI run means your change is
structurally sound, not that it works. Behavioural changes need live-loop
verification, and the pull-request template asks you to describe what you ran.

---

## Secrets

Never commit `.env` or any real credential. `.env.example` is the template and
must contain no real values. CI fails the build if `.env` becomes tracked or
if a credential pattern appears in a tracked file.

---

## Questions

Open an issue. For anything touching the value substrate in `soul/`, open an
issue first and discuss before writing code: that surface has a design
authority beyond the maintainer's convenience.
