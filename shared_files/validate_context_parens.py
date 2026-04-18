with open('/PeTTa/repos/omegaclaw/src/context.metta') as f:
    content = f.read()
depth = 0
for i, c in enumerate(content):
    if c == '(': depth += 1
    elif c == ')': depth -= 1
    if depth < 0:
        print(f'UNMATCHED ) at char {i}')
        break
else:
    if depth == 0:
        print('CONTEXT_METTA_PARENS_BALANCED')
    else:
        print(f'UNMATCHED ( remaining, depth={depth}')
