#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from backbone_workspace import BackboneWorkspace
ws = BackboneWorkspace()
text = 'This is wonderful I love what is happening here'
result = ws.process_turn(text, 'test')
print('Result:', json.dumps(result, indent=2))
