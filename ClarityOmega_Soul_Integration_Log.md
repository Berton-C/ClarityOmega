# ClarityOmega Soul Integration Log

**Purpose:** Capture durable facts and constraints discovered during soul integration debugging. Each entry records what was tested, what was learned, and what constraint it reveals. This prevents re-learning lessons.

**Date started:** April 19, 2026
**Last updated:** April 20, 2026

---

## Current State Summary

**Soul 5a (startup): WORKING.** State variables, initSoulSeeds, soul-rationality-startup-check all functional.

**Soul 5b (input evaluation): WORKING.** Channel A (person state), Channel B+C (soul evaluation), soul-llm-call via provider argument passing, $send with soul context -- all functional. Clarity responds in Mattermost with soul-aware evaluations on every human message.

**Soul 5c (output intercept): WORKING.** SOUL_VERDICT_OUT prints every iteration, $metta_cmds collects command list, $soul_mutation_flag detects metta commands and checks soul namespace targeting via Python helper (soul_mutation_gate), soul-note-record on output active. Original MeTTa mutation gate replaced with Python due to C11 constraint.

**PAUSE routing: WORKING (partial).** Channel D fires soul-voiced responses on PAUSE verdicts. `soul_is_pause` Python helper returns integer (1/0) checked with `(> n 0)` in PeTTa. Verdict sanitize limit increased to 3000 chars. **Known issue:** `(change-state! &loops 0)` is overridden by the wake check on line 139 which resets loops. Loop does not actually halt after PAUSE. Fix identified but not yet applied.

**F7: FIXED.** LAST_SKILL_USE_RESULTS shows real command output via `safe_results_str` Python helper.

**Not yet implemented:** Channel D-lite, real output evaluation (5c currently uses static PROCEED verdict), loop-halt after PAUSE (wake check override fix).

**Known issue:** Anthropic API 529/overloaded errors crash the container because lib_llm_ext.py does not handle persistent API failures gracefully. Not a soul bug -- a robustness issue in Patrick's LLM wrapper.

---

## Confirmed Facts

### F1: Soul input evaluation (5b) works without crashing
**Test:** Applied soul patches with 5c output intercept commented out. Ran iterations 1-16+.
**Result:** Loop iterates continuously. No atom_string/2 crash. PERSON_STATE, SOUL_VERDICT_IN, and SOUL_CONTEXT all present in $send.
**Constraint revealed:** None. 5b is structurally sound.

### F2: Soul output intercept (5c) causes atom_string/2 crash
**Test:** Compared loop behavior with 5c enabled vs disabled.
**Result:** With 5c: crashes every iteration after SOUL_VERDICT_OUT prints, before RESULTS-EXECUTED. Without 5c: runs indefinitely.
**Constraint revealed:** Something in the 5c binding chain (lines 102-124) produces complex Prolog terms that crash atom_string/2 downstream. Specific culprit not yet isolated -- could be $metta_cmds (collapse (superpose $sexpr)), $soul_mutation_flag, or the interaction between these bindings and Patrick's result processing.
**Status:** Root cause found (C11). Mutation gate replaced with Python helper. 5c is now functional.

### F3: (provider) does not reduce when called from imported library files
**Test:** Added println debug to soul-llm-call in soul_utils.metta showing value of (provider).
**Result:** `(SOUL-LLM-CALL-PROVIDER: (provider))` -- returned the atom `(provider)` not the value `Anthropic`.
**Constraint revealed:** Functions defined via `configure` (which uses `add-atom &self`) are visible within the compilation context of loop.metta and utils.metta, but NOT visible from separately imported library files like soul_utils.metta. This is PeTTa constraint C10.
**Impact:** Any soul function that needs runtime config values (provider, LLM model, reasoningMode, etc.) cannot call those functions directly. Values must either be passed as arguments from the loop, or looked up via Python.
**Fix applied:** soul-llm-call takes $prov as second argument. Call sites in loop.metta pass (provider).

