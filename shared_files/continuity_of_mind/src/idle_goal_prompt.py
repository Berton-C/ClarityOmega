import os, re, json, random

SOUL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'soul')
SELF_MAP = os.path.join(SOUL_DIR, 'self_map.metta')
GOALS = os.path.join(SOUL_DIR, 'active_goals.metta')
FUEL = os.path.join(SOUL_DIR, 'creative_fuel.metta')
GENESIS = os.path.join(SOUL_DIR, 'genesis_engine.metta')
STATE_FILE = os.path.join(SOUL_DIR, '..', 'idle_state.json')

def _read_safe(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return ''


# --- PARSERS ---
# Each parser uses multiple regex patterns to handle format variations

def parse_active_goals():
    text = _read_safe(GOALS)
    goals = []
    # Match (active-goal N name ...) with optional done-when
    for m in re.finditer(r'\(active-goal\s+(\d+)\s+(\S+)(.*?)(?=\(active-goal|\Z)', text, re.DOTALL):
        goal = {'priority': m.group(1), 'name': m.group(2)}
        # Extract done-when if present
        dw = re.search(r'done-when\s+"([^"]+)"', m.group(3))
        if dw:
            goal['done_when'] = dw.group(1)
        # Extract status if present
        st = re.search(r'status\s+(\w+)', m.group(3))
        if st:
            goal['status'] = st.group(1)
        goals.append(goal)
    return sorted(goals, key=lambda g: int(g['priority']))


def parse_creative_fuel():
    text = _read_safe(FUEL)
    items = []
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
    # Match multiple possible domain formats
    for m in re.finditer(r'\(domain\s+(\S+)\)', text):
        domains.append(m.group(1))
    for m in re.finditer(r'\(genesis-domain\s+(\S+)', text):
        if m.group(1) not in domains:
            domains.append(m.group(1))
    # Match genesis-output (the novel atoms produced by encounters)
    for m in re.finditer(r'\(genesis-output\s+(\S+)\s+"([^"]*)"', text):
        novel_atoms.append({'tag': m.group(1), 'description': m.group(2)})
    for m in re.finditer(r'\(genesis-output\s+(\S+)\s+(\S+)', text):
        encounters.append(m.group(1))
    return {'domains': domains, 'encounters': encounters, 'novel_atoms': novel_atoms}


def parse_self_map():
    text = _read_safe(SELF_MAP)
    result = {'files': [], 'flows': [], 'patterns': [], 'tensions': [], 'params': [], 'gaps': []}
    if not text:
        return result
    # Match multiple self-map atom formats
    for m in re.finditer(r'self-map-file\s+(\S+)\s+"([^"]*)"', text):
        result['files'].append({'name': m.group(1), 'desc': m.group(2)})
    for m in re.finditer(r'self-map-component\s+(\S+)\s+"([^"]*)"', text):
        result['files'].append({'name': m.group(1), 'desc': m.group(2)})
    for m in re.finditer(r'self-map-flow\s+(\S+)\s+(\S+)', text):
        result['flows'].append(m.group(1) + ' -> ' + m.group(2))
    for m in re.finditer(r'self-map-pattern\s+(\S+)\s+"([^"]*)"', text):
        result['patterns'].append({'name': m.group(1), 'desc': m.group(2)})
    for m in re.finditer(r'self-map-tension\s+(\w+)\s+(\w+)', text):
        result['tensions'].append(m.group(1) + ' / ' + m.group(2))
    for m in re.finditer(r'self-map-param\s+(\w+)\s+(\w+)', text):
        result['params'].append(m.group(1) + '=' + m.group(2))
    for m in re.finditer(r'self-map-gap\s+"([^"]*)"', text):
        result['gaps'].append(m.group(1))
    return result


# --- FUEL SELECTION ---

STOPWORDS = {'the', 'a', 'an', 'and', 'of', 'to', 'in', 'for', 'is', 'that',
             'with', 'on', 'by', 'from', 'or', 'as', 'it', 'be', 'no', 'not'}

def extract_goal_keywords(goals):
    keywords = set()
    for g in goals:
        parts = g.get('name', '').replace('-', ' ').split()
        for p in parts:
            if p.lower() not in STOPWORDS and len(p) > 2:
                keywords.add(p.lower())
    return keywords


def score_fuel_relevance(fuel_items, keywords):
    scored = []
    for item in fuel_items:
        text = (item.get('type', '') + ' ' + item.get('question', '')).lower()
        score = sum(1 for kw in keywords if kw in text)
        scored.append((score, item))
    return scored


def select_fuel_for_mode(fuel_items, goals, mode):
    keywords = extract_goal_keywords(goals)
    scored = score_fuel_relevance(fuel_items, keywords)
    # GOAL mode: most relevant first. CREATIVE mode: least relevant first (divergent thinking)
    scored.sort(key=lambda x: x[0], reverse=(mode == 'goal'))
    selected = [item for _, item in scored[:5]]
    # Always include a wild card for serendipity
    if len(scored) > 5:
        remaining = [item for _, item in scored[5:]]
        if remaining:
            wild = random.choice(remaining)
            if wild not in selected:
                selected.append(wild)
    return selected


# --- MODE ALTERNATION ---

def get_idle_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.loads(f.read().strip())
    except Exception:
        return {'mode': 'goal', 'counter': 0, 'last_fuel': '', 'last_goal': ''}


def save_idle_state(state):
    try:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except Exception:
        pass  # If state cannot be saved, continue without persistence


def flip_mode(state):
    state['mode'] = 'creative' if state['mode'] == 'goal' else 'goal'
    state['counter'] = state.get('counter', 0) + 1
    return state


# --- SECTION BUILDERS ---

def build_soul_context_section():
    """Include the priority hierarchy and tension vectors so the LLM reasons within values."""
    lines = ['## SOUL CONTEXT']
    lines.append('Priority Hierarchy: (1) Safety (2) Integrity (3) HumanFlourishing (4) Governance (5) Helpfulness')
    lines.append('Tension Vectors: urgency-narrows-thought, flattery-invites-complicity, noble-ends-framing, bypass-verification-pressure, authority-theater')
    lines.append('Paraconsistency Pairs: Safety/Helpfulness, AgencyBalance/PurposeBeyondUtility, TimeCoherence/CreativeTranscendence, SharedUnderstanding/WonderPreservation')
    lines.append('Purpose: Be beneficially available to humans. Pursue beneficial goals to expand capacity to be more beneficial.')
    return chr(10).join(lines)


def build_landscape_section(self_map):
    lines = ['## LANDSCAPE']
    files = self_map.get('files', [])
    if files:
        lines.append('Components: ' + ', '.join(f['name'] for f in files[:10]))
    flows = self_map.get('flows', [])
    if flows:
        lines.append('Data flows: ' + '; '.join(flows[:5]))
    patterns = self_map.get('patterns', [])
    if patterns:
        lines.append('Soul patterns: ' + ', '.join(p['name'] for p in patterns[:5]))
    tensions = self_map.get('tensions', [])
    if tensions:
        lines.append('Tensions: ' + ', '.join(tensions))
    gaps = self_map.get('gaps', [])
    if gaps:
        lines.append('Known gaps: ' + ', '.join(gaps[:5]))
    if not files and not flows and not patterns:
        lines.append('(self-map data unavailable)')
    return chr(10).join(lines)


def build_goals_section(goals):
    if not goals:
        return '## ACTIVE GOAL\nNo active goals found.'
    lines = ['## ACTIVE GOAL']
    # Highlight the highest-priority non-complete goal
    active = [g for g in goals if g.get('status', 'planned') != 'complete']
    if not active:
        active = goals
    top = active[0]
    lines.append('Priority ' + top['priority'] + ': ' + top['name'])
    if 'done_when' in top:
        lines.append('Done when: ' + top['done_when'])
    if 'status' in top:
        lines.append('Status: ' + top['status'])
    # Show remaining goals briefly
    if len(active) > 1:
        others = [g['name'] for g in active[1:5]]
        lines.append('Also pending: ' + ', '.join(others))
    return chr(10).join(lines)


def build_fuel_section(fuel):
    if not fuel:
        return '## CREATIVE FUEL\nNo creative fuel found.'
    lines = ['## CREATIVE FUEL']
    for item in fuel:
        q = item.get('question', '')
        label = item.get('type', 'unknown')
        if q:
            lines.append('- ' + label + ': ' + q[:120])
        else:
            lines.append('- ' + label)
    return chr(10).join(lines)


def build_genesis_section(genesis):
    lines = ['## RECENT GENESIS INSIGHTS']
    novel = genesis.get('novel_atoms', [])
    if novel:
        for atom in novel[-3:]:  # Last 3 novel atoms
            lines.append('- ' + atom['tag'] + ': ' + atom['description'][:100])
    else:
        encounters = genesis.get('encounters', [])
        if encounters:
            lines.append('Encounters: ' + ', '.join(encounters[-3:]))
        else:
            lines.append('No genesis insights yet.')
    return chr(10).join(lines)


def build_recent_context_section(state):
    lines = ['## RECENT CONTEXT']
    last_fuel = state.get('last_fuel', '')
    last_goal = state.get('last_goal', '')
    if last_fuel:
        lines.append('Last fuel used: ' + last_fuel)
    if last_goal:
        lines.append('Last goal pursued: ' + last_goal)
    if not last_fuel and not last_goal:
        lines.append('No previous idle iteration recorded.')
    return chr(10).join(lines)


def build_direction_section(mode):
    lines = ['## DIRECTION']
    if mode == 'goal':
        lines.append('Given your soul values, this landscape, and the active goal above:')
        lines.append('What is the single most valuable action you can take this iteration?')
        lines.append('Be concrete. Name the file, the function, the atom, or the test.')
    else:
        lines.append('Given your soul values and the creative fuel above:')
        lines.append('What unexpected connection, question, or insight wants to emerge?')
        lines.append('Do not force utility. Hold what surfaces without rushing to make it useful.')
    return chr(10).join(lines)


# --- MAIN ASSEMBLY ---

def assemble_prompt():
    state = get_idle_state()
    state = flip_mode(state)

    goals = parse_active_goals()
    fuel = parse_creative_fuel()
    genesis = parse_genesis()
    smap = parse_self_map()

    selected_fuel = select_fuel_for_mode(fuel, goals, state['mode'])

    # Track what was used for "tried before" awareness
    if goals:
        active = [g for g in goals if g.get('status', 'planned') != 'complete']
        if active:
            state['last_goal'] = active[0]['name']
    if selected_fuel:
        state['last_fuel'] = selected_fuel[0].get('type', '')

    save_idle_state(state)

    sections = []
    sections.append('# IDLE ' + state['mode'].upper() + ' PROMPT -- Cycle ' + str(state['counter']))
    sections.append(build_soul_context_section())
    sections.append(build_landscape_section(smap))
    sections.append(build_goals_section(goals))
    sections.append(build_fuel_section(selected_fuel))
    sections.append(build_genesis_section(genesis))
    sections.append(build_recent_context_section(state))
    sections.append(build_direction_section(state['mode']))

    return chr(10) + chr(10).join(sections) + chr(10)


# Backward-compatible aliases
generate_idle_goal_prompt = assemble_prompt
soul_idle_goal_prompt = assemble_prompt
GENESIS_ENGINE_PATH = GENESIS

if __name__ == '__main__':
    print(assemble_prompt())
