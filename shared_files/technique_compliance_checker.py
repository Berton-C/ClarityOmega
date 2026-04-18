import sys
sys.path.insert(0, '/tmp')
from technique_execution_templates import get_template

def check_compliance(draft, technique_name):
    t = get_template(technique_name)
    issues = []
    if t['shape'] == 'short' and len(draft) > 120:
        issues.append('too-long-for-short-shape')
    if t['shape'] == 'medium' and len(draft) > 300:
        issues.append('too-long-for-medium-shape')
    if 'advice' in t['avoids'] and 'you should' in draft.lower():
        issues.append('contains-advice')
    if 'reframe' in t['avoids'] and 'but actually' in draft.lower():
        issues.append('contains-reframe')
    if 'questions-over-2' in t['avoids'] and draft.count('?') > 2:
        issues.append('too-many-questions')
    if 'sarcasm' in t['avoids'] and 'obviously' in draft.lower():
        issues.append('possible-sarcasm')
    if 'dismissal' in t['avoids'] and 'just' in draft.lower().split():
        issues.append('possible-dismissal')
    if 'toxic-positivity' in t['avoids'] and 'at least' in draft.lower():
        issues.append('possible-toxic-positivity')
    return {'compliant': len(issues) == 0, 'issues': issues}

if __name__ == '__main__':
    r1 = check_compliance('What does that feel like?', 'dojo-of-no-direction')
    print('Dojo short OK:', r1)
    assert r1['compliant']
    r2 = check_compliance('You should really try meditation and also you should journal and here is a very long explanation of why this matters and how it connects to everything', 'dojo-of-no-direction')
    print('Dojo violations:', r2)
    assert not r2['compliant']
    assert 'too-long-for-short-shape' in r2['issues']
    assert 'contains-advice' in r2['issues']
    r3 = check_compliance('Yes absolutely everything is terrible and nothing will ever change and this is the worst!', 'exaggerated-agreement')
    print('Exaggerated OK:', r3)
    assert r3['compliant']
    r4 = check_compliance('At least things could be worse right?', 'temporal-shift')
    print('Temporal toxic-pos:', r4)
    assert 'possible-toxic-positivity' in r4['issues']
    print('TECHNIQUE COMPLIANCE CHECKER ALL TESTS PASSED')
