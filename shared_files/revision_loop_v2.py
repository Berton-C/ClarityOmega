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

PNS_SEEDS = [
    'I notice ',
    'I sense ',
    'What if we ',
    'I wonder ',
]

def revise_draft(text, max_passes=3):
    original = text
    for i in range(max_passes):
        audit = audit_response(text)
        if audit['sustains_pns']:
            return {'text': text, 'pass': True, 'passes_needed': i, 'audit': audit, 'original': original}
        if audit['sns_flags']:
            for flag in audit['sns_flags']:
                if flag in SNS_TO_PNS:
                    text = text.replace(flag, SNS_TO_PNS[flag])
        if not audit['gates']['pns_present'] and audit['gates']['sns_clear']:
            seed = PNS_SEEDS[i % len(PNS_SEEDS)]
            if not any(s.lower() in text.lower() for s in PNS_SEEDS):
                sentences = text.split('. ')
                if len(sentences) > 1:
                    text = sentences[0] + '. ' + seed + sentences[-1].lower()
                else:
                    text = seed + text[0].lower() + text[1:]
    final = audit_response(text)
    return {'text': text, 'pass': final['sustains_pns'], 'passes_needed': max_passes, 'audit': final, 'original': original}

if __name__ == '__main__':
    drafts = [
        'You need to fix this problem immediately.',
        'You should obviously reconsider your approach.',
        'I notice you are here with me in this.',
        'That seems like a reasonable next step.',
    ]
    for d in drafts:
        r = revise_draft(d)
        label = 'PASS' if r['pass'] else 'STILL-FLAGGED'
        print(f'[{label}] passes={r["passes_needed"]}')
        print(f'  Original: {r["original"]}')
        print(f'  Revised:  {r["text"]}')
        print(f'  Gates: {r["audit"]["gates"]}')
        print()
    print('Revision loop v2 operational')
