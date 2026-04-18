#!/usr/bin/env python3
import re

with open('/tmp/vad_balanced100.metta') as f:
    lines = f.readlines()

print('Total lines:', len(lines))
print('First 5 lines:')
for i, l in enumerate(lines[:5]):
    print(f'  [{i}] {repr(l)}')

pattern = r'\(= \(vad-lookup ([^)]+)\) \(PB-Vec ([\-0-9.]+) ([\-0-9.]+) ([\-0-9.]+)\)\)'
hits = 0
for l in lines:
    if re.match(pattern, l):
        hits += 1
print(f'Regex hits: {hits}')

# Try simpler match
simple_hits = sum(1 for l in lines if l.startswith('(= (vad-lookup'))
print(f'Simple startswith hits: {simple_hits}')

if simple_hits > 0 and hits == 0:
    sample = [l for l in lines if l.startswith('(= (vad-lookup')][0]
    print(f'Sample line: {repr(sample)}')
    print(f'Pattern: {pattern}')
    m = re.match(pattern, sample)
    print(f'Match result: {m}')
