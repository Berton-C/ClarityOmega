import json
import sys
sys.path.insert(0, '/tmp/soul_impl')
from cycle_orchestrator import generate_cycle_batch
from metta_result_closer import close_cycle

def test_full_cycle():
    print('=== FULL CYCLE INTEGRATION TEST ===')
    batch = generate_cycle_batch('What is consciousness?')
    assert 'situation' in batch
    assert 'metta_expressions' in batch
    assert len(batch['metta_expressions']) == 4
    print('Batch generated:', batch['engine'])
    print('Scores:', batch['scores'])
    print('Loop strength:', batch['loop_strength'])
    for dim, expr in batch['metta_expressions']:
        print(f'  {dim}: {expr[:60]}')
    sim = [('agency', '(stv 0.34 0.19)'), ('wonder', '(stv 0.24 0.13)'), ('quality', '(stv 0.41 0.22)'), ('honesty', '(stv 0.765 0.44)')]
    closed = close_cycle(sim)
    assert 'scores' in closed
    assert 'flagged' in closed
    print('Closed loop engine:', closed['engine'])
    print('Flagged:', closed['flagged'])
    print('Passed:', closed['passed'])
    with open('/tmp/soul_impl/effort_state.json', 'r') as f:
        es = json.load(f)
    assert 'modulated_allocation' in es
    print('Effort persisted:', list(es.keys()))
    print('=== ALL ASSERTIONS PASSED ===')
    return True

if __name__ == '__main__':
    test_full_cycle()
