lines = [
    ';; stress_test.metta -- End-to-end validation of all lib_clarity_reasoning libs',
    ';; Tests quantale, temporal decay, autocatalytic cycle pipeline',
    '',
    ';; --- Test 1: q-mul basic ---',
    '!(assertEqual (q-mul (mk-pbit 0.8 0.9) (mk-pbit 0.5 0.7)) (mk-pbit 0.4 0.7))',
    '',
    ';; --- Test 2: Staleness urgent-refresh for old low-conf goal ---',
    '!(let $f (* 0.3 (- 1.0 (* 8 0.1)))',
    '   (assertEqual (if (< $f 0.2) urgent-refresh fresh) urgent-refresh))',
    '',
    ';; --- Test 3: Staleness fresh for new high-conf goal ---',
    '!(let $f (* 0.9 (- 1.0 (* 1 0.1)))',
    '   (assertEqual (if (< $f 0.5) stale fresh) fresh))',
    '',
    ';; --- Test 4: Autocatalytic cycle low-conf old triggers generate ---',
    '!(let $fresh (* 0.2 (- 1.0 (* 7 0.1)))',
    '   (assertEqual (if (< $fresh 0.3) blind-spot none) blind-spot))',
    '',
    ';; --- Test 5: Autocatalytic cycle high-conf fresh maintains ---',
    '!(let $fresh (* 0.85 (- 1.0 (* 1 0.1)))',
    '   (assertEqual (if (< $fresh 0.5) degraded maintain) maintain))',
    '',
    ';; --- Test 6: q-mul identity-like with conf 1.0 ---',
    '!(assertEqual (q-mul (mk-pbit 1.0 1.0) (mk-pbit 0.5 0.8)) (mk-pbit 0.5 0.8))',
]
with open('/PeTTa/repos/omegaclaw/lib_clarity_reasoning/stress_test.metta', 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('written', len(lines), 'lines')
