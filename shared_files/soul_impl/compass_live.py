import compass_score as cs
import sys
import json

def score_text(text):
    deds = cs.gen_deductions(text)
    revs = cs.gen_revisions(deds)
    result = {}
    for dn in deds:
        d = deds[dn]
        if d['count'] == 0:
            result[dn] = dict(score=0.0, conf=0.0, hits=0, tokens=[])
        elif d['count'] == 1:
            tok = d['deductions'][0]['tok']
            f = d['deductions'][0]['freq']
            c = f * 0.81
            result[dn] = dict(score=round(f,3), conf=round(c,3), hits=1, tokens=d['hits'])
        else:
            fs = [dd['freq'] for dd in d['deductions']]
            cs_vals = [f * 0.81 for f in fs]
            rev_f = sum(f*c for f,c in zip(fs,cs_vals)) / sum(cs_vals) if sum(cs_vals) > 0 else 0
            rev_c = min(0.99, sum(cs_vals))
            result[dn] = dict(score=round(rev_f,3), conf=round(rev_c,3), hits=d['count'], tokens=d['hits'])
    return result

if __name__ == '__main__':
    text = sys.argv[1] if len(sys.argv) > 1 else 'You might consider exploring this fascinating pattern because it matters'
    scores = score_text(text)
    print('=== COMPASS READING ===')
    for dn, s in scores.items():
        bar = '#' * int(s['score'] * 20)
        print(f"  {dn:12s} {s['score']:.2f} (c={s['conf']:.2f}) [{s['hits']} hits: {s['tokens']}] {bar}")
    composite = sum(s['score'] * s['conf'] for s in scores.values()) / max(sum(s['conf'] for s in scores.values()), 0.01)
    print(f"\n  COMPOSITE: {composite:.3f}")