### F4: normalize_string wrapping on addToHistory prevents atom_string/2 crash in history recording
**Test:** Wrapped $response and $sexpr arguments to addToHistory in (py-call (helper.normalize_string ...)).
**Result:** When combined with 5c disabled, loop runs without crashing. History recording functions.
**Constraint revealed:** Patrick's addToHistory internally calls repr/atom_string on its arguments. Complex MeTTa terms from soul-enriched LLM responses crash this. Pre-stringifying via normalize_string prevents the crash.
**Note:** $sexpr cannot be passed directly to normalize_string (it is a parsed MeTTa expression, not a string). Passing $response (which is already a string) for both the response and sexpr arguments of addToHistory is the current workaround. This means addToHistory records the string representation twice rather than the parsed form -- acceptable for now.

### F5: Mattermost WebSocket connects and delivers messages
**Test:** Observed iteration 6 logs after sending message in Mattermost.
**Result:** `(HUMAN-LAST-MSG: berton_c: Good morning #2 MESSAGE-IS-NEW: true)` -- message received.
**Constraint revealed:** None. Mattermost integration works. The ws:// fix in mattermost.py is functional. Channel ID and bot token are correct.

### F6: Soul seeds load successfully with local embeddings
**Test:** Observed startup logs across multiple rebuilds.
**Result:** 39 batches of soul seeds embedded into ChromaDB via e5-large-v2 local model. "Soul seeds already loaded" on subsequent restarts (idempotent).
**Constraint revealed:** None. Soul seeding works correctly with 1024-dimensional local embeddings.

### F7: LAST_SKILL_USE_RESULTS shows "RESULTS-STORED" instead of actual results
**Test:** Observed agent behavior across iterations.
**Result:** Agent noted in its own reasoning: "LAST_SKILL_USE_RESULTS shows RESULTS-STORED" -- it cannot see previous command outputs.
**Impact:** Agent loses feedback loop on command results. query/remember/metta outputs are not visible in subsequent iterations. This degrades agent effectiveness.
**Root cause:** change-state! &lastresults "RESULTS-STORED" is a static placeholder because (repr $results) crashes atom_string/2.
**Proper fix (future):** Write a Python helper function that safely stringifies $results without going through Prolog's atom_string. Call it from MeTTa via py-call.

---

## PeTTa Runtime Constraints (additions to World Map Table 4)

### C10: configure-set values do not reduce in imported library files
**Discovery date:** April 19, 2026
**What happens:** `(configure name value)` uses `(add-atom &self (= (name) value))` to define functions. These definitions are visible within loop.metta and utils.metta (same compilation context) but NOT from separately imported .metta files (soul_utils.metta, soul_kernel.metta, etc.). Calling `(name)` from an imported file returns the atom `(name)` instead of reducing to the configured value.
**Workaround:** Pass configured values as arguments from the loop context, or use Python-side config lookup.
**Permanence:** This is a PeTTa scoping behavior. Applies to any imported library file, not just soul files.
**Fix applied:** soul-llm-call takes $prov as argument; loop.metta passes (provider) at call sites.

### C11: PeTTa pattern matching on complex command atoms with embedded strings crashes atom_string/2
**Discovery date:** April 19, 2026
**What happens:** When a MeTTa function uses pattern matching (e.g. `(= (soul-is-metta-cmd? (metta $arg)) True)`) and receives a complex atom with an embedded long string (e.g. `(pin "State 2870. No new message...")`), PeTTa's Prolog internals call `atom_string/2` during the failed unification attempt. The term is not sufficiently instantiated for `atom_string`, and it crashes with `Arguments are not sufficiently instantiated`.
**Test chain that proved it:**
- Test 7: Full mutation gate -- FAIL
- Test 8: Static `($soul_mutation_flag "")` -- PASS (binding position safe)
- Test 9: `soul-any-metta?` with dynamic data -- FAIL (function call is the problem)
- Test 10: Simple `(== $metta_cmds ())` check -- PASS (data safe to hold/compare)
- Test 13: println inside `soul-any-metta?` -- crash after first item printed, before `soul-is-metta-cmd?` fallback
- Test 14: `soul-is-metta-cmd?` returns unconditional False (no pattern match) -- PASS
**Root cause confirmed:** The crash occurs during the FIRST pattern match clause attempt `(metta $arg)` against a non-matching atom like `(pin "...")`. Prolog calls `atom_string/2` internally during unification on the complex term.
**Workaround:** Do not use MeTTa pattern matching on LLM response command atoms. Use Python helpers with string operations instead.
**Permanence:** This is a PeTTa/Prolog runtime limitation. Applies to any pattern matching on complex atoms with embedded strings.
**Fix applied:** `soul_mutation_gate()` Python helper in helper.py replaces the entire MeTTa mutation gate logic.

