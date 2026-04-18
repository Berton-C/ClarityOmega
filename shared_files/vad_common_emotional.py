#!/usr/bin/env python3
import sys

LEX = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/vad_common500.metta'

# High-frequency emotional words we MUST include
priority = set(['happy','sad','angry','frustrated','stuck','love','hate','wonder',
    'wonderful','terrible','amazing','horrible','great','awful','good','bad',
    'fear','joy','trust','surprise','disgust','anxious','calm','excited',
    'bored','confused','curious','grateful','hopeful','hopeless','lonely',
    'proud','ashamed','guilty','jealous','content','miserable','delighted',
    'furious','peaceful','nervous','confident','insecure','overwhelmed',
    'inspired','exhausted','energetic','progress','failure','success',
    'beautiful','ugly','kind','cruel','gentle','harsh','warm','cold',
    'bright','dark','safe','dangerous','free','trapped','alive','dead',
    'strong','weak','rich','poor','fast','slow','easy','hard','simple',
    'complex','open','closed','new','old','young','fresh','stale',
    'clean','dirty','quiet','loud','soft','rough','sweet','bitter',
    'interesting','boring','fun','dull','brilliant','stupid','wise','foolish',
    'brave','coward','honest','liar','friend','enemy','help','hurt',
    'win','lose','grow','shrink','build','destroy','create','ruin',
    'laugh','cry','smile','frown','celebrate','mourn','thrive','suffer'])

entries = {}
with open(LEX) as f:
    next(f)
    for line in f:
        p = line.strip().split('\t')
        if len(p) >= 4:
            w = p[0].lower().replace(' ','-')
            try:
                v,a,d = float(p[1]),float(p[2]),float(p[3])
                entries[w] = (v,a,d)
            except: pass

# Priority words first
result = []
found_priority = []
for w in sorted(priority):
    if w in entries:
        found_priority.append((w,)+entries[w])
print(f'Priority words found: {len(found_priority)}/{len(priority)}')

# Fill remaining from most emotionally significant
used = set(w for w,v,a,d in found_priority)
remaining = [(w,v,a,d) for w,(v,a,d) in entries.items() if w not in used]
remaining.sort(key=lambda x: abs(x[1]-0.5)+abs(x[2]-0.5)+abs(x[3]-0.5), reverse=True)
fill = remaining[:500-len(found_priority)]

all_words = found_priority + fill
with open(out,'w') as f:
    f.write(';; VAD Lexicon: %d words (%d priority + %d significant)\n'%(len(all_words),len(found_priority),len(fill)))
    for w,v,a,d in all_words:
        f.write('(= (vad-lookup %s) (PB-Vec %.3f %.3f %.3f))\n'%(w,v,a,d))
print('Wrote %d atoms to %s'%(len(all_words),out))
missing = priority - set(entries.keys())
if missing:
    print('Missing from NRC:', sorted(missing))
