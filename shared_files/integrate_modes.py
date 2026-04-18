import sys
sys.path.insert(0, '/tmp')

with open('/tmp/conversation_handler_v2.py', 'r') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
skip = False
for line in lines:
    if 'EXPANDED_ACTION_MAP' in line or 'action_map' in line:
        skip = True
        continue
    if skip and ('action =' in line or 'EXPANDED' in line):
        skip = False
        new_lines.append('    from mode_vad_mapping import MODE_VAD_MAP')
        new_lines.append('    from mode_atoms_redesign import MODE_ATOMS')
        new_lines.append("    mode = MODE_VAD_MAP.get((vl, al, dl), 'spacious-presence')")
        new_lines.append('    guidance = MODE_ATOMS[mode]')
        continue
    if skip:
        continue
    new_lines.append(line)

with open('/tmp/conversation_handler_v2.py', 'w') as f:
    f.write('\n'.join(new_lines))
print('Handler integrated with mode-of-being routing')
