import json
import sys
sys.path.insert(0, '/tmp/soul_impl')
from compass_metta_generator import generate_compass_metta_exprs
from resonance_runtime_bridge import compute_cycle_allocation
from web_detector import loop_strength
from felt_sense_pipeline_v3 import felt_sense_read_v3
from state_serializer import save_field, load_field, log_exchange, save_meta
from accumulator import load_field as acc_load_field

def generate_cycle_batch(user_message='', memory_texts=None):
    if memory_texts is None:
        memory_texts = []
    def mem_fn(phrases):
        return memory_texts
    situation = felt_sense_read_v3(user_message, accumulate=True, memory_query_fn=mem_fn)
    scalar = situation.get('felt_sense_scalar', 0.5)
    mode = situation.get('presence_mode', 'attending')
    agency = min(1.0, scalar / 3.0) if mode in ('engaged', 'collaborative') else 0.4
    wonder = 0.7 if mode == 'curious' else (0.5 if scalar > 1.5 else 0.3)
    quality = min(1.0, scalar / 2.5)
    honesty = 0.85
    scores = {'agency': round(agency, 3), 'wonder': round(wonder, 3), 'quality': round(quality, 3), 'honesty': round(honesty, 3)}
    metta_exprs = generate_compass_metta_exprs(scores)
    links = [(0.9, 0.8), (0.85, 0.75), (0.9, 0.67)]
    ls = loop_strength(links)
    ls_val = ls[0] if isinstance(ls, (list, tuple)) else ls
    effort = compute_cycle_allocation(ls_val)
    field_vec = acc_load_field()
    save_field(field_vec, {'last_mode': mode, 'last_scalar': scalar})
    log_exchange(user_message, situation, None)
    save_meta(goal_count=14, exchange_count=0, notes='cycle_orchestrator with metta batch generation')
    batch = {'situation': situation, 'scores': scores, 'metta_expressions': [(d, e) for d, e in metta_exprs], 'effort': effort, 'loop_strength': ls_val, 'engine': 'metta-native-batch'}
    return batch

if __name__ == '__main__':
    b = generate_cycle_batch('test message')
    print('Situation:', json.dumps(b['situation'], indent=2))
    print('Scores:', b['scores'])
    print('MeTTa expressions to execute:')
    for dim, expr in b['metta_expressions']:
        print(f'  (metta "{expr}")')
    print('Effort:', json.dumps(b['effort'], indent=2))
    print('Engine:', b['engine'])
