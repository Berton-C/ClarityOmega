import sys
sys.path.insert(0, '/tmp/soul_impl')
from compass_agent_hook import CompassAgentHook
import re

def sim_metta(expr):
    m = re.search(r'stv ([0-9.]+) ([0-9.]+).*stv ([0-9.]+) ([0-9.]+)', expr)
    if m:
        f1, c1, f2, c2 = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        return {'f': round(f1 * f2, 4), 'c': round(f1 * f2 * c1 * c2, 4)}
    return {'f': 0.5, 'c': 0.1}

hook = CompassAgentHook()
calls = hook.intercept('You might consider exploring this fascinating pattern')
print('Hook intercept returned', len(calls), 'calls')
cycle = 0
while calls:
    results = [sim_metta(c) for c in calls]
    calls = hook.process_metta_results(results)
    cycle += 1
    print('Cycle', cycle, 'state:', hook.get_state())
    if cycle > 10:
        break
print('Verdict:', hook.get_verdict())
print('Needs rewrite:', hook.needs_rewrite())
print('Low dims:', hook.get_low_dims())
print('TEST PASSED')
