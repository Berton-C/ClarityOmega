import urllib.request
import sys

urls = [
    'http://saifmohammad.com/WebPages/nrc-vad.html',
    'http://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm',
    'http://saifmohammad.com/WebPages/AffectIntensity.htm',
    'http://saifmohammad.com/WebPages/lexicons.html'
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'})
        resp = urllib.request.urlopen(req, timeout=15)
        print(f'{url} -> {resp.status}')
    except Exception as e:
        print(f'{url} -> ERROR: {e}')
