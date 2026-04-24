#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/continuity_of_mind')
try:
    from src.idle_goal_prompt import assemble_prompt
    p = assemble_prompt()
    checks = {
        'SOUL CONTEXT': 'SOUL CONTEXT' in p,
        'LANDSCAPE': 'LANDSCAPE' in p,
        'ACTIVE GOAL': 'ACTIVE GOAL' in p,
        'CREATIVE FUEL': 'CREATIVE FUEL' in p,
        'GENESIS': 'GENESIS' in p,
        'DIRECTION': 'DIRECTION' in p,
        'CONTEXT': 'CONTEXT' in p,
    }
    all_pass = all(checks.values())
    print('LENGTH:', len(p))
    print('ALL_SECTIONS_PRESENT:', all_pass)
    for k, v in checks.items():
        print(f'  {k}: {v}')
    if all_pass:
        print('VERDICT: PASS - all done-when criteria met')
    else:
        print('VERDICT: FAIL - missing sections:', [k for k,v in checks.items() if not v])
except Exception as e:
    print('ERROR:', e)
    import traceback
    traceback.print_exc()
