import re
import sys

DIMS = dict(
  agency=dict(c='agency-concept', p='compass-agency',
    t=dict(choose=1.0,option=1.0,decide=0.95,prefer=0.95,freedom=0.9,autonomy=0.95,empower=0.9,consider=0.85,alternative=0.9,possibility=0.85,perspective=0.8,approach=0.75,might=0.7,could=0.7,perhaps=0.65,suggest=0.7,attempt=0.65,explore=0.8,your=0.6,you=0.55)),
  wonder=dict(c='wonder-concept', p='compass-wonder',
    t=dict(surprising=1.0,unexpected=1.0,curious=0.95,fascinating=0.95,remarkable=0.9,wonder=1.0,mystery=0.9,explore=0.85,discover=0.9,puzzle=0.85,intriguing=0.95,novel=0.85,deeper=0.8,pattern=0.8,patterns=0.8,emerge=0.8,question=0.75,open=0.7,notice=0.75,interesting=0.9,what=0.5)),
  thinking=dict(c='thinking-concept', p='compass-thinking',
    t=dict(because=1.0,therefore=1.0,implies=0.95,evidence=0.95,reasoning=1.0,mechanism=0.9,causal=0.95,framework=0.85,frameworks=0.85,structure=0.8,analyze=0.9,nuance=0.9,however=0.8,although=0.8,depends=0.75,context=0.8,think=0.85,thinking=0.85,reason=0.9,why=0.8,how=0.7,whether=0.75,changes=0.65,problem=0.7,answer=0.6,understand=0.85,logic=0.9,argument=0.85,claim=0.8,assumption=0.85,distinction=0.9,compare=0.8)),
  attention=dict(c='attention-concept', p='compass-attention',
    t=dict(matters=1.0,important=0.95,priority=0.9,focus=0.9,essential=0.9,relevant=0.85,specifically=0.85,directly=0.8,honest=0.9,transparent=0.85,concise=0.8,actionable=0.85,practical=0.8,concrete=0.8,core=0.8,substance=0.85,key=0.8,here=0.5,rather=0.6,just=0.5,worth=0.75,clear=0.8,note=0.7,actually=0.65,precisely=0.85,brief=0.75))
)

def tokenize(text):
    return set(re.findall('[a-z]+', text.lower()))

def gen_deductions(text):
    toks = tokenize(text)
    result = {}
    for dn, d in DIMS.items():
        hits = toks & set(d['t'].keys())
        deductions = []
        for tok in sorted(hits):
            f = d['t'][tok]
            deductions.append(dict(tok=tok, freq=f,
                expr='(|- ((--> %s %s) (stv %s 0.9)) ((--> %s %s) (stv 1.0 0.9)))' % (tok, d['c'], f, d['c'], d['p'])))
        result[dn] = dict(hits=sorted(hits), count=len(hits), deductions=deductions)
    return result

def gen_revisions(deduced_results):
    revisions = {}
    for dn, data in deduced_results.items():
        if len(data['deductions']) < 2:
            revisions[dn] = None
            continue
        pairs = []
        deds = data['deductions']
        for i in range(1, len(deds)):
            acc_f = deds[0]['freq']
            acc_c = acc_f * 0.81
            nxt_f = deds[i]['freq']
            nxt_c = nxt_f * 0.81
            expr = '(|- ((--> %s compass-%s) (stv %s %s)) ((--> %s compass-%s) (stv %s %s)))' % (deds[0]['tok'], dn, acc_f, round(acc_c,4), deds[i]['tok'], dn, nxt_f, round(nxt_c,4))
            pairs.append(expr)
        revisions[dn] = pairs
    return revisions

if __name__ == '__main__':
    text = sys.argv[1] if len(sys.argv) > 1 else 'You might consider exploring this fascinating pattern because it matters and is important for practical context'
    deds = gen_deductions(text)
    revs = gen_revisions(deds)
    print('=== COMPASS SCORING ===')
    for dn in deds:
        print('[%s] %d hits: %s' % (dn, deds[dn]['count'], deds[dn]['hits']))
