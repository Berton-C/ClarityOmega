# Quantale Composition - MeTTa Expression Generator
# Goal 22: Extend beyond NAL deduction/revision to full quantale algebra
# Proven pattern: inline let-chains with arithmetic (not = definitions)

def q_mul_expr(pairs):
    """Generate sequential composition MeTTa expr for list of (f,c) p-bit pairs.
    q-mul: f_out = product(f_i), c_out = product(c_i)"""
    if len(pairs) < 2:
        raise ValueError('Need at least 2 p-bits to compose')
    bindings = []
    for i, (f, c) in enumerate(pairs):
        bindings.append(f'($f{i} {f})')
        bindings.append(f'($c{i} {c})')
    # Chain multiplications
    f_expr = f'$f0'
    c_expr = f'$c0'
    for i in range(1, len(pairs)):
        prev_f = f'$sf{i-1}' if i > 1 else '$f0'
        prev_c = f'$sc{i-1}' if i > 1 else '$c0'
        bindings.append(f'($sf{i} (* {prev_f} $f{i}))')
        bindings.append(f'($sc{i} (* {prev_c} $c{i}))')
        f_expr = f'$sf{i}'
        c_expr = f'$sc{i}'
    return f'(let* ({" ".join(bindings)}) (sequential-composition (PB {f_expr} {c_expr})))'

def q_join_expr(pairs):
    """Generate parallel composition MeTTa expr. q-join: max of all f, max of all c."""
    if len(pairs) < 2:
        raise ValueError('Need at least 2 p-bits')
    bindings = []
    for i, (f, c) in enumerate(pairs):
        bindings.append(f'($f{i} {f})')
        bindings.append(f'($c{i} {c})')
    # Nested max for f and c
    def nest_max(var, n):
        if n == 1:
            return f'${var}0'
        inner = nest_max(var, n-1)
        return f'(if (> {inner} ${var}{n-1}) {inner} ${var}{n-1})'
    f_max = nest_max('f', len(pairs))
    c_max = nest_max('c', len(pairs))
    return f'(let* ({" ".join(bindings)}) (parallel-bundle (PB {f_max} {c_max})))'

def q_meet_expr(pairs):
    """Generate meet composition. q-meet: min of all f, max of all c."""
    if len(pairs) < 2:
        raise ValueError('Need at least 2 p-bits')
    bindings = []
    for i, (f, c) in enumerate(pairs):
        bindings.append(f'($f{i} {f})')
        bindings.append(f'($c{i} {c})')
    def nest_min(var, n):
        if n == 1:
            return f'${var}0'
        inner = nest_min(var, n-1)
        return f'(if (< {inner} ${var}{n-1}) {inner} ${var}{n-1})'
    def nest_max(var, n):
        if n == 1:
            return f'${var}0'
        inner = nest_max(var, n-1)
        return f'(if (> {inner} ${var}{n-1}) {inner} ${var}{n-1})'
    f_min = nest_min('f', len(pairs))
    c_max = nest_max('c', len(pairs))
    return f'(let* ({" ".join(bindings)}) (q-meet (PB {f_min} {c_max})))'

if __name__ == '__main__':
    pairs = [(0.8, 0.9), (0.7, 0.8), (0.6, 0.85)]
    print('Sequential (q-mul):')
    print(q_mul_expr(pairs))
    print()
    print('Parallel (q-join):')
    print(q_join_expr(pairs))
    print()
    print('Meet (q-meet):')
    print(q_meet_expr(pairs))
