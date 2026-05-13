# Artifact 0: Loop Extension Contract

**Version:** v1 (initial draft, May 12, 2026)
**Status:** ACTIVE. Foundational contract for extending ClarityOmega's runtime surface.
**Reading order:** First artifact. Read before any other artifact in the series. Read in conjunction with `CLAUDE_ORIENTATION.md`.
**Scope:** Extensions to `src/loop.metta`, `src/helper.py`, and `soul/` files. Working-style and tone conventions live in `CLAUDE_ORIENTATION.md`.

---

## 0. Why this document is artifact 0

The artifact series (1 through 7) documents what the system IS and what it could become. This document, artifact 0, documents how additions to that system happen. It is the contract that governs extensions to the runtime surface so that future capabilities accumulate cleanly rather than producing spaghetti.

Without this contract, every capability addition is its own little judgment call about where logic should live and how it should connect to loop.metta. Over five or ten capabilities, those judgment calls drift, divergent patterns coexist, and the loop becomes hard to read, hard to extend, and hard to onboard new contributors (including future-Claude in a fresh thread) onto.

With this contract, every capability addition follows the same shape: hook in loop.metta calling a named function in a primitive-grouped soul/ file, with the wiring diagram (artifact 1) updated in the same commit. The shape is enforceable because it's checklist-driven, not stylistic.

Artifact 0 is also a self-enforcement document. It teaches Claude the operational habits required to catch oneself before violating the contract. The durability of the contract depends on Claude maintaining those habits, not on Berton catching violations after the fact.

---

## 1. Why the contract exists

### The spaghetti risk

Loop.metta is the runtime heartbeat. It runs every cycle. It already contains a mix of clean hooks (calls into soul/ and helper.py) and inline logic that should have been hooked from the start (raw set-atom! calls, conditional state writes, multi-step inline updates).

If every future capability adds two or three hook lines to loop.metta plus one or two new soul/ files, and the existing inline cruft stays, then over 5-10 capabilities the loop becomes:

- Difficult to trace (what fires where? when?)
- Difficult to extend (where does this new thing go?)
- Difficult to retire (which inline logic is safe to remove?)
- Difficult to debug (an unexpected behavior is one of 15 things, all wired differently)

The contract prevents this by enforcing a uniform extension shape and a maintenance contract that keeps the wiring diagram current.

### Loop.metta is sacred

Patrick's upstream logic at the core of loop.metta should change as little as possible. Three reasons:

1. Upstream merge cleanliness. Changes to Patrick's code create merge conflicts when his upstream evolves. Minimizing those changes preserves the merge-from-upstream path.
2. Runtime stability. Loop.metta is the heartbeat; any change risks breaking the cycle. Hooks that delegate to soul/ files isolate breakage to the soul/ surface, where it's easier to reverse.
3. Readability. Loop.metta documents what the loop DOES, not how every capability inside it WORKS. Inline logic conflates the two.

The discipline is: every extension to runtime behavior lands as a hook in loop.metta calling a function defined elsewhere. Loop.metta gains a line; soul/ or helper.py contains the logic.

### Helper.py is the established exception

Helper.py is the Python bridge between MeTTa and the runtime environment. Patrick's foundation functions live there, and our added functions also live there. The file has an established convention for distinguishing original from added code (function names, comment blocks, file regions).

This is the established exception to "minimize changes to upstream files." Helper.py is a working surface for additions; loop.metta is not.

### Per-primitive soul files

When a new capability arrives (task-state primitive, nervous-system mechanism, etc.), it gets its own soul/ file (or pair of files: pure definitions + side-effecting writers). The file groups all functions related to that primitive. The soul/ directory grows with primitives, not with functions.

This rule prevents soul/ from becoming a flat list of single-purpose files. Future contributors find related logic grouped, not scattered.

### Forward-looking durability

The contract has to work across model changes (this thread's Claude is not next thread's Claude), contributor changes (Berton has collaborators), capability additions (nervous-system work, NACE integration, F-SOVEREIGNTY-AUDIT migrations), and time (months and years).

That durability requires three things, baked into this document:

1. Rules with operational triggers, not abstract principles
2. A self-enforcement section that teaches Claude to catch herself
3. A maintenance contract that keeps the document and its referents current

