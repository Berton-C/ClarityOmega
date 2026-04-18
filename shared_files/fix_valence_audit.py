import sys
sys.path.insert(0, '/tmp')
import chromadb

# Fix: collection is at /tmp/chroma_db not /tmp/chromadb_vad
client = chromadb.PersistentClient(path='/tmp/chroma_db')
col = client.get_collection('nrc_vad_full')

# Test lookup
for w in ['notice', 'wonder', 'must', 'wrong', 'gentle']:
    res = col.get(where={'word': w}, include=['metadatas'])
    if res['metadatas']:
        m = res['metadatas'][0]
        print(f'{w}: V={m["valence"]:.3f} A={m["arousal"]:.3f} D={m["dominance"]:.3f}')
    else:
        print(f'{w}: NOT FOUND')

print('\nPath confirmed: /tmp/chroma_db with nrc_vad_full')
