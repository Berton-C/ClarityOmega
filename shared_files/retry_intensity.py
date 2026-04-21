import urllib.request
import zipfile
import os

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
url = 'http://saifmohammad.com/WebDocs/Lexicons/NRC-Emotion-Intensity-Lexicon.zip'
try:
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=60)
    data = resp.read()
    with open('/tmp/NRC-Emotion-Intensity-Lexicon.zip', 'wb') as f:
        f.write(data)
    print(f'Downloaded {len(data)} bytes')
    os.makedirs('/tmp/NRC-Emotion-Intensity-Lexicon', exist_ok=True)
    with zipfile.ZipFile('/tmp/NRC-Emotion-Intensity-Lexicon.zip', 'r') as zf:
        zf.extractall('/tmp/NRC-Emotion-Intensity-Lexicon')
        print(f'Extracted: {zf.namelist()[:10]}')
except Exception as e:
    print(f'FAILED: {e}')