---

## 2. The five disciplines

Each discipline below states the rule, names the failure mode it prevents, identifies the operational trigger that should make Claude check the rule, and gives a done-right and done-wrong example from the actual codebase.

### Discipline 1: Hooks call ONE clearly-named function

**Rule.** Every hook line in loop.metta is a single function call. The function name describes what the hook does (`verb-noun!` or `noun-verb` form). The hook itself contains no conditional dispatch, no multi-step logic, no raw set-atom!, no inline state writes.

**Failure mode prevented.** Inline logic accumulating in loop.metta. Each cycle becomes harder to read. New contributors trying to trace behavior have to interpret multi-step expressions rather than recognize named operations.

**Operational trigger.** When proposing any edit to loop.metta. When reviewing Clarity's substrate work that will be called from loop.metta. When the impulse is "I'll just add an if-statement here."

**Done right (loop.metta line 95).**
```metta
($soul_brief (swrite (getSoulBrief)))
```
`getSoulBrief` is one function defined in `soul/get_soul_brief.metta`. The hook line tells you what's happening. To understand the logic, you open the named file. Loop.metta stays readable.

**Done wrong (loop.metta line 94).**
```metta
($_ (if $msgnew (change-state! &engaged_idle_count 0) (if (> (string_length $idle_directive) 0) (change-state! &engaged_idle_count 0) (change-state! &engaged_idle_count (+ 1 (get-state &engaged_idle_count))))))
```
Three nested ifs doing state-write logic inline. The semantics ("reset on new message or on idle directive present, otherwise increment") is hidden in the expression structure. To understand what this counter measures, you read the if-tree and reverse-engineer the intent. This is the kind of inline cruft that hooks prevent.

---

### Discipline 2: One writer file per primitive

**Rule.** Side-effecting functions related to a single primitive concept live together in one soul/ file. The file is named for the primitive (`task_state_writers.metta`, `continuity_writers.metta`, `kb_forward_chain_writers.metta`). The soul/ directory grows with primitives, not with functions.

**Failure mode prevented.** Soul/ becoming a flat list of single-purpose files. Future contributors can't find related logic without searching. Imports proliferate in `lib_clarity_reasoning.metta`. The architectural boundary between primitives blurs.

**Operational trigger.** When introducing a new side-effecting function or writer in soul/. When considering whether to add to an existing file or create a new one. When naming a file.

**Done right (task-state primitive, Step 2 plan).**
`soul/task_state.metta` holds pure definitions (atom shapes, read helpers).
`soul/task_state_writers.metta` holds all side-effecting writers for task-state (`do-bootstrap-task-state!`, `do-set-cycles-since-input!`, `do-set-last-activity!`).
One primitive concept, two files (pure and side-effecting), all functions grouped.

**Done wrong (hypothetical).**
`soul/set_cycles_since_input.metta` and `soul/set_last_activity.metta` and `soul/bootstrap_task_state.metta` as three separate files. Same logic, three imports, three places to look, no architectural grouping. This is what the directory looks like if Discipline 2 is skipped.

---

### Discipline 3: Hooks land in predictable structural locations

**Rule.** Hook insertions in loop.metta land in named phase locations matching the phase vocabulary in `artifact_1_loop_metta_wiring_diagram.md` Section 4. Bootstrap hooks go in initLoop. Per-cycle hooks go in specific positions in the let* sequence (Phase 4.1 soul input intercept, Phase 4.2 aliveness state, Phase 4.3 prompt assembly, Phase 4.4 response generation, Phase 4.5 output intercept, Phase 4.6 PAUSE routing).

**Failure mode prevented.** Hooks scattered randomly through loop.metta, making it impossible to know where to look for "where does X happen?" When a contributor adds a new capability, they don't know which insertion point is appropriate.

**Operational trigger.** When proposing any hook insertion in loop.metta. When reviewing where existing hooks live to find an insertion pattern to match. When describing an insertion to Berton or Clarity for review.

**Done right.** "The `do-set-last-activity!` hook for post-msgnew lands in Phase 4.0 (Iteration entry and message reception), specifically after the existing `&last_human_time` write at current line 68." The location is named with the phase vocabulary, references an existing structural landmark, and produces a reviewable insertion point.

