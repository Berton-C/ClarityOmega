import sys

def discretize_vad(v, a, d):
    vl = 'neg' if v < -0.5 else ('pos' if v > 0.5 else 'mid')
    al = 'high' if a > 0.5 else ('low' if a < -0.5 else 'mid')
    dl = 'high' if d > 0.3 else ('low' if d < -0.3 else 'mid')
    return vl, al, dl

CASE_BRANCHES = ' '.join([
    '((neg high low) prioritize-validation)',
    '((pos high high) amplify-momentum)',
    '((mid low mid) small-prompts-warmth)',
    '((neg low low) gentle-activation-reframe)',
    '((pos mid high) collaborative-ideation)',
])

ACTION_PROMPTS = {
    'prioritize-validation': 'Acknowledge frustration directly. Reflect feelings before offering solutions.',
    'amplify-momentum': 'Match their energy. Build on excitement. Channel into concrete steps.',
    'small-prompts-warmth': 'Gentle open-ended questions. Do not push. Offer small warmth signals.',
    'gentle-activation-reframe': 'Very gentle approach. Tiny anchors. Normalize without judgment.',
    'collaborative-ideation': 'Engage as thinking partner. Yes-and framing. Probing questions.',
    'neutral-presence': 'Be present and attentive. Follow their lead. Respond with empathy.',
}

def build_metta_expr(v, a, d):
    vl, al, dl = discretize_vad(v, a, d)
    return '(case (%s %s %s) (%s))' % (vl, al, dl, CASE_BRANCHES)

def get_action_prompt(action_atom):
    return ACTION_PROMPTS.get(action_atom, ACTION_PROMPTS['neutral-presence'])

if __name__ == '__main__':
    tests = [(-2.1, 1.5, -0.8), (1.2, 1.8, 0.9), (0.1, -1.2, 0.0), (-1.0, -1.5, -0.8), (0.8, 0.3, 0.7)]
    labels = ['frustrated', 'excited', 'flat', 'withdrawn', 'collaborative']
    for label, vad in zip(labels, tests):
        v, a, d = vad
        vl, al, dl = discretize_vad(v, a, d)
        expr = build_metta_expr(v, a, d)
        prompt = get_action_prompt(label.replace('frustrated','prioritize-validation').replace('excited','amplify-momentum').replace('flat','small-prompts-warmth').replace('withdrawn','gentle-activation-reframe').replace('collaborative','collaborative-ideation'))
        print('%s VAD=(%s,%s,%s) -> (%s,%s,%s)' % (label, v, a, d, vl, al, dl))
        print('  MeTTa: %s' % expr)
        print('  Prompt: %s' % prompt)
        print()
