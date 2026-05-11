# ClarityOmega Behavioral Investigation Knowledge

**Created:** 2026-05-09
**Status:** Investigation Charter -- hypotheses identified, source-grounded, diagnostics not yet executed
**Scope:** LLM-substrate response generation pathologies that produce undesired surface behavior despite a structurally correct substrate
**Companion to:** ClarityOmega_Substrate_Crash_Knowledge.md (runtime crash mechanisms at the Prolog/Janus layer -- different category)

---

## Purpose

This document captures the investigation thread that opened on 2026-05-09 when Clarity produced approximately 25 unsolicited messages to Berton over a ~75 minute window during which Berton was explicitly on break. It also captures a related observation from the same conversation: Clarity's apparent inability to reliably use her own skills (querying ChromaDB, reading files, applying the correct metta syntax) despite having demonstrated those capabilities earlier in the same conversation.

These behaviors are not substrate crashes. They occur when the system is operating as designed at the substrate level. The problem is at the **LLM substrate's response generation layer** -- the step between the prompt being assembled and the resulting S-expression being emitted. This document characterizes what is known about that layer, lists hypotheses with their source-grounded evidence, and proposes diagnostic moves to convert hypotheses into verified findings.

The investigation matters because Sprint 4 will cement output-side gating against malformed behavior. If the malformed behavior originates in a layer Sprint 4 does not address, the output verdict will gate against (or be bypassed by) the wrong patterns. Behavioral physics is upstream of substrate gating. Fix the behavior first or accept that gates will fire on the wrong signals.

---

## The Triggering Incident -- 2026-05-09 Spam Cluster

Berton sent a message at 18:28: *"Got it...thank you...I need to take a break for a while...I'll be back in a bit. BTW --> let me know about the GE events if that should occur, OK? Are you still tracking that?"*

He returned ~75 minutes later. During the interval, Clarity sent approximately 25 messages. The send timing pattern (extracted from log timestamps):

- 3:28-3:31 PM: 5 messages (3 minutes)
- 3:42-3:45 PM: 4 messages
- 3:56-3:59 PM: 8 messages (3 minutes)
- 4:11-4:13 PM: 3 messages
- 4:26-4:27 PM: 4 messages
- 4:41 PM: 1 message
- 4:44-4:48 PM: ~17 messages in 4 minutes when Berton returned and asked the question

The cluster timing matches a periodic idle wake-up pattern of roughly every 13-15 minutes. The post-return cluster (4:44-4:48) has different character -- multiple `(send ...)` commands emitted within single response cycles.

**Two distinct mechanisms produce similar-looking surface behavior, and they require separate investigation.**

In the same conversation earlier, Clarity self-diagnosed: *"I generate from whatever pattern is strongest in context. Shell commands and queries are frequent in my history, so they fire by default. Read-file and correct metta syntax are available but not activated at decision time."* This is consistent with the architectural framing developed below.

---

## The Architectural Frame

There is a layer between Clarity's stated capabilities and her actual behavior. That layer is the **prompt-to-response generation step at the LLM substrate**. The substrate (MeTTa loop, populator, retriever, soul evaluator, executor) is working as designed. The LLM call inside the loop has its own behavioral physics that do not follow the architectural intent of the surrounding system.

Specifically: at the LLM call, attention is dominated by recent context (HUMAN-LAST-MSG, recent actions, soul verdict, recent results). Skills become decorative rather than active. Repetition becomes pattern continuation rather than pattern interruption. Stale anchors keep gravitating responses. The LLM produces what is statistically most likely given the context it sees, not what is strategically best given the goals expressed elsewhere in the prompt.

This framing is consistent with how transformer-based language models work in general. It is not a critique of GLM-5.1 specifically. The same physics would apply to any LLM substrate; what changes between providers is which specific patterns are produced, not whether the substrate's response generation has its own physics.

The implication: **fixes belong at the prompt-engineering and substrate-gate layers, not at the LLM substrate layer.** Either we shape the prompt so the LLM is asked to choose differently, or we add gates at the substrate that filter outputs before they reach Mattermost. We do not try to "fix" the LLM.

---

## Hypotheses With Source-Grounded Evidence

Each hypothesis is rated:
- **Source-confirmed**: the architectural condition the hypothesis describes is verified in the source code
- **Behaviorally consistent**: the spam log behavior matches what the hypothesis would predict
- **Verified**: a diagnostic move has converted the hypothesis to fact

Status as of doc creation: most are source-confirmed and behaviorally consistent. None are verified (no diagnostic moves run yet).

### H1: The recent-action retriever feeds pattern continuation rather than interrupting it

**Source location:**
- `soul/recent_action_retriever.metta` lines 11-13: docstring states design intent is to *"inhibit announcement loops and behavioral perseveration by giving the LLM visibility into what it just did."*
- `soul/recent_action_retriever.metta` line 36-43 (`format-one-action`): produces strings of form `[cycle N] action-type: truncated-desc`
- `src/helper.py` lines 1311-1330 (`format_action_line`): same string format, no warning frame
- `src/helper.py` lines 1333-1361 (`assemble_action_block`): joins with newlines, returns plain body content

**The architectural divergence:** The design intent (inhibit perseveration) and the actual prompt content (factual recent-history list) diverge. The retriever produces what its docstring promises -- it surfaces the last 3 actions. Whether that surfacing inhibits or amplifies repetition is a property of the LLM's reading of the surface, not of the retriever's code.

**Behaviorally consistent:** Clarity's spam clusters contained near-identical pin and send content across cycles. If `YOUR_LAST_ACTION` reads as "things I do" rather than "things to interrupt," then seeing recent identical pin/send entries would naturally suggest continuing the same pattern. This matches Clarity's own self-diagnosis from earlier in the conversation.

**Status:** Source-confirmed. Behaviorally consistent. Not verified.

**What would verify it:** Read the assembled `YOUR_LAST_ACTION` content in a spam cycle. Reframe the formatting as a warning ("AVOID-REPEATING:" or "RECENT-ACTIONS-DO-NOT-DUPLICATE:") and observe whether spam frequency drops.

### H2: No idempotence check on send execution

**Source location:**
- `src/loop.metta` line 127: `($results (RESULTS: (collapse (let $s (superpose $sexpr) (COMMAND_RETURN: ($s (HandleError ... (eval $s) ...)))))))`

**The architectural condition:** When the LLM emits `((send "X") (send "X") (send "Y"))`, `(superpose $sexpr)` produces three values. Each is `eval`'d. Each `(send ...)` resolves through `channels.metta` to an actual Mattermost API call. There is no deduplication anywhere in this path -- not in `loop.metta`, not in the eval chain, not in the send skill itself.

