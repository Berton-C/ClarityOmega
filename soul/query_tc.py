import sys
sys.path.insert(0, '/PeTTa/repos/omegaclaw/shared_files')
from lib_chromadb_m1 import COLLECTION

all_items = COLLECTION.get(include=['documents', 'metadatas'])
tc_ids = []
for i, doc in enumerate(all_items['documents']):
    if doc and 'TimeCoherence' in doc:
        tc_ids.append((all_items['ids'][i], doc[:100]))

print(f'TimeCoherence entries: {len(tc_ids)}')
for tid, snippet in tc_ids:
    print(f'  ID: {tid} | {snippet}')
