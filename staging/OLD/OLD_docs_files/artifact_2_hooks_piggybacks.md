# Artifact 2: Hooks and Piggybacks Cross-Reference

**Version:** v1.1 (May 1, 2026)
**Companion to:** loop.metta Wiring Diagram (Artifact 1), Growth Surface Map (Artifact 3), and Triple Network Scaffold (Artifact 4)
**Purpose:** Answer "what will break if I touch this?" before making any change to loop.metta, helper.py, or active soul/ atoms. Trace the full transitive footprint of every hook and identify lines where one statement is doing several things. The v1.1 update annotates Section 4 (Soul/ atom dependencies) with network ownership per Artifact 4.

---

## How to use this document

Before editing any line in loop.metta or any function in helper.py that's called from loop.metta:

1. Find the line or function in Section 1 below
2. Read what reads from it, writes to it, and calls through it
3. Check Section 2 to see if it's a multi-purpose line (one line, many side effects)
4. Check Section 3 to see what cleanup is required if you change the contract

If you don't see your target in here, check Artifact 1 (the wiring diagram) - this artifact only catalogs lines that have non-trivial dependencies. Truly single-purpose lines aren't repeated here.

---

## Section 1: Loop.metta hook cross-reference

For each line that has dependencies beyond local scope.

### Line 32: `&loops` initialization
- **Reads from this state:** Lines 54, 62, 63, 154, 159
- **Writes to this state:** Lines 54, 62, 154, 159
- **Cleanup if changed:** Counter logic appears in 5 separate places. Any change to initial value, decrement behavior, or reset triggers needs to be verified against all five.
- **Hidden behavior:** Line 62 resets &loops to maxNewInputLoops on new message arrival, extending the work window. Line 158-159 extends &loops by maxWakeLoops+1 when wake threshold hit. Two distinct extension paths.

