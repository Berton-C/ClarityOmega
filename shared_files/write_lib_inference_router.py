lines = [
    ';; lib_inference_router.metta -- Dispatch inference by input structure',
    ';; Routes to deduction, revision, or abduction based on premise patterns',
    '',
    ';; --- Type declarations ---',
    '(: InferenceMode Type)',
    '(: route-inference (-> Atom Atom InferenceMode))',
    '',
    ';; --- Routing logic ---',
    ';; Two inheritance premises with shared middle term -> deduction',
    '(= (route-inference (--> $A $B) (--> $B $C)) (mode deduction $A $C))',
    '',
    ';; Two premises with same term -> revision',
    '(= (route-inference (--> $A $B) (--> $A $B)) (mode revision $A $B))',
    '',
    ';; Two inheritance premises with shared subject -> abduction',
    '(= (route-inference (--> $A $B) (--> $A $C)) (mode abduction $B $C))',
    '',
    ';; Two inheritance premises with shared predicate -> induction',
    '(= (route-inference (--> $A $C) (--> $B $C)) (mode induction $A $B))',
    '',
    ';; Fallback for unrecognized patterns',
    '(= (route-inference $X $Y) (mode unknown $X $Y))',
]
with open('/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_inference_router.metta', 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('written', len(lines), 'lines')