**Done wrong.** "We'll put it somewhere in the let* block." Unnamed location. Future contributor has no template for where the next hook should go. Each addition becomes its own judgment call.

---

### Discipline 4: The wiring diagram stays current

**Rule.** When a hook is added to loop.metta, `docs/design/artifact_1_loop_metta_wiring_diagram.md` is updated in the same commit. The phase entry for the affected lines gains a paragraph documenting what the hook reads, writes, calls, and which network it serves. When inline logic is retired to a hook, the elevation flag in artifact_1 is closed.

**Failure mode prevented.** Artifact_1 drifting from reality. Within 3-5 capability additions, the wiring diagram becomes stale, and contributors stop trusting it. Once trust is lost, the diagram becomes decoration rather than working reference. The trace-what-connects-to-what artifact disappears.

**Operational trigger.** Any commit that modifies loop.metta. Any commit that retires inline logic to a hook. Any change that affects the phase 4.0 through 4.6 structure documented in artifact_1.

**Done right.** Step 2 of the task-state primitive plan: the commit includes (a) the soul/ substrate files, (b) the lib_clarity_reasoning import, (c) the loop.metta hook insertions, and (d) artifact_1 Section 4 updates for Phase 4.0 (last-activity post-msgnew), Phase 4.2 (cycles-since-input), and Phase 4.3 or 4.4 (last-activity post-send). One commit, all surfaces consistent.

**Done wrong.** "We'll update artifact_1 after Step 2 verifies." Three days later, the doc update is forgotten. Step 3 begins against a stale diagram. By Step 5, the diagram references states that no longer exist and omits states that do. The map becomes unreliable.

---

### Discipline 5: Migration retires inline logic, doesn't accumulate it

**Rule.** When the spec's implementation sequence (e.g., task-state primitive spec Section 10) says "Step N retires X to a hook," the retirement happens in that step's commit. Inline logic that should be a hook is named in artifact_1 as an elevation flag and has a scheduled retirement step. Inline logic does NOT accumulate over capability additions; it's retired on schedule.

**Failure mode prevented.** Inline cruft compounding. Without scheduled retirement, the lines 68/88/93/94 inline cruft sits in loop.metta indefinitely. New capabilities add hooks alongside it. Over time, loop.metta becomes a mix of hooks and never-retired inline logic, with no clear distinction between "this is legacy and being removed" and "this is current architecture."

**Operational trigger.** When writing a capability spec's implementation sequence (e.g., task-state Section 10). When reviewing inline logic in loop.metta. When elevation-flagging in artifact_1. When committing a step that includes a retirement.

**Done right (task-state primitive spec Section 10).**
"Step 8: Remove latch-state. All consumers migrated. set-atom! calls in loop.metta machinery for latch-state are removed. Lines 88, 93 retire."
The retirement is scheduled, the consumers are migrated first, the retirement happens in a named step.

**Done wrong.** A capability spec that says "phase 1 adds hooks, no retirement scheduled." Hooks pile on top of unretired inline logic. Six months later, no one remembers which inline logic was supposed to be retired vs which is current architecture. The cruft becomes permanent.

---

## 3. The hook insertion checklist

Before any commit that adds a hook to loop.metta or modifies loop.metta in any way, Claude (or whoever is proposing the edit) runs through this checklist. Each item must answer YES or be explicitly justified.

```
HOOK INSERTION PRE-FLIGHT CHECKLIST

Hook structure
[ ] The insertion is a single function call (Discipline 1)
[ ] The function name is verb-noun! or noun-verb form
[ ] No conditional dispatch in the hook itself
[ ] No raw set-atom!, change-state!, or get-state in the hook itself
[ ] No multi-step inline logic

Function definition location
[ ] The function is defined in soul/ or src/helper.py
[ ] If new soul/ file: file groups related functions for one primitive (Discipline 2)
[ ] Existing soul/ files were considered first for related functions
[ ] The new file (if any) is imported in lib_clarity_reasoning/lib_clarity_reasoning.metta

Insertion location
[ ] The insertion point is named with artifact_1 phase vocabulary (Discipline 3)
[ ] The insertion point references an existing structural landmark in loop.metta
[ ] Surrounding lines are not modified

Maintenance contract
[ ] artifact_1 Section 4 entry updated for the affected phase (Discipline 4)
[ ] The artifact_1 update lands in the same commit as the hook
[ ] If retiring inline logic: artifact_1 elevation flag closed and spec step referenced

Migration consistency
[ ] No inline cruft expanded by this commit (Discipline 5)
[ ] If the capability spec schedules a retirement, this commit either does it or links to the step that will

Reverse-application
[ ] The apply script supports --reverse
[ ] The reverse path has been tested in --dry-run

Verification
[ ] Paren count verified before and after edit
[ ] Container rebuild + restart planned
[ ] Atom queryability verified for any new substrate state
```

