#!/usr/bin/env python3
import os
files = sorted(f for f in os.listdir('/tmp') if any(k in f.lower() for k in ['clarity','kb_','belief','proven','temporal','nal']))
print(f'{len(files)} substrate files:')
for f in files:
    print(f'  {f}')
