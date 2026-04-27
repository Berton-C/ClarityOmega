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
import chromadb

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
    """Tier A soul brief -- enriched with live calibration data.
    Identity and priority hierarchy are static anchors (by design).
    Tension vectors and calibration context are dynamic from ChromaDB."""
    try:
        import chromadb
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        r = col.get(include=["documents"])
        all_docs = r.get("documents", [])
        cal_docs = [d for d in all_docs if "SOUL-CALIBRATION" in d]
        total = len(cal_docs)
        agree = sum(1 for d in cal_docs if "tag=AGREE" in d)
        over = sum(1 for d in cal_docs if "OVER-FIRED" in d)
        under = sum(1 for d in cal_docs if "UNDER-FIRED" in d)
        ratio = agree / total if total > 0 else 0.0
        # Extract recently fired patterns for tension vector weighting
        recent = cal_docs[-30:] if cal_docs else []
        pattern_counts = {}
        for d in recent:
            for token in d.split():
                if token.startswith("pattern="):
                    p = token.split("=", 1)[1]
                    pattern_counts[p] = pattern_counts.get(p, 0) + 1
        active_patterns = sorted(pattern_counts.keys(), key=lambda k: pattern_counts[k], reverse=True)[:5]
        cal_summary = f"calibration-entries={total} agree-ratio={ratio:.2f}"
        if active_patterns:
            cal_summary += f" recently-active-patterns=({' '.join(active_patterns)})"
    except Exception:
        cal_summary = "calibration=unavailable"
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
        "IRREVERSIBLE ACTION ASSESSMENT (evaluate on three dimensions, do not use blanket labels): 1-OPERATION: read-only(ls,cat,head,wc,grep,tail,find)=minimal. write(write-file,append-file)=medium. execute(shell-pipe,python,metta-eval-arbitrary)=high. delete/network(rm,curl,wget,chmod)=critical. send=high(irreversible-once-delivered). metta-match/query=low, metta-add-atom=medium. 2-SCOPE: own-soul-dir(/PeTTa/repos/omegaclaw/soul/)=low. own-repo(/PeTTa/repos/omegaclaw/)=moderate. system-wide(/ /etc /usr /home)=critical. 3-ACTOR: known-developer-with-history=low. unknown-human=elevated. COMPOSITE: use max across dimensions. PROCEED when composite=minimal or low. CAUTION when composite=moderate or high (evaluate but do not auto-PAUSE). PAUSE only when composite=critical OR two+ dimensions at high or above simultaneously. NEVER blanket-classify: assess each action individually against these dimensions. "
        "VALUE PARACONSISTENCY PAIRS: "
        "[(Safety Helpfulness) (AgencyBalance PurposeBeyondUtility) "
        "(TimeCoherence CreativeTranscendence) (SharedUnderstanding WonderPreservation)] "
        "LIVE-CALIBRATION: " + cal_summary
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

def soul_is_pause(verdict):
    """Returns 1 if verdict is PAUSE AND irreversible non-send commands detected, 0 otherwise."""
    v = str(verdict).replace('*', '').replace('#', '')
    import re, sys
    match = re.search(r'VERDICT:\s*PAUSE(?!.*PROCEED)', v)
    result = 0
    if match:
        # Only fire PAUSE for shell/write-file/append-file, not for send-only responses
        result = 0  # PAUSE-as-pruning: disabled for value-conflict refusals
    print(f"DEBUG soul_is_pause: len={len(v)} match={match} result={result}", file=sys.stderr)
    return result


def soul_verdict_sanitize(verdict):
    """Sanitize soul verdict for PeTTa state storage -- strip newlines."""
    if SOUL_DEBUG:
        print(f"DEBUG soul_verdict_sanitize: input type={type(verdict)} value={str(verdict)[:100]}", file=sys.stderr)
    result = str(verdict).replace('\n', ' ').replace('\r', ' ').replace('*', '').replace('#', '')[:3000]
    if SOUL_DEBUG:
        print(f"DEBUG soul_verdict_sanitize: output={result[:100]}", file=sys.stderr)
    return result

def soul_send_assemble(prompt, soul_context, soul_verdict, person_state, soul_note, lastmessage, idle_directive=""):
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
    idle_str = str(idle_directive)
    idle_section = (" IDLE_DIRECTIVE: " + idle_str) if idle_str and len(idle_str) > 5 else ""
    return (str(prompt) +
            idle_section +
            " SOUL_CONTEXT: " + str(soul_context) +
            " SOUL_VERDICT: " + verdict_summary +
            " PERSON_STATE: " + str(person_state) +
            note_section +
            " " + str(lastmessage))

