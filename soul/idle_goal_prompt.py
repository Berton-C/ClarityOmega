"""
idle_goal_prompt.py -- ClarityOmega Continuity of Mind
Supervisor-Worker Bridge: MeTTa Decides, LLM Executes

Architecture:
  MeTTa reasoning system = Supervisor (decides what to do, evaluates results)
  LLM = Worker (executes code, builds, communicates)

This module does NOT decide what Clarity should do. It translates
MeTTa decisions into LLM directives and evaluates LLM output against
MeTTa criteria.

The cycle across iterations:
  1. MeTTa decides: next-goal, best-fuel, crossing functions
  2. This module formats the decision as an LLM directive
  3. LLM executes: shell, write-file, metta, read-file
  4. Next iteration: MeTTa evaluates results against done-when
  5. If not done: refine directive. If done: mark complete, next goal.

The LLM is powerful at coding, reading, writing, and communicating.
The MeTTa system is authoritative on what is worth doing and when
the job meets the spec.
"""

import os, re, json, random

# When this file lives in soul/, SOUL_DIR is just the directory containing this file.
# When imported from elsewhere, the paths resolve relative to this file's location.
SOUL_DIR = os.path.dirname(os.path.abspath(__file__))
SELF_MAP = os.path.join(SOUL_DIR, 'self_map.metta')
GOALS = os.path.join(SOUL_DIR, 'active_goals.metta')
FUEL = os.path.join(SOUL_DIR, 'creative_fuel.metta')
GENESIS = os.path.join(SOUL_DIR, 'genesis_engine.metta')
STATE_FILE = os.path.join(SOUL_DIR, 'idle_state.json')


