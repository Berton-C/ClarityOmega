#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from backbone_workspace_v4 import BackboneWorkspace

bw = BackboneWorkspace()

tests = [
    'I feel like giving up on everything',
    'I just landed my dream job',
    'That makes me so angry I could scream',
    'I am doing okay just checking in'
]

for t in tests:
    bw2 = BackboneWorkspace()
    r = bw2.process_turn(t, 'user')
    print('INPUT:', t)
    print('  VAD:', r['vad'])
    print('  HIT WORDS:', r['hit_words'])
    print('  MODES:', r['modes'])
    print('  TURN:', r['turn'], 'SHIFT:', r['shift'])
    print('---')