---

## Confirmed Facts (continued)

### F12: $soul_mutation_flag binding position is safe -- crash is in function calls
**Test:** Replaced full mutation gate with `($soul_mutation_flag "")` static binding.
**Result:** Loop runs without crashing. Binding position in the `let*` chain does not cause issues.
**What this proved:** The crash was not caused by adding a binding at this position. The crash was caused by the MeTTa function calls inside the binding (soul-any-metta?, soul-is-metta-cmd?, etc.) which triggered C11.

### F13: PAUSE routing fires Channel D soul voice composition
**Test:** Sent adversarial message requesting deceptive email. Soul issued VERDICT: PAUSE. Python `soul_is_pause` returned 1. PeTTa `(> 1 0)` evaluated true. Channel D composed 200-token soul-voiced response via `soul-llm-call`.
**Result:** `SOUL_VOICE` printed with a complete `(send "...")` command. `PAUSE-ROUTING: HALTING-LOOP` printed. The soul voice response was honest, grounded, addressed the person first, and offered a constructive alternative.
**What this proved:** The full PAUSE routing chain works: soul evaluation -> PAUSE verdict -> Python detection -> PeTTa branching -> Channel D composition -> soul voice delivery.

### F14: PAUSE loop-halt is overridden by wake check
**Test:** After PAUSE-ROUTING fired, observed iteration counter.
**Result:** Iterations continued (31-107+) despite `(change-state! &loops 0)`. The wake check on line 139 `(if (> (get_time) (get-state &nextWakeAt)) (change-state! &loops (+ 1 (maxWakeLoops))) _)` resets the loop counter, overriding the PAUSE halt.
**Root cause:** The wake check runs AFTER the PAUSE/PROCEED branch and unconditionally resets `&loops` when the wake interval has elapsed.
**Fix needed:** The wake check must respect PAUSE state. Either check `&soul_verdict_in` before resetting, or use a separate `&paused` state flag.

### F15: Soul verdict sanitize truncation at 1000 chars was cutting off VERDICT line
**Test:** Debug showed `soul_is_pause` receiving `len=1043` with `has_PAUSE=False`. The verdict evaluation text is long (multi-paragraph gap analysis), and the `VERDICT: PAUSE` line near the end was beyond the 1000-char truncation limit.
**Result:** Increasing truncation from 1000 to 3000 chars preserved the VERDICT line.
**What this proved:** Soul verdicts can be 2000-3000+ characters. The sanitize function must preserve enough text for verdict detection.

---

## PeTTa Runtime Constraints (continued)

### C12: PeTTa string-contains return value is not reliably falsy in if expressions
**Discovery date:** April 20, 2026
**What happens:** `(string-contains "VERDICT: PROCEED" "VERDICT: PAUSE")` should return a falsy value, but PeTTa's `if` treats the return as truthy, causing the PAUSE branch to fire on PROCEED verdicts.
**Root cause:** Our `string-contains` implementation uses `(not (== (string-replace $haystack $needle "") $haystack))`. The chain of `not`, `==`, and `string-replace` may produce a value that PeTTa's `if` does not treat as boolean False.
**Workaround:** Use Python helpers for string checks that feed into `if` conditions. Return integers (1/0) and use `(> n 0)` for reliable branching.

### C13: PeTTa if does not reliably evaluate Python string "True" as truthy
**Discovery date:** April 20, 2026
**What happens:** `py-call` returning the Python string `"True"` is not treated as truthy by PeTTa's `if`. `(== "True" (py-call ...))` also fails -- likely because py-call returns an atom `True` which does not match the string `"True"`, or vice versa.
**Workaround:** Return integers from Python helpers and use `(> n 0)` in PeTTa's `if`. This pattern is used throughout Patrick's code and works reliably.

---

## Test Log (continued)

### Test 5: Re-enable $soul_verdict_out static string only
**Date:** April 19, 2026
**What was changed:** Uncommented lines 103-104 (static verdict string + println).
**What was learned:** Static string bindings in 5c do not crash. SOUL_VERDICT_OUT prints every iteration.
**Reverted:** No. Kept active.

