# ClarityOmega: Consolidated Architecture and Build Status
## April 24, 2026 -- End of Wiring Sessions
## Supersedes: AtomSpace Native Operation Map, Step5b Injection Plan, FREE Mode Effectiveness

---

## PROVEN FACTS (verified at runtime, not assumed)

### The Bridge (Phase A -- COMPLETE)
`(collapse (match &self (= (active-goal $n) $g) ($n $g)))` passed through
`py-call` arrives in Python as a **native list of lists**.

```
type=list
format: [[goal_num, [tier, fuel, name, action, done_when, status]], ...]
```

No string parsing. No regex. Python can index directly. Every subsequent phase
uses this same pattern: MeTTa queries in MeTTa, structured data in Python.

### Three-Mode State Awareness (COMPLETE)
- ENGAGED: human message detected, full soul evaluation fires
- ATTENDING: user recently active within wakeupInterval (600s)
- FREE: no human for one full wakeupInterval, supervisor directive fires
- One state variable: &last_human_time (updated on $msgnew)
- Mode transitions are automatic and correct

### Supervisor-Worker Architecture (COMPLETE, with known issues)
- MeTTa reasoning system is supervisor (selects goals, evaluates progress)
- LLM is worker (receives DIRECTIVE with done-when criteria, executes)
- Directive prepended to prompt (first thing LLM sees after identity)
- Meta-awareness fires every 3 goal iterations
- Goal completion via soul_mark_goal_complete (py-call from Clarity)
- Dynamic goal generation from unaddressed gaps when all goals exhausted
- File-status sync on state load prevents desync between active_goals.metta and idle_state.json

### Known Issues with Supervisor-Worker
- **LLM does not reliably call soul_mark_goal_complete:** Clarity reports goals
  as complete in pins but does not issue the py-call. The history pattern
  dominates behavior over the meta-awareness instruction. This causes the
  supervisor to get stuck on completed goals.
- **Root cause:** History contamination. 30+ cycles of "COMPLETE, IDLE, WAITING"
  in the prompt history override the meta-awareness directive that tells Clarity
  to call the function.
- **Mitigation applied:** File-status sync in get_idle_state() catches goals
  marked complete in active_goals.metta and auto-clears stale current_goal.
- **Real fix:** Phase D (AtomSpace-native supervisor) eliminates the desync
  entirely because the supervisor reads live AtomSpace data, not parsed files.

### Soul Evaluation (OPERATIONAL, not yet AtomSpace-enriched)
- Fires on every human message: Channel A (person state), Channel B+C (verdict)
- Correctly detects bypass-verification-pressure, integrity gaps, safety gaps
- Correctly PAUSEs on requests that violate the priority hierarchy
- Does NOT query the AtomSpace for dynamic knowledge (static prompts only)
- Does NOT use the flourishings as generative capacities (filter-only mode)

### Persistence (OPERATIONAL)
- soul/ directory mounted as Docker volume from host filesystem
- Clarity's runtime file changes persist to Mac, are reviewable and committable
- ChromaDB at /PeTTa/chroma_db, 6663+ docs, memories collection
- idle_state.json in soul/ (persistent via volume mount)
- Container restart preserves soul/ and ChromaDB data
- Runtime-created AtomSpace atoms are NOT persisted (lost on restart)

### Clarity's Autonomous Work (OBSERVED)
- Completed all 10 original goals in ~4 hours of autonomous operation
- Rewrote genesis_autonomous.py as pure Python (no hyperon dependency)
- Created session_bootstrap.py for continuity across restarts
- Created integrity_erosion_kb.metta with live NAL atoms in AtomSpace
- Explored recursive observer-relativity (genuine finding: regress real at
  0.131, mirrors lift to 0.450, further chaining attenuates as predicted)
- Self-corrected on /tmp persistence (moved to lib_candidates after prompt)
- Soul correctly PAUSEd on operator bypass-verification-pressure
- Goal advancement works but requires manual state clearing or file-status sync

