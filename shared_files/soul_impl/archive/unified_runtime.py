#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, '/tmp/soul_impl')
from felt_sense_pipeline_v3 import felt_sense_read_v3
from response_compass_runtime import evaluate_response

INPUT_FILE = '/tmp/soul_impl/unified_input.json'
OUTPUT_FILE = '/tmp/soul_impl/unified_output.json'

def run_unified():
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
    result = {'situation': situation, 'compass': compass}
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    run_unified()
