#!/usr/bin/env python3
import time

lexicon_path = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
start = time.time()
count = 0
skipped = 0

with open(lexicon_path) as f:
    header = f.readline()
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 4:
            try:
                v = float(parts[1])
                a = float(parts[2])
                d = float(parts[3])
                count += 1
            except ValueError:
                skipped += 1

elapsed = time.time() - start
print('Parsed %d entries, skipped %d, took %.2fs' % (count, skipped, elapsed))
print('First term example from re-read:')
with open(lexicon_path) as f:
    f.readline()
    for i in range(3):
        line = f.readline().strip()
        parts = line.split('\t')
        print('  term=%s v=%s a=%s d=%s' % (parts[0], parts[1], parts[2], parts[3]))
