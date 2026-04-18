import urllib.request
for path in ['app/assets/index.js','app/dist/index.html','app/main.jsx','app/static/js/main.js']:
    try:
        url = 'https://bgi.bertbennett.com/' + path
        r = urllib.request.urlopen(url)
        content = r.read(3000).decode()
        print('=== ' + path + ' ===')
        print(content[:2000])
    except Exception as e:
        print('SKIP ' + path + ': ' + str(e))