import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v2 import _load_lexicon
lex = _load_lexicon()
targets = ['disgust','contempt','disgusted','contemptuous','revulsion','loathing','disdain','scorn','ashamed','shame','guilty','guilt','embarrassed','humiliated']
for w in targets:
    if w in lex:
        v = lex[w]
        print(w, round(v[0],3), round(v[1],3), round(v[2],3))
    else:
        print(w, 'NOT FOUND')
