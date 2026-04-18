#!/usr/bin/env python3
import sys, re, json

def load_lex(path):
    lex = {}
    with open(path) as f:
        for line in f:
            m = re.match(r'\(= \(vad-lookup ([^)]+)\) \(PB-Vec ([\-0-9.]+) ([\-0-9.]+) ([\-0-9.]+)\)\)', line)
            if m:
                lex[m.group(1).lower()] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
    return lex

def get_vad(text, lex):
    words = re.findall(r'[a-z]+', text.lower())
    hits = [(w, lex[w]) for w in words if w in lex]
    if not hits: return (0,0,0), 0, len(words)
    v = sum(h[1][0] for h in hits)/len(hits)
    a = sum(h[1][1] for h in hits)/len(hits)
    d = sum(h[1][2] for h in hits)/len(hits)
    return (v,a,d), len(hits), len(words)

def classify(v,a,d):
    r = []
    if v < -0.3: r.append('negative-valence')
    elif v > 0.3: r.append('positive-valence')
    if a > 0.5: r.append('high-arousal')
    elif a < -0.1: r.append('low-arousal')
    if d > 0.4: r.append('high-dominance')
    elif d < -0.2: r.append('low-dominance')
    return r

ROUTE = {'negative-valence':'empathic-attunement','low-dominance':'empathic-attunement','positive-valence':'collaborative-exploration','high-arousal':'grounding-presence','high-dominance':'witnessing-celebration','low-arousal':'gentle-activation','high-positive-shift':'momentum-amplification','high-negative-shift':'stabilizing-presence'}

def process_turn(text, tid, prev_vad=None):
    lex = load_lex('/tmp/vad_common500.metta')
    (v,a,d), nhits, nwords = get_vad(text, lex)
    dl = classify(v,a,d)
    shift = v - prev_vad[0] if prev_vad else 0.0
    if shift > 0.4: dl.append('high-positive-shift')
    elif shift < -0.4: dl.append('high-negative-shift')
    modes = list(set(ROUTE[x] for x in dl if x in ROUTE))
    if not modes: modes = ['neutral-presence']
    return {'tid':tid,'hits':nhits,'words':nwords,'vad':[round(v,3),round(a,3),round(d,3)],'shift':round(shift,3),'dims':dl,'modes':modes}

if __name__ == '__main__':
    txt = sys.argv[1] if len(sys.argv) > 1 else 'hello'
    tid = sys.argv[2] if len(sys.argv) > 2 else 'turn'
    print(json.dumps(process_turn(txt, tid), indent=2))
