import urllib.request
try:
    url2 = 'https://bgi.bertbennett.com/app/'
    r = urllib.request.urlopen(url2)
    print(r.read(8000).decode())
except Exception as e:
    print(str(e))