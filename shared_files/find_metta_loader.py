import os

files_to_search = [
    '/PeTTa/repos/omegaclaw/src/helper.py',
    '/PeTTa/repos/omegaclaw/src/agentverse.py',
    '/PeTTa/repos/omegaclaw/lib_llm_ext.py',
]

keywords = ['metta', 'load', 'runner', 'atomspace', 'context', '.metta']

for fpath in files_to_search:
    if not os.path.exists(fpath):
        print(f'NOT FOUND: {fpath}')
        continue
    with open(fpath) as f:
        lines = f.readlines()
    hits = []
    for i, l in enumerate(lines):
        low = l.lower()
        if any(k in low for k in keywords):
            hits.append(f'  {i+1}: {l.rstrip()}')
    if hits:
        print(f'\n=== {fpath} ({len(hits)} hits) ===')
        for h in hits:
            print(h)
    else:
        print(f'\n=== {fpath} (0 hits) ===')
