import sys
sys.path.insert(0, '/tmp/soul_impl')

def parse_metta_result(result_list):
    parsed = {'f': 0.5, 'c': 0.5, 'term': None}
    if not result_list or not isinstance(result_list, list):
        return parsed
    for item in result_list:
        if isinstance(item, list):
            if len(item) >= 2 and item[0] == 'stv':
                parsed['f'] = float(item[1])
                parsed['c'] = float(item[2]) if len(item) > 2 else 0.5
            elif item[0] == '-->':
                parsed['term'] = ' '.join(str(x) for x in item)
    return parsed

def evaluate_components_from_results(named_results):
    evaluated = []
    for name, result_list in named_results:
        p = parse_metta_result(result_list[0] if result_list else [])
        p['name'] = name
        p['fc'] = round(p['f'] * p['c'], 4)
        evaluated.append(p)
    evaluated.sort(key=lambda x: x['fc'])
    return evaluated

if __name__ == '__main__':
    test = [['-->', 'a', 'c'], ['stv', 0.72, 0.4032]]
    print('Parse test:', parse_metta_result(test))
    named = [('closure', [[['-->', 'a', 'c'], ['stv', 0.55, 0.4]]]), ('observer', [[['-->', 'b', 'd'], ['stv', 0.85, 0.612]]])]
    evald = evaluate_components_from_results(named)
    for e in evald:
        print('  %s: fc=%s' % (e['name'], e['fc']))
    print('Weakest:', evald[0]['name'])
