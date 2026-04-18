import urllib.request
try:
    r = urllib.request.urlopen('https://bgi.bertbennett.com/app/src/App.jsx')
    print(r.read(12000).decode())
except Exception as e:
    print(str(e))
try:
    r2 = urllib.request.urlopen('https://bgi.bertbennett.com/app/index.html')
    print(r2.read(8000).decode())
except Exception as e2:
    print(str(e2))