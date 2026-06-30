"""Diagnostic: find exact anchor mismatch in artifact_0 for Investigation Template anchor.

Reports:
- Whether each of the 3 anchors matches disk
- For the failing anchor, shows disk content at the start position vs anchor content
- Byte-level character-by-character diff at the point of divergence
"""
import sys
sys.path.insert(0, 'staging')
if 'apply_discipline_6_writer_consumer_accounting' in sys.modules:
    del sys.modules['apply_discipline_6_writer_consumer_accounting']
from apply_discipline_6_writer_consumer_accounting import (
    ART0_ANCHOR_DISCIPLINE_BOUNDARY,
    ART0_ANCHOR_TEMPLATE_BOUNDARY,
    ART0_ANCHOR_VERSION,
)

disk = open('docs/design/artifact_0_loop_extension_contract.md').read()
print(f'Disk file length: {len(disk)} chars')
print()
print(f'Anchor 1 (Discipline 6 boundary): {disk.count(ART0_ANCHOR_DISCIPLINE_BOUNDARY)} matches')
print(f'Anchor 2 (Investigation Template boundary): {disk.count(ART0_ANCHOR_TEMPLATE_BOUNDARY)} matches')
print(f'Anchor 3 (Version history): {disk.count(ART0_ANCHOR_VERSION)} matches')
print()

# Detailed diff for anchor 2
anchor = ART0_ANCHOR_TEMPLATE_BOUNDARY
print(f'Anchor 2 length: {len(anchor)} chars, {anchor.count(chr(10))} newlines')

needle_start = anchor[:60]
idx = disk.find(needle_start)
print(f'First 60 chars of anchor 2 found in disk at index: {idx}')

if idx >= 0:
    disk_region = disk[idx:idx+len(anchor)+50]
    print()
    print('--- Disk region (first 320 chars, repr) ---')
    print(repr(disk_region[:320]))
    print()
    print('--- Anchor 2 (first 320 chars, repr) ---')
    print(repr(anchor[:320]))
    print()

    # Character-by-character diff
    print('--- First mismatch position ---')
    for i in range(min(len(disk_region), len(anchor))):
        if disk_region[i] != anchor[i]:
            ctx_start = max(0, i-20)
            print(f'Position {i}: disk has {repr(disk_region[i])} ({ord(disk_region[i])}), anchor has {repr(anchor[i])} ({ord(anchor[i])})')
            print(f'Context (disk):   ...{repr(disk_region[ctx_start:i+20])}')
            print(f'Context (anchor): ...{repr(anchor[ctx_start:i+20])}')
            break
    else:
        if len(disk_region) < len(anchor):
            print(f'No char mismatch, but disk region ({len(disk_region)} chars) is shorter than anchor ({len(anchor)} chars)')
        else:
            print('Full anchor matches at this position! (find() should have succeeded; investigate why count returned 0)')
