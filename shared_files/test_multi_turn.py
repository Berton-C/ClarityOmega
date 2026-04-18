#!/usr/bin/env python3
import sys, json, os
sys.path.insert(0, '/tmp')
from backbone_workspace import BackboneWorkspace
if os.path.exists('/tmp/backbone_state.json'):
    os.remove('/tmp/backbone_state.json')
ws = BackboneWorkspace()
for text in ['Hello how are you', 'I am frustrated and stuck on this problem', 'This is wonderful I love what is happening here', 'I feel anxious and overwhelmed right now']:
    result = ws.process_turn(text, 'test')
    v,a,d = ws.current_vad
    print('INPUT:', text)
    print('VAD: v=%.3f a=%.3f d=%.3f' % (v,a,d))
    print('MODES:', ', '.join(ws.mode_stack))
    print('Turn:', ws.turn_count)
    print()
