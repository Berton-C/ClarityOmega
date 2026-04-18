import os
import re
for f in sorted(os.listdir('/tmp')):
  if f.startswith('soul_') and f.endswith('.pdf'):
    path = '/tmp/' + f
    with open(path, 'rb') as fh:
      data = fh.read()
    chunks = []
    for match in re.finditer(rb'BT(.*?)ET', data, re.DOTALL):
      text = match.group(1)
      strings = re.findall(rb'\(([^)]+)\)', text)
      for s in strings:
        try:
          chunks.append(s.decode('utf-8', errors='ignore'))
        except: pass
    txt = path.replace('.pdf','.txt')
    result = ' '.join(chunks)
    with open(txt, 'w') as out:
      out.write(result)
    print('OK: ' + f + ' -> ' + str(len(result)) + ' chars')