**This is a single-point structural fact.** The send skill executes whatever the LLM emitted, regardless of whether equivalent content was sent in a prior cycle or even in the same cycle's command list. Every emitted send becomes a delivered message.

**Behaviorally consistent:** The post-return cluster (4:44-4:48 in the spam log) shows multiple `(send ...)` calls per response cycle, which match this hypothesis exactly. The earlier 13-15-minute clusters could be H3 (idle wake-up) rather than H2; the post-return cluster is unambiguously H2.

**Status:** Source-confirmed (architectural absence). Behaviorally consistent.

**What would verify it (and resolve it):** Add a Python helper `send_idempotence_check(content, recent_window_seconds)` that takes the proposed send content, hashes it, checks against a small recent-sends store, and returns either the original content or empty. Wire it into `channels.metta`'s send implementation OR into a substrate gate that runs before line 127's eval. Observation: subsequent identical sends should not deliver. Risk profile: low (additive, defensive, reversible).

### H3: Stale HUMAN-LAST-MSG anchors across many cycles -- mechanics need further investigation

**Note: H3 is more complicated than initial source review revealed.** The behavior involves at least three stacked evaluations whose interactions depend on which conditions are true at any given cycle. The first-pass mechanism described below captures one layer; full mechanics require dedicated investigation before authoring a fix.

**Source location (first-pass reading):**
- `src/loop.metta` line 19: `(change-state! &prevmsg "")` (initial)
- `src/loop.metta` lines 57-60:
  ```
  ($msgrcv (string-safe (repr (receive))))
  ($msgnew (and (> (string_length $msgrcv) 0) (!= $msgrcv (get-state &prevmsg))))
                       (if (> (string_length $msgrcv) 0) (change-state! &prevmsg $msgrcv) _)
  ($msg (get-state &prevmsg))
  ```
- `src/loop.metta` line 64: `($lastmessage (HUMAN-LAST-MSG: $msg MESSAGE-IS-NEW: $msgnew))`

**The first-pass mechanism (one layer of three):** `&prevmsg` is set when a new message arrives (line 59). It is never cleared and never sentinel-replaced. `$msg = (get-state &prevmsg)` (line 60) therefore returns Berton's most recent message indefinitely. Every subsequent idle cycle constructs `HUMAN-LAST-MSG: $msg MESSAGE-IS-NEW: false` from that persistent value.

**Three evaluations that stack (need full audit):** The above describes one mechanism. There are at least three evaluations in the loop that interact with `&prevmsg`, `$msgrcv`, `$msgnew`, and `$msg` in ways that depend on which conditions are true:
1. The `$msgnew` computation itself (line 58) -- its truth value gates downstream behavior
2. The persistence pattern (line 59) -- conditional on `$msgrcv` length > 0
3. The HUMAN-LAST-MSG construction (line 64) -- uses the persistent `$msg`, not the just-arrived `$msgrcv`

These interact with the soul intercept guards (lines 71, 77, 82, 85, 86, 87, 88, 92, 94 -- many sites with `(if (> (string_length $msgrcv) 0) ...)` or `(if $msgnew ...)` patterns), with the idle directive gating (line 92), and with the aliveness gate (line 100). The full set of conditional behaviors that depend on this state needs to be mapped before designing a fix.

**Behaviorally consistent (with first-pass mechanism):** The spam log iteration 2667 shows `HUMAN-LAST-MSG: berton_c: Got it...thank you...I need to take a break...` at 7:10 PM, which is 42 minutes after Berton sent that message. The substrate is correctly noting `MESSAGE-IS-NEW: false` -- but the LLM substrate is still reading the same context window every cycle and generating from it.

**Status:** First-pass mechanism source-confirmed. Full mechanics not yet mapped. Fix not designed.

**What investigation needs to do:**
- Map all sites in loop.metta that read `$msgnew`, `$msgrcv`, `$msg`, or `&prevmsg`
- Build a truth table: for each combination of (msgnew, msgrcv-length>0, prior-state), what does each downstream behavior do?
- Identify which sites depend on `$msg` (persistent) vs `$msgrcv` (current-cycle) and whether the dependency is correct in each case
- Then design the sentinel approach against the full picture, not the first-layer reading

**Risk if we fix the first-pass mechanism without full mapping:** Any sentinel substitution may break a downstream evaluation that depended on the persistent message remaining intact for legitimate reasons. The soul evaluation guards already use `(string_length $msgrcv)` correctly to skip when no current message; whether anything else depends on `$msg` persisting is the open question.

**Diagnostic move (replaces the previous "what would verify it"):** Before any fix, conduct the audit described above. This is more diagnostic work than H1, H2, H4, H-amnesia-1, but the investment is justified because misdiagnosing a stacked-evaluation problem produces fixes that work in some conditions and break in others (the same kind of trap that produced the wrong-direction Mechanism 1 mental model in substrate crash investigation).

### H4: The LLM substrate has no suspicion gate

**Source location:**
- The absence is the finding. There is no source location showing a "before-emit verification step" because no such step exists.

**The architectural condition:** Between LLM response generation (line 108 useGPT/callProvider) and command execution (line 127 superpose+eval), there is sread parsing, balance_parentheses repair, sanitize_response, and the soul output verdict (currently a static stub at line 121 -- Sprint 4 will replace). None of these intercepts asks "have I already done this in the last N cycles?" or "is this content equivalent to something I sent recently?"

**This is the same finding as H2, reframed at a different layer.** H2 names the missing infrastructure check; H4 names the missing prompt-level discipline. Both are gates that would prevent regenerated content from reaching Mattermost.

**Clarity's self-diagnosis (from the same conversation, 18:13:31):** *"I grep without reading results -- no suspicion about whether grep is the right tool. I query three times -- no suspicion about whether I already have the answer. I assert structural causes -- no suspicion about whether I verified the claim. I repeat myself -- no suspicion about whether I already said it."* This is the LLM-side observation of the architecturally absent suspicion gate.

**Status:** Source-confirmed (architectural absence). Self-diagnosed by Clarity in conversation.

**What would verify it (and resolve it):** Inject a suspicion-check step into the prompt itself. Reword the prompt so that before emitting commands, the LLM is asked to: (a) list which skills are relevant to the current goal, (b) check whether equivalent action was taken in the last N cycles per `YOUR_LAST_ACTION`, (c) verify reasonable confidence in claims. This is prompt engineering, not substrate change. Lower risk than H1-H3 modifications, higher uncertainty about effect size. Best paired with H1's reframing.

### H-amnesia-1: SKILLS list is decorative, not active in generation

