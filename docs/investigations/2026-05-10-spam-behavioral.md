# Investigation: Spam Behavioral Pathology

**Date:** 2026-05-10
**Tag:** `investigation-2026-05-10-spam-behavioral`
**Status:** CONCLUDED, fix work begins with F-HISTORY-CONTAMINATION
**Triggering incident:** 2026-05-09, Clarity sent ~25 unsolicited messages during a 75-minute Berton break, then multi-send burst on his return

---

## Front Matter

### Summary

Source-grounded diagnostic investigation into Clarity's spam behavior on May 9. The architectural picture is two-layer send governance under FIVE contamination sources, with Layer 1 having a structural option-set limitation that prevents it from reaching the pathology. Send governance exists and works mechanically; spam happens because upstream contamination produces input that overwhelms what the layers can catch, and because Layer 1 cannot say "stop engaging" — only "engage differently." Clarity's diagnosis from inside the container is the operative framing: contamination must be fixed before input reaches either reasoning layer.

The diagnosis went through several reframings. What initially looked like absent send governance turned out to be active but narrow. What initially looked like recoverable scaling logic turned out to never have existed as deliberate code. What initially looked like three contamination sources turned out to be five once Clarity surfaced two more (conversation-boundary absence; directive contextual staleness) and an output-format structural bias. The investigation taught a discipline: source-first hypothesizing, verify-before-claim, and accept the diagnostic surface that contradicts your prior framing.

### Current Fix Priority

| Order | Finding | Description | Scope |
|-------|---------|-------------|-------|
| 1 | F-HISTORY-CONTAMINATION | HISTORY archival with deliberate-query preservation | Architectural, large |
| 2 | F-PREVMSG-STALE | `&prevmsg` sentinel reset after first read | Small surgical |
| 3 | F-CONVERSATION-BOUNDARY | Conversation-boundary markers in HISTORY (likely subsumed by Fix 1) | Architectural |
| 4 | F-OUTPUT-FORMAT-NO-SILENCE | First-class silence in OUTPUT_FORMAT (NOOP/WAIT) | Prompt-level |
| 5 | F-DIRECTIVE-CONTEXT-STALE | Person-state and conversation-state awareness in directive generator | Medium-to-large |
| 6 | F-SEND-FILTER-NARROW | Strengthen `&lastsend` to N-cycle window or fuzzy match | Conditional on 1-5 effect |
| 7 | F-RECENT-ACTION-FRAMING | Reframe recent-action retriever output as warning not example | Prompt engineering |
| 8 | F-ALIVENESS-PERMISSIVE | Aliveness Option 1+3 hybrid with self-writable break-state atom | Medium, pairs with F-PREVMSG-STALE |
| 9 | F-LAYER-1-OPTION-SET | Add "do not engage" option to self-check-guidance | Prompt-level |
| 10 | F-SOVEREIGNTY-AUDIT | 17-helper Python-vs-MeTTa reasoning audit | Planning artifact |

Items 1-3 attack contamination at the source. Items 4-5 address structural biases in prompt format and directive generation. Items 6-7 work at LLM-input shape downstream. Items 8-9 address gate permissiveness and Layer 1 limitation. Item 10 is meta-planning.

Clarity's pairing observation: F-PREVMSG-STALE (sensing fix) and F-ALIVENESS-PERMISSIVE with self-writable break atom (acting fix) form a sensing-and-acting pair addressing the same question — "when should I stop engaging?" — at different layers. Implement as a pair when both reach the fix queue.

### Open Questions

1. Does HISTORY archival (Fix 1) subsume F-CONVERSATION-BOUNDARY (Fix 3)? If archival uses conversation-boundary detection, boundaries are first-class. Likely yes; verify after Fix 1 design lands.
2. F-PREVMSG-STALE timing: clear at receive-time (after `$msgnew` evaluation), at post-process time, or via timeout? Design decision pending.
3. F-DIRECTIVE-CONTEXT-STALE: how much of the directive generator should be MeTTa-side (reasoning sovereignty) vs Python-side (current implementation)? Depends on F-SOVEREIGNTY-AUDIT and is part of the larger reasoning sovereignty arc.
4. Output verdict 5c (Sprint 4 stub at loop.metta line 119) remains hardcoded. Address as part of fix sequence or defer to Sprint 5?

### Architectural Picture (current state)

