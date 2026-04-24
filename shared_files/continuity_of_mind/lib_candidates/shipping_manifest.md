# ClarityClaw Shipping Manifest -- Autonomous Cycles 3520-3529
## Date: 2026-04-24
## Context: Build pause lifted by Berton at cycle 3520

### Deliverable 1: soul/soul_utils.metta (Cycle 3524)
- Goal: replace-stub-with-live-chromadb-query
- What: Created soul_utils.metta with live py-call wiring to helper.py
- Stubs replaced: soul-pre-compute, soul-calibration-confidence
- Status: SHIPPED

### Deliverable 2: lib_candidates/calibration_bridge.py (Cycle 3527)
- Goal: implement-actual-calibration-logging
- What: Python bridge writing calibration events to ChromaDB soul_calibration collection
- Functions: log_calibration_event(), get_calibration_count()
- Status: SHIPPED

### Deliverable 3: lib_candidates/calibration_logger_v2.metta (Cycle 3528)
- Goal: implement-actual-calibration-logging
- What: Dual-backend logger writing to BOTH AtomSpace AND ChromaDB
- Supersedes: calibration_logger.metta (AtomSpace-only)
- Status: SHIPPED

### Full Pipeline Data Flow:
log-calibration-event -> AtomSpace counters + ChromaDB write -> soul-calibration-confidence reads ChromaDB via helper.py -> returns STRONG/ADEQUATE/WEAK/INSUFFICIENT-DATA

### In Progress:
- Goal 3: self-map auto-updater (medium-term)
- Known limitation: metta skill cannot parse nested parentheses, no metta CLI available

### Honest Assessment:
- py-call wiring in .metta files is syntactically correct but UNTESTED at runtime
- All files are candidates awaiting Berton review and integration into production
- The calibration system needs actual layer1/layer2 disagreement detection to generate real events
