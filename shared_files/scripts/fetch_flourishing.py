import urllib.request
try:
    r = urllib.request.urlopen('https://bgi.bertbennett.com/pages/flourishing.html')
    print(r.read(12000).decode())
except Exception as e:
    print(str(e))