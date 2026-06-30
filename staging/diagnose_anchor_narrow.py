"""Diagnostic: narrow down which prefix of the anchor matches disk."""
import sys
sys.path.insert(0, 'staging')
if 'apply_discipline_6_writer_consumer_accounting' in sys.modules:
    del sys.modules['apply_discipline_6_writer_consumer_accounting']
from apply_discipline_6_writer_consumer_accounting import ART0_ANCHOR_TEMPLATE_BOUNDARY

disk = open('docs/design/artifact_0_loop_extension_contract.md').read()
anchor = ART0_ANCHOR_TEMPLATE_BOUNDARY

print(f'Disk length: {len(disk)} chars')
print(f'Anchor length: {len(anchor)} chars')
print()

# Try progressively shorter prefixes to find where matching breaks
for n in [256, 200, 150, 100, 80, 60, 40, 30, 20, 15, 10]:
    if n > len(anchor):
        continue
    prefix = anchor[:n]
    count = disk.count(prefix)
    print(f'First {n} chars of anchor: {count} matches in disk')

print()
# Also try searching for the very first SUBSTRING that distinguishes
print('=== Test substring searches ===')
key_strings = [
    '[ ] Atom queryability verified',
    '[ ] Atom queryability verified for any new substrate state',
    'Atom queryability',
    'Any NO answer halts',
    '## 4. Maintenance contract',
]
for s in key_strings:
    print(f'  {s[:50]!r} -> {disk.count(s)} matches')

# And dump the first 10 bytes of anchor as bytes
print()
print('=== Anchor as bytes (first 60) ===')
print(anchor[:60].encode('utf-8'))
print()
print('=== Disk at index of "[ ] Atom queryability" if found ===')
idx = disk.find('[ ] Atom queryability verified for any new substrate state')
print(f'Found at index: {idx}')
if idx >= 0:
    print('Next 80 chars at disk[idx:idx+80] as bytes:')
    print(disk[idx:idx+80].encode('utf-8'))