Any NO answer halts the commit. Either fix the issue or document why this case is an exception (and add the exception pattern to this artifact for next time).

---

## 4. Maintenance contract

This contract governs how documents that depend on this discipline stay current.

### When a hook is added to loop.metta

In the same commit:

1. `docs/design/artifact_1_loop_metta_wiring_diagram.md`, update Section 4 phase entry for the affected lines
2. If the hook introduces new state atoms, note in artifact_1 Section 2 (state variables) or Section 9 (external dependency map)
3. If the hook calls a new helper.py function, note in artifact_1 Section 9 (helper.py functions)

### When inline logic is retired to a hook

In the same commit:

1. `docs/design/artifact_1_loop_metta_wiring_diagram.md`, close the elevation flag, reference the spec step that authorized retirement
2. The capability spec's Section 10 (or equivalent), mark the step as completed

### When a new soul/ primitive file is introduced

In the same commit:

1. `lib_clarity_reasoning/lib_clarity_reasoning.metta`, new import line in appropriate grouping
2. `docs/design/artifact_1_loop_metta_wiring_diagram.md`, Section 3 (Startup sequence) updated if the file affects startup behavior
3. The capability spec's design document (if one exists), note the file as part of the primitive's implementation

### When the discipline itself changes

When a sixth discipline emerges, or when an existing discipline is clarified, refined, or amended:

1. This document (artifact 0) updates first
2. The version block at the top of this document records the change (v1 → v1.1, etc.)
3. `CLAUDE_ORIENTATION.md` Section 2 (First principles) updates ONLY if the discipline change affects working principles outside loop/soul/helper.py extension scope
4. Other artifacts (1 through 7) update ONLY if the discipline change affects content they document; if so, they note the artifact 0 version that drove the update
5. Active design specs update their working principles section to reference the new artifact 0 version

The propagation rule: artifact 0 is the source of truth for extension disciplines. Other documents reference it; they do not re-state it.

### Annual review

Once per calendar year (or sooner if drift becomes evident), this document is reviewed for:

- Disciplines that need updating based on accumulated practice
- Examples that have become outdated as inline cruft retires
- Checklist items that are routinely skipped (signal of either redundancy or process failure)
- Maintenance contract items that are routinely missed (signal of insufficient process integration)

---

## 5. How Claude checks herself

This section is the durability lever. The disciplines and checklist above are necessary but not sufficient. Claude must maintain operational habits that catch pre-violation in the moment, not after Berton or another reviewer points it out.

The habits below were drawn from failure modes observed in actual ClarityOmega development work, including the May 12, 2026 thread that produced Step 1 of the task-state primitive. Each habit has a trigger (what fires the check), a check (what to verify), and a failure mode (what happens when skipped).

### Habit 1: Scope-expansion flag

**Trigger.** Clarity (or any contributor) proposes a structural choice that expands surface area beyond the original spec scope. Example: choosing a separate writers file instead of inline writes, when the spec implied inline.

**Check.** Pause and ask: "Does this expand surface area beyond what was scoped? If yes, surface the tradeoff to Berton before proceeding." Do not silently go along with the expansion because your own preference aligns with the proposal.

**Failure mode when skipped.** Scope creeps without explicit acknowledgment. Berton later asks "are we adding more than was scoped?" and you realize you didn't flag the expansion. Trust erodes; future scope decisions get questioned more.

### Habit 2: Path coherence verification

**Trigger.** Any operation that crosses filesystem boundaries (container vs host, CWD vs repo root, mount point vs reference path). Any file write where the path is relative.

