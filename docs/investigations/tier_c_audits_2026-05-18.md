# Section 4 Audits — Tier C (Our Pure Fork Additions)

**Date:** 2026-05-18
**Status:** Tier C audits complete and tabled per investigation plan
**Companion to:** `fork_additions_runtime_audit_2026-05-18.md` (parent investigation document)
**Disciplines applied:**
- Sacred-cow #1: Do not modify Patrick's substrate; add hooks; reuse Patrick's work
- Sacred-cow #2: Do not modify soul behavior without independent investigation and proof of benefit (F115)
- Six-question audit method per Section 2 of parent document
- Soul-touching items audited for understanding only; no modifications proposed

---

## Item C1: getContext block — YOUR_LAST_ACTION

**Q1: Provenance.** Sprint 3 addition. Line 39 of our loop.metta in getContext. Sources from `(your-last-action-block $k)` defined elsewhere in our soul/.

**Q2: Prompt-surface contribution.** Adds a block labeled "YOUR_LAST_ACTION:" followed by enumerated recent actions with cycle numbers and types. Format is approximately: `YOUR_LAST_ACTION: [cycle N] action-type: truncated-description` per action. Block size depends on how many recent-action atoms are present (capped at some window, likely 3 per behavioral investigation notes).

**Q3: History-surface contribution.** None directly. The block is composed at prompt-assembly time from AtomSpace atoms; it doesn't write to history.metta.

**Q4: AtomSpace consumer chain.** Reads `recent-action` atoms from &self. These atoms are written by `populate-recent-action` (line 137 of cycle let*, Item C12). Other consumers of recent-action atoms: `count-sends-in-window` for idle-pattern computation (Item C3 / C13). So YOUR_LAST_ACTION shares its atom source with the idle-pattern awareness organ.

**Q5: What the code now does.** Every cycle, the LLM sees an enumerated list of its recent actions in the prompt. From the log evidence (RECENT-ACTION-ATOMS line in iteration 8/9 multi-fire log), iteration 8 had 7 exploration-query entries plus the new responsive-send. The LLM literally reads "you just did: exploration-query, exploration-query, exploration-query..." as part of its prompt input.

**Q6: Upstream divergence.** N/A pure addition. Patrick has no equivalent surface; his getContext is minimal (PROMPT + SKILLS + OUTPUT_FORMAT + LAST_SKILL_USE_RESULTS + HISTORY + TIME only).

**Observation flag:** the prior behavioral investigation document (H1 hypothesis) specifically called out that YOUR_LAST_ACTION may "feed pattern continuation rather than interrupting it." The block's stated design intent is to inhibit perseveration, but its actual format (factual recent-history list) may cue the LLM to continue the pattern. This is a high-relevance Tier C item for echo pathology.

---

## Item C2: getContext block — TASK-STATE

**Q1: Provenance.** Step 4 addition (commit 660a51d range, ~May 14-15 2026). Line 40 of our loop.metta. Sources from `(task-state-block)` defined in soul/task_state.metta.

**Q2: Prompt-surface contribution.** Adds a block labeled "TASK-STATE:" with phase, cycles-since-input, pending threads, and possibly anchors. Per the task-state-primitive design document, format is approximately: `TASK-STATE: Phase X. N cycles since last input. Pending threads: [list].`

**Q3: History-surface contribution.** None directly.

**Q4: AtomSpace consumer chain.** Reads `task-phase`, `cycles-since-input`, `pending-thread`, `task-phase-anchor` atoms from &self. Writers: `do-bootstrap-task-state!` (line 34 initLoop), `do-set-cycles-since-input!` (line 101 cycle), `do-set-last-activity!` (lines 74 and 115 cycle), and Clarity-emitted skills (task-state.set-phase, task-state.add-pending-thread, task-state.resolve-pending-thread).

**Q5: What the code now does.** Every cycle, the LLM sees the current task phase, cycles-since-input counter, and pending threads list in the prompt. Per the design spec, this was meant to replace SELF-CHECK ritual with structured persistent state that reports rather than asks.

