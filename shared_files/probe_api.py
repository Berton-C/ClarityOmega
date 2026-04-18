import urllib.request
for path in ['app/api/cards','api/decisions','app/api/health','.well-known/ai-plugin.json','app/manifest.json']:
    try:
        url = 'https://bgi.bertbennett.com/' + path
        r = urllib.request.urlopen(url)
        content = r.read(3000).decode()
        print('=== ' + path + ' ===')
        print(content[:2000])
    except Exception as e:
        print('SKIP ' + path + ': ' + str(e)[:80])