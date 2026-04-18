#!/usr/bin/env python3
import sys
LEX = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
out = sys.argv[2] if len(sys.argv) > 2 else '/tmp/vad_balanced100.metta'
entries = []
with open(LEX) as f:
    next(f)
    for line in f:
        p = line.strip().split('\t')
        if len(p) >= 4:
            w = p[0].lower().replace(' ','-')
            try:
                v,a,d = float(p[1]),float(p[2]),float(p[3])
                entries.append((w,v,a,d))
            except: pass
pos = sorted([e for e in entries if e[1]>0], key=lambda x:-x[1])[:n//2]
neg = sorted([e for e in entries if e[1]<0], key=lambda x:x[1])[:n//2]
with open(out,'w') as f:
    f.write(';; Balanced VAD: %d pos + %d neg\n'%(len(pos),len(neg)))
    for w,v,a,d in pos:
        f.write('(= (vad-lookup %s) (PB-Vec %.3f %.3f %.3f))\n'%(w,v,a,d))
    f.write('\n;; === NEGATIVE ===\n')
    for w,v,a,d in neg:
        f.write('(= (vad-lookup %s) (PB-Vec %.3f %.3f %.3f))\n'%(w,v,a,d))
print('Wrote %d atoms to %s'%(len(pos)+len(neg),out))