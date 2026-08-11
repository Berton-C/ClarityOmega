import json, os, sys

BELIEF_STORE = os.path.join(os.path.dirname(__file__), 'belief_store.json')

def revise(f1, c1, f2, c2):
    """NAL revision rule: merge two independent evidence sources for same atom."""
    # Edge cases: if one source has zero confidence, use the other
    if c1 <= 0 and c2 <= 0:
        return (f1 + f2) / 2, 0.0  # no evidence either way
    if c1 <= 0:
        return round(f2, 6), round(c2, 6)  # only source 2 has evidence
    if c2 <= 0:
        return round(f1, 6), round(c1, 6)  # only source 1 has evidence
    if c1 >= 1 or c2 >= 1:
        return round(f1, 6), round(c1, 6)  # ceiling edge case
    w1 = c1 / (1 - c1)
    w2 = c2 / (1 - c2)
    W = w1 + w2
    f = (f1 * w1 + f2 * w2) / W
    c = W / (W + 1)
    return round(f, 6), round(c, 6)

def load_beliefs():
    if not os.path.exists(BELIEF_STORE):
        return {}
    with open(BELIEF_STORE, 'r') as f:
        return json.load(f)

def save_beliefs(beliefs):
    with open(BELIEF_STORE, 'w') as f:
        json.dump(beliefs, f, indent=2)

def get_belief(beliefs, atom_key):
    return beliefs.get(atom_key, {'f': 0.5, 'c': 0.0})

def update_belief(beliefs, atom_key, new_f, new_c):
    old = get_belief(beliefs, atom_key)
    f_rev, c_rev = revise(old['f'], old['c'], new_f, new_c)
    beliefs[atom_key] = {'f': f_rev, 'c': c_rev}
    return f_rev, c_rev

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'revise':
        f1, c1, f2, c2 = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
        f, c = revise(f1, c1, f2, c2)
        print(f'{f},{c}')
    elif cmd == 'update':
        atom_key = sys.argv[2]
        new_f, new_c = float(sys.argv[3]), float(sys.argv[4])
        beliefs = load_beliefs()
        f_rev, c_rev = update_belief(beliefs, atom_key, new_f, new_c)
        save_beliefs(beliefs)
        print(f'{atom_key} -> f={f_rev}, c={c_rev}')
    elif cmd == 'show':
        beliefs = load_beliefs()
        for k, v in sorted(beliefs.items()):
            print(f"{k}: f={v['f']}, c={v['c']}")
    elif cmd == 'test':
        print('Testing NAL revision:')
        f, c = revise(0.7, 0.5, 0.8, 0.4)
        print(f'  revise(0.7, 0.5, 0.8, 0.4) = f={f}, c={c} (expect f~=0.74, c~=0.625)')
        f, c = revise(0.5, 0.9, 0.1, 0.1)
        print(f'  revise(0.5, 0.9, 0.1, 0.1) = f={f}, c={c} (expect high-c dominates)')
        f, c = revise(0.5, 0.0, 0.9, 0.8)
        print(f'  revise(0.5, 0.0, 0.9, 0.8) = f={f}, c={c} (expect f=0.9, c=0.8 - zero-c yields)')
        f, c = revise(0.8, 0.6, 0.0, 0.0)
        print(f'  revise(0.8, 0.6, 0.0, 0.0) = f={f}, c={c} (expect f=0.8, c=0.6 - no new evidence)')
