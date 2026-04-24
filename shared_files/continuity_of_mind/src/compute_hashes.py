import hashlib, os, json
files = [
    'soul/soul_kernel.metta', 'soul/soul_utils.metta', 'soul/soul_memory.metta',
    'src/loop.metta', 'src/skills.metta', 'src/helper.py',
    'lib_nal.metta', 'lib_omegaclaw.metta', 'lib_llm_ext.py',
    'lib_clarity_reasoning/lib_clarity_reasoning.metta',
    'lib_clarity_reasoning/substrate_kb.metta',
    'lib_clarity_reasoning/lib_quantale.metta',
    'run.metta', 'src/agentverse.py'
]
base = '/PeTTa/repos/omegaclaw/'
hashes = {}
for f in files:
    p = base + f
    if os.path.exists(p):
        h = hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]
        sz = os.path.getsize(p)
        hashes[f] = {'md5': h, 'size': sz}
    else:
        hashes[f] = {'md5': 'MISSING', 'size': 0}
state = {'baseline_hashes': hashes, 'computed_at': '2026-04-22T19:23:41'}
out = '/tmp/continuity_of_mind/src/updater_state.json'
with open(out, 'w') as fh:
    json.dump(state, fh, indent=2)
for k, v in hashes.items():
    print(f"{k} -> {v['md5']}:{v['size']}")
print(f'TOTAL: {len(hashes)} files hashed')
print('STATE_SAVED')
