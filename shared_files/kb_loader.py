#!/usr/bin/env python3
# KB Loader - reads serialized KB and reports atoms
import re

def load_kb(filepath):
    atoms = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('(= (kb-atom'):
                atoms.append(line)
            elif line.startswith('(= (kb-param'):
                atoms.append(line)
    return atoms

if __name__ == '__main__':
    atoms = load_kb('/tmp/kb_bridge.metta')
    print(f'Loaded {len(atoms)} KB atoms')
    for a in atoms:
        print(f'  {a}')
