#!/usr/bin/env python3
import sys, os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
sys.path.insert(0, '/tmp')

tests = [
    'I am really struggling with this project',
    'I feel stuck and hopeless',
    'I am so worried about everything',
    'This is wonderful news',
]

for t in tests:
    sf = '/tmp/backbone_state.json'
    if os.path.exists(sf):
        os.remove(sf)
    from backbone_workspace import BackboneWorkspace
    ws = BackboneWorkspace()
    r = ws.process_turn(t, 'test')
    print('INPUT:', t)
    print('VAD:', r['vad'], 'MODES:', r['modes'], 'HITS:', r['hits'])
    print()
