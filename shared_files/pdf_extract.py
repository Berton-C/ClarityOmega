import zlib, re, sys

for pdf_path in sys.argv[1:]:
    print(f'=== {pdf_path} ===')
    with open(pdf_path, 'rb') as f:
        data = f.read()
    streams = re.findall(rb'stream\r?\n(.+?)\r?\nendstream', data, re.DOTALL)
    text = ''
    for s in streams:
        if len(s) > 50:
            try:
                decoded = zlib.decompress(s).decode('latin-1', 'ignore')
                # Filter for lines with actual words
                for line in decoded.split('\n'):
                    clean = re.sub(r'[^a-zA-Z0-9 .,:;!?\-\'"()]+', ' ', line).strip()
                    if len(clean) > 20 and sum(c.isalpha() for c in clean) > len(clean)*0.4:
                        text += clean + '\n'
            except:
                pass
    if text:
        out_path = pdf_path.replace('.pdf', '.clean.txt')
        with open(out_path, 'w') as f:
            f.write(text[:50000])
        print(f'Extracted {len(text)} chars to {out_path}')
    else:
        print('No readable text extracted')