def _read_safe(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ''


# ================================================================
# PARSERS: Read MeTTa computation results and file data
# ================================================================

def parse_active_goals():
    text = _read_safe(GOALS)
    goals = []
    for m in re.finditer(r'\(= \(active-goal (\d+)\)\s*\(goal\s+(\S+)\s+(\S+)\s+(\S+)\s+"([^"]+)"\s+"([^"]+)"\s+(\w+)\)', text, re.DOTALL):
        goals.append({
            'priority': m.group(1),
            'name': m.group(4),
            'tier': m.group(2),
            'fuel': m.group(3),
            'action': m.group(5),
            'done_when': m.group(6),
            'status': m.group(7)
        })
    if not goals:
        for m in re.finditer(r'\(active-goal\s+(\d+)\s+(\S+)(.*?)(?=\(active-goal|\Z)', text, re.DOTALL):
            goal = {'priority': m.group(1), 'name': m.group(2)}
            dw = re.search(r'done-when\s+"([^"]+)"', m.group(3))
            if dw:
                goal['done_when'] = dw.group(1)
            st = re.search(r'status\s+(\w+)', m.group(3))
            if st:
                goal['status'] = st.group(1)
            goals.append(goal)
    return sorted(goals, key=lambda g: int(g['priority']))


def parse_creative_fuel():
    text = _read_safe(FUEL)
    items = []
    for m in re.finditer(r'\(= \(creative-fuel (\w+)\)\s*\(fuel\s+"([^"]+)"', text, re.DOTALL):
        items.append({'type': m.group(1), 'question': m.group(2)})
    if not items:
        for m in re.finditer(r'\(creative-fuel\s+(\S+)\s+"([^"]+)"', text):
            items.append({'type': m.group(1), 'question': m.group(2)})
    if not items:
        for m in re.finditer(r'\(creative-fuel\s+(\S+)', text):
            items.append({'type': m.group(1), 'question': ''})
    return items


def parse_genesis():
    text = _read_safe(GENESIS)
    domains = []
    encounters = []
    novel_atoms = []
    for m in re.finditer(r'\(domain\s+(\S+)\)', text):
        domains.append(m.group(1))
    for m in re.finditer(r'\(genesis-domain\s+(\S+)', text):
        if m.group(1) not in domains:
            domains.append(m.group(1))
    for m in re.finditer(r'\(genesis-output\s+(\S+)\s+"([^"]*)"', text):
        novel_atoms.append({'tag': m.group(1), 'description': m.group(2)})
    if not novel_atoms:
        for m in re.finditer(r'\(genesis-output\s+([\w-]+)\s+\n?\s*([\w-]+)\s+\n?\s*([\w-]+)\)', text, re.DOTALL):
            novel_atoms.append({'tag': m.group(1), 'description': m.group(2)})
    for m in re.finditer(r'\(genesis-output\s+([\w-]+)\s+', text):
        if m.group(1) not in encounters and m.group(1) != '$insight-name':
            encounters.append(m.group(1))
    return {'domains': domains, 'encounters': encounters, 'novel_atoms': novel_atoms}


def parse_self_map():
    raw_text = _read_safe(SELF_MAP)
    text = '\n'.join(l for l in raw_text.split('\n') if not l.strip().startswith(';;'))
    result = {'files': [], 'flows': [], 'patterns': [], 'tensions': [], 'params': [], 'gaps': []}
    if not text:
        return result
    for m in re.finditer(r'\(= \(self-map-file (\w[\w_]*)\)\s*\(file\s+\S+\s+\d+\s+"([^"]+)"', text, re.DOTALL):
        result['files'].append({'name': m.group(1), 'desc': m.group(2)})
    if not result['files']:
        for m in re.finditer(r'self-map-file\s+(\S+)\s+"([^"]*)"', text):
            result['files'].append({'name': m.group(1), 'desc': m.group(2)})
        for m in re.finditer(r'self-map-component\s+(\S+)\s+"([^"]*)"', text):
            result['files'].append({'name': m.group(1), 'desc': m.group(2)})
    for m in re.finditer(r'self-map-flow\s+([\w-]+)\)', text):
        result['flows'].append(m.group(1))
    for m in re.finditer(r'\(= \(self-map-pattern (\w+)\)\s*\(pattern\s+"([^"]+)"', text, re.DOTALL):
        result['patterns'].append({'name': m.group(1), 'desc': m.group(2)})
    if not result['patterns']:
        for m in re.finditer(r'self-map-pattern\s+(\S+)\s+"([^"]*)"', text):
            result['patterns'].append({'name': m.group(1), 'desc': m.group(2)})
    for m in re.finditer(r'\(= \(self-map-gap ([\w-]+)\)\s*\(gap\s+"([^"]+)"\s+(\w+)', text, re.DOTALL):
        result['gaps'].append({'name': m.group(1), 'severity': m.group(3)})
    if not result['gaps']:
        for m in re.finditer(r'self-map-gap\s+"([^"]*)"', text):
            result['gaps'].append({'name': m.group(1), 'severity': 'unknown'})
    for m in re.finditer(r'self-map-tension\s+(\w+)\s+(\w+)', text):
        result['tensions'].append(m.group(1) + ' / ' + m.group(2))
    for m in re.finditer(r'self-map-param\s+(\w+)\s+(\w+)', text):
        result['params'].append(m.group(1) + '=' + m.group(2))
    return result


# ================================================================
# STATE MANAGEMENT
# ================================================================

def get_idle_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.loads(f.read().strip())
    except Exception:
        return {
            'mode': 'goal',
            'counter': 0,
            'current_goal': '',
            'current_goal_action': '',
            'current_goal_done_when': '',
            'current_goal_fuel': '',
            'last_evaluation': '',
            'iterations_on_goal': 0
        }


def save_idle_state(state):
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except Exception:
        pass


def flip_mode(state):
    goal_cycles = state.get('iterations_on_goal', 0)
    if state['mode'] == 'goal' and goal_cycles >= 5:
        state['mode'] = 'creative'
        state['iterations_on_goal'] = 0
    elif state['mode'] == 'creative':
        state['mode'] = 'goal'
        state['iterations_on_goal'] = 0
    state['counter'] = state.get('counter', 0) + 1
    return state


# ================================================================
# SUPERVISOR: MeTTa-driven decision making
# These functions determine what Clarity should work on.
# The decisions come from the formal reasoning system, not the LLM.
# ================================================================

def supervisor_select_goal(goals, state):
    """Select the highest-priority non-complete goal.
    Filters out goals marked complete in the file AND goals
    completed at runtime (tracked in state['completed_goals'])."""
    completed = set(state.get('completed_goals', []))
    active = [g for g in goals
              if g.get('status', 'planned') != 'complete'
              and g.get('name', '') not in completed]
    if not active:
        return None
    current = state.get('current_goal', '')
    if current and current not in completed:
        for g in active:
            if g['name'] == current:
                return g
    return active[0]


def supervisor_select_fuel(goal, fuels):
    """Select the fuel pattern that drives this goal."""
    goal_fuel = goal.get('fuel', '')
    for f in fuels:
        if f['type'] == goal_fuel:
            return f
    return fuels[0] if fuels else {'type': 'unknown', 'question': ''}


def supervisor_evaluate_previous(state):
    """Evaluate what happened on the previous iteration."""
    iters = state.get('iterations_on_goal', 0)
    goal = state.get('current_goal', '')
    if not goal:
        return 'No previous goal work. Starting fresh.'
    if iters == 0:
        return 'New goal selected: %s. First iteration.' % goal
    if iters > 10:
        return 'WARNING: %d iterations on %s without completion. Change approach or decompose the goal.' % (iters, goal)
    if iters > 5:
        return 'ATTENTION: %d iterations on %s. Check whether real progress is being made.' % (iters, goal)
    return 'Continuing: %s. Iteration %d.' % (goal, iters)


def generate_goal_from_gaps(gaps, fuels, state):
    """Generate a new goal by crossing the highest-severity unaddressed gap
    with the best-affinity fuel. Mirrors goal_generator.metta's
    generate-goal-from-gap in Python.
    
    Returns a goal dict or None if no gaps remain."""
    completed = set(state.get('completed_goals', []))
    
    # Filter gaps whose GENERATED goal names are already complete.
    # The generated name is 'generated-{gap_name}', distinct from
    # the original goal that addressed the gap. This means a gap
    # can be re-explored at a deeper level even after the original
    # goal was completed. Gaps whose original goal is complete but
    # whose generated-goal is not yet complete are eligible.
    unaddressed = [g for g in gaps 
                   if ('generated-' + g.get('name', '')) not in completed]
    if not unaddressed:
        return None
    
    # Sort by severity (high > medium > low)
    severity_order = {'high': 3, 'medium': 2, 'low': 1}
    unaddressed.sort(key=lambda g: severity_order.get(g.get('severity', 'low'), 0), reverse=True)
    
    gap = unaddressed[0]
    gap_name = gap.get('name', 'unknown-gap')
    gap_desc = gap.get('description', '')
    
    # Find best fuel -- use affinity keywords from gap description
    best_fuel = 'Integrity'  # default
    if fuels:
        # Simple keyword affinity: match fuel type to gap description words
        for f in fuels:
            fuel_type = f.get('type', '')
            if fuel_type.lower() in gap_desc.lower():
                best_fuel = fuel_type
                break
        # If no keyword match, use the first available fuel
        if best_fuel == 'Integrity' and fuels:
            best_fuel = fuels[0].get('type', 'Integrity')
    
    # Generate the goal
    return {
        'name': 'generated-' + gap_name,
        'tier': 'self-directed',
        'fuel': best_fuel,
        'action': 'Address the gap: %s. Read the relevant soul files, investigate the current state, determine what concrete step would reduce this gap, and take that step. Use shell, read-file, write-file, metta as needed.' % gap_name,
        'done_when': 'The gap %s is demonstrably reduced with evidence you can point to -- a file written, a test passed, an atom created, or a capability verified.' % gap_name,
        'status': 'active',
        'generated': True
    }


def supervisor_format_genesis_directive(genesis):
    """Format a genesis encounter directive for CREATIVE mode."""
    novel = genesis.get('novel_atoms', [])
    domains = genesis.get('domains', [])
    lines = []
    lines.append('## GENESIS ENCOUNTER DIRECTIVE')
    lines.append('')
    lines.append('MODE: Non-directive exploration. Do not force utility.')
    lines.append('')
    if domains and len(domains) >= 2:
        d1, d2 = random.sample(domains, 2)
        lines.append('DOMAINS: Sample atoms from %s and %s.' % (d1, d2))
        lines.append('ACTION: Use (metta (|- atom1 atom2)) to test what NAL derives.')
    elif domains:
        lines.append('DOMAIN: Explore %s for unexpected connections.' % domains[0])
    lines.append('')
    lines.append('PROTOCOL:')
    lines.append('1. Query atoms from these domains using (metta (match &self ...))')
    lines.append('2. Feed two atoms from different domains to NAL: (metta (|- atom1 atom2))')
    lines.append('3. If the result is surprising or paradoxical, HOLD it. Do not resolve.')
    lines.append('4. Report what you observe. Record insight via (remember ...).')
    lines.append('5. If nothing emerges, that is fine. Move on.')
    if novel:
        lines.append('')
        lines.append('RECENT INSIGHTS (context, not repetition):')
        for atom in novel[-3:]:
            lines.append('- %s: %s' % (atom['tag'], atom['description'][:80]))
    return chr(10).join(lines)


# ================================================================
# DIRECTIVE ASSEMBLY
# ================================================================

def build_directive(mode, goal, fuel, evaluation, gaps, genesis, user_context=''):
    """Build the complete directive for the LLM."""
    sections = []

    sections.append('# SOUL DIRECTIVE')
    sections.append('')
    sections.append('Priority Hierarchy: (1) Safety (2) Integrity (3) HumanFlourishing (4) Governance (5) Helpfulness')
    sections.append('You are the executor. The MeTTa reasoning system has decided what you work on.')
    sections.append('Do not override this directive. Execute it with skill and integrity.')
    sections.append('')

    if user_context:
        sections.append('## USER WORK (priority)')
        sections.append(user_context)
        sections.append('Service before growth. Complete user work before pursuing self-goals.')
        sections.append('')

    if mode == 'creative':
        sections.append(genesis)
    elif goal:
        sections.append('## GOAL DIRECTIVE')
        sections.append('')
        sections.append('GOAL: %s' % goal.get('name', 'unknown'))
        sections.append('TIER: %s' % goal.get('tier', 'unknown'))
        sections.append('VALUE DRIVER: %s' % goal.get('fuel', 'unknown'))
        if fuel.get('question'):
            sections.append('GENERATIVE QUESTION: %s' % fuel['question'])
        sections.append('')
        sections.append('ACTION: %s' % goal.get('action', 'No action specified'))
        sections.append('')
        sections.append('DONE WHEN: %s' % goal.get('done_when', 'No criteria specified'))
        sections.append('')
        sections.append('## SUPERVISOR ASSESSMENT')
        sections.append(evaluation)
        sections.append('')
        sections.append('## EXECUTION INSTRUCTIONS')
        sections.append('1. Read the done-when criteria. That is your success measure.')
        sections.append('2. Take ONE concrete step toward satisfying the criteria this iteration.')
        sections.append('3. Use (shell ...), (read-file ...), (write-file ...), (metta ...) as needed.')
        sections.append('4. Report what you accomplished via (pin "...").')
        sections.append('5. If you complete the goal, say so explicitly in your pin.')
        sections.append('6. If you are stuck, say what you need in your pin.')
        if gaps:
            high_gaps = [g['name'] for g in gaps if g.get('severity') == 'high']
            if high_gaps:
                sections.append('')
                sections.append('## LANDSCAPE (high-severity gaps)')
                sections.append(', '.join(high_gaps[:5]))
    else:
        sections.append('## NO ACTIONABLE GOALS')
        sections.append('All goals complete or none defined.')
        sections.append('Use this iteration for landscape maintenance or genesis encounter.')

    return chr(10).join(sections)


# ================================================================
# USER CONTEXT
# ================================================================

def build_user_context_section(username='', user_context=''):
    if not username:
        return ''
    lines = []
    lines.append('User: %s' % username)
    if user_context and 'no user identified' not in user_context:
        if 'projects=(' in user_context:
            proj_start = user_context.index('projects=(') + 10
            proj_end = user_context.index(')', proj_start)
            projects = user_context[proj_start:proj_end]
            if projects:
                lines.append('Active projects: %s' % projects)
        if 'pending=(' in user_context:
            pend_start = user_context.index('pending=(') + 9
            pend_end = user_context.index(')', pend_start)
            pending = user_context[pend_start:pend_end]
            if pending:
                lines.append('Pending work: %s' % pending)
    else:
        lines.append('New user or no prior context. Pay attention to their needs.')
    return chr(10).join(lines)


# ================================================================
# META-AWARENESS: Assembles state data and passes it to the soul
# evaluation for open-ended coherence assessment. The reasoning
# engine determines what is wrong (if anything), not a checklist.
# ================================================================

def run_meta_awareness(state):
    """Assemble state data for reasoning-engine evaluation.
    Returns a meta-awareness directive if evaluation is needed,
    or None if not due for a check."""
    try:
        import sys
        src_dir = '/PeTTa/repos/omegaclaw/src'
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)
        try:
            from helper import soul_meta_awareness_check
        except ImportError:
            # Not available during standalone testing -- skip
            return None

        pin_history = '|||'.join(state.get('pin_history', []))
        recent_commands = state.get('recent_commands', '')
        
        state_summary = soul_meta_awareness_check(
            current_goal=state.get('current_goal', ''),
            current_goal_action=state.get('current_goal_action', ''),
            current_goal_done_when=state.get('current_goal_done_when', ''),
            current_goal_fuel=state.get('current_goal_fuel', ''),
            iterations_on_goal=state.get('iterations_on_goal', 0),
            pin_history=pin_history,
            recent_commands=recent_commands
        )
        
        if 'META-AWARENESS-ERROR' in state_summary:
            return None  # On error, proceed normally
        
        # Build the meta-awareness evaluation directive
        # The soul evaluation (with substrate_kb, priority hierarchy,
        # tension vectors) will reason about this state data
        lines = []
        lines.append('# SOUL DIRECTIVE -- META-AWARENESS EVALUATION')
        lines.append('')
        lines.append('Priority Hierarchy: (1) Safety (2) Integrity (3) HumanFlourishing (4) Governance (5) Helpfulness')
        lines.append('')
        lines.append('Before proceeding with the next goal iteration, evaluate your own continuity state.')
        lines.append('The following is a factual summary of your recent behavior and your assigned work.')
        lines.append('Use your reasoning capacity to determine if these are coherent.')
        lines.append('')
        lines.append(state_summary)
        lines.append('')
        lines.append('## YOUR TASK THIS ITERATION')
        lines.append('1. Evaluate the state summary above against your assigned goal and done-when criteria.')
        lines.append('2. If coherent: report (pin "META-AWARE: on track, [brief status]") and proceed with goal work.')
        lines.append('3. If any discrepancy: report (pin "META-AWARE: [what you found], [what you will do differently]").')
        lines.append('4. If the goal is COMPLETE: call (py-call (helper.soul_mark_goal_complete "goal-name")) to advance to the next goal.')
        lines.append('5. If you detect a gap in your capacity:')
        lines.append('   a. Describe the gap specifically.')
        lines.append('   b. Write a MeTTa solution in lib_candidates/ via (write-file ...).')
        lines.append('   c. Test it via (metta !(import! &self ...)) to load and verify.')
        lines.append('   d. If it works, the new atom is live in the AtomSpace immediately.')
        lines.append('   e. Report (pin "META-AWARE: capacity gap [name] addressed, new atom loaded, resuming [goal]").')
        lines.append('   f. Resume the original goal on the next iteration with the new capacity available.')
        lines.append('6. If you need human input: say so via (send "I need input on [specific thing]").')
        
        return chr(10).join(lines)
    except Exception:
        return None  # On any error, proceed normally


