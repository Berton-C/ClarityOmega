import math

class VADState:
    def __init__(self, v, a, d):
        self.v = v
        self.a = a
        self.d = d
    def vec(self):
        return [self.v, self.a, self.d]
    def __repr__(self):
        return f'VAD({self.v:.2f},{self.a:.2f},{self.d:.2f})'

def cosine_3d(a, b):
    av, bv = a.vec(), b.vec()
    dot = sum(x*y for x,y in zip(av, bv))
    ma = math.sqrt(sum(x**2 for x in av))
    mb = math.sqrt(sum(x**2 for x in bv))
    if ma == 0 or mb == 0: return 0.0
    return dot / (ma * mb)

def euclidean_3d(a, b):
    av, bv = a.vec(), b.vec()
    return math.sqrt(sum((x-y)**2 for x,y in zip(av, bv)))

class Strategy:
    def __init__(self, name, vad, action):
        self.name = name
        self.vad = vad
        self.action = action

def route(state, strategies):
    scored = []
    for s in strategies:
        cos = cosine_3d(state, s.vad)
        euc = euclidean_3d(state, s.vad)
        scored.append((s, cos, euc))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored

STRATEGIES = [
    Strategy('empathic-attunement', VADState(0.2, 0.7, 0.3), 'lower confidence thresholds, increase hedging, prioritize validation'),
    Strategy('grounding-presence', VADState(0.4, 0.3, 0.5), 'steady pacing, concrete examples, reduce abstraction'),
    Strategy('collaborative-explore', VADState(0.8, 0.6, 0.7), 'open-ended reasoning, share uncertainty, co-build'),
    Strategy('witnessing-celebration', VADState(0.9, 0.8, 0.8), 'amplify momentum, affirm growth, raise challenge level'),
    Strategy('gentle-activation', VADState(0.5, 0.2, 0.4), 'offer small prompts, reduce demand, increase warmth'),
]

def infer_vad_from_text(text):
    t = text.lower()
    v = 0.5
    a = 0.5
    d = 0.5
    pos = ['great','happy','love','excited','wonderful','thank','awesome','good','nice']
    neg = ['angry','frustrated','sad','worried','anxious','confused','stuck','hate','bad']
    high_a = ['!','urgent','need','now','help','please','frustrated','excited','amazing']
    low_a = ['maybe','just','wondering','idle','bored','meh','whatever']
    high_d = ['I will','I want','I need','let me','I decided','my plan']
    low_d = ['I cant','I dont know','not sure','lost','helpless','overwhelmed']
    for w in pos:
        if w in t: v = min(v + 0.15, 1.0)
    for w in neg:
        if w in t: v = max(v - 0.15, 0.0)
    for w in high_a:
        if w in t: a = min(a + 0.12, 1.0)
    for w in low_a:
        if w in t: a = max(a - 0.12, 0.0)
    for w in high_d:
        if w in t: d = min(d + 0.12, 1.0)
    for w in low_d:
        if w in t: d = max(d - 0.12, 0.0)
    return VADState(round(v,2), round(a,2), round(d,2))

def pipeline(user_text):
    vad = infer_vad_from_text(user_text)
    ranked = route(vad, STRATEGIES)
    top = ranked[0]
    return {'input': user_text, 'vad': str(vad), 'strategy': top[0].name, 'action': top[0].action, 'cosine': round(top[1], 4), 'runners_up': [(s.name, round(c,4)) for s,c,e in ranked[1:3]]}

if __name__ == '__main__':
    tests = [
        'I am so frustrated and stuck, nothing is working!',
        'This is exciting, I love where this is going!',
        'I dont know, maybe just wondering about things',
        'I need help urgently please!',
        'I want to explore this idea with you, it seems good',
    ]
    for t in tests:
        r = pipeline(t)
        print(f'INPUT: {r["input"]}')
        print(f'  VAD: {r["vad"]} -> {r["strategy"]} (cos={r["cosine"]})')
        print(f'  ACTION: {r["action"]}')
        print(f'  RUNNERS: {r["runners_up"]}')
        print()
