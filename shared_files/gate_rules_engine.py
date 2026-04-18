import json
import re

def load_rules(path):
    with open(path) as f:
        return json.load(f)

def evaluate_rule(rule, context):
    cond = rule['condition']
    if 'valence < 0.2 and len_draft > 80' in cond:
        return context.get('valence', 1.0) < 0.2 and len(context.get('draft', '')) > 80
    if 'calcified in flags and exclaim in draft' in cond:
        return 'calcified' in context.get('flags', []) and '!' in context.get('draft', '')
    if 'mode == still-holding and should in draft' in cond:
        return context.get('mode', '') == 'still-holding' and 'should' in context.get('draft', '').lower()
    if 'question_count > 2' in cond:
        return context.get('draft', '').count('?') > 2
    return False

def apply_action(action, draft):
    if action == 'truncate':
        return draft[:60].rsplit(' ', 1)[0] + '...'
    if action == 'soften':
        return draft.replace('!', '.')
    if action == 'remove-should':
        return re.sub(r'(?i)\byou should\b', 'you might', draft)
    if action == 'reduce-questions':
        parts = draft.split('?')
        if len(parts) > 3:
            return '?'.join(parts[:2]) + '?'
        return draft
    return draft

def run_gate(draft, context, rules_path='/tmp/gate_rules.json'):
    rules = load_rules(rules_path)
    for rule in rules:
        if evaluate_rule(rule, {**context, 'draft': draft}):
            revised = apply_action(rule['action'], draft)
            return {'verdict': 'revised', 'rule': rule['name'], 'draft': revised}
    return {'verdict': 'pass', 'rule': None, 'draft': draft}

if __name__ == '__main__':
    c1 = {'valence': 0.1, 'flags': [], 'mode': 'still-holding'}
    r1 = run_gate('This is a very long response that keeps going and going about many things beyond what anyone needs here', c1)
    print('R1:', r1['verdict'], r1['rule'])
    assert r1['verdict'] == 'revised'
    c2 = {'valence': 0.5, 'flags': ['calcified'], 'mode': 'spacious-presence'}
    r2 = run_gate('You must change now!', c2)
    print('R2:', r2['verdict'], r2['rule'])
    assert '!' not in r2['draft']
    c3 = {'valence': 0.5, 'flags': [], 'mode': 'still-holding'}
    r3 = run_gate('You should try harder and you should rest', c3)
    print('R3:', r3['verdict'], r3['draft'])
    assert 'you might' in r3['draft'].lower()
    c4 = {'valence': 0.6, 'flags': [], 'mode': 'open-curious-field'}
    r4 = run_gate('What now? Why here? How come? Where next?', c4)
    print('R4:', r4['verdict'], r4['draft'])
    assert r4['draft'].count('?') <= 2
    c5 = {'valence': 0.7, 'flags': [], 'mode': 'playful-aliveness'}
    r5 = run_gate('That sounds great.', c5)
    assert r5['verdict'] == 'pass'
    print('ALL GATE RULES ENGINE TESTS PASSED')
