import zlib, re, sys, os

for pdf_path in sys.argv[1:]:
    basename = os.path.basename(pdf_path)
    print(f'=== {basename} ===')
    with open(pdf_path, 'rb') as f:
        data = f.read()
    streams = re.findall(rb'stream\r?\n(.+?)\r?\nendstream', data, re.DOTALL)
    all_text = []
    for s in streams:
        if len(s) < 50:
            continue
        try:
            decoded = zlib.decompress(s).decode('latin-1', 'ignore')
        except:
            continue
        tj_arrays = re.findall(r'\[([^\]]+)\]\s*TJ', decoded)
        for arr in tj_arrays:
            parts = re.findall(r'\(([^)]+)\)', arr)
            line = ''.join(parts)
            clean = re.sub(r'[^a-zA-Z0-9 .,:;!?/\-]+', '', line).strip()
            if len(clean) > 3:
                all_text.append(clean)
        tj_singles = re.findall(r'\(([^)]+)\)\s*Tj', decoded)
        for t in tj_singles:
            clean = re.sub(r'[^a-zA-Z0-9 .,:;!?/\-]+', '', t).strip()
            if len(clean) > 3:
                all_text.append(clean)
    result = ' '.join(all_text)
    out_path = pdf_path.replace('.pdf', '.v2.txt')
    with open(out_path, 'w') as f:
        f.write(result)
    print(f'Extracted {len(result)} chars, {len(all_text)} fragments')
