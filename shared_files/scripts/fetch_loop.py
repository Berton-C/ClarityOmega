import urllib.request
try:
    req = urllib.request.Request('https://bgi.bertbennett.com/soul/loop.metta', headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=15)
    content = r.read().decode()
    f = open('/tmp/berton_loop.metta', 'w')
    f.write(content)
    f.close()
    print(content[:8000])
except Exception as e:
    print('Failed:', e)