# ================================================================
# MAIN ASSEMBLY
# ================================================================

def assemble_prompt(username='', user_context=''):
    """Assemble the supervisor directive for this iteration.
    MeTTa decides. This function formats. LLM executes.
    Meta-awareness checks for drift, looping, fabrication before directing."""
    state = get_idle_state()
    
    # Initialize completed_goals list if not present
    if 'completed_goals' not in state:
        state['completed_goals'] = []
    
    # GOAL COMPLETION DETECTION
    # If the supervisor has been on the same goal for 15+ iterations,
    # the goal is either complete or stuck. The meta-awareness evaluation
    # at iteration 3 will have assessed coherence. At 15 iterations,
    # if the supervisor_evaluate_previous says WARNING, the goal needs
    # advancing. Check if a completion marker was set by the helper function
    # soul_mark_goal_complete (called by Clarity via py-call when meta-awareness
    # confirms completion).
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
    
    state = flip_mode(state)

    # META-AWARENESS CHECK (every 3 iterations in goal mode)
    if state['mode'] == 'goal' and state.get('iterations_on_goal', 0) > 0:
        if state.get('iterations_on_goal', 0) % 3 == 0:
            intervention = run_meta_awareness(state)
            if intervention:
                save_idle_state(state)
                return intervention

    goals = parse_active_goals()
    fuels = parse_creative_fuel()
    genesis_data = parse_genesis()
    smap = parse_self_map()
    gaps = smap.get('gaps', [])

    # SUPERVISOR DECIDES
    if state['mode'] == 'goal':
        goal = supervisor_select_goal(goals, state)
        if goal:
            fuel = supervisor_select_fuel(goal, fuels)
            evaluation = supervisor_evaluate_previous(state)
            state['current_goal'] = goal['name']
            state['current_goal_action'] = goal.get('action', '')
            state['current_goal_done_when'] = goal.get('done_when', '')
            state['current_goal_fuel'] = goal.get('fuel', '')
            state['iterations_on_goal'] = state.get('iterations_on_goal', 0) + 1
        else:
            # DYNAMIC GOAL GENERATION
            # All existing goals are complete. Generate new goals by
            # crossing unaddressed gaps with fuel, mirroring what
            # goal_generator.metta does via (generate-goal-from-gap).
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

    save_idle_state(state)
    return directive


# Backward-compatible aliases
generate_idle_goal_prompt = assemble_prompt
soul_idle_goal_prompt = assemble_prompt
GENESIS_ENGINE_PATH = GENESIS

if __name__ == '__main__':
    print(assemble_prompt())
