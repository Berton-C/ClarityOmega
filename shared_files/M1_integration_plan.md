# M1 Runtime Integration Plan
Date: 2025-04-15

## What Exists
- Prototype: /tmp/lib_chromadb_m1.py (verified drop-in replacement)
- Design spec: /tmp/M1_retrieval_weight_design.md
- Production file: /PeTTa/repos/petta_lib_chromadb/lib_chromadb.py

## Integration Steps

### Step 1: Replace lib_chromadb.py
Copy M1 prototype over production file. Backward compatible.

### Step 2: Add reinforce skill to skills.metta
Expose reinforce as a callable skill so the loop can invoke it.
Skill signature: (reinforce item_id_in_quotes)
Maps to py-call lib_chromadb.reinforce with item_id and default boost.

### Step 3: Add reinforcement trigger to loop
After query results are used in a response, call reinforce on retrieved item IDs.
This creates the feedback loop: retrieval -> use -> reinforce -> higher future rank.

### Step 4: Add decay_all to periodic maintenance
Call decay_all once per N cycles to prevent unbounded weight growth.
Keeps weights gravitating toward baseline unless actively reinforced.

## Risk Mitigation
- Test with copy first, not production replacement
- Missing weight field defaults to 1.0 so no migration needed
- Cap on reinforce prevents runaway weights
- Decay pulls everything back toward baseline over time

## Next After Integration
- Monitor weight distribution over time
- Tune boost, cap, and decay parameters based on observed behavior
- Connect to M2 co-retrieval tracking for richer signal
