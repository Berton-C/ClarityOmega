import numpy as np
import re

NEUTRAL = np.array([0.0, 0.0, 0.0])
DW = np.array([1.0, 1.5, 0.8])

LANDMARKS = {
    'joy': (0.96, 0.648, 0.588),
    'anger': (-0.666, 0.73, 0.314),
    'fear': (-0.854, 0.68, -0.414),
    'sadness': (-0.663, -0.326, -0.631),
    'calm': (0.75, -0.9, 0.373),
    'disgust': (-0.855, 0.555, -0.349),
    'shame': (-0.88, 0.1, -0.65),
    'warmth': (0.91, -0.1, 0.1),
    'frustration': (-0.75, 0.35, -0.4),
    'contempt': (-0.588, 0.27, -0.208),
}

_LEX = None

def _load_lexicon():
    global _LEX
    if _LEX is not None:
        return _LEX
    path = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
    lex = {}
    with open(path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 4:
                w = parts[0].lower()
                try:
                    v, a, d = float(parts[1]), float(parts[2]), float(parts[3])
                    lex[w] = (v, a, d)
                except ValueError:
                    pass
    _LEX = lex
    return lex

def extremity(vad):
    return float(np.linalg.norm(np.array(vad) - NEUTRAL))

def _wdist(a, b):
    return float(np.linalg.norm((np.array(a) - np.array(b)) * DW))

def sense(text, k=5, min_ext=0.45):
    lex = _load_lexicon()
    words = re.findall(r'[a-z]+', text.lower())
    scored = []
    for w in words:
        if w in lex:
            v = lex[w]; e = extremity(v)
            if e >= min_ext:
                scored.append((e, v, w))
    if len(scored) < 3:
        scored = []
        for w in words:
            if w in lex:
                v = lex[w]; e = extremity(v)
                if e >= 0.3:
                    scored.append((e, v, w))
    if not scored:
        return dict(emotion='unknown', confidence=0.0, vad=[0,0,0], coverage=0.0)
    scored.sort(key=lambda x: x[0], reverse=True)
    best_anchor = None
    for e, v, w in scored[:k]:
        for ln, lv in LANDMARKS.items():
            d = _wdist(v, lv)
            if e >= 0.65 and d < 0.35:
                if best_anchor is None or d < best_anchor[0]:
                    best_anchor = (d, ln, w, e)
    if best_anchor:
        conf = round(1.0 - best_anchor[0], 3)
        cov = len(scored) / max(len(words), 1)
        return dict(emotion=best_anchor[1], confidence=conf, vad=list(lex[best_anchor[2]]), coverage=round(cov,3), anchor=best_anchor[2])
    top = scored[:k]
    vecs = np.array([s[1] for s in top])
    wts = np.array([s[0] for s in top])
    sig = np.average(vecs, axis=0, weights=wts)
    dists = {}
    for nm, lv in LANDMARKS.items():
        dists[nm] = _wdist(sig, lv)
    best = min(dists, key=dists.get)
    conf = round(max(0.0, 1.0 - dists[best]), 3)
    cov = len(scored) / max(len(words), 1)
    return dict(emotion=best, confidence=conf, vad=[round(x,3) for x in sig], coverage=round(cov,3))
