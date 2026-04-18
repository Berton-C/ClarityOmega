#!/usr/bin/env python3
import sys
import re

LEXICON_FILE = '/tmp/vad_common500.metta'

def load_lexicon(path=None):
    if path is None:
        path = LEXICON_FILE
    lexicon = {}
    with open(path) as f:
        for line in f:
            m = re.match(r'\(= \(vad-lookup ([^)]+)\) \(PB-Vec ([\-0-9.]+) ([\-0-9.]+) ([\-0-9.]+)\)\)', line)
            if m:
                lexicon[m.group(1).lower()] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
    return lexicon

def extract_vad(text, lexicon):
    words = re.findall(r'[a-z]+', text.lower())
    hits = [(w, lexicon[w]) for w in words if w in lexicon]
    if not hits:
        return words, [], (0.0, 0.0, 0.0)
    v = sum(h[1][0] for h in hits) / len(hits)
    a = sum(h[1][1] for h in hits) / len(hits)
    d = sum(h[1][2] for h in hits) / len(hits)
    return words, hits, (v, a, d)

def classify_dimensions(vad):
    labels = []
    if vad[0] < -0.3: labels.append('negative-valence')
    elif vad[0] > 0.3: labels.append('positive-valence')
    if vad[1] > 0.5: labels.append('high-arousal')
    elif vad[1] < -0.1: labels.append('low-arousal')
    if vad[2] > 0.4: labels.append('high-dominance')
    elif vad[2] < -0.2: labels.append('low-dominance')
    return labels

def to_metta(turn_id, words, hits, vad, prev_vad=None):
    lines = []
    lines.append('(= (turn-vad %s) (PB-Vec %.3f %.3f %.3f))' % (turn_id, vad[0], vad[1], vad[2]))
    shift = 0.0
    if prev_vad:
        shift = vad[0] - prev_vad[0]
    lines.append('(= (turn-shift %s) %.3f)' % (turn_id, shift))
    dims = classify_dimensions(vad)
    for d in dims:
        lines.append('(--> %s %s)' % (turn_id, d))
    if shift > 0.4:
        lines.append('(--> %s high-positive-shift)' % turn_id)
    elif shift < -0.4:
        lines.append('(--> %s high-negative-shift)' % turn_id)
    return '\n'.join(lines)

if __name__ == '__main__':
    lex = load_lexicon()
    text = sys.argv[1] if len(sys.argv) > 1 else 'I am frustrated and stuck'
    tid = sys.argv[2] if len(sys.argv) > 2 else 'turn-live'
    words, hits, vad = extract_vad(text, lex)
    print(to_metta(tid, words, hits, vad))
    print('\n;; %d words, %d hits, VAD=(%.3f, %.3f, %.3f)' % (len(words), len(hits), vad[0], vad[1], vad[2]))
