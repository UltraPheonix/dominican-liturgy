from clus import *
reps10 = [('sanctórum: honestávit', 'sanctórum: Honestávit'), ('eum: descendítque', 'eum: Descendítque'), ('deprimébant: et mendáces', 'deprimébant: Et mendáces')]
w = "capitals after the colon as printed: 'sanctórum : Honestávit', 'liberávit eum : Descendítque', 'deprimébant : Et mendáces' (seen on the scan)"
canon_entry('C18s', 0, reps10, 'M39 p. 10* (pdf 373)', w)
for k in ('S0327', 'G446'): canon_entry(k, 0, reps10, 'M39 p. 405 (pdf 241)', 'own print p. 405 (= Commune p. 10*): ' + w)
canon_entry('C18s', 1, [('terram: non veni', 'terram: Non veni'), ('perdet illam: et qui', 'perdet illam: Et qui'), ('me récipit: et qui', 'me récipit: Et qui'), ('accípiet: et qui', 'accípiet: Et qui')],
            'M39 p. 11* (pdf 373)', "capitals after the colon as printed: 'terram : Non veni', 'perdet illam : Et qui', 'me récipit : Et qui', 'prophétæ accípiet : Et qui' ('discípuli : amen dico' lower case, as printed; seen on the scan)")
