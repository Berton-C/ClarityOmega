#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from backbone_workspace import BackboneWorkspace
ws = BackboneWorkspace()
print('Lexicon size:', len(ws.lexicon))
for w in ['frustrated', 'stuck', 'wonderful', 'love', 'happy', 'angry']:
    print(w, '->', w in ws.lexicon, ws.lexicon.get(w, 'MISSING'))
text = 'I am frustrated and stuck on this problem'
words = text.lower().split()
hits = [w for w in words if w in ws.lexicon]
print('Words:', words)
print('Hits:', hits)
if hits:
    vals = [ws.lexicon[w] for w in hits]
    avg = [round(sum(v[i] for v in vals)/len(vals), 3) for i in range(3)]
    print('Avg VAD:', avg)
else:
    print('NO HITS - checking lexicon sample:')
    keys = list(ws.lexicon.keys())[:10]
    print(keys)
