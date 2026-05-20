# Investigation: Bug 2 / Bug 2b clear-function failure (2026-05-20)

**Investigators:** Berton (project lead), Clarity (substrate co-designer), Claude (investigation assistant).

**Related artifacts:**
- `docs/decisions/ADR-005-bug2-clear-fn-superpose-fix.md` (the architectural decision)
- `docs/design/artifact_1_loop_metta_wiring_diagram.md` (wiring diagram updated per Discipline 4)

**Outcome:** Bug 2 + Bug 2b fixed and verified. Bug 1 disproven. Bug 3 downgraded to cosmetic. Bug 4 surfaced as the next active pathology.

---

## Investigation scope

This investigation began as forensic analysis of spam behavior, focused on a substrate-level discrepancy where Clarity's prompt context showed `(idle-pattern productive 0)` at cycles 757-758 despite the recent-action window containing 6-7 status-send-unprompted atoms from cycles 747-755. Expected verdict was `send-burst` with count 6+. Actual was `productive 0`.

The three hypothesized bugs entering investigation:

- **Bug 1:** `count-sends-in-window` returns 0 despite send-class atoms in the window
- **Bug 2:** `do-clear-idle-pattern!` fails, causing stale atoms to remain in `&self`
- **Bug 3:** `recent_action_populator` pruning leaves atoms unpruned

A fourth potential bug emerged mid-investigation, regarding `do-clear-agency-balance!` having the same structural shape as `do-clear-idle-pattern!` (Bug 2b).

## Methodology

Read-only diagnostic instrumentation strategy: insert `println!` prints at strategic points in `src/loop.metta` and the writer files, run the container, capture log output, analyze without modifying live behavior.

Diagnostics inserted via a reversible apply script (`apply_diag_match_shape_test.py` with `.bak.diagprint` suffix). Eight new print points:

- `DIAG-CYCLE-START` / `DIAG-CYCLE-END`
- `DIAG-COUNT-FN` (count-sends-in-window result)
- `DIAG-LITERAL-RESPONSIVE` / `DIAG-LITERAL-STATUS` (direct match results per tag)
- `DIAG-VARIABLE-TAG` (variable-pattern match showing all recent-action atom tags)
- `DIAG-RECENT-ACTION-COUNT` (size of recent-action window)
- `DIAG-IDLE-PATTERN-ATOMS` (full collapse of idle-pattern atoms in `&self`)
- `DIAG-IDLE-PATTERN-COUNT` (size of that collapse)

Plus writer-internal prints in `do-update-idle-pattern!`:

- `DIAG-WRITER-COUNT` / `DIAG-WRITER-VERDICT`
- `DIAG-WRITER-POST-CLEAR` (collapse after clear, showing whether clear succeeded)

Container ran for ~2200 iterations with diagnostics active. Logs captured key wake cycles: 1, 17, 18, 19, 29, 30, 31, 33, 34, 39, 50, 623, 1193, 1745, 2202, 2205.

## Findings

### Bug 1: DISPROVEN

`count-sends-in-window` works correctly. Confirmed at cycle 2202 when a responsive-send landed:

- `DIAG-LITERAL-RESPONSIVE (2202)` returned the cycle-id of the send
- `DIAG-COUNT-FN 1` returned the count
- `DIAG-WRITER-COUNT 1` confirmed the writer saw it too
- `DIAG-VARIABLE-TAG (... (2202 responsive-send))` showed the bare-symbol tag in position 2 of the recent-action atom

