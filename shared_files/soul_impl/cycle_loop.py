#!/usr/bin/env python3
"""
Extended Cycle Loop with Result Tracking and Plateau Detection
Python=arithmetic harness, MeTTa=reasoning substrate
2026-04-16
"""
import json
import os
from quantale_harness import PBit, SOUL, WU_WEI, substrate_health, tension_gap, q_mul, q_revise

RESULTS_FILE = '/tmp/soul_impl/cycle_results.json'

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            return json.load(f)
    return {'cycles': [], 'latest_conf': {}, 'plateau_flags': []}

def save_results(data):
    with open(RESULTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def generate_inference_pairs():
    health = substrate_health()
    pairs = []
    for name, val in SOUL.items():
        aligned = q_mul(val, health)
        p1 = f'((--> soul-{name} active) {val.to_stv()})'
        p2 = f'((--> active aligned-with-substrate) {aligned.to_stv()})'
        pairs.append((p1, p2, f'soul-{name}-alignment'))
    gap = tension_gap(health, WU_WEI)
    p1 = f'((--> substrate-health value) {health.to_stv()})'
    p2 = f'((--> value wuwei-{gap.lower()}) (stv 1.0 0.9))'
    pairs.append((p1, p2, 'substrate-wuwei'))
    agency = SOUL['agency']
    honesty = SOUL['honesty']
    p1 = f'((--> substrate-integrity measure) {agency.to_stv()})'
    p2 = f'((--> substrate-integrity measure) {honesty.to_stv()})'
    pairs.append((p1, p2, 'revision-integrity'))
    return pairs

def generate_metta_sexprs():
    pairs = generate_inference_pairs()
    sexprs = []
    for p1, p2, tag in pairs:
        sexprs.append({'sexpr': f'(|- {p1} {p2})', 'tag': tag})
    return sexprs

def detect_plateau(data, tag, new_conf, threshold=0.02):
    history = [c.get(tag, {}).get('conf', 0) for c in data['cycles'] if tag in c]
    if len(history) >= 1 and abs(new_conf - history[-1]) < threshold:
        return True
    return False

def report():
    data = load_results()
    sexprs = generate_metta_sexprs()
    print(f'Cycle {len(data["cycles"])+1}: {len(sexprs)} inference pairs')
    for s in sexprs:
        print(f'  [{s["tag"]}] {s["sexpr"]}')
    if data['plateau_flags']:
        print(f'  PLATEAU detected on: {data["plateau_flags"]}')
        print('  -> Signal: expand to new inference chains')
    return sexprs

if __name__ == '__main__':
    report()
