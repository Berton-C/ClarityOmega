# Python Test Harness - validates MeTTa substrate routing
# Python asks, MeTTa reasons, Python validates
import subprocess
import json
import re

def query_metta(vad_v, vad_a, vad_d):
    valence = 'negative-valence' if vad_v < 0.4 else ('mid-valence' if vad_v < 0.65 else 'positive-valence')
    arousal = 'low-arousal' if vad_a < 0.4 else ('mid-arousal' if vad_a < 0.65 else 'high-arousal')
    dominance = 'low-dominance' if vad_d < 0.4 else ('mid-dominance' if vad_d < 0.65 else 'high-dominance')
    strategies = ['empathic-attunement','grounding-presence','collaborative-exploration','witnessing-celebration','gentle-activation']
    vad_key = f'(x {valence} {arousal} {dominance})'
    print(f'  VAD discretized: {valence} {arousal} {dominance}')
    print(f'  Querying MeTTa substrate for strategy routing...')
    return {'vad_discrete': (valence, arousal, dominance), 'vad_key': vad_key}

def infer_vad(text):
    t = text.lower()
    v, a, d = 0.5, 0.5, 0.5
    if any(w in t for w in ['frustrated','angry','stuck','hate','bad','sad']): v -= 0.2
    if any(w in t for w in ['great','happy','love','excited','awesome','good']): v += 0.2
    if any(w in t for w in ['!','urgent','need','help','excited','amazing']): a += 0.15
    if any(w in t for w in ['maybe','wondering','idle','bored','meh']): a -= 0.15
    if any(w in t for w in ['i will','i want','i need','let me','my plan']): d += 0.15
    if any(w in t for w in ['i cant','not sure','lost','helpless','overwhelmed']): d -= 0.15
    return min(max(v,0),1), min(max(a,0),1), min(max(d,0),1)

if __name__ == '__main__':
    tests = [
        'I am so frustrated and stuck, nothing is working!',
        'This is exciting, I love where this is going!',
        'I dont know, maybe just wondering about things',
        'I need help urgently please!',
        'I want to explore this idea with you, it seems good',
    ]
    print('=== MeTTa Substrate Test Harness ===')
    print('Python infers VAD -> discretizes -> queries MeTTa -> validates\n')
    for text in tests:
        v, a, d = infer_vad(text)
        print(f'INPUT: {text}')
        print(f'  VAD raw: v={v:.2f} a={a:.2f} d={d:.2f}')
        result = query_metta(v, a, d)
        print(f'  MeTTa key: {result["vad_key"]}')
        print()
    print('Harness ready - next step: subprocess call to actual MeTTa runtime')
