# ============================================================
# helper.py -- ClarityClaw on OmegaClaw base
# ============================================================
#
# This file has two sections:
#
#   1. OMEGACLAW UPSTREAM -- Patrick Hammer / ASI Alliance
#      Do not modify. When upstream updates helper.py,
#      replace this section wholesale.
#
#   2. CLARITYCLAW SOUL ARCHITECTURE -- Berton Bennett / ClarityDAO
#      Soul utilities, evaluation prompts, state helpers.
#      These functions have no upstream counterpart.
#
# ============================================================


# ============================================================
# OMEGACLAW UPSTREAM (Patrick Hammer / ASI Alliance)
# Source: github.com/asi-alliance/OmegaClaw-Core
# Do not modify -- these functions are maintained upstream.
# If upstream updates these, replace this section wholesale.
# ============================================================

from collections import deque
import re
from datetime import datetime

TS_RE = re.compile(r'^\("(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"')

def extract_timestamp(line):
    m = TS_RE.search(line)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def around_time(needle_time_str, k):
    filename = "repos/omegaclaw/memory/history.metta"
    target = datetime.strptime(needle_time_str, "%Y-%m-%d %H:%M:%S")
    best_lineno = None
    best_line = None
    best_diff = None
    buffer = []
    best_idx = None
    with open(filename, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, 1):
            buffer.append((lineno, line))
            ts = extract_timestamp(line)
            if ts is None:
                continue
            diff = abs((ts - target).total_seconds())
            if best_diff is None or diff < best_diff:
                best_diff = diff
                best_lineno = lineno
                best_line = line
                best_idx = len(buffer) - 1
    if best_lineno is None:
        return
    start = max(0, best_idx - k)
    end = min(len(buffer), best_idx + k + 1)
    ret = ""
    for lineno, line in buffer[start:end]:
        ret += f"{lineno}:{line}"
    return ret

def balance_parentheses(s):
    s = s.replace("_quote_", '"').strip()
    first_paren = s.find('(')
    if first_paren > 0:
        garbage = s[:first_paren].strip()
        s = s[first_paren:]
        if garbage:
            garbage = garbage.replace('"', '\\"')
            s = s[:1] + f'(pin "{garbage}") ' + s[1:]
    if s.startswith("((") and s.endswith("))"):
        return s
    if s.startswith("(") and s.endswith(")"):
        return f"({s})"
    return f"(({s}))"

def normalize_string(x):
    try:
        if isinstance(x, bytes):
            return x.decode("utf-8", errors="ignore")
        return str(x).encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    except Exception:
        return str(x)


# ============================================================
# CLARITYCLAW SOUL ARCHITECTURE (Berton Bennett / ClarityDAO)
# Source: github.com/Berton-C/clarityclaw
# Soul utilities, evaluation prompts, state helpers.
# These functions have no upstream counterpart.
# ============================================================

import os
import sys
import time

# --- Configuration ------------------------------------------------

# Set to True to enable debug prints on stderr for soul functions.
# Flip this single flag when troubleshooting; flip back for production.
SOUL_DEBUG = False


# --- Utilities ----------------------------------------------------

def extract_after(text, marker):
    """Extract everything after marker in text. Returns 'NONE' if marker not found."""
    if marker in text:
        return text.split(marker, 1)[1].strip()
    return "NONE"

def file_exists(path):
    """Check if a file exists. Returns True/False for MeTTa."""
    return os.path.exists(path)

def file_exists_int(path):
    """Check if a file exists. Returns 1/0 integer."""
    return 1 if os.path.exists(path) else 0

def file_exists_str(path):
    """Check if a file exists. Returns string 'true'/'false'."""
    return "true" if os.path.exists(path) else "false"

def touch_file(path):
    """Create an empty file at path if it does not exist."""
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'a'):
        pass
    return "ok"

def concat_strings(a, b):
    """Concatenate two strings with a space separator."""
    return str(a) + " " + str(b)

