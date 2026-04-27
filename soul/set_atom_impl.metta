;; set-atom! implementation for PeTTa
;; Source: Patrick Hammer, 2026-04-27
;; PeTTa does not have native set-atom!, this implements it via remove+add

(: set-atom! (-> Atom Expression Expression Atom))
(= (set-atom! $space $atom1 $atom2)
   (progn (remove-atom $space $atom1)
          (add-atom $space $atom2)))
