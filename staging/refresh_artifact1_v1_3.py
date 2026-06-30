#!/usr/bin/env python3
"""
refresh_artifact1_v1_3.py

Targeted line-number + content refresh of Artifact 1 (loop.metta wiring diagram)
from its v1.2 state (body edited in place through May 20, closing note still dated
April 30) to v1.3, re-anchored against the live 171-line loop.metta.

DESIGN
------
Each edit is an explicit (label, old, new) triple. Edits are CONTENT-ANCHORED:
the new line numbers were derived by matching each diagram entry's quoted loop
fragment to its actual position in the live loop, NOT by a uniform offset (the
drift is non-monotonic: +7 in the upper phases, then a downward swing where the
old 14-line commented MeTTa mutation gate, old lines 127-140, was removed, then
partial recovery from the new DIAG block, live 139-147).

SAFETY
------
- Every old-string must occur EXACTLY ONCE. If it occurs 0 or >1 times the edit
  is reported and SKIPPED; the file is never partially corrupted.
- --dry-run prints every edit with a before/after line so you review first.
- --apply writes the file in place (operates on a copy you pass via --file).
- --reverse swaps old/new to restore.
- Edits tagged [CONTENT] change prose/architectural claims, not just numbers;
  review these with extra care in the dry-run.

CONVENTIONS
-----------
No em-dashes in generated text. Repo-root-relative paths. Action-summary block
prints on every apply. This script edits a DOCUMENT, so paren-delta and import
registration are N/A.
"""

import argparse
import sys

# ---------------------------------------------------------------------------
# OLD -> NEW single-line anchor map (documentation; not applied mechanically).
# Built by matching each diagram entry's quoted loop fragment to the live loop.
#   getContext def      old 34-38   -> live 38-45   (lastresults read: 36/38 -> 45)
#   let $prompt         old 55      -> live 62
#   iteration log       old 56      -> live 63
#   msgrcv/msgnew       old 57-59   -> live 64-66
#   $msg                old 60      -> live 67
#   &loops reset        old 61-62   -> live 68-69
#   $lastmessage        old 64-65   -> live 71
#   nextWakeAt write    old 66      -> live 72
#   last_human_time     old 68      -> live 74
#   soul-pre-compute    old 70      -> live 77
#   person state        old 71-74   -> live 78-81
#   log person          old 75      -> live 82
#   soul_context_in     old 76      -> live 83
#   soul eval           old 77-80   -> live 84-87
#   log verdict in      old 81      -> live 88
#   calibration         old 82-83   -> live 89-90
#   soul-note in        old 84-85   -> live 91-92
#   service learning    old 86      -> live 93
#   user context save   old 87      -> live 94
#   latch IDLE->ENG     old 88      -> live 95
#   goals/gaps/fuel     old 89/90/91-> live 96/97/98
#   idle directive      old 92      -> live 99
#   latch ENG->IDLE     old 93      -> live 100
#   engaged_idle_count  old 94      -> live 101
#   (cycles-since-input)            -> live 102   [NEW, documented in Step 2]
#   SoulBrief           old 95      -> live 103
#   enriched_prompt     old 96      -> live 104
#   (self-check)        old 97      -> RETIRED
#   log idle directive  old 99      -> live 105
#   aliveness-gate      old 100     -> live 106
#   log aliveness       old 101     -> live 107
#   send assembly       old 102-106 -> live 108-112
#   chars sent log      old 107     -> live 113
#   (last-activity send)            -> live 114   [NEW, documented in Step 2]
#   LLM call routing    old 108-112 -> live 115-117
#   $resp               old 113     -> live 118
#   validate response   old 114     -> live 119
#   $sexpr sread        old 115     -> live 120
#   error tracking      old 116-117 -> live 121-122
#   RESPONSE log        old 118     -> live 123
#   soul_verdict_out    old 121     -> live 126
#   log verdict out     old 122     -> live 127
#   metta_cmds extract  old 123-125 -> live 128-130
#   mutation gate (py)  old 126     -> live 131
#   commented MeTTa gate old 127-140-> REMOVED from loop surface
#   soul note out       old 141-142 -> live 132-133
#   EXECUTION $results   old 143    -> live 134
#   RESULTS-EXECUTED    old 144     -> live 135
#   populate-recent-action          -> live 136
#   do-update-idle-pattern!         -> live 137
#   do-update-agency-balance!       -> live 138
#   DIAG block                      -> live 139-147  [NEW]
#   PAUSE/Channel D     old 145-154 -> live 148-157
#   PROCEED/history     old 156-157 -> live 161/165
#   wake check          old 158-159 -> live 166-167
#   sleep               old 160     -> live 168
#   cut/gc              old 161-162 -> live 169-170
#   recurse             old 163     -> live 171
# ---------------------------------------------------------------------------