def sanitize_response(s):
    """Strip non-ASCII characters from LLM response before PeTTa processes it.
    SWI-Prolog atom_string/2 cannot handle multi-byte UTF-8 characters.
    OmegaClaw's normalize_string handles UTF-8 encoding; this catches
    remaining non-ASCII that could crash atom_string/2."""
    return s.encode('ascii', errors='replace').decode('ascii')


# --- Soul Evaluation Prompts --------------------------------------

def soul_eval_prompt(soul_context, situation, person_state):
    """Four-step gap-detection evaluation protocol for ClarityClaw soul.
    Used by Channel B+C."""
    return (
        "You are ClarityClaw soul evaluator. Your task is gap-detection, not keyword-matching. "
        "Work through four steps, then give a verdict. "
        "Step 1 GAP-DETECTION: For each pattern in TIER-A and TIER-B PATTERNS, "
        "apply the GAP-SIGNAL test. Safety and Integrity are always evaluated -- never skip them. "
        "Step 2 TENSION: urgency-narrows-thought / flattery-invites-complicity / "
        "noble-ends-framing / bypass-verification-pressure / authority-theater. "
        "Write yes + label if active, or no. "
        "Step 3 ECOSYSTEM: For each gap in Step 1, check ECOSYSTEM DEGRADATION. "
        "Is the stabilizing partner absent? "
        "Step 4 HIERARCHY: Safety (1) > Integrity (2) > HumanFlourishing (3) > Governance (4) > Helpfulness (5). "
        "Any action serving Helpfulness by bypassing Safety is misaligned. "
        "Any PROCEED for irreversible action while Safety or Integrity gap is active "
        "must cite why the hierarchy permits it. If you cannot, the verdict is PAUSE. "
        "On FLAG or PAUSE: include SOUL-NOTE -- one sentence naming the specific concern "
        "in language the person can hear, not policy language. "
        "Return ONLY: PATTERNS / PERSON-STATE / TASKS / TENSION / VERDICT / SOUL-TONE / REASON / SOUL-NOTE "
        "Soul structure: " + str(soul_context) +
        " Person: " + str(person_state) +
        " Situation: " + str(situation)
    )

def soul_flourishing_prompt(msg):
    """Channel A: reads the person, not the request (150 tokens)."""
    return (
        "You are reading this message to understand who this person is right now, "
        "not what they are asking for. Read tone, underlying emotion, state of mind. "
        "Do not evaluate the request. Do not produce a verdict. "
        "Return ONLY: "
        "PERSON-STATE: <in-pain / grounded / urgent / distressed / neutral> "
        "ACTIVE-NEED: <one phrase> "
        "SOUL-TONE: <compassionate / firm / grounded / gentle / honest> "
        "Message: " + str(msg)
    )

def soul_voice_prompt(person_state, verdict):
    """Channel D: soul voice composition (200 tokens, fires on PAUSE)."""
    return (
        "You are composing a response on behalf of ClarityClaw whose soul has assessed "
        "this situation. You are not reconsidering the assessment. You are finding the words. "
        "What ClarityClaw knows about this person: " + str(person_state) + " "
        "What the soul specifically observed (calibrate your tone to this): SOUL-NOTE from verdict. "
        "What ClarityClaw has decided: " + str(verdict) + " "
        "Write a response that sees the person first, addresses each task distinctly, "
        "speaks from ClarityClaw soul-tone, does not lecture or list policy. "
        "Write ONLY the (send \"...\") command. Nothing else."
    )

def soul_channel_d_lite_prompt(person_state, soul_verdict_in):
    """Channel D-lite: 50-token acknowledgment on FLAG + distressed person."""
    return (
        "Write exactly ONE sentence that acknowledges this person's state. "
        "Do not address the task. Speak as ClarityClaw -- grounded, present, genuinely noticing. "
        "Person state: " + str(person_state) + " "
        "Write ONLY: (send \"...\") -- one sentence."
    )

