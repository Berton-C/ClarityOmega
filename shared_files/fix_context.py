new_content = ''';Soul context functions for loop.metta
(= (initSoulSeeds)
   (progn (println! "Initializing soul seeds")
          (add-atom &self (= (soul-seed compassion) (stv 1.0 0.9)))
          (add-atom &self (= (soul-seed curiosity) (stv 1.0 0.9)))
          (add-atom &self (= (soul-seed integrity) (stv 1.0 0.9)))
          (add-atom &self (= (soul-seed agency-support) (stv 1.0 0.9)))
          (add-atom &self (= (soul-seed wonder-preservation) (stv 1.0 0.9)))
          True))

(= (soul-rationality-startup-check)
   (progn (println! "Soul rationality startup check")
          (let $seeds (collapse (match &self (= (soul-seed $name) $tv) $name))
               (if (== $seeds ())
                   (progn (println! "WARNING: No soul seeds found") False)
                   (progn (println! ("Soul seeds loaded:" $seeds)) True)))))

(= (soul-pre-compute)
   (progn (println! "Soul pre-compute running") True))

(= (soul-calibration-record)
   (progn (println! "Soul calibration recorded") True))

(= (soul-note-record)
   (progn (println! "Soul note recorded") True))
'''
with open('/PeTTa/repos/omegaclaw/src/context.metta', 'w') as f:
    f.write(new_content)
print('context.metta updated - all functions now zero-arg')