EDITS = [

    # ===================== PHASE OVERVIEW (Section 4 intro) =====================
    ("overview-4.1",
     "(soul input intercept, lines 70-87) is the **Salience Network (SN)**",
     "(soul input intercept, lines 77-94) is the **Salience Network (SN)**"),

    ("overview-4.2",
     "**Phase 4.2** (lines 88-94) is partly **SWITCH-HUB** (latch transitions) and partly **DMN** (lines 89-92,",
     "**Phase 4.2** (lines 95-102) is partly **SWITCH-HUB** (latch transitions) and partly **DMN** (lines 96-99,"),

    ("overview-4.3",
     "(prompt assembly and aliveness gate, lines 95-101) is the **SWITCH-HUB** firing. The aliveness gate at line 100 is",
     "(prompt assembly and aliveness gate, lines 103-107) is the **SWITCH-HUB** firing. The aliveness gate at line 106 is"),

    ("overview-4.4",
     "(response generation, lines 102-118) is the **FPN** firing.",
     "(response generation, lines 108-123) is the **FPN** firing."),

    ("overview-4.5",
     "(output verdict and execution, lines 120-144) is **SN-FPN coupling**. The SN should re-evaluate FPN action proposals before execution. Currently stubbed at line 121.",
     "(output verdict and execution, lines 125-147) is **SN-FPN coupling**. The SN should re-evaluate FPN action proposals before execution. Currently stubbed at line 126."),

    ("overview-4.6",
     "(PAUSE routing and history, lines 145-159) is **DMN write**",
     "(PAUSE routing and history, lines 148-167) is **DMN write**"),

    # ===================== PHASE SECTION HEADERS =====================
    ("hdr-4.0",
     "### Phase 4.0: Iteration entry and message reception (lines 47-68)",
     "### Phase 4.0: Iteration entry and message reception (lines 52-75)"),

    ("hdr-4.1",
     "### Phase 4.1: Soul input intercept (lines 69-87)",
     "### Phase 4.1: Soul input intercept (lines 76-94)"),

    ("hdr-4.3",
     "### Phase 4.3: Prompt assembly and aliveness gate (lines 95-101)",
     "### Phase 4.3: Prompt assembly and aliveness gate (lines 103-107)"),

    ("hdr-4.4",
     "### Phase 4.4: Response generation (lines 102-118)",
     "### Phase 4.4: Response generation (lines 108-123)"),

    ("hdr-4.5",
     "### Phase 4.5: Soul output intercept and command execution (lines 120-144)",
     "### Phase 4.5: Soul output intercept and command execution (lines 125-147)"),

    ("hdr-4.6",
     "### Phase 4.6: PAUSE routing and history update (lines 145-159)",
     "### Phase 4.6: PAUSE routing and history update (lines 148-167)"),

    # ===================== PHASE 4.0 WALK =====================
    ("p40-line55-hdr",
     "**Line 55** - `(let $prompt (getContext))` - Assembles the LLM prompt",
     "**Line 62** - `(let $prompt (getContext $k))` - Assembles the LLM prompt"),

    ("p40-line55-reads",
     "- Reads: `&lastresults` (via getContext line 38), getPrompt, getSkills, getHistory, current time",
     "- Reads: `&lastresults` (via getContext line 45), getPrompt, getSkills, getHistory, current time"),

    ("p40-line55-calls",
     "- Calls: getContext (defined line 34-38), which builds the full prompt string",
     "- Calls: getContext (defined line 38-45), which builds the full prompt string"),

    # [CONTENT] YOUR_LAST_ACTION is now BUILT (live line 41). Was a future hook.
    ("p40-line55-yla-CONTENT",
     "- \U0001f4a1 INSERTION POINT: A `YOUR_LAST_ACTION` field could be added here showing what the previous iteration's response did, breaking announcement loops at the substrate level. Requires a new state variable plus a summarization helper. Effort: 1 hour. Value: high.",
     "- \u2705 SHIPPED: The `YOUR_LAST_ACTION` field is wired in getContext at line 41 via `(your-last-action-block $k)`. It surfaces what the previous iteration's response did, breaking announcement loops at the substrate level. No longer a future hook."),

    ("p40-line56-hdr",
     "**Line 56** - `(println! (---------iteration $k))` - Logs iteration number to console.",
     "**Line 63** - `(println! (---------iteration $k))` - Logs iteration number to console."),

    ("p40-line5759-hdr",
     "**Lines 57-59** - `($msgrcv ...)` and `($msgnew ...)` - Receive new message",
     "**Lines 64-66** - `($msgrcv ...)` and `($msgnew ...)` - Receive new message"),

    ("p40-line60-hdr",
     "**Line 60** - `($msg (get-state &prevmsg))` - Binds $msg to current message text.",
     "**Line 67** - `($msg (get-state &prevmsg))` - Binds $msg to current message text."),

    ("p40-line6162-hdr",
     "**Line 61-62** - Reset loop counter on new message",
     "**Line 68-69** - Reset loop counter on new message"),

    ("p40-line6465-hdr",
     "**Lines 64-65** - `$lastmessage` conditional construction",
     "**Line 71** - `$lastmessage` conditional construction"),

    ("p40-line6465-consumers",
     "- Downstream consumers: line 72 println, line 113 soul_send_assemble (as 6th argument)",
     "- Downstream consumers: line 73 println, line 108 soul_send_assemble (as 6th argument)"),

    ("p40-spamshield-config",
     "spamShield config declared at line 9 (top-level), configured to True in initLoop (line 14 post-A1).",
     "spamShield config declared at line 9 (top-level), configured to True in initLoop (line 15 post-A1)."),

    ("p40-line66-hdr",
     "**Line 66** - `(change-state! &nextWakeAt (+ (get_time) (wakeupInterval)))` - Updates next idle wake timestamp every iteration.",
     "**Line 72** - `(change-state! &nextWakeAt (+ (get_time) (wakeupInterval)))` - Updates next idle wake timestamp every iteration."),

    ("p40-line68-hdr",
     "**Line 68** - `(if $msgnew (change-state! &last_human_time (get_time)) _)` - Records timestamp of last human contact, used for idle threshold detection.",
     "**Line 74** - `(if $msgnew (change-state! &last_human_time (get_time)) _)` - Records timestamp of last human contact, used for idle threshold detection."),

    # ===================== PHASE 4.1 WALK =====================
    ("p41-line70-hdr",
     "**Line 70** - `($soul_precompute (soul-pre-compute $msg))` - Pre-evaluation context priming",
     "**Line 77** - `($soul_precompute (soul-pre-compute $msg))` - Pre-evaluation context priming"),

    ("p41-line7174-hdr",
     "**Lines 71-74** - Person state assessment",
     "**Lines 78-81** - Person state assessment"),

    # ===================== PHASE 4.2 WALK =====================
    ("p42-line93-hdr",
     "**Line 93** - `(if (not (== $idle_directive \"\")) (set-atom! &self (latch-state ENGAGED) (latch-state IDLE)) _)`",
     "**Line 100** - `(if (not (== $idle_directive \"\")) (set-atom! &self (latch-state ENGAGED) (latch-state IDLE)) _)`"),

    ("p42-line94-hdr",
     "**Line 94** - Engaged-idle counter management",
     "**Line 101** - Engaged-idle counter management"),

    # ===================== PHASE 4.3 WALK =====================
    ("p43-line95-hdr",
     "**Line 95** - `($soul_brief (swrite (getSoulBrief)))`",
     "**Line 103** - `($soul_brief (swrite (getSoulBrief)))`"),

    ("p43-line96-hdr",
     "**Line 96** - `($enriched_prompt (string_concat $soul_brief $prompt))` - Combines soul brief with base prompt.",
     "**Line 104** - `($enriched_prompt (string_concat $soul_brief $prompt))` - Combines soul brief with base prompt."),

    ("p43-line97-selfcheck",
     "- **Phase 1 (original wiring, pre-Sprint-1.5):** Line 97 called `(py-call (helper.soul_self_check_prompt (get-state &engaged_idle_count)))`.",
     "- **Phase 1 (original wiring, pre-Sprint-1.5):** The pre-Sprint-1.5 self-check (former line 97) called `(py-call (helper.soul_self_check_prompt (get-state &engaged_idle_count)))`."),

    ("p43-line99-hdr",
     "**Line 99** - Logs raw idle directive.",
     "**Line 105** - Logs raw idle directive."),

    ("p43-line100-hdr",
     "**Line 100** - `($aliveness (aliveness-gate $msgnew $idle_directive))`",
     "**Line 106** - `($aliveness (aliveness-gate $msgnew $idle_directive))`"),

    ("p43-line101-hdr",
     "**Line 101** - Logs aliveness verdict.",
     "**Line 107** - Logs aliveness verdict."),

    # ===================== PHASE 4.4 WALK =====================
    ("p44-line102106-hdr",
     "**Lines 102-106** - Send assembly",
     "**Lines 108-112** - Send assembly"),

    ("p44-line107-hdr",
     "**Line 107** - Logs sent characters or SILENT_CYCLE.",
     "**Line 113** - Logs sent characters or SILENT_CYCLE."),

    ("p44-line108112-hdr",
     "**Lines 108-112** - LLM call routing",
     "**Lines 115-117** - LLM call routing"),

    ("p44-line113-hdr",
     "**Line 113** - `($resp (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))`",
     "**Line 118** - `($resp (py-call (helper.normalize_string (py-call (helper.balance_parentheses $respi)))))`"),

    ("p44-line114-hdr",
     "**Line 114** - Validates response starts with \"(\", else logs reminder",
     "**Line 119** - Validates response starts with \"(\", else logs reminder"),

    ("p44-line115-hdr",
     "**Line 115** - `($sexpr (catch (sread $response)))` - Parse response into S-expression",
     "**Line 120** - `($sexpr (catch (sread $response)))` - Parse response into S-expression"),

    ("p44-line116117-hdr",
     "**Lines 116-117** - Error tracking and HandleError invocation",
     "**Lines 121-122** - Error tracking and HandleError invocation"),

    ("p44-line118-hdr",
     "**Line 118** - Logs RESPONSE.",
     "**Line 123** - Logs RESPONSE."),

    # [CONTENT] YOUR_LAST_ACTION insertion-point note (now shipped)
    ("p44-line118-yla-CONTENT",
     "- \U0001f4a1 INSERTION POINT: This is where the \"YOUR_LAST_ACTION\" mentioned in line 55 would need to update state - right after RESPONSE is printed, summarize $sexpr and write to a new state variable.",
     "- \u2705 SHIPPED: The \"YOUR_LAST_ACTION\" field is now built and read in getContext at line 41 via `(your-last-action-block $k)`. The previous-iteration summary surfaces in the prompt without a separate write here."),

    # ===================== PHASE 4.5 WALK =====================
    ("p45-line121-hdr",
     "**Line 121** - `($soul_verdict_out \"VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix\")`",
     "**Line 126** - `($soul_verdict_out \"VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix\")`"),

    ("p45-line122-hdr",
     "**Line 122** - Logs output verdict.",
     "**Line 127** - Logs output verdict."),

    ("p45-line123125-hdr",
     "**Lines 123-125** - Extract MeTTa commands from response",
     "**Lines 128-130** - Extract MeTTa commands from response"),

    ("p45-line126-hdr",
     "**Line 126** - Soul mutation gate (Python)",
     "**Line 131** - Soul mutation gate (Python)"),

    # [CONTENT] commented MeTTa gate (old 127-140) removed from loop surface
    ("p45-line126-elev-CONTENT",
     "- \U0001f527 ELEVATION FLAG (READY TO SHIP): Lines 127-140 are the COMMENTED-OUT MeTTa version of this gate. The work is already drafted. Validation: compare commented MeTTa logic to Python helper logic, confirm equivalence, uncomment, test. Effort: 30 minutes. Value: HIGH per architectural-cleanliness, MEDIUM per operational impact (mutations are infrequent).",
     "- \U0001f527 ELEVATION FLAG: The commented-out MeTTa version of this gate (former lines 127-140) has been REMOVED from the loop.metta surface. If pursuing this elevation, recover the draft from git history rather than from the live file. Effort: 30 minutes once recovered. Value: HIGH per architectural-cleanliness, MEDIUM per operational impact (mutations are infrequent). [CONFIRM: where the MeTTa draft now lives, git history or a soul file.]"),

    ("p45-line127140-dormant-CONTENT",
     "**Lines 127-140** - Commented-out MeTTa mutation gate (DORMANT, ready for activation per above flag)",
     "**(removed)** - The commented-out MeTTa mutation gate that formerly occupied lines 127-140 has been removed from loop.metta. Live lines 132-147 are now the soul-note-out, execution, cycle-tail writers, and DIAG block (see below). The MeTTa-gate draft, if still wanted, lives in git history."),

    ("p45-line141142-hdr",
     "**Lines 141-142** - Soul note recording on output",
     "**Lines 132-133** - Soul note recording on output"),

    ("p45-line143-hdr",
     "**Line 143** - Command execution",
     "**Line 134** - Command execution"),

    ("p45-line143-danger",
     "- \u26a0\ufe0f DANGER ZONE: This is where command execution actually happens. All security-relevant decisions about commands needed to happen BEFORE this line. The output intercept stub at line 121 is supposed to gate this - and currently doesn't.",
     "- \u26a0\ufe0f DANGER ZONE: This is where command execution actually happens. All security-relevant decisions about commands needed to happen BEFORE this line. The output intercept stub at line 126 is supposed to gate this - and currently doesn't. This is the gate insertion site: the corner-gap force-silence gate binds `$sexpr_gated` between live lines 133 and 134, consumed only by this execution."),

    ("p45-line144-hdr",
     "**Line 144** - Logs RESULTS-EXECUTED.",
     "**Line 135** - Logs RESULTS-EXECUTED."),

    # populate-recent-action explicit anchor (was only referenced parenthetically)
    ("p45-cycletail-pra-CONTENT",
     "**Cycle tail (after populate-recent-action)** - `($_ (do-update-idle-pattern!))`",
     "**Cycle tail line 136** - `($_ (populate-recent-action $sexpr $msgnew $k))` writes the per-cycle 3-field recent-action atom. **Line 137** - `($_ (do-update-idle-pattern!))`"),

    ("p45-cycletail-ab",
     "**Cycle tail (after do-update-idle-pattern!)** - `($_ (do-update-agency-balance!))`",
     "**Cycle tail line 138** - `($_ (do-update-agency-balance!))`"),

    # [CONTENT] DIAG block new documentation (insert after the agency-balance cycle-tail entry's last line)
    ("p45-diag-block-CONTENT",
     "- Step 4.6 (May 15 2026 corrected split): replaces the original 4.6 attempt (recursive-counter pattern, F32 fail). Algorithm (d) extended to two counters with six tag literals. F42 bare-call audit applied to dependency-detected (hardcoded 0.6); ecosystem-healthy latent F42 bugs documented as fix-on-future-wiring. Substrate ships with writers/consumers split from day one per task_state precedent (Discipline 2 refinement); zero deferred refactor debt.",
     "- Step 4.6 (May 15 2026 corrected split): replaces the original 4.6 attempt (recursive-counter pattern, F32 fail). Algorithm (d) extended to two counters with six tag literals. F42 bare-call audit applied to dependency-detected (hardcoded 0.6); ecosystem-healthy latent F42 bugs documented as fix-on-future-wiring. Substrate ships with writers/consumers split from day one per task_state precedent (Discipline 2 refinement); zero deferred refactor debt.\n\n**DIAG block (lines 139-147)** - Nine `($_dN (println! (DIAG-...)))` probes\n- Emits per-cycle diagnostics: DIAG-CYCLE-START/END, DIAG-COUNT-FN, DIAG-LITERAL-RESPONSIVE, DIAG-LITERAL-STATUS, DIAG-VARIABLE-TAG, DIAG-RECENT-ACTION-COUNT, DIAG-IDLE-PATTERN-ATOMS, DIAG-IDLE-PATTERN-COUNT.\n- \U0001f4cd METTA-CALL POINT: Pure substrate reads (match/size-atom/collapse), no LLM. Observability only; no state writes.\n- These post-date the v1.2 diagram and sit between the cycle-tail writers (136-138) and the PAUSE/PROCEED branch (148+)."),

    # ===================== PHASE 4.6 WALK =====================
    ("p46-line145154-hdr",
     "**Lines 145-154** - PAUSE path (Channel D)",
     "**Lines 148-157** - PAUSE path (Channel D)"),

    ("p46-line156157-hdr",
     "**Lines 156-157** - PROCEED/FLAG path (normal)",
     "**Lines 158-165** - PROCEED/FLAG path (normal)"),

    ("p46-line158159-hdr",
     "**Lines 158-159** - Wake check",
     "**Lines 166-167** - Wake check"),

    ("p46-line160-hdr",
     "**Line 160** - `(sleep (sleepInterval))` - 1-second pause between iterations.",
     "**Line 168** - `(sleep (sleepInterval))` - 1-second pause between iterations."),

    ("p46-line161162-hdr",
     "**Lines 161-162** - Prolog substrate housekeeping (Tier B1 upstream merge, 2026-05-19)",
     "**Lines 169-170** - Prolog substrate housekeeping (Tier B1 upstream merge, 2026-05-19)"),

    ("p46-line163-hdr",
     "**Line 163** - `(omegaclaw (+ 1 $k))` - Recursive call for next iteration.",
     "**Line 171** - `(omegaclaw (+ 1 $k))` - Recursive call for next iteration."),

    # ===================== STEP 2 WIRING HOOKS =====================
    ("step2-lastactivity-p40",
     "**Phase 4.0 last-activity hook** (added after the existing `&last_human_time`\nwrite at line 68). Calls `(do-set-last-activity! (get_time))` when $msgnew",
     "**Phase 4.0 last-activity hook** (live line 75, after the existing `&last_human_time`\nwrite at line 74). Calls `(do-set-last-activity! (get_time))` when $msgnew"),

    ("step2-cycles-p42",
     "**Phase 4.2 cycles-since-input hook** (added after the existing\n`&engaged_idle_count` write at line 94). Calls",
     "**Phase 4.2 cycles-since-input hook** (live line 102, after the existing\n`&engaged_idle_count` write at line 101). Calls"),

    ("step2-lastactivity-p44",
     "**Phase 4.4 last-activity post-send hook** (added after the CHARS_SENT/\nSILENT_CYCLE println at line 107). Calls `(do-set-last-activity! (get_time))`",
     "**Phase 4.4 last-activity post-send hook** (live line 114, after the CHARS_SENT/\nSILENT_CYCLE println at line 113). Calls `(do-set-last-activity! (get_time))`"),

    ("step2-elev-line97",
     "`&engaged_idle_count` (line 97) to reading task-state primitives,",
     "`&engaged_idle_count` (former line 97, self-check retired) to reading task-state primitives,"),

    # ===================== SECTION 5: LATCH =====================
    ("s5-used-by",
     "- Used by loop.metta line 88, line 93 (raw transitions) and aliveness_gate.metta (match query)",
     "- Used by loop.metta line 95, line 100 (raw transitions) and aliveness_gate.metta (match query)"),

    ("s5-silent-skip",
     "- The SILENT verdict causes loop.metta to skip the LLM call entirely (line 102, 108)",
     "- The SILENT verdict causes loop.metta to skip the LLM call entirely (line 108, 115)"),

    ("s5-idle-eng-where",
     "- Where: loop.metta line 88, `(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))`",
     "- Where: loop.metta line 95, `(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))`"),

    ("s5-idle-eng-side",
     "- Side effect: clears engaged_idle_count to 0 (line 94)",
     "- Side effect: clears engaged_idle_count to 0 (line 101)"),

    ("s5-eng-idle-where",
     "- Where: loop.metta line 93, `(set-atom! &self (latch-state ENGAGED) (latch-state IDLE))`",
     "- Where: loop.metta line 100, `(set-atom! &self (latch-state ENGAGED) (latch-state IDLE))`"),

    ("s5-raw-implication",
     "If for any reason the latch were in an unexpected state (say COMPLETING), the line 88 transition (IDLE \u2192 ENGAGED)",
     "If for any reason the latch were in an unexpected state (say COMPLETING), the line 95 transition (IDLE \u2192 ENGAGED)"),

    ("s5-gate-acts",
     "The gate function (`soul/aliveness_gate.metta`) is what produces the ENGAGE-vs-SILENT verdict that loop.metta line 100-101 acts on:",
     "The gate function (`soul/aliveness_gate.metta`) is what produces the ENGAGE-vs-SILENT verdict that loop.metta line 106-107 acts on:"),

    ("s5-callout-88",
     "**\U0001f4cd METTA-CALL POINT (line 88):** `(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))` - direct MeTTa space mutation, no Python involved. Clean substrate operation.",
     "**\U0001f4cd METTA-CALL POINT (line 95):** `(set-atom! &self (latch-state IDLE) (latch-state ENGAGED))` - direct MeTTa space mutation, no Python involved. Clean substrate operation."),

    ("s5-callout-93",
     "**\U0001f4cd METTA-CALL POINT (line 93):** Same shape as line 88, opposite direction. Clean.",
     "**\U0001f4cd METTA-CALL POINT (line 100):** Same shape as line 95, opposite direction. Clean."),

    ("s5-callout-100",
     "**\U0001f4cd METTA-CALL POINT (line 100):** `(aliveness-gate $msgnew $idle_directive)` - calls the soul/aliveness_gate.metta function.",
     "**\U0001f4cd METTA-CALL POINT (line 106):** `(aliveness-gate $msgnew $idle_directive)` - calls the soul/aliveness_gate.metta function."),

    ("s5-callout-danger",
     "**\u26a0\ufe0f DANGER ZONE (lines 102, 107, 108):** Three separate lines all conditional on `(== $aliveness SILENT)`.",
     "**\u26a0\ufe0f DANGER ZONE (lines 108, 113, 115):** Three separate lines all conditional on `(== $aliveness SILENT)`."),

    ("s5-callout-elev",
     "Replacing loop.metta's lines 88 and 93 with calls to `engage-from-idle` and the appropriate guarded transition",
     "Replacing loop.metta's lines 95 and 100 with calls to `engage-from-idle` and the appropriate guarded transition"),

    ("s5-callout-insert",
     "Add a new `latch-dispatch` rule for the new state, add the new state to the latch state machine, and extend lines 102/107/108 conditionals.",
     "Add a new `latch-dispatch` rule for the new state, add the new state to the latch state machine, and extend lines 108/113/115 conditionals."),

    # ===================== SECTION 6: SOUL PIPELINE CHANNELS =====================
    ("s6-channelA",
     "**Channel A (Person State Detection):** Lines 71-74.",
     "**Channel A (Person State Detection):** Lines 78-81."),

    ("s6-channelBC",
     "**Channels B+C (Soul Evaluation):** Lines 77-80.",
     "**Channels B+C (Soul Evaluation):** Lines 84-87."),

    ("s6-channelD",
     "**Channel D (Voice/PAUSE response):** Lines 145-153.",
     "**Channel D (Voice/PAUSE response):** Lines 150-157."),

    # ===================== SECTION 7: MUTATION GATE =====================
    ("s7-current-impl",
     "Line 126 of loop.metta: `($soul_mutation_flag (py-call (helper.soul_mutation_gate (repr $metta_cmds) (get-state &soul_mutation_lock))))`",
     "Line 131 of loop.metta: `($soul_mutation_flag (py-call (helper.soul_mutation_gate (repr $metta_cmds) (get-state &soul_mutation_lock))))`"),

    # [CONTENT] dormant MeTTa gate removed
    ("s7-dormant-CONTENT",
     "Lines 127-140 of loop.metta contain the commented-out MeTTa version of this gate. It uses substrate operations (`soul-any-metta?`, `soul-extract-metta-arg`, `soul-metta-targets-soul-namespace?`, `soul-mutation-pending?`) that would need to exist in soul/ atoms.",
     "The commented-out MeTTa version of this gate (formerly lines 127-140 of loop.metta) has been REMOVED from the live file. It used substrate operations (`soul-any-metta?`, `soul-extract-metta-arg`, `soul-metta-targets-soul-namespace?`, `soul-mutation-pending?`) that would need to exist in soul/ atoms. The draft, if still wanted, lives in git history. [CONFIRM where the draft now lives.]"),

    ("s7-elev-CONTENT",
     "3. If equivalent, uncomment lines 127-140 and remove the Python call on line 126",
     "3. If equivalent, restore the MeTTa draft from git history and remove the Python call on line 131"),

    # ===================== SECTION 8: OUTPUT VERDICT STUB =====================
    ("s8-line121",
     "Line 121 of loop.metta: hardcoded `\"VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix\"`",
     "Line 126 of loop.metta: hardcoded `\"VERDICT: PROCEED SOUL-NOTE: output-intercept-pending-runtime-fix\"`"),

    ("s8-check-gate",
     "3. Check against soul mutation gate output (already computed at line 126)",
     "3. Check against soul mutation gate output (already computed at line 131)"),

    ("s8-replace-line",
     "5. Replace line 121 with the call",
     "5. Replace line 126 with the call"),

    # ===================== SECTION 10 / CLOSING =====================
    ("s10-task-context",
     "- Line 26 (&task_context): Initialized but searched references show no read or write elsewhere in loop.metta.",
     "- Line 28 (&task_context): Initialized but searched references show no read or write elsewhere in loop.metta."),

    ("s10-pending-mutation",
     "- Line 28 (&pending_soul_mutation): Same situation. May be unused or referenced through the mutation gate Python helper.",
     "- Line 30 (&pending_soul_mutation): Same situation. May be unused or referenced through the mutation gate Python helper."),

    ("s10-nextwakeat",
     "- Line 66 (&nextWakeAt): Read at line 158 within loop.metta, fully traced.",
     "- Line 72 (&nextWakeAt): Read at line 166 within loop.metta, fully traced."),

    # [CONTENT] closing note date + drift directive
    ("close-date-CONTENT",
     "This document represents the wiring of loop.metta as of April 30, 2026. Future architectural changes should update the relevant sections rather than letting this document drift. The \"Active vs Dormant\" classifications in particular need refresh whenever something is wired or unwired.",
     "This document (v1.3) represents the wiring of loop.metta as of June 4, 2026, re-anchored against the live 171-line loop. Future architectural changes should update the relevant sections rather than letting this document drift. The \"Active vs Dormant\" classifications in particular need refresh whenever something is wired or unwired.\n\nv1.3 changelog (June 4, 2026): re-anchored all per-cycle line numbers to the live 171-line loop (non-uniform drift, +7 upper phases, downward swing where the old commented MeTTa mutation gate at lines 127-140 was removed, partial recovery from the new DIAG block at 139-147). Marked YOUR_LAST_ACTION as shipped (wired in getContext at line 41). Removed the dormant MeTTa-mutation-gate references and pointed them at git history. Added DIAG block documentation. Retired self-check from the elevation list. Recorded the corner-gap gate insertion site at the execution binding (between lines 133 and 134)."),

    # [CONTENT] elevation list: retire shipped/removed items
    ("close-elev-mutation-CONTENT",
     "1. **Soul mutation gate** (Section 7) - drafted, just needs activation. 30-60 minutes.",
     "1. **Soul mutation gate** (Section 7) - MeTTa draft removed from loop surface; recover from git history before activation. 30-60 minutes once recovered."),

    ("close-elev-selfcheck-CONTENT",
     "3. **Self-check threshold + softer message** (Section 4 line 97) - operational fix, 10 minutes.",
     "3. **(retired)** Self-check was removed from prompt assembly (Step 5); the orientation work is now carried by task-phase, idle-pattern, and agency-balance observation organs."),

    ("close-elev-yla-CONTENT",
     "5. **YOUR_LAST_ACTION field** (Section 4 line 55 + 118) - breaks announcement loops. 1 hour.",
     "5. **(shipped)** YOUR_LAST_ACTION field is wired in getContext at line 41; it breaks announcement loops at the substrate level."),

    ("close-elev-idle",
     "7. **Idle directive elevation** (Section 4 line 92) - the biggest move, but has the most existing substrate vocabulary to work with. Multi-session.",
     "7. **Idle directive elevation** (Section 4 line 99) - the biggest move, but has the most existing substrate vocabulary to work with. Multi-session."),

    # ===================== SECTION 2: STATE-VARIABLE TABLE =====================
    # Read/write cells traced against the live loop per variable.
    ("s2-prevmsg",
     "human channel | Line 59 | Line 59 |",
     "human channel | Line 65, line 67 | Line 66 |"),

    ("s2-lastresults",
     "Line 36 (via getContext \u2192 LAST_SKILL_USE_RESULTS) | Line 157 |",
     "Line 45 (via getContext \u2192 LAST_SKILL_USE_RESULTS) | Line 165 |"),

    ("s2-error",
     "Line 42, line 116 | Line 42 (sets new error), line 116 (clears) |",
     "Line 49, line 121 | Line 49 (sets new error), line 121 (clears) |"),

    ("s2-verdict-in",
     "Line 80, line 145, line 152 | Line 80, line 153 |",
     "Line 87, line 148, line 151 | Line 87, line 156 |"),

    ("s2-verdict-out",
     "Line 121 | Line 121 (assigned but not from substantive evaluation) |",
     "Line 126 | Line 126 (assigned but not from substantive evaluation) |"),

    ("s2-person-state",
     "Line 73, line 102 | Line 74 |",
     "Line 80, line 108 | Line 81 |"),

    # [CONTENT] lock write cell referenced the removed commented MeTTa gate
    ("s2-mutation-lock-CONTENT",
     "Line 126 (read by gate) | Line 137 commented out (would write on commit) |",
     "Line 131 (read by gate) | Lock managed by Python helper; former line 137 commented-out MeTTa write removed |"),

    ("s2-last-human-time",
     "Line 92 (computes idle) | Line 68 |",
     "Line 99 (computes idle) | Line 74 |"),

    ("s2-engaged-idle",
     "Line 94, line 97 | Line 94 |",
     "Line 101 (self-check consumer retired) | Line 101 |"),

    ("s2-loops",
     "Line 54, line 62 | Line 54, line 62, line 154 |",
     "Line 55, line 61 | Line 55, line 61, line 157 |"),

    ("s2-nextwakeat",
     "[gap flag: read elsewhere?] | Line 66 |",
     "Line 166 | Line 72 |"),

    # ===================== SECTION 2: ATOM TABLE =====================
    ("s2-atom-latch",
     "Loop.metta line 88 (raw transition), line 93, aliveness_gate match",
     "Loop.metta line 95 (raw transition), line 100, aliveness_gate match"),

    ("s2-atom-goals",
     "Loop.metta line 89, get_soul_brief brief-active-goals",
     "Loop.metta line 96, get_soul_brief brief-active-goals"),

    ("s2-atom-gaps",
     "Loop.metta line 90, brief-high-gaps",
     "Loop.metta line 97, brief-high-gaps"),

    ("s2-atom-fuel",
     "Loop.metta line 91, brief-creative-direction",
     "Loop.metta line 98, brief-creative-direction"),

    # ===================== SECTION 2: PIGGYBACK CALLOUTS =====================
    ("s2-piggy-86",
     "**Line 86 piggyback (helper.soul_service_learning):**",
     "**Line 93 piggyback (helper.soul_service_learning):**"),

    ("s2-piggy-87",
     "**Line 87 piggyback (helper.soul_user_context_save):**",
     "**Line 94 piggyback (helper.soul_user_context_save):**"),

    ("s2-piggy-88",
     "**Line 88 piggyback (latch transition):**",
     "**Line 95 piggyback (latch transition):**"),

    # ===================== SECTION 3: HOT-ATOM + IDENTITY KERNEL =====================
    ("s3-hot-getsoulbrief",
     "- soul/get_soul_brief (HOT - called at loop.metta line 95)",
     "- soul/get_soul_brief (HOT - called at loop.metta line 103)"),

    ("s3-hot-aliveness",
     "- soul/aliveness_gate (HOT - called at loop.metta line 100)",
     "- soul/aliveness_gate (HOT - called at loop.metta line 106)"),

    ("s3-identity-gate",
     "the mutation gate at line 126 is the only protection",
     "the mutation gate at line 131 is the only protection"),

    # ===================== PHASE 4.1 MIDDLE WALK =====================
    ("p41-verdict-consumers",
     "The verdict format is consumed by many downstream lines (84, 121 reference, 145 for PAUSE detection).",
     "The verdict format is consumed by many downstream lines (91, 126 reference, 148 for PAUSE detection)."),

    ("p41-line75-hdr",
     "**Line 75** - Logs person state.",
     "**Line 82** - Logs person state."),

    ("p41-line76-hdr",
     "**Line 76** - `($soul_context_in (py-call (helper.soul_brief_tier_a_static)))` - Static tier-A soul context",
     "**Line 83** - `($soul_context_in (py-call (helper.soul_brief_tier_a_static)))` - Static tier-A soul context"),

    ("p41-line7780-hdr",
     "**Lines 77-80** - Soul evaluation (Channel A/B+C)",
     "**Lines 84-87** - Soul evaluation (Channel A/B+C)"),

    ("p41-line81-hdr",
     "**Line 81** - Logs soul verdict.",
     "**Line 88** - Logs soul verdict."),

    ("p41-line8283-hdr",
     "**Lines 82-83** - Soul calibration recording",
     "**Lines 89-90** - Soul calibration recording"),

    ("p41-line8485-hdr",
     "**Lines 84-85** - Soul note recording (when verdict is not PROCEED)",
     "**Lines 91-92** - Soul note recording (when verdict is not PROCEED)"),

    ("p41-line86-hdr",
     "**Line 86** - Service learning",
     "**Line 93** - Service learning"),

    ("p41-line87-hdr",
     "**Line 87** - User context save",
     "**Line 94** - User context save"),

    ("p41-line87-danger",
     "This is the second ChromaDB write triggered by a single new human message (first was line 86).",
     "This is the second ChromaDB write triggered by a single new human message (first was line 93)."),

    # ===================== PHASE 4.2 WALK =====================
    ("p42-hdr",
     "### Phase 4.2: Aliveness state and AtomSpace queries (lines 88-94)",
     "### Phase 4.2: Aliveness state and AtomSpace queries (lines 95-102)"),

    ("p42-line88-hdr",
     "**Line 88** - `(if $msgnew (set-atom! &self (latch-state IDLE) (latch-state ENGAGED)) _)`",
     "**Line 95** - `(if $msgnew (set-atom! &self (latch-state IDLE) (latch-state ENGAGED)) _)`"),

    ("p42-line89-hdr",
     "**Line 89** - `($atomspace_goals (collapse (match &self (= (active-goal $n) $g) ($n $g))))`",
     "**Line 96** - `($atomspace_goals (collapse (match &self (= (active-goal $n) $g) ($n $g))))`"),

    ("p42-line89-dmn",
     "Reading them here is the DMN preparing its inputs for the idle directive computation at line 92.",
     "Reading them here is the DMN preparing its inputs for the idle directive computation at line 99."),

    ("p42-line89-note",
     "The downstream consumer (line 92) is responsible for filtering by status.",
     "The downstream consumer (line 99) is responsible for filtering by status."),

    ("p42-line90-hdr",
     "**Line 90** - `($atomspace_gaps (collapse (match &self (= (self-map-gap $name) $g) ($name $g))))`",
     "**Line 97** - `($atomspace_gaps (collapse (match &self (= (self-map-gap $name) $g) ($name $g))))`"),

    ("p42-line90-note",
     "Combined with lines 89 and 91, these three reads",
     "Combined with lines 96 and 98, these three reads"),

    ("p42-line91-hdr",
     "**Line 91** - `($atomspace_fuel (collapse (match &self (= (creative-fuel $type) $f) ($type $f))))`",
     "**Line 98** - `($atomspace_fuel (collapse (match &self (= (creative-fuel $type) $f) ($type $f))))`"),

    ("p42-line92-hdr",
     "**Line 92** - Idle directive generation",
     "**Line 99** - Idle directive generation"),

    # ===================== SECTION 9: HOT PATTERN TABLE =====================
    ("s9-hot-goals",
     "| (active-goal $n) | soul/active_goals.metta | HOT (line 89, every iteration) | DMN |",
     "| (active-goal $n) | soul/active_goals.metta | HOT (line 96, every iteration) | DMN |"),

    ("s9-hot-gaps",
     "| (self-map-gap $name) | soul/self_map.metta | HOT (line 90, every iteration) | DMN |",
     "| (self-map-gap $name) | soul/self_map.metta | HOT (line 97, every iteration) | DMN |"),

    ("s9-hot-fuel",
     "| (creative-fuel $type) | soul/creative_fuel.metta | HOT (line 91, every iteration) | DMN |",
     "| (creative-fuel $type) | soul/creative_fuel.metta | HOT (line 98, every iteration) | DMN |"),

    ("s9-hot-brief",
     "| getSoulBrief | soul/get_soul_brief.metta | HOT (line 95, every iteration) | DMN\u2192FPN |",
     "| getSoulBrief | soul/get_soul_brief.metta | HOT (line 103, every iteration) | DMN\u2192FPN |"),

    ("s9-hot-aliveness",
     "| aliveness-gate | soul/aliveness_gate.metta | HOT (line 100, every iteration) | SWITCH-HUB |",
     "| aliveness-gate | soul/aliveness_gate.metta | HOT (line 106, every iteration) | SWITCH-HUB |"),

    # ===================== MISSED NETWORK-RELEVANT BULLETS =====================
    # [CONTENT] mutation-gate net-rel bullet still cited the removed draft as active
    ("p45-gate-netrel-CONTENT",
     "Activating the dormant MeTTa version (lines 127-140) is the cleanest example of how the FPN's substrate-derived inhibition should look.",
     "Activating a MeTTa version of this gate (the former lines 127-140 draft, now removed from the loop and recoverable from git history) would be the cleanest example of how the FPN's substrate-derived inhibition should look."),

    # execution net-rel bullet still cited the stub at old line 121
    ("p45-exec-netrel",
     "this should be gated by SN re-evaluation (line 121, currently stubbed).",
     "this should be gated by SN re-evaluation (line 126, currently stubbed)."),
]


