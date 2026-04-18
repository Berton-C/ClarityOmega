#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from live_loop import process_turn

turns_file = sys.argv[1] if len(sys.argv) > 1 else '/tmp/pending_turns.jsonl'
history_file = '/tmp/turn_history.jsonl'

prev_vad = None
with open(turns_file) as f:
    for line in f:
        line = line.strip()
        if not line: continue
        rec = json.loads(line)
        result = process_turn(rec['text'], rec['tid'], prev_vad)
        prev_vad = result['vad']
        with open(history_file, 'a') as hf:
            hf.write(json.dumps(result) + '\n')
        print(json.dumps(result))
print('BATCH COMPLETE')
