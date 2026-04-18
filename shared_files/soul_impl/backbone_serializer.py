#!/usr/bin/env python3
import json, os

BACKBONE_PATH = '/tmp/soul_impl/persistent_state/backbone_params.json'

def save_backbone(pq):
    data = {
        'tensor_strength': list(pq.tensor_strength),
        'join_breadth': list(pq.join_breadth),
        'meet_floor': list(pq.meet_floor),
        'alignment_coupling': list(pq.alignment_coupling)
    }
    os.makedirs(os.path.dirname(BACKBONE_PATH), exist_ok=True)
    with open(BACKBONE_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    return data

def load_backbone(pq):
    if not os.path.exists(BACKBONE_PATH):
        return False
    with open(BACKBONE_PATH) as f:
        data = json.load(f)
    for key in ['tensor_strength', 'join_breadth', 'meet_floor', 'alignment_coupling']:
        if key in data:
            setattr(pq, key, tuple(data[key]))
    return True

def backbone_exists():
    return os.path.exists(BACKBONE_PATH)
