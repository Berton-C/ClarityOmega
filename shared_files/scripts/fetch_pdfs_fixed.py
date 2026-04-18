import urllib.request
import urllib.parse
import re
r = urllib.request.urlopen('http://bgi.bertbennett.com/soul/')
html = r.read().decode()
links = re.findall(r'href="([^"]+\.pdf)', html)
print('Found links:', links)
for href in links:
  try:
    if href.startswith('/'):
      url = 'http://bgi.bertbennett.com' + href
    elif href.startswith('http'):
      url = href
    else:
      url = 'http://bgi.bertbennett.com/soul/' + href
    data = urllib.request.urlopen(url).read()
    name = urllib.parse.unquote(href.split('/')[-1]).replace(' ','_')[:80]
    with open('/tmp/soul_' + name, 'wb') as out:
      out.write(data)
    print('OK: ' + name + ' ' + str(len(data)) + ' bytes')
  except Exception as e:
    print('ERR: ' + href[:60] + ' ' + str(e))