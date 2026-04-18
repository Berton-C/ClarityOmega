import re

def parse_stv_results(metta_output):
    pattern = r'stv\s+([0-9.]+)\s+([0-9.]+)'
    matches = re.findall(pattern, str(metta_output))
    results = []
    for f_str, c_str in matches:
        results.append({'f': round(float(f_str), 4), 'c': round(float(c_str), 4)})
    return results

def extract_deduction_result(metta_output):
    results = parse_stv_results(metta_output)
    for r in results:
        if r['c'] > 0.5:
            return r
    return results[0] if results else {'f': 0.0, 'c': 0.0}

if __name__ == '__main__':
    test1 = '[((--> consider compass-agency) (stv 0.765 0.6561000000000001)), ((--> compass-agency consider) (stv 0.85 0.4481160000000001))]'
    test2 = '[((--> score-agency compass-agency) (stv 0.713 0.726))]'
    r1 = parse_stv_results(test1)
    print('Parse test1:', r1)
    assert len(r1) == 2
    assert r1[0]['f'] == 0.765
    r2 = extract_deduction_result(test1)
    print('Extract test1:', r2)
    assert r2['f'] == 0.765
    r3 = extract_deduction_result(test2)
    print('Extract test2:', r3)
    assert r3['f'] == 0.713
    print('ALL PARSER TESTS PASSED')
