#!/usr/bin/env python3
import json
import time

WEIGHT_PATH = '/tmp/mycelial/weight_store.json'
LINK_PATH = '/tmp/mycelial/link_store.json'
CORET_PATH = '/tmp/mycelial/coretrieval_log.json'

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def inject_node(node_id, initial_weight=0.7):
    weights = load_json(WEIGHT_PATH)
    if node_id in weights:
        return False
    weights[node_id] = {'weight': initial_weight, 'last_access': time.time(), 'access_count': 1}
    save_json(WEIGHT_PATH, weights)
    return True

def simulate_coretrieval(node_a, node_b, cycle=0):
    try:
        log = load_json(CORET_PATH)
    except Exception:
        log = []
    log.append({'pair': sorted([node_a, node_b]), 'cycle': cycle, 'time': time.time()})
    save_json(CORET_PATH, log)

def enrich(new_nodes, connections, cycle_base=10):
    added = []
    for nid in new_nodes:
        if inject_node(nid):
            added.append(nid)
    for i, pair in enumerate(connections):
        simulate_coretrieval(pair[0], pair[1], cycle_base + i)
    return added

if __name__ == '__main__':
    new = ['m1', 'm2', 'm3', 'e1', 'e2']
    conns = [['m1','g1'], ['m1','m2'], ['m2','m3'], ['m3','g2'], ['e1','br1'], ['e1','e2'], ['e2','b1'], ['m1','e1'], ['m2','e2']]
    added = enrich(new, conns, cycle_base=10)
    print('Nodes added:', added)
    print('Connections logged:', len(conns))
    w = load_json(WEIGHT_PATH)
    print('Total nodes now:', len(w))
    for k,v in w.items():
        print('  ', k, v)
