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
    'disgust': np.array([-0.855, 0.555, -0.349]),
    'shame': np.array([-0.773, 0.269, -0.525]),
}

NEUTRAL = np.array([0.5, 0.5, 0.5])

def cos_sim(a, b):
    d = np.dot(a, b)
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return d / n if n > 0 else 0.0

def extremity(v):
    return float(np.linalg.norm(v - NEUTRAL))

def sense(text, k=5):
    lex = _load_lexicon()
    words = re.findall(r'[a-z]+', text.lower())
    scored = []
    for w in words:
        if w in lex:
            v = lex[w]
            scored.append((extremity(v), v, w))
    if not scored:
        return {'emotion': 'unknown', 'confidence': 0.0, 'vad': None, 'coverage': 0, 'key_words': []}
    n_words = len(words)
    n_found = len(scored)
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:k]
    vecs = np.array([s[1] for s in top])
    wts = np.array([s[0] for s in top])
    sig = np.average(vecs, axis=0, weights=wts)
    sims = {name: cos_sim(sig, lv) for name, lv in LANDMARKS.items()}
    best = max(sims, key=sims.get)
    kw = [s[2] for s in top]
    return {'emotion': best, 'confidence': round(sims[best], 4), 'vad': sig.tolist(), 'coverage': round(n_found/n_words, 2), 'key_words': kw, 'all_scores': sims}
