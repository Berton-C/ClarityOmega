import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v4 import _load_lexicon, extremity, NEUTRAL, LANDMARKS
import numpy as np
import re

lex = _load_lexicon()
DW = np.array([1.0, 1.5, 0.8])

def wld(a, b):
    return float(np.linalg.norm((np.array(a) - np.array(b)) * DW))

def sense_v10(text, k=5, min_ext=0.45):
    words = re.findall(r'[a-z]+', text.lower())
    scored = []
    for w in words:
        if w in lex:
            v = lex[w]; e = extremity(v)
            if e >= min_ext: scored.append((e, v, w))
    if len(scored) < 3:
        scored = []
        for w in words:
            if w in lex:
                v = lex[w]; e = extremity(v)
                if e >= 0.3: scored.append((e, v, w))
    if not scored:
        return dict(emotion='unknown', dist=0, words=[], vad=[])
    scored.sort(key=lambda x: x[0], reverse=True)
    best_anchor = None
    for e, v, w in scored[:k]:
        for ln, lv in LANDMARKS.items():
            d = wld(v, lv)
            if e >= 0.7 and d < 0.25:
                if best_anchor is None or d < best_anchor[0]:
                    best_anchor = (d, ln, w, e)
    if best_anchor:
        kw = [s[2] for s in scored[:k]]
        return dict(emotion=best_anchor[1], dist=round(best_anchor[0],4), words=kw, anchor=best_anchor[2])
    top = scored[:k]
    vecs = np.array([s[1] for s in top])
    wts = np.array([s[0] for s in top])
    sig = np.average(vecs, axis=0, weights=wts)
    dists = {}
    for nm, lv in LANDMARKS.items():
        dists[nm] = float(np.linalg.norm((sig - lv) * DW))
    best = min(dists, key=dists.get)
    kw = [s[2] for s in top]
    top3 = sorted(dists.items(), key=lambda x: x[1])[:3]
    return dict(emotion=best, dist=round(dists[best],4), words=kw, vad=[round(x,3) for x in sig], top3=top3)

texts = [('doctor/panic', 'I just got back from the doctor and they found something on the scan I am trying not to panic but I keep thinking the worst'),('job/grind', 'Honestly I am so done with this job Every day is the same grind and my manager takes credit for everything I do'),('puppy', 'We just adopted a puppy and she is the sweetest thing The kids are over the moon It feels like our family is complete now'),('flat/empty', 'I do not really know what I am feeling right now Everything just feels kind of flat and grey Not sad exactly just empty'),('scared', 'I am so scared'),('furious', 'I am furious'),('frustrated', 'This is so frustrating I keep trying and nothing works')]
for lb, t in texts:
    r = sense_v10(t)
    print(lb, '->', r)