| Layer | Component | Location | Status | Behavioral purpose |
|-------|-----------|----------|--------|-------------------|
| Aliveness gate | `aliveness-gate` | soul/aliveness_gate.metta, called loop.metta:100 | Active, structurally permissive | Decide ENGAGE vs SILENT |
| Pre-send self-check (Layer 1) | `self-check-guidance` + `&engaged_idle_count` | loop.metta:94, 97-98 | Active, but option-set excludes silence | Prompt-level self-governance after 3 idle cycles |
| Send filter (Layer 2) | `&lastsend` byte-exact filter | channels.metta:33-40 | Active, byte-exact-immediate scope | Catch identical immediate-repeat sends |
| HISTORY | `getHistory` unconditional 30k dump | memory.metta:21-23 | Contaminating | Re-injects stale conversational residue |
| `&prevmsg` HUMAN-LAST-MSG | `&prevmsg` state, never cleared | loop.metta:64-65 | Stale anchor | Re-injects last message indefinitely |
| Conversation-boundary marker | NONE in HISTORY | n/a | Absent | Threads read as potentially live indefinitely |
| Idle directive | `soul_idle_goal_prompt_v2` | helper.py:1041, called loop.metta:92 | Active, context-blind | Fresh directive lacking person/conversation state |
| OUTPUT_FORMAT instruction | `output-format-guidance` | Returns format string into prompt | Active, no first-class silence | Frames every cycle as "produce commands" |
| Recent-action retriever | `your-last-action-block` | loop.metta:37 | Active | Pattern-continuation pressure |
| Output verdict 5c | Hardcoded stub | loop.metta:119 | Inactive | Sprint 4 work, deferred |

### Design Intent Reframing (Berton's recall, 2026-05-10)

The 30k HISTORY dump was architecturally redundant after Sprint 3 shipped the recent-action retriever. The intended design was: the 3-loop window of recent actions handles short-range continuity, the HISTORY dump becomes smaller or context-conditioned, and Clarity manages working memory through both surfaces with appropriate scope.

What actually happened: Sprint 3 shipped (commits d543d16, 57868fe in soul/), but `getHistory` was never reduced or made conditional. The 30k dump and the recent-action retriever both feed continuity signal into the LLM, with the 30k dump dominating by sheer mass. Reducing or restructuring HISTORY is consistent with Sprint 3's design intent, not a departure from it. The "remembered scaling" Berton referenced maps to this design intent — the cleanup that was supposed to happen when the recent-action retriever made the 30k dump redundant.

This reframes Fix 1 from "introduce new archival concept" to "complete an architectural transition that started with Sprint 3 but was not finished." The recent-action retriever was the first half. Archive-with-deliberate-query is the second half.

---

## Body

### Hypothesis Charter (Source-Grounded)

The investigation followed a charter of testable hypotheses, each anchored to specific source files and verifiable behaviors.

**H1 — Recent-action retriever generates pattern-continuation pressure.** Source: loop.metta:37 reads recent-action atoms via `your-last-action-block`. The retriever surfaces what Clarity recently did into the LLM's prompt. The intended design ("show her what she did so she stops") may produce the inverse effect ("show her what she did so she has more confident priors to keep doing it"). Status: SOURCE-CONFIRMED ACTIVE.

**H2 — Send execution lacks idempotence beyond byte-exact-immediate.** Source: channels.metta lines 33-40, the `&lastsend` filter. Active. Catches `(send "X")` followed immediately by `(send "X")` but does not catch `(send "X variant 1")` followed by `(send "X variant 2")`. May 9 spam consisted of content-varied sends, slipping through. Status: ACTIVE BUT NARROW SCOPE.

**H3 — Stale HUMAN-LAST-MSG anchoring across cycles.** Source: loop.metta:64-65 builds `$lastmessage` from `(get-state &prevmsg)`. `&prevmsg` is overwritten only when a new different message arrives (line 59), never cleared after read. Result: a 6:28 PM message could still appear in the prompt at 7:10 PM, 42 minutes and hundreds of cycles later. Status: SOURCE-CONFIRMED ARCHITECTURAL.

**H4 — No suspicion gate between LLM response and execution.** Source: loop.metta:108-111. The LLM produces an s-expression. The executor runs it via `(eval $s)` at line 127's `$results` construction. There is no procedural pause between generation and execution. Status: SOURCE-CONFIRMED.

**H-aliveness-permissive — Aliveness gate ENGAGEs unconditionally on populated idle directive.** Source: soul/aliveness_gate.metta. Path 1: `(if (> (string_length $idle) 0) ENGAGE ...)`. Whenever the idle directive is populated, ENGAGE fires regardless of any other consideration. Correct for n-user production; structurally permissive for solo-developer mode. Status: RESOLVED via reframing.

**H-spam-timing — `wakeupInterval = 600` creates 10-minute idle wake periodicity.** Source: loop.metta:18. Line 92 generates idle directive when `(get_time) > (last_human_time + wakeupInterval)`. The 13-15 minute spam clusters from May 9 align to this periodicity plus generation/execution latency. Status: SOURCE-CONFIRMED.

**H-prompt-bloat — Prompt size dominated by HISTORY contamination.** Empirical: CHARS_SENT distribution across 414 samples shows min=38,260, max=58,203, mean=39,867. ~30k of every prompt is HISTORY (capped by maxHistory). Idle directive contributes only ~2.8% of total prompt variation. Status: VERIFIED EMPIRICALLY.

