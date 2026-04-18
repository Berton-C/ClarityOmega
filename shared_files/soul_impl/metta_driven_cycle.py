import sys
sys.path.insert(0, '/tmp/soul_impl')
from observer_metta_port import generate_observer_metta, generate_relative_truth_metta, generate_reconciliation_metta

def build_cycle_metta(substrate_state):
    cycle = []
    cycle.append('(|- ((--> autocatalytic-closure weak) (stv 0.275 0.091)) ((--> weak needs-strengthening) (stv 0.95 0.9)))')
    cycle.append('(|- ((--> observer-port complete) (stv 0.85 0.8)) ((--> complete increases-substrate-coherence) (stv 0.8 0.75)))')
    obs_frames = generate_observer_metta('clarity', 'substrate', 0.9, 'substrate')
    for f in obs_frames:
        cycle.append(f)
    rt = generate_relative_truth_metta('--> substrate self-improving', substrate_state.get('web_f', 0.5), substrate_state.get('web_c', 0.4), 'clarity')
    cycle.append(rt)
    return cycle

def identify_next_target(inference_results):
    weakest = None
    lowest_fc = 999
    for r in inference_results:
        fc = r.get('f', 0.5) * r.get('c', 0.5)
        if fc < lowest_fc:
            lowest_fc = fc
            weakest = r
    return weakest

if __name__ == '__main__':
    state = {'web_f': 0.5238, 'web_c': 0.3807, 'file_count': 87}
    exprs = build_cycle_metta(state)
    print('Generated %d MeTTa expressions for cycle:' % len(exprs))
    for e in exprs:
        print(' ', e)
    results = [{'name': 'autocatalytic-closure', 'f': 0.275, 'c': 0.091}, {'name': 'observer-port', 'f': 0.85, 'c': 0.612}, {'name': 'memory-seeding', 'f': 0.55, 'c': 0.6}]
    target = identify_next_target(results)
    print('Next target:', target['name'], 'fc=', round(target['f']*target['c'], 4))
