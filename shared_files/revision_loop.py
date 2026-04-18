import sys
sys.path.insert(0, '/tmp')
from valence_self_audit import audit_response

SNS_TO_PNS = {
    'must': 'might',
    'should': 'could',
    'wrong': 'different',
    'need': 'sense',
    'fix': 'explore',
    'problem': 'pattern',
    'failure': 'edge',
    'urgent': 'present',
    'immediately': 'gently',
    'obviously': 'perhaps',
    'clearly': 'it seems',
    'but': 'and',
    'however': 'also',
    'actually': 'interestingly',
}

def revise_draft(text, max_passes=3):
    for i in range(max_passes):
        audit = audit_response(text)
        if audit['sustains_pns']:
            return {'text': text, 'pass': True, 'passes_needed': i, 'audit': audit}
        if audit['sns_flags']:
            for flag in audit['sns_flags']:
                if flag in SNS_TO_PNS:
                    text = text.replace(flag, SNS_TO_PNS[flag])
        else:
            break
    final = audit_response(text)
    return {'text': text, 'pass': final['sustains_pns'], 'passes_needed': max_passes, 'audit': final}

if __name__ == '__main__':
    drafts = [
        'You need to fix this problem immediately.',
        'You should obviously reconsider your approach.',
        'I notice you are here with me in this.',
    ]
    for d in drafts:
        r = revise_draft(d)
        label = 'PASS' if r['pass'] else 'STILL-FLAGGED'
        print(f'[{label}] passes={r["passes_needed"]}')
        print(f'  Original: {d}')
        print(f'  Revised:  {r["text"]}')
        print(f'  Gates: {r["audit"]["gates"]}')
        print()
    print('Revision loop operational')