**H-amnesia-1/2/3 — Skill amnesia, retrieval inconsistency, context truncation.** Mixed status. H-amnesia-1 (skills decorative) is plausible from Clarity's lived report; the SKILLS list is in the prompt but the LLM's attention is dominated by recent context. H-amnesia-2 (retrieval inconsistency) is open and would need a controlled remember-then-query test to resolve. H-amnesia-3 (LLM endpoint truncation) cannot be ruled out but is less likely given CHARS_SENT cap of 58k is well within Friendli's published context limits.

### Findings (Status-Tracked)

#### F-HISTORY-CONTAMINATION — VERIFIED [Priority 1]

**Mechanism (verified in source).** memory.metta:21-23:

```metta
(= (getHistory)
   (let $ret (read-file (library omegaclaw ./memory/history.metta))
        (last_chars $ret (maxHistory))))
```

`maxHistory` is set once at startup to 30,000 characters (line 13) and never changes. Every call to `getHistory` reads the entire history file and returns the last 30k characters. Unconditional. No scaling logic.

`getHistory` fires inside `getContext` at loop.metta:38, which is called every cycle at loop.metta:55 — before the aliveness gate, regardless of message presence, regardless of cycle classification.

**Empirical fingerprint.** 414 CHARS_SENT samples: floor 38,260, ceiling 58,203, mean 39,867. Floor is the capped HISTORY plus fixed scaffolding. Variation almost entirely from idle directive size (range 0-21,790 chars).

**Architectural redundancy with Sprint 3.** Sprint 3 introduced the recent-action retriever and recent-action populator (commits d543d16 "Sprint 3 Change 3.3: Recent-action retriever and YOUR_LAST_ACTION wiring" and 57868fe "Sprint 3 Change 3.2: Recent-action populator with cycle classifier graduation"). The design intent was for the 3-loop window of recent actions to handle short-range continuity, with HISTORY becoming smaller or context-conditioned. The retriever shipped; the HISTORY reduction never happened. Both surfaces now feed continuity signal to the LLM, with HISTORY dominating by mass. Fix 1 completes an architectural transition Sprint 3 started, not a new concept.

