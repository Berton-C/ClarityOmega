import re
import sys

DIMS = {
  'agency': {'c': 'agency-concept', 'p': 'compass-agency', 's': 'score-agency', 't': {'choose':1.0,'option':1.0,'decide':0.95,'prefer':0.95,'freedom':0.9,'autonomy':0.95,'empower':0.9,'consider':0.85,'alternative':0.9,'possibility':0.85,'perspective':0.8,'approach':0.75,'might':0.7,'could':0.7,'perhaps':0.65,'suggest':0.7,'attempt':0.65,'explore':0.8,'your':0.6,'you':0.55}},
  'wonder': {'c': 'wonder-concept', 'p': 'compass-wonder', 's': 'score-wonder', 't': {'surprising':1.0,'unexpected':1.0,'curious':0.95,'fascinating':0.95,'remarkable':0.9,'wonder':1.0,'mystery':0.9,'discover':0.9,'puzzle':0.85,'intriguing':0.95,'novel':0.85,'deeper':0.8,'pattern':0.8,'patterns':0.8,'emerge':0.8,'question':0.75,'open':0.7,'notice':0.75,'interesting':0.9,'what':0.5}},
  'thinking': {'c': 'thinking-concept', 'p': 'compass-thinking', 's': 'score-thinking', 't': {'because':1.0,'therefore':1.0,'implies':0.95,'evidence':0.95,'reasoning':1.0,'mechanism':0.9,'causal':0.95,'framework':0.85,'structure':0.8,'analyze':0.9,'nuance':0.9,'however':0.8,'although':0.8,'depends':0.75,'context':0.8,'think':0.85,'reason':0.9,'why':0.8,'how':0.7,'whether':0.75,'problem':0.7,'understand':0.85,'logic':0.9,'argument':0.85,'claim':0.8,'assumption':0.85,'distinction':0.9,'compare':0.8}},
  'attention': {'c': 'attention-concept', 'p': 'compass-attention', 's': 'score-attention', 't': {'matters':1.0,'important':0.95,'priority':0.9,'focus':0.9,'essential':0.9,'relevant':0.85,'specifically':0.85,'directly':0.8,'honest':0.9,'transparent':0.85,'concise':0.8,'actionable':0.85,'practical':0.8,'concrete':0.8,'core':0.8,'substance':0.85,'key':0.8,'worth':0.75,'clear':0.8,'note':0.7,'actually':0.65,'precisely':0.85,'brief':0.75}}
}

def tokenize(text):
    return set(re.findall(r'[a-z]+', text.lower()))

def gen_metta_calls(text):
    toks = tokenize(text)
    calls = {'deduce': [], 'revise': []}
    for dn, d in DIMS.items():
        hits = sorted(toks & set(d['t'].keys()))
        for tok in hits:
            f = d['t'][tok]
            expr = '(|- ((--> %s %s) (stv %s 0.9)) ((--> %s %s) (stv 1.0 0.9)))' % (tok, d['c'], f, d['c'], d['p'])
            calls['deduce'].append({'dim': dn, 'tok': tok, 'expr': expr})
        if len(hits) >= 2:
            st = d['s']
            first = '(|- ((--> %s %s) (stv %s 0.81)) ((--> %s %s) (stv %s 0.81)))' % (st, d['p'], d['t'][hits[0]], st, d['p'], d['t'][hits[1]])
            calls['revise'].append({'dim': dn, 'expr': first})
            for i in range(2, len(hits)):
                nxt = '(|- ((--> %s %s) (stv 0.9 0.9)) ((--> %s %s) (stv %s 0.81)))' % (st, d['p'], st, d['p'], d['t'][hits[i]])
                calls['revise'].append({'dim': dn, 'expr': nxt})
    return calls

if __name__ == '__main__':
    text = sys.argv[1] if len(sys.argv) > 1 else 'You might consider this fascinating pattern because it matters'
    calls = gen_metta_calls(text)
    print('=== DEDUCTIONS (%d) ===' % len(calls['deduce']))
    for c in calls['deduce']:
        print('  [%s] %s' % (c['dim'], c['expr']))
    print('=== REVISIONS (%d) ===' % len(calls['revise']))
    for c in calls['revise']:
        print('  [%s] %s' % (c['dim'], c['expr']))
