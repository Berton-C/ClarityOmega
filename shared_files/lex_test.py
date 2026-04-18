#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp')
from live_loop import load_lex
lex = load_lex('/tmp/vad_common500.metta')
print('Loaded %d words' % len(lex))
if len(lex) > 0:
    keys = list(lex.keys())[:20]
    print('Sample:', keys)
    for w in ['smart','use','happy','love','alive','building','harness','possible']:
        print('  %s: %s' % (w, w in lex))
else:
    print('EMPTY LEXICON - regex mismatch still present')
