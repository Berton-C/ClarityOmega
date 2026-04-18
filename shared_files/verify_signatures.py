import re

with open('/PeTTa/repos/omegaclaw/src/context.metta') as f:
    ctx = f.read()

with open('/PeTTa/repos/omegaclaw/src/loop.metta') as f:
    loop = f.read()

# Extract function definitions from context.metta
defs = re.findall(r'\(= \((\S+)', ctx)
print('Context defines:', defs)

# Extract soul function calls from loop.metta
soul_funcs = ['initSoulSeeds', 'soul-rationality-startup-check', 'soul-pre-compute', 'soul-calibration-record', 'soul-note-record']
for fn in soul_funcs:
    calls = [l.strip() for l in loop.splitlines() if fn in l]
    defs_found = [l.strip() for l in ctx.splitlines() if fn in l and '(= (' in l]
    print(f'\n{fn}:')
    print(f'  defined: {defs_found}')
    print(f'  called:  {calls}')
    # Check arg count match
    for d in defs_found:
        def_args = len(re.findall(r'\$\w+', d))
        print(f'  def expects {def_args} args')
    for c in calls:
        print(f'  call: {c}')