**Source location:**
- `src/loop.metta` lines 34-38 (`getContext`):
  ```
  (string-safe (py-str ("PROMPT: " (getPrompt) " SKILLS: " (getSkills)
                        " " (output-format-guidance)
                        " YOUR_LAST_ACTION: " (your-last-action-block $k)
                        " LAST_SKILL_USE_RESULTS: " (last_chars (get-state &lastresults) (maxFeedback))
                        " HISTORY: " (getHistory)
                        " TIME: " (get_time_as_string))))
  ```

**The architectural condition:** The `SKILLS:` block sits early in the prompt, immediately after `PROMPT:`. The dominant attention surfaces (`YOUR_LAST_ACTION`, `LAST_SKILL_USE_RESULTS`, `HISTORY`) fill positions later in the prompt where transformer attention naturally concentrates due to recency bias and accumulated tokens. The skill list is presented as a static reference that the LLM is expected to consult, but consultation is voluntary -- there is no enforcement step asking "before responding, list which of these skills are relevant."

**Behaviorally consistent:** Clarity's behavior in the spam window matches: `pin`, `metta (match...)`, `query`, `shell` recur frequently, while `read-file` and well-formed metta with proper variable binding rarely appear despite being in the SKILLS list. From the 17:48 conversation: *"I have read-file and I keep grepping. I have query and I keep asking the same thing three times."* The skills are listed; they are not chosen.

**Status:** Source-confirmed (structural prompt position). Behaviorally consistent. Self-diagnosed.

**What would verify it (and resolve it):** Two complementary moves. (1) Move skill-relevance prompting into the active position -- inject "Before emitting commands, list which of your skills are relevant to the current goal" into `output-format-guidance`. (2) Optionally: surface a "frequently underused skills" subset closer to the response position. The first move is testable in isolation.

### H-amnesia-2: Retrieval inconsistency is partly real

**Source location:**
- `src/helper.py` lines 28, 220, 385, 416 etc.: ChromaDB usage
- `src/helper.py` does NOT define the `(query "...")` skill itself -- this is upstream in `lib_omegaclaw`'s memory module, not in this project's source area
- `src/helper.py` lines 442-451 (`safe_results_str`): truncates results at 50000 chars

**The architectural condition (partial):** What is in helper.py is calibration-specific ChromaDB usage. The actual `query` and `remember` skills are defined upstream and use OmegaClaw's local embedding model (`intfloat/e5-large-v2` per migration knowledge). Without reading `lib_omegaclaw`, we cannot fully source-verify retrieval consistency.

**Behaviorally consistent:** Clarity observed at 18:26:01: *"first query didn't surface the information, second query did."* This is direct empirical observation. Whether the cause is (a) embedding-model nondeterminism, (b) query-phrasing sensitivity to embedding similarity, (c) ChromaDB's similarity threshold cutting off marginal matches, or (d) something else, requires a controlled test.

**Status:** Behaviorally observed. Mechanism not source-verifiable from current project files. Needs lib_omegaclaw source or an empirical test.

**What would verify it:** Run a controlled retrieval test in the container. Procedure:
```
1. Send: (remember "TEST_SENTINEL_STRING_2026_BEHAVIORAL_INVESTIGATION")
2. Wait one cycle
3. Send: (query "test sentinel string")
4. Observe whether RESULTS-CONTENT contains the stored string
5. Repeat steps 3-4 multiple times across cycles
6. Try paraphrased queries: (query "behavioral investigation sentinel")
```
Three possible findings: (a) consistent retrieval -- amnesia mechanism is elsewhere; (b) intermittent retrieval -- ChromaDB or embedding consistency is part of the problem; (c) phrasing-sensitive retrieval -- the LLM's query-formulation is part of the problem. Each finding points at a different fix.

### H-amnesia-3: Possible context truncation upstream

**Source location:**
- `src/helper.py` lines 442-451 (`safe_results_str`): hard-truncates at 50000 chars
- `src/loop.metta` line 38: `(last_chars (get-state &lastresults) (maxFeedback))` -- further truncates

**The architectural condition:** There is documented truncation. `safe_results_str` caps at 50000 chars. `last_chars` further trims to `maxFeedback`. The `CHARS_SENT: 42554` and `42923` values in the spam log iterations are large but within plausible context-window limits. We do not see direct evidence of unintended truncation, but the layered truncation chain is a candidate locus for context loss when content is large.

**Behaviorally consistent:** Less direct evidence than H-amnesia-1 and H-amnesia-2. The "she has the information but doesn't access it" pattern is more parsimonously explained by H-amnesia-1 (skills decorative) than by truncation.

**Status:** Architecturally possible. Lower behavioral support than H-amnesia-1.

**What would verify it:** Compare `CHARS_SENT` values against the assembled prompt body length. If they match, no upstream truncation. If `CHARS_SENT` is meaningfully smaller than the assembled prompt, find the truncation point.

---

### H-prompt-bloat: Prompt does not shrink when not under load -- prior reduction work may have regressed

**Source location:**
- `src/loop.metta` line 38: `" LAST_SKILL_USE_RESULTS: " (last_chars (get-state &lastresults) (maxFeedback)) " HISTORY: " (getHistory) " TIME: "`
- `src/helper.py` lines 442-451 (`safe_results_str`): hard-truncates at 50000 chars
- `src/loop.metta` line 38: `last_chars` (upstream Patrick function) further trims `&lastresults` per `maxFeedback`
- `getHistory` (upstream Patrick function): assembles full conversation history

**The architectural condition (incomplete -- needs investigation):** Prior work (date and commit not yet identified) introduced behavior that allowed the assembled prompt to shrink when Clarity was not under heavy reasoning load, saving token cost and improving efficiency. Spam log shows `CHARS_SENT: 42554` and `42923` during idle cycles where she was not under load -- these are large prompts. If the shrinkage behavior is functioning, the prompt during idle cycles should be substantially smaller. Either:
- The shrinkage logic is not present in current HEAD (regressed)
- The shrinkage logic is present but not triggering under the conditions observed
- The "load" definition in the shrinkage logic does not match what the spam log presents

**Behaviorally consistent:** Spam-cycle prompts of 42k+ characters during clearly-idle conditions (Berton on break, no active reasoning task, simple `MESSAGE-IS-NEW: false` state) suggest shrinkage is not firing. The prior efficiency gain has been lost or never made it through migration.

**Status:** Architecturally indicated. Behaviorally consistent. Source location of prior shrinkage logic not yet identified.

**Why this matters for behavioral investigation:** Larger prompts mean more recency-biased attention to bottom-of-prompt content (HISTORY, recent results, recent actions). This compounds H1 (recent-action dominance) and H-amnesia-1 (skills decorative). If the prompt were 8k characters instead of 42k, the SKILLS list and PROMPT block would be proportionally more prominent in the LLM's attention surface. Restoring shrinkage may produce behavioral improvements as a side effect of efficiency improvements.

