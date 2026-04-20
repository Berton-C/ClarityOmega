lines = [
    ';; lib_meta_inference.metta -- Chain router output into NAL |- calls',
    ';; Given two premises, route to correct inference mode then execute',
    '',
    ';; --- Type declarations ---',
    '(: meta-infer (-> Atom Atom Atom))',
    '',
    ';; --- Term extractor ---',
    '(= (get-term ($term (stv $f $c))) $term)',
    '',
    ';; --- Dispatch by mode ---',
    '(= (dispatch (mode deduction $A $C) $P1 $P2) (|- $P1 $P2))',
    '(= (dispatch (mode revision $A $B) $P1 $P2) (|- $P1 $P2))',
    '(= (dispatch (mode abduction $B $C) $P1 $P2) (|- $P1 $P2))',
    '(= (dispatch (mode induction $A $B) $P1 $P2) (|- $P1 $P2))',
    '(= (dispatch (mode unknown $X $Y) $P1 $P2) (no-inference $X $Y))',
]
with open('/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_meta_inference.metta', 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('written', len(lines), 'lines')