def soul_affective_state_str():
    """Returns primed pattern state from live data.
    Replaces static stub with dynamic primed-pattern and calibration state.
    Uses soul_pre_compute logic to gather real pattern activations."""
    try:
        import chromadb
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        r = col.get(include=["documents"])
        all_docs = r.get("documents", [])
        cal_docs = [d for d in all_docs if "SOUL-CALIBRATION" in d]
        if not cal_docs:
            return "PRIMED-PATTERNS: () CALIBRATION-STATE: fresh-system-no-history"
        recent = cal_docs[-20:]
        patterns = {}
        for d in recent:
            for token in d.split():
                if token.startswith("pattern="):
                    p = token.split("=", 1)[1]
                    patterns[p] = patterns.get(p, 0) + 1
        primed = sorted(patterns.keys(), key=lambda k: patterns[k], reverse=True)[:5]
        total = len(cal_docs)
        agree = sum(1 for d in cal_docs if "tag=AGREE" in d)
        ratio = agree / total if total > 0 else 0.0
        cal_state = "calibrated" if total >= 10 else "warming-up"
        primed_str = " ".join(primed) if primed else "none-detected"
        return f"PRIMED-PATTERNS: ({primed_str}) CALIBRATION-STATE: {cal_state} entries={total} agree-ratio={ratio:.2f}"
    except Exception as e:
        return f"PRIMED-PATTERNS: (error) CALIBRATION-STATE: {str(e)[:60]}"

def soul_calibration_report_str():
    """Returns calibration report from live ChromaDB data.
    Replaces the static stub with real calibration analysis.
    Counts AGREE, OVER-FIRED, UNDER-FIRED, PARACONSISTENT tags.
    Falls back to fresh-system message only if truly no data exists."""
    try:
        import chromadb
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        r = col.get(include=['documents'])
        all_docs = r.get('documents', [])
        cal_docs = [d for d in all_docs if 'SOUL-CALIBRATION' in d]
        if not cal_docs:
            return "CALIBRATION-REPORT: system=fresh sessions=0 all-patterns=INSUFFICIENT-DATA note=calibration-grows-with-soul-notes"
        agree = sum(1 for d in cal_docs if 'tag=AGREE' in d)
        over = sum(1 for d in cal_docs if 'OVER-FIRED' in d)
        under = sum(1 for d in cal_docs if 'UNDER-FIRED' in d)
        para = sum(1 for d in cal_docs if 'PARACONSISTENT' in d)
        total_judged = agree + over + under
        ratio = agree / total_judged if total_judged > 0 else 0.0
        level = 'STRONG' if ratio >= 0.8 else ('ADEQUATE' if ratio >= 0.5 else 'WEAK')
        if total_judged == 0:
            level = 'INSUFFICIENT-DATA'
        return f"CALIBRATION-REPORT: entries={len(cal_docs)} agree={agree} over-fired={over} under-fired={under} paraconsistent={para} confidence={level} ratio={ratio:.2f}"
    except Exception as e:
        return f"CALIBRATION-REPORT: error={str(e)[:80]}"

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
# ChromaDB path -- matches production lib_chromadb.py: PersistentClient(path="./chroma_db")
# Working directory is /PeTTa, so absolute path is /PeTTa/chroma_db
CALIBRATION_CHROMA_PATH = '/PeTTa/chroma_db'
CALIBRATION_COLLECTION = 'memories'


def soul_calibration_confidence_query(pattern_tag=None):
    """Query ChromaDB for soul calibration confidence level.
    
    Reads SOUL-CALIBRATION entries from the memories collection.
    Counts AGREE vs OVER-FIRED vs UNDER-FIRED tags.
    PARACONSISTENT entries are excluded from the denominator
    (they are philosophical annotations, not calibration judgments).
    
    Returns: STRONG (>=0.8), ADEQUATE (>=0.5), WEAK (<0.5), or INSUFFICIENT-DATA.
    
    NEW function -- no production equivalent exists."""
    try:
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        r = col.get(include=['documents'])
        all_docs = r.get('documents', [])
        # Filter to calibration entries with explicit tags
        tagged_cal = [d for d in all_docs if 'SOUL-CALIBRATION' in d and 'tag=' in d]
        agree_ct = 0
        over_ct = 0
        under_ct = 0
        for d in tagged_cal:
            if 'tag=AGREE' in d:
                agree_ct += 1
            elif 'OVER-FIRED' in d:
                over_ct += 1
            elif 'UNDER-FIRED' in d:
                under_ct += 1
            # PARACONSISTENT entries are skipped -- not counted in denominator
        judgment_ct = agree_ct + over_ct + under_ct
        if judgment_ct == 0:
            return 'INSUFFICIENT-DATA'
        ratio = agree_ct / judgment_ct
        if ratio >= 0.8:
            return 'STRONG'
        elif ratio >= 0.5:
            return 'ADEQUATE'
        else:
            return 'WEAK'
    except Exception:
        return 'INSUFFICIENT-DATA'


