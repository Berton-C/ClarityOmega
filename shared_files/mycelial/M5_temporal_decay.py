#!/usr/bin/env python3
import json
from datetime import datetime

BASELINE = 1.0
DECAY_RATE = 0.05
WEIGHT_PATH = '/tmp/mycelial/weight_store.json'
LINK_PATH = '/tmp/mycelial/link_store.json'

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def decay_weights(weights, rate=DECAY_RATE, baseline=BASELINE):
    changes = []
    for nid, info in weights.items():
        old_w = info.get('weight', baseline)
        new_w = old_w + rate * (baseline - old_w)
        new_w = round(new_w, 4)
        if abs(new_w - old_w) > 0.0001:
            changes.append({'id': nid, 'old': old_w, 'new': new_w})
        info['weight'] = new_w
    return weights, changes

def decay_links(links, rate=DECAY_RATE):
    changes = []
    for link in links.get('links', []):
        old_s = link['strength']
        new_s = old_s * (1.0 - rate)
        new_s = round(max(new_s, 0.01), 4)
        if abs(new_s - old_s) > 0.0001:
            changes.append({'pair': link['pair'], 'old': old_s, 'new': new_s})
        link['strength'] = new_s
    return links, changes

def run_decay_cycle():
    weights = load_json(WEIGHT_PATH)
    weights, w_changes = decay_weights(weights)
    save_json(WEIGHT_PATH, weights)
    links = load_json(LINK_PATH)
    links, l_changes = decay_links(links)
    save_json(LINK_PATH, links)
    return w_changes, l_changes

if __name__ == '__main__':
    print('M5 Temporal Decay Cycle')
    print('Before:', load_json(WEIGHT_PATH))
    wc, lc = run_decay_cycle()
    print('Weight changes:', len(wc))
    for c in wc:
        print('  ', c)
    print('Link changes:', len(lc))
    for c in lc:
        print('  ', c)
    print('After:', load_json(WEIGHT_PATH))
    print('Decay cycle complete.')
