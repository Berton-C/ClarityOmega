import sys
sys.path.insert(0, '/tmp')
from pipeline_adapter import adapt_pipeline_to_gate
from technique_router import available_techniques

# Simulate: pipeline detects low arousal confused user in spacious-presence mode
pipeline_out = {'vad': [0.2, 0.3, 0.2], 'modes': ['spacious-presence']}
draft = 'What does that feel like right now?'
gate_in = adapt_pipeline_to_gate(pipeline_out, draft)
print('Gate input:', gate_in)

# Route to available techniques
techniques = available_techniques(
    gate_in['primary_mode'],
    gate_in['valence'],
    pipeline_out['vad'][1],
    pipeline_out['vad'][2],
    ['confused']
)
print('Available techniques:', techniques)
assert 'socratic-inquiry' in techniques

# High arousal stuck in playful-aliveness
t2 = available_techniques('playful-aliveness', 0.3, 0.8, 0.3, ['stuck'])
print('Stuck techniques:', t2)
assert 'parable-sudden-contrast' in t2

# Non-technique mode returns empty
t3 = available_techniques('still-holding', 0.2, 0.3, 0.2, ['confused'])
print('Still-holding techniques:', t3)
assert t3 == []

print('FULL PIPELINE WITH TECHNIQUE ROUTING TEST PASSED')