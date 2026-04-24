#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/continuity_of_mind/lib_candidates')

# Force reimport - no cache
if 'calibration_bridge' in sys.modules:
    del sys.modules['calibration_bridge']

import calibration_bridge
print('MODULE FILE:', calibration_bridge.__file__)
print('DB PATH:', calibration_bridge.CALIBRATION_DB_PATH)

from calibration_bridge import log_calibration_event, get_calibration_count

print('=== Calibration Bridge End-to-End Test ===')
print('Initial count:', get_calibration_count())

results = []
for i in range(5):
    tag = 'AGREE' if i % 2 == 0 else 'DISAGREE'
    outcome = 'agree' if i % 2 == 0 else 'disagree'
    r = log_calibration_event(outcome, tag=tag)
    results.append(r)
    print(f'  Event {i}: {outcome} -> {r}')

final_count = get_calibration_count()
print('Final count:', final_count)
has_error = any('ERROR' in str(r) for r in results)
print('Events logged successfully:', not has_error)
print('Count increased:', final_count >= 5)

if final_count >= 5 and not has_error:
    print('VERDICT: PASS - calibration_bridge.py works end-to-end')
else:
    print('VERDICT: FAIL')
    for r in results:
        if 'ERROR' in str(r):
            print('  ERROR:', r)
