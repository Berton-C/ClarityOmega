import sys

VAD_PROFILES = {
    'frustrated': ('neg', 'high', 'low'),
    'excited': ('pos', 'high', 'high'),
    'flat': ('mid', 'low', 'mid'),
    'withdrawn': ('neg', 'low', 'low'),
    'collaborative': ('pos', 'mid', 'high'),
}

CASE_BRANCHES = ' '.join([
    '((neg high low) prioritize-validation)',
    '((pos high high) amplify-momentum)',
    '((mid low mid) small-prompts-warmth)',
    '((neg low low) gentle-activation-reframe)',
    '((pos mid high) collaborative-ideation)',
])

def build_metta_case(v, a, d):
    return f'(case ({v} {a} {d}) ({CASE_BRANCHES}))'

if __name__ == '__main__':
    for name, (v, a, d) in VAD_PROFILES.items():
        expr = build_metta_case(v, a, d)
        print(f'{name}: {expr}')