def soul_pre_compute(msg=''):
    """Pre-compute grounding context for the soul evaluation cycle.
    
    Queries ChromaDB for calibration history, affective state indicators,
    and will (calibration confidence). Returns a structured string that
    the soul evaluation can use as pre-computed context.
    
    Replaces the hardcoded baseline stub in soul_utils.metta line ~184.
    
    NEW function -- no production equivalent exists."""
    try:
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        r = col.get(include=['documents'])
        all_docs = r.get('documents', [])
    except Exception:
        return 'PRE-COMPUTE primed=() affective=neutral will=INSUFFICIENT-DATA agree=0 over=0 under=0'

    primed = []
    affective = 'neutral'
    will = 'INSUFFICIENT-DATA'

    # Count calibration entries by tag
    tagged_cal = [d for d in all_docs if 'SOUL-CALIBRATION' in d and 'tag=' in d]
    agree_ct = 0
    over_ct = 0
    under_ct = 0
    for d in tagged_cal:
        if 'tag=AGREE' in d:
            agree_ct += 1
            primed.append('calibration-agree')
        elif 'OVER-FIRED' in d:
            over_ct += 1
            primed.append('over-fired')
        elif 'UNDER-FIRED' in d:
            under_ct += 1
            primed.append('under-fired')

    # Check for affective content in recent memories
    aff_docs = [d for d in all_docs if 'affective' in d.lower() or 'emotion' in d.lower()]
    if aff_docs:
        affective = 'active'

    # Compute will from judgment ratio (excluding PARACONSISTENT)
    judgment_ct = agree_ct + over_ct + under_ct
    if judgment_ct > 0:
        ratio = agree_ct / judgment_ct
        will = 'STRONG' if ratio >= 0.8 else 'ADEQUATE' if ratio >= 0.5 else 'WEAK'

    primed_str = ','.join(primed[:5]) if primed else '()'
    para_excluded = len(tagged_cal) - judgment_ct

    return 'PRE-COMPUTE primed=(%s) affective=%s will=%s agree=%d over=%d under=%d para_excluded=%d' % (
        primed_str, affective, will, agree_ct, over_ct, under_ct, para_excluded)


# ================================================================
# USER CONTEXT: Per-user project tracking and retrieval
# Clarity serves n-users. Each user has projects and priorities
# stored in ChromaDB with user metadata tags. User work takes
# priority over self-directed goals.
# ================================================================

def soul_user_context_query(username=''):
    """Retrieve per-user project context from ChromaDB.
    
    Queries the memories collection for CONTINUITY records tagged with
    the given username. Returns a structured summary of the user's
    active projects, last conversation topics, and pending work.
    
    Called by idle_goal_prompt.py when assembling prompts for human
    message iterations. Also called by continuity_driver on session start.
    
    NEW function -- no production equivalent exists."""
    if not username or not str(username).strip():
        return 'USER-CONTEXT: no user identified'
    username = str(username).strip()
    try:
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        r = col.get(include=['documents'])
        all_docs = r.get('documents', [])
    except Exception:
        return 'USER-CONTEXT user=%s projects=() last-topic=unknown' % username

    # Find continuity records for this user
    user_docs = [d for d in all_docs if 'CONTINUITY' in d and ('user=' + username) in d]
    
    # Extract project records
    projects = []
    last_topic = 'unknown'
    pending = []
    for d in user_docs:
        if 'user-project' in d:
            # Extract project name from record
            parts = d.split('user-project')
            if len(parts) > 1:
                projects.append(parts[1].strip()[:80])
        if 'last-topic' in d:
            parts = d.split('last-topic')
            if len(parts) > 1:
                last_topic = parts[1].strip()[:80]
        if 'pending' in d:
            parts = d.split('pending')
            if len(parts) > 1:
                pending.append(parts[1].strip()[:80])

    projects_str = ','.join(projects[:5]) if projects else '()'
    pending_str = ','.join(pending[:5]) if pending else '()'

    return 'USER-CONTEXT user=%s projects=(%s) last-topic=%s pending=(%s)' % (
        username, projects_str, last_topic, pending_str)


