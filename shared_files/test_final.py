import sys
sys.path.insert(0, '/tmp')
from emotional_sense_final import sense

tests = [
    ('scared', 'I am so scared'),
    ('doctor', 'I just got back from the doctor and they found something on the scan I am trying not to panic but I keep thinking the worst'),
    ('furious', 'I am furious'),
    ('frustrated', 'This is so frustrating I keep trying and nothing works'),
    ('puppy', 'We just adopted a puppy and she is the sweetest thing The kids are over the moon'),
    ('flat', 'I do not really know what I am feeling Everything just feels kind of flat and grey Not sad exactly just empty'),
    ('job', 'Honestly I am so done with this job Every day is the same grind and my manager takes credit for everything I do'),
]
for label, text in tests:
    r = sense(text)
    print(label, '->', r)
