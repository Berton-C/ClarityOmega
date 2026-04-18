#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, '/tmp/soul_impl')
from felt_sense_pipeline_v3 import felt_sense_read_v3
from memory_signal_parser import parse_memory_signals

INPUT_FILE = '/tmp/soul_impl/handoff_input.json'
OUTPUT_FILE = '/tmp/soul_impl/handoff_output.json'

def run_handoff():
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)
    user_message = data.get('user_message', '')
    memory_texts = data.get('memory_texts', [])
    def real_memory_fn(phrases):
        return memory_texts
    result = felt_sense_read_v3(user_message, accumulate=True, memory_query_fn=real_memory_fn)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    run_handoff()
