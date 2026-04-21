import urllib.request
import os
import zipfile

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
base = 'http://saifmohammad.com/'

downloads = [
    ('WebDocs/Lexicons/NRC-Emotion-Lexicon.zip', '/tmp/NRC-Emotion-Lexicon.zip'),
    ('WebDocs/Lexicons/NRC-Emotion-Intensity-Lexicon.zip', '/tmp/NRC-Emotion-Intensity-Lexicon.zip'),
]

for relpath, outpath in downloads:
    url = base + relpath
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=30)
        data = resp.read()
        with open(outpath, 'wb') as f:
            f.write(data)
        print(f'Downloaded {url} -> {outpath} ({len(data)} bytes)')
        extractdir = outpath.replace('.zip', '')
        os.makedirs(extractdir, exist_ok=True)
        with zipfile.ZipFile(outpath, 'r') as zf:
            zf.extractall(extractdir)
            print(f'  Extracted to {extractdir}: {zf.namelist()[:8]}')
    except Exception as e:
        print(f'FAILED {url}: {e}')

# For the colour lexicon we need to find link from the lexicons page
import re
try:
    with open('/tmp/colour_lexicon_page.html', 'r') as f:
        html = f.read()
    colour_links = [l for l in re.findall(r'href=["\x27]([^"\x27]*(?:colour|color)[^"\x27]*\.(?:zip|txt|csv))["\x27]', html, re.IGNORECASE)]
    print(f'Colour lexicon candidate links: {colour_links[:5]}')
    if not colour_links:
        print('No direct colour lexicon download link found on lexicons.html - may need manual search')
except Exception as e:
    print(f'Colour link search error: {e}')
