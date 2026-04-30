# helper.py ADDITIONS for production merge
# ClarityOmega Continuity of Mind -- 2026-04-23
# These 10 functions are NEW and do NOT exist in production helper.py.
# Merge into /PeTTa/repos/omegaclaw/src/helper.py
# Required: import chromadb (add near top of production file if not present)
#
# Functions:
#   1. soul_calibration_confidence_query -- replaces stub in soul_utils.metta
#   2. soul_pre_compute -- replaces stub in soul_utils.metta
#   3. soul_user_context_query -- per-user project state from ChromaDB
#   4. soul_user_context_save -- per-user project state to ChromaDB
#   5. soul_continuity_save -- soul state persistence to ChromaDB
#   6. soul_continuity_restore -- soul state restoration from ChromaDB
#   7. extract_username -- extracts username from "user: message" format
#   8. soul_idle_goal_prompt -- wrapper that calls idle_goal_prompt.py
#   9. soul_service_learning -- records growth data from each user interaction
#  10. soul_meta_awareness_check -- continuous self-verification for drift/looping/fabrication

import chromadb


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


# ================================================================
# GOAL COMPLETION: Runtime goal advancement
# When meta-awareness confirms a goal is complete, Clarity calls
# this function to mark it in idle_state.json. The supervisor
# reads the marker on the next iteration and advances to the
# next goal. No file rebuild required.
# ================================================================

def soul_mark_goal_complete(goal_name=''):
    """Mark a goal as complete in the supervisor state.
    
    Called by Clarity via (py-call (helper.soul_mark_goal_complete "goal-name"))
    when meta-awareness confirms a goal's done-when criteria are met.
    
    Sets a flag in idle_state.json that the supervisor reads on the next
    iteration. The supervisor adds the goal to completed_goals and selects
    the next incomplete goal.
    
    NEW function -- no production equivalent exists."""
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