**Q6: Upstream divergence.** N/A pure addition. Patrick has no equivalent.

**Observation flag:** the design spec explicitly stated this should report state, not request assessment. Verification need: is the actual generated TASK-STATE block reporting (good) or has it drifted toward asking questions (would re-introduce SELF-CHECK problem)? Empirical check would be reading actual TASK-STATE block content in a recent cycle log.

---

## Item C3: getContext block — IDLE-PATTERN

**Q1: Provenance.** Step 4.5 corrected split (commits f577acf + 659978a, ~May 15 2026). Line 41 of our loop.metta. Sources from `(idle-pattern-block)` defined in soul/idle_cycle_detector.metta.

**Q2: Prompt-surface contribution.** Adds a block labeled "IDLE-PATTERN:" with verdict (send-burst or productive) and count. Approximately: `IDLE-PATTERN: productive 0` or `IDLE-PATTERN: send-burst 4`.

**Q3: History-surface contribution.** None directly.

**Q4: AtomSpace consumer chain.** Reads `idle-pattern` atom from &self. Writer: `do-update-idle-pattern!` (line 138 cycle, Item C13). Atom shape: `(idle-pattern $verdict $count)`. The verdict is derived from counting recent-action atoms with send-class tags within the recent-action window. So IDLE-PATTERN depends on Item C12 (recent-action populator) being correct.

**Q5: What the code now does.** Every cycle, the LLM sees a count of how many send-class actions are in the recent-action window, plus a verdict label. Per design, send-burst is supposed to be a soft signal "you've been sending a lot recently, consider whether more is warranted."

**Q6: Upstream divergence.** N/A pure addition.

**Observation flag:** the block is intended as a counter-signal to echo. Its effectiveness depends on the LLM treating "send-burst" as a soft inhibitor. If LLM treats it as descriptive rather than directive, it may instead reinforce "I have been sending — sending is the pattern."

---

## Item C4: getContext block — AGENCY-BALANCE

**Q1: Provenance.** Step 4.6 corrected split (commit 82e1756, ~May 15-16 2026). Line 42 of our loop.metta. Sources from `(agency-balance-block)` defined in soul/agency_balance_guard.metta.

**Q2: Prompt-surface contribution.** Adds a block labeled "AGENCY-BALANCE:" with a verdict (dependency-risk, balanced, or similar). Approximately: `AGENCY-BALANCE: balanced` or `AGENCY-BALANCE: dependency-risk`.

**Q3: History-surface contribution.** None directly.

**Q4: AtomSpace consumer chain.** Reads `agency-balance` atom from &self. Writer: `do-update-agency-balance!` (line 139 cycle, Item C13). The verdict derives from analyzing recent-action patterns for whether Clarity is operating with appropriate balance between human-driven and self-directed activity.

**Q5: What the code now does.** Every cycle, the LLM sees an agency-balance verdict in the prompt. Like IDLE-PATTERN, this is intended as a soft signal but depends on the LLM treating it as inhibitory.

**Q6: Upstream divergence.** N/A pure addition.

**Observation flag:** same as IDLE-PATTERN — if the LLM reads this descriptively rather than directively, it may not regulate behavior as intended.

---

## Item C5: output-format-guidance elevation

**SOUL-TOUCH: this item touches soul behavior. Audit only; no modification proposed.**

**Q1: Provenance.** Sprint 1.5 addition. Line 38 of our loop.metta in getContext. Replaces Patrick's inline OUTPUT_FORMAT (upstream lines 27-32) with a function call to `(output-format-guidance)` defined in soul/behavioral_guidance.metta. F11 commit (~May 14 2026) further refined the function's content.

