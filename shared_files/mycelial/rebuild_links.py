#!/usr/bin/env python3
import json

links = [
    {"pair": ["g1","g2"], "strength": 0.5, "formed": 4},
    {"pair": ["br1","g1"], "strength": 0.5, "formed": 4},
    {"pair": ["br1","g2"], "strength": 0.5, "formed": 4},
    {"pair": ["b1","br1"], "strength": 0.5, "formed": 5},
    {"pair": ["m1","g1"], "strength": 0.3, "formed": 10},
    {"pair": ["m1","m2"], "strength": 0.3, "formed": 11},
    {"pair": ["m2","m3"], "strength": 0.3, "formed": 12},
    {"pair": ["e1","e2"], "strength": 0.3, "formed": 13}
]
with open("/tmp/mycelial/link_store.json", "w") as f:
    json.dump({"links": links}, f, indent=2)
print("Rebuilt link_store with", len(links), "links")