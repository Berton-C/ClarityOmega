# Deep Chain Confidence Degradation Analysis
## Date: 2026-04-19

### Degradation Pattern
- Per-hop confidence decay factor: ~0.65
- 2 hops: conf ~0.46 (actionable)
- 4 hops: conf ~0.21 (speculative)
- 6 hops: conf ~0.09 (blind spot)
- 8 hops: conf ~0.04 (deep blind spot)

### Implications
1. Beliefs requiring >6 inferential steps ALWAYS need independent evidence injection
2. Analogical transfer becomes essential beyond hop 4
3. Gap detection of deep chains has compound degradation: detector conf * chain conf
4. Periodic reanchoring with direct evidence needed every 3-4 hops

### Reanchoring Strategy
- At hop 3-4: inject analogical evidence via revision
- At hop 5-6: require direct evidence or multiple analogical sources
- Beyond hop 6: treat as hypothesis only, not working belief

### Dashboard Update
- New category: DEEP BLIND SPOTS (chains >6 hops without reanchoring)
- Reanchoring intervals formalized as substrate maintenance protocol
