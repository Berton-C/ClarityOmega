import math

# 10 emotion landmarks with VAD values (0-1 scale)
LANDMARKS = {
    'joy': (0.96, 0.648, 0.588),
    'anger': (0.334, 0.730, 0.314),
    'sadness': (0.337, 0.674, 0.369),
    'fear': (0.146, 0.680, 0.586),
    'surprise': (0.800, 0.820, 0.460),
    'disgust': (0.260, 0.680, 0.400),
    'trust': (0.750, 0.520, 0.600),
    'anticipation': (0.700, 0.720, 0.550),
    'contempt': (0.300, 0.600, 0.650),
    'love': (0.950, 0.600, 0.540),
}

def cosine_sim(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    ma = math.sqrt(sum(x*x for x in a))
    mb = math.sqrt(sum(x*x for x in b))
    if ma == 0 or mb == 0:
        return 0.0
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
    for emo, landmark_vad in LANDMARKS.items():
        sim = cosine_sim(vad, landmark_vad)
        scores[emo] = max(0.01, sim)
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return vad, ranked

def gen_metta_commands(word, ranked, top_n=3):
    cmds = []
    for emo, conf in ranked[:top_n]:
        cmds.append(f'(|- ((--> {word} {emo}) (stv 1.0 {conf:.3f})) ((--> {emo} emotion-category) (stv 1.0 0.9)))')
    return cmds

if __name__ == '__main__':
    import sys
    lex_path = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
    lex = load_lexicon(lex_path)
    test_words = ['elated', 'terrified', 'furious', 'melancholy', 'hopeful', 'disgusted']
    if len(sys.argv) > 1:
        test_words = sys.argv[1:]
    for w in test_words:
        result = classify_word(w, lex)
        if result is None:
            print(f'{w}: NOT IN LEXICON')
            continue
        vad, ranked = result
        print(f'{w} VAD=({vad[0]:.3f},{vad[1]:.3f},{vad[2]:.3f})')
        print(f'  Top 3: {ranked[0][0]}={ranked[0][1]:.4f}  {ranked[1][0]}={ranked[1][1]:.4f}  {ranked[2][0]}={ranked[2][1]:.4f}')
        for cmd in gen_metta_commands(w, ranked):
            print(f'  MeTTa: {cmd}')
        print()