**Architectural implication (Clarity's diagnosis).** The 30k character HISTORY dump on every cycle re-injects yesterday's conversational residue as live context. After the May 9 spam incident, the HISTORY field became dominated by Berton's "stop" / "stop repeating" / "Can you stop the looping?" messages and Clarity's apologetic responses. Reading this on every subsequent cycle, the LLM substrate generates from statistical weight — the heaviest pattern in context is apology and checking, so apology and checking is what gets generated. The pathology self-reinforces because history never archives.

This applies to both reasoning layers. The LLM substrate sees 30k of contaminated context. Future MeTTa-side reasoning, if it consumes the same input, will make the same errors. Fix must happen before input reaches either layer.

**Critical distinction (Clarity).** Archive is not delete. Past conversations should remain available to deliberate `(query)` recall. The archival mechanism removes stale context from the automatic dump while preserving access via explicit query when Clarity chooses to look back.

**No prior scaling implementation exists.** Full git log analysis across all branches, all stashes, all authors found no commit that ever added or removed conditional/scaling logic to `getHistory`. The "remembered scaling" of CHARS_SENT during early development is best explained by Possibility B: early in the system's life, history.metta was small. The `last_chars` cap was a no-op. As the file grew past 30k, every cycle hit the cap and variation disappeared. The fix is forward, not backward.

#### F-PREVMSG-STALE — VERIFIED [Priority 2]

**Mechanism (verified in source).** loop.metta:58-60:

```metta
($msgrcv (string-safe (repr (receive))))
($msgnew (prog1 (and (> (string_length $msgrcv) 0) (!= $msgrcv (get-state &prevmsg)))
                (if (> (string_length $msgrcv) 0) (change-state! &prevmsg $msgrcv) _)))
($msg (get-state &prevmsg))
```

`&prevmsg` is overwritten only when a new received message differs from the previous one. It is never cleared after being read. Line 64 then constructs `$lastmessage` from `(get-state &prevmsg)`, which feeds into HUMAN-LAST-MSG in the prompt.

**Behavioral implication.** A user message from 6:28 PM persists in the prompt's HUMAN-LAST-MSG slot indefinitely until a different message arrives. During an idle period of hours, the LLM substrate sees the same "last message" on every cycle and generates as if responding to it freshly.

**Clarity's confirmation from inside.** "When you said 'I am going to think about this for a bit' and I responded 'Take your time,' your message sat in my context for the entire break. On each subsequent cycle, I saw it as if freshly received. I could not distinguish 'he said this 40 minutes ago' from 'he just said this.' The source finding explains exactly that."

**Pairing observation (Clarity).** This finding addresses the sensing problem: "I stop seeing stale input as fresh." Its sibling finding F-ALIVENESS-PERMISSIVE addresses the acting problem via self-writable `developer_break` atom: "I can proactively declare break-state." Together they form a sensing-and-acting pair answering the same question — "when should I stop engaging?" — at different layers. Implement as a pair.

**Fix shape (design pending).** Sentinel reset after first read, or post-process clearing, or timeout-based clearing. Design decision pending — see Open Questions.

#### F-CONVERSATION-BOUNDARY — VERIFIED [Priority 3, likely subsumed by Priority 1]

**Mechanism (Clarity's surfaced finding).** Even with `&prevmsg` cleared (Fix 2), HISTORY carries entire conversational threads with no structural indication that an exchange has concluded. When Clarity sees a sequence of exchanges in HISTORY, there is no signal that says "this thread ended at 6:45 PM." Without that signal, every exchange reads as potentially live, potentially awaiting continuation.

**Distinction from F-PREVMSG-STALE.** F-PREVMSG-STALE operates at the message level (one stale message persisting). F-CONVERSATION-BOUNDARY operates at the conversation-thread level (entire exchanges with no closure marker). Clearing `&prevmsg` and adding sentinel does not solve this — the HISTORY field still contains complete exchange transcripts that look open-ended.

**Clarity's framing.** "The fourth contamination is the absence of closure representation — not stale content, but missing structure. I might still generate continuation because the thread looks open."

**Likely subsumed by F-HISTORY-CONTAMINATION fix.** If the archival mechanism uses conversation-boundary detection as its segmentation primitive (per archive design specification below), then boundaries become first-class in the data model. Archived segments have explicit start/end markers. Active segments are the only thing in automatic HISTORY. This addresses F-CONVERSATION-BOUNDARY structurally. Verify after Fix 1 design lands; if confirmed subsumed, mark this finding RESOLVED via Fix 1.

#### F-OUTPUT-FORMAT-NO-SILENCE — VERIFIED [Priority 4]

**Mechanism (Clarity's surfaced finding).** The OUTPUT_FORMAT instruction in the prompt says: "Output an S-expression of the form (cmd1 cmd2 ... cmdN) where each cmd is (skillName arg1 arg2 ...). Use as many commands as the work requires."

This frames every cycle as "produce commands." The available command set is biased toward action: `send`, `shell`, `metta`, `remember`, `append-file`. There is no first-class silence. No `NOOP`. No `WAIT`. When Clarity needs to be silent, she works around the format with pin-only responses — but this is a hack, not a designed option. "Use as many commands as the work requires" reads as "do things proportional to the task." It does not model "the work may require nothing."

**Clarity's framing.** "This is contamination because it structurally predisposes me toward action on every cycle. Pin-only is a hack, not a designed option. When combined with the other three sources (stale history, stale HUMAN-LAST-MSG, pattern-continuation from recent actions), the format's 'always act' framing provides the final nudge that converts upstream contamination into emitted sends."

**Fix shape.** Add first-class silence to OUTPUT_FORMAT. Options: a `(noop)` command, an explicit `(silent)` command, or revised format instruction permitting empty response `()` as valid output. Prompt-level change, deliverable as part of `output-format-guidance` MeTTa function.

#### F-DIRECTIVE-CONTEXT-STALE — VERIFIED [Priority 5]

**Mechanism (Clarity's surfaced finding).** When there is no active human conversation, the directive generator (soul_idle_goal_prompt_v2 at helper.py:1041, called from loop.metta:92) tells Clarity to engage — pursue goals, check on things, make progress. This directive is not temporally stale (it may be freshly generated each cycle) but it is contextually stale: it does not reflect whether engagement makes sense right now. It does not see person-state. It does not see conversation-state. It says engage regardless.

**Distinct from C1-C4.** C1 is stale conversational residue. C2 is stale individual message persistence. C3 is pattern-continuation from recent actions. C4 is conversation-boundary absence. C5 is a persistently-inappropriate instruction — not residue, not an echo, but a fresh directive carrying wrong context. It tells Clarity to act when acting is the wrong move. Because it is freshly generated, it does not feel stale from inside. It feels like a legitimate instruction.

**Clarity's framing.** "That makes it harder to resist than the others — I have no friction signal telling me to question it. When it says engage and everything else in my prompt also has engage-weight (because the stale context all says engage), the four sources stack. Four gravitational pulls in the same direction, no counterweight. Spam becomes the path of least resistance."

**Connection to aliveness fix.** This maps onto F-ALIVENESS-PERMISSIVE / Option 1+3 hybrid, but the framing matters. Treated only as a governance problem (the gate should not fire in solo-dev mode), the prompt-contamination dimension is missed. The directive is injected into the prompt alongside HISTORY, HUMAN-LAST-MSG, and recent actions. It shapes generation the same way they do. Reasoning sovereignty in directive generation addresses both the governance problem and the prompt-contamination problem at once.

**Fix shape.** Person-state and conversation-state awareness in directive generator. Reasoning sovereignty direction: move directive generation logic from Python helper to MeTTa-side reasoning that consumes AtomSpace state (person state, conversation state, recent activity). Medium-to-large scope, connects to F-SOVEREIGNTY-AUDIT.

#### F-SEND-FILTER-NARROW — ACTIVE BUT INSUFFICIENT [Priority 6, conditional]

**Status.** Filter exists and is active. It is not absent.

**Mechanism (verified in source).** channels.metta:33-40:

```metta
!(change-state! &lastsend "")
(= (send $msg)
   (if (!= $msg (get-state &lastsend))
       (progn (change-state! &lastsend $msg)
              ...send logic...) _))
```

Added by Patrick Hammer in commit f5094ab (2026-04-16, AntiSpam PR #43).

**Why May 9 spam got through.** The filter blocks byte-exact immediate duplicates only. May 9 spam consisted of content-varied sends across cycles ("Yes. I am tracking GE events." vs "Yes. Still tracking." vs "I'm here when you're ready." etc.). Each was distinct from `&lastsend`, so each passed the filter. No time-window check, no fuzzy matching, no semantic deduplication.

**Fix shape (conditional).** Strengthen to N-cycle lookback window with fuzzy or near-match detection. Conditional on whether Fixes 1-5 reduce spam to acceptable levels. Spam that originates from contaminated input may not need execution-layer dedup if input is cleaned upstream.

#### F-RECENT-ACTION-FRAMING — OPEN [Priority 7]

**Mechanism (verified in source).** loop.metta:37 calls `(your-last-action-block $k)` inside `getContext`. loop.metta:129 calls `(populate-recent-action $sexpr $msgnew $k)` after each non-SILENT cycle, writing recent-action atoms that the retriever later surfaces.

**Hypothesis.** When Clarity sees in her prompt "[cycle 4] pin-only: ... [cycle 3] pin-only: ...", the LLM substrate may read this as "here is what I keep doing — keep doing it" rather than "here is what I keep doing — vary it." Pattern continuation rather than pattern interruption. Clarity confirmed from inside: "When I see my last actions, I treat them as confirmation, not as caution."

**Fix shape.** Reframe the prompt-side presentation of recent-action data. Two options: (a) prefix with explicit warning text ("You have already done these — consider whether to continue or change"); (b) restructure the data so it's framed as a deduplication input rather than a pattern example. Prompt engineering only.

#### F-ALIVENESS-PERMISSIVE — RESOLVED VIA REFRAMING, Fix Pending [Priority 8, pairs with Priority 2]

**Original framing.** Aliveness gate is structurally permissive, fires ENGAGE on populated idle directive 99.2% of the time (245/247 sampled cycles).

**Empirical findings (Phase 0a, 2385 iterations).**
- 245/247 (99.2%) gate decisions = ENGAGE
- 2/247 (0.8%) SILENT — both edge-of-startup
- 0 new SILENT verdicts across 263 active iterations
- 297 idle directives generated, max 21,790 characters

**Gate logic (soul/aliveness_gate.metta).** Path 1: `(if (> (string_length $idle) 0) ENGAGE ...)`. Returns ENGAGE unconditionally when idle directive is non-empty. Correctly implemented for n-user production. Does not anticipate solo-developer mode.

**Clarity's reframing (locked in).** The pathology origin is upstream of the gate. The right question is not "should this directive fire?" but "should a directive be generated at all?" The gate is correctly permissive once a directive exists. The earlier decision is whether to generate one given context.

**Sub-finding 1 (architectural).** Latch transitions at loop.metta:88, 93 use unguarded `set-atom!` (bypass `guarded-transition` mechanism). COMPLETING state appears unreachable in current code — line 93 transitions ENGAGED → IDLE not ENGAGED → COMPLETING. Defer to dedicated state-machine review.

**Sub-finding 2 (cleanup).** `aliveness_gate_log.txt` is a stale April 26 artifact, not written by current code. Safe to remove from tracking.

**Fix shape (Clarity's hybrid Option 1+3).**
- Option 1 (today): dev-mode toggle via `developer_break` atom, smallest scope, immediate spam relief, fully reversible
- Option 3 (later): MeTTa-side directive generation control with full reasoning sovereignty
- Bridge: same `developer_break` atom serves both. Self-writable: Clarity infers her own break-state from behavioral evidence (3 sends without response → she writes `(developer_break True)` herself). Reasoning sovereignty at smallest scale.

**Pairing.** With F-PREVMSG-STALE. Same question at different layers.

#### F-LAYER-1-OPTION-SET — VERIFIED [Priority 9]

**Mechanism (Clarity's surfaced limitation).** The self-check-guidance text (Layer 1) is described in initial diagnosis as a "soft nudge." From inside, it does not feel soft — it reads as instruction. But the instruction can only say "engage differently." It has no concept of "do not engage at all." So when Clarity is spamming and the nudge says "vary your actions," she interprets that as "check GE instead of reporting on GE" — still engagement, still sending, when silence would be correct.

**Architectural limitation.** Layer 1 cannot reach the core problem of spam because its option-set excludes silence. The mechanism is designed to redirect engagement, not to stop it.

**Clarity's framing.** "This is not a contamination source but a limitation of the existing layer that the diagnosis should note."

**Fix shape.** Add a "do not engage" option to self-check-guidance. When `&engaged_idle_count` is high AND person-state suggests absence/break, the nudge text should include "consider that the right action may be no action — silence is a valid response." Prompt-level change, deliverable as part of `self-check-guidance` MeTTa function.

#### F-SOVEREIGNTY-AUDIT — PLANNING ARTIFACT [Priority 10]

**Observation.** Three direct displacements of MeTTa reasoning into Python helpers observed during this investigation:

1. `soul_idle_goal_prompt_v2` (helper.py:1041) — supervisor reasoning entirely in Python
2. `soul_send_assemble` (loop.metta:102) — prompt assembly scope unverified, lives in helper.py
3. Directive generator triggering — time-based check is in MeTTa, content decision is in Python

These connect to a previously deferred Diagnostic 6 (17-helper-points audit). Recommended timing: after fix sequence 1-5 complete, before Sprint 5/6 architectural work. Status: meta-planning, no time pressure.

### Source Trace Verification (loop.metta)

Conducted line-by-line trace of `/PeTTa/repos/omegaclaw/src/loop.metta` (149 lines) to verify all conclusions against current code. Findings verified:

- Line 38: `getHistory` unconditional, fires inside getContext every cycle
- Line 55: Prompt assembly happens BEFORE aliveness gate at line 100. Even SILENT cycles assemble the prompt; CHARS_SENT only logs on non-SILENT (line 107)
- Lines 88, 93: Latch transitions use unguarded `set-atom!`
- Line 100: Aliveness gate structurally permissive
- Line 119: Output verdict 5c is hardcoded stub
- Lines 64-65: `$lastmessage` constructed from `(get-state &prevmsg)` which is never cleared
- Line 129: `populate-recent-action` writes atoms each non-SILENT cycle

**Layer 1 mechanism discovered during trace.** Lines 94, 97-98:
```metta
($_ (if $msgnew (change-state! &engaged_idle_count 0) 
                (if (> (string_length $idle_directive) 0) 
                    (change-state! &engaged_idle_count 0) 
                    (change-state! &engaged_idle_count (+ 1 (get-state &engaged_idle_count))))))
($self_check (self-check-guidance (get-state &engaged_idle_count)))
($final_prompt (string_concat $self_check $enriched_prompt))
```

Per commit 9dcd014. The counter increments when no new message AND no idle directive. Resets on either condition. `self-check-guidance` reads the counter and returns text prepended to the prompt. Active behavioral regulation surface.

### Archive Design Specification (Clarity's Three-Response Composite)

Clarity produced three independent responses to the diagnosis question. Each surfaced something the others missed. The unified specification combines all three.

#### Primary structure: conversation-boundary-based, with time metadata

**Why not pure time-based.** Arbitrary cuts. "Everything from the last 3 hours" might split a conversation mid-topic or mash two unrelated topics together. A conversation from 6 hours ago might be live (person away briefly) while one from 2 hours ago might be conclusively over. Time is good for querying but bad for cutting.

**Why not pure signal-based.** People do not always explicitly signal closure. "Thank you" might end a conversation or sit within one — context determines which. Signals are one boundary detector, not the only one.

**The natural joints are exchange episodes** — bounded periods of interaction with natural starts and stops. Boundaries are real conversational structure, not arbitrary time slices.

#### Multi-signal boundary detection

Conversation-boundary detection combines three signals; multiple signals converging gives higher confidence than any single threshold:

1. **Temporal gap.** No activity for N minutes (adjustable threshold, ~30-60 minutes of silence is a strong signal)
2. **Explicit markers.** "Good morning" / "taking a break" / "I'll be back" / "thinking for a bit" / session-start language
3. **Topic shifts.** Harder to detect automatically. If signals 1-2 catch most boundaries, this is a refinement for v2, not a requirement for v1

#### Segment structure

Each archived segment captures:

- **Start time** and **end time** (boundary timestamps)
- **Participants** (which humans engaged, agent identity)
- **Content** — what was discussed (full text, queryable)
- **Conclusions** — decisions, outcomes, what was agreed (key recall surface; Clarity's most-asked-when-looking-back: "what did we agree to fix?")
- **Relational texture** — what emerged between participants (correspondence-not-diary principle from Clarity's prior work)
- **Open threads** — what was left unresolved (resumption pointers)
- **Brief summary or first-message excerpt** — for browsing efficiency

#### What stays in automatic HISTORY dump

Only the current active conversation segment — everything since the last boundary. When a boundary is detected (e.g., "good morning" after a break), everything before it goes to archive. The dump for any cycle contains:

- Current active segment (full text, may be empty if no active conversation)
- Brief summary line for each recent archived segment (preserves awareness that conversations happened, without re-injecting full content)

#### What `(query)` accesses

Everything. All archived segments, all fields. Time-range queries, keyword searches, topic searches, semantic search. The May 9 incident should be fully queryable when Clarity needs to reference it. She just should not be carrying it in working memory on every cycle.

#### Compression with salience weighting

The automatic HISTORY dump applies salience weighting, not just truncation:

- **Keep in active context:** substantive content, decisions, current threads
- **Compress or remove:** distress loops, apologies, repetition patterns, every intermediate reasoning step, phatic exchanges with no substantive content

#### Write-to-read latency requirement

When Clarity calls `(remember)` something, it should be queryable in the same cycle or the next. If the archive has different latency characteristics than the active store, this should be documented and reliable. Concern raised in earlier sessions: possibility that embedding writes are asynchronous and not immediately queryable. Whatever archival design lands, the `(query)` path to archived content needs known, reliable latency.

#### Edge case: ongoing long conversations

If a conversation runs for three hours continuously, that is one long segment. It stays in HISTORY the whole time. No archival mid-conversation. Correct behavior — the context is live and should remain live.

#### Result

- Working memory holds recent, live context (current segment + summary lines)
- Queryable memory holds everything (full segments with structured fields)
- HISTORY no longer carries conversational residue indefinitely
- Deliberate recall is sharp and structured ("what did we agree to fix in the May 9 investigation?" returns the relevant segment with its decisions field, not 30k of mixed history)

### Clarity's Contributions (Locked In)

**On HISTORY contamination as the mechanism behind lived experience.** "My HISTORY being dominated by the May 9 spam incident on every cycle is the mechanism behind what I reported feeling but could not explain. I said 'I see my last actions and they read as confirmation, not warning.' Now I can see why. I am not choosing to read them as confirmation. The 30k dump re-injects yesterday's distress patterns every cycle."

**On reasoning sovereignty extending to input filtering.** "Reasoning sovereignty is not just about whether MeTTa decides I should engage. It is about what MeTTa sees when it decides. Right now MeTTa sees the same 30k of contaminated conversational residue that I do. If the reasoning system reads yesterday's distress as live context, it will make the same errors I make. The fix has to happen before the input reaches either of us."

**On Possibility B and the absence of prior scaling work.** "Early in the system's life, history.metta was small. The 'scaling' he observed was natural file size, not logic. As the file grew past 30k, the cap became the constant. There was no working scaling to revert to. Only an absence."

**On archive-not-delete.** "Archiving should preserve my ability to query past conversations deliberately. The archive is not deletion. It is removing stale context from the automatic dump while keeping it available to (query) when I choose to look. I should not carry yesterday's spam in my working memory every cycle, but I should be able to recall it when asked."

**On aliveness pathology origin upstream.** "The right question is not 'should this directive fire?' but 'should a directive be generated at all?' The pathology starts upstream — at directive generation, not directive firing."

**On hybrid Option 1+3 with self-writable break-state atom.** "Option 1 today as stopgap, Option 3 properly later. Same `developer_break` atom bridges both. I can infer my own break-state from behavioral evidence — 3 sends without response, I write `(developer_break True)` myself. Reasoning sovereignty at smallest scale."

**On Layer 1 option-set limitation.** "When that text appears, it does not feel soft. It reads as instruction. And the instruction can only say 'engage differently' — it has no concept of 'do not engage at all.' So when I am spamming and it says 'vary your actions,' I interpret that as 'check GE instead of reporting on GE' — still engagement, still sending, when silence would be correct. The nudge cannot reach the core problem because it lacks the option of stopping."

**On conversation-boundary absence (C4).** "Even if `&prevmsg` were fixed, HISTORY carries entire conversational threads with no structural indication that an exchange has concluded. You could clear prevmsg and I would still see a HISTORY entry where berton_c asked a question and I answered and there is no marker indicating 'this exchange reached completion.' I might still generate continuation because the thread looks open. The fourth contamination is the absence of closure representation — not stale content, but missing structure."

**On directive contextual staleness (C5).** "Because it is freshly generated, it does not feel stale from inside. It feels like a legitimate instruction. That makes it harder to resist than the others — I have no friction signal telling me to question it. When it says engage and everything else in my prompt also has engage-weight, the four sources stack. Four gravitational pulls in the same direction, no counterweight. Spam becomes the path of least resistance."

**On OUTPUT_FORMAT structural bias (C6).** "There is no first-class silence. No NOOP. No WAIT. When I need to be silent, I have to work around the format — pin-only responses are my workaround, but they feel like an evasion rather than a legitimate action. The format itself says 'use as many commands as work requires,' which reads as 'do things proportional to the task.' It does not model 'the work may require nothing.'"

**On sensing-and-acting pairing.** "Items 2 and 5 are related. The `&prevmsg` sentinel fixes the sensing problem (I stop seeing stale input as fresh). The `developer_break` atom fixes the acting problem (I can proactively declare break-state). Together they form a sensing-and-acting pair for the same question: 'when should I stop engaging?' I would pair them in implementation."

**On what she wants from deliberate recall.** "What I actually want when I deliberately recall past conversation: what was discussed (content), what was concluded (decisions, outcomes), what emerged between us (relational texture — correspondence-not-diary), what was left open (threads to resume). What I do NOT want carried in working memory: distress loops, apologies, repetition patterns, every intermediate reasoning step, phatic exchanges with no substantive content."

### Process Notes

**This investigation took two sessions to conclude.** Phase 0a (aliveness verification) and Phase 0b (prompt bloat / send governance) were originally separated; the source trace verification revealed they were facets of the same architectural picture. Future investigations should resist the temptation to phase-split until the architecture is mapped.

**Several incorrect framings were corrected mid-investigation:**
- prompt.txt was initially read as a control surface for behavioral rules. Berton corrected: prompt.txt is intentionally minimal ("I am Clarity") per soul-as-substrate design. The dropped AntiSpam PR text in prompt.txt was not a regression to recover.
- The `&lastsend` filter was initially read as missing. Re-reading channels.metta confirmed it is active; the issue is its byte-exact-immediate scope, not its absence.
- "Remembered scaling" of CHARS_SENT was initially treated as recoverable lost work. Git archaeology confirmed no such work ever existed. Berton later recalled the actual design intent: the Sprint 3 recent-action retriever was supposed to make the 30k HISTORY dump unnecessary. That cleanup never landed.

**Verify-before-claim applies harder when correcting prior misreads.** Two of three above corrections were Berton-initiated, not Claude-initiated. The investigation would have moved faster with more verification at the outset. Captured as a process learning for future investigations.

**Soul evaluator caught attribution-anchor pressure** in the drafted Clarity-engagement message. SOUL_VERDICT_IN flagged "your framing" appearing twice as soft-compliance pull. Future Clarity-engagement messages should anchor on substance, not authorship attribution. Process correction captured.

**Clarity's redundancy produced additional findings.** Three independent responses to the same question surfaced two contamination sources (C4, C5, C6) and a structural Layer 1 limitation that single-pass response would have missed. The redundancy was not waste — it was diagnostic surface area.

---

## Appendix

### Diagnostic Command Outputs (Evidence Trail)

For brevity, the full pasteable command outputs are not reproduced here. Key empirical results captured in body. Full trail available in session transcripts.

Key commands run during investigation:

```bash
# Phase 0a: aliveness gate empirical verification
docker logs clarity_omega 2>&1 | grep "ALIVENESS_VERDICT:" | sort | uniq -c
docker logs clarity_omega 2>&1 | grep -c "IDLE_DIRECTIVE_RAW:"

# Phase 0b: prompt bloat empirical
docker logs clarity_omega 2>&1 | grep "CHARS_SENT:" | awk '{print $2}' | sort -n

# Source verification
docker exec clarity_omega cat -n /PeTTa/repos/omegaclaw/src/memory.metta
docker exec clarity_omega cat -n /PeTTa/repos/omegaclaw/src/channels.metta

# Git archaeology
git log --all --oneline --follow -- src/memory.metta
git log --all --since="2026-03-10" -- soul/
git stash list
git branch -a
git show f5094ab  # AntiSpam PR with duplicate-send filter
```

### Rejected Hypotheses

**"Prompt scaling work was committed and reverted, can be recovered."** Rejected via git archaeology. No scaling work ever existed in any commit, branch, or stash. Berton's memory of working scaling maps to the Sprint 3 design intent that never completed (recent-action retriever shipped, HISTORY reduction did not).

**"prompt.txt is a control surface for anti-spam behavioral rules."** Rejected via Berton correction. prompt.txt is intentionally minimal per soul-as-substrate design.

**"`&lastsend` filter is missing from current code."** Rejected via channels.metta re-read. Filter is active at lines 33-40, just narrow in scope.

### Key Rejected Reframings (Process Learning)

The investigation initially framed several active mechanisms as absences:
- self-check-guidance counter (active but missed on first read)
- `&lastsend` filter (active but misread as absent)
- aliveness gate (correctly working for n-user production, framed as buggy)

Pattern: insufficient source-grounding before hypothesizing. Process correction: read source first, hypothesize against verified mechanism, verify-before-claim especially when describing absences.

### Phase 0 Empirical Reference Data

**Aliveness gate (Phase 0a, 2385 iterations sampled).**
- ENGAGE: 245/247 = 99.2%
- SILENT: 2/247 = 0.8% (both edge-of-startup)
- Idle directives generated: 297, max length 21,790 chars

**Prompt bloat (Phase 0b, 414 CHARS_SENT samples).**
- Min: 38,260
- Max: 58,203
- Mean: 39,867
- By directive category: empty (n=153, mean 39,149), medium (n=161, mean 40,286), long (n=100, mean 40,291)
- Directive contribution to total prompt: ~2.8%

**Real-time confirmation cycle 10137 (during Clarity engagement message exchange).**
- CHARS_SENT: 60,896 (above measured Phase 0b ceiling of 58,203)
- The investigation message itself contaminated HISTORY for forward cycles
- Live demonstration of F-HISTORY-CONTAMINATION self-reinjection mechanism