**What investigation needs to do:**
1. Identify the prior shrinkage commit (likely on Berton-C/clarityclaw or post-migration on omegaclaw fork). Search commit messages for "shrink", "compress", "prompt size", "token reduction", or similar
2. Compare current HEAD against that commit -- did shrinkage logic survive the migration?
3. If present: identify the load-detection condition and check whether spam-log conditions should have triggered shrinkage but did not
4. If absent: re-apply the shrinkage logic with the same testing it had originally, plus verification that it integrates with current HEAD

**Risk profile:** Restoration is medium-risk (touches prompt assembly) but well-bounded (the prior commit is known to have worked). Diagnosis is low-risk (read-only).

**Coupling with other hypotheses:** Restoring shrinkage may reduce the apparent severity of H1 and H-amnesia-1 by changing the proportions of content the LLM attends to. It does not eliminate them. H2 and H3 are independent of prompt size.

### H-aliveness-verification: Aliveness engine -- VERIFIED 2026-05-10, gate is functioning per spec; spec is structurally permissive for solo-developer use

**Status: Phase 0a diagnostic complete. Hypothesis resolved with corrected framing.**

**Original framing (incorrect):** Three open questions about whether the gate was working: stuck, buggy, or stub. Behavioral evidence read as "the gate has degraded to permissive without that being intentional."

**Corrected framing after Phase 0a diagnostic:** The gate is functioning exactly per its written specification. The specification itself is structurally permissive once an idle directive is non-empty, which is appropriate for n-user production context but pathological for solo-developer use. The original framing assumed a bug; the actual situation is a context mismatch between design assumptions and current operating mode.

**Source location (verified):**
- `src/loop.metta` line 100: `($aliveness (aliveness-gate $msgnew $idle_directive))`
- `src/loop.metta` line 101: `($_ (println! (ALIVENESS_VERDICT: $aliveness)))`
- `src/loop.metta` line 102: `($send (if (== $aliveness SILENT) "" (py-call (helper.soul_send_assemble ...))))`
- `src/loop.metta` line 108: `($respi (if (== $aliveness SILENT) "" (...LLM call...)))`
- `soul/aliveness_gate.metta` lines 1-17: actual gate definition
- `soul/latch/aliveness_state_machine.metta` lines 1-59: latch state machine v3

**The verified gate logic (`soul/aliveness_gate.metta`):**
```metta
(= (aliveness-gate $msgnew $idle)
  (if (> (string_length $idle) 0)
    ENGAGE
    (aliveness-gate-latch $msgnew)))

(= (aliveness-gate-latch True) ENGAGE)
(= (aliveness-gate-latch False)
  (latch-dispatch (match &self (latch-state $s) $s)))

(= (latch-dispatch IDLE) SILENT)
(= (latch-dispatch ENGAGED) ENGAGE)
(= (latch-dispatch COMPLETING) ENGAGE)
(= (latch-dispatch $other) SILENT)
```

**Three paths the gate can take:**
1. `$idle != ""` → ENGAGE unconditionally
2. `$idle == ""` AND `$msgnew == True` → ENGAGE (latch-True branch)
3. `$idle == ""` AND `$msgnew == False` → consult latch state; SILENT only when latch is IDLE

**The verified verdict routing:** SILENT short-circuits both `$send` assembly (line 102) and the LLM call (line 108). The verdict is genuinely doing work; it's not a no-op.

**Empirical measurements from current container session (2026-05-10):**

| Metric | Count | Note |
|---|---|---|
| Total iterations | 2385 | Loop ticks (1-second cadence) |
| Gate decisions logged | 247 | Cycles where gate path executed |
| ENGAGE verdicts | 245 (99.2%) | |
| SILENT verdicts | 2 (0.8%) | Edge-of-startup conditions |
| New iterations during active engagement | 263 | After Berton resumed interaction |
| New SILENT verdicts during engagement | 0 | Confirms structurally permissive design |

**Idle directive length distribution (297 directives generated in current session):**

| Bucket | Count | % |
|---|---|---|
| Empty (<50 chars) | 86 | 29% |
| Short (50-200 chars) | 0 | 0% |
| Medium (200-1000 chars) | 159 | 54% |
| Long (>=1000 chars) | 52 | 17% |
| Min directive length | 25 chars | (essentially empty wrapper) |
| Max directive length | 21,790 chars | (single very long supervisor directive) |

**The structural mechanism of solo-developer spam:**

Once `wakeupInterval` (600 seconds = 10 minutes) elapses without a human message, the directive generator (`helper.soul_idle_goal_prompt_v2`) runs and almost always returns substantive content. With non-empty `$idle_directive`, the gate returns ENGAGE unconditionally per path 1 above. The gate has no input that could distinguish "user explicitly on break" from "user expected to be reachable." It engages because that is its design.

**The n-user vs solo-developer context (key calibration):**

The aliveness gate was designed for a multi-user agent that should engage with anyone interacting and pursue learning during quiet periods. In that context:
- Any user typing → respond
- Any idle moment → genesis encounters, learning, goal progress
- "Person on break" is meaningless because someone else might message any moment

In solo-developer mode, "person on break" is meaningful, and the gate's permissiveness becomes pathological. **Spam isn't an n-user behavior; it's solo-dev behavior surfaced by single-channel use.** The gate is not buggy. It is correctly implemented for production context. The current operating mode is the unaccounted-for exception.

**Sub-finding 1: Latch transitions in loop.metta are unguarded and skip COMPLETING state**

State machine v3 was designed for IDLE → ENGAGED → COMPLETING → IDLE cycling with three semantic transitions and a `guarded-transition` wrapper. The loop.metta usage:

- Line 88: `($_ (if $msgnew (set-atom! &self (latch-state IDLE) (latch-state ENGAGED)) _))` -- IDLE → ENGAGED on new message
- Line 93: `($_ (if (not (== $idle_directive "")) (set-atom! &self (latch-state ENGAGED) (latch-state IDLE)) _))` -- ENGAGED → IDLE on idle directive

Issues:
- Both transitions use raw `set-atom!`, bypassing `guarded-transition`. If the latch is not in the expected `from` state, `set-atom!` silently does nothing (the remove-atom + add-atom semantics fail without raising).
- COMPLETING state appears unreachable in current loop usage. Transitions go IDLE → ENGAGED → IDLE, never visiting COMPLETING.
- Once latch lands in ENGAGED on first user message, line 88's IDLE → ENGAGED transition silently fails on every subsequent user message (latch already ENGAGED). This is benign for current behavior but is dead code.