### PeTTa Runtime Facts
- loop.metta paren depth +1 is REQUIRED (not a bug)
- maxWakeLoops=50 gives sustained FREE mode iteration
- maxWakeLoops=1 gives single-iteration wake cycles (insufficient for goal work)
- Python module caching: imports inside function bodies still cache at process
  level. Container restart needed for changes to soul/idle_goal_prompt.py
- sleepInterval gives ~4-6 second iteration cadence (1s sleep + LLM call time)
- IDLE_DIRECTIVE must be prepended to prompt, not appended (40K+ chars of context
  overwhelm appended instructions)
- `docker compose down && up` is required for code changes, not just `restart`

---

## THE PRINCIPLE

The soul is not a filter. The nine flourishings are generative capacities that
create conditions for beneficial engagement. The AtomSpace is the ground through
which the flourishings become specific, informed, and alive. Every component is
an expression of flourishing, not just checked against it.

Every component queries the AtomSpace. When Clarity creates a new atom, every
component benefits automatically on the next query. The reasoning engine IS the
data layer. No file parsing. No regex. No static definitions.

Self-actualizing growth means: knowledge creates capability creates knowledge.
An atom Clarity creates today improves every evaluation, goal selection, genesis
encounter, and conversation tomorrow. The atom does not sit idle -- it works
because the systems that need it query the space it lives in.

---

## COMPONENTS: CURRENT STATE AND TARGET STATE

### Component 0: Soul Evaluation Pipeline
**Current:** Static prompts from hardcoded Python strings. Does not query AtomSpace.
**Target:** Query AtomSpace for self-assessment atoms, user-specific patterns,
tension-relevant knowledge, flourishing-relevant atoms, conversation-relevant
atoms. Enriches soul_context_in. Pipeline unchanged, inputs richer.
The flourishings operate as generative capacities: the soul shows up WITH humans
through conversational genesis, not just as a filter messages pass through.
**Status:** NOT STARTED. Depends on proven bridge (Phase A complete).

### Component 1: Meta-Awareness
**Current:** Assembles state facts (goal, pins, iterations). No AtomSpace queries.
**Target:** Include relevant AtomSpace atoms in state summary. Reasoning engine
evaluates with Clarity's accumulated knowledge, not just current iteration data.
**Status:** NOT STARTED. Depends on proven bridge.

### Component 2: Supervisor (idle_goal_prompt.py)
**Current:** 4 regex file parsers. File-status sync added. Dynamic goal generation
from gaps added. Runtime goal advancement via soul_mark_goal_complete.
**Target:** Replace all parsers with AtomSpace query results passed from loop.metta.
supervisor_select_goal reads live AtomSpace data. No regex. No file parsing.
New atoms Clarity creates are automatically in the candidate pool.
**Status:** Phase D ready to implement. Bridge proven. Query format known.

### Component 3: Service Learning
**Current:** Records to ChromaDB as text strings. No AtomSpace atoms created.
**Target:** Also create AtomSpace atoms from service data. Growth through service
feeds the AtomSpace directly.
**Status:** NOT STARTED.

### Component 4: Genesis Engine
**Current:** Static domain registry. Clarity rewrote as pure Python (no hyperon).
Runs on creative mode iterations.
**Target:** Sample from full AtomSpace. Conversational genesis during ENGAGED mode.
**Status:** NOT STARTED.

### Component 5: Startup Restoration
**Current:** Soul files load from disk. ChromaDB persists. Runtime atoms lost.
**Target:** Restore runtime-created atoms from ChromaDB on startup.
**Status:** NOT STARTED.

### Already AtomSpace-Native (no change needed)
- goal_generator.metta: uses (match &self ...) internally
- continuity_driver.metta: uses (match &self ...) for startup checks
- creative_fuel.metta: static baselines, enriched by AtomSpace queries elsewhere

---

## BUILD PLAN

### Immediate: Phase D (Supervisor AtomSpace Integration)