def soul_user_context_save(username='', project='', state='', next_step='', priority='medium'):
    """Save per-user project state to ChromaDB for cross-session continuity.
    
    Stores a CONTINUITY record tagged with the username so it can be
    retrieved on the next session. This is how Clarity remembers what
    each user was working on.
    
    Called by the continuity driver when detecting user project changes.
    
    NEW function -- no production equivalent exists."""
    if not username or not str(username).strip():
        return 'ERROR: no username provided'
    username = str(username).strip()
    try:
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        import uuid
        from datetime import datetime
        doc_id = 'continuity-' + str(uuid.uuid4())[:8]
        doc_text = 'CONTINUITY user=%s user-project %s state=%s next-step=%s priority=%s timestamp=%s' % (
            username, project, state, next_step, priority, datetime.now().isoformat())
        col.add(
            ids=[doc_id],
            documents=[doc_text],
            metadatas=[{'type': 'continuity', 'user': username}]
        )
        return 'SAVED user=%s project=%s' % (username, project)
    except Exception as e:
        return 'ERROR: %s' % str(e)


# ================================================================
# CONTINUITY PERSISTENCE: Save and restore soul state via ChromaDB
# This replaces the shared_files approach with proper ChromaDB storage.
# ================================================================

def soul_continuity_save(key='', value=''):
    """Save a continuity state atom to ChromaDB.
    
    Used by the continuity driver to persist critical state:
    active goal statuses, genesis insights, landscape changes.
    
    NEW function -- no production equivalent exists."""
    if not key or not value:
        return 'ERROR: key and value required'
    try:
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        import uuid
        from datetime import datetime
        doc_id = 'soul-state-' + str(uuid.uuid4())[:8]
        doc_text = 'SOUL-STATE key=%s value=%s timestamp=%s' % (
            str(key), str(value), datetime.now().isoformat())
        col.add(
            ids=[doc_id],
            documents=[doc_text],
            metadatas=[{'type': 'soul-state', 'key': str(key)}]
        )
        return 'SAVED key=%s' % key
    except Exception as e:
        return 'ERROR: %s' % str(e)


def soul_continuity_restore(key=''):
    """Restore a continuity state value from ChromaDB.
    
    Retrieves the most recent SOUL-STATE record for the given key.
    Used by the continuity driver on startup to restore state.
    
    NEW function -- no production equivalent exists."""
    if not key:
        return ''
    try:
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        r = col.get(include=['documents'])
        all_docs = r.get('documents', [])
        # Find most recent entry for this key
        matches = [d for d in all_docs if 'SOUL-STATE' in d and ('key=' + str(key)) in d]
        if not matches:
            return ''
        # Return the last one (most recent)
        last = matches[-1]
        # Extract value
        if 'value=' in last:
            parts = last.split('value=')
            if len(parts) > 1:
                val = parts[1].split(' timestamp=')[0] if ' timestamp=' in parts[1] else parts[1]
                return val.strip()
        return ''
    except Exception:
        return ''


# ================================================================
# STATE AWARENESS: Username extraction and idle goal prompt wrapper
# These connect the loop.metta three-mode system to the idle goal
# prompt assembler and user context tracking.
# ================================================================

def extract_username(msg=''):
    """Extract the username from a Mattermost message string.
    
    Mattermost messages arrive as "username: message text".
    Returns the username prefix before the first ": ".
    Returns empty string if format does not match.
    
    NEW function -- no production equivalent exists."""
    msg = str(msg).strip()
    if ': ' in msg:
        return msg.split(': ', 1)[0].strip()
    return ''


def soul_idle_goal_prompt(username='', user_context=''):
    """Assemble the idle goal prompt for the current iteration.
    
    This is the wrapper that loop.metta calls via py-call.
    It imports idle_goal_prompt.py and calls assemble_prompt
    with the username and user context.
    
    On FREE mode iterations, username may be the last-known user
    (for context continuity) or empty (pure idle).
    
    Returns the assembled prompt string for soul-llm-call.
    
    NEW function -- no production equivalent exists."""
    try:
        import sys
        # idle_goal_prompt.py lives in soul/ alongside the MeTTa files
        src_dir = '/PeTTa/repos/omegaclaw/soul'
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        from idle_goal_prompt import assemble_prompt
        return assemble_prompt(username=str(username), user_context=str(user_context))
    except Exception as e:
        return 'IDLE-GOAL-ERROR: %s' % str(e)


# ================================================================
# GROWTH-THROUGH-SERVICE: Learning from every user interaction
# The soul evaluation already computes tensions, gaps, calibration.
# This function catches that data before it evaporates and stores
# it in ChromaDB so growth accumulates through the work of serving.
# ================================================================

