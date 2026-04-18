#!/usr/bin/env python3

PHRASE_BOOSTS = {
    'giving up': [-2.5, -1.0, -2.0],
    'give up': [-2.5, -1.0, -2.0],
    'end it all': [-3.0, 0.5, -2.5],
    'want to die': [-3.0, 0.5, -2.5],
    'no point': [-2.0, -1.5, -2.0],
    'dream job': [2.5, 1.5, 1.5],
    'amazing news': [2.5, 1.5, 1.0],
    'so happy': [2.5, 1.0, 1.0],
    'incredible news': [2.5, 1.5, 1.0],
    'best day': [2.0, 1.0, 1.0],
    'feel lost': [-2.0, -0.5, -2.0],
    'all alone': [-2.0, -1.0, -2.0],
    'so angry': [-2.0, 2.0, 1.0],
    'could scream': [-1.5, 2.0, 0.5],
    'feeling great': [2.0, 1.0, 1.0],
    'so excited': [2.0, 2.0, 1.0],
    'feeling down': [-1.5, -1.0, -1.5],
    'really struggling': [-2.0, 0.0, -2.0],
    'hopeless': [-2.5, -0.5, -2.5],
    'worthless': [-2.5, -0.5, -2.5],
    'thrilled': [2.5, 2.0, 1.5],
    'devastated': [-3.0, 0.5, -2.5],
    'cant take it': [-2.5, 1.0, -2.0],
    'falling apart': [-2.5, 0.5, -2.5],
    'on top of the world': [2.5, 1.5, 2.0],
    'over the moon': [2.5, 1.5, 1.5],
    'sick of': [-1.5, 1.5, 0.0],
    'fed up': [-1.5, 1.5, 0.0],
    'burned out': [-2.0, -1.5, -2.0],
    'burn out': [-2.0, -1.5, -2.0],
    'panic attack': [-2.5, 2.5, -2.5],
    'anxiety': [-2.0, 1.5, -2.0],
    'so proud': [2.0, 1.0, 2.0],
    'hate myself': [-3.0, 0.5, -2.5],
    'love this': [2.0, 1.0, 1.0],
    'grateful': [2.0, 0.5, 1.0],
    'overwhelmed': [-1.5, 1.5, -2.0],
    'exhausted': [-1.5, -2.0, -1.5],
    'inspired': [2.0, 1.5, 1.5],
    'frustrated': [-1.5, 1.5, -0.5],
    'terrified': [-2.5, 2.5, -2.5],
    'at peace': [2.0, -1.5, 1.5],
    'broken': [-2.5, -0.5, -2.5],
    'numb': [-2.0, -2.0, -2.0],
}

def find_phrase_boosts(text):
    text_lower = text.lower()
    found = []
    for phrase, vad in PHRASE_BOOSTS.items():
        if phrase in text_lower:
            found.append((phrase, vad))
    return found

def apply_boosts(base_vad, text):
    boosts = find_phrase_boosts(text)
    if not boosts:
        return base_vad, []
    v, a, d = base_vad
    for phrase, pvad in boosts:
        v = (v + pvad[0]) / 2.0
        a = (a + pvad[1]) / 2.0
        d = (d + pvad[2]) / 2.0
    return [round(v,3), round(a,3), round(d,3)], [b[0] for b in boosts]
