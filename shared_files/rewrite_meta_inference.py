import os
path = '/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_meta_inference.metta'
content = ';; lib_meta_inference.metta -- Direct NAL calls\n'
content += ';; |- does not reduce through let*-defined wrappers\n'
content += '\n'
content += '(= (get-term ($term (stv $f $c))) $term)\n'
content += '\n'
content += '(= (meta-infer $P1 $P2)\n'
content += '   (let $result (|- $P1 $P2) $result))\n'
with open(path, 'w') as f:\n    f.write(content)
print('done')
