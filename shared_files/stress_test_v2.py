#!/usr/bin/env python3
import sys, os
sys.path.insert(0, '/tmp')

TESTS = [
    ('I am having a panic attack right now', ['empathic-attunement']),
    ('feeling so grateful for everything', ['momentum-amplification']),
    ('I feel numb and broken inside', ['empathic-attunement']),
    ('just exhausted from work today', ['gentle-activation']),
    ('this inspired me so much', ['momentum-amplification']),
    ('I am frustrated but pushing through', ['empathic-attunement']),
    ('feeling at peace with things finally', ['momentum-amplification']),
    ('I hate myself and feel worthless', ['empathic-attunement']),
    ('over the moon about this news', ['momentum-amplification']),
    ('I am burned out and overwhelmed', ['empathic-attunement']),
    ('the weather is nice today', ['neutral-presence']),
    ('can you help me with my code', ['neutral-presence']),
    ('I am terrified of what comes next', ['empathic-attunement']),
    ('so proud of what we built', ['momentum-amplification']),
    ('fed up with all of this nonsense', ['empathic-attunement']),
]
passed = 0
failed = 0
for text, expected_has in TESTS:
    sf = '/tmp/backbone_state.json'
    if os.path.exists(sf):
        os.remove(sf)
    from backbone_workspace_v4 import BackboneWorkspace
    bw = BackboneWorkspace()
    r = bw.process_turn(text, 'user')
    modes = r['modes']
    boosts = r.get('boost_phrases', [])
    ok = any(e in modes for e in expected_has)
    status = 'PASS' if ok else 'FAIL'
    if ok: passed += 1
    else: failed += 1
    print(f'{status} | {text}')
    print(f'  VAD:{r["vad"]} modes:{modes} boosts:{boosts}')
    if not ok: print(f'  EXPECTED one of: {expected_has}')
    print('---')
print(f'Results: {passed}/{passed+failed} passed, {failed} failed')
