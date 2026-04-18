#!/usr/bin/env python3
import sys, os, json
sys.path.insert(0, '/tmp')

# Clean state
if os.path.exists('/tmp/backbone_state.json'):
    os.remove('/tmp/backbone_state.json')

from backbone_bridge import get_response_directives

r1 = get_response_directives('I feel lost and alone', 'user')
print('NEGATIVE:', r1)
print()

if os.path.exists('/tmp/backbone_state.json'):
    os.remove('/tmp/backbone_state.json')

r2 = get_response_directives('I am so excited about this', 'user')
print('POSITIVE:', r2)
print()

if os.path.exists('/tmp/backbone_state.json'):
    os.remove('/tmp/backbone_state.json')

r3 = get_response_directives('the weather is fine', 'user')
print('NEUTRAL:', r3)
