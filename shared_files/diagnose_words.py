import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v3 import _load_lexicon, extremity, NEUTRAL
import numpy as np
lex = _load_lexicon()
for w in ['sweetest','puppy','moon','worst','panic','grind','done','credit','frustration','annoyed','irritated','delighted','overjoyed','thrilled','complete','family']:
    if w in lex:
        v = lex[w]
        e = extremity(v)
        print(w, 'V='+str(round(v[0],3)), 'A='+str(round(v[1],3)), 'D='+str(round(v[2],3)), 'ext='+str(round(e,3)))
    else:
        print(w, 'NOT FOUND')
