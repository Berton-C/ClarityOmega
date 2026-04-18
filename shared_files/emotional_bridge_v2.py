import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v2 import sense

def get_value_weights(text):
    r = sense(text)
    em = r['emotion']
    conf = r['confidence']
    cov = r.get('coverage', 0)
    base = {'honesty': 1.0, 'compassion': 1.0, 'agency_support': 1.0, 'epistemic_humility': 1.0}
    if conf < 0.85 or cov < 0.3:
        return {'weights': base, 'sensing': r, 'modulated': False}
    if em in ('fear', 'sadness'):
        base['compassion'] = 1.5
        base['agency_support'] = 0.8
    elif em == 'anger':
        base['honesty'] = 1.3
        base['epistemic_humility'] = 1.3
    elif em == 'surprise':
        base['epistemic_humility'] = 1.4
    return {'weights': base, 'sensing': r, 'modulated': True}

if __name__ == '__main__':
    tests = [
        'I am so scared right now',
        'I love you but I am scared',
        'This makes me furious',
        'I am happy and calm',
        'hello',
        'I feel nothing',
    ]
    for t in tests:
        w = get_value_weights(t)
        mod = 'MODULATED' if w['modulated'] else 'default'
        em = w['sensing']['emotion']
        co = w['sensing']['confidence']
        print(t + ' -> ' + em + ' ' + str(co) + ' ' + mod + ' ' + str(w['weights']))
