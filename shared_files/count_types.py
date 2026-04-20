import os, glob
files = sorted(glob.glob('/PeTTa/repos/omegaclaw/lib_clarity_reasoning/*.metta'))
total = 0
for f in files:
    count = sum(1 for l in open(f) if l.strip().startswith('(: '))
    total += count
    print(f'{os.path.basename(f):40s} types={count}')
print(f'\nTOTAL type declarations: {total}')
print(f'Files: {len(files)}')