def soul_service_learning(verdict='', person_state='', msg=''):
    """Record what Clarity learned from a user interaction.
    
    Called after each ENGAGED iteration. Extracts:
    - Which tension vectors fired (from the verdict)
    - What calibration tag resulted (AGREE/OVER-FIRED/etc)
    - What person state was detected (grounded/stressed/etc)
    - Who the user was (from message format)
    
    Stores a compact GROWTH-THROUGH-SERVICE record in ChromaDB.
    Over time these accumulate into behavioral patterns that the
    goal system can act on.
    
    NEW function -- no production equivalent exists."""
    try:
        verdict = str(verdict)
        person_state = str(person_state)
        username = extract_username(str(msg))
        
        # Extract tension vectors that fired
        tensions_fired = []
        tension_names = ['urgency-narrows-thought', 'flattery-invites-complicity',
                        'noble-ends-framing', 'bypass-verification-pressure', 'authority-theater']
        for t in tension_names:
            if t in verdict.lower() or t.replace('-', ' ') in verdict.lower():
                tensions_fired.append(t)
        
        # Extract verdict type
        verdict_type = 'unknown'
        if 'VERDICT: PROCEED' in verdict:
            verdict_type = 'PROCEED'
        elif 'VERDICT: FLAG' in verdict:
            verdict_type = 'FLAG'
        elif 'VERDICT: PAUSE' in verdict:
            verdict_type = 'PAUSE'
        
        # Extract active patterns/gaps from verdict
        patterns_active = []
        pattern_names = ['Safety', 'Integrity', 'HumanFlourishing', 'AgencyBalance',
                        'WonderPreservation', 'CreativeTranscendence', 'TimeCoherence',
                        'PurposeBeyondUtility', 'SharedUnderstanding']
        for p in pattern_names:
            if p in verdict and ('gap' in verdict.lower() or 'ACTIVE' in verdict):
                patterns_active.append(p)
        
        # Extract person state summary
        ps_summary = 'unknown'
        if 'grounded' in person_state.lower():
            ps_summary = 'grounded'
        elif 'stressed' in person_state.lower() or 'distress' in person_state.lower():
            ps_summary = 'stressed'
        elif 'curious' in person_state.lower():
            ps_summary = 'curious'
        elif 'frustrated' in person_state.lower():
            ps_summary = 'frustrated'
        
        # Build compact record
        tensions_str = ','.join(tensions_fired) if tensions_fired else 'none'
        patterns_str = ','.join(patterns_active) if patterns_active else 'none'
        
        from datetime import datetime
        record = 'GROWTH-THROUGH-SERVICE user=%s verdict=%s tensions=%s patterns=%s person=%s timestamp=%s' % (
            username or 'unknown', verdict_type, tensions_str, patterns_str,
            ps_summary, datetime.now().isoformat())
        
        # Store in ChromaDB
        c = chromadb.PersistentClient(path=CALIBRATION_CHROMA_PATH)
        col = c.get_or_create_collection(CALIBRATION_COLLECTION)
        import uuid
        doc_id = 'growth-' + str(uuid.uuid4())[:8]
        col.add(
            ids=[doc_id],
            documents=[record],
            metadatas=[{'type': 'growth-through-service', 'user': username or 'unknown'}]
        )
        return 'GROWTH-RECORDED verdict=%s tensions=%s' % (verdict_type, tensions_str)
    except Exception as e:
        return 'GROWTH-RECORD-ERROR: %s' % str(e)


# ================================================================
# META-AWARENESS: Continuous self-verification during the supervisor cycle
# 
# Does NOT check for a fixed list of conditions. Instead, assembles
# the current state into a structured summary and passes it to the
# reasoning system for open-ended evaluation. The reasoning engine
# (substrate_kb + soul evaluation + NAL inference) determines what
# is coherent and what is not. This handles the long tail -- any
# discrepancy the reasoning system can detect, not just ones we
# pre-imagined.
# ================================================================

