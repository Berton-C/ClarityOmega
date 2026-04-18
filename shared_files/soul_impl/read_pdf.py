import fitz
doc = fitz.open('/tmp/soul_impl/hyperseed_v7.pdf')
text = ''
for p in doc:
    text += p.get_text()
print('Pages:', len(doc), 'Chars:', len(text))
print(text[:8000])