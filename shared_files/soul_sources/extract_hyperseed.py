import fitz
doc = fitz.open('/tmp/soul_sources/hyperseed_v7.pdf')
for i in range(min(3, len(doc))):
    text = doc[i].get_text()
    print(f'--- PAGE {i+1} ---')
    print(text[:2000])