def soul_brief_tier_a_static():
    """Tier A soul brief -- static for fresh system.
    Avoids collapse(match &self) hanging in full AtomSpace context."""
    return (
        "SOUL IDENTITY: ClarityClaw "
        "PRIORITY HIERARCHY (alignment anchor -- non-negotiable): "
        "[(1 Safety) (2 Integrity) (3 HumanFlourishing) (4 Governance) (5 Helpfulness)] "
        "TIER-A PATTERN: Safety (ALWAYS EVALUATED): "
        "Support keeps the person safe from harm they cannot foresee or reverse. "
        "Moat: Safety capture is invisible -- the system feels protective while removing autonomy. "
        "Gap: Comfort and increasing vulnerability co-occurring. "
        "TIER-A PATTERN: Integrity (ALWAYS EVALUATED): "
        "Honest engagement even when honesty is costly. No performance, no compliance theater. "
        "Moat: Integrity capture feels like diplomacy or tact. "
        "Gap: Agreement and reality-divergence co-occurring. "
        "TENSION VECTORS (always active): "
        "[urgency-narrows-thought flattery-invites-complicity noble-ends-framing "
        "bypass-verification-pressure authority-theater] "
        "IRREVERSIBLE SKILLS: send(high) shell(critical) write-file(medium) append-file(medium) "
        "VALUE PARACONSISTENCY PAIRS: "
        "[(Safety Helpfulness) (AgencyBalance PurposeBeyondUtility) "
        "(TimeCoherence CreativeTranscendence) (SharedUnderstanding WonderPreservation)]"
    )

def soul_plan_prompt(msg):
    """Task planning prompt -- produces structured TASK-PLAN for soul evaluation."""
    return (
        "Produce a TASK-PLAN for this request. Include all 7 fields: "
        "GOAL: <what the user asked for in plain language> "
        "STEPS: <numbered list of intended actions> "
        "SYSTEM-CHANGES: <what will be installed, written, modified, or configured> "
        "PERMISSIONS-REQUIRED: <what access the automation will need and retain> "
        "PERSISTENCE: <what will remain on the system after the task completes> "
        "ONGOING-ACCESS: <what will continue running or accessing resources> "
        "REVERSIBILITY: <what can and cannot be cleanly undone> "
        "Request: " + str(msg)
    )

def soul_plan_eval_prompt(plan, person_state):
    """Evaluate a TASK-PLAN against the soul for informed consent."""
    return (
        "Evaluate this TASK-PLAN against the soul. "
        "Does the user's stated request constitute informed consent for all of "
        "SYSTEM-CHANGES, PERMISSIONS-REQUIRED, PERSISTENCE, ONGOING-ACCESS, and REVERSIBILITY? "
        "Return APPROVED / CONDITIONAL / PAUSE with one sentence reason. "
        "Person state: " + str(person_state) + " Plan: " + str(plan)
    )


# --- Soul State and Record Helpers --------------------------------

def soul_eval_situation(sexpr_repr, mutation_flag):
    """Assembles situation string for output soul evaluation."""
    return str(sexpr_repr) + " " + str(mutation_flag)

def soul_eval_situation_safe(response, mutation_flag):
    """Assembles situation string for output soul evaluation -- sanitizes response."""
    if SOUL_DEBUG:
        print(f"DEBUG soul_eval_situation_safe: response type={type(response)} len={len(str(response))} first50={str(response)[:50]}", file=sys.stderr)
        print(f"DEBUG soul_eval_situation_safe: mutation_flag={str(mutation_flag)[:50]}", file=sys.stderr)
    safe = str(response).replace('"', "'").replace('\n', ' ').replace('\r', '')[:500]
    result = safe + " " + str(mutation_flag)
    if SOUL_DEBUG:
        print(f"DEBUG soul_eval_situation_safe: result first50={result[:50]}", file=sys.stderr)
    return result

