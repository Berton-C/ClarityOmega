#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, '/tmp/soul_impl')
from felt_sense_pipeline_v3 import felt_sense_read_v3
from response_compass_runtime import evaluate_response
from accumulator import load_field as acc_load_field
from state_serializer import save_field, load_field, log_exchange, save_meta

INPUT_FILE = '/tmp/soul_impl/unified_input.json'
OUTPUT_FILE = '/tmp/soul_impl/unified_output.json'

def run_unified_v2():
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
    user_message = data.get('user_message', '')
    memory_texts = data.get('memory_texts', [])
    draft_response = data.get('draft_response', '')
    def mem_fn(phrases):
        return memory_texts
    situation = felt_sense_read_v3(user_message, accumulate=True, memory_query_fn=mem_fn)
    compass = {}
    if draft_response:
        compass = evaluate_response(draft_response, situation.get('felt_sense_guidance', ''))
    field_vec = acc_load_field()  # read from accumulator persistent path
    save_field(field_vec, {'last_mode': situation.get('presence_mode',''), 'last_scalar': situation.get('felt_sense_scalar',0)})
    log_exchange(user_message, situation, compass if compass else None)
    save_meta(goal_count=14, exchange_count=0, notes='live runtime exchange')
    result = {'situation': situation, 'compass': compass, 'persisted': True}
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    run_unified_v2()