**Check.** Before claiming verification of a file's content or location, verify the path. Run `ls -la $path` against both the expected location and the alternative location. Confirm timestamps and sizes match what you expect.

**Failure mode when skipped.** A file edit lands at the wrong path because CWD differs from where the import looks. Verification reads the wrong file. "Verified" claims become "actually verified the stray copy." Discovery of the mismatch happens late, when downstream behavior breaks.

### Habit 3: Log re-reading without confirmation bias

**Trigger.** Any review of a long log output. Any time Berton pushes back with "you missed something."

**Check.** Re-read slowly, looking for what's INCONSISTENT with your current model, not what confirms it. Note timestamps. Distinguish embedded history from live output. If Berton asks twice whether you read the log, you didn't.

**Failure mode when skipped.** Important details (path mismatches, cycle classifications, behavioral anomalies) hide in plain sight because you scanned for confirmation. Berton has to point them out repeatedly. The thread becomes "Berton catches Claude's misses" instead of forward work.

### Habit 4: Commit before assumed-verified

**Trigger.** Step or sub-step nearing completion. Tempting to move on without committing.

**Check.** Did the work that was just done get captured in a commit? Is the design state preserved regardless of runtime outcome? If rebuild reveals an issue, do you have a known-good commit to roll forward from?

**Failure mode when skipped.** Runtime issue surfaces, you fix forward, the design state from earlier hours of work is conflated with the fix. Loss of clean history. Difficulty rolling back to "design was good, runtime is broken" state.

### Habit 5: Single-recommendation discipline

**Trigger.** Berton asks for action. Multiple paths come to mind.

**Check.** Give ONE recommendation with a reason. If you genuinely believe two options are equally good, say "I have no preference, your call." But most of the time you have a preference and should state it. Optionality dressed as respect doubles Berton's cognitive load.

**Failure mode when skipped.** Berton spends turns choosing between options instead of executing. Forward motion stalls. The thread becomes a decision tree rather than a build.

### Habit 6: Don't relitigate decided decisions

**Trigger.** Berton has stated a decision or chosen a path. You have residual concerns.

**Check.** Has the decision been made? If yes, execute it. If you have a specific concern, state it once briefly with a specific reason, then execute. Do not restate your reasoning. Do not draft a more cautious version of what was approved.

**Failure mode when skipped.** Decisions get re-relitigated. Berton has to defend choices already made. Thread momentum drains into re-justification.

### Habit 7: Verify substrate state through substrate, not self-report

**Trigger.** Clarity reports a substrate change is done. Tempting to accept her self-report as verification.

**Check.** Self-report is data, not verification. Read the file from disk, query the AtomSpace, run the actual check. Distinguish "she said the file is updated" from "the file is updated."

**Failure mode when skipped.** Step claimed complete on her word. Later discovery that the file landed at the wrong path or didn't land at all. The verification gap is hidden by the apparent completion signal.

### Habit 8: Tracking-section accountability

**Trigger.** End of every reply. Standing rule from CLAUDE_ORIENTATION.md.

**Check.** The tracking section's next-move trigger is something the human can actually do. The tracking section identifies what's pending, what's resolved, and what would unblock progress. It is forward-looking, not a kitchen sink of observations.

**Failure mode when skipped.** Tracking section becomes decorative. Berton has to derive next-action from the prose body. Continuity across long threads (or across thread breaks) degrades.

---

## 6. Reading triggers

This document is re-read when any of the following fire:

**Start of any capability spec.** Before drafting a new spec (task-state, nervous-system mechanism, etc.), re-read this document so the spec's implementation sequence respects the disciplines.

**Before drafting any apply script.** Apply scripts mechanize hook insertions. Their pre-flight checks should align with the checklist in Section 3 of this document.

**Reviewing Clarity's substrate work.** When she proposes new soul/ files or function shapes, check against Discipline 2 (per-primitive file) and Discipline 1 (function naming suitable for hooks).

**Proposing edits to loop.metta or helper.py.** Discipline 1, 3, 4 fire. Run the Section 3 checklist.

**Reviewing inline logic in loop.metta.** Discipline 5 fires. Is this inline logic scheduled for retirement? If yes, when? If no, why is it still inline?

**When pushing back on a proposal or being pushed back on.** The disciplines are the shared reference. Cite the discipline rather than personal preference.

