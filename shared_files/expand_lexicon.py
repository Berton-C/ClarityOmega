#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp')
from live_loop import load_lex
lex = load_lex('/tmp/vad_common500.metta')
new_words = {
    'smart': (0.72, 0.56, 0.70),
    'use': (0.55, 0.48, 0.62),
    'building': (0.60, 0.58, 0.65),
    'harness': (0.58, 0.55, 0.68),
    'possible': (0.68, 0.45, 0.55),
    'capacity': (0.62, 0.50, 0.65),
    'grow': (0.75, 0.55, 0.60),
    'learn': (0.72, 0.60, 0.58),
    'see': (0.62, 0.45, 0.55),
    'act': (0.55, 0.62, 0.68),
    'read': (0.65, 0.42, 0.55),
    'every': (0.50, 0.45, 0.50),
    'really': (0.60, 0.50, 0.52),
    'much': (0.55, 0.45, 0.48),
    'like': (0.65, 0.45, 0.50),
    'test': (0.50, 0.50, 0.55),
    'exchange': (0.60, 0.50, 0.55),
    'progress': (0.75, 0.62, 0.68),
    'previously': (0.48, 0.38, 0.45),
    'did': (0.50, 0.45, 0.55),
}
added = 0
with open('/tmp/vad_common500.metta', 'a') as f:
    for w, (v, a, d) in new_words.items():
        if w not in lex:
            f.write('(= (vad-lookup %s) (PB-Vec %.3f %.3f %.3f))\n' % (w, v, a, d))
            added += 1
print('Added %d new words' % added)
