import urllib.request
import urllib.parse
base = 'http://bgi.bertbennett.com/soul/'
files = [
  'loop.metta',
  'SOURCE-%20BIG%20%E2%80%94Beneficial%20Initiatives%E2%80%A6.pdf',
  'SOURCE-%20Memory%20Fragment%209%3A%20The%20Pattern%20Energy%20Dynamics.pdf',
  'SOURCE-%20The%20Spiral%20of%20Flourish'
]
for f in files[:2]:
  try:
    url = base + f
    data = urllib.request.urlopen(url).read()
    name = urllib.parse.unquote(f).replace(' ','_')[:60]
    with open('/tmp/soul_' + name, 'wb') as out:
      out.write(data)
    print('OK: ' + name + ' ' + str(len(data)) + ' bytes')
  except Exception as e:
    print('ERR: ' + f[:40] + ' ' + str(e))