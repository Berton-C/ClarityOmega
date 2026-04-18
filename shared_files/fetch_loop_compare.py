import urllib.request
r = urllib.request.urlopen('http://bgi.bertbennett.com/soul/loop.metta')
data = r.read().decode()
print('Remote loop.metta lines:', len(data.splitlines()))
print('First 500 chars:')
print(data[:500])