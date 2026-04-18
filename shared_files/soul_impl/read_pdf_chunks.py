import fitz
doc = fitz.open('/tmp/soul_impl/hyperseed_v7.pdf')
text = ''
for p in doc:
    text += p.get_text()
print('Pages:', len(doc), 'Chars:', len(text))
chunk_size = 8000
for i in range(0, min(len(text), 48000), chunk_size):
    print(f'\n=== CHUNK {i//chunk_size + 1} ===')
    print(text[i:i+chunk_size])