#!/usr/bin/env python3
import json
from datetime import datetime
from M5_temporal_decay import run_decay_cycle
from M6_self_reflection import generate_report
from M3_synthesizer import run_synthesis_cycle
from M1_weight_manager import load_weights
from M3_cluster_detector import load_links, build_adjacency

def run_maintenance_cycle(cycle_num=1):
    results = {'cycle': cycle_num, 'timestamp': datetime.now().isoformat(), 'phases': {}}
    wc, lc = run_decay_cycle()
    results['phases']['M5_decay'] = {'weight_changes': len(wc), 'link_changes': len(lc)}
    all_c, syntheses = run_synthesis_cycle(quorum_threshold=0.25)
    results['phases']['M3_synthesis'] = {'clusters': len(all_c), 'new_syntheses': len(syntheses)}
    report = generate_report()
    results['phases']['M6_reflection'] = {'health': report['health'], 'concerns': report['concerns']}
    return results

def run_n_cycles(n=3):
    all_results = []
    for i in range(1, n+1):
        r = run_maintenance_cycle(i)
        all_results.append(r)
        print('Cycle ' + str(i) + ': health=' + r['phases']['M6_reflection']['health'] + ' decay_w=' + str(r['phases']['M5_decay']['weight_changes']) + ' synth=' + str(r['phases']['M3_synthesis']['new_syntheses']))
    with open('/tmp/mycelial/orchestration_log.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    return all_results

if __name__ == '__main__':
    print('Orchestration Loop - 3 maintenance cycles')
    run_n_cycles(3)
    print('Complete. Log at orchestration_log.json')
