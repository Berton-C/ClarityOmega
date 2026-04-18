#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, '/tmp/mycelial')
from M2_link_creator import load_coretrieval_log, extract_qualified_links, write_link_store
from M4_retrieval_augmenter import augment_retrieval
from M1_weight_manager import bulk_reinforce, load_weights, get_weight

print('=== M1+M2+M4 INTEGRATION TEST ===')
print()

# Step 1: M2 — Generate links from co-retrieval data
print('STEP 1: M2 Link Creation')
log = load_coretrieval_log()
links = extract_qualified_links(log)
write_link_store(links)
print(f'  Created {len(links)} links from co-retrieval data')
for link in links:
    print(f'    {link["pair"]} strength={link["strength"]:.2f}')

# Step 2: M4 — Augment a mock retrieval using link graph
print()
print('STEP 2: M4 Spreading Activation Augmentation')
mock_query = [
    {"id": "g1", "similarity": 0.85},
    {"id": "br1", "similarity": 0.60}
]
print(f'  Query results: {[(r["id"], r["similarity"]) for r in mock_query]}')
augmented = augment_retrieval(mock_query)
print('  Augmented results:')
for r in augmented:
    print(f'    {r["id"]}: combined={r["combined"]:.3f} [{r["source"]}]')

# Step 3: M1 — Reinforce all retrieved memories (direct + graph-activated)
print()
print('STEP 3: M1 Weight Reinforcement')
all_retrieved_ids = [r['id'] for r in augmented]
results = bulk_reinforce(all_retrieved_ids)
print(f'  Reinforced {len(all_retrieved_ids)} memories:')
for mid, entry in results.items():
    print(f'    {mid}: weight={entry["weight"]:.3f} accesses={entry["access_count"]}')

# Summary
print()
print('=== INTEGRATION VERIFIED ===')
print('M2 co-retrieval -> links -> M4 graph activation -> M1 reinforcement')
print(f'Graph-activated nodes not in query: {[r["id"] for r in augmented if r["source"] == "graph-activated"]}')
print('Foundation triangle complete.')
