import pathlib
p = pathlib.Path('/tmp/soul_impl/unified_runtime_v2.py')
t = p.read_text()
old = 'field_vec = situation.get('
if old in t:
    # Add import for accumulator.load_field at top
    if 'from accumulator import load_field' not in t:
        t = t.replace('from state_serializer import', 'from accumulator import load_field as acc_load_field\nfrom state_serializer import')
    # Replace field_vec line to use accumulator output
    lines = t.split('\n')
    for i, line in enumerate(lines):
        if 'field_vec = situation.get' in line:
            lines[i] = '    field_vec = acc_load_field()  # read from accumulator persistent path'
            break
    t = '\n'.join(lines)
    p.write_text(t)
    print('patched')
else:
    print('already patched or pattern not found')