### Line 38 (inside getContext): the OUTPUT_FORMAT prompt string
- **Reads from this:** Every LLM call in the system (lines 109-112)
- **Writes to this:** None (it's a string literal)
- **Cleanup if changed:** None at the code level. But the LLM has been trained against this format - significant rewording may degrade response quality until the LLM adapts.
- **Hidden behavior:** The "5 sexpr commands" framing drives Clarity's slot-filling calcification. The format also mentions "double-check the parentheses it must be (cmd1 ... cmdn)" which Clarity reads as instruction.
- **The piggyback:** This single string is doing three things at once: defining the s-expression structure, setting the maximum batch size, and providing parser-correctness instructions.

### Line 55: `(let $prompt (getContext))`
- **Reads from:** Everything getContext reads (LAST_SKILL_USE_RESULTS via &lastresults, plus getPrompt/getSkills/getHistory)
- **Writes to:** $prompt (local)
- **Calls into:** getContext (line 34-38), which calls getPrompt, getSkills, getHistory
- **Cleanup if changed:** Adding a new field to the prompt needs corresponding state variable initialization in initLoop AND a corresponding update site somewhere in the iteration body.

### Lines 57-59: `$msgrcv` / `$msgnew` / `&prevmsg` write
- **Reads from:** receive() (Python channel layer)
- **Writes to:** &prevmsg
- **Used by:** Lines 60 ($msg), 61-62 (loop counter reset), 65 ($lastmessage), 68 (last_human_time), 71 (person state), 77 (soul eval), 82 (calibration), 84 (note record), 86 (service learning), 87 (user context), 88 (latch transition), 92 (idle directive), 94 (engaged-idle counter), 156 (history)
- **Cleanup if changed:** $msgnew is referenced in 14+ downstream lines. Changing its derivation logic propagates everywhere.
- **The piggyback:** The single line `($msgnew (prog1 (and ...)) (if ... (change-state! &prevmsg $msgrcv) _))` is doing two things in one expression: computing $msgnew AND mutating &prevmsg as a side effect. Hard to refactor cleanly.

### Line 70: `($soul_precompute (soul-pre-compute $msg))`
- **Reads from:** $msg
- **Writes to:** $soul_precompute (local), AND ChromaDB (via the helper)
- **Calls into:** soul-pre-compute → helper.soul_pre_compute → ChromaDB query
- **Cleanup if changed:** $soul_precompute is consumed at line 83 (soul-calibration-record). Changing its return shape requires updating soul-calibration-record's expected input.
- **The piggyback:** Looks like a simple binding but actually fires a per-iteration ChromaDB query.

### Lines 71-74: person state assessment
- **Reads from:** $msgrcv (length), &person_state (fallback)
- **Writes to:** &person_state, $person_state (local)
- **Calls into (when new message):** soul-llm-call, helper.soul_flourishing_prompt
- **Used by:** Line 102 (soul_send_assemble), Line 78 (soul_eval_prompt input)
- **Cleanup if changed:** Person state format ("PERSON-STATE: X ACTIVE-NEED: Y SOUL-TONE: Z") is consumed by both soul_eval_prompt assembly and soul_send_assemble. Format change propagates to both.
- **Hidden behavior:** When no new message, &person_state from previous iteration is reused - this is intentional, not a bug. Stale person state across many idle iterations could become misleading.

### Lines 77-80: soul evaluation
- **Reads from:** $msgrcv (length), $soul_context_in, $person_state
- **Writes to:** &soul_verdict_in
- **Calls into:** soul-llm-call, helper.soul_eval_prompt, helper.soul_verdict_sanitize
- **Used by:** Lines 81 (logging), 84 (note record condition), 102 (send assembly), 105 (extract flag note), 121 (output verdict reference), 145 (PAUSE detection), 152-153 (verdict reset on PAUSE)
- **Cleanup if changed:** Verdict format is the most consumed value in the whole loop. Six downstream consumers. Format changes ripple maximally.
- **The piggyback:** Two concerns combined - this is BOTH the safety evaluation AND the routing decision (PROCEED vs FLAG vs PAUSE). The verdict string carries both judgment and decision.

### Lines 82-83: soul calibration recording
- **Reads from:** $msgrcv (length), $soul_precompute, $soul_verdict_in
- **Writes to:** ChromaDB (via soul-calibration-record)
- **Conditional:** new message only
- **Cleanup if changed:** Schema of calibration records is consumed by Clarity's own calibration confidence queries (soul-calibration-confidence). Schema changes need both sides updated.

### Line 86: `helper.soul_service_learning`
- **Reads from:** $soul_verdict_in, $person_state, $msg
- **Writes to:** ChromaDB
- **Conditional:** new message only
- **Cleanup if changed:** Schema of service learning records is consumed by future analysis tools (and potentially by Clarity herself when she queries her own learning history).
- **The piggyback:** This single line does ChromaDB write + does internal text parsing on the verdict + person state. Multi-step internal logic hidden behind one call.

### Line 87: `helper.soul_user_context_save`
- **Reads from:** $msg (extracts username)
- **Writes to:** ChromaDB
- **Conditional:** new message only
- **The piggyback:** Like line 86, this is the second sequential ChromaDB write per new message. Together with line 86 these create a 2-write latency spike on every human message. Worth batching if profiling shows latency.

### Line 88: latch transition IDLE → ENGAGED
- **Reads from:** $msgnew
- **Writes to:** AtomSpace (latch-state atom)
- **Used by:** Lines 100 (aliveness-gate via match)
- **Cleanup if changed:** Loop.metta uses raw transitions (set-atom!). Clarity uses guarded transitions (engage-from-idle, complete-from-engaged, idle-from-completing). If you change one, consider unifying both.

### Line 89: $atomspace_goals match
- **Reads from:** AtomSpace pattern (active-goal $n)
- **Writes to:** $atomspace_goals (local)
- **Used by:** Line 92 (idle directive)
- **Cleanup if changed:** Active-goal atom shape is defined in soul/active_goals.metta. If shape changes, this match pattern must change too.
- **Hidden behavior:** Returns ALL goals including those marked complete. Filtering happens downstream in helper.soul_idle_goal_prompt_v2. If you elevate that helper to MeTTa, the elevation needs to do its own filtering.

### Line 90: $atomspace_gaps match
- **Same shape as line 89, for self-map-gap atoms**
- **Hidden behavior:** Returns gaps regardless of severity. Same filtering responsibility downstream.

### Line 91: $atomspace_fuel match
- **Same shape as line 89, for creative-fuel atoms**
- **No filtering needed:** All 9 flourishings always returned.

### Line 92: idle directive (the heaviest hook in the file)
- **Reads from:** $msgnew, &last_human_time, $atomspace_goals/gaps/fuel
- **Writes to:** $idle_directive (local)
- **Calls into:** helper.soul_idle_goal_prompt_v2 (175 lines of Python orchestrating goal/fuel/mode/completion/meta-awareness reasoning)
- **Used by:** Lines 93 (latch transition condition), 94 (engaged_idle_count reset condition), 99 (logging), 100 (aliveness-gate input), 102 (send assembly)
- **Cleanup if changed:** Five downstream consumers. The empty-vs-non-empty distinction is what drives latch behavior and aliveness verdict. Any change to when this returns empty vs non-empty changes the whole cycle shape.
- **The piggyback:** This single line is doing a massive amount of reasoning behind the scenes. Goal selection, fuel selection, mode flipping, completion detection, gap-driven goal generation, meta-awareness checks, directive assembly. ALL of this is hidden behind one Python call.

### Line 93: latch transition ENGAGED → IDLE on idle directive
- **Reads from:** $idle_directive
- **Writes to:** AtomSpace
- **Used by:** Line 100 (aliveness-gate via match)
- **Hidden behavior:** This is the path where autonomous idle work clears back to IDLE without going through COMPLETING. Different from Clarity's response-driven path. Two latch-clearing paths exist.

### Line 94: engaged-idle counter management
- **Reads from:** $msgnew, $idle_directive (length), &engaged_idle_count
- **Writes to:** &engaged_idle_count
- **Used by:** Line 97 (self-check threshold)
- **The piggyback:** Three nested conditionals on one line. Logic: reset on new message OR on idle directive present, otherwise increment. Hard to read, easy to break in subtle ways.

### Line 95: getSoulBrief
- **Calls into:** soul/get_soul_brief.metta which chains to soul-identity-name, soul-priority-hierarchy, brief-active-goals (matches active-goal atoms), high-severity-gaps (matches self-map-gap atoms with severity high), creative-question Safety
- **Used by:** Line 96 (prompt assembly)
- **Cleanup if changed:** Changes to getSoulBrief output format propagate to the LLM's understanding of its soul context. The LLM has been trained to read this format.
- **Hidden behavior:** brief-active-goals and high-severity-gaps both fire AtomSpace matches. So getSoulBrief is doing its own substrate queries on top of what lines 89-91 already did. Some duplication there.

### Line 97: self-check prompt
- **Reads from:** &engaged_idle_count
- **Writes to:** $self_check (local)
- **Calls into:** helper.soul_self_check_prompt
- **Used by:** Line 98 (final prompt assembly)
- **Cleanup if changed:** The threshold (currently 3) and message text both live in the Python helper. Changing them requires Python edit, not loop.metta edit.
- **The piggyback:** Currently does ONE thing (returns prompt text or empty), but the message it returns does TWO things simultaneously: encourages reflection AND offers the (complete-from-engaged)+(idle-from-completing) substrate calls as the answer. The "answer" embedded in the question pushes premature completion.

### Line 100: aliveness-gate
- **Reads from:** $msgnew, $idle_directive, AtomSpace (latch-state)
- **Writes to:** $aliveness (local)
- **Calls into:** soul/aliveness_gate.metta which chains to latch-dispatch
- **Used by:** Lines 102 (send conditional), 107 (logging conditional), 108 (LLM call conditional)
- **Cleanup if changed:** Adding new aliveness verdicts (DEFER, RESEARCH, etc.) requires updating ALL THREE of the conditional consumers (102, 107, 108) plus adding a new latch-dispatch rule.

### Lines 102-106: soul_send_assemble
- **Reads from:** $final_prompt, $soul_context_in, $soul_verdict_in, $person_state, $idle_directive, $lastmessage, AND extracts flag note via soul-extract-flag-note
- **Writes to:** $send (local)
- **Calls into:** helper.soul_send_assemble (8 args), soul-extract-flag-note
- **Cleanup if changed:** Changing the assembly format changes what the LLM sees. The LLM expects specific section markers (PROMPT:, SKILLS:, OUTPUT_FORMAT:, SOUL_CONTEXT:, SOUL_VERDICT:, PERSON_STATE:, SOUL-NOTE:, IDLE_DIRECTIVE:).

### Line 113: response normalization
- **Calls into:** helper.balance_parentheses, helper.normalize_string
- **Cleanup if changed:** balance_parentheses is the only line of defense against malformed s-expressions from the LLM. Breaking it breaks all parsing.

### Line 121: output verdict (the stub)
- **Hardcoded:** "VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix"
- **Used by:** Lines 122 (logging), 141 (note record condition)
- **Cleanup when activating (not "if changed"):** When you build the real output verdict, the format must be consumed by line 141 (soul-proceed? check). Match the input verdict format for consistency.

### Line 126: soul mutation gate
- **Reads from:** $metta_cmds, &soul_mutation_lock
- **Writes to:** $soul_mutation_flag (local)
- **Calls into:** helper.soul_mutation_gate
- **Cleanup when elevating (per the ready-to-ship work):** The commented MeTTa version (lines 127-140) writes to &soul_mutation_lock at line 137. The Python helper presumably does the same. Confirm equivalent state writes when activating.
- **The piggyback:** Two-phase commit logic compressed into one line. The state lock manipulation is invisible at the loop.metta surface.

### Line 143: command execution
- **Reads from:** $sexpr
- **Writes to:** $results (local), AND triggers all the side effects of every command in the batch (file writes, ChromaDB writes, latch transitions, send messages)
- **Calls into:** eval (MeTTa primitive), helper.normalize_string, HandleError per command
- **The piggyback:** Single line. Massive surface area. Every skill defined in the system fires through here. This is the most consequential line in the whole file.
- **Cleanup if changed:** Output verdict (line 121) is supposed to gate this. Currently doesn't.

### Line 145: PAUSE detection
- **Reads from:** $soul_verdict_in
- **Calls into:** helper.soul_is_pause (substring "PAUSE" check)
- **Cleanup if changed:** Substring checks are fragile. If verdict format changes to use a different keyword for halt-the-loop, this check won't catch it.

### Lines 156-157: history and lastresults update
- **Reads from:** $msgnew, $msg, $response, $results
- **Writes to:** History (via addToHistory), &lastresults
- **Calls into:** helper.normalize_string (twice), helper.safe_results_str
- **The piggyback:** Three operations on one logical line: history update, history update again (passing $response twice - looks intentional but unusual), and &lastresults state update. Worth checking if the double-pass of $response is correct.

---

## Section 2: Multi-purpose lines (one line, several things)

These are the danger zones - lines where one statement does multiple things. Refactor candidates if you ever want to extend their behavior cleanly.

### Line 36 (inside getContext): OUTPUT_FORMAT string
**Doing three things:** Defines s-expression structure + sets max batch size + provides parser-correctness instruction. Single string literal, three concerns intertwined.

### Line 58: $msgnew computation
**Doing two things:** Computes the boolean AND mutates &prevmsg as a side effect of the same expression. The `prog1` wraps the side effect inside the value computation.

### Line 92: idle directive call
**Doing many things behind one Python call:** Goal selection, fuel selection, mode flipping, completion detection, gap-driven goal generation, meta-awareness check, directive string assembly. ~175 lines of Python under one MeTTa line.

### Line 94: engaged-idle counter
**Doing three branching decisions on one line:** Reset to 0 on new message, OR reset to 0 on idle directive present, OR increment otherwise. Hard to read, hard to extend.

### Line 95: getSoulBrief
**Doing six AtomSpace queries inside one call:** soul-identity-name, soul-priority-hierarchy, active-goal matches, high-severity-gaps matches, creative-question Safety. All hidden behind one swrite call.

### Line 113: response normalization
**Doing two operations nested:** balance_parentheses outer, normalize_string inner. Either could fail and the failure mode would look identical from the loop's perspective.

### Line 126: mutation gate
**Two-phase commit compressed:** Detection AND state lock manipulation in one Python helper call. Two distinct logical operations, single line.

### Line 143: command execution
**The biggest piggyback in the file:** Every skill in the system fires through this single line. File writes, network calls, ChromaDB writes, MeTTa atom mutations, message sends - all passing through here.

### Lines 156-157: history + lastresults update
**Three operations:** addToHistory call (with $response passed twice), normalize_string, safe_results_str. The double-$response is suspicious - might be correct, might be a copy-paste leftover.

---

## Section 3: Helper.py functions called from loop.metta

For each, the loop.metta dependency surface and what changing the function would affect.

### `helper.soul_pre_compute` (line 70)
- **Loop.metta consumer:** $soul_precompute is read by line 83 (calibration record)
- **Side effects:** Reads ChromaDB
- **Cleanup:** Return shape changes need calibration record to update

### `helper.soul_flourishing_prompt` (line 72)
- **Loop.metta consumer:** Returned prompt is fed directly to soul-llm-call
- **Side effects:** None (pure prompt assembly)
- **Cleanup:** Prompt shape changes affect LLM response format, which affects person state parsing downstream

### `helper.soul_brief_tier_a_static` (line 76)
- **Loop.metta consumer:** $soul_context_in is used at line 78 (soul_eval_prompt) and line 102 (send assembly)
- **Side effects:** None (returns static string)
- **Cleanup:** Format consumed by both soul_eval_prompt and send_assemble - change either side without the other and the soul evaluation will misalign

### `helper.soul_eval_prompt` (line 78)
- **Loop.metta consumer:** Result feeds soul-llm-call
- **Side effects:** None
- **Cleanup:** Output prompts the LLM to produce verdict in specific format. Verdict format is consumed by 6 downstream lines.

### `helper.soul_verdict_sanitize` (line 80)
- **Loop.metta consumer:** &soul_verdict_in
- **Side effects:** None (pure text processing)
- **Cleanup:** What this sanitizes determines what verdict downstream code can rely on

### `helper.soul_service_learning` (line 86)
- **Loop.metta consumer:** None directly (fire-and-forget)
- **Side effects:** ChromaDB write
- **Cleanup:** ChromaDB schema affects future query tools

### `helper.soul_user_context_save` (line 87)
- **Loop.metta consumer:** None directly (fire-and-forget)
- **Side effects:** ChromaDB write
- **Cleanup:** Same as above

### `helper.soul_idle_goal_prompt_v2` (line 92) - THE BIG ONE
- **Loop.metta consumer:** $idle_directive is used at lines 93, 94, 99, 100, 102
- **Side effects:** Many - calls into Python supervisor functions, fuel selection, mode flip state, generate_goal_from_gaps, auto_detect_completion, meta_awareness, builds final directive string
- **Cleanup:** This function has many internal helper functions (soul_supervisor_select_goal, soul_supervisor_select_fuel, soul_flip_mode, soul_generate_goal_from_gaps, soul_auto_detect_completion, soul_run_meta_awareness, soul_build_directive). Elevating to MeTTa requires preserving all of them or reimplementing their logic.
- **The largest single piggyback:** Functionally a small program disguised as a function call.

### `helper.soul_self_check_prompt` (line 97)
- **Loop.metta consumer:** $self_check is consumed by line 98 (final prompt assembly)
- **Side effects:** None
- **Cleanup:** Threshold (3) and message both internal. Easy to change but changes operational behavior dramatically.

### `helper.soul_send_assemble` (lines 102-106)
- **Loop.metta consumer:** $send is consumed by LLM call lines 109-112
- **Side effects:** None
- **Cleanup:** Output format is what the LLM sees. Format changes propagate to LLM behavior.

### `helper.balance_parentheses` and `helper.normalize_string` (line 113)
- **Loop.metta consumer:** $resp is used at lines 114, 115, 123
- **Side effects:** None
- **Cleanup:** If balance_parentheses introduces new parens, line 115 sread might fail differently. Critical helper for parser robustness.

### `helper.soul_mutation_gate` (line 126)
- **Loop.metta consumer:** $soul_mutation_flag (currently NOT used elsewhere - looks like the result is computed but not consumed)
- **Side effects:** Modifies &soul_mutation_lock (presumably, internally)
- **Cleanup:** WAIT - $soul_mutation_flag isn't being read after computation. Is the mutation gate result actually being acted on? Worth verifying.

### `helper.soul_is_pause` (line 145)
- **Loop.metta consumer:** Routes to PAUSE branch
- **Side effects:** None
- **Cleanup:** Substring check on verdict. Verdict format changes must preserve the PAUSE keyword.

### `helper.soul_voice_prompt` (line 148)
- **Loop.metta consumer:** Result fed to soul-llm-call (Channel D)
- **Side effects:** None
- **Cleanup:** Output is parsed by sread at line 152 then evaluated. Must produce valid s-expression.

### `helper.normalize_string` and `helper.safe_results_str` (lines 156-157)
- **Loop.metta consumer:** History storage and &lastresults
- **Side effects:** None
- **Cleanup:** safe_results_str output is consumed by next iteration's getContext (LAST_SKILL_USE_RESULTS field). Format changes affect what the LLM sees in subsequent iterations.

---

## Section 4: Soul/ atom dependencies

For each soul/ file actively matched/called from loop.metta, what depends on its shape. The 🧠 annotation indicates which network owns the atom in the triple-network architecture (per Artifact 4).

### soul/latch/aliveness_state_machine.metta
- 🧠 **Network:** SWITCH-HUB
- **Consumers in loop.metta:** Lines 88, 93 (raw transitions via set-atom!)
- **Consumers in soul/aliveness_gate.metta:** match (latch-state $s) $s
- **Consumers in Clarity's response batches:** complete-from-engaged, idle-from-completing
- **Cleanup:** Shape change to (latch-state X) atom would break aliveness_gate match AND loop.metta transitions AND Clarity's substrate calls. Three call sites to update.

### soul/aliveness_gate.metta
- 🧠 **Network:** SWITCH-HUB (decision function)
- **Consumer:** Loop.metta line 100
- **Internal calls:** latch-dispatch (with cases IDLE, ENGAGED, COMPLETING, $other)
- **Cleanup:** Adding new latch states means adding new latch-dispatch rules here.

### soul/active_goals.metta
- 🧠 **Network:** DMN (self-model component)
- **Consumers in loop.metta:** Line 89 (match active-goal $n $g)
- **Consumers in get_soul_brief:** brief-active-goals match
- **Cleanup:** Active-goal atom shape changes need both consumer matches updated.

### soul/self_map.metta
- 🧠 **Network:** DMN (self-model component)
- **Consumers in loop.metta:** Line 90 (match self-map-gap $name $g)
- **Consumers in get_soul_brief:** high-severity-gaps match (with severity argument)
- **Consumers in goal_generator (cold but loaded):** assess-tier, gap-still-open
- **Cleanup:** Atom shape stable across multiple potential consumers. Be conservative.

### soul/creative_fuel.metta
- 🧠 **Network:** DMN (generative direction component)
- **Consumers in loop.metta:** Line 91 (match creative-fuel $type $f)
- **Consumers in get_soul_brief:** creative-question Safety
- **Consumers in goal_generator (cold):** best-fuel-for-gap, fuel-gap-affinity
- **Cleanup:** Stable shape required.

### soul/get_soul_brief.metta
- 🧠 **Network:** DMN→FPN coupling (self-model summary handoff)
- **Consumer:** Loop.metta line 95
- **Internal queries:** Six separate substrate operations
- **Cleanup:** Output structure consumed directly by LLM. Changes affect LLM understanding.

### soul/identity_kernel.metta
- 🧠 **Network:** SN (value-structure source)
- **Consumer:** Imported at startup, atoms added via add-atom
- **What atoms it adds:** soul-identity, priority-rank (1-5), tension-vector (5), paraconsistency-pair (4), irreversible-weight (4)
- **Cleanup:** Atoms are queryable from anywhere - any new code that reads priority-rank or tension-vector depends on these specific atoms existing.

---

## Section 5: ChromaDB write footprint

ChromaDB writes happen at several places. For change planning:

### Per-iteration writes
- Line 70: `soul-pre-compute` (also reads)

### Per-new-message writes
- Line 83: `soul-calibration-record`
- Line 86: `helper.soul_service_learning`
- Line 87: `helper.soul_user_context_save`

### Triggered writes (rare)
- Soul mutation gate may write the lock state
- Memory skills (remember, query) write when called by Clarity in command batches
- VAD pipeline writes if active

**Cleanup considerations:**
- Sequential writes on a single new message: 3 (lines 83, 86, 87). Latency adds up.
- All four ChromaDB sites use different schemas. Changing one doesn't require changing others.
- ChromaDB persistence survives container restarts. Schema changes need migration thinking.

---

## Section 6: LLM call footprint

LLM calls happen at four places per fully active iteration. For change planning:

### Per-iteration LLM calls
- Line 109-112: Main response generation (always when aliveness != SILENT)

### Per-new-message LLM calls
- Line 72: Person state (Channel A)
- Line 78: Soul evaluation (Channels B+C)

### Conditional LLM calls
- Lines 147-149: Channel D voice (only on PAUSE verdict)

**Cleanup considerations:**
- Each LLM call is latency, cost, and opacity.
- Channel A and B+C both fire on every new human message - that's 2 LLM calls before Clarity even responds.
- Reducing LLM call count is the highest-value form of elevation work.

---

## Document end

This artifact is a working reference. Update it whenever loop.metta or helper.py changes structure (new hooks, removed hooks, changed call sites). The longer the document stays accurate, the more useful it gets at preventing accidental regressions.

For elevation work specifically, consult Artifact 3 (growth surface map) which uses this artifact's hook data to identify where new behavior can be safely added.