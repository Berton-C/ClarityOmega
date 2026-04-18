import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v3 import sense

texts = [
    ('doctor/scan/panic', 'I just got back from the doctor and they found something on the scan I am trying not to panic but I keep thinking the worst'),
    ('job/grind/done', 'Honestly I am so done with this job Every day is the same grind and my manager takes credit for everything I do'),
    ('puppy/sweetest/moon', 'We just adopted a puppy and she is the sweetest thing The kids are over the moon It feels like our family is complete now'),
    ('flat/grey/empty', 'I do not really know what I am feeling right now Everything just feels kind of flat and grey Not sad exactly just empty'),
]

for label, t in texts:
    r = sense(t)
    print(label)
    print('  emotion:', r['emotion'], 'conf:', r['confidence'])
    print('  key_words:', r['key_words'])
    print('  all_scores:', {k: round(v,3) for k,v in r['all_scores'].items()})
    print()
