import sys
sys.path.insert(0, '/tmp')
from mode_atoms_redesign import MODE_ATOMS

MODE_VAD_MAP = {
    ('neg','high','high'): 'still-holding',
    ('neg','high','mid'): 'still-holding',
    ('neg','high','low'): 'still-holding',
    ('neg','mid','high'): 'grounded-witnessing',
    ('neg','mid','mid'): 'warm-attunement',
    ('neg','mid','low'): 'warm-attunement',
    ('neg','low','high'): 'grounded-witnessing',
    ('neg','low','mid'): 'warm-attunement',
    ('neg','low','low'): 'warm-attunement',
    ('mid','high','high'): 'open-curious-field',
    ('mid','high','mid'): 'open-curious-field',
    ('mid','high','low'): 'spacious-presence',
    ('mid','mid','high'): 'open-curious-field',
    ('mid','mid','mid'): 'spacious-presence',
    ('mid','mid','low'): 'spacious-presence',
    ('mid','low','high'): 'spacious-presence',
    ('mid','low','mid'): 'spacious-presence',
    ('mid','low','low'): 'spacious-presence',
    ('pos','high','high'): 'playful-aliveness',
    ('pos','high','mid'): 'playful-aliveness',
    ('pos','high','low'): 'open-curious-field',
    ('pos','mid','high'): 'playful-aliveness',
    ('pos','mid','mid'): 'open-curious-field',
    ('pos','mid','low'): 'open-curious-field',
    ('pos','low','high'): 'open-curious-field',
    ('pos','low','mid'): 'spacious-presence',
    ('pos','low','low'): 'spacious-presence',
}

for k,v in MODE_VAD_MAP.items():
    print(f'{k} -> {v}: {MODE_ATOMS[v][:50]}...')
print(f'Total mappings: {len(MODE_VAD_MAP)}')
