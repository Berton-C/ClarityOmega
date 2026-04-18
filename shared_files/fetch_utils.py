import urllib.request
try:
    req = urllib.request.Request('https://bgi.bertbennett.com/soul/soul_utils.metta', headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=15)
    content = r.read().decode()
    f = open('/tmp/berton_soul_utils.metta', 'w')
    f.write(content)
    f.close()
    print('SUCCESS: ' + str(len(content)) + ' bytes')
    print(content[:6000])
except Exception as e:
    print('Failed:', e)