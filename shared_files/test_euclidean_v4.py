import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v4 import _load_lexicon, extremity, NEUTRAL, LANDMARKS
import numpy as np
import re

def sense_euclid(text, k=5):
    lex = _load_lexicon()
    words = re.findall(r'[a-z]+', text.lower())
    scored = []
    for w in words:
        if w in lex:
            v = lex[w]
            scored.append((extremity(v), v, w))
    if not scored:
        return {'emotion': 'unknown'}
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:k]
    vecs = np.array([s[1] for s in top])
    wts = np.array([s[0] for s in top])
    sig = np.average(vecs, axis=0, weights=wts)
    dists = {name: float(np.linalg.norm(sig - lv)) for name, lv in LANDMARKS.items()}
    best = min(dists, key=dists.get)
    kw = [s[2] for s in top]
    return {'emotion': best, 'dist': round(dists[best], 4), 'key_words': kw, 'vad': sig.tolist(), 'all_dists': dists}

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
    r = sense_euclid(t)
    print(label)
    print('  emotion:', r['emotion'], 'dist:', r['dist'])
    print('  key_words:', r['key_words'])
    top3 = sorted(r['all_dists'].items(), key=lambda x: x[1])[:3]
    print('  closest3:', [(k, round(v,3)) for k,v in top3])
    print()
