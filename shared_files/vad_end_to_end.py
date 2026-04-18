import sys

CASE_BRANCHES = ' '.join([
    '((neg high low) prioritize-validation)',
    '((pos high high) amplify-momentum)',
    '((mid low mid) small-prompts-warmth)',
    '((neg low low) gentle-activation-reframe)',
    '((pos mid high) collaborative-ideation)',
])

ACTION_PROMPTS = {
    'prioritize-validation': 'Acknowledge their frustration directly. Reflect what they are feeling before offering any solutions. Use phrases like I hear you and that sounds really difficult.',
    'amplify-momentum': 'Match their energy. Build on their excitement. Ask what they want to do next and help them channel this momentum into concrete steps.',
    'small-prompts-warmth': 'Use gentle open-ended questions. Do not push. Offer small warmth signals. Try what is on your mind right now or I am here whenever you are ready.',
    'gentle-activation-reframe': 'Very gentle approach. Do not force engagement. Offer tiny anchors like I noticed you are here and that matters. Normalize their withdrawal without judgment.',
    'collaborative-ideation': 'Engage as a thinking partner. Build on their ideas. Use yes-and framing. Ask probing questions that deepen their exploration.',
}

def get_metta_expr(v, a, d):
    return f'(case ({v} {a} {d}) ({CASE_BRANCHES}))'

def get_prompt(action_atom):
    return ACTION_PROMPTS.get(action_atom, 'Respond with empathy and presence.')

if __name__ == '__main__':
    profiles = {
        'frustrated': ('neg', 'high', 'low'),
        'excited': ('pos', 'high', 'high'),
        'flat': ('mid', 'low', 'mid'),
        'withdrawn': ('neg', 'low', 'low'),
        'collaborative': ('pos', 'mid', 'high'),
    }
    actions = {
        'frustrated': 'prioritize-validation',
        'excited': 'amplify-momentum',
        'flat': 'small-prompts-warmth',
        'withdrawn': 'gentle-activation-reframe',
        'collaborative': 'collaborative-ideation',
    }
    for name in profiles:
        v, a, d = profiles[name]
        action = actions[name]
        prompt = get_prompt(action)
        print(f'{name} -> {action}')
        print(f'  PROMPT: {prompt[:80]}...')
        print()
