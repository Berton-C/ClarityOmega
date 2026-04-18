import urllib.request
import urllib.parse
base = 'http://bgi.bertbennett.com/soul/'
# Get directory listing first to find exact filenames
r = urllib.request.urlopen(base)
html = r.read().decode()
import re
links = re.findall(r'href="([^"]+\.pdf)"', html)
print('Found PDFs:', links)
for f in links:
  try:
    url = base + f
    data = urllib.request.urlopen(url).read()
    name = urllib.parse.unquote(f).replace(' ','_')[:80]
    with open('/tmp/soul_' + name, 'wb') as out:
      out.write(data)
    print('OK: ' + name + ' ' + str(len(data)) + ' bytes')
  except Exception as e:
    print('ERR: ' + f[:50] + ' ' + str(e))