from clus import *
R2 = [('importúne: árgue', 'importúne: Argue'), ('opus fac evangelístæ', 'opus fac Evangelístæ'), ('judex: non solum', 'judex: Non solum')]
R5 = [('prophétas: non veni', 'prophétas: Non veni'), ('cælórum: qui autem', 'cælórum: Qui autem')]
w2 = "as printed: 'importúne : Argue', 'opus fac Evangelístæ', 'justus judex : Non solum' (seen on the scan)"
w5 = "as printed: 'prophétas : Non veni', 'cælórum : Qui autem' (seen on the scan)"
s = 'M39 pp. 20*-21* (pdf 378), Comm. Doctorum (In medio)'
canon_entry('C35s', 0, R2, s, w2); canon_entry('C35s', 1, R5, s, w5)
for k in ('S0114', 'S0127', 'S0129', 'S0209', 'S0223', 'S1124'):
    canon_entry(k, 0, R2, s, 'Commune copy (2 Tim. 4: 1-8, p. 20*): ' + w2)
    canon_entry(k, 1, R5, s, 'Commune copy (Matth. 5: 13-19, p. 21*): ' + w5)
own = {'S1204': 'M39 p. 330 (pdf 204)', 'S1207': 'M39 p. 330 (pdf 204)', 'S0312': 'M39 pp. 394-395 (pdf 236-237)', 'S1231': 'M39 p. 349 (pdf 213)'}
for k, p in own.items(): canon_entry(k, 0, R2, p, 'own print (same text as the Commune p. 20*): ' + w2)
own5 = {'S0123': 'M39 p. 361 (pdf 219)', 'S0307': 'M39 p. 392 (pdf 235)', 'S1204': 'M39 p. 330 (pdf 204)', 'S1207': 'M39 p. 330 (pdf 204)', 'S0312': 'M39 p. 395 (pdf 237)', 'S1115': 'M39 p. 622 (pdf 350)'}
for k, p in own5.items(): canon_entry(k, 1, R5, p, 'own print (same text as the Commune p. 21*): ' + w5)