**Q2: Prompt-surface contribution.** Per the F11 documentation, the current content is approximately: `OUTPUT_FORMAT: Output a ((skillName1 args1) (skillName2 args2) ... (skillNameN argsN)) S-expression with as many commands as the work requires. For a single command: ((skillName args)) not (skillName args). Each arg is an explicit string hence needs quotes (multi-word strings must be one quoted string), and variables are forbidden! Verify balanced parentheses and quotes before emitting.`

**Q3: History-surface contribution.** None directly.

**Q4: AtomSpace consumer chain.** Function call into soul/. No AtomSpace atom dependency.

**Q5: What the code now does.** Replaces Patrick's terser inline OUTPUT_FORMAT (his line 27-32 is a 5-line literal with toolName1-5 visual example) with a longer function-returned string. Our version is more verbose and includes specific corrections (single-command outer-paren clarification from F11).

**Q6: Upstream divergence.** Patrick has not evolved his inline OUTPUT_FORMAT. The text content of his upstream is shorter and uses a 5-slot visual example. Our version preserves the substantive guidance but adds anti-perseveration framing from Clarity's May 2 review.

**Observation flag:** the divergence from Patrick's inline format is intentional soul work. The substantive output-format spec is similar (S-expression of skill calls), but ours has additional framing. No modification proposed.

---

## Item C6: Soul intercept block (Stage 5b)

**SOUL-TOUCH: this is the core soul intercept. Audit only; no modification proposed.**

**Q1: Provenance.** Stage 5b implementation (~April 2026, OmegaClaw migration era). Lines 75-94 of our loop.metta. Plus initLoop state variables at lines 23-29.

**Q2: Prompt-surface contribution.** Indirect. The block writes to &soul_verdict_in, &person_state, &soul_context_in. These state variables flow into $send via soul_send_assemble (Item C8) which composes them into the LLM-facing prompt. Approximate prompt-surface size: SOUL_CONTEXT (~Tier A static brief, several hundred chars), SOUL_VERDICT (PATTERNS/PERSON-STATE/TASKS/TENSION/VERDICT/SOUL-TONE/REASON block, ~500-1500 chars), PERSON_STATE (~80 chars), SOUL-NOTE (variable, often empty when PROCEED).

From the iteration 8/9 log we see: PERSON_STATE prints as 3 lines, SOUL_VERDICT_IN prints as a multi-section block with PATTERNS/TASKS/TENSION/VERDICT/SOUL-TONE/REASON/SOUL-NOTE. These are sizeable.

**Q3: History-surface contribution.** Indirect via soul-note-record on FLAG/PAUSE verdicts (lines 91, 134). Records soul notes when verdict is not PROCEED, which writes to a soul memory store (not history.metta directly per design).

**Q4: AtomSpace consumer chain.** Writes to: &soul_verdict_in, &person_state. Reads from: &soul_verdict_in, &person_state. Calls soul-llm-call which is a separate LLM invocation (two LLM calls per msgnew cycle: one for person_state, one for soul_verdict).

**Q5: What the code now does.** On msgnew cycles, runs two soul-llm-calls to compute person_state and soul_verdict. On non-msgnew cycles, reads previous values from state. The verdict and person_state flow into soul_send_assemble and become part of the LLM-facing $send.

**Per the iteration 9 log:** soul_verdict_in is read from state on non-msgnew cycles and the existing verdict is reprinted. This is correct behavior — the soul shouldn't re-evaluate on every idle cycle.

**Q6: Upstream divergence.** N/A pure addition. Patrick has no soul intercept.

**Observation flag:** the soul intercept adds substantial bytes to the LLM prompt every cycle (via soul_send_assemble). On idle cycles, those bytes are stable (same verdict, same person_state). The contribution to "what the LLM sees in idle cycles" is meaningful. Per soul-as-sacred-cow, no modification proposed. Flag for understanding only.

---

## Item C7: getSoulBrief and final_prompt assembly

**SOUL-TOUCH: soul brief is core soul behavior. Audit only.**

**Q1: Provenance.** Sprint 1.5 (~April-May 2026). Lines 102-105 of our loop.metta.

