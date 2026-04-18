import os
try:
    from PyPDF2 import PdfReader
except ImportError:
    print('No PyPDF2')
    import sys; sys.exit(1)
for f in sorted(os.listdir('/tmp')):
  if f.startswith('soul_') and f.endswith('.pdf'):
    path = '/tmp/' + f
    txt = path.replace('.pdf','.txt')
    try:
      reader = PdfReader(path)
      text = ''
      for page in reader.pages:
        text += page.extract_text() or ''
      with open(txt,'w') as out:
        out.write(text)
      print('OK: ' + f + ' -> ' + str(len(text)) + ' chars')
    except Exception as e:
      print('ERR: ' + f + ' ' + str(e))
