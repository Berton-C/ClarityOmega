#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/soul_impl')
from presence_modulator_v2 import get_vad_centroid, presence_mode, presence_guidance
from semantic_uncertainty_layer import should_override_to_transitional
from emotion_bridge_live import load_lex

LEX_PATH = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
_lex_cache = None

def get_lex():
    global _lex_cache
    if _lex_cache is None:
        _lex_cache = load_lex(LEX_PATH)
    return _lex_cache

def full_presence_read(user_message):
    lex = get_lex()
    v, a, d, cov = get_vad_centroid(user_message, lex)
    mode, read = presence_mode(v, a, d, cov)
    override, override_reason = should_override_to_transitional(mode, user_message)
    if override:
        mode = 'transitional'
        read = override_reason
    guidance = presence_guidance(mode)
    return {'mode': mode, 'read': read, 'guidance': guidance, 'vad': (v, a, d), 'coverage': cov, 'overridden': override}

if __name__ == '__main__':
    tests = ['I dont know what to think anymore', 'things are okay I guess', 'I feel peaceful and curious', 'whatever it does not matter', 'I am scared and confused', 'I am generally experiencing contentment and enjoyment', 'I am terrified and helpless']
    for t in tests:
        r = full_presence_read(t)
        print('Text: %s' % t)
        print('  Mode: %s  Overridden: %s' % (r['mode'], r['overridden']))
        print('  Read: %s' % r['read'])
        print('  Guidance: %s' % r['guidance'])
        print()
