#!/usr/bin/env python3
import json
import time
import os

WEIGHT_STORE_PATH = '/tmp/mycelial/weight_store.json'
REINFORCE_AMOUNT = 0.1
DECAY_RATE = 0.01
BASELINE_WEIGHT = 0.5

def load_weights():
    if os.path.exists(WEIGHT_STORE_PATH):
        with open(WEIGHT_STORE_PATH) as f:
            return json.load(f)
    return {}

def save_weights(weights):
    with open(WEIGHT_STORE_PATH, 'w') as f:
        json.dump(weights, f, indent=2)

def reinforce(memory_id, weights=None):
    if weights is None:
        weights = load_weights()
    now = time.time()
    entry = weights.get(memory_id, {'weight': BASELINE_WEIGHT, 'last_access': now, 'access_count': 0})
    elapsed = (now - entry['last_access']) / 3600
    decayed = max(0.1, entry['weight'] - DECAY_RATE * elapsed)
    entry['weight'] = min(1.0, decayed + REINFORCE_AMOUNT)
    entry['last_access'] = now
    entry['access_count'] = entry.get('access_count', 0) + 1
    weights[memory_id] = entry
    save_weights(weights)
    return entry

def get_weight(memory_id, weights=None):
    if weights is None:
        weights = load_weights()
    now = time.time()
    entry = weights.get(memory_id, {'weight': BASELINE_WEIGHT, 'last_access': now, 'access_count': 0})
    elapsed = (now - entry['last_access']) / 3600
    return max(0.1, entry['weight'] - DECAY_RATE * elapsed)

def bulk_reinforce(memory_ids):
    weights = load_weights()
    results = {}
    for mid in memory_ids:
        results[mid] = reinforce(mid, weights)
    return results

if __name__ == '__main__':
    ids = ['g1', 'g2', 'br1', 'b1', 'b2']
    print('Reinforcing:', ids)
    results = bulk_reinforce(ids)
    for mid, entry in results.items():
        print(f'  {mid}: weight={entry["weight"]:.3f} accesses={entry["access_count"]}')
    print('\nSecond reinforcement of g1 and br1:')
    reinforce('g1')
    entry = reinforce('br1')
    w = load_weights()
    for mid in ['g1', 'br1']:
        print(f'  {mid}: weight={w[mid]["weight"]:.3f} accesses={w[mid]["access_count"]}')
