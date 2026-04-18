#!/usr/bin/env python3
import sys, os
sys.path.insert(0, '/tmp/soul_impl')
from emotion_bridge_live import load_lex

LEX_PATH = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'

def get_vad_centroid(text, lex):
    words = text.lower().split()
    vals = [lex[w] for w in words if w in lex]
    if not vals:
        return 0.0, 0.0, 0.0, 0.0
    v = sum(x[0] for x in vals)/len(vals)
    a = sum(x[1] for x in vals)/len(vals)
    d = sum(x[2] for x in vals)/len(vals)
    cov = len(vals)/max(len(words),1)
    return v, a, d, cov

def presence_mode(v, a, d, cov):
    if cov < 0.05:
        return 'engaged', 'insufficient coverage for SNS/PNS read'
    if a > 0.0 and v < -0.1 and d < 0.0:
        return 'spacious', 'SNS reactive - elevated arousal negative valence low dominance'
    if a < 0.0 and v > 0.1 and d > 0.0:
        return 'engaged', 'PNS settled - low arousal positive valence'
    if v < -0.1 and a > -0.1:
        return 'spacious', 'SNS leaning - negative valence with non-low arousal'
    if v > 0.1 and a < 0.1:
        return 'engaged', 'PNS leaning - positive valence with low arousal'
    return 'transitional', 'mixed signals - follow their lead'

def presence_guidance(mode):
    if mode == 'spacious':
        return 'Non-directive. Do not solve advise or teach. Be open curious present. Make room for PNS to assert.'
    if mode == 'engaged':
        return 'Can engage directly with content. Meet curiosity with substance. Explore together.'
    return 'Light touch. Stay attentive to shifts. Follow their lead.'

if __name__ == '__main__':
    lex = load_lex(LEX_PATH)
    tests = ['I am scared and confused about everything', 'I am generally experiencing contentment and enjoyment', 'I am so angry nobody listens to me', 'I feel peaceful and curious about what comes next', 'I am terrified and helpless']
    for text in tests:
        v, a, d, cov = get_vad_centroid(text, lex)
        mode, read = presence_mode(v, a, d, cov)
        guidance = presence_guidance(mode)
        print('Text: %s' % text)
        print('  VAD: V=%.3f A=%.3f D=%.3f Cov=%.3f' % (v, a, d, cov))
        print('  Mode: %s | Read: %s' % (mode, read))
        print('  Guidance: %s' % guidance)
        print()
