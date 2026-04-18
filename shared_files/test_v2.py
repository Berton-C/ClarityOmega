import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v2 import sense

tests = [
    'I am so scared right now',
    'I love you but I am scared',
    'I am terrified',
    'This makes me furious',
    'I am happy and calm',
    'hello',
    'I feel nothing',
]

for t in tests:
    r = sense(t)
    em = r['emotion']
    co = r['confidence']
    cv = r.get('coverage', 0)
    print(t, '->', em, 'conf=' + str(co), 'cov=' + str(cv))
