import subprocess
import sys
r = subprocess.run(['pdftotext', '/PeTTa/repos/omegaclaw/soul/sources/hyperseed_v7.pdf', '-'], capture_output=True, text=True)
lines = r.stdout.split('\n')
found = False
count = 0
for line in lines:
    low = line.lower()
    if '16.2' in line or 'self-development' in low or '17.1' in line or 'reflective will' in low:
        found = True
    if found:
        print(line)
        count += 1
        if count > 300:
            break
if not found:
    print('No 16.2+ markers found. Printing last 100 lines:')
    for l in lines[-100:]:
        print(l)
