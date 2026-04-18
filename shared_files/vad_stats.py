import chromadb
c = chromadb.PersistentClient(path='/tmp/chroma_db')
col = c.get_collection('nrc_vad_full')
res = col.get(limit=500, include=['metadatas'])
vals = [m['valence'] for m in res['metadatas']]
vals.sort()
n = len(vals)
print(f'n={n}')
print(f'min={min(vals):.3f} max={max(vals):.3f} mean={sum(vals)/n:.3f}')
print(f'median={vals[n//2]:.3f} q25={vals[n//4]:.3f} q75={vals[3*n//4]:.3f}')
# Check specific PNS/SNS words
for w in ['notice','wonder','gentle','open','curious','must','wrong','fix','urgent','problem']:
    r = col.get(where={'word': w}, include=['metadatas'])
    if r['metadatas']:
        m = r['metadatas'][0]
        print(f'  {w}: v={m["valence"]:.3f} a={m["arousal"]:.3f} d={m["dominance"]:.3f}')
    else:
        print(f'  {w}: NOT FOUND')
