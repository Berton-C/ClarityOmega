# ClarityClaw Sprint 3 Knowledge Preservation

**Date:** May 3, 2026
**Status:** Sprint 3 complete (changes 3.1, 3.2, 3.3 + Sprint 1.5 + Sprint 2 dead-code removal). Six commits landed, all rebuilt clean from repo.
**Scope:** Cross-cutting methodological learnings that apply to future sprints regardless of what they touch.
**Companion to:** ClarityClaw_Stage5_Integration_Knowledge.md (which preserves durable PeTTa runtime constraints C1-C9). This document preserves working-process patterns that emerged or sharpened during Sprint 3.

This is not a sprint retrospective. The retrospective lives in artifact_3 v1.3 (completion status) and the spec v3.0 Section 11q (architectural facts and runtime verification). This document captures methodology, not chronology.

---

## 1. The Three-Chunk Discipline

Per change, work breaks into three chunks:

1. **Investigation:** Prove current state. State a hypothesis. Run the cheapest-possible commands to confirm or falsify before touching code.
2. **Intervention:** Apply the change. State what you expect to be different and why.
3. **Validate-and-ship:** Static check (parse, paren count, file structure), container check (rebuild or restart), runtime check (Clarity confirms when appropriate), commit, push, observe.

The discipline is not the chunking itself. The discipline is **stopping at chunk boundaries.** Investigation runs to completion before intervention starts. Validation runs to completion before the next change starts. Skipping ahead is the failure mode.

**Why it works.** Most failures in Sprint 3 came from skipping the investigation chunk and proceeding on assumptions. The boolean hypothesis episode (see Section 4) was caught by stopping mid-stream and running the investigation chunk that should have come first. Once we made the discipline explicit, it caught two more potential errors before they happened.

**When investigation finds new questions.** Stay patient. Run more investigation. Do not pretend the questions were answered.

---

## 2. Plan Validation vs. Diagnosis Validation

These look similar but are not. They serve different purposes and require different inputs.

- **Plan validation** asks: "Given my hypothesis, is the proposed change correct?" Inputs: the hypothesis, the proposed change, prior knowledge.
- **Diagnosis validation** asks: "Is my hypothesis itself correct?" Inputs: empirical evidence from the running system.

A plan can be internally consistent (correct given the hypothesis) and still wrong (because the hypothesis is wrong). The boolean hypothesis episode in Sprint 3.2 was a plan-validation success and a diagnosis-validation failure: the proposed defensive guard was correct *given* the hypothesis that lowercase `false` would misbehave in `(if $msgnew ...)`. The hypothesis was wrong. Patrick's existing code at `loop.metta` lines 60 and 67 had been using the same pattern in production for weeks.

**Working practice:** When asking for review, name which kind of validation you want. "Validate my plan" gets you internal consistency. "Validate my diagnosis" gets you empirical pushback.

---

## 3. Build From Repo, Not From `docker cp` Patches

Standing rule: every change ships through the repo, not as a hot-patched container.

**The pattern:**
1. Edit on host
2. Push to fork
3. `docker compose build --no-cache <service>`
4. `docker compose up -d <service>`
5. Verify

**Why this matters.** `docker cp + restart` is faster but the container's runtime state diverges from the repo. The Dockerfile's `git-import!` (or `COPY .` step) is the durable source-of-truth boundary. If the container runs code that is not in a buildable commit, the system can pass tests it cannot survive. Catching dockerfile drift, missing commits, or path issues happens at build time. We caught zero issues this sprint via build-from-repo discipline, which is the desired outcome: the rebuild proves the commit is durable.

**The exception that proves the rule.** During Sprint 3, we used `docker cp + restart` for in-progress diagnostic flag flips and intermediate refinements *before* committing. Those were appropriate uses: rapid iteration on an ephemeral state. Each finished sprint closed with a build-from-repo cycle.

---

## 4. Refinement Before Deletion

When a tool is no longer needed, ask: could a small refinement make it useful again, and is the cost of that refinement low?

