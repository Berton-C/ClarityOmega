#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp')
from backbone_workspace_v2 import BackboneWorkspace
bw = BackboneWorkspace()
for phrase in ['I feel hopeless and angry', 'This is wonderful and I feel joy', 'I am calm and peaceful today', 'Everything is falling apart I cannot cope']:
    print('INPUT:', phrase)
    r = bw.process_turn(phrase, 'test')
    print('  VAD:', r['vad'], ' Modes:', r['modes'])
    print('  Hits:', r['hit_words'], ' Shift:', r['shift'])
    print()
print('Final guidance:', bw.get_guidance())
