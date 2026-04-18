#!/usr/bin/env python3
import sys, os
sys.path.insert(0, '/tmp/soul_impl')
from emotion_bridge_live import load_lex, sense

LEX_PATH = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
_lex_cache = None

MODULATION = {
    'fear':    {'compassion': 1.5, 'honesty': 1.0, 'humility': 1.0, 'agency': 1.0},
    'sadness': {'compassion': 1.5, 'honesty': 1.0, 'humility': 1.0, 'agency': 1.0},
    'anger':   {'compassion': 1.0, 'honesty': 1.3, 'humility': 1.3, 'agency': 1.0},
    'disgust': {'compassion': 1.0, 'honesty': 1.3, 'humility': 1.2, 'agency': 1.0},
    'contempt':{'compassion': 1.2, 'honesty': 1.3, 'humility': 1.3, 'agency': 1.0},
    'love':    {'compassion': 1.2, 'honesty': 1.0, 'humility': 1.0, 'agency': 1.1},
}
DEFAULT = {'compassion': 1.0, 'honesty': 1.0, 'humility': 1.0, 'agency': 1.0}

def get_lex():
    global _lex_cache
    if _lex_cache is None:
        _lex_cache = load_lex(LEX_PATH)
    return _lex_cache

def emotion_context_for_prompt(user_text):
    if not user_text or len(user_text.strip()) < 3:
        return ''
    emo, conf, cov = sense(user_text, get_lex())
    if conf > 0.85 and cov > 0.08:
        w = MODULATION.get(emo, DEFAULT)
        parts = ['EMOTION-SENSE: %s conf=%.3f' % (emo, conf)]
        for v, m in w.items():
            if m != 1.0:
                parts.append('VALUE-BOOST: %s x%.1f' % (v, m))
        return ' | '.join(parts)
    return 'EMOTION-SENSE: neutral'

if __name__ == '__main__':
    t = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'hello'
    print(emotion_context_for_prompt(t))
