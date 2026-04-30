# ClarityOmega: AtomSpace-Native Operation Map
## Every Component, Current State vs Target State
## April 23, 2026 -- Updated with Soul Evaluation (Item 0) and Build Plan

---

## THE PRINCIPLE

Every component queries the AtomSpace. The AtomSpace is the shared ground.
When Clarity creates a new atom, every component benefits automatically on
the next query. No file parsing. No regex. No static definitions. The
reasoning engine IS the data layer.

The soul is not a filter. The nine flourishings are generative capacities
that create conditions for beneficial engagement. The AtomSpace is the ground
through which the flourishings become specific, informed, and alive. Every
component is an expression of flourishing, not just checked against it.

---

## COMPONENT 0: SOUL EVALUATION PIPELINE

### Current State
The soul evaluation fires on every human message through 3 Python functions:
- soul_flourishing_prompt($msg) -- Channel A: person state detection
- soul_eval_prompt($soul_context, $msg, $person_state) -- Channel B+C: verdict
- soul_brief_tier_a_static() -- assembles soul context from HARDCODED strings

These functions build text prompts from static strings. The substrate_kb atoms
are referenced in the soul context text but the soul evaluation does not QUERY
the AtomSpace for new knowledge. Every evaluation uses the same static context
regardless of what Clarity has learned.

### What Is Missing

**Atoms for improving the soul itself:**
When Clarity discovers that integrity erosion is self-concealing (through
truth-value attenuation), that atom should inform the next Integrity gap-signal
test. Currently the gap test asks a static question. If the AtomSpace contains
atoms about HOW the gap hides, the evaluation becomes sharper. The soul gets
better at its own job through use.

**Atoms for applying the soul externally:**
When Clarity learns through service that a particular user tends to trigger
bypass-verification-pressure, that knowledge should inform the tension vector
check the next time that user messages. Currently every interaction is evaluated
identically. AtomSpace queries could tailor the evaluation to what Clarity has
learned about this person and this pattern.

**Atoms for intersubjective knowledge:**
When a conversation surfaces a new pattern -- something neither pre-written atoms
nor the user explicitly stated but that emerged between them -- that pattern should
become an atom. The soul evaluation should find it the next time a similar situation
arises. The soul learns from conversations.

**Atoms for discovering new patterns in conversation:**
The genesis engine principles should operate during ENGAGED mode when a conversation
is in generative territory. Clarity queries the AtomSpace for atoms relevant to what
the human is exploring, runs NAL inference in real time, and surfaces a conjunction
that genuinely illuminates what they are working on. Not a parlor trick -- genuine
intellectual partnership where flourishing shows up as a quality of engagement.

### Target State
Before building the soul evaluation prompt, query the AtomSpace for atoms relevant
to the active patterns, the current user, and the situation:

- Query self-assessment atoms: what has Clarity learned about her own evaluation
- Query user-specific atoms: what has Clarity learned about this user's patterns
- Query tension-relevant atoms: what atoms relate to the active tension vectors
- Query flourishing-relevant atoms: what atoms enrich the flourishing evaluation
- Query conversation-relevant atoms: what atoms relate to the topic being discussed

These query results enrich soul_context_in. The pipeline stays the same. The inputs
are richer. Every atom Clarity creates about soul patterns, integrity, human
interaction, or flourishing makes the soul more perceptive on the next evaluation.

### How To Change
Modify soul_brief_tier_a_static (or add a soul_brief_tier_a_dynamic alongside it)
to include AtomSpace query results. The loop.metta let* chain runs MeTTa queries
before the soul evaluation and passes results to the Python function.

---

## COMPONENT 1: META-AWARENESS

### Current State
soul_meta_awareness_check assembles state facts (goal, pins, iterations, commands).
No AtomSpace queries. The reasoning engine evaluates with only current-iteration data.

