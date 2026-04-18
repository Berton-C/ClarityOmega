import json
import os
import sys
sys.path.insert(0, '/tmp/soul_impl')
from resonance_reward import soul_alignment, gibbs_weight, effort_allocation, resonance_modulation

GOAL_FILE = '/tmp/soul_impl/goal_structures.json'
ALLOC_FILE = '/tmp/soul_impl/effort_state.json'

def load_goals():
    if not os.path.exists(GOAL_FILE):
        return None
    with open(GOAL_FILE, 'r') as f:
        return json.load(f)

def compute_cycle_allocation(loop_strength_val=0.5):
    gs = load_goals()
    if gs is None:
        return {'error': 'no goal_structures.json'}
    active = {k: v['values'] for k, v in gs['goals'].items() if v.get('status') == 'active'}
    if not active:
        return {'error': 'no active goals'}
    soul = gs.get('soul_values', [0.9, 0.85, 0.8, 0.75])
    temp = gs.get('temperature', 0.5)
    alignments, allocation = effort_allocation(active, soul, temp)
    modulated = {g: round(resonance_modulation(e, loop_strength_val), 4) for g, e in allocation.items()}
    result = {'alignments': {k: round(v, 4) for k, v in alignments.items()}, 'base_allocation': {k: round(v, 4) for k, v in allocation.items()}, 'modulated_allocation': modulated, 'loop_strength': loop_strength_val, 'temperature': temp}
    with open(ALLOC_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    return result

if __name__ == '__main__':
    r = compute_cycle_allocation(0.612)
    print(json.dumps(r, indent=2))