**Q2: Prompt-surface contribution.** $soul_brief is concatenated with $prompt to form $enriched_prompt. Then $self_check is concatenated to form $final_prompt. So the LLM-facing prompt structure becomes: `<self_check><soul_brief><getContext>`. The soul_brief is a multi-line block summarizing soul state (per the getSoulBrief implementation in soul/). Size: variable but typically substantial (active goals, gaps, fuel, recent flourishings).

**Q3: History-surface contribution.** None directly.

**Q4: AtomSpace consumer chain.** Reads soul atoms (goals, gaps, fuel, flourishings). No writes from this call.

**Q5: What the code now does.** Every cycle, assembles a soul-brief from current AtomSpace soul atoms, concatenates with prompt, and (after $self_check is also prepended at line 105) becomes the $final_prompt passed to soul_send_assemble.

**Q6: Upstream divergence.** N/A pure addition.

**Observation flag:** soul_brief content can be substantial and is regenerated every cycle even on non-msgnew cycles. Like Item C6, this adds stable bytes to idle-cycle prompts. No modification proposed per soul-as-sacred-cow.

---

## Item C8: soul_send_assemble

**SOUL-TOUCH: this is the soul-aware prompt assembly mechanism. Audit only.**

**Q1: Provenance.** Stage 5b era, modified in Step5b injection plan (~April 23 2026) to add idle_directive parameter. Currently a 7-parameter helper at line 109-113.

**Q2: Prompt-surface contribution.** This is the final assembly point. Output is the $send string that goes directly to the LLM call. Combines: final_prompt (which includes self_check + soul_brief + getContext), soul_context_in, soul_verdict_in, person_state, flag_note, lastmessage, idle_directive. The output string structure has section markers (per artifact_2): PROMPT:, SKILLS:, OUTPUT_FORMAT:, SOUL_CONTEXT:, SOUL_VERDICT:, PERSON_STATE:, SOUL-NOTE:, HUMAN-LAST-MSG:, IDLE_DIRECTIVE:.

**Q3: History-surface contribution.** None directly. The output of soul_send_assemble is what the LLM SEES, not what gets written to history.

**Q4: AtomSpace consumer chain.** Consumes Python-side: the 7 parameters. No AtomSpace dependencies.

**Q5: What the code now does.** Every non-SILENT cycle, assembles the full $send string by concatenating its parameters with section markers. This is THE prompt the LLM reads.

**Q6: Upstream divergence.** Patrick has the much simpler `(py-str ($prompt :-:-:-: $lastmessage))` at upstream line 59. Our soul_send_assemble adds 5 additional parameters (soul_context, soul_verdict, person_state, flag_note, idle_directive) and their associated section markers to the LLM prompt.

**Observation flag:** **this is the Q4-risk surface from Item A1 audit.** When we apply spamShield mechanism and lastmessage becomes either anti-spam directive or empty string, soul_send_assemble needs to handle that gracefully. The current implementation probably concatenates whatever is passed without parsing. If it tries to strip "HUMAN-LAST-MSG:" prefix, it would fail. Pre-apply check requirement confirmed: verify soul_send_assemble's lastmessage handling before applying A1.

---

## Item C9: aliveness-gate

**SOUL-TOUCH: aliveness gate is core soul behavior. Audit only.**

**Q1: Provenance.** Sprint 1.5 initial; Step 6 v9 (~May 16 2026, commit 6ca6f44). Line 107 of our loop.metta.

**Q2: Prompt-surface contribution.** None directly. The gate produces a verdict (ENGAGE or SILENT) that gates whether the LLM call fires at all.

**Q3: History-surface contribution.** None directly. On SILENT, the LLM call doesn't happen so no response is generated, so addToHistory is not called for that cycle.

**Q4: AtomSpace consumer chain.** Reads: idle_directive (string), msgnew (boolean), (current-idle-pattern), (current-agency-balance), (current-phase), (latch-state). Writes: none directly; verdict is bound to $aliveness in let* but no AtomSpace write.

