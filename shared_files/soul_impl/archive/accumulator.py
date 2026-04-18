#!/usr/bin/env python3
import json
import os
import sys
sys.path.insert(0, '/tmp/soul_impl')
from situation_encoder import encode_situation

FIELD_PATH = '/tmp/soul_impl/bundled_field.json'
PERSISTENT_FIELD_PATH = '/tmp/soul_impl/persistent_state/accumulated_field.json'

def _normalize_field(raw):
    if not raw:
        return None
    if isinstance(raw[0], list):
        return raw
    return [[v, 0.9] for v in raw]

def load_field():
    if os.path.exists(PERSISTENT_FIELD_PATH):
        with open(PERSISTENT_FIELD_PATH) as f:
            state = json.load(f)
        vec = state.get('field', None)
        if vec and any(v != 0.0 for v in (vec if not isinstance(vec[0], list) else [x[0] for x in vec])):
            return _normalize_field(vec)
    if os.path.exists(FIELD_PATH):
        with open(FIELD_PATH) as f:
            return json.load(f)
    return None

def save_field(field):
    with open(FIELD_PATH, 'w') as f:
        json.dump(field, f, indent=2)

def q_join_fields(field_a, field_b):
    joined = []
    for (sa, ca), (sb, cb) in zip(field_a, field_b):
        joined.append([max(sa, sb), max(ca, cb)])
    return joined

def accumulate_exchange(vad_scores, conversation_signals):
    new_vec = encode_situation(vad_scores, conversation_signals)
    new_field = [[s, c] for s, c in new_vec]
    existing = load_field()
    if existing is None:
        save_field(new_field)
        return new_field, 'initialized'
    merged = q_join_fields(existing, new_field)
    save_field(merged)
    return merged, 'accumulated'

if __name__ == '__main__':
    print('Testing persistent-state-aware load_field')
    result = load_field()
    print('Loaded field:', result)
    print('Persistent exists:', os.path.exists(PERSISTENT_FIELD_PATH))