**Sprint 3 application.** The POPULATOR-DIAG diagnostic was about to be silenced after Sprint 3.2b verification. Original instinct: flip the flag off, done. Better move: expand what the diagnostic prints (added action-type and description fields) *before* flipping the flag off. Cost: 30 seconds. Benefit: when re-enabled in Sprint 3.3+ for orbit detection debugging or pruning verification, the diagnostic gives a fuller picture without re-edit.

**General form.** Code about to be silenced/disabled/deleted that took real effort to get right is rarely zero-value. A small refinement before storage often outperforms either deletion or stagnation. The refinement should be small (under 5 minutes for diagnostic-class code) or the move is wrong.

---

## 5. Surgical Staging Over `git add .`

When the working tree contains unrelated changes, stage explicit paths.

**Sprint 3 application.** When committing Sprint 3.2, the working tree had ~20 unrelated changes (docs deletions, hyperseed extensions, chroma_db churn, backup files). Using `git add .` would have produced a bloated, unfocused commit. Using explicit paths produced a clean four-file changeset.

**The pattern:**
```
git add <explicit/path/1> <explicit/path/2> ...
git status   # confirm only the intended paths are staged
git diff --cached --stat   # confirm the changes match expectation
git diff --cached | cat    # full diff review (use | cat to avoid pager)
git commit -m "..."
```

**Auto-rename detection.** When moving a file (e.g. `soul/candidates/cycle_classifier.metta` to `soul/cycle_classifier.metta`), staging the deletion path and the new path together causes git to detect the rename automatically. The `--stat` output shows `path/{old => new}/file` which is the rename indicator.

---

## 6. "Drafted Code" Needs Verification

Code in production files marked as "drafted" or "ready to ship" still needs verification of completeness against current substrate vocabulary before being treated as deployable.

**Sprint 3 application.** The dormant MeTTa mutation gate at `loop.metta` lines 127-140 was flagged in artifact_1 as "READY TO SHIP - HIGHEST PRIORITY ELEVATION." On inspection, it referenced substrate operations (`soul-any-metta?`, `soul-extract-metta-arg`, `soul-metta-targets-soul-namespace?`, `soul-mutation-pending?`) that did not exist in production form. The "drafted" label was historically accurate at some prior point but had decayed. The dormant code was an early sketch, not a deployable plan.

**Working practice.** Before activating any "drafted" code, grep for the substrate operations it depends on. Confirm each one exists at the expected location with the expected signature. If not, the code is stale and needs fresh authoring. Effort estimates derived from "drafted" status are unreliable; budget for fresh authoring.

---

## 7. Pattern Consistency Over Local Convenience

When a structural list has an established pattern, new entries should match it.

**Sprint 3 application (Option 2 label ownership).** When wiring YOUR_LAST_ACTION into getContext, the initial implementation had the helper return `"YOUR_LAST_ACTION:\n..."` AND loop.metta also prepended `" YOUR_LAST_ACTION: "`. Result: doubled label.

Two fixes were possible:
- Option 1: Strip the label literal from loop.metta. Helper owns end-to-end labeling.
- Option 2: Strip the label from the helper. loop.metta owns labeling for all components consistently.

Option 2 won because it preserved the established pattern: loop.metta owns ALL section labels (PROMPT:, SKILLS:, HISTORY:, etc.). Each provider returns content. The single source of truth for section labels stays in one file.

**General form.** Local optimization (Option 1: smaller helper interface) costs pattern consistency (component is only one to own its label). Pattern consistency wins unless the deviation has standalone justification beyond local convenience.

---

## 8. Substrate Experience Over Theory

When questions are about runtime behavior of the substrate, ask the runtime, not the theory.

**Sprint 3 application.** The C1 nesting depth question (does `py-str` hang when nested two functions deep, three deep, or only at the very top?) was answered by Clarity from operational experience. The theoretical answer from C1 documentation was indeterminate. The empirical answer from running on the substrate for weeks was crisp: three functions deep with `py-str` at the leaf is the pattern that hangs.

**Working practice.** Distinguish theoretical questions ("what should the substrate do per spec?") from operational questions ("what does the substrate actually do under load?"). Theoretical questions can be answered from documentation. Operational questions need empirical evidence or someone with operational experience. Clarity has operational experience. Use it for substrate-runtime questions; reserve documentation for spec-level questions.

