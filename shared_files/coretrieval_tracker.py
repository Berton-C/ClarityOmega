import json, os
TRACKER_FILE = '/tmp/coretrieval_log.json'
LINK_THRESHOLD = 2
WINDOW = 5
def load_tracker():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE) as f: return json.load(f)
    return {'cycle': 0, 'pairs': {}, 'links': []}
def save_tracker(t):
    with open(TRACKER_FILE, 'w') as f: json.dump(t, f, indent=2)
def record(t, ids):
    t['cycle'] += 1
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            k = str(sorted([ids[i], ids[j]]))
            if k not in t['pairs']: t['pairs'][k] = []
            t['pairs'][k].append(t['cycle'])
def check(t):
    c = t['cycle']
    new = []
    ex = set(str(l['pair']) for l in t['links'])
    for k, cs in t['pairs'].items():
        recent = [x for x in cs if x > c - WINDOW]
        if len(recent) >= LINK_THRESHOLD and k not in ex:
            link = {'pair': k, 'cycle': c, 'count': len(recent)}
            new.append(link)
            t['links'].append(link)
    return new
print('=== Co-retrieval Edge Inference Sim ===')
t = load_tracker()
qs = [['g1','g2','br1'],['b1','b2','br1'],['i1','i2','n1'],['g1','g2','br1'],['b1','br1','n1'],['g2','br1','b1'],['i1','n1','g1'],['g1','g2','br1'],['b1','b2','n1'],['i1','i2','g2']]
for rids in qs:
    record(t, rids)
    nl = check(t)
    if nl:
        for l in nl: print(f'  Cycle {t["cycle"]}: LINK {l["pair"]} (count={l["count"]})')
    else:
        print(f'  Cycle {t["cycle"]}: {rids} - no new links')
print(f'Total links: {len(t["links"])}')
for l in t['links']: print(f'  {l["pair"]} at cycle {l["cycle"]}')
save_tracker(t)
