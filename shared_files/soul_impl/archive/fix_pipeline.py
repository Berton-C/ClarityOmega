import pathlib
p = pathlib.Path('/tmp/soul_impl/felt_sense_pipeline_v3.py')
t = p.read_text()
t = t.replace('from accumulator_v2 import accumulate_with_decay', 'from accumulator import accumulate_exchange')
t = t.replace('accumulate_with_decay(vad_scores, signals)', 'accumulate_exchange(vad_scores, signals)')
p.write_text(t)
print('patched')
