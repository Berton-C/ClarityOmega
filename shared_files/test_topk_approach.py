import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v2 import _load_lexicon, cos_sim, extremity, LANDMARKS
import numpy as np
import re

def sense_topk(text, k=5):
    lex = _load_lexicon()
    words = re.findall(r'[a-z]+', text.lower())
    scored = []
    for w in words:
        if w in lex:
            v = lex[w]
            scored.append((float(extremity(v)), v, w))
    if not scored:
        return {'emotion': 'unknown', 'confidence': 0.0}
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:k]
    vecs = np.array([s[1] for s in top])
    wts = np.array([s[0] for s in top])
    sig = np.average(vecs, axis=0, weights=wts)
    sims = {name: cos_sim(sig, lv) for name, lv in LANDMARKS.items()}
    best = max(sims, key=sims.get)
    words_used = [s[2] for s in top]
    return {'emotion': best, 'confidence': round(sims[best], 4), 'key_words': words_used}

texts = [
    'I just got back from the doctor and they found something on the scan. I am trying not to panic but I keep thinking the worst.',
    'Honestly I am so done with this job. Every day is the same grind and my manager takes credit for everything I do.',
    'We just adopted a puppy and she is the sweetest thing. The kids are over the moon. It feels like our family is complete now.',
    'I do not really know what I am feeling right now. Everything just feels kind of flat and grey. Not sad exactly just empty.',
]

for t in texts:
    r = sense_topk(t)
    print('TEXT:', t[:60] + '...')
    print('  ->', r['emotion'], 'conf=' + str(r['confidence']), 'keys=' + str(r.get('key_words','')))
    print()
