# M2 Co-Retrieval Pipeline Integration Design
Date: 2025-04-15

## Current State
- M2 prototype: /tmp/coretrieval_tracker.py (verified working)
- Tracks which memories are retrieved together
- Builds co-retrieval frequency graph
- Infers associative edges from usage patterns

## Integration Architecture

### Hook Point
After query_with_ids returns results in lib_chromadb.py:
1. Pass returned item IDs to co-retrieval tracker
2. Tracker updates pairwise co-occurrence counts
3. When count exceeds threshold, edge is inferred

### Query Augmentation
When a query returns item A and A has strong M2 edges to B and C:
1. Fetch B and C even if they scored below similarity threshold
2. Include them as associative retrievals tagged differently
3. Let the LLM see both similarity-matched and association-matched results

### Data Flow
query_embedding -> ChromaDB similarity -> M1 weight re-rank -> top k results
                                                                    |
                                                              M2 tracker update
                                                                    |
                                                         M2 edge lookup for top results
                                                                    |
                                                         augmented result set -> LLM

## Implementation Steps
1. Add co_retrieval_update call after query_with_ids in lib_chromadb_m1.py
2. Add associative_fetch function that takes IDs and returns linked memories
3. Modify query to return both similarity and associative results
4. Store co-retrieval graph in persistent file or separate ChromaDB collection

## Parameters
- co_retrieval_threshold: 3 (min co-occurrences to infer edge)
- max_associative_augment: 3 (max extra results from M2)
- edge_decay: 0.9 per 100 cycles without co-retrieval