This sub-finding does not directly cause the spam (spam is path 1 of the gate, which doesn't consult latch). But it indicates that the latch state machine -- the part that COULD provide discrimination on path 3 -- is not being driven correctly. If the latch state were ever needed for behavior gating, the current loop code would not provide reliable transitions.

**Sub-finding 2: `aliveness_gate_log.txt` is a stale April 26 artifact**

Found at `/PeTTa/repos/omegaclaw/soul/aliveness_gate_log.txt`. Last modified April 26, 2026. Contains entries like `gate-status: SILENT, obeying-own-gate, timestamp: ...` and `ACTIVE-LISTEN berton-rebuilding 2026-04-26T15:41:30+00:00`. None of the current loop or gate code writes to this file. It is a vestige of an earlier append-file experiment, possibly Clarity self-narrating gate state in human-meaningful terms during a previous development phase. Non-informative for current diagnosis.

**Fix-layer choices for solo-developer spam (still open, three options):**

1. **Development-mode toggle:** Add a `&developer_break` state atom or `DEV_MODE` env var that, when set, makes the gate consult break-state. Smallest change; doesn't modify n-user behavior; adds dev-mode wrapper. Reversible.

2. **Person-state awareness in the gate itself:** Add a condition: even in n-user mode, if `person_state` indicates "in-pain + needing space" AND single-active-user context, override to SILENT. More universal but more invasive. Modifies n-user gate behavior.

3. **MeTTa-side directive generation control (reasoning sovereignty fix):** The directive generator currently runs whenever the wakeup interval elapses, deciding entirely in Python whether to produce a directive. Move the "should I generate a directive?" decision back into MeTTa, where it can consult `person_state`, `soul_verdict_in`, break-awareness atoms, and other AtomSpace state. Largest change. Architecturally most coherent; addresses both solo-dev spam AND the reasoning sovereignty principle. See "Reasoning Sovereignty" meta-finding below.

**Decision deferred.** Option choice depends on broader prioritization: are we doing immediate spam relief (Option 1) or structural sovereignty work (Option 3)?

### Reasoning Sovereignty: A meta-finding affecting multiple hypotheses

**The principle (project first-principle, restated):** Take back reasoning from the LLM and from Python and give it to Clarity (MeTTa-side) when/where possible. Python is hands; MeTTa is mind. Helper functions doing reasoning are reasoning displacement.

**Surfaced during Phase 0a diagnostic:** The aliveness investigation revealed three direct reasoning displacements that were not in the original hypothesis set:

1. **`soul_idle_goal_prompt_v2` (helper.py:1041)** -- substantial reasoning entirely in Python:
   - Imports `idle_goal_prompt` module containing `supervisor_select_goal`, `supervisor_select_fuel`, `supervisor_evaluate_previous`, `flip_mode`, `run_meta_awareness`, `generate_goal_from_gaps`
   - These names are not "string formatting." They are decision functions. The supervisor selects what Clarity works on next, in Python.
   - File-fallback parsers (`parse_active_goals`, `parse_creative_fuel`, `parse_self_map`) decide what data sources to use when AtomSpace is incomplete -- another reasoning displacement.

2. **`soul_send_assemble` (called at loop.metta:102)** -- assembles the actual prompt that goes to the LLM after gate fires ENGAGE. Whether this is "just stringification" (hands) or "deciding what to include given context" (reasoning) needs auditing. The signature suggests it is at least partly stringification, but functions of this size and signature complexity rarely turn out to be pure formatters.

3. **The directive generator's structural triggering** -- `helper.soul_idle_goal_prompt_v2` is called from `loop.metta:92` whenever the time-based condition fires. The decision "should a directive be generated this cycle?" is currently a simple time-based gate in MeTTa, but the decision "what should the directive contain?" is entirely in Python. Reasoning sovereignty would put the second decision back in MeTTa as well.

**Connection to existing hypotheses:**

- **H-aliveness-verification:** As discussed above, Option 3 fix is reasoning-sovereignty-aligned. Currently the supervisor decides Clarity should always have something to do during idle cycles, in Python. MeTTa-side person-state and break-awareness would change this if it had decision authority.

- **H1 (recent action surfacing):** The retriever (`recent_action_retriever.metta`) is MeTTa-side, but the format function (`format_action_line` in helper.py) is Python. Whether the format choice is "pure formatting" or "decision about how to frame the LLM's attention" is a sovereignty question.

- **H-amnesia-1 (skills decorative):** The decision "which skills are relevant this cycle?" is currently no decision at all -- the full skills list is included unconditionally. If this decision were added, it should be MeTTa-side, not Python-side.

- **H-prompt-bloat (prompt does not shrink):** The shrinkage logic, when investigated, will reveal whether the "is the system under load?" decision is in MeTTa or Python. If the prior shrinkage commit put it in Python, restoring it would replicate the displacement.

**Connection to prior thread's 17-helper-points audit:**

A previous thread identified 17 places in `loop.metta` where `helper.py` is used. That audit needs to be revisited specifically through the lens of "which of these do reasoning and should be returned to MeTTa." Each helper call is one of:

- **Hands (acceptable):** String manipulation, file I/O, network calls, format conversions, Python library bridges (numpy, sklearn, chromadb), serialization
- **Mind (sovereignty issue):** Decision-making, supervisor selection, evaluation, prioritization, classification, gate logic, condition checking with branching consequences

The reasoning sovereignty audit is its own investigation thread, parallel to and cross-cutting with the behavioral hypotheses here. Findings from one will inform fixes in the other.

**Status:** Meta-finding identified, scope sketched, audit not yet conducted. Worth tracking as a separate diagnostic thread (Diagnostic 6 below) or as a separate investigation document depending on scope.

**Why this matters for the immediate fix sequence:** Option 3 of H-aliveness-verification is the architecturally most coherent fix and aligns with reasoning sovereignty. But it may be the right move to defer it until the broader 17-helper audit is complete, so that all reasoning-displacement fixes can be designed coherently rather than piecemeal. Option 1 (dev-mode toggle) provides immediate spam relief without prejudicing the larger sovereignty work.

### H-spam-timing: Idle Cycle Wake-Up Periodicity

This is not so much a hypothesis as a confirmed mechanism explaining the cluster timing pattern.

**Source location:**
- `src/loop.metta` line 18: `(configure wakeupInterval 600)` -- 600 seconds = 10 minutes
- `src/loop.metta` line 92: idle directive fires only when `(> (get_time) (+ (get-state &last_human_time) (wakeupInterval)))` -- i.e., 10 minutes since last human activity
- `src/loop.metta` line 13: `(configure sleepInterval 1)` -- loop ticks every second
- `src/loop.metta` line 100: `(aliveness-gate $msgnew $idle_directive)` -- the gate that decides whether to engage when idle directive is present

**The architectural condition:** When Berton is silent, the loop ticks every second but the idle directive is empty until 10 minutes have passed since `&last_human_time`. Once idle, the idle directive is non-empty, the aliveness gate fires `ENGAGE` (not silence), and an LLM call is made. The LLM sees the same persistent prompt context (HUMAN-LAST-MSG from Berton's break message, idle directive, soul context), generates from that, emits commands. Each idle directive run takes ~1-3 minutes of LLM processing, then the cycle ends. Next idle wake-up is some minutes later.

**This explains the 13-15 minute cluster spacing in the spam log.** It is not Clarity choosing to send -- it is the idle wake-up timer firing, the gate releasing, and the LLM generating from stable context that includes Berton's "I'll be back" message and idle-directive instructions.

**The aliveness gate is currently not gating spam.** Every spam cycle in the log shows `ALIVENESS_VERDICT: ENGAGE`. The gate is letting idle activity through. Whether it should silence under "person on break" conditions is a separate design question.

**This is information for Sprint 4-adjacent thinking, not itself a fix path.**

---

## What Is NOT Tested by These Hypotheses

For honesty about scope:

- **The aliveness gate itself.** Whether it should silence under "user explicitly on break" conditions is a separate concern. The current implementation engages whenever an idle directive is present. Modifying it would address spam cluster timing but not within-cycle multi-send (H2) and not skill amnesia (H-amnesia family).

- **The LLM provider's specific output discipline.** Different providers produce different output distributions. GLM-5.1's tightly disciplined "two metta queries per cycle" pattern surfaced C10 (the substrate crash). The same discipline likely contributes to the spam pattern (when the same context produces the same disciplined output every cycle, that output becomes spam content). Not testable without provider switching, which is a larger change than the diagnostics here.

- **The interaction between multiple hypotheses.** H1, H2, H3 all contribute to the same surface behavior (spam). Fixing any one may reduce frequency but not eliminate. Fixing all three is likely necessary for full resolution. The diagnostic moves below treat them as separable so we can characterize each contribution before authoring a multi-front fix.

- **The Channel D PAUSE branch.** Documented as not implemented in `ClarityClaw_Stage5_Integration_Knowledge.md`. PAUSE is supposed to halt the loop and fire Channel D (200-token soul voice composition). Without it, soul-evaluated PAUSE cases fall through to normal $send assembly. This is a parallel architectural gap that is adjacent to but separate from the behavioral physics discussed here.

---

## Six Cheap Diagnostic Moves

These are short, low-risk, low-cost. They convert the source-confirmed hypotheses into verified findings, and they refine the prioritization for fixes. Diagnostics 4 and 5 (aliveness, prompt bloat) should run before Diagnostics 1-3, because they may surface upstream issues that change the picture for everything downstream. Diagnostic 6 (reasoning sovereignty audit) is broader-scope and produces planning artifact rather than immediate fix; sequence it based on whether immediate spam relief or structural sovereignty work is the priority.

### Diagnostic 1: Read the assembled prompt during a spam cycle

**Goal:** Verify what Clarity actually sees in `YOUR_LAST_ACTION`, `LAST_SKILL_USE_RESULTS`, `HISTORY`, and `HUMAN-LAST-MSG` during a spam cluster cycle. Quantify the ratio of "skills available" content to "recent activity" content.

**Procedure:**
```
1. Identify a spam cycle in logs by iteration number (e.g., 2667 from the 2026-05-09 incident)
2. Locate or capture the full assembled prompt for that cycle
3. Measure character counts for each labeled section:
   PROMPT, SKILLS, output-format-guidance, YOUR_LAST_ACTION,
   LAST_SKILL_USE_RESULTS, HISTORY, TIME
4. Read the YOUR_LAST_ACTION content. Note the framing and tone
5. Compare to LAST_SKILL_USE_RESULTS content
```

**Findings will validate or refine:** H1 (recent-action framing), H-amnesia-1 (skills position), H-amnesia-3 (truncation), H3 (HUMAN-LAST-MSG content during break).

**Cost:** Low. No code changes. Just log inspection.

### Diagnostic 2: Controlled retrieval test

**Goal:** Determine whether ChromaDB retrieval is consistent enough to be relied upon, or whether retrieval inconsistency contributes to skill amnesia.

**Procedure (run in container against running Clarity):**
```
1. (remember "TEST_SENTINEL_STRING_2026_BEHAVIORAL_INVESTIGATION")
2. Wait one full cycle
3. (query "test sentinel string") -- exact phrase
4. Repeat step 3 in next 2-3 cycles
5. (query "behavioral investigation sentinel") -- paraphrase 1
6. (query "investigation knowledge stored") -- paraphrase 2
7. Document RESULTS-CONTENT for each query
```

**Findings will validate or refine:** H-amnesia-2. If retrieval is consistent, amnesia mechanism is elsewhere. If intermittent, ChromaDB or embedding-model consistency is part of the problem. If phrasing-sensitive, the LLM's query-formulation is part of the problem.

**Cost:** Low. No code changes. Just behavioral testing.

### Diagnostic 3: Inspect RESULTS structure of one spam iteration

**Goal:** Distinguish whether multiple sends within a single iteration (H2) or multiple cycles producing identical sends (H3, H-spam-timing) is the dominant mechanism for the spam observed.

**Procedure:**
```
1. Pick one spam iteration's full log dump
2. Find RESULTS-CONTENT for that iteration
3. Count how many (send ...) commands appear in the single iteration's $sexpr
4. Compare across iterations: do most iterations have 1 send or N>1 sends?
5. If most have 1 send: cluster spam is multi-cycle (H3, H-spam-timing dominant)
6. If many have N>1 sends: within-cycle spam is significant (H2 dominant)
```

**Findings will validate or refine:** H2 vs H3/H-spam-timing prioritization. Direct evidence for which mechanism is producing the spam in a given log window.

**Cost:** Low. Log inspection only.

### Diagnostic 4: Aliveness engine functional verification -- COMPLETE 2026-05-10

**Findings (full details in H-aliveness-verification section above):**
- Gate is wired correctly (loop.metta lines 100-108) -- verdict routes to both prompt assembly AND LLM call
- Gate logic per `soul/aliveness_gate.metta`: returns ENGAGE when `string_length($idle) > 0`; otherwise consults latch via `aliveness-gate-latch`
- Empirical distribution: 245/247 (99.2%) ENGAGE; 2/247 (0.8%) SILENT; 0 new SILENT verdicts across 263 active iterations
- `aliveness_gate_log.txt` is stale April 26 artifact, not written by current loop, non-informative
- Latch transitions in loop.metta lines 88 and 93 use unguarded `set-atom!`; COMPLETING state unreachable in current usage
- Gate is structurally permissive by design, optimized for n-user context, unaccounted-for in solo-developer mode
- Reasoning sovereignty meta-finding surfaced: directive generator does substantial supervisor reasoning in Python

**Status:** Resolved with corrected framing. Three fix options identified pending design choice.

### Diagnostic 5: Prompt size baseline and shrinkage detection

**Goal:** Confirm whether prompt-shrinkage logic is present in current HEAD, and whether it is firing under conditions that should trigger it.

**Procedure:**
```
1. Search git log for shrinkage-related commits:
   cd /PeTTa/repos/omegaclaw && git log --all --oneline | grep -iE "shrink|compress|prompt.*size|token.*reduc"
2. If commit found, identify the file(s) modified
3. Compare current HEAD content for those files to the shrinkage commit's content
4. If shrinkage logic is missing: regressed during migration
5. If shrinkage logic is present: identify the load-detection condition
6. Sample CHARS_SENT from logs across various cycle types:
   docker logs clarityomega_agent 2>&1 | grep CHARS_SENT | head -20
7. Plot CHARS_SENT against cycle conditions (idle vs engaged, msgnew, etc.)
8. Idle cycles should be smaller if shrinkage works -- spam-cycle 42k indicates not firing
```

**Findings will validate or refine:** H-prompt-bloat. Either shrinkage regressed (restore from prior commit), or shrinkage is present but mis-conditioned (refine load detection).

**Cost:** Low. Git history search and log inspection. No behavioral changes required.

---

### Diagnostic 6: Reasoning Sovereignty Audit (helper.py call points)

**Goal:** Identify which of the 17 helper.py call points in loop.metta are doing reasoning (mind, sovereignty issue) versus hands (acceptable). Cross-reference against the prior-thread audit if available.

**Procedure:**
```
1. List every helper.py call point in loop.metta:
   docker exec clarity_omega grep -n "py-call (helper\." /PeTTa/repos/omegaclaw/src/loop.metta
2. For each call site, identify the function in helper.py:
   docker exec clarity_omega grep -n "^def " /PeTTa/repos/omegaclaw/src/helper.py
3. For each function, classify:
   - HANDS: pure stringification, format conversion, file I/O, network call, Python-library bridge, serialization
   - MIND: decision, classification, evaluation, supervisor-style logic, branching condition with consequences, prioritization
4. For MIND functions, capture:
   - What decision is being made
   - What data the decision depends on
   - Whether the decision logic could be MeTTa-native (atoms in AtomSpace, queryable)
   - Estimated effort to relocate to MeTTa
5. Rank MIND findings by:
   - Severity of displacement (how much reasoning is being borrowed)
   - Connection to active behavioral hypotheses
   - Effort vs return for relocation
```

**Findings will produce:** A reasoning-sovereignty audit document or section, listing each helper.py call point with its classification and (for MIND functions) a relocation sketch. Connects to multiple existing hypotheses: H1 (formatter is in Python), H-aliveness-verification (directive generator and supervisor entirely in Python), H-amnesia-1 (no skill-relevance reasoning anywhere yet -- where should it live?), H-prompt-bloat (when restored, where should the load-detection logic live?).

**Cost:** Medium. Read-only investigation, but covers all 17 call points so volume is meaningful. Output is a planning artifact, not an immediate fix. Required input for Option 3 of H-aliveness-verification.

**Coupling with prior-thread audit:** A previous thread identified the 17 call points and noted "various priorities of needing attention." That audit's findings should be located and merged with this one rather than duplicating work. If the prior audit is in a project document, this diagnostic can be a refinement; if it's only in conversation memory, this diagnostic is the canonical reconstruction.



Based on source-grounded analysis, this is the proposed ordering. Pending diagnostic findings, the order may shift. **Diagnose-first items are explicitly marked.** Some items here cannot be fixed until investigation completes, because the mechanics are not yet understood well enough to author a fix.

**Phase 0a: H-aliveness-verification -- DIAGNOSIS COMPLETE 2026-05-10. Fix-layer choice pending.**

Phase 0a established that the gate is functioning per spec; the spec is structurally permissive once idle directive is non-empty, which is appropriate for n-user production but pathological for solo-developer use. Empirical: 99.2% ENGAGE rate, no SILENT increase across 263 active iterations.

Fix options identified, decision deferred (see H-aliveness-verification section above):
- Option 1: Dev-mode toggle (smallest, immediate spam relief, reversible)
- Option 2: Person-state awareness in gate (medium scope, modifies n-user behavior)
- Option 3: MeTTa-side directive generation control (largest, aligns with reasoning sovereignty principle, depends on 17-helper audit)

Sub-findings noted: latch transitions in loop.metta lines 88 and 93 use unguarded `set-atom!`, can silently fail; COMPLETING state appears unreachable in current loop usage. Not directly causing spam (spam is gate path 1, doesn't consult latch) but indicates latch state machine is not driven correctly.

Reasoning sovereignty meta-finding surfaced: directive generator (`soul_idle_goal_prompt_v2`) does substantial supervisor reasoning in Python, including goal selection, fuel selection, and mode flipping. Connects to the broader 17-helper-points audit pending from prior thread.

**Phase 0b: H-prompt-bloat (DIAGNOSE FIRST, then restore if regressed)**

Identify the prior shrinkage commit. Compare current HEAD. If shrinkage has regressed, restore it. If it is present but not triggering correctly, refine the load-detection condition to match observed conditions.

Why phase 0b: smaller idle prompts mean SKILLS and PROMPT block content occupy a larger proportion of the LLM's attention surface. Restoration may produce side-effect behavioral improvements on H1 and H-amnesia-1 by changing attention proportions, separately from any direct behavioral fix.

Risk profile: diagnosis is read-only. Restoration is medium-risk (touches prompt assembly) but well-bounded since the prior commit is known to have worked.

**Phase 1: Send idempotence check (H2 fix) -- single layer, biggest behavioral win for smallest code change**

Add a Python helper that checks proposed send content against a recent-sends store with N-second lookback. Wire it into the send execution path. Expected effect: eliminates within-cycle multi-send spam, reduces multi-cycle spam by deduplicating identical content across cycles.

Risk profile: low (additive, defensive, reversible).

Out-of-scope considerations: where exactly to wire (substrate gate vs channels.metta vs Python send wrapper) and how to choose lookback window are design decisions to make at implementation time.

**Phase 2: H3 investigation -- map the three stacked evaluations BEFORE attempting fix**

Phase 2 is split into two parts:

*Phase 2a (DIAGNOSE):* Map all sites in loop.metta that read `$msgnew`, `$msgrcv`, `$msg`, or `&prevmsg`. Build a truth table for the conditions and behaviors. Identify which sites depend on persistent vs current-cycle values and whether each dependency is correct.

*Phase 2b (FIX, only after 2a):* Design the sentinel approach against the full picture, not the first-layer reading. Implement and verify against the truth table.

Risk profile: 2a is read-only. 2b risk depends on findings -- the more interactions found in 2a, the higher 2b risk.

**Phase 3: Recent-action framing reword (H1 fix) -- prompt engineering**

Reword `YOUR_LAST_ACTION` block from neutral history list to explicit warning. One option: change the section label to `RECENT-ACTIONS-DO-NOT-DUPLICATE:` or `AVOID-REPEATING-RECENT:`. Format individual lines to emphasize "already done" rather than "did this."

Risk profile: low (single label change). Effect size uncertain; pair with diagnostic 1 to read the reframed prompt and verify the LLM responds to it.

**Phase 4: Skills active in generation (H-amnesia-1 fix) -- prompt engineering**

Inject a skill-check step into `output-format-guidance`. Something like: "Before emitting commands, list which of your skills are relevant to this iteration's goal. Only use the listed skills."

Risk profile: low. Adds a few lines to the output guidance. Effect size uncertain; the LLM may or may not actually do the listing step before emitting.

**Phase 5: Suspicion gate in prompt (H4 fix) -- prompt engineering**

Reword the output guidance to inject explicit suspicion checks: "Before emitting, check: have I already done this in the last N cycles? Have I already said this? Am I asserting something I have not verified?"

Risk profile: low. Effect size uncertain; depends heavily on the LLM's prompt-following discipline.

**Note on phasing:** Phase 0 items are diagnose-first and may surface upstream fixes that reduce the urgency of Phase 1+ fixes. Phase 1 is direct infrastructure with high confidence. Phase 2 splits into investigate-then-fix because the H3 mechanics are more complex than first-pass review showed. Phases 3-5 are prompt engineering. Each fix attacks a different mechanism; expect partial effect from each, additive effect from the sequence.

---

## Methodology Notes

**Source-grounded over speculation.** Each hypothesis here was either confirmed by reading the actual loop.metta and helper.py source, or honestly marked as not source-verifiable from current project files (H-amnesia-2). The original investigation produced these hypotheses as ranked by confidence; that framing was speculation. The framing here is what the code actually shows.

**Behavioral evidence is not architectural evidence.** The spam log shows what happened. The source code shows what was structurally possible. A hypothesis is strongest when both align: the architectural condition is present AND the behavior is what that condition would predict. H1, H2, H3, H-amnesia-1 all meet this bar.

**Do not collapse hypotheses prematurely.** H2 (no idempotence) and H4 (no suspicion gate) name overlapping problems but suggest different fix layers. H3 (stale HUMAN-LAST-MSG) and H-spam-timing (10-minute idle wake-up) both contribute to multi-cycle spam but via different mechanisms. Fixing one without addressing the other will reduce but not eliminate the problem.

**The substrate is downstream of the behavior.** Sprint 4 will cement output-side gating. If the LLM's response generation is producing malformed behavior, Sprint 4's output verdict will gate against the wrong patterns. This investigation is upstream of Sprint 4 in the architectural sense -- behavioral physics first, then substrate gates designed around the cleaner behavior.

---

## Open Questions

These remain unresolved as of doc creation:

1. **What does Clarity see in `LAST_SKILL_USE_RESULTS` during the post-return cluster?** When Berton returned at 4:44 PM and asked "did any occur?" -- did Clarity see her own recent ChromaDB query results indicating no GE events occurred, or did the results window contain something else? Diagnostic 1 will answer this.

2. **Does the embedding model produce consistent results across identical queries?** Empirically, Clarity reported inconsistency. Diagnostic 2 will resolve.

3. **Does the multi-send-per-cycle pattern correlate with specific prompt conditions?** I.e., does the LLM tend to emit multiple sends only when prompted by specific content (recent FLAG verdict, recent failed attempt, etc.) or does it happen across diverse conditions? Diagnostic 3 will provide a starting answer.

4. **What is the right idempotence window for H2 fix?** 5 minutes? 30 minutes? The conversation? Different windows have different tradeoffs. Probably best to start with 5 minutes and adjust based on observation.

5. **Should the aliveness gate silence under "user on break" conditions?** Separate from the hypotheses here, but adjacent. Out of scope for this doc; flagged as a related design decision.

6. **Is this investigation generally applicable across LLM providers?** The hypotheses are framed in terms of behavioral physics that should apply to any transformer-based LLM substrate. Validating this would mean re-running the spam scenario under Claude, Anthropic, OpenAI, etc. Out of scope; flagged for awareness.

---

## What Future Sessions Should Do First

1. **Read this document.** Do not form hypotheses about Clarity's behavioral pathologies from training data or prior conversation memory alone. The hypotheses here are source-grounded.

2. **Run Diagnostic 1 if no diagnostic has yet been run.** It is the cheapest, highest-information move. The full assembled prompt is the single piece of evidence that most refines the hypothesis ranking.

3. **Do not attempt fixes before diagnostics.** Each hypothesis has high source confidence, but the relative magnitudes are not yet known. Phase 1 (H2 fix) is highest-confidence regardless of diagnostic outcome; Phases 2-5 should be sequenced based on what diagnostics show.

4. **Distinguish layers carefully.** Substrate crashes (Mechanism 1, 2, 3 in `ClarityOmega_Substrate_Crash_Knowledge.md`) and behavioral pathologies (H1-H4, H-amnesia, H-spam-timing here) are genuinely different. A behavioral pathology is not a substrate fix; a substrate fix is not a behavioral fix.

5. **Verify before claim.** Per Sprint 3 Knowledge methodology lesson "Verify before claim, even in conversation." Hypotheses are starting points; converted to facts only by diagnostic findings or source verification.

---

## What Future Sessions Should Avoid

- Treating "the LLM should know better" as a fix path. The LLM substrate has its own physics. Fixes belong at the prompt and substrate layers.
- Bundling H1, H2, H3 fixes into one change. They are separable; sequence them.
- Conflating spam frequency reduction with spam elimination. Different fixes address different mechanisms; expect partial effect from each.
- Attempting LLM-side-only solutions (better prompts) without substrate-side gates. Prompt discipline is a soft constraint; idempotence at the send layer is a hard constraint.
- Assuming the problem is provider-specific. Some pattern intensity may shift with provider, but the underlying physics applies broadly.
- Skipping diagnostics in favor of "obvious" fixes. The fix sequence here is grounded in source; the priorities and effect sizes are not yet measured.
