import sys
sys.path.insert(0, '/tmp/soul_impl')
from harness_with_bridge import run_cycle
from web_fc_bridge import get_web_fc

web_fc = get_web_fc()
web_f = 0.75 if web_fc > 0.5 else 0.392
web_c = web_fc / web_f if web_f > 0 else 0.1

results = [
    ('web', [['-->', 'w', 's'], ['stv', round(web_f, 3), round(web_c, 4)]]),
    ('memory', [['-->', 'm', 'l'], ['stv', 0.42, 0.1365]]),
    ('closure', [['-->', 'c', 'v'], ['stv', 0.44, 0.132]]),
    ('harness', [['-->', 'h', 'c'], ['stv', 0.68, 0.3808]]),
    ('observer', [['-->', 'o', 'r'], ['stv', 0.765, 0.544]]),
    ('bridge', [['-->', 'b', 's'], ['stv', 0.855, 0.648]])
]

r = run_cycle(results)
print('Cycle', r['cycle'], 'Weakest:', r['weakest'])
for c in r['history'][-1]['components']:
    print('  %s: fc=%s' % (c['name'], c['fc']))