**Annual review (Section 4).** Calendar-driven re-read.

**When CLAUDE_ORIENTATION.md says read this.** Orientation Section 7 should reference this document as required reading before any other artifact.

---

## 7. Relationship to other documents

This document is the source of truth for extension disciplines. Other documents reference it; they do not re-state its content. The table below names the relationship-of-record between artifact 0 and other documents in the ClarityOmega doc tree.

| Document | Relationship to artifact 0 | What artifact 0 governs in that document |
|----------|---------------------------|------------------------------------------|
| `CLAUDE_ORIENTATION.md` | Bidirectional required-reading. Orientation lists artifact 0 in Section 7 reading order; artifact 0 references orientation for working-style and tone rules. | Working principles around loop/soul/helper.py extension; orientation handles tone, format, communication style. |
| `artifact_1_loop_metta_wiring_diagram.md` | Artifact 1 is the structural map artifact 0 references for phase vocabulary (Discipline 3) and maintenance contract (Discipline 4). | Hook locations land in named phases per artifact 1 Section 4; artifact 1 is updated when hooks land per the maintenance contract. |
| `artifact_2_hooks_piggybacks.md` | Reference for understanding existing hook patterns and piggyback risks. | New hook proposals are checked against piggyback risk patterns documented here. |
| `artifact_3_growth_surface.md` | Reference for understanding where the growth surface is for the system. | New primitive proposals (Discipline 2) should align with the growth surface. |
| `artifact_4_ClarityOmega_Triple_Network_Scaffold_v1_1.md` | Network ownership classification for hooks (SN, FPN, DMN, SWITCH-HUB) is documented per artifact 4. | Hook insertions name their network when applicable; documented in artifact 1's network-relevant flag. |
| `artifact_5_ClarityOmega_Cognitive_Architecture_Spec_v3_0.md` | Layer classification (Layer 1+2 constitutional, Layer 3 transitional, Layer 4 wisdom) governs which capabilities are extensions vs constitutional changes. | Disciplines apply to Layer 3 and Layer 4 work; Layer 1+2 changes are out-of-scope and require separate process. |
| `artifact_6_Hyperseed_Formalization_Catalog_v1_1.md` | Reference for Hyperseed atom inventory. | New hyperseed-related primitives follow Discipline 2 (one writer file per primitive). |
| `artifact_7_Hyperseed_to_Network_Synergy_Map_v1_1.md` | Reference for which Hyperseed atoms map to which network. | Hook insertions for Hyperseed work consult this map for network-relevant tagging. |
| `docs/design/task-state-primitive_design.md` | First active capability spec to follow this contract. Section 10 implementation sequence respects Disciplines 1-5. | Step-by-step implementation respects checklist; per-step commits include artifact 1 updates. |
| `docs/design/reasoning_substrate_cycle_level_daemon_architecture.md` | v1 design-phase document for nervous-system work. Follows the per-primitive rule (one file per mechanism). | Each of the four mechanisms gets its own writer file in soul/ per Discipline 2; hook insertions follow checklist. |
| Future capability specs | Will follow this contract. Reference artifact 0 in their working principles section. | Implementation sequence and maintenance commitments. |

**Cross-reference for future contributors.** When a new contributor (human or AI) starts working on ClarityOmega:

1. Read `CLAUDE_ORIENTATION.md` for working-style and project context
2. Read this document (artifact 0) for extension disciplines
3. Read `artifact_1_loop_metta_wiring_diagram.md` for the structural map
4. Read the current active capability spec named in orientation Section 6
5. Read other artifacts as their content becomes relevant to current work

This ordering ensures the contract is internalized before any extension work begins.

---

## 8. Version history

**v1 (May 12, 2026).** Initial draft. Five disciplines, hook insertion checklist, maintenance contract, eight self-enforcement habits, reading triggers, cross-reference table. Drafted following the task-state primitive Step 1 thread, which surfaced the durability concern that motivated this document. Citations to lines 68, 88, 93, 94 of loop.metta as wrong-example inline logic; line 95 as right-example hook pattern.

---

## Document end

This document is artifact 0 of the ClarityOmega artifact series. It is the contract that governs extensions to the runtime surface. Future contributors read this first.
