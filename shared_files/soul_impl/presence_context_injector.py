#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/soul_impl')
from presence_modulator_v2 import get_vad_centroid, presence_mode, presence_guidance
from emotion_bridge_live import load_lex

LEX_PATH = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
_lex_cache = None

def get_lex():
    global _lex_cache
    if _lex_cache is None:
        _lex_cache = load_lex(LEX_PATH)
    return _lex_cache

def inject_presence_context(user_message):
    lex = get_lex()
    v, a, d, cov = get_vad_centroid(user_message, lex)
    mode, read = presence_mode(v, a, d, cov)
    guidance = presence_guidance(mode)
    context_block = 'PRESENCE_MODE: %s\nSNS_PNS_READ: %s\nGUIDANCE: %s\nVAD_COVERAGE: %.2f' % (mode, read, guidance, cov)
    return context_block, mode, read

if __name__ == '__main__':
    tests = ['I am scared and confused', 'I feel peaceful and curious', 'I dont know what to think anymore', 'whatever it does not matter', 'I am excited but also nervous']
    for t in tests:
        ctx, mode, read = inject_presence_context(t)
        print('--- Input: %s ---' % t)
        print(ctx)
        print()
