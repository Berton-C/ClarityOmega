import re, sys, zlib
fp = sys.argv[1]
with open(fp, chr(114)+chr(98)) as f:
    data = f.read()
ss = []
i = 0
while True:
    s = data.find(b'stream', i)
    if s < 0: break
    s = data.index(b'\n', s) + 1
    e = data.find(b'endstream', s)
    if e < 0: break
    try: ss.append(zlib.decompress(data[s:e]))
    except: pass
    i = e + 9
a = b'\n'.join(ss)
ms = re.findall(rb'\(([\x20-\x7e]+)\)', a)
r = b' '.join(ms)
print('LEN:', len(r))
chunk = int(sys.argv[2]) if len(sys.argv) > 2 else 0
print(r[chunk*12000:(chunk+1)*12000].decode('latin-1', errors='replace'))