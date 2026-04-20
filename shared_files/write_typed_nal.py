import os
os.makedirs('/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_candidates', exist_ok=True)
content = '; ; lib_nal_extended.metta -- Typed Extensions to Patrick lib_nal\n'
content += '; ; Types as contracts, reductions as computation.\n'
content += '; ; Uses stv pattern matching Patrick exactly.\n\n'
content += '(: confidence-band (-> Atom Atom))\n'
content += '(: belief-strength (-> Atom Number))\n'
content += '(: epistemic-distance (-> Atom Atom Number))\n'
content += '(: frame-shift (-> Atom Number Atom))\n'
content += '(: revision-delta (-> Atom Atom Atom))\n\n'
content += '(= (confidence-band (stv $f $c))\n'
content += '   (if (< $c 0.15) blind-spot\n'
content += '   (if (< $c 0.4) weak\n'
content += '   (if (< $c 0.7) moderate\n'
content += '   (if (< $c 0.9) strong\n'
content += '       established)))))\n\n'
content += '(= (belief-strength (stv $f $c))\n'
content += '   (* $f $c))\n\n'
content += '(= (epistemic-distance (stv $f1 $c1) (stv $f2 $c2))\n'
content += '   (+ (abs (- $f1 $f2)) (abs (- $c1 $c2))))\n\n'
content += '(= (frame-shift (stv $f $c) $cs)\n'
content += '   (Truth_Revision (stv $f $c) (stv 0.0 $cs)))\n\n'
content += '(= (revision-delta (stv $f1 $c1) (stv $f2 $c2))\n'
content += '   (let (stv $fr $cr) (Truth_Revision (stv $f1 $c1) (stv $f2 $c2))\n'
content += '        (stv (abs (- $f1 $fr)) (- $cr $c1))))\n'
with open('/PeTTa/repos/omegaclaw/lib_clarity_reasoning/lib_candidates/lib_nal_extended.metta', 'w') as f:
    f.write(content)
print('written', len(content.splitlines()), 'lines')
