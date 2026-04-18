#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from live_loop import process_turn
from integrate_backbone import get_latest_guidance

def full_cycle(text, tid, history_file='/tmp/turn_history.jsonl'):
    prev_vad = None
    try:
        with open(history_file) as f:
            for line in f:
                if line.strip():
                    prev_vad = json.loads(line).get('vad')
    except FileNotFoundError:
        pass
    result = process_turn(text, tid, prev_vad)
    with open(history_file, 'a') as hf:
        hf.write(json.dumps(result) + '\n')
    guidance = get_latest_guidance(history_file)
    return {'result': result, 'guidance': guidance}

if __name__ == '__main__':
    txt = sys.argv[1] if len(sys.argv) > 1 else 'hello'
    tid = sys.argv[2] if len(sys.argv) > 2 else 'turn'
    r = full_cycle(txt, tid)
    print(json.dumps(r, indent=2))
