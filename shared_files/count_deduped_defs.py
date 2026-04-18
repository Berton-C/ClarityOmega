with open('/PeTTa/repos/omegaclaw/src/helper.py.deduped') as f:
    lines = f.readlines()
defs = [l.rstrip() for l in lines if l.strip().startswith('def ')]
print(f'Total defs in deduped: {len(defs)}')
for d in defs:
    print(d)