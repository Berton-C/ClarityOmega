#!/usr/bin/env python3
import sys, json, os
sys.path.insert(0, '/tmp')
from respond_with_backbone import shape_response
if os.path.exists('/tmp/backbone_state.json'):
    os.remove('/tmp/backbone_state.json')
for text in ['I am frustrated and stuck on this problem', 'This is wonderful I love what is happening here', 'I feel anxious and overwhelmed right now']:
    r = shape_response(text, 'test')
    print('INPUT:', text)
    print('VAD: v=%.3f a=%.3f d=%.3f' % tuple(r['vad']))
    print('MODES:', ', '.join(r['modes']))
    print('DIRECTIVES:', ' | '.join(r['directives']))
    print()
