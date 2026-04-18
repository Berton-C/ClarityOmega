import sys
sys.path.insert(0, '/tmp/soul_impl')
from metta_inference_bridge import parse_metta_result, evaluate_components_from_results
import json
import os

def load_last_cycle():
    path = '/tmp/soul_impl/harness_state.json'
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {'cycle': 0, 'weakest': None, 'history': []}

def save_cycle(state):
    with open('/tmp/soul_impl/harness_state.json', 'w') as f:
        json.dump(state, f, indent=2)

def run_cycle(metta_results):
    state = load_last_cycle()
    state['cycle'] += 1
    evald = evaluate_components_from_results(metta_results)
    state['weakest'] = evald[0]['name'] if evald else None
    entry = {'cycle': state['cycle'], 'weakest': state['weakest'], 'components': []}
    for e in evald:
        entry['components'].append({'name': e['name'], 'f': e['f'], 'c': e['c'], 'fc': e['fc']})
    state['history'].append(entry)
    save_cycle(state)
    return state

if __name__ == '__main__':
    mock = [
        ('closure', [[['--> ', 'autocatalytic-closure', 'compounds'], ['stv', 0.44, 0.3]]]),
        ('observer', [[['--> ', 'observer-port', 'self-reference'], ['stv', 0.765, 0.68]]]),
        ('web', [[['--> ', 'web-detection', 'coherence'], ['stv', 0.5553, 0.55]]]),
        ('bridge', [[['--> ', 'inference-bridge', 'steering'], ['stv', 0.95, 0.727]]])
    ]
    state = run_cycle(mock)
    print('Cycle %d complete. Weakest: %s' % (state['cycle'], state['weakest']))
    for c in state['history'][-1]['components']:
        print('  %s: fc=%s' % (c['name'], c['fc']))
