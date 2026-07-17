#!/usr/bin/env python3
"""ChromaDB Live Bridge for VAD Lookup
Queries nrc_vad_full collection for any word, returns discretized VAD cell.
Usable standalone or importable as a module for MeTTa integration."""
import chromadb
import sys

DB_PATH = '/tmp/chroma_db'
COLLECTION = 'nrc_vad_full'

def get_client():
    return chromadb.PersistentClient(path=DB_PATH)

def lookup_word(word, collection=None):
    if collection is None:
        client = get_client()
        collection = client.get_collection(COLLECTION)
    results = collection.get(where={'word': word}, include=['metadatas'])
    if not results['ids']:
        return None
    m = results['metadatas'][0]
    return float(m['valence']), float(m['arousal']), float(m['dominance'])

def discretize(val):
    if val < -0.33:
        return 'neg' if True else 'low'
    elif val > 0.33:
        return 'pos' if True else 'high'
    return 'mid'

def discretize_vad(v, a, d):
    vl = 'neg' if v < -0.33 else ('pos' if v > 0.33 else 'mid')
    al = 'low' if a < -0.33 else ('high' if a > 0.33 else 'mid')
    dl = 'low' if d < -0.33 else ('high' if d > 0.33 else 'mid')
    return vl, al, dl

def to_metta_atom(word, vl, al, dl):
    return '(= (vad-cell %s) (VADCell %s %s %s))' % (word, vl, al, dl)

def bridge(word):
    result = lookup_word(word)
    if result is None:
        return None
    v, a, d = result
    vl, al, dl = discretize_vad(v, a, d)
    return {'word': word, 'v': v, 'a': a, 'd': d,
            'cell': (vl, al, dl), 'metta': to_metta_atom(word, vl, al, dl)}

if __name__ == '__main__':
    words = sys.argv[1:] if len(sys.argv) > 1 else ['happy', 'angry', 'peaceful', 'terrified', 'love']
    client = get_client()
    coll = client.get_collection(COLLECTION)
    for w in words:
        r = lookup_word(w, coll)
        if r:
            v, a, d = r
            vl, al, dl = discretize_vad(v, a, d)
            print('%s: V=%.3f A=%.3f D=%.3f -> cell=(%s,%s,%s) -> %s' % (w, v, a, d, vl, al, dl, to_metta_atom(w, vl, al, dl)))
        else:
            print('%s: NOT FOUND' % w)
