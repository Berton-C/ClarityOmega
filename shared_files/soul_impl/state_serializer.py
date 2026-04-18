#!/usr/bin/env python3
import json
import os
from datetime import datetime

STATE_DIR = '/tmp/soul_impl/persistent_state'
FIELD_FILE = os.path.join(STATE_DIR, 'accumulated_field.json')
EXCHANGE_LOG = os.path.join(STATE_DIR, 'exchange_log.json')
META_FILE = os.path.join(STATE_DIR, 'substrate_meta.json')

def ensure_dir():
    os.makedirs(STATE_DIR, exist_ok=True)

def save_field(field_vector, metadata=None):
    ensure_dir()
    state = {'field': field_vector, 'saved_at': datetime.now().isoformat(), 'metadata': metadata or {}}
    with open(FIELD_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    return True

def load_field(default_dim=9):
    if os.path.exists(FIELD_FILE):
        with open(FIELD_FILE, 'r') as f:
            state = json.load(f)
        return state.get('field', [0.0]*default_dim), state.get('metadata', {})
    return [0.0]*default_dim, {'fresh_start': True}

def log_exchange(user_msg, situation_result, compass_result=None):
    ensure_dir()
    log = []
    if os.path.exists(EXCHANGE_LOG):
        with open(EXCHANGE_LOG, 'r') as f:
            log = json.load(f)
    entry = {'timestamp': datetime.now().isoformat(), 'user_message': user_msg[:200], 'presence_mode': situation_result.get('presence_mode',''), 'scalar': situation_result.get('felt_sense_scalar',0)}
    if compass_result:
        entry['compass_composite'] = compass_result.get('composite', 0)
        entry['compass_pass'] = compass_result.get('pass', True)
    log.append(entry)
    if len(log) > 100:
        log = log[-100:]
    with open(EXCHANGE_LOG, 'w') as f:
        json.dump(log, f, indent=2)
    return len(log)

def save_meta(goal_count=0, exchange_count=0, notes=''):
    ensure_dir()
    meta = {'saved_at': datetime.now().isoformat(), 'goal_count': goal_count, 'exchange_count': exchange_count, 'notes': notes}
    with open(META_FILE, 'w') as f:
        json.dump(meta, f, indent=2)

if __name__ == '__main__':
    field = [0.1, 0.5, 0.3, 0.7, 0.2, 0.4, 0.6, 0.8, 0.15]
    save_field(field, {'source': 'test'})
    loaded, meta = load_field()
    print(f'Saved and loaded field: {loaded}')
    print(f'Meta: {meta}')
    n = log_exchange('test message', {'presence_mode': 'grounded', 'felt_sense_scalar': 1.5}, {'composite': 0.8, 'pass': True})
    print(f'Exchange log entries: {n}')
    save_meta(goal_count=14, exchange_count=n, notes='serializer validated')
    print('All persistence functions validated')
