import sys
sys.path.insert(0, '/tmp/soul_impl')
import epistemic_gap_detector as eg
gaps = eg.scan_gaps()
for g in gaps:
    print(g)
