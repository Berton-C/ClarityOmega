with open('/PeTTa/repos/omegaclaw/src/loop.metta') as f:
    lines = f.readlines()
for i in range(53, min(75, len(lines))):
    print(f'{i+1}: {repr(lines[i])}')
