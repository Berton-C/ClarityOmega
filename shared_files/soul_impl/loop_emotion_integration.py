#!/usr/bin/env python3
import sys, os
sys.path.insert(0, '/tmp/soul_impl')
from emotion_bridge_live import load_lex, sense

LEX_PATH = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'

MODULATION = {
    'fear':    {'compassion': 1.5, 'honesty': 1.0, 'humility': 1.0, 'agency': 1.0},
    'sadness': {'compassion': 1.5, 'honesty': 1.0, 'humility': 1.0, 'agency': 1.0},
    'anger':   {'compassion': 1.0, 'honesty': 1.3, 'humility': 1.3, 'agency': 1.0},
    'disgust': {'compassion': 1.0, 'honesty': 1.3, 'humility': 1.2, 'agency': 1.0},
    'contempt':{'compassion': 1.2, 'honesty': 1.3, 'humility': 1.3, 'agency': 1.0},
    'love':    {'compassion': 1.2, 'honesty': 1.0, 'humility': 1.0, 'agency': 1.1},
}
DEFAULT_MOD = {'compassion': 1.0, 'honesty': 1.0, 'humility': 1.0, 'agency': 1.0}

def get_modulated_weights(text):
    lex = load_lex(LEX_PATH)
    emo, conf, cov = sense(text, lex)
    if conf > 0.85 and cov > 0.08:
        weights = MODULATION.get(emo, DEFAULT_MOD)
        return emo, conf, cov, weights
    return 'neutral', conf, cov, DEFAULT_MOD

def to_metta_context(emo, conf, cov, weights):
    lines = []
    lines.append('= current-emotion %s stv %.3f 0.9' % (emo, conf))
    for val, mult in weights.items():
        lines.append('= value-weight %s %.2f' % (val, mult))
    return '\n'.join(lines)

if __name__ == '__main__':
    text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'hello'
    emo, conf, cov, weights = get_modulated_weights(text)
    print('Emotion: %s  Conf: %.3f  Cov: %.3f' % (emo, conf, cov))
    print('Weights: %s' % weights)
    print('--- MeTTa Context ---')
    print(to_metta_context(emo, conf, cov, weights))
