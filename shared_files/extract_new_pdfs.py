import zlib,re,os

def extract_pdf(path):
    f=open(path,'rb');d=f.read();f.close();t=[];i=0
    while True:
        s=d.find(b'stream',i)
        if s<0:break
        s=d.index(b'\n',s)+1
        e=d.find(b'endstream',s)
        try:
            c=zlib.decompress(d[s:e])
            for m in re.findall(rb'\(([^)]+)\)',c)+re.findall(rb'\[([^\]]+)\]TJ',c):
                x=m.decode('latin-1','ignore').strip()
                if len(x)>1:t.append(x)
        except:pass
        i=e+1 if e and e>0 else i+1
    return t

sd='/tmp/soul_sources/'
for f in os.listdir(sd):
    if f.endswith('.pdf') and ('Flourishing' in f or 'Fragment 9' in f):
        print(f'=== {f} ===')
        lines=extract_pdf(os.path.join(sd,f))
        out=os.path.join(sd,f.replace('.pdf','.v2.txt'))
        with open(out,'w') as fh:fh.write('\n'.join(lines))
        print(f'Extracted {len(lines)} lines to {out}')
        print('\n'.join(lines[:80]))
        print('...')
