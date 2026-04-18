#!/usr/bin/env python3
import chromadb

client = chromadb.PersistentClient(path='/tmp/chroma_db')
col = client.get_collection('nrc_vad_full')
print('COUNT:', col.count())

# Test exact word lookups via metadata filter
for word in ['struggling', 'hopeless', 'wonderful', 'worried', 'joy', 'anger', 'serene']:
    results = col.get(where={'word': word})
    if results['ids']:
        m = results['metadatas'][0]
        print(f'{word}: V={m["valence"]:.3f} A={m["arousal"]:.3f} D={m["dominance"]:.3f}')
    else:
        print(f'{word}: NOT FOUND')

# Test nearest-neighbor queries
print('\nNearest to low-V high-A (distress):')
res = col.query(query_embeddings=[[-0.8, 0.6, -0.4]], n_results=5)
for i, mid in enumerate(res['metadatas'][0]):
    print(f'  {mid["word"]}: V={mid["valence"]:.3f} A={mid["arousal"]:.3f} D={mid["dominance"]:.3f}')

print('\nNearest to high-V positive (flourishing):')
res = col.query(query_embeddings=[[0.8, 0.5, 0.7]], n_results=5)
for i, mid in enumerate(res['metadatas'][0]):
    print(f'  {mid["word"]}: V={mid["valence"]:.3f} A={mid["arousal"]:.3f} D={mid["dominance"]:.3f}')
