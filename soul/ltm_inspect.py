import chromadb
import json

client = chromadb.PersistentClient(path='/PeTTa/repos/omegaclaw/volumes/omegaclaw/chroma_db')
cols = client.list_collections()
for c in cols:
    print(f'Collection: {c.name}, Count: {c.count()}')

mem_col = client.get_collection('memories')
results = mem_col.get(include=['documents', 'metadatas'], limit=20)
for i, (doc, meta) in enumerate(zip(results['documents'], results['metadatas'])):
    print(f'--- Entry {i} ---')
    print(f'ID: {results["ids"][i]}')
    print(f'Meta: {meta}')
    print(f'Doc: {doc[:200]}')
