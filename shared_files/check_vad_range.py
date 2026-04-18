#!/usr/bin/env python3
import chromadb
c = chromadb.PersistentClient(path='/tmp/chroma_db')
col = c.get_collection('nrc_vad_full')
for w in ['hopeless','joy','angry','wonderful','calm','peaceful','falling','apart','cope','cannot']:
    r = col.get(where={'word': w})
    if r['ids']:
        m = r['metadatas'][0]
        print(f"{w}: V={m['valence']:.3f} A={m['arousal']:.3f} D={m['dominance']:.3f}")
    else:
        print(f"{w}: NOT FOUND")
r = col.get(limit=100)
vs = [m['valence'] for m in r['metadatas']]
ars = [m['arousal'] for m in r['metadatas']]
ds = [m['dominance'] for m in r['metadatas']]
print(f"\nSample 100 ranges:")
print(f"V: {min(vs):.3f} to {max(vs):.3f}")
print(f"A: {min(ars):.3f} to {max(ars):.3f}")
print(f"D: {min(ds):.3f} to {max(ds):.3f}")
