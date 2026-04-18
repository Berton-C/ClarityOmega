import sys
sys.path.insert(0, '/tmp')
from pipeline_adapter import adapt_pipeline_to_gate, adapt_gate_to_revision, adapt_revision_to_presend

p = {'vad': [0.3, 0.7, 0.4], 'modes': ['holding-space']}
r1 = adapt_pipeline_to_gate(p, 'I hear you')
print('gate_input:', r1)
assert r1['valence'] == 0.3
assert r1['primary_mode'] == 'holding-space'

r2 = adapt_gate_to_revision({'verdict': 'revise', 'flags': ['too-directive']}, 'I hear you')
print('revision_input:', r2)
assert r2['needs_revision'] == True

r3 = adapt_revision_to_presend('I am here with you', 0.3, {'verdict': 'pass', 'flags': []})
print('presend_input:', r3)
assert r3['gate_verdict'] == 'pass'

print('ALL ADAPTER TESTS PASSED')
