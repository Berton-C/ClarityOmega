import re
from metta_compass_real import tokenize_for_compass, generate_deduction_exprs, generate_revision_expr
from stv_parser import parse_stv_results, extract_deduction_result
from compass_gate import compass_gate

def compass_evaluate(text, metta_fn):
    hits = tokenize_for_compass(text)
    if not hits:
        return {'pass': True, 'flags': [], 'scores': {}, 'note': 'no compass tokens found'}
    deduction_exprs = generate_deduction_exprs(hits)
    dim_stvs = {}
    for dim, word, expr in deduction_exprs:
        raw = metta_fn(expr)
        stv = extract_deduction_result(raw)
        if dim not in dim_stvs:
            dim_stvs[dim] = []
        dim_stvs[dim].append(stv)
    final_scores = {}
    for dim, stvs in dim_stvs.items():
        if len(stvs) == 1:
            final_scores[dim] = stvs[0]
        else:
            current = stvs[0]
            for i in range(1, len(stvs)):
                rev_expr = generate_revision_expr(dim, (current['f'], current['c']), (stvs[i]['f'], stvs[i]['c']))
                raw = metta_fn(rev_expr)
                current = extract_deduction_result(raw)
            final_scores[dim] = current
    return compass_gate(final_scores)

if __name__ == '__main__':
    MOCK_RESULTS = {
        'agency': '[((--> consider compass-agency) (stv 0.765 0.6561))]',
        'wonder': '[((--> fascinating compass-wonder) (stv 0.855 0.69))]',
        'thinking': '[((--> because compass-thinking) (stv 0.9 0.73))]',
        'attention': '[((--> matters compass-attention) (stv 0.765 0.62))]',
    }
    call_log = []
    def mock_metta(expr):
        call_log.append(expr)
        for dim in MOCK_RESULTS:
            if f'compass-{dim}' in expr:
                return MOCK_RESULTS[dim]
        return '[]'
    text = 'Consider your options. This is fascinating because it matters.'
    result = compass_evaluate(text, mock_metta)
    print('E2E Result:', result)
    print(f'MeTTa calls made: {len(call_log)}')
    for c in call_log:
        print(f'  {c}')
    assert result['pass'] == True
    assert 'agency' in result['scores']
    assert 'wonder' in result['scores']
    print('E2E TEST PASSED')
