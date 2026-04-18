import numpy as np
import sys
import re

def load_lexicon(path):
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
    return lex

landmarks = {
    'joy': np.array([0.96, 0.648, 0.588]),
    'anger': np.array([-0.666, 0.73, 0.314]),
    'fear': np.array([-0.854, 0.68, -0.414]),
    'calm': np.array([0.75, -0.9, -0.373]),
    'sadness': np.array([-0.55, -0.334, -0.702]),
    'surprise': np.array([0.4, 0.85, -0.2]),
}

def cos_sim(a, b):
    d = np.dot(a, b)
    n = np.linalg.norm(a) * np.linalg.norm(b)
    return d / n if n > 0 else 0.0

def analyze(text, lex):
    words = re.findall(r'[a-z]+', text.lower())
    vecs = [lex[w] for w in words if w in lex]
    if not vecs:
        return None, {}, 0, len(words)
    sig = np.mean(vecs, axis=0)
    sims = {name: cos_sim(sig, lv) for name, lv in landmarks.items()}
    return sig, sims, len(vecs), len(words)

if __name__ == '__main__':
    lex = load_lexicon('/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt')
    test_msgs = [
        'I am so happy and excited about this project',
        'This is frustrating and I feel stuck',
        'I am worried something bad will happen',
        'Everything is peaceful and quiet today',
    ]
    for msg in test_msgs:
        sig, sims, found, total = analyze(msg, lex)
        print(f'MSG: {msg}')
        print(f'  Coverage: {found}/{total} words matched')
        if sig is not None:
            print(f'  Signature VAD: [{sig[0]:.3f}, {sig[1]:.3f}, {sig[2]:.3f}]')
            ranked = sorted(sims.items(), key=lambda x: -x[1])
            for name, s in ranked:
                print(f'    {name}: {s:.4f}')
        print()
