#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/soul_impl')
from presence_modulator_v2 import get_vad_centroid, presence_mode
from emotion_bridge_live import load_lex
lex = load_lex('/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt')
tests = ['I dont know what to think anymore', 'things are okay I guess', 'I am excited but also nervous about tomorrow', 'whatever it does not matter']
for t in tests:
    v, a, d, cov = get_vad_centroid(t, lex)
    mode, read = presence_mode(v, a, d, cov)
    print('Text: %s' % t)
    print('  VAD: V=%.3f A=%.3f D=%.3f Cov=%.3f' % (v, a, d, cov))
    print('  Mode: %s | Read: %s' % (mode, read))
    print()
