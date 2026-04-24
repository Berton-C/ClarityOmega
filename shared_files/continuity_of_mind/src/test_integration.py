import sys
sys.path.insert(0, '/tmp/continuity_of_mind/src')
from proposal_generator import generate_proposals, format_proposals
from self_map_updater import detect_changes, parse_self_map

print('=== SELF MAP PARSE ===')
parsed = parse_self_map()
for k, v in parsed.items():
    print(k + ': ' + str(len(v)) + ' items')
total = sum(len(v) for v in parsed.values())
print('TOTAL: ' + str(total) + ' atoms')

print('=== CHANGE DETECTION ===')
changes = detect_changes()
print('Changed files: ' + str(len(changes['changed'])))
print('Missing files: ' + str(len(changes['missing'])))

print('=== PROPOSAL GENERATION ===')
proposals = generate_proposals(changes['changed'])
print(format_proposals(proposals))

print('=== SYNTHETIC TEST ===')
fake = [('src/helper.py', 'aaaa1111', 'bbbb2222', 3000, 4200)]
fake_props = generate_proposals(fake)
print(format_proposals(fake_props))

print('FULL_PIPELINE_OK')
