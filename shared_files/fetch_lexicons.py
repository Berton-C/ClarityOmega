import urllib.request
import os
import re

base = 'http://saifmohammad.com/WebPages/'
pages = [
    ('NRC-Emotion-Lexicon.htm', 'emotion_lexicon'),
    ('AffectIntensity.htm', 'affect_intensity'),
    ('lexicons.html', 'colour_lexicon')
]

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}

for page, label in pages:
    try:
        req = urllib.request.Request(base + page, headers=headers)
        resp = urllib.request.urlopen(req, timeout=20)
        html = resp.read().decode('utf-8', errors='replace')
        outpath = f'/tmp/{label}_page.html'
        with open(outpath, 'w') as f:
            f.write(html)
        links = re.findall(r'href=["\x27]([^"\x27]*\.(?:txt|zip|csv|xlsx|tar\.gz))["\x27]', html, re.IGNORECASE)
        print(f'{label}: saved page ({len(html)} bytes), found data links: {links[:10]}')
    except Exception as e:
        print(f'{label}: ERROR - {e}')
