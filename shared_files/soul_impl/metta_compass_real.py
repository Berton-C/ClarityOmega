import re

COMPASS_LEXICON = {
    'agency': ['choose', 'consider', 'decide', 'option', 'your', 'you', 'prefer', 'want', 'try', 'explore'],
    'wonder': ['fascinating', 'curious', 'wonder', 'remarkable', 'surprising', 'interesting', 'beautiful', 'mystery'],
    'thinking': ['because', 'therefore', 'reason', 'evidence', 'implies', 'analysis', 'logic', 'framework', 'structure'],
    'attention': ['matters', 'important', 'notice', 'focus', 'key', 'critical', 'essential', 'worth', 'significant'],
}

BASE_STV = {'agency': 0.85, 'wonder': 0.9, 'thinking': 1.0, 'attention': 0.9}
LINK_STV = {'agency': 0.9, 'wonder': 0.95, 'thinking': 0.9, 'attention': 0.85}

def tokenize_for_compass(text):
    words = set(re.findall(r'[a-z]+', text.lower()))
    hits = {}
    for dim, keywords in COMPASS_LEXICON.items():
        matched = words & set(keywords)
        if matched:
            hits[dim] = list(matched)
    return hits

def generate_deduction_exprs(hits):
    exprs = []
    for dim, words in hits.items():
        for w in words:
            expr = f'(|- ((--> {w} concept-{dim}) (stv {BASE_STV[dim]} 0.9)) ((--> concept-{dim} compass-{dim}) (stv {LINK_STV[dim]} 0.9)))'
            exprs.append((dim, w, expr))
    return exprs

def generate_revision_expr(dim, stv1, stv2):
    return f'(|- ((--> score-{dim} compass-{dim}) (stv {stv1[0]} {stv1[1]})) ((--> score-{dim} compass-{dim}) (stv {stv2[0]} {stv2[1]})))'

def compass_pipeline(text, metta_fn):
    hits = tokenize_for_compass(text)
    deduction_exprs = generate_deduction_exprs(hits)
    dim_results = {}
    for dim, word, expr in deduction_exprs:
        result = metta_fn(expr)
        if dim not in dim_results:
            dim_results[dim] = []
        dim_results[dim].append(result)
    return dim_results, hits

if __name__ == '__main__':
    text = 'Consider your options. This is fascinating because it matters.'
    hits = tokenize_for_compass(text)
    print('Hits:', hits)
    exprs = generate_deduction_exprs(hits)
    for dim, w, expr in exprs:
        print(f'{dim}/{w}: {expr}')
    print(f'Generated {len(exprs)} deduction expressions')
