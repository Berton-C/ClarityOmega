#!/usr/bin/env python3
import json
import os

FIELD_PATH = '/tmp/soul_impl/field_state.json'
DEFAULT_FIELD = [[0.5,0.5]]*9

def load_field():
    if os.path.exists(FIELD_PATH):
        try:
            with open(FIELD_PATH, 'r') as f:
                data = json.load(f)
            if isinstance(data, list) and len(data) >= 9:
                return data
            if isinstance(data, dict) and 'field' in data:
                return data['field']
        except (json.JSONDecodeError, ValueError):
            pass
    return [pair[:] for pair in DEFAULT_FIELD]

def save_field(field_data):
    count = 0
    if os.path.exists(FIELD_PATH):
        try:
            with open(FIELD_PATH, 'r') as f:
                old = json.load(f)
            if isinstance(old, dict):
                count = old.get('count', 0)
        except (json.JSONDecodeError, ValueError):
            pass
    with open(FIELD_PATH, 'w') as f:
        json.dump({'field': field_data, 'count': count+1}, f, indent=2)

def accumulate_exchange(vad_scores, signals):
    field = load_field()
    if vad_scores:
        blend = 0.2
        scalar = sum(vad_scores) / len(vad_scores) if isinstance(vad_scores, (list,tuple)) else 0.5
        for i in range(len(field)):
            field[i][0] = round(field[i][0]*(1-blend) + scalar*blend, 6)
            field[i][1] = round(min(1.0, field[i][1] + 0.02), 6)
    save_field(field)
    return field
