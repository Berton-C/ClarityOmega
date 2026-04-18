# Spreading Activation Findings 2025-04-15

## Tested
Toy 8-memory network, 3 domains, bridge nodes.
Flat cosine vs graph spreading activation.

## Results
- Cross-domain memories promoted into top-5 that flat missed
- Bridge scores amplified 2.5x
- b1 nutrient transport: below top-5 to rank 4
- n1 emergent coordination: promoted to rank 5

## Key Insight
Value is CORPUS-DEPENDENT.
Helps most for implicit connections never explicitly stated.
Helps less when bridges already in memory text.

## Open Questions
1. Automatic edge inference without manual annotation
2. Optimal decay and step count
3. Scaling with corpus size
4. Co-retrieval frequency as edge weight

## NAL confidence: stv 0.721 0.8
