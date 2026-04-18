import sys
sys.path.insert(0, '/tmp')
from pipeline_orchestrator import run_pipeline

# Edge 1: Non-technique mode should return empty techniques
r1 = run_pipeline('I feel sad', [0.2, 0.3, 0.2], 'still-holding', 'I am here with you.')
print('Edge1 techniques:', r1['techniques'])
assert r1['techniques'] == []
assert r1['send'] == True

# Edge 2: Calcified pattern with low dominance
r2 = run_pipeline('It is always like this and never changes', [0.2, 0.5, 0.2], 'spacious-presence', 'What if it could be different?')
print('Edge2 flags:', r2['flags'])
print('Edge2 techniques:', r2['techniques'])
assert 'calcified' in r2['flags']
assert 'exaggerated-agreement' in r2['techniques']

# Edge 3: Externalized blame
r3 = run_pipeline('They made me fail because of their mistakes', [0.3, 0.6, 0.4], 'open-curious-field', 'What part of this is yours to shape?')
print('Edge3 flags:', r3['flags'])
assert 'externalized' in r3['flags']
assert 'public-context-reframe' in r3['techniques']

# Edge 4: No flags defaults to dojo
r4 = run_pipeline('I had a nice walk today', [0.7, 0.4, 0.6], 'playful-aliveness', 'That sounds lovely.')
print('Edge4 techniques:', r4['techniques'])
assert 'dojo-of-no-direction' in r4['techniques']

print('ALL ORCHESTRATOR EDGE TESTS PASSED')
