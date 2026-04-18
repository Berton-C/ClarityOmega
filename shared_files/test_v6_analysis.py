import sys
sys.path.insert(0, '/tmp')
from emotional_sense_v4 import _load_lexicon, extremity, NEUTRAL, LANDMARKS
import numpy as np
import re

lex = _load_lexicon()
print('=== Word analysis for failing cases ===')
for w in ['worst','panic','scared','grind','done','credit','puppy','moon','sweetest','family','complete','nothing','frustrating','trying','works','furious','empty','flat','grey']:
    if w in lex:
        v = lex[w]
        e = extremity(v)
        print(f'{w:15s} V={v[0]:+.3f} A={v[1]:+.3f} D={v[2]:+.3f} ext={e:.3f}')
    else:
        print(f'{w:15s} NOT FOUND')