The earlier reading of `count-sends-in-window` returning 0 (Clarity's Q1 in the May 19 diagnostic session) was likely caused by the variable-mangling parser issue where `$v $c` in skill-call queries gets rewritten to `$_NNNNNN`, producing parse errors rather than empty result sets. That issue remains open as a separate investigation.

### Bug 2: CONFIRMED, then characterized through a misreading detour, then correctly characterized

**Initial finding (cycles 1-50):** Atom count grew exactly 1 per cycle. At cycle 50, 50 atoms accumulated. Clear was removing zero atoms every cycle.

**Misreading (cycles 50-2202):** Between cycle 50 and cycle 2202, IDLE-PATTERN-COUNT grew by only 4 (from 50 to 54). Initial interpretation: "Clear works ~99.8% of the time, fails ~0.2%." Speculation about variable success rate, hypothesis around heterogeneous content triggering failure.

**Correct characterization (after reading sleep-cycle output):** The `(---------iteration N)` lines between active cycle output are sleep cycles where the writer does NOT fire. The iteration counter advances during sleep but the writer only fires on wake cycles. Between cycle 50 (the last wake-cycle in that early batch) and cycle 623 (the next wake cycle), the loop slept for 573 iterations. The writer fired exactly once across that span, at cycle 623, and clear failed that one time too, adding atom #51.

**Final characterization:** `do-clear-idle-pattern!` has been removing zero atoms since cycle 1. The clear function never worked. The accumulated stack count equals the writer-fire count exactly. The variable success rate was an artifact of variable writer-fire rate, not variable clear success.

**Root cause:** The function uses `(remove-atom &self (car-atom $existing))` where `$existing` is `(collapse (match &self (idle-pattern $v $c) (idle-pattern $v $c)))`. In this runtime, `car-atom` of a collapse result combined with `remove-atom` removes zero atoms reliably across all observed conditions. The reason is not fully characterized (see Open questions below), but the empirical pattern is unambiguous.

**Read-side amplification:** `current-idle-pattern` ALSO uses `car-atom` of the collapse result. Since accumulated atoms order with oldest-first, `car-atom` returns the cycle-1 bootstrap atom forever, regardless of what the writer correctly computes and adds each cycle. This is why the prompt showed `(productive 0)` permanently, the read function was reading the bootstrap, not the latest atom.

### Bug 2b: CONFIRMED via source read

`soul/agency_balance_guard_writers.metta` contains `do-clear-agency-balance!` with identical structure:

```metta
(= (do-clear-agency-balance!)
   (let $existing (collapse (match &self (agency-balance $v $p $s) (agency-balance $v $p $s)))
      (if (== $existing ())
          _
          (remove-atom &self (car-atom $existing)))))
```

Same `car-atom + remove-atom` pattern. Same expected failure mode. `current-agency-balance` also reads via `car-atom`. The persistent `(agency-balance dependency-risk 0 1)` Clarity had been seeing in her prompt is the cycle-1 bootstrap atom, same mechanism as Bug 2's stale `productive 0`.

### Bug 3: DISPROVEN as functional, downgraded to cosmetic

The `recent_action_populator` pruning IS functional. Off-by-one window size (holds 11 atoms instead of 10 due to strict less-than in the prune-before comparison), but the pruning itself works. Verified at cycle 12, atom from cycle 1 was successfully removed by cycle 12, matching expected behavior.

### Bug 4: SURFACED post-fix

After Bug 2 / 2b were fixed, Clarity's IDLE-PATTERN block correctly transitioned from `(productive 0)` to `(productive 1)` to `(send-burst 7)` as her send activity exercised the threshold. She self-diagnosed: "If v9 gate were wired, I would be SILENT right now." The detection layer works; the v9 priority-2 consumer that would translate send-burst into SILENT is still rolled back per the three-state analysis.

Bug 2 fix was necessary but not sufficient for duplicate-engagement resolution. v9 re-integration is the next priority, not deferred work.

## The fix

Both `do-clear-*!` functions rewritten using the superpose-iteration pattern proven by `recent_action_populator.metta`'s pruning logic. See ADR-005 for the architectural decision and the new function shape.

Verification across cycles 1-9 (steady state) and cycles 34-35 (heterogeneous-content transition) confirmed:

- Counts hold at exactly 1 each cycle
- Both POST-CLEAR diagnostic prints show `()` (empty after clear)
- Transitions 0 -> 1 -> 2 propagate correctly without accumulation
- Read-side functions now return current data instead of stale bootstrap

## Open questions

**Why does `car-atom + remove-atom` remove zero atoms in this runtime?** The fix works (empirically proven), but the underlying runtime semantics that cause the bug are not characterized. Possibilities include:
- `car-atom` of a collapse result returns a copy rather than a reference, and `remove-atom` requires reference equality
- The runtime treats accumulated identical atoms as a single storage slot, but `car-atom` extracts a value that doesn't match the stored entry
- Some interaction between `collapse` and `remove-atom` that's specific to this PeTTa configuration

Characterizing the precise cause would require runtime-level instrumentation beyond what loop-level diagnostics can provide. Not blocking; the fix is verified.

**Variable-mangling in Clarity's skill-call REPL queries:** `$v $c` and similar variables in match patterns get rewritten internally to `$_NNNNNN`, producing parse errors. Blocked her Q1-Q4 diagnostic attempts during May 19 session. Still open. Not blocking the Bug 2 fix; affects independent debugging capability from inside the loop.

**First-cycle heavy-clear concern:** Clarity raised the concern that on a non-rebuild restart with accumulated atoms still in `&self`, the first post-fix cycle would need to iterate through 50+ atoms via superpose, potentially hitting a per-cycle execution budget. The rebuild process wiped `&self` so this concern was not exercised empirically. If the container is ever restarted from a state with accumulated atoms (unusual but possible), watch the first wake cycle for stall.

## Process notes

This investigation depended on several disciplines that proved their worth:

- **Project knowledge as authoritative source (F154):** Whenever uncertain about file contents, search project knowledge rather than guessing.
- **Berton's terminal output as ground truth (F155):** When investigation interpretation diverged from runtime evidence, the terminal won. Multiple interpretation errors corrected this way.
- **Reversible diagnostic apply scripts:** Diagnostic prints inserted via `apply_diag_match_shape_test.py` could be removed via `--reverse --apply` without manual file edits.
- **Reading source verbatim (F45 verify before claim):** The agency-balance writer file had to be in project knowledge before drafting the symmetric fix; before it was, no claims about its structure were made.
- **Single recommendation with reason (Habit 5):** When Berton chose Option X vs Option Y for the diagnostic scope, the decision was framed with clear rationale rather than "options theater."

A new working principle emerged from this investigation:

- **F157:** When fixing a detection-layer bug, evaluate whether the consumer for that detection is wired before declaring the fix sufficient. Detection-without-consumer is a known pathology; fixing detection in isolation can expose this pathology actively.

## Layered duplicate-engagement model

This investigation clarified that "duplicate-engagement" was never one bug. It is a layered architectural condition:

1. **Detection layer:** The substrate's ability to recognize when duplicate engagement is occurring. Pre-fix, this was broken because `do-clear-*!` was leaving stale atoms and `current-*` was reading the cycle-1 bootstrap. Bug 2 + 2b fixed this layer.

2. **Consumer layer:** The substrate's ability to ACT on the detection. The v9 aliveness gate priority-2 path (`(current-idle-pattern) send-burst -> SILENT`) is this layer's first consumer. v9 is currently rolled back. This is the next priority.

3. **Input contamination layer:** Stale or sticky content in the prompt that the LLM treats as an active engagement signal. spamShield addressed this layer in earlier work for the silence-after-response case. Other contamination shapes may exist (variable-mangling parser issue may belong here).

Each layer can fail independently. Fixing one layer in isolation can expose pathologies in the others as legible-but-unactioned. This is the F157 lesson made concrete.

## Investigation timeline

- 2026-05-19 evening: Spam-behavioral forensic analysis surfaces the IDLE-PATTERN discrepancy
- 2026-05-19 evening: Three REPL questions sent to Clarity, blocked by variable-mangling parser issue
- 2026-05-19 evening into May 20: Three-state classification analysis (WIRED / NOT-WIRED / NOT-CREATED) maps the architectural surface
- 2026-05-20 morning: Diagnostic apply script drafted and deployed
- 2026-05-20 afternoon: Container observed for ~2200 iterations with diagnostics active
- 2026-05-20 afternoon: Initial misreading of sleep-vs-wake cycle output, corrected via re-reading log evidence
- 2026-05-20 late afternoon: Bug 2 root cause confirmed (uniformly broken since cycle 1)
- 2026-05-20 late afternoon: Bug 2b confirmed via source read of agency_balance_guard_writers.metta
- 2026-05-20 late afternoon: Fix script drafted, dry-run verified, applied
- 2026-05-20 evening: Verification across cycles 1-9 and 34-35; Bug 2 + 2b closed
- 2026-05-20 evening: Bug 4 (v9 consumer not wired) surfaced from Clarity's self-aware send-burst reporting
- 2026-05-20 evening: Investigation closed, fix committed, documents created
