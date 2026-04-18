#!/usr/bin/env python3
import chromadb, time

lexicon_path = '/tmp/NRC_VAD_Lexicon_v2.1/NRC-VAD-Lexicon-v2.1.txt'
client = chromadb.PersistentClient(path='/tmp/chroma_db')

try:
    client.delete_collection('nrc_vad_full')
    print('Deleted old collection')
except:
    print('No old collection to delete')

collection = client.create_collection('nrc_vad_full', metadata={'hnsw:space': 'l2'})
print('Created collection')

words = []
embeddings = []
metadatas = []
ids = []

with open(lexicon_path) as f:
    f.readline()
    for idx, line in enumerate(f):
        parts = line.strip().split('\t')
        if len(parts) >= 4:
            word = parts[0].strip()
            try:
                v = float(parts[1]) * 2 - 1
                a = float(parts[2]) * 2 - 1
                d = float(parts[3]) * 2 - 1
            except ValueError:
                continue
            safe_id = 'w_%d' % idx
            words.append(word)
            embeddings.append([v, a, d])
            metadatas.append({'word': word, 'valence': v, 'arousal': a, 'dominance': d})
            ids.append(safe_id)

print('Parsed %d words' % len(words))
total_start = time.time()
batch = 500
for i in range(0, len(words), batch):
    end = min(i + batch, len(words))
    t0 = time.time()
    collection.add(embeddings=embeddings[i:end], metadatas=metadatas[i:end], ids=ids[i:end])
    dt = time.time() - t0
    print('Batch %d-%d done in %.2fs (total %.1fs)' % (i, end, dt, time.time()-total_start))

print('DONE. Total: %d entries in %.1fs' % (collection.count(), time.time()-total_start))
