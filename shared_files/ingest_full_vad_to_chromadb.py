#!/usr/bin/env python3
import chromadb

lexicon_path = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
client = chromadb.PersistentClient(path='/tmp/chroma_db')

try:
    client.delete_collection('nrc_vad_full')
except:
    pass

collection = client.create_collection('nrc_vad_full', metadata={'hnsw:space': 'l2'})

words = []
embeddings = []
metadatas = []
ids = []
skipped = 0

with open(lexicon_path) as f:
    header = f.readline()
    for idx, line in enumerate(f):
        parts = line.strip().split('\t')
        if len(parts) >= 4:
            word = parts[0].strip()
            try:
                v = float(parts[1]) * 2 - 1
                a = float(parts[2]) * 2 - 1
                d = float(parts[3]) * 2 - 1
            except ValueError:
                skipped += 1
                continue
            safe_id = 'w_%d_%s' % (idx, word.replace(' ', '_')[:40])
            words.append(word)
            embeddings.append([v, a, d])
            metadatas.append({'word': word, 'valence': v, 'arousal': a, 'dominance': d})
            ids.append(safe_id)

print('Parsed %d words, skipped %d' % (len(words), skipped))

batch = 5000
for i in range(0, len(words), batch):
    end = min(i + batch, len(words))
    collection.add(embeddings=embeddings[i:end], metadatas=metadatas[i:end], ids=ids[i:end])
    print('Ingested %d-%d of %d' % (i, end, len(words)))

print('DONE. Total entries in nrc_vad_full:', collection.count())
print('Nearest to low-valence high-arousal:', collection.query(query_embeddings=[[-0.8, 0.6, -0.4]], n_results=5))
print('Nearest to high-valence positive:', collection.query(query_embeddings=[[0.8, 0.5, 0.7]], n_results=5))