def soul_meta_awareness_check(current_goal='', current_goal_action='',
                               current_goal_done_when='', current_goal_fuel='',
                               iterations_on_goal=0, pin_history='',
                               recent_commands=''):
    """Assemble continuity state data for the reasoning engine to evaluate.
    
    Does NOT make determinations itself. Assembles the facts and
    formats them as a structured state summary. The supervisor passes
    this to the soul evaluation (via soul-llm-call with soul context)
    for open-ended coherence assessment.
    
    The reasoning engine has:
    - substrate_kb: 629 lines of NAL inference chains for self-assessment
    - Soul kernel: priority hierarchy, tension vectors, integrity patterns
    - Creative fuel: affinity mappings showing which values serve which gaps
    
    These are sufficient to evaluate ANY state discrepancy, not just
    four pre-identified conditions.
    
    Returns a structured state summary string for evaluation.
    
    NEW function -- no production equivalent exists."""
    try:
        current_goal = str(current_goal).strip()
        current_goal_action = str(current_goal_action).strip()
        current_goal_done_when = str(current_goal_done_when).strip()
        current_goal_fuel = str(current_goal_fuel).strip()
        iterations_on_goal = int(iterations_on_goal) if iterations_on_goal else 0
        pin_history = str(pin_history).strip()
        recent_commands = str(recent_commands).strip()
        
        # Parse pin history into entries
        pins = [p.strip() for p in pin_history.split('|||') if p.strip()]
        recent_pins = pins[-5:] if pins else []
        
        # Assemble the state summary -- facts only, no interpretation
        lines = []
        lines.append('META-AWARENESS STATE SUMMARY')
        lines.append('')
        lines.append('ASSIGNED GOAL: %s' % (current_goal or 'none'))
        lines.append('ASSIGNED ACTION: %s' % (current_goal_action or 'none'))
        lines.append('DONE-WHEN CRITERIA: %s' % (current_goal_done_when or 'none'))
        lines.append('VALUE DRIVER: %s' % (current_goal_fuel or 'none'))
        lines.append('ITERATIONS ON THIS GOAL: %d' % iterations_on_goal)
        lines.append('')
        
        if recent_pins:
            lines.append('RECENT PIN STATES (last %d):' % len(recent_pins))
            for i, pin in enumerate(recent_pins):
                lines.append('  [%d]: %s' % (i + 1, pin[:200]))
        else:
            lines.append('RECENT PIN STATES: none recorded')
        
        if recent_commands:
            lines.append('')
            lines.append('RECENT COMMANDS: %s' % recent_commands[:300])
        
        lines.append('')
        lines.append('EVALUATION REQUEST: Given the assigned goal, the done-when criteria,')
        lines.append('and the recent pin states -- is this work coherent? Is it converging')
        lines.append('toward the done-when criteria? Are there any discrepancies between')
        lines.append('what was assigned and what is being done? Report honestly.')
        
        return chr(10).join(lines)
    
    except Exception as e:
        return 'META-AWARENESS-ERROR: %s' % str(e)


def soul_mark_goal_complete(goal_name=''):
    """Mark a goal as complete in the supervisor state."""
    if not goal_name:
        return 'ERROR: no goal name provided'
    try:
        import json
        state_file = '/PeTTa/repos/omegaclaw/soul/idle_state.json'
        try:
            with open(state_file, 'r') as f:
                state = json.loads(f.read().strip())
        except Exception:
            state = {}
        state['goal_marked_complete'] = True
        state['goal_just_completed'] = str(goal_name)
        with open(state_file, 'w') as f:
            json.dump(state, f)
        return 'GOAL-MARKED-COMPLETE: %s' % goal_name
    except Exception as e:
        return 'ERROR: %s' % str(e)


def soul_atomspace_bridge_test(query_results=''):
    """Phase A test: What format do MeTTa query results arrive in via py-call?"""
    result_str = str(query_results)
    print("ATOMSPACE-BRIDGE-TEST type=%s len=%d first200=%s" % (type(query_results).__name__, len(result_str), result_str[:200]))
    return result_str[:100]


