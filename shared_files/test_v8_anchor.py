import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v4 import _load_lexicon, extremity, NEUTRAL, LANDMARKS
import numpy as np
import re

lex = _load_lexicon()
DIM_WEIGHTS = np.array([1.0, 1.5, 0.8])

def word_landmark_dist(vad, lm_vad):
    diff = (np.array(vad) - np.array(lm_vad)) * DIM_WEIGHTS
    return float(np.linalg.norm(diff))

def sense_v8(text, k=5, min_ext=0.45):
    words = re.findall(r'[a-z]+', text.lower())
    scored = []
    for w in words:
        if w in lex:
            v = lex[w]
            e = extremity(v)
            if e >= min_ext:
                scored.append((e, v, w))
    if len(scored) < 3:
        scored = []
        for w in words:
            if w in lex:
                v = lex[w]
                e = extremity(v)
                if e >= 0.3:
                    scored.append((e, v, w))
    if not scored:
        return dict(emotion='unknown', dist=0, words=[], vad=[], top3=[])
    scored.sort(key=lambda x: x[0], reverse=True)
    anchor_hits = {}
    for e, v, w in scored[:k]:
        for lname, lv in LANDMARKS.items():
            d = word_landmark_dist(v, lv)
            if d < 0.35:
                if lname not in anchor_hits or d < anchor_hits[lname][0]:
                    anchor_hits[lname] = (d, w)
    top = scored[:k]
    vecs = np.array([s[1] for s in top])
    wts = np.array([s[0] for s in top])
    sig = np.average(vecs, axis=0, weights=wts)
    dists = {}
    for name, lv in LANDMARKS.items():
        diff = (sig - lv) * DIM_WEIGHTS
        base = float(np.linalg.norm(diff))
        if name in anchor_hits:
            base *= 0.6
        dists[name] = base
    best = min(dists, key=dists.get)
    kw = [s[2] for s in top]
    top3 = sorted(dists.items(), key=lambda x: x[1])[:3]
    return dict(emotion=best, dist=round(dists[best],4), words=kw, vad=[round(x,3) for x in sig], top3=top3, anchors=anchor_hits)

texts = [
    ('doctor/panic', 'I just got back from the doctor and they found something on the scan I am trying not to panic but I keep thinking the worst'),
    ('job/grind', 'Honestly I am so done with this job Every day is the same grind and my manager takes credit for everything I do'),
    ('puppy/sweet', 'We just adopted a puppy and she is the sweetest thing The kids are over the moon It feels like our family is complete now'),
    ('flat/empty', 'I do not really know what I am feeling right now Everything just feels kind of flat and grey Not sad exactly just empty'),
    ('scared', 'I am so scared'),
    ('furious', 'I am furious'),
    ('frustrated', 'This is so frustrating I keep trying and nothing works'),
]
for label, t in texts:
    r = sense_v8(t)
    print(label, '->', r['emotion'], 'dist:', r['dist'], 'words:', r['words'])
    print('  vad:', r['vad'], 'top3:', [(k,round(v,3)) for k,v in r.get('top3',[])])
    print('  anchors:', r.get('anchors',{}))
