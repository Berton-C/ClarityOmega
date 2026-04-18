#!/usr/bin/env python3
import json
from datetime import datetime
from M5_temporal_decay import run_decay_cycle
from M3_synthesizer import run_synthesis_cycle
from M6_self_reflection import generate_report
from M7_link_reinforcer import reinforce_coretrieval
from M8_wonder_preservation import WonderPreservation

SIMULATED_RETRIEVALS = [
    ['g1','g2','br1'],
    ['br1','b1'],
    ['m1','m2','m3'],
    ['e1','e2'],
    ['g1','br1','b1']
]

def run_orchestration_cycle(cycle_num, log, wonder_gate):
    entry = {'cycle': cycle_num, 'time': datetime.now().isoformat()}
    decay_result = run_decay_cycle()
    entry['decay'] = decay_result
    retrieved = SIMULATED_RETRIEVALS[cycle_num % len(SIMULATED_RETRIEVALS)]
    reinforced = reinforce_coretrieval(retrieved, boost=0.03)
    entry['reinforcement'] = {'retrieved': retrieved, 'links_reinforced': len(reinforced)}
    all_c, syntheses, blocked = run_synthesis_cycle(quorum_threshold=0.25, wonder_gate=wonder_gate)
    entry['synthesis'] = {'clusters': len(all_c), 'syntheses_generated': len(syntheses), 'wonder_blocked': len(blocked)}
    reflection = generate_report()
    entry['reflection'] = reflection
    log.append(entry)
    return entry

def run_full_orchestration(cycles=20):
    wonder_gate = WonderPreservation()
    log = []
    for i in range(cycles):
        e = run_orchestration_cycle(i, log, wonder_gate)
        if (i+1) % 5 == 0:
            print('Cycle', i+1, ':', e['reflection'].get('health','?'), 'wonder_blocked', e['synthesis']['wonder_blocked'])
    with open('/tmp/mycelial/orchestration_v2_log.json', 'w') as f:
        json.dump(log, f, indent=2)
    print('Done.', cycles, 'cycles logged.')
    return log

if __name__ == '__main__':
    run_full_orchestration(20)
