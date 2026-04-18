import sys
sys.path.insert(0, '/tmp/soul_impl')
from harness_with_bridge import run_cycle

results = [
    ('web', [[['-->', 'w', 's'], ['stv', 0.392, 0.1176]]]),
    ('memory', [[['-->', 'm', 'l'], ['stv', 0.42, 0.1365]]]),
    ('closure', [[['-->', 'c', 'v'], ['stv', 0.44, 0.132]]]),
    ('harness', [[['-->', 'h', 'c'], ['stv', 0.68, 0.3808]]]),
    ('observer', [[['-->', 'o', 'r'], ['stv', 0.765, 0.544]]]),
    ('bridge', [[['-->', 'b', 's'], ['stv', 0.855, 0.648]]])
]

r = run_cycle(results)
print('Cycle', r['cycle'], 'Weakest:', r['weakest'])
for c in r['history'][-1]['components']:
    print('  %s: fc=%s' % (c['name'], c['fc']))
