import re

with open('/PeTTa/repos/omegaclaw/src/loop.metta') as f:
    lines = f.readlines()

print('=== LINES 54-75 RAW ===')
for i in range(53, min(75, len(lines))):
    print(f'{i+1}: |{lines[i].rstrip()}|')

print()
print('=== LET* VARIABLE BINDINGS ===')
for i in range(53, min(75, len(lines))):
    line = lines[i]
    binding = re.findall(r'\(\s*(\$\w+)', line)
    if binding:
        print(f'{i+1}: binds {binding} | {line.rstrip()}')
