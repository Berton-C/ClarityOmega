with open('/PeTTa/repos/omegaclaw/src/helper.py') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    s = l.strip()
    if s.startswith('def '):
        print(f'{i}: {s[:80]}')
