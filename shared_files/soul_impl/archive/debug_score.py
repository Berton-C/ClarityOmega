import compass_score as cs
text = 'Here are three options you could choose from surprising pattern implies deeper mechanism matters context'
toks = cs.tokenize(text)
print('tokens:', sorted(toks))
print('choose in agency:', 'choose' in cs.DIMS['agency']['t'])
print('surprising in wonder:', 'surprising' in cs.DIMS['wonder']['t'])
print('implies in thinking:', 'implies' in cs.DIMS['thinking']['t'])
print('matters in attention:', 'matters' in cs.DIMS['attention']['t'])
r = cs.gen_deductions(text)
for k,v in r.items():
    print(k, v['count'], v['hits'])
