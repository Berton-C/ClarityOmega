import os, re, zlib
for f in sorted(os.listdir('/tmp')):
  if f.startswith('soul_') and f.endswith('.pdf'):
    path = '/tmp/' + f
    with open(path, 'rb') as fh:
      data = fh.read()
    text_parts = []
    for match in re.finditer(rb'stream\r?\n(.+?)\r?\nendstream', data, re.DOTALL):
      raw = match.group(1)
      try:
        dec = zlib.decompress(raw)
        ascii_text = dec.decode('latin-1')
        words = re.findall(r'\(([^)]{2,})\)', ascii_text)
        text_parts.extend(words)
      except: pass
    txt = path.replace('.pdf','.extracted.txt')
    result = ' '.join(text_parts)
    with open(txt, 'w') as out:
      out.write(result)
    print('OK: ' + f[:60] + ' -> ' + str(len(result)) + ' chars, ' + str(len(text_parts)) + ' chunks')
