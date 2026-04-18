import math

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

tests = {
    'elated': (0.584, 0.897, 0.450),
    'furious': (-0.876, 0.906, 0.196),
    'terrified': (-0.854, 0.680, -0.414),
    'hopeful': (0.730, 0.284, 0.440),
    'melancholy': (-0.500, -0.463, -0.500),
}

for w, vad in tests.items():
    scores = {e: cosine_sim(vad, lv) for e, lv in LANDMARKS.items()}
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    print(f'{w}: TOP={ranked[0][0]}({ranked[0][1]:.3f}) 2nd={ranked[1][0]}({ranked[1][1]:.3f}) 3rd={ranked[2][0]}({ranked[2][1]:.3f})')
