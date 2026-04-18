#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from live_loop import process_turn
txt = sys.argv[1] if len(sys.argv) > 1 else 'hello'
tid = sys.argv[2] if len(sys.argv) > 2 else 'turn'
print(json.dumps(process_turn(txt, tid), indent=2))
