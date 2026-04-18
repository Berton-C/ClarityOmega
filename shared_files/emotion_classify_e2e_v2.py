import math
import sys

LANDMARKS = {
    'joy': (0.960, 0.648, 0.588),
    'anger': (-0.666, 0.730, 0.314),
    'sadness': (-0.740, -0.370, -0.494),
    'fear': (-0.854, 0.680, -0.414),
    'surprise': (0.400, 0.820, 0.160),
    'disgust': (-0.896, 0.550, -0.366),
    'trust': (0.580, -0.020, 0.440),
    'anticipation': (0.380, 0.416, 0.316),
    'contempt': (-0.588, 0.270, -0.208),
    'love': (0.890, 0.540, 0.400),
}

def cosine_sim(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    ma = math.sqrt(sum(x*x for x in a))
    mb = math.sqrt(sum(x*x for x in b))
    if ma == 0 or mb == 0: return 0.0
    return dot / (ma * mb)

def load_lexicon(path):
    lex = {}
    with open(path) as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 4:
                try:
                    lex[parts[0].lower()] = (float(parts[1]), float(parts[2]), float(parts[3]))
                except ValueError:
                    continue
    return lex

def classify_word(word, lexicon):
    word = word.lower()
    if word not in lexicon:
        return None
    vad = lexicon[word]
    scores = {}
    for emo, lv in LANDMARKS.items():
        scores[emo] = cosine_sim(vad, lv)
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return vad, ranked

if __name__ == '__main__':
    lex = load_lexicon('/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt')
    words = ['elated','furious','terrified','hopeful','melancholy','disgusted','serene','anxious','grateful','bitter']
    if len(sys.argv) > 1:
        words = sys.argv[1:]
    for w in words:
        r = classify_word(w, lex)
        if r is None:
            print(f'{w}: NOT IN LEXICON')
        else:
            vad, ranked = r
            print(f'{w} VAD=({vad[0]:.3f},{vad[1]:.3f},{vad[2]:.3f}) -> {ranked[0][0]}({ranked[0][1]:.3f}) {ranked[1][0]}({ranked[1][1]:.3f}) {ranked[2][0]}({ranked[2][1]:.3f})')
