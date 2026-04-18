import sys
sys.path.insert(0, '/tmp')

with open('/tmp/conversation_handler_v2.py', 'r') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
skip = False
for line in lines:
    if 'action_map = {' in line:
        skip = True
        continue
    if skip and 'action = action_map.get' in line:
        skip = False
        new_lines.append('    from expanded_action_map import EXPANDED_ACTION_MAP')
        new_lines.append('    action = EXPANDED_ACTION_MAP.get((vl, al, dl), neutral-presence)')
        continue
    if skip:
        continue
    new_lines.append(line)

with open('/tmp/conversation_handler_v2.py', 'w') as f:
    f.write('\n'.join(new_lines))
print('Handler updated successfully')
