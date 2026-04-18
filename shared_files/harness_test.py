#!/usr/bin/env python3
import re

def load_lex(path):
    lex = {}
    with open(path) as f:
        for line in f:
            m = re.match(r'\(= \(vad-lookup ([^)]+)\) \(PB-Vec ([\-0-9.]+) ([\-0-9.]+) ([\-0-9.]+)\)\)', line)
            if m:
                lex[m.group(1).lower()] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
    return lex

def vad(text, lex):
    words = re.findall(r'[a-z]+', text.lower())
    hits = [(w, lex[w]) for w in words if w in lex]
    if not hits: return (0,0,0), 0
    v = sum(h[1][0] for h in hits)/len(hits)
    a = sum(h[1][1] for h in hits)/len(hits)
    d = sum(h[1][2] for h in hits)/len(hits)
    return (v,a,d), len(hits)

def dims(v,a,d):
    r = []
    if v < -0.3: r.append('negative-valence')
    elif v > 0.3: r.append('positive-valence')
    if a > 0.5: r.append('high-arousal')
    elif a < -0.1: r.append('low-arousal')
    if d > 0.4: r.append('high-dominance')
    elif d < -0.2: r.append('low-dominance')
    return r

route = {'negative-valence':'empathic-attunement','low-dominance':'empathic-attunement','positive-valence':'collaborative-exploration','high-arousal':'grounding-presence','high-dominance':'witnessing-celebration','low-arousal':'gentle-activation','high-positive-shift':'momentum-amplification','high-negative-shift':'stabilizing-presence'}

lex = load_lex('/tmp/vad_common500.metta')
print('Lexicon: %d words' % len(lex))
turns = [('t1','I am frustrated and stuck and feeling hopeless'),('t2','but maybe there is something I am not seeing'),('t3','actually this is interesting and I feel curious now'),('t4','yes this is wonderful I love where this is going'),('t5','I feel confident and strong about this direction')]
prev = None
for tid, txt in turns:
    (v,a,d), nhits = vad(txt, lex)
    dl = dims(v,a,d)
    shift = v - prev[0] if prev else 0.0
    if shift > 0.4: dl.append('high-positive-shift')
    elif shift < -0.4: dl.append('high-negative-shift')
    modes = list(set(route[x] for x in dl if x in route))
    print('[%s] %s' % (tid, txt))
    print('  hits=%d VAD=(%.3f,%.3f,%.3f) shift=%.3f' % (nhits,v,a,d,shift))
    print('  dims=%s -> modes=%s' % (dl, modes))
    prev = (v,a,d)
print('HARNESS COMPLETE')
