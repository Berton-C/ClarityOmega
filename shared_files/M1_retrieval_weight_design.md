# M1 Retrieval-Weight Reinforcement: Implementation Design
Date: 2025-04-15

## Current State
lib_chromadb.py at /PeTTa/repos/petta_lib_chromadb/lib_chromadb.py
Metadata: only time field stored
query() returns time and content - distances discarded
query_with_ids() gets distances but does not use them for ranking

## Proposed Changes

### 1. Add weight field to metadata on remember()
Default weight 1.0 for all new memories

### 2. Add reinforce() function
Reads current weight from metadata, adds boost of 0.1, updates via collection.update()
Called after successful retrieval used in a response

### 3. Add weighted re-ranking to query_with_ids()
Compute effective_score = similarity * weight then re-sort

### 4. Decay mechanism
Optional: weight = weight * 0.99 per cycle without retrieval

## Migration
Existing memories default missing weight to 1.0
No breaking changes to existing API

## Files to Modify
- lib_chromadb.py: add weight to remember, add reinforce, modify query_with_ids
- memory.metta: add reinforce skill binding
- skills.metta: expose reinforce as available skill

## Risk Assessment
- Low risk: metadata extension is backward compatible
- ChromaDB supports metadata updates natively
- Re-ranking preserves original similarity as base signal