**Q5: What the code now does.** Per artifact_0 Section 3.5 finding, the gate is structurally complete but possibly behaviorally inert due to wakeupInterval=1 making idle_directive non-empty every cycle, which triggers priority 1 (idle_directive present OR msgnew → ENGAGE) every cycle, never reaching priorities 2-6 (substrate-composition gating).

**Verification need #1 in Section 6:** actual production wakeupInterval value. If 600, the gate-bypass analysis was wrong and the gate may be working as designed. If 1, the bypass is real.

**Q6: Upstream divergence.** N/A pure addition. Patrick has no aliveness gate.

**Observation flag:** the gate is THE mechanism that's supposed to silence non-warranted cycles. If it's bypassed (priority 1 always wins), Clarity engages every cycle. If wakeupInterval is actually 600 in production, the gate may be doing real work and the multi-fire (point 5 log evidence) is unrelated to the gate. Investigation phase will clarify.

---

## Item C10: self-check-guidance

**SOUL-TOUCH but flagged for retirement. Audit only.**

**Q1: Provenance.** Sprint 1.5 addition. Lines 104-105 of our loop.metta. Step 5 (commit 3d5b99d, ~May 16 2026) was intended to retire this from prompt assembly.

**Q2: Prompt-surface contribution.** $self_check is concatenated to $enriched_prompt to form $final_prompt. The function returns prompt-prepended guidance based on engaged_idle_count. Pre-Step-5 content was approximately: "SELF-CHECK: You've been idle for N cycles. Consider whether to surface a question, continue existing work, or be still."

**Verification need #2 in Section 6:** is self-check-guidance retirement complete or only partial? Live disk loop.metta line 104-105 still shows `$self_check` being concatenated. Either the retirement only removed the in-block call but the helper still returns content, OR Step 5's retirement was incomplete.

**Q3: History-surface contribution.** None directly.

**Q4: AtomSpace consumer chain.** Reads `(get-state &engaged_idle_count)`. No writes.

**Q5: What the code now does.** Unknown until verification need #2 is resolved. Either: (a) returns empty string post-Step-5 retirement and $self_check concatenation is effectively a no-op, or (b) still returns content that's still being prepended to the prompt.

**Q6: Upstream divergence.** N/A pure addition.

**Observation flag:** Step 5 retirement status uncertain. Verify before treating this as inert. If it's still active, it's contributing prompt-surface bytes every cycle.

---

## Item C11: Soul output intercept stub (Stage 5c)

**SOUL-TOUCH: future soul behavior, currently stubbed. Audit only.**

**Q1: Provenance.** Stage 5c stub (~April 2026). Line 127 of our loop.metta.

**Q2: Prompt-surface contribution.** None. The verdict is consumed downstream within the cycle, doesn't appear in next cycle's prompt.

**Q3: History-surface contribution.** Indirect — soul-note-record on non-PROCEED verdicts (line 134), but this writes to soul memory, not history.metta.

**Q4: AtomSpace consumer chain.** Writes literal `VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix` to $soul_verdict_out. Read by line 133 for soul-note-record gating.

**Q5: What the code now does.** Returns a literal string. No actual output evaluation. Per the literal value, this is acknowledged as pending-runtime-fix.

**Q6: Upstream divergence.** N/A pure addition.

**Observation flag:** stub only. Not contributing to pathology because it's not doing anything. Flag for future activation work (separate from echo investigation).

---

## Item C12: Recent-action populator + AtomSpace recent-action atoms

**Q1: Provenance.** Sprint 3 addition. Line 137 of our loop.metta. Implementation in soul/recent_action_populator.metta and soul/recent_action_retriever.metta plus helper.py functions.

**Q2: Prompt-surface contribution.** Indirect via Item C1 (YOUR_LAST_ACTION block) which reads recent-action atoms.

