import chromadb
import json

# Try the volumes DB first
for path in ['./volumes/omegaclaw/chroma_db', './shared_files/chroma_db']:
    try:
        client = chromadb.PersistentClient(path=path)
        coll = client.get_collection('memories')
        count = coll.count()
        print(f'Path: {path}, Count: {count}')
        # Query TimeCoherence entries
        results = coll.get(where={'category': {'$eq': 'TimeCoherence'}}, include=['documents','metadatas'])
        print(f'TimeCoherence entries: {len(results["ids"])}')
        for i in range(min(10, len(results['ids']))):
            doc_preview = results['documents'][i][:100] if results['documents'][i] else 'None'
            print(f'  id={results["ids"][i]}, doc={doc_preview}')
    except Exception as e:
        print(f'Path: {path}, Error: {e}')
