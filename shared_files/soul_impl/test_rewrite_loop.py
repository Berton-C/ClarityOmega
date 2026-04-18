import sys
sys.path.insert(0, '/tmp/soul_impl')
from rewrite_loop import RewriteLoop
import re

def sim_metta(expr):
    m = re.search(r'stv ([0-9.]+) ([0-9.]+).*stv ([0-9.]+) ([0-9.]+)', expr)
    if m:
        f1, c1, f2, c2 = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        return {'f': round(f1 * f2, 4), 'c': round(f1 * f2 * c1 * c2, 4)}
    return {'f': 0.5, 'c': 0.1}

rl = RewriteLoop(max_rewrites=2)
result = rl.start('You might consider exploring this fascinating pattern that opens new questions')
print('Start:', result['phase'], 'attempt:', result['attempt'], 'calls:', len(result['metta_calls']))
cycle = 0
while result['phase'] == 'scoring':
    metta_results = [sim_metta(c) for c in result['metta_calls']]
    result = rl.feed_metta_results(metta_results)
    cycle += 1
    if cycle > 15:
        break
print('After scoring:', result['phase'], 'attempt:', result.get('attempt'))
if result['phase'] == 'needs_rewrite':
    print('Low dims:', result['low_dims'])
    print('Rewrite prompt preview:', result['rewrite_prompt'][:150])
    result = rl.submit_rewrite('Here is a rewritten draft with better coverage of all dimensions consider exploring and think about')
    while result['phase'] == 'scoring':
        metta_results = [sim_metta(c) for c in result['metta_calls']]
        result = rl.feed_metta_results(metta_results)
print('Final phase:', result['phase'])
print('Done:', rl.is_done())
if rl.is_done():
    r = rl.get_result()
    print('Attempts:', r['attempts'], 'History entries:', len(r['history']))
print('REWRITE LOOP TEST PASSED')