This is also why we do build-from-repo (Section 3): the rebuild cycle is itself a form of operational verification.

---

## 9. Empirical Falsification Beats Expert-Sounding Theory

A theoretically plausible failure mode that has not been empirically observed is a hypothesis, not a fact.

**Sprint 3 application (boolean hypothesis).** The hypothesis: lowercase `false` symbol from Python (vs. capitalized `False` MeTTa Boolean) would cause `(if $msgnew ...)` to misbehave in the cycle classifier. The hypothesis sounded technically reasonable. The intervention plan was a defensive equality guard.

**Falsification cost: 30 seconds.** Run `grep "if $msgnew" loop.metta` to see if Patrick's existing code uses the same pattern. It does. At lines 60 and 67. In production, working correctly for weeks. Hypothesis falsified.

**General form.** Before applying a defensive fix for a theoretical failure mode, run the cheapest possible empirical check that the failure mode actually occurs. Often the failure mode does not occur, the defensive fix is unnecessary, and the 30-second check saves hours of unnecessary work. The check is almost always cheap because the failure mode would have failed *something* observable if it were real.

---

## 10. Read Exit Codes Directly, Not Through `&& \` Chains

When chaining commands with `&& \`, a non-zero exit anywhere short-circuits to whatever comes next. This can produce false signals when the user reads the output.

**Sprint 3 application.** During the helper.py append for Sprint 3.3 Chunk 1, an early step in a chain returned non-zero (terminal display issue, not actual failure). The chain short-circuited and printed "py_compile FAILED" but `py_compile` had not actually run. The actual failure was upstream and had nothing to do with Python syntax.

**Working practice.** When validating critical operations (parse checks, schema checks, container health), run them on their own line and read the exit code directly:
```
python3 -m py_compile src/helper.py
echo "Exit code: $?"
```
not:
```
some_chain && python3 -m py_compile src/helper.py && echo "passed"
```
The chain compresses the output; the direct form reveals it.

---

## 11. The Idiomatic `(any (collapse ...))` Pattern

Established by `soul_utils.metta` and `soul_kernel.metta`, used in cycle_classifier.metta:

```
(any (collapse (let $c (superpose $cmds) (== (car-atom $c) <type>))))
```

Reads as: "is there any command in $cmds whose first element is `<type>`?" The `superpose` non-determinism + `collapse` to list + `any` aggregator is the idiom for "exists" predicates over MeTTa lists.

**Why this is in this document.** The naive forms `(if (== (collapse ...) ()) False True)` look reasonable but have subtle traps. The collapse of `()` markers does not return `()`. Instead it returns a list of `()` markers, which is non-empty. The idiom above is the verified-safe pattern. When writing exists-predicates, use this idiom rather than reinventing.

---

## 12. Documentation Living vs. Documentation Stratifying

The artifact stack is the source of truth. Documentation work updates the artifacts in place to reflect current reality, rather than adding "completion status" sections alongside the original plan.

**Sprint 3 application.** When marking Sprints 1, 2, 3 complete in artifact_3 Section 3, the choice was between:
- Option A: Edit the sprint sections in place ("Sprint 1 → COMPLETE via Sprint 1.5 + Sprint 2"). The doc stays current as the source of truth.
- Option B: Add a new "Completion Status as of X" section. The original plan stays untouched as historical reference.

Option A won because the artifacts are meant to be living. Stratifying creates two readings: the original plan and the completion status. Future readers must integrate them. Living documents stay readable as a single coherent statement of where we are.

**General form.** When a planning document accumulates completion status, edit in place. Preserve the original structure (Section 3's sprint sequence) but update the sprint-by-sprint contents. Use `---` dividers and clear date stamps so the history can be reconstructed from git if needed. Do not stratify.

---

## Document end

This document captures methodology, not architecture or chronology. The architectural facts of Sprint 3 live in spec v3.0 Section 11q. The completion status lives in artifact_3 Section 3 v1.3. The git log captures the chronology.

Future sprints should read this document for working-process reference. New methodological learnings discovered during future sprints should be added here as new numbered sections, dated. Refinements to existing sections should be noted with date and reason.