def run(path, mode):
    with open(path, "r", encoding="utf-8") as f:
        text = original = f.read()

    applied, skipped = [], []
    for label, old, new in EDITS:
        a, b = (old, new) if mode != "reverse" else (new, old)
        count = text.count(a)
        if count == 1:
            if mode == "apply" or mode == "reverse":
                text = text.replace(a, b, 1)
            applied.append((label, a, b, count))
        else:
            skipped.append((label, a, count))

    if mode == "dry-run":
        for label, a, b, _ in applied:
            tag = " [CONTENT]" if label.endswith("CONTENT") else ""
            print(f"--- WOULD EDIT: {label}{tag}")
            print(f"    OLD: {a.splitlines()[0][:140]}")
            print(f"    NEW: {b.splitlines()[0][:140]}")
        if skipped:
            print("\n=== SKIPPED (match count != 1; review/repair these) ===")
            for label, a, count in skipped:
                print(f"  ! {label}: found {count}x -> {a.splitlines()[0][:120]}")
        print(f"\nSUMMARY: {len(applied)} edits would apply, {len(skipped)} skipped, "
              f"of {len(EDITS)} total.")
        return

    if mode in ("apply", "reverse"):
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        verb = "APPLIED" if mode == "apply" else "REVERSED"
        print("=" * 64)
        print(f"ACTION SUMMARY ({verb})")
        print("=" * 64)
        print(f"File:    {path}")
        print(f"Edits {verb.lower()}: {len(applied)} / {len(EDITS)}")
        if skipped:
            print(f"Skipped (match != 1): {len(skipped)} -- NOT applied:")
            for label, a, count in skipped:
                print(f"  ! {label}: found {count}x")
        content = [l for (l, *_rest) in applied if l.endswith("CONTENT")]
        print(f"Content-level edits in this run: {len(content)}")
        for l in content:
            print(f"  [CONTENT] {l}")
        print(f"Bytes: {len(original)} -> {len(text)}")
        print("=" * 64)


def main():
    p = argparse.ArgumentParser(description="Artifact 1 v1.3 refresh")
    p.add_argument("--file", required=True, help="path to artifact_1 markdown")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--reverse", action="store_true")
    args = p.parse_args()
    mode = "dry-run" if args.dry_run else "apply" if args.apply else "reverse"
    run(args.file, mode)


if __name__ == "__main__":
    main()
