#!/usr/bin/env python3
import json
from datetime import datetime

def load_links(path='/tmp/mycelial/link_store.json'):
    with open(path) as f:
        return json.load(f)

def save_links(data, path='/tmp/mycelial/link_store.json'):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def reinforce_coretrieval(retrieved_ids, boost=0.05, cap=1.0):
    data = load_links()
    reinforced = []
    id_set = set(retrieved_ids)
    for link in data['links']:
        pair = link['pair']
        if isinstance(pair, str):
            import ast
            pair = ast.literal_eval(pair)
        a, b = pair[0], pair[1]
        if a in id_set and b in id_set:
            old_s = link['strength']
            link['strength'] = min(cap, old_s + boost)
            link['last_reinforced'] = datetime.now().isoformat()
            reinforced.append({'pair': [a, b], 'old': old_s, 'new': link['strength']})
    save_links(data)
    return reinforced

def simulate_retrieval_reinforcement(cycles=10, retrieved_per_cycle=None):
    if retrieved_per_cycle is None:
        retrieved_per_cycle = [['g1','g2','br1'], ['br1','b1'], ['m1','m2','m3'], ['e1','e2'], ['g1','br1','b1']]
    results = []
    for i in range(cycles):
        ids = retrieved_per_cycle[i % len(retrieved_per_cycle)]
        r = reinforce_coretrieval(ids)
        results.append({'cycle': i+1, 'retrieved': ids, 'reinforced': len(r)})
    return results

if __name__ == '__main__':
    print('M7 Link Reinforcer Test')
    r = simulate_retrieval_reinforcement(5)
    for entry in r:
        print('  Cycle', entry['cycle'], ':', entry['reinforced'], 'links reinforced')
    data = load_links()
    for link in data['links']:
        print('  ', link['pair'], 'strength:', link['strength'])
    print('Done')
