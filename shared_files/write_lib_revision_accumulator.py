lines = [
    ';; lib_revision_accumulator.metta -- NAL evidence revision across goal cycles',
    ';; Enables cross-cycle learning by merging evidence from repeated observations',
    '',
    ';; --- Type declarations ---',
    '(: EvidenceCount Type)',
    '(: RevisionResult Type)',
    '(: nal-revision (-> Number Number Number Number RevisionResult))',
    '(: accumulate (-> Number Number Number Number RevisionResult))',
    '',
    ';; --- NAL revision: merge two truth values with evidence ---',
    ';; f_rev = (f1*c1*(1-c2) + f2*c2*(1-c1)) / (c1*(1-c2) + c2*(1-c1))',
    ';; c_rev = (c1 + c2 - c1*c2) bounded by horizon k',
    '(= (nal-revision $f1 $c1 $f2 $c2)',
    '   (let $w1 (* $c1 (- 1.0 $c2))',
    '     (let $w2 (* $c2 (- 1.0 $c1))',
    '       (let $wsum (+ $w1 $w2)',
    '         (let $f_rev (if (< $wsum 0.001) (* 0.5 (+ $f1 $f2)) (/ (+ (* $f1 $w1) (* $f2 $w2)) $wsum))',
    '           (let $c_rev (- (+ $c1 $c2) (* $c1 $c2))',
    '             (revised $f_rev $c_rev)))))))',
    '',
    ';; --- Accumulate is alias for nal-revision ---',
    '(= (accumulate $f1 $c1 $f2 $c2)',
    '   (nal-revision $f1 $c1 $f2 $c2))',
]
with open('/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_revision_accumulator.metta', 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('written', len(lines), 'lines')
