#!/usr/bin/env python3
import sys
import time
sys.path.insert(0, '/tmp/soul_impl')
from accumulator import load_field, save_field, q_join_fields
from field_decay import apply_decay, load_meta, save_meta

def accumulate_with_decay(vad, signals):
    meta = load_meta()
    elapsed = time.time() - meta.get('last_decay', time.time())
    decay_steps = max(1, int(elapsed / 60))
    field = load_field()
    if field is None:
        field = [[0.5,0.5]]*9
    field = apply_decay(field, steps=decay_steps)
    v = vad.get('valence',0.5)
    a = vad.get('arousal',0.5)
    d = vad.get('dominance',0.5)
    rd = signals.get('relational_depth',0.5)
    sm = signals.get('shift_magnitude',0.3)
    ss = signals.get('shift_source',0.5)
    do = signals.get('domain_ontological',0.5)
    dt = signals.get('domain_technical',0.5)
    de = signals.get('domain_emotional',0.5)
    new_vec = [[v,0.9],[a,0.9],[d,0.9],[rd,0.9],[sm,0.9],[ss,0.9],[do,0.9],[dt,0.9],[de,0.9]]
    merged = q_join_fields(field, new_vec)
    save_field(merged)
    meta['last_decay'] = time.time()
    meta['exchanges'] = meta.get('exchanges',0) + 1
    save_meta(meta)
    return merged, 'decayed_and_accumulated'

if __name__ == '__main__':
    seed = [[0.95,0.9]]*9
    save_field(seed)
    save_meta({'last_decay': time.time()-3600, 'exchanges': 10})
    vad = {'valence':0.7,'arousal':0.5,'dominance':0.6}
    sig = {'relational_depth':0.8,'shift_magnitude':0.3,'shift_source':0.5,'domain_ontological':0.6,'domain_technical':0.4,'domain_emotional':0.7}
    result, status = accumulate_with_decay(vad, sig)
    print('Status:', status)
    for i,d in enumerate(result):
        print(f'  dim{i}: {d[0]:.4f} conf={d[1]:.4f}')
