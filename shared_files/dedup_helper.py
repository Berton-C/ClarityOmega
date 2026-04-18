import re

with open('/PeTTa/repos/omegaclaw/src/helper.py') as f:
    content = f.read()

lines = content.split('\n')
func_defs = {}
duplicates = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('def '):
        name = stripped.split('(')[0].replace('def ', '').strip()
        if name in func_defs:
            duplicates.append((name, func_defs[name]+1, i+1))
        else:
            func_defs[name] = i

print(f'Total unique function defs: {len(func_defs)}')
print(f'Duplicate defs found: {len(duplicates)}')
for name, first, dup in duplicates:
    print(f'  {name}: first at line {first}, duplicate at line {dup}')
