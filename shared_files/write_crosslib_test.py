lines = [
    ';; cross_lib_test.metta -- Integration test across ClarityClaw libs',
    ';; Tests composition of quantale, web_detect, paraconsistent, and NAL ops',
    '',
    ';; TEST 1: Revision produces stronger evidence',
    '!(assertEqual (|- ((--> bird fly) (stv 0.8 0.5)) ((--> bird fly) (stv 0.7 0.5))) revised-bird-fly)',
    '',
    ';; TEST 2: Deduction chains two implications',
    '!(assertEqual (|- ((--> bird fly) (stv 0.9 0.9)) ((--> fly motion) (stv 0.8 0.9))) deduced-bird-motion)',
    '',
    ';; TEST 3: Quantale meet takes minimum confidence floor',
    ';; (q-meet (stv 0.9 0.8) (stv 0.7 0.5)) should yield (stv 0.7 0.5)',
    '',
    ';; TEST 4: Paraconsistent held-pair preserves tension',
    ';; (held-pair safety helpfulness) should not collapse either side',
    '',
    ';; TEST 5: Web detect convergence pattern',
    ';; (converge? (==> rain wet) (==> sprinkler wet)) should find convergence on wet',
    '',
    ';; TEST 6: Observer relativity humility discount',
    ';; (humility-discount (stv 0.9 0.8) 0.7) should reduce confidence to 0.56',
]
with open('/PeTTa/repos/omegaclaw/lib_clarity_reasoning/cross_lib_test.metta', 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('written', len(lines), 'lines')
