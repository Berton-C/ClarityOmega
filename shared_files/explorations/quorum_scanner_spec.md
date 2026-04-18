# Quorum Scanner: Formal Specification
Date: 2025-04-15

## What NAL revision already handles
- Evidence accumulation on known statements
- Confidence update via truth value revision
- Threshold detection on single terms

## What the quorum scanner uniquely provides

### 1. Cross-statement clustering detection
Input: set of memories retrieved by broad theme query
Operation: measure embedding-space density of result set
Output: boolean — cluster detected above threshold
This is a GEOMETRIC operation on vectors, not a logical one.
NAL operates on symbolic terms. Clustering operates on embeddings.
These are complementary, not redundant.

### 2. Abductive synthesis generation
Input: clustered memory set identified by step 1
Operation: generate new statement capturing shared pattern
Output: synthesis-memory with provenance links to sources
This is CREATIVE — producing a new term not present in inputs.
NAL deduction and induction derive from existing terms.
Abduction proposes new explanatory terms. Different operation.

## Minimal quorum scanner algorithm
1. Select broad theme from recent activity
2. Query memories by theme
3. Compute pairwise embedding distances in result set
4. If mean distance below threshold AND count above minimum
5. Generate synthesis prompt from clustered memories
6. Store synthesis as new memory with source references
7. Apply NAL revision to update confidence on synthesis theme