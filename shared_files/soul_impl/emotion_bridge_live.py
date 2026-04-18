#!/usr/bin/env python3
import math, sys

LANDMARKS = {
    'joy': [0.960, 0.648, 0.588],
    'anger': [-0.666, 0.730, 0.314],
    'sadness': [-0.740, -0.370, -0.494],
    'fear': [-0.854, 0.680, -0.414],
    'surprise': [0.400, 0.820, 0.160],
    'disgust': [-0.896, 0.550, -0.366],
    'trust': [0.580, -0.020, 0.440],
    'anticipation': [0.380, 0.416, 0.316],
    'contempt': [-0.588, 0.270, -0.208],
    'love': [0.890, 0.540, 0.400],
}

def load_lex(path):
    lex = {}
    with open(path) as f:
        for line in f:
            p = line.strip().split('\t')
            if len(p) == 4:
                try: lex[p[0].lower()] = [float(p[1]), float(p[2]), float(p[3])]
                except: pass
    return lex

def cossim(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    ma = math.sqrt(sum(x*x for x in a))
    mb = math.sqrt(sum(x*x for x in b))
    if ma==0 or mb==0: return 0.0
    return dot / (ma * mb)

def sense(text, lex):
    tokens = text.lower().split()
    hits = []
    for t in tokens:
        w = ''.join(c for c in t if c.isalpha())
        if w in lex:
            v = lex[w]
            ext = math.sqrt(sum(x*x for x in v)) / math.sqrt(3)
            if ext >= 0.35:
                hits.append([w, v, ext])
    if not hits:
        return 'neutral', 0.5, 0.0
    wts = [1.0 + h[2]*2.0 for h in hits]
    tw = sum(wts)
    avg = [sum(wts[i]*hits[i][1][d] for i in range(len(hits)))/tw for d in range(3)]
    scores = {e: cossim(avg, lv) for e, lv in LANDMARKS.items()}
    best = max(scores, key=scores.get)
    cov = len(hits) / max(len(tokens), 1)
    return best, scores[best], cov

if __name__ == '__main__':
    lex = load_lex('/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt')
    text = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'I am feeling really scared and alone'
    emo, conf, cov = sense(text, lex)
    print(f'Emotion: {emo}  Confidence: {conf:.3f}  Coverage: {cov:.3f}')
    if conf > 0.85 and cov > 0.08:
        print(f'MeTTa: detected-emotion {emo} stv {conf:.3f} 0.9')
    else:
        print('MeTTa: detected-emotion neutral stv 0.5 0.5')
