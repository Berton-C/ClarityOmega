import sys
sys.path.insert(0, '/tmp')
from mode_vad_mapping import MODE_VAD_MAP
from mode_atoms_redesign import MODE_ATOMS

test_cases = [
    (('neg','high','low'), 'still-holding', 'angry and helpless'),
    (('neg','low','low'), 'warm-attunement', 'withdrawn depleted'),
    (('mid','mid','mid'), 'spacious-presence', 'neutral checking in'),
    (('pos','high','high'), 'playful-aliveness', 'excited and empowered'),
    (('mid','high','high'), 'open-curious-field', 'energized exploring'),
    (('neg','mid','high'), 'grounded-witnessing', 'frustrated but capable'),
]

passed = 0
for vad, expected_mode, label in test_cases:
    mode = MODE_VAD_MAP.get(vad, 'spacious-presence')
    guidance = MODE_ATOMS[mode]
    ok = mode == expected_mode
    if ok: passed += 1
    print(f"{'PASS' if ok else 'MISS'} {label}: {vad} -> {mode} | {guidance[:60]}...")
print(f"\n{passed}/{len(test_cases)} passed")