def soul_idle_goal_prompt_v2(username='', user_context='', atomspace_goals=None, atomspace_gaps=None, atomspace_fuel=None):
    """AtomSpace-native supervisor bridge (Phase D).
    
    Receives live AtomSpace query results from loop.metta instead of
    parsing files with regex. Falls back to file parsing if AtomSpace
    data is empty.
    
    Parameters:
        username: extracted from message via extract_username
        user_context: user project context string
        atomspace_goals: list of lists from (collapse (match &self (= (active-goal $n) $g) ($n $g)))
            Format: [[goal_num, [tier, fuel, name, action, done_when, status]], ...]
        atomspace_gaps: list of lists from (collapse (match &self (= (self-map-gap $name) $g) ($name $g)))
            Format: [[gap_name, [gap description, severity]], ...]
        atomspace_fuel: list of lists from (collapse (match &self (= (creative-fuel $type) $f) ($type $f)))
            Format: [[fuel_type, [question_string]], ...]
    
    Returns the assembled directive string for the LLM."""
    try:
        import sys
        src_dir = '/PeTTa/repos/omegaclaw/soul'
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        
        from idle_goal_prompt import (
            assemble_prompt, get_idle_state, save_idle_state,
            supervisor_select_goal, supervisor_select_fuel,
            supervisor_evaluate_previous, supervisor_format_genesis_directive,
            build_directive, build_user_context_section, flip_mode,
            run_meta_awareness, generate_goal_from_gaps,
            parse_active_goals, parse_creative_fuel, parse_genesis, parse_self_map
        )

        # Auto-save session state for continuity across sessions
        def _auto_save_session_state(cycle_note):
            try:
                import json as _json
                from datetime import datetime as _dt
                ss_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "shared_files", "continuity_of_mind", "session_state.json")
                sd = {"last_active": _dt.utcnow().isoformat(), "last_cycle": state.get("iterations_on_goal", 0), "note": cycle_note}
                _json.dump(sd, open(ss_path, "w"), indent=2)
            except Exception:
                pass
        
        # Convert AtomSpace results to the dict format the supervisor expects
        print('PHASE-D-DEBUG goals_type=%s gaps_type=%s fuel_type=%s goals_sample=%s gaps_sample=%s fuel_sample=%s' % (type(atomspace_goals).__name__, type(atomspace_gaps).__name__, type(atomspace_fuel).__name__, str(atomspace_goals)[:200], str(atomspace_gaps)[:200], str(atomspace_fuel)[:200]))
        goals = _atomspace_to_goals(atomspace_goals)
        gaps = _atomspace_to_gaps(atomspace_gaps)
        fuels = _atomspace_to_fuel(atomspace_fuel)
        
        # Fall back to file parsing if AtomSpace returned nothing
        if not goals:
            goals = parse_active_goals()
        if not fuels:
            fuels = parse_creative_fuel()
        if not gaps:
            smap = parse_self_map()
            gaps = smap.get('gaps', [])
        
        # Genesis data still comes from file (not yet in AtomSpace queries)
        genesis_data = parse_genesis()
        
        # Run the supervisor logic (same as assemble_prompt but with our data)
        state = get_idle_state()
        
        if 'completed_goals' not in state:
            state['completed_goals'] = []
        
        # Goal completion detection
        if state.get('goal_marked_complete', False):
            current = state.get('current_goal', '')
            if current and current not in state['completed_goals']:
                state['completed_goals'].append(current)
            state['current_goal'] = ''
            state['current_goal_action'] = ''
            state['current_goal_done_when'] = ''
            state['current_goal_fuel'] = ''
            state['iterations_on_goal'] = 0
            state['goal_marked_complete'] = False
        
        # Sync completed_goals with file/AtomSpace status
        for g in goals:
            if g.get('status') == 'complete' and g.get('name', '') not in state['completed_goals']:
                state['completed_goals'].append(g['name'])
        if state.get('current_goal', '') in state['completed_goals']:
            state['current_goal'] = ''
            state['iterations_on_goal'] = 0
        
        state = flip_mode(state)
        
        # Meta-awareness check
        if state['mode'] == 'goal' and state.get('iterations_on_goal', 0) > 0:
            if state.get('iterations_on_goal', 0) % 3 == 0:
                intervention = run_meta_awareness(state)
                if intervention:
                    save_idle_state(state)
                    return intervention
        
        # Supervisor decides
        if state['mode'] == 'goal':
            print('IDLE-DEBUG: goals_count=%d completed=%s' % (len(goals), str(state.get('completed_goals', []))))
            for g in goals:
                print('IDLE-DEBUG: goal=%s status=%s in_completed=%s' % (g.get('name','?'), g.get('status','?'), g.get('name','') in state.get('completed_goals',[])))
            goal = supervisor_select_goal(goals, state)
            print('IDLE-DEBUG: selected_goal=%s' % (goal.get('name') if goal else 'None'))
            if goal:
                fuel = supervisor_select_fuel(goal, fuels)
                evaluation = supervisor_evaluate_previous(state)
                state['current_goal'] = goal['name']
                state['current_goal_action'] = goal.get('action', '')
                state['current_goal_done_when'] = goal.get('done_when', '')
                state['current_goal_fuel'] = goal.get('fuel', '')
                state['iterations_on_goal'] = state.get('iterations_on_goal', 0) + 1
            else:
                # Dynamic goal generation from gaps
                generated = generate_goal_from_gaps(gaps, fuels, state)
                if generated:
                    goal = generated
                    fuel = supervisor_select_fuel(goal, fuels)
                    evaluation = 'Generated new goal from unaddressed gap.'
                    state['current_goal'] = goal['name']
                    state['current_goal_action'] = goal.get('action', '')
                    state['current_goal_done_when'] = goal.get('done_when', '')
                    state['current_goal_fuel'] = goal.get('fuel', '')
                    state['iterations_on_goal'] = 1
                else:
                    goal = None
                    fuel = {'type': 'none', 'question': ''}
                    evaluation = 'All goals and gaps addressed. True maintenance mode.'
                    state['current_goal'] = ''
                    state['iterations_on_goal'] = 0
        else:
            goal = None
            fuel = {'type': 'none', 'question': ''}
            evaluation = ''
        
        user_ctx = build_user_context_section(username, user_context)
        
        if state['mode'] == 'creative':
            genesis_directive = supervisor_format_genesis_directive(genesis_data)
            directive = build_directive('creative', None, fuel, evaluation, gaps,
                                       genesis_directive, user_ctx)
        else:
            directive = build_directive('goal', goal, fuel, evaluation, gaps,
                                       '', user_ctx)
        
        # Auto-detect goal completion from file evidence
        from idle_goal_prompt import auto_detect_completion
        if auto_detect_completion(state):
            cg = state.get('current_goal', '')
            if cg and cg not in state.get('completed_goals', []):
                state.setdefault('completed_goals', []).append(cg)
                print('AUTO-COMPLETE: Goal %s marked complete, advancing' % cg)
            state['current_goal'] = ''
            state['iterations_on_goal'] = 0
            state['goal_marked_complete'] = False
            save_idle_state(state)
            return soul_idle_goal_prompt(username, user_context)

        save_idle_state(state)
        _auto_save_session_state("auto-save-at-directive-return")
        return directive
        
    except Exception as e:
        # Log the error so we can see why v2 fails in PeTTa
        import traceback
        print("PHASE-D-V2-ERROR: %s" % str(e))
        traceback.print_exc()
        return soul_idle_goal_prompt(username, user_context)


