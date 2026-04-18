#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp')
from backbone_workspace import BackboneWorkspace

bw = BackboneWorkspace()
print('Test 1: I feel hopeless and angry')
r = bw.process_turn('I feel hopeless and angry', 'test')
print(r)
print()
print('Test 2: This is wonderful and I feel joy')
r = bw.process_turn('This is wonderful and I feel joy', 'test')
print(r)
print()
print('Guidance:', bw.get_guidance())
