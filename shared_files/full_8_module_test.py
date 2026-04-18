import sys
sys.path.insert(0, '/tmp')
from pipeline_adapter import adapt_pipeline_to_gate, adapt_gate_to_revision, adapt_revision_to_presend

# Simulate 5-module pipeline output
pipeline_out = {'vad': [0.3, 0.7, 0.4], 'modes': ['holding-space']}
draft = 'I hear that you feel stuck. What does stuck feel like in your body right now?'

# Stage 6: Adapter to gate
gate_in = adapt_pipeline_to_gate(pipeline_out, draft)
print('6 Gate input:', gate_in)

# Stage 7: Simulate gate result
gate_result = {'verdict': 'revise', 'flags': ['too-directive']}
rev_in = adapt_gate_to_revision(gate_result, draft)
print('7 Revision input:', rev_in)
assert rev_in['needs_revision'] == True

# Stage 8: Simulate revision done
revised = 'I am here with you in this.'
presend_in = adapt_revision_to_presend(revised, 0.3, {'verdict': 'pass', 'flags': []})
print('8 Presend input:', presend_in)
assert presend_in['gate_verdict'] == 'pass'

print('FULL 8-MODULE PIPELINE TEST COMPLETE')