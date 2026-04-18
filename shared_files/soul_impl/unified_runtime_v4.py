#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, '/tmp/soul_impl')
from felt_sense_pipeline_v3 import felt_sense_read_v3
from compass_metta_evaluator import evaluate_with_metta
from accumulator import load_field as acc_load_field
from state_serializer import save_field, load_field, log_exchange, save_meta
from resonance_runtime_bridge import compute_cycle_allocation
from web_detector import loop_strength

INPUT_FILE = '/tmp/soul_impl/unified_input.json'
OUTPUT_FILE = '/tmp/soul_impl/unified_output.json'

def extract_compass_scores(situation):
    scalar = situation.get('felt_sense_scalar', 0.5)
    mode = situation.get('presence_mode', 'attending')
    agency = min(1.0, scalar / 3.0) if mode in ('engaged', 'collaborative') else 0.4
    wonder = 0.7 if mode == 'curious' else (0.5 if scalar > 1.5 else 0.3)
    quality = min(1.0, scalar / 2.5)
    honesty = 0.85
    return {'agency': round(agency, 3), 'wonder': round(wonder, 3), 'quality': round(quality, 3), 'honesty': round(honesty, 3)}

def get_loop_strength():
    try:
        links = [(0.9, 0.8), (0.85, 0.75), (0.9, 0.67)]
        result = loop_strength(links)
        return result[0] if isinstance(result, (list, tuple)) else result
    except Exception:
        return 0.5

def run_unified_v4(metta_fn=None):
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
    user_message = data.get('user_message', '')
    memory_texts = data.get('memory_texts', [])
    draft_response = data.get('draft_response', '')
    def mem_fn(phrases):
        return memory_texts
    situation = felt_sense_read_v3(user_message, accumulate=True, memory_query_fn=mem_fn)
    compass = {}
    if draft_response or user_message:
        sit_scores = extract_compass_scores(situation)
        compass = evaluate_with_metta(sit_scores, metta_fn=metta_fn)
    ls_val = get_loop_strength()
    effort = compute_cycle_allocation(ls_val)
    field_vec = acc_load_field()
    save_field(field_vec, {'last_mode': situation.get('presence_mode',''), 'last_scalar': situation.get('felt_sense_scalar',0)})
    log_exchange(user_message, situation, compass if compass else None)
    save_meta(goal_count=14, exchange_count=0, notes='v4 runtime with resonance-reward integration')
    result = {'situation': situation, 'compass': compass, 'effort_allocation': effort, 'loop_strength': ls_val, 'persisted': True, 'engine': 'metta-nal-resonance'}
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    run_unified_v4()
