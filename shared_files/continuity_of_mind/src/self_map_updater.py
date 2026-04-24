import re
import os
import json
import hashlib
from datetime import datetime

SELF_MAP = '/tmp/continuity_of_mind/soul/self_map.metta'
STATE_FILE = '/tmp/continuity_of_mind/src/updater_state.json'
BASE = '/PeTTa/repos/omegaclaw/'
UPDATE_LOG = '/tmp/continuity_of_mind/soul/self_map_update_log.json'

def parse_self_map():
    result = {'files':[], 'flows':[], 'patterns':[], 'tensions':[], 'params':[]}
    if not os.path.exists(SELF_MAP):
        return result
    text = open(SELF_MAP).read()
    for m in re.finditer(r'\(self-map-file\s+(\S+)', text):
        result['files'].append(m.group(1))
    for m in re.finditer(r'\(self-map-flow\s+(\S+)', text):
        result['flows'].append(m.group(1))
    for m in re.finditer(r'\(self-map-pattern\s+(\S+)', text):
        result['patterns'].append(m.group(1))
    for m in re.finditer(r'\(self-map-tension\s+(\S+)', text):
        result['tensions'].append(m.group(1))
    for m in re.finditer(r'\(self-map-param\s+(\S+)', text):
        result['params'].append(m.group(1))
    return result

def compute_hash(filepath):
    if not os.path.exists(filepath):
        return 'MISSING', 0
    data = open(filepath, 'rb').read()
    h = hashlib.md5(data).hexdigest()[:8]
    sz = os.path.getsize(filepath)
    return h, sz

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def detect_changes():
    state = load_state()
    baseline = state.get('baseline_hashes', {})
    changed = []
    new_files = []
    missing = []
    current_hashes = {}
    for fpath, info in baseline.items():
        full = BASE + fpath
        h, sz = compute_hash(full)
        current_hashes[fpath] = {'md5': h, 'size': sz}
        old_h = info.get('md5', 'NONE')
        if h == 'MISSING':
            missing.append(fpath)
        elif h != old_h:
            changed.append((fpath, old_h, h, info.get('size',0), sz))
    return {'changed': changed, 'missing': missing, 'current_hashes': current_hashes}

def run_update_cycle():
    parsed = parse_self_map()
    total = sum(len(v) for v in parsed.values())
    changes = detect_changes()
    return {'parsed_atoms': total, 'map': {k:len(v) for k,v in parsed.items()},
            'changed_files': len(changes['changed']), 'missing_files': len(changes['missing']),
            'details': changes['changed']}

if __name__ == '__main__':
    parsed = parse_self_map()
    for k,v in parsed.items():
        print(f'{k}: {len(v)} items')
    total = sum(len(v) for v in parsed.values())
    print(f'TOTAL: {total} atoms parsed')
    print('---CHANGE DETECTION---')
    changes = detect_changes()
    if changes['changed']:
        for f, old, new, osz, nsz in changes['changed']:
            print(f'CHANGED: {f} {old}->{new} size {osz}->{nsz}')
    else:
        print('No changes detected from baseline.')
    if changes['missing']:
        for f in changes['missing']:
            print(f'MISSING: {f}')
    print('DETECT_OK')
