import re

with open('/PeTTa/repos/omegaclaw/src/loop.metta') as f:
    lines = f.readlines()

print('=== Lines 55-75 of loop.metta ===')
for i in range(54, min(75, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()}')

print()
print('=== Variable threading ===')
for i in range(54, min(75, len(lines))):
    line = lines[i]
    vars_found = re.findall(r'\$\w+', line)
    if vars_found:
        print(f'{i+1}: vars={vars_found}  | {line.rstrip()}')