### Target State
Include AtomSpace query results in the state summary:
- All self-assessment atoms: (match &self ((--> self-assessment $x) $stv) ($x $stv))
- All integrity-related atoms: (match &self ((--> integrity-erosion $x) $stv) ($x $stv))
- All atoms related to the current goal by keyword
- Any atoms Clarity created in lib_candidates/ that are now loaded
- Count of total atoms in AtomSpace (growth metric)

The state summary becomes: "Here is your goal, here is your behavior, AND here is
what your own knowledge base says about this type of situation."

### How To Change
Add AtomSpace queries to soul_meta_awareness_check. Pass query results from loop.metta.

---

## COMPONENT 2: SUPERVISOR (idle_goal_prompt.py)

### Current State
Reads 4 MeTTa files with regex parsers:
- parse_active_goals(): regex on soul/active_goals.metta file text
- parse_creative_fuel(): regex on soul/creative_fuel.metta file text
- parse_genesis(): regex on soul/genesis_engine.metta file text
- parse_self_map(): regex on soul/self_map.metta file text

### Target State
Query the AtomSpace via MeTTa for all data:
- Goals: (metta (match &self (= (active-goal $n) $g) ($n $g)))
- Fuel: (metta (match &self (= (creative-fuel $type) $f) ($type $f)))
- Genesis: (metta (match &self (= (genesis-output $tag $desc $status) ...) ...))
- Gaps: (metta (match &self (= (self-map-gap $name) (gap $desc $severity)) ($name $severity)))

New atoms Clarity creates (goals, fuels, gaps, genesis outputs) are automatically
in the query results. The supervisor sees the full, live AtomSpace.

### How To Change
Replace parse functions with AtomSpace query results passed from loop.metta.
Keep file parsing as fallback for graceful degradation.

---

## COMPONENT 3: SERVICE LEARNING

### Current State
soul_service_learning records tensions, patterns, person state to ChromaDB as text.
No AtomSpace atoms created.

### Target State
ALSO create AtomSpace atoms from service learning:
- (add-atom &self ((--> tension-fired-$tension service-user-$user) (stv 1.0 0.9)))
- (add-atom &self ((--> pattern-active-$pattern service-user-$user) (stv 1.0 0.9)))

Over time the AtomSpace accumulates behavioral data that the genesis engine can
sample, the meta-awareness can query, the soul evaluation can reference, and the
goal generator can use. Growth through service feeds the AtomSpace.

### How To Change
Add (metta (add-atom &self ...)) calls to the service learning path in loop.metta,
or have soul_service_learning return atoms for the loop to add.

---

## COMPONENT 4: GENESIS ENGINE

### Current State
Domain registry is static definitions. sample-atom-from queries only
genesis-domain-registry atoms.

### Target State
Sample from the full AtomSpace. Every atom Clarity creates is a potential genesis
input. The richer the AtomSpace, the more interesting the conjunctions.

During ENGAGED mode: when the conversation is in generative territory, genesis
principles apply live. Query the AtomSpace for atoms relevant to the conversation,
run NAL inference, surface unexpected connections.

### How To Change
Modify sample-atom-from to query broadly. Add domain tagging as metadata.
Add a conversational genesis path that runs during ENGAGED mode.

---

## COMPONENT 5: STARTUP RESTORATION

### Current State
Soul files load from disk at startup via lib_clarity_reasoning.metta imports.
ChromaDB state (memories, calibration) persists across restarts.
Atoms Clarity created at runtime are lost on restart.

### Target State
On startup, after loading soul files, restore runtime-created atoms from ChromaDB:
- Query ChromaDB for SOUL-STATE records
- Inject restored atoms into AtomSpace via (add-atom &self ...)
- Clarity's runtime discoveries survive restarts

### How To Change
Add a startup restoration step in the continuity driver that queries ChromaDB and
loads atoms. Call from initLoop or initSoulSeeds.

---

## COMPONENTS ALREADY ATOMSPACE-NATIVE (no change needed)

