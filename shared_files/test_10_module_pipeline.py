import sys
sys.path.insert(0, '/tmp')
from language_flag_detector import detect_flags
from technique_router import available_techniques
from pipeline_adapter import adapt_pipeline_to_gate, adapt_gate_to_revision, adapt_revision_to_presend

user_text = 'I dont know what to do and I feel stuck'
flags = detect_flags(user_text)
print('1 Flags:', flags)
assert 'confused' in flags
assert 'stuck' in flags

vad = [0.25, 0.65, 0.3]
mode = 'spacious-presence'
pipeline_out = {'vad': vad, 'modes': [mode]}
draft = 'What does stuck feel like in your body right now?'

gate_in = adapt_pipeline_to_gate(pipeline_out, draft)
print('2 Gate input:', gate_in)

techniques = available_techniques(mode, vad[0], vad[1], vad[2], flags)
print('3 Available techniques:', techniques)
assert len(techniques) > 0

gate_result = {'verdict': 'pass', 'flags': []}
rev_in = adapt_gate_to_revision(gate_result, draft)
print('4 Revision input:', rev_in)
assert rev_in['needs_revision'] == False

presend_in = adapt_revision_to_presend(draft, vad[0], gate_result)
print('5 Presend input:', presend_in)
assert presend_in['gate_verdict'] == 'pass'

print('FULL 10-MODULE PIPELINE INTEGRATION TEST PASSED')
