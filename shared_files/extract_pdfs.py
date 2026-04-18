import subprocess
import os
for f in sorted(os.listdir('/tmp')):
  if f.startswith('soul_') and f.endswith('.pdf'):
    path = '/tmp/' + f
    txt = path.replace('.pdf','.txt')
    try:
      r = subprocess.run(['pdftotext',path,txt], capture_output=True, timeout=10)
      if os.path.exists(txt):
        size = os.path.getsize(txt)
        print('OK: ' + f + ' -> ' + str(size) + ' bytes text')
      else:
        print('NO_OUTPUT: ' + f)
    except Exception as e:
      print('ERR: ' + f + ' ' + str(e))
