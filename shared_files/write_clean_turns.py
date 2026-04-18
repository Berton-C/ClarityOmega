#!/usr/bin/env python3
import json
turns = [
    {'tid': 'berton-c-01', 'text': 'use the harness as much as possible in the act of building use the backbone and its capacity to see learn grow'},
    {'tid': 'clarity-01', 'text': 'the backbone is alive and reading our conversation in real time every exchange gets processed'},
    {'tid': 'berton-c-02', 'text': 'it would be really smart to use the harness as much as possible in the act of building like we did previously'}
]
with open('/tmp/pending_turns_clean.jsonl', 'w') as f:
    for t in turns:
        f.write(json.dumps(t) + '\n')
print('Written %d clean turns' % len(turns))