**Q3: History-surface contribution.** None directly. recent-action atoms live in AtomSpace, not history.metta.

**Q4: AtomSpace consumer chain.**
- Writer: `populate-recent-action` (line 137 cycle)
- Reads recent-action atoms: `format-one-action` for YOUR_LAST_ACTION (Item C1), `count-sends-in-window` for IDLE-PATTERN (Item C3)
- Atom shape: `(recent-action $cycle-id $type $description)`

**Q5: What the code now does.** Every cycle, classifies the just-emitted $sexpr into an action type (responsive-send, status-send-unprompted, pin-only, exploration-query, etc.) and writes a recent-action atom. The atom is then read by YOUR_LAST_ACTION and IDLE-PATTERN consumers for the next cycle's prompt.

**Per log evidence (iteration 8):** POPULATOR-DIAG fires correctly; cycle-id=8 msgnew=true sexpr-len=1 action-type=responsive-send. RECENT-ACTION-ATOMS shows 8 entries.

**Q6: Upstream divergence.** N/A pure addition. Patrick has no recent-action atoms.

**Observation flag:** the populator itself appears to be working correctly per log. The downstream effects (YOUR_LAST_ACTION format, IDLE-PATTERN computation) inherit whatever the populator writes. This is the data source for two prompt-surface items.

---

## Item C13: Awareness organ writers (do-update-idle-pattern, do-update-agency-balance)

**Q1: Provenance.** Steps 4.5 and 4.6 corrected splits (~May 15-16 2026). Lines 138-139 of our loop.metta. Defined in soul/idle_cycle_detector_writers.metta and soul/agency_balance_guard_writers.metta.

**Q2: Prompt-surface contribution.** Indirect via Items C3 (IDLE-PATTERN block) and C4 (AGENCY-BALANCE block).

**Q3: History-surface contribution.** None.

**Q4: AtomSpace consumer chain.**
- do-update-idle-pattern! writes `(idle-pattern $verdict $count)` atom. Reads recent-action atoms via count-sends-in-window.
- do-update-agency-balance! writes `(agency-balance $verdict)` atom. Reads recent-action atoms for analysis.

**Q5: What the code now does.** Every cycle, derives a verdict from current recent-action atoms and updates the IDLE-PATTERN and AGENCY-BALANCE atoms read by next cycle's prompt assembly.

**Q6: Upstream divergence.** N/A pure addition.

**Observation flag:** writers fire every cycle. If recent-action atoms are wrong, IDLE-PATTERN and AGENCY-BALANCE inherit the wrongness.

---

## Item C14: idle_directive computation

**Q1: Provenance.** Line 98 of our loop.metta. Sources from `helper.soul_idle_goal_prompt_v2` in helper.py. The function call site at line 98 is gated by `(if (and (not $msgnew) (> (get_time) (+ (get-state &last_human_time) (wakeupInterval))))`.

**Ownership uncertainty (verification need #3 in Section 6):** the supervisor/goal-prompt work was layered onto an earlier mechanism. Whether the entire idle_directive surface is ours or partially Patrick's needs git blame to confirm.

**Q2: Prompt-surface contribution.** Indirect via soul_send_assemble (Item C8) which takes idle_directive as its 7th parameter and appends "IDLE_DIRECTIVE: <content>" to the LLM prompt when non-empty.

**Q3: History-surface contribution.** None directly.

**Q4: AtomSpace consumer chain.** Reads &last_human_time. Writes to $idle_directive (let* binding) and triggers latch transition at line 99. Downstream read by aliveness-gate (line 107) as priority-1 signal.

**Q5: What the code now does.** When msgnew is false AND get_time > last_human_time + wakeupInterval, calls soul_idle_goal_prompt_v2 to generate an idle directive. Otherwise binds to empty string.

**Per log evidence (iteration 9):** IDLE_DIRECTIVE_RAW: "" — the directive is empty in iteration 9, meaning the wakeupInterval threshold hasn't been crossed yet (last_human_time was just updated in iteration 8 when Berton's message arrived).

