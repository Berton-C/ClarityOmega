#!/usr/bin/env python3
import re, sys
sys.path.insert(0, '/tmp')

def load_lexicon(path='/tmp/vad_common500.metta'):
    lex = {}
    with open(path) as f:
        for line in f:
            m = re.match(r'\(= \(vad-lookup ([^)]+)\) \(vad ([\d.]+) ([\d.]+) ([\d.]+)\)\)', line)
            if m:
                lex[m.group(1).lower()] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
    return lex

test_texts = [
    'it would be really smart to use the harness as much as possible in the act of building like we did previously',
    'use the harness as much as possible in the act of building use the backbone and its capacity to see learn grow',
    'the backbone is alive and reading our conversation in real time every exchange gets processed',
    'this is a test of the unified cycle',
    'I am feeling really happy and excited about this progress',
    'I am scared and worried about what might happen next'
]

lex = load_lexicon()
print('Lexicon size: %d words' % len(lex))
print()
for txt in test_texts:
    words = txt.lower().split()
    hits = [w for w in words if w in lex]
    misses = [w for w in words if w not in lex]
    print('TEXT: %s' % txt[:60])
    print('  HITS (%d): %s' % (len(hits), hits))
    print('  MISS (%d): %s' % (len(misses), misses))
    print()
