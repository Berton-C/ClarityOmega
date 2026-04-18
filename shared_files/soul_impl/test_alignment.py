#!/usr/bin/env python3
from alignment_observer import AlignmentObserver
from sixth_loop_bridge import SixthLoopBridge

br = SixthLoopBridge()
ao = AlignmentObserver(br)
print('Initial alignment_coupling:', br.pq.alignment_coupling)
results = ao.auto_cross_validate()
print('Alignment after cross-validation:', br.pq.alignment_coupling)
print('Pairs tested:', len(results))
print('Last 3:')
for r in results[-3:]:
    print(' ', r)
print()
print('=== Full NAL Export ===')
for stmt in br.pq.state_as_nal():
    print(' ', stmt)
print('DONE')
