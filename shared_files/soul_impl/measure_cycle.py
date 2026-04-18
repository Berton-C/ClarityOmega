import sys
sys.path.insert(0, '/tmp/soul_impl')
import json
from live_web_bridge import live_web_check
from metta_driven_cycle import build_cycle_metta, identify_next_target

r = live_web_check({'total': 40, 'completed': 34}, 208, 29)
print('Web metric: f=', round(r['f'], 4), 'c=', round(r['c'], 4), 'status=', r['status'])

state = {'web_f': r['f'], 'web_c': r['c'], 'file_count': 88}
exprs = build_cycle_metta(state)
print('Cycle expressions:', len(exprs))

results = [
    {'name': 'autocatalytic-closure', 'f': 0.55, 'c': 0.4},
    {'name': 'observer-port', 'f': 0.85, 'c': 0.612},
    {'name': 'memory-seeding', 'f': 0.6, 'c': 0.5}
]
t = identify_next_target(results)
print('Next target:', t['name'], 'fc=', round(t['f'] * t['c'], 4))
