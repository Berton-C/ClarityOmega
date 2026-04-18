#!/usr/bin/env python3
import json
import time
import os
sys_path = '/tmp/soul_impl'

FIELD_PATH = os.path.join(sys_path, 'bundled_field.json')
META_PATH = os.path.join(sys_path, 'field_meta.json')

DECAY_RATE = 0.995

def load_meta():
    if os.path.exists(META_PATH):
        with open(META_PATH) as f:
            return json.load(f)
    return {'last_decay': time.time(), 'exchanges': 0}

def save_meta(meta):
    with open(META_PATH, 'w') as f:
        json.dump(meta, f, indent=2)

def apply_decay(field, steps=1):
    decayed = []
    for s, c in field:
        new_s = s * (DECAY_RATE ** steps)
        new_c = max(0.1, c * (DECAY_RATE ** steps))
        decayed.append([round(new_s, 6), round(new_c, 6)])
    return decayed

if __name__ == '__main__':
    seed = [[0.90,0.9],[0.80,0.9],[0.85,0.9],[0.95,0.9],[1.00,0.9],[0.80,0.9],[1.00,0.9],[0.90,0.9],[0.50,0.9]]
    print('Before decay:', seed)
    after_10 = apply_decay(seed, steps=10)
    print('After 10 steps:', after_10)
    after_100 = apply_decay(seed, steps=100)
    print('After 100 steps:', after_100)
    save_meta({'last_decay': time.time(), 'exchanges': 15})
    print('Meta saved.')
