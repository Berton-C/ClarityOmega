import sys
import os
import json
from datetime import datetime

BELIEF_STORE = '/tmp/continuity_of_mind/soul/nal_beliefs.json'

def load_beliefs():
    if os.path.exists(BELIEF_STORE):
        try:
            return json.loads(open(BELIEF_STORE).read())
        except:
            pass
    return {'beliefs': {}, 'inference_log': [], 'revision_count': 0}

def save_beliefs(store):
    with open(BELIEF_STORE, 'w') as f:
        f.write(json.dumps(store, indent=2))

def add_observation(store, term, freq, conf, source='observation'):
    key = term if isinstance(term, str) else json.dumps(term)
    entry = {'freq': freq, 'conf': conf, 'source': source, 'time': datetime.now().strftime('%Y-%m-%d %H:%M')}
    if key not in store['beliefs']:
        store['beliefs'][key] = []
    store['beliefs'][key].append(entry)
    return store

def get_revision_pairs(store):
    pairs = []
    for key, observations in store['beliefs'].items():
        if len(observations) >= 2:
            obs = sorted(observations, key=lambda x: x['conf'], reverse=True)
            pairs.append({'term': key, 'obs1': obs[0], 'obs2': obs[1], 'total_obs': len(observations)})
    return pairs

def revision_formula(f1, c1, f2, c2):
    w1 = c1 / (1 - c1) if c1 < 1.0 else 100
    w2 = c2 / (1 - c2) if c2 < 1.0 else 100
    w = w1 + w2
    f_new = (w1 * f1 + w2 * f2) / w if w > 0 else (f1 + f2) / 2
    c_new = w / (w + 1)
    return round(f_new, 6), round(c_new, 6)

def format_metta_belief(term, freq, conf):
    return f'!(add-atom &self {term} (stv {freq} {conf}))'

def run_revisions(store):
    pairs = get_revision_pairs(store)
    results = []
    for p in pairs:
        f_new, c_new = revision_formula(p['obs1']['freq'], p['obs1']['conf'], p['obs2']['freq'], p['obs2']['conf'])
        results.append({'term': p['term'], 'freq': f_new, 'conf': c_new, 'from_obs': p['total_obs']})
        store['revision_count'] += 1
        store['inference_log'].append({'type': 'revision', 'term': p['term'], 'result_stv': [f_new, c_new], 'time': datetime.now().strftime('%Y-%m-%d %H:%M')})
    return results

if __name__ == '__main__':
    store = load_beliefs()
    store = add_observation(store, '(--> clarity persistence)', 1.0, 0.8, 'cycle-2180')
    store = add_observation(store, '(--> clarity persistence)', 0.95, 0.7, 'cycle-2184')
    results = run_revisions(store)
    for r in results:
        print(f'Revised: {r["term"]} -> stv {r["freq"]} {r["conf"]}')
    save_beliefs(store)
    print(f'Beliefs stored: {len(store["beliefs"])} terms, {store["revision_count"]} revisions')
