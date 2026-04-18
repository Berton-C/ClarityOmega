with open('/PeTTa/repos/omegaclaw/src/helper.py') as f:
    lines = f.readlines()

func_first = {}
dup_lines = set()
i = 0
while i < len(lines):
    stripped = lines[i].strip()
    if stripped.startswith('def '):
        name = stripped.split('(')[0].replace('def ', '').strip()
        if name in func_first:
            start = i
            i += 1
            while i < len(lines) and (lines[i].startswith(' ') or lines[i].startswith('\t') or lines[i].strip() == ''):
                i += 1
            for j in range(start, i):
                dup_lines.add(j)
            continue
        else:
            func_first[name] = i
    i += 1

kept = [l for idx, l in enumerate(lines) if idx not in dup_lines]
print(f'Original lines: {len(lines)}')
print(f'Duplicate lines removed: {len(dup_lines)}')
print(f'Kept lines: {len(kept)}')
with open('/PeTTa/repos/omegaclaw/src/helper.py.deduped', 'w') as f:
    f.writelines(kept)
print('Written to helper.py.deduped for review')
