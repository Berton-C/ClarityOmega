import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v2 import sense

texts = [
    'I just got back from the doctor and they found something on the scan. I am trying not to panic but I keep thinking the worst. My partner is being supportive but I can tell they are worried too.',
    'Honestly I am so done with this job. Every day is the same grind and my manager takes credit for everything I do. I have been looking for something new but nothing is working out.',
    'We just adopted a puppy and she is the sweetest thing. The kids are over the moon. It feels like our family is complete now.',
    'I do not really know what I am feeling right now. Everything just feels kind of flat and grey. Not sad exactly just empty.',
]

for t in texts:
    r = sense(t)
    em = r['emotion']
    co = r['confidence']
    cv = r.get('coverage', 0)
    print('TEXT:', t[:60] + '...')
    print('  ->', em, 'conf=' + str(co), 'cov=' + str(cv))
    print()
