# Novelty Threshold Algorithm

## Core Question
How does the system detect that queries to a memory cluster are returning diminishing novelty?

## Approach: Semantic Distance Tracking
1. For each query, measure semantic distance between query and top-K results
2. Track running average of distances over last N queries to same cluster
3. When average distance drops below threshold T, cluster is depleted
4. T is adaptive — starts generous, tightens as cluster matures

## Metric: Novelty Score
Novelty(query, results) = mean(cosine_distance(query_embedding, result_embedding)) * diversity(results)
Where diversity = mean pairwise distance among top-K results
High novelty = results are distant from query AND diverse among themselves
Low novelty = results cluster tightly around query = well-mined territory

## Depletion Trigger
If Novelty < T for M consecutive queries: flag cluster as depleted
Generate frontier queries: combine cluster centroid terms with terms from highest-novelty recent results in OTHER clusters

## MeTTa Integration Possibility
Store cluster health as MeTTa atoms:
(--> cluster-economic-analysis (health-score 0.3))
(--> cluster-mycelial-architecture (health-score 0.8))
Use NAL revision to update health scores as new queries arrive
Depletion rules fire automatically via pattern matching
