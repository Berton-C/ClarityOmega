#!/usr/bin/env python3
import os

new_words = [
    ['struggling', 0.2, 0.6, 0.3],
    ['stuck', 0.2, 0.3, 0.2],
    ['nervous', 0.25, 0.6, 0.3],
    ['lost', 0.2, 0.4, 0.2],
    ['overwhelmed', 0.2, 0.7, 0.2],
    ['confused', 0.3, 0.5, 0.3],
    ['hopeless', 0.1, 0.3, 0.1],
    ['defeated', 0.15, 0.3, 0.2],
    ['exhausted', 0.2, 0.2, 0.2],
    ['worried', 0.25, 0.6, 0.3],
    ['stressed', 0.2, 0.7, 0.3],
    ['miserable', 0.1, 0.4, 0.2],
    ['discouraged', 0.2, 0.3, 0.2],
    ['lonely', 0.15, 0.3, 0.2],
    ['helpless', 0.15, 0.3, 0.1],
]

path = '/tmp/vad_common500.metta'
with open(path, 'a') as f:
    f.write('\n; === NEGATIVE-AFFECT EXPANSION 2026-04-17 ===\n')
    for w, v, a, d in new_words:
        f.write('(PB-Vec %s (FloatV %.2f) (FloatV %.2f) (FloatV %.2f))\n' % (w, v, a, d))

print('Added %d words' % len(new_words))
with open(path) as f:
    count = sum(1 for l in f if 'PB-Vec' in l)
print('Total PB-Vec entries: %d' % count)