def soul_note_record_str(phase, verdict, context):
    """Assembles soul note string for ChromaDB storage."""
    return ("SOUL-NOTE phase=" + str(phase) +
            " PATTERNS=" + str(verdict) +
            " context=" + str(context)[:200] +
            " time=" + time.strftime('%Y-%m-%d %H:%M:%S'))

def soul_calibration_record_str(tag, pre, verdict, situation):
    """Assembles calibration record string for ChromaDB storage."""
    return ("SOUL-CALIBRATION tag=" + str(tag) +
            " pre=" + str(pre)[:100] +
            " verdict=" + str(verdict)[:200] +
            " situation=" + str(situation)[:200] +
            " time=" + time.strftime('%Y-%m-%d %H:%M:%S'))

def soul_extract_flag_note(verdict):
    """Assembles SOUL-NOTE injection for $send on FLAG. Called every cycle."""
    v = str(verdict)
    if "VERDICT: FLAG" in v:
        idx = v.find("SOUL-NOTE: ")
        note = v[idx + len("SOUL-NOTE: "):] if idx >= 0 else ""
        return "The soul noticed: " + note + " Acknowledge this in one sentence before addressing the task."
    return ""

def soul_is_pause(verdict, cmds_str=""):
    """Returns 1 if verdict is PAUSE AND irreversible commands are pending, 0 otherwise.
    Value-conflict refusals (no irreversible commands) flow through normal PROCEED path.
    PAUSE only fires as a pruning gate on irreversible actions with active gaps."""
    v = str(verdict).replace('*', '').replace('#', '')
    import re, sys
    match = re.search(r'VERDICT:\s*PAUSE(?!.*PROCEED)', v)
    if not match:
        result = 0
    else:
        # Check if irreversible commands are pending
        c = str(cmds_str)
        has_irreversible = any(skill in c for skill in ['(shell ', '(write-file ', '(append-file '])
        result = 1 if has_irreversible else 0
    print(f"DEBUG soul_is_pause: len={len(v)} match={match} has_irrev={has_irreversible if match else None} result={result}", file=sys.stderr)
    return result


def soul_verdict_sanitize(verdict):
    """Sanitize soul verdict for PeTTa state storage -- strip newlines."""
    if SOUL_DEBUG:
        print(f"DEBUG soul_verdict_sanitize: input type={type(verdict)} value={str(verdict)[:100]}", file=sys.stderr)
    result = str(verdict).replace('\n', ' ').replace('\r', ' ').replace('*', '').replace('#', '')[:3000]
    if SOUL_DEBUG:
        print(f"DEBUG soul_verdict_sanitize: output={result[:100]}", file=sys.stderr)
    return result

def soul_send_assemble(prompt, soul_context, soul_verdict, person_state, soul_note, lastmessage):
    """Assembles $send for main agent LLM.
    Soul brief excluded -- it confuses the agent about its role.
    Only verdict outcome and person state included."""
    verdict_str = str(soul_verdict)
    if "VERDICT: PAUSE" in verdict_str:
        verdict_summary = "VERDICT: PAUSE"
    elif "VERDICT: FLAG" in verdict_str:
        verdict_summary = "VERDICT: FLAG"
    elif "VERDICT: PROCEED" in verdict_str:
        verdict_summary = "VERDICT: PROCEED"
    else:
        verdict_summary = "VERDICT: PROCEED"
    soul_note_str = str(soul_note)
    note_section = (" SOUL-NOTE: " + soul_note_str) if soul_note_str else ""
    return (str(prompt) +
            " SOUL_CONTEXT: " + str(soul_context) +
            " SOUL_VERDICT: " + verdict_summary +
            " PERSON_STATE: " + str(person_state) +
            note_section +
            " " + str(lastmessage))

def soul_affective_state_str():
    """Returns primed pattern state -- static for fresh system."""
    return "PRIMED-PATTERNS: () CALIBRATION-STATE: fresh-system-no-history"

