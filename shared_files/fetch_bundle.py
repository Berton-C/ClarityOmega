import urllib.request
try:
    r = urllib.request.urlopen('https://bgi.bertbennett.com/app/assets/index-BSMfxzAV.js')
    content = r.read(15000).decode()
    print(content[:12000])
except Exception as e:
    print(str(e))