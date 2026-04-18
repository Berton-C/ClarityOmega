import re

with open('/PeTTa/repos/omegaclaw/src/loop.metta') as f:
    lines = f.readlines()

print('=== RAW REPR OF SOUL CALL LINES ===')
for i in range(len(lines)):
    if 'soul-' in lines[i] or 'initSoul' in lines[i]:
        print(f'Line {i+1}: {repr(lines[i])}')
        dvars = re.findall(r'\$\w+', lines[i])
        print(f'  vars: {dvars}')

print()
print('=== ALL DOLLAR VARS IN LET CHAIN ===')
for i in range(53, min(79, len(lines))):
    dvars = re.findall(r'\$\w+', lines[i])
    if dvars:
        print(f'Line {i+1}: {dvars} | {lines[i].rstrip()}')
