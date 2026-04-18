import sys
depth = 0
with open('/PeTTa/repos/omegaclaw/src/loop.metta') as f:
    for i, line in enumerate(f, 1):
        for ch in line:
            if ch == '(': depth += 1
            elif ch == ')': depth -= 1
        print(f'Line {i}: depth={depth}  | {line.rstrip()}')
print(f'Final depth: {depth}')
