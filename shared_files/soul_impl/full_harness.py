import sys
sys.path.insert(0, '/tmp/soul_impl')
import json
from live_web_bridge import live_web_check
from metta_driven_cycle import build_cycle_metta, identify_next_target
from autocatalytic_closer import close_loop
from observer_metta_port import generate_observer_metta, generate_relative_truth_metta

print('=== FULL HARNESS CYCLE ===')
print()

# 1. Measure current web metric
r = live_web_check({'total': 40, 'completed': 34}, 208, 29)
print('1. WEB METRIC: f=%s c=%s status=%s' % (round(r['f'],4), round(r['c'],4), r['status']))
print('   Gap to threshold: %s' % round(r.get('gap',0),4))
print()

# 2. Generate MeTTa cycle expressions
state = {'web_f': r['f'], 'web_c': r['c'], 'file_count': 88}
exprs = build_cycle_metta(state)
print('2. METTA EXPRESSIONS GENERATED:', len(exprs))
for e in exprs:
    print('   ', e)
print()

# 3. Simulate inference results and identify weakest
results = [
    {'name': 'autocatalytic-closure', 'f': 0.55, 'c': 0.4},
    {'name': 'observer-port', 'f': 0.85, 'c': 0.612},
    {'name': 'memory-seeding', 'f': 0.6, 'c': 0.5},
    {'name': 'memory-goal-gen', 'f': 0.736, 'c': 0.636}
]
t = identify_next_target(results)
print('3. WEAKEST LINK:', t['name'], 'fc=', round(t['f']*t['c'],4))
print()

# 4. Run autocatalytic closer
completed = ['observer_metta_port.py', 'metta_driven_cycle.py', 'autocatalytic_closer.py', 'measure_cycle.py', 'full_harness.py']
current = ['Strengthen autocatalytic closure', 'Port more logic to native MeTTa', 'Build paraconsistent handler']
closure = close_loop(completed, current)
print('4. CLOSURE: strength=%s goals_seeded=%s memories=%s' % (closure['closure_strength'], closure['goals_seeded'], closure['memories_generated']))
print('   New goals:', closure['new_goals'][:3])
print()

# 5. Observer frame
frames = generate_observer_metta('clarity', 'harness-cycle', 0.9, 'substrate')
rt = generate_relative_truth_metta('--> substrate self-improving', r['f'], r['c'], 'clarity')
print('5. OBSERVER FRAME:', len(frames), 'expressions')
print('   Relative truth:', rt)
print()
print('=== HARNESS COMPLETE ===')
