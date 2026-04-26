import fitz
doc = fitz.open('/PeTTa/repos/omegaclaw/soul/sources/hyperseed_v7.pdf')
pages = len(doc)
print(f'Total pages: {pages}')
text = ''
for i in range(pages):
    t = doc[i].get_text()
    if t.strip():
        text += t
lines = text.split('\n')
found = False
count = 0
for line in lines:
    if '16.2' in line or 'Self as' in line or 'self-development' in line.lower() or 'Section 17' in line or '17.1' in line:
        found = True
    if found:
        print(line)
        count += 1
        if count > 250:
            break
if not found:
    print('No section 16.2+ markers found in extracted text')
    print(f'Total lines: {len(lines)}')
    for l in lines[-100:]:
        print(l)
