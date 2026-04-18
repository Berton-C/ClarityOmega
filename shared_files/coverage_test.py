#!/usr/bin/env python3
import sys, os
sys.path.insert(0, '/tmp')

if os.path.exists('/tmp/backbone_state.json'):
    os.remove('/tmp/backbone_state.json')

from backbone_workspace_v4 import BackboneWorkspace

PHRASES = [
    'how are you doing',
    'what do you think about that',
    'I guess so',
    'sure whatever',
    'tell me more',
    'that makes sense',
    'I see what you mean',
    'okay cool',
    'not sure about this',
    'let me think about it',
    'thanks for your help',
    'I appreciate that',
    'sounds good to me',
    'I disagree with that',
    'can we try something else',
]

zero_hits = 0
for p in PHRASES:
    if os.path.exists('/tmp/backbone_state.json'):
        os.remove('/tmp/backbone_state.json')
    bw = BackboneWorkspace()
    r = bw.process_turn(p, 'user')
    tag = 'ZERO' if r['hits'] == 0 else 'OK'
    if r['hits'] == 0:
        zero_hits += 1
    print(f'{tag} | hits={r["hits"]} modes={r["modes"]} | {p}')
    print(f'  hit_words={r["hit_words"]} boosts={r["boost_phrases"]}')
print(f'\nCoverage: {len(PHRASES)-zero_hits}/{len(PHRASES)} phrases had VAD hits ({zero_hits} zero-hit)')
