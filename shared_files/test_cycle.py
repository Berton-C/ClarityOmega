#!/usr/bin/env python3
import sys, json
sys.path.insert(0, '/tmp')
from cycle import full_cycle
r = full_cycle('this is a test of the unified cycle', 'test-01')
print(json.dumps(r, indent=2))
