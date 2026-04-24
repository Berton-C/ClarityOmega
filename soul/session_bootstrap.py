#!/usr/bin/env python3
"""session_bootstrap.py -- ClarityOmega Session Continuity Bootstrap

Run at container startup or first idle cycle to restore critical state
from persistent soul/ directory into working memory.

Reads:
  - soul/session_state.json (last cycle, goals status, active goal)
  - soul/active_goals.metta (goal priorities and completion status)
  - soul/self_map.metta (landscape gaps)
  - soul/creative_fuel.metta (value drivers)

Outputs a structured summary string suitable for pin or remember.
"""

import json
import os
import re
import datetime

SOUL_DIR = os.path.dirname(os.path.abspath(__file__))

def load_session_state():
    path = os.path.join(SOUL_DIR, 'session_state.json')
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

def save_session_state(state):
    path = os.path.join(SOUL_DIR, 'session_state.json')
    with open(path, 'w') as f:
        json.dump(state, f, indent=2)

def scan_goals():
    path = os.path.join(SOUL_DIR, 'active_goals.metta')
    if not os.path.exists(path):
        return [], []
    with open(path) as f:
        content = f.read()
    complete = re.findall(r'\(goal\s+(\S+)\s+(\S+)\s+(\S+).*?complete\)', content, re.DOTALL)
    planned = re.findall(r'\(goal\s+(\S+)\s+(\S+)\s+(\S+).*?planned\)', content, re.DOTALL)
    return complete, planned

def scan_self_map_gaps():
    path = os.path.join(SOUL_DIR, 'self_map.metta')
    if not os.path.exists(path):
        return []
    with open(path) as f:
        content = f.read()
    gaps = re.findall(r'self-map-gap\s+(\S+)', content)
    return gaps

def build_restore_summary():
    state = load_session_state()
    complete, planned = scan_goals()
    gaps = scan_self_map_gaps()
    ts = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')
    lines = [f'SESSION RESTORE at {ts}']
    if state:
        lines.append(f'Last session: cycle {state.get("cycle", "?")}, active goal: {state.get("active_goal", "?")}')
    lines.append(f'Goals complete: {len(complete)}, Goals planned: {len(planned)}')
    if planned:
        next_goals = [f'{g[2]}' for g in planned[:3]]
        lines.append(f'Next planned goals: {", ".join(next_goals)}')
    if gaps:
        lines.append(f'Self-map gaps ({len(gaps)}): {", ".join(gaps[:5])}')
    return '\n'.join(lines)

if __name__ == '__main__':
    print(build_restore_summary())
