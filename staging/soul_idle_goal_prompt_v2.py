

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
        
        # Convert AtomSpace results to the dict format the supervisor expects
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
        
        save_idle_state(state)
        return directive
        
    except Exception as e:
        # On any error, fall back to v1
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
                    goals.append({
                        'priority': str(n),
                        'tier': str(fields[0]),
                        'fuel': str(fields[1]),
                        'name': str(fields[2]),
                        'action': str(fields[3]),
                        'done_when': str(fields[4]),
                        'status': str(fields[5]) if len(fields) > 5 else 'planned'
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
                    gaps.append({
                        'name': name,
                        'description': str(fields[0]),
                        'severity': str(fields[1])
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
                    fuels.append({'type': fuel_type, 'question': str(fields[0])})
                else:
                    fuels.append({'type': fuel_type, 'question': str(fields)})
    except Exception:
        pass
    return fuels
