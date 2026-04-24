import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import self_map_updater as smu
import self_nal_inference as sni

STATE_FILE = '/tmp/continuity_of_mind/soul/updater_state.json'
UPDATE_INTERVAL_CYCLES = 10

SIGNAL_TO_BELIEF = {
    'new_function': ('(--> clarity capability-growth)', 0.9, 0.7),
    'error_recovery': ('(--> clarity error-resilience)', 0.85, 0.65),
    'recurring_pattern': ('(--> clarity pattern-recognition)', 0.9, 0.7),
    'goal_progress': ('(--> clarity goal-completion)', 0.85, 0.6),
    'deep_work': ('(--> clarity sustained-focus)', 0.9, 0.75),
}

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.loads(open(STATE_FILE).read())
        except:
            pass
    return {'last_update_cycle': 0, 'total_updates': 0, 'total_runs': 0, 'total_revisions': 0}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        f.write(json.dumps(state, indent=2))

def should_update(current_cycle, force=False):
    state = load_state()
    if force:
        return True
    return (current_cycle - state['last_update_cycle']) >= UPDATE_INTERVAL_CYCLES

def run_if_due(current_cycle, pin_text='', force=False):
    if not should_update(current_cycle, force):
        return {'skipped': True, 'reason': 'not yet due', 'next_at': load_state()['last_update_cycle'] + UPDATE_INTERVAL_CYCLES}
    # Phase 1: Signal detection and self-map updates
    update_result = smu.run_update_cycle(pin_text)
    # Phase 2: Convert signals to NAL observations and run revision
    belief_store = sni.load_beliefs()
    signals = update_result.get('signals', [])
    obs_added = 0
    for sig in signals:
        sig_type = sig.get('type', '') if isinstance(sig, dict) else str(sig)
        if sig_type in SIGNAL_TO_BELIEF:
            term, freq, conf = SIGNAL_TO_BELIEF[sig_type]
            source = f'cycle-{current_cycle}-{sig_type}'
            belief_store = sni.add_observation(belief_store, term, freq, conf, source)
            obs_added += 1
    revision_results = sni.run_revisions(belief_store)
    sni.save_beliefs(belief_store)
    # Phase 3: Update state
    state = load_state()
    state['last_update_cycle'] = current_cycle
    state['total_updates'] += update_result.get('updates_applied', 0)
    state['total_runs'] += 1
    state['total_revisions'] += len(revision_results)
    state['last_run_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    save_state(state)
    return {
        'skipped': False,
        'result': update_result,
        'observations_added': obs_added,
        'revisions': len(revision_results),
        'revision_details': revision_results,
        'state': state
    }

if __name__ == '__main__':
    print('Integration module loaded OK')
    state = load_state()
    print(f'State: {state}')
    print(f'Signal-to-belief mappings: {len(SIGNAL_TO_BELIEF)}')
    print(f'Should update at cycle 2187: {should_update(2187)}')