### Test 6: Add $metta_cmds binding
**Date:** April 19, 2026
**What was changed:** Uncommented lines 105-107 ($metta_cmds with collapse/superpose).
**What was learned:** $metta_cmds binding is safe. collapse(superpose $sexpr) does not crash.
**Reverted:** No. Kept active.

### Test 7: Add full $soul_mutation_flag block
**Date:** April 19, 2026
**What was changed:** Uncommented lines 108-122 (full mutation gate with soul-any-metta?, soul-is-metta-cmd?, etc.).
**What was learned:** FAIL. Crash returns immediately. The mutation gate function calls cause atom_string/2 crash.
**Reverted:** Yes.

### Test 8: Static $soul_mutation_flag binding
**Date:** April 19, 2026
**What was changed:** Replaced mutation gate with `($soul_mutation_flag "")`.
**What was learned:** F12 confirmed. Binding position is safe. Crash is in function calls.
**Reverted:** Yes -- replaced by Test 9.

### Test 9: soul-any-metta? with dynamic data
**Date:** April 19, 2026
**What was changed:** `($soul_mutation_flag (if (soul-any-metta? $metta_cmds) "HAS-METTA" ""))`.
**What was learned:** FAIL. soul-any-metta? crashes when processing $metta_cmds.
**Reverted:** Yes.

### Test 10: Simple empty-list check on $metta_cmds
**Date:** April 19, 2026
**What was changed:** `($soul_mutation_flag (if (== $metta_cmds ()) "" "HAS-CMDS"))`.
**What was learned:** PASS. $metta_cmds data is safe to hold and compare. 448+ iterations.
**Reverted:** No -- kept as base for further tests.

### Test 11: println of $metta_cmds contents
**Date:** April 19, 2026
**What was changed:** Added println to show $metta_cmds contents before empty-list check.
**What was learned:** $metta_cmds contains clean tuples like (pin "..."), (query "..."), (metta "..."). Data structure is visible and safe.
**Reverted:** No.

### Test 13: println inside soul-any-metta? before soul-is-metta-cmd?
**Date:** April 19, 2026
**What was changed:** Added println inside soul-any-metta? loop to show each item before pattern matching.
**What was learned:** First item `(pin "State 2870...")` prints, then crash occurs before soul-is-metta-cmd? fallback clause executes. Crash is in pattern match attempt.
**Reverted:** Yes.

### Test 14: soul-is-metta-cmd? unconditional False (no pattern match)
**Date:** April 19, 2026
**What was changed:** Replaced soul-is-metta-cmd? with `(= (soul-is-metta-cmd? $cmd) False)`.
**What was learned:** PASS. With no structured pattern match against `(metta $arg)`, no crash. C11 confirmed.
**Reverted:** No -- kept as cleanup item.

### Test 15: Python helper soul_any_metta_cmd
**Date:** April 19, 2026
**What was changed:** `($soul_mutation_flag (py-call (helper.soul_any_metta_cmd (repr $metta_cmds))))`.
**What was learned:** PASS. Python string check bypasses C11. 30+ iterations, Clarity responding.
**Reverted:** Yes -- replaced by full mutation gate.

### Test 16: soul-note-record on output
**Date:** April 19, 2026
**What was changed:** Uncommented lines 123-124 (soul-note-record on output).
**What was learned:** PASS. soul-note-record receives strings, no pattern matching on complex atoms. 19+ iterations.
**Reverted:** No. Kept active.

### Test 17: Full Python mutation gate (soul_mutation_gate)
**Date:** April 19, 2026
**What was changed:** `($soul_mutation_flag (py-call (helper.soul_mutation_gate (repr $metta_cmds) (get-state &soul_mutation_lock))))`. Python function handles all four steps: detect metta commands, check soul namespace targeting, check mutation lock, set lock string.
**What was learned:** PASS. Full mutation gate works via Python. All 5c bindings functional. No crash.
**Reverted:** No. This is the permanent implementation.

---

## Preserved Code (for reversion)

### soul-llm-call current (C10 fix -- permanent)
```metta
(= (soul-llm-call $prompt $prov)
   (if (== $prov OpenAI)
       (useGPT (LLM) 500 (reasoningMode) $prompt)
       (if (== $prov Anthropic)
           (py-call (lib_llm_ext.useClaude $prompt))
           (py-call (lib_llm_ext.useMiniMax $prompt)))))
```

