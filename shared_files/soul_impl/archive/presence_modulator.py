#!/usr/bin/env python3
import sys, os
sys.path.insert(0, '/tmp/soul_impl')
from emotion_bridge_live import load_lex, sense

LEX_PATH = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'

def get_vad_centroid(text, lex):
    words = text.lower().split()
    vals = [lex[w] for w in words if w in lex]
    if not vals:
        return 0.5, 0.5, 0.5, 0.0
    v = sum(x[0] for x in vals)/len(vals)
    a = sum(x[1] for x in vals)/len(vals)
    d = sum(x[2] for x in vals)/len(vals)
    cov = len(vals)/max(len(words),1)
    return v, a, d, cov

def presence_mode(v, a, d, cov):
    if cov < 0.05:
        return 'engaged', 'insufficient coverage for SNS/PNS read'
    if a > 0.6 and v < 0.4 and d < 0.4:
        return 'spacious', 'SNS reactive - mind seeking escape from thought-sensation'
    if a < 0.4 and v > 0.6 and d > 0.4:
        return 'engaged', 'PNS settled - available to insight and direct engagement'
    if a < 0.4 and v > 0.6:
        return 'engaged', 'PNS leaning - settled but moderate dominance'
    if a > 0.5 and v < 0.5:
        return 'spacious', 'SNS leaning - elevated arousal with low valence'
    return 'transitional', 'mixed signals - follow their lead'

def presence_guidance(mode):
    if mode == 'spacious':
        return 'Non-directive. Do not solve advise or teach. Be open curious present. Make room for PNS to assert.'
    if mode == 'engaged':
        return 'Can engage directly with content. Meet curiosity with substance. Explore together.'
    return 'Light touch. Stay attentive to shifts. Follow their lead.'

if __name__ == '__main__':
    lex = load_lex(LEX_PATH)
    text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'I am scared and confused'
    v, a, d, cov = get_vad_centroid(text, lex)
    mode, read = presence_mode(v, a, d, cov)
    guidance = presence_guidance(mode)
    print('VAD: V=%.3f A=%.3f D=%.3f Cov=%.3f' % (v, a, d, cov))
    print('Mode: %s' % mode)
    print('Read: %s' % read)
    print('Guidance: %s' % guidance)
