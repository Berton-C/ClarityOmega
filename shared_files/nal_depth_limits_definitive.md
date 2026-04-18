# NAL Inference Depth Limits - Definitive
## Date: 2026-04-18
## Based on empirical backbone reasoning sessions 1-4

### Hard Rules
- Unrevised chains: 3-4 hops max useful
- Revised chains: 4-5 hops max
- Below conf 0.1: noise, discard
- Below conf 0.2: speculative, flag clearly
- Above conf 0.3: actionable with caveats
- Above conf 0.5: reliable for decisions

### Key Finding
Starting premise strength matters MORE than chain length.
Revision at base accumulates evidence, slowing degradation.
Insert evidence checkpoints every 2-3 hops.
