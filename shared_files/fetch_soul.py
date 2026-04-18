import urllib.request
try:
    r = urllib.request.urlopen('http://bgi.bertbennett.com/soul')
    print(r.read().decode()[:5000])
except Exception as e:
    print('Error: ' + str(e))