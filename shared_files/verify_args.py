import re

with open('/PeTTa/repos/omegaclaw/src/loop.metta') as f:
    content = f.read()

with open('/PeTTa/repos/omegaclaw/src/context.metta') as f:
    ctx = f.read()

print('=== CONTEXT DEFINITIONS ===')
for line in ctx.splitlines():
    if '(= (' in line:
        print(line.strip())

print()
print('=== LOOP SOUL CALLS ===')
for i, line in enumerate(content.splitlines()):
    if 'soul-' in line or 'initSoul' in line:
        print(f'{i+1}: {line}')