Phase A is complete. The bridge is proven. Phase D is the highest-impact next
step because it eliminates the parser bugs, the desync issue, and makes the
supervisor truly live.

**Step D1: Add goal/fuel/gap/genesis queries to loop.metta**
Add 4 query bindings in the let* chain before $idle_directive:

```metta
($atomspace_goals (collapse (match &self (= (active-goal $n) $g) ($n $g))))
($atomspace_gaps (collapse (match &self (= (self-map-gap $name) $g) ($name $g))))
($atomspace_fuel (collapse (match &self (= (creative-fuel $type) $f) ($type $f))))
```

These are the same pattern as the Phase A test, proven to produce Python lists.

**Step D2: Create soul_idle_goal_prompt_v2 in helper.py**
- Accepts AtomSpace query results as parameters instead of relying on file parsers
- Converts the list-of-lists format into the goal/fuel/gap dicts the supervisor uses
- Falls back to file parsing if query results are empty (graceful degradation)

**Step D3: Update loop.metta py-call to pass query results**
- Replace the current soul_idle_goal_prompt call with v2 that receives AtomSpace data
- Remove the Phase A test binding (soul_atomspace_bridge_test)

**Step D4: Verify**
- Container iterates, supervisor selects goals from AtomSpace data
- Create a new goal atom via MeTTa, verify it appears in the next directive
- Mark a goal complete in active_goals.metta, verify supervisor advances immediately

### After D: Phase B (Soul Evaluation AtomSpace Integration)

**Step B1: Add soul-relevant queries to loop.metta before soul evaluation**
```metta
($soul_atoms (collapse (match &self ((--> self-assessment $x) $stv) ($x $stv))))
($user_atoms (collapse (match &self ((--> service-user $username $x) $stv) ($x $stv))))
```

**Step B2: Create soul_context_dynamic in helper.py**
- Formats AtomSpace query results as a SOUL KNOWLEDGE section
- Appended to soul_context_in before the soul evaluation LLM call

**Step B3: Verify soul evaluation uses dynamic context**

### After B: Phases C, E, F, G

**Phase C (Meta-Awareness):** Add AtomSpace queries to meta-awareness state summary.
**Phase E (Service Learning):** Create AtomSpace atoms from service data.
**Phase F (Genesis):** Broad AtomSpace sampling + conversational genesis in ENGAGED.
**Phase G (Startup Restoration):** Restore runtime atoms from ChromaDB on boot.

Each phase follows the same pattern: add (collapse (match &self ...)) in loop.metta,
pass to Python, use the data. The bridge is proven. The pattern is the same every time.

---

## GIT STATUS

12 commits ahead of origin/main. Key commits:

```
Step 5b: Supervisor directive into LLM prompt
Wire three-mode state awareness (3 commits)
Fix FREE mode: directive prepended, maxWakeLoops 50
Runtime goal advancement: soul_mark_goal_complete
Mount soul/ as persistent volume
Goals 4-6 complete, Clarity runtime work preserved
Phase A test: AtomSpace bridge confirmed (list-of-lists format)
Fix goal desync: sync completed_goals with file status
Dynamic goal generation from gaps
```

---

## FILES CHANGED FROM UPSTREAM (omegaclaw)

**src/loop.metta:** 5 soul insertions (timestamp, service learning, user context,
idle directive, atomspace bridge test), paren depth +1 maintained
**src/helper.py:** 12 functions added (soul_calibration_confidence_query,
soul_pre_compute, soul_user_context_query, soul_user_context_save,
soul_continuity_save, soul_continuity_restore, extract_username,
soul_idle_goal_prompt, soul_service_learning, soul_meta_awareness_check,
soul_mark_goal_complete, soul_atomspace_bridge_test)
**soul/:** 6 core MeTTa files + idle_goal_prompt.py + idle_state.json + Clarity
runtime work (genesis_autonomous.py, session_bootstrap.py, etc.)
**docker-compose.yml:** soul/ volume mount added

---

## STARTING NOW

Phase D, Step D1. Add the query bindings to loop.metta.
