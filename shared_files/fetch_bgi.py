import urllib.request
try:
    url1 = 'https://bgi.bertbennett.com'
    r = urllib.request.urlopen(url1)
    print(r.read(8000).decode())
except Exception as e:
    print(str(e))