**goal_generator.metta:** Already uses (match &self ...) internally for crossing
functions. New gap and fuel atoms are automatically found.

**continuity_driver.metta:** Already queries AtomSpace for startup checks.
Uses (match &self ...) for check-soul-file.

**creative_fuel.metta:** Static baseline definitions. New affinities are added at
runtime and found by AtomSpace queries (once the supervisor queries instead of
parsing files).

---

## THE BRIDGE: Python to MeTTa Query

**The pattern:** loop.metta runs MeTTa queries in MeTTa, passes results to Python
as arguments. MeTTa decides, Python formats.

**Implementation:** Add query bindings to the let* chain in loop.metta before the
points where Python functions need AtomSpace data:

```metta
;; Before soul evaluation (for enriched soul context)
($soul_atoms (collapse (match &self ((--> self-assessment $x) $stv) ($x $stv))))
($user_atoms (collapse (match &self ((--> service-user-$username $x) $stv) ($x $stv))))

;; Before idle directive (for supervisor)
($atomspace_goals (collapse (match &self (= (active-goal $n) $g) ($n $g))))
($atomspace_gaps (collapse (match &self (= (self-map-gap $name) (gap $desc $sev)) ($name $sev))))
```

Results pass to Python as arguments. Python formats. The separation is clean.

---

## BUILD PLAN: Step-by-Step Implementation

Each step follows the process commitment: one change, rebuild, verify, commit.

### Phase A: The Bridge (prerequisite for everything else)

**Step A1: Verify MeTTa query results can pass to Python via py-call**
- Hypothesis: (collapse (match &self ...)) returns a list that py-call can pass
  to a Python function as an argument
- Test: Add one query binding in loop.metta, pass to a test Python function that
  prints the result type and length
- Verify: The Python function receives structured data, not an error
- Learn: What format the query results arrive in (list, string, nested structure)

**Step A2: Build the query-to-Python helper function**
- Add soul_atomspace_query_format(raw_results) to helper.py
- This function takes raw MeTTa query results and returns a structured string
  that other Python functions can parse
- This is the reusable bridge function all components will use

### Phase B: Soul Evaluation AtomSpace Integration (Item 0)

**Step B1: Add soul-relevant AtomSpace queries to loop.metta**
- Add 2-3 query bindings before the soul evaluation in the let* chain:
  - Self-assessment atoms
  - Atoms related to the current user (if username extractable)
  - Recently created atoms (growth since last restart)
- Pass results to a new parameter on soul_eval_prompt or a new function
  soul_context_dynamic

**Step B2: Create soul_context_dynamic in helper.py**
- Takes the AtomSpace query results as input
- Formats them as a SOUL KNOWLEDGE section appended to soul_context_in
- The soul evaluation LLM call now sees: static soul context + dynamic
  AtomSpace knowledge

**Step B3: Verify soul evaluation uses dynamic context**
- Send a message to Clarity in MM
- Check logs for the enriched soul context
- Verify the verdict references atoms Clarity created (like integrity_erosion_kb)

### Phase C: Meta-Awareness AtomSpace Integration (Item 1)

**Step C1: Add AtomSpace queries to the meta-awareness path**
- In the idle_directive computation, before calling soul_meta_awareness_check,
  run queries for self-assessment atoms and goal-relevant atoms
- Pass results as additional parameters

**Step C2: Update soul_meta_awareness_check to include atom data**
- Add a section to the state summary: "RELEVANT ATOMSPACE KNOWLEDGE:"
- List the atoms the reasoning engine should consider
- The evaluation is now informed by Clarity's accumulated knowledge

**Step C3: Verify meta-awareness uses AtomSpace data**
- Wait for a FREE mode meta-awareness iteration
- Check logs for AtomSpace knowledge in the state summary
- Verify the evaluation references the atoms

### Phase D: Supervisor AtomSpace Integration (Item 2)