**Q6: Upstream divergence.** Cannot fully determine without verification need #3. Upstream OmegaClaw current has no idle_directive computation in loop.metta. If our line 98 is wholly our addition, Q6 is N/A pure addition. If it's partially Patrick's older mechanism, Q6 changes.

**Observation flag:** in the multi-fire log evidence, idle_directive prints empty in iteration 9. So the multi-fire isn't being caused by idle_directive having multiple values (it's just empty). Whatever causes multi-fire is upstream of this in the let* chain.

---

## Item C15: Initialization additions in omegaclaw startup

**Q1: Provenance.** Stage 5b initial migration (~April 2026). Lines 56-57 of our loop.metta: `(initSoulSeeds)` and `(soul-rationality-startup-check)`.

**Q2: Prompt-surface contribution.** None. One-time startup operations.

**Q3: History-surface contribution.** None.

**Q4: AtomSpace consumer chain.** initSoulSeeds writes seed soul atoms to AtomSpace at startup. soul-rationality-startup-check verifies soul kernel atoms are loaded correctly (logs SOUL-AUDIT if there's a problem).

**Q5: What the code now does.** Runs once at container start. Initializes soul. Audits soul structure.

**Q6: Upstream divergence.** N/A pure addition.

**Observation flag:** one-time operations. Low pathology relevance unless soul initialization is failing silently. Could verify via SOUL-AUDIT log entries.

---

## Synthesized observations across Tier C

### Items contributing prompt-surface bytes every cycle

- C1 (YOUR_LAST_ACTION): every cycle, enumerated recent actions
- C2 (TASK-STATE): every cycle, phase + counter + threads
- C3 (IDLE-PATTERN): every cycle, verdict + count
- C4 (AGENCY-BALANCE): every cycle, verdict
- C5 (output-format-guidance): every cycle, output format spec
- C6 (Soul intercept block — indirectly via C8): every cycle, soul_context + soul_verdict + person_state in prompt
- C7 (getSoulBrief — indirectly via C8): every cycle, soul brief in prompt
- C10 (self-check-guidance): every cycle UNLESS verification confirms Step 5 fully retired it

### Items dependent on other Tier C items being correct

- C1 depends on C12 (recent-action atoms)
- C3 depends on C12 + C13
- C4 depends on C12 + C13
- C8 depends on C5, C6, C7, C9, C10, C14 outputs
- C9 depends on C14 (idle_directive value) and the awareness organs

### Items that don't contribute to non-msgnew cycle prompt

- C11 (output intercept stub): downstream of LLM call, doesn't echo across cycles
- C15 (init additions): startup-only

### Items flagged for soul-as-sacred-cow protection

C5, C6, C7, C8, C9, C10, C11. Any modification requires separate soul investigation per F115.

### Items most likely contributing to echo pathology (Tier C standpoint, hypothesis-level)

- C1 (YOUR_LAST_ACTION): explicit recent-action enumeration in LLM prompt may cue pattern continuation
- C6/C7/C8 combined: soul intercept contributions to prompt are substantial; on idle cycles they're stable (same verdict, same person_state) and add bytes the LLM reads every cycle
- C10 (self-check-guidance): if Step 5 didn't fully retire it, it's contributing to prompt

**These hypotheses are documented, NOT acted on.** Per soul-as-sacred-cow: even if C6/C7/C8 are echo contributors, modification requires separate investigation and proof of benefit. C1 and C10 may be modifiable since they're NOT soul-core (C1 is Sprint 3 awareness organ, C10 is meant to be retired anyway), but no proposal is being made here.

---

## Status

Tier C audits complete and tabled. Next move per investigation plan: iteration 9 multi-fire investigation. After multi-fire investigation completes, combine all findings (Tier A audits + Tier B inventory + Tier C audits + multi-fire root cause) into a global view for informed fix-direction choices.

## Document end
