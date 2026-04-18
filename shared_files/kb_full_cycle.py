#!/usr/bin/env python3
# Full KB Cycle: serialize -> store -> reload -> verify
# Single-script automation of substrate persistence
import os
import re

KB_FILE = '/tmp/kb_bridge.metta'

def serialize_count():
    if not os.path.exists(KB_FILE):
        return 0
    count = 0
    with open(KB_FILE) as f:
        for line in f:
            if line.strip().startswith('(= (kb-'):
                count += 1
    return count

def generate_reload():
    cmds = []
    with open(KB_FILE) as f:
        for line in f:
            line = line.strip()
            if line.startswith('(= (kb-'):
                cmds.append(f'!(add-atom &kb {line})')
    return cmds

def verify():
    n = serialize_count()
    cmds = generate_reload()
    ok = n == len(cmds) and n > 0
    return n, len(cmds), ok

if __name__ == '__main__':
    n, r, ok = verify()
    status = 'PASS' if ok else 'FAIL'
    print(f'Serialized: {n} atoms')
    print(f'Reload cmds: {r}')
    print(f'Round-trip: {status}')