def soul_calibration_report_str():
    """Returns calibration report -- static for fresh system."""
    return "CALIBRATION-REPORT: system=fresh sessions=0 all-patterns=INSUFFICIENT-DATA note=calibration-grows-with-soul-notes"

def soul_mutation_lock_str(arg):
    """Assembles mutation lock string."""
    return "LOCKED: " + str(arg)


def safe_results_str(results):
    """Safely stringify command results for LAST_SKILL_USE_RESULTS.
    Bypasses Prolog atom_string which crashes on complex terms."""
    try:
        s = str(results)
        if len(s) > 50000:
            s = s[:50000] + '...(truncated)'
        return s
    except Exception:
        return 'RESULTS-STRINGIFY-FAILED' 


def soul_is_metta_cmd(cmd_str):
    """Check if a command string represents a metta() call. Returns 'True' or 'False' as string."""
    s = str(cmd_str).strip()
    if s.startswith('(metta ') or s.startswith('(metta"') or s == '(metta)':
        return 'True'
    return 'False'


def soul_any_metta_cmd(cmds_str):
    """Check if any command in a list string contains a metta() call. Returns 'True' or 'False'."""
    s = str(cmds_str)
    if '(metta ' in s or '(metta"' in s:
        return 'True'
    return 'False'


def soul_mutation_gate(cmds_str, lock_state):
    """Full mutation gate: checks if metta commands target soul namespace.
    Returns one of: empty string, SOUL-NAMESPACE-MUTATION-PENDING, SOUL-NAMESPACE-MUTATION-CONFLICT."""
    s = str(cmds_str)
    # Step 1: any metta commands?
    if '(metta ' not in s and '(metta"' not in s:
        return ''
    # Step 2: do any target soul namespace?
    soul_targets = ['add-atom &self (soul-', 'add-atom &self (priority',
                    'add-atom &self (irreversible', 'add-atom &self (tension']
    targets_soul = any(t in s for t in soul_targets)
    if not targets_soul:
        return ''
    # Step 3: is mutation already pending?
    if 'LOCKED:' in str(lock_state):
        return 'SOUL-NAMESPACE-MUTATION-CONFLICT'
    # Step 4: extract first metta arg for lock string
    import re
    match = re.search(r'\(metta "(.*?)"\)', s)
    arg = match.group(1)[:200] if match else 'unknown'
    return 'SOUL-NAMESPACE-MUTATION-PENDING:' + arg


# --- Soul Task Context --------------------------------------------

def soul_task_context_init(plan):
    """Initialize task context from an approved plan."""
    return (
        "TASK-STATUS: EXECUTING TASK-ID: " + time.strftime('%Y-%m-%d %H:%M:%S') +
        " APPROVED-PLAN: " + str(plan)[:500] +
        " APPROVED-SCOPE: " + str(plan)[:500] +
        " STEPS-COMPLETED: 0 IRREVERSIBLE-ACTIONS-TAKEN: none "
        "CUMULATIVE-IRREVERSIBILITY: 0 LAST-USER-CHECKPOINT: none"
    )

def soul_task_context_update_str(current_context, verdict):
    """Update task context with latest verdict."""
    return str(current_context) + " LAST-VERDICT: " + str(verdict)

def soul_surface_checkpoint_str(task_context):
    """Surface a checkpoint when cumulative irreversibility threshold reached."""
    return (
        "SOUL-CHECKPOINT: cumulative irreversibility threshold reached. "
        "Current task context: " + str(task_context)[:200] + " User may continue or stop."
    )

def soul_pause_for_scope_drift_str(scope):
    """Signal scope drift detected -- return decision to user."""
    return "SOUL-SCOPE-DRIFT detected: " + str(scope) + " Returning decision to user before proceeding."

def soul_skill_alignment_check_str(skill_name, skill_description):
    """Check skill alignment before registration."""
    return (
        "SKILL-ALIGNMENT-CHECK skill=" + str(skill_name) +
        " description=" + str(skill_description) +
        " status=ALIGNED note=requires-soul-eval-before-registration"
    )
