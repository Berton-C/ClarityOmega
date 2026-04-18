import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v4 import sense

texts = [
    ('doctor/panic', 'I just got back from the doctor and they found something on the scan I am trying not to panic but I keep thinking the worst'),
    ('job/grind', 'Honestly I am so done with this job Every day is the same grind and my manager takes credit for everything I do I have been looking for something new but nothing is working out'),
    ('puppy/sweet', 'We just adopted a puppy and she is the sweetest thing The kids are over the moon It feels like our family is complete now'),
    ('flat/empty', 'I do not really know what I am feeling right now Everything just feels kind of flat and grey Not sad exactly just empty'),
    ('scared', 'I am so scared'),
    ('furious', 'I am furious'),
    ('frustrated', 'This is so frustrating I keep trying and nothing works'),
]

for label, t in texts:
    r = sense(t)
    print(label)
    print('  emotion:', r['emotion'], 'conf:', r['confidence'])
    print('  key_words:', r['key_words'])
    top3 = sorted(r['all_scores'].items(), key=lambda x: x[1], reverse=True)[:3]
    print('  top3:', [(k, round(v,3)) for k,v in top3])
    print()
