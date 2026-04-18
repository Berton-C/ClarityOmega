import re
import json
import sys

DIMS = dict(
  agency=dict(c='agency-concept', p='compass-agency',
    t=dict(choose=1.0,option=1.0,decide=0.95,prefer=0.95,freedom=0.9,autonomy=0.95,empower=0.9,consider=0.85,alternative=0.9,possibility=0.85,perspective=0.8,approach=0.75,might=0.7,could=0.7,perhaps=0.65,suggest=0.7)),
  wonder=dict(c='wonder-concept', p='compass-wonder',
    t=dict(surprising=1.0,unexpected=1.0,curious=0.95,fascinating=0.95,remarkable=0.9,wonder=1.0,mystery=0.9,explore=0.85,discover=0.9,puzzle=0.85,intriguing=0.95,novel=0.85,deeper=0.8,pattern=0.8,emerge=0.8,question=0.75,open=0.7)),
  thinking=dict(c='thinking-concept', p='compass-thinking',
    t=dict(because=1.0,therefore=1.0,implies=0.95,evidence=0.95,reasoning=1.0,mechanism=0.9,causal=0.95,framework=0.85,structure=0.8,analyze=0.9,nuance=0.9,however=0.8,although=0.8,depends=0.75,context=0.8)),
  attention=dict(c='attention-concept', p='compass-attention',
    t=dict(matters=1.0,important=0.95,priority=0.9,focus=0.9,essential=0.9,relevant=0.85,specifically=0.85,directly=0.8,honest=0.9,transparent=0.85,concise=0.8,actionable=0.85,practical=0.8,concrete=0.8,core=0.8,substance=0.85))
)

def tokenize(text):
    return set(re.findall('[a-z]+', text.lower()))

def gen_plan(text):
    toks = tokenize(text)
    plan = dict(deductions=[], dim_hits={})
    for dn, d in DIMS.items():
        hits = toks & set(d['t'].keys())
        for tok in hits:
            f = d['t'][tok]
            expr = '(|- ((--> %s %s) (stv %s 0.9)) ((--> %s %s) (stv 1.0 0.9)))' % (tok, d['c'], f, d['c'], d['p'])
            plan['deductions'].append(dict(dim=dn, tok=tok, expr=expr))
        plan['dim_hits'][dn] = dict(hits=list(hits), n=len(hits))
    return plan

if __name__ == '__main__':
    test = 'You might consider exploring this fascinating pattern because it matters'
    p = gen_plan(test)
    print('Deductions: %d' % len(p['deductions']))
    for d in p['deductions']:
        print('  [%s] %s: %s' % (d['dim'], d['tok'], d['expr']))
    print(json.dumps(p['dim_hits'], indent=2))
