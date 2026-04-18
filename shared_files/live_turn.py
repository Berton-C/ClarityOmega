#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp')
from harness_test import load_lex, vad, dims, route

lex = load_lex('/tmp/vad_common500.metta')

txt = 'use the harness as much as possible in the act of building use the backbone and its capacity to see learn grow'
tid = 'berton-c-live'

(v,a,d), nhits = vad(txt, lex)
dl = dims(v,a,d)
modes = list(set(route[x] for x in dl if x in route))

print('LIVE BACKBONE PROCESSING')
print('========================')
print('[%s] %s' % (tid, txt))
print('  hits=%d VAD=(%.3f, %.3f, %.3f)' % (nhits, v, a, d))
print('  dimensions=%s' % dl)
print('  -> presence modes=%s' % modes)
print()
print('ROUTING RECOMMENDATION: %s' % (modes if modes else ['neutral-presence']))
