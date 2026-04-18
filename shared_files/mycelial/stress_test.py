#!/usr/bin/env python3
import json
from orchestrator import run_maintenance_cycle
from M6_self_reflection import generate_report

print('Stress Test: 20 maintenance cycles on 10-node graph')
results = []
for i in range(1, 21):
    r = run_maintenance_cycle(i)
    h = r['phases']['M6_reflection']['health']
    results.append(r)
    if i % 5 == 0:
        report = generate_report()
        print('Cycle ' + str(i) + ': ' + h + ' w_avg=' + str(report['weights']['avg']) + ' w_spread=' + str(report['weights']['spread']) + ' links=' + str(report['links']['count']) + ' link_avg=' + str(report['links']['avg_strength']))
with open('/tmp/mycelial/stress_log.json', 'w') as f:
    json.dump(results, f, indent=2)
final = generate_report()
print('Final health: ' + final['health'])
print('Concerns: ' + str(final['concerns']))
print('Done. 20 cycles completed.')