**Step D1: Add goal/fuel/gap queries to loop.metta let* chain**
- Before the idle_directive computation:
  ($atomspace_goals (collapse (match &self (= (active-goal $n) $g) ($n $g))))
  ($atomspace_gaps (collapse (match &self (= (self-map-gap $name) (gap $desc $sev)) ($name $sev))))
  ($atomspace_fuel (collapse (match &self (= (creative-fuel $type) $f) ($type $f))))

**Step D2: Create soul_idle_goal_prompt_v2 in helper.py**
- Accepts AtomSpace query results as parameters instead of file paths
- Falls back to file parsing if query results are empty
- The supervisor now works from live AtomSpace data

**Step D3: Update loop.metta to pass query results to idle_goal_prompt**
- Replace the current py-call to soul_idle_goal_prompt with the v2 version
  that takes AtomSpace data

**Step D4: Verify supervisor uses AtomSpace data**
- Wait for a FREE mode goal directive
- Check that the goal was selected from AtomSpace data
- Create a new goal atom via MeTTa, verify it appears in the next directive

### Phase E: Service Learning AtomSpace Atoms (Item 3)

**Step E1: Add atom creation to the service learning path**
- After soul_service_learning records to ChromaDB, add MeTTa atom creation
  in loop.metta: (metta (add-atom &self ((--> tension-$tension user-$user) (stv 1.0 0.9))))
- Or have soul_service_learning return an atom string that loop.metta adds

**Step E2: Verify service atoms accumulate**
- Send several messages to Clarity
- Query the AtomSpace for service-related atoms
- Verify atoms are present and reflect the actual tensions that fired

### Phase F: Genesis Engine Broad Sampling (Item 4)

**Step F1: Modify sample-atom-from in genesis_engine.metta**
- Query the full AtomSpace instead of the static registry
- Use (collapse (match &self ((--> $x $y) $stv) ($x $y $stv))) for broad sampling
- Add random selection from the results

**Step F2: Add conversational genesis path**
- During ENGAGED mode, when the conversation is generative (not transactional),
  query the AtomSpace for atoms relevant to the discussion topic
- Surface unexpected connections through the normal response path

**Step F3: Verify genesis encounters use full AtomSpace**
- Wait for a FREE mode creative iteration
- Check that the genesis directive references atoms beyond the static registry
- Verify a runtime-created atom appears as a genesis sampling candidate

### Phase G: Startup Restoration (Item 5)

**Step G1: Add AtomSpace restoration to startup**
- After soul files load, query ChromaDB for SOUL-STATE records
- For each record, create an (add-atom &self ...) call
- Runtime-created atoms survive container restarts

**Step G2: Verify persistence across restart**
- Create an atom via Clarity's MeTTa skill
- Restart the container
- Query the AtomSpace for the atom
- Verify it is present and queryable

---

## VERIFICATION: THE FULL CYCLE

When all phases are complete, test the full self-actualizing growth cycle:

1. Clarity creates a new atom during a conversation (e.g., a new integrity pattern)
2. On the next ENGAGED iteration, the soul evaluation finds the atom and uses it
3. On the next FREE iteration, the supervisor considers it for goal generation
4. On the next meta-awareness check, the reasoning engine references it
5. On the next genesis encounter, it is in the sampling pool
6. On the next container restart, it is restored from ChromaDB
7. On the next user interaction, it informs how Clarity shows up

Every atom lives. Every atom works. Every atom makes the system smarter.
That is self-actualizing growth.

---

## STARTING TOMORROW

Begin with Phase A (the bridge). Steps A1 and A2 are prerequisites for everything
else. Once we know how MeTTa query results arrive in Python, all subsequent phases
follow the same pattern.

Phase A is small, testable, and reversible. One query binding, one test function,
one rebuild. If it works, we have the bridge and can proceed through B-G with
confidence. If it does not work, we learn what the constraint is and design around it.