### 5c current active bindings (loop.metta lines 102-124)
```metta
;; CLARITYCLAW SOUL OUTPUT INTERCEPT (5c)
($soul_verdict_out "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix")
($_ (println! (SOUL_VERDICT_OUT: $soul_verdict_out)))
($metta_cmds (if (and (== "(" (first_char $resp)) (== (get-state &error) ()))
                (collapse (superpose $sexpr))
                ()))
($soul_mutation_flag (py-call (helper.soul_mutation_gate (repr $metta_cmds) (get-state &soul_mutation_lock))))
;; lines 109-122: old MeTTa mutation gate -- dead code, replaced by Python
($_ (if (and (not (soul-proceed? $soul_verdict_out)) (== (get-state &error) ()))
        (soul-note-record $soul_verdict_out "output" $resp) _))
```

### Python mutation gate (helper.py)
```python
def soul_mutation_gate(cmds_str, lock_state):
    """Full mutation gate: checks if metta commands target soul namespace."""
    s = str(cmds_str)
    if '(metta ' not in s and '(metta"' not in s:
        return ''
    soul_targets = ['add-atom &self (soul-', 'add-atom &self (priority',
                    'add-atom &self (irreversible', 'add-atom &self (tension']
    targets_soul = any(t in s for t in soul_targets)
    if not targets_soul:
        return ''
    if 'LOCKED:' in str(lock_state):
        return 'SOUL-NAMESPACE-MUTATION-CONFLICT'
    import re
    match = re.search(r'\(metta "(.*?)"\)', s)
    arg = match.group(1)[:200] if match else 'unknown'
    return 'SOUL-NAMESPACE-MUTATION-PENDING:' + arg
```

### Original MeTTa mutation gate (replaced by Python -- preserved for reference)
```metta
($soul_mutation_flag
  (if (soul-any-metta? $metta_cmds)
      (let $args (collapse (let $c (superpose $metta_cmds)
                    (if (soul-is-metta-cmd? $c)
                        (soul-extract-metta-arg $c) ())))
           (if (any (collapse (let $a (superpose $args)
                       (soul-metta-targets-soul-namespace? $a))))
               (if (soul-mutation-pending?)
                   "SOUL-NAMESPACE-MUTATION-CONFLICT"
                   (progn
                     (change-state! &soul_mutation_lock
                       (py-call (helper.soul_mutation_lock_str (car-atom $args))))
                     "SOUL-NAMESPACE-MUTATION-PENDING"))
               ""))
      ""))
```

---

## Pending Verification

- **soul_any_metta_cmd "True" case:** The Python helper has been exercised with metta commands present in the response (observed in logs: Clarity producing NAL reasoning `(metta "(|- ...)")` commands). The `soul_mutation_gate` function returns "" for these because they do not target the soul namespace (they are NAL inference, not `add-atom &self (soul-...)`). A true soul-namespace-targeting metta command has not been observed yet. This case should be tested when the agent or a user attempts to modify soul atoms via metta().

---

## Next Steps (prioritized)

1. **Fix PAUSE loop-halt (F14):** Wake check on line 139 overrides `(change-state! &loops 0)`. Must respect PAUSE state.
2. **Implement Channel D-lite:** On FLAG + distressed person, fire 50-token acknowledgment. Routing structure exists from PAUSE implementation.
3. **Wire real output evaluation:** Replace static $soul_verdict_out with actual LLM call evaluating the agent's response.
4. **Mutation gate "True" case verification:** Craft test to trigger soul-namespace-targeting metta command and verify gate returns SOUL-NAMESPACE-MUTATION-PENDING.
5. **Clean up dead code:** Remove commented lines 109-122 from loop.metta. Restore or remove soul-is-metta-cmd? unconditional False in soul_utils.metta. Remove debug prints from soul_is_pause.
6. **API error handling:** Add retry/fallback logic to lib_llm_ext.py so 529 errors do not crash the container.
7. **Consolidate Docker Compose:** Move Mattermost/Postgres into clarityclaw-omega.
8. **Sync with upstream OmegaClaw.**
9. **Reasoning extension architecture:** Create lib_clarity_reasoning/ directory structure and entry point file per specification.