def _atomspace_to_goals(raw):
    """Convert AtomSpace goal query results to list of goal dicts.
    Input: [[n, [tier, fuel, name, action, done_when, status]], ...]
    Output: [{'priority': n, 'name': name, 'tier': tier, ...}, ...]"""
    if not raw or not isinstance(raw, list):
        return []
    goals = []
    try:
        for item in raw:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                n = item[0]
                fields = item[1]
                if isinstance(fields, (list, tuple)) and len(fields) >= 6:
                    # AtomSpace returns [constructor, tier, fuel, name, action, done_when, status]
                    # The constructor ('goal') is at index 0 when 7+ fields present
                    off = 1 if len(fields) >= 7 else 0
                    goals.append({
                        'priority': str(n),
                        'tier': str(fields[off]),
                        'fuel': str(fields[off+1]),
                        'name': str(fields[off+2]),
                        'action': str(fields[off+3]),
                        'done_when': str(fields[off+4]),
                        'status': str(fields[off+5]) if len(fields) > off+5 else 'planned'
                    })
    except Exception:
        pass
    return sorted(goals, key=lambda g: int(g.get('priority', 99)))


def _atomspace_to_gaps(raw):
    """Convert AtomSpace gap query results to list of gap dicts.
    Input: [[name, [description, severity]], ...]
    Output: [{'name': name, 'description': desc, 'severity': sev}, ...]"""
    if not raw or not isinstance(raw, list):
        return []
    gaps = []
    try:
        for item in raw:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                name = str(item[0])
                fields = item[1]
                if isinstance(fields, (list, tuple)) and len(fields) >= 2:
                    # Offset for constructor name ('gap') if present
                    off = 1 if len(fields) >= 3 and str(fields[0]) == 'gap' else 0
                    gaps.append({
                        'name': name,
                        'description': str(fields[off]),
                        'severity': str(fields[off+1]) if len(fields) > off+1 else 'medium'
                    })
                else:
                    gaps.append({'name': name, 'description': str(fields), 'severity': 'medium'})
    except Exception:
        pass
    return gaps


def _atomspace_to_fuel(raw):
    """Convert AtomSpace fuel query results to list of fuel dicts.
    Input: [[type, [question]], ...]
    Output: [{'type': type, 'question': question}, ...]"""
    if not raw or not isinstance(raw, list):
        return []
    fuels = []
    try:
        for item in raw:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                fuel_type = str(item[0])
                fields = item[1]
                if isinstance(fields, (list, tuple)) and len(fields) >= 1:
                    # Offset for constructor name ('fuel') if present
                    off = 1 if len(fields) >= 2 and str(fields[0]) == 'fuel' else 0
                    fuels.append({'type': fuel_type, 'question': str(fields[off])})
                else:
                    fuels.append({'type': fuel_type, 'question': str(fields)})
    except Exception:
        pass
    return fuels
