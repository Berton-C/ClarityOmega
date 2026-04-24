#!/usr/bin/env python3
import sys, os, traceback
sys.path.insert(0, '/tmp/continuity_of_mind/lib_candidates')

print('=== ChromaDB Environment Diagnostics ===')
for k, v in sorted(os.environ.items()):
    if 'CHROMA' in k.upper() or 'PERSIST' in k.upper():
        print(f'  {k}={v}')
    if 'nonexistent' in v:
        print(f'  FOUND nonexistent in env: {k}={v}')

print('HOME:', os.environ.get('HOME', 'NOT SET'))
print('XDG_DATA_HOME:', os.environ.get('XDG_DATA_HOME', 'NOT SET'))

import chromadb
print('chromadb version:', chromadb.__version__)
print('chromadb file:', chromadb.__file__)

try:
    path = '/tmp/continuity_of_mind/data/calibration_db'
    print(f'Attempting PersistentClient(path={path})...')
    client = chromadb.PersistentClient(path=path)
    print('SUCCESS: PersistentClient created')
    col = client.get_or_create_collection(name='test_diag')
    col.add(ids=['test1'], documents=['hello'])
    print('SUCCESS: document added, count:', col.count())
except Exception as e:
    print(f'FAILED: {e}')
    traceback.print_exc()
