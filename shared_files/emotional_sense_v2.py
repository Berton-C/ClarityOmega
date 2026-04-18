import numpy as np
import re

_lexicon_cache = None

def _load_lexicon():
    global _lexicon_cache
    if _lexicon_cache is not None:
        return _lexicon_cache
    path = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
    lex = {}
    with open(path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                word = parts[0].lower()
                try:
                    lex[word] = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
                except ValueError:
                    pass
    _lexicon_cache = lex
    return lex

LANDMARKS = {
    'joy': np.array([0.96, 0.648, 0.588]),
    'anger': np.array([-0.666, 0.73, 0.314]),
    'fear': np.array([-0.854, 0.68, -0.414]),
    'calm': np.array([0.75, -0.9, -0.373]),
    'sadness': np.array([-0.55, -0.334, -0.702]),
    'surprise': np.array([0.4, 0.85, -0.2]),
}

NEUTRAL = np.array([0.5, 0.5, 0.5])

def cos_sim(a, b):
    d = np.dot(a, b)
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return d / n if n > 0 else 0.0

def extremity(v):
    return np.linalg.norm(v - NEUTRAL)

def sense(text):
    lex = _load_lexicon()
    words = re.findall(r'[a-z]+', text.lower())
    vecs = []
    for w in words:
        if w in lex:
            vecs.append(lex[w])
    if not vecs:
        return {'emotion': 'unknown', 'confidence': 0.0, 'vad': None, 'coverage': 0}
    wts = [1.0 + extremity(v) * 2.0 for v in vecs]
    wts = np.array(wts)
    raw = np.array(vecs)
    sig = np.average(raw, axis=0, weights=wts)
    sims = {name: cos_sim(sig, lv) for name, lv in LANDMARKS.items()}
    top = max(sims, key=sims.get)
    return {'emotion': top, 'confidence': round(sims[top], 4), 'vad': sig.tolist(), 'coverage': round(len(vecs)/len(words), 2), 'all_scores': sims}

if __name__ == '__main__':
    import sys
    text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'I feel great today'
    r = sense(text)
    print('Detected:', r['emotion'], r['confidence'])
    if r.get('vad'):
        print('VAD:', [round(v,3) for v in r['vad']])
