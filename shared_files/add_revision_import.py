path = '/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_clarity_reasoning.metta'
with open(path) as f:
    lines = f.readlines()
new_import = '!(import! &self (library omegaclaw lib_revision_accumulator))\n'
for i, line in enumerate(lines):
    if 'lib_autocatalytic_cycle' in line:
        lines.insert(i+1, new_import)
        break
with open(path, 'w') as f:
    f.writelines(lines)
print('done', len(lines), 'lines')
